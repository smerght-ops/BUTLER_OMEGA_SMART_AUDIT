# A_01_CORE/project_state_builder.py
import json
import sys
import hashlib
import time
import socket
import os
import shutil
from pathlib import Path

ARCH_VERSION = "1.2.0"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARCH_DIR = PROJECT_ROOT / "A_00_ARCHITECTURE"
SNAPSHOT_DIR = ARCH_DIR / "SNAPSHOTS"

STATE_PATH = ARCH_DIR / "PROJECT_STATE.json"
LOCK_PATH = ARCH_DIR / "ARCHITECTURE_LOCK.json"
BACKUP_LOCK_PATH = ARCH_DIR / "ARCHITECTURE_LOCK.backup.json"
AUDIT_PATH = ARCH_DIR / "audit.log"

SNAPSHOT_LIMIT = 50

ARCH_FILES = [
    "PROJECT_STATE.json",
    "ARCHITECTURE_LOCK.json",
    "ARCHITECTURE_LOCK.backup.json",
    "INVARIANTS.json",
    "CONSTITUTION.md",
]


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    tmp_path.replace(path)


def write_audit_log(action: str, details: str):
    ARCH_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    entry = (
        f"{timestamp}\n"
        f"ACTION: {action}\n"
        f"USER: local\n"
        f"PID: {os.getpid()}\n"
        f"HOST: {socket.gethostname()}\n"
        f"DETAILS: {details}\n"
        f"----------------------------------------\n"
    )

    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(entry)


def load_lock_source() -> dict:
    if LOCK_PATH.exists() and LOCK_PATH.stat().st_size > 0:
        return json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    if BACKUP_LOCK_PATH.exists() and BACKUP_LOCK_PATH.stat().st_size > 0:
        return json.loads(BACKUP_LOCK_PATH.read_text(encoding="utf-8"))

    raise FileNotFoundError("ARCHITECTURE_LOCK.json and backup are missing or empty")


def create_architecture_snapshot(reason: str = "manual") -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    stamp = time.strftime("%Y%m%d_%H%M%S")
    target = SNAPSHOT_DIR / f"snapshot_{stamp}"
    target.mkdir(parents=True, exist_ok=True)

    copied = {}
    for name in ARCH_FILES:
        src = ARCH_DIR / name
        if src.exists():
            dst = target / name
            shutil.copy2(src, dst)
            copied[name] = {
                "sha256": file_sha256(dst),
                "size": dst.stat().st_size
            }

    metadata = {
        "snapshot_version": "1.0",
        "created_at": stamp,
        "architecture_version": ARCH_VERSION,
        "reason": reason,
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
        "files": copied
    }

    atomic_write_json(target / "metadata.json", metadata)

    snapshots = sorted(
        [p for p in SNAPSHOT_DIR.iterdir() if p.is_dir() and p.name.startswith("snapshot_")],
        key=lambda p: p.name
    )

    removed = []
    while len(snapshots) > SNAPSHOT_LIMIT:
        old = snapshots.pop(0)
        shutil.rmtree(old)
        removed.append(old.name)

    write_audit_log(
        "create_snapshot",
        f"snapshot={target.name}; reason={reason}; removed={removed}"
    )

    print(f"✓ [SNAPSHOT] Создан: {target}")
    if removed:
        print(f"✓ [SNAPSHOT] Удалены старые снимки: {removed}")

    return target


def rebuild_lock_manifest() -> bool:
    print("• [BUILDER] Переподписание ARCHITECTURE_LOCK.json...")

    try:
        lock_data = load_lock_source()
        lock_data["architecture_version"] = ARCH_VERSION
        lock_data["lock_signature"] = "None"

        if STATE_PATH.exists():
            lock_data["state_file_sha256"] = file_sha256(STATE_PATH)

        guardian_path = PROJECT_ROOT / "A_01_CORE" / "memory_guardian.py"
        if guardian_path.exists():
            lock_data["guardian_self_sha256"] = file_sha256(guardian_path)

        raw = json.dumps(lock_data, sort_keys=True)
        lock_data["lock_signature"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        atomic_write_json(LOCK_PATH, lock_data)
        atomic_write_json(BACKUP_LOCK_PATH, lock_data)

        write_audit_log(
            "rebuild_lock",
            "ARCHITECTURE_LOCK.json and backup were signed"
        )

        print("✓ [BUILDER] LOCK и backup синхронизированы и подписаны.")
        return True

    except Exception as e:
        print(f"❌ [BUILDER] Ошибка переподписания LOCK: {e}")
        return False


def collect_critical_files(lock_data: dict) -> dict:
    result = {}

    for comp in lock_data.get("critical_components", []):
        rel = comp.get("path")
        if not rel:
            continue

        p = PROJECT_ROOT / rel

        if p.exists():
            st = p.stat()
            result[rel] = {
                "exists": True,
                "sha256": file_sha256(p),
                "size": st.st_size,
                "mtime": int(st.st_mtime)
            }
        else:
            result[rel] = {
                "exists": False,
                "sha256": None,
                "size": 0,
                "mtime": 0
            }

    return result


def build_state() -> bool:
    if "--snapshot" in sys.argv:
        create_architecture_snapshot(reason="manual_cli")
        return True

    if "--rebuild-lock" in sys.argv:
        return rebuild_lock_manifest()

    approved = "--approve" in sys.argv

    try:
        lock_data = load_lock_source()
    except Exception as e:
        print(f"❌ [BUILDER] Не удалось прочитать LOCK: {e}")
        return False

    current_files = collect_critical_files(lock_data)

    if not approved:
        print("⚠️ [DIAGNOSTIC MODE] Сверка завершена.")
        print("Для фиксации состояния используй:")
        print("  python A_01_CORE\\project_state_builder.py --approve")
        return True

    # ВАЖНО: snapshot создаётся ДО перезаписи PROJECT_STATE и LOCK
    create_architecture_snapshot(reason="before_approve")

    state = {
        "generated_at": int(time.time()),
        "project": "BUTLER_OMEGA_SMART",
        "architecture_version": ARCH_VERSION,
        "approved": True,
        "critical_files": current_files
    }

    atomic_write_json(STATE_PATH, state)
    write_audit_log("build_state", "PROJECT_STATE.json was rebuilt with --approve")

    ok = rebuild_lock_manifest()
    if not ok:
        return False

    print("✓ [BUILDER] PROJECT_STATE.json обновлён.")
    return True


if __name__ == "__main__":
    sys.exit(0 if build_state() else 1)
