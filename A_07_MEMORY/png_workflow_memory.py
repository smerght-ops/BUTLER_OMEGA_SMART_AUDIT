# -*- coding: utf-8 -*-

import json
from pathlib import Path


class PNGWorkflowMemory:

    def __init__(self):

        self.memory_dir = Path("A_07_MEMORY")
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.db = self.memory_dir / "PNG_WORKFLOW_MEMORY.json"

        if not self.db.exists():
            self.db.write_text(
                "{}",
                encoding="utf-8"
            )

    def _load(self):

        return json.loads(
            self.db.read_text(
                encoding="utf-8"
            )
        )

    def _save(self, data):

        self.db.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def register(
        self,
        image_name,
        workflow_name
    ):

        data = self._load()

        data[image_name] = workflow_name

        self._save(data)

    def get_workflow(
        self,
        image_name
    ):

        data = self._load()

        return data.get(image_name)
