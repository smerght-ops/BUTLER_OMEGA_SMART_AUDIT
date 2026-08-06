# -*- coding: utf-8 -*-
"""Fail-closed Continuous Acceptance gate for Butler Omega Smart.

The gate coordinates existing verification mechanisms.  It does not alter the
runtime request path, Dispatcher, Departments, or the Result Contract.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Sequence


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "A_99_TESTS" / "reports"
PHASE_TEST_PATTERN = "test_*phase*.py"


@dataclass(frozen=True)
class StageResult:
    name: str
    status: str
    command: list[str]
    exit_code: int
    output: str


CommandRunner = Callable[[Sequence[str], Path], tuple[int, str]]


def run_command(command: Sequence[str], cwd: Path) -> tuple[int, str]:
    completed = subprocess.run(
        list(command), cwd=str(cwd), text=True, encoding="utf-8",
        errors="replace", stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def changed_python_files(runner: CommandRunner = run_command) -> list[Path]:
    """Return changed and untracked Python files, constrained to the project."""
    commands = (
        ("git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD", "--", "*.py"),
        ("git", "ls-files", "--others", "--exclude-standard", "--", "*.py"),
    )
    names: set[str] = set()
    for command in commands:
        code, output = runner(command, ROOT)
        if code != 0:
            raise RuntimeError(f"CHANGE_DISCOVERY_FAILED: {' '.join(command)}\n{output}")
        names.update(line.strip() for line in output.splitlines() if line.strip())
    files = []
    root = ROOT.resolve()
    for name in sorted(names):
        path = (ROOT / name).resolve()
        if path.is_relative_to(root) and path.is_file():
            files.append(path)
    return files


def _stage(name: str, command: Sequence[str], runner: CommandRunner) -> StageResult:
    try:
        code, output = runner(command, ROOT)
    except Exception as exc:
        return StageResult(name, "ERROR", list(command), 2,
                           f"{type(exc).__name__}: {exc}")
    return StageResult(name, "PASS" if code == 0 else "FAIL", list(command),
                       int(code), output)


def execute_gate(
    acceptance_mode: str = "fast",
    runner: CommandRunner = run_command,
    python_executable: str = sys.executable,
) -> list[StageResult]:
    """Run every mandatory stage in order and stop on the first failure."""
    try:
        changed = changed_python_files(runner)
    except Exception as exc:
        return [StageResult("py_compile", "ERROR", [], 2,
                            f"{type(exc).__name__}: {exc}")]

    compile_command = [python_executable, "-m", "py_compile"]
    compile_command.extend(str(path.relative_to(ROOT)) for path in changed)
    if changed:
        result = _stage("py_compile", compile_command, runner)
    else:
        result = StageResult("py_compile", "PASS", compile_command, 0,
                             "No changed Python files.")
    results = [result]
    if result.status != "PASS":
        return results

    phase_tests = [str(path.relative_to(ROOT)) for path in sorted(
        (ROOT / "A_09_TESTS").glob(PHASE_TEST_PATTERN)
    )]
    commands = (
        ("unit_tests", [python_executable, "-m", "pytest", "-q"]),
        ("phase_regression", [python_executable, "-m", "pytest", "-q",
                              *phase_tests]),
        ("user_acceptance", [python_executable,
                             "A_99_TESTS/full_acceptance.py",
                             "--mode", acceptance_mode]),
    )
    for name, command in commands:
        result = _stage(name, command, runner)
        results.append(result)
        if result.status != "PASS":
            break
    return results


def write_report(results: Sequence[StageResult], acceptance_mode: str,
                 reports: Path = REPORTS) -> tuple[Path, Path]:
    reports.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    accepted = len(results) == 4 and all(item.status == "PASS" for item in results)
    payload = {
        "schema_version": "1.0",
        "phase": 9,
        "acceptance_mode": acceptance_mode,
        "timestamp": stamp,
        "accepted": accepted,
        "exit_code": 0 if accepted else 1,
        "stages": [asdict(item) for item in results],
    }
    json_path = reports / f"continuous_acceptance_{stamp}.json"
    md_path = reports / f"continuous_acceptance_{stamp}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    lines = [
        "# Butler Omega Smart — Continuous Acceptance",
        "",
        f"Result: **{'PASS' if accepted else 'FAIL'}**",
        f"Acceptance mode: `{acceptance_mode}`",
        "",
        "| Stage | Status | Exit code |",
        "|---|---:|---:|",
    ]
    lines.extend(f"| {item.name} | {item.status} | {item.exit_code} |"
                 for item in results)
    for item in results:
        if item.status != "PASS":
            lines.extend(("", f"## {item.name}", "", "```text",
                          item.output[-8000:], "```"))
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (reports / "latest_continuous_acceptance.json").write_text(
        json_path.read_text(encoding="utf-8"), encoding="utf-8")
    (reports / "latest_continuous_acceptance.md").write_text(
        md_path.read_text(encoding="utf-8"), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Butler Phase 9 acceptance gate")
    parser.add_argument("--acceptance-mode", choices=("fast", "full"),
                        default="fast")
    args = parser.parse_args()
    results = execute_gate(args.acceptance_mode)
    json_path, _ = write_report(results, args.acceptance_mode)
    accepted = len(results) == 4 and all(item.status == "PASS" for item in results)
    for item in results:
        print(f"[{item.status:5}] {item.name}")
    print(f"REPORT: {json_path}")
    print("CHANGE ACCEPTED" if accepted else "CHANGE BLOCKED")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
