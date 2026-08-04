"""Butler Department boundary for canonical read-only repository knowledge."""

import time
from pathlib import Path

from A_04_AGENTS.base_department import BaseDepartment
from A_03_ORCHESTRATION.observation_layer import ObservationLayer
from .service import RepositoryKnowledgeService


class RepositoryKnowledgeDepartment(BaseDepartment):
    NAME = "REPOSITORY_KNOWLEDGE"
    VERSION = "1.0"
    CAPABILITIES = ("repository_knowledge", "engineering_query", "architecture_report")
    KEYWORDS = (
        "repository knowledge", "repository architecture", "repository index",
        "knowledge repository", "знания репозитория", "индекс репозитория",
        "архитектура репозитория", "регистрация department", "permission chain",
    )

    def __init__(self, root=None, observation=None):
        self.root = Path(root or Path(__file__).resolve().parents[2]).resolve()
        self.observation = observation or ObservationLayer()
        self._service = RepositoryKnowledgeService(self.root, self.observation)

    def can_handle(self, query: str, context: dict = None) -> bool:
        normalized = " ".join(str(query or "").casefold().split())
        return bool((context or {}).get("repository_knowledge")) or any(
            marker in normalized for marker in self.KEYWORDS
        )

    def execute(self, query: str, context: dict = None, **kwargs) -> dict:
        started = time.perf_counter()
        try:
            data = self.query(query, context=context)
            return self._result(started, True, data, None)
        except Exception as error:
            return self._result(started, False, {}, f"{type(error).__name__}: {error}")

    def _result(self, started, ok, data, error):
        return {
            "ok": bool(ok), "department": self.NAME, "model": "RepositoryKnowledgeIndex",
            "latency_ms": int((time.perf_counter() - started) * 1000),
            "text": "Repository knowledge query completed." if ok else "Repository knowledge query failed.",
            "error": error, "metadata": {"repository_knowledge": data},
        }

    def query(self, query: str, context: dict = None):
        context = dict(context or {})
        operation = context.get("repository_operation") or self._operation_from_query(query)
        value = context.get("repository_value")
        filters = context.get("repository_filters")
        if operation == "build_index": return self.build_index()
        if operation == "refresh_index": return self.refresh_index()
        if operation == "build_project_graph": return self.build_project_graph()
        if operation == "build_dependency_graph": return self.build_dependency_graph()
        if operation == "build_runtime_graph": return self.build_runtime_graph()
        if operation == "build_architecture_report": return self.build_architecture_report()
        if operation == "get_index":
            index = self._service.index()
            return self._service._operation("get_index", index.to_dict(), time.perf_counter())
        if operation == "find_duplicates": return self.find_duplicates(value)
        return self._service.query(operation, value if value is not None else query, filters)

    @staticmethod
    def _operation_from_query(query):
        normalized = str(query or "").casefold()
        routes = (("refresh", "refresh_index"), ("обнови индекс", "refresh_index"),
            ("build index", "build_index"), ("построй индекс", "build_index"),
            ("duplicate", "find_duplicates"), ("дубликат", "find_duplicates"),
            ("permission chain", "find_permission_chain"), ("runtime graph", "build_runtime_graph"),
            ("dependency graph", "build_dependency_graph"), ("project graph", "build_project_graph"),
            ("architecture report", "build_architecture_report"), ("department", "find_department"),
            ("class", "find_class"), ("function", "find_function"), ("import", "find_import"),
            ("registration", "find_registration"), ("runtime", "find_runtime"),
            ("dependency", "find_dependency"), ("category", "find_category"))
        return next((operation for marker, operation in routes if marker in normalized), "query")

    def build_index(self): return self._service.build_index()
    def refresh_index(self): return self._service.refresh_index()
    def find_department(self, name): return self._service.find_department(name)
    def find_manager(self, name): return self._service.find_manager(name)
    def find_handler(self, name): return self._service.find_handler(name)
    def find_engine(self, name): return self._service.find_engine(name)
    def find_class(self, name): return self._service.find_class(name)
    def find_function(self, name): return self._service.find_function(name)
    def find_import(self, name): return self._service.find_import(name)
    def find_registration(self, name): return self._service.find_registration(name)
    def find_runtime(self, name): return self._service.find_runtime(name)
    def find_dependency(self, name): return self._service.find_dependency(name)
    def find_owner(self, name): return self._service.find_owner(name)
    def find_category(self, name): return self._service.find_category(name)
    def find_entry_point(self, name): return self._service.find_entry_point(name)
    def find_duplicates(self, name=None): return self._service.find_duplicates(name)
    def find_execution_chain(self, name=None): return self._service.find_execution_chain(name)
    def find_permission_chain(self, name=None): return self._service.find_permission_chain(name)
    def build_project_graph(self): return self._service.build_project_graph()
    def build_dependency_graph(self): return self._service.build_dependency_graph()
    def build_runtime_graph(self): return self._service.build_runtime_graph()
    def build_architecture_report(self): return self._service.build_architecture_report()
