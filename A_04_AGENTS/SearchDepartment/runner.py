# -*- coding: utf-8 -*-
import time
import re
from pathlib import Path
from A_04_AGENTS.base_department import BaseDepartment
from A_07_MEMORY.catalog_search_bridge import CatalogSearchBridge
from A_07_MEMORY.profile_manager import load_profile
from A_04_AGENTS.BrowserDepartment.runner import BrowserDepartment

class SearchDepartment(BaseDepartment):
    NAME = "SEARCH"
    VERSION = "1.0"
    CAPABILITIES = (
        "catalog_full_text_search", "profile_memory_search",
        "local_first_information_search",
    )
    DEPENDENCIES = (
        "A_07_MEMORY.catalog_search_bridge.CatalogSearchBridge",
        "A_07_MEMORY.profile_manager",
    )
    DATA_READS = (
        "catalog database through CatalogSearchBridge",
        "profile memory through ProfileManager",
    )
    DATA_WRITES = ("search session context through CatalogSearchBridge",)

    INFORMATION_INTENT = re.compile(
        r"^(?:найди|поищи)\s+информацию\s+о\s+|"
        r"^(?:найди|поищи)\s+(?:инструкцию|руководство|мануал|документацию)\s+по\s+|"
        r"^что\s+такое\s+|"
        r"^расскажи\s+о\s+|"
        r"^покажи\s+информацию\s+по\s+|"
        r"^.*(?:погод|курс|\bцен(?:а|ы|е|у|ой|ами|ах)?\b|стоимост|новост|сегодня|сейчас|последн|актуаль).*$",
        re.IGNORECASE,
    )
    CURRENT_INFORMATION_MARKERS = (
        "сейчас", "сегодня", "актуаль", "последн", "свеж",
        "текущ", "курс", "цена", "стоимост", "погода", "новост",
    )
    CONFIRM_ANSWERS = {"да", "разрешаю", "разрешить", "согласен", "согласна"}
    CANCEL_ANSWERS = {"нет", "не разрешаю", "отмена", "отказ", "не надо"}

    def __init__(self, bridge=None, model_provider=None, browser=None):
        self.bridge = bridge or CatalogSearchBridge()
        self.model_provider = model_provider
        self.browser = browser or BrowserDepartment()
        self._pending_web_search = None

    def can_handle(self, query: str, context: dict = None) -> bool:
        q = (query or "").lower()
        media_knowledge = (
            any(stem in q for stem in ("изображ", "аудио", "видео", "медиа"))
            and any(stem in q for stem in ("знан", "проект", "сохран", "связан"))
        )
        if media_knowledge:
            return False
        if self._pending_web_search is not None and self._confirmation_answer(q):
            return True
        keys = [
            "найди", "поиск", "какие документы", 
            "какие изображения", "что есть в архиве", "ищи",
            "поищи информацию о", "что такое", "расскажи о",
            "покажи информацию по",
        ]
        return self._is_information_request(q) or any(k in q for k in keys)

    def _clean_query(self, text: str) -> str:
        if not text:
            return ""

        q = text.strip().strip('"`').lower()

        q = re.sub(
            r"^(найди|найти|поиск|ищи|найди мне|покажи|поищи)\s*[:\s]*",
            "",
            q,
            flags=re.IGNORECASE
        )

        for noise in [
            "в базе данных",
            "в архиве",
            "в каталоге",
            "сведения по",
            "сведения о",
            "информацию о",
            "информацию про",
            "файл",
            "документ"
        ]:
            q = q.replace(noise, "")

        q = re.split(
            r"(,\s*выдели|\s+выдели|,\s*открой|\s+открой|для редактирования|и открой)",
            q,
            flags=re.IGNORECASE
        )[0]

        mapping = {
            "финам": "finam",
            "отчет": "report"
        }

        for ru_word, en_word in mapping.items():
            q = q.replace(ru_word, en_word)

        return q.strip().strip('"`.,!?;:')
    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        context = dict(context or {})
        if self._pending_web_search is not None:
            answer = self._confirmation_answer(query)
            if answer:
                return self._resolve_web_confirmation(answer, start)

        clean_text = self._clean_query(query)
        
        # Если после очистки ничего не осталось, ищем по исходному тексту
        search_term = clean_text if clean_text else query
        if self._is_information_request(query):
            information_topic = self._information_topic(query)
            if information_topic:
                search_term = information_topic

        try:
            bridge_res = self.bridge.search(search_term)
        except Exception as exc:
            return {
                "ok": False,
                "department": self.NAME,
                "model": "CatalogSearchBridge",
                "latency_ms": int((time.time() - start) * 1000),
                "text": "Поиск не выполнен.",
                "error": "SEARCH_BRIDGE_ERROR",
                "metadata": {
                    "query": search_term,
                    "semantic": context.get("semantic", {}),
                    "exception_type": type(exc).__name__,
                },
                "results": [],
            }

        semantic = context.get("semantic", {})
        results = bridge_res.get("results", [])

        if not results:
            memory_matches = self._search_profile_memory(query)
            if memory_matches and re.search(
                r"(?:только\s+(?:лучший|наиболее\s+релевантный)|"
                r"покажи\s+только\s+(?:лучший|наиболее\s+релевантный))",
                query or "",
                re.IGNORECASE,
            ):
                memory_matches = memory_matches[:1]
            if memory_matches:
                memory_summary = "\n".join(
                    f"{item['key']} = {item['value']}" for item in memory_matches
                )
                memory_path = Path(__file__).resolve().parents[2] / "A_05_STORAGE" / "USER_MEMORY.md"
                results = [{
                    "id": "memory:profile",
                    "filepath": str(memory_path),
                    "summary": memory_summary,
                    "tags": "memory,profile",
                    "matches": memory_matches,
                }]
                self.bridge.session_manager.update_search_context(
                    original_query=query,
                    normalized=search_term,
                    expanded=[],
                    rich_results=results,
                )
                bridge_res = {
                    "ok": True,
                    "text": memory_summary,
                    "results": results,
                    "error": None,
                }

        if (
            results
            and self._is_information_request(query)
            and not self._information_results_relevant(
                self._information_topic(query), results
            )
        ):
            results = []
            bridge_res = {
                "ok": True,
                "text": "В локальной памяти релевантной информации не найдено.",
                "results": [],
                "error": None,
            }
        
        if not results and self._is_information_request(query):
            topic = self._information_topic(query)
            if not topic:
                return self._information_result(
                    start, False, "Укажите тему для поиска информации.",
                    "SEARCH_INFORMATION_TOPIC_MISSING", "LocalFirstSearch",
                    stage="invalid_request",
                )

            if self._requires_current_information(topic):
                return self._request_web_confirmation(topic, start)

            model_result = self._ask_internal_model(topic)
            if model_result["sufficient"]:
                return self._information_result(
                    start, True, model_result["text"], None,
                    model_result["model"], stage="internal_knowledge",
                    query=topic, source="internal_model",
                )
            return self._request_web_confirmation(
                topic, start, model_reason=model_result["reason"]
            )

        return {
            "ok": bridge_res.get("ok", False),
            "department": self.NAME,
            "model": "CatalogSearchBridge",
            "latency_ms": int((time.time() - start) * 1000),
            "text": bridge_res.get("text", "Ничего не найдено."),
            "semantic": semantic,
            "error": bridge_res.get("error"),
            "metadata": {
                "query": search_term,
                "semantic": semantic,
                "result_count": len(results),
            },
            "results": results,
        }

    def _is_information_request(self, query: str) -> bool:
        return bool(self.INFORMATION_INTENT.search((query or "").strip()))

    def _information_topic(self, query: str) -> str:
        topic = re.sub(
            r"^(?:найди|поищи)\s+",
            "",
            (query or "").strip(),
            count=1,
            flags=re.IGNORECASE,
        )
        topic = re.sub(
            r"^(?:информацию\s+о|информацию\s+про|сведения\s+о|сведения\s+по)\s+",
            "",
            topic,
            count=1,
            flags=re.IGNORECASE,
        )
        return topic.strip().strip('"`.,!?;:')

    def _requires_current_information(self, topic: str) -> bool:
        lowered = topic.casefold()
        return any(marker in lowered for marker in self.CURRENT_INFORMATION_MARKERS)

    def _information_results_relevant(self, topic: str, results: list) -> bool:
        if any(not str(item.get("id", "")).startswith("memory:") for item in results):
            return True
        tokens = {
            token for token in re.findall(r"[a-zа-яё0-9]+", topic.casefold())
            if len(token) > 2
        }
        searchable = " ".join(
            f"{item.get('summary', '')} {item.get('tags', '')}" for item in results
        ).casefold()
        return bool(tokens and any(token in searchable for token in tokens))

    def _ask_internal_model(self, topic: str) -> dict:
        if self.model_provider is None:
            from A_02_MANAGERS.smart_dispatcher import SmartDispatcher
            self.model_provider = SmartDispatcher()
        result = self.model_provider.execute_employee(
            employee="chat",
            system_prompt=(
                "Ответь только из внутренних знаний модели, без Интернета. "
                "Если для надёжного ответа нужны актуальные данные или ты не знаешь ответ, "
                "верни ровно INSUFFICIENT. Иначе верни содержательный ответ по-русски."
            ),
            user_content=f"Что известно по теме: {topic}?",
        )
        text = self.model_provider.clean_model_output(result.get("text") or "").strip()
        insufficient = (
            result.get("status") != "ok"
            or not text
            or text.upper() == "INSUFFICIENT"
            or any(marker in text.casefold() for marker in (
                "не знаю", "недостаточно информации", "нужны актуальные данные",
            ))
        )
        return {
            "sufficient": not insufficient,
            "text": text,
            "model": result.get("model") or "InternalModel",
            "reason": result.get("fallback_reason") or (
                "MODEL_REPORTED_INSUFFICIENT" if insufficient else None
            ),
        }

    def _request_web_confirmation(self, topic: str, started: float, model_reason=None) -> dict:
        self._pending_web_search = topic
        return self._information_result(
            started, True,
            f"Для получения актуальной информации по запросу «{topic}» требуется доступ в Интернет. Разрешить?",
            None, "LocalFirstSearch", stage="awaiting_web_confirmation",
            query=topic, confirmation_required=True, model_reason=model_reason,
        )

    def _resolve_web_confirmation(self, answer: str, started: float) -> dict:
        topic = self._pending_web_search
        self._pending_web_search = None
        if answer == "cancel":
            return self._information_result(
                started, False, "Выход в Интернет отменён. Браузер не открыт.",
                "BROWSER_SEARCH_CANCELLED", "LocalFirstSearch",
                stage="web_search_cancelled", query=topic,
            )
        from A_03_ORCHESTRATION.permission import DepartmentExecutionGateway
        result = DepartmentExecutionGateway().execute(
            self.browser, f"Найди в интернете {topic}"
        )
        metadata = dict(result.get("metadata") or {})
        metadata.update({"local_first": True, "confirmation": "accepted"})
        result["metadata"] = metadata
        return result

    def _confirmation_answer(self, query: str):
        answer = " ".join(str(query or "").casefold().split()).strip(" .!?")
        if answer in self.CONFIRM_ANSWERS:
            return "confirm"
        if answer in self.CANCEL_ANSWERS:
            return "cancel"
        return None

    def _information_result(self, started, ok, text, error, model, **metadata):
        return {
            "ok": ok,
            "department": self.NAME,
            "model": model,
            "latency_ms": int((time.time() - started) * 1000),
            "text": text,
            "error": error,
            "metadata": metadata,
            "results": [],
        }

    def _search_profile_memory(self, query: str) -> list:
        stop_words = {
            "найди", "информацию", "информация", "которую", "который",
            "ранее", "запомнил", "запомнила", "память", "памяти", "мой",
            "моя", "мое", "моё", "обо", "мне", "про", "этот", "этой",
            "наиболее", "релевантную", "релевантный", "сохранённую",
            "сохраненную", "точному", "точный", "значению", "значение", "по",
        }
        tokens = {
            token for token in re.findall(r"[a-zа-яё0-9_]+", query.lower())
            if len(token) > 2 and token not in stop_words
        }
        if not tokens:
            return []

        matches = []
        profile = load_profile()
        for section, values in profile.items():
            if not isinstance(values, dict):
                continue
            for key, data in values.items():
                if not isinstance(data, dict) or "value" not in data:
                    continue
                value = str(data["value"])
                searchable = f"{section} {key} {value}".lower().replace("_", " ")
                searchable_tokens = re.findall(r"[a-zа-яё0-9]+", searchable)
                score = sum(1 for token in tokens if any(
                    token in candidate
                    or candidate in token
                    or (len(token) >= 5 and len(candidate) >= 5 and token[:5] == candidate[:5])
                    for candidate in searchable_tokens
                ))
                if score:
                    matches.append({
                        "section": section,
                        "key": key,
                        "value": value,
                        "score": score,
                    })
        return sorted(matches, key=lambda item: item["score"], reverse=True)





