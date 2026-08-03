# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
import time
import uuid
import zipfile
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment


class ArchiveDepartment(BaseDepartment):
    NAME = "ARCHIVE"
    VERSION = "2.1"
    CAPABILITIES = ("create_archive", "extract_archive", "inspect_archive")
    DEPENDENCIES = ("zipfile", "pathlib")
    DATA_READS = ("user-selected ZIP archive or source directory",)
    DATA_WRITES = ("requested ZIP archive or extraction directory",)
    SUPPORTED_EXTENSIONS = {".zip"}

    def can_handle(self, text: str, context: dict = None) -> bool:
        q = " ".join((text or "").casefold().split())
        return (
            any(marker in q for marker in (
                "заархивируй", "упакуй", "распакуй архив",
                "покажи содержимое архива", ".zip",
            ))
            or any(
                Path(str(path)).suffix.casefold() == ".zip"
                for path in (context or {}).get("attachments", [])
            )
        )

    def execute(self, text: str, context: dict = None, **kwargs) -> dict:
        started = time.time()
        try:
            action, source, target = self._request(text, context or {})
            if action == "create":
                return self._create(source, target, started)
            if action == "extract":
                return self._extract(source, target, started)
            return self._inspect(source, started)
        except ArchiveRequestError as exc:
            return self._error(started, exc.code, exc.text, exc.metadata)
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            return self._error(
                started,
                "ARCHIVE_OPERATION_FAILED",
                "Не удалось выполнить операцию с ZIP-архивом.",
                {"exception_type": type(exc).__name__, "exception_message": str(exc)},
            )

    @classmethod
    def _request(cls, text: str, context: dict) -> tuple[str, Path, Path | None]:
        normalized = " ".join(str(text or "").split())
        patterns = (
            ("create", r"^(?:заархивируй|упакуй)(?:\s+папку)?\s+(.+?)\s+в\s+архив\s+(.+)$"),
            ("extract", r"^распакуй\s+архив\s+(.+?)\s+в\s+папку\s+(.+)$"),
            ("inspect", r"^покажи\s+содержимое\s+архива\s+(.+)$"),
        )
        for action, pattern in patterns:
            match = re.match(pattern, normalized, flags=re.IGNORECASE)
            if not match:
                continue
            source = cls._path(match.group(1))
            target = cls._path(match.group(2)) if match.lastindex == 2 else None
            cls._require_absolute(source)
            if target is not None:
                cls._require_absolute(target)
            return action, source, target

        attachments = context.get("attachments", [])
        if attachments:
            source = cls._path(str(attachments[0]))
            cls._require_absolute(source)
            return "inspect", source, None
        raise ArchiveRequestError(
            "ARCHIVE_REQUEST_INVALID",
            "Не удалось определить операцию, исходный путь и путь назначения.",
        )

    @staticmethod
    def _path(value: str) -> Path:
        return Path(str(value).strip().strip('"\''))

    @staticmethod
    def _require_absolute(path: Path) -> None:
        if re.match(r"^[A-Za-z]:[\\/]", str(path)) is None:
            raise ArchiveRequestError(
                "ARCHIVE_PATH_NOT_ABSOLUTE",
                "Поддерживаются только абсолютные Windows-пути.",
                {"path": str(path)},
            )

    def _create(self, source: Path, target: Path, started: float) -> dict:
        if not source.is_dir():
            raise ArchiveRequestError(
                "ARCHIVE_SOURCE_NOT_FOUND", "Исходная папка не найдена.", {"source": str(source)}
            )
        self._require_zip(target)
        if target.exists():
            raise ArchiveRequestError(
                "ARCHIVE_TARGET_EXISTS", "Целевой архив уже существует; перезапись запрещена.",
                {"target": str(target)},
            )

        files = sorted((path for path in source.rglob("*") if path.is_file()), key=str)
        folders = sorted((path for path in source.rglob("*") if path.is_dir()), key=str)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
        try:
            with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
                for folder in folders:
                    archive.writestr(folder.relative_to(source).as_posix().rstrip("/") + "/", b"")
                for item in files:
                    archive.write(item, item.relative_to(source).as_posix())
            os.replace(temporary, target)
        finally:
            if temporary.exists():
                temporary.unlink()

        return self._result(
            started, True, f"ZIP-архив создан: {target}. Файлов: {len(files)}; папок: {len(folders)}.",
            None, action="create", source=str(source), output=str(target),
            file_count=len(files), folder_count=len(folders),
        )

    def _extract(self, source: Path, target: Path, started: float) -> dict:
        if not source.is_file():
            raise ArchiveRequestError("ARCHIVE_NOT_FOUND", "ZIP-архив не найден.", {"source": str(source)})
        self._require_zip(source)
        with zipfile.ZipFile(source) as archive:
            members = archive.infolist()
            destinations = self._validated_destinations(target, members)
            conflicts = [
                str(destination) for info, destination in destinations
                if destination.exists() and (not info.is_dir() or not destination.is_dir())
            ]
            if conflicts:
                raise ArchiveRequestError(
                    "ARCHIVE_EXTRACT_CONFLICT",
                    "Распаковка не начата: целевые объекты уже существуют.",
                    {"conflicts": conflicts},
                )

            target.mkdir(parents=True, exist_ok=True)
            for info, destination in destinations:
                if info.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info, "r") as src, destination.open("xb") as dst:
                    while chunk := src.read(1024 * 1024):
                        dst.write(chunk)

        file_count = sum(not info.is_dir() for info in members)
        folders = self._archive_folders(members)
        return self._result(
            started, True,
            f"ZIP-архив распакован: {target}. Файлов: {file_count}; папок: {len(folders)}.",
            None, action="extract", source=str(source), output=str(target),
            file_count=file_count, folder_count=len(folders),
        )

    def _inspect(self, source: Path, started: float) -> dict:
        if not source.is_file():
            raise ArchiveRequestError("ARCHIVE_NOT_FOUND", "ZIP-архив не найден.", {"source": str(source)})
        self._require_zip(source)
        with zipfile.ZipFile(source) as archive:
            members = archive.infolist()
            entries = [
                {"path": info.filename, "type": "folder" if info.is_dir() else "file", "size": info.file_size}
                for info in members
            ]
        lines = ["Содержимое ZIP-архива:"] + [
            f"{'Папка' if entry['type'] == 'folder' else 'Файл'}: {entry['path']} — {entry['size']} байт"
            for entry in entries
        ]
        return self._result(
            started, True, "\n".join(lines), None,
            action="inspect", source=str(source), read_only=True,
            file_count=sum(entry["type"] == "file" for entry in entries),
            folder_count=len(self._archive_folders(members)), entries=entries,
        )

    @staticmethod
    def _validated_destinations(target: Path, members: list[zipfile.ZipInfo]):
        root = target.resolve()
        destinations = []
        for info in members:
            member = info.filename.replace("\\", "/")
            if member.startswith("/") or re.match(r"^[A-Za-z]:", member):
                raise ArchiveRequestError("ARCHIVE_UNSAFE_PATH", "Архив содержит небезопасный путь.")
            destination = (target / member).resolve()
            try:
                destination.relative_to(root)
            except ValueError:
                raise ArchiveRequestError("ARCHIVE_UNSAFE_PATH", "Архив содержит выход за целевую папку.")
            destinations.append((info, destination))
        return destinations

    @staticmethod
    def _archive_folders(members: list[zipfile.ZipInfo]) -> set[str]:
        folders = set()
        for info in members:
            parts = Path(info.filename.rstrip("/")).parts
            limit = len(parts) if info.is_dir() else len(parts) - 1
            for index in range(1, limit + 1):
                folders.add(Path(*parts[:index]).as_posix())
        return folders

    @staticmethod
    def _require_zip(path: Path) -> None:
        if path.suffix.casefold() != ".zip":
            raise ArchiveRequestError(
                "UNSUPPORTED_ARCHIVE_FORMAT", "Поддерживается только формат ZIP.", {"path": str(path)}
            )

    def _result(self, started, ok, text, error, **metadata):
        return {
            "ok": ok, "department": self.NAME, "model": "ArchiveDepartment",
            "latency_ms": int((time.time() - started) * 1000),
            "text": text, "error": error, "metadata": metadata,
        }

    def _error(self, started, error, text, metadata=None):
        return self._result(started, False, text, error, **dict(metadata or {}))


class ArchiveRequestError(Exception):
    def __init__(self, code: str, text: str, metadata: dict | None = None):
        super().__init__(text)
        self.code = code
        self.text = text
        self.metadata = dict(metadata or {})
