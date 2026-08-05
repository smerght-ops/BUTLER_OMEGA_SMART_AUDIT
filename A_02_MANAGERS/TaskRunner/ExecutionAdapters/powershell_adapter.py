# -*- coding: utf-8 -*-

"""
Stage 6.11

PowerShell Execution Adapter
"""

import subprocess
import time

from A_02_MANAGERS.TaskRunner.execution_result import ExecutionResult
from A_02_MANAGERS.TaskRunner.ExecutionAdapters.base_adapter import (
    BaseExecutionAdapter
)


class PowerShellExecutionAdapter(BaseExecutionAdapter):

    engine_name = "powershell"

    def execute_step(self, step):

        start = time.time()

        cmd = [
            "powershell",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            step.command
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        return ExecutionResult(
            success=result.returncode == 0,
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            duration_ms=int((time.time()-start)*1000),
            executed_steps=[step.command]
        )
