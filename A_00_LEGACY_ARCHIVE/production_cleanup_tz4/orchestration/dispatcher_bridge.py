from pathlib import Path
import shutil
import json

ROOT = Path(__file__).resolve().parents[1]

INBOX = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "INBOX"
ACTIVE = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "ACTIVE"
LOGS = ROOT / "A_08_LOGS"

class DispatcherBridge:

    def __init__(self):
        INBOX.mkdir(parents=True, exist_ok=True)
        ACTIVE.mkdir(parents=True, exist_ok=True)
        LOGS.mkdir(parents=True, exist_ok=True)

    def log(self, msg):
        with open(LOGS / "dispatcher.log", "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    def fetch_task(self):
        tasks = list(INBOX.glob("*.json"))

        if not tasks:
            return None

        task_file = tasks[0]

        try:
            data = json.loads(task_file.read_text(encoding="utf-8-sig"))
            task_id = data.get("task_id", task_file.stem)
        except Exception:
            task_id = task_file.stem

        shutil.move(str(task_file), str(ACTIVE / task_file.name))

        self.log(f"DISPATCHED: {task_id}")

        return {
            "task_id": task_id,
            "file": str(ACTIVE / task_file.name)
        }
