#!/usr/bin/env python3
"""
BaseInspector — общий каркас для всех измерительных приборов.
Обеспечивает:
- загрузку PhysicalMap
- фильтрацию файлов по kind и передачу полной информации о файле
- обработку файлов с pathlib и кодировкой utf-8-sig
- сбор ошибок и сохранение относительных путей (id)
- генерацию метаданных и статистики
- запись JSON с единой структурой
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class BaseInspector(ABC):
    SCHEMA: str = "base"
    SCHEMA_VERSION: str = "1.0"
    GENERATOR: str = "BaseInspector"
    GENERATOR_VERSION: str = "1.0"
    TARGET_KIND: str = "python"  # по умолчанию

    def __init__(self, input_path: str, output_path: str):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.errors: List[Dict] = []
        self.payload: List[Dict] = []
        self.metadata: Dict = {}
        self.project_root: Path = None

    def load_physical_map(self) -> Dict:
        """Загружает PhysicalMap из JSON."""
        try:
            with open(self.input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Cannot read {self.input_path}: {e}", file=sys.stderr)
            sys.exit(1)

    def get_file_infos(self, physical_map: Dict) -> List[Dict]:
        """Возвращает список словарей с информацией о файлах заданного kind."""
        self.project_root = Path(physical_map["metadata"]["project_root"])
        infos = []
        for item in physical_map["payload"]:
            if item.get("kind") == self.TARGET_KIND:
                path = self.project_root / item["relative_path"]
                if path.exists():
                    infos.append({
                        "id": item.get("id"),
                        "relative_path": item["relative_path"],  # обязательно есть
                        "path": path,
                        "kind": item.get("kind"),
                        "size_bytes": item.get("size_bytes"),
                        "modified_utc": item.get("modified_utc"),
                    })
                else:
                    print(f"WARNING: File not found: {path}", file=sys.stderr)
        return infos

    @abstractmethod
    def process_file(self, file_info: Dict) -> Dict:
        """Абстрактный метод сбора данных из одного файла.
        Получает словарь file_info с ключами:
            id, relative_path, path, kind, size_bytes, modified_utc
        Должен возвращать словарь с данными. Ошибки добавляются через поле 'error'.
        """
        pass

    def run(self):
        """Основной конвейер: загрузка, обработка, формирование вывода."""
        physical_map = self.load_physical_map()
        file_infos = self.get_file_infos(physical_map)

        total_files = len(file_infos)
        total_errors = 0

        for file_info in file_infos:
            data = self.process_file(file_info)
            if "error" in data:
                total_errors += 1
                self.errors.append({
                    "stage": "process_file",
                    "id": data.get("id", file_info["id"]),
                    "error": data["error"]
                })
            self.payload.append(data)

        # Формируем метаданные
        self.metadata = {
            "schema": self.SCHEMA,
            "schema_version": self.SCHEMA_VERSION,
            "generator": self.GENERATOR,
            "generator_version": self.GENERATOR_VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "input": {
                "physical_map": str(self.input_path),
                "total_files_processed": total_files,
            },
            "statistics": {
                "total_files": len(self.payload),
                "total_errors": total_errors,
            }
        }

        # Дополнительная статистика от наследника
        self._add_statistics()

        # Запись выходного JSON
        output = {
            "metadata": self.metadata,
            "errors": self.errors,
            "payload": self.payload,
        }
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ERROR: Failed to write output: {e}", file=sys.stderr)
            sys.exit(1)

        # Итоговый отчёт в консоль
        print(f"STATUS  : SUCCESS")
        print(f"OUTPUT  : {self.output_path}")
        print(f"FILES   : {len(self.payload)}")
        print(f"ERRORS  : {total_errors}")

    def _add_statistics(self):
        """Метод для добавления дополнительной статистики наследниками."""
        pass
