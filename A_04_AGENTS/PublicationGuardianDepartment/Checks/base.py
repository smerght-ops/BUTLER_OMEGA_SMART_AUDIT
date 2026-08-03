from __future__ import annotations

import hashlib
import re
import time
from abc import ABC, abstractmethod
from typing import Any, Iterable

from ..Contracts.models import InspectorResult, Severity, Violation


class Inspector(ABC):
    inspector_id = "base"
    inspector_version = "1.0"
    cache_per_file = False

    def inspect(self, context: Any, policy: dict) -> InspectorResult:
        started = time.perf_counter()
        violations, warnings = self.run(context, policy)
        return InspectorResult(
            self.inspector_id,
            self.inspector_version,
            int((time.perf_counter() - started) * 1000),
            "COMPLETED",
            tuple(violations),
            tuple(warnings),
        )

    @abstractmethod
    def run(self, context: Any, policy: dict) -> tuple[Iterable[Violation], Iterable[Violation]]:
        raise NotImplementedError

    def finding(self, code: str, severity: str, message: str, recommendation: str,
                path: str | None = None, evidence: str | None = None) -> Violation:
        return Violation(code, Severity(severity), message, recommendation, path,
                         mask_secret(evidence) if evidence else None, self.inspector_id)


def mask_secret(value: str | None) -> str | None:
    if value is None:
        return None
    compact = str(value).replace("\r", "").replace("\n", "\\n")
    if len(compact) <= 4:
        return "*" * len(compact)
    return compact[:3] + "*" * max(8, min(32, len(compact) - 3))


def safe_digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def patterns(policy: dict, section: str) -> list[tuple[str, re.Pattern[str], str]]:
    result = []
    for rule in policy.get(section, []):
        result.append((rule["id"], re.compile(rule["pattern"], re.IGNORECASE | re.MULTILINE), rule["severity"]))
    return result
