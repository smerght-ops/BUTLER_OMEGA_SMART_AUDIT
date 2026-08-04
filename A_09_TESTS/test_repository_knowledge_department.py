import json
from pathlib import Path
import tempfile
import unittest

from A_04_AGENTS.RepositoryKnowledgeDepartment.loaders import (
    InventoryLoader, ManifestLoader, ScopeResolver,
)
from A_04_AGENTS.RepositoryKnowledgeDepartment.runner import RepositoryKnowledgeDepartment
from A_04_AGENTS.RepositoryKnowledgeDepartment.scanner import RepositoryScanner
from A_04_AGENTS.RepositoryKnowledgeDepartment.service import RepositoryKnowledgeService


class RecordingObservation:
    def __init__(self): self.rows = []
    def record(self, source, event, payload=None): self.rows.append((source, event, payload))


class RepositoryKnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "PROJECT_SCOPE.yaml").write_text(
            "metadata:\n  scope_version: '1.0'\n"
            "production:\n  - name: src\nengineering: []\nworkspace: []\nlaboratory: []\n"
            "archive: []\ngenerated: []\nignore: []\nreview_required: []\n"
            "classification_rules: []\naudit_policy: {}\nfuture_consumers: []\n",
            encoding="utf-8",
        )
        (self.root / "system_manifest.json").write_text(
            json.dumps({"version": "1.0", "paths": {"core": "src"}}), encoding="utf-8"
        )
        (self.root / "A_00_ARCHITECTURE").mkdir()
        (self.root / "A_00_ARCHITECTURE/RECONSTRUCTION_INVENTORY.json").write_text(
            json.dumps({"schema_version": 1, "components": []}), encoding="utf-8"
        )
        (self.root / "src").mkdir()
        (self.root / "src/base.py").write_text(
            "class Base:\n    pass\n", encoding="utf-8"
        )
        (self.root / "src/department.py").write_text(
            "from src.base import Base\n\nclass DemoDepartment(Base):\n"
            "    def execute(self, query):\n        return query\n",
            encoding="utf-8",
        )
        self.observation = RecordingObservation()
        self.service = RepositoryKnowledgeService(self.root, self.observation)

    def tearDown(self): self.temporary.cleanup()

    def test_source_loaders(self):
        scope, scope_diagnostic = ScopeResolver().load(self.root)
        self.assertEqual(scope_diagnostic.status, "OK")
        self.assertEqual(scope["categories"]["production"], ["src"])
        self.assertEqual(ManifestLoader().load(self.root)[1].status, "OK")
        self.assertEqual(InventoryLoader().load(self.root)[1].status, "OK")

    def test_degraded_loaders_do_not_raise(self):
        empty = self.root / "empty"
        empty.mkdir()
        self.assertEqual(ScopeResolver().load(empty)[1].status, "DEGRADED")
        self.assertEqual(ManifestLoader().load(empty)[1].status, "DEGRADED")
        self.assertEqual(InventoryLoader().load(empty)[1].status, "DEGRADED")

    def test_scanner_is_deterministic_and_scope_driven(self):
        scope = ScopeResolver().load(self.root)[0]
        first = RepositoryScanner(self.root, scope).scan()[0]
        second = RepositoryScanner(self.root, scope).scan()[0]
        self.assertEqual([item.relative_path for item in first], [item.relative_path for item in second])
        target = next(item for item in first if item.relative_path == "src/department.py")
        self.assertEqual(target.category, "production")
        self.assertTrue(any(item["name"] == "DemoDepartment" for item in target.symbols))
        self.assertIn("mtime_ns", target.metadata)
        self.assertEqual(target.metadata["size"], target.size)

    def test_scanner_excludes_archive_restore_backup_and_symlink(self):
        for name in ("legacy", "restore", "BACKUP_one"):
            (self.root / name).mkdir()
            (self.root / name / "hidden.py").write_text("x = 1", encoding="utf-8")
        text = (self.root / "PROJECT_SCOPE.yaml").read_text(encoding="utf-8")
        text = text.replace("archive: []", "archive: [legacy, restore, 'BACKUP_*']")
        (self.root / "PROJECT_SCOPE.yaml").write_text(text, encoding="utf-8")
        scope = ScopeResolver().load(self.root)[0]
        paths = [item.relative_path for item in RepositoryScanner(self.root, scope).scan()[0]]
        assert not any("hidden.py" in path for path in paths)

    def test_index_build_refresh_and_cache(self):
        built = self.service.build_index()
        self.assertTrue(built["success"])
        initial = self.service.cache.get()
        query = self.service.find_class("DemoDepartment")
        self.assertEqual(query["index_version"], initial.index_version)
        self.assertTrue(query["data"]["matches"])
        self.assertIs(self.service.cache.get(), initial)
        refreshed = self.service.refresh_index()
        self.assertTrue(refreshed["success"])
        self.assertIsNot(self.service.cache.get(), initial)

    def test_graphs_duplicates_and_report(self):
        self.service.build_index()
        project = self.service.build_project_graph()
        dependency = self.service.build_dependency_graph()
        runtime = self.service.build_runtime_graph()
        self.assertTrue(project["data"]["nodes"])
        self.assertIn("imports", dependency["data"]["edge_types"])
        self.assertIn("permission", runtime["data"]["edge_types"])
        self.assertIsInstance(self.service.find_duplicates()["data"], list)
        report = self.service.build_architecture_report()
        self.assertTrue(report["success"])
        self.assertIn("architecture_health", report["data"])

    def test_department_contract_and_observation(self):
        department = RepositoryKnowledgeDepartment(self.root, self.observation)
        self.assertTrue(department.can_handle("покажи индекс репозитория"))
        result = department.execute(
            "DemoDepartment",
            context={"repository_knowledge": True, "repository_operation": "find_class", "repository_value": "DemoDepartment"},
        )
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["department"], "REPOSITORY_KNOWLEDGE")
        self.assertTrue(result["metadata"]["repository_knowledge"]["data"]["matches"])
        events = [row[1] for row in self.observation.rows]
        self.assertIn("INDEX_COLD_BUILD", events)
        self.assertIn("QUERY_EXECUTION", events)

    def test_dispatcher_harness_gateway_permission_integration(self):
        from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway

        class Harness:
            calls = 0
            def execute(inner_self, department_name, task, executor, **kwargs):
                inner_self.calls += 1
                value = executor()
                return {"committed": True, "commit_result": value}

        department = RepositoryKnowledgeDepartment(self.root, self.observation)
        gateway = DepartmentExecutionGateway(observation=self.observation)
        harness = Harness()
        harness_result = harness.execute(
            "REPOSITORY_KNOWLEDGE",
            "find class",
            executor=lambda: gateway.execute(
                department,
                "DemoDepartment",
                context={"repository_knowledge": True, "repository_operation": "find_class", "repository_value": "DemoDepartment"},
            ),
        )
        result = harness_result["commit_result"]
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["department"], "REPOSITORY_KNOWLEDGE")
        self.assertEqual(harness.calls, 1)
        events = [row[1] for row in self.observation.rows]
        self.assertIn("PERMISSION_DECISION_STAGE1", events)


if __name__ == "__main__":
    unittest.main()
