"""Stable engineering API and explicit index lifecycle orchestration."""

from datetime import datetime, timezone
from pathlib import Path
import time
from threading import RLock

from .analyzers import DuplicateDetector
from .graphs import ProjectGraphBuilder
from .index import IndexBuilder, KnowledgeCache
from .loaders import InventoryLoader, ManifestLoader, ScopeResolver
from .query import QueryEngine
from .reports import ArchitectureReporter
from .scanner import RepositoryScanner


class RepositoryKnowledgeService:
    def __init__(self, root: Path, observation=None):
        self.root, self.observation = root.resolve(), observation
        self.cache, self.query_engine = KnowledgeCache(), QueryEngine()
        self._build_lock = RLock()
        self.build_count = 0
        self.scan_count = 0
        self.last_build_duration_ms = 0
        self.last_error = None

    def _record(self, event, payload):
        if self.observation is None: return
        try: self.observation.record(source="RepositoryKnowledgeDepartment", event=event, payload=payload)
        except Exception: pass

    def build_index(self):
        return self._build("INDEX_COLD_BUILD")

    def refresh_index(self):
        return self._build("INDEX_REFRESH")

    def _build(self, event):
        with self._build_lock:
            if event == "INDEX_COLD_BUILD" and self.cache.get() is not None:
                self._record("INDEX_CACHE_HIT", {"index_version": self.cache.get().index_version})
                return self._operation("get_index", self.cache.get().to_dict(), time.perf_counter())
            started = time.perf_counter()
            previous = self.cache.get()
            try:
                scope, scope_diag = ScopeResolver().load(self.root)
                if scope_diag.status != "OK":
                    raise RuntimeError(f"{scope_diag.reason}: {dict(scope_diag.details)}")
                manifest, manifest_diag = ManifestLoader().load(self.root)
                if manifest_diag.status != "OK":
                    raise RuntimeError(f"{manifest_diag.reason}: {dict(manifest_diag.details)}")
                inventory, inventory_diag = InventoryLoader().load(self.root)
                self.scan_count += 1
                files, scan_diags = RepositoryScanner(self.root, scope).scan()
                diagnostics = [scope_diag.to_dict(), manifest_diag.to_dict(), inventory_diag.to_dict(), *scan_diags]
                candidate = IndexBuilder().build(files, {"scope":scope,"manifest":manifest,"inventory":inventory}, diagnostics)
                published = self.cache.publish(candidate)
                self.build_count += 1
                self.last_error = None
                self.last_build_duration_ms = int((time.perf_counter() - started) * 1000)
                self._record(event, {"index_version":published.index_version,"files":len(files),
                    "duration_ms":self.last_build_duration_ms,"scan_count":self.scan_count})
                return self._operation(event.casefold(), published.to_dict(), started)
            except Exception as error:
                self.last_error = f"{type(error).__name__}: {error}"
                self.last_build_duration_ms = int((time.perf_counter() - started) * 1000)
                failed_event = "INDEX_REFRESH_FAILED" if event == "INDEX_REFRESH" else "INDEX_COLD_BUILD_FAILED"
                self._record(failed_event, {"error": self.last_error, "index_preserved": previous is not None})
                if previous is None:
                    raise
                return {**self._operation("refresh_index", previous.to_dict(), started),
                        "degraded": True, "status": "DEGRADED", "errors": [self.last_error]}

    def index(self):
        index = self.cache.get()
        if index is not None:
            self._record("INDEX_CACHE_HIT", {"index_version": index.index_version})
            return index
        self.build_index()
        index = self.cache.get()
        if index is None:
            raise RuntimeError("Repository index is unavailable")
        return index

    def get_index_status(self):
        started = time.perf_counter()
        index = self.cache.get()
        data = {
            "root": str(self.root), "index_ready": index is not None,
            "index_version": index.index_version if index else None,
            "repository_version": index.repository_version if index else None,
            "built_at": index.build_timestamp if index else None,
            "build_count": self.build_count, "scan_count": self.scan_count,
            "last_build_duration_ms": self.last_build_duration_ms, "last_error": self.last_error,
        }
        return self._operation("get_index_status", data, started)

    def query(self, operation="query", value=None, filters=None):
        started = time.perf_counter(); result = self.query_engine.query(self.index(), operation, value, filters)
        self._record("QUERY_EXECUTION", {"operation":operation,"matches":len(result["matches"])})
        return self._operation("query", result, started)

    def find_department(self, name): return self.query("find_department", name)
    def find_manager(self, name): return self.query("find_manager", name)
    def find_handler(self, name): return self.query("find_handler", name)
    def find_engine(self, name): return self.query("find_engine", name)
    def find_class(self, name): return self.query("find_class", name)
    def find_function(self, name): return self.query("find_function", name)
    def find_import(self, name): return self.query("find_import", name)
    def find_registration(self, name): return self.query("find_registration", name)
    def find_runtime(self, name): return self.query("find_runtime", name)
    def find_dependency(self, name): return self.query("find_dependency", name)
    def find_owner(self, name): return self.query("find_owner", name)
    def find_category(self, name): return self.query("find_category", name)
    def find_entry_point(self, name): return self.query("find_entry_point", name)
    def find_execution_chain(self, name=None): return self._operation("find_execution_chain", self._runtime_graph(), time.perf_counter())
    def find_permission_chain(self, name=None):
        graph = self._runtime_graph(); graph["edges"] = [edge for edge in graph["edges"] if edge["edge_type"] in {"permission","execute"}]
        return self._operation("find_permission_chain", graph, time.perf_counter())
    def find_duplicates(self, name=None):
        started=time.perf_counter(); data=DuplicateDetector().detect(self.index().nodes,self.index().edges)
        return self._operation("find_duplicates", data, started)
    def _project_graph(self): return ProjectGraphBuilder().build(self.index())
    def _dependency_graph(self): return ProjectGraphBuilder().dependency(self.index())
    def _runtime_graph(self): return ProjectGraphBuilder().runtime(self.index())
    def build_project_graph(self): return self._operation("build_project_graph", self._project_graph(), time.perf_counter())
    def build_dependency_graph(self): return self._operation("build_dependency_graph", self._dependency_graph(), time.perf_counter())
    def build_runtime_graph(self): return self._operation("build_runtime_graph", self._runtime_graph(), time.perf_counter())
    def build_architecture_report(self):
        started=time.perf_counter(); data=ArchitectureReporter().report(self.index(),self._project_graph(),self._dependency_graph(),self._runtime_graph())
        self._record("REPORT_GENERATION", {"index_version":self.index().index_version})
        return self._operation("build_architecture_report", data, started)

    # ------------------------------------------------------------------ #
    #  File enumeration via RepositoryIndex (replaces direct tree scans)   #
    # ------------------------------------------------------------------ #

    def list_files(self, extension=None):
        """Return all indexed file paths, optionally filtered by extension."""
        filters = {"type": "File"}
        if extension:
            filters["extension"] = extension
        result = self.query("list_files", filters=filters)
        matches = result.get("data", {}).get("matches", [])
        return [m["file"] for m in matches]

    def find_by_extension(self, ext):
        """Convenience: list files matching a given extension."""
        return self.list_files(extension=ext)

    def get_file_metadata(self, path):
        """Return metadata dict for a specific indexed file path."""
        result = self.query("list_files", filters={"type": "File"})
        matches = result.get("data", {}).get("matches", [])
        for m in matches:
            if m["file"] == path:
                return m
        return None

    def _operation(self, operation, data, started):
        index = self.cache.get()
        return {"success":True,"operation":operation,"timestamp":datetime.now(timezone.utc).isoformat(),
            "repository_version":index.repository_version if index else None,
            "index_version":index.index_version if index else None,
            "execution_time_ms":int((time.perf_counter()-started)*1000),"data":data,
            "diagnostics":list(index.diagnostics) if index else [],"warnings":[],"errors":[]}
