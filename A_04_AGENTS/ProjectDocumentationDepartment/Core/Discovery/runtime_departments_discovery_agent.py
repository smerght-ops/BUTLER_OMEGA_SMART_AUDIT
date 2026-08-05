# -*- coding: utf-8 -*-

from engineering_agent import EngineeringAgent
from engineering_evidence import EngineeringEvidence
from engineering_evidence_collection import EngineeringEvidenceCollection

from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2


class RuntimeDepartmentsDiscoveryAgent(EngineeringAgent):
    """
    Stage 2.1

    Discover Runtime Departments
    from the official Runtime source.
    """

    NAME = "RUNTIME_DEPARTMENTS_DISCOVERY"
    ROLE = "DISCOVERY"
    SOURCE = "SmartDispatcherV2"

    def discover(self):

        dispatcher = SmartDispatcherV2()

        collection = EngineeringEvidenceCollection()

        for dept in dispatcher.departments:

            collection.add(

                EngineeringEvidence(

                    source=self.SOURCE,

                    object_type="Department",

                    object_name=type(dept).__name__,

                    discovery_method="dispatcher.departments",

                    evidence=[
                        "Runtime registration"
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
            "role": self.ROLE,
            "source": self.SOURCE
        }
