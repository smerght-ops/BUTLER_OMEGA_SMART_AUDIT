# -*- coding: utf-8 -*-

import os
import re
import time
import uuid
import requests
from A_00_UTILS.llm_output_sanitizer import NO_REASONING_PROMPT, sanitize_llm_output

OLLAMA_URL = os.environ.get(
    "BUTLER_OLLAMA_BASE",
    "http://127.0.0.1:11434"
).rstrip("/") + "/api/generate"


class SmartDispatcher:
    def __init__(self, project_root=None):
        self.project_root = project_root

    def determine_role(self, text: str, has_image: bool = False) -> str:
        text = (text or "").lower()

        if has_image:
            return "vision"

        if re.search(r"(python|РєРѕРґ|code|traceback|ЃРїСЂР°РІСЊ|СЃРєСЂїС‚)", text):
            return "coder"

        if re.search(r"(РЅР°СЂЃСѓР№|СЃРіРµРЅРµСЂЂСѓР№.*РєР°СЂС‚Ѕ|СЃРѕР·РґР°Р№.*·РѕР±СЂР°Р¶)", text):
            return "image"

        return "chat"

    def _model_for_role(self, role: str) -> str:
        mapping = {
            "chat": "qwen35-ru:latest",
            "coder": "Codestral-Pro:latest",
            "vision": "qwen2.5-vl:latest",
            "dream": "qwen35-ru:latest",
            "image": "qwen35-ru:latest"
        }
        return mapping.get(role, "qwen35-ru:latest")

    def execute_employee(
        self,
        employee=None,
        system_prompt="",
        user_content="",
        has_image=False
    ):
        start = time.time()

        role = employee or self.determine_role(user_content, has_image)
        model = self._model_for_role(role)

        prompt = f"SYSTEM:\n{system_prompt}\n{NO_REASONING_PROMPT}\n\nUSER:\n{user_content}"

        dto = {
            "request_id": uuid.uuid4().hex[:8],
            "role": role,
            "model": model,
            "status": "error",
            "text": "",
            "latency_ms": 0,
            "fallback_used": False,
            "fallback_reason": None,
        }

        try:
            request_payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            if role == "chat":
                request_payload["think"] = False
                request_payload["options"] = {
                    "num_ctx": 4096,
                    "temperature": 0,
                }

            last_error = None
            data = None
            text = ""
            for attempt in range(3):
                try:
                    response = requests.post(
                        OLLAMA_URL,
                        json=request_payload,
                        timeout=180
                    )
                    response.raise_for_status()
                    candidate = response.json()
                    raw_text = candidate.get("response", "")
                    if not raw_text and "message" in candidate:
                        raw_text = candidate["message"].get("content", "")
                    cleaned = self.clean_model_output(raw_text)
                    if cleaned:
                        data = candidate
                        text = cleaned
                        break
                    last_error = RuntimeError("EMPTY_CHAT_RESPONSE")
                except Exception as exc:
                    last_error = exc
                if attempt < 2:
                    time.sleep(0.25)
            if data is None:
                raise last_error

            dto["status"] = "ok"
            dto["text"] = text

        except Exception as ex:
            dto["status"] = "error"
            dto["fallback_reason"] = str(ex)
            dto["text"] = ""

        dto["latency_ms"] = int((time.time() - start) * 1000)

        return dto

    @staticmethod
    def clean_model_output(text: str) -> str:
        return sanitize_llm_output(text)
