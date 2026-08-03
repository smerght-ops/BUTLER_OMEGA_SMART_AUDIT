from pathlib import Path

class OCRBackend:
    """
    Butler OCR Backend v1.0

    Предназначен для:
      - OCR печатного текста;
      - будущей поддержки рукописного текста;
      - использования VisionEngine и PDFHandler.
    """

    def analyze(self, image_path):
        image_path = Path(image_path)

        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "backend": "OCRBackend",
                    "available": False,
                    "reason": "pytesseract is not installed",
                    "install": "pip install pytesseract pillow"
                }
            }

        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)

            return {
                "success": True,
                "text": text.strip(),
                "metadata": {
                    "backend": "OCRBackend",
                    "available": True,
                    "text_length": len(text.strip())
                }
            }

        except Exception as ex:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "backend": "OCRBackend",
                    "available": True,
                    "error": str(ex)
                }
            }