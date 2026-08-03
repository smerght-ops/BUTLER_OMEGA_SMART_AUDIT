# -*- coding: utf-8 -*-

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from A_02_MANAGERS.ArchitectAgent.dependency_analyzer import DependencyAnalyzer
from A_02_MANAGERS.ArchitectAgent.goal_analyzer import GoalAnalyzer
from A_02_MANAGERS.ArchitectAgent.recipe_builder import RecipeBuilder
from A_02_MANAGERS.goal_manager import GoalManager


class PlannerManager:
    """Read-only orchestration facade over GoalManager and ArchitectAgent."""

    def __init__(self, root=None, storage_path=None, goal_manager=None):
        self.root = Path(root) if root else Path(__file__).resolve().parents[2]
        self.storage_path = Path(storage_path) if storage_path else self.root / "A_07_MEMORY" / "plans_registry.json"
        self.goal_manager = goal_manager or GoalManager()
        self.goal_analyzer = GoalAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer(self.root)
        self.recipe_builder = RecipeBuilder()
        self._lock = threading.RLock()
        self._ensure_storage()

    def _result(self, ok, text, error=None, **metadata):
        return {"ok": bool(ok), "text": str(text), "error": error, "metadata": metadata}

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _ensure_storage(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._save({"version": "1.0", "plans": []})

    def _load(self):
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8-sig"))
            if not isinstance(data, dict) or not isinstance(data.get("plans"), list):
                raise ValueError("invalid plans registry")
            return data
        except Exception as exc:
            raise RuntimeError("PLANS_STORAGE_READ_ERROR") from exc

    def _save(self, data):
        temporary = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
        try:
            temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(self.storage_path)
        except Exception as exc:
            if temporary.exists():
                temporary.unlink()
            raise RuntimeError("PLANS_STORAGE_WRITE_ERROR") from exc

    def _architect_context(self, goal):
        phase_id = "goal_tasks"
        return {
            "goals_registry": {
                "active_goal": goal["id"],
                "current_phase": phase_id,
                "status": goal.get("status", "active"),
                "subgoals": [{"id": phase_id, "tasks": list(goal.get("tasks", []))}],
            }
        }

    def _build(self, goal):
        context = self._architect_context(goal)
        analysis = self.goal_analyzer.analyze(context)
        dependencies = self.dependency_analyzer.analyze(analysis, context)
        recipe = self.recipe_builder.build_planning_recipe(analysis, dependencies)
        return analysis, dependencies, recipe

    def generate_plan(self, goal_id):
        goal_result = self.goal_manager.get_goal(goal_id)
        if not goal_result.get("ok"):
            return self._result(False, "Не удалось построить план: цель не найдена.", goal_result.get("error"), goal_id=goal_id)
        goal = goal_result["metadata"]["goal"]
        try:
            analysis, dependencies, recipe = self._build(goal)
            now = self._now()
            plan = {
                "id": "plan_" + uuid.uuid4().hex[:12], "goal_id": goal_id,
                "status": "planned", "revision": 1, "analysis": analysis,
                "dependency_summary": {"graph_nodes": dependencies["graph_nodes"], "graph_edges": dependencies["graph_edges"], "safe_execution": dependencies["safe_execution"]},
                "recipe": recipe, "created_at": now, "updated_at": now,
            }
            with self._lock:
                data = self._load(); data["plans"].append(plan); self._save(data)
            return self._result(True, f"План создан: {plan['id']}", plan_id=plan["id"], plan=plan)
        except RuntimeError as exc:
            return self._result(False, "Не удалось создать план.", str(exc), goal_id=goal_id)

    def get_plan(self, plan_id):
        try:
            with self._lock:
                plan = next((item for item in self._load()["plans"] if item.get("id") == plan_id), None)
            if plan is None:
                return self._result(False, "План не найден.", "PLAN_NOT_FOUND", plan_id=plan_id)
            return self._result(True, f"План найден: {plan_id}", plan_id=plan_id, plan=plan)
        except RuntimeError as exc:
            return self._result(False, "Не удалось прочитать план.", str(exc), plan_id=plan_id)

    def latest_plan_id(self):
        data = self._load()
        return data["plans"][-1]["id"] if data["plans"] else None

    def optimize_plan(self, plan_id):
        current = self.get_plan(plan_id)
        if not current.get("ok"):
            return current
        plan = current["metadata"]["plan"]
        goal_result = self.goal_manager.get_goal(plan["goal_id"])
        if not goal_result.get("ok"):
            return self._result(False, "Не удалось оптимизировать план: цель не найдена.", goal_result.get("error"), plan_id=plan_id)
        try:
            analysis, dependencies, recipe = self._build(goal_result["metadata"]["goal"])
            with self._lock:
                data = self._load()
                stored = next(item for item in data["plans"] if item.get("id") == plan_id)
                stored.update({"analysis": analysis, "dependency_summary": {"graph_nodes": dependencies["graph_nodes"], "graph_edges": dependencies["graph_edges"], "safe_execution": dependencies["safe_execution"]}, "recipe": recipe, "revision": int(stored.get("revision", 1)) + 1, "updated_at": self._now()})
                self._save(data)
            return self._result(True, f"План оптимизирован: {plan_id}", plan_id=plan_id, plan=stored)
        except RuntimeError as exc:
            return self._result(False, "Не удалось оптимизировать план.", str(exc), plan_id=plan_id)
