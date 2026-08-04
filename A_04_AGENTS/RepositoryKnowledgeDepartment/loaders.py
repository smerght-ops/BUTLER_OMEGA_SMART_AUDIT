"""Strict read-only loaders for the three approved engineering sources."""

import json
from pathlib import Path

from .models import Diagnostic


def _strict_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise UnicodeError("UTF8_BOM_NOT_ALLOWED")
    return raw.decode("utf-8")


class ScopeResolver:
    SOURCE = "PROJECT_SCOPE.yaml"

    def load(self, root: Path):
        path = root / self.SOURCE
        if not path.is_file():
            return {}, Diagnostic(self.SOURCE, "DEGRADED", "SOURCE_UNAVAILABLE")
        try:
            text = _strict_text(path)
            result = {"metadata": {}, "categories": {}, "rules": []}
            section = None
            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or line == "---":
                    continue
                if not raw_line.startswith((" ", "\t")) and line.endswith(":"):
                    section = line[:-1]
                    result["categories"].setdefault(section, [])
                elif line.startswith("- name:") and section:
                    result["categories"].setdefault(section, []).append(
                        line.split(":", 1)[1].strip().strip('"\'')
                    )
                elif section == "metadata" and ":" in line:
                    key, value = line.split(":", 1)
                    result["metadata"][key.strip()] = value.strip().strip('"\'')
                elif section == "classification_rules" and line.startswith("-"):
                    result["rules"].append(line[1:].strip().strip('"'))
            return result, Diagnostic(self.SOURCE, "OK")
        except (OSError, UnicodeError, ValueError) as error:
            return {}, Diagnostic(self.SOURCE, "DEGRADED", type(error).__name__)


class ManifestLoader:
    SOURCE = "system_manifest.json"

    def load(self, root: Path):
        path = root / self.SOURCE
        if not path.is_file():
            return {}, Diagnostic(self.SOURCE, "DEGRADED", "SOURCE_UNAVAILABLE")
        try:
            value = json.loads(_strict_text(path))
            if not isinstance(value, dict):
                raise ValueError("MANIFEST_NOT_OBJECT")
            return value, Diagnostic(self.SOURCE, "OK")
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
            return {}, Diagnostic(self.SOURCE, "DEGRADED", type(error).__name__)


class InventoryLoader:
    SOURCE = "A_00_ARCHITECTURE/RECONSTRUCTION_INVENTORY.json"

    def load(self, root: Path):
        path = root / Path(self.SOURCE)
        if not path.is_file():
            return {}, Diagnostic(self.SOURCE, "DEGRADED", "SOURCE_UNAVAILABLE")
        try:
            value = json.loads(_strict_text(path))
            if not isinstance(value, dict):
                raise ValueError("INVENTORY_NOT_OBJECT")
            return value, Diagnostic(self.SOURCE, "OK")
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
            return {}, Diagnostic(self.SOURCE, "DEGRADED", type(error).__name__)
