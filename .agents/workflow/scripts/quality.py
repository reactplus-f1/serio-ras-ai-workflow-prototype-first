"""Validate Markdown quality records. Does not run tests or authenticate reviewers."""
import re
from pathlib import Path


class QualityError(ValueError):
    pass


def table(body, heading, columns):
    match = re.search(r"^## " + re.escape(heading) + r"\s*\n([\s\S]*?)(?=^## |\Z)", body, re.M)
    if not match:
        raise QualityError(f"Missing section: {heading}")
    lines = [line.strip() for line in match.group(1).splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        raise QualityError(f"Missing table: {heading}")
    def cells(line):
        return [c.strip().replace(r"\|", "|") for c in re.split(r"(?<!\\)\|", line)[1:-1]]
    headers = cells(lines[0])
    if not set(columns).issubset(headers) or len(set(headers)) != len(headers):
        raise QualityError(f"{heading}: required columns {', '.join(columns)}")
    result = []
    for line in lines[2:]:
        values = cells(line)
        if not any(values):
            continue
        if len(values) != len(headers):
            raise QualityError(f"{heading}: malformed row")
        result.append(dict(zip(headers, values)))
    return result


def records(body, heading, columns, key, allow_empty=False):
    rows = table(body, heading, columns)
    if not rows and not allow_empty:
        raise QualityError(f"{heading}: no records")
    ids = [r[key] for r in rows]
    if any(not re.fullmatch(r"[A-Za-z0-9_.:-]+", ident) for ident in ids) or len(set(ids)) != len(ids):
        raise QualityError(f"{heading}: empty, invalid or duplicate {key}")
    return {r[key]: r for r in rows}


def read(dest, name):
    return (dest / name).read_text(encoding="utf-8")


def require(value, label):
    if not value or value in {"-", "PENDING", "未確定"}:
        raise QualityError(f"{label}: missing or unresolved")


def yes_no(value):
    if value not in {"YES", "NO"}:
        raise QualityError("Required must be YES or NO")


GUIDE = "pg-guide.md"


def rules(dest, name=GUIDE):
    return records(read(dest, name), "Rules", ["Rule ID", "Source", "Statement", "Required"], "Rule ID")


def review(body):
    if not re.search(r"^判定: PASS\s*$", body, re.M):
        raise QualityError("Review requires a standalone 判定: PASS")
    rows = table(body, "Finding", ["ID", "Severity", "Status", "Decision"])
    for row in rows:
        if row["Severity"] not in {"BLOCKER", "MAJOR", "MINOR"}:
            raise QualityError("Unknown finding severity")
        if row["Status"] == "CLOSED":
            require(row["Decision"], "Finding closure evidence")
        elif row["Status"] == "ACCEPTED" and row["Severity"] == "MINOR":
            require(row["Decision"], "Human decision reference")
        else:
            raise QualityError(f"Open/blocking finding: {row['ID']}")


def design(dest):
    defined = rules(dest)
    dd = rules(dest, "DD.md")
    if set(defined) != set(dd):
        raise QualityError("PG guide rules do not match DD rule IDs")
    for row in defined.values():
        yes_no(row["Required"])
        require(row["Source"], "Rule source")
        require(row["Statement"], "Rule statement")
    for ident, row in dd.items():
        if row["Required"] != defined[ident]["Required"]:
            raise QualityError(f"DD changed required status: {ident}")
        require(row["Source"], "DD source")
        require(row["Statement"], "DD expected behavior")
    return dd


def modules(dest):
    result = records(read(dest, "quality-plan.md"), "Modules",
                     ["Module ID", "Scope", "C1 method", "C2 method", "Evidence plan"], "Module ID")
    for row in result.values():
        require(row["Scope"], "Module scope")
        require(row["Evidence plan"], "Evidence plan")
        if row["C1 method"] not in {"TOOL", "MATRIX"} or row["C2 method"] not in {"TOOL", "MATRIX"}:
            raise QualityError("Coverage method must be TOOL or MATRIX, validated on actual stack")
    return result


def cases(dest):
    return records(read(dest, "ut-design.md"), "Cases",
                   ["Case ID", "Rule ID", "Precondition", "Input", "Expected", "Source", "Required"], "Case ID")


def ut_design(dest, require_dd=True):
    defined = design(dest) if require_dd else rules(dest)
    planned, scoped = cases(dest), modules(dest)
    for row in planned.values():
        if row["Rule ID"] not in defined:
            raise QualityError("UT case references unknown rule")
        yes_no(row["Required"])
        for key in ("Precondition", "Input", "Expected", "Source"):
            require(row[key], f"UT {key}")
    for ident, row in defined.items():
        if row["Required"] == "YES" and not any(c["Rule ID"] == ident and c["Required"] == "YES" for c in planned.values()):
            raise QualityError(f"Required rule has no required case: {ident}")
    atomic = records(read(dest, GUIDE), "Atomic conditions",
                     ["Condition ID", "Rule ID", "Expression", "True/False meaning", "Source"], "Condition ID", True)
    condition_plan = records(read(dest, "ut-design.md"), "Condition plan",
                             ["Condition ID", "Rule ID", "Expression", "True cases", "False cases", "Short-circuit / unresolved"],
                             "Condition ID", True)
    if not set(atomic).issubset(condition_plan):
        raise QualityError("UT condition plan is missing analyzed atomic conditions")
    for ident, row in condition_plan.items():
        if row["Rule ID"] not in defined:
            raise QualityError("Condition plan references unknown rule")
        require(row["Expression"], "Condition expression")
        if ident in atomic and any(row[key] != atomic[ident][key] for key in ("Rule ID", "Expression")):
            raise QualityError("UT plan changed an approved atomic condition")
        for key in ("True cases", "False cases"):
            ids = split_ids(row[key])
            if not ids or any(cid not in planned for cid in ids):
                raise QualityError(f"Condition plan lacks cases for {ident} {key}")
    readiness = table(read(dest, "ut-design.md"), "Readiness", ["Item", "Status", "Owner", "Evidence"])
    required_items = {"Build/test environment/data", "Tool versions/config and C1/C2 trial",
                      "Customer UT/evidence format", "Real/mock dependencies and regression scope",
                      "Independent reviewers and acceptance owner"}
    if {row["Item"] for row in readiness} != required_items or len(readiness) != len(required_items):
        raise QualityError("UT readiness is missing/duplicating required prerequisites")
    for row in readiness:
        if row["Status"] != "READY":
            raise QualityError("UT readiness has unresolved prerequisites")
        require(row["Owner"], "Readiness owner")
        require(row["Evidence"], "Readiness evidence")
    decisions = records(read(dest, "decision-table.md"), "Decisions",
                        ["Decision ID", "Rule ID", "Conditions", "Outcome", "Source"], "Decision ID", True)
    for row in decisions.values():
        if row["Rule ID"] not in defined:
            raise QualityError("Decision references unknown rule")
        for key in ("Conditions", "Outcome", "Source"):
            require(row[key], f"Decision {key}")
    return defined, planned, scoped


def metadata(dest, name):
    # Commit is optional (user commits; no SHA lock). Only read what is written.
    body = read(dest, name)
    values = {}
    for label in ("Code commit", "Test commit"):
        found = re.search(r"^\|\s*" + label + r"\s*\|\s*(.*?)\s*\|\s*$", body, re.M)
        values[label] = found.group(1).strip() if found else ""
    return values


def manifest(dest, name):
    rows = records(read(dest, name), "Files", ["ID", "Path", "Role"], "ID")
    for row in rows.values():
        require(row["Role"], f"{name}: Role")
        path = Path(row["Path"])
        if not path.is_absolute():
            path = dest / path
        if not path.is_file():
            raise QualityError(f"{name}: missing artifact {row['ID']}")
    return rows


def split_ids(value):
    return [] if value == "-" else [v.strip() for v in value.split(",") if v.strip()]


def evidence(dest):
    defined, planned, scoped = ut_design(dest)
    if metadata(dest, "implementation.md") != metadata(dest, "test-report.md"):
        raise QualityError("Test results belong to different code/test commits")
    raw = manifest(dest, "evidence-manifest.md")
    report = read(dest, "test-report.md")
    for label in ("Run ID", "Environment", "Tool versions", "Data version"):
        match = re.search(r"^\|\s*" + label + r"\s*\|\s*(.*?)\s*\|\s*$", report, re.M)
        require(match.group(1) if match else "", label)
    executed = records(report, "Results", ["Case ID", "Test ID", "Status", "Actual", "Evidence ID"], "Case ID")
    if set(executed) != set(planned):
        raise QualityError("Results must contain every planned case, with no unknown cases")
    for ident, row in executed.items():
        if row["Status"] not in {"PASS", "FAIL", "SKIPPED", "NOT_RUN"}:
            raise QualityError("Unknown test status")
        # All planned cases must pass before acceptance; omitted/optional cases need a new reviewed plan.
        if row["Status"] != "PASS":
            raise QualityError(f"Test not passed: {ident}")
        require(row["Test ID"], "Test ID")
        require(row["Actual"], "Actual result")
        if row["Evidence ID"] not in raw:
            raise QualityError(f"Missing result evidence: {ident}")
    trace = table(read(dest, "traceability.md"), "Traceability",
                  ["Rule ID", "Source", "Case ID", "Test ID", "Run ID", "Evidence ID"])
    linked = set()
    run_id = re.search(r"^\|\s*Run ID\s*\|\s*(.*?)\s*\|\s*$", report, re.M).group(1)
    for row in trace:
        ident = row["Case ID"]
        if ident not in planned or row["Rule ID"] != planned[ident]["Rule ID"]:
            raise QualityError("Traceability references unknown/mismatched rule or case")
        if any(row[key] != executed[ident][key] for key in ("Test ID", "Evidence ID")) or row["Run ID"] != run_id:
            raise QualityError("Traceability mismatches actual test result/run")
        require(row["Source"], "Traceability source")
        linked.add(ident)
    if linked != set(planned):
        raise QualityError("Traceability missing planned cases")
    exceptions = records(read(dest, "exceptions.md"), "Exceptions",
                         ["Exception ID", "Kind", "Target ID", "Reason", "Evidence ID", "Reviewer", "Decision", "Date"],
                         "Exception ID", True)
    used = set()
    def excluded(row, kind, target):
        ident = row["Exception ID"]
        if ident == "-":
            return False
        ex = exceptions.get(ident, {})
        if ex.get("Kind") != kind or ex.get("Target ID") != target or ex.get("Decision") != "APPROVED":
            raise QualityError("Invalid/unapproved coverage exception")
        for key in ("Reviewer", "Date", "Reason"):
            require(ex.get(key, ""), f"Exception {key}")
        if ex["Evidence ID"] not in raw:
            raise QualityError("Exception has no evidence")
        used.add(ident)
        return True
    def exercised(case_value, evidence_value):
        case_ids, evidence_ids = split_ids(case_value), split_ids(evidence_value)
        if not case_ids or len(case_ids) != len(evidence_ids) or len(set(case_ids)) != len(case_ids):
            raise QualityError("Coverage needs paired case/evidence IDs")
        for cid, eid in zip(case_ids, evidence_ids):
            if cid not in executed or eid not in raw:
                raise QualityError("Coverage references unknown case/evidence")
            if eid != executed[cid]["Evidence ID"]:
                raise QualityError("Coverage evidence is not from its referenced case")
    coverage = read(dest, "coverage.md")
    branches = records(coverage, "Branches",
                       ["Branch ID", "Module ID", "Location", "Outcome", "Case IDs", "Evidence IDs", "Exception ID"], "Branch ID", True)
    conditions = records(coverage, "Conditions",
                         ["Condition ID", "Module ID", "Location", "Expression", "True cases", "False cases", "True evidence", "False evidence", "Exception ID"],
                         "Condition ID", True)
    planned_conditions = records(read(dest, "ut-design.md"), "Condition plan",
                                 ["Condition ID"], "Condition ID", True)
    if not set(planned_conditions).issubset(conditions):
        raise QualityError("Code coverage inventory is missing planned conditions")
    totals = {mid: [0, 0, 0, 0] for mid in scoped}  # raw branches, exclusions, raw T/F, exclusions
    for bid, row in branches.items():
        mid = row["Module ID"]
        if mid not in totals:
            raise QualityError("Unknown coverage module")
        require(row["Location"], "Branch location")
        require(row["Outcome"], "Branch outcome")
        totals[mid][0] += 1
        if excluded(row, "BRANCH", bid):
            totals[mid][1] += 1
        else:
            exercised(row["Case IDs"], row["Evidence IDs"])
    for cid, row in conditions.items():
        mid = row["Module ID"]
        if mid not in totals:
            raise QualityError("Unknown condition module")
        require(row["Location"], "Condition location")
        require(row["Expression"], "Atomic expression")
        totals[mid][2] += 2
        if excluded(row, "CONDITION", cid):
            totals[mid][3] += 2
        else:
            exercised(row["True cases"], row["True evidence"])
            exercised(row["False cases"], row["False evidence"])
    if used != set(exceptions):
        raise QualityError("Unused/unknown exception records")
    metrics = records(coverage, "Modules",
                      ["Module ID", "C1 raw", "C1 excluded", "C1 covered", "C2 raw", "C2 excluded", "C2 covered", "Evidence ID"], "Module ID")
    if set(metrics) != set(scoped):
        raise QualityError("Coverage must report every scoped module separately")
    for mid, row in metrics.items():
        try:
            counts = [int(row[key]) for key in ("C1 raw", "C1 excluded", "C1 covered", "C2 raw", "C2 excluded", "C2 covered")]
        except ValueError as exc:
            raise QualityError("Coverage counts must be integers") from exc
        b, bx, bc, c, cx, cc = counts
        if min(counts) < 0 or [b, bx, c, cx] != totals[mid] or bc != b - bx or cc != c - cx:
            raise QualityError(f"C1/C2 counts do not prove 100% or mismatch inventory: {mid}")
        if row["Evidence ID"] not in raw:
            raise QualityError("Module coverage inventory needs evidence, including N/A")
    return scoped


def problems(dest, task, step):
    if task["kit_version"] != "0.3.0":
        return ["Unsupported quality profile; do not silently downgrade validation"]
    try:
        ident = step["id"]
        if ident == "S1":
            manifest(dest, "source-manifest.md")
            defined = rules(dest)
            for row in defined.values():
                yes_no(row["Required"])
                require(row["Source"], "Rule source")
                require(row["Statement"], "Rule statement")
            for row in records(read(dest, GUIDE), "Atomic conditions",
                               ["Condition ID", "Rule ID", "Expression", "True/False meaning", "Source"], "Condition ID", True).values():
                if row["Rule ID"] not in defined:
                    raise QualityError("Atomic condition references unknown rule")
                for key in ("Expression", "True/False meaning", "Source"):
                    require(row[key], f"Atomic condition {key}")
            plan = table(read(dest, GUIDE), "Kế hoạch code", ["Mục", "Rule ID", "Vị trí dự kiến", "Việc cần làm"])
            if not plan:
                raise QualityError("PG guide needs a non-empty implementation plan")
            for row in plan:
                for rid in re.split(r"[,\s]+", row["Rule ID"].strip()):
                    if rid and rid not in defined:
                        raise QualityError(f"Implementation plan references unknown rule: {rid}")
                require(row["Việc cần làm"], "Implementation plan item")
        elif ident == "S2":
            read(dest, "pg-implementation.md")
            manifest(dest, "pg-artifact-manifest.md")
        elif ident == "S3":
            ut_design(dest, require_dd=False)
        elif ident == "S4":
            design(dest)
            review(read(dest, "review.md"))
        elif ident == "S5":
            ut_design(dest)
            metadata(dest, "implementation.md")
            manifest(dest, "artifact-manifest.md")
            review(read(dest, "code-review.md"))
        elif ident == "S6":
            evidence(dest)
        elif ident == "S7":
            body = read(dest, "acceptance.md")
            review(body)
            checklist = table(body, "Acceptance checklist", ["Check", "Result", "Evidence / reviewer"])
            required_checks = {
                "C1 and C2 per module, raw/effective scope and inventory verified",
                "Expected result and all planned cases PASS",
                "No blocking defects; integration/regression and real/mock limits checked",
                "Source/commits/run/tool/data version and evidence reproducible",
                "Exceptions are real human decisions, not agent assumptions",
                "Handoff format, receiver and artifact access",
            }
            if {row["Check"] for row in checklist} != required_checks or len(checklist) != len(required_checks):
                raise QualityError("Acceptance checklist missing/duplicate checks")
            for row in checklist:
                if row["Result"] not in {"PASS", "N/A"}:
                    raise QualityError("Acceptance contains unverified checks")
                require(row["Evidence / reviewer"], "Acceptance evidence/reviewer")
                if row["Result"] == "N/A" and row["Check"] in {
                    "C1 and C2 per module, raw/effective scope and inventory verified",
                    "Expected result and all planned cases PASS",
                    "Source/commits/run/tool/data version and evidence reproducible",
                }:
                    raise QualityError("Core quality checks cannot be marked N/A")
        return []
    except (QualityError, OSError) as exc:
        return [str(exc)]
