# -*- coding: utf-8 -*-

import json

from A_07_CONFIG.project_memory_loader import ProjectMemoryLoader

loader = ProjectMemoryLoader()

print("=" * 60)
print("BUILT FEATURES")
print("=" * 60)

print(
    json.dumps(
        loader.get_built_features(),
        indent=2,
        ensure_ascii=False
    )
)

print()
print("=" * 60)
print("CURRENT WORK")
print("=" * 60)

print(
    json.dumps(
        loader.get_current_work(),
        indent=2,
        ensure_ascii=False
    )
)

print()
print("=" * 60)
print("NEXT WORK")
print("=" * 60)

print(
    json.dumps(
        loader.get_next_work(),
        indent=2,
        ensure_ascii=False
    )
)
