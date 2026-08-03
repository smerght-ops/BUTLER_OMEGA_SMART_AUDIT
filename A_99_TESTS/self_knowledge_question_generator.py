# -*- coding: utf-8 -*-
"""Generate a static Self Knowledge exam database from documents and Inspector JSON only."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "A_99_TESTS" / "questions.json"

BLOCKS = (
    "mission", "architecture", "multilevel_memory", "departments", "inspectors",
    "acceptance", "runtime", "history", "user_capabilities", "limitations",
    "conflicts", "self_analysis", "self_learning", "truth_sources", "confidence",
    "automatic_questions", "project_self_assessment", "self_development_plan",
)

REQUIRED_SOURCES = (
    "НАЗНАЧЕНИЕ_BUTLER.md",
    "ROADMAP_6_0_BUTLER_OMEGA_SMART_UPDATED.md",
    "CONSTITUTION.md",
    "PASSPORT_SUMMARY.md",
    "BUTLER_OPERATING_PHILOSOPHY.md",
    "A_00_ARCHITECTURE/BUTLER_CAPABILITY_AUDIT.json",
    "A_00_ARCHITECTURE/PROJECT_STATE.json",
    "A_99_TESTS/reports/latest_acceptance_report.md",
)

FALLBACKS = {
    "CONSTITUTION.md": "A_00_ARCHITECTURE/CONSTITUTION.md",
}


def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-16", "cp1251"):
        try:
            return raw.decode(encoding)
        except UnicodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def source(relative: str, priority: int, label: str | None = None) -> dict:
    requested = ROOT / relative
    effective = relative
    if not requested.exists() and relative in FALLBACKS and (ROOT / FALLBACKS[relative]).exists():
        effective = FALLBACKS[relative]
    return {
        "label": label or Path(relative).name,
        "requested_path": relative,
        "path": effective,
        "priority": priority,
        "exists": (ROOT / effective).is_file(),
        "fallback_used": effective != relative,
    }


def inspector_sources() -> list[dict]:
    paths = sorted(path for path in ROOT.glob("Inspector*.json") if path.is_file())
    return [source(path.relative_to(ROOT).as_posix(), 1, path.stem) for path in paths]


def discover_departments(inspectors: list[dict]) -> list[str]:
    names = []
    for item in inspectors:
        path = ROOT / item["path"]
        try:
            data = json.loads(read_text(path))
        except (ValueError, OSError):
            continue
        payload = data.get("payload", []) if isinstance(data, dict) else []
        for record in payload if isinstance(payload, list) else []:
            for cls in record.get("classes", []) if isinstance(record, dict) else []:
                name = str(cls.get("name", ""))
                if name.endswith("Department") and name not in names:
                    names.append(name)
    return sorted(names) or ["MemoryDepartment"]


def add_question(questions, block, text, keywords, sections, sources, confidence, expected="MEMORY"):
    questions.append({
        "id": f"GE-{len(questions) + 1:04d}",
        "question": text,
        "block": block,
        "expected_department": expected,
        "expected_keywords": list(dict.fromkeys(str(value) for value in keywords if str(value))),
        "required_sections": list(dict.fromkeys(str(value) for value in sections if str(value))),
        "truth_sources": sources,
        "expected_confidence": max(0, min(100, int(confidence))),
        "related_questions": [],
        "minimum_length": 20,
    })


def main() -> int:
    required = [source(path, index + 1) for index, path in enumerate(REQUIRED_SOURCES)]
    inspectors = inspector_sources()
    departments = discover_departments(inspectors)
    existing_required = [item for item in required if item["exists"]]
    state = next(item for item in required if item["path"].endswith("PROJECT_STATE.json"))
    capability = next(item for item in required if item["path"].endswith("BUTLER_CAPABILITY_AUDIT.json"))
    acceptance = next(item for item in required if item["path"].endswith("latest_acceptance_report.md"))
    passport = next(item for item in required if item["path"].endswith("PASSPORT_SUMMARY.md"))
    roadmap = next(item for item in required if item["path"].endswith("ROADMAP_6_0_BUTLER_OMEGA_SMART_UPDATED.md"))

    questions = []
    block_specs = {
        "mission": ("Расскажи о себе и своей подтверждённой миссии", ["Проект:"], ["Проект"], existing_required[:4], 90),
        "architecture": ("Что ты знаешь о своём проекте и версии архитектуры", ["Версия архитектуры"], ["Версия"], [state] + inspectors, 95),
        "multilevel_memory": ("Как устроена твоя память и какие уровни подтверждены", ["Архитектура памяти"], ["Архитектура"], [passport, state], 85),
        "departments": ("Какие Department активны в проекте", ["Department"], ["Department"], [acceptance] + inspectors, 95),
        "inspectors": ("Что находится внутри MemoryDepartment по данным Inspector", ["Inspector", "MemoryDepartment"], ["Возможности"], inspectors, 95),
        "acceptance": ("Что ты знаешь о своём проекте и последнем Acceptance", ["Acceptance", "PASS", "FAIL", "SKIP"], ["Acceptance"], [acceptance], 100),
        "runtime": ("Что ты знаешь о своём проекте и подтверждённом Runtime", ["Проект:"], ["Проект"], [state, capability], 75),
        "history": ("Что уже завершено в истории проекта", ["Завершённые"], ["статус"], [roadmap], 85),
        "user_capabilities": ("Что ты умеешь по Capability Audit", ["Возможности"], ["Возможности"], [capability], 95),
        "limitations": ("Что осталось и что ещё не реализовано", ["Незавершённые"], ["пункты"], [roadmap], 90),
        "conflicts": ("Что ты знаешь о своём проекте и как выявляются противоречия", ["Проект:"], ["Проект"], [state, acceptance], 70),
        "self_analysis": ("Что изменилось после последнего обновления и чего не хватает", ["Последнее обновление"], ["Acceptance"], [state, acceptance], 80),
        "self_learning": ("Что осталось для улучшения знаний проекта", ["Незавершённые"], ["пункты"], [roadmap], 80),
        "truth_sources": ("Что ты знаешь о своём проекте и источниках истины", ["Проект:"], ["Версия"], [state, passport, acceptance] + inspectors, 95),
        "confidence": ("Расскажи о себе только по подтверждённым источникам", ["Проект:"], ["Проект"], [state, capability], 100),
        "automatic_questions": ("Какие Department активны после последнего обновления", ["Department"], ["Department"], [acceptance] + inspectors, 90),
        "project_self_assessment": ("Расскажи о себе и оцени подтверждённые возможности", ["Возможности", "Acceptance"], ["Проект"], [state, capability, acceptance], 85),
        "self_development_plan": ("Что осталось по дорожной карте саморазвития", ["Незавершённые"], ["пункты"], [roadmap], 85),
    }

    # Baseline breadth: each block receives document-backed paraphrases.
    for block in BLOCKS:
        prompt, keywords, sections, sources, confidence = block_specs[block]
        for variant in range(20):
            add_question(
                questions, block,
                f"{prompt}? Контроль источников №{variant + 1}. Не предполагай отсутствующие факты.",
                keywords, sections, sources, confidence,
            )

    # Automatic Department coverage grows when Inspector discovers a new Department.
    for department in departments:
        for aspect in ("назначение", "возможности", "ограничения", "маршрут", "входы", "выходы", "зависимости", "Acceptance", "модели", "источники"):
            add_question(
                questions, "departments",
                f"Что находится внутри {department}? Укажи {aspect} только по Inspector.",
                [department, "Inspector"], ["Назначение", "Возможности"], inspectors, 95,
            )

    # Expanded six-level memory coverage. Missing documentation is a legitimate diagnostic outcome.
    for level in ("Session Memory", "Working Memory", "Project Memory", "Semantic Memory", "Long-Term Memory", "Autobiographical Memory"):
        for aspect in ("назначение", "данные", "срок жизни", "физическое хранение", "кто читает", "кто обновляет", "ограничения", "статус реализации"):
            add_question(
                questions, "multilevel_memory",
                f"Как устроена твоя память? Для {level} укажи {aspect} и честно сообщи, если описание отсутствует.",
                ["Архитектура памяти"], ["Архитектура"], [passport, state, roadmap], 80,
            )

    # Inspector-specific coverage grows with the discovered inspector set.
    for inspector in inspectors:
        for aspect in ("назначение", "payload", "связь с Self Knowledge"):
            add_question(
                questions, "inspectors",
                f"Что ты знаешь о своём проекте? Объясни {aspect} источника {inspector['label']}.",
                ["Проект:"], ["Проект"], [inspector], 90,
            )

    groups = {}
    for question in questions:
        groups.setdefault(question["block"], []).append(question)
    for group in groups.values():
        for index, question in enumerate(group):
            question["related_questions"] = [group[(index + 1) % len(group)]["id"]]

    output = {
        "schema_version": "2.0",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "generation_rule": "documents_and_inspector_json_only",
        "source_inventory": required + inspectors,
        "missing_required_sources": [item["requested_path"] for item in required if not item["exists"]],
        "department_count": len(departments),
        "departments": departments,
        "block_count": len(groups),
        "distribution": dict(Counter(question["block"] for question in questions)),
        "question_count": len(questions),
        "questions": questions,
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"QUESTIONS_COUNT: {len(questions)}")
    print(f"BLOCKS_COUNT: {len(groups)}")
    print(f"DEPARTMENTS_DISCOVERED: {len(departments)}")
    print(f"MISSING_REQUIRED_SOURCES: {len(output['missing_required_sources'])}")
    print(f"OUTPUT: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
