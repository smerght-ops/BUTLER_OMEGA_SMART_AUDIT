# -*- coding: utf-8 -*-

"""Request-driven reminder orchestration over existing Goal/Task managers."""

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from A_02_MANAGERS.Planner.planner_manager import PlannerManager
from A_02_MANAGERS.goal_manager import GoalManager
from A_02_MANAGERS.priority_engine import PriorityEngine
from A_02_MANAGERS.progress_tracker import ProgressTracker


class ReminderEngine:
    """Persist and check reminders without scheduling or executing tasks."""

    def __init__(self, storage_path=None, goal_manager=None, planner=None,
                 progress_tracker=None, priority_engine=None):
        root = Path(__file__).resolve().parents[1]
        self.storage_path = Path(storage_path) if storage_path else root / "A_07_MEMORY" / "reminders_registry.json"
        self.goal_manager = goal_manager or GoalManager()
        self.planner = planner or PlannerManager(goal_manager=self.goal_manager)
        self.progress_tracker = progress_tracker or ProgressTracker(
            goal_manager=self.goal_manager, planner=self.planner
        )
        self.priority_engine = priority_engine or PriorityEngine(
            goal_manager=self.goal_manager, planner=self.planner,
            progress_tracker=self.progress_tracker,
        )
        self._lock = threading.RLock()
        self._ensure_storage()

    @staticmethod
    def _result(ok, text, error=None, **metadata):
        return {"ok": bool(ok), "text": str(text), "error": error, "metadata": metadata}

    @staticmethod
    def _now():
        return datetime.now(timezone.utc)

    @classmethod
    def _parse_datetime(cls, value):
        if isinstance(value, datetime):
            parsed = value
        elif str(value or "").strip().casefold() == "now":
            parsed = cls._now()
        else:
            parsed = datetime.fromisoformat(str(value or "").strip().replace("Z", "+00:00"))
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)

    def _ensure_storage(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._save({"version": "1.0", "reminders": []})

    def _load(self):
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8-sig"))
            if not isinstance(data, dict) or not isinstance(data.get("reminders"), list):
                raise ValueError("invalid reminders registry")
            return data
        except Exception as exc:
            raise RuntimeError("REMINDERS_STORAGE_READ_ERROR") from exc

    def _save(self, data):
        temporary = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
        try:
            temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(self.storage_path)
        except Exception as exc:
            if temporary.exists():
                temporary.unlink()
            raise RuntimeError("REMINDERS_STORAGE_WRITE_ERROR") from exc

    def _goal_and_task(self, goal_id, task_id):
        goal_result = self.goal_manager.get_goal(goal_id)
        if not goal_result.get("ok"):
            return None, None
        goal = goal_result["metadata"]["goal"]
        task = next((item for item in goal.get("tasks", []) if item.get("id") == task_id), None) if task_id else None
        return goal, task

    def _planner_snapshot(self, goal_id):
        try:
            plan_id = self.planner.latest_plan_id()
            result = self.planner.get_plan(plan_id) if plan_id else None
            plan = result.get("metadata", {}).get("plan") if result and result.get("ok") else None
            return plan_id if plan and plan.get("goal_id") == goal_id else None
        except RuntimeError:
            return None

    def set_reminder(self, goal_id, due_at, task_id=None, message=""):
        try:
            due = self._parse_datetime(due_at)
        except (TypeError, ValueError):
            return self._result(False, "Некорректная дата напоминания.", "INVALID_REMINDER_DATETIME")
        goal, task = self._goal_and_task(goal_id, task_id)
        if goal is None:
            return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
        if task_id and task is None:
            return self._result(False, "Задача не найдена.", "TASK_NOT_FOUND", goal_id=goal_id, task_id=task_id)
        priority = self.priority_engine.calculate_priority(task_id) if task_id else self.priority_engine.next_task(goal_id)
        progress = self.progress_tracker.get_goal_progress(goal_id)
        now = self._now().isoformat()
        reminder = {
            "id": "reminder_" + uuid.uuid4().hex[:12], "goal_id": goal_id,
            "task_id": task_id, "due_at": due.isoformat(),
            "message": str(message or "").strip(), "status": "pending",
            "created_at": now, "updated_at": now,
            "context": {
                "plan_id": self._planner_snapshot(goal_id),
                "progress": progress.get("metadata", {}).get("progress"),
                "priority": priority.get("metadata", {}).get("priority") or priority.get("metadata", {}).get("task"),
            },
        }
        with self._lock:
            data = self._load(); data["reminders"].append(reminder); self._save(data)
        return self._result(True, f"Напоминание создано: {reminder['id']}", reminder_id=reminder["id"], reminder=reminder)

    def list_reminders(self, goal_id=None, task_id=None, status=None):
        with self._lock:
            reminders = list(self._load()["reminders"])
        if goal_id:
            reminders = [item for item in reminders if item.get("goal_id") == goal_id]
        if task_id:
            reminders = [item for item in reminders if item.get("task_id") == task_id]
        if status:
            reminders = [item for item in reminders if item.get("status") == status]
        reminders.sort(key=lambda item: (item.get("due_at", ""), item.get("id", "")))
        return self._result(True, f"Напоминаний: {len(reminders)}", reminders=reminders, count=len(reminders))

    def check_reminders(self, now=None):
        try:
            current = self._parse_datetime(now or self._now())
        except (TypeError, ValueError):
            return self._result(False, "Некорректное время проверки.", "INVALID_REMINDER_DATETIME")
        listed = self.list_reminders(status="pending")["metadata"]["reminders"]
        due = [item for item in listed if self._parse_datetime(item["due_at"]) <= current]
        due.sort(key=lambda item: (item.get("due_at", ""), item.get("id", "")))
        return self._result(True, f"Активных напоминаний: {len(due)}", checked_at=current.isoformat(), reminders=due, count=len(due))

    def acknowledge_reminder(self, reminder_id):
        with self._lock:
            data = self._load()
            reminder = next((item for item in data["reminders"] if item.get("id") == reminder_id), None)
            if reminder is None:
                return self._result(False, "Напоминание не найдено.", "REMINDER_NOT_FOUND", reminder_id=reminder_id)
            now = self._now().isoformat()
            reminder.update({"status": "acknowledged", "acknowledged_at": now, "updated_at": now})
            self._save(data)
        return self._result(True, f"Напоминание подтверждено: {reminder_id}", reminder_id=reminder_id, reminder=reminder)

    def latest_reminder_id(self):
        with self._lock:
            reminders = self._load()["reminders"]
        return reminders[-1]["id"] if reminders else None
