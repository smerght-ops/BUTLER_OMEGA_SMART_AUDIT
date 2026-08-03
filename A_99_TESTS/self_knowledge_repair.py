# -*- coding: utf-8 -*-
"""Create repair proposals only. Never applies changes to Butler working code."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "A_99_TESTS" / "reports" / "latest_analysis_report.json"
QUESTIONS = ROOT / "A_99_TESTS" / "questions.json"
OUTPUT = ROOT / "A_99_TESTS" / "repair_proposals.json"


def proposal_text(problem: dict) -> tuple[str, str]:
    actual = set(problem.get("actual_departments", []))
    expected = problem.get("expected_department")
    if actual and actual != {expected}:
        return (
            "routing_before_memory",
            "Не добавлять данные в MemoryDepartment автоматически. Проверить приоритет существующего маршрута для этой формулировки; "
            "после ручного решения убедиться, что запрос достигает MemoryDepartment, который уже читает заявленные источники.",
        )
    if problem.get("classification") == "INCOMPLETE_ANSWER":
        return (
            "memory_answer_projection",
            "Предложить минимальное расширение существующего формирования Self Knowledge ответа данными из найденного источника истины; "
            "Result Contract и архитектуру не менять.",
        )
    return (
        "knowledge_source_exposure",
        "Предложить MemoryDepartment явно экспонировать существующий источник истины в Self Knowledge ответе; отсутствующие факты не придумывать.",
    )


def main() -> int:
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8-sig"))
    question_db = json.loads(QUESTIONS.read_text(encoding="utf-8-sig"))
    questions = {item["id"]: item for item in question_db.get("questions", [])}
    proposals = []
    for index, problem in enumerate(analysis.get("problems", []), 1):
        found = [path for path in problem.get("found_sources", []) if (ROOT / path).is_file()]
        if not found:
            continue
        question = questions.get(problem.get("id"), {})
        cause, suggestion = proposal_text(problem)
        confidence = min([int(item.get("expected_confidence", 70)) for item in [question] if item] or [70])
        proposals.append({
            "proposal_id": f"RP-{index:04d}",
            "problem_id": problem.get("id"),
            "problem_text": problem.get("cause"),
            "problem_type": problem.get("classification"),
            "root_cause": cause,
            "truth_sources": found,
            "source_reference": {"file": found[0], "line": None, "document": Path(found[0]).name},
            "proposed_fix": suggestion,
            "candidate_target": "A_04_AGENTS/MemoryDepartment/runner.py",
            "confidence": confidence,
            "requires_human_confirmation": True,
            "applied_to_working_project": False,
            "validation_status": "PENDING",
            "validation_errors": [],
            "validation_date": None,
        })
    payload = {
        "schema_version": "1.0", "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_analysis_timestamp": analysis.get("timestamp"),
        "proposal_count": len(proposals), "automatic_application": False,
        "proposals": proposals,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"REPAIR_PROPOSALS_GENERATED: {len(proposals)}")
    print("AUTOMATIC_APPLICATION: DISABLED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
