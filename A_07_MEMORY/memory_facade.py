# -*- coding: utf-8 -*-

import json
from pathlib import Path
from A_07_MEMORY.project_history import ProjectHistory
from A_07_MEMORY.change_request_manager import ChangeRequestManager
from A_07_MEMORY.agent_planner import AgentPlannerV2
from A_07_CONFIG.passport_report import PassportReport


class MemoryFacade:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.passport_path = self.project_root / "A_07_CONFIG" / "project_passport.json"
        self.history_engine = ProjectHistory()
        self.cr = ChangeRequestManager()
        self.planner = AgentPlannerV2()

    def _load_raw_passport(self):
        if not self.passport_path.exists():
            return {}
        try:
            return json.loads(self.passport_path.read_text(encoding="utf-8-sig"))
        except Exception:
            return {}

    def get_unified_context(self):
        raw_passport = self._load_raw_passport()
        if not raw_passport:
            return {"error": "Базовый паспорт проекта недоступен."}

        identity = raw_passport.get("project_identity", {})
        freeze = raw_passport.get("architecture_freeze", {})
        roadmap = raw_passport.get("roadmap_pointer", {})

        # Читаем выровненный контракт v2
        plan = self.planner.get_current_action_plan()

        passport = {
            "project_name": identity.get("name", "UNKNOWN"),
            "version": identity.get("version", "UNKNOWN"),
            "current_stage": identity.get("current_stage", "UNKNOWN"),
            "frozen_modules": freeze.get("frozen_modules", []),
            "active_modules": freeze.get("active_modules", []),
            "current_task": roadmap.get("current_task", "UNKNOWN"),
            "next_task": roadmap.get("next_task", "UNKNOWN")
        }

        return {
            "passport": passport,
            "plan_meta": plan
        }

    def get_passport_string(self):
        context = self.get_unified_context()
        if "error" in context:
            return context["error"]

        p = context["passport"]

        lines = [
            "===== BUTLER PASSPORT (AUTONOMOUS V2) =====",
            f"\nNAME:\n{p.get('project_name')}",
            f"\nVERSION:\n{p.get('version')}",
            f"\nCURRENT STAGE (PHASE):\n{p.get('current_stage')}",
            "\nFROZEN MODULES:"
        ]
        for mod in p.get("frozen_modules", []):
            lines.append(f"- {mod}")

        lines.append("\nACTIVE MODULES:")
        for mod in p.get("active_modules", []):
            lines.append(f"- {mod}")

        lines.append(f"\nCURRENT TARGET TASK:\n{p.get('current_task')}")
        lines.append(f"\nGLOBAL GOAL V2:\n{p.get('next_task')}")
        return "\n".join(lines)


if __name__ == "__main__":
    facade = MemoryFacade()
    print(facade.get_passport_string())
