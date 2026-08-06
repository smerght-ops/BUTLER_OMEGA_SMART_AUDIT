"""Contracts for authenticated remote Butler sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SessionState(str, Enum):
    CREATED = "CREATED"
    AUTHENTICATED = "AUTHENTICATED"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class DeviceIdentity:
    device_id: str
    fingerprint: str

    def validate(self) -> None:
        if not self.device_id.strip() or not self.fingerprint.strip():
            raise ValueError("device_id and fingerprint are required")


@dataclass
class TokenRecord:
    token_id: str
    token_digest: str
    device: DeviceIdentity
    created_at: datetime
    expires_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
    revoked_at: datetime | None = None

    @property
    def revoked(self) -> bool:
        return self.revoked_at is not None


@dataclass
class RemoteSession:
    session_id: str
    device: DeviceIdentity
    token_id: str
    created_at: datetime
    expires_at: datetime
    last_heartbeat_at: datetime
    state: SessionState = SessionState.CREATED
    context: dict[str, Any] = field(default_factory=dict)
    cancellation_token: Any = None


@dataclass(frozen=True)
class AuthenticationResult:
    token_id: str
    device: DeviceIdentity
    metadata: dict[str, Any]


class RemoteAccessError(RuntimeError):
    """Base error safe to return over the remote boundary."""


class AuthenticationError(RemoteAccessError):
    pass


class DeviceBindingError(AuthenticationError):
    pass


class SessionError(RemoteAccessError):
    pass

