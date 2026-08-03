from __future__ import annotations

import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from A_04_AGENTS.PublicationGuardianDepartment.Checks import DEFAULT_INSPECTORS
from A_04_AGENTS.PublicationGuardianDepartment.Contracts.models import PublicationRequest

from .helpers import copy_policy, engine, request


class PublicationGuardianUnitTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_request_contract_rejects_missing_field(self):
        value = request(self.root)
        value.pop("initiator")
        with self.assertRaises(ValueError):
            PublicationRequest.from_dict(value)

    def test_safe_file_passes(self):
        path = self.root / "README.md"
        path.write_text("Safe documentation.\n", encoding="utf-8")
        result = engine(self.root).inspect(request(self.root, paths=[path]))
        self.assertEqual("PASS", result.status)

    def test_env_blocks(self):
        path = self.root / ".env"
        path.write_text("SAFE_PLACEHOLDER=true\n", encoding="utf-8")
        result = engine(self.root).inspect(request(self.root, paths=[path]))
        self.assertEqual("BLOCK", result.status)

    def test_api_key_blocks_and_is_masked(self):
        secret = "sk-proj-abcdefghijklmnopqrstuvwxyz123456"
        path = self.root / "code.txt"
        path.write_text(secret, encoding="utf-8")
        result = engine(self.root).inspect(request(self.root, paths=[path]))
        self.assertEqual("BLOCK", result.status)
        self.assertNotIn(secret, json.dumps(result.to_dict(), ensure_ascii=False))

    def test_private_key_blocks(self):
        path = self.root / "key.pem"
        path.write_text("-----BEGIN PRIVATE KEY-----\nabc\n", encoding="utf-8")
        self.assertEqual("BLOCK", engine(self.root).inspect(request(self.root, paths=[path])).status)

    def test_bearer_blocks(self):
        path = self.root / "header.txt"
        path.write_text("Authorization: Bearer abcdefghijklmnopqrstuvwxyz", encoding="utf-8")
        self.assertEqual("BLOCK", engine(self.root).inspect(request(self.root, paths=[path])).status)

    def test_allowed_binary_passes(self):
        path = self.root / "image.png"
        path.write_bytes(b"\x89PNG\x00\x01")
        self.assertEqual("PASS", engine(self.root).inspect(request(self.root, paths=[path])).status)

    def test_unknown_binary_warns(self):
        path = self.root / "object.xyzq"
        path.write_bytes(b"\x00\x01\x02")
        self.assertEqual("PASS_WITH_WARNINGS", engine(self.root).inspect(request(self.root, paths=[path])).status)

    def test_corrupt_policy_fault_blocks(self):
        policy = copy_policy(self.root)
        value = json.loads(policy.read_text(encoding="utf-8"))
        value["author"] = "tampered"
        policy.write_text(json.dumps(value), encoding="utf-8")
        path = self.root / "safe.txt"
        path.write_text("safe", encoding="utf-8")
        self.assertEqual("FAULT_BLOCK", engine(self.root, policy_path=policy).inspect(request(self.root, paths=[path])).status)

    def test_unavailable_required_inspector_fault_blocks(self):
        without_secrets = tuple(kind for kind in DEFAULT_INSPECTORS if kind.inspector_id != "secrets")
        path = self.root / "safe.txt"
        path.write_text("safe", encoding="utf-8")
        self.assertEqual("FAULT_BLOCK", engine(self.root, inspector_types=without_secrets).inspect(request(self.root, paths=[path])).status)

    def test_incremental_cache_is_used(self):
        path = self.root / "safe.txt"
        path.write_text("safe", encoding="utf-8")
        guardian = engine(self.root)
        guardian.inspect(request(self.root, "cache-1", paths=[path]))
        second = guardian.inspect(request(self.root, "cache-2", paths=[path]))
        cacheable = [item for item in second.inspectors if item["inspector_id"] in {"configuration", "secrets", "privacy", "binary"}]
        self.assertTrue(all(item["status"] == "CACHED" for item in cacheable))


    def test_cache_cannot_bypass_path_sensitive_inspector(self):
        safe = self.root / "safe.txt"
        dangerous = self.root / ".env"
        safe.write_text("same bytes", encoding="utf-8")
        dangerous.write_text("same bytes", encoding="utf-8")
        guardian = engine(self.root)
        self.assertEqual("PASS", guardian.inspect(request(self.root, "cache-safe", paths=[safe])).status)
        self.assertEqual("BLOCK", guardian.inspect(request(self.root, "cache-danger", paths=[dangerous])).status)

    def test_file_mode_rejects_object_outside_repository_root(self):
        outside = self.root.parent / f"outside-{self.root.name}.txt"
        outside.write_text("safe", encoding="utf-8")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        result = engine(self.root).inspect(request(self.root, "outside", paths=[outside]))
        self.assertEqual("FAULT_BLOCK", result.status)

    def test_archive_member_traversal_fault_blocks(self):
        archive = self.root / "unsafe.zip"
        with zipfile.ZipFile(archive, "w") as stream:
            stream.writestr("../escape.txt", "safe")
        result = engine(self.root).inspect(request(self.root, "archive", mode="zip", paths=[archive]))
        self.assertEqual("FAULT_BLOCK", result.status)

    def test_executable_disguised_as_allowed_image_blocks(self):
        path = self.root / "photo.png"
        path.write_bytes(b"MZ" + b"\x00" * 32)
        self.assertEqual("BLOCK", engine(self.root).inspect(request(self.root, paths=[path])).status)

    def test_empty_git_publication_fault_blocks(self):
        import subprocess
        subprocess.run(["git", "-C", str(self.root), "init"], check=True, capture_output=True)
        result = engine(self.root).inspect(request(self.root, mode="git"))
        self.assertEqual("FAULT_BLOCK", result.status)


if __name__ == "__main__":
    unittest.main()
