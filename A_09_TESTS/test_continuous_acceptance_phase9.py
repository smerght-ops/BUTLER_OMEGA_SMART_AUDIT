import json

from A_99_TESTS.continuous_acceptance import execute_gate, write_report


class FakeRunner:
    def __init__(self, failures=None, changed=""):
        self.failures = failures or {}
        self.changed = changed
        self.commands = []

    def __call__(self, command, cwd):
        command = list(command)
        self.commands.append(command)
        joined = " ".join(command)
        if "git diff" in joined:
            return 0, self.changed
        if "git ls-files" in joined:
            return 0, ""
        for marker, code in self.failures.items():
            if marker in joined:
                return code, f"injected failure: {marker}"
        return 0, "PASS"


def test_all_required_stages_pass_in_order():
    runner = FakeRunner()
    results = execute_gate("fast", runner=runner, python_executable="python")

    assert [item.name for item in results] == [
        "py_compile", "unit_tests", "phase_regression", "user_acceptance",
    ]
    assert all(item.status == "PASS" for item in results)
    assert runner.commands[-1][-2:] == ["--mode", "fast"]


def test_failure_blocks_change_and_prevents_later_stages():
    runner = FakeRunner(failures={"test_runtime_foundation_phase1.py": 7})
    results = execute_gate("full", runner=runner, python_executable="python")

    assert [item.name for item in results] == [
        "py_compile", "unit_tests", "phase_regression",
    ]
    assert results[-1].status == "FAIL"
    assert not any("full_acceptance.py" in " ".join(c) for c in runner.commands)


def test_changed_python_files_are_compiled():
    runner = FakeRunner(changed="A_99_TESTS/continuous_acceptance.py\n")
    results = execute_gate("fast", runner=runner, python_executable="python")

    compile_command = next(c for c in runner.commands if "py_compile" in c)
    assert "A_99_TESTS\\continuous_acceptance.py" in compile_command or (
        "A_99_TESTS/continuous_acceptance.py" in compile_command
    )
    assert results[0].status == "PASS"


def test_report_is_fail_closed_when_a_required_stage_is_missing(tmp_path):
    runner = FakeRunner(failures={"pytest -q": 1})
    results = execute_gate("fast", runner=runner, python_executable="python")
    json_path, md_path = write_report(results, "fast", reports=tmp_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["accepted"] is False
    assert payload["exit_code"] == 1
    assert "FAIL" in md_path.read_text(encoding="utf-8")
