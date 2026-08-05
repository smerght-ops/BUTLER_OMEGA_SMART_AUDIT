from pathlib import Path

p=Path(r"A_99_TEST_DATA\test_context_provider.py")

t=p.read_text(encoding="utf-8")

header="""import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

"""

t=t.replace(
    "# -*- coding: utf-8 -*-\n\n",
    "# -*- coding: utf-8 -*-\n\n"+header
)

p.write_text(t,encoding="utf-8")

print("TEST IMPORT FIXED")
