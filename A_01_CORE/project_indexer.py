import ast, json, hashlib, os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "A_08_LOGS" / "PROJECT_INDEX"
OUT.mkdir(parents=True, exist_ok=True)

SKIP_DIRS = {
    "__pycache__", ".git", ".venv", "venv", "env",
    "node_modules", ".mypy_cache", ".pytest_cache"
}

TEXT_EXT = {
    ".py", ".json", ".md", ".txt", ".bat", ".ps1",
    ".yml", ".yaml", ".ini", ".cfg", ".toml"
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_text_safe(path):
    for enc in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return path.read_text(encoding=enc), enc, None
        except Exception as e:
            last = str(e)
    return "", None, last

def analyze_py(path):
    text, enc, err = read_text_safe(path)
    info = {
        "encoding": enc,
        "parse_error": err,
        "imports": [],
        "classes": [],
        "functions": []
    }
    if err:
        return info

    try:
        tree = ast.parse(text)
    except Exception as e:
        info["parse_error"] = str(e)
        return info

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imports.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
        elif isinstance(node, ast.ClassDef):
            info["classes"].append(node.name)
        elif isinstance(node, ast.FunctionDef):
            info["functions"].append(node.name)

    info["imports"] = sorted(imports)
    return info

def main():
    files = []
    dirs = []

    for root, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        r = Path(root)
        rel_dir = str(r.relative_to(ROOT))
        dirs.append(rel_dir)

        for name in filenames:
            p = r / name
            rel = str(p.relative_to(ROOT))
            ext = p.suffix.lower()
            stat = p.stat()

            item = {
                "path": rel,
                "name": name,
                "ext": ext,
                "size": stat.st_size,
                "mtime": int(stat.st_mtime),
                "sha256": sha256_file(p),
                "kind": "text" if ext in TEXT_EXT else "binary_or_data"
            }

            if ext == ".py":
                item["python"] = analyze_py(p)

            files.append(item)

    index = {
        "project": "BUTLER_OMEGA_SMART",
        "root": str(ROOT),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dirs_count": len(dirs),
        "files_count": len(files),
        "files": sorted(files, key=lambda x: x["path"].lower())
    }

    (OUT / "PROJECT_INDEX.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    summary = []
    summary.append("# BUTLER_OMEGA_SMART PROJECT INDEX")
    summary.append("")
    summary.append(f"Generated: {index['generated_at']}")
    summary.append(f"Directories: {index['dirs_count']}")
    summary.append(f"Files: {index['files_count']}")
    summary.append("")
    summary.append("## Python modules")
    for f in index["files"]:
        if f["ext"] == ".py":
            py = f.get("python", {})
            summary.append(f"- {f['path']}")
            if py.get("classes"):
                summary.append(f"  - classes: {', '.join(py['classes'])}")
            if py.get("functions"):
                summary.append(f"  - functions: {', '.join(py['functions'][:20])}")
            if py.get("imports"):
                summary.append(f"  - imports: {', '.join(py['imports'][:20])}")
            if py.get("parse_error"):
                summary.append(f"  - ERROR: {py['parse_error']}")

    (OUT / "PROJECT_INDEX.md").write_text(
        "\n".join(summary),
        encoding="utf-8"
    )

    print("OK: индекс создан")
    print(OUT / "PROJECT_INDEX.json")
    print(OUT / "PROJECT_INDEX.md")

if __name__ == "__main__":
    main()
