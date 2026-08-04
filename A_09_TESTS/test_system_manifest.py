from pathlib import Path

from A_04_AGENTS.RepositoryKnowledgeDepartment.loaders import ManifestLoader
from A_04_AGENTS.RepositoryKnowledgeDepartment.service import RepositoryKnowledgeService


ROOT = Path(__file__).resolve().parents[1]


def test_manifest_has_no_bom_loader_ok_and_paths_exist():
    assert not (ROOT / "system_manifest.json").read_bytes().startswith(b"\xef\xbb\xbf")
    manifest, diagnostic = ManifestLoader().load(ROOT)
    assert diagnostic.status == "OK"
    assert manifest["active_paths"]
    assert all((ROOT / path).is_dir() for path in manifest["active_paths"])


def test_manifest_is_in_repository_index():
    index = RepositoryKnowledgeService(ROOT).index()
    manifest = ManifestLoader().load(ROOT)[0]
    assert index.source_versions["system_manifest"] == manifest["version"]
    assert any(node.get("file") == "system_manifest.json" for node in index.nodes)
