# -*- coding: utf-8 -*-
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "A_08_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "safety_gate_events.jsonl"

def log(event, **data):
    row = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        **data
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def create_snapshot():
    snap = ROOT / "create_snapshot.py"
    if snap.exists():
        r = subprocess.run([sys.executable, str(snap)], cwd=str(ROOT))
        log("snapshot_created", returncode=r.returncode)
        return r.returncode == 0
    log("snapshot_missing")
    return False

def backup_file(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p

    if not p.exists():
        log("backup_skipped_missing", file=str(p))
        return None

    bak = p.with_name(p.name + ".backup")
    shutil.copy2(p, bak)
    log("file_backup_created", file=str(p), backup=str(bak))
    return bak

def restore_backup(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p

    bak = p.with_name(p.name + ".backup")
    if not bak.exists():
        log("restore_failed_no_backup", file=str(p))
        return False

    shutil.copy2(bak, p)
    log("file_restored_from_backup", file=str(p), backup=str(bak))
    return True

def py_compile(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p

    if p.suffix.lower() != ".py":
        log("compile_skipped_not_python", file=str(p))
        return True

    r = subprocess.run(
        [sys.executable, "-m", "py_compile", str(p)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if r.returncode == 0:
        log("compile_ok", file=str(p))
        return True

    log("compile_failed", file=str(p), stderr=r.stderr)
    return False

def guarded_write(path, content):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p

    print("[SAFETY] Snapshot...")
    create_snapshot()

    print("[SAFETY] Backup...")
    backup_file(p)

    print("[SAFETY] Writing file...")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    log("file_written", file=str(p))

    print("[SAFETY] Compile check...")
    if not py_compile(p):
        print("[SAFETY] ERROR detected. Auto-restore from backup...")
        restore_backup(p)

        if py_compile(p):
            print("[SAFETY] AUTO-RESTORE OK")
            log("auto_restore_ok", file=str(p))
            return False

        print("[SAFETY] AUTO-RESTORE FAILED")
        log("auto_restore_failed", file=str(p))
        return False

    print("[SAFETY] WRITE OK")
    log("guarded_write_ok", file=str(p))
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("python A_01_CORE/safety_gate.py --protect <file>")
        print("python A_01_CORE/safety_gate.py --restore <file>")
        sys.exit(0)

    cmd = sys.argv[1]
    target = sys.argv[2]

    if cmd == "--protect":
        create_snapshot()
        backup_file(target)
    elif cmd == "--restore":
        restore_backup(target)
    else:
        print("Unknown command:", cmd)