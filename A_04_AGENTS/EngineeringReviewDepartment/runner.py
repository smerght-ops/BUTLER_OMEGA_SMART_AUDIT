# -*- coding: utf-8 -*-
"""Engineering Review Department — read-only engineering verification.

This department performs a complete engineering review of project changes
without modifying any files. It is invoked through the standard Butler
architecture (SmartDispatcherV2 → DepartmentExecutionGateway).
"""

import time
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment
from A_03_ORCHESTRATION.observation_layer import ObservationLayer
from .checker import run_full_review, format_report


class EngineeringReviewDepartment(BaseDepartment):
    NAME = "ENGINEERING_REVIEW"
    VERSION = "1.0"
    CAPABILITIES = ("engineering_review", "project_audit", "change_verification")
    KEYWORDS = (
        "engineering review", "инженерная ревизия", "инженерный аудит",
        "проверка изменений", "engineering audit", "change verification",
        "приёмка изменений", "revision check",
    )

    def __init__(self, root=None, observation=None):
        self.root = Path(root or Path(__file__).resolve().parents[2]).resolve()
        self.observation = observation or ObservationLayer()

    def can_handle(self, query: str, context: dict = None) -> bool:
        normalized = " ".join(str(query or "").casefold().split())
        return any(marker in normalized for marker in self.KEYWORDS)

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.perf_counter()
        try:
            report = run_full_review()
            text = format_report(report)
            return self._result(started, True, {"report": report}, None, text=text)
        except Exception as error:
            return self._result(started, False, {}, f"{type(error).__name__}: {error}")

    def _result(self, started, ok, data, error, text=None):
        return {
            "ok": bool(ok),
            "department": self.NAME,
            "model": "EngineeringReviewDepartment",
            "latency_ms": int((time.perf_counter() - started) * 1000),
            "text": text or ("Engineering review completed." if ok else "Engineering review failed."),
            "error": error,
            "metadata": {"engineering_review": data},
        }
