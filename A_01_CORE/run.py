from pathlib import Path

from A_01_CORE.manifest_loader import ManifestLoader


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def startup():

    print("=================================")
    print("BUTLER OMEGA FOUNDATION")
    print("=================================")

    try:

        config = ManifestLoader.load()

        print("✓ Manifest загружен")
        print(f"✓ Версия: {config.get('version')}")

        all_ok = True

        for key in ["workspace", "storage", "logs"]:

            relative_path = config.get(key, "")
            full_path = PROJECT_ROOT / relative_path

            if full_path.exists():
                print(f"✓ {key}: {full_path}")
            else:
                print(f"✗ {key}: {full_path} отсутствует")
                all_ok = False

        if all_ok:
            print("\nSYSTEM READY")
        else:
            print("\nSYSTEM NOT READY")

    except Exception as e:

        print(f"\n✗ ОШИБКА ЗАПУСКА: {e}")


if __name__ == "__main__":
    startup()