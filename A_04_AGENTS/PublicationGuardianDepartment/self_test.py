from __future__ import annotations

import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .Core.engine import PublicationGuardianEngine


def _request(root: Path, request_id: str, path: Path) -> dict:
    return {
        "api_version": "v1",
        "request_id": request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "initiator": "publication-guardian-self-test",
        "publication_target": "local-self-test",
        "publication_mode": "files",
        "publication_scope": "single-file",
        "repository_root": str(root),
        "git_reference": "",
        "staged_files": [],
        "policy_version": "1.0",
        "metadata": {"paths": [str(path)]},
    }


def run_self_test() -> dict:
    department_root = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="publication_guardian_self_test_") as folder:
        root = Path(folder)
        engine = PublicationGuardianEngine(department_root, root / "runtime")
        safe = root / "safe.txt"
        safe.write_text("safe publication content\n", encoding="utf-8", newline="\n")
        blocked = root / ".env"
        blocked.write_text("EXAMPLE_ONLY=true\n", encoding="utf-8", newline="\n")
        safe_result = engine.inspect(_request(root, "self-test-pass", safe))
        blocked_result = engine.inspect(_request(root, "self-test-block", blocked))
        checks = {
            "safe_status": safe_result.status,
            "blocked_status": blocked_result.status,
            "report_created": bool(safe_result.report.get("path") and Path(safe_result.report["path"]).is_file()),
            "audit_created": (root / "runtime" / "audit.jsonl").is_file(),
            "log_created": (root / "runtime" / "guardian.jsonl").is_file(),
        }
        checks["ok"] = (
            checks["safe_status"] == "PASS"
            and checks["blocked_status"] == "BLOCK"
            and checks["report_created"]
            and checks["audit_created"]
            and checks["log_created"]
        )
        return checks


if __name__ == "__main__":
    result = run_self_test()
    print(result)
    raise SystemExit(0 if result["ok"] else 1)
