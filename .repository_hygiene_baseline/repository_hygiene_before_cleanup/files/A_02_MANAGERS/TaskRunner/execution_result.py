# -*- coding: utf-8 -*-

"""
Stage 6.1

Execution Result

Universal execution contract.
"""

from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class ExecutionResult:

    success: bool

    exit_code: int

    stdout: str = ""

    stderr: str = ""

    duration_ms: int = 0

    executed_steps: List[str] = field(default_factory=list)

    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )


if __name__ == "__main__":

    result = ExecutionResult(

        success=True,

        exit_code=0,

        stdout="Everything OK",

        duration_ms=842,

        executed_steps=[

            "py_compile",

            "integration_test"

        ]

    )

    print(result)
