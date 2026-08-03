# -*- coding: utf-8 -*-
"""Analyze State Exam problems without modifying Butler working code or truth sources."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "A_99_TESTS" / "reports"
EXAM = REPORTS / "latest_exam_report.json"
QUESTIONS = ROOT / "A_99_TESTS" / "questions.json"


def classify(item: dict) -> str:
    categories = set(item.get("error_categories", []))
    if "NO_SOURCE" in categories:
        return "NO_SOURCE"
    if "DOCUMENTATION_GAP" in categories or item.get("status") == "UNKNOWN":
        return "DOCUMENTATION_GAP"
    if "LOW_CONFIDENCE" in categories:
        return "LOW_CONFIDENCE"
    if item.get("consistency_conflicts"):
        return "CONFLICT"
    if item.get("status") == "PARTIAL":
        return "INCOMPLETE_ANSWER"
    answers = item.get("answers", [])
    if not answers or any(not str(answer.get("text") or "").strip() for answer in answers):
        return "MISSING_ANSWER"
    if item.get("status") == "UNSTABLE":
        return "CONFLICT"
    return "MISSING_ANSWER"


def markdown(report: dict) -> str:
    lines = ["# Self Knowledge Analysis", "", f"Timestamp: `{report['timestamp']}`  ", f"Problems: **{report['problem_count']}**", "", "## Classification", ""]
    for name, count in report["classification_counts"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Problems", ""])
    for item in report["problems"][:250]:
        lines.append(f"- `{item['id']}` {item['classification']}: {item['cause']}")
    if len(report["problems"]) > 250:
        lines.append(f"- … and {len(report['problems']) - 250} more; see JSON report.")
    lines.extend(["", "## Missing source inventory", ""])
    lines.extend(f"- `{path}`" for path in report["missing_sources"]) or lines.append("None")
    return "\n".join(lines) + "\n"


def main() -> int:
    exam = json.loads(EXAM.read_text(encoding="utf-8-sig"))
    question_db = json.loads(QUESTIONS.read_text(encoding="utf-8-sig"))
    known_questions = {item["id"]: item for item in question_db.get("questions", [])}
    problems, missing_sources = [], set()
    for item in exam.get("results", []):
        if item.get("status") == "PASS" and not item.get("consistency_conflicts") and not item.get("error_categories"):
            continue
        question = known_questions.get(item.get("id"), item)
        truth_sources = []
        found_sources = []
        for source in question.get("truth_sources", []):
            record = dict(source)
            exists = (ROOT / str(record.get("path", ""))).is_file()
            record["verified_exists"] = exists
            truth_sources.append(record)
            if exists:
                found_sources.append(record["path"])
            else:
                missing_sources.add(str(record.get("requested_path") or record.get("path")))
        classification = classify(item)
        actual_departments = sorted({str(answer.get("department")) for answer in item.get("answers", []) if answer.get("department")})
        if actual_departments and actual_departments != [str(item.get("expected_department"))]:
            cause = f"Official routing mismatch: expected {item.get('expected_department')}, actual {actual_departments}"
        elif not found_sources:
            cause = "No readable truth source exists; documentation gap"
        elif classification == "INCOMPLETE_ANSWER":
            cause = "Truth source exists, but the answer omits required keywords or sections"
        elif classification == "CONFLICT":
            cause = "Linked or repeated answers are inconsistent"
        elif classification == "DOCUMENTATION_GAP":
            cause = "Butler reports missing information; documentation/source exposure is incomplete"
        else:
            cause = "; ".join(item.get("reasons", [])) or "Answer does not satisfy the verified question contract"
        problems.append({
            "id": item.get("id"), "block": item.get("block"), "status": item.get("status"),
            "classification": classification, "cause": cause,
            "expected_department": item.get("expected_department"), "actual_departments": actual_departments,
            "truth_sources": truth_sources, "found_sources": found_sources,
            "observed_sources": item.get("observed_sources", []),
            "reasons": item.get("reasons", []), "conflicts_with": item.get("consistency_conflicts", []),
        })
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    classifications = Counter(item["classification"] for item in problems)
    by_block = defaultdict(int)
    for item in problems:
        by_block[item["block"]] += 1
    report = {
        "timestamp": timestamp, "exam_timestamp": exam.get("timestamp"),
        "problem_count": len(problems), "classification_counts": dict(classifications),
        "problems_by_block": dict(by_block), "missing_sources": sorted(missing_sources),
        "problems": problems, "working_code_modified": False,
    }
    json_path = REPORTS / f"analysis_report_{timestamp}.json"
    md_path = REPORTS / f"analysis_report_{timestamp}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    (REPORTS / "latest_analysis_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORTS / "latest_analysis_report.md").write_text(markdown(report), encoding="utf-8")
    print(f"PROBLEMS: {len(problems)}")
    print(" ".join(f"{name}={count}" for name, count in sorted(classifications.items())))
    print(f"REPORT_JSON: {json_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
