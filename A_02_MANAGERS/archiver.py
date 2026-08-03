import shutil
from pathlib import Path

class Archiver:
    def __init__(self):
        self.incoming = Path("A_06_WORKSPACE/incoming")
        self.processing = Path("A_06_WORKSPACE/processing")
        self.processing.mkdir(parents=True, exist_ok=True)

    def move_to_processing(self, filename):
        src = self.incoming / filename
        dst = self.processing / filename
        if src.exists():
            shutil.move(str(src), str(dst))
            return True
        return False

if __name__ == "__main__":
    arch = Archiver()
    # Берем первый попавшийся файл из входящих
    files = [f.name for f in Path("A_06_WORKSPACE/incoming").iterdir() if not f.name.startswith('.')]
    if files:
        target = files[0]
        if arch.move_to_processing(target):
            print(f"✓ Файл {target} перемещен в PROCESSING")
        else:
            print("✗ Ошибка перемещения")
    else:
        print("Входящих файлов нет")
