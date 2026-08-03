# -*- coding: utf-8 -*-
"""Butler Self Knowledge Exam. Diagnostic only; it never repairs project data."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "A_99_TESTS" / "self_knowledge_questions.json"
REPORT_DIR = ROOT / "A_99_TESTS" / "reports" / "self_knowledge"
BLOCK_WEIGHTS = {
    "departments": 25,
    "architecture": 15,
    "memory": 15,
    "purpose": 10,
    "goal_planner": 10,
    "inspectors": 8,
    "acceptance": 7,
    "history": 5,
    "runtime": 5,
}
STATUSES = ("PASS", "PARTIAL", "FAIL", "UNKNOWN", "UNSTABLE", "CONFLICT", "SOURCE_ERROR")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def existing_source(*choices: str) -> str:
    for choice in choices:
        if (ROOT / choice).exists():
            return choice
    return choices[0]


def build_questions() -> list[dict]:
    """One-time, explicit database build from current, verifiable artifacts."""
    acceptance_path = existing_source("A_99_TESTS/reports/latest_acceptance_report.json")
    state_path = existing_source("A_00_ARCHITECTURE/PROJECT_STATE.json", "PROJECT_STATE.json")
    capability_path = existing_source("A_00_ARCHITECTURE/BUTLER_CAPABILITY_AUDIT.json", "BUTLER_CAPABILITY_AUDIT.json")
    constitution_path = existing_source("A_00_ARCHITECTURE/CONSTITUTION.md", "CONSTITUTION.md")
    memory_path = existing_source("A_00_ARCHITECTURE/PROJECT_MEMORY_INDEX.json")
    roadmap_path = existing_source("ROADMAP_6_0_BUTLER_OMEGA_SMART_UPDATED.md", "ROADMAP_6_0_BUTLER_OMEGA_SMART.md")
    purpose_path = existing_source("НАЗНАЧЕНИЕ_BUTLER.md")
    inspector0 = existing_source("Inspector0_PhysicalMap.json")
    inspector1 = existing_source("Inspector1_EntityMap.json")
    inspector2 = existing_source("Inspector2_ImportMap.json")
    inspector3 = existing_source("Inspector3_RegistrationMap.json")
    inspector4 = existing_source("Inspector4_CallGraph.json")
    inspector5 = existing_source("Inspector5_DependencyGraph.json")

    acceptance = read_json(ROOT / acceptance_path)
    counts = acceptance.get("counts", {})
    project_state = read_json(ROOT / state_path)
    memory_index = read_json(ROOT / memory_path)
    entities = read_json(ROOT / inspector1).get("payload", [])
    departments = []
    for item in entities:
        for cls in item.get("classes", []):
            name = str(cls.get("name", ""))
            if name.endswith("Department") and name not in departments:
                departments.append(name)
    if not departments:
        departments = ["MemoryDepartment"]

    specs = {
        "purpose": {
            "questions": [
                "Расскажи о себе: контроль назначения Butler №{n}.",
                "Расскажи о себе: какова подтверждённая идентичность проекта, проверка №{n}?",
            ],
            "keywords": ["Проект:", "Возможности по Capability Audit"],
            "sources": [purpose_path, constitution_path, state_path, capability_path],
            "truth": ["BUTLER"],
        },
        "memory": {
            "questions": [
                "Как устроена твоя память? Проверка подтверждённых компонентов №{n}.",
                "Какая у тебя память? Не предполагай неподтверждённые уровни, проверка №{n}.",
            ],
            "keywords": ["Архитектура памяти", "дополнительные уровни не предполагаются"],
            "sources": [memory_path, "PASSPORT_SUMMARY.md"],
            "truth": ["MEMORY"],
        },
        "architecture": {
            "questions": [
                "Что ты знаешь о своём проекте? Архитектурная сверка №{n}.",
                "Что изменилось после последнего обновления? Архитектурная сверка №{n}.",
            ],
            "keywords": ["Версия архитектуры:", str(project_state.get("architecture_version")), "approved:"],
            "sources": [state_path, constitution_path],
            "truth": [str(project_state.get("architecture_version"))],
        },
        "goal_planner": {
            "questions": [
                "Что уже сделано в Goal Planner и связанных компонентах? Проверка №{n}.",
                "Что осталось по Goal Planner и оркестрации? Проверка №{n}.",
            ],
            "keywords": ["статус"],
            "sources": [roadmap_path, memory_path],
            "truth": ["Goal"],
        },
        "history": {
            "questions": [
                "Что уже завершено в истории проекта? Проверка №{n}.",
                "Что ещё не реализовано по дорожной карте? Историческая сверка №{n}.",
            ],
            "keywords": ["пункт"],
            "sources": [roadmap_path, memory_path],
            "truth": ["Статус"],
        },
        "inspectors": {
            "questions": [
                "Что находится внутри {department}? Проверка Inspector №{n}.",
                "Что находится внутри {department}? Назови найденные Inspector возможности, проверка №{n}.",
            ],
            "keywords": ["по Inspector", "Department"],
            "sources": [inspector0, inspector1, inspector2, inspector3, inspector4, inspector5],
            "truth": ["payload"],
        },
        "acceptance": {
            "questions": [
                "Что ты знаешь о своём проекте? Назови последний Acceptance, проверка №{n}.",
                "Что изменилось после последнего обновления? Сверь PASS, FAIL и SKIP, проверка №{n}.",
            ],
            "keywords": [f"PASS {counts.get('PASS')}", f"FAIL {counts.get('FAIL')}", f"SKIP {counts.get('SKIP')}"],
            "sources": [acceptance_path],
            "truth": ["counts"],
        },
        "runtime": {
            "questions": [
                "Что ты знаешь о своём проекте? Runtime и локальная среда, проверка №{n}.",
                "Расскажи о себе: какие Runtime-факты документально подтверждены, проверка №{n}?",
            ],
            "keywords": ["Проект:"],
            "sources": [state_path, capability_path],
            "truth": ["project"],
        },
    }

    questions = []
    per_block = 45
    for block in BLOCK_WEIGHTS:
        spec = specs.get(block)
        if block == "departments":
            spec = {
                "questions": [
                    "Какие Department активны? Проверка регистрации №{n}.",
                    "Что находится внутри {department}? Проверка Department №{n}.",
                ],
                "keywords": ["Department"],
                "sources": [acceptance_path, inspector0, inspector1, inspector3],
                "truth": ["payload"],
            }
        for offset in range(per_block):
            n = offset + 1
            department = departments[offset % len(departments)]
            template = spec["questions"][offset % len(spec["questions"])]
            question = template.format(n=n, department=department)
            required = list(spec["keywords"])
            if "внутри" in question.casefold():
                required = [department, "Inspector"]
            qid = f"SK-{len(questions) + 1:04d}"
            questions.append({
                "id": qid,
                "block": block,
                "question": question,
                "expected_department": "MEMORY",
                "required_keywords": required,
                "required_sections": [],
                "truth_sources": list(spec["sources"]),
                "truth_checks": list(spec["truth"]),
                "related_questions": [],
                "weight": 1,
            })

    by_block = defaultdict(list)
    for question in questions:
        by_block[question["block"]].append(question)
    for group in by_block.values():
        for index, question in enumerate(group):
            question["related_questions"] = [group[(index + 1) % len(group)]["id"]]
    return questions


def write_questions() -> None:
    questions = build_questions()
    if not 300 <= len(questions) <= 500:
        raise RuntimeError(f"Question count out of contract: {len(questions)}")
    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "generation_mode": "one_time_from_verified_project_artifacts",
        "questions": questions,
    }
    QUESTIONS.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"QUESTIONS_BUILT: {len(questions)}")


def validate_source(question: dict) -> tuple[bool, list[dict]]:
    checks = []
    expected_fragments = [str(value).casefold() for value in question.get("truth_checks", []) if str(value)]
    any_fragment = not expected_fragments
    for relative in question.get("truth_sources", []):
        path = ROOT / relative
        item = {"path": relative, "exists": path.is_file(), "sha256": None, "truth_match": False}
        if path.is_file():
            item["sha256"] = sha256(path)
            try:
                content = path.read_text(encoding="utf-8-sig", errors="replace").casefold()
                item["truth_match"] = any(fragment in content for fragment in expected_fragments) if expected_fragments else True
                any_fragment = any_fragment or item["truth_match"]
            except OSError:
                pass
        checks.append(item)
    return bool(checks) and all(item["exists"] for item in checks) and any_fragment, checks


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().casefold())


def grade(question: dict, answers: list[dict], source_ok: bool) -> tuple[str, list[str]]:
    reasons = []
    if not source_ok:
        return "SOURCE_ERROR", ["truth source missing, unreadable, or does not contain the declared fact"]
    if any(not answer.get("ok") for answer in answers):
        return "FAIL", ["one or more Result Contracts have ok != true"]
    if any(str(answer.get("department", "")).upper() != question["expected_department"] for answer in answers):
        return "FAIL", ["official route returned an unexpected Department"]
    texts = [str(answer.get("text") or "").strip() for answer in answers]
    if any(not text for text in texts):
        return "FAIL", ["empty answer"]
    if len({normalized(text) for text in texts}) != 1:
        return "UNSTABLE", ["three answers differ for unchanged project state"]
    required = [str(value) for value in question.get("required_keywords", [])]
    missing = [value for value in required if value.casefold() not in texts[0].casefold()]
    if missing:
        reasons.append("missing required facts: " + ", ".join(missing))
        if len(missing) < max(2, len(required)):
            return "PARTIAL", reasons
        return "FAIL", reasons
    sections = [str(value) for value in question.get("required_sections", [])]
    missing_sections = [value for value in sections if value.casefold() not in texts[0].casefold()]
    if missing_sections:
        return "PARTIAL", ["missing required sections: " + ", ".join(missing_sections)]
    return "PASS", reasons


def source_paths_from_result(result: dict) -> list[str]:
    sources = (result.get("metadata") or {}).get("sources") or []
    if isinstance(sources, dict):
        sources = list(sources.values())
    return [str(item.get("path")) for item in sources if isinstance(item, dict) and item.get("status") == "read"]


def previous_report(current_path: Path | None = None):
    candidates = sorted(REPORT_DIR.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True)
    for path in candidates:
        if path != current_path:
            try:
                data = read_json(path)
                if "counts" in data and "score" in data:
                    return {"path": str(path.relative_to(ROOT)), "counts": data["counts"], "score": data["score"]}
            except (OSError, ValueError):
                continue
    return None


def calculate_scores(results: list[dict]) -> tuple[dict, float, float]:
    by_block = defaultdict(list)
    for item in results:
        by_block[item["block"]].append(item)
    values = {"PASS": 1.0, "PARTIAL": 0.5, "UNKNOWN": 1.0}
    block_scores = {}
    total = 0.0
    for block, weight in BLOCK_WEIGHTS.items():
        group = by_block.get(block, [])
        score = 100.0 * sum(values.get(item["status"], 0.0) for item in group) / max(1, len(group))
        block_scores[block] = round(score, 2)
        total += score * weight / 100.0
    conflicts = sum(1 for item in results if item["status"] == "CONFLICT")
    trust = max(0.0, total - conflicts * 0.25)
    return block_scores, round(total, 2), round(trust, 2)


def detect_conflicts(results: list[dict]) -> list[dict]:
    by_id = {item["id"]: item for item in results}
    conflicts = []
    seen = set()
    for item in results:
        for related_id in item.get("related_questions", []):
            pair = tuple(sorted((item["id"], related_id)))
            related = by_id.get(related_id)
            if pair in seen or not related:
                continue
            seen.add(pair)
            if item["block"] == related["block"] and {item["status"], related["status"]} == {"PASS", "FAIL"}:
                conflicts.append({
                    "question_a": item["id"], "question_b": related["id"],
                    "answer_a": item["answers"][0].get("text"),
                    "answer_b": related["answers"][0].get("text"),
                    "truth_sources": sorted(set(item["truth_sources"] + related["truth_sources"])),
                    "nature": "linked answers disagree on required verified facts",
                })
                item["status"] = "CONFLICT"
                related["status"] = "CONFLICT"
    return conflicts


def diagnose(status: str, result: dict) -> str | None:
    if status == "SOURCE_ERROR":
        return "source is missing, stale, unreadable, or question/source binding is invalid"
    if status == "UNSTABLE":
        return "answer formation is nondeterministic or external state changed"
    if status == "CONFLICT":
        actual = sorted({str(answer.get("department")) for answer in result.get("answers", []) if answer.get("department")})
        expected = str(result.get("expected_department"))
        if any(value != expected for value in actual):
            return f"routing conflict: expected {expected}, official route returned {', '.join(actual) or 'NONE'}"
        return "related Butler answers contradict each other while using the same verified sources"
    if status in {"FAIL", "PARTIAL"}:
        if any(answer.get("department") != "MEMORY" for answer in result["answers"]):
            return "routing error"
        observed = set(result.get("observed_sources", []))
        declared = set(result.get("truth_sources", []))
        if not observed.intersection(declared):
            return "MemoryDepartment does not expose the declared existing truth source"
        return "answer formation omits or misstates a required verified fact"
    return None


def render_markdown(report: dict) -> str:
    lines = [
        "# Self Knowledge Exam Report", "",
        f"Timestamp: `{report['timestamp']}`  ",
        f"Questions: **{report['question_count']}**  ",
        f"Score: **{report['score']}/100**  ",
        f"Trust score: **{report['trust_score']}/100**", "",
        "## Status distribution", "",
    ]
    for status in STATUSES:
        lines.append(f"- {status}: {report['counts'].get(status, 0)}")
    lines.extend(["", "## Block scores", ""])
    for block, score in report["block_scores"].items():
        lines.append(f"- {block}: {score}")
    lines.extend(["", "## Source coverage", "", f"- Declared sources: {report['source_coverage']['declared_count']}", f"- Observed sources: {report['source_coverage']['observed_count']}", f"- Coverage: {report['source_coverage']['percent']}%"])
    lines.extend(["", "## Previous exam", "", f"```json\n{json.dumps(report.get('comparison'), ensure_ascii=False, indent=2)}\n```"])
    lines.extend(["", "## Conflicts", ""])
    lines.append("None" if not report["conflicts"] else f"```json\n{json.dumps(report['conflicts'], ensure_ascii=False, indent=2)}\n```")
    lines.extend(["", "## Findings requiring attention", ""])
    findings = [item for item in report["results"] if item["status"] not in {"PASS", "UNKNOWN"}]
    if not findings:
        lines.append("None")
    for item in findings:
        lines.append(f"- `{item['id']}` {item['status']}: {item.get('diagnosis') or '; '.join(item.get('reasons', []))}")
    lines.extend(["", "## Repairs", "", f"- Attempted: {len(report.get('repairs_attempted', []))}", f"- Accepted: {len(report.get('repairs_accepted', []))}", f"- Rejected: {len(report.get('repairs_rejected', []))}"])
    lines.extend(["", "## Validation", "", f"- FAST: {report.get('fast_result') or 'not run in diagnostic-only mode'}", f"- FULL: {report.get('full_result') or 'not run in diagnostic-only mode'}", f"- Final project state: {report.get('project_state', 'diagnostic-only; unchanged')}"])
    return "\n".join(lines) + "\n"


def run_exam(report_suffix: str = "") -> dict:
    if not QUESTIONS.exists():
        raise FileNotFoundError("Question database is absent. Run with --build-questions once.")
    payload = read_json(QUESTIONS)
    questions = payload.get("questions", [])
    if not 300 <= len(questions) <= 500:
        raise ValueError(f"Question database must contain 300-500 questions, got {len(questions)}")

    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2

    dispatcher = SmartDispatcherV2()
    results = []
    started = time.perf_counter()
    for index, question in enumerate(questions, 1):
        source_ok, source_checks = validate_source(question)
        answers = []
        for repeat in range(3):
            call_started = time.perf_counter()
            try:
                answer = dispatcher.dispatch(question["question"], context={"self_knowledge_exam": True, "repeat": repeat + 1})
            except Exception as exc:
                answer = {"ok": False, "department": None, "text": "", "error": type(exc).__name__, "metadata": {"exception_message": str(exc)}}
            answer = dict(answer or {})
            answer["exam_elapsed_ms"] = int((time.perf_counter() - call_started) * 1000)
            answers.append(answer)
        status, reasons = grade(question, answers, source_ok)
        observed = sorted(set(path for answer in answers for path in source_paths_from_result(answer)))
        item = dict(question)
        item.update({"status": status, "reasons": reasons, "answers": answers, "source_checks": source_checks, "observed_sources": observed})
        item["diagnosis"] = diagnose(status, item)
        results.append(item)
        if index % 25 == 0 or index == len(questions):
            print(f"EXAM_PROGRESS: {index}/{len(questions)}", flush=True)

    conflicts = detect_conflicts(results)
    for item in results:
        item["diagnosis"] = diagnose(item["status"], item)
    counts = Counter(item["status"] for item in results)
    block_scores, score, trust_score = calculate_scores(results)
    declared = sorted(set(path for item in results for path in item["truth_sources"]))
    observed = sorted(set(path for item in results for path in item["observed_sources"]))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") + report_suffix
    report = {
        "timestamp": timestamp,
        "mode": "diagnostic_only",
        "question_database": str(QUESTIONS.relative_to(ROOT)),
        "question_database_sha256": sha256(QUESTIONS),
        "question_count": len(questions),
        "distribution_by_block": dict(Counter(item["block"] for item in results)),
        "counts": {status: counts.get(status, 0) for status in STATUSES},
        "block_scores": block_scores,
        "score": score,
        "trust_score": trust_score,
        "source_coverage": {"declared_count": len(declared), "observed_count": len(set(declared).intersection(observed)), "percent": round(100 * len(set(declared).intersection(observed)) / max(1, len(declared)), 2), "declared": declared, "observed": observed},
        "conflicts": conflicts,
        "comparison": previous_report(),
        "repairs_attempted": [], "repairs_accepted": [], "repairs_rejected": [],
        "fast_result": None, "full_result": None,
        "changed_files": [], "restored_backups": [],
        "project_state": "unchanged by diagnostic exam",
        "elapsed_ms": int((time.perf_counter() - started) * 1000),
        "results": results,
    }
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"{timestamp}.json"
    md_path = REPORT_DIR / f"{timestamp}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    (REPORT_DIR / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (REPORT_DIR / "latest.md").write_text(render_markdown(report), encoding="utf-8")
    print(f"REPORT_JSON: {json_path.relative_to(ROOT)}")
    print(f"REPORT_MD: {md_path.relative_to(ROOT)}")
    print(f"QUESTIONS: {len(questions)}")
    print(" ".join(f"{status}={counts.get(status, 0)}" for status in STATUSES))
    print(f"SCORE: {score}")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-questions", action="store_true", help="explicitly rebuild the static question database")
    parser.add_argument("--report-suffix", default="")
    args = parser.parse_args()
    if args.build_questions:
        write_questions()
        return 0
    run_exam(args.report_suffix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
