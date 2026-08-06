"""Production project audit skill governed by the existing SkillRuntime."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Callable, Sequence

from A_01_CORE.skill_runtime import SkillManager


PROJECT_AUDIT_SIGNATURE = (
    "repository.inspect",
    "acceptance.fast",
    "evidence.collect",
)


CommandRunner = Callable[[Sequence[str], Path], tuple[int, str]]


def run_command(command: Sequence[str], cwd: Path) -> tuple[int, str]:
    completed = subprocess.run(
        list(command), cwd=str(cwd), text=True, encoding="utf-8",
        errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


class ProjectAuditSkill:
    """Inspect repository state and execute the existing acceptance boundary."""

    name = "project_audit_skill"
    signature = PROJECT_AUDIT_SIGNATURE

    def __init__(
        self,
        manager: SkillManager,
        root: Path | None = None,
        runner: CommandRunner = run_command,
        python_executable: str = sys.executable,
    ):
        self.manager = manager
        self.root = (root or Path(__file__).resolve().parents[1]).resolve()
        self.runner = runner
        self.python_executable = python_executable
        self.report_path = self.root / "A_99_TESTS" / "reports" / "latest_acceptance_report.json"

    def propose(self, trace, provenance: str) -> dict:
        return self.manager.propose(
            "skill save project_audit_skill",
            self.signature,
            trace,
            provenance,
        )

    def approve(self, skill_id: str, approver: str) -> dict:
        return self.manager.approve(skill_id, approver)

    def execute(self) -> dict:
        active = self.manager.match_active(self.signature)
        if active is None:
            return self._result(
                False, "SKILL_NOT_ACTIVE", lifecycle_status="INACTIVE",
                evidence=[], repository={}, acceptance={},
            )

        evidence = []
        repository = {}
        acceptance = {}

        code, output = self.runner(("git", "rev-parse", "HEAD"), self.root)
        evidence.append(self._evidence("repository.head", code == 0, output, code))
        if code != 0:
            return self._result(False, "REPOSITORY_INSPECTION_FAILED", active["status"],
                                evidence, repository, acceptance)
        repository["head"] = output.strip()

        code, output = self.runner(("git", "status", "--short"), self.root)
        evidence.append(self._evidence("repository.status", code == 0, output, code))
        if code != 0:
            return self._result(False, "REPOSITORY_INSPECTION_FAILED", active["status"],
                                evidence, repository, acceptance)
        changes = [line for line in output.splitlines() if line.strip()]
        repository.update({"clean": not changes, "changes": changes})

        command = (
            self.python_executable,
            "A_99_TESTS/full_acceptance.py",
            "--mode", "fast",
        )
        code, output = self.runner(command, self.root)
        evidence.append(self._evidence("acceptance.fast", code == 0, output, code))
        try:
            payload = json.loads(self.report_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            evidence.append(self._evidence(
                "acceptance.report", False, f"{type(exc).__name__}: {exc}", 2,
            ))
            return self._result(False, "ACCEPTANCE_EVIDENCE_INVALID", active["status"],
                                evidence, repository, acceptance)

        acceptance = {
            "mode": payload.get("mode"),
            "counts": payload.get("counts"),
            "cleanup_ok": payload.get("cleanup_ok"),
            "all_scenarios_passed": payload.get("all_scenarios_passed"),
            "exit_code": payload.get("exit_code"),
            "report": str(self.report_path.relative_to(self.root)),
        }
        report_valid = (
            code == 0
            and acceptance["mode"] == "fast"
            and acceptance["cleanup_ok"] is True
            and acceptance["all_scenarios_passed"] is True
            and acceptance["exit_code"] == 0
            and isinstance(acceptance["counts"], dict)
            and acceptance["counts"].get("FAIL") == 0
        )
        evidence.append(self._evidence(
            "acceptance.report", report_valid,
            json.dumps(acceptance, ensure_ascii=False, sort_keys=True),
            0 if report_valid else 1,
        ))
        return self._result(
            report_valid,
            None if report_valid else "ACCEPTANCE_FAILED",
            active["status"], evidence, repository, acceptance,
        )

    def _result(self, ok, error, lifecycle_status, evidence, repository, acceptance):
        return {
            "ok": bool(ok),
            "skill": self.name,
            "signature": list(self.signature),
            "lifecycle_status": lifecycle_status,
            "repository": repository,
            "acceptance": acceptance,
            "evidence": evidence,
            "error": error,
        }

    @staticmethod
    def _evidence(source: str, verified: bool, output: str, exit_code: int) -> dict:
        return {
            "source": source,
            "verified": bool(verified),
            "exit_code": int(exit_code),
            "output": str(output or "")[-8000:],
        }
