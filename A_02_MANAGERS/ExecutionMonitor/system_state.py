# -*- coding: utf-8 -*-

"""
Stage 8.5

System State

Aggregates current Butler execution state.
"""

from dataclasses import dataclass
from pathlib import Path

from A_02_MANAGERS.ExecutionMonitor.execution_state import ExecutionState


QUEUE = Path("./A_06_WORKSPACE/queue")


@dataclass
class SystemStateSnapshot:

    pending: int

    running: int

    completed: int

    failed: int

    runner_online: bool

    last_recipe_id: str = ""

    last_title: str = ""


class SystemState:

    @staticmethod
    def current():

        pending = len(list((QUEUE / "pending").glob("*.json")))

        running = len(list((QUEUE / "running").glob("*.json")))

        completed = len(list((QUEUE / "completed").glob("*.json")))

        failed = len(list((QUEUE / "failed").glob("*.json")))

        last = ExecutionState.last()

        last_recipe_id = ""

        last_title = ""

        if last:

            last_recipe_id = last.get("recipe_id", "")

            last_title = last.get("title", "")

        return SystemStateSnapshot(

            pending=pending,

            running=running,

            completed=completed,

            failed=failed,

            runner_online=True,

            last_recipe_id=last_recipe_id,

            last_title=last_title

        )


if __name__ == "__main__":

    state = SystemState.current()

    print(state)

