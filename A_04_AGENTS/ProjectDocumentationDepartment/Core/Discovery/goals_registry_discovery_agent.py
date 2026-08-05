# -*- coding: utf-8 -*-

import json
from pathlib import Path

from engineering_agent import EngineeringAgent
from engineering_evidence import EngineeringEvidence
from engineering_evidence_collection import EngineeringEvidenceCollection


class GoalsRegistryDiscoveryAgent(EngineeringAgent):
    """
    PHASE 1.4

    Discover official Goals Registry information.

    Source:
        A_07_CONFIG/goals_registry.json

    Read-only.
    """

    NAME = "GOALS_REGISTRY_DISCOVERY"
    ROLE = "DISCOVERY"
    SOURCE = "goals_registry.json"

    def discover(self):

        goals = (
            Path(__file__).resolve().parents[3]
            / "A_07_CONFIG"
            / "goals_registry.json"
        )

        data = json.loads(
            goals.read_text(encoding="utf-8-sig")
        )

        collection = EngineeringEvidenceCollection()

        for key in sorted(data.keys()):

            collection.add(

                EngineeringEvidence(

                    source=self.SOURCE,

                    object_type="GoalsRegistrySection",

                    object_name=key,

                    discovery_method="goals_registry.json",

                    evidence=[
                        "Goals Registry section discovered"
                    ],

                    confidence=100,

                    status="DISCOVERED"

                )

            )

        return collection

    def collect_evidence(self):
        return self.discover()

    def verify(self):
        return True

    def report(self):
        return {
            "agent": self.NAME,
            "source": self.SOURCE
        }
