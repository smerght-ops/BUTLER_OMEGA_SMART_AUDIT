import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_active_system_matches_runtime_contract():
    active = (ROOT / "A_00_ARCHITECTURE/ACTIVE_SYSTEM.md").read_text(encoding="utf-8")
    runtime = load("A_00_ARCHITECTURE/RUNTIME_CONTRACT.json")
    assert runtime["official_launcher"] in active
    assert runtime["official_stop_launcher"] in active
    assert "A_00_LEGACY_ARCHIVE/production_cleanup_tz4" in active


def test_system_manifest_matches_production_architecture():
    manifest = load("system_manifest.json")
    architecture = load(manifest["production_architecture"])
    assert manifest["project"] == "BUTLER_OMEGA_SMART"
    assert architecture["status"] == "ACTIVE_PRODUCTION"
    assert architecture["canonical_department_registry"] == "A_02_MANAGERS/department_registry.py"
    assert architecture["tests"] == ["python -m pytest -c pytest.ini"]


def test_no_multiple_active_architecture_documents():
    architecture = load("A_00_ARCHITECTURE/PRODUCTION_ARCHITECTURE.json")
    runtime = load("A_00_ARCHITECTURE/RUNTIME_CONTRACT.json")
    assert architecture["status"] == runtime["runtime_status"]
    assert (ROOT / "A_10_BUTLER_OS/README.md").read_text(encoding="utf-8").find("ACTIVE_SUPPORT") >= 0


def test_tree_classification_contains_required_groups():
    classification = load("A_00_ARCHITECTURE/PRODUCTION_TREE_CLASSIFICATION.json")
    assert {"launcher", "router_bridge", "memory", "knowledge_review", "evidence"} <= set(classification["groups"])
    assert classification["moves"]
    assert sum(status == "ACTIVE_PRODUCTION" for status in classification["departments"].values()) == 18
    assert set(classification["departments"].values()) <= {"ACTIVE_PRODUCTION", "ACTIVE_PARTIAL", "DEVELOPMENT", "LEGACY", "UNUSED"}
