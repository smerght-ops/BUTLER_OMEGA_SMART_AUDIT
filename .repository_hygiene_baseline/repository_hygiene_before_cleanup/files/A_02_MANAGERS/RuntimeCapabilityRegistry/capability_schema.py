# -*- coding: utf-8 -*-

"""
Stage 5.5.1

Runtime Capability Schema

Foundation only.
"""

from dataclasses import dataclass, field
from typing import List
from datetime import datetime


@dataclass
class RuntimeCapability:

    capability: str

    available: bool = False

    providers: List[str] = field(default_factory=list)

    latency_ms: int = 0

    quality: str = "unknown"

    last_seen: str = ""

    metadata: dict = field(default_factory=dict)


if __name__ == "__main__":

    cap = RuntimeCapability(
        capability="reasoning",
        available=True,
        providers=["ollama"],
        latency_ms=120,
        quality="good",
        last_seen=datetime.now().isoformat()
    )

    print(cap)
