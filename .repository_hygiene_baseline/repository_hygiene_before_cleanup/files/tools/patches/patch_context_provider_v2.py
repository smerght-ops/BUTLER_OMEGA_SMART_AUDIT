from pathlib import Path

p=Path(r"A_02_MANAGERS\ArchitectAgent\context_provider.py")

t=p.read_text(encoding="utf-8")

if "from A_07_CONFIG.project_state_v2 import ProjectState" not in t:
    t=t.replace(
        "import json",
        "import json\nfrom A_07_CONFIG.project_state_v2 import ProjectState\nfrom A_07_MEMORY.project_context_builder import ProjectContextBuilder"
    )

old="""    def __init__(self, root=None):
        self.root = Path(root) if root else Path.cwd()
"""

new="""    def __init__(self, root=None):
        self.root = Path(root) if root else Path.cwd()
        self.project_state = ProjectState()
        self.memory = ProjectContextBuilder()
"""

if old not in t:
    raise SystemExit("INIT BLOCK NOT FOUND")

t=t.replace(old,new)

anchor='''        context["project_map"] = self._read_json("A_07_CONFIG/dependency_map.json")
        context["internal_graph"] = self._read_json("A_07_CONFIG/dependency_internal.json")
        context["indexed_files_count"] = len(context["project_map"]) if isinstance(context["project_map"], dict) else 0
'''

insert=anchor+'''

        try:
            context["project_state"]=self.project_state.summary()
        except Exception as e:
            context["project_state"]={"error":str(e)}

        try:
            context["project_memory"]=self.memory.build_context()
        except Exception as e:
            context["project_memory"]=str(e)
'''

if anchor not in t:
    raise SystemExit("ANCHOR NOT FOUND")

t=t.replace(anchor,insert)

p.write_text(t,encoding="utf-8")

print("UNIFIED CONTEXT PATCH OK")
