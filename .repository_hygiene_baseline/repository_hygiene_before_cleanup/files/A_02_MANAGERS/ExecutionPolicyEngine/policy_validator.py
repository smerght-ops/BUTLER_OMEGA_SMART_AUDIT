# -*- coding: utf-8 -*-

"""
Stage 5.3

Execution Policy Validator

Foundation only.
"""

from A_02_MANAGERS.ExecutionPolicyEngine.policy_loader import PolicyLoader


class PolicyValidator:

    REQUIRED_CAPABILITIES = {
        "reasoning",
        "coding",
        "vision",
        "image_generation",
        "audio",
    }

    @staticmethod
    def validate(policy):

        errors = []

        if not policy.policy_name:
            errors.append("policy_name is empty")

        if policy.goal.capability not in PolicyValidator.REQUIRED_CAPABILITIES:
            errors.append(
                f"Unknown capability: {policy.goal.capability}"
            )

        if policy.constraints.max_latency_ms <= 0:
            errors.append(
                "max_latency_ms must be > 0"
            )

        return len(errors) == 0, errors


if __name__ == "__main__":

    policy = PolicyLoader.default_policy()

    ok, errors = PolicyValidator.validate(policy)

    print("VALID:", ok)

    if errors:
        for e in errors:
            print("-", e)
