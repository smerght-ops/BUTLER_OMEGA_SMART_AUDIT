# -*- coding: utf-8 -*-

"""
Stage 5.2

Execution Policy Loader

Foundation only.
No runtime decisions.
"""

from A_07_CONFIG.execution_policy_schema import (
    ExecutionPolicy,
    Goal,
    Constraints,
    Verification,
    Fallback,
)


class PolicyLoader:

    @staticmethod
    def default_policy():

        return ExecutionPolicy(

            policy_name="DEFAULT",

            goal=Goal("reasoning"),

            constraints=Constraints(),

            verification=Verification(),

            fallback=Fallback(
                chain=["ollama", "glm", "claude"]
            ),
        )


if __name__ == "__main__":

    policy = PolicyLoader.default_policy()

    print(policy.policy_name)
    print(policy.goal.capability)
    print(policy.constraints.privacy)
    print(policy.fallback.chain)
