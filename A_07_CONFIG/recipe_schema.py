# -*- coding: utf-8 -*-

"""
Stage 6.2

Recipe Schema

Universal execution recipe.
"""

from dataclasses import dataclass, field
from typing import List, Dict

SCHEMA_VERSION = "6.2"


@dataclass
class RecipeStep:

    engine: str

    command: str

    args: List[str] = field(default_factory=list)


@dataclass
class Recipe:

    recipe_id: str

    title: str

    description: str = ""

    dry_run: bool = True

    steps: List[RecipeStep] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)


if __name__ == "__main__":

    recipe = Recipe(

        recipe_id="TEST001",

        title="Compile",

        steps=[

            RecipeStep(

                engine="python",

                command="-m",

                args=[

                    "py_compile",

                    "main.py"

                ]

            )

        ]

    )

    print(recipe)
