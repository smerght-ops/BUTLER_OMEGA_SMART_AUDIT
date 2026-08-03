# A_09_TESTS/test_pdf_ocr_pipeline.py
import sys
from pathlib import Path

sys.path.insert(0, ".")

from A_03_HANDLERS.pdf_ocr_pipeline import PDFOCRPipeline


def run_tests():
    print("=" * 60)
    print("RUNNING PDF OCR PIPELINE TESTS")
    print("=" * 60)

    pdf_path = Path("A_99_TEST_DATA/hello.pdf")

    assert pdf_path.exists(), "Test PDF not found: A_99_TEST_DATA/hello.pdf"

    pipeline = PDFOCRPipeline()
    result = pipeline.process(pdf_path, max_pages=1)

    assert result["success"] is True, "PDFOCRPipeline failed"
    assert result["text"], "PDFOCRPipeline returned empty text"

    metadata = result.get("metadata", {})

    assert metadata.get("resume_supported") is True, "Resume support flag missing"
    assert Path(metadata.get("progress_file")).exists(), "Progress file was not created"

    print("[ OK ] PDF page rendered and processed through VisionEngine.")
    print("[ OK ] Progress file:", metadata.get("progress_file"))
    print("[ OK ] Text length:", len(result["text"]))
    print("=" * 60)


if __name__ == "__main__":
    run_tests()