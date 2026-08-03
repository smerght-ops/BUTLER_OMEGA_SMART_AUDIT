# -*- coding: utf-8 -*-

import json
from pathlib import Path, PurePosixPath


class FrozenCoreGuard:

    def __init__(self):
        self.frozen_directories = {"A_01_CORE"}
        self.frozen_files = {"chat_router.py"}

    def validate(self, cr_path: Path) -> dict:

        if not cr_path.exists():
            return {
                "status": "REJECTED",
                "code": "404_CR_NOT_FOUND",
                "reason": f"CR not found: {cr_path.name}"
            }

        try:
            with open(cr_path, "r", encoding="utf-8") as f:
                cr_data = json.load(f)

        except Exception as ex:
            return {
                "status": "REJECTED",
                "code": "400_INVALID_JSON",
                "reason": str(ex)
            }

        target_files = cr_data.get("target_files", [])

        for file_path in target_files:

            p = PurePosixPath(
                str(file_path).replace("\\", "/")
            )

            if any(
                part in self.frozen_directories
                for part in p.parts
            ):
                return {
                    "status": "REJECTED",
                    "code": "403_FROZEN_CORE_VIOLATION",
                    "reason": f"Frozen directory: {file_path}"
                }

            if p.name in self.frozen_files:
                return {
                    "status": "REJECTED",
                    "code": "403_FROZEN_CORE_VIOLATION",
                    "reason": f"Frozen file: {file_path}"
                }

        return {
            "status": "APPROVED",
            "code": "200_GUARD_OK",
            "reason": "Validation passed"
        }


if __name__ == "__main__":

    guard = FrozenCoreGuard()

    print("=== FROZEN_CORE_GUARD V1 ===")

    cr_clean = Path(
        r".\A_00_ARCHITECTURE\CHANGE_REQUESTS\CR_000_TEST.json"
    )

    print(
        "[TEST1]",
        guard.validate(cr_clean)
    )

    cr_attack = Path(
        r".\A_00_ARCHITECTURE\CHANGE_REQUESTS\CR_ATTACK_TEST.json"
    )

    cr_attack.write_text(
        '{"target_files":["A_01_CORE/sys_init.py"]}',
        encoding="utf-8"
    )

    print(
        "[TEST2]",
        guard.validate(cr_attack)
    )

    cr_backup = Path(
        r".\A_00_ARCHITECTURE\CHANGE_REQUESTS\CR_BACKUP_TEST.json"
    )

    cr_backup.write_text(
        '{"target_files":["A_06_WORKSPACE/chat_router.py.backup"]}',
        encoding="utf-8"
    )

    print(
        "[TEST3]",
        guard.validate(cr_backup)
    )

    if cr_attack.exists():
        cr_attack.unlink()

    if cr_backup.exists():
        cr_backup.unlink()
