# -*- coding: utf-8 -*-
"""Regression tests for Evidence-Gated Completion (P0 blocker fix).

Covers all 8 required scenarios from the technical specification:
1. Structure only — SUCCESS forbidden
2. Mixed directory — requires content evidence
3. Placeholder answer — never leads to SUCCESS
4. Filename inference — filenames are not content
5. Unsupported content — SUCCESS forbidden when analysis impossible
6. Representative content — at least one supported document must be read
7. Multimodal scope — vision only when query requires it
8. Reasoning continuation — loop continues after structure until content present

Each test uses a mock department_dispatch that simulates realistic tool observations.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure the project root is on sys.path so CapabilityRegistry can be imported
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from A_03_ORCHESTRATION.agent_core_coordinator import EvidenceTracker


# ===================================================================
# Helper: build a mock observation that simulates a tool result
# ===================================================================

def _structure_obs(ok=True) -> dict:
    """Simulate a directory listing / file metadata observation."""
    return {
        "ok": ok,
        "department": "FILESYSTEM",
        "text": (
            "Directory contents:\n"
            "- report.txt\n"
            "- data.xlsx\n"
            "- image.png\n"
            "- notes.docx\n"
        ),
    }


def _content_obs(ok=True, text: str = "Actual file content here") -> dict:
    """Simulate a file-read observation with actual extracted content."""
    return {
        "ok": ok,
        "department": "FILESYSTEM",
        "text": text,
    }


def _error_obs() -> dict:
    """Simulate a failed tool call."""
    return {"ok": False, "error": "READ_FAILED"}


# ===================================================================
# Test 1 — Structure only: SUCCESS forbidden when content required
# ===================================================================

def test_structure_only_content_query():
    """Query asks for file contents but only structure evidence is collected.
    
    Expected: evidence_sufficient() == False → completion blocked.
    """
    tracker = EvidenceTracker()
    tracker.classify_query("Проанализируй содержимое каталога C:\\Test")
    tracker.record_observation(_structure_obs())

    assert not tracker.evidence_sufficient(), (
        "FAIL: Structure-only evidence should NOT be sufficient for content query"
    )
    assert tracker.requires_content is True
    assert tracker.has_structure_evidence is True
    assert tracker.has_content_evidence is False
    print("TEST 1 PASS — structure only blocks completion")


# ===================================================================
# Test 2 — Mixed directory: requires content evidence
# ===================================================================

def test_mixed_directory_requires_content():
    """Mixed directory (txt, xlsx, png) with a query asking for analysis.
    
    Expected: without reading any file → insufficient; after reading one → sufficient.
    """
    tracker = EvidenceTracker()
    tracker.classify_query("Проанализируй каталог и покажи что внутри файлов")

    # Before any reads
    assert not tracker.evidence_sufficient(), "Should be insufficient before reads"

    # After structure listing only
    tracker.record_observation(_structure_obs())
    assert not tracker.evidence_sufficient(), (
        "Structure listing alone should NOT satisfy content analysis query"
    )

    # After reading one file's content
    tracker.record_observation(_content_obs(text="This is the report content"))
    assert tracker.evidence_sufficient(), (
        "After reading at least one file, evidence should be sufficient"
    )
    print("TEST 2 PASS — mixed directory requires content evidence")


# ===================================================================
# Test 3 — Placeholder answer: never leads to SUCCESS
# ===================================================================

def test_placeholder_never_success():
    """A query requiring content analysis with only placeholder/empty observations.
    
    Expected: insufficient regardless of observation count if no real content.
    """
    tracker = EvidenceTracker()
    tracker.classify_query("Прочитай все файлы в каталоге и опиши их")

    # Multiple structure-only observations (e.g., repeated directory listings)
    for _ in range(3):
        tracker.record_observation(_structure_obs())

    assert not tracker.evidence_sufficient(), (
        "Repeated structure observations should NOT satisfy content query"
    )

    # Empty text observation (simulates a read that returned nothing useful)
    tracker.record_observation({"ok": True, "department": "FILESYSTEM", "text": ""})
    assert not tracker.evidence_sufficient(), (
        "Empty-text observation should NOT count as content evidence"
    )
    print("TEST 3 PASS — placeholder/empty observations don't satisfy completion")


# ===================================================================
# Test 4 — Filename inference: filenames are not content
# ===================================================================

def test_filename_inference_not_content():
    """A query that could be answered from filenames alone should NOT be
    accepted as sufficient when the user asked for content analysis.
    
    Expected: structure evidence (filenames) is insufficient for content queries.
    """
    tracker = EvidenceTracker()
    tracker.classify_query("Что написано в файлах каталога C:\\Test")

    # Only filename-based observations
    tracker.record_observation(_structure_obs())
    assert not tracker.evidence_sufficient(), (
        "Filename-only evidence should NOT satisfy 'what is written' query"
    )

    # Verify the classification was correct
    assert tracker.requires_content is True, (
        "Query about what's written in files must require content analysis"
    )
    print("TEST 4 PASS — filenames are not content")


# ===================================================================
# Test 5 — Unsupported content: SUCCESS forbidden when analysis impossible
# ===================================================================

def test_unsupported_content():
    """When the query requires content but all reads fail or return unsupported format.
    
    Expected: evidence_sufficient() == False → completion blocked, loop continues.
    """
    tracker = EvidenceTracker()
    tracker.classify_query("Проанализируй содержимое всех файлов в каталоге")

    # Multiple failed reads
    for _ in range(3):
        tracker.record_observation(_error_obs())

    assert not tracker.evidence_sufficient(), (
        "Failed reads should NOT satisfy content query"
    )

    # One structure listing + multiple failures
    tracker.record_observation(_structure_obs())
    assert not tracker.evidence_sufficient(), (
        "Structure + failed reads should still be insufficient"
    )
    print("TEST 5 PASS — unsupported/unreadable content blocks completion")


# ===================================================================
# Test 6 — Representative content: at least one supported document read
# ===================================================================

def test_representative_content():
    """When a directory contains supported documents and the query asks for analysis,
    reading at least one representative file should be sufficient.
    
    Expected: after reading one file → evidence_sufficient() == True.
    """
    tracker = EvidenceTracker()
    tracker.classify_query("Прочитай документы в каталоге и дай краткий обзор")

    # Structure listing first (typical workflow)
    tracker.record_observation(_structure_obs())
    assert not tracker.evidence_sufficient(), "Structure alone insufficient"

    # Read one representative document
    tracker.record_observation(_content_obs(
        text="Annual report 2025: revenue increased by 15% compared to previous year."
    ))
    assert tracker.evidence_sufficient(), (
        "After reading one representative file, evidence should be sufficient"
    )
    print("TEST 6 PASS — representative content satisfies completion")


# ===================================================================
# Test 7 — Multimodal scope: vision only when query requires it
# ===================================================================

def test_multimodal_scope():
    """A structure-only query (list files) should NOT require vision.
    A query about images SHOULD require content/vision evidence.
    
    Expected: different classification based on query intent.
    """
    # Structure-only query — no vision needed
    tracker1 = EvidenceTracker()
    tracker1.classify_query("Перечисли файлы в каталоге C:\\Test")
    assert tracker1._query_type == "structure", (
        "Listing files should be classified as structure-only"
    )

    # Image analysis query — requires content/vision
    tracker2 = EvidenceTracker()
    tracker2.classify_query("Проанализируй изображения в каталоге")
    assert tracker2.requires_content is True, (
        "Image analysis query should require content evidence"
    )

    # Structure listing for image query — insufficient
    tracker2.record_observation(_structure_obs())
    assert not tracker2.evidence_sufficient(), (
        "Structure alone insufficient for image analysis query"
    )
    print("TEST 7 PASS — multimodal scope correctly classified")


# ===================================================================
# Test 8 — Reasoning continuation: loop continues after structure
# ===================================================================

def test_reasoning_continuation():
    """After receiving only a directory listing, the evidence gate must force
    the reasoning loop to continue until content evidence is collected.
    
    Expected: evidence_sufficient() == False after structure → True after content read.
    """
    tracker = EvidenceTracker()
    tracker.classify_query("Проанализируй содержимое каталога C:\\Test")

    # Step 1: receive directory listing (typical first tool call)
    tracker.record_observation(_structure_obs())
    assert not tracker.evidence_sufficient(), (
        "After structure only, loop MUST continue"
    )

    # Step 2: read one file's content
    tracker.record_observation(_content_obs(text="File contents extracted"))
    assert tracker.evidence_sufficient(), (
        "After reading content, evidence is sufficient — loop can complete"
    )
    print("TEST 8 PASS — reasoning continues until content evidence collected")


# ===================================================================
# Additional: query classification edge cases
# ===================================================================

def test_query_classification_edge_cases():
    """Verify that the classifier handles various query forms correctly."""
    # English queries
    t1 = EvidenceTracker()
    t1.classify_query("Read all files in C:\\Test and analyze their content")
    assert t1.requires_content is True, "English 'read and analyze' should require content"

    t2 = EvidenceTracker()
    t2.classify_query("List the directory structure of C:\\Test")
    assert t2._query_type == "structure", "Listing should be structure-only"

    # Ambiguous query — defaults to permissive (unknown)
    t3 = EvidenceTracker()
    t3.classify_query("Tell me about this folder")
    assert t3._query_type in ("unknown", "structure"), (
        f"Ambiguous query classified as '{t3._query_type}'"
    )

    # Query with both structure and content keywords — content takes priority
    t4 = EvidenceTracker()
    t4.classify_query("Покажи список файлов и прочитай их содержимое")
    assert t4.requires_content is True, (
        "Query mentioning both listing and reading should require content"
    )

    print("TEST EDGE CASES PASS — query classification handles edge cases correctly")


# ===================================================================
# Run all tests
# ===================================================================

if __name__ == "__main__":
    tests = [
        test_structure_only_content_query,
        test_mixed_directory_requires_content,
        test_placeholder_never_success,
        test_filename_inference_not_content,
        test_unsupported_content,
        test_representative_content,
        test_multimodal_scope,
        test_reasoning_continuation,
        test_query_classification_edge_cases,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"FAIL — {test_fn.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR — {test_fn.__name__}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"Evidence Gate Regression Tests: {passed} passed, {failed} failed")
    if failed == 0:
        print("ALL TESTS PASSED — Evidence-Gated Completion verified.")
    else:
        sys.exit(1)
