# -*- coding: utf-8 -*-

"""
Stage 5.1

Execution Policy Schema

Foundation only.
No runtime logic.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Goal:

    capability: str

    quality: str = "normal"


@dataclass
class Constraints:

    privacy: str = "local_preferred"

    max_cost: float = 0.0

    max_latency_ms: int = 5000

    allow_remote: bool = True


@dataclass
class Verification:

    level: int = 1

    self_check: bool = True


@dataclass
class Fallback:

    chain: List[str] = field(default_factory=list)

    strategy: str = "escalate"


@dataclass
class ExecutionPolicy:

    policy_name: str

    goal: Goal

    constraints: Constraints

    verification: Verification

    fallback: Fallback


if __name__ == "__main__":

    policy = ExecutionPolicy(

        policy_name="DEFAULT",

        goal=Goal("reasoning"),

        constraints=Constraints(),

        verification=Verification(),

        fallback=Fallback(["ollama","glm","claude"])

    )

    print(policy)

