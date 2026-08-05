# -*- coding: utf-8 -*-

from engineering_object_catalog import EngineeringObjectCatalog
from engineering_evidence_collection import EngineeringEvidenceCollection


class EvidenceConsolidation:
    """
    PHASE 5.4

    Attaches EngineeringEvidence to EngineeringObjects.
    """

    def consolidate(
        self,
        catalog: EngineeringObjectCatalog,
        evidence_collection: EngineeringEvidenceCollection
    ):

        grouped = {}

        for evidence in evidence_collection.all():

            grouped.setdefault(
                evidence.object_name,
                []
            ).append(evidence)

        for obj in catalog.all():

            obj.evidence = grouped.get(
                obj.name,
                []
            )

        return catalog


if __name__ == "__main__":

    from engineering_object import EngineeringObject
    from engineering_evidence import EngineeringEvidence

    catalog = EngineeringObjectCatalog()

    obj = EngineeringObject()
    obj.object_id = "ENG-000001"
    obj.name = "Passport"

    catalog.register(obj)

    collection = EngineeringEvidenceCollection()

    e1 = EngineeringEvidence()
    e1.object_name = "Passport"
    e1.source = "PASSPORT"

    e2 = EngineeringEvidence()
    e2.object_name = "Passport"
    e2.source = "LEDGER"

    collection.add(e1)
    collection.add(e2)

    consolidator = EvidenceConsolidation()

    result = consolidator.consolidate(
        catalog,
        collection
    )

    print("=== EVIDENCE CONSOLIDATION TEST ===")
    print()

    print("OBJECTS  :", result.count())
    print("EVIDENCE :", len(result.all()[0].evidence))
