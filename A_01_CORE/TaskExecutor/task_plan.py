from __future__ import annotations

from dataclasses import dataclass, field

from .task_step import TaskStep


@dataclass
class TaskPlan:
    goal: str
    steps: list[TaskStep] = field(default_factory=list)

    @property
    def missing(self) -> list[str]:
        return list(dict.fromkeys(
            step.action for step in self.steps if step.status == "missing_capability"
        ))

    @property
    def status(self) -> str:
        if self.missing:
            return "missing_capability"
        return "planned" if self.steps else "unresolved"

    def to_dict(self) -> dict:
        result = {
            "goal": self.goal,
            "status": self.status,
            "steps": [step.to_dict() for step in self.steps],
        }
        if self.missing:
            result["missing"] = self.missing
        return result
