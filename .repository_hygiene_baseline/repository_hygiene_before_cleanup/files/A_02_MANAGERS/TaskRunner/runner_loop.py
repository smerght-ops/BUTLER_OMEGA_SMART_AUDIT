# -*- coding: utf-8 -*-

"""
Stage 7.1

Runner Loop

Continuously executes pending recipes.

Ctrl+C to stop.
"""

import time

from A_02_MANAGERS.TaskRunner.recipe_queue_watcher import RecipeQueueWatcher
from A_02_MANAGERS.TaskRunner.runner_once import run_once


def run():

    watcher = RecipeQueueWatcher("./A_06_WORKSPACE/queue")

    print("=" * 60)
    print("TASK RUNNER LOOP STARTED")
    print("Watching queue...")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    while True:

        if watcher.has_work():

            try:

                run_once()

            except Exception as e:

                print("RUNNER ERROR:", e)

        time.sleep(1)


if __name__ == "__main__":

    run()




