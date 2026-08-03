from pathlib import Path
import tempfile

from A_03_HANDLERS.base_handler import BaseHandler
from A_03_HANDLERS.code_detector import looks_like_code


class PDFHandler(BaseHandler):

    SUPPORTED = {".pdf"}

    def can_handle(self, path):
        return Path(path).suffix.lower() in self.SUPPORTED

    def operate(self, action, **kwargs):
        from A_03_HANDLERS import pdf_operations
        function = getattr(pdf_operations, action, None)
        if function is None:
            raise pdf_operations.PDFOperationError("PDF_OPERATION_FAILED", f"Неизвестная PDF-операция: {action}")
        return function(**kwargs)

    def extract(self, path):

        path = Path(path)

        text_result = self._extract_text_pdf(path)

        if text_result.get("success") and text_result.get("text", "").strip():
            return text_result

        vision_result = self._extract_scanned_pdf_with_vision(path)

        if vision_result.get("success"):
            return vision_result

        return {
            "success": False,
            "text": "",
            "metadata": {
                "handler": "PDFHandler",
                "needs_ocr": True,
                "text_pdf_error": text_result.get("metadata", {}),
                "vision_pdf_error": vision_result.get("metadata", {}),
            }
        }

    def _extract_text_pdf(self, path):

        try:
            try:
                import PyPDF2 as pdf_library
            except ImportError:
                import pypdf as pdf_library
        except Exception:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "handler": "PDFHandler",
                    "error": "PyPDF2/pypdf is not installed",
                    "needs_ocr": False
                }
            }

        try:
            pages_text = []

            with open(path, "rb") as f:
                reader = pdf_library.PdfReader(f)

                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    pages_text.append(page_text)

            text = "\n".join(pages_text).strip()

            return {
                "success": True,
                "text": text,
                "metadata": {
                    "handler": "PDFHandler",
                    "mode": "text",
                    "pages": len(pages_text),
                    "needs_ocr": False,
                    "is_code": looks_like_code(text),
                    "text_length": len(text)
                }
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "handler": "PDFHandler",
                    "mode": "text",
                    "error": str(e),
                    "needs_ocr": True
                }
            }

    def _extract_scanned_pdf_with_vision(self, path):

        try:
            import fitz
        except Exception:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "handler": "PDFHandler",
                    "mode": "vision_ocr",
                    "error": "PyMuPDF is not installed",
                    "needs_dependency": "pip install pymupdf",
                    "needs_ocr": True
                }
            }

        try:
            from A_03_HANDLERS.vision_engine import VisionEngine

            vision = VisionEngine()
            doc = fitz.open(str(path))

            page_texts = []
            page_metadata = []

            with tempfile.TemporaryDirectory(prefix="butler_pdf_ocr_") as tmp:
                tmp_dir = Path(tmp)

                for index in range(len(doc)):
                    page = doc.load_page(index)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

                    img_path = tmp_dir / f"page_{index + 1}.png"
                    pix.save(str(img_path))

                    result = vision.analyze(img_path)

                    metadata = result.get("metadata", {}) or {}
                    text = result.get("text", "") or ""

                    page_texts.append(text)
                    page_metadata.append({
                        "page": index + 1,
                        "success": bool(result.get("success")),
                        "text_length": len(text),
                        "backend": metadata.get("backend"),
                        "engine": metadata.get("engine"),
                        "type": metadata.get("type"),
                        "summary": metadata.get("summary"),
                        "needs_review": metadata.get("needs_review", False)
                    })

            merged_text = "\n\n".join(
                t for t in page_texts if t.strip()
            ).strip()

            if not merged_text:
                return {
                    "success": False,
                    "text": "",
                    "metadata": {
                        "handler": "PDFHandler",
                        "mode": "vision_ocr",
                        "pages": len(page_texts),
                        "needs_ocr": True,
                        "page_metadata": page_metadata,
                        "error": "Vision OCR returned empty text"
                    }
                }

            return {
                "success": True,
                "text": merged_text,
                "metadata": {
                    "handler": "PDFHandler",
                    "mode": "vision_ocr",
                    "pages": len(page_texts),
                    "needs_ocr": False,
                    "is_code": looks_like_code(merged_text),
                    "text_length": len(merged_text),
                    "engine": "VisionEngine-v3-Hybrid",
                    "page_metadata": page_metadata
                }
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "handler": "PDFHandler",
                    "mode": "vision_ocr",
                    "error": str(e),
                    "needs_ocr": True
                }
            }
