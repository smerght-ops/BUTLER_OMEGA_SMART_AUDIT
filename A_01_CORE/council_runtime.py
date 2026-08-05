"""Bounded multi-model council built on the canonical model-provider layer."""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable

from A_01_CORE.judge_runtime import Evidence, JudgeRuntime
from A_01_CORE.resource_awareness import ResourceAwareness, ResourceSnapshot
from A_01_CORE.runtime_contracts import CancellationToken, ModelLease


class CouncilMode(str, Enum):
    SINGLE = "SINGLE"
    DUAL_REVIEW = "DUAL_REVIEW"
    COUNCIL_3 = "COUNCIL_3"
    COUNCIL_5 = "COUNCIL_5"
    LOCAL_ONLY = "LOCAL_ONLY"


@dataclass(frozen=True)
class CouncilLimits:
    max_workers: int = 5
    max_tokens: int = 8192
    timeout_seconds: float = 180.0
    max_cost: float = 0.0
    cost_per_1000_tokens: float = 0.0

    def __post_init__(self):
        if self.max_workers < 1 or self.max_tokens < 1 or self.timeout_seconds <= 0:
            raise ValueError("council limits must be positive")
        if self.max_cost < 0 or self.cost_per_1000_tokens < 0:
            raise ValueError("council cost limits cannot be negative")


@dataclass(frozen=True)
class CouncilContract:
    prompt: str
    mode: CouncilMode = CouncilMode.SINGLE
    system_prompt: str = "Provide a concise, evidence-based answer."
    limits: CouncilLimits = field(default_factory=CouncilLimits)
    roles: tuple[str, ...] = ("chat", "coder", "chat", "coder", "chat")

    def __post_init__(self):
        if not str(self.prompt or "").strip():
            raise ValueError("council prompt cannot be empty")
        if not self.roles:
            raise ValueError("council roles cannot be empty")


@dataclass(frozen=True)
class ModelWorker:
    worker_id: str
    role: str

    def run(self, provider, contract: CouncilContract, token: CancellationToken) -> dict[str, Any]:
        token.raise_if_cancelled()
        started = time.perf_counter()
        lease = ModelLease("model", self.worker_id, provider="canonical", model=self.role)
        try:
            response = provider.execute_employee(
                employee=self.role,
                system_prompt=contract.system_prompt,
                user_content=contract.prompt,
            )
            token.raise_if_cancelled()
            text = str(response.get("text") or "")
            return {
                "worker_id": self.worker_id,
                "role": self.role,
                "ok": response.get("status") == "ok" and bool(text),
                "text": text,
                "error": response.get("fallback_reason"),
                "model": response.get("model"),
                "latency_ms": int((time.perf_counter() - started) * 1000),
                "estimated_tokens": max(1, len(text) // 4) if text else 0,
            }
        except Exception as exc:
            return {
                "worker_id": self.worker_id,
                "role": self.role,
                "ok": False,
                "text": "",
                "error": f"{type(exc).__name__}: {exc}",
                "model": None,
                "latency_ms": int((time.perf_counter() - started) * 1000),
                "estimated_tokens": 0,
            }
        finally:
            lease.release()


class CouncilRuntime:
    MODE_SIZE = {
        CouncilMode.SINGLE: 1,
        CouncilMode.DUAL_REVIEW: 2,
        CouncilMode.COUNCIL_3: 3,
        CouncilMode.COUNCIL_5: 5,
        CouncilMode.LOCAL_ONLY: 1,
    }
    RAM_THRESHOLDS = {5: 16 * 1024**3, 4: 16 * 1024**3, 3: 8 * 1024**3, 2: 4 * 1024**3, 1: 0}

    def __init__(
        self,
        provider=None,
        judge: JudgeRuntime | None = None,
        resources: ResourceAwareness | None = None,
    ):
        self._provider = provider
        self.judge = judge or JudgeRuntime()
        self.resources = resources or ResourceAwareness()

    def _model_provider(self):
        if self._provider is None:
            from A_02_MANAGERS.smart_dispatcher import get_chat_provider
            self._provider = get_chat_provider()
        return self._provider

    def _size(self, contract: CouncilContract, snapshot: ResourceSnapshot) -> tuple[int, list[str]]:
        requested = min(self.MODE_SIZE[contract.mode], contract.limits.max_workers)
        reasons = []
        available = snapshot.ram_available_bytes
        size = requested
        if available is not None:
            while size > 1 and available < self.RAM_THRESHOLDS[size]:
                size = {5: 3, 4: 3, 3: 2, 2: 1}[size]
            if size != requested:
                reasons.append(f"RAM_FALLBACK:{requested}->{size}")
        if size != self.MODE_SIZE[contract.mode]:
            reasons.append(f"WORKER_LIMIT:{self.MODE_SIZE[contract.mode]}->{size}")
        return size, reasons

    def run(self, contract: CouncilContract, cancellation_token: CancellationToken | None = None) -> dict:
        if not isinstance(contract, CouncilContract):
            raise TypeError("contract must be CouncilContract")
        token = cancellation_token or CancellationToken()
        snapshot = self.resources.snapshot()
        size, fallback = self._size(contract, snapshot)
        workers = [ModelWorker(f"worker_{index + 1}", contract.roles[index % len(contract.roles)]) for index in range(size)]
        responses = []
        started = time.perf_counter()

        if token.is_cancelled:
            return self._result(contract, snapshot, fallback, responses, "CANCELLED", token.reason, started)

        executor = ThreadPoolExecutor(max_workers=size, thread_name_prefix="butler-council")
        futures = [executor.submit(worker.run, self._model_provider(), contract, token) for worker in workers]
        try:
            for future in as_completed(futures, timeout=contract.limits.timeout_seconds):
                responses.append(future.result())
                if token.is_cancelled:
                    break
        except TimeoutError:
            token.cancel("COUNCIL_TIMEOUT")
            fallback.append("TIME_LIMIT_REACHED")
        finally:
            for future in futures:
                future.cancel()
            executor.shutdown(wait=False, cancel_futures=True)

        total_tokens = sum(item["estimated_tokens"] for item in responses)
        estimated_cost = total_tokens * contract.limits.cost_per_1000_tokens / 1000
        error = None
        status = "COMPLETED"
        if token.is_cancelled:
            status, error = "CANCELLED", token.reason
        elif total_tokens > contract.limits.max_tokens:
            status, error = "LIMIT_REACHED", "TOKEN_LIMIT_EXCEEDED"
        elif contract.limits.max_cost and estimated_cost > contract.limits.max_cost:
            status, error = "LIMIT_REACHED", "COST_LIMIT_EXCEEDED"
        elif not any(item["ok"] for item in responses):
            status, error = "FAILED", "NO_SUCCESSFUL_WORKER"
        return self._result(contract, snapshot, fallback, responses, status, error, started, estimated_cost)

    def _result(self, contract, snapshot, fallback, responses, status, error, started, estimated_cost=0.0):
        successful = [item for item in responses if item["ok"]]
        synthesis = max(successful, key=lambda item: (len(item["text"]), item["worker_id"]))["text"] if successful else ""
        ok = status == "COMPLETED" and bool(successful)
        evidence = [
            Evidence(item["worker_id"], "model response", item["text"], verified=item["ok"], kind="model_response")
            for item in responses
        ]
        judgment = self.judge.evaluate({"ok": ok, "error": error, "text": synthesis}, evidence=evidence)
        return {
            "ok": ok,
            "status": status,
            "requested_mode": contract.mode.value,
            "actual_workers": len(responses),
            "fallback": fallback,
            "responses": sorted(responses, key=lambda item: item["worker_id"]),
            "synthesis": synthesis,
            "judge": judgment,
            "limits": asdict(contract.limits),
            "usage": {
                "estimated_tokens": sum(item["estimated_tokens"] for item in responses),
                "estimated_cost": estimated_cost,
                "elapsed_ms": int((time.perf_counter() - started) * 1000),
            },
            "resources": snapshot.to_dict(),
            "error": error,
        }
