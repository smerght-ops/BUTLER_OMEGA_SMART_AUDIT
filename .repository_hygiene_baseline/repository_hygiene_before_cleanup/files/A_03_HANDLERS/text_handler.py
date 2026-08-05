from pathlib import Path
from A_03_HANDLERS.base_handler import BaseHandler

class TextHandler(BaseHandler):

    supported_extensions = [".txt", ".md", ".log"]

    def extract(self, path: Path):

        for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
            try:
                text = path.read_text(encoding=enc)
                return {
                    "success": True,
                    "text": text,
                    "metadata": {
                        "encoding": enc,
                        "handler": "TextHandler"
                    }
                }
            except Exception:
                pass

        return {
            "success": False,
            "text": "",
            "metadata": {
                "handler": "TextHandler"
            }
        }
