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

OUT_DIR = ROOT / "facts"
OUT_DIR.mkdir(exist_ok=True)

OUT_FILE = OUT_DIR / "calls.json"

class CallVisitor(ast.NodeVisitor):

    def __init__(self, filename):
        self.filename = filename
        self.calls = []

    def fullname(self, node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            left = self.fullname(node.value)
            if left:
                return left + "." + node.attr
        return None

    def literal(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        if getattr(ast, 'Str', None) and isinstance(node, ast.Str):
            return node.s
        if isinstance(node, ast.JoinedStr):
            return "<fstring>"
        if isinstance(node, ast.Name):
            return "<variable>"
        if isinstance(node, ast.Call):
            return "<call>"
        if isinstance(node, ast.BinOp):
            return "<concat>"
        return "<dynamic>"

    def evidence(self, typ, node, value):

        if isinstance(value, str) and not is_allowed(value.replace("\\","/")):
            return

        self.calls.append({
            "type": typ,
            "file": self.filename,
            "line": node.lineno,
            "value": value
        })

    def visit_Call(self, node):
        name = self.fullname(node.func)
        if name:
            arg = None
            if node.args:
                arg = self.literal(node.args[0])

            if name.startswith("subprocess."):
                self.evidence("subprocess", node, arg)
            elif name in ("os.system","os.startfile"):
                self.evidence("os", node, arg)
            elif name in ("importlib.import_module","__import__"):
                self.evidence("dynamic_import", node, arg)
            elif name.startswith("requests."):
                self.evidence("requests", node, arg)
            elif name.startswith("httpx."):
                self.evidence("httpx", node, arg)
            elif name == "open":
                self.evidence("open", node, arg)
            elif name.endswith(".open"):
                self.evidence("path_open", node, arg)
            elif name.endswith(".read_text"):
                self.evidence("read_text", node, arg)
            elif name.endswith(".write_text"):
                self.evidence("write_text", node, arg)
        self.generic_visit(node)

records = []

for py in ROOT.rglob("*.py"):

    rel_path = str(py.relative_to(ROOT)).replace("\\","/")

    # ЕДИНАЯ ТОЧКА ФИЛЬТРАЦИИ
    if not is_allowed(rel_path):
        continue

    try:
        text = py.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = py.read_text(
            encoding="utf-8-sig",
            errors="replace"
        )
    try:
        tree = ast.parse(text)
    except Exception:
        continue

    v = CallVisitor(rel_path)
    v.visit(tree)
    records.extend(v.calls)

OUT_FILE.write_text(
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
print("CALL GRAPH READY")
print("="*70)
print("Evidence :",len(records))
print("Output   :",OUT_FILE)


