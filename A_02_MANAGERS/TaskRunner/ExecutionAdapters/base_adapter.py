# -*- coding: utf-8 -*-

"""
Stage 6.9

Base Execution Adapter
"""

from A_02_MANAGERS.TaskRunner.execution_result import ExecutionResult


class BaseExecutionAdapter:

    engine_name = None

    def execute_step(self, step) -> ExecutionResult:

        raise NotImplementedError(
            "Execution adapter must implement execute_step()"
        )
