# -*- coding: utf-8 -*-

"""
Stage 6.4

Automatic Verifier

Analyzes execution results.
"""

from A_02_MANAGERS.TaskRunner.execution_result import (
    ExecutionResult
)


class AutomaticVerifier:

    @staticmethod
    def verify(result: ExecutionResult):

        if result.success:

            return {

                "status": "SUCCESS",

                "reason": None

            }

        if "SyntaxError" in result.stderr:

            return {

                "status": "FAILED",

                "reason": "Python Syntax Error"

            }

        if "ModuleNotFoundError" in result.stderr:

            return {

                "status": "FAILED",

                "reason": "Missing Module"

            }

        return {

            "status": "FAILED",

            "reason": "Unknown Error"

        }


if __name__ == "__main__":

    ok = ExecutionResult(

        success=True,

        exit_code=0

    )

    bad = ExecutionResult(

        success=False,

        exit_code=1,

        stderr="ModuleNotFoundError"

    )

    print(AutomaticVerifier.verify(ok))

    print(AutomaticVerifier.verify(bad))
