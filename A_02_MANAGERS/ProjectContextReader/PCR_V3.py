# -*- coding: utf-8 -*-

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SKIP = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "A_00_HISTORY",
    "A_00_BACKUPS",
    "A_00_ARCHIVE_BACKUPS",
    "A_00_AVARIYKA",
    "A_01_CORE_BACKUP",
    "A_02_MANAGERS_BACKUP",
    "A_99_TEST_DATA",
}

result = {}

for py in ROOT.rglob("*.py"):

    if any(part in SKIP for part in py.parts):
        continue

    try:
        tree = ast.parse(py.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        continue

    imports = []
    classes = []
    functions = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

    rel = str(py.relative_to(ROOT))

    result[rel] = {
        "imports": sorted(set(imports)),
        "classes": sorted(classes),
        "functions": sorted(functions),
    }

out = ROOT / "A_07_CONFIG" / "dependency_map.json"
out.parent.mkdir(parents=True, exist_ok=True)

out.write_text(
    json.dumps(result, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("=" * 60)
print("PCR v3 COMPLETE")
print("=" * 60)
print("Files indexed :", len(result))
print("Saved to      :", out)
