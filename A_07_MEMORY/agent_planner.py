# -*- coding: utf-8 -*-

import json
import subprocess
from pathlib import Path


class AgentPlannerV2:
    """Управляет полулинейным графом целей с жесткой изоляцией активной фазы."""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.registry_path = self.project_root / "A_07_CONFIG" / "goals_registry.json"

    def load_registry(self) -> dict:
        if not self.registry_path.exists():
            return {}
        try:
            return json.loads(self.registry_path.read_text(encoding="utf-8-sig"))
        except Exception:
            return {}

    def _save_registry(self, data: dict) -> bool:
        try:
            self.registry_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            return True
        except Exception:
            return False

    def get_current_action_plan(self) -> dict:
        """Возвращает строго изолированную задачу текущей активной фазы."""
        reg = self.load_registry()
        if not reg:
            return {
                "active_goal": "STABILIZATION",
                "active_phase": "CRITICAL_ERROR",
                "active_task": "FIX_REGISTRY"
            }

        current_phase = reg.get("current_phase", "UNKNOWN")

        plan = {
            "active_goal": reg.get("active_goal", "UNKNOWN"),
            "active_phase": current_phase,
            "active_task": "UNKNOWN"
        }

        for subgoal in reg.get("subgoals", []):
            # ЖЕСТКИЙ ФИЛЬТР: Смотрим ТОЛЬКО на текущую активную фазу
            if subgoal.get("id") != current_phase:
                continue

            if subgoal.get("status") == "COMPLETED":
                return {"status": "ALL_TASKS_COMPLETED"}

            for task in subgoal.get("tasks", []):
                if task.get("status") == "PENDING":
                    plan["active_task"] = task.get("id")
                    return plan

        return plan

    def complete_task(self, task_id: str) -> bool:
        reg = self.load_registry()
        if not reg:
            return False

        current_phase = reg.get("current_phase")
        task_changed = False
        phase_subgoals = [s for s in reg.get("subgoals", []) if s.get("id") == current_phase]

        if not phase_subgoals:
            return False

        subgoal = phase_subgoals[0]
        for task in subgoal.get("tasks", []):
            if task.get("id") == task_id and task.get("status") == "PENDING":
                task["status"] = "COMPLETED"
                task_changed = True
                break

        if not task_changed:
            return False

        all_done = all(t.get("status") == "COMPLETED" for t in subgoal.get("tasks", []))

        if all_done:
            subgoal["status"] = "COMPLETED"
            for s in reg.get("subgoals", []):
                if s.get("status") == "PENDING":
                    reg["current_phase"] = s.get("id")
                    s["status"] = "ACTIVE"
                    break

        return self._save_registry(reg)


class FeedbackValidatorV2:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]

    def validate_file_syntax(self, relative_path: str) -> bool:
        target_file = self.project_root / relative_path
        if not target_file.exists():
            return False
        try:
            res = subprocess.run(
                ["python", "-m", "py_compile", str(target_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return res.returncode == 0
        except Exception:
            return False
