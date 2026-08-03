# -*- coding: utf-8 -*-

import json
from pathlib import Path

from engineering_agent import EngineeringAgent
from engineering_evidence import EngineeringEvidence
from engineering_evidence_collection import EngineeringEvidenceCollection


class ExecutionRegistryDiscoveryAgent(EngineeringAgent):
    """
    PHASE 1.5

    Discover official Execution Registry information.

    Source:
        A_07_CONFIG/execution_registry.json

    Read-only.
    """

    NAME = "EXECUTION_REGISTRY_DISCOVERY"
    ROLE = "DISCOVERY"
    SOURCE = "execution_registry.json"

    def discover(self):

        registry = (
            Path(__file__).resolve().parents[3]
            / "A_07_CONFIG"
            / "execution_registry.json"
        )

        data = json.loads(
            registry.read_text(encoding="utf-8-sig")
        )

        collection = EngineeringEvidenceCollection()

        for key in sorted(data.keys()):

            collection.add(

                EngineeringEvidence(

                    source=self.SOURCE,

                    object_type="ExecutionRegistrySection",

                    object_name=key,

                    discovery_method="execution_registry.json",

                    evidence=[
                        "Execution Registry section discovered"
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

