from A_01_CORE.model_fleet_audit_skill import (
    ConfiguredModelLocation,
    ModelFleetAuditSkill,
    discover_configured_locations,
)
from A_01_CORE.skill_runtime import SkillManager
from A_07_MEMORY.semantic_memory import SemanticMemory


TRACE = [
    {"capability_id": "model_locations.inspect", "ok": True},
    {"capability_id": "model_metadata.collect", "ok": True},
    {"capability_id": "model_missing.detect", "ok": True},
    {"capability_id": "model_duplicates.detect", "ok": True},
    {"capability_id": "evidence.collect", "ok": True},
]


def manager(tmp_path):
    memory = SemanticMemory()
    memory.memory_dir = tmp_path / "memory"
    memory.memory_dir.mkdir()
    memory.index_path = memory.memory_dir / "MEMORY_INDEX.jsonl"
    memory.index_path.touch()
    return SkillManager(memory=memory)


def make_skill(tmp_path):
    models = tmp_path / "models"
    models.mkdir()
    (models / "alpha.gguf").write_bytes(b"same-model")
    (models / "alpha-copy.gguf").write_bytes(b"same-model")
    (models / "unique.safetensors").write_bytes(b"unique-model")
    location = ConfiguredModelLocation(
        "test-config", str(models), ("alpha.gguf", "missing.pt"),
    )
    return ModelFleetAuditSkill(manager(tmp_path), root=tmp_path, locations=[location])


def activate(skill):
    proposed = skill.propose(TRACE, "phase11-regression")
    return proposed, skill.approve(proposed["candidate"]["skill_id"], "human-owner")


def test_lifecycle_blocks_audit_until_judge_and_human_approval(tmp_path):
    skill = make_skill(tmp_path)
    proposed = skill.propose(TRACE, "phase11-regression")
    skill_id = proposed["candidate"]["skill_id"]

    assert proposed["candidate"]["status"] == "CANDIDATE"
    assert proposed["candidate"]["judge"]["verdict"] == "PASS"
    assert skill.execute()["error"] == "SKILL_NOT_ACTIVE"
    assert skill.approve(skill_id, "")["error"] == "HUMAN_APPROVAL_REQUIRED"


def test_active_audit_collects_metadata_missing_and_duplicates(tmp_path):
    skill = make_skill(tmp_path)
    _, approved = activate(skill)

    result = skill.execute()

    assert approved["skill"]["status"] == "ACTIVE"
    assert result["ok"] is True
    assert result["lifecycle_status"] == "ACTIVE"
    assert result["health"] == "DEGRADED"
    assert result["summary"] == {
        "locations": 1, "models": 3, "missing": 1,
        "duplicate_groups": 1, "errors": 0,
    }
    assert result["missing"][0]["reason"] == "EXPECTED_MODEL_MISSING"
    assert result["duplicates"][0]["count"] == 2
    assert all(model["sha256"] for model in result["models"])


def test_missing_configured_location_is_structured_audit_evidence(tmp_path):
    location = ConfiguredModelLocation("test-config", str(tmp_path / "absent"))
    skill = ModelFleetAuditSkill(manager(tmp_path), root=tmp_path, locations=[location])
    activate(skill)

    result = skill.execute()

    assert result["ok"] is True
    assert result["health"] == "DEGRADED"
    assert result["missing"] == [{
        "path": str((tmp_path / "absent").resolve()),
        "reason": "CONFIGURED_LOCATION_MISSING",
        "source": "test-config",
    }]


def test_existing_engine_configuration_is_discovered_without_import(tmp_path):
    source = tmp_path / "A_03_ENGINES" / "Audio_Engine" / "whisper_engine.py"
    source.parent.mkdir(parents=True)
    source.write_text(
        'MODELS_PATH = "configured-models"\n'
        'AVAILABLE_MODELS = ["turbo", "large-v3"]\n',
        encoding="utf-8",
    )

    locations = discover_configured_locations(tmp_path)

    assert locations == [ConfiguredModelLocation(
        "A_03_ENGINES/Audio_Engine/whisper_engine.py",
        str(tmp_path / "configured-models"),
        ("turbo.pt", "large-v3.pt"),
    )]
