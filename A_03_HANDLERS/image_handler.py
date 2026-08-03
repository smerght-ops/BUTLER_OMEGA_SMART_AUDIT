from pathlib import Path

from A_03_HANDLERS.base_handler import BaseHandler
from A_03_HANDLERS.vision_engine import VisionEngine

class ImageHandler(BaseHandler):

    SUPPORTED = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".tif",
        ".tiff",
        ".webp",
    }

    def __init__(self):
        self.engine = VisionEngine()

    def can_handle(self, path):
        return Path(path).suffix.lower() in self.SUPPORTED

    def extract(self, path):
        result = self.engine.analyze(path)

        result.setdefault("metadata", {})
        result["metadata"]["handler"] = "ImageHandler"

        return result