# -*- coding: utf-8 -*-

"""
Stage 8.4.1

Execution History

Reads completed recipes.
"""

import json
from pathlib import Path


COMPLETED = Path("./A_06_WORKSPACE/queue/completed")


class ExecutionHistory:

    @staticmethod
    def load():

        history = []

        for file in sorted(COMPLETED.glob("*.json")):

            with open(file, "r", encoding="utf-8-sig") as f:

                history.append(
                    json.load(f)
                )

        return history


if __name__ == "__main__":

    history = ExecutionHistory.load()

    print("COUNT :", len(history))
    print()

    if history:

        print(history[-1])

