"""Opaque, revocable and device-bound remote access tokens."""

from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import timedelta
from threading import RLock
from typing import Callable

from .remote_models import (
    AuthenticationError,
    DeviceBindingError,
    DeviceIdentity,
    TokenRecord,
    utc_now,
)


class TokenManager:
    def __init__(self, *, clock: Callable = utc_now) -> None:
        self._clock = clock
        self._records: dict[str, TokenRecord] = {}
        self._lock = RLock()

    @staticmethod
    def _digest(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def _split(token: str) -> tuple[str, str]:
        try:
            prefix, token_id, secret = token.split(".", 2)
        except ValueError as exc:
            raise AuthenticationError("INVALID_TOKEN") from exc
        if prefix != "bo9" or not token_id or not secret:
            raise AuthenticationError("INVALID_TOKEN")
        return token_id, secret

    def create_token(
        self,
        device_id: str,
        fingerprint: str,
        *,
        ttl_seconds: float = 3600,
        metadata: dict | None = None,
    ) -> str:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        device = DeviceIdentity(device_id, fingerprint)
        device.validate()
        now = self._clock()
        token_id = secrets.token_urlsafe(12)
        token = f"bo9.{token_id}.{secrets.token_urlsafe(32)}"
        record = TokenRecord(
            token_id=token_id,
            token_digest=self._digest(token),
            device=device,
            created_at=now,
            expires_at=now + timedelta(seconds=ttl_seconds),
            metadata=dict(metadata or {}),
        )
        with self._lock:
            self._records[token_id] = record
        return token

    def verify(self, token: str, device_id: str, fingerprint: str) -> TokenRecord:
        token_id, _ = self._split(token)
        with self._lock:
            record = self._records.get(token_id)
            if record is None or not hmac.compare_digest(
                record.token_digest, self._digest(token)
            ):
                raise AuthenticationError("INVALID_TOKEN")
            if record.revoked:
                raise AuthenticationError("TOKEN_REVOKED")
            if self._clock() >= record.expires_at:
                raise AuthenticationError("TOKEN_EXPIRED")
            if record.device != DeviceIdentity(device_id, fingerprint):
                raise DeviceBindingError("DEVICE_BINDING_MISMATCH")
            return record

    def revoke(self, token: str) -> bool:
        token_id, _ = self._split(token)
        with self._lock:
            record = self._records.get(token_id)
            if record is None or not hmac.compare_digest(
                record.token_digest, self._digest(token)
            ):
                return False
            if not record.revoked:
                record.revoked_at = self._clock()
            return True

    def metadata(self, token_id: str) -> dict:
        with self._lock:
            record = self._records.get(token_id)
            if record is None:
                raise KeyError(token_id)
            return {
                "token_id": record.token_id,
                "device_id": record.device.device_id,
                "fingerprint": record.device.fingerprint,
                "created_at": record.created_at.isoformat(),
                "expires_at": record.expires_at.isoformat(),
                "revoked_at": (
                    record.revoked_at.isoformat() if record.revoked_at else None
                ),
                "metadata": dict(record.metadata),
            }

