# -*- coding: utf-8 -*-

import json
from pathlib import Path


class QueueManager:
    """
    Writes generated recipes into A_07_CONFIG/queue.
    Does not execute them.
    """

    def __init__(self, root=None):
        self.root = Path(root) if root else Path.cwd()
        self.queue_dir = self.root / "A_07_CONFIG" / "queue"
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def enqueue(self, recipe):
        task_id = recipe.get("task_id", "unknown_recipe")
        path = self.queue_dir / f"{task_id}.json"
        path.write_text(
            json.dumps(recipe, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return str(path)
