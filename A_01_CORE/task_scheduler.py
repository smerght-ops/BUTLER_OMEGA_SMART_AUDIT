"""Dependency-aware scheduler for controlled read-only parallel execution."""

from __future__ import annotations

import threading
import re
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from A_01_CORE.runtime_contracts import CancellationToken


class TaskGraph:
    STEP_REFERENCE = re.compile(r"\{\{step_(\d+)\.[^}]+\}\}")

    def __init__(self, steps: Iterable[dict], satisfied: Iterable[int] = ()):
        values = [dict(step) for step in steps]
        self.steps = {int(step["order"]): step for step in values}
        satisfied = {int(item) for item in satisfied}
        if len(self.steps) != len(values):
            raise ValueError("TASK_GRAPH_DUPLICATE_ORDER")
        for order, step in self.steps.items():
            dependencies = {int(item) for item in step.get("depends_on", [])}
            dependencies.update(self._references(step.get("arguments") or {}))
            if order in dependencies or not dependencies <= (self.steps.keys() | satisfied):
                raise ValueError("TASK_GRAPH_INVALID_DEPENDENCY")
            step["depends_on"] = sorted(dependencies - satisfied)

    @classmethod
    def _references(cls, value) -> set[int]:
        if isinstance(value, dict):
            return set().union(*(cls._references(item) for item in value.values())) if value else set()
        if isinstance(value, (list, tuple)):
            return set().union(*(cls._references(item) for item in value)) if value else set()
        if isinstance(value, str):
            return {int(match) for match in cls.STEP_REFERENCE.findall(value)}
        return set()

    def layers(self) -> list[list[dict]]:
        pending = set(self.steps)
        completed = set()
        layers = []
        while pending:
            ready = sorted(order for order in pending if set(self.steps[order].get("depends_on", [])) <= completed)
            if not ready:
                raise ValueError("TASK_GRAPH_CYCLE")
            layers.append([self.steps[order] for order in ready])
            completed.update(ready)
            pending.difference_update(ready)
        return layers


class WorkspaceIsolation:
    MUTATING_ACTIONS = ("create_", "save_", "write_", "delete_", "move_", "rename_", "edit_", "update_")

    @classmethod
    def is_read_only(cls, step: dict) -> bool:
        declared = step.get("read_only") is True or (step.get("arguments") or {}).get("read_only") is True
        action = str(step.get("action") or "").casefold()
        return declared and not action.startswith(cls.MUTATING_ACTIONS)


@dataclass
class _ResourceState:
    readers: int = 0
    writer: bool = False


class ResourceManager:
    """Process-local reader/writer locks for scheduler resource keys."""

    def __init__(self):
        self._condition = threading.Condition(threading.RLock())
        self._states: dict[str, _ResourceState] = {}

    @contextmanager
    def lease(self, resource: str, read_only: bool):
        key = str(Path(resource).resolve()) if resource else "workspace://default"
        with self._condition:
            state = self._states.setdefault(key, _ResourceState())
            self._condition.wait_for(lambda: not state.writer and (read_only or state.readers == 0))
            if read_only:
                state.readers += 1
            else:
                state.writer = True
        try:
            yield key
        finally:
            with self._condition:
                if read_only:
                    state.readers -= 1
                else:
                    state.writer = False
                self._condition.notify_all()


class TaskScheduler:
    def __init__(self, max_workers: int = 4, resources: ResourceManager | None = None):
        if max_workers < 1:
            raise ValueError("max_workers must be positive")
        self.max_workers = max_workers
        self.resources = resources or ResourceManager()

    @staticmethod
    def _resource(step: dict) -> str:
        arguments = step.get("arguments") or {}
        return str(arguments.get("workspace") or arguments.get("path") or arguments.get("folder") or "")

    def execute_layer(self, steps: list[dict], worker: Callable[[dict], object], token: CancellationToken) -> list:
        if not steps:
            return []
        parallel = len(steps) > 1 and all(WorkspaceIsolation.is_read_only(step) for step in steps)

        def guarded(step):
            token.raise_if_cancelled()
            read_only = WorkspaceIsolation.is_read_only(step)
            with self.resources.lease(self._resource(step), read_only=read_only):
                value = worker(step)
            token.raise_if_cancelled()
            return value

        if not parallel:
            return [guarded(step) for step in steps]
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(steps)), thread_name_prefix="butler-task") as pool:
            futures = [pool.submit(guarded, step) for step in steps]
            return [future.result() for future in futures]
