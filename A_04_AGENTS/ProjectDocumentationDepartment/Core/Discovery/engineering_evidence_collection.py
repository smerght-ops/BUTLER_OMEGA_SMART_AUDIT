# -*- coding: utf-8 -*-

from typing import List

from engineering_evidence import EngineeringEvidence


class EngineeringEvidenceCollection:
    """
    Read-only collection of engineering evidence.

    Stores evidence discovered by
    PROJECT_DOCUMENTATION_DEPARTMENT agents.
    """

    def __init__(self):

        self.items: List[EngineeringEvidence] = []

    def add(self, evidence: EngineeringEvidence):

        self.items.append(evidence)

    def all(self):

        return self.items

    def count(self):

        return len(self.items)

    def by_source(self, source):

        return [
            e for e in self.items
            if e.source == source
        ]

    def by_artifact(self, artifact_name):

        return [
            e for e in self.items
            if e.object_name == artifact_name
        ]

