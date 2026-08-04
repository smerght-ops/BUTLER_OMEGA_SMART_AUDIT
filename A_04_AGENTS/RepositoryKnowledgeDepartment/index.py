"""Atomic builder and thread-safe lifecycle for the immutable repository index."""

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from threading import RLock

from .analyzers import ImportAnalyzer, RegistrationAnalyzer, RuntimeAnalyzer
from .models import RepositoryIndex, SCHEMA_VERSION


class IndexBuilder:
    def build(self, files, source_models, diagnostics):
        file_nodes = []
        for item in files:
            node_type = "File"
            file_nodes.append({"identifier": item.identifier, "name": item.name, "type": node_type,
                "category": item.category, "file": item.relative_path, "line": 1,
                "owner": item.relative_path.rsplit("/", 1)[0] if "/" in item.relative_path else "repository",
                "confidence": "HIGH", "sha256": item.sha256, "module": item.module,
                "runtime_status": "UNKNOWN", "registration_status": "UNKNOWN",
                "dependencies": [], "reverse_dependencies": [], "metadata": dict(item.metadata)})
            for symbol in item.symbols:
                identifier = "symbol:" + hashlib.sha256(f"{item.relative_path}:{symbol['name']}:{symbol['line']}".encode()).hexdigest()[:20]
                symbol_type = "Class" if symbol["kind"] == "ClassDef" else "Function"
                if symbol_type == "Class":
                    for suffix, specialized in (("Department","Department"),("Manager","Manager"),
                            ("Handler","Handler"),("Engine","Engine"),("Gateway","Gateway"),
                            ("Coordinator","Coordinator")):
                        if symbol["name"].endswith(suffix):
                            symbol_type = specialized
                            break
                file_nodes.append({"identifier": identifier, "name": symbol["name"],
                    "type": symbol_type,
                    "category": item.category, "file": item.relative_path, "line": symbol["line"],
                    "owner": item.identifier, "confidence": "HIGH", "runtime_status": "UNKNOWN",
                    "registration_status": "UNKNOWN", "dependencies": [], "reverse_dependencies": [], "metadata": {}})
        inventory = source_models.get("inventory", {})
        path_identifiers = {item["file"]: item["identifier"] for item in file_nodes if item["type"] == "File"}
        for component in inventory.get("components", []) if isinstance(inventory, dict) else []:
            path = str(component.get("path") or "")
            if not path or path in path_identifiers:
                continue
            identifier = "inventory:" + hashlib.sha256(path.encode()).hexdigest()[:20]
            path_identifiers[path] = identifier
            file_nodes.append({"identifier":identifier,"name":path.rsplit("/",1)[-1],
                "type":str(component.get("category") or "File"),
                "category":str(component.get("preliminary_classification") or component.get("category") or "UNKNOWN"),
                "file":path,"line":None,"owner":path.rsplit("/",1)[0] if "/" in path else "repository",
                "confidence":str(component.get("confidence") or "MEDIUM"),"sha256":component.get("sha256"),
                "module":None,"runtime_status":"ACTIVE" if component.get("production_reachability") else "UNKNOWN",
                "registration_status":"UNKNOWN","dependencies":[],"reverse_dependencies":[],
                "metadata":{"inventory_only":True,"decision":component.get("preliminary_decision")}})
        import_edges, broken = ImportAnalyzer().analyze(files)
        for relationship in inventory.get("relationships", []) if isinstance(inventory, dict) else []:
            source_path, target_path = relationship.get("source"), relationship.get("target")
            if source_path in path_identifiers and target_path in path_identifiers:
                import_edges.append(ImportAnalyzer._edge(path_identifiers[source_path], path_identifiers[target_path],
                    str(relationship.get("type") or "uses").casefold(), source_path, relationship.get("line")))
        departments, registrations = RegistrationAnalyzer().analyze(files)
        known = {item["identifier"] for item in file_nodes}
        file_nodes.extend(item for item in departments if item["identifier"] not in known)
        runtime_nodes, runtime_edges = RuntimeAnalyzer().analyze(files)
        nodes, edges = file_nodes + runtime_nodes, import_edges + runtime_edges
        forward, reverse = defaultdict(list), defaultdict(list)
        for edge in edges:
            forward[edge["source"]].append(edge["target"]); reverse[edge["target"]].append(edge["source"])
        for node in nodes:
            node["dependencies"] = sorted(set(forward[node["identifier"]]))
            node["reverse_dependencies"] = sorted(set(reverse[node["identifier"]]))
        repository_version = hashlib.sha256("\n".join(sorted(item.sha256 for item in files)).encode()).hexdigest()
        index_version = hashlib.sha256(f"{SCHEMA_VERSION}:{repository_version}".encode()).hexdigest()[:24]
        collections = defaultdict(list)
        for node in nodes:
            collections[node["type"].casefold() + "s"].append(node["identifier"])
            collections["categories:" + str(node["category"])].append(node["identifier"])
        source_versions = {
            "PROJECT_SCOPE": source_models.get("scope", {}).get("metadata", {}).get("scope_version"),
            "system_manifest": source_models.get("manifest", {}).get("version"),
            "RECONSTRUCTION_INVENTORY": source_models.get("inventory", {}).get("schema_version"),
        }
        all_diagnostics = list(diagnostics) + ([{"source":"imports","status":"DEGRADED","reason":"BROKEN_IMPORTS","details":{"count":len(broken)}}] if broken else [])
        statistics = {"node_count": len(nodes), "edge_count": len(edges),
            "file_count": len(files), "department_count": len(departments),
            "registration_source_count": len(registrations), "broken_import_count": len(broken),
            "node_type_counts": dict(Counter(item["type"] for item in nodes)),
            "category_counts": dict(Counter(item["category"] for item in nodes))}
        return RepositoryIndex(SCHEMA_VERSION, index_version, repository_version,
            datetime.now(timezone.utc).isoformat(), source_versions, tuple(nodes), tuple(edges),
            {key: tuple(value) for key, value in collections.items()}, tuple(all_diagnostics), statistics)


class KnowledgeCache:
    def __init__(self):
        self._lock = RLock()
        self._index = None
    def get(self):
        with self._lock: return self._index
    def publish(self, index):
        with self._lock: self._index = index
        return index
