import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FEEDER = ROOT / "A_01_CORE" / "task_feeder.py"
LOOP = ROOT / "A_01_CORE" / "execution_loop.py"
MONITOR = ROOT / "A_01_CORE" / "flow_monitor.py"

def start(name, path):
    print(f"[START] {name}: {path}")
    return subprocess.Popen(["python", str(path)])

if __name__ == "__main__":
    print("\n=== BUTLER SAFE LAUNCH KIT ===\n")

    p1 = start("FEEDER", FEEDER)
    time.sleep(1)

    p2 = start("LOOP", LOOP)
    time.sleep(1)

    p3 = start("MONITOR", MONITOR)

    print("\n[OK] ALL SYSTEMS ONLINE")
    print("[FLOW] INBOX → ACTIVE → LOOP → RUNNER → OUTBOX")

    p1.wait()
    p2.wait()
    p3.wait()
