# -*- coding: utf-8 -*-

"""
Stage 8.4

Execution Monitor

Observes execution results.
"""

from pathlib import Path


QUEUE = Path("./A_06_WORKSPACE/queue")


class ExecutionMonitor:

    def __init__(self):

        self.completed = QUEUE / "completed"
        self.failed = QUEUE / "failed"

    def completed_recipes(self):

        return sorted(
            self.completed.glob("*.json")
        )

    def failed_recipes(self):

        return sorted(
            self.failed.glob("*.json")
        )


if __name__ == "__main__":

    monitor = ExecutionMonitor()

    print("COMPLETED:")
    print(monitor.completed_recipes())

    print()

    print("FAILED:")
    print(monitor.failed_recipes())
