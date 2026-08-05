import base64
import json
from pathlib import Path

import requests


class OllamaVisionBackend:

    def __init__(
        self,
        url="http://127.0.0.1:11434/api/generate",
        model="qwen2.5-vl:latest"
    ):
        self.url = url
        self.model = model

    def analyze(self, image_path):

        image_path = Path(image_path)

        with open(image_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")

        prompt = """
Проанализируй изображение.

Верни СТРОГО JSON:

{
  "text": "...",
  "type": "document|code|diagram|photo|ui|other",
  "summary": "...",
  "entities": [],
  "needs_review": false
}

Не используй markdown.
Не добавляй пояснений.
Верни только JSON.
"""

        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "prompt": prompt,
            "images": [img_b64]
        }

        try:

            r = requests.post(
                self.url,
                json=payload,
                timeout=300
            )

            r.raise_for_status()

            raw = r.json().get("response", "{}")

            parsed = json.loads(raw)

            return {
                "success": True,
                "text": parsed.get("text", ""),
                "metadata": {
                    "backend": "OllamaVisionBackend",
                    "type": parsed.get("type", "other"),
                    "summary": parsed.get("summary", ""),
                    "entities": parsed.get("entities", []),
                    "needs_review": parsed.get(
                        "needs_review",
                        False
                    )
                }
            }

        except Exception as ex:

            return {
                "success": False,
                "text": "",
                "metadata": {
                    "backend": "OllamaVisionBackend",
                    "error": str(ex)
                }
            }