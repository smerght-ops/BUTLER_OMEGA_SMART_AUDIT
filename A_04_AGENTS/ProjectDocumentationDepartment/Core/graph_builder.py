# -*- coding: utf-8 -*-

import json
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
FACTS = ROOT / "facts"

FILES = [
    "calls.json",
    "paths.json",
    "configs.json"
]

graph = {
    "generated": datetime.now().isoformat(timespec="seconds"),
    "nodes": [],
    "sources": {}
}

for name in FILES:

    p = FACTS / name

    if not p.exists():
        continue

    data = json.loads(p.read_text(encoding="utf-8-sig"))

    graph["sources"][name] = data.get("count", 0)

    for r in data.get("records", []):

        graph["nodes"].append(r)

OUT = FACTS / "PROJECT_GRAPH.json"

OUT.write_text(
    json.dumps(
        graph,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8-sig"
)

print("="*70)
print("GRAPH BUILDER READY")
print("="*70)
print("Nodes :", len(graph["nodes"]))
print("Output:", OUT)
