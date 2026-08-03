# -*- coding: utf-8 -*-

"""
Stage 6.7

Recipe Loader

Loads Recipe objects from JSON.
"""

import json

from pathlib import Path

from A_07_CONFIG.recipe_schema import (
    Recipe,
    RecipeStep
)


class RecipeLoader:

    @staticmethod
    def load(path):

        path = Path(path)

        with open(path, "r", encoding="utf-8-sig") as f:

            data = json.load(f)

        steps = []

        for s in data["steps"]:

            steps.append(

                RecipeStep(

                    engine=s["engine"],

                    command=s["command"],

                    args=s.get("args", [])

                )

            )

        return Recipe(

            recipe_id=data["recipe_id"],

            title=data["title"],

            description=data.get("description", ""),

            dry_run=data.get("dry_run", True),

            steps=steps,

            metadata=data.get("metadata", {})

        )


if __name__ == "__main__":

    recipe = RecipeLoader.load(

        "./A_06_WORKSPACE/queue/pending/recipe_test.json"

    )

    print(recipe)

    print()

    print(recipe.steps[0])

