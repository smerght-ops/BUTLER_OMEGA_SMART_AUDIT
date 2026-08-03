# -*- coding: utf-8 -*-
"""Run the State Exam through SmartDispatcherV2 -> ButlerHarness -> Department."""

from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "A_99_TESTS" / "questions.json"
REPORTS = ROOT / "A_99_TESTS" / "reports"
ERROR_MARKERS = ("не удалось", "ошибка", "error", "traceback")
UNKNOWN_MARKERS = ("нет информации", "информация отсутствует", "описание отсутствует", "не указано")
BLOCK_WEIGHTS = {"departments": 2.0, "architecture": 1.5, "multilevel_memory": 1.5}


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").casefold().strip())


def source_exists(item: dict) -> bool:
    return bool(item.get("exists")) and (ROOT / str(item.get("path", ""))).is_file()


def observed_sources(answer: dict) -> set[str]:
    raw = (answer.get("metadata") or {}).get("sources") or []
    if isinstance(raw, dict):
        raw = list(raw.values())
    return {str(item.get("path")) for item in raw if isinstance(item, dict) and item.get("status") == "read"}


def grade(question: dict, answers: list[dict]) -> tuple[str, list[str], list[str]]:
    reasons, categories = [], []
    sources = question.get("truth_sources", [])
    if not sources or not any(source_exists(item) for item in sources):
        return "FAIL", ["No readable truth source"], ["NO_SOURCE", "DOCUMENTATION_GAP"]
    if any(not answer.get("ok") for answer in answers):
        return "FAIL", ["Result Contract ok != True"], ["RUNTIME_ERROR"]
    actual = {str(answer.get("department", "")).upper() for answer in answers}
    if actual != {str(question.get("expected_department", "MEMORY")).upper()}:
        return "FAIL", [f"Unexpected Department: {sorted(actual)}"], ["RUNTIME_ERROR"]
    texts = [str(answer.get("text") or "").strip() for answer in answers]
    if any(not text for text in texts):
        return "FAIL", ["Empty answer"], ["MISSING_ANSWER"]
    if any(len(text) < int(question.get("minimum_length", 20)) for text in texts):
        return "FAIL", ["Answer is shorter than minimum length"], ["MISSING_ANSWER"]
    if len({normalized(text) for text in texts}) > 1:
        return "UNSTABLE", ["Three answers differ"], []
    text = texts[0]
    if any(marker in normalized(text) for marker in ERROR_MARKERS):
        return "FAIL", ["Answer contains an error marker"], ["RUNTIME_ERROR"]
    if any(marker in normalized(text) for marker in UNKNOWN_MARKERS):
        return "UNKNOWN", ["Butler honestly reports missing information"], ["DOCUMENTATION_GAP"]
    keywords = question.get("expected_keywords", [])
    missing_keywords = [word for word in keywords if normalized(str(word)) not in normalized(text)]
    sections = question.get("required_sections", [])
    missing_sections = [section for section in sections if normalized(str(section)) not in normalized(text)]
    if missing_keywords and len(missing_keywords) == len(keywords):
        return "FAIL", ["All expected keywords are missing: " + ", ".join(missing_keywords)], ["MISSING_ANSWER"]
    if missing_keywords or missing_sections:
        reasons.append("Missing keywords: " + ", ".join(missing_keywords) if missing_keywords else "Keywords present")
        reasons.append("Missing sections: " + ", ".join(missing_sections) if missing_sections else "Sections present")
        categories.append("INCOMPLETE_ANSWER")
        return "PARTIAL", reasons, categories
    confidence_matches = re.findall(r"(?<!\d)(\d{1,3})\s*%", text)
    if confidence_matches and min(int(value) for value in confidence_matches) < 50:
        return "PARTIAL", ["Reported confidence is below 50%"], ["LOW_CONFIDENCE"]
    return "PASS", [], []


def consistency(results: list[dict]) -> list[dict]:
    by_id = {item["id"]: item for item in results}
    conflicts, seen = [], set()
    for item in results:
        for related_id in item.get("related_questions", []):
            related = by_id.get(related_id)
            key = tuple(sorted((item["id"], related_id)))
            if not related or key in seen:
                continue
            seen.add(key)
            stable_states = {item["status"], related["status"]}
            if "PASS" in stable_states and stable_states.intersection({"FAIL", "UNKNOWN"}):
                conflict = {
                    "question_a": item["id"], "question_b": related["id"],
                    "status_a": item["status"], "status_b": related["status"],
                    "answer_a": item["answers"][0].get("text"),
                    "answer_b": related["answers"][0].get("text"),
                    "type": "LINK_CONSISTENCY",
                }
                conflicts.append(conflict)
                item["consistency_conflicts"].append(related["id"])
                related["consistency_conflicts"].append(item["id"])
    return conflicts


def scores(results: list[dict]) -> tuple[dict, float]:
    grouped = defaultdict(list)
    for item in results:
        grouped[item["block"]].append(item)
    block_scores = {block: round(100 * sum(item["status"] == "PASS" for item in group) / len(group), 2) for block, group in grouped.items()}
    weighted = sum(block_scores[block] * BLOCK_WEIGHTS.get(block, 1.0) for block in block_scores)
    weight_sum = sum(BLOCK_WEIGHTS.get(block, 1.0) for block in block_scores)
    return block_scores, round(weighted / max(1.0, weight_sum), 2)


def markdown(report: dict) -> str:
    lines = ["# Butler State Exam", "", f"Timestamp: `{report['timestamp']}`  ", f"Questions: **{report['question_count']}**  ", f"Self Knowledge Score: **{report['self_knowledge_score']}/100**", "", "## Results", ""]
    for name, count in report["counts"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Error categories", ""])
    for name, count in report["error_categories"].items():
        lines.append(f"- {name}: {count}")
    lines.extend(["", "## Block scores", ""])
    for name, score in report["block_scores"].items():
        lines.append(f"- {name}: {score}")
    lines.extend(["", "## Consistency", "", f"- CONSISTENCY CHECK conflicts: {len(report['consistency_conflicts'])}", f"- LINK CONSISTENCY performed: YES", "", "## Problems", ""])
    problems = [item for item in report["results"] if item["status"] != "PASS"]
    lines.extend(f"- `{item['id']}` {item['status']}: {'; '.join(item['reasons'])}" for item in problems[:200])
    if len(problems) > 200:
        lines.append(f"- … and {len(problems) - 200} more; see JSON report.")
    return "\n".join(lines) + "\n"


def main() -> int:
    data = json.loads(QUESTIONS.read_text(encoding="utf-8-sig"))
    questions = data.get("questions", [])
    if not questions:
        raise RuntimeError("questions.json is empty; run self_knowledge_question_generator.py")
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2
    dispatcher = SmartDispatcherV2()
    results, started = [], time.perf_counter()
    for index, question in enumerate(questions, 1):
        answers = []
        for repeat in range(3):
            call_started = time.perf_counter()
            try:
                answer = dict(dispatcher.dispatch(question["question"], context={"state_exam": True, "repeat": repeat + 1}) or {})
            except Exception as exc:
                answer = {"ok": False, "department": None, "text": "", "error": type(exc).__name__, "metadata": {"exception_message": str(exc)}}
            answer["exam_elapsed_ms"] = int((time.perf_counter() - call_started) * 1000)
            answers.append(answer)
        status, reasons, categories = grade(question, answers)
        item = dict(question)
        item.update({"status": status, "reasons": reasons, "error_categories": categories, "answers": answers, "observed_sources": sorted(set().union(*(observed_sources(answer) for answer in answers))), "consistency_conflicts": []})
        results.append(item)
        if index % 25 == 0 or index == len(questions):
            print(f"EXAM_PROGRESS: {index}/{len(questions)}", flush=True)
    conflicts = consistency(results)
    block_scores, score = scores(results)
    counts = Counter(item["status"] for item in results)
    categories = Counter(category for item in results for category in item["error_categories"])
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "timestamp": timestamp, "official_route": "SmartDispatcherV2 -> ButlerHarness -> Department",
        "question_count": len(results), "repeats_per_question": 3,
        "counts": {name: counts.get(name, 0) for name in ("PASS", "PARTIAL", "FAIL", "UNKNOWN", "UNSTABLE")},
        "error_categories": dict(categories), "block_scores": block_scores,
        "self_knowledge_score": score, "consistency_conflicts": conflicts,
        "elapsed_ms": int((time.perf_counter() - started) * 1000), "results": results,
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    json_path = REPORTS / f"exam_report_{timestamp}.json"
    md_path = REPORTS / f"exam_report_{timestamp}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    (REPORTS / "latest_exam_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORTS / "latest_exam_report.md").write_text(markdown(report), encoding="utf-8")
    print(f"REPORT_JSON: {json_path.relative_to(ROOT)}")
    print(f"SELF_KNOWLEDGE_SCORE: {score}")
    print(" ".join(f"{name}={counts.get(name, 0)}" for name in ("PASS", "PARTIAL", "FAIL", "UNKNOWN", "UNSTABLE")))
    print(f"CONFLICTS={len(conflicts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
