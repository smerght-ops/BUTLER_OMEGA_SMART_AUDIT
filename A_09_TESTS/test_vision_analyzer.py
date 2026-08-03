# A_09_TESTS/test_vision_analyzer.py
import sys

sys.path.insert(0, ".")

from A_03_HANDLERS.vision_analyzer import VisionAnalyzer


def run_tests():
    analyzer = VisionAnalyzer()

    print("=" * 60)
    print("RUNNING VISION ANALYZER TESTS")
    print("=" * 60)

    result = analyzer.analyze_document("A_99_TEST_DATA/hello.png")

    assert result["success"] is True, "VisionAnalyzer failed on hello.png"
    assert result["text"], "VisionAnalyzer returned empty text"
    assert "engine" in result, "Missing engine field"
    assert "profile" in result, "Missing profile field"

    print("[ OK ] Document image analysis works.")
    print("[ OK ] Text:", result["text"])
    print("[ OK ] Type:", result["type"])
    print("[ OK ] Engine:", result["engine"])

    result_pdf_page = analyzer.analyze_document("A_99_TEST_DATA/pdf_page_test.png")

    assert result_pdf_page["success"] is True, "VisionAnalyzer failed on rendered PDF page"
    assert result_pdf_page["text"], "Rendered PDF page returned empty text"

    print("[ OK ] Rendered PDF page analysis works.")
    print("[ OK ] Text length:", len(result_pdf_page["text"]))
    print("=" * 60)


if __name__ == "__main__":
    run_tests()