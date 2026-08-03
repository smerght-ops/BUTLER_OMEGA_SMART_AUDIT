from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


API_VERSION = "v1"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class Violation:
    code: str
    severity: Severity
    message: str
    recommendation: str
    path: str | None = None
    evidence: str | None = None
    inspector_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["severity"] = self.severity.value
        return value


@dataclass(frozen=True)
class InspectorResult:
    inspector_id: str
    inspector_version: str
    execution_time_ms: int
    status: str
    violations: tuple[Violation, ...] = ()
    warnings: tuple[Violation, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "inspector_id": self.inspector_id,
            "inspector_version": self.inspector_version,
            "execution_time_ms": self.execution_time_ms,
            "status": self.status,
            "violations": [item.to_dict() for item in self.violations],
            "warnings": [item.to_dict() for item in self.warnings],
        }


@dataclass(frozen=True)
class PublicationRequest:
    api_version: str
    request_id: str
    timestamp: str
    initiator: str
    publication_target: str
    publication_mode: str
    publication_scope: str
    repository_root: str
    git_reference: str
    staged_files: tuple[str, ...]
    policy_version: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "PublicationRequest":
        if not isinstance(value, dict):
            raise ValueError("PublicationRequest must be an object")
        required = (
            "api_version", "request_id", "timestamp", "initiator", "publication_target",
            "publication_mode", "publication_scope", "repository_root", "git_reference",
            "staged_files", "policy_version", "metadata",
        )
        missing = [key for key in required if key not in value]
        if missing:
            raise ValueError("Missing required fields: " + ", ".join(missing))
        if value["api_version"] != API_VERSION:
            raise ValueError(f"Unsupported api_version: {value['api_version']}")
        if not value["request_id"] or not isinstance(value["staged_files"], (list, tuple)):
            raise ValueError("request_id must be non-empty and staged_files must be a list")
        if not isinstance(value["metadata"], dict):
            raise ValueError("metadata must be an object")
        return cls(**{**value, "staged_files": tuple(str(path) for path in value["staged_files"])})


@dataclass(frozen=True)
class PublicationResult:
    api_version: str
    request_id: str
    status: str
    execution_time_ms: int
    inspectors: tuple[dict[str, Any], ...]
    violations: tuple[dict[str, Any], ...]
    warnings: tuple[dict[str, Any], ...]
    report: dict[str, Any]
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
