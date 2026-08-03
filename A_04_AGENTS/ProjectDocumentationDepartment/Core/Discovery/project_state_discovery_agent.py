# -*- coding: utf-8 -*-

from engineering_agent import EngineeringAgent
from engineering_evidence import EngineeringEvidence
from engineering_evidence_collection import EngineeringEvidenceCollection

from A_07_CONFIG.project_state import ProjectState


class ProjectStateDiscoveryAgent(EngineeringAgent):
    """
    PHASE 1.3

    Discover official Project State information.

    Read-only.
    """

    NAME = "PROJECT_STATE_DISCOVERY"
    ROLE = "DISCOVERY"
    SOURCE = "ProjectState"

    def discover(self):

        state = ProjectState()

        collection = EngineeringEvidenceCollection()

        for key in sorted(vars(state).keys()):

            collection.add(

                EngineeringEvidence(

                    source=self.SOURCE,

                    object_type="ProjectStateField",

                    object_name=key,

                    discovery_method="vars(ProjectState)",

                    evidence=[
                        "ProjectState field discovered"
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

