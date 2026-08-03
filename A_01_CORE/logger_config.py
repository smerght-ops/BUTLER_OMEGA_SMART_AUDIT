import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

LOG_DIR = PROJECT_ROOT / "A_08_LOGS"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def setup_logger(name):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
    )

    system_handler = logging.FileHandler(
        LOG_DIR / "system.log",
        encoding="utf-8"
    )

    error_handler = logging.FileHandler(
        LOG_DIR / "errors.log",
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    system_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    error_handler.setLevel(logging.ERROR)

    logger.addHandler(system_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)

    return logger
