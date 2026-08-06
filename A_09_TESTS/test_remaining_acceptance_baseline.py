from A_02_MANAGERS.ArchitectAgent.architect_agent import ArchitectAgent
from A_02_MANAGERS.ArchitectAgent.context_provider import ContextProvider
from A_04_AGENTS.MemoryDepartment.runner import MemoryDepartment
from A_07_MEMORY.profile_manager import get_memory_summary
from A_07_MEMORY.semantic_reasoning_engine import SemanticReasoningEngine


def test_canonical_registry_populates_architect_runtime_inventory():
    runtime = ContextProvider()._runtime_inventory()
    names = [item["class"] for item in runtime["departments"]]

    assert "FilesystemDepartment" in names
    assert "MemoryDepartment" in names


def test_department_listing_preserves_acceptance_contract():
    context = ContextProvider().build_context("Какие Department существуют?")
    answer = ArchitectAgent._factual_answer("Какие Department существуют?", context)

    assert "Полный состав Department" in answer
    assert "FilesystemDepartment" in answer


def test_artifact_backed_self_knowledge_is_not_claimed_by_architect_intent():
    engine = SemanticReasoningEngine()
    cases = (
        "Что уже сделано?",
        "Что осталось?",
        "Что находится внутри MemoryDepartment?",
        "Что ты знаешь о своём проекте?",
    )

    for query in cases:
        intent = engine.detect_intent(
            query, inherited_intent="PROJECT_SELF_KNOWLEDGE"
        )
        assert intent["name"] is None
        assert MemoryDepartment().can_handle(query)


def test_exact_favorite_color_precedes_fuzzy_knowledge_search():
    department = MemoryDepartment()
    answer = department._answer_memory_query(
        "Какой мой любимый цвет?", get_memory_summary()
    )

    assert answer == "Ваш любимый цвет — зелёный."


def test_department_contents_uses_live_ast_when_inspector_maps_are_absent():
    department = MemoryDepartment()
    answer = department._department_answer(
        "Что находится внутри MemoryDepartment?", {"inspectors": {}}
    )

    assert "Назначение Department" in answer
    assert "Возможности по Inspector" in answer
    assert "Ограничения" in answer
