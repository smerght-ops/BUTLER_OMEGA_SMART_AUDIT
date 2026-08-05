#!/usr/bin/env python3
# InspectorKnowledgeLayer.py
# READ ONLY. Только поиск упоминаний. Без записи, без pip, без subprocess.

import sys
import re
from pathlib import Path

MAX_FILE_SIZE = 10 * 1024 * 1024

TEXT_EXT = {
    ".txt", ".md", ".json", ".yml", ".yaml",
    ".ini", ".cfg", ".py", ".ps1", ".bat", ".cmd"
}

IGNORE_DIRS = {
    "__pycache__", ".git", "venv", ".venv", "env",
    "node_modules", "chroma_db", "dist", "build",
    "A_00_ARCHIVE_BACKUPS", "ROLLBACK_POINTS",
    "EMERGENCY_BEFORE_RESTORE"
}

IGNORE_EXT = {
    ".pyc", ".pyo", ".dll", ".exe",
    ".7z", ".zip", ".rar", ".bin", ".dat"
}

INTERNAL_KNOWLEDGE_DIRS = [
    "A_00_ARCHITECTURE",
    "A_07_CONFIG",
    "A_08_LOGS"
]

EXTERNAL_KNOWLEDGE_DIRS = [
    r"C:\Users\KOS\Desktop\Работа с батлером файлы\Docs",
    r"C:\Users\KOS\Desktop\Работа с батлером файлы\Data"
]

HISTORY_DIRS = [
    "A_08_LOGS",
    "A_00_ARCHITECTURE",
    "A_07_MEMORY",
    "A_07_CONFIG"
]

def ignored(p: Path) -> bool:
    if any(part in IGNORE_DIRS for part in p.parts):
        return True
    return p.suffix.lower() in IGNORE_EXT

def safe_read(p: Path) -> str:
    try:
        if not p.exists() or not p.is_file():
            return ""
        if ignored(p):
            return ""
        if p.suffix.lower() not in TEXT_EXT:
            return ""
        if p.stat().st_size > MAX_FILE_SIZE:
            return ""

        raw = p.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return ""

def make_patterns(query: str):
    q = query.strip()
    words = [w for w in re.split(r"\s+", q) if len(w) > 2]

    patterns = []

    if q:
        patterns.append(re.compile(re.escape(q), re.IGNORECASE))

    joined = "".join(words)
    snake = "_".join(w.lower() for w in words)

    if len(joined) > 2:
        patterns.append(re.compile(re.escape(joined), re.IGNORECASE))
    if len(snake) > 2:
        patterns.append(re.compile(re.escape(snake), re.IGNORECASE))

    # ВАЖНО: отдельные слова слишком шумные.
    # Runtime Registry НЕ должен ловить RuntimeError.
    return patterns

def search_roots(query: str, roots):
    patterns = make_patterns(query)
    result = {}

    for base in roots:
        base = Path(base)
        if not base.exists():
            continue

        for f in base.rglob("*"):
            text = safe_read(f)
            if not text:
                continue

            if not any(p.search(text) for p in patterns):
                continue

            lines = text.splitlines()
            snippets = []

            for i, line in enumerate(lines):
                if any(p.search(line) for p in patterns):
                    a = max(0, i - 1)
                    b = min(len(lines), i + 2)
                    frag = " | ".join(lines[a:b])[:400]
                    snippets.append(f"line {i+1}: {frag}")
                    if len(snippets) >= 5:
                        break

            try:
                rel = str(f.relative_to(Path.cwd()))
            except Exception:
                rel = str(f)

            result[rel] = snippets

    return result

def print_block(title: str, data: dict):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(f"FILES: {len(data)}")

    if not data:
        print("(нет совпадений)")
        return

    for path, snippets in sorted(data.items()):
        print(f"- {path} ({len(snippets)} fragments)")
        for s in snippets[:2]:
            print(f"  {s}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python InspectorKnowledgeLayer.py <query>")
        sys.exit(1)

    root = Path.cwd()
    query = sys.argv[1]

    internal_roots = [root / d for d in INTERNAL_KNOWLEDGE_DIRS]
    external_roots = [Path(d) for d in EXTERNAL_KNOWLEDGE_DIRS]
    history_roots = [root / d for d in HISTORY_DIRS]

    print_block("PROJECT KNOWLEDGE / INTERNAL", search_roots(query, internal_roots))
    print_block("PROJECT KNOWLEDGE / LEGACY DOCS", search_roots(query, external_roots))
    print_block("PROJECT HISTORY / SAFE", search_roots(query, history_roots))

if __name__ == "__main__":
    main()
