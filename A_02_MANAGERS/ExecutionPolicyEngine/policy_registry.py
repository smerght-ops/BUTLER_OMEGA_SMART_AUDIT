# -*- coding: utf-8 -*-

"""
Stage 5.4

Execution Policy Registry

Foundation only.
"""

from A_02_MANAGERS.ExecutionPolicyEngine.policy_loader import PolicyLoader


class PolicyRegistry:

    _registry = {}

    @classmethod
    def register(cls, policy):

        cls._registry[policy.policy_name] = policy

    @classmethod
    def get(cls, name):

        return cls._registry.get(name)

    @classmethod
    def exists(cls, name):

        return name in cls._registry

    @classmethod
    def names(cls):

        return sorted(cls._registry.keys())


if __name__ == "__main__":

    PolicyRegistry.register(
        PolicyLoader.default_policy()
    )

    print("REGISTERED:", PolicyRegistry.names())

    policy = PolicyRegistry.get("DEFAULT")

    print(policy.policy_name)
    print(policy.goal.capability)
