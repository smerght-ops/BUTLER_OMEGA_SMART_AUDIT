# -*- coding: utf-8 -*-

import json
from pathlib import Path

from engineering_agent import EngineeringAgent
from engineering_evidence import EngineeringEvidence
from engineering_evidence_collection import EngineeringEvidenceCollection


class RegistryReaderAgent(EngineeringAgent):
    """
    Stage 3.0

    Read Registry departments.

    Read-only.
    """

    NAME = "REGISTRY_READER"
    ROLE = "READER"
    SOURCE = "project_registry.json"

    def discover(self):

        registry = (
            Path(__file__).resolve().parents[3]
            / "A_07_CONFIG"
            / "project_registry.json"
        )

        data = json.loads(
            registry.read_text(encoding="utf-8-sig")
        )

        collection = EngineeringEvidenceCollection()

        for department in data.get("departments", []):

            collection.add(

                EngineeringEvidence(

                    source=self.SOURCE,

                    object_type="Department",

                    object_name=department.get("name", ""),

                    discovery_method="project_registry.json",

                    evidence=["Registry entry"],

                    confidence=100,

                    status="REGISTERED"

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
