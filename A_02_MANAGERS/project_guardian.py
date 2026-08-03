# -*- coding: utf-8 -*-

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCAN_DIRS = [
    "A_01_CORE",
    "A_02_MANAGERS",
    "A_03_ORCHESTRATION",
    "A_04_AGENTS"
]

graph = {}
reverse = {}

for folder in SCAN_DIRS:

    d = ROOT / folder

    if not d.exists():
        continue

    for py in d.rglob("*.py"):

        if "__pycache__" in py.parts:
            continue

        mod = ".".join(py.relative_to(ROOT).with_suffix("").parts)

        graph[mod] = []

for folder in SCAN_DIRS:

    d = ROOT / folder

    if not d.exists():
        continue

    for py in d.rglob("*.py"):

        if "__pycache__" in py.parts:
            continue

        mod = ".".join(py.relative_to(ROOT).with_suffix("").parts)

        try:

            tree = ast.parse(
                py.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            )

        except Exception:
            continue

        deps = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for n in node.names:

                    deps.append(n.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:

                    deps.append(node.module)

        deps = sorted(set(deps))

        graph[mod] = deps

        for dep in deps:

            reverse.setdefault(dep, [])

            if mod not in reverse[dep]:
                reverse[dep].append(mod)

cfg = ROOT / "A_07_CONFIG"
cfg.mkdir(exist_ok=True)

(graph_path := cfg / "dependency_map.json").write_text(
    json.dumps(graph, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

(reverse_path := cfg / "dependency_reverse.json").write_text(
    json.dumps(reverse, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("=" * 60)
print("PROJECT GUARDIAN")
print("=" * 60)
print("Modules :", len(graph))
print("Saved   :", graph_path)
print("Reverse :", reverse_path)