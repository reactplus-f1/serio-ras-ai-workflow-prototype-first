"""Work log (作業ログ) in Excel: one shared log, one row per AI/human activity.

Two sheets: "Hiệu chỉnh workflow" (log=workflow) and "Tạo thành phẩm" (log=output, S1–S8).
IDs L-xxx are unique across both sheets.

Commands (run from repo root):
  python .agents/workflow/scripts/worklog.py template            # (re)build log/作業ログ_template.xlsx
  python .agents/workflow/scripts/worklog.py add --json entry.json   # append one activity (new L-xxx)
  python .agents/workflow/scripts/worklog.py set --id L-003 --field status --value "Thất bại"
  python .agents/workflow/scripts/worklog.py list               # print rows + minute totals

Rules: .agents/workflow/rules/WORKLOG_RULES.md (the workbook holds data only).
"""
import argparse
import json
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[3]
LOG_DIR = ROOT / "log"
LOG = LOG_DIR / "作業ログ.xlsx"
TEMPLATE = LOG_DIR / "作業ログ_template.xlsx"
# "log" key of an entry -> sheet. workflow: chỉnh workflow/quy trình/rule/skill/template/script/log.
# output: tạo/hiệu chỉnh thành phẩm S1–S8 của run (hồ sơ run, code, hướng dẫn test, môi trường test).
SHEETS = {"workflow": "Hiệu chỉnh workflow", "output": "Tạo thành phẩm"}

# (key, label) — required items, in order.
FIELDS = [
    ("time", "Ngày và thời gian thực hiện"),
    ("run_id", "Run ID"),
    ("people", "Người thực hiện"),
    ("ticket", "Ticket / nội dung công việc"),
    ("type", "Loại hoạt động"),
    ("inputs", "Tài liệu / code đầu vào"),
    ("prompt", "Yêu cầu / chỉ thị gửi AI"),
    ("tool", "Công cụ AI và model"),
    ("commands", "Lệnh đã chạy và kết quả (exit code)"),
    ("ai_result", "Kết quả ban đầu do AI tạo"),
    ("human_changes", "Nội dung người đã hiệu chỉnh / bổ sung / loại bỏ"),
    ("review", "Kết quả review và test"),
    ("status", "Trạng thái"),
    ("time_ai", "Thời gian AI xử lý (phút)"),
    ("time_review", "Thời gian review thủ công (phút)"),
    ("time_rework", "Thời gian sửa lại (phút)"),
    ("notes", "Ghi chú / vấn đề phát sinh"),
]
LABEL = dict(FIELDS)
HEADER = ["ID"] + [label for _, label in FIELDS]
MINUTES = ("time_ai", "time_review", "time_rework")
TYPES = ["Chạy bước (AI tạo mới)", "Hiệu chỉnh", "Tạo lại", "Thử thất bại", "Chỉnh workflow",
         "Chỉnh repo code / môi trường"]
STATUSES = ["Thành công", "Thất bại", "Cần thực hiện lại"]
WIDTH = {"ID": 7, "time": 17, "run_id": 24, "people": 22, "ticket": 32, "type": 18, "inputs": 45,
         "prompt": 60, "tool": 22, "commands": 55, "ai_result": 60, "human_changes": 45, "review": 40,
         "status": 16, "time_ai": 10, "time_review": 10, "time_rework": 10, "notes": 45}
FONT = "Meiryo UI"  # Vietnamese + Japanese glyphs
_side = Side(style="thin", color="A6A6A6")
BORDER = Border(left=_side, right=_side, top=_side, bottom=_side)


def _style_row(ws, r, header=False):
    for c in ws[r]:
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="center" if header else "top")
        c.font = Font(name=FONT, size=9, bold=header, color="FFFFFF" if header else None)
        if header:
            c.fill = PatternFill("solid", fgColor="1F4E78")


def build(path):
    wb = Workbook()
    wb.remove(wb.active)
    for title in SHEETS.values():
        _build_sheet(wb.create_sheet(title))
    path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)


def _build_sheet(ws):
    ws.append(HEADER)
    _style_row(ws, 1, header=True)
    ws.row_dimensions[1].height = 42
    for i, key in enumerate(["ID"] + [k for k, _ in FIELDS], start=1):
        ws.column_dimensions[ws.cell(1, i).column_letter].width = WIDTH[key]
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:{ws.cell(1, len(HEADER)).column_letter}1"
    st = ws.cell(1, HEADER.index(LABEL["status"]) + 1).column_letter
    dv = DataValidation(type="list", formula1='"' + ",".join(STATUSES) + '"', allow_blank=True,
                        showErrorMessage=False)
    dv.add(f"{st}2:{st}2000")
    ws.add_data_validation(dv)


def _book():
    if not LOG.exists():
        build(LOG)
    wb = load_workbook(LOG)
    for title in SHEETS.values():
        if title not in wb.sheetnames or [c.value for c in wb[title][1]] != HEADER:
            raise SystemExit(f"Sheet '{title}' thiếu hoặc header khác format hiện tại (xem HEADER trong worklog.py)")
    return wb


def _minutes(value):
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def _cell_value(key, value):
    if key in MINUTES and _minutes(value) is not None:
        m = _minutes(value)
        return int(m) if m == int(m) else m
    return value


def add(values):
    if values.get("log") not in SHEETS:
        raise SystemExit("log must be: " + " / ".join(f"{k} ({v})" for k, v in SHEETS.items()))
    missing = [k for k, _ in FIELDS if not str(values.get(k, "")).strip()]
    if missing:
        raise SystemExit("Missing fields: " + ", ".join(missing) + " (ghi “—” nếu không có)")
    if not any(values["status"].startswith(s) for s in STATUSES):
        raise SystemExit("status must start with: " + ", ".join(STATUSES))
    for k in MINUTES:
        if _minutes(values[k]) is None and not str(values[k]).startswith(("—", "chờ user ghi")):
            raise SystemExit(f"{k} must be minutes (number), “chờ user ghi” or “— (lý do)”")
    wb = _book()
    nums = [int(str(r[0])[2:]) for title in SHEETS.values()
            for r in wb[title].iter_rows(min_row=2, values_only=True) if str(r[0]).startswith("L-")]
    lid = f"L-{(max(nums) + 1 if nums else 1):03d}"
    ws = wb[SHEETS[values["log"]]]
    ws.append([lid] + [_cell_value(k, values[k]) for k, _ in FIELDS])
    _style_row(ws, ws.max_row)
    wb.save(LOG)
    print(f"{lid} added to {LOG.relative_to(ROOT).as_posix()} [{ws.title}]")


def set_field(lid, key, value):
    if key not in LABEL:
        raise SystemExit("field must be one of: " + ", ".join(LABEL))
    wb = _book()
    col = HEADER.index(LABEL[key]) + 1
    for title in SHEETS.values():
        ws = wb[title]
        for r in range(2, ws.max_row + 1):
            if ws.cell(r, 1).value == lid:
                ws.cell(r, col).value = _cell_value(key, value)
                wb.save(LOG)
                print(f"{lid}.{key} = {value}")
                return
    raise SystemExit(f"{lid} not found")


def entries(path=LOG):
    wb = load_workbook(path, read_only=True)
    keys = ["id"] + [k for k, _ in FIELDS]
    out = []
    for log, title in SHEETS.items():
        for r in wb[title].iter_rows(min_row=2, values_only=True):
            if r[0]:
                out.append(dict(zip(keys, ("" if v is None else str(v) for v in r)), log=log))
    return sorted(out, key=lambda e: e["id"])


def main():
    for stream in (sys.stdout, sys.stderr, sys.stdin):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("template")
    a = sub.add_parser("add"); a.add_argument("--json", required=True, help="file JSON (object hoặc list)")
    s = sub.add_parser("set"); s.add_argument("--id", required=True); s.add_argument("--field", required=True); s.add_argument("--value", required=True)
    sub.add_parser("list")
    args = ap.parse_args()
    if args.cmd == "template":
        build(TEMPLATE); print(TEMPLATE.relative_to(ROOT).as_posix())
    elif args.cmd == "add":
        data = json.loads(Path(args.json).read_text(encoding="utf-8"))
        for v in (data if isinstance(data, list) else [data]):
            add(v)
    elif args.cmd == "set":
        set_field(args.id, args.field, args.value)
    else:
        es = entries()
        for e in es:
            print(" | ".join([e["id"], e["log"], e["time"], e["run_id"], e["ticket"][:50], e["status"][:20]] + [e[k] for k in MINUTES]))
        tot = [sum(m for m in (_minutes(e[k]) for e in es) if m is not None) for k in MINUTES]
        print(f"{len(es)} entries | tổng phút AI {tot[0]:g}, review {tot[1]:g}, sửa lại {tot[2]:g} (mục “—” không tính)")


if __name__ == "__main__":
    try:
        main()
    except PermissionError as exc:
        raise SystemExit(f"Không ghi được {exc.filename}: file đang mở trong Excel — đóng file rồi chạy lại.")
