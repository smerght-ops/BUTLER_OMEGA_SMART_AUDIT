# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path

from A_04_AGENTS.CodingDepartment.runner import CodingDepartment
from A_04_AGENTS.MemoryDepartment.runner import MemoryDepartment
from A_04_AGENTS.VisionDepartment.runner import VisionDepartment
from A_04_AGENTS.ImageDepartment.runner import ImageDepartment
from A_04_AGENTS.AudioDepartment.runner import AudioDepartment
from A_03_ENGINES.Audio_Engine.whisper_engine import create_audio_engine
from A_04_AGENTS.TextDepartment.runner import TextDepartment
from A_04_AGENTS.VideoDepartment.runner import VideoDepartment
from A_04_AGENTS.ArchiveDepartment.runner import ArchiveDepartment
from A_04_AGENTS.FilesystemDepartment.runner import FilesystemDepartment
from A_04_AGENTS.SearchDepartment.runner import SearchDepartment
from A_04_AGENTS.DocumentsDepartment.runner import DocumentsDepartment
from A_04_AGENTS.OpenDocumentDepartment.runner import OpenDocumentDepartment
from A_04_AGENTS.ProjectDocumentationDepartment.runner import ProjectDocumentationDepartment
from A_04_AGENTS.HomeDepartment.runner import HomeDepartment
from A_04_AGENTS.BrowserDepartment.runner import BrowserDepartment
from A_04_AGENTS.PublicationGuardianDepartment.runner import PublicationGuardianDepartment
from A_07_MEMORY.semantic_memory import SemanticMemory
from A_07_MEMORY.semantic_reasoning_engine import SemanticReasoningEngine
from A_03_ORCHESTRATION.butler_harness import ButlerHarness
from A_02_MANAGERS.smart_dispatcher import SmartDispatcher
from A_02_MANAGERS.goal_manager import GoalManager
from A_07_MEMORY.memory_orchestrator_v2 import MemoryOrchestratorV2
from A_01_CORE.TaskExecutor.task_executor import TaskExecutor


class SmartDispatcherV2:

    def __init__(self):
        self.semantic_memory = SemanticMemory()
        self.reasoning_engine = SemanticReasoningEngine()
        self._last_semantic_intent = None
        self.harness = ButlerHarness()
        self.chat_provider = SmartDispatcher()
        self.memory_orchestrator = MemoryOrchestratorV2(token_budget=1200)
        self.task_executor = TaskExecutor()
        self.audio_engine = create_audio_engine()

        # Specialized handlers precede broad HOME/DOCUMENTS handlers.
        self.departments = [
            # Publication inspection is a mandatory security gate and must be
            # registered before broad operational departments.
            PublicationGuardianDepartment(),
            ProjectDocumentationDepartment(),
            BrowserDepartment(),
            ImageDepartment(),
            VideoDepartment(),
            AudioDepartment(),
            ArchiveDepartment(),
            FilesystemDepartment(),
            GoalManager(),
            CodingDepartment(),
            VisionDepartment(),
            SearchDepartment(),
            MemoryDepartment(),
            OpenDocumentDepartment(),
            DocumentsDepartment(),
            TextDepartment(),
            HomeDepartment(),
        ]

    def _dept_name(self, dept):
        return str(
            getattr(
                dept,
                "NAME",
                getattr(dept, "name", type(dept).__name__)
            )
        ).upper()

    def _find_dept_by_name(self, name: str):
        for dept in self.departments:
            if self._dept_name(dept) == name.upper():
                return dept
        return None

    @staticmethod
    def _publication_guardian_fault(error: str) -> dict:
        """Return a stable fail-closed dispatcher response without leaking data."""
        return {
            "ok": False,
            "department": "PUBLICATION_GUARDIAN",
            "model": "SmartDispatcherV2",
            "latency_ms": 0,
            "text": "Publication Guardian: FAULT_BLOCK",
            "error": error,
            "metadata": {
                "publication_allowed": False,
                "publication_result": {
                    "api_version": "v1",
                    "status": "FAULT_BLOCK",
                    "error_category": error,
                },
            },
        }

    def _dispatch_publication_guardian(self, query: str, context: dict) -> dict:
        guardian = self._find_dept_by_name("PUBLICATION_GUARDIAN")
        if guardian is None:
            return self._publication_guardian_fault("GUARDIAN_UNAVAILABLE")
        try:
            result = self._execute_department(guardian, query, context=context)
        except Exception:
            return self._publication_guardian_fault("GUARDIAN_EXECUTION_FAILED")
        if not isinstance(result, dict):
            return self._publication_guardian_fault("GUARDIAN_INVALID_RESPONSE")
        metadata = result.get("metadata")
        publication = metadata.get("publication_result") if isinstance(metadata, dict) else None
        status = publication.get("status") if isinstance(publication, dict) else None
        allowed = metadata.get("publication_allowed") is True if isinstance(metadata, dict) else False
        expected_allowed = status in {"PASS", "PASS_WITH_WARNINGS"}
        if status not in {"PASS", "PASS_WITH_WARNINGS", "BLOCK", "FAULT_BLOCK"}:
            return self._publication_guardian_fault("GUARDIAN_INVALID_RESPONSE")
        if allowed != expected_allowed or bool(result.get("ok")) != expected_allowed:
            return self._publication_guardian_fault("GUARDIAN_CONTRACT_MISMATCH")
        return result

    def _execute_task_plan(self, plan: dict, context: dict = None) -> dict:
        """Execute all steps in a TaskPlan through existing departments."""
        context = dict(context or {})
        step_outputs = {}

        for step in plan.get("steps", []):
            dept_name = step.get("department", "UNKNOWN")
            dept = self._find_dept_by_name(dept_name)
            if not dept:
                return {
                    "ok": False,
                    "error": f"Department {dept_name} not found",
                    "step": step
                }

            action = step.get("action", "")
            arguments = dict(step.get("arguments", {}))
            query = arguments.pop("query", action)

            # Handle dependencies - substitute previous outputs
            for dep_order in step.get("depends_on", []):
                dep_output = step_outputs.get(dep_order, {}).get("output")
                if dep_output:
                    placeholder = f"{{{{step_{dep_order}.output}}}}"
                    query = str(query).replace(placeholder, str(dep_output))
                    for key in arguments:
                        arguments[key] = str(arguments[key]).replace(placeholder, str(dep_output))

            # Build context from step arguments
            step_context = dict(context)
            step_context.update(arguments)

            result = self._execute_department(dept, query, context=step_context)
            step_outputs[step.get("order", 0)] = {
                "output": result,
                "department": dept_name,
                "action": action
            }

        # Return final output from last step
        if step_outputs:
            last_order = max(step_outputs.keys())
            return step_outputs[last_order]["output"]

        return {"ok": False, "error": "No steps executed"}

    def _execute_department(self, dept, query, context=None):

        context = dict(context or {})
        if self._dept_name(dept) == "AUDIO":
            context["audio_engine"] = self.audio_engine

        def executor():

            try:
                return dept.execute(query, context=context)
            except TypeError:
                return dept.execute(query)

        harness_result = self.harness.execute(
            department_name=self._dept_name(dept),
            task=query,
            executor=executor
        )

        if harness_result.get("committed"):
            committed = harness_result.get("commit_result")
            if (
                self._dept_name(dept) == "AUDIO"
                and committed.get("ok")
                and committed.get("metadata", {}).get("mode") == "recognize"
            ):
                return self._persist_voice_inbox(committed)
            return committed

        return harness_result

    def _persist_voice_inbox(self, audio_result: dict) -> dict:
        """Persist an unchanged recognized transcript through FILESYSTEM,
        then compile DKI from the saved RAW transcript."""
        transcript = audio_result.get("text")
        if transcript is None:
            return audio_result

        folder = (
            Path(__file__).resolve().parents[1]
            / "A_06_WORKSPACE" / "STAGE4_OUTPUT" / "voice_inbox"
        )
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
        filename = f"{timestamp}_raw_transcript.md"
        collision = 1
        while (folder / filename).exists():
            filename = f"{timestamp}_{collision}_raw_transcript.md"
            collision += 1
        filesystem = self._find_dept_by_name("FILESYSTEM")
        save_result = self._execute_department(
            filesystem,
            "Сохрани RAW transcript в Voice Inbox.",
            context={
                "capability_action": "save_text",
                "folder": str(folder),
                "filename": filename,
                "content": transcript,
                "raw_transcript": True,
            },
        )
        metadata = audio_result.setdefault("metadata", {})
        metadata["voice_inbox"] = {
            "ok": bool(save_result.get("ok")),
            "path": save_result.get("metadata", {}).get("path"),
            "filesystem_capability": "save_text",
            "error": save_result.get("error"),
        }
        if not save_result.get("ok"):
            audio_result["ok"] = False
            audio_result["error"] = "VOICE_INBOX_SAVE_FAILED"
            return audio_result

        # --- DKI compilation (post-save, non-destructive) -------------------
        raw_path = save_result.get("metadata", {}).get("path")
        if raw_path:
            try:
                from A_07_MEMORY.dki_compiler import DKICompiler
                compiler = DKICompiler(memory=self.semantic_memory)
                compile_result = compiler.compile(str(raw_path), transcript, model_name="butler-router-70b:latest")
                metadata["dki_compile"] = {
                    "status": compile_result.get("status", "UNKNOWN"),
                    "source_id": compile_result.get("source_id", ""),
                    "written_count": compile_result.get("written_count", 0),
                    "rejected_count": compile_result.get("rejected_count", 0),
                }
            except Exception as exc:
                metadata["dki_compile"] = {
                    "status": "ERROR",
                    "error": str(exc),
                }

        return audio_result

    def _execute_chat(self, query, context=None):

        context = dict(context or {})

        def executor():

            memory_packet = context.get("memory_packet") or {}
            memory_block = memory_packet.get("budget_context", "")

            provider_result = self.chat_provider.execute_employee(
                employee="chat",
                system_prompt=(
                    "Ты Butler Omega Smart. Отвечай пользователю по-русски, "
                    "содержательно и по существу. Верни только готовый ответ. "
                    "Не показывай внутренний анализ, планы и служебные инструкции."
                ),
                user_content=(
                    f"РЕЛЕВАНТНАЯ ПАМЯТЬ:\n{memory_block}\n\nЗАПРОС:\n{query}"
                    if memory_block else query
                ),
            )

            text = self.chat_provider.clean_model_output(
                provider_result.get("text") or ""
            )
            if provider_result.get("status") != "ok" or not text:
                return {
                    "ok": False,
                    "department": "CHAT",
                    "model": provider_result.get("model"),
                    "latency_ms": provider_result.get("latency_ms", 0),
                    "text": "Не удалось получить ответ CHAT-модели.",
                    "error": "CHAT_PROVIDER_ERROR",
                    "metadata": {
                        "provider": "SmartDispatcher.execute_employee",
                        "reason": provider_result.get("fallback_reason"),
                    },
                }

            return {
                "ok": True,
                "department": "CHAT",
                "model": provider_result.get("model"),
                "latency_ms": provider_result.get("latency_ms", 0),
                "text": text,
                "error": None,
                "metadata": {
                    "provider": "SmartDispatcher.execute_employee",
                    "request_id": provider_result.get("request_id"),
                    "memory_provenance": memory_packet.get("provenance", []),
                    "memory_used_tokens": memory_packet.get("used_tokens", 0),
                },
            }

        harness_result = self.harness.execute(
            department_name="CHAT",
            task=query,
            executor=executor,
        )

        if harness_result.get("committed"):
            return harness_result.get("commit_result")

        return harness_result

    def dispatch(self, query: str, context: dict = None):

        context = dict(context or {})

        # An actual PublicationRequest is never routed through semantic/chat or
        # another department. Missing, failed, or malformed Guardian execution
        # remains a hard FAULT_BLOCK.
        if "publication_request" in context:
            return self._dispatch_publication_guardian(query, context)

        if "memory_packet" not in context:
            try:
                context["memory_packet"] = self.memory_orchestrator.build_memory_packet(query)
            except Exception as exc:
                context["memory_packet"] = {
                    "error": type(exc).__name__,
                    "budget_context": "",
                }

        # Project self-knowledge has one owner. Resolve the semantic intent
        # before broad operational departments and ungrounded CHAT.
        semantic_intent = self.reasoning_engine.detect_intent(
            query,
            inherited_intent=self._last_semantic_intent,
        )
        semantic_contract = self.reasoning_engine.build_task_contract(query)
        if semantic_intent.get("name") == "PROJECT_SELF_KNOWLEDGE":
            self._last_semantic_intent = "PROJECT_SELF_KNOWLEDGE"
            context["architectural_query"] = True
            context["semantic_intent"] = semantic_intent
            context["semantic_contract"] = semantic_contract
            architect_department = next(
                dept for dept in self.departments
                if self._dept_name(dept) == "PROJECT_DOCUMENTATION"
            )
            return self._execute_department(architect_department, query, context=context)

        # Context inheritance belongs to the active dialogue only. A turn with a
        # different intent ends the project-self-knowledge continuation chain.
        self._last_semantic_intent = None
        context["semantic_contract"] = semantic_contract

        try:
            context["semantic"] = self.reasoning_engine.reason(
                query=query,
                candidates=[
                    self._dept_name(d)
                    for d in self.departments
                ]
            )
        except Exception:
            context["semantic"] = {
                "query": query,
                "tokens": [],
                "matches": []
            }


        # Try TaskExecutor first as new primary route
        task_plan = self.task_executor.plan(query)
        context["task_plan"] = task_plan
        
        # Check if plan is valid and has executable steps
        steps = task_plan.get("steps", [])
        if not steps:
            # Fallback to original department routing logic
            q = (query or "").lower()

            # Explicit editing of an existing DOCX must go directly to DOCUMENTS
            # before broad SEARCH and CHAT routing.
            explicit_docx_edit = (
                ".docx" in q
                and any(marker in q for marker in (
                    "сделай", "жирн", "курсив", "размер", "центр",
                    "выровняй", "формат", "заголовок", "основной текст"
                ))
            )

            if explicit_docx_edit:
                documents_department = next(
                    dept for dept in self.departments
                    if self._dept_name(dept) == "DOCUMENTS"
                )
                return self._execute_department(
                    documents_department, query, context=context
                )

            explicit_memory_intent = any(marker in q for marker in (
                "в памяти",
                "из памяти",
                "запомни",
                "что ты помнишь",
                "что помнишь",
                "какой мой",
                "как меня зовут",
                "в своих знаниях",
            ))

            for dept in self.departments:

                try:
                    if self._dept_name(dept) == "SEARCH" and explicit_memory_intent:
                        continue
                    try:
                        handled = dept.can_handle(query, context=context)
                    except TypeError:
                        handled = dept.can_handle(query)

                    if not handled:
                        continue

                    try:
                        return self._execute_department(dept, query, context=context)

                    except Exception as ex:
                        return {
                            "ok": False,
                            "department": self._dept_name(dept),
                            "error": str(ex)
                        }

                except Exception:
                    continue

            try:
                reasoning = context.get("semantic", {})

                if reasoning.get("matches"):
                    matches = reasoning["matches"]
                else:
                    matches = self.semantic_memory.search_by_text(query)


                if matches:
                    target = str(matches[0].get("handler", "")).upper()

                    for dept in self.departments:
                        if self._dept_name(dept) == target:
                            try:
                                return self._execute_department(dept, query, context=context)
                            except Exception as ex:
                                return {
                                    "ok": False,
                                    "department": self._dept_name(dept),
                                    "skill_router": True,
                                    "error": str(ex)
                                }

            except Exception as ex:
                return {
                    "ok": False,
                    "department": "SKILL_ROUTER",
                    "error": str(ex)
                }

        # TaskExecutor plan is valid, execute it through existing departments
        return self._execute_task_plan(task_plan, context)

    @staticmethod
    def _is_architectural_query(query: str) -> bool:
        intent = SemanticReasoningEngine().detect_intent(query)
        return intent.get("name") == "PROJECT_SELF_KNOWLEDGE"


if __name__ == "__main__":
    d = SmartDispatcherV2()

    for q in [
        "привет",
        "напиши функцию на python",
        "создай картинку дракона",
        "что изображено файл: C:\\test.jpg"
    ]:
        print(q, "=>", d.dispatch(q).get("department"))












