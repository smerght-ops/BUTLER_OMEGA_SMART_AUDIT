"""Shared, dependency-free contracts for the Butler task runtime."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class TaskState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CancellationToken:
    """Thread-safe cooperative cancellation signal."""

    def __init__(self) -> None:
        self._event = threading.Event()
        self._reason: str | None = None

    def cancel(self, reason: str = "cancelled") -> None:
        self._reason = str(reason or "cancelled")
        self._event.set()

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()

    @property
    def reason(self) -> str | None:
        return self._reason

    def raise_if_cancelled(self) -> None:
        if self.is_cancelled:
            raise RuntimeError(f"TASK_CANCELLED:{self.reason}")


@dataclass(frozen=True)
class TaskContract:
    goal: str
    plan: Mapping[str, Any]
    task_id: str = field(default_factory=lambda: "task_" + uuid.uuid4().hex[:16])
    created_at: str = field(default_factory=utc_now)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_plan(cls, plan: Mapping[str, Any], task_id: str) -> "TaskContract":
        return cls(goal=str(plan.get("goal") or ""), plan=dict(plan), task_id=task_id)


@dataclass(frozen=True)
class TaskResult:
    task_id: str
    state: TaskState
    ok: bool
    output: Any = None
    error: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    completed_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "state": self.state.value,
            "ok": self.ok,
            "output": self.output,
            "error": self.error,
            "metadata": dict(self.metadata),
            "completed_at": self.completed_at,
        }


@dataclass
class ResourceLease:
    resource: str
    owner: str
    lease_id: str = field(default_factory=lambda: "lease_" + uuid.uuid4().hex[:16])
    acquired_at: str = field(default_factory=utc_now)
    released_at: str | None = None

    @property
    def active(self) -> bool:
        return self.released_at is None

    def release(self) -> None:
        if self.released_at is None:
            self.released_at = utc_now()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.release()


@dataclass
class ModelLease(ResourceLease):
    provider: str = "unknown"
    model: str = "unknown"
