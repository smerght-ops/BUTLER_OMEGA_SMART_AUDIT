# -*- coding: utf-8 -*-

from engineering_object import EngineeringObject
from engineering_object_catalog import EngineeringObjectCatalog
from engineering_evidence_collection import EngineeringEvidenceCollection


class ObjectMerge:
    """
    PHASE 5.1

    Converts EngineeringEvidence into EngineeringObjects.
    """

    def __init__(self):

        self.catalog = EngineeringObjectCatalog()

    def merge(self, evidence_collection: EngineeringEvidenceCollection):

        for evidence in evidence_collection.all():

            object_id = getattr(
                evidence,
                "object_id",
                evidence.object_name
            )

            if self.catalog.exists(object_id):
                continue

            obj = EngineeringObject()

            obj.object_id = object_id
            obj.name = evidence.object_name
            obj.type = evidence.object_type

            self.catalog.register(obj)

        return self.catalog


if __name__ == "__main__":

    from engineering_evidence import EngineeringEvidence

    collection = EngineeringEvidenceCollection()

    e = EngineeringEvidence()
    e.object_id = "ENG-000001"
    e.object_name = "Passport"
    e.object_type = "PASSPORT"

    collection.add(e)

    merger = ObjectMerge()

    catalog = merger.merge(collection)

    print("=== OBJECT MERGE TEST ===")
    print()
    print("OBJECTS :", catalog.count())
    print("FIRST   :", catalog.all()[0].name)
