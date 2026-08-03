# -*- coding: utf-8 -*-

import time

import requests

from A_01_CORE.manifest_loader import ManifestLoader
from A_02_MANAGERS.model_registry import MODEL_REGISTRY
from A_04_AGENTS.base_department import BaseDepartment
from A_00_UTILS.llm_output_sanitizer import sanitize_llm_output


class TextDepartment(BaseDepartment):
    NAME = "TEXT"
    VERSION = "1.1"
    CAPABILITIES = ("text_generation", "text_rewriting", "text_explanation")
    DEPENDENCIES = ("requests", "Ollama")
    DATA_READS = ()
    DATA_WRITES = ()

    def __init__(self):
        self.cfg = ManifestLoader.load()
        self.base_url = self.cfg.get(
            "ollama_url", "http://127.0.0.1:11434/api/chat"
        ).replace("/api/chat", "")
        self.generate_url = self.base_url.rstrip("/") + "/api/generate"
        self.tags_url = self.base_url.rstrip("/") + "/api/tags"
        self.model = MODEL_REGISTRY.get(
            "TEXT", self.cfg.get("analysis_model", "qwen35-ru:latest")
        )

    def can_handle(self, query: str, context: dict = None) -> bool:
        q = (query or "").lower()
        keys = [
            "переведи", "перевод", "перефразируй", "перефразировать",
            "исправь грамматику", "исправить грамматику", "исправь текст",
            "напиши текст", "напиши стихотворение", "составь текст",
            "перепиши", "объясни", "сформулируй", "письмо", "описание",
            "план", "рапорт", "отчет", "отчёт", "деловой документ",
        ]
        return any(key in q for key in keys)

    def clean_text(self, text: str) -> str:
        text = sanitize_llm_output(text)
        if text.startswith("```python"):
            text = text[len("```python"):].lstrip()
        elif text.startswith("```powershell"):
            text = text[len("```powershell"):].lstrip()
        elif text.startswith("```"):
            text = text[len("```"):].lstrip()
        if text.endswith("```"):
            text = text[:-3].rstrip()
        return text.strip()

    def available_models(self):
        try:
            response = requests.get(self.tags_url, timeout=5)
            response.raise_for_status()
            return [
                item.get("name")
                for item in response.json().get("models", [])
                if item.get("name")
            ]
        except Exception:
            return []

    def _select_model(self, context):
        role_name = "Эксперт"
        if not isinstance(self.model, dict):
            return self.model, role_name

        choice = str(context.get("text_role", "analytic")).strip().lower()
        if choice in {"2", "writer"}:
            role_name = "Писатель"
            model = self.model.get("writer")
        elif choice in {"3", "engineer"}:
            role_name = "Инженер"
            model = self.model.get("engineer")
        else:
            role_name = "Аналитик"
            model = self.model.get("analytic")
        return model or self.model.get("default", "qwen35-ru:latest"), role_name

    @staticmethod
    def _build_prompt(user_text):
        return (
            "Ты выполняешь задачу обработки пользовательского текста.\n"
            "Верни только окончательный обработанный текст без анализа, пояснений, "
            "служебных меток и markdown.\n"
            "Для перевода верни только перевод. Для перефразирования верни только "
            "перефразированный текст. Для исправления грамматики верни только "
            "исправленный текст.\n\n"
            f"Запрос пользователя:\n{user_text}"
        )

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        context = dict(context or {})
        user_text = (query or "").strip()

        if not user_text:
            return self._error_result(
                start, "EMPTY_QUERY", "Не указан запрос для генерации текста."
            )

        models = self.available_models()
        if not models:
            return self._error_result(
                start,
                "OLLAMA_UNAVAILABLE",
                "Ollama недоступна или список моделей не получен. Проверьте, запущен ли Ollama.",
                metadata={"available_models": []},
            )

        model, role_name = self._select_model(context)
        if model not in models:
            return self._error_result(
                start,
                "MODEL_NOT_FOUND",
                f"Текстовая модель {model} не найдена в Ollama.",
                model=model,
                metadata={"available_models": models, "role": role_name},
            )

        prompt = self._build_prompt(user_text)
        try:
            answer = ""
            for attempt in range(2):
                current_prompt = prompt
                if attempt:
                    current_prompt += (
                        "\n\nПредыдущая генерация не содержала окончательного текста. "
                        "Верни только готовый результат."
                    )
                response = requests.post(
                    self.generate_url,
                    json={
                        "model": model,
                        "prompt": current_prompt,
                        "stream": False,
                        "think": False,
                        "options": {"temperature": 0},
                    },
                    timeout=180,
                )
                response.raise_for_status()
                answer = self.clean_text(response.json().get("response", ""))
                if answer:
                    break

            if not answer:
                return self._error_result(
                    start,
                    "EMPTY_TEXT_RESPONSE",
                    "Text Engine вернул пустой ответ.",
                    model=model,
                    metadata={"available_models": models, "role": role_name},
                )

            return {
                "ok": True,
                "department": self.NAME,
                "model": model,
                "latency_ms": int((time.time() - start) * 1000),
                "text": answer,
                "error": None,
                "metadata": {
                    "available_models": models,
                    "role": role_name,
                    "engine": "OllamaText",
                },
                "available_models": models,
            }
        except Exception as exc:
            return self._error_result(
                start,
                "TEXT_ENGINE_ERROR",
                "Ошибка при обращении к Text Engine Ollama.",
                model=model,
                metadata={
                    "available_models": models,
                    "role": role_name,
                    "exception_type": type(exc).__name__,
                },
            )

    def _error_result(self, start, error, text, model=None, metadata=None):
        return {
            "ok": False,
            "department": self.NAME,
            "model": model,
            "latency_ms": max(0, int((time.time() - start) * 1000)),
            "text": text,
            "error": str(error),
            "metadata": dict(metadata or {}),
        }
