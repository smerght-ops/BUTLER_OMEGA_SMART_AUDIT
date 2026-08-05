# -*- coding: utf-8 -*-

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

DISCOVERY = Path(__file__).resolve().parent
sys.path.insert(0, str(DISCOVERY))

from engineering_object import EngineeringObject


class EngineeringObjectCatalog:

    def __init__(self):
        self._objects = {}

    def register(self, obj: EngineeringObject):
        self._objects[obj.object_id] = obj

    def exists(self, object_id: str):
        return object_id in self._objects

    def get(self, object_id: str):
        return self._objects.get(object_id)

    def all(self):
        return list(self._objects.values())

    def count(self):
        return len(self._objects)


if __name__ == "__main__":
    catalog = EngineeringObjectCatalog()

    obj = EngineeringObject()
    obj.object_id = "ENG-000001"
    obj.name = "Engineering Object"

    catalog.register(obj)

    print("=== ENGINEERING OBJECT CATALOG TEST ===")
    print()

    print("COUNT  :", catalog.count())
    print("EXISTS :", catalog.exists("ENG-000001"))
    print("OBJECT :", catalog.get("ENG-000001").name)
