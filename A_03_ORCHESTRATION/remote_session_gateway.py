"""Single remote-session gateway into the existing Agent Core coordinator."""

from __future__ import annotations

import inspect
from datetime import timedelta
from threading import RLock
from typing import Callable
from uuid import uuid4

from A_01_CORE.runtime_contracts import CancellationToken

from .authentication import RemoteAuthenticator
from .observation_layer import ObservationLayer
from .remote_models import (
    AuthenticationResult,
    RemoteSession,
    SessionError,
    SessionState,
    utc_now,
)


class RemoteSessionGateway:
    _TRANSITIONS = {
        SessionState.CREATED: {SessionState.AUTHENTICATED, SessionState.CLOSED},
        SessionState.AUTHENTICATED: {SessionState.ACTIVE, SessionState.CLOSED},
        SessionState.ACTIVE: {
            SessionState.EXPIRED,
            SessionState.CLOSED,
        },
        SessionState.EXPIRED: {SessionState.CLOSED},
        SessionState.CLOSED: set(),
    }

    def __init__(
        self,
        coordinator,
        authenticator: RemoteAuthenticator,
        *,
        heartbeat_timeout_seconds: float = 60,
        session_ttl_seconds: float = 3600,
        clock: Callable = utc_now,
        telemetry=None,
    ) -> None:
        if heartbeat_timeout_seconds <= 0 or session_ttl_seconds <= 0:
            raise ValueError("session timeouts must be positive")
        self._assert_coordinator_contract(coordinator)
        self.coordinator = coordinator
        self.authenticator = authenticator
        self.heartbeat_timeout = timedelta(seconds=heartbeat_timeout_seconds)
        self.session_ttl = timedelta(seconds=session_ttl_seconds)
        self._clock = clock
        self.telemetry = telemetry or ObservationLayer()
        self._sessions: dict[str, RemoteSession] = {}
        self._lock = RLock()

    @staticmethod
    def _assert_coordinator_contract(coordinator) -> None:
        execute = getattr(coordinator, "execute", None)
        if execute is None or not callable(execute):
            raise TypeError("coordinator must expose execute(query, context)")
        parameters = inspect.signature(execute).parameters
        if len(parameters) < 1:
            raise TypeError("invalid AgentCoreCoordinator.execute contract")

    def _record(self, event: str, payload: dict) -> None:
        self.telemetry.record(source="RemoteButler", event=event, payload=payload)

    def _transition(self, session: RemoteSession, target: SessionState) -> None:
        if target not in self._TRANSITIONS[session.state]:
            raise SessionError(f"INVALID_SESSION_TRANSITION:{session.state}->{target}")
        session.state = target

    def open_session(
        self,
        token: str,
        device_id: str,
        fingerprint: str,
        *,
        context: dict | None = None,
    ) -> RemoteSession:
        auth: AuthenticationResult
        try:
            auth = self.authenticator.authenticate(token, device_id, fingerprint)
            self._record("REMOTE_AUTHENTICATION", {"ok": True, "device_id": device_id})
        except Exception as exc:
            self._record(
                "REMOTE_AUTHENTICATION",
                {"ok": False, "device_id": device_id, "error": str(exc)},
            )
            raise
        now = self._clock()
        session = RemoteSession(
            session_id=str(uuid4()),
            device=auth.device,
            token_id=auth.token_id,
            created_at=now,
            expires_at=now + self.session_ttl,
            last_heartbeat_at=now,
            context=dict(context or {}),
            cancellation_token=CancellationToken(),
        )
        self._transition(session, SessionState.AUTHENTICATED)
        self._transition(session, SessionState.ACTIVE)
        with self._lock:
            self._sessions[session.session_id] = session
        self._record("REMOTE_SESSION_START", self._summary(session))
        return session

    @staticmethod
    def _summary(session: RemoteSession) -> dict:
        return {
            "session_id": session.session_id,
            "device_id": session.device.device_id,
            "state": session.state.value,
        }

    def _active(self, session_id: str) -> RemoteSession:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                raise SessionError("SESSION_NOT_FOUND")
            now = self._clock()
            timed_out = now - session.last_heartbeat_at > self.heartbeat_timeout
            if session.state is SessionState.ACTIVE and (
                timed_out or now >= session.expires_at
            ):
                self._transition(session, SessionState.EXPIRED)
                session.cancellation_token.cancel("remote session expired")
                self._record("REMOTE_SESSION_EXPIRED", self._summary(session))
            if session.state is not SessionState.ACTIVE:
                raise SessionError(f"SESSION_NOT_ACTIVE:{session.state.value}")
            return session

    def heartbeat(self, session_id: str) -> dict:
        session = self._active(session_id)
        session.last_heartbeat_at = self._clock()
        return self._summary(session)

    def execute(self, session_id: str, query: str, context: dict | None = None):
        if not isinstance(query, str) or not query.strip():
            raise SessionError("QUERY_REQUIRED")
        session = self._active(session_id)
        request_context = dict(session.context)
        request_context.update(dict(context or {}))
        request_context["remote_session"] = {
            "session_id": session.session_id,
            "device_id": session.device.device_id,
            "cancellation_token": session.cancellation_token,
        }
        self._record(
            "REMOTE_REQUEST",
            {"session_id": session_id, "query_length": len(query)},
        )
        return self.coordinator.execute(query, request_context)

    def emergency_stop(self, session_id: str, reason: str = "remote emergency stop") -> dict:
        session = self._active(session_id)
        session.cancellation_token.cancel(reason)
        self._record("REMOTE_EMERGENCY_STOP", self._summary(session))
        return self.close_session(session_id, reason=reason)

    def close_session(self, session_id: str, *, reason: str = "closed") -> dict:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                raise SessionError("SESSION_NOT_FOUND")
            if session.state is not SessionState.CLOSED:
                if session.state is SessionState.EXPIRED:
                    self._transition(session, SessionState.CLOSED)
                elif session.state in {
                    SessionState.CREATED,
                    SessionState.AUTHENTICATED,
                    SessionState.ACTIVE,
                }:
                    self._transition(session, SessionState.CLOSED)
                session.cancellation_token.cancel(reason)
            summary = self._summary(session)
        self._record("REMOTE_SESSION_CLOSE", {**summary, "reason": reason})
        return summary

    def expire_stale_sessions(self) -> list[str]:
        expired = []
        with self._lock:
            identifiers = list(self._sessions)
        for session_id in identifiers:
            try:
                self._active(session_id)
            except SessionError as exc:
                if "SESSION_NOT_ACTIVE:EXPIRED" in str(exc):
                    expired.append(session_id)
                    self.close_session(session_id, reason="heartbeat timeout")
        return expired

    def get_session(self, session_id: str) -> RemoteSession:
        with self._lock:
            try:
                return self._sessions[session_id]
            except KeyError as exc:
                raise SessionError("SESSION_NOT_FOUND") from exc

