# -*- coding: utf-8 -*-
import sys
import json
import hashlib
import py_compile
import importlib
import sqlite3
from pathlib import Path

ARCH_VERSION = "1.2.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARCH_DIR = PROJECT_ROOT / "A_00_ARCHITECTURE"

CONST_PATH = ARCH_DIR / "CONSTITUTION.md"
INV_PATH = ARCH_DIR / "INVARIANTS.json"
LOCK_PATH = ARCH_DIR / "ARCHITECTURE_LOCK.json"
STATE_PATH = ARCH_DIR / "PROJECT_STATE.json"
DB_PATH = PROJECT_ROOT / "A_05_STORAGE" / "catalog.db"

LEGACY_MAX_ID = 100
LEGACY_MAX_EMPTY_HASH = 50
ALLOWED_SAFE_COMMANDS = {"--self-test", "--status", "--repair", "--safe"}


def fail(msg: str) -> bool:
    print(f"\n❌ [FATAL LOCKDOWN] {msg}")
    return False


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def verify_lock_manifest():
    if not LOCK_PATH.exists():
        return False, "Манифест ARCHITECTURE_LOCK.json отсутствует."
    try:
        data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        saved_sig = data.get("lock_signature")
        data["lock_signature"] = "None"
        raw = json.dumps(data, sort_keys=True)
        current_sig = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        if saved_sig != current_sig:
            return False, "Криптографическая подпись ARCHITECTURE_LOCK.json скомпрометирована."
    except Exception as e:
        return False, f"Ошибка подписи LOCK: {e}"
    return True, None


def verify_project_state():
    if not STATE_PATH.exists():
        return False, "Паспорт PROJECT_STATE.json отсутствует."
    try:
        lock_data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        expected = lock_data.get("state_file_sha256")
        if expected and file_sha256(STATE_PATH) != expected:
            return False, "PROJECT_STATE.json изменен в обход project_state_builder."
    except Exception as e:
        return False, f"Ошибка кросс-валидации паспорта: {e}"
    return True, None


def verify_database(safe_reasons):
    if not DB_PATH.exists():
        return fail("catalog.db уничтожен.")

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    try:
        lock_data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        required_columns = lock_data.get("required_columns", {})

        for table, columns in required_columns.items():
            exists = cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table,)
            ).fetchone()

            if not exists:
                return fail(f"Уничтожена обязательная таблица: {table}")

            actual = {r[1] for r in cur.execute(f"PRAGMA table_info({table})").fetchall()}
            missing = set(columns) - actual
            if missing:
                return fail(f"Дрейф колонок в {table}: {missing}")

        duplicates = cur.execute(
            """
            SELECT file_hash, COUNT(*)
            FROM documents
            WHERE file_hash IS NOT NULL AND file_hash != ''
            GROUP BY file_hash
            HAVING COUNT(*) > 1
            """
        ).fetchall()

        if duplicates:
            return fail(f"Конституция нарушена. Дубли file_hash: {duplicates[:3]}")

        legacy_count = cur.execute(
            """
            SELECT COUNT(*)
            FROM documents
            WHERE id <= ?
              AND status='completed'
              AND (file_hash IS NULL OR file_hash='')
            """,
            (LEGACY_MAX_ID,)
        ).fetchone()[0]

        if legacy_count > LEGACY_MAX_EMPTY_HASH:
            return fail(
                f"Регрессия legacy: пустых хэшей {legacy_count}, лимит {LEGACY_MAX_EMPTY_HASH}."
            )

        new_empty = cur.execute(
            """
            SELECT id
            FROM documents
            WHERE id > ?
              AND status='completed'
              AND (file_hash IS NULL OR file_hash='')
            """,
            (LEGACY_MAX_ID,)
        ).fetchall()

        if new_empty:
            return fail(f"Новые completed-документы без file_hash: {new_empty}")

        return True

    except Exception as e:
        return fail(f"Ошибка проверки СУБД: {e}")

    finally:
        conn.close()


def check_code_layer(lock_data, saved_files, safe_reasons):
    for comp in lock_data.get("critical_components", []):
        rel = comp.get("path")
        p = PROJECT_ROOT / rel

        if not p.exists():
            return False

        try:
            py_compile.compile(str(p), doraise=True)
        except Exception:
            return False

        if comp.get("safe_import") and comp.get("module"):
            try:
                importlib.invalidate_caches()
                importlib.import_module(comp.get("module"))
            except Exception:
                return False

        current_hash = file_sha256(p)
        saved_hash = saved_files.get(rel, {}).get("sha256")

        if saved_hash and current_hash != saved_hash:
            safe_reasons.append(f"SHA256 {rel} отличается от PROJECT_STATE.")
        if not saved_hash:
            safe_reasons.append(f"Файл отсутствует в PROJECT_STATE.json: {rel}")

    return True


def run_memory_guardian(self_test_mode: bool = False) -> bool:
    print("\n" + "=" * 46)
    print(f"  BUTLER OMEGA HARDCORE GUARDIAN v{ARCH_VERSION}")
    print("=" * 46)

    safe_reasons = []

    if not CONST_PATH.exists() or not INV_PATH.exists():
        return fail("Декларативный слой уничтожен.")

    lock_ok, lock_err = verify_lock_manifest()
    if not lock_ok:
        return fail(lock_err)

    state_ok, state_err = verify_project_state()
    if not state_ok:
        return fail(state_err)

    if not verify_database(safe_reasons):
        return False

    try:
        lock_data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
        state_data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        saved_files = state_data.get("critical_files", {})
    except Exception as e:
        return fail(f"Ошибка чтения архитектурных метаданных: {e}")

    if not check_code_layer(lock_data, saved_files, safe_reasons):
        return fail("Критический сбой кода.")

    final_mode = "SAFE" if safe_reasons else "NORMAL"

    if safe_reasons:
        print("\n=== SAFE REASONS ===")
        for r in safe_reasons:
            print(f" - {r}")
        print("====================")

    if self_test_mode:
        print(f"\n=== SELF-TEST COMPLETED: {final_mode} ===")
        return True

    args = set(sys.argv[1:])
    if final_mode == "SAFE":
        if args & ALLOWED_SAFE_COMMANDS:
            print("\n⚠️ [SAFE MODE] Разрешен только сервисный доступ.")
            return True
        print("\n❌ [FATAL] Рантайм заблокирован в SAFE MODE.")
        return False

    print("\n✓ [NORMAL MODE] Двухключевой рантайм чист. Старт разрешен.")
    return True


if __name__ == "__main__":
    sys.exit(0 if run_memory_guardian("--self-test" in sys.argv) else 1)
