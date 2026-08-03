# BUTLER OMEGA — LLM CONTEXT PACKAGE

## IMPACT SUMMARY
- Target file: `base_department.py`
- Target module: `A_04_AGENTS.base_department`
- Risk level: `CRITICAL_INFRASTRUCTURE`
- Affected count: `6`
- Requires rollback: `True`

---

## TARGET: A_04_AGENTS.base_department
Path: `A_04_AGENTS/base_department.py`

```python
﻿# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class BaseDepartment(ABC):
    NAME = "BASE"

    @abstractmethod
    def can_handle(self, query: str, context: dict = None) -> bool:
        pass

    @abstractmethod
    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        pass

    def __repr__(self):
        return f"<Department: {self.NAME}>"

```

---

## AFFECTED: A_04_AGENTS.ArchiveDepartment.runner
Path: `A_04_AGENTS/ArchiveDepartment/runner.py`

```python
from A_04_AGENTS.base_department import BaseDepartment

class ArchiveDepartment(BaseDepartment):
    NAME = "ARCHIVE"

    def can_handle(self, text: str) -> bool:
        return False

    def execute(self, text: str, **kwargs) -> dict:
        return {
            "department": self.NAME,
            "status": "ok",
            "handled": False,
            "text": text
        }
```

---

## AFFECTED: A_04_AGENTS.AudioDepartment.runner
Path: `A_04_AGENTS/AudioDepartment/runner.py`

```python
from A_04_AGENTS.base_department import BaseDepartment

class AudioDepartment(BaseDepartment):
    NAME = "AUDIO"

    def can_handle(self, text: str) -> bool:
        return False

    def execute(self, text: str, **kwargs) -> dict:
        return {
            "department": self.NAME,
            "status": "ok",
            "handled": False,
            "text": text
        }
```

---

## AFFECTED: A_04_AGENTS.CodingDepartment.runner
Path: `A_04_AGENTS/CodingDepartment/runner.py`

```python
# -*- coding: utf-8 -*-

import re
import time
import requests

from A_01_CORE.manifest_loader import ManifestLoader
from A_04_AGENTS.base_department import BaseDepartment


class CodingDepartment(BaseDepartment):
    name = "CODING"

    def __init__(self):
        self.cfg = ManifestLoader.load()
        self.base_url = self.cfg.get("ollama_url", "http://127.0.0.1:11434/api/chat").replace("/api/chat", "")
        self.generate_url = self.base_url.rstrip("/") + "/api/generate"
        self.model_chain = [
            self.cfg.get("coder_model", "DeepSeek-Coder-V2-Lite-Instruct-Q6_K:latest"),
            "sub-coder-32b:latest",
            self.cfg.get("fallback_model", "codestral:latest")
        ]

    def can_handle(self, query: str, context=None) -> bool:
        text = (query or "").lower()
        keys = ["python", "код", "скрипт", "ошибка", "traceback", "исправь", "функция", "класс", "powershell"]
        return any(k in text for k in keys)

    def _ask(self, model: str, prompt: str, timeout=180) -> str:
        response = requests.post(
            self.generate_url,
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=timeout
        )
        response.raise_for_status()
        raw = response.json().get("response", "") or ""
        raw = re.sub(r"<think>.*?</think>\s*", "", raw, flags=re.DOTALL | re.IGNORECASE)
        return raw.strip()

    def execute(self, query: str, context=None) -> dict:
        prompt = (
            "Ты инженер отдела CODING проекта BUTLER_OMEGA. "
            "Отвечай по-русски. Если пользователь просит код — выдавай готовый код. "
            "Если просит PowerShell — выдавай только PowerShell-команды без лишней воды.\n\n"
            f"ЗАДАЧА:\n{query}"
        )

        errors = []

        for model in self.model_chain:
            start = time.time()
            try:
                text = self._ask(model, prompt)
                if text:
                    return {
                        "ok": True,
                        "department": self.name,
                        "model": model,
                        "latency_ms": int((time.time() - start) * 1000),
                        "fallback_used": model != self.model_chain[0],
                        "text": text,
                        "error": None
                    }
            except Exception as exc:
                errors.append(f"{model}: {exc}")

        return {
            "ok": False,
            "department": self.name,
            "model": None,
            "fallback_used": True,
            "text": "",
            "error": " | ".join(errors)
        }
```

---

## AFFECTED: A_04_AGENTS.TextDepartment.runner
Path: `A_04_AGENTS/TextDepartment/runner.py`

```python
# -*- coding: utf-8 -*-

import re
import time
import requests

from A_04_AGENTS.base_department import BaseDepartment
from A_02_MANAGERS.model_registry import MODEL_REGISTRY
from A_01_CORE.manifest_loader import ManifestLoader


class TextDepartment(BaseDepartment):
    NAME = "TEXT"

    def __init__(self):
        self.cfg = ManifestLoader.load()
        self.base_url = self.cfg.get("ollama_url", "http://127.0.0.1:11434/api/chat").replace("/api/chat", "")
        self.generate_url = self.base_url.rstrip("/") + "/api/generate"
        self.tags_url = self.base_url.rstrip("/") + "/api/tags"
        self.model = MODEL_REGISTRY.get("TEXT", self.cfg.get("analysis_model", "qwen35-ru:latest"))

    def can_handle(self, text: str) -> bool:
        q = (text or "").lower()
        keys = [
            "напиши текст",
            "составь текст",
            "перепиши",
            "объясни",
            "сформулируй",
            "письмо",
            "описание",
            "план",
            "рапорт",
            "отчет",
            "отчёт",
            "документ"
        ]
        return any(k in q for k in keys)

    def clean_text(self, text: str) -> str:
        text = (text or "").strip()
        text = re.sub(r"<think>.*?</think>\s*", "", text, flags=re.DOTALL | re.IGNORECASE)
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
            r = requests.get(self.tags_url, timeout=5)
            r.raise_for_status()
            return [m.get("name") for m in r.json().get("models", []) if m.get("name")]
        except Exception:
            return []

    def execute(self, text: str, **kwargs) -> dict:
        start = time.time()
        models = self.available_models()

        if not models:
            return {
                "ok": False,
                "department": self.NAME,
                "model": None,
                "text": "Ollama недоступна или список моделей не получен. Проверьте, запущен ли Ollama.",
                "error": "OLLAMA_UNAVAILABLE",
                "available_models": []
            }

        model = self.model
        if model not in models:
            return {
                "ok": False,
                "department": self.NAME,
                "model": model,
                "text": "Нужная текстовая модель не найдена. Можно выбрать одну из доступных локальных моделей.",
                "error": "MODEL_NOT_FOUND",
                "available_models": models
            }

        prompt = (
            "Ты сотрудник текстового отдела Butler Omega. "
            "Отвечай по-русски, понятно и по делу. "
            "Верни только готовый результат без markdown и без лишних пояснений.\n\n"
            f"ЗАДАЧА:\n{text}"
        )

        try:
            r = requests.post(
                self.generate_url,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=180
            )
            r.raise_for_status()
            answer = self.clean_text(r.json().get("response", ""))

            return {
                "ok": True,
                "department": self.NAME,
                "model": model,
                "latency_ms": int((time.time() - start) * 1000),
                "text": answer,
                "error": None,
                "available_models": models
            }

        except Exception as exc:
            return {
                "ok": False,
                "department": self.NAME,
                "model": model,
                "text": "",
                "error": str(exc),
                "available_models": models
            }
```

---

## AFFECTED: A_04_AGENTS.VideoDepartment.runner
Path: `A_04_AGENTS/VideoDepartment/runner.py`

```python
from A_04_AGENTS.base_department import BaseDepartment

class VideoDepartment(BaseDepartment):
    NAME = "VIDEO"

    def can_handle(self, text: str) -> bool:
        return False

    def execute(self, text: str, **kwargs) -> dict:
        return {
            "department": self.NAME,
            "status": "ok",
            "handled": False,
            "text": text
        }
```

---

## AFFECTED: A_04_AGENTS.VisionDepartment.runner
Path: `A_04_AGENTS/VisionDepartment/runner.py`

```python
# -*- coding: utf-8 -*-

import re
import time
import requests
import base64
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment
from A_02_MANAGERS.model_registry import MODEL_REGISTRY
from A_01_CORE.manifest_loader import ManifestLoader

class VisionDepartment(BaseDepartment):
    NAME = "VISION"

    def __init__(self):
        self.cfg = ManifestLoader.load()
        self.base_url = self.cfg.get("ollama_url", "http://127.0.0.1:11434/api/chat").replace("/api/chat", "")
        self.generate_url = self.base_url.rstrip("/") + "/api/generate"
        self.model = MODEL_REGISTRY.get("VISION", self.cfg.get("vision_model", "qwen2.5-vl:latest"))

    def can_handle(self, query: str, context: dict = None) -> bool:
        q = (query or "").lower()
        keys = [
            "что на картинке",
            "опиши изображение",
            "проанализируй изображение",
            "проанализируй фото",
            "что на фото",
            "что изображено",
            "анализ изображения",
            "ocr",
            "фото",
            "скрин",
            "прочитай текст",
            "распознай"
        ]
        return any(k in q for k in keys)

    def _encode_image(self, image_path: Path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception as e:
            return None

    def _extract_image_path(self, text: str):
        text = (text or "").strip()

        lower_text = text.lower()

        for prefix in ("файл:", "путь:"):
            if prefix in lower_text:
                idx = lower_text.index(prefix) + len(prefix)
                part = text[idx:].strip()
                part = part.strip("\"'")
                return part.replace("\\", "/")

        m = re.search(r"[A-Za-z]:[\\/][^\s]+", text)
        if m:
            return m.group(0).replace("\\", "/")

        return None

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        
        context = context or {}
        attachments = context.get("attachments", [])

        if attachments:
            image_path_str = attachments[0]
        else:
            image_path_str = self._extract_image_path(query)
        if not image_path_str:
            return {
                "ok": False,
                "department": self.NAME,
                "model": self.model,
                "text": "Ошибка: Пожалуйста, укажите путь к файлу изображения (например: файл: C:\\image.png).",
                "error": "MISSING_IMAGE_PATH"
            }

        image_path = Path(image_path_str)
        if not image_path.exists():
            return {
                "ok": False,
                "department": self.NAME,
                "model": self.model,
                "text": f"Ошибка: Файл не найден по пути {image_path}",
                "error": "IMAGE_NOT_FOUND"
            }

        base64_image = self._encode_image(image_path)
        if not base64_image:
             return {
                "ok": False,
                "department": self.NAME,
                "model": self.model,
                "text": "Ошибка: Не удалось прочитать или закодировать изображение.",
                "error": "ENCODE_FAILED"
            }

        prompt = (
            "Проведи подробный визуальный анализ предоставленного изображения.\n"
            f"Запрос пользователя: {query}\n"
            "Отчет должен быть структурированным, без лишних размышлений и markdown разметки кода."
        )

        try:
            r = requests.post(
                self.generate_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "images": [base64_image],
                    "stream": False
                },
                timeout=300
            )
            r.raise_for_status()
            raw = r.json().get("response", "") or ""
            answer = re.sub(r"<think>.*?</think>\s*", "", raw, flags=re.DOTALL | re.IGNORECASE).strip()

            return {
                "ok": True,
                "department": self.NAME,
                "model": self.model,
                "latency_ms": int((time.time() - start) * 1000),
                "text": answer,
                "error": None
            }
        except Exception as exc:
            return {
                "ok": False,
                "department": self.NAME,
                "model": self.model,
                "text": "Ошибка при обращении к VLM модели Ollama.",
                "error": str(exc)
            }


```

---
