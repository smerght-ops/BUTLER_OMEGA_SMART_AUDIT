# -*- coding: utf-8 -*-

import json
from pathlib import Path

from A_03_ORCHESTRATION.repository_knowledge_gateway import query_repository

ROOT = Path(__file__).resolve().parent.parent
canonical = query_repository(ROOT, "get_index")["data"]
file_nodes = {node["identifier"]: node for node in canonical["nodes"] if node.get("type") == "File"}
graph = {node.get("module") or node["file"]: [] for node in file_nodes.values()}
reverse = {}

for edge in canonical["edges"]:
    if edge.get("edge_type") != "imports" or edge.get("source") not in file_nodes:
        continue
    source_node = file_nodes[edge["source"]]
    source = source_node.get("module") or source_node["file"]
    target = edge.get("target", "")
    graph[source].append(target)
    reverse.setdefault(target, []).append(source)

graph = {key: sorted(set(value)) for key, value in graph.items()}
reverse = {key: sorted(set(value)) for key, value in reverse.items()}
cfg = ROOT / "A_07_CONFIG"
cfg.mkdir(exist_ok=True)
(graph_path := cfg / "dependency_map.json").write_text(
    json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
)
(reverse_path := cfg / "dependency_reverse.json").write_text(
    json.dumps(reverse, ensure_ascii=False, indent=2), encoding="utf-8"
)

print("=" * 60)
print("PROJECT GUARDIAN")
print("=" * 60)
print("Modules :", len(graph))
print("Saved   :", graph_path)
print("Reverse :", reverse_path)
