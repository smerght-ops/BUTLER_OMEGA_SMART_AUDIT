# -*- coding: utf-8 -*-
"""Infrastructure contract and compatibility validator for Department results."""

from __future__ import annotations

from typing import Any


RESULT_SUCCESS = "SUCCESS"
RESULT_CONTROLLED_FAILURE = "CONTROLLED_FAILURE"
RESULT_NO_RESULT = "NO_RESULT"
RESULT_INVALID = "INVALID_RESULT"


def _invalid(reason: str) -> dict[str, Any]:
    return {
        "valid": False,
        "outcome": RESULT_INVALID,
        "normalized": None,
        "error": reason,
    }


def validate_department_result(result: Any, department_name: str) -> dict[str, Any]:
    """Validate and normalize current and legacy Department result dictionaries."""

    if result is None:
        return {
            "valid": False,
            "outcome": RESULT_NO_RESULT,
            "normalized": None,
            "error": "DEPARTMENT_NO_RESULT",
        }

    if not isinstance(result, dict):
        return _invalid("DEPARTMENT_RESULT_NOT_DICT")

    recognized_keys = {
        "ok", "status", "department", "text", "message",
        "permanent", "project", "session", "error",
    }
    if not result or not (recognized_keys & set(result)):
        return _invalid("DEPARTMENT_RESULT_UNRECOGNIZED_DICT")

    normalized = dict(result)

    if "ok" in normalized and not isinstance(normalized["ok"], bool):
        return _invalid("DEPARTMENT_RESULT_OK_NOT_BOOL")

    metadata = normalized.get("metadata", {})
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        return _invalid("DEPARTMENT_RESULT_METADATA_NOT_DICT")

    if "ok" in normalized:
        ok = normalized["ok"]
    else:
        legacy_status = str(normalized.get("status", "")).strip().lower()
        if legacy_status in {"error", "failed", "failure"}:
            ok = False
        elif normalized.get("error") not in (None, ""):
            ok = False
        else:
            ok = True

    if ok and normalized.get("error") not in (None, ""):
        return _invalid("DEPARTMENT_RESULT_OK_WITH_ERROR")

    latency = normalized.get("latency_ms", 0)
    if isinstance(latency, bool) or not isinstance(latency, (int, float)):
        latency = 0

    normalized["ok"] = ok
    normalized["department"] = str(
        normalized.get("department") or department_name
    )
    normalized.setdefault("model", None)
    normalized["latency_ms"] = max(0, int(latency))
    normalized["text"] = str(normalized.get("text") or "")
    normalized["metadata"] = metadata

    if ok:
        normalized["error"] = None
        outcome = RESULT_SUCCESS
    else:
        normalized["error"] = str(
            normalized.get("error") or "DEPARTMENT_CONTROLLED_FAILURE"
        )
        outcome = RESULT_CONTROLLED_FAILURE

    return {
        "valid": True,
        "outcome": outcome,
        "normalized": normalized,
        "error": None,
    }
