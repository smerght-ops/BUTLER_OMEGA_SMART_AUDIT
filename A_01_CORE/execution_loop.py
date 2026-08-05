from pathlib import Path
import json
import time

ROOT = Path(__file__).resolve().parents[1]

ACTIVE = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "ACTIVE"
OUTBOX = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "OUTBOX"

class ExecutionLoop:

    def __init__(self):
        self.running = True

    def fetch_task(self):
        tasks = list(ACTIVE.glob("*.json"))
        if not tasks:
            return None

        task_file = tasks[0]

        try:
            data = json.loads(task_file.read_text(encoding="utf-8-sig"))
        except Exception:
            data = {"task_id": task_file.stem}

        task_file.unlink()  # уб из ACTIVE (поглощение задачи)

        return data

    def execute(self, task):
        task_id = task.get("task_id", "unknown")

        # пока stub выполнения (позже подключим RUNNER)
        result = {
            "task_id": task_id,
            "status": "done"
        }


        # LOG EVENT (LAYER 2)
        try:
            from datetime import datetime
            log_path = ROOT / "A_08_LOGS" / "system_events.jsonl"
            with open(log_path, "a", encoding="utf-8") as f:
                f.write('{"event":"task_executed","task_id":"' + str(task_id) + '"}\n')
        except:
            pass

        OUTBOX.mkdir(parents=True, exist_ok=True)
        out_file = OUTBOX / f"{task_id}_result.json"
        out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        return result

    def run(self, delay=1):

        print("[LOOP] CONNECTED TO DISPATCHER")

        while self.running:

            task = self.fetch_task()

            if task:
                print("[LOOP] TASK:", task.get("task_id"))
                self.execute(task)
            else:
                time.sleep(delay)






if __name__ == "__main__":
    loop = ExecutionLoop()
    loop.run()
