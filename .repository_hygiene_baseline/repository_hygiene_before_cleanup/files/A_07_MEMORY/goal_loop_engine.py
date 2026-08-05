# -*- coding: utf-8 -*-

import json
from pathlib import Path


class GoalLoopEngine:
    """Управляет макро-эволюцией целей. Избавляет от bootstrap-петли."""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.registry_path = self.project_root / "A_07_CONFIG" / "goals_registry.json"

    def load(self) -> dict:
        if not self.registry_path.exists():
            return {}
        try:
            return json.loads(self.registry_path.read_text(encoding="utf-8-sig"))
        except Exception:
            return {}

    def save(self, data: dict):
        try:
            self.registry_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def run(self):
        reg = self.load()
        if not reg:
            return

        current_phase = reg.get("current_phase")
        
        # Если макро-движок видит, что мы застряли на bootstrap - принудительно двигаем на финал и бэкап ядра
        if reg.get("active_goal") == "SYSTEM_EVOLUTION_LOOP" or current_phase == "PHASE_1_INIT":
            reg["active_goal"] = "PRODUCTION_CORE_FINAL"
            reg["current_phase"] = "PHASE_3_CLEANUP_AND_BACKUP"
            reg["subgoals"] = [
                {
                    "id": "PHASE_3_CLEANUP_AND_BACKUP",
                    "status": "ACTIVE",
                    "tasks": [
                        {"id": "run_core_backup", "status": "PENDING"}
                    ]
                }
            ]
            self.save(reg)
            print("[GOAL_ENGINE] Макро-цель успешно переключена на PHASE_3_CLEANUP_AND_BACKUP.")
