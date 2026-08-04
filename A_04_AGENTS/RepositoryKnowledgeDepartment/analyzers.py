"""Pure analyzers consuming scanner records without traversing the repository."""

from collections import Counter, defaultdict
import hashlib


class ImportAnalyzer:
    def analyze(self, files):
        modules = {item.module: item.identifier for item in files if item.module}
        edges, broken = [], []
        for item in files:
            for imported in item.imports:
                name = str(imported.get("module") or "").lstrip(".")
                targets = [(len(module), identifier) for module, identifier in modules.items()
                           if name == module or name.startswith(module + ".") or module.startswith(name + ".")]
                if targets:
                    edges.append(self._edge(item.identifier, max(targets)[1], "imports", item.relative_path, imported.get("line")))
                elif name and not self._stdlib_or_external(name):
                    broken.append({"source": item.relative_path, "module": name, "line": imported.get("line")})
        return edges, broken

    @staticmethod
    def _stdlib_or_external(name):
        return name.split(".", 1)[0] in {
            "abc", "ast", "collections", "contextlib", "contextvars", "copy", "csv",
            "dataclasses", "datetime", "enum", "functools", "hashlib", "importlib",
            "inspect", "io", "itertools", "json", "logging", "math", "os", "pathlib",
            "queue", "re", "shutil", "sqlite3", "stat", "subprocess", "sys", "tempfile",
            "threading", "time", "traceback", "types", "typing", "unittest", "urllib", "uuid",
            "requests", "numpy", "PIL", "scipy", "sounddevice", "yaml",
        }

    @staticmethod
    def _edge(source, target, edge_type, path, line):
        value = f"{edge_type}:{source}:{target}:{path}:{line}"
        return {"identifier": "edge:" + hashlib.sha256(value.encode()).hexdigest()[:20],
                "source": source, "target": target, "edge_type": edge_type,
                "source_file": path, "source_line": line, "metadata": {}}


class RegistrationAnalyzer:
    def analyze(self, files):
        departments, registrations = [], []
        for item in files:
            for symbol in item.symbols:
                name = symbol.get("name", "")
                if name.endswith("Department"):
                    departments.append({"identifier": "symbol:" + hashlib.sha256(f"{item.relative_path}:{name}:{symbol.get('line')}".encode()).hexdigest()[:20],
                        "name": name, "type": "Department", "category": item.category,
                        "file": item.relative_path, "line": symbol.get("line"), "owner": item.identifier,
                        "confidence": "HIGH", "metadata": {}})
            if item.relative_path in {
                "A_02_MANAGERS/smart_dispatcher_v2.py", "A_02_MANAGERS/department_registry.py",
                "A_01_CORE/TaskExecutor/capability_executor.py",
            }:
                registrations.append({"source": item.identifier, "file": item.relative_path,
                                      "kind": "runtime" if "smart_dispatcher" in item.relative_path else "catalog"})
        return departments, registrations


class DependencyAnalyzer:
    def analyze(self, nodes, edges):
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[edge["source"]].add(edge["target"])
        cycles, visited, active = [], set(), []
        def visit(node):
            if node in active:
                cycle = active[active.index(node):] + [node]
                if cycle not in cycles: cycles.append(cycle)
                return
            if node in visited: return
            active.append(node)
            for target in sorted(adjacency[node]): visit(target)
            active.pop(); visited.add(node)
        for node in sorted(item["identifier"] for item in nodes): visit(node)
        incoming = Counter(edge["target"] for edge in edges)
        unused = [item["identifier"] for item in nodes if not incoming[item["identifier"]] and not adjacency[item["identifier"]]]
        return {"cycles": cycles, "unused": unused,
                "edge_type_counts": dict(Counter(edge["edge_type"] for edge in edges))}


class RuntimeAnalyzer:
    CHAIN = (
        ("runtime:user", "runtime:butler_os", "dispatch"),
        ("runtime:butler_os", "runtime:coordinator", "dispatch"),
        ("runtime:coordinator", "runtime:dispatcher", "dispatch"),
        ("runtime:dispatcher", "runtime:harness", "execute"),
        ("runtime:harness", "runtime:gateway", "execute"),
        ("runtime:gateway", "runtime:permission", "permission"),
        ("runtime:permission", "runtime:department", "execute"),
        ("runtime:department", "runtime:result", "return"),
    )
    def analyze(self, files):
        runtime_nodes = [{"identifier": identifier, "name": identifier.split(":", 1)[1],
            "type": "Runtime", "category": "runtime", "file": None, "line": None,
            "owner": None, "confidence": "HIGH", "metadata": {}}
            for identifier in sorted({value for edge in self.CHAIN for value in edge[:2]})]
        runtime_edges = [ImportAnalyzer._edge(source, target, edge_type, "runtime-contract", None)
                         for source, target, edge_type in self.CHAIN]
        return runtime_nodes, runtime_edges


class DuplicateDetector:
    def detect(self, nodes, edges):
        groups = []
        for field, reason in (("sha256", "identical_content"), ("name", "duplicate_name")):
            grouped = defaultdict(list)
            for node in nodes:
                value = node.get(field)
                if value: grouped[str(value)].append(node["identifier"])
            for value, identifiers in sorted(grouped.items()):
                if len(identifiers) > 1:
                    groups.append({"identifier": "duplicate:" + hashlib.sha256(f"{field}:{value}".encode()).hexdigest()[:20],
                        "locations": identifiers, "reason": reason, "evidence": {field: value},
                        "confidence": "HIGH" if field == "sha256" else "MEDIUM"})
        return groups
