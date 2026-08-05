# -*- coding: utf-8 -*-

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAP_FILE = ROOT / "A_07_CONFIG" / "dependency_map.json"

if not MAP_FILE.exists():
    print("dependency_map.json not found")
    raise SystemExit(1)

data = json.loads(MAP_FILE.read_text(encoding="utf-8"))

reverse = {}

for module, info in data.items():
    imports = info.get("imports", [])
    for imp in imports:
        reverse.setdefault(imp, []).append(module)

ranking = sorted(
    reverse.items(),
    key=lambda x: len(x[1]),
    reverse=True
)

print("=" * 60)
print("BUTLER PCR v3.1 - CRITICAL MODULES")
print("=" * 60)

for module, users in ranking[:30]:
    print(f"{len(users):3d} <- {module}")

print()
print(f"Modules indexed : {len(data)}")
print(f"Referenced      : {len(reverse)}")
