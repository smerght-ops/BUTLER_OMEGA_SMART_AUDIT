# -*- coding: utf-8 -*-
"""Runtime-only trace for the real BUTLER_OS entry point; no production edits."""
import inspect
import json
import time
from pathlib import Path

import BUTLER_OS
import A_03_ORCHESTRATION.dispatcher_bridge_v2 as bridge
import A_04_AGENTS.DocumentsDepartment.runner as documents_module

LOG = Path(__file__).with_name("trace_documents_runtime.jsonl")


def emit(event, **data):
    record = {"time": time.time(), "event": event, **data}
    with LOG.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


LOG.write_text("", encoding="utf-8")
dispatcher = bridge._dispatcher
emit(
    "bootstrap",
    butler_os_file=inspect.getfile(BUTLER_OS),
    bridge_file=inspect.getfile(bridge),
    dispatcher_class_file=inspect.getfile(type(dispatcher)),
    documents_module_file=documents_module.__file__,
    documents_class_file=inspect.getfile(documents_module.DocumentsDepartment),
    dispatcher_id=id(dispatcher),
    departments=[{
        "index": index,
        "id": id(department),
        "class": type(department).__qualname__,
        "module": type(department).__module__,
        "class_file": inspect.getfile(type(department)),
        "name": dispatcher._dept_name(department),
    } for index, department in enumerate(dispatcher.departments)],
)

original_plan = BUTLER_OS._task_planner.plan
def traced_plan(query):
    result = original_plan(query)
    emit("task_plan", query=query, plan=result)
    return result
BUTLER_OS._task_planner.plan = traced_plan

original_capability_execute = BUTLER_OS._capability_executor.execute
def traced_capability_execute(plan):
    emit("capability_execute_enter", plan=plan)
    result = original_capability_execute(plan)
    emit("capability_execute_exit", result=result)
    return result
BUTLER_OS._capability_executor.execute = traced_capability_execute

original_dispatch = dispatcher.dispatch
def traced_dispatch(query, context=None):
    emit("dispatcher_enter", query=query, context=context)
    result = original_dispatch(query, context)
    emit("dispatcher_exit", query=query, result=result)
    return result
dispatcher.dispatch = traced_dispatch

DocumentsDepartment = documents_module.DocumentsDepartment
original_can_handle = DocumentsDepartment.can_handle
def traced_can_handle(self, query, context=None):
    result = original_can_handle(self, query, context=context)
    emit(
        "documents_can_handle",
        instance_id=id(self), query=query, result=result,
        method_file=inspect.getfile(original_can_handle),
        method_first_line=original_can_handle.__code__.co_firstlineno,
    )
    return result
DocumentsDepartment.can_handle = traced_can_handle

original_execute = DocumentsDepartment.execute
def traced_execute(self, query, context=None):
    emit(
        "documents_execute_enter",
        instance_id=id(self), query=query,
        method_file=inspect.getfile(original_execute),
        caller=[f"{frame.filename}:{frame.lineno}:{frame.function}" for frame in inspect.stack()[1:7]],
    )
    result = original_execute(self, query, context=context)
    emit("documents_execute_exit", instance_id=id(self), result=result)
    return result
DocumentsDepartment.execute = traced_execute

emit("instrumentation_ready")
BUTLER_OS.main()
