# -*- coding: utf-8 -*-

"""
Stage 7.2

Recipe Builder

Builds Recipe objects programmatically.
"""

from uuid import uuid4

from uuid import uuid4

from A_07_CONFIG.recipe_schema import Recipe, RecipeStep


class RecipeBuilder:

    @staticmethod
    def python(command,*args):

        return Recipe(
            recipe_id=f"AUTO_{uuid4().hex[:8]}",
            title="Python Task",
            dry_run=False,
            steps=[
                RecipeStep(
                    engine="python",
                    command=command,
                    args=list(args)
                )
            ]
        )


    @staticmethod
    def powershell(command):

        return Recipe(
            recipe_id=f"AUTO_{uuid4().hex[:8]}",
            title="PowerShell Task",
            dry_run=False,
            steps=[
                RecipeStep(
                    engine="powershell",
                    command=command,
                    args=[]
                )
            ]
        )


if __name__ == "__main__":

    print(
        RecipeBuilder.powershell(
            "Write-Output 'HELLO'"
        )
    )






