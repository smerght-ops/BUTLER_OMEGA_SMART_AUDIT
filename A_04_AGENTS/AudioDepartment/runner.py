# -*- coding: utf-8 -*-
import re
import time
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment
from A_00_UTILS.llm_output_sanitizer import sanitize_llm_output


class AudioDepartment(BaseDepartment):
    NAME = "AUDIO"
    VERSION = "2.0"
    CAPABILITIES = ["speech_synthesis", "speech_recognition"]
    DEPENDENCIES = ["configured audio_engine"]
    DATA_READS = ["user-provided audio path"]
    DATA_WRITES = ["audio engine output"]
    AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".flac"}

    def can_handle(self, text: str, context: dict = None) -> bool:
        q = (text or "").lower()
        attachments = (context or {}).get("attachments", [])
        return any(x in q for x in (
            "озвучь", "озвучить", "скажи голосом",
            "прочитай вслух", "распознай речь", "транскрибируй", "mp3", ".wav",
        )) or any(str(path).lower().endswith(tuple(self.AUDIO_EXTENSIONS)) for path in attachments)

    def _mode(self, query, context):
        q = (query or "").lower()
        attachments = context.get("attachments", [])
        if attachments or any(x in q for x in ("распознай", "транскриб", "что сказано")):
            return "recognize"
        return "synthesize"

    def execute(self, text: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        context = dict(context or {})
        mode = self._mode(text, context)
        engine = context.get("audio_engine")

        if mode == "recognize":
            attachments = context.get("attachments", [])
            path = Path(str(attachments[0]).strip().strip("\"'")) if attachments else None
            if path is None or not path.exists() or not path.is_file():
                return self._result(start, False, "Аудиофайл не найден.", "AUDIO_NOT_FOUND", mode, path)
            payload = str(path)
        else:
            payload = re.sub(
                r"^(?:озвучь(?:\s+текст)?|озвучить|скажи голосом|прочитай вслух)\s*[:—-]?\s*",
                "", (text or "").strip(), flags=re.I,
            ).strip().strip("\"")
            if not payload:
                return self._result(start, False, "Не указан текст для озвучивания.", "EMPTY_AUDIO_RESPONSE", mode)

        if not callable(engine):
            return self._result(
                start, False, "Движок синтеза/распознавания речи не настроен.",
                "AUDIO_ENGINE_NOT_AVAILABLE", mode,
            )
        try:
            output = engine(mode=mode, payload=payload, context=context)
            if isinstance(output, dict):
                output = output.get("text") or output.get("audio_path")
            output = sanitize_llm_output(output)
            if not output:
                return self._result(start, False, "Audio Engine вернул пустой ответ.", "EMPTY_AUDIO_RESPONSE", mode)
            return self._result(start, True, output, None, mode)
        except Exception as exc:
            return self._result(
                start, False, "Ошибка Audio Engine.", "AUDIO_ENGINE_NOT_AVAILABLE", mode,
                extra={"exception_type": type(exc).__name__},
            )

    def _result(self, start, ok, text, error, mode, path=None, extra=None):
        metadata = {"mode": mode, **dict(extra or {})}
        if path is not None:
            metadata["path"] = str(path)
        return {
            "ok": ok, "department": self.NAME, "model": "AudioDepartment",
            "latency_ms": int((time.time() - start) * 1000), "text": text,
            "error": error, "metadata": metadata,
        }
