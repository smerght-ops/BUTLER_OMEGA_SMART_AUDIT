import os
import json
import logging
from pathlib import Path

# Настраиваем конфигурацию логирования
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "A_08_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "system.log", encoding="utf-8"),
        logging.StreamHandler() # Оставляем вывод в консоль
    ]
)
logger = logging.getLogger("HEALTHCHECK")

def check_system():
    manifest_path = PROJECT_ROOT / "A_07_CONFIG" / "system_manifest.json"

    if not manifest_path.exists():
        logger.error("Manifest отсутствует по пути %s", manifest_path)
        return False, ["✗ Manifest отсутствует"]

    with open(manifest_path, "r", encoding="utf-8-sig") as f:
        config = json.load(f)

    paths = {
        "Workspace": PROJECT_ROOT / config["workspace"],
        "Storage": PROJECT_ROOT / config["storage"],
        "Logs": PROJECT_ROOT / config["logs"]
    }

    results = []
    all_ok = True

    for name, path in paths.items():
        if path.exists():
            results.append(f"✓ {name} найден")
            logger.info("%s каталог подтвержден: %s", name, path)
        else:
            results.append(f"✗ Каталог {name} ({path}) отсутствует")
            logger.error("Каталог %s ОТСУТСТВУЕТ по пути: %s", name, path)
            all_ok = False

    return all_ok, results

if __name__ == "__main__":
    logger.info("=== ЗАПУСК ПРОВЕРКИ СИСТЕМЫ BUTLER OMEGA v1.1 ===")
    ok, lines = check_system()

    if not ok:
        logger.error("!!! SYSTEM NOT READY !!!")
        exit(1)
    else:
        logger.info("SYSTEM READY")