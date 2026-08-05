# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "A_07_CONFIG" / "dependency_map.json"
DST = ROOT / "A_07_CONFIG" / "dependency_internal.json"

KEEP = (
    "A_01_",
    "A_02_",
    "A_03_",
    "A_04_",
    "A_07_",
)

data = json.loads(SRC.read_text(encoding="utf-8"))

result = {}

for module, info in data.items():
    imports = info.get("imports", [])
    internal = [x for x in imports if x.startswith(KEEP)]
    result[module] = internal

DST.write_text(
    json.dumps(result, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("=" * 60)
print("BUTLER PCR v3.2 - INTERNAL GRAPH")
print("=" * 60)
print("Modules :", len(result))

edges = sum(len(v) for v in result.values())
print("Links   :", edges)

print()
print("Top internal modules:")
rank = {}

for values in result.values():
    for item in values:
        rank[item] = rank.get(item, 0) + 1

for name, cnt in sorted(rank.items(), key=lambda x: x[1], reverse=True)[:20]:
    print(f"{cnt:3d}  {name}")

print()
print("Saved:", DST)
