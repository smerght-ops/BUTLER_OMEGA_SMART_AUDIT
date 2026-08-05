import sys
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2

dispatcher = SmartDispatcherV2()
result = dispatcher.dispatch("нарисуй синего кита")

print()
print("=" * 70)
print("DISPATCH RESULT:")
if isinstance(result, dict):
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(result)
print("=" * 70)
print()
