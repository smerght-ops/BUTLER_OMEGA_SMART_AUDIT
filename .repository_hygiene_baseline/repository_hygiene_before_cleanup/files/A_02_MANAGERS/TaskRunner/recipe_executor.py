# -*- coding: utf-8 -*-

"""
Stage 6.10

Recipe Executor

Uses ExecutorFactory and ExecutionAdapters.
"""

import time

from A_07_CONFIG.recipe_schema import Recipe, RecipeStep
from A_02_MANAGERS.TaskRunner.execution_result import ExecutionResult
from A_02_MANAGERS.TaskRunner.executor_factory import ExecutorFactory


class RecipeExecutor:

    @staticmethod
    def execute(recipe: Recipe):

        start = time.time()

        stdout = ""

        stderr = ""

        executed = []

        exit_code = 0

        success = True

        for step in recipe.steps:

            adapter = ExecutorFactory.get(step.engine)

            step_result = adapter.execute_step(step)

            stdout += step_result.stdout

            stderr += step_result.stderr

            executed.extend(step_result.executed_steps)

            exit_code = step_result.exit_code

            if not step_result.success:

                success = False

                break

        return ExecutionResult(
            success=success,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            duration_ms=int((time.time() - start) * 1000),
            executed_steps=executed
        )


if __name__ == "__main__":

    recipe = Recipe(
        recipe_id="TEST_FACTORY",
        title="Python Version via Factory",
        dry_run=False,
        steps=[
            RecipeStep(
                engine="python",
                command="--version",
                args=[]
            )
        ]
    )

    result = RecipeExecutor.execute(recipe)

    print(result)
