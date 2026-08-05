# -*- coding: utf-8 -*-

"""
Stage 5.7

Runtime Capability Registry
"""

from A_02_MANAGERS.RuntimeCapabilityRegistry.capability_schema import RuntimeCapability


class RuntimeCapabilityRegistry:

    _capabilities = {}

    @classmethod
    def register(cls, capability: RuntimeCapability):
        cls._capabilities[capability.capability] = capability

    @classmethod
    def get(cls, name):
        return cls._capabilities.get(name)

    @classmethod
    def exists(cls, name):
        return name in cls._capabilities

    @classmethod
    def names(cls):
        return sorted(cls._capabilities.keys())

    @classmethod
    def all(cls):
        return dict(cls._capabilities)

    @classmethod
    def snapshot(cls):

        return {
            name: {
                "available": cap.available,
                "providers": list(cap.providers),
                "latency_ms": cap.latency_ms,
                "quality": cap.quality,
                "last_seen": cap.last_seen,
            }
            for name, cap in cls._capabilities.items()
        }


if __name__ == "__main__":

    RuntimeCapabilityRegistry.register(

        RuntimeCapability(

            capability="reasoning",

            available=True,

            providers=["ollama"],

            latency_ms=120,

            quality="good"

        )

    )

    print(RuntimeCapabilityRegistry.names())

    print(RuntimeCapabilityRegistry.get("reasoning"))

    print()

    print("SNAPSHOT")

    print(RuntimeCapabilityRegistry.snapshot())
