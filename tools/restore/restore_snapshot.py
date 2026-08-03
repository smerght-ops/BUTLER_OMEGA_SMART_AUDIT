import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(".").resolve()
ARCH = ROOT / "A_00_ARCHITECTURE"
SNAP = ARCH / "SNAPSHOTS"

FILES = [
    "PROJECT_STATE.json",
    "ARCHITECTURE_LOCK.json",
    "ARCHITECTURE_LOCK.backup.json",
    "INVARIANTS.json",
    "CONSTITUTION.md",
]

def list_snapshots():
    folders = sorted(
        [x.name for x in SNAP.iterdir() if x.is_dir()],
        reverse=True
    )

    print("=" * 50)
    print("AVAILABLE SNAPSHOTS")
    print("=" * 50)

    if not folders:
        print("Нет доступных snapshot.")
        return

    for f in folders:
        print(f)

def restore(name):
    src = SNAP / name

    if not src.exists():
        print(f"❌ Snapshot '{name}' не найден.")
        sys.exit(1)

    print("=" * 50)
    print("RESTORING SNAPSHOT")
    print("=" * 50)

    for fn in FILES:
        s = src / fn
        d = ARCH / fn
        if s.exists():
            shutil.copy2(s, d)
            print(f"✓ {fn}")

    print()
    print("Переподписание PROJECT_STATE...")

    subprocess.run(
        ["python", "A_01_CORE/project_state_builder.py", "--approve"],
        check=True
    )

    print()
    print("Самопроверка Guardian...")

    subprocess.run(
        ["python", "RUN_PIPELINE_V12.py", "--self-test"],
        check=True
    )

    print()
    print("=" * 50)
    print("✓ RESTORE COMPLETED")
    print("=" * 50)

if __name__ == "__main__":

    if "--list" in sys.argv:
        list_snapshots()
        sys.exit(0)

    if "--restore" in sys.argv:

        idx = sys.argv.index("--restore")

        if idx + 1 >= len(sys.argv):
            print("Укажите имя snapshot.")
            sys.exit(1)

        restore(sys.argv[idx + 1])
        sys.exit(0)

    print("Использование:")
    print("python restore_snapshot.py --list")
    print("python restore_snapshot.py --restore snapshot_YYYYMMDD_HHMMSS")