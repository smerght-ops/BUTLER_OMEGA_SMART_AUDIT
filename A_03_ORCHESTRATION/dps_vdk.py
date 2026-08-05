# -*- coding: utf-8 -*-

class DPSVDK:

    def __init__(self):

        self.blocked_actions = {
            "DELETE_PROJECT",
            "FORMAT_DISK",
            "REMOVE_WORKSPACE"
        }

    def check(
        self,
        action
    ):

        if action in self.blocked_actions:

            return {
                "allowed": False,
                "reason": "BLOCKED_ACTION"
            }

        return {
            "allowed": True
        }
