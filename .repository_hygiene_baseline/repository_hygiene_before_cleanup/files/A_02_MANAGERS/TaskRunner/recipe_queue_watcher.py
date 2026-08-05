# -*- coding: utf-8 -*-

"""
Stage 6.5

Recipe Queue Watcher

Foundation only.
"""

from pathlib import Path


class RecipeQueueWatcher:

    def __init__(self, root):

        self.root = Path(root)

        self.pending = self.root / "pending"

        self.running = self.root / "running"

        self.completed = self.root / "completed"

        self.failed = self.root / "failed"

    def pending_recipes(self):

        return sorted(self.pending.glob("*.json"))

    def has_work(self):

        return len(self.pending_recipes()) > 0


if __name__ == "__main__":

    watcher = RecipeQueueWatcher(

        "./A_06_WORKSPACE/queue"

    )

    print("PENDING:", watcher.pending_recipes())

    print("HAS WORK:", watcher.has_work())
