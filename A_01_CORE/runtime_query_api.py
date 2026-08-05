"""Read-only query facade for UI and future remote transports."""

from __future__ import annotations

from pathlib import Path
import json

from .execution_journal import ExecutionJournal
from .resource_awareness import ResourceAwareness


class RuntimeQueryAPI:
    def __init__(self, root: Path | None = None, resources: ResourceAwareness | None = None):
        self.root = Path(root) if root else Path(__file__).resolve().parents[1]
        self.journal = ExecutionJournal(self.root, create=False)
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

    @staticmethod
    def _json_lines(path: Path, limit: int = 100) -> list[dict]:
        if not path.is_file():
            return []
        values = []
        for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines()[-limit:]:
            try:
                value = json.loads(line)
            except (ValueError, TypeError):
                continue
            if isinstance(value, dict):
                values.append(value)
        return values

    def skills(self) -> dict:
        records = self._json_lines(self.root / "A_07_MEMORY" / "MEMORY_INDEX.jsonl", limit=5000)
        events = [item for item in records if item.get("type") in {"skill", "skill_telemetry"}]
        return {
            "active": sum(item.get("status") == "ACTIVE" for item in events),
            "candidates": sum(item.get("status") == "CANDIDATE" for item in events),
            "telemetry_events": sum(item.get("type") == "skill_telemetry" for item in events),
        }

    def memory(self) -> dict:
        records = self._json_lines(self.root / "A_07_MEMORY" / "MEMORY_INDEX.jsonl", limit=5000)
        return {
            "records": len(records),
            "knowledge": sum(item.get("type") == "knowledge" for item in records),
            "needs_review": sum(bool(item.get("needs_review")) for item in records),
        }

    def workspace_files(self, limit: int = 100) -> list[dict]:
        workspace = self.root / "A_06_WORKSPACE"
        if not workspace.is_dir():
            return []
        values = []
        for path in sorted(workspace.iterdir(), key=lambda item: item.name.casefold())[:limit]:
            try:
                stat = path.stat()
            except OSError:
                continue
            values.append({"name": path.name, "kind": "directory" if path.is_dir() else "file", "size": stat.st_size})
        return values

    def observations(self, limit: int = 50) -> list[dict]:
        return self._json_lines(self.root / "A_08_LOGS" / "OBSERVATIONS.jsonl", limit=limit)

    def logs(self, limit: int = 50) -> list[dict]:
        log_dir = self.root / "A_08_LOGS"
        if not log_dir.is_dir():
            return []
        values = []
        for path in sorted(log_dir.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)[:limit]:
            stat = path.stat()
            values.append({"name": path.name, "size": stat.st_size, "modified": stat.st_mtime})
        return values

    def dashboard(self) -> dict:
        status = self.status()
        tasks = self.tasks()
        return {
            "conversation": {"available": False, "message": "Conversation state is owned by AgentCoreCoordinator."},
            "voice": {"available": (self.root / "A_09_INTERFACE" / "voice_input.py").is_file()},
            "runtime": status,
            "tasks": tasks[-50:],
            "council": {"available": (self.root / "A_01_CORE" / "council_runtime.py").is_file()},
            "models": status["resources"]["services"],
            "memory": self.memory(),
            "skills": self.skills(),
            "files": self.workspace_files(),
            "permissions": self.observations(),
            "logs": self.logs(),
            "results": [item for item in tasks[-50:] if item.get("final_status") == "completed"],
        }
