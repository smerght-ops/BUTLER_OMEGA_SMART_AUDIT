import ast
import json
from pathlib import Path

from A_04_AGENTS.MemoryDepartment.runner import MemoryDepartment
from A_07_MEMORY.memory_orchestrator_v2 import MemoryOrchestratorV2


ROOT = Path(__file__).resolve().parents[1]


def test_memory_type_has_single_writer():
    contract = json.loads((ROOT / "A_00_ARCHITECTURE/MEMORY_CONTRACT.json").read_text(encoding="utf-8"))
    assert all(row["writer"] for row in contract["types"])
    assert contract["production_orchestrator"].endswith("MemoryOrchestratorV2")


def test_memory_department_uses_orchestrator():
    department = MemoryDepartment()
    assert isinstance(department.memory, MemoryOrchestratorV2)
    source = (ROOT / "A_04_AGENTS/MemoryDepartment/runner.py").read_text(encoding="utf-8")
    assert "MemoryFacadeV2" not in source


def test_dki_does_not_import_chat_router():
    source = (ROOT / "A_07_MEMORY/dki_compiler.py").read_text(encoding="utf-8")
    assert "A_03_ORCHESTRATION.chat_router" not in source
    assert "get_chat_provider" in source


def test_production_memory_orchestrator_is_shared():
    from A_07_MEMORY.memory_orchestrator_v2 import get_memory_orchestrator

    assert get_memory_orchestrator() is get_memory_orchestrator()


def test_production_chat_provider_is_shared():
    from A_02_MANAGERS.smart_dispatcher import get_chat_provider

    assert get_chat_provider() is get_chat_provider()


def test_architectural_graph_uses_rkd_and_does_not_scan():
    source = (ROOT / "A_07_MEMORY/architectural_knowledge_graph.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert "repository_knowledge_gateway" in source
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "rglob" for node in ast.walk(tree))


def test_memory_contract_matches_runtime():
    runtime = json.loads((ROOT / "A_00_ARCHITECTURE/RUNTIME_CONTRACT.json").read_text(encoding="utf-8"))
    memory = json.loads((ROOT / "A_00_ARCHITECTURE/MEMORY_CONTRACT.json").read_text(encoding="utf-8"))
    assert runtime["runtime_status"] == "ACTIVE_PRODUCTION"
    assert memory["department_interface"].endswith("MemoryDepartment")
