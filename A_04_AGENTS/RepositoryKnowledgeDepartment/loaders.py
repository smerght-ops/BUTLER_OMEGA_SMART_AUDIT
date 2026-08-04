"""Strict read-only loaders for the three approved engineering sources."""

import json
from pathlib import Path

import yaml

from .models import Diagnostic


def _strict_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise UnicodeError("UTF8_BOM_NOT_ALLOWED")
    return raw.decode("utf-8")


class ScopeResolver:
    SOURCE = "PROJECT_SCOPE.yaml"
    REQUIRED = (
        "metadata", "production", "engineering", "workspace", "laboratory", "archive",
        "generated", "ignore", "review_required", "classification_rules", "audit_policy",
        "future_consumers",
    )
    CATEGORIES = ("production", "engineering", "workspace", "laboratory", "archive", "generated", "ignore")

    def load(self, root: Path):
        path = root / self.SOURCE
        if not path.is_file():
            return {}, Diagnostic(self.SOURCE, "DEGRADED", "SOURCE_UNAVAILABLE")
        try:
            value = yaml.safe_load(_strict_text(path))
            if not isinstance(value, dict):
                return {}, Diagnostic(self.SOURCE, "DEGRADED", "INVALID_SCHEMA")
            missing = [name for name in self.REQUIRED if name not in value]
            if missing:
                return {}, Diagnostic(self.SOURCE, "DEGRADED", "MISSING_REQUIRED_SECTION", {"sections": missing})
            unknown = sorted(set(value).difference(self.REQUIRED))
            if unknown:
                return {}, Diagnostic(self.SOURCE, "DEGRADED", "UNKNOWN_CATEGORY", {"categories": unknown})
            categories, entries, owners = {}, {}, {}
            for category in self.CATEGORIES:
                rows = value.get(category)
                if not isinstance(rows, list):
                    return {}, Diagnostic(self.SOURCE, "DEGRADED", "INVALID_SCHEMA", {"section": category})
                normalized = []
                normalized_entries = []
                for row in rows:
                    item = {"name": row} if isinstance(row, str) else row
                    if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                        return {}, Diagnostic(self.SOURCE, "DEGRADED", "INVALID_SCHEMA", {"section": category})
                    name = item["name"].strip().replace("\\", "/").rstrip("/")
                    key = name.casefold()
                    if key in owners:
                        return {}, Diagnostic(self.SOURCE, "DEGRADED", "DUPLICATE_PATH_CLASSIFICATION",
                                              {"path": name, "categories": [owners[key], category]})
                    owners[key] = category
                    normalized.append(name)
                    normalized_entries.append({**item, "name": name})
                categories[category] = normalized
                entries[category] = normalized_entries
            result = dict(value)
            result["categories"] = categories
            result["category_entries"] = entries
            result["rules"] = list(value["classification_rules"])
            return result, Diagnostic(self.SOURCE, "OK")
        except yaml.MarkedYAMLError as error:
            mark = getattr(error, "problem_mark", None)
            return {}, Diagnostic(self.SOURCE, "DEGRADED", "YAML_PARSE_ERROR",
                                  {"message": str(error)},
                                  mark.line + 1 if mark else None, mark.column + 1 if mark else None)
        except UnicodeError as error:
            return {}, Diagnostic(self.SOURCE, "DEGRADED", "UTF8_BOM_NOT_ALLOWED" if str(error) == "UTF8_BOM_NOT_ALLOWED" else "INVALID_SCHEMA")
        except OSError:
            return {}, Diagnostic(self.SOURCE, "DEGRADED", "SOURCE_UNAVAILABLE")


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
