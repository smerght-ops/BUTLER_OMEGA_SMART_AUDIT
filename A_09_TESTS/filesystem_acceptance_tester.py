from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import time
import ctypes
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_03_ORCHESTRATION.dispatcher_bridge_v2 import dispatch


REPORTS = PROJECT_ROOT / "A_09_TESTS" / "reports"
REQUIRED_CONTRACT = {"ok", "department", "model", "latency_ms", "text", "error", "metadata"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def snapshot(root: Path) -> dict:
    if not root.exists():
        return {"exists": False, "files": {}, "directories": []}
    files = {}
    directories = []
    for item in sorted(root.rglob("*"), key=lambda value: str(value).casefold()):
        relative = item.relative_to(root).as_posix()
        if item.is_dir():
            directories.append(relative)
        elif item.is_file():
            files[relative] = {"size": item.stat().st_size, "sha256": sha256(item)}
    return {"exists": True, "files": files, "directories": directories}


class FilesystemAcceptanceTester:
    def __init__(self):
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.root = Path(f"C:/Test/ButlerAcceptance_{stamp}_{os.getpid()}").resolve()
        self.scenarios = []

    @staticmethod
    def write(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @staticmethod
    def contract_ok(result: dict, expected_ok: bool, expected_department: str = "FILESYSTEM") -> bool:
        return (
            isinstance(result, dict)
            and REQUIRED_CONTRACT.issubset(result)
            and result.get("department") == expected_department
            and result.get("ok") is expected_ok
        )

    def execute(self, query: str) -> dict:
        return dispatch(query, {})

    @staticmethod
    def execute_with_context(query: str, context: dict) -> dict:
        return dispatch(query, context)

    def record(self, group, name, query, before, result, after, checks):
        expected_department = checks.pop("expected_department", "FILESYSTEM")
        passed = self.contract_ok(result, checks.pop("expected_ok"), expected_department) and all(checks.values())
        portable_result = json.loads(json.dumps(result, ensure_ascii=False, default=str))
        self.scenarios.append({
            "group": group,
            "name": name,
            "query": query,
            "passed": passed,
            "checks": checks,
            "before": before,
            "after": after,
            "result_contract": portable_result,
        })

    def rename_checks(self):
        folder = self.root / "rename_numbered"
        for name in ("zeta.jpg", "Alpha.jpg", "beta.jpg"):
            self.write(folder / name, name)
        query = f'Переименуй все фотографии в папке "{folder}" в формат "Photo_{{n:03d}}.jpg"'
        before = snapshot(folder)
        result = self.execute(query)
        after = snapshot(folder)
        self.record("rename", "numbered", query, before, result, after, {
            "expected_ok": True,
            "names": set(after["files"]) == {"Photo_001.jpg", "Photo_002.jpg", "Photo_003.jpg"},
            "count_preserved": len(before["files"]) == len(after["files"]) == 3,
            "reported_count": result.get("metadata", {}).get("renamed_count") == 3,
        })

        folder = self.root / "rename_extensions"
        self.write(folder / "a.jpg", "jpg")
        self.write(folder / "b.png", "png")
        query = f'Переименуй файлы в папке "{folder}" в формат "Document_{{n:03d}}"'
        before = snapshot(folder)
        result = self.execute(query)
        after = snapshot(folder)
        self.record("rename", "preserve_extensions", query, before, result, after, {
            "expected_ok": True,
            "extensions": set(after["files"]) == {"Document_001.jpg", "Document_002.png"},
            "hashes_preserved": sorted(x["sha256"] for x in before["files"].values()) == sorted(x["sha256"] for x in after["files"].values()),
        })

        folder = self.root / "rename_empty"
        folder.mkdir(parents=True)
        query = f'Переименуй файлы в папке "{folder}" в формат "Empty_{{n}}.txt"'
        before = snapshot(folder)
        result = self.execute(query)
        after = snapshot(folder)
        self.record("rename", "empty", query, before, result, after, {
            "expected_ok": True,
            "empty": after["files"] == {},
            "reported_zero": result.get("metadata", {}).get("renamed_count") == 0,
        })

        folder = self.root / "rename_conflict"
        self.write(folder / "a.jpg", "source")
        (folder / "Photo_001.jpg").mkdir(parents=True)
        query = f'Переименуй файлы в папке "{folder}" в формат "Photo_{{n:03d}}.jpg"'
        before = snapshot(folder)
        result = self.execute(query)
        after = snapshot(folder)
        self.record("rename", "conflict", query, before, result, after, {
            "expected_ok": False,
            "error": result.get("error") == "FILESYSTEM_RENAME_CONFLICT",
            "unchanged": before == after,
        })

        folder = self.root / "rename_repeat"
        self.write(folder / "a.jpg", "a")
        self.write(folder / "b.jpg", "b")
        query = f'Переименуй файлы в папке "{folder}" в формат "Photo_{{n:03d}}.jpg"'
        first = self.execute(query)
        before = snapshot(folder)
        result = self.execute(query)
        after = snapshot(folder)
        self.record("rename", "repeat", query, before, result, after, {
            "expected_ok": True,
            "first_passed": self.contract_ok(first, True),
            "unchanged": before == after,
            "reported_zero": result.get("metadata", {}).get("renamed_count") == 0,
        })

    def copy_checks(self):
        source = self.root / "copy_file_source.txt"
        target = self.root / "copy_file_target" / "renamed.txt"
        self.write(source, "copy-file")
        query = f'Скопируй файл "{source}" в "{target}"'
        before = snapshot(self.root)
        result = self.execute(query)
        after = snapshot(self.root)
        self.record("copy", "file_to_file", query, before, result, after, {
            "expected_ok": True,
            "source_exists": source.is_file(),
            "target_exists": target.is_file(),
            "hash_equal": target.is_file() and sha256(source) == sha256(target),
        })

        source = self.root / "copy_folder_source.txt"
        destination = self.root / "copy_file_folder"
        self.write(source, "copy-folder")
        destination.mkdir()
        query = f'Скопируй файл "{source}" в "{destination}"'
        before = snapshot(self.root)
        result = self.execute(query)
        target = destination / source.name
        after = snapshot(self.root)
        self.record("copy", "file_to_folder", query, before, result, after, {
            "expected_ok": True,
            "source_exists": source.is_file(),
            "target_exists": target.is_file(),
            "hash_equal": target.is_file() and sha256(source) == sha256(target),
        })

        source = self.root / "copy_batch_source"
        destination = self.root / "copy_batch_destination"
        self.write(source / "a.txt", "a")
        self.write(source / "b.jpg", "b")
        self.write(source / "Nested" / "ignored.txt", "nested")
        query = f'Скопируй все файлы из папки "{source}" в "{destination}"'
        before = snapshot(source)
        result = self.execute(query)
        after = snapshot(destination)
        self.record("copy", "first_level", query, before, result, after, {
            "expected_ok": True,
            "only_first_level": set(after["files"]) == {"a.txt", "b.jpg"},
            "source_unchanged": snapshot(source) == before,
            "hashes": all(after["files"][name]["sha256"] == before["files"][name]["sha256"] for name in ("a.txt", "b.jpg")),
        })

        source = self.root / "copy_tree_source"
        destination = self.root / "copy_tree_destination"
        self.write(source / "root.txt", "root")
        self.write(source / "Sub" / "child.txt", "child")
        query = f'Скопируй папку "{source}" в "{destination}"'
        before = snapshot(source)
        result = self.execute(query)
        target = destination / source.name
        after = snapshot(target)
        self.record("copy", "folder_tree", query, before, result, after, {
            "expected_ok": True,
            "structure": set(after["files"]) == {"root.txt", "Sub/child.txt"},
            "source_unchanged": snapshot(source) == before,
            "hashes": after["files"] == before["files"],
        })

        source = self.root / "copy_conflict_source"
        destination = self.root / "copy_conflict_destination"
        self.write(source / "a.txt", "source")
        self.write(destination / "a.txt", "occupied")
        query = f'Скопируй все файлы из папки "{source}" в "{destination}"'
        before_source, before_destination = snapshot(source), snapshot(destination)
        result = self.execute(query)
        after_source, after_destination = snapshot(source), snapshot(destination)
        self.record("copy", "conflict", query, {"source": before_source, "destination": before_destination}, result, {"source": after_source, "destination": after_destination}, {
            "expected_ok": False,
            "error": result.get("error") == "FILESYSTEM_COPY_CONFLICT",
            "source_unchanged": before_source == after_source,
            "destination_unchanged": before_destination == after_destination,
        })

    def move_checks(self):
        source = self.root / "move_file_source.txt"
        target = self.root / "move_file_target" / "renamed.txt"
        self.write(source, "move-file")
        source_hash = sha256(source)
        query = f'Перемести файл "{source}" в "{target}"'
        before = snapshot(self.root)
        result = self.execute(query)
        after = snapshot(self.root)
        self.record("move", "file_to_file", query, before, result, after, {
            "expected_ok": True,
            "source_absent": not source.exists(),
            "target_exists": target.is_file(),
            "hash_equal": target.is_file() and sha256(target) == source_hash,
        })

        source = self.root / "move_folder_source.txt"
        destination = self.root / "move_file_folder"
        self.write(source, "move-folder")
        source_hash = sha256(source)
        destination.mkdir()
        query = f'Перемести файл "{source}" в папку "{destination}"'
        result = self.execute(query)
        target = destination / source.name
        self.record("move", "file_to_folder", query, {"source_hash": source_hash}, result, snapshot(destination), {
            "expected_ok": True,
            "source_absent": not source.exists(),
            "target_exists": target.is_file(),
            "hash_equal": target.is_file() and sha256(target) == source_hash,
        })

        source = self.root / "move_batch_source"
        destination = self.root / "move_batch_destination"
        self.write(source / "a.txt", "a")
        self.write(source / "b.jpg", "b")
        self.write(source / "Nested" / "ignored.txt", "nested")
        before = snapshot(source)
        query = f'Перемести все файлы из папки "{source}" в папку "{destination}"'
        result = self.execute(query)
        after = snapshot(destination)
        self.record("move", "first_level", query, before, result, after, {
            "expected_ok": True,
            "moved": set(after["files"]) == {"a.txt", "b.jpg"},
            "sources_absent": not (source / "a.txt").exists() and not (source / "b.jpg").exists(),
            "nested_remains": (source / "Nested" / "ignored.txt").is_file(),
            "hashes": all(after["files"][name]["sha256"] == before["files"][name]["sha256"] for name in ("a.txt", "b.jpg")),
        })

        source = self.root / "move_tree_source"
        destination = self.root / "move_tree_destination"
        self.write(source / "root.txt", "root")
        self.write(source / "Sub" / "child.txt", "child")
        before = snapshot(source)
        query = f'Перемести папку "{source}" в папку "{destination}"'
        result = self.execute(query)
        target = destination / source.name
        after = snapshot(target)
        self.record("move", "folder_tree", query, before, result, after, {
            "expected_ok": True,
            "source_absent": not source.exists(),
            "structure": set(after["files"]) == {"root.txt", "Sub/child.txt"},
            "hashes": after["files"] == before["files"],
        })

        source = self.root / "move_conflict_source"
        destination = self.root / "move_conflict_destination"
        self.write(source / "a.txt", "source")
        self.write(destination / "a.txt", "occupied")
        query = f'Перемести все файлы из папки "{source}" в папку "{destination}"'
        before_source, before_destination = snapshot(source), snapshot(destination)
        result = self.execute(query)
        after_source, after_destination = snapshot(source), snapshot(destination)
        self.record("move", "conflict", query, {"source": before_source, "destination": before_destination}, result, {"source": after_source, "destination": after_destination}, {
            "expected_ok": False,
            "error": result.get("error") == "FILESYSTEM_MOVE_CONFLICT",
            "source_unchanged": before_source == after_source,
            "destination_unchanged": before_destination == after_destination,
        })

    def delete_checks(self):
        target = self.root / "delete_file" / "report.txt"
        self.write(target, "delete-confirmed")
        query = f'Удали файл "{target}"'
        before = snapshot(target.parent)
        requested = self.execute(query)
        before_confirmation = target.is_file()
        result = self.execute("Да")
        after = snapshot(target.parent)
        self.record("delete", "file_confirmed", query, before, result, after, {
            "expected_ok": True,
            "confirmation_requested": requested.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
            "unchanged_before_confirmation": before_confirmation,
            "deleted": not target.exists(),
            "reported_file_count": result.get("metadata", {}).get("deleted_file_count") == 1,
        })

        repeated = self.execute("Да")
        self.record("delete", "repeat_confirmation", "Да", after, repeated, snapshot(target.parent), {
            "expected_ok": False,
            "not_filesystem_replay": repeated.get("error") != "FILESYSTEM_DELETE_PARTIAL_FAILURE",
            "target_absent": not target.exists(),
        })

        target = self.root / "delete_without_confirmation.txt"
        self.write(target, "keep")
        query = f'Удали файл "{target}"'
        before = snapshot(self.root)
        result = self.execute(query)
        after = snapshot(self.root)
        self.record("delete", "without_confirmation", query, before, result, after, {
            "expected_ok": False,
            "confirmation_requested": result.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
            "unchanged": before == after,
            "target_exists": target.is_file(),
        })
        self.execute("Отмена")

        target = self.root / "delete_cancelled.txt"
        self.write(target, "keep")
        query = f'Удали файл "{target}"'
        self.execute(query)
        before = snapshot(self.root)
        result = self.execute("Отмена")
        repeated = self.execute("Да")
        after = snapshot(self.root)
        self.record("delete", "cancelled", f"{query} -> Отмена", before, result, after, {
            "expected_ok": False,
            "cancelled": result.get("error") == "FILESYSTEM_DELETE_CANCELLED",
            "unchanged": before == after,
            "target_exists": target.is_file(),
            "repeat_did_not_delete": target.is_file() and not repeated.get("ok"),
        })

        target = self.root / "delete_ambiguous.txt"
        self.write(target, "keep")
        query = f'Удали файл "{target}"'
        self.execute(query)
        before = snapshot(self.root)
        result = self.execute("Наверное")
        after = snapshot(self.root)
        self.record("delete", "ambiguous", f"{query} -> Наверное", before, result, after, {
            "expected_ok": False,
            "not_accepted": result.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_NOT_ACCEPTED",
            "unchanged": before == after,
            "target_exists": target.is_file(),
        })

        folder = self.root / "delete_flat"
        self.write(folder / "a.txt", "a")
        self.write(folder / "b.jpg", "b")
        self.write(folder / "Nested" / "keep.txt", "keep")
        query = f'Удали все файлы из папки "{folder}"'
        self.execute(query)
        result = self.execute("Подтверждаю удаление")
        after = snapshot(folder)
        self.record("delete", "first_level", query, {}, result, after, {
            "expected_ok": True,
            "top_files_removed": not (folder / "a.txt").exists() and not (folder / "b.jpg").exists(),
            "nested_preserved": (folder / "Nested" / "keep.txt").is_file(),
            "root_preserved": folder.is_dir(),
        })

        folder = self.root / "delete_tree"
        self.write(folder / "root.txt", "root")
        self.write(folder / "Sub" / "child.txt", "child")
        (folder / "EmptyFolder").mkdir(parents=True)
        query = f'Удали папку "{folder}"'
        requested = self.execute(query)
        existed_before_confirmation = folder.is_dir()
        result = self.execute("Да")
        self.record("delete", "folder_tree", query, {}, result, snapshot(folder), {
            "expected_ok": True,
            "confirmation_requested": requested.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
            "existed_before_confirmation": existed_before_confirmation,
            "root_removed": not folder.exists(),
            "reported_files": result.get("metadata", {}).get("deleted_file_count") == 2,
            "reported_folders": result.get("metadata", {}).get("deleted_folder_count") == 3,
        })

        folder = self.root / "delete_empty"
        folder.mkdir(parents=True)
        query = f'Удали папку "{folder}"'
        self.execute(query)
        result = self.execute("Удалить")
        self.record("delete", "empty_folder", query, {}, result, snapshot(folder), {
            "expected_ok": True,
            "root_removed": not folder.exists(),
            "zero_files": result.get("metadata", {}).get("deleted_file_count") == 0,
            "one_folder": result.get("metadata", {}).get("deleted_folder_count") == 1,
        })

        missing = self.root / "does_not_exist.txt"
        query = f'Удали файл "{missing}"'
        result = self.execute(query)
        self.record("delete", "missing", query, {}, result, {}, {
            "expected_ok": False,
            "not_found": result.get("error") == "FILESYSTEM_SOURCE_NOT_FOUND",
            "no_confirmation": result.get("metadata", {}).get("state") != "awaiting_confirmation",
        })

        query = 'Удали папку "C:\\Windows"'
        result = self.execute(query)
        self.record("delete", "protected_path", query, {}, result, {}, {
            "expected_ok": False,
            "blocked": result.get("error") == "FILESYSTEM_DELETE_PATH_FORBIDDEN",
            "windows_still_exists": Path("C:/Windows").is_dir(),
        })

        outside = PROJECT_ROOT
        query = f'Удали папку "{outside}"'
        result = self.execute(query)
        self.record("delete", "outside_allowed_roots", query, {}, result, {}, {
            "expected_ok": False,
            "blocked": result.get("error") == "FILESYSTEM_DELETE_PATH_FORBIDDEN",
            "project_still_exists": outside.is_dir(),
        })

        hidden = self.root / "delete_hidden.txt"
        self.write(hidden, "hidden")
        attributes = ctypes.windll.kernel32.GetFileAttributesW(str(hidden))
        hidden_set = attributes != 0xFFFFFFFF and bool(ctypes.windll.kernel32.SetFileAttributesW(str(hidden), attributes | 0x2))
        query = f'Удали файл "{hidden}"'
        result = self.execute(query)
        self.record("delete", "hidden_file", query, {}, result, {}, {
            "expected_ok": False,
            "attribute_created": hidden_set,
            "blocked": result.get("error") == "FILESYSTEM_DELETE_PROTECTED_OBJECT",
            "target_exists": hidden.is_file(),
        })
        if hidden.exists() and attributes != 0xFFFFFFFF:
            ctypes.windll.kernel32.SetFileAttributesW(str(hidden), attributes)

        link_root = self.root / "delete_link_tree"
        target = self.root / "link_target.txt"
        self.write(target, "target")
        link_root.mkdir(parents=True)
        link = link_root / "link.txt"
        try:
            os.symlink(target, link)
        except OSError as exc:
            self.scenarios.append({
                "group": "delete", "name": "reparse_point", "query": "safe symlink creation",
                "passed": True, "not_applicable": True,
                "checks": {"reason": f"{type(exc).__name__}: {exc}"},
                "before": {}, "after": {}, "result_contract": None,
            })
        else:
            query = f'Удали папку "{link_root}"'
            result = self.execute(query)
            self.record("delete", "reparse_point", query, {}, result, {}, {
                "expected_ok": False,
                "blocked": result.get("error") == "FILESYSTEM_DELETE_SPECIAL_OBJECT",
                "link_target_unchanged": target.read_text(encoding="utf-8") == "target",
            })

    def base_regression_checks(self):
        folder = self.root / "regression_create"
        result = self.execute_with_context("Создай папку", {
            "capability_action": "create_folder",
            "folder_name": folder.name,
            "parent_folder": self.root,
        })
        self.record("regression", "create_folder", "Создай папку", {}, result, snapshot(folder), {
            "expected_ok": True,
            "folder_created": folder.is_dir(),
        })

        text_target = self.root / "regression_text" / "saved.txt"
        result = self.execute_with_context("Сохрани текст в файл", {
            "capability_action": "save_text",
            "folder": text_target.parent,
            "filename": text_target.name,
            "content": "regression-text",
        })
        self.record("regression", "save_text", "Сохрани текст в файл", {}, result, snapshot(text_target.parent), {
            "expected_ok": True,
            "content_saved": text_target.is_file() and text_target.read_text(encoding="utf-8") == "regression-text",
        })

        image_source = self.root / "regression_image_source.png"
        image_source.write_bytes(b"butler-image-regression")
        image_target = self.root / "regression_image" / "saved.png"
        result = self.execute_with_context("Сохрани изображение в файл", {
            "capability_action": "save_image",
            "source": image_source,
            "folder": image_target.parent,
            "filename": image_target.name,
        })
        self.record("regression", "save_image", "Сохрани изображение в файл", {}, result, snapshot(image_target.parent), {
            "expected_ok": True,
            "bytes_preserved": image_target.is_file() and image_target.read_bytes() == image_source.read_bytes(),
        })

    def analysis_fixture(self, name: str) -> Path:
        root = self.root / name
        self.write(root / "main.py", "print('working code')")
        self.write(root / "cache.pyc", "compiled")
        self.write(root / "__pycache__" / "module.pyc", "cached-module")
        self.write(root / "document.txt.bak", "backup")
        self.write(root / "config.json.BAK_2025", "backup-composite")
        self.write(root / "application.log", "log")
        self.write(root / "A_08_LOGS" / "diagnostic.txt", "diagnostic-log")
        self.write(root / "A_08_LOGS" / "OBSERVATIONS.jsonl", "state-log")
        self.write(root / "ordinary.txt", "ordinary")
        self.write(root / "work.tmp", "temporary")
        self.write(root / "GENERATED_IMAGES" / "image.png", "generated-image")
        self.write(root / "outside_image.png", "user-image")
        self.write(root / "A_09_TESTS" / "reports" / "old_report.json", "report")
        self.write(root / "PROJECT_DUMP.txt", "project-dump")
        self.write(root / "duplicates" / "copy_a.bin", "identical-duplicate")
        self.write(root / "duplicates" / "copy_b.bin", "identical-duplicate")
        self.write(root / "unknown.xyz", "unknown")
        self.write(root / "catalog.db", "database")
        self.write(root / "config.json", "configuration")
        large = root / "large.bin"
        large.parent.mkdir(parents=True, exist_ok=True)
        with large.open("wb") as stream:
            stream.truncate(10 * 1024 * 1024)
        return root

    def analyze(self, root: Path) -> dict:
        return self.execute(f'Проанализируй папку "{root}" и покажи, что можно удалить')

    def analysis_checks(self):
        root = self.analysis_fixture("analysis_read_only")
        before = snapshot(root)
        query = f'Проанализируй папку "{root}" и покажи, что можно удалить'
        result = self.execute(query)
        after = snapshot(root)
        categories = result.get("metadata", {}).get("categories", {})
        entries = result.get("metadata", {}).get("analysis_snapshot", {}).get("entries", [])
        by_relative = {item["relative_path"]: item["category"] for item in entries}
        duplicates = categories.get("duplicates", {}).get("groups", [])
        self.record("analysis", "read_only_classification", query, before, result, after, {
            "expected_ok": True,
            "read_only": before == after and result.get("metadata", {}).get("read_only") is True,
            "python_code_safe": by_relative.get("main.py") == "unknown_protected",
            "pyc_classified": by_relative.get("cache.pyc") == "python_cache",
            "composite_backup": by_relative.get("config.json.BAK_2025") == "backup_files",
            "ordinary_text_not_log": by_relative.get("ordinary.txt") == "unknown_protected",
            "database_safe": by_relative.get("catalog.db") == "unknown_protected",
            "config_safe": by_relative.get("config.json") == "unknown_protected",
            "generated_by_location": by_relative.get("GENERATED_IMAGES/image.png") == "generated_images" and by_relative.get("outside_image.png") == "unknown_protected",
            "report_classified": by_relative.get("A_09_TESTS/reports/old_report.json") == "test_audit_reports",
            "observations_protected": by_relative.get("A_08_LOGS/OBSERVATIONS.jsonl") == "unknown_protected",
            "duplicate_sha256": any(group.get("copy_count") == 2 and len(group.get("sha256", "")) == 64 for group in duplicates),
            "large_manual": categories.get("large_files", {}).get("file_count") == 1 and not categories.get("large_files", {}).get("selectable"),
        })

        root = self.analysis_fixture("analysis_backup_delete")
        self.analyze(root)
        before = snapshot(root)
        planned = self.execute("Удали резервные файлы")
        unchanged_before_confirmation = snapshot(root) == before
        result = self.execute("Да")
        self.record("analysis", "delete_backup_files", "Удали резервные файлы -> Да", before, result, snapshot(root), {
            "expected_ok": True,
            "planned": planned.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
            "unchanged_before_confirmation": unchanged_before_confirmation,
            "backups_removed": not (root / "document.txt.bak").exists() and not (root / "config.json.BAK_2025").exists(),
            "working_files_preserved": (root / "main.py").is_file() and (root / "config.json").is_file(),
            "other_categories_preserved": (root / "cache.pyc").is_file() and (root / "application.log").is_file(),
        })

        root = self.analysis_fixture("analysis_python_cache")
        self.analyze(root)
        self.execute("Удали Python-кэш")
        result = self.execute("Подтверждаю удаление")
        self.record("analysis", "delete_python_cache", "Удали Python-кэш -> Подтверждаю удаление", {}, result, snapshot(root), {
            "expected_ok": True,
            "pyc_removed": not (root / "cache.pyc").exists(),
            "cache_folder_removed": not (root / "__pycache__").exists(),
            "python_preserved": (root / "main.py").is_file(),
            "other_category_preserved": (root / "document.txt.bak").is_file(),
        })

        root = self.analysis_fixture("analysis_logs")
        self.analyze(root)
        self.execute("Удали логи")
        result = self.execute("Да")
        self.record("analysis", "delete_logs", "Удали логи -> Да", {}, result, snapshot(root), {
            "expected_ok": True,
            "logs_removed": not (root / "application.log").exists() and not (root / "A_08_LOGS" / "diagnostic.txt").exists(),
            "ordinary_text_preserved": (root / "ordinary.txt").is_file(),
            "observations_preserved": (root / "A_08_LOGS" / "OBSERVATIONS.jsonl").is_file(),
        })

        root = self.analysis_fixture("analysis_generated")
        self.analyze(root)
        self.execute("Удали сгенерированные изображения")
        result = self.execute("Да")
        self.record("analysis", "delete_generated_images", "Удали сгенерированные изображения -> Да", {}, result, snapshot(root), {
            "expected_ok": True,
            "generated_removed": not (root / "GENERATED_IMAGES" / "image.png").exists(),
            "outside_preserved": (root / "outside_image.png").is_file(),
        })

        root = self.analysis_fixture("analysis_all_safe")
        self.analyze(root)
        planned = self.execute("Очисти всё безопасное")
        result = self.execute("Да")
        metadata = result.get("metadata", {})
        self.record("analysis", "cleanup_all_safe", "Очисти всё безопасное -> Да", {}, result, snapshot(root), {
            "expected_ok": True,
            "only_safe_selected": set(metadata.get("selected_categories", [])) == {"python_cache", "backup_files", "logs", "temporary_files", "generated_images", "test_audit_reports"},
            "safe_removed": not (root / "cache.pyc").exists() and not (root / "document.txt.bak").exists() and not (root / "application.log").exists() and not (root / "work.tmp").exists(),
            "manual_preserved": (root / "PROJECT_DUMP.txt").is_file() and (root / "large.bin").is_file(),
            "unknown_preserved": (root / "main.py").is_file() and (root / "catalog.db").is_file() and (root / "config.json").is_file(),
            "duplicates_preserved": (root / "duplicates" / "copy_a.bin").is_file() and (root / "duplicates" / "copy_b.bin").is_file(),
            "confirmation_was_required": planned.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
        })

        root = self.analysis_fixture("analysis_cancel")
        self.analyze(root)
        self.execute("Удали резервные файлы")
        before = snapshot(root)
        result = self.execute("Отмена")
        self.record("analysis", "cleanup_cancelled", "Отмена", before, result, snapshot(root), {
            "expected_ok": False,
            "cancelled": result.get("error") == "FILESYSTEM_DELETE_CANCELLED",
            "unchanged": before == snapshot(root),
        })

        root = self.analysis_fixture("analysis_stale")
        self.analyze(root)
        self.execute("Удали резервные файлы")
        changed = root / "document.txt.bak"
        changed.write_text("replacement-after-analysis", encoding="utf-8")
        result = self.execute("Да")
        self.record("analysis", "stale_object", "изменение после анализа -> Да", {}, result, snapshot(root), {
            "expected_ok": False,
            "blocked": result.get("error") == "FILESYSTEM_DELETE_REVALIDATION_FAILED",
            "changed_object_preserved": changed.is_file(),
        })

        root = self.analysis_fixture("analysis_forbidden_categories")
        analysis = self.analyze(root)
        duplicates = self.execute("Удали дубликаты")
        large = self.execute("Удали крупные файлы")
        self.record("analysis", "duplicates_and_large_forbidden", "Удали дубликаты / крупные файлы", {}, duplicates, snapshot(root), {
            "expected_ok": False,
            "duplicates_blocked": duplicates.get("error") == "FILESYSTEM_CLEANUP_CATEGORY_FORBIDDEN",
            "large_blocked": large.get("error") == "FILESYSTEM_CLEANUP_CATEGORY_FORBIDDEN",
            "duplicate_reported": bool(analysis.get("metadata", {}).get("categories", {}).get("duplicates", {}).get("groups")),
            "large_reported": analysis.get("metadata", {}).get("categories", {}).get("large_files", {}).get("threshold_bytes") == 10 * 1024 * 1024,
            "files_preserved": (root / "duplicates" / "copy_a.bin").is_file() and (root / "large.bin").is_file(),
        })

        query = 'Проанализируй папку "C:\\Windows" и покажи, что можно удалить'
        result = self.execute(query)
        self.record("analysis", "forbidden_path", query, {}, result, {}, {
            "expected_ok": False,
            "blocked": result.get("error") == "FILESYSTEM_ANALYSIS_PATH_FORBIDDEN",
            "windows_exists": Path("C:/Windows").is_dir(),
        })

    def routing_checks(self):
        query = f'Очисти папку "{self.root}"'
        result = self.execute(query)
        self.record("routing", "cleanup_folder_without_analysis", query, {}, result, snapshot(self.root), {
            "expected_ok": False,
            "filesystem": result.get("department") == "FILESYSTEM",
            "not_chat": result.get("department") != "CHAT",
            "analysis_required": result.get("error") == "FILESYSTEM_ANALYSIS_REQUIRED",
        })

        query = f'Очисти проект "{self.root}"'
        result = self.execute(query)
        self.record("routing", "cleanup_project_without_analysis", query, {}, result, snapshot(self.root), {
            "expected_ok": False,
            "filesystem": result.get("department") == "FILESYSTEM",
            "analysis_required": result.get("error") == "FILESYSTEM_ANALYSIS_REQUIRED",
        })

        root = self.analysis_fixture("routing_catalog")
        query = f'Проанализируй каталог "{root}"'
        result = self.execute(query)
        self.record("routing", "analyze_catalog", query, snapshot(root), result, snapshot(root), {
            "expected_ok": True,
            "filesystem": result.get("department") == "FILESYSTEM",
            "not_documents_or_chat": result.get("department") not in {"DOCUMENTS", "CHAT"},
            "read_only": result.get("metadata", {}).get("read_only") is True,
        })

        query = f'Проанализируй директорию "{root}"'
        result = self.execute(query)
        self.record("routing", "analyze_directory", query, snapshot(root), result, snapshot(root), {
            "expected_ok": True,
            "filesystem": result.get("department") == "FILESYSTEM",
            "not_documents": result.get("department") != "DOCUMENTS",
        })

        root = self.analysis_fixture("routing_project")
        query = f'Проанализируй проект "{root}"'
        result = self.execute(query)
        self.record("routing", "analyze_project", query, snapshot(root), result, snapshot(root), {
            "expected_ok": True,
            "filesystem": result.get("department") == "FILESYSTEM",
            "recommendations": "Безопасно удалить" in result.get("text", ""),
        })

        query = f'Проанализируй проект "{root}" и покажи, что можно безопасно удалить'
        result = self.execute(query)
        self.record("routing", "full_project_recommendation_phrase", query, snapshot(root), result, snapshot(root), {
            "expected_ok": True,
            "filesystem": result.get("department") == "FILESYSTEM",
            "safe_section": "Безопасно удалить" in result.get("text", ""),
            "manual_section": "Не рекомендуется удалять" in result.get("text", ""),
        })

        query = f'Покажи, что можно удалить из проекта "{root}"'
        result = self.execute(query)
        self.record("routing", "show_project_candidates", query, snapshot(root), result, snapshot(root), {
            "expected_ok": True,
            "filesystem": result.get("department") == "FILESYSTEM",
        })

        recommended = self.execute("Удали рекомендованное")
        self.record("routing", "delete_recommended_plan", "Удали рекомендованное", snapshot(root), recommended, snapshot(root), {
            "expected_ok": False,
            "confirmation_required": recommended.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
            "safe_categories_only": set(recommended.get("metadata", {}).get("selected_categories", [])) == {"python_cache", "backup_files", "logs", "temporary_files", "generated_images", "test_audit_reports"},
        })
        self.execute("Отмена")

        self.analyze(root)
        safe_alias = self.execute("Удали всё безопасное")
        self.record("routing", "delete_all_safe_alias", "Удали всё безопасное", snapshot(root), safe_alias, snapshot(root), {
            "expected_ok": False,
            "confirmation_required": safe_alias.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
            "same_categories": safe_alias.get("metadata", {}).get("selected_categories") == recommended.get("metadata", {}).get("selected_categories"),
        })
        self.execute("Отмена")

        self.analyze(root)
        before = snapshot(root)
        recommended = self.execute("Удали рекомендованное")
        confirmed = self.execute("Подтверждаю удаление")
        after = snapshot(root)
        self.record("routing", "delete_recommended_confirmed", "Удали рекомендованное / Подтверждаю удаление", before, confirmed, after, {
            "expected_ok": True,
            "plan_required_confirmation": recommended.get("error") == "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
            "safe_files_removed": not (root / "__pycache__" / "module.pyc").exists() and not (root / "trace.log").exists(),
            "source_preserved": (root / "main.py").is_file(),
        })

        root = self.analysis_fixture("routing_show_cleanup")
        query = f'Покажи, что можно удалить из папки "{root}"'
        result = self.execute(query)
        self.record("routing", "show_cleanup_candidates", query, snapshot(root), result, snapshot(root), {
            "expected_ok": True,
            "filesystem": result.get("department") == "FILESYSTEM",
            "not_documents_or_chat": result.get("department") not in {"DOCUMENTS", "CHAT"},
            "read_only": result.get("metadata", {}).get("read_only") is True,
        })

        document = self.root / "routing_document.txt"
        self.write(document, "document route regression")
        query = f'Проанализируй документ "{document}"'
        result = self.execute(query)
        self.record("routing", "documents_regression", query, snapshot(document.parent), result, snapshot(document.parent), {
            "expected_ok": True,
            "expected_department": "DOCUMENTS",
            "documents": result.get("department") == "DOCUMENTS",
            "not_filesystem": result.get("department") != "FILESYSTEM",
        })

        for name, query in (
            ("project_documentation_regression", "Подготовь документацию проекта Butler"),
            ("project_status_not_filesystem", "Какой статус проекта Butler?"),
            ("project_architecture_not_filesystem", "Проанализируй архитектуру проекта Butler"),
            ("project_without_absolute_path", "Проанализируй проект Butler"),
        ):
            result = self.execute(query)
            self.scenarios.append({
                "group": "routing", "name": name, "query": query,
                "passed": isinstance(result, dict) and REQUIRED_CONTRACT.issubset(result) and result.get("department") != "FILESYSTEM",
                "checks": {"not_filesystem": result.get("department") != "FILESYSTEM"},
                "before": {}, "after": {},
                "result_contract": json.loads(json.dumps(result, ensure_ascii=False, default=str)),
            })

    def run(self) -> tuple[dict, Path]:
        started = time.time()
        self.root.mkdir(parents=True, exist_ok=False)
        error = None
        try:
            self.routing_checks()
            self.analysis_checks()
            self.rename_checks()
            self.copy_checks()
            self.move_checks()
            self.base_regression_checks()
            self.delete_checks()
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
        passed = error is None and bool(self.scenarios) and all(item["passed"] for item in self.scenarios)
        report = {
            "status": "PASS" if passed else "FAIL",
            "official_route": "BUTLER_OS.py -> dispatcher_bridge_v2.dispatch -> SmartDispatcherV2 -> FilesystemDepartment",
            "direct_department_calls": False,
            "test_root": str(self.root),
            "started_at": datetime.fromtimestamp(started).isoformat(),
            "duration_ms": int((time.time() - started) * 1000),
            "error": error,
            "summary": {
                "total": len(self.scenarios),
                "passed": sum(item["passed"] for item in self.scenarios),
                "failed": sum(not item["passed"] for item in self.scenarios),
            },
            "scenarios": self.scenarios,
        }
        REPORTS.mkdir(parents=True, exist_ok=True)
        report_path = REPORTS / f"filesystem_acceptance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        shutil.rmtree(self.root)
        report["test_root_cleaned"] = not self.root.exists()
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return report, report_path


def main() -> int:
    report, path = FilesystemAcceptanceTester().run()
    print(json.dumps({"status": report["status"], "summary": report["summary"], "report": str(path), "test_root_cleaned": report["test_root_cleaned"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
