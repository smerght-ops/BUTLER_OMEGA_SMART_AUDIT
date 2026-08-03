from pathlib import Path
from A_03_HANDLERS.base_handler import BaseHandler
from A_03_HANDLERS.code_detector import detect_language_by_extension

class CodeHandler(BaseHandler):

    supported_extensions = [
        ".py", ".ps1", ".bat", ".cmd",
        ".js", ".ts", ".html", ".css", ".json",
        ".sql", ".cpp", ".c", ".h", ".hpp",
        ".cs", ".java", ".php", ".rb", ".go",
        ".rs", ".sh", ".yml", ".yaml", ".xml"
    ]

    def extract(self, path: Path):

        for enc in ("utf-8", "utf-8-sig", "cp1251", "latin-1"):
            try:
                text = path.read_text(encoding=enc)

                return {
                    "success": True,
                    "text": text,
                    "metadata": {
                        "handler": "CodeHandler",
                        "encoding": enc,
                        "language": detect_language_by_extension(path),
                        "is_code": True,
                        "lines": len(text.splitlines())
                    }
                }

            except Exception:
                pass

        return {
            "success": False,
            "text": "",
            "metadata": {
                "handler": "CodeHandler",
                "is_code": True,
                "error": "Cannot read file with supported encodings"
            }
        }