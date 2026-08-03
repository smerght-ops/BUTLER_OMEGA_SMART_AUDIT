from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from A_04_AGENTS.PublicationGuardianDepartment.Core.engine import PublicationGuardianEngine


DEPARTMENT_ROOT = Path(__file__).resolve().parents[1]


def engine(tmp_path: Path, inspector_types=None, policy_path=None):
    runtime = tmp_path / "runtime"
    return PublicationGuardianEngine(
        DEPARTMENT_ROOT, runtime_root=runtime, inspector_types=inspector_types,
        policy_path=policy_path,
    )


def request(root: Path, request_id="test", mode="files", paths=(), staged_files=(), policy_version="1.0"):
    return {
        "api_version": "v1", "request_id": request_id,
        "timestamp": datetime.now(timezone.utc).isoformat(), "initiator": "test",
        "publication_target": "test-target", "publication_mode": mode,
        "publication_scope": "test-scope", "repository_root": str(root),
        "git_reference": "HEAD", "staged_files": list(staged_files),
        "policy_version": policy_version, "metadata": {"paths": [str(path) for path in paths]},
    }


def copy_policy(tmp_path: Path) -> Path:
    target = tmp_path / "policy.json"
    shutil.copyfile(DEPARTMENT_ROOT / "Policies" / "default_v1.json", target)
    return target
