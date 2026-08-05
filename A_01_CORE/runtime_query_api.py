"""Read-only query facade for UI and future remote transports."""

from __future__ import annotations

from pathlib import Path

from .execution_journal import ExecutionJournal
from .resource_awareness import ResourceAwareness


class RuntimeQueryAPI:
    def __init__(self, root: Path | None = None, resources: ResourceAwareness | None = None):
        self.root = Path(root) if root else Path(__file__).resolve().parents[1]
        self.journal = ExecutionJournal(self.root)
        self.resources = resources or ResourceAwareness()

    def task(self, task_id: str) -> dict | None:
        value = self.journal.load(task_id)
        return value or None

    def tasks(self, state: str | None = None) -> list[dict]:
        values = self.journal.list_tasks()
        if state is not None:
            values = [item for item in values if item.get("final_status") == state]
        return values

    def status(self) -> dict:
        tasks = self.tasks()
        return {
            "resources": self.resources.snapshot().to_dict(),
            "tasks": {
                "total": len(tasks),
                "running": sum(item.get("final_status") == "running" for item in tasks),
                "failed": sum(item.get("final_status") in {"failed", "execution_error", "step_failed"} for item in tasks),
                "completed": sum(item.get("final_status") == "completed" for item in tasks),
            },
        }
