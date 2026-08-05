"""Controlled lifecycle over the existing SemanticMemory skill records."""

from __future__ import annotations

import hashlib
import time
from dataclasses import asdict, dataclass
from typing import Any, Iterable

from A_01_CORE.judge_runtime import Evidence, JudgeRuntime
from A_07_MEMORY.semantic_memory import SemanticMemory


@dataclass(frozen=True)
class SkillContract:
    skill_id: str
    name: str
    signature: tuple[str, ...]
    trace: tuple[dict[str, Any], ...]
    version: int
    status: str
    provenance: str

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["signature"] = list(self.signature)
        value["trace"] = list(self.trace)
        return value


class SkillIndex:
    """Computed index; SemanticMemory remains the sole persistence owner."""

    def __init__(self, memory: SemanticMemory):
        self.memory = memory

    def events(self, skill_id: str | None = None) -> list[dict]:
        values = self.memory.skill_events()
        return [item for item in values if skill_id is None or item.get("skill_id") == skill_id]

    def versions(self, skill_id: str) -> list[dict]:
        return [item for item in self.events(skill_id) if item.get("event") == "SKILL_CANDIDATE"]

    def current(self, skill_id: str) -> dict | None:
        events = self.events(skill_id)
        if not events:
            return None
        last = events[-1]
        if last.get("event") == "SKILL_ROLLBACK":
            version = last.get("active_version")
            candidate = next((item for item in reversed(self.versions(skill_id)) if item.get("version") == version), None)
            if candidate:
                value = dict(candidate)
                value.update({"status": "ACTIVE", "approval": last.get("approval"), "event": "SKILL_ROLLBACK"})
                return value
        return last

    def active(self) -> list[dict]:
        ids = list(dict.fromkeys(item.get("skill_id") for item in self.events() if item.get("skill_id")))
        return [item for item in (self.current(skill_id) for skill_id in ids) if item and item.get("status") == "ACTIVE"]


class SkillRouter:
    def __init__(self, index: SkillIndex):
        self.index = index

    def match(self, signature: Iterable[str]) -> dict | None:
        target = [str(item) for item in signature if item]
        return next((item for item in reversed(self.index.active()) if item.get("signature") == target), None)


class SkillCandidateBuilder:
    COMMAND_PREFIXES = ("skill save ", "save skill ", "сохрани навык ")

    def __init__(self, judge: JudgeRuntime):
        self.judge = judge

    def build(self, command: str, signature, trace, provenance: str, version: int) -> tuple[SkillContract, dict]:
        normalized = str(command or "").strip()
        prefix = next((item for item in self.COMMAND_PREFIXES if normalized.casefold().startswith(item)), None)
        if prefix is None:
            raise PermissionError("EXPLICIT_SKILL_SAVE_COMMAND_REQUIRED")
        name = normalized[len(prefix):].strip()
        signature = tuple(str(item) for item in signature if item)
        trace = tuple(dict(item) for item in trace)
        if not name or not signature or not trace:
            raise ValueError("SKILL_CANDIDATE_INCOMPLETE")
        evidence = [
            Evidence("TaskExecutor", f"step {index}", item, verified=item.get("ok") is True, kind="execution_trace")
            for index, item in enumerate(trace, 1)
        ]
        judgment = self.judge.evaluate(
            {"ok": all(item.get("ok") is True for item in trace), "error": None}, evidence=evidence,
        )
        if judgment["verdict"] != "PASS":
            raise ValueError("SKILL_JUDGE_VALIDATION_FAILED")
        digest = hashlib.sha256("|".join(signature).encode("utf-8")).hexdigest()[:16]
        return SkillContract(
            skill_id=f"skill:{digest}", name=name, signature=signature, trace=trace,
            version=version, status="CANDIDATE", provenance=str(provenance),
        ), judgment


class SkillManager:
    """Sole lifecycle owner for candidate, approval, rollback, and telemetry."""

    def __init__(self, memory: SemanticMemory | None = None, judge: JudgeRuntime | None = None):
        self.memory = memory or SemanticMemory()
        self.judge = judge or JudgeRuntime()
        self.index = SkillIndex(self.memory)
        self.router = SkillRouter(self.index)
        self.builder = SkillCandidateBuilder(self.judge)

    def propose(self, command: str, signature, trace, provenance: str) -> dict:
        signature = tuple(str(item) for item in signature if item)
        provisional_id = "skill:" + hashlib.sha256("|".join(signature).encode("utf-8")).hexdigest()[:16]
        version = len(self.index.versions(provisional_id)) + 1
        contract, judgment = self.builder.build(command, signature, trace, provenance, version)
        record = {
            "path": f"memory://skills/{contract.skill_id.split(':', 1)[1]}",
            "handler": "SkillManager", "type": "skill", "event": "SKILL_CANDIDATE",
            "timestamp": int(time.time()), **contract.to_dict(), "judge": judgment,
            "needs_review": True, "source": str(provenance),
        }
        self.memory.append_skill_event(record)
        return {"ok": True, "candidate": record, "requires_approval": True}

    def approve(self, skill_id: str, approver: str) -> dict:
        current = self.index.current(skill_id)
        if not current or current.get("status") != "CANDIDATE":
            return {"ok": False, "error": "SKILL_CANDIDATE_NOT_FOUND"}
        if not str(approver or "").strip():
            return {"ok": False, "error": "HUMAN_APPROVAL_REQUIRED"}
        evidence = [Evidence("SkillManager", "candidate trace", item, verified=item.get("ok") is True)
                    for item in current.get("trace", [])]
        judgment = self.judge.evaluate({"ok": True, "error": None}, evidence=evidence)
        if judgment["verdict"] != "PASS":
            return {"ok": False, "error": "SKILL_JUDGE_VALIDATION_FAILED", "judge": judgment}
        event = dict(current)
        event.update({
            "event": "SKILL_APPROVED", "status": "ACTIVE", "timestamp": int(time.time()),
            "approval": {"approver": str(approver), "approved": True}, "judge": judgment,
            "needs_review": False,
        })
        self.memory.append_skill_event(event)
        return {"ok": True, "skill": event}

    def rollback(self, skill_id: str, version: int, approver: str) -> dict:
        target = next((item for item in self.index.versions(skill_id) if item.get("version") == int(version)), None)
        if target is None:
            return {"ok": False, "error": "SKILL_VERSION_NOT_FOUND"}
        if not str(approver or "").strip():
            return {"ok": False, "error": "HUMAN_APPROVAL_REQUIRED"}
        event = {
            "path": target["path"], "handler": "SkillManager", "type": "skill",
            "event": "SKILL_ROLLBACK", "skill_id": skill_id, "active_version": int(version),
            "status": "ACTIVE", "timestamp": int(time.time()), "signature": target["signature"],
            "approval": {"approver": str(approver), "approved": True}, "needs_review": False,
        }
        self.memory.append_skill_event(event)
        return {"ok": True, "skill": self.index.current(skill_id), "event": event}

    def record_telemetry(self, signature, trace, provenance: str, reused: bool = False) -> dict:
        record = {
            "path": "memory://skills/telemetry", "handler": "SkillManager", "type": "skill_telemetry",
            "event": "SKILL_EXECUTION_OBSERVED", "timestamp": int(time.time()),
            "signature": [str(item) for item in signature if item],
            "successful": bool(trace and all(item.get("ok") for item in trace)),
            "steps": len(trace or []), "reused": bool(reused), "source": str(provenance),
        }
        self.memory.append_skill_event(record)
        return record

    def match_active(self, signature) -> dict | None:
        return self.router.match(signature)
