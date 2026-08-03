from __future__ import annotations

import time
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment

from .Core.engine import PublicationGuardianEngine


class PublicationGuardianDepartment(BaseDepartment):
    NAME = "PUBLICATION_GUARDIAN"
    VERSION = "1.0"
    API_VERSION = "v1"
    CAPABILITIES = ("inspect_publication",)

    def __init__(self, engine: PublicationGuardianEngine | None = None):
        root = Path(__file__).resolve().parent
        self.engine = engine or PublicationGuardianEngine(root)

    def can_handle(self, query: str, context: dict = None) -> bool:
        normalized = " ".join(str(query or "").casefold().split())
        return bool((context or {}).get("publication_request")) or any(marker in normalized for marker in (
            "проверить публикацию", "проверка публикации", "publication guardian", "inspect publication",
        ))

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.perf_counter()
        request = dict((context or {}).get("publication_request") or {})
        result = self.engine.inspect(request).to_dict()
        status = result["status"]
        return {
            # At the department boundary, BLOCK/FAULT_BLOCK must never look like
            # a successful operation to a generic dispatcher.
            "ok": status in {"PASS", "PASS_WITH_WARNINGS"},
            "department": self.NAME,
            "model": "PublicationGuardianEngine",
            "latency_ms": int((time.perf_counter() - started) * 1000),
            "text": f"Publication Guardian: {status}",
            "error": None,
            "metadata": {"publication_result": result, "publication_allowed": status in {"PASS", "PASS_WITH_WARNINGS"}},
        }
