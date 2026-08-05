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


def test_profile_manager_is_sole_owner_of_user_profile():
    """Подтверждение: единственный владелец user_profile.json — profile_manager.py.
    
    profile_sync.py является дубликатом и помечен как DEPRECATED/LEGACY.
    Ни один продакшен-модуль не импортирует profile_sync напрямую.
    """
    # 1. profile_sync.py помечен как DEPRECATED
    sync_source = (ROOT / "A_07_MEMORY/profile_sync.py").read_text(encoding="utf-8")
    assert "DEPRECATED" in sync_source, "profile_sync.py должен быть помечен как DEPRECATED"
    assert "LEGACY" in sync_source, "profile_sync.py должен иметь статус LEGACY"

    # 2. profile_manager.py — активный модуль (без deprecated-меток)
    mgr_source = (ROOT / "A_07_MEMORY/profile_manager.py").read_text(encoding="utf-8")
    assert "DEPRECATED" not in mgr_source, "profile_manager.py не должен быть помечен как DEPRECATED"

    # 3. profile_sync.py НЕ импортируется никем в продакшене (чистый Python)
    prod_dirs = ["A_01_CORE", "A_03_ORCHESTRATION", "A_04_AGENTS", "A_07_MEMORY"]
    for d in prod_dirs:
        dir_path = ROOT / d
        if not dir_path.exists():
            continue
        for py_file in dir_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            content = py_file.read_text(encoding="utf-8", errors="replace")
            assert "from A_07_MEMORY.profile_sync import" not in content, \
                f"profile_sync.py импортируется в {py_file.relative_to(ROOT)}"

    # 4. profile_manager.py активно импортируется
    memory_dept = (ROOT / "A_04_AGENTS/MemoryDepartment/runner.py").read_text(encoding="utf-8")
    assert "profile_manager" in memory_dept, "MemoryDepartment должен импортировать profile_manager"

    # 5. MEMORY_CONTRACT.json подтверждает единственного владельца
    contract = json.loads((ROOT / "A_00_ARCHITECTURE/MEMORY_CONTRACT.json").read_text(encoding="utf-8"))
    permanent_user = [t for t in contract["types"] if t["type"] == "PERMANENT_USER"]
    assert len(permanent_user) == 1
    assert "ProfileManager" in permanent_user[0]["writer"]
