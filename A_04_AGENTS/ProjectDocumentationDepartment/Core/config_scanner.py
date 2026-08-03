# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path
from datetime import datetime

# Подключаем единый scope_loader
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))
from scope_loader import is_allowed

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

for f in ROOT.rglob("*"):

    if not f.is_file():
        continue

    rel_path = str(f.relative_to(ROOT)).replace("\\","/")

    # ЕДИНАЯ ТОЧКА ФИЛЬТРАЦИИ
    if not is_allowed(rel_path):
        continue

    name = f.name.lower()

    for k in KEYWORDS:

        if k in name:

            records.append({
                "file": rel_path,
                "keyword": k
            })

(OUT/"configs.json").write_text(
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

print("="*70)
print("CONFIG SCANNER READY")
print("="*70)
print("Configs :",len(records))
print("Output  :",OUT/"configs.json")
