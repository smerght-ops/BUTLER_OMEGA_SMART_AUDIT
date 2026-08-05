# -*- coding: utf-8 -*-

class EngineeringObject:
    """
    PHASE 0.1

    Universal engineering object.

    Every discoverable object inside
    BUTLER_OMEGA_SMART must be representable
    by this contract.
    """

    def __init__(self):

        self.object_id = ""

        self.name = ""

        self.object_type = ""

        self.status = ""

        self.parent = None

        self.children = []

        self.sources = []

        self.evidence = []

        self.first_seen = None

        self.last_seen = None

