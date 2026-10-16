#!/usr/bin/env python3
"""Read text and cell coordinates from an .xlsx using only Python stdlib.

Usage: python scripts/xlsx_view.py BD.xlsx --list
       python scripts/xlsx_view.py BD.xlsx --sheet イベント定義
This prints to stdout and does not create another task output file.
"""

import argparse
import posixpath
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def text_nodes(node):
    if node is None:
        return ""
    parts = []
    for child in node:
        if child.tag == f"{{{MAIN}}}t":
            parts.append(child.text or "")
        elif child.tag == f"{{{MAIN}}}r":
            run_text = child.find(f"{{{MAIN}}}t")
            if run_text is not None:
                parts.append(run_text.text or "")
    return "".join(parts)


def read_book(path):
    archive = ZipFile(path)
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels.findall(f"{{{REL_PKG}}}Relationship")}
    shared = []
    if "xl/sharedStrings.xml" in archive.namelist():
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        shared = [text_nodes(si) for si in root.findall(f"{{{MAIN}}}si")]
    sheets = []
    for sheet in workbook.findall(f"{{{MAIN}}}sheets/{{{MAIN}}}sheet"):
        rid = sheet.attrib[f"{{{REL_DOC}}}id"]
        target = targets[rid]
        member = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
        sheets.append((sheet.attrib["name"], member))
    return archive, shared, sheets


def cell_value(cell, shared):
    kind = cell.attrib.get("t")
    if kind == "inlineStr":
        inline = cell.find(f"{{{MAIN}}}is")
        return text_nodes(inline) if inline is not None else ""
    value = cell.find(f"{{{MAIN}}}v")
    if value is not None and value.text is not None:
        if kind == "s":
            idx = int(value.text)
            return shared[idx] if idx < len(shared) else f"[bad shared string {idx}]"
        return value.text
    formula = cell.find(f"{{{MAIN}}}f")
    return f"[FORMULA: {formula.text or ''}]" if formula is not None else ""


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Inspect .xlsx sheet names or cell text with coordinates")
    parser.add_argument("file", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true")
    group.add_argument("--sheet")
    parser.add_argument("--max-rows", type=int, default=300)
    args = parser.parse_args()
    if not args.file.is_file():
        parser.error(f"File does not exist: {args.file}")
    archive, shared, sheets = read_book(args.file)
    try:
        if args.list:
            for name, _ in sheets:
                print(name)
            return
        matching = [(name, member) for name, member in sheets if name == args.sheet]
        if not matching:
            parser.error(f"Unknown sheet: {args.sheet}. Use --list to see names.")
        name, member = matching[0]
        root = ET.fromstring(archive.read(member))
        print(f"# {args.file.name} | {name}")
        rows = root.findall(f"{{{MAIN}}}sheetData/{{{MAIN}}}row")
        for row in rows[: args.max_rows]:
            values = []
            for cell in row.findall(f"{{{MAIN}}}c"):
                value = cell_value(cell, shared).replace("\r", " ").replace("\n", " / ").strip()
                if value:
                    values.append(f"{cell.attrib.get('r', '?')}={value}")
            if values:
                print(" | ".join(values))
        if len(rows) > args.max_rows:
            print(f"[Only first {args.max_rows} rows printed; set --max-rows to increase]")
    finally:
        archive.close()


if __name__ == "__main__":
    main()
