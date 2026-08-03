from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from A_04_AGENTS.PublicationGuardianDepartment.runner import PublicationGuardianDepartment

from .helpers import DEPARTMENT_ROOT, request


def git(root, *args, check=True):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=check)


class PublicationGuardianE2ETests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        git(self.root, "init")

    def tearDown(self):
        self.temporary.cleanup()

    def guardian(self):
        from A_04_AGENTS.PublicationGuardianDepartment.Core.engine import PublicationGuardianEngine
        return PublicationGuardianDepartment(PublicationGuardianEngine(DEPARTMENT_ROOT, self.root / "runtime"))

    def test_git_index_safe_publication_passes_end_to_end(self):
        (self.root / "README.md").write_text("safe\n", encoding="utf-8")
        git(self.root, "add", "README.md")
        raw = request(self.root, "e2e-safe", mode="git", staged_files=["README.md"])
        result = self.guardian().execute("проверить публикацию", {"publication_request": raw})
        publication = result["metadata"]["publication_result"]
        self.assertEqual("PASS", publication["status"])
        self.assertTrue(result["metadata"]["publication_allowed"])
        self.assertTrue(Path(publication["report"]["path"]).is_file())
        self.assertTrue((self.root / "runtime" / "audit.jsonl").is_file())

    def test_corrupt_git_index_fault_blocks_end_to_end(self):
        (self.root / ".git" / "index").write_bytes(b"corrupt-index")
        raw = request(self.root, "e2e-corrupt", mode="git")
        result = self.guardian().execute("проверить публикацию", {"publication_request": raw})
        publication = result["metadata"]["publication_result"]
        self.assertEqual("FAULT_BLOCK", publication["status"])
        self.assertFalse(result["metadata"]["publication_allowed"])


if __name__ == "__main__":
    unittest.main()
