# -*- coding: utf-8 -*-
import os
import re
import sys
import uuid
from A_03_ORCHESTRATION.dispatcher_bridge_v2 import dispatch
from A_03_ORCHESTRATION.agent_core_coordinator import (
    AgentCoreCoordinator,
    AgentCoreUnavailable,
)
from A_03_ORCHESTRATION.ConversationContext.context_engine import (
    ConversationContextEngine,
)
from A_01_CORE.TaskExecutor import CapabilityExecutor, TaskExecutor
from A_04_AGENTS.DocumentsDepartment.runner import DocumentsDepartment
from A_07_MEMORY.memory_orchestrator_v2 import MemoryOrchestratorV2

EXIT_WORDS = {"выход", "exit", "quit", "q"}
VOICE_COMMAND = {"voice", "mic", "голос"}
_task_planner = TaskExecutor()
_capability_executor = CapabilityExecutor()
_documents_capability = DocumentsDepartment()
_memory_orchestrator = MemoryOrchestratorV2(token_budget=1200)
def _start_secretary_session():
    from A_09_INTERFACE.voice_input import ramble_session
    return ramble_session()


_agent_core = AgentCoreCoordinator(
    dispatch,
    secretary_session=_start_secretary_session,
    memory_orchestrator=_memory_orchestrator,
)

_SYSTEM_ECHO_EXACT = {
    "=" * 70,
    "[OK] Ядро загружено.",
    "[OK] SmartDispatcherV2 подключен.",
    "[OK] Департаменты доступны.",
    "Введите exit / q / выход для завершения.",
    "Изображение готово.",
}
_SYSTEM_ECHO_PREFIXES = ("[BUTLER |", "Файл:", "[KOS] >")


def _is_system_echo(query):
    """Reject exact Butler console output before it reaches any planner/router."""
    value = (query or "").strip()
    return value in _SYSTEM_ECHO_EXACT or any(
        value.startswith(prefix) for prefix in _SYSTEM_ECHO_PREFIXES
    )


def _is_active_document_command(query, context):
    """Recognize document-state commands before generic filesystem planning."""
    q = (query or "").casefold()
    document_save = (
        re.search(r"\bсохрани(?:ть)?\b", q) is not None
        and re.search(r"\b(?:word[-\s]?)?документ\b", q) is not None
    )
    return document_save and _documents_capability.can_handle(query, context=context)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def _create_request_envelope(text="", input_method="keyboard", context=None):
    """Create the common request contract at the user-input boundary."""
    return {
        "correlation_id": str(uuid.uuid4()),
        "input_method": input_method,
        "original_text": text,
        "context": dict(context or {}),
    }


def _execute_query(request):
    envelope = (
        request if isinstance(request, dict)
        else _create_request_envelope(request, input_method="keyboard")
    )
    query = str(envelope.get("original_text") or "")
    context = dict(envelope.get("context") or {})
    context.setdefault("attachments", [])
    context["request_envelope"] = {
        "correlation_id": envelope["correlation_id"],
        "input_method": envelope["input_method"],
        "original_text": query,
    }
    context = ConversationContextEngine.enrich_context(query, context)
    for quote in ('"', "'"):
        for part in query.split(quote):
            candidate = part.strip()
            if candidate and os.name == "nt" and os.path.exists(candidate):
                if candidate not in context["attachments"]:
                    context["attachments"].append(candidate)

    try:
        result = _agent_core.execute(query, context)
    except AgentCoreUnavailable as exc:
        # Compatibility path: the official Butler remains usable when the local
        # Agent Core server/model is unavailable or cannot complete the turn.
        result = dispatch(query, context)
        result.setdefault("metadata", {}).update({
            "agent_core_fallback": True,
            "agent_core_error": str(exc),
        })
    result.setdefault("metadata", {}).update({
        "correlation_id": envelope["correlation_id"],
        "input_method": envelope["input_method"],
    })
    ConversationContextEngine.update(query, result)
    return result


def _print_result(result):
    dept = result.get("department", "UNKNOWN")
    model = result.get("model", "-")
    latency = result.get("latency_ms", 0)
    err = result.get("error")
    text = (
        result.get("text")
        or result.get("message")
        or result.get("permanent")
        or result.get("project")
        or result.get("session")
        or ""
    )
    print(f"\n[BUTLER | {dept} | model={model} | {latency}ms]")
    if err:
        print(f"\n[ERROR] {err}")
    metadata = result.get("metadata") or {}
    if metadata.get("agent_core_fallback"):
        print(
            "\n[DIAGNOSTIC] Agent Core fallback: "
            f"{metadata.get('agent_core_error') or 'UNKNOWN'}"
        )
    if text:
        print(f"\n{text}")
    else:
        print("\n[INFO] Отдел ответил без текстового вывода.")


def main(once_query=None):
    clear_screen()
    print("=" * 70)
    print(" BUTLER OMEGA OS v1.1 — WORK TERMINAL")
    print("=" * 70)
    print("[OK] Ядро загружено.")
    print("[OK] SmartDispatcherV2 подключен.")
    print("[OK] Департаменты доступны.")
    print(f"[PID] Butler OS: {os.getpid()} / parent: {os.getppid()}")
    print("Нажмите Enter, чтобы говорить, или просто введите задачу.")
    print("Введите exit / q / выход для завершения.")
    print("=" * 70)

    if once_query is not None:
        query = once_query.strip()
        if not query or _is_system_echo(query):
            print("\n[INFO] Служебный вывод отклонён; задача не создана.")
            return
        try:
            _print_result(_execute_query(query))
        except Exception as ex:
            _print_result({"ok": False, "department": "SYSTEM", "model": "-", "error": str(ex), "latency_ms": 0})
        return

    while True:
        try:
            query = input("\n[KOS] > ").strip()

            if not query:
                try:
                    from A_09_INTERFACE.voice_input import voice_command
                    result = voice_command(
                        agent_execute=_execute_query,
                        request_envelope_factory=_create_request_envelope,
                    )
                    if isinstance(result, dict):
                        _print_result(result)
                except Exception as ex:
                    print(f"\n[VOICE ERROR] {ex}")
                continue

            if _is_system_echo(query):
                print("\n[INFO] Служебный вывод отклонён; задача не создана.")
                continue

            if query.lower() in VOICE_COMMAND:
                try:
                    from A_09_INTERFACE.voice_input import voice_command
                    result = voice_command(
                        agent_execute=_execute_query,
                        request_envelope_factory=_create_request_envelope,
                    )
                    if isinstance(result, dict):
                        _print_result(result)
                except Exception as ex:
                    print(f"\n[VOICE ERROR] {ex}")
                continue

            if query.lower() in EXIT_WORDS:
                print("\n[OK] Butler OS остановлен.")
                break

            try:
                result = _execute_query(query)
            except Exception as ex:
                result = {
                    "ok": False,
                    "department": "SYSTEM",
                    "model": "-",
                    "text": "",
                    "message": "",
                    "error": str(ex),
                    "latency_ms": 0
                }

            _print_result(result)

        except KeyboardInterrupt:
            print("\n\n[OK] Butler OS остановлен.")
            break

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == "--once":
        if len(sys.argv) < 3:
            raise SystemExit("Usage: START_BUTLER_OS.bat --once \"command\"")
        main(" ".join(sys.argv[2:]))
    else:
        main()
