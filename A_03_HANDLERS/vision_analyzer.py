# A_03_HANDLERS/vision_analyzer.py
from pathlib import Path
from A_03_HANDLERS.vision_engine import VisionEngine


class VisionAnalyzer:
    """
    High-level cognitive analyzer over VisionEngine.
    Does not replace VisionEngine and does not touch Butler core.
    """

    ROLE_PROFILES = {
        "document": {
            "intent": "extract_text_and_summary",
            "description": "General document or scan analysis"
        },
        "code": {
            "intent": "detect_code_and_preserve_structure",
            "description": "Code screenshot analysis"
        },
        "schematic": {
            "intent": "describe_structure_and_entities",
            "description": "Schematic, drawing or technical diagram analysis"
        },
        "photo": {
            "intent": "describe_scene_and_objects",
            "description": "Photo understanding"
        },
        "auto": {
            "intent": "auto_detect",
            "description": "Automatic content type detection"
        }
    }

    def __init__(self):
        self.engine = VisionEngine()

    def analyze(self, image_path, profile="auto"):
        image_path = Path(image_path)

        if profile not in self.ROLE_PROFILES:
            profile = "auto"

        raw = self.engine.analyze(image_path)
        metadata = raw.get("metadata", {}) or {}

        text = raw.get("text", "") or ""
        detected_type = metadata.get("type", "unknown")
        summary = metadata.get("summary", "")
        entities = metadata.get("entities", [])
        tags = metadata.get("tags", [])

        is_code = self._looks_like_code(text)

        if is_code and "code" not in tags:
            tags.append("code")

        result = {
            "success": bool(raw.get("success")),
            "path": str(image_path),
            "profile": profile,
            "profile_intent": self.ROLE_PROFILES[profile]["intent"],
            "type": "code_screenshot" if is_code else detected_type,
            "text": text,
            "summary": summary,
            "entities": entities,
            "tags": tags,
            "is_code": is_code,
            "needs_review": bool(metadata.get("needs_review", False)),
            "engine": metadata.get("engine", "VisionEngine"),
            "backend": metadata.get("backend", ""),
            "raw_metadata": metadata
        }

        return result

    def analyze_document(self, image_path):
        return self.analyze(image_path, profile="document")

    def analyze_code_screenshot(self, image_path):
        return self.analyze(image_path, profile="code")

    def analyze_schematic(self, image_path):
        return self.analyze(image_path, profile="schematic")

    def _looks_like_code(self, text):
        if not text:
            return False

        markers = [
            "def ",
            "class ",
            "import ",
            "from ",
            "return ",
            "function ",
            "const ",
            "let ",
            "var ",
            "{",
            "}",
            "=>",
            "SELECT ",
            "CREATE TABLE",
            "if ",
            "else:",
            "try:",
            "except "
        ]

        lowered = text.lower()
        hits = 0

        for marker in markers:
            if marker.lower() in lowered:
                hits += 1

        return hits >= 2