from collections import Counter
from pathlib import Path

from A_03_ORCHESTRATION.repository_knowledge_gateway import list_repository_files

ROOT = Path(__file__).resolve().parents[2]
folder_counter = Counter()
python_counter = Counter()

for relative in list_repository_files(ROOT):
    parent = str(Path(relative).parent)
    folder_counter[parent] += 1
    if relative.lower().endswith(".py"):
        python_counter[parent] += 1

print("=" * 70)
print("BUTLER PROJECT MAP")
print("=" * 70)
print("\nTOP 30 folders by total files:\n")
for name, count in folder_counter.most_common(30):
    print(f"{count:6d}  {name}")
print("\nTOP 30 folders by Python files:\n")
for name, count in python_counter.most_common(30):
    print(f"{count:6d}  {name}")
