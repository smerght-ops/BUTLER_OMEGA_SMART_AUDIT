# -*- coding: utf-8 -*-

import json
from pathlib import Path


class ProjectMemoryLoader:

    def __init__(self):
        self.memory_path = (
            Path(__file__).resolve().parent.parent /
            "A_00_ARCHITECTURE" /
            "PROJECT_MEMORY_INDEX.json"
        )

    def load_memory_index(self):
        with open(
            self.memory_path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    def get_built_features(self):
        return self.load_memory_index().get(
            "built",
            []
        )

    def get_current_work(self):
        return self.load_memory_index().get(
            "current_work",
            []
        )

    def get_next_work(self):
        return self.load_memory_index().get(
            "next_work",
            []
        )
