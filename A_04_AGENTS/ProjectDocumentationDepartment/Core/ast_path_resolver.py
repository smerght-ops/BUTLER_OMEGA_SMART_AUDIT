# -*- coding: utf-8 -*-

import ast
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

class Resolver(ast.NodeVisitor):

    def __init__(self, filename):
        self.file = filename

    def visit_Call(self,node):

        if isinstance(node.func,ast.Attribute):

            name=node.func.attr

            if name=="join":

                records.append({
                    "type":"os.path.join",
                    "file":self.file,
                    "line":node.lineno
                })

        self.generic_visit(node)

    def visit_BinOp(self,node):

        if isinstance(node.op,ast.Div):

            records.append({
                "type":"path_div",
                "file":self.file,
                "line":node.lineno
            })

        self.generic_visit(node)

for py in ROOT.rglob("*.py"):

    rel_path = str(py.relative_to(ROOT)).replace("\\","/")

    # ЕДИНАЯ ТОЧКА ФИЛЬТРАЦИИ
    if not is_allowed(rel_path):
        continue

    try:
        tree=ast.parse(py.read_text(encoding="utf-8-sig",errors="replace"))
    except:
        continue

    Resolver(rel_path).visit(tree)

(OUT/"paths.json").write_text(
    json.dumps(
        {
            "generated":datetime.now().isoformat(timespec="seconds"),
            "count":len(records),
            "records":records
        },
        indent=2,
        ensure_ascii=False
    ),
    encoding="utf-8-sig"
)

print("="*70)
print("PATH RESOLVER READY")
print("="*70)
print("Evidence :",len(records))
print("Output   :",OUT/"paths.json")
