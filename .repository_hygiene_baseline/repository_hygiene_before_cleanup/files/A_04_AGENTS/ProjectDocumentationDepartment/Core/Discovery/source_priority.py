# -*- coding: utf-8 -*-

from engineering_evidence_collection import EngineeringEvidenceCollection


class SourcePriority:
    """
    PHASE 5.3

    Selects the highest-priority EngineeringEvidence
    for every engineering object.
    """

    PRIORITY = {
        "PASSPORT": 100,
        "REGISTRY": 90,
        "PROJECT_STATE": 80,
        "GOALS": 70,
        "EXECUTION": 60,
        "LEDGER": 50,
        "HISTORY": 40,
        "REPORT": 30,
        "OBSERVATION": 20,
        "RUNTIME": 10,
    }

    def resolve(self, collection: EngineeringEvidenceCollection):

        selected = {}

        for evidence in collection.all():

            key = evidence.object_name

            score = self.PRIORITY.get(
                evidence.source.upper(),
                0
            )

            if key not in selected:
                selected[key] = (score, evidence)
                continue

            if score > selected[key][0]:
                selected[key] = (score, evidence)

        result = EngineeringEvidenceCollection()

        for _, evidence in selected.values():
            result.add(evidence)

        return result


if __name__ == "__main__":

    from engineering_evidence import EngineeringEvidence

    collection = EngineeringEvidenceCollection()

    e1 = EngineeringEvidence()
    e1.object_name = "Passport"
    e1.source = "HISTORY"

    e2 = EngineeringEvidence()
    e2.object_name = "Passport"
    e2.source = "PASSPORT"

    collection.add(e1)
    collection.add(e2)

    resolver = SourcePriority()

    result = resolver.resolve(collection)

    print("=== SOURCE PRIORITY TEST ===")
    print()

    print("OBJECTS :", result.count())
    print("SOURCE  :", result.all()[0].source)
