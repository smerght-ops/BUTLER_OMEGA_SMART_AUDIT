from __future__ import annotations

import unittest
import sys
import types
import tempfile
from pathlib import Path


class _DependencyStub:
    def __init__(self, *args, **kwargs):
        pass


def _stub(module_name, **symbols):
    module = types.ModuleType(module_name)
    for name, value in symbols.items():
        setattr(module, name, value)
    sys.modules[module_name] = module


# These contract tests exercise SmartDispatcherV2's guardian gate only. Stub
# unrelated heavyweight departments so a missing optional package cannot hide
# a security regression in this integration boundary.
for module_name, symbol in (
    ("A_04_AGENTS.CodingDepartment.runner", "CodingDepartment"),
    ("A_04_AGENTS.MemoryDepartment.runner", "MemoryDepartment"),
    ("A_04_AGENTS.VisionDepartment.runner", "VisionDepartment"),
    ("A_04_AGENTS.ImageDepartment.runner", "ImageDepartment"),
    ("A_04_AGENTS.AudioDepartment.runner", "AudioDepartment"),
    ("A_04_AGENTS.TextDepartment.runner", "TextDepartment"),
    ("A_04_AGENTS.VideoDepartment.runner", "VideoDepartment"),
    ("A_04_AGENTS.ArchiveDepartment.runner", "ArchiveDepartment"),
    ("A_04_AGENTS.FilesystemDepartment.runner", "FilesystemDepartment"),
    ("A_04_AGENTS.SearchDepartment.runner", "SearchDepartment"),
    ("A_04_AGENTS.DocumentsDepartment.runner", "DocumentsDepartment"),
    ("A_04_AGENTS.OpenDocumentDepartment.runner", "OpenDocumentDepartment"),
    ("A_04_AGENTS.ProjectDocumentationDepartment.runner", "ProjectDocumentationDepartment"),
    ("A_04_AGENTS.HomeDepartment.runner", "HomeDepartment"),
    ("A_04_AGENTS.BrowserDepartment.runner", "BrowserDepartment"),
    ("A_07_MEMORY.semantic_memory", "SemanticMemory"),
    ("A_07_MEMORY.semantic_reasoning_engine", "SemanticReasoningEngine"),
    ("A_03_ORCHESTRATION.butler_harness", "ButlerHarness"),
    ("A_02_MANAGERS.smart_dispatcher", "SmartDispatcher"),
    ("A_02_MANAGERS.goal_manager", "GoalManager"),
    ("A_07_MEMORY.memory_orchestrator_v2", "MemoryOrchestratorV2"),
    ("A_01_CORE.TaskExecutor.task_executor", "TaskExecutor"),
):
    _stub(module_name, **{symbol: _DependencyStub})

_stub("A_03_ENGINES.Audio_Engine.whisper_engine", create_audio_engine=lambda: _DependencyStub())

from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2
from A_04_AGENTS.PublicationGuardianDepartment.Core.engine import PublicationGuardianEngine
from A_04_AGENTS.PublicationGuardianDepartment.runner import PublicationGuardianDepartment
from A_04_AGENTS.PublicationGuardianDepartment.Tests.helpers import DEPARTMENT_ROOT, request


class _Guardian:
    NAME = "PUBLICATION_GUARDIAN"


class SmartDispatcherPublicationGuardianTests(unittest.TestCase):
    def dispatcher(self, response=None, departments=None):
        dispatcher = SmartDispatcherV2.__new__(SmartDispatcherV2)
        dispatcher.departments = [_Guardian()] if departments is None else departments
        dispatcher._execute_department = lambda dept, query, context=None: response
        return dispatcher

    @staticmethod
    def response(status):
        allowed = status in {"PASS", "PASS_WITH_WARNINGS"}
        return {
            "ok": allowed,
            "department": "PUBLICATION_GUARDIAN",
            "metadata": {
                "publication_allowed": allowed,
                "publication_result": {"api_version": "v1", "status": status},
            },
        }

    def test_publication_request_routes_directly_to_guardian(self):
        dispatcher = self.dispatcher(self.response("PASS"))
        result = dispatcher.dispatch("publish", {"publication_request": {"request_id": "one"}})
        self.assertEqual("PASS", result["metadata"]["publication_result"]["status"])
        self.assertTrue(result["metadata"]["publication_allowed"])

    def test_block_is_preserved(self):
        dispatcher = self.dispatcher(self.response("BLOCK"))
        result = dispatcher.dispatch("publish", {"publication_request": {"request_id": "two"}})
        self.assertFalse(result["ok"])
        self.assertFalse(result["metadata"]["publication_allowed"])

    def test_missing_guardian_fault_blocks(self):
        dispatcher = self.dispatcher(self.response("PASS"), departments=[])
        result = dispatcher.dispatch("publish", {"publication_request": {"request_id": "three"}})
        self.assertEqual("FAULT_BLOCK", result["metadata"]["publication_result"]["status"])
        self.assertFalse(result["metadata"]["publication_allowed"])

    def test_malformed_guardian_response_fault_blocks(self):
        dispatcher = self.dispatcher({"ok": True, "metadata": {}})
        result = dispatcher.dispatch("publish", {"publication_request": {"request_id": "four"}})
        self.assertEqual("FAULT_BLOCK", result["metadata"]["publication_result"]["status"])

    def test_contract_mismatch_fault_blocks(self):
        response = self.response("BLOCK")
        response["ok"] = True
        dispatcher = self.dispatcher(response)
        result = dispatcher.dispatch("publish", {"publication_request": {"request_id": "five"}})
        self.assertEqual("FAULT_BLOCK", result["metadata"]["publication_result"]["status"])

    def test_real_guardian_executes_end_to_end_through_dispatcher(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "README.md"
            source.write_text("safe", encoding="utf-8")
            guardian = PublicationGuardianDepartment(
                PublicationGuardianEngine(DEPARTMENT_ROOT, root / "runtime")
            )
            dispatcher = SmartDispatcherV2.__new__(SmartDispatcherV2)
            dispatcher.departments = [guardian]
            dispatcher._execute_department = lambda dept, query, context=None: dept.execute(
                query, context=context
            )
            result = dispatcher.dispatch(
                "publish",
                {"publication_request": request(root, "dispatcher-real-e2e", paths=[source])},
            )
            publication = result["metadata"]["publication_result"]
            self.assertEqual("PASS", publication["status"])
            self.assertTrue(Path(publication["report"]["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
