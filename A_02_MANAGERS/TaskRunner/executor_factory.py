# -*- coding: utf-8 -*-

"""
Stage 6.9

Executor Factory

Adapter registry.
"""

from A_02_MANAGERS.TaskRunner.ExecutionAdapters.python_adapter import (
    PythonExecutionAdapter
)
from A_02_MANAGERS.TaskRunner.ExecutionAdapters.powershell_adapter import (
    PowerShellExecutionAdapter
)


class ExecutorFactory:

    _adapters = {}

    @classmethod
    def register(cls, adapter_class):

        engine = adapter_class.engine_name

        if not engine:

            raise ValueError("Adapter has no engine_name")

        cls._adapters[engine] = adapter_class()

    @classmethod
    def get(cls, engine_name):

        adapter = cls._adapters.get(engine_name)

        if adapter is None:

            raise ValueError(
                f"No execution adapter registered for engine: {engine_name}"
            )

        return adapter

    @classmethod
    def names(cls):

        return sorted(cls._adapters.keys())


ExecutorFactory.register(PythonExecutionAdapter)
ExecutorFactory.register(PowerShellExecutionAdapter)


if __name__ == "__main__":

    print("ADAPTERS:", ExecutorFactory.names())
