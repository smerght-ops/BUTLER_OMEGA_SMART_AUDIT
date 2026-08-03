from pathlib import Path
from collections import Counter
import os

ROOT = Path(__file__).resolve().parents[2]

folder_counter = Counter()
python_counter = Counter()

for current, dirs, files in os.walk(ROOT):

    dirs[:] = [
        d for d in dirs
        if d not in (
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "A_00_HISTORY",
            "A_00_BACKUPS",
            "A_00_ARCHIVE_BACKUPS",
            "A_00_AVARIYKA",
            "ROLLBACK_POINTS",
            "EMERGENCY_BEFORE_RESTORE"
        )
    ]

    rel = Path(current).relative_to(ROOT)

    folder_counter[str(rel)] += len(files)

    for f in files:
        if f.lower().endswith(".py"):
            python_counter[str(rel)] += 1

print("=" * 70)
print("BUTLER PROJECT MAP")
print("=" * 70)

print("\nTOP 30 folders by total files:\n")

for name, count in folder_counter.most_common(30):
    print(f"{count:6d}  {name}")

print("\nTOP 30 folders by Python files:\n")

for name, count in python_counter.most_common(30):
    print(f"{count:6d}  {name}")

