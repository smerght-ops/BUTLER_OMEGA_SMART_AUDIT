import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from A_04_AGENTS.RepositoryKnowledgeDepartment.lifecycle import clear_instances, get_department
from A_04_AGENTS.RepositoryKnowledgeDepartment.scanner import RepositoryScanner


def make_root(tmp_path, name="project"):
    root = tmp_path / name
    root.mkdir()
    (root / "src").mkdir()
    (root / "src/app.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "PROJECT_SCOPE.yaml").write_text(
        "metadata: {scope_version: '1'}\nproduction: [{name: src}]\nengineering: []\nworkspace: []\n"
        "laboratory: []\narchive: []\ngenerated: []\nignore: []\nreview_required: []\n"
        "classification_rules: []\naudit_policy: {}\nfuture_consumers: []\n", encoding="utf-8")
    (root / "system_manifest.json").write_text(json.dumps({"version": "1", "active_paths": ["src"]}), encoding="utf-8")
    return root


def setup_function():
    clear_instances()


def test_gateway_reuses_department_and_service_instance(tmp_path):
    root = make_root(tmp_path)
    first, second = get_department(root), get_department(root / ".")
    assert first is second
    assert first._service is second._service


def test_second_query_does_not_rescan_and_refresh_rescans_once(tmp_path):
    service = get_department(make_root(tmp_path))._service
    service.query("list_files")
    assert service.scan_count == 1
    service.query("list_files")
    assert service.scan_count == 1
    service.refresh_index()
    assert service.scan_count == 2


def test_failed_refresh_keeps_previous_index(tmp_path, monkeypatch):
    service = get_department(make_root(tmp_path))._service
    old = service.index()
    monkeypatch.setattr(RepositoryScanner, "scan", lambda self: (_ for _ in ()).throw(OSError("boom")))
    result = service.refresh_index()
    assert result["degraded"] is True
    assert service.cache.get() is old


def test_parallel_cold_queries_build_once(tmp_path):
    service = get_department(make_root(tmp_path))._service
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: service.query("list_files"), range(8)))
    assert service.scan_count == 1
    assert service.build_count == 1


def test_different_roots_have_different_instances(tmp_path):
    assert get_department(make_root(tmp_path, "one")) is not get_department(make_root(tmp_path, "two"))
