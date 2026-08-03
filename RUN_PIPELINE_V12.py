import sys
import os
from pathlib import Path

# Жесткая привязка корня к рантайму
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import sys
from pathlib import Path
# RUN_PIPELINE_V12.py
import sys
import time
import sqlite3
import shutil
from pathlib import Path

from A_01_CORE.memory_guardian import run_memory_guardian
from A_01_CORE.project_state_builder import build_state
from A_01_CORE.orchestrator import MainOrchestrator
from A_03_ORCHESTRATION.worker import Worker

ARCH_VERSION = "1.2.0"
DB_PATH = Path("A_05_STORAGE/catalog.db")
CHANGELOG_PATH = Path("A_00_ARCHITECTURE/CHANGELOG.md")

def ensure_changelog():
    CHANGELOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CHANGELOG_PATH.exists():
        CHANGELOG_PATH.profile_manager.set_fact("# ЖУРНАЛ АРХИТЕКТУРНЫХ ИЗМЕНЕНИЙ\n", encoding="utf-8")

def execute_repair():
    print("\n" + "=" * 46)
    print("      BUTLER OMEGA REPAIR MODE")
    print("=" * 46)

    if not DB_PATH.exists():
        print("✗ catalog.db не найден. Ремонт невозможен без существующей базы.")
        return False

    print("⚠️  Внимание! Будет произведено автоматическое восстановление структуры таблиц и индексов.")
    confirm = input("Вы уверены, что хотите продолжить? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("❌ Операция ремонта отменена пользователем.")
        return False

    timestamp = time.strftime("%Y-%m-%d_%H%M%S")
    backup_path = DB_PATH.with_name(f"catalog.db.bak_{timestamp}")

    try:
        shutil.copy2(DB_PATH, backup_path)
        print(f"✓ Бэкап БД создан: {backup_path}")
    except Exception as e:
        print(f"✗ Не удалось создать бэкап БД: {e}")
        return False

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS worker_heartbeat (
                worker_id TEXT PRIMARY KEY,
                boot_id TEXT,
                last_seen INTEGER
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_documents_file_hash ON documents(file_hash)")
        conn.commit()
        conn.close()
        print("✓ Таблица worker_heartbeat проверена/создана.")
        print("✓ Индекс idx_documents_file_hash проверен/создан.")
    except Exception as e:
        print(f"✗ Ошибка ремонта SQLite: {e}")
        return False

    ensure_changelog()
    with open(CHANGELOG_PATH, "a", encoding="utf-8") as f:
        f.write(
            f"\n## Сервисный ремонт: {timestamp}\n"
            f"- Создан backup базы: `{backup_path.name}`\n"
            f"- Проверена таблица `worker_heartbeat`\n"
            f"- Проверен индекс `idx_documents_file_hash`\n"
        )
    print("✓ CHANGELOG.md обновлен.")

    print("\n• Запуск самопроверки после ремонта...")
    if run_memory_guardian(self_test_mode=True):
        print("\n✓ REPAIR MODE завершен успешно.")
        return True
    print("\n⚠️ REPAIR MODE завершен, но Guardian обнаружил предупреждения.")
    return False

def run_pipeline():
    print("[PIPELINE] === СТАРТ КОНВЕЙЕРА БАТЛЕР-ОМЕГА ===")
    print("[PIPELINE] Шаг 1: Запуск Оркестратора (Сканирование папки incoming)...")
    orchestrator = MainOrchestrator()
    orchestrator.run()
    print("[PIPELINE] Оркестратор завершил постановку задач в очередь.")

    print("\n[PIPELINE] Шаг 2: Инициализация Воркера и разбор очереди jobs...")
    worker = Worker()
    processed_count = 0
    while True:
        has_job = worker.process_once()
        if not has_job:
            break
        processed_count += 1
        time.sleep(1)
    print(f"\n[PIPELINE] === КОНВЕЙЕР ЗАВЕРШЕН === Обработано задач: {processed_count}")

def main():
    if "--repair" in sys.argv:
        ok = execute_repair()
        sys.exit(0 if ok else 1)

    if "--self-test" in sys.argv:
        ok = run_memory_guardian(self_test_mode=True)
        sys.exit(0 if ok else 1)

    if not run_memory_guardian(self_test_mode=False):
        print("\n[FATAL] Запуск RUN_PIPELINE заблокирован Memory Guardian.")
        sys.exit(1)

    run_pipeline()

if __name__ == '__main__':
    main()
