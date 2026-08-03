# A_09_TESTS/test_search_engine.py
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, ".")

from A_07_MEMORY.search_engine import SemanticSearchEngine


TEST_INDEX = Path("A_07_MEMORY/TEST_INDEX.jsonl")
TEST_SYNONYMS = Path("A_07_MEMORY/TEST_SYNONYMS.json")


def setup_mock_data():
    synonyms = {
        "смазка": ["масло", "литол", "солидол"],
        "масло": ["смазка"],
        "передняя бабка": ["headstock"],
        "станок": ["lathe", "machine"]
    }

    records = [
        {
            "path": "A_06_WORKSPACE\\incoming\\lathe_1E61M.pdf",
            "handler": "PDFHandler",
            "tags": ["mechanical", "lathe", "1E61M", "смазка"],
            "entities": ["Станок 1E61M", "Передняя бабка", "Суппорт"],
            "summary": "Чертеж передняя бабка и узлы смазки станка",
            "text": "В документе описана смазка передней бабки и масло для узлов."
        },
        {
            "path": "A_06_WORKSPACE\\incoming\\trolley_axis.txt",
            "handler": "TextHandler",
            "tags": ["butler", "axis", "engineering"],
            "entities": ["Тележка", "Ось 26мм"],
            "summary": "Расчет смещения центра оси от низа рамы тележки",
            "text": "Тележка и ось 26мм."
        }
    ]

    with TEST_SYNONYMS.open("w", encoding="utf-8") as f:
        json.dump(synonyms, f, ensure_ascii=False, indent=2)

    with TEST_INDEX.open("w", encoding="utf-8") as f:
        f.write(json.dumps(records[0], ensure_ascii=False) + "\n")
        f.write("{\n")
        f.write(json.dumps(records[1], ensure_ascii=False) + "\n")


def cleanup():
    if TEST_INDEX.exists():
        os.remove(TEST_INDEX)
    if TEST_SYNONYMS.exists():
        os.remove(TEST_SYNONYMS)


def run_tests():
    setup_mock_data()

    engine = SemanticSearchEngine(
        index_path=TEST_INDEX,
        synonyms_path=TEST_SYNONYMS
    )

    print("=" * 60)
    print("RUNNING SEMANTIC SEARCH ENGINE v2.0 TESTS")
    print("=" * 60)

    records = engine._load_all()
    assert len(records) == 2, f"Expected 2 valid records, got {len(records)}"
    print("[ OK ] JSONL recovery works.")

    res_phrase = engine.search('"передняя бабка"')
    assert len(res_phrase) >= 1, "Phrase search failed"
    assert "lathe_1E61M.pdf" in res_phrase[0][1]["path"], "Wrong phrase result"
    print(f"[ OK ] Phrase search works. Score: {res_phrase[0][0]}")

    res_multi = engine.search("станок смазка")
    assert len(res_multi) >= 1, "Multi-token search failed"
    assert "lathe_1E61M.pdf" in res_multi[0][1]["path"], "Wrong multi-token result"
    print(f"[ OK ] Multi-token search works. Score: {res_multi[0][0]}")

    res_morph = engine.search("смазкой")
    assert len(res_morph) >= 1, "Russian word-form search failed"
    assert "lathe_1E61M.pdf" in res_morph[0][1]["path"], "Wrong morphology result"
    print(f"[ OK ] Simple Russian word-form normalization works. Score: {res_morph[0][0]}")

    res_syn = engine.search("масло")
    assert len(res_syn) >= 1, "Synonym search failed"
    assert "lathe_1E61M.pdf" in res_syn[0][1]["path"], "Wrong synonym result"
    print(f"[ OK ] Synonym expansion works. Score: {res_syn[0][0]}")

    res_tag = engine.search_by_tag("lathe")
    assert len(res_tag) == 1, "Tag search failed"
    print("[ OK ] search_by_tag works.")

    res_entity = engine.search_by_entity("передняя")
    assert len(res_entity) == 1, "Entity search failed"
    print("[ OK ] search_by_entity works.")

    cleanup()
    print("=" * 60)


if __name__ == "__main__":
    try:
        run_tests()
    finally:
        cleanup()