# -*- coding: utf-8 -*-
import json
import hashlib
import shutil
import socket
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARCH = ROOT / "A_00_ARCHITECTURE"
SNAP_ROOT = ARCH / "SNAPSHOTS"

SNAP_ROOT.mkdir(parents=True, exist_ok=True)

MAX_SNAPSHOTS = 100

FILES = [
    "PROJECT_STATE.json",
    "ARCHITECTURE_LOCK.json",
    "ARCHITECTURE_LOCK.backup.json",
    "INVARIANTS.json",
    "CONSTITUTION.md",
]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

stamp = time.strftime("%Y%m%d_%H%M%S")
snapshot_dir = SNAP_ROOT / f"snapshot_{stamp}"
snapshot_dir.mkdir(parents=True, exist_ok=True)

manifest = {
    "snapshot_version": "2.0",
    "created_at": stamp,
    "hostname": socket.gethostname(),
    "pid": os.getpid(),
    "files": []
}

for name in FILES:
    src = ARCH / name
    if src.exists():
        dst = snapshot_dir / name
        shutil.copy2(src, dst)
        manifest["files"].append({
            "path": name,
            "sha256": sha256(dst),
            "size": dst.stat().st_size
        })

(snapshot_dir / "metadata.json").write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

snapshots = sorted(
    [p for p in SNAP_ROOT.iterdir() if p.is_dir() and p.name.startswith("snapshot_")],
    key=lambda p: p.name
)

while len(snapshots) > MAX_SNAPSHOTS:
    oldest = snapshots.pop(0)
    shutil.rmtree(oldest, ignore_errors=True)
    print(f"[ROTATE] Removed old snapshot: {oldest.name}")

print("=" * 55)
print("✓ ARCHITECTURE SNAPSHOT CREATED")
print(f"LOCATION: {snapshot_dir}")
print(f"MAX SNAPSHOTS: {MAX_SNAPSHOTS}")
print("=" * 55)