from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

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
