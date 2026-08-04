"""Explicit, fail-open Stage 1 gateway for executing a selected Department."""

from contextvars import ContextVar
import inspect
import sys
from typing import Optional

from A_03_ORCHESTRATION.observation_layer import ObservationLayer

from .engine import PermissionEngine
from .models import PermissionDecision, PermissionRequest


_current_request: ContextVar[Optional[PermissionRequest]] = ContextVar(
    "permission_current_request", default=None
)
_active_decisions: ContextVar[dict] = ContextVar("permission_active_decisions", default={})


def _department_identity(department) -> str:
    return str(
        getattr(department, "NAME", getattr(department, "name", type(department).__name__))
    )


def _caller_identity() -> str:
    frame = inspect.currentframe()
    try:
        caller = frame.f_back.f_back if frame and frame.f_back else None
        if caller is None:
            return "UNKNOWN"
        module = caller.f_globals.get("__name__", "UNKNOWN")
        return f"{module}:{caller.f_code.co_name}:{caller.f_lineno}"
    finally:
        del frame


class DepartmentExecutionGateway:
    """Make one permission decision, then transparently call ``department.execute``."""

    def __init__(self, engine=None, observation=None):
        self.engine = engine or PermissionEngine()
        self.observation = observation or ObservationLayer()

    def _record(self, request, decision, engine_error=None):
        payload = {
            "execution_id": request.execution_id,
            "parent_execution_id": request.parent_execution_id,
            "department": request.department,
            "caller": request.caller,
            "decision": decision.value,
            "engine_error": engine_error,
        }
        try:
            self.observation.record(
                source="PermissionEngine",
                event="PERMISSION_DECISION_STAGE1",
                payload=payload,
            )
        except Exception as error:
            # Logging must never recursively block Department execution on Stage 1.
            print(f"[PERMISSION_LOG_ERROR] {type(error).__name__}: {error}", file=sys.stderr)

    def execute(self, department, *args, permission_request=None, **kwargs):
        parent = _current_request.get()
        request = permission_request or PermissionRequest.create(
            department=_department_identity(department),
            caller=_caller_identity(),
            parent_execution_id=parent.execution_id if parent else None,
        )

        decisions = _active_decisions.get()
        decision = decisions.get(request.execution_id)
        if decision is None:
            engine_error = None
            try:
                decision = self.engine.decide(request)
            except Exception as error:
                # Stage 1 is deliberately fail-open. Future stages may choose otherwise.
                decision = PermissionDecision.ALLOW
                engine_error = f"{type(error).__name__}: {error}"
            self._record(request, decision, engine_error)

        decisions_token = _active_decisions.set({**decisions, request.execution_id: decision})
        request_token = _current_request.set(request)
        try:
            return department.execute(*args, **kwargs)
        finally:
            _current_request.reset(request_token)
            _active_decisions.reset(decisions_token)
