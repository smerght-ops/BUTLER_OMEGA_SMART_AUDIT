import sys
import subprocess
import py_compile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FACTORY = ROOT / "A_00_AVARIYKA" / "BUTLER_FACTORY"
ROLLBACK = ROOT / "A_00_HISTORY" / "ROLLBACK_POINTS"

IGNORE = {
    "__pycache__",
    "A_00_HISTORY",
    "A_08_LOGS",
    ".git"
}

def bad_path(p: Path):
    parts = set(p.relative_to(ROOT).parts)
    return bool(parts & IGNORE)

def latest_rollback_has_factory():
    points = sorted([p for p in ROLLBACK.iterdir() if p.is_dir()], key=lambda x: x.name)
    if not points:
        return False, None
    last = points[-1]
    return (last / "A_00_AVARIYKA" / "BUTLER_FACTORY").exists(), last

def check_py_files():
    errors = []
    for p in ROOT.rglob("*.py"):
        if bad_path(p):
            continue
        try:
            with p.open("rb") as f:
                if f.read(3) == b"\xef\xbb\xbf":
                    raise RuntimeError("BOM в начале файла")
            py_compile.compile(str(p), doraise=True)
        except Exception as e:
            errors.append((str(p.relative_to(ROOT)), str(e)))
    return errors

def main():
    print("=" * 60)
    print("ЕДИНЫЙ КОНТУР БЕЗОПАСНОСТИ BUTLER_OMEGA_SMART + BUTLER_FACTORY")
    print("=" * 60)

    ok_factory, last = latest_rollback_has_factory()

    print("Корень проекта:", ROOT)
    print("Фабрика:", FACTORY)
    print("Последняя точка:", last)
    print("BUTLER_FACTORY в rollback:", "ДА" if ok_factory else "НЕТ")

    if not ok_factory:
        print("ОШИБКА: фабрика не входит в последнюю точку восстановления")
        return 1

    print("")
    print("Проверка Python-файлов...")
    errors = check_py_files()

    if errors:
        print("НАЙДЕНЫ ОШИБКИ:", len(errors))
        for file, err in errors[:30]:
            print("ОШИБКА:", file)
            print("  ", err)
        return 1

    print("ВСЁ В ПОРЯДКЕ. Единый контур работает.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
