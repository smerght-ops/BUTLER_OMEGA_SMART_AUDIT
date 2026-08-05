from A_01_CORE.skill_runtime import SkillManager
from A_07_MEMORY.semantic_memory import SemanticMemory


def manager(tmp_path):
    memory = SemanticMemory()
    memory.memory_dir = tmp_path
    memory.index_path = tmp_path / "MEMORY_INDEX.jsonl"
    memory.index_path.touch()
    return SkillManager(memory=memory)


TRACE = [{"capability_id": "cap.one", "department": "TEST", "ok": True}]


def test_candidate_requires_explicit_command(tmp_path):
    skills = manager(tmp_path)
    try:
        skills.propose("remember this", ["cap.one"], TRACE, "test")
    except PermissionError as exc:
        assert "EXPLICIT" in str(exc)
    else:
        raise AssertionError("implicit skill candidate accepted")


def test_candidate_requires_human_approval_before_routing(tmp_path):
    skills = manager(tmp_path)
    proposed = skills.propose("skill save demo", ["cap.one"], TRACE, "test")
    skill_id = proposed["candidate"]["skill_id"]
    assert proposed["requires_approval"] is True
    assert skills.match_active(["cap.one"]) is None
    assert skills.approve(skill_id, "")["error"] == "HUMAN_APPROVAL_REQUIRED"
    approved = skills.approve(skill_id, "architect")
    assert approved["ok"] is True
    assert skills.match_active(["cap.one"])["status"] == "ACTIVE"


def test_failed_trace_is_rejected_by_judge(tmp_path):
    skills = manager(tmp_path)
    try:
        skills.propose("skill save broken", ["cap.one"], [{"ok": False}], "test")
    except ValueError as exc:
        assert "JUDGE" in str(exc)
    else:
        raise AssertionError("failed trace accepted")


def test_versioning_and_rollback_are_append_only(tmp_path):
    skills = manager(tmp_path)
    first = skills.propose("skill save demo", ["cap.one"], TRACE, "v1")
    skill_id = first["candidate"]["skill_id"]
    skills.approve(skill_id, "architect")
    second = skills.propose("skill save demo updated", ["cap.one"], TRACE, "v2")
    assert second["candidate"]["version"] == 2
    skills.approve(skill_id, "architect")
    rolled = skills.rollback(skill_id, 1, "architect")
    assert rolled["ok"] is True
    assert rolled["skill"]["version"] == 1
    assert len(skills.index.events(skill_id)) == 5


def test_telemetry_does_not_promote_skill(tmp_path):
    skills = manager(tmp_path)
    event = skills.record_telemetry(["cap.one"], TRACE, "execution")
    assert event["successful"] is True
    assert skills.match_active(["cap.one"]) is None
