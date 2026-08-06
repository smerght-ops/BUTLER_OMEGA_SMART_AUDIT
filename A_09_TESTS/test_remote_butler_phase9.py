from datetime import datetime, timedelta, timezone

import pytest

from A_03_ORCHESTRATION.authentication import RemoteAuthenticator
from A_03_ORCHESTRATION.remote_models import (
    AuthenticationError,
    DeviceBindingError,
    SessionError,
    SessionState,
)
from A_03_ORCHESTRATION.remote_session_gateway import RemoteSessionGateway
from A_03_ORCHESTRATION.remote_transport import (
    RemoteMessageRouter,
    WebSocketRemoteTransport,
)
from A_03_ORCHESTRATION.token_manager import TokenManager


class Clock:
    def __init__(self):
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += timedelta(seconds=seconds)


class Telemetry:
    def __init__(self):
        self.events = []

    def record(self, source, event, payload=None):
        self.events.append((source, event, payload or {}))


class Coordinator:
    def __init__(self):
        self.calls = []

    def execute(self, query, context=None):
        self.calls.append((query, context))
        return {"ok": True, "text": query}


@pytest.fixture
def system():
    clock = Clock()
    tokens = TokenManager(clock=clock)
    telemetry = Telemetry()
    coordinator = Coordinator()
    gateway = RemoteSessionGateway(
        coordinator,
        RemoteAuthenticator(tokens),
        clock=clock,
        heartbeat_timeout_seconds=10,
        session_ttl_seconds=60,
        telemetry=telemetry,
    )
    return clock, tokens, telemetry, coordinator, gateway


def test_token_authentication_device_binding_expiry_and_revocation(system):
    clock, tokens, _, _, _ = system
    token = tokens.create_token("phone", "fp-1", ttl_seconds=5, metadata={"role": "owner"})
    record = tokens.verify(token, "phone", "fp-1")
    assert tokens.metadata(record.token_id)["metadata"] == {"role": "owner"}
    with pytest.raises(DeviceBindingError, match="DEVICE_BINDING_MISMATCH"):
        tokens.verify(token, "other", "fp-1")
    clock.advance(6)
    with pytest.raises(AuthenticationError, match="TOKEN_EXPIRED"):
        tokens.verify(token, "phone", "fp-1")
    active = tokens.create_token("phone", "fp-1")
    assert tokens.revoke(active)
    with pytest.raises(AuthenticationError, match="TOKEN_REVOKED"):
        tokens.verify(active, "phone", "fp-1")


def test_authentication_happens_before_session_creation(system):
    _, _, telemetry, _, gateway = system
    with pytest.raises(AuthenticationError):
        gateway.open_session("bad", "phone", "fp")
    assert gateway._sessions == {}
    assert telemetry.events[-1][1] == "REMOTE_AUTHENTICATION"


def test_remote_request_uses_only_agent_core_coordinator(system):
    _, tokens, telemetry, coordinator, gateway = system
    token = tokens.create_token("phone", "fp")
    session = gateway.open_session(token, "phone", "fp", context={"locale": "ru"})
    result = gateway.execute(session.session_id, "hello", {"turn": 1})
    assert result == {"ok": True, "text": "hello"}
    assert len(coordinator.calls) == 1
    query, context = coordinator.calls[0]
    assert query == "hello"
    assert context["locale"] == "ru" and context["turn"] == 1
    assert context["remote_session"]["session_id"] == session.session_id
    assert "dispatcher" not in vars(gateway)
    assert "permission_engine" not in vars(gateway)
    assert "department" not in vars(gateway)
    assert any(event == "REMOTE_REQUEST" for _, event, _ in telemetry.events)


def test_heartbeat_timeout_closes_resources(system):
    clock, tokens, _, _, gateway = system
    session = gateway.open_session(tokens.create_token("phone", "fp"), "phone", "fp")
    gateway.heartbeat(session.session_id)
    clock.advance(11)
    assert gateway.expire_stale_sessions() == [session.session_id]
    assert session.state is SessionState.CLOSED
    assert session.cancellation_token.is_cancelled
    with pytest.raises(SessionError, match="SESSION_NOT_ACTIVE"):
        gateway.execute(session.session_id, "late")


def test_emergency_stop_uses_session_cancellation_token(system):
    _, tokens, telemetry, _, gateway = system
    session = gateway.open_session(tokens.create_token("phone", "fp"), "phone", "fp")
    result = gateway.emergency_stop(session.session_id, "operator stop")
    assert result["state"] == "CLOSED"
    assert session.cancellation_token.is_cancelled
    assert session.cancellation_token.reason == "operator stop"
    assert any(event == "REMOTE_EMERGENCY_STOP" for _, event, _ in telemetry.events)


def test_websocket_and_https_message_router_share_gateway(system):
    _, tokens, _, coordinator, gateway = system
    router = RemoteMessageRouter(gateway)
    opened = router.dispatch({
        "action": "open",
        "token": tokens.create_token("phone", "fp"),
        "device_id": "phone",
        "fingerprint": "fp",
    })
    session_id = opened["session"]["session_id"]
    websocket = WebSocketRemoteTransport(router)
    response = websocket.handle_text(
        '{"action":"request","session_id":"%s","query":"ws"}' % session_id
    )
    assert '"ok":true' in response
    assert coordinator.calls[-1][0] == "ws"
    https_style = router.dispatch({
        "action": "request", "session_id": session_id, "query": "https"
    })
    assert https_style["result"]["text"] == "https"

