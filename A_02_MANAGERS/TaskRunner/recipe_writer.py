# -*- coding: utf-8 -*-

"""
Stage 7.2

Recipe Writer

Writes Recipe into queue/pending.
"""

import json
from dataclasses import asdict
from pathlib import Path


class RecipeWriter:

    ROOT = Path("./A_06_WORKSPACE/queue/pending")


    @classmethod
    def write(cls, recipe):

        cls.ROOT.mkdir(parents=True, exist_ok=True)

        filename = cls.ROOT / f"{recipe.recipe_id}.json"

        with open(filename, "w", encoding="utf-8") as f:

            json.dump(
                asdict(recipe),
                f,
                ensure_ascii=False,
                indent=4
            )

        return filename


if __name__ == "__main__":

    from A_02_MANAGERS.TaskRunner.recipe_builder import RecipeBuilder

    recipe = RecipeBuilder.powershell(
        "Write-Output 'RecipeWriter OK'"
    )

    path = RecipeWriter.write(recipe)

    print(path)
