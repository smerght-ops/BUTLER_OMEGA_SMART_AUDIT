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
    VERSION = "1.0"
    CAPABILITIES = ("image_analysis", "image_text_recognition")
    DEPENDENCIES = ("requests", "Ollama", "configured vision model")
    DATA_READS = ("user-provided image path",)
    DATA_WRITES = ()
    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

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

        if '"' in text:
            try:
                return text.split('"')[1].strip().replace("\\", "/")
            except Exception:
                pass

        if "'" in text:
            try:
                return text.split("'")[1].strip().replace("\\", "/")
            except Exception:
                pass

        # Command-line launchers may consume quotation marks. Recover a
        # concrete Windows image path from the remaining natural-language text.
        match = re.search(
            r"[A-Za-z]:[\\/][^\r\n\"']+?\.(?:png|jpe?g|webp|bmp)",
            text, re.IGNORECASE,
        )
        if match:
            return match.group(0).strip().replace("\\", "/")

        return None

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        start = time.time()

        context = dict(context or {})
        attachments = context.get("attachments", [])

        if not isinstance(attachments, (list, tuple)):
            return self._error_result(
                start, "INVALID_ATTACHMENTS",
                "Ошибка: attachments должен быть списком путей."
            )

        if not attachments:
            extracted_path = self._extract_image_path(query)
            if extracted_path:
                attachments = [extracted_path]
                context['attachments'] = attachments

        if not attachments:
            return self._error_result(
                start, "MISSING_ATTACHMENT",
                "Ошибка: изображение не передано через context['attachments']."
            )

        image_path_str = str(attachments[0]).strip().strip("\"'")
        image_path = Path(image_path_str)
        if not image_path.exists():
            return self._error_result(
                start, "IMAGE_NOT_FOUND",
                f"Ошибка: Файл не найден по пути {image_path}",
                path=image_path,
            )

        if not image_path.is_file():
            return self._error_result(
                start, "NOT_A_FILE",
                f"Ошибка: указанный путь не является файлом: {image_path}",
                path=image_path,
            )

        extension = image_path.suffix.lower()
        if extension not in self.SUPPORTED_EXTENSIONS:
            return self._error_result(
                start, "UNSUPPORTED_FORMAT",
                f"Ошибка: формат изображения {extension or '<без расширения>'} не поддерживается.",
                path=image_path,
            )

        base64_image = self._encode_image(image_path)
        if not base64_image:
            return self._error_result(
                start, "ENCODE_FAILED",
                "Ошибка: Не удалось прочитать или закодировать изображение.",
                path=image_path,
            )

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

            if not answer:
                return self._error_result(
                    start, "EMPTY_VISION_RESPONSE",
                    "Vision-модель вернула пустой результат.",
                    path=image_path,
                )

            return {
                "ok": True,
                "department": self.NAME,
                "model": self.model,
                "latency_ms": int((time.time() - start) * 1000),
                "text": answer,
                "metadata": {
                    "path": str(image_path),
                    "format": extension,
                    "engine": "OllamaVision",
                },
                "error": None
            }
        except Exception as exc:
            return self._error_result(
                start, "VISION_ENGINE_ERROR",
                "Ошибка при обращении к VLM модели Ollama.",
                path=image_path,
                metadata={"exception_type": type(exc).__name__},
            )

    def _error_result(self, start, error, text, path=None, metadata=None):
        result_metadata = dict(metadata or {})
        if path is not None:
            result_metadata["path"] = str(path)
            result_metadata["format"] = path.suffix.lower()
        return {
            "ok": False,
            "department": self.NAME,
            "model": self.model,
            "latency_ms": max(0, int((time.time() - start) * 1000)),
            "text": text,
            "error": str(error),
            "metadata": result_metadata,
        }
