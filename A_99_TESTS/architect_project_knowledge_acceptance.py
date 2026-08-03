# -*- coding: utf-8 -*-
"""Read-only specialized acceptance for Architect project knowledge."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from A_02_MANAGERS.ArchitectAgent.context_provider import ContextProvider
from A_02_MANAGERS.ArchitectAgent.architect_agent import ArchitectAgent


CASES = (
    ("combined_architecture", """Архитектор, проанализируй текущее состояние проекта Butler Omega Smart.
Покажи основные компоненты и связи между ними, Runtime и Dispatcher,
Department, память, безопасность, Inspector-систему и capabilities.
Укажи подтверждённые возможности и результаты Acceptance.
Отдельно укажи устаревшие данные как STALE,
а неподтверждённые факты как UNCONFIRMED.
Используй только фактические данные текущего проекта.""",
     ("Состояние", "Основные компоненты", "Связи", "Runtime и Dispatcher", "Departments",
      "Память", "Безопасность", "Inspector/Scanner/Analyzer", "Capabilities", "Acceptance", "STALE", "UNCONFIRMED")),
    ("stage", "На какой стадии находится проект?", ("стадия", "project_passport.json")),
    ("departments", "Какие Department существуют?", ("SmartDispatcherV2", "FilesystemDepartment")),
    ("department_capabilities", "Что умеет FilesystemDepartment?", ("FilesystemDepartment", "rename")),
    ("subsystem_files", "Какие файлы относятся к подсистеме памяти?", ("Memory",)),
    ("module_entities", "Какие классы существуют в модуле FilesystemDepartment?", ("FilesystemDepartment", "runner.py")),
    ("callers", "Кто вызывает ArchitectAgent?", ("AST",)),
    ("dependencies", "Какие компоненты зависят от ArchitectAgent?", ("импорт",)),
    ("memory", "Какие уровни памяти существуют?", ("памяти", "Memory")),
    ("security", "Какие механизмы безопасности существуют?", ("безопасности",)),
    ("inspectors", "Какие Inspector существуют?", ("Inspector",)),
    ("maps", "Какие MAP-артефакты существуют?", ("Inspector0_PhysicalMap.json", "AVAILABLE")),
    ("capabilities", "Какие capabilities уже реализованы?", ("Runtime-capabilities", "Capability")),
    ("proof", "Чем доказано, что capability работает?", ("Acceptance evidence", "official_entry")),
    ("offline", "Какие компоненты являются offline-инструментами?", ("OFFLINE_TOOL",)),
    ("limits", "Какие известные ограничения существуют?", ("ограничения",)),
    ("unknown", "Существует ли QuantumTeleportationDepartment?", ("UNCONFIRMED",)),
)


def main():
    provider = ContextProvider(ROOT)
    failed = []
    for case_id, question, markers in CASES:
        context = provider.build_context(question)
        answer = ArchitectAgent._factual_answer(question, context)
        ok = all(marker.casefold() in answer.casefold() for marker in markers)
        print(f"{'PASS' if ok else 'FAIL'} {case_id}: {answer[:280]}")
        if not ok:
            failed.append(case_id)
    print(f"RESULT: {len(CASES)-len(failed)} PASS / {len(failed)} FAIL")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
