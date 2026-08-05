# -*- coding: utf-8 -*-

"""
Stage 5.6

Execution Context

Unifies all execution inputs.
"""

from dataclasses import dataclass
from typing import Optional

from A_07_CONFIG.execution_policy_schema import ExecutionPolicy
from A_02_MANAGERS.RuntimeCapabilityRegistry.runtime_registry import (
    RuntimeCapabilityRegistry
)


@dataclass
class ExecutionContext:

    policy: ExecutionPolicy

    runtime: RuntimeCapabilityRegistry

    history: Optional[object] = None


if __name__ == "__main__":

    from A_02_MANAGERS.ExecutionPolicyEngine.policy_loader import (
        PolicyLoader
    )

    ctx = ExecutionContext(

        policy=PolicyLoader.default_policy(),

        runtime=RuntimeCapabilityRegistry

    )

    print(ctx.policy.policy_name)

    print(ctx.runtime.names())
