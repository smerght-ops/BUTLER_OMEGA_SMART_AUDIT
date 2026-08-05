import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from A_04_AGENTS.ImageDepartment.runner import ImageDepartment

img = ImageDepartment()

result = img.execute("нарисуй слона")

print(result)
