# -*- coding: utf-8 -*-

import json
from pathlib import Path

from engineering_agent import EngineeringAgent
from engineering_evidence import EngineeringEvidence
from engineering_evidence_collection import EngineeringEvidenceCollection


class PassportDiscoveryAgent(EngineeringAgent):
    """
    PHASE 1.1

    Discover official Passport information.

    Source:
        A_07_CONFIG/project_passport.json

    Read-only.
    """

    NAME = "PASSPORT_DISCOVERY"
    ROLE = "DISCOVERY"
    SOURCE = "project_passport.json"

    def discover(self):

        passport = (
            Path(__file__).resolve().parents[3]
            / "A_07_CONFIG"
            / "project_passport.json"
        )

        data = json.loads(
            passport.read_text(encoding="utf-8-sig")
        )

        collection = EngineeringEvidenceCollection()

        for key in sorted(data.keys()):

            collection.add(

                EngineeringEvidence(

                    source=self.SOURCE,

                    object_type="PassportSection",

                    object_name=key,

                    discovery_method="project_passport.json",

                    evidence=[
                        "Passport section discovered"
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
