# -*- coding: utf-8 -*-
"""Structural extractor — uses RepositoryKnowledgeDepartment for file enumeration.

Uses the approved gateway-backed canonical Python file inventory.
"""

import ast
import json
from pathlib import Path
from datetime import datetime

from A_03_ORCHESTRATION.repository_knowledge_gateway import list_repository_files

ROOT = Path.cwd()

EXCLUDED = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    "backup",
    "backups",
    "rollback",
    "rollbacks",
    "archive",
    "archives",
    "a_00_avariyka",
    "a_00_archive",
    "a_00_archive_backups",
    "a_00_history",
}

OUT = ROOT / "facts"
OUT.mkdir(exist_ok=True)

records = []


def ignored(path):
    parts = {p.lower() for p in path.parts}
    return any(x in parts for x in EXCLUDED)


class StructuralVisitor(ast.NodeVisitor):

    def __init__(self, filename):
        self.filename = filename
        self.current_class = None

    def visit_ClassDef(self, node):

        bases = []

        for b in node.bases:
            if isinstance(b, ast.Name):
                bases.append(b.id)
            elif isinstance(b, ast.Attribute):
                bases.append(b.attr)

        records.append({
            "type": "class",
            "file": self.filename,
            "line": node.lineno,
            "name": node.name,
            "bases": bases
        })

        old = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = old

    def visit_FunctionDef(self, node):

        records.append({
            "type": "method" if self.current_class else "function",
            "file": self.filename,
            "line": node.lineno,
            "class": self.current_class,
            "name": node.name
        })

        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef


py_files_rel = list_repository_files(ROOT, ".py")

for rel in py_files_rel:
    try:
        text = (ROOT / rel).read_text(
            encoding="utf-8-sig",
            errors="replace"
        )
        tree = ast.parse(text)
    except Exception:
        continue

    StructuralVisitor(
        str(Path(rel).relative_to(ROOT)).replace("\\", "/") if not Path(rel).is_absolute() else rel.replace("\\", "/")
    ).visit(tree)

(OUT / "structure.json").write_text(
    json.dumps(
        {
            "generated": datetime.now().isoformat(timespec="seconds"),
            "count": len(records),
            "records": records
        },
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8"
)

print("=" * 70)
print("STRUCTURAL EXTRACTOR READY")
print("=" * 70)
print("Evidence :", len(records))
print("Output   :", OUT / "structure.json")
