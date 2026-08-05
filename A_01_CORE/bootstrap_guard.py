# A_01_CORE/bootstrap_guard.py
import sys
import hashlib
import py_compile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GUARDIAN_PATH = PROJECT_ROOT / "A_01_CORE" / "memory_guardian.py"
LOCK_PATH = PROJECT_ROOT / "A_00_ARCHITECTURE" / "ARCHITECTURE_LOCK.json"

def calculate_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def boot_verify() -> bool:
    print("• [BOOTSTRAP] Первичный контроль целостности Стража...")

    if not GUARDIAN_PATH.exists():
        print("❌ [BOOTSTRAP FATAL] Файл memory_guardian.py физически уничтожен!")
        return False

    try:
        py_compile.compile(str(GUARDIAN_PATH), doraise=True)
    except Exception as e:
        print(f"❌ [BOOTSTRAP FATAL] Код Стража поврежден и не компилируется: {e}")
        return False

    # Сверяем хэш Стража напрямую с тем, что ожидает LOCK-манифест
    if LOCK_PATH.exists():
        try:
            import json
            lock_data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
            expected_hash = lock_data.get("guardian_self_sha256")
            if expected_hash and calculate_sha256(GUARDIAN_PATH) != expected_hash:
                print("❌ [BOOTSTRAP FATAL] Нарушена подпись Стража! Обнаружено несанкционированное изменение ядра.")
                return False
        except Exception as e:
            print(f"❌ [BOOTSTRAP FATAL] Ошибка парсинга LOCK при бутстрапе: {e}")
            return False

    print("✓ [BOOTSTRAP] Контроль пройден. Запуск ядра Стража разрешен.")
    return True

if __name__ == "__main__":
    sys.exit(0 if boot_verify() else 1)