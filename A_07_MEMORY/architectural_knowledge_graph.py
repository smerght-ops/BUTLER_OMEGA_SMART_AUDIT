# -*- coding: utf-8 -*-

"""
BUTLER OMEGA SMART
ROADMAP 6.0

Architectural Knowledge Graph
Stage 1.6
"""

import ast
from pathlib import Path

ROOT = Path(".")

graph = []

IGNORE = (
    "A_00_HISTORY",
    "A_00_ARCHIVE",
    "A_00_ARCHIVE_BACKUPS",
    "__pycache__"
)

for file in ROOT.rglob("*.py"):

    if any(x in file.parts for x in (
        "A_00_HISTORY",
        "A_00_ARCHIVE",
        "A_00_ARCHIVE_BACKUPS",
        "__pycache__"
    )):
        continue

    if any(part in file.parts for part in IGNORE):
        continue

    try:
        tree = ast.parse(file.read_text(encoding="utf-8"))

    except Exception as ex:
        print("SKIP:", file)
        print(type(ex).__name__, ex)
        continue

    module = file.relative_to(ROOT).as_posix()

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for n in node.names:

                graph.append({
                    "from": module,
                    "to": n.name,
                    "type": "import"
                })

        elif isinstance(node, ast.ImportFrom):

            if node.module:

                graph.append({
                    "from": module,
                    "to": node.module,
                    "type": "from"
                })

print("="*70)
print("ARCHITECTURAL KNOWLEDGE GRAPH")
print("="*70)

print("MODULE LINKS:", len(graph))

for g in graph[:40]:
    print(g)

print()
print("="*70)
print("QUERY TEST")
print("="*70)

TARGET="semantic_reasoning_engine_v2"

hits=0

for g in graph:

    if TARGET in g["to"]:
        hits+=1
        print(g["from"]," ---> ",g["to"])

print()
print("FOUND:",hits)

print()
print("="*70)
print("ALL A_07_MEMORY IMPORTS")
print("="*70)

for g in graph:
    if "A_07_MEMORY" in g["to"]:
        print(g)






