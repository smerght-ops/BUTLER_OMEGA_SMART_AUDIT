import ast
from pathlib import Path

p = Path("A_02_MANAGERS/ArchitectAgent/architect_agent.py")
tree = ast.parse(p.read_text(encoding="utf-8"))

for n in ast.walk(tree):
    if isinstance(n, ast.Import):
        print("IMPORT FOUND:")
        for a in n.names:
            print("  ->", a.name)
    elif isinstance(n, ast.ImportFrom):
        print(f"FROM FOUND: level={n.level}, module={repr(n.module)}")
        for a in n.names:
            print("  ->", a.name)
