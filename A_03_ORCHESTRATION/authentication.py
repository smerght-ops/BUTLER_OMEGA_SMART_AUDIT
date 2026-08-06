"""Authentication boundary used before a remote session is allocated."""

from __future__ import annotations

from collections.abc import Mapping

from .remote_models import AuthenticationError, AuthenticationResult
from .token_manager import TokenManager


class RemoteAuthenticator:
    def __init__(self, token_manager: TokenManager) -> None:
        self.token_manager = token_manager

    @staticmethod
    def token_from_headers(headers: Mapping[str, str]) -> str:
        normalized = {str(key).lower(): str(value) for key, value in headers.items()}
        api_key = normalized.get("x-api-key")
        authorization = normalized.get("authorization", "")
        if api_key:
            return api_key.strip()
        if authorization.lower().startswith("bearer "):
            return authorization[7:].strip()
        raise AuthenticationError("AUTHENTICATION_REQUIRED")

    def authenticate(
        self, token: str, device_id: str, fingerprint: str
    ) -> AuthenticationResult:
        record = self.token_manager.verify(token, device_id, fingerprint)
        return AuthenticationResult(
            token_id=record.token_id,
            device=record.device,
            metadata=dict(record.metadata),
        )

    def authenticate_headers(
        self, headers: Mapping[str, str], device_id: str, fingerprint: str
    ) -> AuthenticationResult:
        return self.authenticate(
            self.token_from_headers(headers), device_id, fingerprint
        )

