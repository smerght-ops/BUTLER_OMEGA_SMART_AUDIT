# -*- coding: utf-8 -*-
"""Permanent FAST/FULL acceptance runner for Butler Omega Smart."""

import argparse
import importlib
import json
import py_compile
import shutil
import struct
import sys
import time
import traceback
import zipfile
import zlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = ROOT / "A_99_TESTS"
CONFIG_PATH = TEST_ROOT / "acceptance_config.json"
REPORTS = TEST_ROOT / "reports"
FIXTURES = TEST_ROOT / "fixtures"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def ensure_fixtures():
    FIXTURES.mkdir(parents=True, exist_ok=True)
    png = FIXTURES / "vision_test_image.png"
    width = height = 64
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            row.extend((220, 40, 40) if (x // 16 + y // 16) % 2 == 0 else (40, 170, 70))
        rows.append(bytes(row))
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff)
    png.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
        + chunk(b"IEND", b"")
    )
    doc = FIXTURES / "document_test.txt"
    if not doc.exists():
        doc.write_text("BUTLER_ACCEPTANCE_DOCUMENT\nSafe project acceptance fixture.\n", encoding="utf-8")
    unsupported = FIXTURES / "unsupported.bin"
    if not unsupported.exists():
        unsupported.write_bytes(b"BUTLER_ACCEPTANCE_UNSUPPORTED")
    archive = FIXTURES / "archive_test.zip"
    if not archive.exists():
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(doc, arcname="document_test.txt")


class StorageGuard:
    def __init__(self, paths, stamp):
        self.paths = [ROOT / p for p in paths]
        self.backup = REPORTS / (".acceptance_backup_" + stamp)
        self.manifest = []
        self.errors = []

    def capture(self):
        self.backup.mkdir(parents=True, exist_ok=False)
        for source in self.paths:
            relative = source.relative_to(ROOT)
            target = self.backup / relative
            existed = source.exists()
            self.manifest.append((source, target, existed, source.is_dir() if existed else False))
            if not existed:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)

    def restore(self):
        for source, target, existed, was_dir in reversed(self.manifest):
            try:
                if source.exists():
                    if source.is_dir():
                        shutil.rmtree(source)
                    else:
                        source.unlink()
                if existed:
                    source.parent.mkdir(parents=True, exist_ok=True)
                    if was_dir:
                        shutil.copytree(target, source)
                    else:
                        shutil.copy2(target, source)
            except Exception as exc:
                self.errors.append(f"{source}: {type(exc).__name__}: {exc}")
        if not self.errors:
            shutil.rmtree(self.backup, ignore_errors=True)
        return not self.errors


def result_contract(result, require_text=True):
    problems = []
    if not isinstance(result, dict):
        return ["result is not a dictionary"]
    for field in ("ok", "department", "text", "error", "metadata"):
        if field not in result:
            problems.append("missing field: " + field)
    if not isinstance(result.get("ok"), bool):
        problems.append("ok is not boolean")
    if not str(result.get("department") or "").strip():
        problems.append("department is empty")
    if not isinstance(result.get("metadata"), dict):
        problems.append("metadata is not a dictionary")
    if result.get("ok") is True and result.get("error") not in (None, ""):
        problems.append("successful result contains error")
    if require_text and not str(result.get("text") or "").strip():
        problems.append("text is empty")
    return problems


def metadata_summary(metadata):
    if not isinstance(metadata, dict):
        return {}
    safe = {}
    allowed = {"path", "filepath", "format", "engine", "result_count", "mode", "action", "prompt_id", "image_path"}
    for key, value in metadata.items():
        if key not in allowed:
            continue
        if isinstance(value, (str, int, float, bool)) or value is None:
            safe[key] = value
    return safe


def _none(value):
    return value if value not in (None, "") else None


def failure_diagnostics(name, expected, result, breakpoint, exception, duration_ms, command):
    metadata = result.get("metadata") if isinstance(result.get("metadata"), dict) else {}
    nested = metadata.get("diagnostics") if isinstance(metadata.get("diagnostics"), dict) else {}
    exception_lines = str(exception or metadata.get("traceback") or nested.get("traceback") or "").strip().splitlines()
    timed_out = "timeout" in str(breakpoint or "").lower()
    actual = result.get("department")
    stage = (nested.get("failure_stage") or metadata.get("last_pipeline_step")
             or metadata.get("last_executed_step") or breakpoint)
    exception_type = nested.get("exception_type") or metadata.get("exception_type")
    exception_message = nested.get("exception_message") or metadata.get("exception_message")
    if timed_out:
        exception_type = exception_type or "TimeoutError"
        exception_message = exception_message or breakpoint
    diagnostics = {
        "failure_source": _none(nested.get("failure_source") or actual or expected),
        "failure_stage": _none(stage),
        "exception_type": _none(exception_type),
        "exception_message": _none(exception_message or result.get("error") or breakpoint),
        "elapsed_time_ms": duration_ms,
        "traceback": _none("\n".join(exception_lines[-10:])),
    }
    if str(expected or "").upper() == "IMAGE" or name.startswith("IMAGE_"):
        diagnostics.update({
            "prompt": _none(metadata.get("prompt") or command),
            "workflow": _none(metadata.get("workflow")),
            "checkpoint": _none(metadata.get("checkpoint")),
            "output_directory": _none(metadata.get("output_directory")),
            "http_status": _none(metadata.get("http_status") or metadata.get("status_code")),
            "http_response": _none(metadata.get("http_response")),
            "last_pipeline_step": _none(metadata.get("last_pipeline_step") or stage),
        })
    if str(expected or "").upper() == "OPEN_DOCUMENT" or name.startswith("OPEN_"):
        diagnostics.update({
            "file_path": _none(metadata.get("filepath") or metadata.get("path")),
            "last_executed_step": _none(metadata.get("last_executed_step") or "official dispatch returned"),
            "timeout_location": _none(metadata.get("timeout_location") or ("WindowsShell.os.startfile / dispatch" if timed_out else None)),
            "current_state": _none(metadata.get("current_state") or ("returned after timeout threshold" if timed_out else None)),
        })
    return diagnostics


def route_only(dispatcher, query):
    from A_03_ORCHESTRATION.ConversationContext.context_engine import ConversationContextEngine
    resolved = ConversationContextEngine.resolve(query)
    context = {"image_followup": ConversationContextEngine.last_was_image_followup}
    for department in dispatcher.departments:
        try:
            handled = department.can_handle(resolved, context=context)
        except TypeError:
            handled = department.can_handle(resolved)
        if handled:
            actual = dispatcher._dept_name(department)
            ConversationContextEngine.update(query, {"department": actual})
            return actual, resolved
    return None, resolved


def record(name, mode, command, expected, status, started, result=None, breakpoint=None,
           exception=None, artifacts=None, cleanup="pending"):
    result = result if isinstance(result, dict) else {}
    preview = str(result.get("text") or "")[:300]
    if str(result.get("department") or "").upper() == "MEMORY":
        preview = "[memory response redacted; non-empty=%s]" % bool(str(result.get("text") or "").strip())
    duration_ms = int((time.perf_counter() - started) * 1000)
    item = {
        "name": name, "mode": mode, "command": command,
        "expected_department": expected,
        "actual_department": result.get("department"),
        "status": status,
        "duration_ms": duration_ms,
        "ok": result.get("ok"),
        "text_preview": preview,
        "error": result.get("error"),
        "metadata_summary": metadata_summary(result.get("metadata")),
        "artifact_paths": list(artifacts or []),
        "cleanup_result": cleanup,
        "breakpoint": breakpoint,
        "exception": exception,
    }
    if status == "FAIL":
        item["diagnostics"] = failure_diagnostics(
            name, expected, result, breakpoint, exception, duration_ms, command
        )
    return item


def execute_case(dispatch, case, mode, context=None):
    started = time.perf_counter()
    command = case["command"]
    expected = case["expected_department"]
    try:
        result = dispatch(command, dict(context or {}))
        problems = result_contract(result, require_text=True)
        controlled_error = result.get("error") in case.get("allowed_errors", []) and result.get("ok") is False
        if str(result.get("department") or "").upper() != expected.upper():
            problems.append(f"department expected {expected}, got {result.get('department')}")
        if not result.get("ok") and not controlled_error:
            problems.append("ok is not true")
        lowered = str(result.get("text") or "").lower()
        for required in case.get("contains", []):
            if required.lower() not in lowered:
                problems.append("missing text: " + required)
        if lowered.strip() == "использовать qwen35-ru" or "использовать qwen35-ru" == lowered.strip(" ."):
            problems.append("model result not executed")
        if (time.perf_counter() - started) > case.get("timeout", 30):
            problems.append("scenario timeout exceeded")
        status = "PASS" if not problems else "FAIL"
        if controlled_error and not problems:
            status = "CONTROLLED_ERROR"
        return record(case["name"], mode, command, expected, status, started, result,
                      "; ".join(problems) or None)
    except Exception as exc:
        return record(case["name"], mode, command, expected, "FAIL", started,
                      breakpoint="UNHANDLED_EXCEPTION", exception=traceback.format_exc())


def negative_case(dispatch, name, command, expected, context):
    started = time.perf_counter()
    try:
        result = dispatch(command, context)
        problems = result_contract(result, require_text=True)
        if str(result.get("department") or "").upper() != expected:
            problems.append("wrong department")
        if result.get("ok") is not False or not result.get("error"):
            problems.append("controlled failure not returned")
        return record(name, "full", command, expected, "PASS" if not problems else "FAIL",
                      started, result, "; ".join(problems) or None)
    except Exception:
        return record(name, "full", command, expected, "FAIL", started,
                      breakpoint="UNHANDLED_EXCEPTION", exception=traceback.format_exc())


def run_fast(config):
    results = []
    started = time.perf_counter()
    key_files = [
        ROOT / "BUTLER_OS.py", ROOT / "A_03_ORCHESTRATION/dispatcher_bridge_v2.py",
        ROOT / "A_02_MANAGERS/smart_dispatcher_v2.py", ROOT / "A_03_ORCHESTRATION/butler_harness.py",
        ROOT / "A_04_AGENTS/MemoryDepartment/runner.py", Path(__file__),
    ]
    errors = []
    for path in key_files:
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            errors.append(f"{path}: {exc}")
    results.append(record("PY_COMPILE", "fast", "py_compile key components", "INFRASTRUCTURE",
                          "PASS" if not errors else "FAIL", started,
                          {"ok": not errors, "department": "INFRASTRUCTURE", "text": "compiled", "error": errors or None, "metadata": {}},
                          "; ".join(errors) or None))
    started = time.perf_counter()
    try:
        importlib.import_module("BUTLER_OS")
        bridge = importlib.import_module("A_03_ORCHESTRATION.dispatcher_bridge_v2")
        dispatcher = bridge._dispatcher
        names = [dispatcher._dept_name(d) for d in dispatcher.departments]
        expected = {"MEMORY","SEARCH","OPEN_DOCUMENT","DOCUMENTS","VISION","IMAGE","TEXT","CODING","HOME","ARCHIVE","AUDIO","VIDEO"}
        missing = sorted(expected - set(names))
        results.append(record("RUNTIME_IMPORT_AND_REGISTRATION", "fast", "import official runtime", "INFRASTRUCTURE",
                              "PASS" if not missing else "FAIL", started,
                              {"ok": not missing, "department": "INFRASTRUCTURE", "text": ",".join(names), "error": missing or None, "metadata": {"departments": names}},
                              ("missing: " + ",".join(missing)) if missing else None))
    except Exception:
        results.append(record("RUNTIME_IMPORT_AND_REGISTRATION", "fast", "import official runtime", "INFRASTRUCTURE", "FAIL", started,
                              breakpoint="RUNTIME_INITIALIZATION", exception=traceback.format_exc()))
        return results, 2
    for case in config["scenarios"]:
        if case.get("enabled") and "fast" in case.get("modes", []):
            results.append(execute_case(bridge.dispatch, case, "fast"))
    routing = [
        ("ROUTE_IMAGE", "Нарисуй дракона", "IMAGE"), ("ROUTE_TEXT", "Напиши стихотворение", "TEXT"),
        ("ROUTE_CODING", "Напиши функцию Python", "CODING"), ("ROUTE_SEARCH", "Найди договор", "SEARCH"),
    ]
    for name, query, expected in routing:
        started = time.perf_counter(); actual, resolved = route_only(dispatcher, query)
        fake = {"ok": actual == expected, "department": actual or "NONE", "text": resolved, "error": None if actual == expected else "ROUTE_MISMATCH", "metadata": {"resolved": resolved}}
        results.append(record(name, "fast", query, expected, "PASS" if actual == expected else "FAIL", started, fake,
                              None if actual == expected else "ROUTING_MISMATCH"))
    return results, None


def run_full(config):
    bridge = importlib.import_module("A_03_ORCHESTRATION.dispatcher_bridge_v2")
    dispatch = bridge.dispatch
    results = []
    by_name = {c["name"]: c for c in config["scenarios"] if c.get("enabled") and "full" in c.get("modes", [])}
    for name in (
        "GOAL_CREATE", "GOAL_GET", "GOAL_LIST", "GOAL_UPDATE",
        "GOAL_ADD_TASK", "PRIORITY_CALCULATE", "PRIORITY_LIST", "PRIORITY_NEXT",
        "REMINDER_SET", "REMINDER_LIST", "REMINDER_CHECK", "REMINDER_ACKNOWLEDGE",
        "PROGRESS_UPDATE", "PROGRESS_GET",
        "PROGRESS_TIMELINE", "GOAL_PROGRESS", "PLANNER_GENERATE",
        "PLANNER_GET", "PLANNER_OPTIMIZE", "GOAL_DELETE",
    ):
        results.append(execute_case(dispatch, by_name[name], "full"))
    for name in ("MEMORY_PROFILE", "MEMORY_COLOR", "MEMORY_GENERAL"):
        results.append(execute_case(dispatch, by_name[name], "full"))
    for name in (
        "SELF_KNOWLEDGE_CAPABILITIES", "SELF_KNOWLEDGE_DEPARTMENTS",
        "SELF_KNOWLEDGE_DONE", "SELF_KNOWLEDGE_PENDING",
        "SELF_MEMORY_ARCHITECTURE", "SELF_DEPARTMENT_CONTENTS", "SELF_PROJECT",
    ):
        results.append(execute_case(dispatch, by_name[name], "full"))
    marker = "ACCEPTANCE_MEMORY_" + datetime.now().strftime("%Y%m%d%H%M%S")
    write = dict(by_name["MEMORY_PROFILE"], name="MEMORY_WRITE", command=f"Запомни: acceptance_marker = {marker}", contains=[marker])
    read = dict(by_name["MEMORY_PROFILE"], name="MEMORY_PERSISTENCE", command="какой мой acceptance_marker", contains=[marker])
    results.append(execute_case(dispatch, write, "full")); results.append(execute_case(dispatch, read, "full"))
    for name in ("CHAT_POEM", "CHAT_SELF_INFO", "CODING_HELLO_WORLD", "SEARCH_PASSPORT", "OPEN_FIRST"):
        results.append(execute_case(dispatch, by_name[name], "full"))
    vision = by_name["VISION_EXISTING"]
    results.append(execute_case(dispatch, vision, "full", {"attachments": [str(ROOT / vision["fixture"])]}))
    results.append(negative_case(dispatch, "VISION_MISSING", "что на фото", "VISION", {"attachments": [str(FIXTURES / "missing.png")]}))
    results.append(negative_case(dispatch, "VISION_UNSUPPORTED", "что на фото", "VISION", {"attachments": [str(FIXTURES / "unsupported.bin")]}))
    documents = by_name["DOCUMENTS_EXISTING"]
    results.append(execute_case(dispatch, documents, "full", {"attachments": [str(ROOT / documents["fixture"])]}))
    results.append(negative_case(dispatch, "DOCUMENTS_MISSING", "прочитай документ", "DOCUMENTS", {"attachments": [str(FIXTURES / "missing.txt")]}))
    archive = by_name["ARCHIVE_EXISTING"]
    results.append(execute_case(dispatch, archive, "full", {"attachments": [str(ROOT / archive["fixture"])]}))
    for name in ("AUDIO", "VIDEO"):
        case = by_name[name]
        started = time.perf_counter()
        results.append(record(name, "full", case["command"], case["expected_department"], "SKIP", started,
                              breakpoint="NO_REAL_PROVIDER: registered minimal acknowledgement only"))
    from A_03_ORCHESTRATION.ConversationContext.context_engine import ConversationContextEngine
    from A_03_ORCHESTRATION.ConversationContext.ImageSession.image_session import ImageSession
    ConversationContextEngine.last_department = None; ConversationContextEngine.last_user_query = ""; ImageSession.clear()
    image_steps = [("IMAGE_INITIAL", "нарисуй девушку"), ("IMAGE_CONTINUATION_1", "не лицо"),
                   ("IMAGE_CONTINUATION_2", "в полный рост"), ("IMAGE_WATERFALL", "под водопадом")]
    for name, command in image_steps:
        case = {"name":name,"command":command,"expected_department":"IMAGE","contains":[],"timeout":300}
        item = execute_case(dispatch, case, "full")
        if name == "IMAGE_WATERFALL" and item["actual_department"] == "HOME":
            item["breakpoint"] = 'IMAGE_CONTEXT_LOST; Expected IMAGE; Actual HOME; Input: "под водопадом"'
        results.append(item)
    return results, None


def write_reports(mode, stamp, results, cleanup_ok, cleanup_errors, initial_code=None):
    REPORTS.mkdir(parents=True, exist_ok=True)
    counts = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS","FAIL","CONTROLLED_ERROR","SKIP")}
    mandatory_fail = any(r["status"] == "FAIL" for r in results)
    exit_code = 3 if not cleanup_ok else (initial_code if initial_code is not None else (1 if mandatory_fail else 0))
    payload = {"timestamp": stamp, "mode": mode, "official_entry": "A_03_ORCHESTRATION.dispatcher_bridge_v2.dispatch",
               "results": results, "counts": counts, "cleanup_ok": cleanup_ok, "cleanup_errors": cleanup_errors,
               "all_scenarios_passed": not mandatory_fail, "exit_code": exit_code}
    json_path = REPORTS / f"acceptance_report_{stamp}.json"; md_path = REPORTS / f"acceptance_report_{stamp}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# Butler Omega Smart — {mode.upper()} Acceptance", "", f"Timestamp: {stamp}", "",
             "| Scenario | Status | Expected | Actual | Duration ms |", "|---|---:|---|---|---:|"]
    for r in results:
        lines.append(f"| {r['name']} | {r['status']} | {r.get('expected_department') or ''} | {r.get('actual_department') or ''} | {r['duration_ms']} |")
    lines += ["", f"PASS: {counts['PASS']}", f"FAIL: {counts['FAIL']}", f"SKIP: {counts['SKIP']}",
              f"CONTROLLED_ERROR: {counts['CONTROLLED_ERROR']}",
              f"Cleanup: {'PASS' if cleanup_ok else 'FAIL'}", f"Exit code: {exit_code}", "", "## Failures", ""]
    for r in results:
        if r["status"] == "FAIL":
            diagnostics = r.get("diagnostics") or failure_diagnostics(
                r["name"], r.get("expected_department"), {}, r.get("breakpoint"),
                r.get("exception"), r["duration_ms"], r.get("command")
            )
            lines += [f"### {r['name']}", "", f"- Input: `{r['command']}`", f"- Expected: `{r['expected_department']}`",
                      f"- Actual: `{r.get('actual_department')}`", f"- Error: `{r.get('error')}`",
                      f"- Breakpoint: {r.get('breakpoint') or 'None'}"]
            labels = {
                "failure_source": "Failure Source", "failure_stage": "Failure Stage",
                "exception_type": "Exception Type", "exception_message": "Exception Message",
                "elapsed_time_ms": "Elapsed Time", "traceback": "Traceback",
                "prompt": "Prompt", "workflow": "Workflow", "checkpoint": "Checkpoint",
                "output_directory": "Output Directory", "http_status": "HTTP Status",
                "http_response": "HTTP Response", "last_pipeline_step": "Last Pipeline Step",
                "file_path": "File Path", "last_executed_step": "Last Executed Step",
                "timeout_location": "Timeout Location", "current_state": "Current State",
            }
            for key, label in labels.items():
                if key in diagnostics:
                    value = diagnostics.get(key)
                    lines.append(f"- {label}: `{value if value not in (None, '') else 'None'}`")
            lines.append("")
    if cleanup_errors: lines += ["## Cleanup errors", ""] + [f"- {e}" for e in cleanup_errors]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(json_path, REPORTS / "latest_acceptance_report.json"); shutil.copy2(md_path, REPORTS / "latest_acceptance_report.md")
    return payload, json_path, md_path


def print_console(mode, payload):
    print("=" * 70); print(f" BUTLER OMEGA SMART — {mode.upper()} ACCEPTANCE"); print("=" * 70)
    for r in payload["results"]: print(f"[ {r['name']:<28} ] {r['status']}")
    print("-" * 70)
    for key in ("PASS","FAIL","CONTROLLED_ERROR","SKIP"): print(f"{key}: {payload['counts'][key]}")
    print(f"TOTAL: {len(payload['results'])}"); print("-" * 70)
    print("ALL SCENARIOS PASSED:", "YES" if payload["all_scenarios_passed"] else "NO")
    print("EXIT CODE:", payload["exit_code"]); print("=" * 70)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--mode", choices=("fast","full"), required=True); args = parser.parse_args()
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8")); ensure_fixtures(); REPORTS.mkdir(parents=True, exist_ok=True)
    except Exception:
        traceback.print_exc(); return 2
    guard = StorageGuard(config.get("storage", []), stamp); results = []; initial_code = None
    try:
        guard.capture()
        results, initial_code = run_fast(config) if args.mode == "fast" else run_full(config)
    except Exception:
        results.append(record("RUNNER_INTERNAL", args.mode, "runner", "INFRASTRUCTURE", "FAIL", time.perf_counter(), breakpoint="RUNNER_INTERNAL", exception=traceback.format_exc()))
        initial_code = 2
    finally:
        cleanup_ok = guard.restore()
    for item in results: item["cleanup_result"] = "PASS" if cleanup_ok else "FAIL"
    payload, _, _ = write_reports(args.mode, stamp, results, cleanup_ok, guard.errors, initial_code)
    print_console(args.mode, payload)
    return payload["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
