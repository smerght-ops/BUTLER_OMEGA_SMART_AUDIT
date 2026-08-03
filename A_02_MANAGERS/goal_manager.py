# -*- coding: utf-8 -*-

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


class GoalManager:
    """CRUD manager for user goals stored in the existing memory subsystem."""

    NAME = "GOAL_MANAGER"
    name = "GOAL_MANAGER"

    def __init__(self, storage_path=None):
        project_root = Path(__file__).resolve().parents[1]
        self.storage_path = Path(storage_path) if storage_path else project_root / "A_07_MEMORY" / "goals_registry.json"
        self._lock = threading.RLock()
        self._ensure_storage()

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def _result(self, ok, text, error=None, **metadata):
        return {"ok": bool(ok), "text": str(text), "error": error, "metadata": metadata}

    def _ensure_storage(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._save({"version": "1.0", "goals": []})

    def _load(self):
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8-sig"))
            if not isinstance(data, dict) or not isinstance(data.get("goals"), list):
                raise ValueError("invalid goals registry")
            return data
        except Exception as exc:
            raise RuntimeError("GOALS_STORAGE_READ_ERROR") from exc

    def _save(self, data):
        temporary = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
        try:
            temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            temporary.replace(self.storage_path)
        except Exception as exc:
            if temporary.exists():
                temporary.unlink()
            raise RuntimeError("GOALS_STORAGE_WRITE_ERROR") from exc

    def _find(self, data, goal_id):
        return next((goal for goal in data["goals"] if goal.get("id") == goal_id), None)

    def _resolve_goal_id(self, reference):
        reference = str(reference or "").strip()
        data = self._load()
        direct = self._find(data, reference)
        if direct:
            return direct["id"]
        lowered = reference.casefold()
        match = next(
            (goal for goal in data["goals"] if str(goal.get("title", "")).casefold() == lowered),
            None,
        )
        return match.get("id") if match else reference

    def can_handle(self, query, context=None):
        command = str(query or "").strip().casefold()
        return any(command.startswith(prefix) for prefix in ("goal ", "plan ", "progress ", "priority ", "reminder "))

    def execute(self, query, context=None, **kwargs):
        started = perf_counter()
        command = str(query or "").strip()
        lowered = command.casefold()

        try:
            if lowered.startswith("reminder "):
                result = self._execute_reminder_command(command, lowered)
            elif lowered.startswith("priority "):
                result = self._execute_priority_command(command, lowered)
            elif lowered.startswith("progress "):
                result = self._execute_progress_command(command, lowered)
            elif lowered.startswith("plan "):
                result = self._execute_plan_command(command, lowered)
            elif lowered.startswith("goal create "):
                result = self.create_goal(command[len("goal create "):])
            elif lowered == "goal list":
                result = self.list_goals()
            elif lowered.startswith("goal get "):
                reference = command[len("goal get "):]
                result = self.get_goal(self._resolve_goal_id(reference))
            elif lowered.startswith("goal update "):
                reference = command[len("goal update "):]
                result = self.update_goal(self._resolve_goal_id(reference), {"status": "active"})
            elif lowered.startswith("goal add task "):
                task_title = command[len("goal add task "):]
                active = self.list_goals({"status": "active"})
                goals = active.get("metadata", {}).get("goals", [])
                if not goals:
                    result = self._result(False, "Активная цель не найдена.", "GOAL_NOT_FOUND")
                else:
                    result = self.add_task_to_goal(goals[-1]["id"], task_title)
            elif lowered.startswith("goal progress "):
                reference = command[len("goal progress "):]
                result = self.get_goal_progress(self._resolve_goal_id(reference))
            elif lowered.startswith("goal delete "):
                reference = command[len("goal delete "):]
                result = self.delete_goal(self._resolve_goal_id(reference))
            else:
                result = self._result(False, "Неизвестная команда цели.", "INVALID_GOAL_COMMAND")
        except RuntimeError as exc:
            result = self._result(False, "Не удалось обработать команду цели.", str(exc))

        return {
            "ok": bool(result.get("ok")),
            "department": self.NAME,
            "model": "GoalManager",
            "latency_ms": max(0, int((perf_counter() - started) * 1000)),
            "text": str(result.get("text") or ""),
            "error": result.get("error"),
            "metadata": dict(result.get("metadata") or {}),
        }

    def _execute_priority_command(self, command, lowered):
        from A_02_MANAGERS.priority_engine import PriorityEngine

        engine = PriorityEngine(goal_manager=self)
        if lowered.startswith("priority calculate "):
            reference = command[len("priority calculate "):].strip()
            if reference.casefold() == "latest":
                tasks = [task for goal in self._load()["goals"] for task in goal.get("tasks", [])]
                reference = tasks[-1]["id"] if tasks else ""
            return engine.calculate_priority(reference)
        if lowered.startswith("priority list "):
            reference = command[len("priority list "):].strip()
            return engine.get_prioritized_tasks(self._resolve_goal_id(reference))
        if lowered.startswith("priority next "):
            reference = command[len("priority next "):].strip()
            return engine.next_task(self._resolve_goal_id(reference))
        return self._result(False, "Неизвестная команда приоритета.", "INVALID_PRIORITY_COMMAND")

    def _execute_reminder_command(self, command, lowered):
        from A_02_MANAGERS.reminder_engine import ReminderEngine

        engine = ReminderEngine(goal_manager=self)
        if lowered.startswith("reminder set "):
            arguments = command[len("reminder set "):].split(maxsplit=2)
            if len(arguments) < 2:
                return self._result(False, "Не указаны target и due_at.", "INVALID_REMINDER_COMMAND")
            target, due_at = arguments[:2]
            message = arguments[2] if len(arguments) > 2 else ""
            tasks = [task for goal in self._load()["goals"] for task in goal.get("tasks", [])]
            task_id = tasks[-1]["id"] if target.casefold() == "latest" and tasks else target
            goal = next((goal for goal in self._load()["goals"] if any(task.get("id") == task_id for task in goal.get("tasks", []))), None)
            if goal is None:
                return self._result(False, "Задача не найдена.", "TASK_NOT_FOUND", task_id=task_id)
            return engine.set_reminder(goal["id"], due_at, task_id=task_id, message=message)
        if lowered == "reminder list":
            return engine.list_reminders()
        if lowered == "reminder check":
            return engine.check_reminders()
        if lowered.startswith("reminder acknowledge "):
            reference = command[len("reminder acknowledge "):].strip()
            reminder_id = engine.latest_reminder_id() if reference.casefold() == "latest" else reference
            return engine.acknowledge_reminder(reminder_id or "")
        return self._result(False, "Неизвестная команда напоминания.", "INVALID_REMINDER_COMMAND")

    def _execute_plan_command(self, command, lowered):
        from A_02_MANAGERS.Planner.planner_manager import PlannerManager

        planner = PlannerManager(goal_manager=self)
        if lowered.startswith("plan generate "):
            reference = command[len("plan generate "):]
            return planner.generate_plan(self._resolve_goal_id(reference))
        if lowered.startswith("plan get "):
            reference = command[len("plan get "):].strip()
            plan_id = planner.latest_plan_id() if reference.casefold() == "latest" else reference
            return planner.get_plan(plan_id or "")
        if lowered.startswith("plan optimize "):
            reference = command[len("plan optimize "):].strip()
            plan_id = planner.latest_plan_id() if reference.casefold() == "latest" else reference
            return planner.optimize_plan(plan_id or "")
        return self._result(False, "Неизвестная команда планирования.", "INVALID_PLAN_COMMAND")

    def _execute_progress_command(self, command, lowered):
        from A_02_MANAGERS.progress_tracker import ProgressTracker

        tracker = ProgressTracker(goal_manager=self)
        if lowered.startswith("progress update "):
            arguments = command[len("progress update "):].rsplit(maxsplit=1)
            if len(arguments) != 2:
                return self._result(False, "Не указаны task_id и status.", "INVALID_PROGRESS_COMMAND")
            task_id, status = arguments
            if task_id.casefold() == "latest":
                goals = self._load()["goals"]
                tasks = [task for goal in goals for task in goal.get("tasks", [])]
                task_id = tasks[-1]["id"] if tasks else ""
            return tracker.update_task_status(task_id, status)
        if lowered.startswith("progress get "):
            reference = command[len("progress get "):]
            return tracker.get_goal_progress(self._resolve_goal_id(reference))
        if lowered.startswith("progress timeline "):
            reference = command[len("progress timeline "):]
            return tracker.get_timeline(self._resolve_goal_id(reference))
        return self._result(False, "Неизвестная команда прогресса.", "INVALID_PROGRESS_COMMAND")

    def create_goal(self, title, description="", priority="normal"):
        title = str(title or "").strip()
        if not title:
            return self._result(False, "Название цели не указано.", "INVALID_GOAL_TITLE")
        with self._lock:
            try:
                data = self._load()
                goal_id = "goal_" + uuid.uuid4().hex[:12]
                now = self._now()
                goal = {"id": goal_id, "title": title, "description": str(description or "").strip(),
                        "priority": str(priority or "normal"), "status": "active", "tasks": [],
                        "created_at": now, "updated_at": now}
                data["goals"].append(goal)
                self._save(data)
                return self._result(True, f"Цель создана: {title}", goal_id=goal_id, goal=goal)
            except RuntimeError as exc:
                return self._result(False, "Не удалось создать цель.", str(exc))

    def get_goal(self, goal_id):
        with self._lock:
            try:
                goal = self._find(self._load(), goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                return self._result(True, f"Цель найдена: {goal['title']}", goal=goal, goal_id=goal_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось прочитать цель.", str(exc), goal_id=goal_id)

    def update_goal(self, goal_id, updates):
        allowed = {"title", "description", "priority", "status"}
        if not isinstance(updates, dict) or not updates:
            return self._result(False, "Изменения цели не указаны.", "INVALID_GOAL_UPDATES", goal_id=goal_id)
        changes = {key: value for key, value in updates.items() if key in allowed}
        if not changes or ("title" in changes and not str(changes["title"] or "").strip()):
            return self._result(False, "Допустимые изменения цели не указаны.", "INVALID_GOAL_UPDATES", goal_id=goal_id)
        with self._lock:
            try:
                data = self._load(); goal = self._find(data, goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                goal.update(changes); goal["updated_at"] = self._now(); self._save(data)
                return self._result(True, "Цель обновлена.", goal=goal, goal_id=goal_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось обновить цель.", str(exc), goal_id=goal_id)

    def delete_goal(self, goal_id):
        with self._lock:
            try:
                data = self._load(); goal = self._find(data, goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                data["goals"].remove(goal); self._save(data)
                return self._result(True, "Цель удалена.", goal_id=goal_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось удалить цель.", str(exc), goal_id=goal_id)

    def list_goals(self, filter=None):
        with self._lock:
            try:
                goals = list(self._load()["goals"])
                filters = filter if isinstance(filter, dict) else ({"status": filter} if filter else {})
                for key, value in filters.items():
                    goals = [goal for goal in goals if goal.get(key) == value]
                return self._result(True, f"Найдено целей: {len(goals)}", goals=goals, count=len(goals), filter=filters)
            except RuntimeError as exc:
                return self._result(False, "Не удалось получить список целей.", str(exc), goals=[], count=0)

    def add_task_to_goal(self, goal_id, task):
        title = task.get("title") if isinstance(task, dict) else task
        title = str(title or "").strip()
        if not title:
            return self._result(False, "Название задачи не указано.", "INVALID_TASK", goal_id=goal_id)
        with self._lock:
            try:
                data = self._load(); goal = self._find(data, goal_id)
                if goal is None:
                    return self._result(False, "Цель не найдена.", "GOAL_NOT_FOUND", goal_id=goal_id)
                task_id = "task_" + uuid.uuid4().hex[:12]
                item = dict(task) if isinstance(task, dict) else {"title": title}
                item.update({"id": task_id, "title": title, "status": item.get("status", "pending"), "created_at": self._now()})
                goal["tasks"].append(item); goal["updated_at"] = self._now(); self._save(data)
                return self._result(True, f"Задача добавлена: {title}", goal_id=goal_id, task_id=task_id, task=item)
            except RuntimeError as exc:
                return self._result(False, "Не удалось добавить задачу.", str(exc), goal_id=goal_id)

    def update_task_status(self, task_id, status):
        normalized = str(status or "").strip().lower()
        if normalized not in {"pending", "in_progress", "completed", "cancelled"}:
            return self._result(False, "Недопустимый статус задачи.", "INVALID_TASK_STATUS", task_id=task_id)
        with self._lock:
            try:
                data = self._load()
                for goal in data["goals"]:
                    task = next((item for item in goal.get("tasks", []) if item.get("id") == task_id), None)
                    if task is None:
                        continue
                    now = self._now()
                    task["status"] = normalized
                    task["updated_at"] = now
                    if normalized == "completed":
                        task["completed_at"] = now
                    else:
                        task.pop("completed_at", None)
                    goal["updated_at"] = now
                    self._save(data)
                    return self._result(True, f"Статус задачи обновлён: {normalized}", goal_id=goal.get("id"), task_id=task_id, task=task)
                return self._result(False, "Задача не найдена.", "TASK_NOT_FOUND", task_id=task_id)
            except RuntimeError as exc:
                return self._result(False, "Не удалось обновить статус задачи.", str(exc), task_id=task_id)

    def get_goal_progress(self, goal_id):
        result = self.get_goal(goal_id)
        if not result["ok"]:
            return result
        tasks = result["metadata"]["goal"].get("tasks", [])
        total = len(tasks); completed = sum(1 for task in tasks if task.get("status") == "completed")
        percent = round(completed * 100 / total, 2) if total else 0.0
        return self._result(True, f"Прогресс цели: {percent}%", goal_id=goal_id,
                            progress={"total": total, "completed": completed, "percent": percent})
