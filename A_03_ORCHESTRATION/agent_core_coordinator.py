# -*- coding: utf-8 -*-
"""Minimal production boundary between Butler Agent Core and Departments."""

from __future__ import annotations

import json
import os
import re
import subprocess
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from CapabilityRegistry import CapabilityRegistry


class AgentCoreUnavailable(RuntimeError):
    """The local Agent Core cannot serve this turn; the caller should fall back."""


# ---------------------------------------------------------------------------
# Evidence tracking — generic, format-agnostic completion gate
# ---------------------------------------------------------------------------

class EvidenceTracker:
    """Tracks observation types during a reasoning loop.

    Classifies each tool observation into one of two categories:
      - STRUCTURE : directory listings, file metadata, capability catalogues
      - CONTENT   : actual file content reads (text, documents, images, etc.)

    The tracker is query-aware: it records what the user asked for and
    whether the collected evidence satisfies that request.
    """

    # Keywords that indicate a query requires reading actual file contents
    _CONTENT_INDICATORS = re.compile(
        r"""
        (?:
            # Russian content-analysis verbs
            проанализируй|прочитай|содержимое|что\s+внутри|открой|
            содержимое\s+файл|текст\s+файла|прочитать\s+файл|
            покажи\s+содержимое|найди\s+в\s+файле|извлеки|расшифруй|
            переведи\s+содержимое|оцени\s+содержимое|проверь\s+содержимое|
            что\s+написано|какой\s+текст|прочитать\s+внутреннее|
            # English content-analysis verbs (fallback)
            analyze.*content|read.*file|what.*inside|open.*file|
            read.*the.*contents|extract.*text|transcribe|translate.*content|
            evaluate.*content|check.*content|written|text\s+of\s+file|
            # Generic "content" mentions in investigative context
            содержимое.*файл|анализ.*содержимого|чтение.*файла|
            file.*contents|read.*content|analyze.*file|inspect.*content
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # Keywords that indicate a query only needs directory structure
    _STRUCTURE_INDICATORS = re.compile(
        r"""
        (?:
            перечисл|список\s+файлов|структур|каталог\s+(?:без\s+)?анализа?|
            покажи\s+список|перечисли\s+содержимое\s+папки|
            what.*files?\s*(?:in|at)\s|list\s+directory|show\s+structure|
            directory\s+listing|file\s+names?\s*only|только\s+названия|
            без\s+чтения|без\s+анализа|структурный\s+обзор
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def __init__(self) -> None:
        self._structure_count: int = 0
        self._content_count: int = 0
        self._query_type: str = "unknown"   # structure | content | mixed | unknown
        self._observation_history: list[dict] = []

    # Patterns that indicate a directory listing / metadata output rather
    # than actual file content.  If the text matches these patterns it is
    # classified as STRUCTURE even when it has a long "text" field.
    _DIRECTORY_LISTING_PATTERNS = re.compile(
        r"""
        (?:
            directory\s+contents|directory\s+listing|folder\s+contents|
            files?\s*:\s*$|entries?\s*:|file\s+list|contents\s+of|
            ^-\s+[a-z0-9._-]+\b|^\*\s+[a-z0-9._-]+\b  # bullet-style file lists
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def record_observation(self, observation: dict) -> None:
        """Classify and record a tool observation.

        Classification rules (generic, no special-case paths):
          1. If the text matches directory-listing patterns → STRUCTURE
          2. If the observation has an error / is empty → STRUCTURE
          3. Otherwise, if it has a meaningful "text" field → CONTENT
          4. Default → STRUCTURE (conservative)
        """
        obs_text = json.dumps(observation, ensure_ascii=False, default=str).lower()
        raw_text = str(observation.get("text", "") or "")

        # Rule 1: directory listing patterns → STRUCTURE
        if self._DIRECTORY_LISTING_PATTERNS.search(raw_text):
            self._structure_count += 1
            self._observation_history.append({
                "type": "structure",
                "ok": observation.get("ok"),
            })
            return

        # Rule 2: error or empty → STRUCTURE (no useful content gathered)
        if not observation.get("ok") or len(raw_text) <= 10:
            self._structure_count += 1
            self._observation_history.append({
                "type": "structure",
                "ok": observation.get("ok"),
            })
            return

        # Rule 3: meaningful text field → CONTENT
        if any(k in observation for k in ("text", "content", "extracted_text", "body")):
            self._content_count += 1
            self._observation_history.append({
                "type": "content",
                "ok": observation.get("ok"),
            })
            return

        # Rule 4: default → STRUCTURE (conservative)
        self._structure_count += 1
        self._observation_history.append({
            "type": "structure",
            "ok": observation.get("ok"),
        })

    def classify_query(self, query: str) -> None:
        """Determine what type of investigation the user requested."""
        q_lower = query.lower()
        has_content = bool(self._CONTENT_INDICATORS.search(q_lower))
        has_structure = bool(self._STRUCTURE_INDICATORS.search(q_lower))

        if has_content and not has_structure:
            self._query_type = "content"
        elif has_structure and not has_content:
            self._query_type = "structure"
        elif has_content and has_structure:
            # If content analysis is mentioned, treat as requiring content
            self._query_type = "content"
        else:
            # Default heuristic: directory-related queries need structure at minimum
            if any(kw in q_lower for kw in ("каталог", "папка", "directory", "folder", "list")):
                self._query_type = "structure"
            elif any(kw in q_lower for kw in ("файл", "file", "content", "содержимое")):
                self._query_type = "content"
            else:
                self._query_type = "unknown"

    @property
    def requires_content(self) -> bool:
        return self._query_type == "content"

    @property
    def has_structure_evidence(self) -> bool:
        return self._structure_count > 0

    @property
    def has_content_evidence(self) -> bool:
        return self._content_count > 0

    def evidence_sufficient(self) -> bool:
        """Return True if collected evidence meets the query requirements.

        Rules (generic, no special cases):
          - If query requires content analysis and no content evidence exists → False
          - If query only needs structure and we have at least one observation → True
          - If query type is unknown but we have observations → True (permissive)
          - If no observations yet → False (nothing to base answer on)
        """
        if not self.has_structure_evidence:
            return False

        if self._query_type == "unknown":
            # Unknown intent — any observation is acceptable
            return True

        if self._query_type == "structure":
            return True

        # Content-required query: need at least one content observation
        return self.has_content_evidence


# ---------------------------------------------------------------------------
# Agent Core Coordinator
# ---------------------------------------------------------------------------

class AgentCoreCoordinator:
    HEAVY_DEPARTMENTS = {"AUDIO", "IMAGE", "VIDEO", "VISION"}
    LM_STUDIO_MARKERS = (".lmstudio", "lm studio", "lm-studio", "lmstudio")
    TOOL_NAME = "execute_butler_capability"
    VOICE_TOOL_NAME = "start_secretary_session"

    def __init__(self, department_dispatch: Callable[[str, dict], dict],
                 secretary_session: Callable[[], dict] | None = None,
                 memory_orchestrator=None):
        self.department_dispatch = department_dispatch
        self.secretary_session = secretary_session
        self.memory_orchestrator = memory_orchestrator
        self.api_url = os.getenv(
            "BUTLER_AGENT_CORE_URL",
            "http://127.0.0.1:11434/api/chat",
        )
        self.model = os.getenv("BUTLER_AGENT_CORE_MODEL", "qwen36-butler:latest")
        self.keep_alive = os.getenv("BUTLER_AGENT_CORE_KEEP_ALIVE", "5m")
        self.timeout = float(os.getenv("BUTLER_AGENT_CORE_TIMEOUT", "300"))
        self._capabilities = {
            item["id"]: item for item in CapabilityRegistry().all()
            if item.get("confidence") == "confirmed"
        }

    def _post(self, url: str, payload: dict) -> dict:
        try:
            request = Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, OSError, ValueError) as exc:
            raise AgentCoreUnavailable(f"AGENT_CORE_HTTP_FAILED: {exc}") from exc

    def _llama_server_processes(self) -> list[dict]:
        if os.name != "nt":
            return []
        scripts = (
            (
                "Get-CimInstance Win32_Process -Filter \"Name='llama-server.exe'\" "
                "| Select-Object ExecutablePath,CommandLine | ConvertTo-Json "
                "-Compress -Depth 3"
            ),
            (
                "Get-Process -Name 'llama-server' -ErrorAction SilentlyContinue "
                "| Select-Object @{Name='ExecutablePath';Expression={$_.Path}},"
                "@{Name='CommandLine';Expression={$null}} "
                "| ConvertTo-Json -Compress -Depth 3"
            ),
        )
        for script in scripts:
            completed = subprocess.run(
                ["powershell", "-NoProfile", "-Command", script],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
                check=False,
            )
            if completed.returncode != 0:
                continue
            output = completed.stdout.strip()
            if not output:
                return []
            try:
                payload = json.loads(output)
            except ValueError:
                continue
            return payload if isinstance(payload, list) else [payload]
        return []

    @classmethod
    def _is_lm_studio_process(cls, process: dict) -> bool:
        metadata = " ".join(
            str(process.get(key) or "")
            for key in ("ExecutablePath", "CommandLine")
        ).casefold()
        return any(marker in metadata for marker in cls.LM_STUDIO_MARKERS)

    def _external_lmstudio_active(self) -> bool:
        return any(
            self._is_lm_studio_process(process)
            for process in self._llama_server_processes()
        )

    def _chat(self, messages: list[dict], tools=None) -> dict:
        # This is the boundary that can load the heavy Ollama Agent Core model.
        if self._external_lmstudio_active():
            raise AgentCoreUnavailable("EXTERNAL_LM_STUDIO_RUNTIME_ACTIVE")
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "keep_alive": self.keep_alive,
            "options": {"temperature": 0.1},
        }
        if tools:
            payload["tools"] = tools
        try:
            message = self._post(self.api_url, payload)["message"]
            # Ollama may return internal thinking separately. It is neither
            # exposed to the user nor carried as a visible conversation field.
            return {
                key: message[key]
                for key in ("role", "content", "tool_calls")
                if key in message
            }
        except KeyError as exc:
            raise AgentCoreUnavailable(f"AGENT_CORE_RESPONSE_INVALID: {exc}") from exc

    def _tool_definitions(self) -> list[dict]:
        catalog = [
            {
                "id": item["id"],
                "department": item["department"],
                "action": item["action"],
                "object": item["object"],
                "input": item["input"],
                "output": item["output"],
                "aliases": item["aliases"],
            }
            for item in self._capabilities.values()
        ]
        tools = [{
            "type": "function",
            "function": {
                "name": self.TOOL_NAME,
                "description": (
                    "Execute one existing Butler capability. Choose capability_id "
                    "only from this registry: "
                    + json.dumps(catalog, ensure_ascii=False, separators=(",", ":"))
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "capability_id": {"type": "string"},
                        "query": {
                            "type": "string",
                            "description": "Complete natural-language task for the Department.",
                        },
                        "context": {
                            "type": "object",
                            "description": "Optional structured arguments such as paths.",
                        },
                    },
                    "required": ["capability_id", "query"],
                },
            },
        }]
        if self.secretary_session is not None:
            tools.append({
                "type": "function",
                "function": {
                    "name": self.VOICE_TOOL_NAME,
                    "description": (
                        "Start a long user-controlled secretary/ramble recording. "
                        "Use ONLY when the current user message explicitly requests a "
                        "long or continuing capture session. Never infer this from a "
                        "normal voice question or from the input method. Supply an exact "
                        "quote from the current user message as evidence. Captured speech "
                        "is knowledge, not commands."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "explicit_user_request": {"type": "boolean"},
                            "request_quote": {
                                "type": "string",
                                "description": "Exact supporting quote from the current user message.",
                            },
                        },
                        "required": ["explicit_user_request", "request_quote"],
                    },
                },
            })
        return tools

    @staticmethod
    def _normalized_evidence(value: str) -> str:
        return " ".join(str(value or "").casefold().split())

    def _execute_secretary_tool(self, arguments: dict, user_query: str) -> dict:
        arguments = dict(arguments or {})
        quote = self._normalized_evidence(arguments.get("request_quote"))
        query = self._normalized_evidence(user_query)
        if (arguments.get("explicit_user_request") is not True
                or not quote or len(quote) < 8 or quote not in query):
            return {
                "ok": False,
                "error": "SECRETARY_EXPLICIT_REQUEST_REQUIRED",
                "text": "Режим секретаря не запущен: нет явного запроса пользователя.",
            }
        return self.secretary_session()

    def _unload_agent(self) -> None:
        base_url = self.api_url.split("/api/", 1)[0]
        self._post(
            f"{base_url}/api/generate",
            {"model": self.model, "keep_alive": 0, "stream": False},
        )

    def _execute_tool(self, arguments: dict, trusted_context: dict | None = None) -> dict:
        capability_id = arguments.get("capability_id")
        capability = self._capabilities.get(capability_id)
        if not capability:
            return {"ok": False, "error": "UNKNOWN_CAPABILITY_ID"}
        context = dict(arguments.get("context") or {})
        trusted_context = dict(trusted_context or {})
        if trusted_context.get("attachments"):
            context["attachments"] = list(trusted_context["attachments"])
        if trusted_context.get("request_envelope"):
            context["request_envelope"] = dict(
                trusted_context["request_envelope"]
            )
        if trusted_context.get("memory_packet"):
            context["memory_packet"] = dict(trusted_context["memory_packet"])
        for key in ("conversation_context", "resolved_referent", "path"):
            if trusted_context.get(key) is not None:
                value = trusted_context[key]
                context[key] = dict(value) if isinstance(value, dict) else value
        context.update({
            "capability_id": capability_id,
            "capability_action": capability["action"],
            "capability_object": capability["object"],
            "agent_core": True,
        })
        heavy = capability["department"].upper() in self.HEAVY_DEPARTMENTS
        if heavy:
            # The next /api/chat round reloads the same Agent Core model while
            # Python-owned messages preserve the logical conversation.
            self._unload_agent()
        return self.department_dispatch(arguments.get("query") or "", context)

    def _enrich_memory(self, query: str, context: dict | None) -> dict:
        context = dict(context or {})
        if self.memory_orchestrator is None or "memory_packet" in context:
            return context
        try:
            context["memory_packet"] = (
                self.memory_orchestrator.build_memory_packet(query)
            )
        except Exception as exc:
            context["memory_packet"] = {
                "error": type(exc).__name__,
                "budget_context": "",
                "provenance": [],
                "used_tokens": 0,
            }
        return context

    @staticmethod
    def _model_context(context: dict) -> dict:
        model_context = dict(context)
        memory_packet = model_context.pop("memory_packet", {})
        bounded_context = memory_packet.get("budget_context", "")
        if bounded_context:
            model_context["bounded_memory_context"] = bounded_context
        return model_context

    @staticmethod
    def _attach_memory_metadata(result: dict, context: dict) -> dict:
        memory_packet = context.get("memory_packet") or {}
        metadata = result.setdefault("metadata", {})
        metadata["memory_provenance"] = list(
            memory_packet.get("provenance") or []
        )
        metadata["memory_used_tokens"] = memory_packet.get("used_tokens", 0)
        if memory_packet.get("error"):
            metadata["memory_retrieval_error"] = memory_packet["error"]
        return result

    def execute(self, query: str, context: dict | None = None) -> dict:
        context = self._enrich_memory(query, context)
        model_context = self._model_context(context)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Butler Agent Core. Decide how to satisfy the user. "
                    "Use the Butler tool for executable capabilities. After each "
                    "tool observation, continue reasoning and return a concise final "
                    "answer in the user's language. Never invent capability IDs. "
                    "Voice is only an input method. Never start secretary recording "
                    "for a normal voice request. Call start_secretary_session only "
                    "when the current user message explicitly asks for a continuing "
                    "recording session, with an exact supporting quote. Use bounded "
                    "memory only when it contains a relevant fact. If a requested "
                    "stored fact is absent, say it was not found; never invent it."
                    " Treat memory as historical context, not as proof of current "
                    "external state. Questions about what currently exists in a "
                    "directory or file must use an available filesystem read "
                    "capability and the final answer must follow its observation. "
                    "If the live path cannot be read, report that failure honestly."
                ),
            },
            {
                "role": "user",
                "content": (
                    query if not model_context else
                    f"{query}\n\nBUTLER_CONTEXT:\n"
                    f"{json.dumps(model_context, ensure_ascii=False, default=str)}"
                ),
            },
        ]
        tools = self._tool_definitions()

        # --- Evidence gate: classify the query and track observations --------
        tracker = EvidenceTracker()
        tracker.classify_query(query)

        last_observation = None
        for _ in range(6):
            try:
                message = self._chat(messages, tools)
            except AgentCoreUnavailable:
                if last_observation is None:
                    raise
                result = dict(last_observation)
                result.setdefault("metadata", {})["agent_core_continuation"] = "FAILED"
                return self._attach_memory_metadata(result, context)

            messages.append(message)
            calls = message.get("tool_calls") or []

            if not calls:
                # --- Completion gate check -----------------------------------
                if tracker.requires_content and not tracker.has_content_evidence:
                    # Content evidence required but absent — force continuation.
                    # Append a system reminder so the model knows it must read files.
                    messages.append({
                        "role": "system",
                        "content": (
                            "EVIDENCE GATE: Your query requires content analysis, "
                            "but no file contents have been read yet. You MUST call "
                            "a filesystem read capability to inspect actual file "
                            "contents before providing a final answer. Do not base "
                            "your answer on filenames alone."
                        ),
                    })
                    continue

                if tracker.evidence_sufficient():
                    return self._attach_memory_metadata({
                        "ok": True,
                        "department": "AGENT_CORE",
                        "model": self.model,
                        "latency_ms": 0,
                        "text": message.get("content") or "",
                        "error": None,
                        "metadata": {
                            "tool_source": "CapabilityRegistry",
                            "evidence_type": tracker._query_type,
                            "structure_evidence": tracker.has_structure_evidence,
                            "content_evidence": tracker.has_content_evidence,
                        },
                    }, context)
                else:
                    # No observations at all — something is wrong. Continue.
                    messages.append({
                        "role": "system",
                        "content": (
                            "EVIDENCE GATE: You have not called any tool yet. "
                            "You must execute at least one capability to gather "
                            "evidence before providing a final answer."
                        ),
                    })
                    continue

            for call in calls:
                function = call.get("function") or {}
                arguments = function.get("arguments") or {}
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments)
                    except ValueError:
                        arguments = {}
                if function.get("name") == self.VOICE_TOOL_NAME and self.secretary_session:
                    observation = self._execute_secretary_tool(arguments, query)
                elif function.get("name") != self.TOOL_NAME:
                    observation = {"ok": False, "error": "UNKNOWN_TOOL"}
                else:
                    observation = self._execute_tool(arguments, context)

                last_observation = observation
                tracker.record_observation(observation)

                messages.append({
                    "role": "tool",
                    "content": json.dumps(observation, ensure_ascii=False, default=str),
                })

        raise AgentCoreUnavailable("AGENT_CORE_STEP_LIMIT")