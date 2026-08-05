from pathlib import Path

from A_04_AGENTS.EngineeringReviewDepartment import checker


def test_review_changed_and_full_mode(monkeypatch):
    monkeypatch.setattr(checker, "_get_modified_python_files", lambda: [])
    monkeypatch.setattr(checker, "_production_python_files", lambda: [])
    assert checker.check_python("changed")["status"] == "PASS"
    assert checker.check_python("full")["status"] == "PASS"


def test_full_review_includes_root_launchers():
    files = {path.name for path in checker._scope_files({".py", ".ps1", ".json", ".yaml", ".txt"})}
    assert {"START_BUTLER_OS.ps1", "STOP_BUTLER_OS.ps1", "BUTLER_OS.py", "system_manifest.json"} <= files


def test_import_check_executes_loader_and_reports_failure(tmp_path, monkeypatch):
    good = tmp_path / "good.py"
    good.write_text("VALUE = 1\n", encoding="utf-8")
    bad = tmp_path / "bad.py"
    bad.write_text("raise RuntimeError('expected')\n", encoding="utf-8")
    monkeypatch.setattr(checker, "_production_python_files", lambda: [good])
    result = checker.check_imports("full")
    assert result["items"][0]["result"] == "IMPORT_PASS"
    monkeypatch.setattr(checker, "_production_python_files", lambda: [bad])
    result = checker.check_imports("full")
    assert result["items"][0]["result"] in {"IMPORT_FAIL", "IMPORT_UNSAFE"}


def test_import_docstring_is_not_unsafe():
    tree = checker.ast.parse('"""module docs"""\nVALUE = 1\ndef work():\n    return 1\n')
    assert checker._import_unsafe_reason(tree) is None


def test_import_side_effect_is_unsafe():
    tree = checker.ast.parse("import subprocess\nsubprocess.run(['tool'])\n")
    assert "top-level" in checker._import_unsafe_reason(tree)


def test_complete_pytest_profile_is_real_pytest_source():
    source = Path(checker.__file__).read_text(encoding="utf-8")
    assert '"-m", "pytest"' in source
    assert '"-c", "pytest.ini"' in source


def test_pytest_uses_workspace_temp_and_cache(tmp_path):
    config = (Path(checker.__file__).resolve().parents[2] / "pytest.ini").read_text(encoding="utf-8")
    root = Path(checker.__file__).resolve().parents[2]
    assert root / ".pytest_runtime_tmp" in tmp_path.parents
    assert "cache_dir = .pytest_runtime_cache" in config


def test_git_oserror_is_diagnostic(monkeypatch):
    def fail(*args, **kwargs):
        raise OSError(6, "invalid handle")

    monkeypatch.setattr(checker, "_run", fail)
    result = checker._git("ls-files")
    assert result.returncode == 126
    assert "git ls-files" in result.stderr
    assert "OSError" in result.stderr


def test_repository_baseline_checks_working_tree(monkeypatch):
    calls = []

    def fake_git(*args):
        calls.append(args)
        return checker.subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(checker, "_git", fake_git)
    assert checker.check_repository()["status"] == "PASS"
    empty_tree = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    baseline_call = next(call for call in calls if call[:3] == ("diff", "--check", empty_tree))
    assert "A_01_CORE" in baseline_call
    assert "START_BUTLER_OS.ps1" in baseline_call
    assert ":(exclude,glob).repository_hygiene_baseline/**" in baseline_call
    assert ":(exclude,glob).stabilization_backups/**" in baseline_call
    assert ("diff", "--check", empty_tree, "HEAD") not in calls


def test_baseline_whitespace_scope_comes_from_active_manifest():
    scope = checker._baseline_whitespace_pathspecs()
    assert "A_03_ORCHESTRATION" in scope
    assert "A_09_TESTS" not in scope
    assert all("evidence" not in item.lower() for item in scope if not item.startswith(":(exclude"))


def test_repository_review_allows_intentional_working_changes(monkeypatch):
    def fake_git(*args):
        stdout = " M reviewed_file.py\n" if args == ("status", "--porcelain") else ""
        return checker.subprocess.CompletedProcess(args, 0, stdout, "")

    monkeypatch.setattr(checker, "_git", fake_git)
    result = checker.check_repository()
    assert result["status"] == "PASS"
    assert "Uncommitted changes detected" in result["details"]


def test_subprocess_uses_explicit_safe_handles(monkeypatch):
    captured = {}

    def fake_run(command, **kwargs):
        captured.update(kwargs)
        return checker.subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(checker.subprocess, "run", fake_run)
    checker._run(["git", "ls-files"], Path.cwd())
    assert captured["stdin"] is checker.subprocess.DEVNULL
    assert captured["stdout"] is checker.subprocess.PIPE
    assert captured["stderr"] is checker.subprocess.PIPE
    assert captured["close_fds"] is True


def test_full_encoding_checks_json_yaml_md_ps1(tmp_path, monkeypatch):
    files = []
    for name, content in (("a.json", "{}"), ("a.yaml", "x: 1"), ("a.md", "текст"), ("a.ps1", "Write-Host ok")):
        path = tmp_path / name
        path.write_text(content, encoding="utf-8")
        files.append(path)
    monkeypatch.setattr(checker, "_scope_files", lambda suffixes: files)
    assert checker.check_encoding("full")["status"] == "PASS"


def test_changed_encoding_uses_only_changed_files(tmp_path, monkeypatch):
    changed = tmp_path / "changed.md"
    changed.write_text("clean", encoding="utf-8")
    corrupt = tmp_path / "production.md"
    corrupt.write_bytes(b"\xff")
    monkeypatch.setattr(checker, "_changed_files", lambda: [changed])
    monkeypatch.setattr(checker, "_scope_files", lambda suffixes: [changed, corrupt])
    assert checker.check_encoding("changed")["status"] == "PASS"
    assert checker.check_encoding("full")["status"] == "FAIL"


def test_scope_manifest_and_lifecycle_sections_present():
    assert checker.check_scope()["status"] == "PASS"
    assert checker.check_manifest()["status"] == "PASS"
    assert "status" in checker.check_rkd_lifecycle()
