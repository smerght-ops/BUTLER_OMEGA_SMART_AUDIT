"""Deterministic queries over a published RepositoryIndex only."""

from datetime import datetime, timezone
import re


class QueryEngine:
    def query(self, index, operation, value=None, filters=None):
        filters = dict(filters or {})
        operation = str(operation or "query").casefold()
        value = "" if value is None else str(value)
        type_map = {
            "find_department": "Department", "find_manager": "Manager", "find_handler": "Handler",
            "find_engine": "Engine", "find_class": "Class", "find_function": "Function",
            "find_runtime": "Runtime", "find_import": None, "find_registration": "Department",
            "find_dependency": None, "find_owner": None, "find_category": None,
            "find_entry_point": None, "query": None, "list_files": None,
        }
        nodes = list(index.nodes)
        expected_type = type_map.get(operation)
        if operation == "find_class":
            class_types = {"Class", "Department", "Manager", "Handler", "Engine", "Gateway", "Coordinator"}
            nodes = [item for item in nodes if item.get("type") in class_types]
        elif expected_type:
            nodes = [item for item in nodes if item.get("type") == expected_type]
        if operation == "find_category":
            nodes = [item for item in nodes if value.casefold() in str(item.get("category", "")).casefold()]
        elif operation == "find_owner":
            nodes = [item for item in nodes if value.casefold() in str(item.get("owner", "")).casefold()]
        elif operation in {"find_dependency", "find_import"}:
            identifiers = {item["identifier"] for item in index.nodes if self._matches(item, value, "contains")}
            edge_type = "imports" if operation == "find_import" else None
            related = {edge["source"] for edge in index.edges if (not edge_type or edge["edge_type"] == edge_type) and (edge["source"] in identifiers or edge["target"] in identifiers)}
            related |= {edge["target"] for edge in index.edges if (not edge_type or edge["edge_type"] == edge_type) and (edge["source"] in identifiers or edge["target"] in identifiers)}
            nodes = [item for item in index.nodes if item["identifier"] in related]
        elif value:
            mode = filters.get("match", "contains")
            nodes = [item for item in nodes if self._matches(item, value, mode)]
        # list_files: return File nodes, optionally filtered by extension
        if operation == "list_files":
            ext_filter = filters.get("extension")
            file_nodes = [item for item in nodes if item.get("file") is not None]
            if ext_filter:
                file_nodes = [item for item in file_nodes if str(item.get("file", "")).endswith(ext_filter)]
            # Also apply standard type filter if specified
            if filters.get("type"):
                file_nodes = [item for item in file_nodes if str(item.get("type", "")).casefold() == str(filters["type"]).casefold()]
            nodes = file_nodes
        else:
            for key in ("type", "category", "owner", "registration_status", "runtime_status"):
                if filters.get(key) is not None:
                    nodes = [item for item in nodes if str(item.get(key, "")).casefold() == str(filters[key]).casefold()]
        matches = [self._match(index, item) for item in sorted(nodes, key=lambda item: self._rank(item, value))[:200]]
        return {"success": True, "query": {"operation":operation,"value":value,"filters":filters},
            "timestamp": datetime.now(timezone.utc).isoformat(), "index_version": index.index_version,
            "matches": matches, "diagnostics": list(index.diagnostics)}

    @staticmethod
    def _matches(item, value, mode):
        fields = " ".join(str(item.get(key, "")) for key in ("identifier","name","type","category","file","owner"))
        needle, haystack = value.casefold(), fields.casefold()
        if mode == "exact": return needle == str(item.get("name", "")).casefold()
        if mode == "prefix": return str(item.get("name", "")).casefold().startswith(needle)
        if mode == "suffix": return str(item.get("name", "")).casefold().endswith(needle)
        if mode == "regex":
            try: return re.search(value, fields, re.I) is not None
            except re.error: return False
        return needle in haystack

    @staticmethod
    def _rank(item, value):
        name, needle = str(item.get("name", "")).casefold(), value.casefold()
        return (0 if name == needle else 1 if name.startswith(needle) else 2, name, item["identifier"])

    @staticmethod
    def _match(index, item):
        identifier = item["identifier"]
        edges = [edge for edge in index.edges if identifier in {edge["source"], edge["target"]}]
        related = sorted({edge["target"] if edge["source"] == identifier else edge["source"] for edge in edges})
        return {"identifier":identifier,"name":item.get("name"),"type":item.get("type"),
            "category":item.get("category"),"file":item.get("file"),"line":item.get("line"),
            "owner":item.get("owner"),"confidence":item.get("confidence"),
            "related_nodes":related,"related_edges":edges}
