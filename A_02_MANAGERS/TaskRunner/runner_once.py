# -*- coding: utf-8 -*-

"""
Stage 6.8

Runner Once

One autonomous execution cycle.
"""

from pathlib import Path
import shutil

from A_02_MANAGERS.TaskRunner.recipe_queue_watcher import RecipeQueueWatcher
from A_02_MANAGERS.TaskRunner.recipe_loader import RecipeLoader
from A_02_MANAGERS.TaskRunner.recipe_executor import RecipeExecutor
from A_02_MANAGERS.TaskRunner.automatic_verifier import AutomaticVerifier


QUEUE = "./A_06_WORKSPACE/queue"


def run_once():

    watcher = RecipeQueueWatcher(QUEUE)

    pending = watcher.pending_recipes()

    if not pending:

        print("QUEUE EMPTY")

        return

    recipe_file = pending[0]

    print("FOUND :", recipe_file.name)

    recipe = RecipeLoader.load(recipe_file)

    result = RecipeExecutor.execute(recipe)

    verdict = AutomaticVerifier.verify(result)

    print("RESULT :", verdict)

    if verdict["status"] == "SUCCESS":

        target = watcher.completed / recipe_file.name

    else:

        target = watcher.failed / recipe_file.name

    shutil.move(str(recipe_file), str(target))

    print("MOVED TO:", target)


if __name__ == "__main__":

    run_once()

