import sys
import os
import sqlite3
import contextlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_01_CORE.manifest_loader import ManifestLoader
from A_02_MANAGERS.provider_manager import ProviderManager
from A_02_MANAGERS.catalog_manager import CatalogManager

sys.stdout.reconfigure(encoding='utf-8')

def run_guardian():
    print("==================================")
    print("   BUTLER OMEGA SYSTEM GUARDIAN   ")
    print("              v1.0                ")
    print("==================================")

    score = 100

    # 1. КОНТРОЛЬ КРИТИЧЕСКИХ ФАЙЛОВ ЯДРА
    print("\n[CORE FILES]")
    critical_files = [
        "A_01_CORE/orchestrator.py",
        "A_03_ORCHESTRATION/worker.py",
        "A_02_MANAGERS/queue_manager.py",
        "A_04_AGENTS/professor.py"
    ]
    for rel_f in critical_files:
        if (PROJECT_ROOT / rel_f).exists():
            print(f"  ✓ {rel_f} (На месте)")
        else:
            print(f"  ✗ {rel_f} ОТСУТСТВУЕТ")
            score -= 15

    # 2. CONFIG & MANIFEST
    try:
        config = ManifestLoader.load()
        print("  ✓ system_manifest.json загружен")
    except Exception as e:
        print(f"  ✗ Ошибка манифеста: {e}")
        score -= 40
        config = {}

    # 3. ФИЗИЧЕСКИЕ ДИРЕКТОРИИ
    print("\n[FILESYSTEM]")
    workspace = PROJECT_ROOT / config.get("workspace", "A_06_WORKSPACE")
    storage = PROJECT_ROOT / config.get("storage", "A_05_STORAGE")
    logs = PROJECT_ROOT / config.get("logs", "A_08_LOGS")

    for name, path_obj in [("Workspace", workspace), ("Storage", storage), ("Logs", logs)]:
        if path_obj.exists():
            print(f"  ✓ {name} каталог подтвержден")
        else:
            print(f"  ✗ {name} ОШИБКА: {path_obj} не найден")
            score -= 10

    # 4. РАБОТА СУБД И ТАБЛИЦ
    print("\n[DATABASE INTERNALS]")
    try:
        cm = CatalogManager()
        if cm.db_path.exists():
            conn = sqlite3.connect(cm.db_path)
            try:
                cursor = conn.execute("SELECT COUNT(*) FROM documents")
                count = cursor.fetchone()[0]
                print(f"  ✓ catalog.db active (Файлов в индексе: {count})")
            except sqlite3.OperationalError as db_err:
                print(f"  ✗ Структура таблицы нарушена: {db_err}")
                score -= 20
            finally:
                conn.close()
        else:
            print("  [-] catalog.db отсутствует (Ожидает инициализации)")
            score -= 10
    except Exception as e:
        print(f"  ✗ Критический сбой СУБД: {e}")
        score -= 20

    # 5. ИНСПЕКЦИЯ OLLAMA И МОДЕЛЕЙ СРЕДЫ
    print("\n[OLLAMA & COGNITIVE MODELS]")
    try:
        pm = ProviderManager()

        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stdout(devnull):
                is_online = pm.check_ollama_status()
                models = pm.get_local_models() if is_online else []

        if is_online:
            print("  ✓ Локальный server Ollama доступен")

            req_analysis = config.get("analysis_model", "qwen-3_5:latest")
            req_vision = config.get("vision_model", "qwen2.5-vl:latest")

            for model_type, model_name in [("Анализ", req_analysis), ("Зрение", req_vision)]:
                clean_req = model_name.split(':')[0]
                if any(clean_req in m for m in models):
                    print(f"  ✓ [{model_type}] Модель готова: {model_name}")
                else:
                    print(f"  ✗ [{model_type}] Модель {model_name} НЕ НАЙДЕНА в Ollama")
                    score -= 10
        else:
            print("  ✗ Локальный сервер Ollama ОТКЛЮЧЕН (OFFLINE)")
            score -= 30
    except Exception as e:
        print(f"  ✗ Не удалось запустить инспекцию провайдера: {e}")
        score -= 30

    # МЕТРИКИ ОЧЕРЕДИ
    print('\n==================================')
    print('QUEUE HEALTH')
    print('----------------------------------')
    try:
        conn = sqlite3.connect('A_05_STORAGE/catalog.db')
        status_counts = dict(conn.execute('SELECT status, COUNT(*) FROM documents GROUP BY status').fetchall())
        conn.close()
        for st in ['queued', 'processing', 'completed', 'failed']:
            print(f'  {st:<12} : {status_counts.get(st, 0)}')
    except Exception as e:
        print(f'  [!] Ошибка чтения очереди: {e}')

    # ГРЕЙДИНГ СИСТЕМЫ
    score = max(0, score)
    if score >= 95:
        status = "GREEN"
    elif score >= 80:
        status = "YELLOW"
    else:
        status = "RED"

    print("\n==================================")
    print(f"HEALTH SCORE :  {score} / 100")
    print(f"STATUS       :  {status}")
    print("==================================")

    return status == "GREEN"

if __name__ == '__main__':
    run_guardian()