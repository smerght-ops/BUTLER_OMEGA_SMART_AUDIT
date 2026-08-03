import tempfile
import unittest
from pathlib import Path

from PIL import Image

from A_01_CORE.TaskExecutor.capability_executor import CapabilityExecutor
from A_01_CORE.TaskExecutor.execution_context import ArtifactReference, ExecutionContext
from A_04_AGENTS.FilesystemDepartment.runner import FilesystemDepartment


class Stage5BArtifactAddressingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        self.filesystem = FilesystemDepartment()
        self.filesystem.workspace_root = self.root
        self.filesystem.allowed_roots = (self.root,)
        self.executor = CapabilityExecutor()
        self.executor._departments["FILESYSTEM"] = self.filesystem

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def step(order, action, arguments, output, kind):
        capability_ids = {
            "create_folder": "filesystem_create_folder_folder",
            "save_text": "filesystem_save_text_text",
            "save_image": "filesystem_save_image_image",
        }
        return {
            "order": order,
            "department": "FILESYSTEM",
            "action": action,
            "capability_id": capability_ids[action],
            "status": "planned",
            "arguments": dict(arguments, artifact_id=output),
            "artifacts": {"output": output, "type": kind},
        }

    def execute_project(self, name, child, filename, content):
        plan = {"steps": [
            self.step(1, "create_folder", {"folder_name": name, "location": "workspace"}, "project_root", "directory_path"),
            self.step(2, "create_folder", {"folder_name": child, "parent_folder": "{{step_1.output}}"}, "content_folder", "directory_path"),
            self.step(3, "save_text", {"folder": "{{step_2.output}}", "filename": filename, "content": content}, "content_file", "file_path"),
        ]}
        result = self.executor.execute(plan, ExecutionContext())
        self.assertTrue(result["ok"], result)
        reference = result["metadata"]["results"]["step_2"]["output"]
        self.assertIsInstance(reference, ArtifactReference)
        self.assertEqual("content_folder", reference.artifact_id)
        self.assertTrue((self.root / name / child / filename).is_file())
        return result

    def test_three_projects_use_the_same_addressing_mechanism(self):
        cases = (
            ("PoetryProject", "Texts", "poem.txt", "sea poem"),
            ("ReportProject", "Reports", "report.txt", "quarterly report"),
            ("PhotoArchive", "Descriptions", "index.txt", "photo index"),
        )
        for case in cases:
            with self.subTest(project=case[0]):
                self.execute_project(*case)

    def test_image_can_be_saved_to_referenced_child_folder(self):
        source = self.root / "source.png"
        Image.new("RGB", (4, 4), "red").save(source)
        plan = {"steps": [
            self.step(1, "create_folder", {"folder_name": "PhotoArchive", "location": "workspace"}, "project_root", "directory_path"),
            self.step(2, "create_folder", {"folder_name": "Images", "parent_folder": "{{step_1.output}}"}, "images", "directory_path"),
            self.step(3, "save_image", {"folder": "{{step_2.output}}", "filename": "photo.png", "source": str(source)}, "photo", "image"),
        ]}
        result = self.executor.execute(plan, ExecutionContext())
        self.assertTrue(result["ok"], result)
        self.assertTrue((self.root / "PhotoArchive" / "Images" / "photo.png").is_file())

    def test_snapshot_exposes_logical_reference_not_locator(self):
        context = ExecutionContext()
        reference = ArtifactReference("project_root", "directory", str(self.root / "Project"))
        context.record(1, {"artifacts": {"output": "project_root", "type": "directory_path"}}, {"ok": True, "department": "FILESYSTEM", "error": None}, reference)
        snapshot = context.snapshot()
        self.assertEqual({"artifact_ref": "project_root", "kind": "directory"}, snapshot["results"]["step_1"]["output"])
        self.assertNotIn(str(self.root), str(snapshot))


if __name__ == "__main__":
    unittest.main()
