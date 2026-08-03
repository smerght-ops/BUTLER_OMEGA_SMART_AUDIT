import re

CODE_PATTERNS = [
    r"\bdef\s+\w+\s*\(",
    r"\bclass\s+\w+",
    r"\bimport\s+\w+",
    r"\bfrom\s+\w+",
    r"\bfunction\s+\w+\s*\(",
    r"\bconst\s+\w+\s*=",
    r"\blet\s+\w+\s*=",
    r"\bvar\s+\w+\s*=",
    r"\bSELECT\b.+\bFROM\b",
    r"\bINSERT\s+INTO\b",
    r"\bUPDATE\b.+\bSET\b",
    r"\bparam\s*\(",
    r"\bWrite-Host\b",
    r"\bGet-Content\b",
    r"[{};]{3,}",
]

CODE_EXTENSIONS = {
    ".py": "python",
    ".ps1": "powershell",
    ".bat": "batch",
    ".cmd": "batch",
    ".js": "javascript",
    ".ts": "typescript",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".sql": "sql",
    ".cpp": "cpp",
    ".c": "c",
    ".h": "c_header",
    ".hpp": "cpp_header",
    ".cs": "csharp",
    ".java": "java",
    ".php": "php",
    ".rb": "ruby",
    ".go": "go",
    ".rs": "rust",
    ".sh": "shell",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".xml": "xml",
}

def detect_language_by_extension(path):
    return CODE_EXTENSIONS.get(path.suffix.lower())

def looks_like_code(text: str) -> bool:
    if not text:
        return False

    sample = text[:5000]
    hits = 0

    for pattern in CODE_PATTERNS:
        if re.search(pattern, sample, re.IGNORECASE | re.DOTALL):
            hits += 1

    lines = [x for x in sample.splitlines() if x.strip()]
    if lines:
        indented = sum(1 for x in lines if x.startswith(("    ", "\t")))
        if indented / max(len(lines), 1) > 0.25:
            hits += 1

    return hits >= 2