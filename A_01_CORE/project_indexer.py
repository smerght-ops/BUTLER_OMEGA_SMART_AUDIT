import json
from pathlib import Path
from datetime import datetime

from A_03_ORCHESTRATION.repository_knowledge_gateway import query_repository

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "A_08_LOGS" / "PROJECT_INDEX"
OUT.mkdir(parents=True, exist_ok=True)

TEXT_EXT = {
    ".py", ".json", ".md", ".txt", ".bat", ".ps1",
    ".yml", ".yaml", ".ini", ".cfg", ".toml"
}


def main():
    payload = query_repository(ROOT, "get_index")
    canonical = payload["data"]
    file_nodes = [node for node in canonical["nodes"] if node.get("type") == "File"]
    files = []
    directories = set()
    for node in file_nodes:
        rel_path = node.get("file", "")
        extension = Path(rel_path).suffix.lower()
        metadata = node.get("metadata", {})
        files.append({
            "path": rel_path,
            "name": Path(rel_path).name,
            "ext": extension,
            "size": node.get("size", metadata.get("size", 0)),
            "mtime_ns": node.get("mtime_ns", metadata.get("mtime_ns", 0)),
            "sha256": node.get("sha256", ""),
            "category": node.get("category", "UNKNOWN"),
            "kind": "text" if extension in TEXT_EXT else "binary_or_data",
            "python": {
                "encoding": node.get("encoding", metadata.get("encoding")),
                "parse_error": metadata.get("parse_error"),
                "imports": metadata.get("imports", []),
                "classes": metadata.get("classes", []),
                "functions": metadata.get("functions", []),
            },
        })
        parent = Path(rel_path).parent
        while str(parent) not in ("", "."):
            directories.add(parent.as_posix())
            parent = parent.parent

    index = {
        "project": "BUTLER_OMEGA_SMART",
        "root": str(ROOT),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dirs_count": len(directories),
        "files_count": len(files),
        "source": "RepositoryKnowledgeDepartment",
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
