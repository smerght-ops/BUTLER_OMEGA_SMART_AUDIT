"""Allow-only policy for Permission Engine Stage 1."""

from .models import PermissionDecision, PermissionRequest


class PermissionEngine:
    def decide(self, request: PermissionRequest) -> PermissionDecision:
        return PermissionDecision.ALLOW
