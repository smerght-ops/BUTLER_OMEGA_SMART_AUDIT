# A_03_HANDLERS/pdf_ocr_pipeline.py
import hashlib
import json
import tempfile
from datetime import datetime
from pathlib import Path

import fitz

from A_03_HANDLERS.vision_engine import VisionEngine


class PDFOCRPipeline:
    """
    Resumable OCR pipeline for scanned or image-based PDFs.

    This module is an extension over VisionEngine.
    It does NOT replace PDFHandler and does NOT touch Butler core.
    """

    def __init__(
        self,
        progress_dir="A_08_LOGS/pdf_ocr_progress",
        render_dpi=200
    ):
        self.progress_dir = Path(progress_dir)
        self.progress_dir.mkdir(parents=True, exist_ok=True)
        self.render_dpi = render_dpi
        self.vision = VisionEngine()

    def _sha256(self, path):
        h = hashlib.sha256()
        with Path(path).open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def _progress_path(self, pdf_path):
        pdf_hash = self._sha256(pdf_path)
        return self.progress_dir / f"{pdf_hash}.json"

    def _load_progress(self, pdf_path):
        progress_path = self._progress_path(pdf_path)

        if not progress_path.exists():
            return {
                "pdf_path": str(pdf_path),
                "pdf_hash": self._sha256(pdf_path),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "pages": {},
                "complete": False
            }

        try:
            with progress_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {
                "pdf_path": str(pdf_path),
                "pdf_hash": self._sha256(pdf_path),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "pages": {},
                "complete": False,
                "recovered_from_corrupt_progress": True
            }

    def _save_progress(self, pdf_path, progress):
        progress["updated_at"] = datetime.utcnow().isoformat()
        progress_path = self._progress_path(pdf_path)

        tmp_path = progress_path.with_suffix(".tmp")

        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

        tmp_path.replace(progress_path)

    def _render_page_to_png(self, page, output_path):
        pix = page.get_pixmap(dpi=self.render_dpi)
        pix.save(str(output_path))
        return output_path

    def process(self, pdf_path, max_pages=None, force=False):
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "error": "PDF file not found",
                    "path": str(pdf_path),
                    "pipeline": "PDFOCRPipeline"
                }
            }

        progress = self._load_progress(pdf_path)

        try:
            doc = fitz.open(str(pdf_path))
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "metadata": {
                    "error": str(e),
                    "pipeline": "PDFOCRPipeline"
                }
            }

        page_count = len(doc)
        target_pages = page_count

        if max_pages is not None:
            target_pages = min(page_count, int(max_pages))

        processed = 0
        failed = 0

        with tempfile.TemporaryDirectory(prefix="butler_pdf_ocr_") as tmp_dir:
            tmp_dir = Path(tmp_dir)

            for page_index in range(target_pages):
                page_key = str(page_index)

                if (
                    not force
                    and page_key in progress["pages"]
                    and progress["pages"][page_key].get("success") is True
                ):
                    continue

                page_result = {
                    "page": page_index + 1,
                    "success": False,
                    "text": "",
                    "metadata": {}
                }

                try:
                    page = doc[page_index]
                    image_path = tmp_dir / f"page_{page_index + 1}.png"

                    self._render_page_to_png(page, image_path)

                    vision_result = self.vision.analyze(image_path)

                    page_result["success"] = bool(vision_result.get("success"))
                    page_result["text"] = vision_result.get("text", "")
                    page_result["metadata"] = vision_result.get("metadata", {})
                    page_result["engine"] = page_result["metadata"].get(
                        "engine",
                        "VisionEngine"
                    )

                    if page_result["success"]:
                        processed += 1
                    else:
                        failed += 1

                except Exception as e:
                    page_result["success"] = False
                    page_result["error"] = str(e)
                    failed += 1

                progress["pages"][page_key] = page_result
                self._save_progress(pdf_path, progress)

        doc.close()

        ordered_pages = [
            progress["pages"][str(i)]
            for i in range(target_pages)
            if str(i) in progress["pages"]
        ]

        combined_text_parts = []

        for item in ordered_pages:
            page_number = item.get("page", "?")
            text = item.get("text", "") or ""

            if text.strip():
                combined_text_parts.append(
                    f"--- PAGE {page_number} ---\n{text.strip()}"
                )

        complete = all(
            str(i) in progress["pages"]
            and progress["pages"][str(i)].get("success") is True
            for i in range(target_pages)
        )

        progress["complete"] = complete
        self._save_progress(pdf_path, progress)

        return {
            "success": complete or bool(combined_text_parts),
            "text": "\n\n".join(combined_text_parts),
            "metadata": {
                "pipeline": "PDFOCRPipeline",
                "engine": "VisionEngine",
                "pdf_path": str(pdf_path),
                "page_count": page_count,
                "target_pages": target_pages,
                "processed_now": processed,
                "failed_now": failed,
                "complete": complete,
                "progress_file": str(self._progress_path(pdf_path)),
                "resume_supported": True
            }
        }