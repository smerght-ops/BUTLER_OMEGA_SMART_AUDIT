"""Stage 1 permission boundary for explicit Department execution."""

from .engine import PermissionEngine
from .gateway import DepartmentExecutionGateway
from .models import PermissionDecision, PermissionRequest

__all__ = [
    "DepartmentExecutionGateway",
    "PermissionDecision",
    "PermissionEngine",
    "PermissionRequest",
]
