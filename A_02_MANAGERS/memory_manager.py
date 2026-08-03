import os
from pathlib import Path
from A_01_CORE.manifest_loader import ManifestLoader

class MemoryManager:
    def __init__(self):
        self.PROJECT_ROOT = Path(__file__).resolve().parent.parent
        config = ManifestLoader.load()
        self.storage_dir = self.PROJECT_ROOT / config.get("storage", "A_05_STORAGE")
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_to_memory(self, filename, text):
        """Сохраняет текстовый отчет напрямую в физическую память (storage)"""
        try:
            storage_report_path = self.storage_dir / filename
            with open(storage_report_path, "w", encoding="utf-8") as r:
                r.write(text)
            print(f"✓ MemoryManager: Данные успешно записаны в память -> {filename}")
            return True
        except Exception as e:
            print(f"✗ MemoryManager ОШИБКА ЗАПИСИ: {e}")
            return False
