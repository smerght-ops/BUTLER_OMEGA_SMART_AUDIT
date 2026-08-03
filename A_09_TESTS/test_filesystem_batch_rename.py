import tempfile
import unittest
from pathlib import Path

from A_04_AGENTS.FilesystemDepartment.runner import FilesystemDepartment


class FilesystemBatchRenameTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        self.department = FilesystemDepartment()
        self.department.allowed_roots = (self.root,)

    def tearDown(self):
        self.temporary.cleanup()

    def folder(self, name="Photos"):
        path = self.root / name
        path.mkdir()
        return path

    def rename(self, folder, pattern):
        query = f'Переименуй файлы в папке "{folder}" в формат "{pattern}"'
        return self.department.execute(query)

    def test_number_format_and_stable_name_order(self):
        folder = self.folder()
        for name in ("zeta.jpg", "Alpha.jpg", "beta.jpg"):
            (folder / name).write_bytes(name.encode())
        result = self.rename(folder, "Photo_{n:03d}.jpg")
        self.assertTrue(result["ok"], result)
        self.assertEqual(["Photo_001.jpg", "Photo_002.jpg", "Photo_003.jpg"], sorted(p.name for p in folder.iterdir()))
        self.assertEqual(
            [("Alpha.jpg", "Photo_001.jpg"), ("beta.jpg", "Photo_002.jpg"), ("zeta.jpg", "Photo_003.jpg")],
            [(item["old_name"], item["new_name"]) for item in result["metadata"]["renamed"]],
        )

    def test_explicit_extension_filters_other_files(self):
        folder = self.folder()
        (folder / "a.jpg").write_bytes(b"jpg")
        (folder / "keep.png").write_bytes(b"png")
        result = self.rename(folder, "Photo_{n:03d}.jpg")
        self.assertTrue(result["ok"])
        self.assertEqual({"Photo_001.jpg", "keep.png"}, {p.name for p in folder.iterdir()})

    def test_pattern_without_extension_preserves_extensions(self):
        folder = self.folder()
        (folder / "a.jpg").write_bytes(b"jpg")
        (folder / "b.png").write_bytes(b"png")
        (folder / "Nested").mkdir()
        result = self.rename(folder, "Document_{n:03d}")
        self.assertTrue(result["ok"])
        self.assertEqual({"Document_001.jpg", "Document_002.png", "Nested"}, {p.name for p in folder.iterdir()})

    def test_empty_folder_is_success_with_zero(self):
        folder = self.folder()
        result = self.rename(folder, "Photo_{n}.jpg")
        self.assertTrue(result["ok"])
        self.assertEqual(0, result["metadata"]["renamed_count"])

    def test_conflict_is_detected_before_changes(self):
        folder = self.folder()
        (folder / "a.jpg").write_bytes(b"source")
        (folder / "Photo_001.jpg").mkdir()
        before = {p.name for p in folder.iterdir()}
        result = self.rename(folder, "Photo_{n:03d}.jpg")
        self.assertFalse(result["ok"])
        self.assertEqual("FILESYSTEM_RENAME_CONFLICT", result["error"])
        self.assertEqual(before, {p.name for p in folder.iterdir()})
        self.assertEqual(b"source", (folder / "a.jpg").read_bytes())

    def test_repeated_run_is_idempotent(self):
        folder = self.folder()
        (folder / "a.jpg").write_bytes(b"a")
        (folder / "b.jpg").write_bytes(b"b")
        first = self.rename(folder, "Photo_{n:03d}.jpg")
        second = self.rename(folder, "Photo_{n:03d}.jpg")
        self.assertTrue(first["ok"] and second["ok"])
        self.assertEqual(0, second["metadata"]["renamed_count"])
        self.assertEqual({"Photo_001.jpg", "Photo_002.jpg"}, {p.name for p in folder.iterdir()})

    def test_invalid_pattern_is_controlled_error(self):
        folder = self.folder()
        (folder / "a.jpg").write_bytes(b"a")
        result = self.rename(folder, "Photo.jpg")
        self.assertFalse(result["ok"])
        self.assertEqual("FILESYSTEM_INVALID_RENAME_PATTERN", result["error"])

    def test_missing_folder_is_controlled_error(self):
        result = self.rename(self.root / "missing", "Photo_{n}.jpg")
        self.assertFalse(result["ok"])
        self.assertEqual("FILESYSTEM_FOLDER_NOT_FOUND", result["error"])


if __name__ == "__main__":
    unittest.main()
