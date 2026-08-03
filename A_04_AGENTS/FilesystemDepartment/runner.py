# -*- coding: utf-8 -*-
from __future__ import annotations

import shutil
import time
import uuid
import re
import os
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment
from A_01_CORE.TaskExecutor.execution_context import ArtifactReference
from A_04_AGENTS.FilesystemDepartment.file_analyzer import (
    CATEGORY_LABELS,
    SAFE_CATEGORIES,
    analyze as analyze_tree,
    build_recommendations,
    classify as classify_analysis_path,
    fingerprint as analysis_fingerprint,
)


class FilesystemDepartment(BaseDepartment):
    NAME = "FILESYSTEM"
    VERSION = "1.1"
    CAPABILITIES = ("analyze_folder", "create_folder", "save_text", "save_image")
    DEPENDENCIES = ("pathlib", "shutil")
    DATA_READS = (
        "executor-provided source artifact",
        "user-selected directory under approved read roots",
    )
    DATA_WRITES = ("executor-approved workspace or Desktop path",)

    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.workspace_root = (self.root / "A_06_WORKSPACE" / "STAGE4_OUTPUT").resolve()
        self.project_workspace_root = (self.root / "A_06_WORKSPACE").resolve()
        self.desktop_root = (Path.home() / "Desktop").resolve()
        self.automation_root = Path("C:/Test").resolve()
        self.allowed_roots = (self.workspace_root, self.desktop_root, self.automation_root)
        self.allowed_read_roots = (
            self.project_workspace_root, self.desktop_root, self.automation_root,
        )
        self._pending_delete = None
        self._delete_confirmation_closed = False
        self._analysis_snapshot = None

    def can_handle(self, query: str, context: dict = None) -> bool:
        context = dict(context or {})
        return (
            self._pending_delete is not None
            or (self._delete_confirmation_closed and self._is_delete_response(query))
            or self._is_contextual_directory_read(query, context)
            or self._route_action(query) is not None
        )

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.time()
        context = dict(context or {})
        action = str(
            context.get("capability_action")
            or (
                "analyze_folder"
                if self._is_contextual_directory_read(query, context)
                else None
            )
            or self._route_action(query)
            or query
            or ""
        ).strip().lower()
        try:
            if self._pending_delete is not None:
                return self._resolve_delete_confirmation(query, started)
            if self._delete_confirmation_closed and self._is_delete_response(query):
                self._delete_confirmation_closed = False
                return self._result(
                    started, False, "Нет операции удаления, ожидающей подтверждения.",
                    "FILESYSTEM_DELETE_NO_PENDING_CONFIRMATION",
                    action="delete", state="closed", deleted_count=0,
                )
            if action == "analyze_folder":
                return self._analyze_folder(query, started, context)
            if action == "recommendations":
                return self._recommendations(started)
            if action == "cleanup_selection":
                return self._prepare_cleanup(query, started)
            if action == "delete":
                return self._prepare_delete(query, started)
            if action == "move":
                return self._move(query, started)
            if action == "copy":
                return self._copy(query, started)
            if action == "rename":
                return self._rename_files(query, started)
            if action == "create_folder":
                output = self._create_folder(context)
            elif action == "save_text":
                output = self._save_text(context)
            elif action == "save_image":
                output = self._save_image(context)
            else:
                return self._result(
                    started,
                    False,
                    f"Filesystem operation '{action}' is not supported.",
                    "UNSUPPORTED_FILESYSTEM_CAPABILITY",
                    action=action,
                )
            return self._result(
                started,
                True,
                f"Выполнено {action}: {output}",
                None,
                action=action,
                output=output,
            )
        except FileExistsError:
            return self._result(started, False, "Целевой объект уже существует.", "FILESYSTEM_TARGET_EXISTS", action=action)
        except FileNotFoundError:
            return self._result(started, False, "Исходный файл не найден.", "FILESYSTEM_SOURCE_NOT_FOUND", action=action)
        except (OSError, ValueError) as exc:
            return self._result(
                started, False, "Файловая операция не выполнена.", "FILESYSTEM_OPERATION_FAILED",
                action=action, exception_type=type(exc).__name__,
            )

    @staticmethod
    def _route_action(query: str) -> str | None:
        q = " ".join(str(query or "").casefold().split())
        absolute_path = FilesystemDepartment._has_absolute_windows_path(query)
        folder_analysis = (
            "проанализируй папку" in q or "проанализируй каталог" in q
            or "проанализируй директорию" in q
            or "анализ папки" in q or "анализ каталога" in q or "анализ директории" in q
            or "покажи, что можно удалить из папки" in q
            or "покажи что можно удалить из папки" in q
            or "покажи, что можно удалить из каталога" in q
            or "покажи что можно удалить из каталога" in q
            or "покажи, что можно удалить из директории" in q
            or "покажи что можно удалить из директории" in q
            or "analyze folder" in q
        )
        project_analysis = absolute_path and "проект" in q and (
            "проанализируй проект" in q or "проанализируй копию проекта" in q
            or "что можно удалить из проекта" in q
            or "что можно безопасно удалить из проекта" in q
        )
        if (
            folder_analysis
            or project_analysis
            or FilesystemDepartment._is_directory_read_query(q)
        ):
            return "analyze_folder"
        if q in {"что можно безопасно удалить", "что можно удалить", "покажи рекомендации по очистке"}:
            return "recommendations"
        if FilesystemDepartment._is_cleanup_selection(q):
            return "cleanup_selection"
        if "скопир" in q or "copy file" in q:
            return "copy"
        if "перемест" in q or "move file" in q:
            return "move"
        if "переимен" in q or "rename" in q:
            return "rename"
        if (
            "удали файл" in q or "удалить файл" in q
            or "удали все файлы" in q or "удалить все файлы" in q
            or "удали папку" in q or "удалить папку" in q
            or "delete file" in q or "delete folder" in q
        ):
            return "delete"
        if "создай папк" in q or "создать папк" in q or "создай каталог" in q:
            return "create_folder"
        if ("сохрани" in q or "запиши" in q) and (" в файл" in q or " по пути" in q):
            return "save_text"
        return None

    @staticmethod
    def _is_directory_read_query(query: str) -> bool:
        """Recognize a read-only question about a named directory."""
        q = " ".join(str(query or "").casefold().split())
        has_directory_object = re.search(
            r"\b(?:папк\w*|каталог\w*|директори\w*|folder|directory)\b",
            q,
        ) is not None
        asks_for_contents = (
            re.search(r"\bчто\b.*\b(?:лежит|находится|содержится)\b", q)
            is not None
            or re.search(r"\b(?:покажи|перечисли)\b.*\bсодержим\w*\b", q)
            is not None
        )
        return has_directory_object and asks_for_contents

    @staticmethod
    def _is_contextual_directory_read(query: str, context: dict) -> bool:
        referent = context.get("resolved_referent") or {}
        if referent.get("kind") != "directory" or not referent.get("path"):
            return False
        q = " ".join(str(query or "").casefold().split())
        requests_inspection = re.search(
            r"\b(?:изуч\w*|проанализир\w*|исслед\w*|прочита\w*|покаж\w*|"
            r"расскаж\w*|объясн\w*)\b",
            q,
        ) is not None
        mentions_contents = re.search(
            r"\b(?:содержим\w*|файл\w*|объект\w*|материал\w*)\b",
            q,
        ) is not None
        return requests_inspection and mentions_contents

    @staticmethod
    def _is_cleanup_selection(query: str) -> bool:
        q = " ".join(str(query or "").casefold().split())
        if q.startswith((
            "очисти папку ", "очистить папку ", "очисти каталог ", "очистить каталог ",
            "очисти директорию ", "очистить директорию ",
        )):
            return True
        if q.startswith(("очисти проект ", "очистить проект ")):
            return FilesystemDepartment._has_absolute_windows_path(query)
        if "из папки" in q or q.startswith(("удали файл ", "удалить файл ", "удали папку ", "удалить папку ")):
            return False
        markers = (
            "резервные файл", "python-кэш", "python кэш", "кэш", "логи",
            "временные файл", "сгенерированные изображ", "отчёты", "отчеты",
            "дубликаты", "крупные файлы", "всё безопасное", "все безопасное",
            "рекомендованное",
        )
        return (q.startswith(("удали ", "удалить ", "очисти ")) and any(marker in q for marker in markers))

    @staticmethod
    def _has_absolute_windows_path(query: str) -> bool:
        return re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]', str(query or "")) is not None

    def _analyze_folder(self, query: str, started: float, context: dict | None = None) -> dict:
        try:
            root = self._approved_read(self._analysis_request(query, context))
            if not root.exists():
                return self._result(started, False, "Папка для анализа не существует.", "FILESYSTEM_FOLDER_NOT_FOUND", action="analyze_folder")
            if not root.is_dir():
                return self._result(started, False, "Указанный путь не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY", action="analyze_folder")
            self._validate_delete_object(root)
            snapshot = analyze_tree(root)
            recommendations = build_recommendations(snapshot)
            self._analysis_snapshot = snapshot
            entries = [
                item["relative_path"]
                for item in snapshot["entries"]
            ]
            visible_entries = entries[:200]
            contents_text = "\n".join(f"- {item}" for item in visible_entries)
            if len(entries) > len(visible_entries):
                contents_text += (
                    f"\n- ... ещё {len(entries) - len(visible_entries)} объектов"
                )
            if not contents_text:
                contents_text = "- папка пуста"
            return self._result(
                started, True,
                f"READ ONLY анализ завершён: {root}. Файлов: {snapshot['file_count']}; "
                f"папок: {snapshot['folder_count']}; размер: {snapshot['total_bytes']} байт. "
                f"Изменений файловой системы нет.\n\n"
                f"Текущее содержимое:\n{contents_text}\n\n"
                f"{recommendations['text']}",
                None, action="analyze_folder", path=str(root), read_only=True,
                file_count=snapshot["file_count"], folder_count=snapshot["folder_count"],
                total_bytes=snapshot["total_bytes"], safe_category_bytes=snapshot["safe_category_bytes"],
                duration_ms=snapshot["duration_ms"], categories=snapshot["categories"],
                analysis_errors=snapshot["errors"], analysis_snapshot=snapshot,
                recommendations=recommendations,
            )
        except ValueError as exc:
            return self._result(
                started, False, f"Анализ заблокирован: {exc}",
                "FILESYSTEM_ANALYSIS_PATH_FORBIDDEN", action="analyze_folder",
            )
        except OSError as exc:
            return self._result(
                started, False, f"Анализ не завершён: {exc}",
                "FILESYSTEM_ANALYSIS_FAILED", action="analyze_folder",
                exception_type=type(exc).__name__,
            )

    def _recommendations(self, started: float) -> dict:
        if self._analysis_snapshot is None:
            return self._result(
                started, False, "Сначала проанализируйте папку или проект.",
                "FILESYSTEM_ANALYSIS_REQUIRED", action="recommendations",
            )
        recommendations = build_recommendations(self._analysis_snapshot)
        return self._result(
            started, True, recommendations["text"], None,
            action="recommendations", path=self._analysis_snapshot["root"],
            recommendations=recommendations,
        )

    @staticmethod
    def _analysis_request(query: str, context: dict | None = None) -> Path:
        context = dict(context or {})
        structured_path = context.get("path") or context.get("folder")
        if structured_path:
            return Path(str(structured_path)).expanduser()
        text = " ".join(str(query or "").split())
        match = re.search(
            r'(?:проанализируй\s+(?:папку|каталог|директорию|проект|копию\s+проекта)|'
            r'анализ\s+(?:папки|каталога|директории|проекта)|'
            r'покажи,?\s+что\s+можно\s+(?:безопасно\s+)?удалить\s+из\s+(?:папки|каталога|директории|проекта)|'
            r'что\s+можно\s+(?:безопасно\s+)?удалить\s+из\s+проекта|analyze\s+folder)\s+'
            r'(?:"([^"]+)"|(.+?))(?=\s+(?:и\s+покажи|and\s+show)|$)',
            text, re.IGNORECASE,
        )
        if not match:
            read_match = re.search(
                r'\b(?:папк\w*|каталог\w*|директори\w*|folder|directory)\s+'
                r'(?:"([^"]+)"|([^\s?!,;]+))',
                text,
                re.IGNORECASE,
            )
            if not read_match:
                raise ValueError("не удалось однозначно определить папку")
            return Path(read_match.group(1) or read_match.group(2)).expanduser()
        return Path(match.group(1) or match.group(2)).expanduser()

    def _prepare_cleanup(self, query: str, started: float) -> dict:
        if self._analysis_snapshot is None:
            return self._result(
                started, False, "Сначала проанализируйте папку. Путь не выбирается автоматически.",
                "FILESYSTEM_ANALYSIS_REQUIRED", action="cleanup_selection",
            )
        selected, forbidden = self._selected_categories(query)
        if forbidden:
            return self._result(
                started, False,
                f"Категория {', '.join(CATEGORY_LABELS[item] for item in forbidden)} не удаляется автоматически.",
                "FILESYSTEM_CLEANUP_CATEGORY_FORBIDDEN", action="cleanup_selection",
                forbidden_categories=forbidden,
            )
        if not selected:
            return self._result(
                started, False, "Не удалось определить разрешённую категорию очистки.",
                "FILESYSTEM_CLEANUP_UNKNOWN_CATEGORY", action="cleanup_selection",
            )
        try:
            plan = self._cleanup_plan(selected)
        except (OSError, ValueError) as exc:
            return self._result(
                started, False, f"План очистки не создан: {exc}",
                "FILESYSTEM_CLEANUP_SNAPSHOT_STALE", action="cleanup_selection",
                exception_type=type(exc).__name__,
            )
        if plan["file_count"] == 0 and plan["folder_count"] == 0:
            return self._result(
                started, True, "Безопасных объектов для удаления не обнаружено.",
                None, action="cleanup_selection", state="completed",
                path=str(plan["path"]), selected_categories=selected,
                file_count=0, folder_count=0, total_bytes=0, deleted_count=0,
            )
        self._pending_delete = plan
        self._delete_confirmation_closed = False
        labels = [CATEGORY_LABELS[item] for item in selected]
        return self._result(
            started, False,
            f"Требуется подтверждение очистки: {plan['path']}. Категории: {', '.join(labels)}. "
            f"Файлов: {plan['file_count']}; папок: {plan['folder_count']}; "
            f"объём: {plan['total_bytes']} байт. Удаление окончательное. Ответьте «Да».",
            "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED", action="delete",
            state="awaiting_confirmation", mode="selection", path=str(plan["path"]),
            selected_categories=selected, file_count=plan["file_count"],
            folder_count=plan["folder_count"], total_bytes=plan["total_bytes"],
            planned_paths=[str(item) for item in plan["files"] + plan["folders"]],
            deleted_count=0,
        )

    @staticmethod
    def _selected_categories(query: str) -> tuple[list[str], list[str]]:
        q = " ".join(str(query or "").casefold().split())
        if "всё безопасное" in q or "все безопасное" in q or "рекомендованное" in q:
            return list(SAFE_CATEGORIES), []
        selected = []
        mapping = (
            ("backup_files", ("резерв", "backup")),
            ("python_cache", ("python-кэш", "python кэш", "кэш", "cache")),
            ("logs", ("логи", "журналы", " logs")),
            ("temporary_files", ("временные", "temporary", " temp")),
            ("generated_images", ("сгенерированные изображ", "generated images")),
            ("test_audit_reports", ("отчёты", "отчеты", "аудит", "reports")),
        )
        for category, markers in mapping:
            if any(marker in q for marker in markers):
                selected.append(category)
        forbidden = []
        if "дубликат" in q or "duplicate" in q:
            forbidden.append("duplicates")
        if "крупные файл" in q or "large file" in q:
            forbidden.append("large_files")
        return selected, forbidden

    def _cleanup_plan(self, selected: list[str]) -> dict:
        snapshot = self._analysis_snapshot
        root = self._approved(Path(snapshot["root"]))
        selected_entries = [item for item in snapshot["entries"] if item["category"] in selected]
        files = [Path(item["path"]) for item in selected_entries if item["kind"] == "file"]
        folders = [Path(item["path"]) for item in selected_entries if item["kind"] == "directory"]
        fingerprints = {item["path"]: tuple(item["fingerprint"]) for item in selected_entries}
        plan = {
            "mode": "selection", "path": root, "selected_categories": list(selected),
            "files": files, "folders": folders, "file_count": len(files),
            "folder_count": len(folders),
            "total_bytes": sum(item["size"] for item in selected_entries if item["kind"] == "file"),
            "fingerprints": fingerprints,
        }
        self._revalidate_cleanup_plan(plan)
        return plan

    def _revalidate_cleanup_plan(self, plan: dict) -> dict:
        root = self._approved(Path(plan["path"]))
        expected = set(plan["fingerprints"])
        for value in plan["files"] + plan["folders"]:
            path = self._approved(Path(value))
            if not path.exists() or not path.is_relative_to(root):
                raise ValueError(f"объект исчез или вышел за пределы анализа: {path}")
            self._validate_delete_object(path)
            actual = analysis_fingerprint(path)
            if actual != tuple(plan["fingerprints"][str(path)]):
                raise ValueError(f"объект изменился после анализа: {path}")
            category = classify_analysis_path(path, root, is_dir=path.is_dir())
            if category not in plan["selected_categories"]:
                raise ValueError(f"категория объекта изменилась: {path}")
        for folder in plan["folders"]:
            folder = Path(folder)
            descendants = {str(item) for item in folder.rglob("*")}
            if not descendants.issubset(expected):
                raise ValueError(f"содержимое папки изменилось после анализа: {folder}")
        return plan

    def _prepare_delete(self, query: str, started: float) -> dict:
        try:
            mode, requested = self._delete_request(query)
            path = self._approved_delete_path(requested)
            plan = self._delete_plan(mode, path)
            self._pending_delete = plan
            self._delete_confirmation_closed = False
            operation = {
                "file": "удаление одного файла",
                "files": "удаление файлов первого уровня",
                "folder": "рекурсивное удаление папки",
            }[mode]
            return self._result(
                started, False,
                f"Требуется подтверждение: {operation}: {path}. "
                f"Файлов: {plan['file_count']}; папок: {plan['folder_count']}. "
                "Удаление окончательное. Ответьте «Да» или «Подтверждаю удаление».",
                "FILESYSTEM_DELETE_CONFIRMATION_REQUIRED",
                action="delete", state="awaiting_confirmation", mode=mode,
                path=str(path), file_count=plan["file_count"],
                folder_count=plan["folder_count"], deleted_count=0,
            )
        except FileNotFoundError:
            return self._result(
                started, False, "Удаляемый объект не существует.",
                "FILESYSTEM_SOURCE_NOT_FOUND", action="delete",
            )
        except ValueError as exc:
            return self._result(
                started, False, f"Удаление заблокировано: {exc}",
                self._delete_error_code(exc), action="delete",
            )
        except OSError as exc:
            return self._result(
                started, False, f"Предварительная проверка удаления не выполнена: {exc}",
                "FILESYSTEM_DELETE_PREFLIGHT_FAILED", action="delete",
                exception_type=type(exc).__name__,
            )

    @staticmethod
    def _delete_request(query: str) -> tuple[str, Path]:
        text = " ".join(str(query or "").split())
        forms = (
            ("files", r'^удал(?:и|ить)\s+все\s+файлы\s+из\s+папки\s+(?:"([^"]+)"|(.+))$'),
            ("folder", r'^удал(?:и|ить)\s+папку\s+(?:"([^"]+)"|(.+))$'),
            ("file", r'^удал(?:и|ить)\s+файл\s+(?:"([^"]+)"|(.+))$'),
            ("folder", r'^delete\s+folder\s+(?:"([^"]+)"|(.+))$'),
            ("file", r'^delete\s+file\s+(?:"([^"]+)"|(.+))$'),
        )
        for mode, expression in forms:
            match = re.match(expression, text, re.IGNORECASE)
            if match:
                return mode, Path(match.group(1) or match.group(2)).expanduser()
        raise ValueError("не удалось однозначно определить тип удаления и путь")

    def _approved_delete_path(self, path: Path) -> Path:
        resolved = self._approved(path)
        if any(resolved == root for root in self.allowed_roots):
            raise ValueError("корень разрешённой области защищён")
        protected = (
            Path(os.environ.get("SystemRoot", "C:/Windows")).resolve(strict=False),
            Path(os.environ.get("ProgramFiles", "C:/Program Files")).resolve(strict=False),
            Path(os.environ.get("ProgramFiles(x86)", "C:/Program Files (x86)")).resolve(strict=False),
            Path.home().resolve(strict=False),
            (Path.home() / "AppData").resolve(strict=False),
            self.root,
        )
        drive_root = Path(resolved.anchor).resolve(strict=False)
        if resolved == drive_root or any(resolved == item for item in protected):
            raise ValueError("путь защищён политикой удаления")
        return resolved

    def _delete_plan(self, mode: str, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(str(path))
        self._validate_delete_object(path)
        if mode == "file":
            if not path.is_file():
                raise ValueError("указанный путь не является обычным файлом")
            files, folders = [path], []
        elif mode == "files":
            if not path.is_dir():
                raise ValueError("указанный путь не является папкой")
            files = []
            for item in sorted(path.iterdir(), key=lambda value: (value.name.casefold(), value.name)):
                if self._is_special(item):
                    if item.is_file() or not item.is_dir():
                        raise ValueError(f"обнаружен специальный объект: {item}")
                    continue
                if item.is_file():
                    self._validate_delete_object(item)
                    files.append(item)
            folders = []
        else:
            if not path.is_dir():
                raise ValueError("указанный путь не является папкой")
            files, folders = self._walk_delete_tree(path)
        objects = files + folders
        return {
            "mode": mode, "path": path, "files": files, "folders": folders,
            "file_count": len(files), "folder_count": len(folders),
            "fingerprints": {str(item): self._delete_fingerprint(item) for item in objects},
        }

    def _walk_delete_tree(self, root: Path) -> tuple[list[Path], list[Path]]:
        files = []
        folders = [root]
        stack = [root]
        while stack:
            folder = stack.pop()
            with os.scandir(folder) as entries:
                ordered = sorted(entries, key=lambda entry: (entry.name.casefold(), entry.name))
            for entry in ordered:
                item = Path(entry.path)
                self._validate_delete_object(item)
                if entry.is_file(follow_symlinks=False):
                    files.append(item)
                elif entry.is_dir(follow_symlinks=False):
                    folders.append(item)
                    stack.append(item)
                else:
                    raise ValueError(f"обнаружен специальный объект: {item}")
        return files, folders

    @staticmethod
    def _file_attributes(path: Path) -> int:
        return int(getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0))

    def _is_special(self, path: Path) -> bool:
        attributes = self._file_attributes(path)
        return path.is_symlink() or bool(attributes & 0x400)

    def _validate_delete_object(self, path: Path) -> None:
        attributes = self._file_attributes(path)
        if path.is_symlink() or attributes & 0x400:
            raise ValueError(f"обнаружена ссылка или reparse point: {path}")
        if attributes & (0x2 | 0x4):
            raise ValueError(f"обнаружен скрытый или системный объект: {path}")
        if not os.access(path, os.W_OK) or not os.access(path.parent, os.W_OK):
            raise ValueError(f"нет подтверждённого доступа на удаление: {path}")

    def _delete_fingerprint(self, path: Path) -> tuple:
        details = path.stat(follow_symlinks=False)
        return (
            details.st_dev, details.st_ino, details.st_mode, details.st_size,
            details.st_mtime_ns, self._file_attributes(path),
        )

    @staticmethod
    def _delete_error_code(exc: ValueError) -> str:
        reason = str(exc).casefold()
        if "allowed roots" in reason or "разрешённой области" in reason or "защищён" in reason:
            return "FILESYSTEM_DELETE_PATH_FORBIDDEN"
        if "ссылк" in reason or "reparse" in reason or "специальн" in reason:
            return "FILESYSTEM_DELETE_SPECIAL_OBJECT"
        if "скрыт" in reason or "системн" in reason:
            return "FILESYSTEM_DELETE_PROTECTED_OBJECT"
        return "FILESYSTEM_DELETE_INVALID_REQUEST"

    def _resolve_delete_confirmation(self, query: str, started: float) -> dict:
        answer = " ".join(str(query or "").casefold().split()).strip(" .!?")
        cancel = {"нет", "отмена", "не удаляй", "отменить"}
        confirm = {"да", "подтверждаю", "подтверждаю удаление", "удалить"}
        if answer in cancel:
            plan = self._pending_delete
            self._pending_delete = None
            self._delete_confirmation_closed = True
            return self._result(
                started, False, "Удаление отменено. Файловая система не изменена.",
                "FILESYSTEM_DELETE_CANCELLED", action="delete", state="cancelled",
                path=str(plan["path"]), deleted_count=0,
            )
        if answer not in confirm:
            plan = self._pending_delete
            self._pending_delete = None
            self._delete_confirmation_closed = True
            return self._result(
                started, False,
                "Ответ не является явным подтверждением. Удаление отменено без изменений.",
                "FILESYSTEM_DELETE_CONFIRMATION_NOT_ACCEPTED", action="delete",
                state="cancelled", path=str(plan["path"]), deleted_count=0,
            )
        plan = self._pending_delete
        self._pending_delete = None
        self._delete_confirmation_closed = True
        return self._execute_delete(plan, started)

    @staticmethod
    def _is_delete_response(query: str) -> bool:
        answer = " ".join(str(query or "").casefold().split()).strip(" .!?")
        return answer in {
            "да", "подтверждаю", "подтверждаю удаление", "удалить",
            "нет", "отмена", "не удаляй", "отменить",
        }

    def _execute_delete(self, plan: dict, started: float) -> dict:
        try:
            current = (
                self._revalidate_cleanup_plan(plan)
                if plan["mode"] == "selection"
                else self._delete_plan(plan["mode"], plan["path"])
            )
            if current["fingerprints"] != plan["fingerprints"]:
                return self._result(
                    started, False, "Объекты изменились после запроса подтверждения.",
                    "FILESYSTEM_DELETE_PLAN_CHANGED", action="delete",
                    path=str(plan["path"]), deleted_count=0,
                )
        except (OSError, ValueError, FileNotFoundError) as exc:
            return self._result(
                started, False, f"Повторная проверка удаления не пройдена: {exc}",
                "FILESYSTEM_DELETE_REVALIDATION_FAILED", action="delete",
                path=str(plan["path"]), deleted_count=0,
            )

        removed = []
        targets = list(current["files"])
        if current["mode"] in {"folder", "selection"}:
            targets.extend(sorted(current["folders"], key=lambda item: len(item.parts), reverse=True))
        try:
            for item in targets:
                if item.is_dir():
                    item.rmdir()
                else:
                    item.unlink()
                removed.append(str(item))
        except OSError as exc:
            return self._result(
                started, False,
                f"Удаление остановлено после частичного выполнения: {exc}",
                "FILESYSTEM_DELETE_PARTIAL_FAILURE", action="delete",
                path=str(plan["path"]), deleted_count=len(removed), deleted=removed,
                failed=[str(item)], exception_type=type(exc).__name__,
            )
        if current["mode"] == "folder" and current["path"].exists():
            return self._result(
                started, False, "Корневая папка осталась после удаления.",
                "FILESYSTEM_DELETE_PARTIAL_FAILURE", action="delete",
                path=str(plan["path"]), deleted_count=len(removed), deleted=removed,
            )
        return self._result(
            started, True,
            f"Удаление завершено. Удалено файлов: {current['file_count']}; "
            f"папок: {current['folder_count']}.",
            None, action="delete", state="completed", path=str(plan["path"]),
            deleted_file_count=current["file_count"],
            deleted_folder_count=current["folder_count"],
            deleted_count=len(removed), deleted=removed,
            freed_bytes=current.get("total_bytes", 0),
            selected_categories=current.get("selected_categories", []),
            skipped_count=0,
        )

    def _move(self, query: str, started: float) -> dict:
        try:
            mode, source, destination = self._move_request(query)
            source = self._approved(source)
            destination = self._approved(destination)
            if not source.exists():
                return self._result(started, False, "Источник не существует.", "FILESYSTEM_SOURCE_NOT_FOUND")
            if source.is_symlink():
                return self._result(started, False, "Перемещение ссылок не поддерживается.", "FILESYSTEM_LINK_NOT_SUPPORTED")
            if mode == "file":
                return self._move_file(source, destination, started)
            if not source.is_dir():
                return self._result(started, False, "Источник не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY")
            if mode == "files":
                return self._move_first_level(source, destination, started)
            return self._move_folder(source, destination, started)
        except (OSError, ValueError) as exc:
            return self._result(
                started, False, f"Перемещение не выполнено: {exc}",
                "FILESYSTEM_MOVE_FAILED", exception_type=type(exc).__name__,
            )

    @staticmethod
    def _move_request(query: str) -> tuple[str, Path, Path]:
        text = " ".join(str(query or "").split())
        forms = (
            ("files", r'^перемести\s+все\s+файлы\s+из\s+папки\s+(?:"([^"]+)"|(.+?))\s+в(?:\s+папку)?\s+(?:"([^"]+)"|(.+))$'),
            ("folder", r'^перемести\s+папку\s+(?:"([^"]+)"|(.+?))\s+в(?:\s+папку)?\s+(?:"([^"]+)"|(.+))$'),
            ("file", r'^перемести\s+файл\s+(?:"([^"]+)"|(.+?))\s+в(?:\s+папку)?\s+(?:"([^"]+)"|(.+))$'),
        )
        for mode, expression in forms:
            match = re.match(expression, text, re.IGNORECASE)
            if match:
                source = Path(match.group(1) or match.group(2)).expanduser()
                destination = Path(match.group(3) or match.group(4)).expanduser()
                return mode, source, destination
        raise ValueError("не удалось определить источник и назначение из запроса")

    def _move_file(self, source: Path, destination: Path, started: float) -> dict:
        if not source.is_file():
            return self._result(started, False, "Источник не является файлом.", "FILESYSTEM_NOT_A_FILE")
        target = destination / source.name if destination.is_dir() or (not destination.exists() and not destination.suffix) else destination
        if target == source:
            return self._result(started, False, "Источник и назначение совпадают.", "FILESYSTEM_MOVE_SAME_PATH")
        if target.exists():
            return self._move_conflict(started, target)
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        return self._move_result(started, source, destination, [(source, target)])

    def _move_first_level(self, source: Path, destination: Path, started: float) -> dict:
        if destination == source:
            return self._result(started, False, "Источник и назначение совпадают.", "FILESYSTEM_MOVE_SAME_PATH")
        if destination.exists() and not destination.is_dir():
            return self._result(started, False, "Назначение не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY")
        files = sorted(
            (item for item in source.iterdir() if item.is_file() and not item.is_symlink()),
            key=lambda item: (item.name.casefold(), item.name),
        )
        changes = [(item, destination / item.name) for item in files]
        conflict = next((target for _, target in changes if target.exists()), None)
        if conflict is not None:
            return self._move_conflict(started, conflict)
        destination.mkdir(parents=True, exist_ok=True)
        staged = []
        try:
            for item, target in changes:
                temporary = source / f".butler_move_{uuid.uuid4().hex}.tmp"
                item.rename(temporary)
                staged.append((item, temporary, target))
            completed = []
            for item, temporary, target in staged:
                temporary.rename(target)
                completed.append((item, target))
        except OSError:
            self._restore_move(staged)
            raise
        return self._move_result(started, source, destination, completed)

    def _move_folder(self, source: Path, destination: Path, started: float) -> dict:
        if destination == source:
            return self._result(started, False, "Источник и назначение совпадают.", "FILESYSTEM_MOVE_SAME_PATH")
        if destination.is_relative_to(source):
            return self._result(started, False, "Нельзя перемещать папку внутрь самой себя.", "FILESYSTEM_MOVE_INTO_SELF")
        links = [item for item in source.rglob("*") if item.is_symlink()]
        if links:
            return self._result(started, False, f"Перемещение ссылок не поддерживается: {links[0].name}", "FILESYSTEM_LINK_NOT_SUPPORTED")
        if destination.exists() and not destination.is_dir():
            return self._result(started, False, "Назначение не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY")
        target_root = destination / source.name
        if target_root == source:
            return self._result(started, False, "Источник и назначение совпадают.", "FILESYSTEM_MOVE_SAME_PATH")
        if target_root.exists():
            return self._move_conflict(started, target_root)
        destination.mkdir(parents=True, exist_ok=True)
        source.rename(target_root)
        changes = [
            (source / item.relative_to(target_root), item)
            for item in target_root.rglob("*") if item.is_file()
        ]
        return self._move_result(started, source, destination, changes, target_root=target_root)

    @staticmethod
    def _restore_move(staged) -> None:
        for source, temporary, target in reversed(staged):
            current = target if target.exists() else temporary
            if current.exists() and not source.exists():
                try:
                    current.rename(source)
                except OSError:
                    pass

    def _move_conflict(self, started: float, target: Path) -> dict:
        return self._result(
            started, False, f"Целевой объект уже существует: {target}",
            "FILESYSTEM_MOVE_CONFLICT", conflict=str(target),
        )

    def _move_result(self, started, source, destination, changes, target_root=None):
        moved = [{"source": str(old), "destination": str(new)} for old, new in changes]
        return self._result(
            started, True, f"Перемещено файлов: {len(moved)}.", None,
            action="move", source=str(source), destination=str(destination),
            target_root=str(target_root) if target_root else None,
            moved_count=len(moved), moved=moved,
        )

    def _copy(self, query: str, started: float) -> dict:
        try:
            mode, source, destination = self._copy_request(query)
            source = self._approved(source)
            destination = self._approved(destination)
            if not source.exists():
                return self._result(started, False, "Источник не существует.", "FILESYSTEM_SOURCE_NOT_FOUND")
            if source.is_symlink():
                return self._result(started, False, "Копирование ссылок не поддерживается.", "FILESYSTEM_LINK_NOT_SUPPORTED")
            if mode == "file":
                return self._copy_file(source, destination, started)
            if not source.is_dir():
                return self._result(started, False, "Источник не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY")
            if mode == "files":
                return self._copy_first_level(source, destination, started)
            return self._copy_folder(source, destination, started)
        except (OSError, ValueError) as exc:
            return self._result(
                started, False, f"Копирование не выполнено: {exc}",
                "FILESYSTEM_COPY_FAILED", exception_type=type(exc).__name__,
            )

    @staticmethod
    def _copy_request(query: str) -> tuple[str, Path, Path]:
        text = " ".join(str(query or "").split())
        forms = (
            ("files", r'^скопируй\s+все\s+файлы\s+из\s+папки\s+(?:"([^"]+)"|(.+?))\s+в\s+(?:"([^"]+)"|(.+))$'),
            ("folder", r'^скопируй\s+папку\s+(?:"([^"]+)"|(.+?))\s+в\s+(?:"([^"]+)"|(.+))$'),
            ("file", r'^скопируй\s+файл\s+(?:"([^"]+)"|(.+?))\s+в\s+(?:"([^"]+)"|(.+))$'),
        )
        for mode, expression in forms:
            match = re.match(expression, text, re.IGNORECASE)
            if match:
                source = Path(match.group(1) or match.group(2)).expanduser()
                destination = Path(match.group(3) or match.group(4)).expanduser()
                return mode, source, destination
        raise ValueError("не удалось определить источник и назначение из запроса")

    def _copy_file(self, source: Path, destination: Path, started: float) -> dict:
        if not source.is_file():
            return self._result(started, False, "Источник не является файлом.", "FILESYSTEM_NOT_A_FILE")
        target = destination / source.name if destination.is_dir() or (not destination.exists() and not destination.suffix) else destination
        if target.exists():
            return self._copy_conflict(started, target)
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(source, target)
        except OSError:
            target.unlink(missing_ok=True)
            raise
        return self._copy_result(started, source, destination, [(source, target)])

    def _copy_first_level(self, source: Path, destination: Path, started: float) -> dict:
        if destination.exists() and not destination.is_dir():
            return self._result(started, False, "Назначение не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY")
        files = sorted(
            (item for item in source.iterdir() if item.is_file() and not item.is_symlink()),
            key=lambda item: (item.name.casefold(), item.name),
        )
        changes = [(item, destination / item.name) for item in files]
        conflict = next((target for _, target in changes if target.exists()), None)
        if conflict is not None:
            return self._copy_conflict(started, conflict)
        destination.mkdir(parents=True, exist_ok=True)
        copied = []
        try:
            for item, target in changes:
                shutil.copy2(item, target)
                copied.append(target)
        except OSError:
            for target in copied:
                target.unlink(missing_ok=True)
            raise
        return self._copy_result(started, source, destination, changes)

    def _copy_folder(self, source: Path, destination: Path, started: float) -> dict:
        if destination == source or destination.is_relative_to(source):
            return self._result(started, False, "Нельзя копировать папку внутрь самой себя.", "FILESYSTEM_COPY_INTO_SELF")
        links = [item for item in source.rglob("*") if item.is_symlink()]
        if links:
            return self._result(started, False, f"Копирование ссылок не поддерживается: {links[0].name}", "FILESYSTEM_LINK_NOT_SUPPORTED")
        if destination.exists() and not destination.is_dir():
            return self._result(started, False, "Назначение не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY")
        target_root = destination / source.name
        if target_root.exists():
            return self._copy_conflict(started, target_root)
        destination.mkdir(parents=True, exist_ok=True)
        temporary = destination / f".butler_copy_{uuid.uuid4().hex}.tmp"
        try:
            shutil.copytree(source, temporary)
            temporary.rename(target_root)
        except OSError:
            if temporary.exists():
                shutil.rmtree(temporary, ignore_errors=True)
            raise
        changes = [
            (item, target_root / item.relative_to(source))
            for item in source.rglob("*") if item.is_file()
        ]
        return self._copy_result(started, source, destination, changes, target_root=target_root)

    def _copy_conflict(self, started: float, target: Path) -> dict:
        return self._result(
            started, False, f"Целевой объект уже существует: {target}",
            "FILESYSTEM_COPY_CONFLICT", conflict=str(target),
        )

    def _copy_result(self, started, source, destination, changes, target_root=None):
        copied = [{"source": str(old), "destination": str(new)} for old, new in changes]
        return self._result(
            started, True, f"Скопировано файлов: {len(copied)}.", None,
            action="copy", source=str(source), destination=str(destination),
            target_root=str(target_root) if target_root else None,
            copied_count=len(copied), copied=copied,
        )

    def _rename_files(self, query: str, started: float) -> dict:
        try:
            folder, pattern = self._rename_request(query)
            folder = self._approved(folder)
            if not folder.exists():
                return self._result(started, False, "Указанная папка не существует.", "FILESYSTEM_FOLDER_NOT_FOUND")
            if not folder.is_dir():
                return self._result(started, False, "Указанный путь не является папкой.", "FILESYSTEM_NOT_A_DIRECTORY")

            token = re.search(r"\{n(?::(\d+)d)?\}", pattern)
            if token is None or len(re.findall(r"\{[^{}]+\}", pattern)) != 1:
                return self._result(started, False, "Шаблон должен содержать {n} или {n:03d}.", "FILESYSTEM_INVALID_RENAME_PATTERN")

            explicit_extension = Path(pattern).suffix
            files = (
                item for item in folder.iterdir()
                if item.is_file() and not item.is_symlink()
            )
            if explicit_extension:
                files = (item for item in files if item.suffix.casefold() == explicit_extension.casefold())
            sources = sorted(files, key=lambda item: (item.name.casefold(), item.name))

            changes = []
            width = int(token.group(1) or 0)
            for number, source in enumerate(sources, 1):
                rendered_number = f"{number:0{width}d}" if width else str(number)
                target_name = pattern[:token.start()] + rendered_number + pattern[token.end():]
                if not explicit_extension:
                    target_name += source.suffix
                self._validate_target_name(folder, target_name)
                changes.append((source, folder / target_name))

            source_keys = {str(source).casefold() for source, _ in changes}
            target_keys = [str(target).casefold() for _, target in changes]
            if len(target_keys) != len(set(target_keys)):
                return self._result(started, False, "Шаблон создаёт повторяющиеся имена.", "FILESYSTEM_RENAME_CONFLICT")
            for source, target in changes:
                if target.exists() and str(target).casefold() not in source_keys and target != source:
                    return self._result(
                        started, False, f"Целевое имя уже занято: {target.name}",
                        "FILESYSTEM_RENAME_CONFLICT", conflict=target.name,
                    )

            pending = [(source, target) for source, target in changes if source != target]
            if not pending:
                return self._rename_result(started, folder, pattern, [])

            staged = []
            try:
                for source, target in pending:
                    temporary = folder / f".butler_rename_{uuid.uuid4().hex}.tmp"
                    source.rename(temporary)
                    staged.append((source, temporary, target))
                completed = []
                for source, temporary, target in staged:
                    temporary.rename(target)
                    completed.append((source, target))
            except OSError as exc:
                self._restore_rename(staged)
                return self._result(
                    started, False, f"Операционная система отказала в переименовании: {exc}",
                    "FILESYSTEM_RENAME_FAILED", exception_type=type(exc).__name__,
                )
            return self._rename_result(started, folder, pattern, completed)
        except (OSError, ValueError) as exc:
            return self._result(
                started, False, f"Переименование не выполнено: {exc}",
                "FILESYSTEM_RENAME_FAILED", exception_type=type(exc).__name__,
            )

    @staticmethod
    def _rename_request(query: str) -> tuple[Path, str]:
        text = " ".join(str(query or "").split())
        match = re.search(
            r'(?:папке|папку|folder)\s+(?:"([^"]+)"|(.+?))\s+(?:в\s+формат|по\s+шаблону|(?:to|as)\s+format)\s+(?:"([^"]+)"|(\S+))',
            text,
            re.IGNORECASE,
        )
        if not match:
            raise ValueError("не удалось определить папку и шаблон из запроса")
        folder = Path(match.group(1) or match.group(2)).expanduser()
        pattern = (match.group(3) or match.group(4)).strip()
        return folder, pattern

    @staticmethod
    def _validate_target_name(folder: Path, name: str) -> None:
        if not name or Path(name).name != name or any(char in name for char in '<>:"/\\|?*'):
            raise ValueError(f"недопустимое имя файла: {name}")
        if len(str(folder / name)) > 259:
            raise ValueError(f"путь превышает ограничение Windows: {name}")

    @staticmethod
    def _restore_rename(staged) -> None:
        for source, temporary, target in reversed(staged):
            current = target if target.exists() else temporary
            if current.exists() and not source.exists():
                try:
                    current.rename(source)
                except OSError:
                    pass

    def _rename_result(self, started, folder, pattern, completed):
        renamed = [{"old_name": source.name, "new_name": target.name} for source, target in completed]
        return self._result(
            started, True,
            f"Переименование выполнено: {len(renamed)} файлов в {folder}.",
            None,
            action="rename", folder=str(folder), pattern=pattern,
            renamed_count=len(renamed), renamed=renamed,
        )

    def _create_folder(self, context: dict) -> ArtifactReference:
        name = self._safe_name(context.get("folder_name"), "Новая папка")
        parent = context.get("parent_folder")
        if parent is not None:
            base = self._folder(parent)
        else:
            location = str(context.get("location") or "workspace").lower()
            base = self.desktop_root if location == "desktop" else self.workspace_root
        target = self._approved(base / name)
        target.mkdir(parents=True, exist_ok=True)
        return self._reference(target, context, "directory")

    def _save_text(self, context: dict) -> Path:
        folder = self._folder(context.get("folder") or self.workspace_root)
        folder.mkdir(parents=True, exist_ok=True)
        filename = self._safe_name(context.get("filename"), "output.txt")
        target = self._approved(folder / filename)
        content = context.get("content")
        if content is None:
            raise ValueError("text content is missing")
        target.write_text(str(content), encoding="utf-8")
        return self._reference(target, context, "file")

    def _save_image(self, context: dict) -> Path:
        folder = self._folder(context.get("folder") or self.workspace_root)
        folder.mkdir(parents=True, exist_ok=True)
        source = Path(str(context.get("source") or "")).expanduser().resolve(strict=False)
        if not source.is_file():
            raise FileNotFoundError(str(source))
        filename = self._safe_name(context.get("filename"), "image.png")
        target = self._approved(folder / filename)
        shutil.copy2(source, target)
        return self._reference(target, context, "image")

    def _folder(self, value) -> Path:
        locator = value.locator if isinstance(value, ArtifactReference) else value
        folder = self._approved(Path(str(locator)))
        if folder.exists() and not folder.is_dir():
            raise ValueError("parent artifact is not a directory")
        return folder

    @staticmethod
    def _reference(path: Path, context: dict, kind: str) -> ArtifactReference:
        artifact_id = str(context.get("artifact_id") or f"{kind}_{uuid.uuid4().hex}")
        return ArtifactReference(artifact_id=artifact_id, kind=kind, _locator=str(path))

    def _approved(self, path: Path) -> Path:
        resolved = path.expanduser().resolve(strict=False)
        if not any(resolved == root or resolved.is_relative_to(root) for root in self.allowed_roots):
            raise ValueError("path is outside allowed roots")
        return resolved

    def _approved_read(self, path: Path) -> Path:
        candidate = path.expanduser()
        if not candidate.is_absolute():
            parts = candidate.parts
            if parts and parts[0].casefold() == "a_06_workspace":
                candidate = self.root / candidate
            else:
                candidate = self.project_workspace_root / candidate
        resolved = candidate.resolve(strict=False)
        if not any(
            resolved == root or resolved.is_relative_to(root)
            for root in self.allowed_read_roots
        ):
            raise ValueError("read path is outside allowed roots")
        return resolved

    @staticmethod
    def _safe_name(value, default: str) -> str:
        name = str(value or default).strip().strip("\"'")
        if not name or name in {".", ".."} or Path(name).name != name:
            raise ValueError("invalid filename")
        return name

    def _result(self, started, ok, text, error, **metadata):
        output = metadata.get("output")
        if output is not None:
            metadata["path"] = output.locator if isinstance(output, ArtifactReference) else str(output)
        return {
            "ok": bool(ok),
            "department": self.NAME,
            "model": "FilesystemDepartment",
            "latency_ms": max(0, int((time.time() - started) * 1000)),
            "text": str(text),
            "error": error,
            "metadata": metadata,
        }
