# -*- coding: utf-8 -*-

from copy import deepcopy

from A_07_CONFIG.task_registry import TASKS
from A_07_CONFIG.recipe_schema import SCHEMA_VERSION


class RecipeGenerator:
    """
    Converts legacy TASKS registry into Recipe Schema v1.0.
    Does not execute anything.
    """

    def generate(self, task_id: str) -> dict:

        task_id = task_id.lower()

        if task_id not in TASKS:
            raise KeyError(f"Unknown task: {task_id}")

        recipe = {
            "schema_version": SCHEMA_VERSION,
            "task_id": task_id,
            "steps": []
        }

        for cmd in deepcopy(TASKS[task_id]):

            if isinstance(cmd, dict):

                if cmd.get("action") == "patch":

                    recipe["steps"].append({
                        "action": "patch",
                        "target": cmd.get("target", cmd.get("file")),
                        "payload": {
                            "old": cmd.get("old"),
                            "new": cmd.get("new"),
                        }
                    })

                    continue

                raise RuntimeError(f"Unknown legacy dict action: {cmd}")

            if not isinstance(cmd, list):
                raise TypeError(f"Unsupported legacy step: {cmd}")

            if len(cmd) >= 4 and cmd[1] == "-m" and cmd[2] == "py_compile":

                recipe["steps"].append({
                    "action": "compile",
                    "target": cmd[3]
                })

                continue

            if len(cmd) >= 3 and cmd[1] == "-m":

                recipe["steps"].append({
                    "action": "execute",
                    "module": cmd[2]
                })

                continue

            if len(cmd) >= 3 and cmd[1] == "-c":

                recipe["steps"].append({
                    "action": "execute",
                    "command": cmd[2]
                })

                continue

            raise RuntimeError(f"Unknown legacy command: {cmd}")

        return recipe


if __name__ == "__main__":

    import pprint

    generator = RecipeGenerator()

    for name in TASKS:
        print("=" * 70)
        print(name)
        pprint.pp(generator.generate(name))
