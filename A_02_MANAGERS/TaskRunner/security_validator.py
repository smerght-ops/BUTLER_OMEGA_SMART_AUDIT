# -*- coding: utf-8 -*-

"""
Stage 6.6

Security Validator

Validates Recipe before execution.
"""

from pathlib import Path


class SecurityViolation(Exception):
    pass


class SecurityValidator:

    ALLOWED_ENGINES = {
        "python",
    }

    FORBIDDEN_WORDS = {
        "format",
        "diskpart",
        "shutdown",
        "del",
        "rd",
        "rmdir",
        "Remove-Item",
    }

    @classmethod
    def validate(cls, recipe):

        for step in recipe.steps:

            if step.engine not in cls.ALLOWED_ENGINES:

                raise SecurityViolation(
                    f"Engine not allowed: {step.engine}"
                )

            cmd = step.command.lower()

            for word in cls.FORBIDDEN_WORDS:

                if word.lower() in cmd:

                    raise SecurityViolation(
                        f"Forbidden command: {step.command}"
                    )

        return True


if __name__ == "__main__":

    from A_02_MANAGERS.TaskRunner.recipe_loader import RecipeLoader

    recipe = RecipeLoader.load(
        "./A_06_WORKSPACE/queue/completed/recipe_test.json"
    )

    print(SecurityValidator.validate(recipe))
