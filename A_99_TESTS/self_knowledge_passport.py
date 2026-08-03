# -*- coding: utf-8 -*-
"""Update Self Passport, baseline and append-only learning history."""

from __future__ import annotations

import json
import socket
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM = ROOT / "A_99_TESTS/reports/latest_exam_report.json"
ANALYSIS = ROOT / "A_99_TESTS/reports/latest_analysis_report.json"
PROPOSALS = ROOT / "A_99_TESTS/repair_proposals.json"
QUESTIONS = ROOT / "A_99_TESTS/questions.json"
ACCEPTANCE = ROOT / "A_99_TESTS/reports/latest_acceptance_report.json"
STATE = ROOT / "A_00_ARCHITECTURE/PROJECT_STATE.json"
CAPABILITIES = ROOT / "A_00_ARCHITECTURE/BUTLER_CAPABILITY_AUDIT.json"
PASSPORT = ROOT / "SELF_PASSPORT.md"
BASELINE = ROOT / "SELF_KNOWLEDGE_BASELINE.json"
HISTORY = ROOT / "SELF_KNOWLEDGE_HISTORY.json"


def online(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def capability_count(data) -> int:
    groups = data.get("capabilities", {}) if isinstance(data, dict) else {}
    if isinstance(groups, dict):
        return sum(len(value) if isinstance(value, list) else 1 for value in groups.values())
    return len(groups) if isinstance(groups, list) else 0


def main() -> int:
    now = datetime.now().isoformat(timespec="seconds")
    exam = json.loads(EXAM.read_text(encoding="utf-8-sig"))
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8-sig"))
    proposals = json.loads(PROPOSALS.read_text(encoding="utf-8-sig"))
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8-sig"))
    acceptance = json.loads(ACCEPTANCE.read_text(encoding="utf-8-sig"))
    state = json.loads(STATE.read_text(encoding="utf-8-sig"))
    capabilities = json.loads(CAPABILITIES.read_text(encoding="utf-8-sig"))
    validated = [item["proposal_id"] for item in proposals.get("proposals", []) if item.get("validation_status") == "VALIDATED"]
    conflicts = len(exam.get("consistency_conflicts", []))
    documentation_gaps = analysis.get("classification_counts", {}).get("DOCUMENTATION_GAP", 0) + len(questions.get("missing_required_sources", []))
    full_ok = acceptance.get("counts", {}).get("FAIL") == 0 and acceptance.get("exit_code") == 0
    previous = json.loads(BASELINE.read_text(encoding="utf-8-sig")) if BASELINE.exists() else None
    baseline = {
        "created_at": now, "project": state.get("project"), "architecture_version": state.get("architecture_version"),
        "exam_timestamp": exam.get("timestamp"), "self_knowledge_score": exam.get("self_knowledge_score"),
        "counts": {**exam.get("counts", {}), "CONFLICT": conflicts},
        "sources": sorted({source.get("path") for item in questions.get("questions", []) for source in item.get("truth_sources", []) if source.get("exists")}),
        "validated_proposals": validated, "full_acceptance_pass": full_ok,
    }
    BASELINE.write_text(json.dumps(baseline, ensure_ascii=False, indent=2), encoding="utf-8")
    history = json.loads(HISTORY.read_text(encoding="utf-8-sig")) if HISTORY.exists() else {"schema_version": "1.0", "entries": []}
    before_score = previous.get("self_knowledge_score") if previous else None
    history["entries"].append({
        "date": now, "score": exam.get("self_knowledge_score"),
        "changes": {"previous_score": before_score, "delta": None if before_score is None else round(exam.get("self_knowledge_score", 0) - before_score, 2)},
        "applied_repair_proposals": [], "validated_repair_proposals": validated,
        "validation": proposals.get("validation_summary", {}),
    })
    HISTORY.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# SELF PASSPORT", "", "Passport version: 1.0  ", f"Updated: {now}  ",
        f"Last exam: {exam.get('timestamp')}", "", "## Knowledge", "",
        f"- Self Knowledge Score: {exam.get('self_knowledge_score')}/100",
        f"- Department count: {questions.get('department_count')}",
        f"- Capability count: {capability_count(capabilities)}",
        f"- Conflict count: {conflicts}", f"- Documentation Gap count: {documentation_gaps}",
        f"- Validated Repair Proposals: {len(validated)}", "", "## Block scores", "",
    ]
    lines.extend(f"- {block}: {score}" for block, score in exam.get("block_scores", {}).items())
    lines.extend(["", "## Project validation", "", f"- Last FULL Acceptance: {'PASS' if full_ok else 'FAIL'}", f"- FULL counts: {acceptance.get('counts')}", f"- Baseline date: {now}", f"- Baseline architecture version: {state.get('architecture_version')}", "", "## Runtime", "", f"- Ollama 127.0.0.1:11434: {'ONLINE' if online(11434) else 'OFFLINE'}", f"- ComfyUI 127.0.0.1:8188: {'ONLINE' if online(8188) else 'OFFLINE'}"])
    PASSPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("SELF_PASSPORT_UPDATED: YES")
    print("BASELINE_CREATED: YES")
    print(f"HISTORY_ENTRIES: {len(history['entries'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
