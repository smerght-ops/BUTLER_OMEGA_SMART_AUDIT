from __future__ import annotations

import hashlib
import os
import re
import time
from collections import defaultdict
from pathlib import Path


LARGE_FILE_BYTES = 10 * 1024 * 1024
SAFE_CATEGORIES = (
    "python_cache", "backup_files", "logs", "temporary_files",
    "generated_images", "test_audit_reports",
)
CATEGORY_ORDER = SAFE_CATEGORIES + (
    "project_dumps", "unknown_protected",
)
CATEGORY_LABELS = {
    "python_cache": "Python Cache",
    "backup_files": "Backup Files",
    "logs": "Logs",
    "temporary_files": "Temporary Files",
    "generated_images": "Generated Images",
    "test_audit_reports": "Test and Audit Reports",
    "project_dumps": "Project Dumps and Snapshots",
    "unknown_protected": "Unknown or Protected",
    "duplicates": "Duplicates",
    "large_files": "Large Files",
}
SAFE_REASONS = {
    "python_cache": "Автоматически создаваемый кэш Python. Безопасно восстанавливается.",
    "backup_files": "Формально распознанные резервные копии; основные рабочие файлы не включены.",
    "logs": "Диагностические журналы, не являющиеся рабочими документами или защищённым журналом состояния.",
    "temporary_files": "Однозначно распознанные временные файлы.",
    "generated_images": "Результаты генерации из специально обозначенных каталогов.",
    "test_audit_reports": "Сформированные результаты тестов и аудитов; исходный код тестов не включён.",
}
MANUAL_REASONS = {
    "project_dumps": "Может содержать рабочие данные, карты и снимки проекта.",
    "duplicates": "Требуется явно определить, какой экземпляр сохранять.",
    "large_files": "Большой размер не означает, что файл не нужен.",
    "unknown_protected": "Назначение не подтверждено формальной безопасной категорией или объект защищён.",
}


def fingerprint(path: Path) -> tuple:
    details = path.stat(follow_symlinks=False)
    attributes = int(getattr(details, "st_file_attributes", 0))
    return (
        details.st_dev, details.st_ino, details.st_mode, details.st_size,
        details.st_mtime_ns, attributes,
    )


def is_special(path: Path) -> bool:
    try:
        attributes = int(getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0))
    except OSError:
        return True
    return path.is_symlink() or bool(attributes & (0x2 | 0x4 | 0x400))


def classify(path: Path, root: Path, is_dir: bool = False) -> str:
    if is_special(path):
        return "unknown_protected"
    relative = path.relative_to(root)
    parts = tuple(part.casefold() for part in relative.parts)
    name = path.name.casefold()
    suffix = path.suffix.casefold()

    if "__pycache__" in parts or name == "__pycache__" or suffix in {".pyc", ".pyo"}:
        return "python_cache"
    if not is_dir and re.search(
        r'(?:\.|_)(?:safe_)?(?:bak\d*|backup|before|stable|legacy)(?:[._-].*)?$',
        name, re.IGNORECASE,
    ):
        return "backup_files"
    if not is_dir and (
        suffix in {".tmp", ".temp"}
        or name.startswith(("temp_", "temporary_", ".butler_"))
        or ".butler_" in name
    ):
        return "temporary_files"
    if "generated_images" in parts and not is_dir:
        return "generated_images"
    if _inside_report_directory(parts) and not is_dir:
        return "test_audit_reports"
    if not is_dir and name == "observations.jsonl":
        return "unknown_protected"
    if not is_dir and (suffix == ".log" or "a_08_logs" in parts):
        return "logs"
    if not is_dir and _is_project_dump(name):
        return "project_dumps"
    return "unknown_protected"


def _inside_report_directory(parts: tuple[str, ...]) -> bool:
    joined = "/".join(parts)
    return (
        "a_09_tests/reports/" in joined
        or "a_99_tests/reports/" in joined
        or "a_06_workspace/audits/" in joined
        or "audit_packs/" in joined
    )


def _is_project_dump(name: str) -> bool:
    exact = {
        "project_dump.txt", "project_structure.txt", "project_tree.txt",
        "fullcapabilityregistry_fixed.json", "dependencymodel.json",
        "linkmap.json", "unifiedinspectorfacts.json",
    }
    return (
        name in exact
        or name.startswith("project_full_context_pack")
        or (name.startswith("inspector") and name.endswith(".json"))
    )


def analyze(root: Path) -> dict:
    started = time.time()
    entries = []
    errors = []
    size_groups = defaultdict(list)
    stack = [root]
    directory_count = 0
    file_count = 0
    total_size = 0

    while stack:
        folder = stack.pop()
        try:
            with os.scandir(folder) as iterator:
                children = sorted(iterator, key=lambda item: (item.name.casefold(), item.name))
        except OSError as exc:
            errors.append({"path": str(folder), "error": f"{type(exc).__name__}: {exc}"})
            continue
        for child in children:
            path = Path(child.path)
            try:
                special = is_special(path)
                is_dir = child.is_dir(follow_symlinks=False)
                is_file = child.is_file(follow_symlinks=False)
                category = classify(path, root, is_dir=is_dir)
                details = path.stat(follow_symlinks=False)
                size = details.st_size if is_file else 0
                record = {
                    "path": str(path), "relative_path": path.relative_to(root).as_posix(),
                    "kind": "directory" if is_dir else "file" if is_file else "special",
                    "category": category, "size": size,
                    "fingerprint": list(fingerprint(path)),
                }
                entries.append(record)
                if is_dir:
                    directory_count += 1
                    if not special:
                        stack.append(path)
                elif is_file:
                    file_count += 1
                    total_size += size
                    size_groups[size].append(record)
                else:
                    errors.append({"path": str(path), "error": "special object"})
            except OSError as exc:
                errors.append({"path": str(path), "error": f"{type(exc).__name__}: {exc}"})
                entries.append({
                    "path": str(path), "relative_path": path.relative_to(root).as_posix(),
                    "kind": "unknown", "category": "unknown_protected", "size": 0,
                    "fingerprint": None,
                })

    duplicate_groups = []
    for size, candidates in size_groups.items():
        if size == 0 or len(candidates) < 2:
            continue
        hashes = defaultdict(list)
        for candidate in candidates:
            try:
                hashes[_sha256(Path(candidate["path"]))].append(candidate["path"])
            except OSError as exc:
                errors.append({"path": candidate["path"], "error": f"{type(exc).__name__}: {exc}"})
        for digest, paths in hashes.items():
            if len(paths) > 1:
                duplicate_groups.append({
                    "sha256": digest, "size_each": size, "copy_count": len(paths),
                    "paths": paths, "potential_bytes": size * (len(paths) - 1),
                })

    categories = {}
    for key in CATEGORY_ORDER:
        objects = [item for item in entries if item["category"] == key]
        categories[key] = _category_summary(key, objects, key in SAFE_CATEGORIES)
    large = [item for item in entries if item["kind"] == "file" and item["size"] >= LARGE_FILE_BYTES]
    categories["duplicates"] = {
        "label": CATEGORY_LABELS["duplicates"], "selectable": False,
        "requires_manual_decision": True, "groups": duplicate_groups,
        "file_count": sum(group["copy_count"] for group in duplicate_groups),
        "folder_count": 0,
        "bytes": sum(group["size_each"] * group["copy_count"] for group in duplicate_groups),
        "potential_bytes": sum(group["potential_bytes"] for group in duplicate_groups),
        "paths": [path for group in duplicate_groups for path in group["paths"]],
    }
    categories["large_files"] = _category_summary("large_files", large, False)
    categories["large_files"]["threshold_bytes"] = LARGE_FILE_BYTES
    safe_bytes = sum(categories[key]["bytes"] for key in SAFE_CATEGORIES)
    return {
        "root": str(root), "read_only": True, "created_at": time.time(),
        "duration_ms": max(0, int((time.time() - started) * 1000)),
        "file_count": file_count, "folder_count": directory_count,
        "total_bytes": total_size, "safe_category_bytes": safe_bytes,
        "manual_decision_bytes": categories["project_dumps"]["bytes"] + categories["large_files"]["bytes"],
        "categories": categories, "entries": entries, "errors": errors,
    }


def build_recommendations(snapshot: dict) -> dict:
    categories = snapshot["categories"]
    safe = []
    for key in SAFE_CATEGORIES:
        value = categories[key]
        safe.append({
            "category": key, "label": value["label"],
            "file_count": value["file_count"], "folder_count": value["folder_count"],
            "bytes": value["bytes"], "reason": SAFE_REASONS[key],
        })
    manual_keys = ("project_dumps", "duplicates", "large_files", "unknown_protected")
    manual = [
        {
            "category": key, "label": categories[key]["label"],
            "file_count": categories[key]["file_count"],
            "folder_count": categories[key]["folder_count"],
            "bytes": categories[key]["bytes"], "reason": MANUAL_REASONS[key],
        }
        for key in manual_keys
    ]
    total_files = sum(item["file_count"] for item in safe)
    total_folders = sum(item["folder_count"] for item in safe)
    total_bytes = sum(item["bytes"] for item in safe)
    lines = ["Безопасно удалить", ""]
    if total_files == 0 and total_folders == 0:
        lines.extend(("Безопасных объектов для удаления не обнаружено.", ""))
    else:
        for item in safe:
            lines.extend((
                item["label"],
                f"{item['file_count']} файлов; {item['folder_count']} папок; {_format_size(item['bytes'])}.",
                f"Причина: {item['reason']}", "",
            ))
    lines.extend(("Не рекомендуется удалять", ""))
    for item in manual:
        lines.extend((
            item["label"],
            f"{item['file_count']} файлов; {item['folder_count']} папок; {_format_size(item['bytes'])}.",
            f"Причина: {item['reason']}", "",
        ))
    lines.extend((
        "Итог",
        f"Безопасно может быть освобождено: {total_files} файлов; "
        f"{total_folders} папок; {_format_size(total_bytes)}.",
    ))
    return {
        "safe_categories": safe, "not_recommended": manual,
        "total_file_count": total_files, "total_folder_count": total_folders,
        "total_bytes": total_bytes, "has_safe_objects": bool(total_files or total_folders),
        "text": "\n".join(lines),
    }


def _format_size(value: int) -> str:
    size = float(value)
    units = ("байт", "КБ", "МБ", "ГБ", "ТБ")
    index = 0
    while size >= 1024 and index < len(units) - 1:
        size /= 1024
        index += 1
    return f"{int(size)} {units[index]}" if index == 0 else f"{size:.2f} {units[index]}"


def _category_summary(key: str, objects: list[dict], selectable: bool) -> dict:
    ordered = sorted(objects, key=lambda item: (-item["size"], item["path"].casefold()))
    return {
        "label": CATEGORY_LABELS[key], "selectable": selectable,
        "requires_manual_decision": not selectable,
        "file_count": sum(item["kind"] == "file" for item in objects),
        "folder_count": sum(item["kind"] == "directory" for item in objects),
        "bytes": sum(item["size"] for item in objects),
        "potential_bytes": sum(item["size"] for item in objects) if selectable else 0,
        "largest_examples": [item["path"] for item in ordered[:5]],
        "paths": [item["path"] for item in objects],
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
