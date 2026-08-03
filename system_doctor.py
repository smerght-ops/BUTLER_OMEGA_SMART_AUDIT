import json
import sqlite3
import py_compile
import sys
import subprocess
import shutil
from pathlib import Path

ROOT = Path(".")
DB = ROOT / "A_05_STORAGE" / "catalog.db"
ARCH = ROOT / "A_00_ARCHITECTURE"

FILES = [
    ARCH / "PROJECT_STATE.json",
    ARCH / "ARCHITECTURE_LOCK.json",
    ARCH / "ARCHITECTURE_LOCK.backup.json",
    ARCH / "INVARIANTS.json",
    ARCH / "CONSTITUTION.md",
]

MODULES = [
    "A_01_CORE/memory_guardian.py",
    "A_01_CORE/project_state_builder.py",
    "A_01_CORE/orchestrator.py",
    "A_02_MANAGERS/catalog_manager.py",
    "A_04_AGENTS/professor.py",
]

def repair():
    print("=" * 60)
    print("          BUTLER AUTO REPAIR MODE")
    print("=" * 60)

    if not DB.exists():
        print("❌ catalog.db отсутствует")
        return 1

    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_file_hash
        ON documents(file_hash)
        WHERE file_hash IS NOT NULL
          AND file_hash <> ''
    """)

    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_documents_file_hash
        ON documents(file_hash)
    """)

    conn.commit()
    conn.close()

    print("✓ Индексы восстановлены")

    for p in ROOT.rglob("__pycache__"):
        try:
            shutil.rmtree(p)
            print(f"✓ Удален {p}")
        except Exception:
            pass

    subprocess.run(
        ["python", "A_01_CORE/project_state_builder.py", "--approve"],
        check=False
    )

    print("✓ PROJECT_STATE и LOCK переподписаны")
    print("✓ Автовосстановление завершено")
    print("=" * 60)

    return 0

def main():
    if "--repair" in sys.argv:
        raise SystemExit(repair())

    score = 100

    print("=" * 60)
    print("        BUTLER OMEGA SYSTEM DOCTOR v3.1")
    print("=" * 60)

    if not DB.exists():
        print("❌ catalog.db отсутствует")
        score -= 50
    else:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()

        print("\n[DATABASE]")

        cols = {r[1] for r in cur.execute("PRAGMA table_info(documents)")}
        required = {
            "filepath",
            "file_hash",
            "status",
            "summary",
            "tags",
            "registered_at",
            "updated_at",
            "is_legacy",
        }

        missing = required - cols
        if missing:
            print("❌ Отсутствуют колонки:", sorted(missing))
            score -= 20
        else:
            print("✓ Схема documents корректна")

        idx = {r[1] for r in cur.execute("PRAGMA index_list(documents)")}

        if "idx_unique_file_hash" in idx:
            print("✓ UNIQUE INDEX присутствует")
        else:
            print("❌ idx_unique_file_hash отсутствует")
            score -= 10

        completed = cur.execute("SELECT COUNT(*) FROM documents WHERE status='completed'").fetchone()[0]
        queued = cur.execute("SELECT COUNT(*) FROM documents WHERE status='queued'").fetchone()[0]
        processing = cur.execute("SELECT COUNT(*) FROM documents WHERE status='processing'").fetchone()[0]
        legacy = cur.execute("SELECT COUNT(*) FROM documents WHERE is_legacy=1").fetchone()[0]
        modern = cur.execute("SELECT COUNT(*) FROM documents WHERE is_legacy=0").fetchone()[0]

        duplicates = cur.execute("""
            SELECT COUNT(*)
            FROM (
                SELECT file_hash
                FROM documents
                WHERE file_hash <> ''
                GROUP BY file_hash
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]

        modern_empty = cur.execute("""
            SELECT COUNT(*)
            FROM documents
            WHERE is_legacy=0
              AND status='completed'
              AND (file_hash IS NULL OR file_hash='')
        """).fetchone()[0]

        print("\n[DOCUMENTS]")
        print(f"Completed : {completed}")
        print(f"Queued    : {queued}")
        print(f"Processing: {processing}")
        print(f"Modern    : {modern}")
        print(f"Legacy    : {legacy}")

        print("\n[INTEGRITY]")
        print(f"Duplicate hashes        : {duplicates}")
        print(f"Modern without hash     : {modern_empty}")

        if duplicates:
            score -= 20
        if modern_empty:
            score -= 20

        conn.close()

    print("\n[ARCHITECTURE]")

    versions = []
    for f in FILES:
        if f.exists():
            print(f"✓ {f.name}")
            if f.suffix == ".json":
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    if "architecture_version" in data:
                        versions.append(data["architecture_version"])
                except Exception:
                    print(f"❌ {f.name} поврежден")
                    score -= 10
        else:
            print(f"❌ {f.name}")
            score -= 5

    if len(set(versions)) > 1:
        print("❌ Несовпадение architecture_version")
        score -= 10
    elif versions:
        print(f"✓ Версия архитектуры: {versions[0]}")

    print("\n[CODE]")

    for mod in MODULES:
        try:
            py_compile.compile(mod, doraise=True)
            print(f"✓ {mod}")
        except Exception as ex:
            print(f"❌ {mod}: {ex}")
            score -= 10

    print("\n" + "=" * 60)

    if score >= 100:
        status = "EXCELLENT"
    elif score >= 90:
        status = "GOOD"
    elif score >= 75:
        status = "WARNING"
    else:
        status = "CRITICAL"

    print(f"HEALTH SCORE : {score}/100")
    print(f"STATUS       : {status}")
    print("=" * 60)

if __name__ == "__main__":
    main()