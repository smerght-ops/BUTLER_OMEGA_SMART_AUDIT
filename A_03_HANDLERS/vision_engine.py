from pathlib import Path

from A_03_HANDLERS.ocr_backend import OCRBackend
from A_03_HANDLERS.ollama_vision_backend import OllamaVisionBackend


class VisionEngine:

    def __init__(self):
        self.vision = OllamaVisionBackend()
        self.ocr = OCRBackend()

    def analyze(self, image_path):

        image_path = Path(image_path)

        # 1. Сначала пробуем Ollama Vision
        result = self.vision.analyze(image_path)

        if result.get("success"):
            result.setdefault("metadata", {})
            result["metadata"]["engine"] = "VisionEngine-v3-Hybrid"
            return result

        # 2. Если Ollama недоступна — резервный OCR
        fallback = self.ocr.analyze(image_path)

        fallback.setdefault("metadata", {})
        fallback["metadata"]["engine"] = "VisionEngine-v3-Hybrid"

        return fallback