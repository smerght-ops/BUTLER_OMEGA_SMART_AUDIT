import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "A_01_CORE/project_indexer.py"


def test_project_indexer_uses_only_rkd_and_does_not_scan():
    text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(text)
    calls = [node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)]
    assert "rglob" not in calls
    assert "walk" not in calls
    assert "scandir" not in calls
    assert "query_repository" in text
    assert "cp1251" not in text.casefold()
    assert "utf-8-sig" not in text.casefold()


def test_project_index_outputs_explicit_utf8_without_bom():
    text = SOURCE.read_text(encoding="utf-8")
    assert 'encoding="utf-8"' in text
