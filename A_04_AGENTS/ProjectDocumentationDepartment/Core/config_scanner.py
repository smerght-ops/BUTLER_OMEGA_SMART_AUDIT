# -*- coding: utf-8 -*-
"""Config scanner — uses RepositoryKnowledgeDepartment for file enumeration.

Uses the approved gateway-backed canonical file inventory.
"""

import json
from pathlib import Path
from datetime import datetime

from A_03_ORCHESTRATION.repository_knowledge_gateway import list_repository_files

ROOT = Path.cwd()

OUT = ROOT / "facts"
OUT.mkdir(exist_ok=True)

records = []

KEYWORDS = [
    "passport",
    "project_state",
    "config",
    "settings",
    ".env"
]


def _matches_keywords(rel_path):
    """Check if a file path matches any config keyword."""
    name = Path(rel_path).name.lower()
    for k in KEYWORDS:
        if k in name:
            return True
    return False


all_files_rel = list_repository_files(ROOT)

for rel_path in all_files_rel:
    if _matches_keywords(rel_path):
        records.append({
            "file": rel_path,
            "keyword": next((k for k in KEYWORDS if k in Path(rel_path).name.lower()), "")
        })

(OUT / "configs.json").write_text(
    json.dumps(
        {
            "generated": datetime.now().isoformat(timespec="seconds"),
            "count": len(records),
            "records": records
        },
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8-sig"
)

print("=" * 70)
print("CONFIG SCANNER READY")
print("=" * 70)
print("Configs :", len(records))
print("Output  :", OUT / "configs.json")
