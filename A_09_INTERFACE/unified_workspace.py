"""Local read-only HTTP facade for the Unified Workspace client."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from A_01_CORE.runtime_query_api import RuntimeQueryAPI


STATIC = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
}


def handler_factory(api: RuntimeQueryAPI, static_root: Path):
    class UnifiedWorkspaceHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/api/dashboard":
                return self._json(api.dashboard())
            if self.path == "/api/tasks":
                return self._json(api.tasks())
            resource = STATIC.get(self.path)
            if resource is None:
                return self.send_error(404)
            name, content_type = resource
            try:
                payload = (static_root / name).read_bytes()
            except OSError:
                return self.send_error(404)
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_POST(self):
            self.send_error(405, "Unified Workspace is read-only")

        def _json(self, value):
            payload = json.dumps(value, ensure_ascii=False, default=str).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *_args):
            return

    return UnifiedWorkspaceHandler


def create_server(host="127.0.0.1", port=8765, root=None):
    project_root = Path(root) if root else Path(__file__).resolve().parents[1]
    static_root = Path(__file__).resolve().parent / "unified_workspace"
    return ThreadingHTTPServer((host, int(port)), handler_factory(RuntimeQueryAPI(project_root), static_root))


if __name__ == "__main__":
    server = create_server()
    print(f"Unified Workspace: http://{server.server_address[0]}:{server.server_address[1]}")
    server.serve_forever()
