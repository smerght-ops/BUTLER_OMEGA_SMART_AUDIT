# -*- coding: utf-8 -*-
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_07_MEMORY.memory_facade_v2 import MemoryFacadeV2 as MemoryFacade
from A_07_MEMORY.project_history import ProjectHistory
import subprocess


class PassportCommandHandler:

    def __init__(self):
        self.facade = MemoryFacade()
        self.history = ProjectHistory()

    def handle_command(self, user_input: str):
        # Приводим к нижнему регистру и очищаем от мусора
        clean = str(user_input).lower().strip().rstrip("?.!")

        # 1. Слой перехвата Паспорта и Статуса
        if any(w in clean for w in ["кто ты", "статус", "паспорт"]):
            return self.facade.get_passport_string()

        # 2. Слой перехвата Истории и Памяти
        if any(w in clean for w in ["что сделано", "память", "истори"]):
            return self.history.get_lesson_summary()

        # 3. Evidence Doctor
        if any(w in clean for w in ["доктор проекта","doctor","evidence"]):
            doctor = PROJECT_ROOT / "A_04_AGENTS" / "ProjectDocumentationDepartment" / "Core" / "evidence_doctor.py"

            result = subprocess.run(
                [sys.executable, str(doctor)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=PROJECT_ROOT
            )

            return result.stdout if result.returncode == 0 else result.stderr

        # 3. Слой перехвата Планов и Роадмапа
        if any(w in clean for w in ["что дальше", "план", "roadma"]):
            frozen = []
            frozen_text = "\n- ".join(frozen) if frozen else "None"
            return f"===== NEXT ROADMAP TASKS =====\nCURRENT: PHASE_TRANSITION_VALIDATED\nNEXT: BUTLER_HARNESS_V3_INTEGRATION"

        return None


if __name__ == "__main__":
    handler = PassportCommandHandler()
    print("=== ТЕСТ ИНТЕГРАЦИИ ЕДИННОГО ФАСАДА ПАМЯТИ ===")
    print(handler.handle_command("паспорт"))






