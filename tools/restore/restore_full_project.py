from pathlib import Path
import shutil
import subprocess
import sys
import datetime

ROOT = Path(__file__).resolve().parent
ROLLBACK_ROOT = ROOT / "A_00_HISTORY" / "ROLLBACK_POINTS"

FOLDERS = [
    "A_00_ARCHITECTURE",
    "A_00_AVARIYKA",
    "A_01_CORE",
    "A_02_MANAGERS",
    "A_03_ORCHESTRATION",
    "A_04_AGENTS",
    "A_05_STORAGE",
    "A_07_CONFIG",
]

def latest_rollback():
    points = sorted(
        [p for p in ROLLBACK_ROOT.iterdir() if p.is_dir() and p.name.startswith("AUTO_")],
        key=lambda p: p.name
    )
    if not points:
        print("ERROR: no AUTO rollback points found")
        sys.exit(1)
    return points[-1]

def compile_python():
    targets = []
    for folder in ["A_01_CORE", "A_02_MANAGERS", "A_03_ORCHESTRATION", "A_04_AGENTS"]:
        root = ROOT / folder
        if root.exists():
            targets.extend(root.rglob("*.py"))

    failed = 0
    for f in targets:
        r = subprocess.run(
            [sys.executable, "-m", "py_compile", str(f)],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        if r.returncode != 0:
            failed += 1
            print("COMPILE ERROR:", f)

    if failed:
        print("RESTORE CHECK FAILED:", failed, "compile errors")
        sys.exit(2)

    print("COMPILE CHECK OK")

def restore(dry_run=True):
    point = latest_rollback()

    print("=" * 60)
    print("BUTLER FULL RESTORE BUTTON")
    print("ROLLBACK:", point)
    print("MODE:", "DRY-RUN" if dry_run else "RESTORE")
    print("=" * 60)

    if dry_run:
        for name in FOLDERS:
            src = point / name
            print(("OK   " if src.exists() else "MISS "), name)
        print("=" * 60)
        print("DRY-RUN COMPLETE. NO FILES CHANGED.")
        print("=" * 60)
        return

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    emergency = ROOT / "A_00_HISTORY" / "EMERGENCY_BEFORE_RESTORE" / stamp
    emergency.mkdir(parents=True, exist_ok=True)

    for name in FOLDERS:
        cur = ROOT / name
        src = point / name

        if cur.exists():
            shutil.copytree(cur, emergency / name, dirs_exist_ok=True)

        if src.exists():
            if cur.exists():
                shutil.rmtree(cur)
            shutil.copytree(src, cur)
            print("RESTORED:", name)

    compile_python()

    print("=" * 60)
    print("FULL RESTORE COMPLETE")
    print("EMERGENCY COPY:", emergency)
    print("=" * 60)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    restore(dry_run=(mode != "--restore"))
