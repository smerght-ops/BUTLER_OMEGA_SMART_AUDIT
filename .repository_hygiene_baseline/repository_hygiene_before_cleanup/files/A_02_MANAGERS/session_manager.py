# -*- coding: utf-8 -*-
import json
from pathlib import Path


class ButlerSessionManager:

    def __init__(self, project_root=None):
        if project_root is None:
            self.root = Path(__file__).resolve().parent.parent
        else:
            self.root = Path(project_root)

        self.storage_dir = self.root / "A_05_STORAGE"
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.history_file = self.storage_dir / "session_history.jsonl"

    def append(self, role: str, text: str):
        payload = {
            "role": role,
            "text": str(text).replace("\n", " ")
        }

        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def get_recent(self, limit=12):
        if not self.history_file.exists():
            return ""

        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()[-limit:]

            result = []

            for line in lines:
                if not line.strip():
                    continue

                obj = json.loads(line)

                if obj.get("role") == "user":
                    who = "Пользователь"
                else:
                    who = "Ассистент"

                result.append(f"{who}: {obj.get('text','')}")

            return "\n".join(result)

        except Exception:
            return ""

    def get_events(self, limit=12):
        if not self.history_file.exists():
            return []

        try:
            events = []
            with open(self.history_file, "r", encoding="utf-8") as f:
                lines = f.readlines()[-limit:]
            for line in lines:
                if not line.strip():
                    continue
                payload = json.loads(line)
                events.append({
                    "time": payload.get("time"),
                    "event": payload.get("text", ""),
                    "role": payload.get("role", "assistant"),
                })
            return events
        except Exception:
            return []

    def clear(self):
        if self.history_file.exists():
            self.history_file.unlink()
