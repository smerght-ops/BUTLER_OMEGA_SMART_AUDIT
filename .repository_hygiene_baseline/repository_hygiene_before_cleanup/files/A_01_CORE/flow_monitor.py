import os
import time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

INBOX = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "INBOX"
ACTIVE = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "ACTIVE"
OUTBOX = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY" / "02_ENGINEERS" / "Text_Department" / "OUTBOX"

def count(p):
    try:
        return len(list(p.glob("*.json")))
    except:
        return 0

def draw():
    os.system("cls")

    inbox = count(INBOX)
    active = count(ACTIVE)
    outbox = count(OUTBOX)

    print("=" * 50)
    print(" BUTLER OMEGA FLOW MONITOR")
    print("=" * 50)
    print(f"INBOX : {inbox}")
    print(f"ACTIVE: {active}")
    print(f"OUTBOX: {outbox}")
    print("=" * 50)
    print("TIME:", datetime.now().strftime("%H:%M:%S"))
    print("=" * 50)

if __name__ == "__main__":
    while True:
        draw()
        time.sleep(1)
