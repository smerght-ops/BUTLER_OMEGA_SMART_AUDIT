"""HTTPS and WebSocket delivery adapters without Butler business logic."""

from __future__ import annotations

import json
import ssl
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .remote_models import RemoteAccessError


class RemoteMessageRouter:
    """Decode transport messages and delegate all work to RemoteSessionGateway."""

    def __init__(self, gateway) -> None:
        self.gateway = gateway

    def dispatch(self, message: dict[str, Any], headers: dict | None = None) -> dict:
        action = message.get("action")
        try:
            if action == "open":
                token = message.get("token")
                if not token:
                    token = self.gateway.authenticator.token_from_headers(headers or {})
                session = self.gateway.open_session(
                    token,
                    str(message.get("device_id", "")),
                    str(message.get("fingerprint", "")),
                    context=message.get("context"),
                )
                return {"ok": True, "session": self.gateway._summary(session)}
            if action == "heartbeat":
                return {"ok": True, "session": self.gateway.heartbeat(message["session_id"])}
            if action == "request":
                result = self.gateway.execute(
                    message["session_id"], message.get("query", ""), message.get("context")
                )
                return {"ok": True, "result": result}
            if action == "emergency_stop":
                result = self.gateway.emergency_stop(
                    message["session_id"], message.get("reason", "remote emergency stop")
                )
                return {"ok": True, "session": result}
            if action == "close":
                result = self.gateway.close_session(message["session_id"])
                return {"ok": True, "session": result}
            return {"ok": False, "error": "UNKNOWN_REMOTE_ACTION"}
        except (RemoteAccessError, KeyError, TypeError, ValueError) as exc:
            return {"ok": False, "error": str(exc)}


class WebSocketRemoteTransport:
    """Message-level adapter for any RFC 6455 server implementation."""

    def __init__(self, router: RemoteMessageRouter) -> None:
        self.router = router

    def handle_text(self, text: str, headers: dict | None = None) -> str:
        try:
            message = json.loads(text)
            if not isinstance(message, dict):
                raise ValueError("message must be an object")
            response = self.router.dispatch(message, headers)
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            response = {"ok": False, "error": f"INVALID_JSON:{exc}"}
        return json.dumps(response, ensure_ascii=False, separators=(",", ":"))


class HTTPSRemoteTransport:
    """TLS-wrapped JSON HTTP server delegating to RemoteMessageRouter."""

    def __init__(self, router: RemoteMessageRouter) -> None:
        self.router = router

    def create_server(
        self,
        host: str,
        port: int,
        *,
        certificate: str,
        private_key: str,
    ) -> ThreadingHTTPServer:
        router = self.router

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802 - stdlib callback name
                if self.path != "/remote/v1/message":
                    self.send_error(404)
                    return
                try:
                    size = int(self.headers.get("Content-Length", "0"))
                    if size <= 0 or size > 1_048_576:
                        raise ValueError("invalid content length")
                    message = json.loads(self.rfile.read(size).decode("utf-8"))
                    if not isinstance(message, dict):
                        raise ValueError("message must be an object")
                    response = router.dispatch(message, dict(self.headers.items()))
                    status = 200 if response.get("ok") else 400
                except (ValueError, UnicodeError, json.JSONDecodeError) as exc:
                    response = {"ok": False, "error": f"INVALID_REQUEST:{exc}"}
                    status = 400
                body = json.dumps(response, ensure_ascii=False).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args) -> None:
                return

        server = ThreadingHTTPServer((host, port), Handler)
        tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        tls.minimum_version = ssl.TLSVersion.TLSv1_2
        tls.load_cert_chain(certificate, private_key)
        server.socket = tls.wrap_socket(server.socket, server_side=True)
        return server

