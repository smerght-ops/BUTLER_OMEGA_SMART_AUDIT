from pathlib import Path

p=Path(r"A_02_MANAGERS\ArchitectAgent\context_provider.py")

t=p.read_text(encoding="utf-8")

old="""        return {
            "project_root": str(self.root),
            "goals_registry": self._read_json("A_07_CONFIG/goals_registry.json"),
            "recipe_schema": self._read_text("A_07_CONFIG/recipe_schema.py"),
            "task_registry_exists": (self.root / "A_07_CONFIG/task_registry.py").exists(),
            "butler_gate_exists": (self.root / "Butler_Gate.py").exists(),
        }"""

new="""        context = {
            "project_root": str(self.root),
            "goals_registry": self._read_json("A_07_CONFIG/goals_registry.json"),
            "recipe_schema": self._read_text("A_07_CONFIG/recipe_schema.py"),
            "task_registry_exists": (self.root / "A_07_CONFIG/task_registry.py").exists(),
            "butler_gate_exists": (self.root / "Butler_Gate.py").exists(),
        }

        context["project_map"] = self._read_json("A_07_CONFIG/dependency_map.json")
        context["internal_graph"] = self._read_json("A_07_CONFIG/dependency_internal.json")
        context["indexed_files_count"] = len(context["project_map"]) if isinstance(context["project_map"], dict) else 0

        return context"""

if old not in t:
    raise SystemExit("PATCH TARGET NOT FOUND")

p.write_text(
    t.replace(old,new),
    encoding="utf-8"
)

print("CONTEXT BRIDGE OK")
