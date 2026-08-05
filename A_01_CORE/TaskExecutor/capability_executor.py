from __future__ import annotations

import ast
import importlib
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path

from tools.inspectors.CapabilityRegistry import CapabilityRegistry

from .execution_context import ExecutionContext
from A_01_CORE.event_bus import EventBus
from A_01_CORE.execution_journal import ExecutionJournal
from A_01_CORE.runtime_contracts import (
    CancellationToken,
    ResourceLease,
    TaskContract,
    TaskResult,
    TaskState,
)
from A_07_MEMORY.semantic_memory import SemanticMemory
from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway


class CapabilityExecutor:
    REQUIRED_RESULT_FIELDS = {"ok", "department", "model", "latency_ms", "text", "error", "metadata"}

    def __init__(self, registry_path=None):
        self.root = Path(__file__).resolve().parents[2]
        self.registry = CapabilityRegistry(registry_path or self.root / "CapabilityRegistry.json")
        self._departments = {}
        self._department_sources = None
        self.skill_memory = SemanticMemory()
        self.department_gateway = DepartmentExecutionGateway()
        self.journal = ExecutionJournal(self.root)
        self.journal_dir = self.journal.directory

    def execute(
        self,
        plan: dict | TaskContract,
        context: ExecutionContext | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> dict:
        started = time.time()
        contract = plan if isinstance(plan, TaskContract) else None
        plan = dict(contract.plan) if contract else plan
        task_id = contract.task_id if contract else "task_" + hashlib.sha256(
            json.dumps(plan, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()[:16]
        token = cancellation_token or CancellationToken()
        journal_path = self.journal.path_for(task_id)
        journal = self.journal.load(task_id)
        if context is None and journal.get("final_status") not in {None, "completed"}:
            context = ExecutionContext.from_snapshot(journal.get("context"))
        context = context or ExecutionContext(plan.get("variables"))
        self._active_plan, self._active_task_id, self._active_journal = plan, task_id, journal_path
        self._active_lease = ResourceLease("task_execution", task_id)
        EventBus.publish("task.started", {"task_id": task_id, "goal": plan.get("goal")})
        steps = list(plan.get("steps") or [])
        completed_count = len(context.history)
        self._write_journal(journal_path, plan, context, completed_count, "running")
        missing = [step.get("action") for step in steps if step.get("status") == "missing_capability"]
        if missing:
            return self._final(started, False, "missing_capability", context, missing=missing)

        for index, step in enumerate(steps, 1):
            if index <= completed_count:
                continue
            if token.is_cancelled:
                return self._final(
                    started, False, "cancelled", context,
                    failed_step=index, error=token.reason or "cancelled",
                )
            capability = self._capability(step)
            if capability is None:
                return self._final(
                    started, False, "missing_capability", context,
                    failed_step=index, missing=[step.get("action")],
                )
            try:
                department = self._department(capability["department"])
                arguments = context.resolve(step.get("arguments") or {})
                query = str(arguments.pop("query", None) or step.get("source_text") or step.get("action") or "")
                call_context = dict(arguments)
                call_context.update({
                    "capability_action": capability["action"],
                    "execution_context": context.snapshot(),
                })
                result = None
                last_failure = None
                for attempt in range(1, 3):
                    call_context["retry_attempt"] = attempt
                    candidate = self.department_gateway.execute(
                        department, query, context=call_context
                    )
                    result = candidate
                    if isinstance(candidate, dict) and candidate.get("ok"):
                        break
                    failure = (candidate or {}).get("error") if isinstance(candidate, dict) else type(candidate).__name__
                    if failure == last_failure:
                        break
                    last_failure = failure
            except Exception as exc:
                return self._final(
                    started, False, "execution_error", context,
                    failed_step=index,
                    error=f"{type(exc).__name__}: {exc}",
                )

            if not isinstance(result, dict) or not self.REQUIRED_RESULT_FIELDS.issubset(result):
                return self._final(
                    started, False, "invalid_result_contract", context,
                    failed_step=index,
                )

            if result.get("ok") and capability.get("output") == "image":
                result = self._verify_visual_artifact(
                    department, query, call_context, result,
                )

            output = self._output(result)
            context.record(index, step, result, output)
            self._write_journal(journal_path, plan, context, index, "running")
            if not result.get("ok"):
                return self._final(
                    started, False, "step_failed", context,
                    failed_step=index,
                    error=result.get("error"),
                )

        return self._final(started, True, "completed", context)

    def _verify_visual_artifact(self, creator, query, call_context, result):
        path = self._output(result)
        if not path or not Path(str(path)).is_file():
            return result
        verification = []
        try:
            vision = self._department("VISION")
            check = self.department_gateway.execute(
                vision,
                "Проверь созданный визуальный артефакт и перечисли объективные дефекты.",
                context={"attachments": [str(path)], "verification_mode": True},
            )
            verification.append(check)
            text = str(check.get("text", "")).casefold()
            has_defect = check.get("ok") and any(word in text for word in ("дефект", "ошиб", "искаж", "невер"))
            if has_defect:
                corrected_context = dict(call_context)
                corrected_context["vision_feedback"] = check.get("text")
                corrected = self.department_gateway.execute(
                    creator,
                    f"{query}\nИсправь подтверждённые Vision-дефекты: {check.get('text', '')}",
                    context=corrected_context,
                )
                if corrected.get("ok"):
                    result = corrected
                    path = self._output(corrected)
                    recheck = self.department_gateway.execute(
                        vision,
                        "Повторно проверь исправленный визуальный артефакт.",
                        context={"attachments": [str(path)], "verification_mode": True},
                    )
                    verification.append(recheck)
            result.setdefault("metadata", {})["vision_verification"] = verification
            result["metadata"]["vision_verified"] = bool(verification and verification[-1].get("ok"))
        except Exception as exc:
            result.setdefault("metadata", {})["vision_verification_error"] = f"{type(exc).__name__}: {exc}"
            result["metadata"]["vision_verified"] = False
        return result

    def _write_journal(self, path, plan, context, current_step, status, error=None):
        payload = {
            "task_id": self._active_task_id, "original_request": plan.get("goal"),
            "plan": plan, "current_step": current_step,
            "completed_steps": len(context.history), "artifacts": context.artifacts,
            "errors": [item for item in context.history if item.get("error")],
            "retries": sum(max(0, int(item.get("retry_attempt", 1)) - 1)
                           for item in context.history),
            "verification_status": "passed" if status == "completed" else "pending",
            "final_status": status, "error": error, "context": context.snapshot(),
            "updated_at": datetime.now().isoformat(),
        }
        self.journal.write(self._active_task_id, payload, default=self._json_value)

    def _capability(self, step: dict) -> dict | None:
        capability_id = step.get("capability_id")
        for record in self.registry.all():
            if capability_id and record["id"] == capability_id:
                return record
            if not capability_id and record["action"] == step.get("action"):
                return record
        return None

    def _department(self, name: str):
        if name in self._departments:
            return self._departments[name]
        source = self._sources().get(name)
        if source is None:
            raise LookupError(f"Department source not found for {name}")
        module_name = ".".join(source.with_suffix("").relative_to(self.root).parts)
        module = importlib.import_module(module_name)
        candidates = [
            value for value in vars(module).values()
            if isinstance(value, type) and getattr(value, "NAME", None) == name and callable(getattr(value, "execute", None))
        ]
        if len(candidates) != 1:
            raise LookupError(f"Department class is not unique for {name}")
        instance = candidates[0]()
        self._departments[name] = instance
        return instance

    def _sources(self) -> dict[str, Path]:
        if self._department_sources is not None:
            return self._department_sources
        sources = {}
        for path in sorted((self.root / "A_04_AGENTS").glob("*/runner.py")):
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
            for node in tree.body:
                if not isinstance(node, ast.ClassDef):
                    continue
                for item in node.body:
                    if not isinstance(item, ast.Assign):
                        continue
                    if any(isinstance(target, ast.Name) and target.id == "NAME" for target in item.targets):
                        try:
                            value = ast.literal_eval(item.value)
                        except (ValueError, TypeError, SyntaxError):
                            continue
                        if isinstance(value, str):
                            sources[value] = path
        self._department_sources = sources
        return sources

    @staticmethod
    def _output(result: dict):
        metadata = result.get("metadata") or {}
        search_results = result.get("results") or metadata.get("results") or []
        first_path = next((item.get("filepath") or item.get("path")
                           for item in search_results if isinstance(item, dict)
                           and (item.get("filepath") or item.get("path"))), None)
        return (
            metadata.get("output")
            or result.get("image_path")
            or metadata.get("image_path")
            or first_path
            or result.get("text")
            or ""
        )

    def _final(self, started, ok, status, context, failed_step=None, missing=None, error=None):
        artifacts = context.artifacts
        paths = [item["path"] for item in artifacts]
        text = "Задача выполнена." if ok else f"Выполнение остановлено: {status}."
        if paths:
            text += "\nАртефакты:\n" + "\n".join(paths)
        result = {
            "ok": bool(ok),
            "department": "TASK_EXECUTOR",
            "model": "CapabilityExecutor",
            "latency_ms": max(0, int((time.time() - started) * 1000)),
            "text": text,
            "error": error if error is not None else (None if ok else status.upper()),
            "metadata": {
                "status": status,
                "failed_step": failed_step,
                "missing": list(dict.fromkeys(item for item in (missing or []) if item)),
                "artifacts": artifacts,
                "history": context.history,
                "results": context.results,
                "variables": context.variables,
                "task_id": getattr(self, "_active_task_id", None),
                "resumable_journal": str(getattr(self, "_active_journal", "")),
            },
        }
        state = {
            "completed": TaskState.COMPLETED,
            "cancelled": TaskState.CANCELLED,
        }.get(status, TaskState.FAILED)
        structured = TaskResult(
            task_id=getattr(self, "_active_task_id", ""),
            state=state,
            ok=bool(ok),
            output=text,
            error=result["error"],
            metadata={"failed_step": failed_step, "artifacts": artifacts},
        )
        result["metadata"]["structured_result"] = structured.to_dict()
        journal_path = getattr(self, "_active_journal", None)
        plan = getattr(self, "_active_plan", {})
        if journal_path:
            self._write_journal(journal_path, plan, context, failed_step or len(context.history), status, error)
        if ok and context.history:
            signature = [step.get("capability_id") or step.get("action")
                         for step in plan.get("steps", [])]
            learned = self.skill_memory.record_tested_skill(
                signature, context.history, provenance=str(journal_path),
            )
            result["metadata"]["procedural_learning"] = learned
            result["metadata"]["procedural_reuse"] = bool(
                (plan.get("procedural_memory") or {}).get("reused")
            )
        log_dir = self.root / "A_08_LOGS"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / f"execution_log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        log_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=self._json_value) + "\n",
            encoding="utf-8",
        )
        result["metadata"]["execution_log"] = str(log_path)
        lease = getattr(self, "_active_lease", None)
        if lease is not None:
            lease.release()
            result["metadata"]["resource_lease"] = {
                "lease_id": lease.lease_id,
                "resource": lease.resource,
                "released_at": lease.released_at,
            }
        EventBus.publish("task.finished", result["metadata"]["structured_result"])
        return result

    @staticmethod
    def _json_value(value):
        to_dict = getattr(value, "to_dict", None)
        if callable(to_dict):
            return to_dict(include_locator=True)
        raise TypeError(f"not JSON serializable: {type(value).__name__}")
