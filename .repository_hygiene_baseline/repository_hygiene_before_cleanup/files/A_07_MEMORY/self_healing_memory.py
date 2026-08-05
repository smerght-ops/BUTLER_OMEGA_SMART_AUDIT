import json
from pathlib import Path
from datetime import datetime

class SelfHealingMemory:

    def __init__(self):
        self.profile_path = Path(__file__).resolve().parent / "profile_manager.py"
        self.backup_path = Path(__file__).resolve().parent / "memory_backups"
        self.backup_path.mkdir(exist_ok=True)

    def validate_profile(self, profile_data: dict):

        if not isinstance(profile_data, dict):
            return False, "INVALID_PROFILE_TYPE"

        required_sections = ["user_name", "preferences", "hardware", "projects", "settings"]

        missing = [s for s in required_sections if s not in profile_data]

        if missing:
            return False, f"MISSING_SECTIONS: {missing}"

        return True, "OK"

    def backup_profile(self, raw_text: str):

        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        file = self.backup_path / f"profile_backup_{ts}.json"

        file.write_text(raw_text, encoding="utf-8")

        return str(file)

    def heal_profile(self, raw_text: str):

        try:
            profile = json.loads(raw_text)
        except Exception:
            return {
                "status": "CORRUPTED_JSON",
                "action": "RESTORE_FROM_LAST_BACKUP"
            }

        ok, status = self.validate_profile(profile)

        if not ok:
            return {
                "status": status,
                "action": "REPAIR_REQUIRED",
                "missing": status
            }

        return {
            "status": "OK",
            "action": "NO_HEALING_REQUIRED"
        }

    def auto_repair(self, profile_path: str):

        path = Path(profile_path)

        if not path.exists():
            return {"status": "FILE_MISSING", "action": "CREATE_DEFAULT_PROFILE"}

        raw = path.read_text(encoding="utf-8-sig")

        # backup before anything
        backup_file = self.backup_profile(raw)

        result = self.heal_profile(raw)

        result["backup"] = backup_file

        return result


if __name__ == "__main__":
    healer = SelfHealingMemory()
    print(healer.auto_repair("A_05_STORAGE/user_profile.json"))
