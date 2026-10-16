#!/usr/bin/env python3
"""Validate versioned Markdown workflows; review points G0-G6 are confirmed by the user in chat, not recorded here."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FLOW = json.loads((ROOT / "config/workflow.json").read_text(encoding="utf-8"))
STEPS = FLOW["steps"]
sys.path.insert(0, str(ROOT / "scripts"))
import quality


class WorkflowError(Exception):
    pass


def workflow(task):
    version = task["kit_version"]
    if version == FLOW["kit_version"]:
        return FLOW
    raise WorkflowError(f"Unsupported kit version: {version}; do not silently migrate")


def review_point(task, step_id):
    steps = workflow(task)["steps"]
    for index, step in enumerate(steps):
        if step["id"] == step_id and step.get("gate"):
            following = steps[index + 1]["id"] if index + 1 < len(steps) else None
            tail = f"; then continue {following}" if following else ""
            return f"review point {step['gate']}: user confirms in chat{tail}"
    return None


def field(body, label):
    found = re.search(r"^\|\s*" + re.escape(label) + r"\s*\|\s*(.*?)\s*\|\s*$", body, re.M)
    if not found or not found.group(1).strip():
        raise WorkflowError(f"Missing task.md field: {label}")
    return found.group(1).strip().strip("`")


def load(task_dir):
    path = task_dir / "task.md"
    if not path.is_file():
        raise WorkflowError(f"Missing {path}; run init")
    body = path.read_text(encoding="utf-8")
    task = {"function_id": field(body, "Function ID"), "bd_path": field(body, "BD path"),
            "kit_version": field(body, "Kit version")}
    workflow(task)
    bd = Path(task["bd_path"])
    if not bd.is_absolute():
        bd = task_dir / bd
    if not bd.is_file():
        raise WorkflowError("BD missing at the path recorded in task.md; stop and start a new reviewed run")
    if (task_dir / "source-manifest.md").exists():
        try:
            sources = quality.manifest(task_dir, "source-manifest.md")
            if not any((Path(row["Path"]) if Path(row["Path"]).is_absolute() else task_dir / row["Path"]).resolve() == bd.resolve()
                       for row in sources.values()):
                raise WorkflowError("source-manifest.md must include the BD recorded in task.md")
        except quality.QualityError as exc:
            raise WorkflowError(f"Source manifest problem: {exc}") from exc
    return task


def issues(task_dir, task, step):
    found = []
    for name in step["outputs"]:
        path = task_dir / name
        if not path.is_file():
            found.append(f"{name}: missing")
            continue
        body = path.read_text(encoding="utf-8").strip()
        if len(body) < 120 or not body.startswith("#") or task["function_id"] not in body:
            found.append(f"{name}: incomplete Markdown or Function ID missing")
        elif name in {"pg-guide.md", "DD.md"} and "[SRC:" not in body:
            found.append(f"{name}: source reference missing")
        elif "<Function ID>" in body or "{{" in body:
            found.append(f"{name}: template placeholder remains")
    if not found:
        found.extend(quality.problems(task_dir, task, step))
    return found


def next_action(task_dir, task):
    steps = workflow(task)["steps"]
    for step in steps:
        problems = issues(task_dir, task, step)
        if problems:
            return "step", step["id"], step["skill"], problems
    return "complete", steps[-1]["id"], "Product accepted with human review and C1+C2 evidence", []


def init(args):
    dest, bd = Path(args.task_dir).resolve(), Path(args.bd).resolve()
    if not bd.is_file() or bd.suffix.lower() != ".xlsx":
        raise WorkflowError("--bd must be an existing .xlsx")
    # Skill 01 saves the BD into runs/<ID>/inputs/ before init; only that folder may pre-exist.
    if dest.exists() and any(p.name != "inputs" for p in dest.iterdir()):
        raise WorkflowError(f"Task directory is not empty: {dest}")
    dest.mkdir(parents=True, exist_ok=True)
    # BD inside the run is recorded relative to the run so the repo can be moved/cloned.
    if bd.is_relative_to(dest):
        bd = bd.relative_to(dest).as_posix()
    scope = (args.scope or "Chờ người phụ trách chốt tại G0").replace("|", "/")
    task = f"""# Task {args.function_id}

| Mục | Giá trị |
|---|---|
| Function ID | {args.function_id} |
| Workflow step | Xem `python .agents/workflow/scripts/kit.py next`; không tự chuyển bước |
| Kit version | {FLOW['kit_version']} |
| BD path | {bd} |
| Tài liệu liên quan | Xem pg-guide.md và source-manifest.md; user đưa theo bước (SOURCE_MAP) |
| Scope | {scope} |
| Ngoài scope | Chờ người phụ trách chốt tại G0 |
| Repository / build / test | PENDING: user đưa đường dẫn repo code, branch và quyền build/test khi đến S2 |
| Dependency thật / mock | Chờ xác nhận tại G0/G3 |
| Quality target | C1 = 100%, C2 = 100% trong phạm vi hợp lệ được người review chốt; mọi case trong kế hoạch phải PASS |

## Người phụ trách

- User chốt nghiệp vụ: chưa ghi
- Dev chốt thiết kế: chưa ghi
- Reviewer UT/code: chưa ghi
- Người nghiệm thu: chưa ghi

## Ghi chú task

Hồ sơ task là Markdown theo config/workflow.json. Code và artifacts ở repo code / nơi user
chỉ định, liên kết qua manifest (đường dẫn). Điểm review G0–G6: user xác nhận trong chat; nguồn đã dùng ở
source-manifest.md; quality-plan.md (S4) ghi phạm vi kiểm thử. Agent không thao tác Git.
"""
    (dest / "task.md").write_text(task, encoding="utf-8")
    write_intake_records(dest, args.function_id, bd)
    print(f"Created {dest / 'task.md'}; next S1")


def show_next(args):
    dest = Path(args.task_dir).resolve()
    task = load(dest)
    kind, ident, detail, problems = next_action(dest, task)
    steps = workflow(task)["steps"]
    if kind == "step":
        index = next(i for i, s in enumerate(steps) if s["id"] == ident)
        if index > 0 and steps[index - 1].get("gate"):
            print(f"{steps[index - 1]['id']} READY - {review_point(task, steps[index - 1]['id'])}")
    print(f"{kind.upper()} {ident}: {detail}")
    for problem in problems:
        print(f"  - {problem}")
    if kind == "step":
        print(f"Read {ROOT / detail}")


def check(args):
    dest = Path(args.task_dir).resolve()
    task = load(dest)
    print(f"{task['function_id']} | BD present | kit {task['kit_version']}")
    for step in workflow(task)["steps"]:
        problems = issues(dest, task, step)
        print(f"{step['id']}: {'READY' if not problems else 'INCOMPLETE'}")
        for problem in problems:
            print(f"  - {problem}")
        if step.get("gate") and not problems:
            print(f"  {review_point(task, step['id'])}")
    kind, ident, _, _ = next_action(dest, task)
    print(f"Next: {kind} {ident}")
    if getattr(args, "strict", False) and kind == "step":
        raise WorkflowError(f"Current step {ident} is incomplete; strict check failed")


def write_intake_records(dest, function_id, bd):
    body = (f"# Source manifest {function_id}\n\nNguồn thực sự được dùng; bổ sung đủ nguồn (Category, Version) theo "
            "templates/source-manifest.md trước G0.\n\n## Files\n\n| ID | Path | Role | Category | Version | Used in |\n"
            f"|---|---|---|---|---|---|\n| BD01 | {bd} | BD chính | CUSTOMER | PENDING | S1 |\n")
    (dest / "source-manifest.md").write_text(body, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="SERIO versioned development workflow checker")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init")
    p.add_argument("--task-dir", required=True)
    p.add_argument("--function-id", required=True)
    p.add_argument("--bd", required=True)
    p.add_argument("--scope")
    p.set_defaults(func=init)
    for name, func in (("next", show_next), ("check", check)):
        p = sub.add_parser(name)
        p.add_argument("--task-dir", required=True)
        if name == "check":
            p.add_argument("--strict", action="store_true", help="Fail if the currently allowed step is incomplete")
        p.set_defaults(func=func)
    args = parser.parse_args()
    try:
        args.func(args)
    except (WorkflowError, OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
