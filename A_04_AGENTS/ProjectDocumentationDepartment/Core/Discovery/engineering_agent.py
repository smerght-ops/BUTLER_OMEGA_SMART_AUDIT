# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class EngineeringAgent(ABC):
    """
    Base contract for every PROJECT_DOCUMENTATION_DEPARTMENT agent.

    The agent NEVER modifies the Butler project.

    Responsibilities:

    - discover
    - collect evidence
    - verify
    - report

    Read-only architecture.
    """

    NAME = "ENGINEERING_AGENT"
    ROLE = "BASE"
    SOURCE = "UNDEFINED"

    def __init__(self):

        self.confidence = 0
        self.evidence = []

    @abstractmethod
    def discover(self):
        pass

    @abstractmethod
    def collect_evidence(self):
        pass

    @abstractmethod
    def verify(self):
        pass

    @abstractmethod
    def report(self):
        pass
