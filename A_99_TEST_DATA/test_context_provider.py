# -*- coding: utf-8 -*-

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pprint import pprint

from A_02_MANAGERS.ArchitectAgent.context_provider import ContextProvider

ctx = ContextProvider().build_context()

print("="*70)
print("UNIFIED CONTEXT TEST")
print("="*70)

print()

print("KEYS:")
for k in sorted(ctx.keys()):
    print(" -", k)

print()

print("FILES INDEXED :", ctx.get("indexed_files_count"))

pm = ctx.get("project_map", {})
print("PROJECT MAP   :", len(pm) if isinstance(pm, dict) else "ERROR")

ig = ctx.get("internal_graph", {})
print("INTERNAL GRAPH:", len(ig) if isinstance(ig, dict) else "ERROR")

ps = ctx.get("project_state", {})
print()

print("CURRENT STAGE:")
print(ps.get("current_stage"))

print()

print("MEMORY PREVIEW:")

mem = ctx.get("project_memory","")

print(mem[:1000])

print()
print("="*70)
