# -*- coding: utf-8 -*-
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from A_02_MANAGERS.smart_dispatcher import get_chat_provider
from A_01_CORE.safety_gate import guarded_write

SANDBOX = ROOT / "A_00_AVARIYKA" / "SELF_HEALING_SANDBOX"
LOGS = SANDBOX / "LOGS"
TARGET = SANDBOX / "target_task.py"

LOGS.mkdir(parents=True, exist_ok=True)

BROKEN = """
print("START")
print(broken_variable_trigger_error)
"""

TARGET.write_text(BROKEN.strip() + "\n", encoding="utf-8")

dispatcher = get_chat_provider(ROOT)

for attempt in range(1, 4):

    print(f"[TRY {attempt}]")

    p = subprocess.run(
        [sys.executable, str(TARGET)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    (LOGS / "last_stdout.log").write_text(p.stdout or "", encoding="utf-8")
    (LOGS / "last_stderr.log").write_text(p.stderr or "", encoding="utf-8")

    if p.returncode == 0:
        print("[SUCCESS]")
        sys.exit(0)

    current = TARGET.read_text(encoding="utf-8")

    dto = dispatcher.execute_employee(
        employee="coder",
        system_prompt="Исправь Python-код. Верни только готовый код без markdown.",
        user_content=f"ERROR:\n{p.stderr}\n\nCODE:\n{current}",
        has_image=False
    )

    if dto.get("status") != "ok":
        print(dto)
        sys.exit(1)

    fixed = dto.get("text", "")
    fixed = fixed.replace("```python", "").replace("```", "").strip()

    TARGET.write_text(fixed + "\n", encoding="utf-8")

print("[FAILED AFTER 3 ATTEMPTS]")
sys.exit(1)
