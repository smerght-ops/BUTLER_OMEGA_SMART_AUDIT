# -*- coding: utf-8 -*-

import json
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
FACTS = ROOT / "facts"

FILES = {
    "imports": ROOT / "PROJECT_FACTS_IMPORTS.json",
    "calls": FACTS / "calls.json",
    "paths": FACTS / "paths.json",
    "configs": FACTS / "configs.json",
    "structure": FACTS / "structure.json"
}

report = {
    "generated": datetime.now().isoformat(timespec="seconds"),
    "version": "1.0",
    "status": "FACTUAL_ONLY",
    "sources": {},
    "summary": {},
    "evidence": {}
}

for name, path in FILES.items():

    if not path.exists():
        report["sources"][name] = {
            "exists": False
        }
        continue

    data = json.loads(path.read_text(encoding="utf-8-sig"))

    report["sources"][name] = {
        "exists": True,
        "file": str(path.relative_to(ROOT)).replace("\\","/")
    }

    report["evidence"][name] = data

    if isinstance(data, dict):

        if "count" in data:
            report["summary"][name] = data["count"]

        elif "python_imports" in data:
            report["summary"][name] = len(data["python_imports"])

        else:
            report["summary"][name] = len(data)

OUT = FACTS / "PROJECT_EVIDENCE.json"

OUT.write_text(
    json.dumps(
        report,
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8-sig"
)

print("="*70)
print("EVIDENCE BUILDER READY")
print("="*70)

for k,v in report["summary"].items():
    print(f"{k:12} : {v}")

print("="*70)
print("Output :", OUT)
