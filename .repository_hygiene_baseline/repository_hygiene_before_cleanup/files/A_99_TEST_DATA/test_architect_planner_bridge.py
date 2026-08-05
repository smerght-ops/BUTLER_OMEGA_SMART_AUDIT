# -*- coding: utf-8 -*-

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from A_02_MANAGERS.ArchitectAgent.architect_agent import ArchitectAgent

print("="*70)
print("ARCHITECT -> PLANNER BRIDGE TEST")
print("="*70)

agent = ArchitectAgent()

result = agent.execute_goal("python version")

print("RESULT:", result)

print("="*70)
