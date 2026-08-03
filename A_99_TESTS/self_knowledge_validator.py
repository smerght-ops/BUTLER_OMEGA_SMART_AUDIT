# -*- coding: utf-8 -*-
"""Validate proposals in an isolated diagnostic sandbox; never patches production."""

from __future__ import annotations

import json
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROPOSALS = ROOT / "A_99_TESTS" / "repair_proposals.json"
EXAM = ROOT / "A_99_TESTS" / "reports" / "latest_exam_report.json"
SANDBOX_ROOT = ROOT / "A_99_TESTS" / "reports" / "self_knowledge_validation"


def run(command: list[str], timeout: int) -> dict:
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return {"exit_code": completed.returncode, "stdout_tail": completed.stdout.splitlines()[-30:], "stderr_tail": completed.stderr.splitlines()[-15:]}


def acceptance(mode: str) -> dict:
    result = run([sys.executable, str(ROOT / "A_99_TESTS" / "full_acceptance.py"), "--mode", mode], 600)
    path = ROOT / "A_99_TESTS" / "reports" / "latest_acceptance_report.json"
    data = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}
    result.update({"counts": data.get("counts", {}), "all_scenarios_passed": data.get("all_scenarios_passed")})
    return result


def main() -> int:
    payload = json.loads(PROPOSALS.read_text(encoding="utf-8-sig"))
    baseline = json.loads(EXAM.read_text(encoding="utf-8-sig"))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sandbox = SANDBOX_ROOT / stamp
    candidate_dir = sandbox / "A_04_AGENTS" / "MemoryDepartment"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    source_runner = ROOT / "A_04_AGENTS" / "MemoryDepartment" / "runner.py"
    candidate_runner = candidate_dir / "runner.py"
    shutil.copy2(source_runner, candidate_runner)
    (sandbox / "proposal_overlay.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    py_compile.compile(str(candidate_runner), doraise=True)

    # Proposals are descriptive and require human confirmation; no executable patch is fabricated.
    # One shared safety run validates the unchanged baseline while each candidate is rejected if it cannot prove improvement.
    fast = acceptance("fast")
    full = acceptance("full") if fast["exit_code"] == 0 else {"exit_code": None, "counts": {}, "all_scenarios_passed": False}
    repeated = run([sys.executable, str(ROOT / "A_99_TESTS" / "self_knowledge_exam.py")], 300) if full["exit_code"] == 0 else {"exit_code": None}
    after = json.loads(EXAM.read_text(encoding="utf-8-sig")) if repeated.get("exit_code") == 0 else baseline
    baseline_conflicts = len(baseline.get("consistency_conflicts", []))
    after_conflicts = len(after.get("consistency_conflicts", []))
    score_ok = float(after.get("self_knowledge_score", 0)) >= float(baseline.get("self_knowledge_score", 0))
    conflicts_reduced = after_conflicts < baseline_conflicts
    acceptance_ok = fast["exit_code"] == 0 and full["exit_code"] == 0

    for proposal in payload.get("proposals", []):
        errors = []
        if proposal.get("requires_human_confirmation"):
            errors.append("Human confirmation is required before any production change")
        if proposal.get("root_cause") == "routing_before_memory":
            errors.append("Candidate target MemoryDepartment cannot correct a request intercepted before MemoryDepartment")
        if not acceptance_ok:
            errors.append("FAST or FULL Acceptance failed")
        if not score_ok:
            errors.append("Self Knowledge Score decreased")
        if not conflicts_reduced:
            errors.append("Conflict count did not decrease in the isolated proposal-only validation")
        proposal["validation_status"] = "REJECTED" if errors else "VALIDATED"
        proposal["validation_errors"] = errors
        proposal["validation_date"] = datetime.now().isoformat(timespec="seconds")
        proposal["sandbox_path"] = str(sandbox.relative_to(ROOT))
        proposal["applied_to_working_project"] = False
    payload["validation_summary"] = {
        "sandbox": str(sandbox.relative_to(ROOT)), "candidate_compiled": True,
        "fast": fast, "full": full, "repeated_exam_exit_code": repeated.get("exit_code"),
        "score_before": baseline.get("self_knowledge_score"), "score_after": after.get("self_knowledge_score"),
        "conflicts_before": baseline_conflicts, "conflicts_after": after_conflicts,
        "validated": sum(item["validation_status"] == "VALIDATED" for item in payload.get("proposals", [])),
        "rejected": sum(item["validation_status"] == "REJECTED" for item in payload.get("proposals", [])),
        "working_project_modified": False,
    }
    PROPOSALS.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"VALIDATED: {payload['validation_summary']['validated']}")
    print(f"REJECTED: {payload['validation_summary']['rejected']}")
    print(f"FAST_EXIT: {fast['exit_code']}")
    print(f"FULL_EXIT: {full['exit_code']}")
    print("WORKING_PROJECT_MODIFIED: NO")
    return 0 if acceptance_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
