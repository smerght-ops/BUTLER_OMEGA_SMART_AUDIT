from pathlib import Path
import json

ARTIFACT_KEYWORDS = ["__pycache__", ".bak", ".before_", ".broken_", ".tmp"]

COMMAND_HINTS = ["run", "execute", "dispatch", "move", "process"]
DATA_HINTS = ["json", "txt", "md", "csv", "log"]

class SemanticLayer:

    def classify(self, file_path: str) -> dict:
        p = Path(file_path)

        name = p.name.lower()
        full = str(p).lower()

        # 1. мусор / технические файлы
        for k in ARTIFACT_KEYWORDS:
            if k in name or k in full:
                return {
                    "type": "artifact",
                    "route": "ARCHIVE",
                    "reason": "system_artifact_detected"
                }

        # 2. python / execution
        if name.endswith(".py"):
            return {
                "type": "command",
                "route": "RUNNER",
                "reason": "python_execution_unit"
            }

        # 3. json task (фабрика задач)
        if name.endswith(".json"):
            return {
                "type": "data",
                "route": "DISPATCHER",
                "reason": "task_data"
            }

        # 4. текст / память
        if name.endswith((".txt", ".md")):
            return {
                "type": "memory",
                "route": "REVIEW",
                "reason": "text_memory"
            }

        # fallback
        return {
            "type": "unknown",
            "route": "QUARANTINE",
            "reason": "unclassified"
        }
