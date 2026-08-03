from __future__ import annotations

import json
from pathlib import Path

from ..Contracts.models import InspectorResult, Severity, Violation
from ..Checks.base import safe_digest


class InspectionCache:
    def __init__(self, path: Path):
        self.path = path
        self.values = self._load()

    def _load(self):
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except (OSError, UnicodeError, json.JSONDecodeError):
            return {}

    @staticmethod
    def key(inspector_id, inspector_version, policy_checksum, path, content):
        # Several inspectors make path-sensitive decisions (.env, extensions,
        # policy globs). Content-only keys could reuse a clean result for a
        # dangerous filename containing identical bytes.
        path_digest = safe_digest(path.replace("\\", "/").encode("utf-8"))
        return ":".join((inspector_id, inspector_version, policy_checksum,
                         path_digest, safe_digest(content)))

    def get(self, key):
        value = self.values.get(key)
        if not value:
            return None
        return InspectorResult(
            value["inspector_id"], value["inspector_version"], 0, "CACHED",
            tuple(_violation(item) for item in value["violations"]),
            tuple(_violation(item) for item in value["warnings"]),
        )

    def put(self, key, result):
        self.values[key] = result.to_dict()

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.values, ensure_ascii=False, sort_keys=True), encoding="utf-8", newline="\n")
        temporary.replace(self.path)


def _violation(value):
    return Violation(
        value["code"], Severity(value["severity"]), value["message"], value["recommendation"],
        value.get("path"), value.get("evidence"), value.get("inspector_id"),
    )
