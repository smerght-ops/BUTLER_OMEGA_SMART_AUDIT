# -*- coding: utf-8 -*-

import json
from pathlib import Path
from datetime import datetime


class ExecutionRegistry:
    """Single Source of Truth для верификации реальности выполненных задач."""

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]
        self.path = self.project_root / "A_07_CONFIG" / "execution_registry.json"

    def load(self) -> dict:
        if not self.path.exists():
            return {"tasks": {}, "phases": {}}
        try:
            return json.loads(self.path.read_text(encoding="utf-8-sig"))
        except Exception:
            return {"tasks": {}, "phases": {}}

    def save(self, data: dict):
        try:
            data["last_update"] = datetime.now().isoformat()
            self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    def mark_done(self, phase: str, task: str) -> str:
        data = self.load()
        key = f"{phase.strip().upper()}::{task.strip().upper()}"
        data["tasks"][key] = {
            "status": "DONE",
            "timestamp": datetime.now().isoformat()
        }
        self.save(data)
        return key

    def is_done(self, phase: str, task: str) -> bool:
        data = self.load()
        key = f"{phase.strip().upper()}::{task.strip().upper()}"
        return key in data["tasks"]
