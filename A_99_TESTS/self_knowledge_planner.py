# -*- coding: utf-8 -*-
"""Build the separate Self Knowledge roadmap from diagnostic evidence."""

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM = ROOT / "A_99_TESTS/reports/latest_exam_report.json"
PROPOSALS = ROOT / "A_99_TESTS/repair_proposals.json"
QUESTIONS = ROOT / "A_99_TESTS/questions.json"
OUTPUT = ROOT / "ROADMAP_SELF_KNOWLEDGE.md"


def main() -> int:
    exam = json.loads(EXAM.read_text(encoding="utf-8-sig"))
    proposals = json.loads(PROPOSALS.read_text(encoding="utf-8-sig"))
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8-sig"))
    low_blocks = sorted(exam.get("block_scores", {}).items(), key=lambda item: item[1])
    rejected = [item for item in proposals.get("proposals", []) if item.get("validation_status") == "REJECTED"]
    validated = [item for item in proposals.get("proposals", []) if item.get("validation_status") == "VALIDATED"]
    missing = questions.get("missing_required_sources", [])
    lines = [
        "# ROADMAP SELF KNOWLEDGE", "", f"Generated: {datetime.now().isoformat(timespec='seconds')}  ",
        f"Current score: **{exam.get('self_knowledge_score')}/100**", "", "## Today", "",
    ]
    for block, score in low_blocks:
        if score < 100:
            lines.append(f"- Разобрать блок `{block}`: PASS score {score}.")
    if not any(score < 100 for _, score in low_blocks):
        lines.append("- Блоков ниже 100 нет.")
    lines.extend(["", "## Manual conflict review", ""])
    if rejected:
        roots = sorted({item.get("root_cause") for item in rejected})
        lines.extend(f"- Ручной разбор причины `{root}`; не применять изменения без подтверждения." for root in roots)
    else:
        lines.append("- Непроверенных конфликтов нет.")
    lines.extend(["", "## Sources", ""])
    lines.extend(f"- Документировать отсутствующий источник `{path}` либо официально исключить его из обязательных." for path in missing)
    if not missing:
        lines.append("- Все обязательные источники найдены.")
    lines.extend(["", "## Validated proposals", "", f"- VALIDATED: {len(validated)}", f"- REJECTED: {len(rejected)}", "", "## Next exam", "", "- После ручного решения выполнить generator → exam → analyzer.", "- Принять изменение только при FAST/FULL без FAIL, score не ниже baseline и уменьшении conflicts."])
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PLAN_CREATED: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
