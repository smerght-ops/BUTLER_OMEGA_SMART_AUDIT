from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TaskStep:
    order: int
    department: str
    action: str
    object: str
    status: str = "planned"
    capability_id: str | None = None
    requested_action: str | None = None
    source_text: str = ""
    depends_on: tuple[int, ...] = field(default_factory=tuple)
    arguments: dict = field(default_factory=dict)
    output_artifact: str | None = None
    artifact_type: str | None = None

    def to_dict(self) -> dict:
        result = {
            "order": self.order,
            "department": self.department,
            "action": self.action,
            "object": self.object,
            "status": self.status,
            "depends_on": list(self.depends_on),
            "arguments": dict(self.arguments),
        }
        if self.capability_id:
            result["capability_id"] = self.capability_id
        if self.requested_action:
            result["requested_action"] = self.requested_action
        if self.source_text:
            result["source_text"] = self.source_text
        if self.output_artifact:
            result["artifacts"] = {
                "output": self.output_artifact,
                "type": self.artifact_type or "text",
            }
        return result
