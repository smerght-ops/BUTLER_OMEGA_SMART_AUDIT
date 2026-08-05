from pathlib import Path
import hashlib

ROOT = Path(".").resolve()
OUT = ROOT / "PROJECT_FULL_CONTEXT_PACK.md"

EXCLUDE_DIRS = {
    ".git","__pycache__",".venv","venv",
    "A_06_WORKSPACE","A_08_LOGS",
    "A_00_HISTORY","A_00_ARCHIVE_BACKUPS"
}

EXCLUDE_PARTS = {
    "Secrets",
    "OLYMPICS",
    "GENERATED_IMAGES",
    "Image_Checkpoints"
}

INCLUDE_EXT = {
    ".py",".json",".md",".txt",".ps1",".bat",".cmd",
    ".yaml",".yml",".toml",".ini"
}

def skip(p: Path):
    parts = set(p.parts)
    if parts & EXCLUDE_DIRS:
        return True
    if parts & EXCLUDE_PARTS:
        return True
    if p.suffix.lower() not in INCLUDE_EXT:
        return True
    if p.name == "PROJECT_FULL_CONTEXT_PACK.md":
        return True
    return False

files = [p for p in ROOT.rglob("*") if p.is_file() and not skip(p)]
files = sorted(files, key=lambda x: str(x).lower())

with OUT.open("w", encoding="utf-8") as out:
    out.write("# FULL PROJECT CONTEXT PACK — BUTLER_OMEGA_SMART\n\n")
    out.write(f"ROOT: {ROOT}\n\n")
    out.write("## FILE TREE\n\n")
    for p in files:
        rel = p.relative_to(ROOT)
        out.write(f"- {rel} ({p.stat().st_size} bytes)\n")

    out.write("\n\n## FILE CONTENTS\n\n")

    for p in files:
        rel = p.relative_to(ROOT)
        data = p.read_bytes()
        sha = hashlib.sha256(data).hexdigest()[:16]
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")

        out.write("\n\n---\n")
        out.write(f"## FILE: {rel}\n")
        out.write(f"SIZE: {len(data)} bytes\n")
        out.write(f"SHA256-16: {sha}\n\n")
        out.write("```text\n")
        out.write(text)
        out.write("\n```\n")

print("PACK CREATED:", OUT)
print("FILES:", len(files))
print("SIZE MB:", round(OUT.stat().st_size / 1024 / 1024, 2))
