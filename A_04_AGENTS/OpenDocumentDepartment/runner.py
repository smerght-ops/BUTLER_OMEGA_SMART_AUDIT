# -*- coding: utf-8 -*-
import os
import re
import time
import logging
import traceback
from pathlib import Path
from A_04_AGENTS.base_department import BaseDepartment
from A_07_MEMORY.SESSION.reference_resolver import ReferenceResolver

logger = logging.getLogger("ButlerOS.OpenDocumentDepartment")

class OpenDocumentDepartment(BaseDepartment):
    NAME = "OPEN_DOCUMENT"
    VERSION = "1.0"
    CAPABILITIES = ("resolve_search_reference", "open_local_document")
    DEPENDENCIES = ("A_07_MEMORY.SESSION.reference_resolver.ReferenceResolver", "Windows Shell")
    DATA_READS = ("Search session context", "resolved local file path")
    DATA_WRITES = ()
    SUPPORTED_EXTENSIONS = {
        ".txt", ".md", ".log", ".docx", ".csv", ".xlsx", ".pdf",
        ".jpg", ".jpeg", ".png", ".webp",
    }

    def __init__(self):
        self.resolver = ReferenceResolver()
        self._opener = os.startfile
        self.TRIGGERS = ["открой", "запусти", "покажи", "открыть", "показать"]

    def can_handle(self, query: str, context: dict = None) -> bool:
        q = (query or "").lower()

        if ".pdf" in q and ("информац" in q or "сколько страниц" in q):
            return False

        if any(archive in q for archive in (".zip", ".tar", ".tgz", ".gz", " zip", " tar", " tgz")):
            return False

        # Системные стоп-слова для защиты департамента памяти
        if any(ignored in q for ignored in ["наблюдения", "бюджет сессии", "контекстный бюджет", "лог"]):
            return False

        has_trigger = any(t in q for t in self.TRIGGERS)
        has_reference = any(r in q for r in ["перв", "втор", "трет", "четвер", "пят", "последн", "тот", "этот", "текущ"])

        # Обязательный маркер работы с физическими файлами
        has_file_marker = any(m in q for m in ["документ", "файл", "отчет", "справка", "реестр", "картинка", "изображение", "лог", ".txt", ".xlsx", ".pdf", ".jpg", ".png", ".webp"])

        return has_trigger and (has_reference or has_file_marker)

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start_time = time.time()
        context = dict(context or {})

        # Direct absolute local path takes precedence over Search session references.
        direct_match = re.search(
            r'["“«]?([A-Za-z]:[\\/][^"”»\r\n]+?\.[A-Za-z0-9]+)["”»]?(?:\s*$)',
            query or "",
            re.IGNORECASE,
        )
        if direct_match:
            direct_path = Path(direct_match.group(1).strip()).expanduser().resolve(strict=False)
            if direct_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                return self._error_result(
                    start_time, "UNSUPPORTED_FORMAT",
                    f"Формат файла не поддерживается: {direct_path.suffix}",
                    path=direct_path,
                )
            if not direct_path.is_file():
                return self._error_result(
                    start_time, "FILE_NOT_FOUND",
                    f"Файл не найден: {direct_path}",
                    path=direct_path,
                )
            try:
                self._opener(str(direct_path))
            except Exception as exc:
                return self._error_result(
                    start_time, "OPEN_FAILED",
                    f"Не удалось открыть файл: {direct_path.name}",
                    path=direct_path,
                    metadata={"exception_type": type(exc).__name__},
                )
            return {
                "ok": True,
                "department": self.NAME,
                "model": "WindowsShell",
                "latency_ms": max(0, int((time.time() - start_time) * 1000)),
                "text": f"Файл открыт: {direct_path}",
                "error": None,
                "metadata": {
                    "filepath": str(direct_path),
                    "absolute_path": str(direct_path),
                    "format": direct_path.suffix.lower(),
                    "open_method": "WindowsShell.os.startfile",
                },
            }

        try:
            resolved = self.resolver.resolve(query)
        except Exception as exc:
            return self._error_result(
                start_time, "REFERENCE_RESOLVER_ERROR",
                "Не удалось получить ссылку на документ из контекста поиска.",
                metadata={
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "traceback": "\n".join(traceback.format_exc().strip().splitlines()[-10:]),
                    "last_executed_step": "ReferenceResolver.resolve",
                    "timeout_location": None,
                    "current_state": "resolver_failed",
                },
            )

        reason = resolved.get("reason", "INVALID_RESOLVER_RESULT")

        if not resolved["ok"]:
            if reason == ReferenceResolver.ERR_EMPTY_CONTEXT:
                text_reply = "Контекст сессии пуст. Пожалуйста, сначала выполните поиск файлов."
            elif reason == ReferenceResolver.ERR_INDEX_OUT_OF_RANGE:
                text_reply = "Запрошенный индекс файла отсутствует в результатах последнего поиска."
            else:
                text_reply = "Не удалось распознать, какой именно файл требуется открыть."

            return self._error_result(start_time, reason, text_reply)

        doc = resolved["document"]

        if not isinstance(doc, dict):
            return self._error_result(
                start_time, "INVALID_DOCUMENT",
                "Ошибка: некорректная структура документа в кэше сессии."
            )

        filepath = doc.get("filepath")
        doc_id = doc.get("id")

        if not filepath:
            return self._error_result(
                start_time, "MISSING_FILEPATH",
                "Ошибка сессии: в кэшированном документе отсутствует путь к файлу."
            )

        attempted_path = str(filepath)
        file_path = Path(filepath).expanduser().resolve(strict=False)
        if doc.get("available") is False or not file_path.exists():
            return self._error_result(
                start_time, "FILE_NOT_FOUND",
                f"Ошибка: целевой файл не найден на диске по пути {filepath}",
                path=file_path,
                metadata={
                    "catalog_available": False,
                    "document_id": doc_id,
                    "attempted_path": attempted_path,
                    "absolute_path": str(file_path),
                    "open_method": "WindowsShell.os.startfile",
                },
            )

        if not file_path.is_file():
            return self._error_result(
                start_time, "NOT_A_FILE",
                f"Ошибка: целевой путь не является файлом: {filepath}",
                path=file_path,
            )

        extension = file_path.suffix.lower()
        if extension not in self.SUPPORTED_EXTENSIONS:
            return self._error_result(
                start_time, "UNSUPPORTED_FORMAT",
                f"Ошибка: тип файла {extension or '<без расширения>'} не поддерживается для открытия.",
                path=file_path,
            )

        file_size = file_path.stat().st_size
        try:
            open_started = time.perf_counter()
            self._opener(str(file_path))
            open_elapsed_ms = int((time.perf_counter() - open_started) * 1000)
        except Exception as exc:
            return self._error_result(
                start_time, "OPEN_FAILED",
                f"Не удалось открыть файл: {file_path.name}.",
                path=file_path,
                metadata={
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                    "elapsed_ms": int((time.perf_counter() - open_started) * 1000),
                    "attempted_path": attempted_path,
                    "absolute_path": str(file_path),
                    "open_method": "WindowsShell.os.startfile",
                    "file_size": file_size,
                    "traceback": "\n".join(traceback.format_exc().strip().splitlines()[-10:]),
                    "last_executed_step": "WindowsShell.os.startfile",
                    "timeout_location": None,
                    "current_state": "open_failed",
                },
            )

        return {
            "ok": True,
            "department": self.NAME,
            "model": "WindowsShell",
            "latency_ms": int((time.time() - start_time) * 1000),
            "text": f"Файл открыт из контекста поиска (ID: {doc_id}). Путь: {filepath}",
            "metadata": {
                "doc_id": doc_id,
                "filepath": str(file_path),
                "attempted_path": attempted_path,
                "absolute_path": str(file_path),
                "open_method": "WindowsShell.os.startfile",
                "elapsed_ms": open_elapsed_ms,
                "file_size": file_size,
                "format": extension,
                "resolver_reason": reason,
                "opened": True,
                "last_executed_step": "WindowsShell.os.startfile returned",
                "timeout_location": "WindowsShell.os.startfile" if open_elapsed_ms > 30000 else None,
                "current_state": "returned_success",
                "open_elapsed_ms": open_elapsed_ms,
            },
            "error": None
        }

    def _error_result(self, start_time, error, text, path=None, metadata=None):
        result_metadata = dict(metadata or {})
        if path is not None:
            result_metadata["filepath"] = str(path)
            result_metadata["format"] = path.suffix.lower()
            result_metadata["opened"] = False
        return {
            "ok": False,
            "department": self.NAME,
            "model": "WindowsShell",
            "latency_ms": max(0, int((time.time() - start_time) * 1000)),
            "text": text,
            "error": str(error),
            "metadata": result_metadata,
        }
