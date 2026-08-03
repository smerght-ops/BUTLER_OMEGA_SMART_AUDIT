# -*- coding: utf-8 -*-
"""Read-only access to the generated Butler capability registry."""

from __future__ import annotations

import json
from pathlib import Path


class CapabilityRegistry:
    REQUIRED_FIELDS = {
        "id", "department", "action", "object",
        "input", "output", "confidence", "aliases",
    }

    def __init__(self, path=None):
        self.path = Path(path) if path else Path(__file__).resolve().with_name("CapabilityRegistry.json")

    def load(self) -> dict:
        payload = json.loads(self.path.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, dict) or not isinstance(payload.get("capabilities"), list):
            raise ValueError("INVALID_CAPABILITY_REGISTRY")
        for record in payload["capabilities"]:
            if not isinstance(record, dict) or set(record) != self.REQUIRED_FIELDS:
                raise ValueError("INVALID_CAPABILITY_RECORD")
        return payload

    def all(self) -> list[dict]:
        return list(self.load()["capabilities"])

    def by_department(self, department: str) -> list[dict]:
        target = str(department or "").strip().casefold()
        return [
            record for record in self.all()
            if str(record["department"]).casefold() == target
        ]

    def actions_by_department(self, department: str) -> list[str]:
        return sorted({record["action"] for record in self.by_department(department)})

    def find(self, action=None, object_name=None, alias=None) -> list[dict]:
        action = str(action or "").strip().casefold()
        object_name = str(object_name or "").strip().casefold()
        alias = str(alias or "").strip().casefold()
        results = []
        for record in self.all():
            if action and str(record["action"]).casefold() != action:
                continue
            if object_name and str(record["object"]).casefold() != object_name:
                continue
            if alias and alias not in {str(item).casefold() for item in record["aliases"]}:
                continue
            results.append(record)
        return results
