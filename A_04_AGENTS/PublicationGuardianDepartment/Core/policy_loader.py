from __future__ import annotations

import hashlib
import json
from pathlib import Path


REQUIRED_POLICY_FIELDS = {"policy_id", "version", "created_at", "updated_at", "author", "checksum"}
VALID_CATEGORIES = {"ALLOW", "DENY", "WARNING", "LIMIT", "REQUIRED", "OPTIONAL"}


def canonical_checksum(policy: dict) -> str:
    value = {key: item for key, item in policy.items() if key != "checksum"}
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load_policy(path: Path, expected_version: str) -> dict:
    try:
        policy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PolicyError(f"Policy cannot be loaded: {exc}") from exc
    missing = REQUIRED_POLICY_FIELDS.difference(policy)
    if missing:
        raise PolicyError("Policy fields missing: " + ", ".join(sorted(missing)))
    if policy["version"] != expected_version:
        raise PolicyError("Requested policy version is unavailable")
    if policy["checksum"] != canonical_checksum(policy):
        raise PolicyError("Policy checksum mismatch")
    for rule in policy.get("rules", []):
        if rule.get("category") not in VALID_CATEGORIES:
            raise PolicyError(f"Unsupported policy category: {rule.get('category')}")
    return policy


class PolicyError(Exception):
    pass
