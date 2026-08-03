# -*- coding: utf-8 -*-

from A_02_MANAGERS.Planner.planner_manager import PlannerManager
from A_02_MANAGERS.goal_manager import GoalManager


class ProgressTracker:
    """Orchestration facade for goal progress and its read-only timeline."""

    def __init__(self, goal_manager=None, planner=None):
        self.goal_manager = goal_manager or GoalManager()
        self.planner = planner or PlannerManager(goal_manager=self.goal_manager)

    def _result(self, ok, text, error=None, **metadata):
        return {"ok": bool(ok), "text": str(text), "error": error, "metadata": metadata}

    def update_task_status(self, task_id, status):
        return self.goal_manager.update_task_status(task_id, status)

    def get_goal_progress(self, goal_id):
        return self.goal_manager.get_goal_progress(goal_id)

    def get_timeline(self, goal_id):
        goal_result = self.goal_manager.get_goal(goal_id)
        if not goal_result.get("ok"):
            return self._result(False, "Не удалось построить timeline: цель не найдена.", goal_result.get("error"), goal_id=goal_id)

        goal = goal_result["metadata"]["goal"]
        events = []
        self._append(events, goal.get("created_at"), "goal_created", goal_id=goal_id)
        for task in goal.get("tasks", []):
            details = {"goal_id": goal_id, "task_id": task.get("id"), "status": task.get("status")}
            self._append(events, task.get("created_at"), "task_created", **details)
            self._append(events, task.get("updated_at"), "task_status_updated", **details)
            self._append(events, task.get("completed_at"), "task_completed", **details)

        try:
            latest_id = self.planner.latest_plan_id()
            latest = self.planner.get_plan(latest_id) if latest_id else None
            plan = latest.get("metadata", {}).get("plan") if latest and latest.get("ok") else None
            if plan and plan.get("goal_id") == goal_id:
                self._append(events, plan.get("created_at"), "plan_created", goal_id=goal_id, plan_id=plan.get("id"))
                if int(plan.get("revision", 1)) > 1:
                    self._append(events, plan.get("updated_at"), "plan_optimized", goal_id=goal_id, plan_id=plan.get("id"), revision=plan.get("revision"))
        except RuntimeError:
            pass

        self._append(events, goal.get("updated_at"), "goal_updated", goal_id=goal_id, status=goal.get("status"))
        events.sort(key=lambda item: item["timestamp"])
        return self._result(True, f"Timeline событий: {len(events)}", goal_id=goal_id, timeline=events, count=len(events))

    @staticmethod
    def _append(events, timestamp, event, **details):
        if timestamp:
            events.append({"timestamp": timestamp, "event": event, **details})
