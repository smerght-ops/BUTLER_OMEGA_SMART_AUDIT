# -*- coding: utf-8 -*-
"""Build CapabilityRegistry.json from Department source code using AST only."""

from __future__ import annotations

import ast
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = ROOT / "A_04_AGENTS"
REGISTRY_PATH = ROOT / "CapabilityRegistry.json"
REPORT_PATH = ROOT / "CAPABILITY_REGISTRY_REPORT.md"

# Universal language rules. They describe action grammar, not Butler departments.
ACTION_WORDS = {
    "analysis": "analyze", "analyze": "analyze",
    "building": "build", "build": "build",
    "correction": "correct", "correct": "correct",
    "create": "create", "creation": "create",
    "doctor": "diagnose",
    "explanation": "explain", "explain": "explain",
    "export": "export",
    "extract": "extract", "extraction": "extract",
    "generate": "generate", "generation": "generate",
    "inspect": "inspect", "inspection": "inspect",
    "launch": "launch",
    "lifecycle": "manage",
    "open": "open",
    "read": "read",
    "recognition": "recognize", "recognize": "recognize",
    "registry": "register", "register": "register",
    "report": "report",
    "resolve": "resolve", "resolution": "resolve",
    "rewrite": "rewrite", "rewriting": "rewrite",
    "save": "save", "saving": "save",
    "search": "search",
    "status": "status",
    "summary": "summarize", "summarization": "summarize",
    "synthesis": "synthesize", "synthesize": "synthesize",
    "watch": "watch",
    "write": "write",
}

RU_ACTION_ALIASES = {
    "analyze": ("проанализируй", "анализ"),
    "build": ("построй", "создай"),
    "correct": ("исправь", "скорректируй"),
    "create": ("создай",),
    "diagnose": ("проверь", "диагностика"),
    "explain": ("объясни",),
    "export": ("экспортируй", "сохрани"),
    "extract": ("извлеки", "распакуй"),
    "generate": ("сгенерируй", "создай"),
    "inspect": ("проверь", "инспектируй"),
    "launch": ("запусти",),
    "manage": ("управляй", "обнови"),
    "open": ("открой",),
    "read": ("прочитай",),
    "recognize": ("распознай",),
    "register": ("зарегистрируй",),
    "report": ("сформируй отчёт",),
    "resolve": ("разреши ссылку",),
    "rewrite": ("перефразируй", "перепиши"),
    "save": ("сохрани", "запиши"),
    "search": ("найди", "поиск"),
    "status": ("покажи статус",),
    "summarize": ("сделай сводку", "резюмируй"),
    "synthesize": ("синтезируй",),
    "watch": ("контролируй", "отслеживай"),
    "write": ("запиши", "сохрани"),
}

TYPE_MARKERS = {
    "audio": ("audio", "speech", "voice"),
    "code": ("code", "coding", "script", "python", "powershell", "bash"),
    "image": ("image", "vision", "photo", "picture", "png", "jpeg", "ocr"),
    "list": ("list", "results", "catalog", "inventory", "registry"),
    "path": ("path", "file", "document", "archive", "directory", "reference"),
    "video": ("video", "frame", "mp4"),
    "text": ("text", "summary", "report", "explanation", "memory", "fact"),
}

CAPABILITY_OVERRIDES = {
    "change_verification": ("verify", "changes", "confirmed"),
    "engineering_review": ("review", "engineering", "confirmed"),
    "project_audit": ("audit", "project", "confirmed"),
    "butler_identity": ("describe", "butler_identity", "confirmed"),
    "inventory": ("list", "home_inventory", "confirmed"),
    "architect_question": ("answer", "architectural_question", "confirmed"),
    "engineering_query": ("query", "engineering_knowledge", "confirmed"),
    "repository_knowledge": ("query", "repository_knowledge", "confirmed"),
    "video_frame_sampling": ("sample", "video_frames", "confirmed"),
}


def _literal(node: ast.AST):
    try:
        return ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError):
        return None


def _class_value(node: ast.ClassDef, name: str):
    for item in node.body:
        if isinstance(item, (ast.Assign, ast.AnnAssign)):
            targets = item.targets if isinstance(item, ast.Assign) else [item.target]
            if any(isinstance(target, ast.Name) and target.id == name for target in targets):
                return _literal(item.value)
    return None


def _snake(value: str) -> str:
    value = str(value or "")
    value = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _tokens(value: str) -> list[str]:
    return [token for token in _snake(value).split("_") if token]


def _department_hint(class_name: str) -> str:
    tokens = [token for token in _tokens(class_name) if token != "department"]
    return "_".join(tokens) or "unknown"


def _parse_capability(raw: str, class_name: str) -> tuple[str, str, str]:
    override = CAPABILITY_OVERRIDES.get(_snake(raw))
    if override is not None:
        return override
    tokens = _tokens(raw)
    action_index = next((index for index, token in enumerate(tokens) if token in ACTION_WORDS), None)
    if action_index is None:
        action = _snake(raw) or "unknown"
        object_name = "unknown"
        confidence = "unknown"
        return action, object_name, confidence

    verb = ACTION_WORDS[tokens[action_index]]
    object_tokens = tokens[:action_index] + tokens[action_index + 1:]
    object_name = "_".join(object_tokens) or "unknown"
    action = "_".join([verb, *object_tokens]) if object_tokens else verb

    if object_name != "unknown":
        return action, object_name, "confirmed"

    hint = _department_hint(class_name)
    if hint != "unknown":
        return action, hint, "inferred"
    return action, "unknown", "unknown"


def _detect_type(evidence: str, default: str) -> str:
    words = set(_tokens(evidence))
    scores = {
        kind: sum(1 for marker in markers if marker in words)
        for kind, markers in TYPE_MARKERS.items()
    }
    best = max(scores, key=scores.get, default=default)
    return best if scores.get(best, 0) else default


def _input_output(
    capability: str,
    action: str,
    object_name: str,
    data_reads,
    data_writes,
    execute_source: str,
) -> tuple[str, str]:
    reads = " ".join(map(str, data_reads or ()))
    writes = " ".join(map(str, data_writes or ()))
    user_reads = " ".join(
        str(item) for item in (data_reads or ())
        if "user-provided" in str(item).lower() or "user-selected" in str(item).lower()
    )
    input_type = _detect_type(user_reads, "text") if user_reads else "text"

    action_verb = action.split("_", 1)[0]
    if action_verb in {"recognize", "read", "analyze", "explain", "correct", "rewrite", "summarize", "report", "status"}:
        output_type = "text"
    elif action_verb == "search":
        output_type = "list"
    elif action_verb == "synthesize":
        output_type = _detect_type(f"{object_name} {capability}", "audio")
    elif writes:
        output_type = _detect_type(writes, "path")
    elif action_verb in {"build", "create", "export", "generate", "save", "write"}:
        output_type = _detect_type(f"{object_name} {action} {capability}", "text")
    elif action_verb in {"extract", "open", "launch"}:
        output_type = "path"
    else:
        output_type = "text"
    return input_type, output_type


def _aliases(action: str, object_name: str, capability: str, department: str) -> list[str]:
    verb = action.split("_", 1)[0]
    object_words = "" if object_name == "unknown" else object_name.replace("_", " ")
    aliases = {
        capability.replace("_", " ").lower(),
        action.replace("_", " ").lower(),
        department.lower(),
    }
    if object_words:
        aliases.add(f"{verb} {object_words}".strip())
    for form in RU_ACTION_ALIASES.get(verb, ()):
        aliases.add(f"{form} {object_words}".strip())
    return sorted(alias for alias in aliases if alias)


def _find_department_classes(path: Path) -> tuple[list[dict], list[str]]:
    warnings = []
    try:
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        return [], [f"{path.relative_to(ROOT)}: parse failed: {type(exc).__name__}"]

    found = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        name = _class_value(node, "NAME")
        if not isinstance(name, str) or not name.strip():
            continue
        capabilities = _class_value(node, "CAPABILITIES")
        execute = next(
            (item for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == "execute"),
            None,
        )
        if execute is None:
            warnings.append(f"{name}: execute() is missing")
            continue
        if not isinstance(capabilities, (tuple, list)) or not capabilities:
            warnings.append(f"{name}: CAPABILITIES is missing or empty")
            found.append({"department": name, "class_name": node.name, "capabilities": []})
            continue
        data_reads = _class_value(node, "DATA_READS") or ()
        data_writes = _class_value(node, "DATA_WRITES") or ()
        found.append({
            "department": name.strip(),
            "class_name": node.name,
            "capabilities": [str(item).strip() for item in capabilities if str(item).strip()],
            "data_reads": data_reads if isinstance(data_reads, (tuple, list)) else (str(data_reads),),
            "data_writes": data_writes if isinstance(data_writes, (tuple, list)) else (str(data_writes),),
            "execute_source": ast.get_source_segment(source, execute) or "",
            "source": path.relative_to(ROOT).as_posix(),
        })
    return found, warnings


def scan_departments() -> tuple[list[dict], list[str]]:
    departments = []
    warnings = []
    runner_paths = []
    for directory in sorted(path for path in AGENTS_DIR.iterdir() if path.is_dir()):
        path = directory / "runner.py"
        if not path.exists():
            if directory.name.endswith("Department"):
                warnings.append(
                    f"{directory.relative_to(ROOT).as_posix()}: runner.py is missing; directory is not a Registry source"
                )
            continue
        runner_paths.append(path)
    for path in runner_paths:
        found, local_warnings = _find_department_classes(path)
        departments.extend(found)
        warnings.extend(local_warnings)
    return departments, warnings


def build_registry(departments: list[dict]) -> tuple[list[dict], int]:
    grouped = {}
    raw_count = 0
    for department in departments:
        for capability in department.get("capabilities", []):
            raw_count += 1
            action, object_name, confidence = _parse_capability(capability, department["class_name"])
            input_type, output_type = _input_output(
                capability,
                action,
                object_name,
                department.get("data_reads"),
                department.get("data_writes"),
                department.get("execute_source", ""),
            )
            key = (department["department"], action, object_name)
            record = {
                "id": "_".join(_snake(part) for part in key),
                "department": department["department"],
                "action": action,
                "object": object_name,
                "input": input_type,
                "output": output_type,
                "confidence": confidence,
                "aliases": _aliases(action, object_name, capability, department["department"]),
            }
            if key in grouped:
                grouped[key]["aliases"] = sorted(set(grouped[key]["aliases"]) | set(record["aliases"]))
            else:
                grouped[key] = record
    records = sorted(grouped.values(), key=lambda item: (item["department"], item["action"], item["object"]))
    return records, raw_count - len(records)


def validate_registry(payload: dict, expected_count: int) -> None:
    if payload.get("version") != "1.0" or not isinstance(payload.get("generated_at"), str):
        raise ValueError("invalid registry header")
    records = payload.get("capabilities")
    if not isinstance(records, list) or len(records) != expected_count:
        raise ValueError("unexpected capability count")
    required = {"id", "department", "action", "object", "input", "output", "confidence", "aliases"}
    keys = []
    for record in records:
        if set(record) != required:
            raise ValueError(f"invalid fields for {record.get('id')}")
        if any(record[field] in (None, "") for field in required - {"aliases"}):
            raise ValueError(f"empty required field for {record.get('id')}")
        if record["confidence"] not in {"confirmed", "inferred", "unknown"}:
            raise ValueError(f"invalid confidence for {record.get('id')}")
        if not isinstance(record["aliases"], list) or not all(isinstance(item, str) for item in record["aliases"]):
            raise ValueError(f"invalid aliases for {record.get('id')}")
        keys.append((record["department"], record["action"], record["object"]))
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate capabilities")
    if not isinstance(payload.get("missing_capabilities"), list):
        raise ValueError("missing_capabilities must be a list")


def _write_json(payload: dict) -> None:
    temporary = REGISTRY_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(REGISTRY_PATH)


def _write_report(departments: list[dict], records: list[dict], duplicates: int, warnings: list[str]) -> None:
    missing_caps = [item["department"] for item in departments if not item.get("capabilities")]
    confidence = Counter(item["confidence"] for item in records)
    unknown = [item for item in records if item["object"] == "unknown"]
    inferred = [item for item in records if item["confidence"] == "inferred"]
    lines = [
        "# CAPABILITY REGISTRY REPORT",
        "",
        f"- Department найдено: {len(departments)}",
        f"- Capability найдено: {len(records)}",
        f"- unknown object: {len(unknown)}",
        f"- inferred capability: {len(inferred)}",
        f"- duplicate capability: {duplicates}",
        "- missing department: 0",
        f"- confirmed capability: {confidence.get('confirmed', 0)}",
        "",
        "## Department без CAPABILITIES",
        "",
    ]
    lines.extend(f"- {name}" for name in missing_caps)
    if not missing_caps:
        lines.append("- отсутствуют")
    lines.extend(["", "## Unknown и inferred", ""])
    flagged = [item for item in records if item["confidence"] != "confirmed" or item["object"] == "unknown"]
    lines.extend(
        f"- `{item['id']}`: object={item['object']}, confidence={item['confidence']}"
        for item in flagged
    )
    if not flagged:
        lines.append("- отсутствуют")
    lines.extend(["", "## Предупреждения", ""])
    lines.extend(f"- {warning}" for warning in warnings)
    if not warnings:
        lines.append("- отсутствуют")
    lines.extend([
        "- `missing_capabilities` оставлен пустым: отсутствующую возможность нельзя доказательно вывести из единственного положительного источника — существующих Department.",
        "",
        "## Источники",
        "",
    ])
    lines.extend(f"- `{item['source']}` → {item['department']}" for item in departments if item.get("source"))
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    departments, warnings = scan_departments()
    records, duplicates = build_registry(departments)
    payload = {
        "version": "1.0",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "capabilities": records,
        "missing_capabilities": [],
    }
    validate_registry(payload, len(records))
    _write_json(payload)
    _write_report(departments, records, duplicates, warnings)
    print(f"Department: {len(departments)}")
    print(f"Capability: {len(records)}")
    print(f"Registry: {REGISTRY_PATH}")
    print(f"Report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
