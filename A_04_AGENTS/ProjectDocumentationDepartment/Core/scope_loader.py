# -*- coding: utf-8 -*-
import json
from pathlib import Path

class ScopePolicy:
    def __init__(self, scope_file="PROJECT_SCOPE.json"):
        self.scope_data = self._load_scope(scope_file)

        self.ignore_dirs = set(self.scope_data.get("ignore", []))
        self.laboratory = set(self.scope_data.get("laboratory", []))
        self.archives = set(self.scope_data.get("archives", []))

        self.all_ignored_dirs = self.ignore_dirs | self.laboratory | self.archives | {"A_99_TEST_DATA"}

        self.bad_patterns = [
            ".BEFORE", "_BEFORE",
            ".BAK", "_BAK",
            ".BACKUP", "_BACKUP",
            ".OLD", "_OLD",
            ".COPY", "_COPY",
            ".TMP", "_TMP",
            ".SAVE", "_SAVE",
            ".WORKING", "_WORKING",
            ".TEST", "_TEST",
            ".BROKEN", "_BROKEN"
        ]

    def _load_scope(self, filename):
        p = Path(__file__).resolve().parent / filename
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8-sig"))
        return {}

    def is_allowed(self, filepath):
        path_obj = Path(filepath)

        parts = set(path_obj.parts)
        if self.all_ignored_dirs & parts:
            return False

        name_upper = path_obj.name.upper()
        for pattern in self.bad_patterns:
            if pattern in name_upper:
                return False

        return True

policy = ScopePolicy()

def is_allowed(filepath):
    return policy.is_allowed(filepath)

if __name__ == "__main__":
    tests = [
        "A_03_ORCHESTRATION/chat_router.py",
        "A_03_ORCHESTRATION/chat_router.BEFORE_APPEND.py",
        "A_03_ORCHESTRATION/chat_router.STABLE_BEFORE_HYBRID.py",
        "A_99_TEST_DATA/chat_router_bak_pure.py",
        "A_99_TEST_DATA/connect_router_diagnostic.py",
        "A_00_HISTORY/chat_router.py",
        "A_01_CORE/__pycache__/core.pyc"
    ]

    print("--- TEST SCOPE LOADER ---")
    for t in tests:
        print(("ALLOWED" if is_allowed(t) else "IGNORED").ljust(10), ":", t)
