from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
ARCH = ROOT / "A_00_ARCHITECTURE"
SNAP = ARCH / "SNAPSHOTS"

snaps = sorted(
    [p for p in SNAP.iterdir() if p.is_dir() and p.name.startswith("snapshot_")],
    key=lambda x: x.name
)

if not snaps:
    print("ERROR: snapshots not found")
    sys.exit(1)

latest = snaps[-1]
print("=" * 60)
print("RESTORE FROM:", latest)
print("=" * 60)

files = [
    "PROJECT_STATE.json",
    "ARCHITECTURE_LOCK.json",
    "ARCHITECTURE_LOCK.backup.json",
    "INVARIANTS.json",
    "CONSTITUTION.md",
]

for name in files:
    src = latest / name
    dst = ARCH / name
    if src.exists():
        shutil.copy2(src, dst)
        print("RESTORED:", name)

print("=" * 60)
print("RESTORE COMPLETED")
print("=" * 60)
