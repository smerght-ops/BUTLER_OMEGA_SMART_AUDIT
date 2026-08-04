"""Minimal immutable models used by the Stage 1 permission gateway."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, Optional
from uuid import uuid4


class PermissionDecision(str, Enum):
    ALLOW = "ALLOW"


@dataclass(frozen=True)
class PermissionRequest:
    execution_id: str
    parent_execution_id: Optional[str]
    department: str
    caller: str
    timestamp: str
    metadata: Mapping[str, Any] = field(default_factory=dict)
    action: Optional[str] = None
    resource: Optional[str] = None

    @classmethod
    def create(
        cls,
        department: str,
        caller: str,
        parent_execution_id: Optional[str] = None,
        metadata: Optional[Mapping[str, Any]] = None,
    ) -> "PermissionRequest":
        return cls(
            execution_id=str(uuid4()),
            parent_execution_id=parent_execution_id,
            department=department,
            caller=caller,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=dict(metadata or {}),
        )
