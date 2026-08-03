import os
import hashlib
from pathlib import Path
from A_02_MANAGERS.catalog_manager import CatalogManager

class MainOrchestrator:
    def __init__(self):
        self.incoming_dir = Path('A_06_WORKSPACE/incoming')
        self.catalog = CatalogManager()

    def run(self):
        print('--> Оркестратор запущен')
        if not self.incoming_dir.exists():
            os.makedirs(self.incoming_dir, exist_ok=True)

        files = [f for f in self.incoming_dir.iterdir() if not f.name.startswith('.')]

        for file in files:
            try:
                # 1. Железная нормализация абсолютного пути
                db_path = str(file.resolve())

                # 2. Потоковое вычисление MD5 (буфер 8 КБ)
                hasher = hashlib.md5()
                with open(file, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        hasher.update(chunk)
                file_hash = hasher.hexdigest()

                print(f"[DEBUG] {file.name} | MD5 = {file_hash}")

                # 3. Передача реального хэша в CatalogManager
                self.catalog.register_document(
                    filepath=db_path,
                    file_bytes=b'',
                    summary='',
                    tags='',
                    file_hash=file_hash,
                    status='queued'
                )
                print(f'    [✓] {file.name} — задача поставлена в очередь')
            except Exception as e:
                print(f'    [!!!] ОШИБКА при регистрации {file.name}: {e}')

        print('--> Оркестратор отработал успешно')