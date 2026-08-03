import json
import time
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

INBOX = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "INBOX"
ACTIVE = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "ACTIVE"
LOGS = ROOT / "A_08_LOGS" / "FEEDER"

class TaskFeeder:

    def __init__(self):
        self.running = True
        LOGS.mkdir(parents=True, exist_ok=True)

    def log(self, msg):
        with open(LOGS / "feeder.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} | {msg}\n")

    def fetch_task(self):
        tasks = sorted(INBOX.glob("*.json"))
        if not tasks:
            return None
        return tasks[0]

    def move_to_active(self, task_file):
        ACTIVE.mkdir(parents=True, exist_ok=True)

        active_tasks = list(ACTIVE.glob("*.json"))
        if active_tasks:
            return False

        shutil.move(str(task_file), str(ACTIVE / task_file.name))
        self.log(f"MOVED: {task_file.name}")
        return True

    def run(self):
        print("[FEEDER] INBOX → ACTIVE STARTED")

        while self.running:
            task = self.fetch_task()

            if task:
                ok = self.move_to_active(task)
                if ok:
                    print(f"[FEEDER] TASK SENT TO ACTIVE: {task.name}")
                else:
                    print("[FEEDER] ACTIVE BUSY")
            else:
                time.sleep(1)


if __name__ == "__main__":
    TaskFeeder().run()
