# -*- coding: utf-8 -*-

import ast
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from A_03_ORCHESTRATION.repository_knowledge_gateway import query_repository


class ContextProvider:
    """Query-focused, read-only architectural evidence for ArchitectAgent."""

    ARTIFACTS = (
        "Inspector0_PhysicalMap.json", "Inspector1_EntityMap.json",
        "Inspector2_ImportMap.json", "Inspector3_RegistrationAST.json",
        "Inspector4_CallGraph.json", "LinkMap.json", "DependencyModel.json",
        "UnifiedInspectorFacts.json", "CapabilityRegistry.json",
        "CAPABILITY_REGISTRY_V2.json", "AUTO_CAPABILITY_REGISTRY.json",
        "FullCapabilityRegistry.json", "Butler_CapabilityAudit.json",
        "A_00_ARCHITECTURE/BUTLER_CAPABILITY_AUDIT.json",
        "A_00_ARCHITECTURE/PROJECT_STATE.json", "A_07_CONFIG/project_passport.json",
        "A_07_CONFIG/project_registry.json", "A_99_TESTS/reports/latest_acceptance_report.json",
        "facts/PROJECT_ARCHITECTURE_KNOWLEDGE.json",
    )
    EXCLUDED_PARTS = {
        ".git", "__pycache__", ".venv", "venv", "A_00_RESTORE", "A_00_HISTORY",
        "A_00_LEGACY_ARCHIVE", "A_00_ARCHIVE_BACKUPS", "AUDIT_PACKS", "reports",
    }
    TOOL_MARKERS = (
        "inspector", "scanner", "analyzer", "audit", "capability", "registry",
        "evidence", "map", "graph", "discovery", "extractor",
    )

    def __init__(self, root=None):
        self.root = Path(root).resolve() if root else Path.cwd().resolve()
        self._python_cache = None

    def build_context(self, query=""):
        runtime = self._runtime_inventory()
        knowledge = self._knowledge_context(query, runtime)
        context = {
            "project_root": str(self.root), "query": str(query or ""),
            "project_state": self._project_state(), "runtime": runtime,
            "relevant_components": self._relevant_components(query, runtime),
            "architecture_artifacts": self._artifact_manifest(),
            "architectural_knowledge": knowledge,
            "discovery_knowledge": self._discovery_knowledge(),
            "acceptance": self._acceptance_summary(),
            "goals_registry": self._read_json("A_07_CONFIG/goals_registry.json"),
            "project_map": self._read_json("A_07_CONFIG/dependency_map.json"),
            "internal_graph": self._read_json("A_07_CONFIG/dependency_internal.json"),
            "task_registry_exists": (self.root / "A_07_CONFIG/task_registry.py").exists(),
            "butler_gate_exists": (self.root / "Butler_Gate.py").exists(),
        }
        context["indexed_files_count"] = knowledge.get("live_inventory", {}).get("files", 0)
        return context

    def _project_state(self):
        passport = self._read_json("A_07_CONFIG/project_passport.json")
        if not isinstance(passport, dict) or "error" in passport:
            return passport
        identity = passport.get("project_identity", {})
        return {
            "identity": identity, "current_stage": identity.get("current_stage", "UNKNOWN"),
            "roadmap": passport.get("roadmap_pointer", {}),
            "registry": passport.get("architecture_registry", {}),
            "proofs": passport.get("execution_proof_map", {}),
            "limitations": passport.get("known_limitations", {}),
        }

    def _runtime_inventory(self):
        dispatcher_rel = "A_02_MANAGERS/smart_dispatcher_v2.py"
        result = {"official_entry": "BUTLER_OS.py", "dispatcher": dispatcher_rel, "departments": []}
        try:
            tree = ast.parse((self.root / dispatcher_rel).read_text(encoding="utf-8-sig"))
        except (OSError, SyntaxError, UnicodeError) as exc:
            result["error"] = str(exc)
            return result
        imports = {}
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module:
                for item in node.names:
                    imports[item.asname or item.name] = (node.module, item.name)
        registered = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            owns = any(isinstance(target, ast.Attribute) and target.attr == "departments" for target in node.targets)
            if owns and isinstance(node.value, (ast.List, ast.Tuple)):
                registered.extend(item.func.id for item in node.value.elts
                                  if isinstance(item, ast.Call) and isinstance(item.func, ast.Name))
        for class_name in registered:
            module, imported_name = imports.get(class_name, (None, class_name))
            source = module.replace(".", "/") + ".py" if module else None
            info = {"class": imported_name, "registered": True, "runtime_reachable": True,
                    "source": source, "capabilities": [], "public_methods": [], "implementation_markers": []}
            if source:
                info.update(self._class_facts(source, imported_name))
            result["departments"].append(info)
        return result

    def _class_facts(self, relative_path, class_name):
        try:
            text = (self.root / relative_path).read_text(encoding="utf-8-sig")
            tree = ast.parse(text)
        except (OSError, SyntaxError, UnicodeError):
            return {}
        facts = {"capabilities": [], "public_methods": [], "implementation_markers": []}
        for node in tree.body:
            if not isinstance(node, ast.ClassDef) or node.name != class_name:
                continue
            facts["public_methods"] = [item.name for item in node.body
                                       if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("__")]
            for item in node.body:
                if isinstance(item, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CAPABILITIES" for t in item.targets):
                    try:
                        facts["capabilities"] = [str(entry) for entry in ast.literal_eval(item.value)]
                    except (ValueError, TypeError):
                        pass
        lowered = text.casefold()
        patterns = {"rename": ("переимен", "rename"), "move": ("перемест", "move"),
                    "copy": ("скопир", "copy"), "delete": ("удал", "delete"),
                    "create_folder": ("создай пап", "create_folder")}
        facts["implementation_markers"] = [name for name, markers in patterns.items()
                                             if any(marker in lowered for marker in markers)]
        return facts

    def _python_index(self):
        if self._python_cache is not None:
            return self._python_cache
        canonical = query_repository(self.root, "get_index")["data"]
        nodes = canonical["nodes"]
        edges = canonical["edges"]
        symbols_by_owner = {}
        for node in nodes:
            if node.get("type") == "File":
                continue
            symbols_by_owner.setdefault(node.get("owner"), []).append(node)
        rows = []
        for node in nodes:
            rel = node.get("file")
            if node.get("type") != "File" or not str(rel).endswith(".py"):
                continue
            if any(part in self.EXCLUDED_PARTS for part in Path(rel).parts):
                continue
            owned = symbols_by_owner.get(node.get("identifier"), [])
            related = [edge for edge in edges if edge.get("source") == node.get("identifier")]
            rows.append({"path": rel, "module": rel[:-3].replace("/", "."),
                         "classes": [item["name"] for item in owned if item.get("type") in {
                             "Class", "Department", "Manager", "Handler", "Engine", "Gateway", "Coordinator"
                         }],
                         "functions": [item["name"] for item in owned if item.get("type") == "Function"],
                         "imports": [edge.get("target", "") for edge in related if edge.get("edge_type") == "imports"],
                         "calls": [edge.get("target", "") for edge in related if edge.get("edge_type") == "calls"],
                         "registrations": [edge.get("target", "") for edge in related if "register" in edge.get("edge_type", "")],
                         "size": node.get("metadata", {}).get("size", 0)})
        self._python_cache = rows
        return rows

    @staticmethod
    def _query_terms(query):
        raw = re.findall(r"[A-Za-zА-Яа-яЁё0-9_.-]+", str(query or ""))
        stop = {"какие", "какой", "которая", "который", "существуют", "проект", "butler",
                "файлы", "классы", "модуля", "модуль", "компонент", "конкретный", "есть", "ли"}
        return [word.casefold() for word in raw if len(word) >= 3 and word.casefold() not in stop]

    def _knowledge_context(self, query, runtime):
        rows = self._python_index()
        all_files = query_repository(self.root, "list_files", filters={"type": "File"})["data"]["matches"]
        by_area = {}
        for item in all_files:
            rel = item["file"]
            rel_path = Path(rel)
            area = rel_path.parts[0] if rel_path.parts else "."
            by_area[area] = by_area.get(area, 0) + 1
        terms = self._query_terms(query)
        semantic_aliases = {
            "память": ("memory",), "памяти": ("memory",), "уровни": ("layer", "manager", "storage"),
            "безопасность": ("security", "guard", "validator", "policy"),
            "безопасности": ("security", "guard", "validator", "policy"),
            "инспекторы": ("inspector",), "инспектор": ("inspector",),
            "возможности": ("capability",), "capabilities": ("capability",),
        }
        expanded_terms = list(terms)
        for term in terms:
            expanded_terms.extend(semantic_aliases.get(term, ()))
        scored = []
        for row in rows:
            haystack = " ".join([row["path"], *row["classes"], *row["functions"]]).casefold()
            score = sum(3 if term in row["path"].casefold() else 2 if term in " ".join(row["classes"]).casefold() else 1
                        for term in expanded_terms if term in haystack)
            if score:
                scored.append((score, row))
        matches = [row for _, row in sorted(scored, key=lambda pair: (-pair[0], pair[1]["path"]))[:12]]
        target_names = set()
        for row in matches[:6]:
            target_names.update(name.casefold() for name in row["classes"])
            target_names.add(Path(row["path"]).stem.casefold())
            target_names.add(row["module"].casefold())
        callers, dependents = [], []
        for row in rows:
            if target_names and any(call.casefold() in target_names for call in row["calls"]):
                callers.append(row["path"])
            if target_names and any(any(target == imp.casefold() or target.endswith("." + imp.casefold()) or imp.casefold().endswith("." + target)
                                        for target in target_names) for imp in row["imports"]):
                dependents.append(row["path"])
        tool_rows = []
        for row in rows:
            stem = Path(row["path"]).stem.casefold()
            names = [*row["classes"], *row["functions"]]
            blob = " ".join([stem, *names]).casefold()
            kinds = [marker for marker in self.TOOL_MARKERS if marker in blob]
            if kinds:
                status = "OFFLINE" if row["path"].startswith(("AUDIT/", "A_09_TESTS/", "A_99_TESTS/")) or row["path"].count("/") == 0 else "ACTIVE_SOURCE"
                tool_rows.append({"path": row["path"], "kinds": kinds, "entities": names[:8], "status": status})
        artifacts = self._artifact_manifest()
        generated = [item for item in artifacts if item.get("exists")]
        registered_paths = {item.get("source") for item in runtime.get("departments", [])}
        offline_matches = [{"path": row["path"], "classification": "RUNTIME_REACHABLE" if row["path"] in registered_paths else "NOT_PROVEN_RUNTIME_REACHABLE"}
                           for row in matches]
        memory_components = [row["path"] for row in rows
                             if "memory" in row["path"].casefold() or "памят" in row["path"].casefold()]
        security_components = [row["path"] for row in rows
                               if any(marker in row["path"].casefold()
                                      for marker in ("security", "guard", "validator", "policy"))]
        coverage = [
            {"category": "physical_structure", "source": "live filesystem + Inspector0_PhysicalMap.json", "status": "CONNECTED", "note": "live inventory supersedes stale map counts"},
            {"category": "discovery_aggregation", "source": "facts/PROJECT_ARCHITECTURE_KNOWLEDGE.json", "status": "CONNECTED", "note": "Inspector-Discovery V3.1 factual manifest; live source remains authoritative"},
            {"category": "entities", "source": "live Python AST + Inspector1_EntityMap.json", "status": "CONNECTED"},
            {"category": "imports_calls_registrations_dependencies", "source": "live Python AST + Inspector2/3/4 + LinkMap/DependencyModel", "status": "CONNECTED", "note": "static evidence; dynamic calls remain unconfirmed"},
            {"category": "runtime_departments", "source": "smart_dispatcher_v2.py AST", "status": "CONNECTED"},
            {"category": "core_managers_agents", "source": "live Python AST", "status": "CONNECTED"},
            {"category": "memory_security_inspectors", "source": "live Python AST and tool inventory", "status": "CONNECTED"},
            {"category": "capabilities", "source": "runtime CAPABILITIES + capability registries", "status": "PARTIAL", "note": "registry claims are not execution proof"},
            {"category": "configuration_models_state", "source": "A_07_CONFIG + passport/project state", "status": "CONNECTED"},
            {"category": "acceptance_proof", "source": "latest_acceptance_report + passport proof map", "status": "CONNECTED"},
            {"category": "legacy_dead_offline", "source": "path and Runtime registration evidence", "status": "PARTIAL", "note": "absence from dispatcher proves only not registered there, not dead code"},
        ]
        return {
            "source_policy": "LIVE_SOURCE_FIRST; generated maps are supporting evidence and disclose freshness",
            "live_inventory": {"files": len(all_files), "python_files_parsed": len(rows), "areas": by_area},
            "coverage": coverage, "query_matches": matches, "relations": {"callers": sorted(set(callers))[:20], "dependents": sorted(set(dependents))[:20]},
            "tool_inventory": tool_rows[:160], "tool_inventory_total": len(tool_rows),
            "map_and_registry_artifacts": generated, "runtime_classification": offline_matches,
            "category_components": {
                "core": [row["path"] for row in rows if row["path"].startswith("A_01_CORE/")][:12],
                "managers": [row["path"] for row in rows if row["path"].startswith("A_02_MANAGERS/")][:12],
                "orchestration": [row["path"] for row in rows if row["path"].startswith("A_03_ORCHESTRATION/")][:12],
                "memory": memory_components[:16], "security": security_components[:16],
            },
            "known_limits": ["Static AST cannot prove every dynamic call or runtime use.",
                             "Generated Inspector maps are stale when their generated_utc predates live sources.",
                             "NOT_PROVEN_RUNTIME_REACHABLE is not equivalent to dead or legacy."],
        }

    def _relevant_components(self, query, runtime):
        words = set(self._query_terms(query))
        aliases = {"переименование": "rename", "переименовать": "rename", "файлов": "filesystem", "папок": "filesystem"}
        expanded = words | {aliases[word] for word in words if word in aliases}
        matches = []
        for item in runtime.get("departments", []):
            searchable = " ".join([item.get("class", ""), item.get("source", ""), *item.get("capabilities", []),
                                   *item.get("public_methods", []), *item.get("implementation_markers", [])]).casefold()
            score = sum(1 for word in expanded if len(word) >= 4 and word in searchable)
            if score:
                matches.append({**item, "match_score": score})
        return sorted(matches, key=lambda item: item["match_score"], reverse=True)[:8]

    def _artifact_manifest(self):
        manifest = []
        now = datetime.now(timezone.utc)
        for relative in self.ARTIFACTS:
            path = self.root / relative
            item = {"path": relative, "exists": path.is_file()}
            if path.is_file():
                stat = path.stat()
                item.update({"size": stat.st_size, "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()})
                data = self._read_json(relative)
                metadata = data.get("metadata", {}) if isinstance(data, dict) else {}
                generated = metadata.get("generated_utc") or metadata.get("generated")
                item.update({"schema": metadata.get("schema"), "generator": metadata.get("generator"), "generated_utc": generated})
                age = (now - datetime.fromtimestamp(stat.st_mtime, timezone.utc)).days
                item["freshness"] = "STALE" if age >= 2 and (relative.startswith("Inspector") or relative in {"LinkMap.json", "DependencyModel.json", "UnifiedInspectorFacts.json"}) else "AVAILABLE"
                stats = metadata.get("statistics", {})
                if stats:
                    item["statistics"] = stats
            manifest.append(item)
        return manifest

    def _acceptance_summary(self):
        data = self._read_json("A_99_TESTS/reports/latest_acceptance_report.json")
        if not isinstance(data, dict):
            return {}
        scenarios = data.get("scenarios") or data.get("results") or []
        proof = []
        if isinstance(scenarios, list):
            for row in scenarios[:80]:
                if isinstance(row, dict):
                    proof.append({key: row.get(key) for key in ("id", "name", "status", "route", "query") if key in row})
        return {"timestamp": data.get("timestamp"), "official_entry": data.get("official_entry"),
                "counts": data.get("counts", {}), "all_scenarios_passed": data.get("all_scenarios_passed"),
                "scenario_evidence": proof}

    def _discovery_knowledge(self):
        """Read the factual Inspector-Discovery manifest; live source remains authoritative."""
        data = self._read_json("facts/PROJECT_ARCHITECTURE_KNOWLEDGE.json")
        if not isinstance(data, dict) or data.get("status") != "FACTUAL_ONLY":
            return {"status": "UNAVAILABLE", "error": data.get("error") if isinstance(data, dict) else None}
        return {
            "source": "facts/PROJECT_ARCHITECTURE_KNOWLEDGE.json", "loaded": True,
            "status": data.get("status"), "version": data.get("version"),
            "generated": data.get("generated"), "generator": data.get("generator"),
            "role": data.get("role"), "sources": data.get("sources", {}),
            "summary": data.get("summary", {}), "facts": data.get("facts", {}),
        }

    def _read_json(self, relative):
        path = self.root / relative
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            return {"error": str(exc)}
