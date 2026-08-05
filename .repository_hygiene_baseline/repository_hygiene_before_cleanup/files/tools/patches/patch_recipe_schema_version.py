from pathlib import Path

p=Path(r"A_07_CONFIG\recipe_schema.py")

t=p.read_text(encoding="utf-8")

if "SCHEMA_VERSION" not in t:

    insert='''SCHEMA_VERSION = "6.2"

'''

    t=t.replace(
        "from typing import List, Dict\n\n",
        "from typing import List, Dict\n\n"+insert
    )

    p.write_text(t,encoding="utf-8")

print("SCHEMA VERSION RESTORED")
