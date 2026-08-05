# -*- coding: utf-8 -*-

import subprocess
import sys

from A_02_MANAGERS.recipe_generator import RecipeGenerator
from A_02_MANAGERS.recipe_validator import RecipeValidator


def run_guarded_task(task_id):

    print("=" * 70)
    print(f"[GATE] Starting audit for task: {task_id}")
    print("=" * 70)

    generator = RecipeGenerator()
    recipe = generator.generate(task_id)

    validator = RecipeValidator()
    result = validator.validate(recipe)

    if not result.valid:

        print("[GATE] RECIPE REJECTED")

        for err in result.errors:
            print(" [!]", err)

        sys.exit(1)

    print("[GATE] Recipe accepted.")
    print("[GATE] Launching TaskRunner...")

    cmd = [
        sys.executable,
        r".\A_02_MANAGERS\TaskRunner\runner.py",
        task_id
    ]

    completed = subprocess.run(cmd)

    if completed.returncode != 0:
        sys.exit(completed.returncode)

    print("=" * 70)
    print("[GATE] TASK FINISHED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage:")
        print("python Butler_Gate.py <task_id>")

        sys.exit(1)

    run_guarded_task(sys.argv[1])
