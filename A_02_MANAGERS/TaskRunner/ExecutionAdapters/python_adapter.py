# -*- coding: utf-8 -*-

"""
Stage 6.9

Python Execution Adapter
"""

import subprocess
import time

from A_02_MANAGERS.TaskRunner.execution_result import ExecutionResult
from A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter import (
    BaseExecutionAdapter
)


class PythonExecutionAdapter(BaseExecutionAdapter):

    engine_name = "python"

    def execute_step(self, step) -> ExecutionResult:

        start = time.time()

        cmd = ["python", step.command] + step.args

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        return ExecutionResult(
            success=result.returncode == 0,
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            duration_ms=int((time.time() - start) * 1000),
            executed_steps=[step.command]
        )
