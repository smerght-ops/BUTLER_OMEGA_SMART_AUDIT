# -*- coding: utf-8 -*-
"""AST path resolver — uses RepositoryKnowledgeDepartment for file enumeration.

Uses the approved gateway-backed canonical Python file inventory.
"""

import ast
import json
from pathlib import Path
from datetime import datetime

from A_03_ORCHESTRATION.repository_knowledge_gateway import list_repository_files

ROOT = Path.cwd()
OUT = ROOT / "facts"
OUT.mkdir(exist_ok=True)

records = []


class Resolver(ast.NodeVisitor):

    def __init__(self, filename):
        self.file = filename

    def visit_Call(self, node):

        if isinstance(node.func, ast.Attribute):

            name = node.func.attr

            if name == "join":

                records.append({
                    "type": "os.path.join",
                    "file": self.file,
                    "line": node.lineno
                })

        self.generic_visit(node)

    def visit_BinOp(self, node):

        if isinstance(node.op, ast.Div):

            records.append({
                "type": "path_div",
                "file": self.file,
                "line": node.lineno
            })

        self.generic_visit(node)


py_files_rel = list_repository_files(ROOT, ".py")

for rel_path in py_files_rel:
    try:
        tree = ast.parse((ROOT / rel_path).read_text(encoding="utf-8-sig", errors="replace"))
    except Exception:
        continue

    Resolver(rel_path).visit(tree)

(OUT / "paths.json").write_text(
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
