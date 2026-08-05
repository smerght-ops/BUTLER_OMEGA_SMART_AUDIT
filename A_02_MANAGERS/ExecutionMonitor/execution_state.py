# -*- coding: utf-8 -*-

"""
Stage 8.4.2

Execution State

Provides the latest execution result.
"""

from A_02_MANAGERS.ExecutionMonitor.execution_history import ExecutionHistory


class ExecutionState:

    @staticmethod
    def last():

        history = ExecutionHistory.load()

        if not history:

            return None

        return history[-1]


if __name__ == "__main__":

    state = ExecutionState.last()

    print(state)
