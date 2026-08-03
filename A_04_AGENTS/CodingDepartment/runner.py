# -*- coding: utf-8 -*-

import re
import time
import requests
from A_00_UTILS.llm_output_sanitizer import NO_REASONING_PROMPT, sanitize_llm_output

from A_01_CORE.manifest_loader import ManifestLoader
from A_04_AGENTS.base_department import BaseDepartment


class CodingDepartment(BaseDepartment):
    NAME = "CODING"
    name = "CODING"
    VERSION = "1.0"
    CAPABILITIES = ("code_generation", "code_explanation", "code_correction")
    DEPENDENCIES = ("requests", "Ollama", "ManifestLoader")
    DATA_READS = ("system manifest model configuration",)
    DATA_WRITES = ()

    def __init__(self):
        self.cfg = ManifestLoader.load()
        self.base_url = self.cfg.get("ollama_url", "http://127.0.0.1:11434/api/chat").replace("/api/chat", "")
        self.generate_url = self.base_url.rstrip("/") + "/api/generate"
        self.model_chain = [
            self.cfg.get("coder_model", "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"),
            "sub-coder-32b:latest",
            self.cfg.get("fallback_model", "codestral:latest")
        ]

    def can_handle(self, query: str, context: dict = None) -> bool:
        text = (query or "").lower()
        # Если запрос явно про грамматику или текст — не брать (отдаём TextDepartment)
        if any(x in text for x in ["грамматик", "текст", "предложени", "фраз"]):
            return False
        keys = [
            "python", "код", "скрипт", "ошибка", "traceback", "исправь",
            "функция", "класс", "powershell", "bash", "get-process",
            "процесс",
        ]
        return any(k in text for k in keys)

    def _ask(self, model: str, prompt: str, timeout=180) -> str:
        response = requests.post(
            self.generate_url,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout
        )
        response.raise_for_status()
        raw = response.json().get("response", "") or ""
        return sanitize_llm_output(raw)

    def _validate_response(self, query: str, answer: str):
        """Return (relevant, reasons) without asking another LLM to judge."""
        q = (query or "").lower()
        a = (answer or "").strip()
        low = a.lower()
        reasons = []
        if not a:
            return False, ["empty_response"]

        topic_markers = {
            "fibonacci": ("fibonacci", "фибонач"),
            "solid": ("solid",),
            "passwords": ("парол", "password"),
            "random": ("random", "случайн"),
            "csv": ("csv",),
        }
        for topic, markers in topic_markers.items():
            if any(marker in low for marker in markers) and not any(marker in q for marker in markers):
                reasons.append(f"unexpected_topic_{topic}")

        process_task = "процесс" in q or "get-process" in q
        if process_task:
            required = {"get-process": "missing_get_process"}
            if any(x in q for x in ("памят", "memory", "ram")):
                required["sort-object"] = "missing_memory_sort"
            for marker, reason in required.items():
                if marker not in low:
                    reasons.append(reason)
            if any(x in q for x in ("памят", "memory", "ram")) and not any(
                x in low for x in ("workingset", "working set", " ws", ".ws")
            ):
                reasons.append("missing_memory_metric")
            if re.search(r"\b10\b", q) and not any(x in low for x in ("first 10", "-first 10", "select-object -first 10")):
                reasons.append("missing_requested_limit")
        if "powershell" in q or process_task:
            if re.search(r"\b(import |def |print\(|pandas|python)\b", low):
                reasons.append("wrong_language_python")
        elif "python" in q:
            if not re.search(r"\b(def |class |import |from |print\(|async def )", low):
                reasons.append("missing_python_code")
        elif "bash" in q:
            if not any(x in low for x in ("#!/bin/bash", "#!/usr/bin/env bash", "echo ", "for ", "if [", "ps ")):
                reasons.append("missing_bash_code")

        if any(x in q for x in ("код", "скрипт", "функц", "powershell", "python", "bash", "процесс", "get-process")):
            code_signals = ("```", "$", "get-", "set-", "select-object", "def ", "class ", "import ", "function ", "#!/", "echo ", "ps ")
            if not any(x in low for x in code_signals):
                reasons.append("no_code_signals")
        return not reasons, reasons

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.time()
        context = dict(context or {})
        query = (query or "").strip()

        if not query:
            return self._error_result(
                started, "EMPTY_QUERY",
                "Не указан запрос для генерации кода."
            )

        prompt = (
            "Ты — инженер отдела CODING проекта BUTLER_OMEGA_SMART.\n"
            "Выполняй запрос пользователя максимально точно.\n"
            "Правила:\n"
            f"- {NO_REASONING_PROMPT}\n"
            "- Не меняй задачу пользователя.\n"
            "- Выполняй только то, что запрошено.\n"
            "- Строго соблюдай ограничения пользователя.\n"
            "- Если просят PowerShell — отвечай только PowerShell.\n"
            "- Для запроса о процессах используй PowerShell Get-Process; при запросе по памяти сортируй по WorkingSet/WS.\n"
            "- Если просят Python — отвечай только Python.\n"
            "- Если просят Bash — отвечай только Bash.\n"
            "- Если просят только код — не добавляй пояснений.\n"
            "- Если просят объяснение — объясняй именно запрошенный код.\n"
            "- Не предлагай другой язык программирования.\n"
            "- Если задача понятна — не проси уточнений.\n\n"
            f"ЗАДАЧА:\n{query}"
        )

        errors = []
        empty_models = []
        rejected_models = []
        attempted_models = []

        for model in self.model_chain:
            attempted_models.append(model)
            try:
                text = self._ask(model, prompt)
                if text:
                    relevant, reasons = self._validate_response(query, text)
                    if not relevant:
                        rejected_models.append({"model": model, "reasons": reasons})
                        continue
                    return {
                        "ok": True,
                        "department": self.NAME,
                        "model": model,
                        "latency_ms": int((time.time() - started) * 1000),
                        "fallback_used": model != self.model_chain[0],
                        "text": text,
                        "error": None,
                        "metadata": {
                            "engine": "OllamaCoding",
                            "attempted_models": attempted_models,
                            "fallback_used": model != self.model_chain[0],
                        },
                    }
                empty_models.append(model)
            except Exception as exc:
                errors.append({"model": model, "exception_type": type(exc).__name__})

        if errors and not rejected_models and not empty_models:
            return self._error_result(
                started, "CODING_ENGINE_ERROR",
                "Все модели Coding Engine завершились технической ошибкой.",
                metadata={
                    "attempted_models": attempted_models,
                    "errors": errors,
                    "fallback_used": True,
                },
            )

        return self._error_result(
            started, "CODING_GENERATION_FAILED",
            "Ни одна модель Coding Engine не вернула релевантный результат.",
            metadata={
                "attempted_models": attempted_models,
                "errors": errors,
                "empty_models": empty_models,
                "rejected_models": rejected_models,
                "fallback_used": True,
            },
        )

    def _error_result(self, started, error, text, model=None, metadata=None):
        result_metadata = dict(metadata or {})
        return {
            "ok": False,
            "department": self.NAME,
            "model": model,
            "latency_ms": max(0, int((time.time() - started) * 1000)),
            "fallback_used": bool(result_metadata.get("fallback_used", False)),
            "text": text,
            "error": str(error),
            "metadata": result_metadata,
        }

