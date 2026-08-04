# -*- coding: utf-8 -*-

import json
from pathlib import Path

from A_03_ORCHESTRATION.repository_knowledge_gateway import query_repository

ROOT = Path(__file__).resolve().parents[2]
canonical = query_repository(ROOT, "get_index")["data"]
nodes = canonical["nodes"]
result = {}

for node in nodes:
    if node.get("type") != "File" or not node.get("file", "").endswith(".py"):
        continue
    owned = [item for item in nodes if item.get("owner") == node["identifier"]]
    imports = [edge["target"] for edge in canonical["edges"]
               if edge.get("source") == node["identifier"] and edge.get("edge_type") == "imports"]
    result[node["file"]] = {
        "imports": sorted(set(imports)),
        "classes": sorted(item["name"] for item in owned if item.get("type") != "Function"),
        "functions": sorted(item["name"] for item in owned if item.get("type") == "Function"),
    }

out = ROOT / "A_07_CONFIG" / "dependency_map.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print("=" * 60)
print("PCR v3 COMPLETE")
print("=" * 60)
print("Files indexed :", len(result))
print("Saved to      :", out)
