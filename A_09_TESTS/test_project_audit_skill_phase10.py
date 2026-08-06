import json

from A_01_CORE.project_audit_skill import ProjectAuditSkill
from A_01_CORE.skill_runtime import SkillManager
from A_07_MEMORY.semantic_memory import SemanticMemory


TRACE = [
    {"capability_id": "repository.inspect", "ok": True},
    {"capability_id": "acceptance.fast", "ok": True},
    {"capability_id": "evidence.collect", "ok": True},
]


def manager(tmp_path):
    memory = SemanticMemory()
    memory.memory_dir = tmp_path / "memory"
    memory.memory_dir.mkdir()
    memory.index_path = memory.memory_dir / "MEMORY_INDEX.jsonl"
    memory.index_path.touch()
    return SkillManager(memory=memory)


class AuditRunner:
    def __init__(self, report_path, acceptance_code=0):
        self.report_path = report_path
        self.acceptance_code = acceptance_code
        self.commands = []

    def __call__(self, command, cwd):
        command = list(command)
        self.commands.append(command)
        if command[:3] == ["git", "rev-parse", "HEAD"]:
            return 0, "abc123\n"
        if command[:3] == ["git", "status", "--short"]:
            return 0, " M tracked.py\n?? new.py\n"
        passed = self.acceptance_code == 0
        self.report_path.parent.mkdir(parents=True, exist_ok=True)
        self.report_path.write_text(json.dumps({
            "mode": "fast",
            "counts": {"PASS": 36 if passed else 35, "FAIL": 0 if passed else 1},
            "cleanup_ok": True,
            "all_scenarios_passed": passed,
            "exit_code": self.acceptance_code,
        }), encoding="utf-8")
        return self.acceptance_code, "acceptance output"


def make_skill(tmp_path, acceptance_code=0):
    skills = manager(tmp_path)
    report = tmp_path / "A_99_TESTS" / "reports" / "latest_acceptance_report.json"
    runner = AuditRunner(report, acceptance_code)
    skill = ProjectAuditSkill(
        skills, root=tmp_path, runner=runner, python_executable="python",
    )
    return skill, skills, runner


def test_skill_cannot_execute_before_human_approved_active_state(tmp_path):
    skill, skills, runner = make_skill(tmp_path)
    proposed = skill.propose(TRACE, "phase10-regression")
    skill_id = proposed["candidate"]["skill_id"]

    assert proposed["candidate"]["status"] == "CANDIDATE"
    assert proposed["candidate"]["judge"]["verdict"] == "PASS"
    assert skill.execute()["error"] == "SKILL_NOT_ACTIVE"
    assert skill.approve(skill_id, "")["error"] == "HUMAN_APPROVAL_REQUIRED"
    assert runner.commands == []


def test_active_skill_inspects_repository_runs_boundary_and_collects_evidence(tmp_path):
    skill, skills, runner = make_skill(tmp_path)
    proposed = skill.propose(TRACE, "phase10-regression")
    approved = skill.approve(proposed["candidate"]["skill_id"], "human-owner")

    result = skill.execute()

    assert approved["skill"]["status"] == "ACTIVE"
    assert result["ok"] is True
    assert result["lifecycle_status"] == "ACTIVE"
    assert result["repository"] == {
        "head": "abc123", "clean": False,
        "changes": [" M tracked.py", "?? new.py"],
    }
    assert result["acceptance"]["all_scenarios_passed"] is True
    assert all(item["verified"] for item in result["evidence"])
    assert any("full_acceptance.py" in item for item in runner.commands[-1])
    assert skills.match_active(skill.signature)["approval"]["approver"] == "human-owner"


def test_acceptance_failure_is_returned_as_structured_evidence(tmp_path):
    skill, _, _ = make_skill(tmp_path, acceptance_code=1)
    proposed = skill.propose(TRACE, "phase10-regression")
    skill.approve(proposed["candidate"]["skill_id"], "human-owner")

    result = skill.execute()

    assert result["ok"] is False
    assert result["error"] == "ACCEPTANCE_FAILED"
    assert result["acceptance"]["counts"]["FAIL"] == 1
    assert result["evidence"][-1]["verified"] is False
