from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArtifactReference:
    """Opaque project-artifact address passed between TaskPlan steps."""

    artifact_id: str
    kind: str
    _locator: str

    @property
    def locator(self) -> str:
        """Department compatibility boundary; orchestration must not inspect it."""
        return self._locator

    def __str__(self) -> str:
        return self._locator

    def to_dict(self, include_locator=False) -> dict:
        result = {"artifact_ref": self.artifact_id, "kind": self.kind}
        if include_locator:
            result["path"] = self._locator
        return result


class ExecutionContext:
    TEMPLATE = re.compile(r"\{\{(step_\d+)\.([a-zA-Z0-9_.]+)\}\}")

    def __init__(self, variables=None):
        self.results: dict[str, dict] = {}
        self.artifacts: list[dict] = []
        self.variables: dict = dict(variables or {})
        self.history: list[dict] = []

    def record(self, step_number: int, step: dict, result: dict, output):
        key = f"step_{step_number}"
        self.results[key] = {"output": output, "result": result}
        event = {
            "step": step_number,
            "capability_id": step.get("capability_id"),
            "department": result.get("department"),
            "ok": bool(result.get("ok")),
            "error": result.get("error"),
            "output": output,
            "artifact": step.get("artifacts"),
        }
        self.history.append(event)
        locator = output.locator if isinstance(output, ArtifactReference) else output
        if isinstance(locator, str):
            path = Path(locator)
            if path.exists():
                descriptor = step.get("artifacts") or {}
                self.artifacts.append({
                    "step": step_number,
                    "name": descriptor.get("output") or getattr(output, "artifact_id", None),
                    "type": descriptor.get("type", "file_path" if path.is_file() else "directory_path"),
                    "reference": output if isinstance(output, ArtifactReference) else None,
                    "path": str(path),
                    "is_file": path.is_file(),
                })

    def resolve(self, value):
        if isinstance(value, dict):
            return {key: self.resolve(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self.resolve(item) for item in value]
        if not isinstance(value, str):
            return value

        full = self.TEMPLATE.fullmatch(value)
        if full:
            return self._lookup(full.group(1), full.group(2))
        return self.TEMPLATE.sub(
            lambda match: str(self._lookup(match.group(1), match.group(2))),
            value,
        )

    def _lookup(self, step_key: str, field: str):
        if step_key not in self.results:
            raise KeyError(f"unknown step reference: {step_key}")
        current = self.results[step_key]
        for part in field.split("."):
            if not isinstance(current, dict) or part not in current:
                raise KeyError(f"unknown step field: {step_key}.{field}")
            current = current[part]
        return current

    def snapshot(self) -> dict:
        return self._portable({
            "results": self.results,
            "artifacts": self.artifacts,
            "variables": dict(self.variables),
            "history": list(self.history),
        })

    @classmethod
    def from_snapshot(cls, snapshot):
        context = cls((snapshot or {}).get("variables"))
        history = []
        for event in list((snapshot or {}).get("history") or []):
            if not event.get("ok"):
                break
            history.append(event)
        completed = {int(event.get("step", 0)) for event in history}
        context.history = history
        context.results = {
            key: value for key, value in dict((snapshot or {}).get("results") or {}).items()
            if key.startswith("step_") and int(key.split("_", 1)[1]) in completed
        }
        context.artifacts = [
            item for item in list((snapshot or {}).get("artifacts") or [])
            if int(item.get("step", 0)) in completed
        ]
        return context

    @classmethod
    def _portable(cls, value):
        if isinstance(value, ArtifactReference):
            return value.to_dict()
        if isinstance(value, dict):
            return {key: cls._portable(item) for key, item in value.items()}
        if isinstance(value, list):
            return [cls._portable(item) for item in value]
        return value
