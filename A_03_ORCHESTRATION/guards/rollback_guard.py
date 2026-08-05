# -*- coding: utf-8 -*-

import json
import time
from pathlib import Path


class RollbackGuard:

    def __init__(self, max_age_seconds=300):
        self.max_age = max_age_seconds
        self.backup_markers = ["backup", "bak", "before", "stable"]
        self.project_root = Path(__file__).resolve().parents[2]

    def validate(self, cr_path: Path) -> dict:
        cr_path = Path(cr_path)
        if not cr_path.is_absolute():
            cr_path = (self.project_root / cr_path).resolve()

        if not cr_path.exists():
            return {"status": "REJECTED", "code": "404_CR_NOT_FOUND"}

        try:
            with open(cr_path, "r", encoding="utf-8") as f:
                cr_data = json.load(f)
        except Exception as e:
            return {"status": "REJECTED", "code": "400_INVALID_JSON", "reason": str(e)}

        if not cr_data.get("rollback_required", False):
            return {"status": "APPROVED", "code": "200_ROLLBACK_BYPASS"}

        target_files = cr_data.get("target_files", [])
        current_time = time.time()

        for file_path_str in target_files:
            target_file = self.project_root / file_path_str
            target_dir = target_file.parent
            base_name = target_file.stem.lower()

            if not target_dir.exists():
                return {
                    "status": "REJECTED",
                    "code": "409_BACKUP_REQUIRED",
                    "reason": f"Директория {target_dir} не существует."
                }

            valid_backup_found = False
            for item in target_dir.iterdir():
                if item.is_file() and item.name != target_file.name:
                    name_lower = item.name.lower()

                    if base_name in name_lower and any(m in name_lower for m in self.backup_markers):
                        # Вычисляем точный возраст бэкапа
                        file_age = current_time - item.stat().st_mtime
                        if file_age <= self.max_age:
                            valid_backup_found = True
                            break

            if not valid_backup_found:
                return {
                    "status": "REJECTED",
                    "code": "409_BACKUP_TOO_OLD",
                    "reason": f"Все найденные бэкапы для {target_file.name} старше лимита в {self.max_age} секунд."
                }

        return {
            "status": "APPROVED",
            "code": "200_GUARD_OK",
            "reason": "Свежая резервная копия верифицирована."
        }


if __name__ == "__main__":
    guard = RollbackGuard()
    print("=== RUNTIME COMPONENT TEST: ROLLBACK_GUARD V0.6 (AGE FILTER) ===")

    real_cr = Path("A_00_ARCHITECTURE/CHANGE_REQUESTS/CR_000_TEST.json")
    print(f"\n[Тест 1] Проверка со старым бэкапом (Лимит {guard.max_age}с):")
    print(json.dumps(guard.validate(real_cr), indent=2, ensure_ascii=False))
