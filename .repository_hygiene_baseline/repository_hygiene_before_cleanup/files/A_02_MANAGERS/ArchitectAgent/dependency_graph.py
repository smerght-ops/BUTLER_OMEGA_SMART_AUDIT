# -*- coding: utf-8 -*-

import ast
from pathlib import Path

from A_03_ORCHESTRATION.repository_knowledge_gateway import query_repository

SCAN_SCOPE = (
    "A_01_CORE",
    "A_02_MANAGERS",
    "A_07_CONFIG",
    "A_10_BUTLER_OS",
)

class DependencyGraph:

    def __init__(self, root=None):
        self.root = Path(root or Path.cwd())

    def _files(self):
        payload = query_repository(self.root, "list_files", filters={"type": "File", "extension": ".py"})
        for item in payload["data"]["matches"]:
            if any(item["file"].startswith(folder + "/") for folder in SCAN_SCOPE):
                yield self.root / item["file"]

    def build(self):

        graph = {}

        for py in self._files():

            rel = py.relative_to(self.root).as_posix()

            try:
                tree = ast.parse(
                    py.read_text(encoding="utf-8-sig")
                )
            except Exception:
                continue

            deps = []

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for a in node.names:

                        if a.name.startswith("A_"):
                            deps.append(a.name)

                elif isinstance(node, ast.ImportFrom):

                    module = node.module or ""

                    if node.level:

                        pkg = rel[:-3].replace("/", ".").split(".")[:-1]

                        pkg = pkg[:-node.level+1] if node.level <= len(pkg) else []

                        module = ".".join(pkg + module.split(".")) if module else ".".join(pkg)

                    if module.startswith("A_"):

                        deps.append(module)

            graph[rel] = sorted(set(deps))

        return graph


if __name__=="__main__":

    from pprint import pprint

    g = DependencyGraph().build()

    print("="*70)
    print("PROJECT DEPENDENCY GRAPH")
    print("="*70)

    pprint(g)

    print("="*70)
    print("MODULES :",len(g))
    print("EDGES   :",sum(len(v) for v in g.values()))
    print("="*70)
