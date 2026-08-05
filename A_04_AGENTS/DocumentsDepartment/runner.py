# -*- coding: utf-8 -*-
import time
import json
import urllib.request
import re
from datetime import datetime
from pathlib import Path
from A_04_AGENTS.base_department import BaseDepartment

# Пакетный импорт функционального капитала OLD WORLD
from A_03_HANDLERS.text_handler import TextHandler
from A_03_HANDLERS.docx_handler import DocxHandler
from A_03_HANDLERS.spreadsheet_handler import SpreadsheetHandler
from A_03_HANDLERS.pdf_handler import PDFHandler


class DocumentsDepartment(BaseDepartment):
    NAME = "DOCUMENTS"
    VERSION = "1.0"
    CAPABILITIES = (
        "text_extraction", "docx_extraction", "spreadsheet_extraction",
        "pdf_extraction", "optional_local_summary",
    )
    DEPENDENCIES = (
        "TextHandler", "DocxHandler", "SpreadsheetHandler", "PDFHandler",
        "optional Ollama qwen35-ru",
    )
    DATA_READS = ("user-provided document path",)
    DATA_WRITES = ()

    def __init__(self):
        self._active_docx = None
        self.handlers = {
            ".txt": TextHandler(),
            ".md": TextHandler(),
            ".log": TextHandler(),
            ".docx": DocxHandler(),
            ".csv": SpreadsheetHandler(),
            ".xlsx": SpreadsheetHandler(),
            ".pdf": PDFHandler()
        }

    def can_handle(self, query: str, context: dict = None) -> bool:
        q = (query or "").lower()
        absolute_path = re.search(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]', query or "") is not None
        folder_analysis = (
            ("проанализируй" in q or "анализ" in q or "что можно удалить" in q or "что можно безопасно удалить" in q)
            and ("папк" in q or "каталог" in q or "директор" in q)
        )
        project_filesystem_intent = absolute_path and "проект" in q and (
            "проанализируй проект" in q or "проанализируй копию проекта" in q
            or "что можно удалить из проекта" in q or "что можно безопасно удалить из проекта" in q
            or "очисти проект" in q or "очистить проект" in q
        )
        if folder_analysis or project_filesystem_intent:
            return False
        video_exts = (".mp4", ".avi", ".mov", ".mkv", ".webm")
        attachments = (context or {}).get("attachments", [])
        if any(ext in q for ext in video_exts) or any(
            str(path).lower().endswith(video_exts) for path in attachments
        ):
            return False
        open_command = any(command in q for command in ("открой", "открыть", "покажи файл"))
        docx_edit_command = ".docx" in q and any(marker in q for marker in (
            "сделай", "жирн", "курсив", "размер", "центр", "по центру",
            "выровняй", "формат", "заголовок", "основной текст"
        ))
        if open_command and not docx_edit_command:
            return False
        extensions = [".txt", ".md", ".log", ".docx", ".csv", ".xlsx", ".pdf"]
        has_ext = any(ext in q for ext in extensions)
        has_keyword = any(k in q for k in ["прочитай", "документ", "word-документ", "word документ", "word-файл", "word файл", "ворд-документ", "ворд документ", "ворд-файл", "ворд файл", "заголовок", "основной текст", "отчет", "таблица", "скан", "текст файла", "анализ", "сводка",
                                               "объедини pdf", "раздели pdf", "извлеки страниц", "удали страниц", "поверни страниц",
                                               "порядок страниц pdf", "сохрани страниц", "информац", "сколько страниц", "создай pdf"])
        return has_ext or has_keyword

    @staticmethod
    def _quoted(query):
        return re.findall(r'["“](.*?)["”]', query or "")

    def _pdf_request(self, query):
        q = (query or "").lower(); quoted = self._quoted(query)
        page_match = re.search(r"страниц(?:ы|у)?\s+([0-9,\-\s]+)", q)
        pages = page_match.group(1).strip() if page_match else None
        if "информац" in q or "сколько страниц" in q:
            return ("info", {"source": quoted[0]}) if quoted else None
        if "объедини pdf" in q and len(quoted) >= 3:
            return "merge", {"sources": quoted[:-1], "target": quoted[-1]}
        if "раздели pdf" in q and len(quoted) >= 2:
            ranges = re.search(r"диапазонам\s+([0-9,\-\s]+?)\s+в\s+папк", q)
            return "split", {"source": quoted[0], "folder": quoted[-1], "specs": ranges.group(1).strip() if ranges else None}
        if "извлеки страниц" in q and len(quoted) >= 2:
            return "select", {"source": quoted[0], "target": quoted[-1], "spec": pages, "operation": "extract"}
        if "удали страниц" in q and len(quoted) >= 2:
            return "select", {"source": quoted[0], "target": quoted[-1], "spec": pages, "operation": "remove"}
        if "поверни страниц" in q and len(quoted) >= 2:
            angle = re.search(r"на\s+(-?\d+)\s+град", q)
            return "select", {"source": quoted[0], "target": quoted[-1], "spec": pages, "operation": "rotate", "rotation": int(angle.group(1)) if angle else 0}
        if "порядок страниц pdf" in q and len(quoted) >= 2:
            order = re.search(r"на\s+([0-9,\-\s]+?)\s+и\s+сохрани", q)
            return "reorder", {"source": quoted[0], "target": quoted[-1], "spec": order.group(1).strip() if order else ""}
        if "как отдельные pdf" in q and len(quoted) >= 2:
            return "split", {"source": quoted[0], "folder": quoted[-1], "selected": pages}
        if "как png" in q or "как jpg" in q:
            return "unsupported_export", {}
        if "извлеки все изображения" in q:
            return "unsupported_embedded", {}
        if "создай pdf из текста" in q and len(quoted) >= 1:
            # Extract text from first quote, target path from remaining or query
            text_content = quoted[0]
            # Try to find target path after the text
            path_match = re.search(r'в\s+файл\s+["“]?([\w\.\-\/\\]+\.pdf)["”]?', query)
            if path_match:
                target = path_match.group(1)
            else:
                # Default target
                from datetime import datetime
                target = f"Butler_Letter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return "text_to_pdf", {"text": text_content, "target": target}
        if "создай pdf из изображений в папке" in q and len(quoted) >= 2:
            return "folder_to_pdf", {"folder": quoted[0], "target": quoted[-1]}
        if ("создай pdf из изображения" in q or "создай pdf из изображений" in q) and len(quoted) >= 2:
            return "images_to_pdf", {"sources": quoted[:-1], "target": quoted[-1]}
        # Конвертация DOCX в PDF
        if ("преобразуй docx в pdf" in q or "конвертируй docx в pdf" in q or
            "сделай pdf из docx" in q or "из docx в pdf" in q) and len(quoted) >= 2:
            return "convert_docx_to_pdf", {"source": quoted[0], "target": quoted[-1]}
        # Если есть только один файл и сказано сделать PDF - предполагаем DOCX->PDF
        if len(quoted) == 1 and ("сделай pdf" in q or "преобразуй в pdf" in q):
            return "convert_docx_to_pdf", {"source": quoted[0], "target": None}
        return None

    def _extract_file_path(self, text: str) -> str:
        text = (text or "").strip()
        # Ищем от диска (C:) до конца легитимного расширения документа, игнорируя пробелы внутри пути
        match = re.search(r'(?:файл|пут|документ)[а-я]*\s*:\s*([A-Za-z]:.+?\.(?:xlsx|docx|pdf|txt|md|log|csv))', text, re.IGNORECASE)
        if match:
            return match.group(1).strip().strip("\"'").replace("\\", "/")

        if '"' in text:
            try: return text.split('"')[1].strip().replace("\\", "/")
            except: pass
        if "'" in text:
            try: return text.split("'")[1].strip().replace("\\", "/")
            except: pass
        return None

    def _docx_create_request(self, query):
        query = query or ""
        match = re.search(
            r'создай\s+документ\s+(?:["“])?([A-Za-z]:[\\/].+?\.docx)(?:["”])?\s+с\s+текстом\s+["“]([\s\S]*?)["”]\s*$',
            query, re.IGNORECASE,
        )
        if match:
            return match.group(1).strip(), match.group(2)

        intent = re.search(
            r'(?:создай(?:\s+(?:новый|пустой))?|новый)\s+'
            r'(?:(?:word|ворд)[-\s]?)?(?:документ|файл)\b',
            query,
            re.IGNORECASE,
        )
        if not intent:
            return None

        tail = query[intent.end():].strip()

        title_text = re.search(
            r'с\s+заголовк\w*\s*["“«]([\s\S]*?)["”»]\s+и\s+текст\w*\s*["“«]([\s\S]*?)["”»]',
            tail,
            re.IGNORECASE,
        )
        if title_text:
            text = f"{title_text.group(1).strip()}\n\n{title_text.group(2).strip()}"
        else:
            text = None

        quoted_text = re.search(
            r'(?:с\s+текстом|и\s+напиши)\s*:?[\s]*["“«]([\s\S]*?)["”»]',
            tail,
            re.IGNORECASE,
        )
        if text is not None:
            pass
        elif quoted_text:
            quoted_parts = re.findall(r'["“«]([\s\S]*?)["”»]', tail)
            text = "\n".join(part.strip() for part in quoted_parts) if quoted_parts else quoted_text.group(1)
        else:
            two_paragraphs = re.search(
                r'с\s+двумя\s+абзацами\s*:\s*([\s\S]+?)\s+и\s+([\s\S]+?)\s*$',
                tail, re.IGNORECASE,
            )
            if two_paragraphs:
                text = f"{two_paragraphs.group(1).strip()}\n{two_paragraphs.group(2).strip()}"
            else:
                colon_text = re.search(
                    r'с\s+текстом\s*:\s*([\s\S]+?)(?:\s+и\s+сохрани|\s*$)',
                    tail,
                    re.IGNORECASE,
                )
                text = colon_text.group(1).strip() if colon_text else ""

        desktop_requested = bool(re.search(
            r'(?:на|в)\s+рабоч(?:ий|ем)\s+стол(?:е)?',
            query,
            re.IGNORECASE,
        ))
        if desktop_requested:
            target_dir = Path.home() / "Desktop"
        else:
            target_dir = Path(__file__).resolve().parents[2] / "A_06_WORKSPACE" / "STAGE4_OUTPUT"

        filename = f"Butler_Document_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.docx"
        return str(target_dir / filename), text

    @staticmethod
    def _docx_format_request(query):
        q = (query or "").lower().strip().rstrip(".!?")
        if "заголовок" in q and "жирн" in q:
            return "bold_title", None
        if "заголовок" in q and ("центр" in q or "по центру" in q):
            return "center_title", None
        if "заголовок" in q and ("увелич" in q or "размер" in q):
            size = re.search(r"\b(\d+(?:[.,]\d+)?)\b", q)
            if size:
                return "title_font_size", float(size.group(1).replace(",", "."))
            return "invalid", None
        if "основн" in q and "текст" in q and ("по ширине" in q or "выровн" in q):
            return "justify_body", None
        if re.fullmatch(r"сохрани(?:ть)?\s+(?:word[-\s]?)?документ", q):
            return "save", None
        if any(word in q for word in ("жирн", "центр", "шрифт", "формат", "выровн")):
            return "invalid", None
        return None

    def _xlsx_create_request(self, query):
        match = re.search(
            r'создай\s+таблицу\s+(?:["“])?([A-Za-z]:[\\/].+?\.xlsx)(?:["”])?\s+с\s+данными\s*:\s*([\s\S]+?)\s*$',
            query or "", re.IGNORECASE,
        )
        if not match:
            return None
        rows = [[cell.strip() for cell in row.split(",")] for row in match.group(2).split(";") if row.strip()]
        return match.group(1).strip(), rows

    def _csv_create_request(self, query):
        match = re.search(
            r'создай\s+csv\s+(?:["“])?([A-Za-z]:[\\/].+?\.csv)(?:["”])?(?:\s+с\s+данными\s*:\s*([\s\S]*?))?\s*$',
            query or "", re.IGNORECASE,
        )
        if not match:
            return None
        data = (match.group(2) or "").strip()
        rows = [[cell.strip() for cell in row.split(",")] for row in data.split(";") if row.strip()] if data else []
        return match.group(1).strip(), rows

    def _call_local_llm(self, user_query: str, document_text: str) -> str:
        url = "http://127.0.0.1:11434/api/generate"
        prompt = (
            "Ты — аналитический модуль системы Батлер.\n"
            "Твоя задача — проанализировать извлеченный текст документа и составить краткую, "
            "структурированную, человекочитаемую выжимку.\n"
            "Выдели самую суть, ключевые цифры, даты, обязательства или итоговые показатели.\n"
            "Отвечай четко, по делу, без вводных фраз и вступлений.\n\n"
            f"ЗАПРОС ПОЛЬЗОВАТЕЛЬЯ: {user_query}\n"
            f"ТЕКСТ ДОКУМЕНТА:\n{document_text}"
        )

        data = json.dumps({
            "model": "qwen35-ru:latest",
            "prompt": prompt,
            "stream": False
        }).encode("utf-8")

        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=25) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            answer = res_json.get("response", "").strip()
            return re.sub(r"<think>.*?</think>\s*", "", answer, flags=re.DOTALL | re.IGNORECASE).strip()

    def _parse_edit_commands(self, query: str) -> list | None:
        """
        Использует TaskDecomposer для извлечения команд редактирования.
        Возвращает список словарей для универсального 'edit' или None.
        """
        try:
            decomposer = TaskDecomposer()
            intents = decomposer.decompose(query)
            edits = []
            for intent in intents:
                if 'italic' in intent.requested_action.lower() or 'bold' in intent.requested_action.lower() or 'format' in intent.requested_action.lower():
                    target = 'title' if 'title' in intent.source_text.lower() else 'paragraph'
                    style = 'italic' if 'italic' in intent.requested_action.lower() else 'bold'
                    value = intent.arguments.get('text', '')
                    edits.append({'target': target, 'style': style, 'value': value})
            return edits if edits else None
        except Exception:
            return None

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        context = dict(context or {})
        # Semantic Task Contract from SmartDispatcherV2
        semantic_contract = context.get("semantic_contract", {})

        # Если contract отсутствует — работать по существующей логике
        if not semantic_contract:
            pass  # Продолжаем выполнение существующей логики
        elif not semantic_contract.get("execution_ready"):
            # execution_ready == false: не выполняем операции, возвращаем missing_information
            missing = semantic_contract.get("missing_information", [])
            return {
                "ok": False,
                "department": self.NAME,
                "model": "SemanticReasoningEngine",
                "latency_ms": max(0, int((time.time() - start) * 1000)),
                "text": "Недостаточно информации для выполнения задачи:\n" + "\n".join(f"• {item}" for item in missing),
                "error": None,
                "metadata": {
                    "semantic_contract_missing_information": missing,
                    "execution_ready": False
                }
            }

        attachments = context.get("attachments", [])

        if context.get("capability_action") == "create_docx":
            target = context.get("output_path")
            if not target:
                desktop_requested = bool(re.search(
                    r'(?:на|в)\s+рабоч(?:ий|ем)\s+стол(?:е)?',
                    query,
                    re.IGNORECASE,
                ))
                if desktop_requested:
                    target_dir = Path.home() / "Desktop"
                else:
                    target_dir = Path(__file__).resolve().parents[2] / "A_06_WORKSPACE" / "exports"
                target_dir.mkdir(parents=True, exist_ok=True)
                target = target_dir / f"Butler_Result_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.docx"
            text = str(context.get("content") or context.get("previous_result") or query)
            result = self.handlers[".docx"].create_from_text(target, text, open_after_create=True)
            if result.get("success"):
                self._active_docx = Path(target)
                metadata = dict(result.get("metadata") or {})
                metadata["output"] = str(target)
                return {"ok": True, "department": self.NAME, "model": "DocxHandler",
                        "latency_ms": max(0, int((time.time() - start) * 1000)),
                        "text": result.get("text", "DOCX успешно создан."), "error": None,
                        "metadata": metadata}
            return self._error_result(start, result.get("error", "CREATE_FAILED"),
                                      result.get("text", "Не удалось создать DOCX."),
                                      model="DocxHandler", metadata=result.get("metadata", {}))

                # Проверяем универсальные команды редактирования
        docx_edit_commands = self._parse_edit_commands(query)
        if docx_edit_commands:
            path_match = re.search(r'["“«]?([A-Za-z]:[\\/][^"”»\r\n]+?\.docx)["”»]?', query or '', re.IGNORECASE)
            target_docx = Path(path_match.group(1)) if path_match else self._active_docx
            if target_docx is None or not target_docx.is_file():
                return self._error_result(start, 'DOCUMENT_NOT_FOUND', 'Указанный Word-документ не найден.', model='DocxHandler')
            result = self.handlers['.docx'].format_document(target_docx, 'edit', docx_edit_commands)
            if result.get('success'):
                return {'ok': True, 'department': self.NAME, 'model': 'DocxHandler', 'latency_ms': max(0, int((time.time() - start) * 1000)), 'text': result.get('text', 'Оформление DOCX применено.'), 'error': None, 'metadata': result.get('metadata', {})}
            return self._error_result(start, result.get('error', 'EDIT_FAILED'), result.get('text', 'Не удалось применить оформление.'), model='DocxHandler', metadata=result.get('metadata', {}))
        # Fallback: старая точечная логика
        docx_format = self._docx_format_request(query)
        if docx_format:
            operation, value = docx_format
            if operation == "invalid":
                return self._error_result(
                    start, "INVALID_COMMAND",
                    "Команда оформления документа не поддерживается.", model="DocxHandler",
                )
            # If an explicit DOCX path is present, edit exactly that document.
            path_match = re.search(
                r'["“«]?([A-Za-z]:[\\/][^"”»\r\n]+?\.docx)["”»]?',
                query or "",
                re.IGNORECASE,
            )
            target_docx = Path(path_match.group(1)) if path_match else self._active_docx

            if target_docx is None or not target_docx.is_file():
                return self._error_result(
                    start, "DOCUMENT_NOT_FOUND",
                    "Указанный Word-документ не найден.", model="DocxHandler",
                )

            self._active_docx = target_docx
            result = self.handlers[".docx"].format_document(
                target_docx, operation, value,
            )
            if result.get("success"):
                return {
                    "ok": True, "department": self.NAME, "model": "DocxHandler",
                    "latency_ms": max(0, int((time.time() - start) * 1000)),
                    "text": result.get("text", "Оформление DOCX применено."), "error": None,
                    "metadata": result.get("metadata", {}),
                }
            return self._error_result(
                start, result.get("error", "FORMATTING_FAILED"),
                result.get("text", "Не удалось применить оформление DOCX."),
                model="DocxHandler", metadata=result.get("metadata", {}),
            )

        docx_create = self._docx_create_request(query)
        if docx_create:
            target, text = docx_create
            result = self.handlers[".docx"].create_from_text(target, text, open_after_create=True)
            if result.get("success"):
                self._active_docx = Path(target)
                return {
                    "ok": True, "department": self.NAME, "model": "DocxHandler",
                    "latency_ms": max(0, int((time.time() - start) * 1000)),
                    "text": result.get("text", "DOCX успешно создан."), "error": None,
                    "metadata": result.get("metadata", {}),
                }
            return self._error_result(
                start, result.get("error", "CREATE_FAILED"), result.get("text", "Не удалось создать DOCX."),
                model="DocxHandler", metadata=result.get("metadata", {}),
            )

        xlsx_create = self._xlsx_create_request(query)
        if xlsx_create:
            target, rows = xlsx_create
            result = self.handlers[".xlsx"].create_xlsx(target, rows)
            if result.get("success"):
                return {
                    "ok": True, "department": self.NAME, "model": "SpreadsheetHandler",
                    "latency_ms": max(0, int((time.time() - start) * 1000)),
                    "text": result.get("text", "XLSX успешно создан."), "error": None,
                    "metadata": result.get("metadata", {}),
                }
            return self._error_result(
                start, result.get("error", "CREATE_FAILED"), result.get("text", "Не удалось создать XLSX."),
                model="SpreadsheetHandler", metadata=result.get("metadata", {}),
            )

        csv_create = self._csv_create_request(query)
        if csv_create:
            target, rows = csv_create
            result = self.handlers[".csv"].create_csv(target, rows)
            if result.get("success"):
                return {
                    "ok": True, "department": self.NAME, "model": "SpreadsheetHandler",
                    "latency_ms": max(0, int((time.time() - start) * 1000)),
                    "text": result.get("text", "CSV успешно создан."), "error": None,
                    "metadata": result.get("metadata", {}),
                }
            return self._error_result(
                start, result.get("error", "CREATE_FAILED"), result.get("text", "Не удалось создать CSV."),
                model="SpreadsheetHandler", metadata=result.get("metadata", {}),
            )

        pdf_request = self._pdf_request(query)
        if pdf_request:
            operation, arguments = pdf_request
            handler = self.handlers[".pdf"]
            try:
                metadata = handler.operate(operation, **arguments)
                metadata["duration_ms"] = max(0, int((time.time() - start) * 1000))
                return {"ok": True, "department": self.NAME, "model": "PDFHandler",
                        "latency_ms": metadata["duration_ms"], "text": "PDF-операция успешно выполнена.",
                        "error": None, "metadata": metadata}
            except Exception as exc:
                from A_03_HANDLERS.pdf_operations import PDFOperationError
                code = exc.code if isinstance(exc, PDFOperationError) else "PDF_OPERATION_FAILED"
                return self._error_result(start, code, f"PDF-операция не выполнена: {exc}", model="PDFHandler",
                                          metadata={"operation": operation, "duration_ms": max(0, int((time.time() - start) * 1000))})

        if not isinstance(attachments, (list, tuple)):
            return self._error_result(
                start, "INVALID_ATTACHMENTS",
                "Ошибка: attachments должен быть списком путей."
            )

        if attachments:
            file_path_str = str(attachments[0]).strip().strip("\"'")
        else:
            file_path_str = self._extract_file_path(query)

        if not file_path_str:
            return self._error_result(
                start, "MISSING_ATTACHMENT",
                "Ошибка: Путь к документу не найден в запросе."
            )

        file_path = Path(file_path_str)
        if not file_path.exists():
            return self._error_result(
                start, "FILE_NOT_FOUND",
                f"Ошибка: Файл не найден по пути {file_path}",
                path=file_path,
            )

        if not file_path.is_file():
            return self._error_result(
                start, "NOT_A_FILE",
                f"Ошибка: Указанный путь не является файлом: {file_path}",
                path=file_path,
            )

        ext = file_path.suffix.lower()
        handler = self.handlers.get(ext)

        if not handler:
            return self._error_result(
                start, "UNSUPPORTED_FORMAT",
                f"Ошибка: Расширение {ext} не поддерживается департаментом документов.",
                path=file_path,
            )

        try:
            raw_result = handler.extract(file_path)
            if not raw_result.get("success", False):
                return self._error_result(
                    start,
                    raw_result.get("metadata", {}).get("error", "EXTRACT_FAILED"),
                    "Не удалось извлечь текст из документа.",
                    model=type(handler).__name__,
                    path=file_path,
                    metadata={"raw_metrics": raw_result.get("metadata", {})},
                )

            extracted_text = raw_result.get("text", "")
            if ext == ".docx":
                self._active_docx = file_path
            output_text = extracted_text
            intelligence_active = False

            q_low = (query or "").lower()
            has_trigger = any(k in q_low for k in ["анализ", "сводка", "резюме", "суть", "выжимка"])

            if (len(extracted_text) > 1000 or has_trigger) and extracted_text.strip():
                try:
                    analyzed_text = self._call_local_llm(query or "", extracted_text)
                    if not analyzed_text.strip():
                        raise ValueError("EMPTY_LLM_RESPONSE")
                    output_text = analyzed_text
                    intelligence_active = True
                except Exception as intel_err:
                    output_text = f"[Откат к сырому тексту: ИИ-анализ недоступен из-за ошибки {str(intel_err)}]\n\n{extracted_text}"

            return {
                "ok": True,
                "department": self.NAME,
                "model": f"{type(handler).__name__} + qwen35-ru" if intelligence_active else type(handler).__name__,
                "latency_ms": int((time.time() - start) * 1000),
                "text": output_text,
                "metadata": {
                    "raw_metrics": raw_result.get("metadata", {}),
                    "intelligence_layer": intelligence_active,
                    "text_length": len(extracted_text),
                    "path": str(file_path),
                    "format": ext,
                },
                "error": None
            }

        except Exception as exc:
            return self._error_result(
                start, "DOCUMENT_HANDLER_ERROR",
                f"Критический сбой хендлера при обработке файла {file_path.name}.",
                model=type(handler).__name__,
                path=file_path,
                metadata={"exception_type": type(exc).__name__},
            )

    def _error_result(self, start, error, text, model=None, path=None, metadata=None):
        result_metadata = dict(metadata or {})
        if path is not None:
            result_metadata["path"] = str(path)
            result_metadata["format"] = path.suffix.lower()
        return {
            "ok": False,
            "department": self.NAME,
            "model": model,
            "latency_ms": max(0, int((time.time() - start) * 1000)),
            "text": text,
            "error": str(error),
            "metadata": result_metadata,
        }
