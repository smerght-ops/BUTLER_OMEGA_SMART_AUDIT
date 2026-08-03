# -*- coding: utf-8 -*-
import base64
import os
import re
import time
from pathlib import Path

import requests

from A_01_CORE.manifest_loader import ManifestLoader
from A_02_MANAGERS.model_registry import MODEL_REGISTRY
from A_04_AGENTS.base_department import BaseDepartment
from A_00_UTILS.llm_output_sanitizer import NO_REASONING_PROMPT, sanitize_llm_output


class VideoDepartment(BaseDepartment):
    NAME = "VIDEO"
    VERSION = "2.0"
    CAPABILITIES = ["video_frame_sampling", "video_content_analysis"]
    DEPENDENCIES = ["OpenCV", "Ollama", "configured vision model"]
    DATA_READS = ["user-provided video path"]
    DATA_WRITES = []
    SUPPORTED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}

    def __init__(self):
        cfg = ManifestLoader.load()
        base = cfg.get("ollama_url", "http://127.0.0.1:11434/api/chat").replace("/api/chat", "")
        self.generate_url = base.rstrip("/") + "/api/generate"
        self.model = MODEL_REGISTRY.get("VISION", cfg.get("vision_model", "qwen2.5-vl:latest"))

    def can_handle(self, text: str, context: dict = None) -> bool:
        q = (text or "").lower()
        attachments = (context or {}).get("attachments", [])
        explicit_action = any(x in q for x in (
            "проанализируй видео", "опиши видео", "создай видео", "сделай видео",
            "что на видео", "извлеки кадры", "распознай видео",
        ))
        concrete_path = any(x in q for x in (".mp4", ".avi", ".mov", ".mkv", ".webm"))
        return explicit_action or concrete_path or any(
            str(path).lower().endswith(tuple(self.SUPPORTED_EXTENSIONS)) for path in attachments
        )

    def _path(self, query, context):
        attachments = context.get("attachments", [])
        if attachments:
            return Path(str(attachments[0]).strip().strip("\"'"))
        match = re.search(r"([A-Za-z]:[^\n\r\"']+\.(?:mp4|avi|mov|mkv|webm))", query or "", re.I)
        return Path(match.group(1).strip()) if match else None

    def _sample_frames(self, path, count=6):
        try:
            import cv2
        except ImportError as exc:
            raise RuntimeError("OpenCV is not installed") from exc
        capture = cv2.VideoCapture(str(path))
        if not capture.isOpened():
            raise RuntimeError("video decoder could not open the file")
        total = max(1, int(capture.get(cv2.CAP_PROP_FRAME_COUNT)))
        frames = []
        try:
            for index in sorted({int(i * (total - 1) / max(1, count - 1)) for i in range(count)}):
                capture.set(cv2.CAP_PROP_POS_FRAMES, index)
                ok, frame = capture.read()
                if not ok:
                    continue
                encoded, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 82])
                if encoded:
                    frames.append(base64.b64encode(buffer.tobytes()).decode("ascii"))
        finally:
            capture.release()
        if not frames:
            raise RuntimeError("no frames decoded")
        return frames

    def execute(self, text: str, context: dict = None, **kwargs) -> dict:
        start = time.time()
        context = dict(context or {})
        path = self._path(text, context)
        if path is None or not path.exists() or not path.is_file():
            return self._result(start, False, "Видеофайл не найден.", "VIDEO_NOT_FOUND", path)
        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return self._result(start, False, f"Формат {path.suffix} не поддерживается.", "UNSUPPORTED_VIDEO_FORMAT", path)
        try:
            frames = self._sample_frames(path)
            prompt = (
                f"{NO_REASONING_PROMPT}\nПроанализируй последовательные кадры одного видео. "
                f"Опиши происходящее, объекты, людей, действия и заметные изменения.\nЗапрос: {text}"
            )
            response = requests.post(
                self.generate_url,
                json={"model": self.model, "prompt": prompt, "images": frames, "stream": False},
                timeout=300,
            )
            response.raise_for_status()
            answer = sanitize_llm_output(response.json().get("response", ""))
            if not answer:
                return self._result(start, False, "Видео-модель вернула пустой ответ.", "EMPTY_VIDEO_RESPONSE", path)
            return self._result(start, True, answer, None, path, {"sampled_frames": len(frames)})
        except Exception as exc:
            return self._result(
                start, False, "Ошибка при анализе видео.", "VIDEO_ENGINE_ERROR", path,
                {"exception_type": type(exc).__name__, "exception_message": str(exc)},
            )

    def _result(self, start, ok, text, error, path=None, extra=None):
        metadata = {"mode": "video_analysis", **dict(extra or {})}
        if path is not None:
            metadata.update({"path": str(path), "format": path.suffix.lower()})
        return {
            "ok": ok, "department": self.NAME, "model": self.model,
            "latency_ms": int((time.time() - start) * 1000), "text": text,
            "error": error, "metadata": metadata,
        }
