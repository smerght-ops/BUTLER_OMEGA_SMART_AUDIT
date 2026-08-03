# -*- coding: utf-8 -*-

"""Deterministic, read-only priority calculation for existing goal tasks."""

from A_02_MANAGERS.Planner.planner_manager import PlannerManager
from A_02_MANAGERS.goal_manager import GoalManager
from A_02_MANAGERS.progress_tracker import ProgressTracker


class PriorityEngine:
    """Compute task order without mutating goals, plans, progress, or tasks."""

    PRIORITY_WEIGHTS = {"low": 10, "normal": 20, "high": 30, "critical": 40}
    STATUS_WEIGHTS = {"pending": 20, "in_progress": 30, "completed": 0, "cancelled": 0}

    def __init__(self, goal_manager=None, planner=None, progress_tracker=None):
        self.goal_manager = goal_manager or GoalManager()
        self.planner = planner or PlannerManager(goal_manager=self.goal_manager)
        self.progress_tracker = progress_tracker or ProgressTracker(
            goal_manager=self.goal_manager, planner=self.planner
        )

    @staticmethod
    def _result(ok, text, error=None, **metadata):
        return {"ok": bool(ok), "text": str(text), "error": error, "metadata": metadata}

    def _goals(self):
        result = self.goal_manager.list_goals()
        return result.get("metadata", {}).get("goals", []) if result.get("ok") else []

    def _find_task(self, task_id):
        for goal in self._goals():
            for task in goal.get("tasks", []):
                if task.get("id") == task_id:
                    return goal, task
        return None, None

    def _planner_next_task(self, goal_id):
        try:
            plan_id = self.planner.latest_plan_id()
            plan_result = self.planner.get_plan(plan_id) if plan_id else None
            plan = plan_result.get("metadata", {}).get("plan") if plan_result and plan_result.get("ok") else None
            if plan and plan.get("goal_id") == goal_id:
                return plan.get("analysis", {}).get("next_task")
        except RuntimeError:
            pass
        return None

    def _calculate(self, goal, task):
        goal_priority = str(goal.get("priority", "normal")).casefold()
        task_priority = str(task.get("priority", goal_priority)).casefold()
        status = str(task.get("status", "pending")).casefold()
        progress_result = self.progress_tracker.get_goal_progress(goal["id"])
        progress = progress_result.get("metadata", {}).get("progress", {})
        remaining = max(0.0, 100.0 - float(progress.get("percent", 0.0)))
        planner_next = self._planner_next_task(goal["id"])
        components = {
            "priority": self.PRIORITY_WEIGHTS.get(task_priority, self.PRIORITY_WEIGHTS["normal"]),
            "status": self.STATUS_WEIGHTS.get(status, self.STATUS_WEIGHTS["pending"]),
            "planner_next": 15 if planner_next == task.get("id") else 0,
            "remaining_progress": round(remaining / 10.0, 2),
        }
        score = round(sum(components.values()), 2)
        return {
            "task_id": task.get("id"), "goal_id": goal.get("id"),
            "title": task.get("title"), "status": status,
            "priority": task_priority, "score": score,
            "eligible": status not in {"completed", "cancelled"},
            "components": components,
        }

    def calculate_priority(self, task_id):
        goal, task = self._find_task(task_id)
        if task is None:
            return self._result(False, "Задача не найдена.", "TASK_NOT_FOUND", task_id=task_id)
        calculated = self._calculate(goal, task)
        return self._result(
            True, f"Приоритет задачи {task_id}: {calculated['score']}",
            task_id=task_id, goal_id=goal["id"], priority=calculated,
        )

    def get_prioritized_tasks(self, goal_id):
        goal_result = self.goal_manager.get_goal(goal_id)
        if not goal_result.get("ok"):
            return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
        goal = goal_result["metadata"]["goal"]
        tasks = [self._calculate(goal, task) for task in goal.get("tasks", [])]
        tasks.sort(key=lambda item: (-item["score"], str(item["task_id"])))
        return self._result(
            True, f"Приоритетный список задач: {len(tasks)}",
            goal_id=goal_id, tasks=tasks, count=len(tasks),
        )

    def next_task(self, goal_id):
        result = self.get_prioritized_tasks(goal_id)
        if not result.get("ok"):
            return result
        task = next(
            (item for item in result["metadata"]["tasks"] if item["eligible"]),
            None,
        )
        return self._result(
            True,
            f"Следующая задача: {task['task_id']}" if task else "Доступных задач нет.",
            goal_id=goal_id, task=task,
        )
