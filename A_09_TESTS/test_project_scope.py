from pathlib import Path

from A_04_AGENTS.RepositoryKnowledgeDepartment.loaders import ScopeResolver


ROOT = Path(__file__).resolve().parents[1]


def test_scope_yaml_full_parse_and_required_sections():
    scope, diagnostic = ScopeResolver().load(ROOT)
    assert diagnostic.status == "OK", diagnostic
    assert scope["categories"]["production"]
    assert scope["categories"]["engineering"]
    assert "A_00_ARCHITECTURE" in scope["categories"]["engineering"]
    assert "A_00_ARCHITECTURE" not in scope["categories"]["archive"]


def test_duplicate_scope_path_rejected(tmp_path):
    (tmp_path / "PROJECT_SCOPE.yaml").write_text(
        "metadata: {}\nproduction: [x]\nengineering: [x]\nworkspace: []\nlaboratory: []\narchive: []\n"
        "generated: []\nignore: []\nreview_required: []\nclassification_rules: []\naudit_policy: {}\nfuture_consumers: []\n",
        encoding="utf-8")
    _, diagnostic = ScopeResolver().load(tmp_path)
    assert diagnostic.reason == "DUPLICATE_PATH_CLASSIFICATION"
