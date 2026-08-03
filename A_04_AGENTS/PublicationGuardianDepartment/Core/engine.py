from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

from ..Checks import DEFAULT_INSPECTORS
from ..Contracts.models import InspectorResult, PublicationRequest, PublicationResult, Severity, Violation
from ..Reports.writer import ReportWriter
from .cache import InspectionCache
from .context import build_context
from .policy_loader import PolicyError, load_policy


class PublicationGuardianEngine:
    API_VERSION = "v1"

    def __init__(self, department_root: Path, runtime_root: Path | None = None,
                 inspector_types=None, policy_path: Path | None = None):
        self.department_root = department_root
        self.runtime_root = runtime_root or department_root / "Resources" / "runtime"
        self.inspector_types = tuple(DEFAULT_INSPECTORS if inspector_types is None else inspector_types)
        self.policy_path = policy_path or department_root / "Policies" / "default_v1.json"
        self.state = "UNINITIALIZED"

    def inspect(self, raw_request: dict) -> PublicationResult:
        started = time.perf_counter()
        request_id = str(raw_request.get("request_id", "unknown")) if isinstance(raw_request, dict) else "unknown"
        request = None
        policy = None
        inspector_results = []
        context = None
        try:
            self._log(request_id, "department", "START", "INFO", 0)
        except OSError:
            return self._failure(request_id, "FAULT_BLOCK", "AUDIT_ERROR",
                                 "Runtime journal is unavailable", started, raw_request,
                                 persist=False, log=False)
        try:
            request = PublicationRequest.from_dict(raw_request)
        except (TypeError, ValueError) as exc:
            return self._failure(request_id, "BLOCK", "INPUT_ERROR", str(exc), started, raw_request)
        try:
            policy = load_policy(self.policy_path, request.policy_version)
            self.state = "READY"
            ordered_types = self._ordered_inspector_types()
            registered = frozenset(item.inspector_id for item in (kind() for kind in ordered_types))
            required_missing = set(policy.get("required_inspectors", ())).difference(registered)
            context = build_context(request, registered)
            self.state = "EXECUTING"
            cache = InspectionCache(self.runtime_root / "cache.json")
            had_fault = bool(required_missing)
            for kind in ordered_types:
                inspector = kind()
                inspector_started = time.perf_counter()
                try:
                    result = self._run_inspector(inspector, context, policy, cache)
                except Exception as exc:
                    had_fault = True
                    result = InspectorResult(
                        inspector.inspector_id, inspector.inspector_version,
                        int((time.perf_counter() - inspector_started) * 1000), "FAILED",
                        (Violation(
                            "INSPECTOR_ERROR", Severity.BLOCK,
                            f"Инспектор {inspector.inspector_id} завершился ошибкой.",
                            "Восстановите инспектор и повторите проверку.", inspector_id=inspector.inspector_id,
                        ),), (),
                    )
                    self._log(request.request_id, inspector.inspector_id, "FAILED", "BLOCK",
                              result.execution_time_ms, type(exc).__name__)
                else:
                    top = _top_severity((*result.violations, *result.warnings))
                    self._log(request.request_id, inspector.inspector_id, result.status, top,
                              result.execution_time_ms)
                inspector_results.append(result)
            cache.save()
            violations = tuple(item for result in inspector_results for item in result.violations)
            warnings = tuple(item for result in inspector_results for item in result.warnings)
            status = "FAULT_BLOCK" if had_fault else _decision((*violations, *warnings))
            return self._complete(request, policy, context, inspector_results, violations, warnings,
                                  status, started)
        except PolicyError as exc:
            return self._failure(request.request_id, "FAULT_BLOCK", "POLICY_ERROR", str(exc), started, raw_request)
        except (OSError, RuntimeError, UnicodeError) as exc:
            return self._failure(request.request_id, "FAULT_BLOCK", "SYSTEM_ERROR", str(exc), started, raw_request)
        except Exception as exc:
            return self._failure(request.request_id, "FAULT_BLOCK", "UNKNOWN_ERROR", str(exc), started, raw_request)

    def _run_inspector(self, inspector, context, policy, cache):
        if not inspector.cache_per_file:
            return inspector.inspect(context, policy)
        results = []
        for item in context.files:
            key = cache.key(inspector.inspector_id, inspector.inspector_version, policy["checksum"],
                            item.path, item.content)
            result = cache.get(key)
            if result is None:
                result = inspector.inspect(context.for_file(item), policy)
                cache.put(key, result)
            results.append(result)
        return InspectorResult(
            inspector.inspector_id, inspector.inspector_version,
            sum(item.execution_time_ms for item in results),
            "CACHED" if results and all(item.status == "CACHED" for item in results) else "COMPLETED",
            tuple(item for result in results for item in result.violations),
            tuple(item for result in results for item in result.warnings),
        )

    def _complete(self, request, policy, context, inspector_results, violations, warnings, status, started):
        duration = int((time.perf_counter() - started) * 1000)
        self.state = "REPORT"
        writer = ReportWriter(self.runtime_root)
        report = writer.build(request, policy, inspector_results, status, duration, violations, warnings)
        try:
            path = writer.persist(report, tuple(item.path for item in context.files))
            report["file_count"] = len(context.files)
            report["path"] = str(path)
        except OSError as exc:
            self.state = "FAIL_CLOSED"
            return self._failure(request.request_id, "FAULT_BLOCK", "SYSTEM_ERROR",
                                 f"Report persistence failed: {exc}", started, request.__dict__, persist=False)
        self.state = "READY"
        self._log(request.request_id, "department", status, _top_severity((*violations, *warnings)), duration)
        recommendation = "Публикация разрешена." if status == "PASS" else "Выполните рекомендации отчёта до публикации."
        return PublicationResult(
            request.api_version, request.request_id, status, duration,
            tuple(item.to_dict() for item in inspector_results),
            tuple(item.to_dict() for item in violations), tuple(item.to_dict() for item in warnings),
            report, recommendation,
        )

    def _failure(self, request_id, status, category, message, started, raw_request,
                 persist=True, log=True):
        duration = int((time.perf_counter() - started) * 1000)
        self.state = "FAIL_CLOSED"
        violation = Violation(
            category, Severity.BLOCK, f"Проверка заблокирована: {category}.",
            "Исправьте указанную ошибку и повторите полную проверку.",
            evidence=type(message).__name__, inspector_id="department",
        )
        report = {
            "report_id": f"publication-{request_id}", "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id, "policy_version": str(raw_request.get("policy_version", "unknown")) if isinstance(raw_request, dict) else "unknown",
            "api_version": str(raw_request.get("api_version", self.API_VERSION)) if isinstance(raw_request, dict) else self.API_VERSION,
            "inspectors": [], "duration_ms": duration, "file_count": 0, "warning_count": 0,
            "violation_count": 1, "violations": [violation.to_dict()], "warnings": [], "status": status,
            "recommendations": [violation.recommendation], "error_category": category,
        }
        if persist:
            try:
                path = ReportWriter(self.runtime_root).persist(report, ())
                report["path"] = str(path)
            except OSError:
                report["path"] = None
        if log:
            try:
                self._log(request_id, "department", status, "BLOCK", duration, category)
            except OSError:
                pass
        return PublicationResult(
            self.API_VERSION, request_id, status, duration, (), (violation.to_dict(),), (), report,
            violation.recommendation,
        )

    def _ordered_inspector_types(self):
        canonical = {kind.inspector_id: index for index, kind in enumerate(DEFAULT_INSPECTORS)}
        instances = [kind() for kind in self.inspector_types]
        identifiers = [item.inspector_id for item in instances]
        if len(identifiers) != len(set(identifiers)):
            raise RuntimeError("Duplicate inspector identifier")
        pairs = list(zip(self.inspector_types, instances))
        return tuple(kind for kind, item in sorted(
            pairs, key=lambda pair: (canonical.get(pair[1].inspector_id, len(canonical)),
                                     pair[1].inspector_id)
        ))

    def _log(self, request_id, inspector, result, severity, duration, detail=None):
        self.runtime_root.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(), "request_id": request_id,
            "inspector": inspector, "duration": duration, "result": result, "severity": severity,
        }
        if detail:
            record["detail"] = detail
        with (self.runtime_root / "guardian.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _decision(findings):
    severities = {item.severity for item in findings}
    if Severity.BLOCK in severities or Severity.CRITICAL in severities:
        return "BLOCK"
    if Severity.HIGH in severities or Severity.WARNING in severities:
        return "PASS_WITH_WARNINGS"
    return "PASS"


def _top_severity(findings):
    order = {Severity.INFO: 0, Severity.WARNING: 1, Severity.HIGH: 2, Severity.CRITICAL: 3, Severity.BLOCK: 4}
    return max((item.severity for item in findings), key=lambda value: order[value]).value if findings else "INFO"
