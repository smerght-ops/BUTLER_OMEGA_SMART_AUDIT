# -*- coding: utf-8 -*-

import json
from pathlib import Path


class ProjectPassportLoader:

    def __init__(self):
        self.passport_path = (
            Path(__file__).resolve().parent /
            "project_passport.json"
        )

    def load_passport(self):
        with open(
            self.passport_path,
            "r",
            encoding="utf-8-sig"
        ) as f:
            return json.load(f)

    def get_identity(self):
        return self.load_passport().get(
            "project_identity",
            {}
        )

    def get_frozen_modules(self):
        return self.load_passport().get(
            "architecture_freeze",
            {}
        ).get(
            "frozen_modules",
            []
        )

    def get_current_stage(self):
        return self.load_passport().get(
            "project_identity",
            {}
        ).get(
            "current_stage",
            "UNKNOWN"
        )

    def _save_passport(self, data):
        with open(self.passport_path, "w", encoding="utf-8-sig") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def commit_proof(self, proof_key, status_value):
        try:
            passport = self.load_passport()
            if "execution_proof_map" not in passport:
                passport["execution_proof_map"] = {}
            passport["execution_proof_map"][proof_key] = status_value
            self._save_passport(passport)
            return True
        except Exception as e:
            print(f"[PASSPORT API ERROR] {str(e)}")
            return False


    def evaluate_stage_transitions(self):
        """Runtime proofs never advance development-roadmap milestones."""
        return False
