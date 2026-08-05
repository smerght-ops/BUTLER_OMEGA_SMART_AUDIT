"""Single append-safe persistence boundary for task execution state."""

from __future__ import annotations

import json
from pathlib import Path


class ExecutionJournal:
    def __init__(self, root: Path, create: bool = True):
        self.directory = Path(root) / "A_05_STORAGE" / "tasks"
        if create:
            self.directory.mkdir(parents=True, exist_ok=True)

    def path_for(self, task_id: str) -> Path:
        return self.directory / f"{task_id}.json"

    def load(self, task_id: str) -> dict:
        try:
            value = json.loads(self.path_for(task_id).read_text(encoding="utf-8-sig"))
            return value if isinstance(value, dict) else {}
        except (OSError, ValueError, TypeError):
            return {}

    def write(self, task_id: str, payload: dict, default=None) -> Path:
        path = self.path_for(task_id)
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, default=default) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
        return path

    def list_tasks(self) -> list[dict]:
        tasks = []
        for path in sorted(self.directory.glob("task_*.json")):
            try:
                value = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError, TypeError):
                continue
            if isinstance(value, dict):
                tasks.append(value)
        return tasks
