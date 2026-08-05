# -*- coding: utf-8 -*-

from A_04_AGENTS.base_department import BaseDepartment
from A_04_AGENTS.ProjectDocumentationDepartment.Core.engineering_pipeline import EngineeringPipeline
from A_04_AGENTS.ProjectDocumentationDepartment.Core.evidence_doctor import dispatch as evidence_doctor
from A_02_MANAGERS.ArchitectAgent.architect_agent import ArchitectAgent
from A_07_MEMORY.semantic_reasoning_engine import SemanticReasoningEngine
from io import StringIO
from contextlib import redirect_stdout
import sys
import time


class ProjectDocumentationDepartment(BaseDepartment):

    NAME = "PROJECT_DOCUMENTATION"
    VERSION = "1.0"
    CAPABILITIES = ("engineering_report", "project_evidence_doctor", "architect_question")
    DEPENDENCIES = ("EngineeringPipeline", "evidence_doctor", "ArchitectAgent")
    DATA_READS = ("project engineering evidence sources",)
    DATA_WRITES = ("evidence doctor command-dependent outputs",)

    KEYWORDS = [
        "кто ты",
        "что сделано",
        "состояние проекта",
        "статус проекта",
        "архитектура",
        "документация",
        "инженерная документация",
        "engineering",
        "roadmap",
        "дорожная карта",
        "доктор проекта",
        "capability",
        "зарегистрирован",
        "стадия проекта",
        "стад",
        "нужно создать новый",
    ]

    def __init__(self, architect=None):
        self.architect = architect or ArchitectAgent()

    def can_handle(self, query: str, context: dict = None) -> bool:

        q = (query or "").lower()
        return bool((context or {}).get("architectural_query")) or any(k in q for k in self.KEYWORDS) or self._is_architect_query(q)

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.time()
        context = dict(context or {})
        query = (query or "").strip()

        if not query:
            return self._error_result(
                started, "EMPTY_QUERY",
                "Не указан запрос к проектной документации."
            )

        q = query.lower()

        if context.get("architectural_query") or self._is_architect_query(q):
            try:
                architect_query = query
                semantic_intent = context.get("semantic_intent", {})
                if semantic_intent.get("name") == "PROJECT_SELF_KNOWLEDGE":
                    if semantic_intent.get("focus") == "PROJECT_LIFECYCLE":
                        architect_query = f"{query}\nСостояние проекта"
                    elif semantic_intent.get("focus") == "PROJECT_OVERVIEW":
                        architect_query = f"{query}\nПокажи всю архитектуру Butler"
                answer = self.architect.answer(architect_query)
            except Exception as exc:
                return self._error_result(
                    started, "ARCHITECT_AGENT_ERROR",
                    "ArchitectAgent не смог сформировать ответ.",
                    metadata={"exception_type": type(exc).__name__},
                )
            return {
                "ok": True,
                "department": self.NAME,
                "model": answer.get("model"),
                "latency_ms": int((time.time() - started) * 1000),
                "text": answer.get("text", ""),
                "metadata": {
                    "architect_agent": True,
                    "llm_used": answer.get("llm_used", False),
                    "model_output_accepted": answer.get("model_output_accepted", False),
                    "provider": answer.get("provider"),
                    "provider_error": answer.get("provider_error"),
                    "evidence": answer.get("evidence", {}),
                },
                "error": None,
            }

        if "доктор проекта" in q:
            if "статус" in q:
                doctor_command = "status"
            elif "пересобери" in q:
                doctor_command = "rebuild"
            elif "аудит" in q:
                doctor_command = "audit"
            elif "план" in q:
                doctor_command = "plan"
            elif "примен" in q:
                doctor_command = "apply"
            elif "подтверд" in q:
                doctor_command = "confirm"
            else:
                doctor_command = "status"

            buf = StringIO()
            original_argv = list(sys.argv)

            try:
                sys.argv = ["evidence_doctor.py", doctor_command]
                with redirect_stdout(buf):
                    evidence_doctor()
            except Exception as exc:
                return self._error_result(
                    started, "EVIDENCE_DOCTOR_ERROR",
                    "Ошибка выполнения Project Evidence Doctor.",
                    metadata={
                        "doctor": True,
                        "command": doctor_command,
                        "exception_type": type(exc).__name__,
                    },
                )
            finally:
                sys.argv = original_argv

            doctor_text = buf.getvalue().strip()
            if not doctor_text:
                return self._error_result(
                    started, "EMPTY_PROJECT_DOCUMENTATION_RESULT",
                    "Project Evidence Doctor не вернул результат.",
                    metadata={"doctor": True, "command": doctor_command},
                )

            return {
                "ok": True,
                "department": self.NAME,
                "model": "PROJECT_DOCUMENTATION_DEPARTMENT",
                "latency_ms": int((time.time() - started) * 1000),
                "text": doctor_text,
                "metadata": {"doctor": True, "command": doctor_command},
                "error": None,
            }

        try:
            pipeline = EngineeringPipeline()
            catalog = pipeline.execute()
        except Exception as exc:
            return self._error_result(
                started, "PROJECT_DOCUMENTATION_PIPELINE_ERROR",
                "Ошибка выполнения Engineering Pipeline.",
                metadata={"exception_type": type(exc).__name__},
            )

        if catalog is None or not callable(getattr(catalog, "count", None)) or not callable(getattr(catalog, "all", None)):
            return self._error_result(
                started, "EMPTY_PROJECT_DOCUMENTATION_RESULT",
                "Engineering Pipeline не вернул корректный каталог."
            )

        lines = [
            "=== PROJECT ENGINEERING REPORT ===",
            "",
            f"OBJECTS : {catalog.count()}",
            ""
        ]

        for obj in catalog.all():
            lines.append(
                f"{obj.object_id} | {obj.name} | {len(getattr(obj,'evidence',[]))} evidence"
            )

        return {
            "ok":True,
            "department":self.NAME,
            "model":"PROJECT_DOCUMENTATION_DEPARTMENT",
            "latency_ms": int((time.time() - started) * 1000),
            "text":"\n".join(lines),
            "metadata":{"objects":catalog.count(), "doctor":False},
            "error":None
        }

    @staticmethod
    def _is_architect_query(query: str) -> bool:
        intent = SemanticReasoningEngine().detect_intent(query)
        return intent.get("name") == "PROJECT_SELF_KNOWLEDGE"

    def _error_result(self, started, error, text, metadata=None):
        return {
            "ok": False,
            "department": self.NAME,
            "model": "PROJECT_DOCUMENTATION_DEPARTMENT",
            "latency_ms": max(0, int((time.time() - started) * 1000)),
            "text": text,
            "metadata": dict(metadata or {}),
            "error": str(error),
        }


if __name__ == "__main__":

    dep = ProjectDocumentationDepartment()

    result = dep.execute("что сделано")

    print(result["text"])
