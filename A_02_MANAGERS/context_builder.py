# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAX_FILE_CHARS = 60000
MAX_PACKAGE_CHARS = 240000

def module_to_path(module_name: str) -> Path:
    return ROOT / (module_name.replace(".", "/") + ".py")

def read_limited(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return f"# READ_ERROR: {exc}"

    if len(text) <= MAX_FILE_CHARS:
        return text

    head = text[:MAX_FILE_CHARS]
    return head + "\n\n# FILE_TRUNCATED_BY_CONTEXT_BUILDER\n"

def build_minimal_context():
    cache_path = ROOT / "A_07_CONFIG" / "impact_cache.json"
    out_path = ROOT / "A_07_CONFIG" / "llm_context_package.md"
    manifest_path = ROOT / "A_07_CONFIG" / "llm_context_manifest.json"

    if not cache_path.exists():
        print("ERROR: impact_cache.json not found. Run impact_analyzer.py first.")
        raise SystemExit(1)

    cache = json.loads(cache_path.read_text(encoding="utf-8"))

    target_file = cache.get("target_file", "")
    target_module = cache.get("target_module", "")
    risk_level = cache.get("risk_level", "")
    affected_modules = cache.get("affected_modules", [])
    affected_count = cache.get("affected_count", 0)
    requires_rollback = cache.get("requires_rollback", False)

    files_added = []
    files_missing = []
    package = []

    package.append("# BUTLER OMEGA — LLM CONTEXT PACKAGE")
    package.append("")
    package.append("## IMPACT SUMMARY")
    package.append(f"- Target file: `{target_file}`")
    package.append(f"- Target module: `{target_module}`")
    package.append(f"- Risk level: `{risk_level}`")
    package.append(f"- Affected count: `{affected_count}`")
    package.append(f"- Requires rollback: `{requires_rollback}`")
    package.append("")
    package.append("---")
    package.append("")

    modules = []

    if target_module:
        modules.append(("TARGET", target_module))

    for mod in sorted(set(affected_modules)):
        modules.append(("AFFECTED", mod))

    total_chars = 0

    for role, mod in modules:
        path = module_to_path(mod)

        if not path.exists():
            files_missing.append(str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path))
            continue

        rel = path.relative_to(ROOT).as_posix()
        code = read_limited(path)

        block = []
        block.append(f"## {role}: {mod}")
        block.append(f"Path: `{rel}`")
        block.append("")
        block.append("```python")
        block.append(code)
        block.append("```")
        block.append("")
        block.append("---")
        block.append("")

        block_text = "\n".join(block)

        if total_chars + len(block_text) > MAX_PACKAGE_CHARS:
            package.append("## CONTEXT_LIMIT_REACHED")
            package.append(f"Skipped remaining modules after `{mod}`.")
            package.append("")
            break

        package.append(block_text)
        total_chars += len(block_text)

        files_added.append({
            "role": role,
            "module": mod,
            "path": rel,
            "chars": len(code)
        })

    final_text = "\n".join(package)

    out_path.write_text(final_text, encoding="utf-8")

    manifest = {
        "target_file": target_file,
        "target_module": target_module,
        "risk_level": risk_level,
        "affected_count": affected_count,
        "requires_rollback": requires_rollback,
        "max_file_chars": MAX_FILE_CHARS,
        "max_package_chars": MAX_PACKAGE_CHARS,
        "package_chars": len(final_text),
        "files_added": files_added,
        "files_missing": files_missing,
        "output": str(out_path)
    }

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=" * 70)
    print("CONTEXT BUILDER v1")
    print("=" * 70)
    print(f"Target    : {target_file}")
    print(f"Risk      : {risk_level}")
    print(f"Added     : {len(files_added)} files")
    print(f"Missing   : {len(files_missing)} files")
    print(f"Size      : {len(final_text)} chars")
    print(f"Saved     : {out_path}")
    print(f"Manifest  : {manifest_path}")
    print("=" * 70)

if __name__ == "__main__":
    build_minimal_context()