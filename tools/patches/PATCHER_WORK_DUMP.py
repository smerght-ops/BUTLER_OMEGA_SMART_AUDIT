from pathlib import Path
import sys

P = Path("Inspector-Discovery_v2.py")

# Читаем с поддержкой BOM
code = P.read_text(encoding="utf-8-sig")
lines = code.splitlines()

def find_func(name):
    target = f"def {name}("
    for i, line in enumerate(lines):
        if line.startswith(target):
            start = i
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("def "):
                    end = j
                    break
            return start, end
    return None, None

collect_start, collect_end = find_func("collect_entity_evidence")
build_start, build_end = find_func("build_capability_cluster")

print("collect_entity_evidence:", collect_start, collect_end)
print("build_capability_cluster:", build_start, build_end)

if collect_start is None or build_start is None:
    print("ERROR: required function not found")
    sys.exit(1)

print("PATCHER READY")