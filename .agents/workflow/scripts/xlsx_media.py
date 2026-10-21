#!/usr/bin/env python3
"""Extract layout images and text shapes from an .xlsx, grouped by sheet.

Usage: python scripts/xlsx_media.py BD.xlsx --out runs/<ID>/inputs/layout
       python scripts/xlsx_media.py BD.xlsx --out <dir> --sheet レイアウト --scale 2

For each sheet with a drawing: copies the embedded images (EMF/WMF are converted to PNG so the
agent can view them), prints the cell anchor of each picture and the text of each shape.
EMF conversion uses Pillow on Windows, falling back to PowerShell System.Drawing.
"""

import argparse
import posixpath
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
XDR = "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"


def rels(zf, part):
    rel_path = posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")
    if rel_path not in zf.namelist():
        return {}
    root = ET.fromstring(zf.read(rel_path))
    base = posixpath.dirname(part)
    return {
        r.get("Id"): posixpath.normpath(posixpath.join(base, r.get("Target")))
        for r in root.findall(f"{{{REL_PKG}}}Relationship")
    }


def sheets(zf):
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    wb_rels = rels(zf, "xl/workbook.xml")
    for s in wb.find(f"{{{MAIN}}}sheets"):
        yield s.get("name"), wb_rels[s.get(f"{{{REL_DOC}}}id")]


def col_name(idx):
    name = ""
    idx += 1
    while idx:
        idx, rem = divmod(idx - 1, 26)
        name = chr(65 + rem) + name
    return name


def anchor_text(anchor):
    frm = anchor.find(f"{{{XDR}}}from")
    to = anchor.find(f"{{{XDR}}}to")

    def cell(node):
        if node is None:
            return "?"
        c = int(node.find(f"{{{XDR}}}col").text)
        r = int(node.find(f"{{{XDR}}}row").text)
        return f"{col_name(c)}{r + 1}"

    if frm is None:
        return "absolute"
    return f"{cell(frm)}:{cell(to)}" if to is not None else cell(frm)


def convert_emf(src, dst, scale):
    try:
        from PIL import Image

        with Image.open(src) as img:
            img.load(dpi=int(96 * scale))
            img.convert("RGB").save(dst)
        return True
    except Exception:
        pass
    ps = (
        "Add-Type -AssemblyName System.Drawing;"
        f"$m=New-Object Drawing.Imaging.Metafile('{src}');"
        f"$w=[int]($m.Width*{scale});$h=[int]($m.Height*{scale});"
        "$b=New-Object Drawing.Bitmap($w,$h);$g=[Drawing.Graphics]::FromImage($b);"
        "$g.Clear([Drawing.Color]::White);$g.DrawImage($m,0,0,$w,$h);"
        f"$b.Save('{dst}',[Drawing.Imaging.ImageFormat]::Png)"
    )
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, capture_output=True)
        return Path(dst).exists()
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("xlsx")
    parser.add_argument("--out", required=True)
    parser.add_argument("--sheet", help="only this sheet name")
    parser.add_argument("--scale", type=float, default=2.0, help="EMF render scale")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    failed = 0
    with ZipFile(args.xlsx) as zf:
        for name, sheet_part in sheets(zf):
            if args.sheet and name != args.sheet:
                continue
            for drawing in rels(zf, sheet_part).values():
                if not drawing.endswith(".xml") or "/drawings/" not in drawing or drawing not in zf.namelist():
                    continue
                d_rels = rels(zf, drawing)
                root = ET.fromstring(zf.read(drawing))
                print(f"== {name} ({posixpath.basename(drawing)})")
                for anchor in root:
                    where = anchor_text(anchor)
                    for blip in anchor.iter(f"{{{A}}}blip"):
                        media = d_rels.get(blip.get(f"{{{REL_DOC}}}embed"))
                        if not media:
                            continue
                        raw = out / posixpath.basename(media)
                        raw.write_bytes(zf.read(media))
                        shown = raw
                        if raw.suffix.lower() in (".emf", ".wmf"):
                            png = raw.with_suffix(".png")
                            if convert_emf(str(raw.resolve()), str(png.resolve()), args.scale):
                                shown = png
                                raw.unlink()
                            else:
                                failed += 1
                                shown = f"{raw} (CONVERT FAILED - ask user for a screenshot)"
                        print(f"  IMAGE {where}: {shown}")
                    texts = [
                        "".join(t.text or "" for t in p.iter(f"{{{A}}}t"))
                        for p in anchor.iter(f"{{{A}}}p")
                    ]
                    texts = [t for t in texts if t.strip()]
                    if texts:
                        print(f"  SHAPE {where}: {' / '.join(texts)}")
    if failed:
        sys.exit(2)


if __name__ == "__main__":
    main()
