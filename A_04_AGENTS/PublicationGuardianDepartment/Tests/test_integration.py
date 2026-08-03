import tempfile
import unittest
from pathlib import Path

from A_04_AGENTS.PublicationGuardianDepartment.Core.engine import PublicationGuardianEngine
from A_04_AGENTS.PublicationGuardianDepartment.runner import PublicationGuardianDepartment

from .helpers import DEPARTMENT_ROOT, request


class PublicationGuardianLocalIntegrationTests(unittest.TestCase):
    def test_runner_and_engine_contract(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "safe.txt"
            source.write_text("safe", encoding="utf-8")
            department = PublicationGuardianDepartment(
                PublicationGuardianEngine(DEPARTMENT_ROOT, root / "runtime")
            )
            result = department.execute(
                "проверить публикацию",
                {"publication_request": request(root, "local-integration", paths=[source])},
            )
            self.assertTrue(result["ok"])
            self.assertEqual("PASS", result["metadata"]["publication_result"]["status"])
            self.assertTrue(result["metadata"]["publication_allowed"])

    def test_route_contract_is_explicit(self):
        department = PublicationGuardianDepartment()
        self.assertTrue(department.can_handle("проверить публикацию"))
        self.assertFalse(department.can_handle("обычный разговор"))


    def test_block_is_not_reported_as_generic_success(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / ".env"
            source.write_text("placeholder=true", encoding="utf-8")
            department = PublicationGuardianDepartment(
                PublicationGuardianEngine(DEPARTMENT_ROOT, root / "runtime")
            )
            result = department.execute(
                "inspect publication",
                {"publication_request": request(root, "blocked-integration", paths=[source])},
            )
            self.assertFalse(result["ok"])
            self.assertFalse(result["metadata"]["publication_allowed"])


if __name__ == "__main__":
    unittest.main()
