import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from A_01_CORE.runtime_query_api import RuntimeQueryAPI
from A_09_INTERFACE.unified_workspace import create_server


def test_runtime_query_dashboard_is_read_only_and_complete(tmp_path):
    (tmp_path / "A_07_MEMORY").mkdir()
    (tmp_path / "A_07_MEMORY" / "MEMORY_INDEX.jsonl").write_text(
        json.dumps({"type": "skill", "status": "ACTIVE"}) + "\n", encoding="utf-8",
    )
    (tmp_path / "A_06_WORKSPACE").mkdir()
    (tmp_path / "A_06_WORKSPACE" / "example.txt").write_text("x", encoding="utf-8")
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    dashboard = RuntimeQueryAPI(tmp_path).dashboard()
    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert before == after
    assert dashboard["skills"]["active"] == 1
    assert dashboard["files"][0]["name"] == "example.txt"
    assert {"conversation", "voice", "tasks", "council", "models", "memory", "skills", "files", "permissions", "logs", "results"} <= dashboard.keys()


def test_http_facade_exposes_get_and_rejects_post(tmp_path):
    static = tmp_path / "A_09_INTERFACE" / "unified_workspace"
    static.mkdir(parents=True)
    for name in ("index.html", "app.js", "styles.css"):
        (static / name).write_text(name, encoding="utf-8")
    server = create_server(port=0, root=tmp_path)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        with urlopen(base + "/api/dashboard", timeout=2) as response:
            assert json.load(response)["runtime"]["tasks"]["total"] == 0
        try:
            urlopen(Request(base + "/api/dashboard", data=b"{}", method="POST"), timeout=2)
        except HTTPError as exc:
            assert exc.code == 405
        else:
            raise AssertionError("write method accepted")
    finally:
        server.shutdown()
        server.server_close()
