from A_04_AGENTS.CodingDepartment.runner import CodingDepartment
from A_04_AGENTS.MemoryDepartment.runner import MemoryDepartment
from A_04_AGENTS.VisionDepartment.runner import VisionDepartment
from A_04_AGENTS.ImageDepartment.runner import ImageDepartment
from A_04_AGENTS.AudioDepartment.runner import AudioDepartment
from A_04_AGENTS.TextDepartment.runner import TextDepartment
from A_04_AGENTS.VideoDepartment.runner import VideoDepartment
from A_04_AGENTS.ArchiveDepartment.runner import ArchiveDepartment

deps = [
    CodingDepartment(),
    MemoryDepartment(),
    VisionDepartment(),
    ImageDepartment(),
    AudioDepartment(),
    TextDepartment(),
    VideoDepartment(),
    ArchiveDepartment(),
]

print("=== BUTLER OMEGA DEPARTMENT TEST ===")
for d in deps:
    print(f"[OK] {d.__class__.__name__}")