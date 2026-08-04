"""Architecture reports calculated only from a RepositoryIndex."""

from collections import Counter

from .analyzers import DependencyAnalyzer, DuplicateDetector


class ArchitectureReporter:
    def report(self, index, project_graph, dependency_graph, runtime_graph):
        duplicates = DuplicateDetector().detect(index.nodes, index.edges)
        dependencies = DependencyAnalyzer().analyze(index.nodes, index.edges)
        health = self._health(index, duplicates, dependencies)
        validations = self._validate(index, duplicates, dependencies, runtime_graph)
        return {"versions":{"schema":index.schema_version,"index":index.index_version,
                "repository":index.repository_version,"sources":dict(index.source_versions)},
            "production_components":[item for item in index.nodes if str(item.get("category")).casefold()=="production"],
            "engineering_components":[item for item in index.nodes if str(item.get("category")).casefold()=="engineering"],
            "runtime_entry_points":[item for item in index.nodes if item.get("name") in {"BUTLER_OS.py","START_BUTLER_OS.ps1"}],
            "duplicate_components":duplicates,"dependency_summary":dependencies,
            "import_summary":dict(Counter(edge["edge_type"] for edge in index.edges)),
            "registration_summary":{"departments":index.statistics.get("department_count",0),
                "sources":index.statistics.get("registration_source_count",0)},
            "architecture_health":health,"validation_results":validations,
            "repository_statistics":dict(index.statistics),
            "project_graph":{"nodes":len(project_graph["nodes"]),"edges":len(project_graph["edges"])},
            "dependency_graph":{"nodes":len(dependency_graph["nodes"]),"edges":len(dependency_graph["edges"])},
            "runtime_graph":{"nodes":len(runtime_graph["nodes"]),"edges":len(runtime_graph["edges"])}}

    @staticmethod
    def _health(index, duplicates, dependencies):
        broken = int(index.statistics.get("broken_import_count", 0))
        score = max(0, 100 - min(35, broken) - min(25, len(dependencies["cycles"]) * 5) - min(20, len(duplicates) // 10))
        return {"repository_health_score":score,"registration_health":100 if index.statistics.get("department_count") else 0,
            "dependency_health":max(0,100-len(dependencies["cycles"])*5),"runtime_health":100,
            "import_health":max(0,100-min(100,broken)),"permission_health":100,
            "architecture_stability":score,"duplicate_density":len(duplicates)/max(1,len(index.nodes)),
            "index_freshness":"CURRENT","repository_completeness":"DEGRADED" if index.diagnostics else "COMPLETE"}

    @staticmethod
    def _validate(index, duplicates, dependencies, runtime_graph):
        results = []
        def add(code, severity, evidence, affected, action):
            results.append({"code":code,"severity":severity,"evidence":evidence,
                "affected_components":affected,"suggested_engineering_action":action})
        if index.statistics.get("broken_import_count"):
            add("BROKEN_IMPORTS", "WARNING", {"count":index.statistics["broken_import_count"]}, [], "Review unresolved local imports.")
        if dependencies["cycles"]:
            add("CIRCULAR_DEPENDENCIES", "WARNING", {"cycles":dependencies["cycles"][:20]},
                sorted({item for cycle in dependencies["cycles"] for item in cycle}), "Review cycle ownership and contracts.")
        if duplicates:
            add("DUPLICATE_COMPONENTS", "INFO", {"count":len(duplicates)},
                sorted({item for group in duplicates for item in group["locations"]})[:200], "Classify before merge or archive.")
        edge_types = {edge["edge_type"] for edge in runtime_graph["edges"]}
        if "permission" not in edge_types:
            add("BROKEN_PERMISSION_PATH", "ERROR", {"edge_types":sorted(edge_types)}, [], "Restore Gateway to Permission execution edge.")
        entry_names = {item.get("name") for item in index.nodes}
        if "BUTLER_OS.py" not in entry_names:
            add("MISSING_RUNTIME_ENTRY_POINT", "ERROR", {"expected":"BUTLER_OS.py"}, [], "Restore or reclassify the official entry point.")
        return results
