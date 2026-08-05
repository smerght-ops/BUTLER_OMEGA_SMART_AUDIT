from __future__ import annotations
import re
from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class TaskIntent:
    requested_action: str
    action_families: tuple[str, ...]
    object_candidates: tuple[str, ...]
    source_text: str
    missing_action: str | None = None
    depends_on_previous: bool = False
    arguments: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ProjectSpec:
    project_name: str
    count: int
    count_source: str
    location: str = "desktop"


class TaskDecomposer:
    """Deterministic decomposition. It describes needs, not Butler capabilities."""

    _SPLIT = re.compile(
        r"\s*(?:,|;|\n|\bи\s+(?=(?:создай|сохрани|нарисуй|опиши|переведи|найди|"
        r"сделай|скачай|загрузи|извлеки|проверь|сформируй)))\s*", re.I,
    )
    _NUMBER_WORDS = {
        "один": 1, "одно": 1, "одну": 1, "два": 2, "две": 2,
        "три": 3, "четыре": 4, "пять": 5, "шесть": 6,
        "семь": 7, "восемь": 8, "девять": 9, "десять": 10,
    }

    def _semantic_decompose(self, request: str) -> list[TaskIntent]:
        # Словарь для преобразования русских действий в английские capability
        action_map = {
            'открыть': 'open_local_document',
            'сделать_курсивом': 'edit_docx',
            'сделать_жирным': 'edit_docx',
            'отформатировать': 'edit_docx',
            'редактировать': 'edit_docx',
            'изменить': 'edit_docx',
            'сохранить': 'save_document',
            'создать_документ': 'create_docx',
        }
        # После получения интентов от LLM, преобразуем действия
        intents = []
        for idx, item in enumerate(raw):
            if not isinstance(item, dict):
                continue
            action = str(item.get('action', '')).strip()
            obj = str(item.get('object', '')).strip()
            arguments = item.get('arguments', {})
            if not isinstance(arguments, dict):
                arguments = {}
            if not action:
                continue
            # Преобразуем русское действие в английское, если есть
            english_action = action_map.get(action, action)
            # Создаём TaskIntent с английским действием
            if docx_path and 'docx_path' not in arguments:
                arguments['docx_path'] = docx_path
            intent = TaskIntent(
                requested_action=english_action,
                action_families=(english_action,),
                object_candidates=(obj,) if obj else (),
                source_text=request,
                missing_action=None,
                depends_on_previous=(idx > 0),
                arguments=arguments
            )
            intents.append(intent)
        return intents
        """
        Use LLM to decompose a complex request into TaskIntent objects.
        Returns empty list if decomposition fails.
        """
        if not hasattr(self, '_chat_provider'):
            from A_02_MANAGERS.smart_dispatcher import get_chat_provider
            self._chat_provider = get_chat_provider()
        import re
        match = re.search(r'["\']+([^"\']+\.docx)["\']+', request, re.I)
        docx_path = match.group(1) if match else None
        prompt = f"""
        Разбери следующий запрос на последовательные действия, которые может выполнить Butler.
        Для каждого действия укажи:
        - "action": глагол в инфинитиве (например, "открыть", "сохранить", "сделать_курсивом", "извлечь_текст", "скачать", "создать_документ", "проверить")
        - "object": существительное, над которым выполняется действие (например, "документ", "файл", "изображение", "текст") – может быть пустым
        - "arguments": словарь дополнительных параметров. Если действие относится к документу, включи:
          - "docx_path" (если известен)
          - "text" для заголовка
          - "formatting" (например, "italic")
        Верни JSON-массив объектов с этими полями. Если невозможно, верни пустой массив.
        Запрос: {request}
        """
        try:
            result = self._chat_provider.execute_employee(
                employee="chat",
                system_prompt="Ты помощник по декомпозиции задач Butler. Отвечай только JSON.",
                user_content=prompt
            )
            if not result or result.get("status") != "ok":
                return []
            text = result["text"].strip()
            start = text.find('[')
            if start == -1:
                start = text.find('{')
            if start != -1:
                text = text[start:]
            end = text.rfind(']')
            if end == -1:
                end = text.rfind('}')
            if end != -1:
                text = text[:end+1]
            raw = json.loads(text)
            if not isinstance(raw, list):
                return []
        except Exception:
            return []

        intents = []
        for idx, item in enumerate(raw):
            if not isinstance(item, dict):
                continue
            action = str(item.get("action", "")).strip()
            obj = str(item.get("object", "")).strip()
            arguments = item.get("arguments", {})
            if not isinstance(arguments, dict):
                arguments = {}
            if not action:
                continue
            if docx_path and "docx_path" not in arguments:
                arguments["docx_path"] = docx_path
            intent = TaskIntent(
                requested_action=action,
                action_families=(action,),
                object_candidates=(obj,) if obj else (),
                source_text=request,
                missing_action=None,
                depends_on_previous=(idx > 0),
                arguments=arguments
            )
            intents.append(intent)
        return intents

    def project_spec(self, request: str) -> ProjectSpec | None:
        text = re.sub(r"\s+", " ", str(request or "")).strip()
        q = text.casefold()
        is_project = "проект" in q
        has_repeatable_content = self._contains(q, "стихотвор", "стих", "поэм")
        has_assembly = self._contains(q, "иллюстрац", "изображен") and self._contains(q, "архив", "zip", "упакуй")
        if not (is_project and has_repeatable_content and has_assembly):
            return None

        count, source = self._extract_count(q)
        name = self._quoted_value(text) or "Стихи о море"
        location = "desktop" if self._contains(q, "рабочем стол", "рабочий стол", "desktop") else "workspace"
        return ProjectSpec(name, count, source, location)

    def _extract_count(self, text: str) -> tuple[int, str]:
        digit = re.search(r"\b(\d{1,2})\s+(?:стих|стихотвор|поэм)", text)
        if digit:
            value = int(digit.group(1))
            if 1 <= value <= 20:
                return value, "explicit"
        for word, value in self._NUMBER_WORDS.items():
            if re.search(rf"\b{word}\w*\s+(?:стих|стихотвор|поэм)", text):
                return value, "explicit"
        return 3, "default"

    def decompose(self, request: str) -> list[TaskIntent]:
        request = re.sub(r"\s+", " ", str(request or "")).strip()
        if not request:
            return []

        clauses = [part.strip(" .") for part in self._SPLIT.split(request) if part.strip(" .")]
        intents: list[TaskIntent] = []
        whole = request.casefold()
        web_download_request = (
            self._contains(whole, "в интернете", "в сети")
            and self._contains(whole, "скачай", "загрузи")
        )
        if web_download_request:
            intents.append(self._intent(
                "download_url", ("download",), ("document",), request,
                arguments={"network_allowed": True, "resolve_search": True},
            ))
        folder_requested = False
        image_requested = False
        explicit_image_save = False

        for clause in clauses:
            q = clause.casefold()

            if self._contains(q, "скачай", "загрузи") and re.search(r"https?://", clause, re.I):
                intents.append(self._intent(
                    "download_url", ("download",), ("document",), clause,
                    arguments={"network_allowed": "разрешаю" in q},
                ))

            if self._contains(q, "найди", "поиск", "отыщи") and not web_download_request:
                intents.append(self._intent(
                    "search_catalog", ("search",), ("catalog_full_text",), clause
                ))

            if "pdf" in q and self._contains(q, "найди", "поиск", "кратк", "содержание", "сводк"):
                intents.append(self._intent(
                    "extract_pdf", ("extract",), ("pdf",), clause, depends=True
                ))

            if self._contains(q, "извлеки", "извлечь"):
                objects = (("pdf",) if "pdf" in q else
                           (("docx",) if "docx" in q or "word" in q else ("text", "pdf", "docx")))
                intents.append(self._intent(
                    "extract_document", ("extract",), objects, clause, depends=True
                ))

            if self._contains(q, "переведи", "перевести", "перевод"):
                if self._contains(q, "документ", "pdf", "файл"):
                    object_candidates = ("pdf",) if "pdf" in q else ("text", "docx", "pdf")
                    intents.append(self._intent(
                        "extract_document", ("extract",), object_candidates, clause
                    ))
                intents.append(self._intent(
                    "translate_text", ("rewrite", "generate"), ("text",), clause, depends=True
                ))
                continue

            if self._contains(q, "опиши изображение", "опиши фото", "что на изображении", "что на фото"):
                intents.append(self._intent(
                    "analyze_image", ("analyze", "recognize"), ("image",), clause
                ))

            if self._contains(q, "краткое содержание", "кратк", "сводк", "резюме"):
                intents.append(self._intent(
                    "summarize_text", ("generate", "rewrite", "summarize"), ("text",), clause, depends=True
                ))

            if (self._contains(q, "создай", "сформируй")
                    and self._contains(q, "word", "документ", "docx")):
                title_match = re.search(
                    r'заголовк\w*\s+[«"]([^»"]+)[»"]',
                    clause, re.IGNORECASE
                )
                text_match = re.search(
                    r'текст\w*\s+[«"]([^»"]+)[»"]',
                    clause, re.IGNORECASE
                )
                docx_parts = []
                if title_match:
                    docx_parts.append(title_match.group(1).strip())
                if text_match:
                    docx_parts.append(text_match.group(1).strip())
                docx_arguments = (
                    {"content": "\n\n".join(docx_parts)}
                    if docx_parts else {}
                )
                intents.append(self._intent(
                    "create_docx", ("create",), ("docx",), clause,
                    depends=True, arguments=docx_arguments
                ))

            if self._contains(q, "проверь", "проверифицируй") and self._contains(q, "документ", "word", "результат"):
                intents.append(self._intent(
                    "verify_document", ("extract",), ("docx",), clause, depends=True
                ))

            # Обработка: напиши письмо / напиши текст / составь текст
            if self._contains(q, "напиши") or self._contains(q, "составь"):
                if not self._contains(q, "стихотвор", "стих", "поэм"):
                    intents.append(self._intent(
                        "generate_text", ("generate",), ("text",), clause
                    ))
            # Обработка: напиши стихотворение / сочини стих
            poem_command = self._contains(q, "напиши", "сочини") or self._contains(
                q, "создай стихотвор", "создай стих ", "создай поэм"
            )
            if self._contains(q, "стихотвор", "стих", "поэм") and poem_command:
                intents.append(self._intent(
                    "generate_poem", ("generate",), ("text",), clause
                ))

            if self._contains(q, "создай папк", "создать папк", "создай каталог", "создать каталог"):
                folder_requested = True
                folder_name = self._quoted_value(clause) or self._folder_name(clause) or "Новая папка"
                intents.append(self._missing(
                    "create_folder", "folder", clause,
                    arguments={"folder_name": folder_name, "location": "workspace"},
                ))

            if self._contains(q, "сохрани", "положи", "запиши"):
                if self._contains(q, "документ", "word", "docx") and any(
                    item.requested_action == "create_docx" for item in intents
                ):
                    continue
                is_image = self._contains(q, "изображен", "иллюстрац", "картин", " её", " ее") and image_requested
                explicit_image_save = explicit_image_save or is_image
                intents.append(self._missing(
                    "save_image" if is_image else "save_text",
                    "image" if is_image else "text",
                    clause,
                    depends=True,
                    arguments={"filename": self._filename(clause)},
                ))

            if self._contains(q, "нарисуй", "иллюстрац", "создай изображение", "создай картин"):
                image_requested = True
                intents.append(self._intent(
                    "generate_image", ("generate",), ("comfyui_image", "image"), clause
                ))

        if folder_requested and image_requested and not explicit_image_save:
            intents.append(self._missing(
                "save_image", "image", "implicit: save generated image to requested folder", depends=True,
                arguments={"filename": "sea.png"},
            ))

        # Verification can be expressed in a subordinate clause ("проверь,
        # что он создан") where the object is carried by the preceding DOCX
        # operation. Preserve that dependency instead of losing the step.
        has_docx_create = any(item.requested_action == "create_docx" for item in intents)
        has_docx_verify = any(item.requested_action == "verify_document" for item in intents)
        if has_docx_create and not has_docx_verify and self._contains(whole, "проверь", "проверить"):
            intents.append(self._intent(
                "verify_document", ("extract",), ("docx",), request, depends=True,
            ))

        intents = self._deduplicate(intents)
        return intents

    @staticmethod
    def _contains(text: str, *markers: str) -> bool:
        return any(marker in text for marker in markers)

    @staticmethod
    def _intent(requested, actions, objects, source, depends=False, arguments=None):
        return TaskIntent(requested, tuple(actions), tuple(objects), source,
                          depends_on_previous=depends, arguments=dict(arguments or {}))

    @staticmethod
    def _missing(action, object_name, source, depends=False, arguments=None):
        return TaskIntent(
            action, (), (object_name,), source,
            missing_action=action,
            depends_on_previous=depends,
            arguments=dict(arguments or {}),
        )

    @staticmethod
    def _quoted_value(text: str) -> str | None:
        match = re.search(r'["«](.+?)["»]', text)
        return match.group(1).strip() if match else None

    @staticmethod
    def _filename(text: str) -> str | None:
        match = re.search(r"\b([\w.-]+\.(?:txt|md|png|jpg|jpeg|webp))\b", text, re.I)
        return match.group(1) if match else None

    @staticmethod
    def _folder_name(text: str) -> str | None:
        match = re.search(r"(?:папк\w*|каталог\w*)\s+([\wА-Яа-яЁё.-]+)", text, re.I)
        return match.group(1).strip() if match else None

    @staticmethod
    def _deduplicate(intents: list[TaskIntent]) -> list[TaskIntent]:
        result = []
        seen = set()
        for intent in intents:
            key = (intent.requested_action, intent.source_text)
            if key not in seen:
                seen.add(key)
                result.append(intent)
        return result
