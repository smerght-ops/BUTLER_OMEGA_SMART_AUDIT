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
    assert "test_repository_knowledge_lifecycle.py" in source


def test_full_encoding_checks_json_yaml_md_ps1(tmp_path, monkeypatch):
    files = []
    for name, content in (("a.json", "{}"), ("a.yaml", "x: 1"), ("a.md", "текст"), ("a.ps1", "Write-Host ok")):
        path = tmp_path / name
        path.write_text(content, encoding="utf-8")
        files.append(path)
    monkeypatch.setattr(checker, "_changed_files", lambda: files)
    assert checker.check_encoding("full")["status"] == "PASS"


def test_scope_manifest_and_lifecycle_sections_present():
    assert checker.check_scope()["status"] == "PASS"
    assert checker.check_manifest()["status"] == "PASS"
    assert "status" in checker.check_rkd_lifecycle()
