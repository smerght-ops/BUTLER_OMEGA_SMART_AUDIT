"""Bounded deterministic repository discovery and Python AST extraction."""

import ast
import hashlib
import os
import re
import stat
from pathlib import Path

from .models import Diagnostic, FileRecord


class RepositoryScanner:
    MAX_TEXT_BYTES = 2 * 1024 * 1024
    TEXT_SUFFIXES = {".py", ".json", ".yaml", ".yml", ".md", ".ps1", ".bat", ".cmd"}
    ALWAYS_IGNORE = {".git", ".agents", ".codex", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules", ".venv", "venv", "env"}
    SENSITIVE = re.compile(r"(^|[._-])(env|token|secret|credential|cookie|password|passwd|private.?key|id_rsa|certificate)([._-]|$)", re.I)

    def __init__(self, root: Path, scope: dict | None = None):
        self.root = root.resolve()
        self.scope = dict(scope or {})
        categories = self.scope.get("categories", {})
        self.excluded_roots = {
            str(name).casefold()
            for category in ("archive", "generated", "ignore")
            for name in categories.get(category, []) or []
        }

    @staticmethod
    def _reparse(entry) -> bool:
        try:
            return entry.is_symlink() or bool(
                entry.stat(follow_symlinks=False).st_file_attributes
                & stat.FILE_ATTRIBUTE_REPARSE_POINT
            )
        except (AttributeError, OSError):
            return entry.is_symlink()

    def _category_map(self):
        mapping = {}
        for category, values in self.scope.get("categories", {}).items():
            for name in values or []:
                mapping[str(name).casefold()] = category
        return mapping

    def _classify(self, relative: str, mapping: dict) -> str:
        top = relative.split("/", 1)[0].casefold()
        if top in mapping:
            return mapping[top]
        return "UNKNOWN"

    def _walk(self):
        stack = [self.root]
        while stack:
            directory = stack.pop()
            try:
                entries = sorted(os.scandir(directory), key=lambda item: item.name.casefold())
            except OSError:
                continue
            for entry in entries:
                if self._reparse(entry):
                    continue
                if entry.is_dir(follow_symlinks=False):
                    if (entry.name not in self.ALWAYS_IGNORE
                            and entry.name.casefold() not in self.excluded_roots
                            and not entry.name.casefold().startswith(("backup", "restore", "snapshot", "checkpoint"))):
                        stack.append(Path(entry.path))
                elif entry.is_file(follow_symlinks=False):
                    yield Path(entry.path)

    def scan(self):
        records, diagnostics = [], []
        mapping = self._category_map()
        for path in self._walk():
            relative = path.relative_to(self.root).as_posix()
            try:
                size = path.stat().st_size
                raw = path.read_bytes() if size <= self.MAX_TEXT_BYTES else b""
            except OSError as error:
                diagnostics.append(Diagnostic(relative, "DEGRADED", type(error).__name__).to_dict())
                continue
            digest = hashlib.sha256(raw if raw else f"{relative}:{size}".encode()).hexdigest()
            encoding, symbols, imports, calls, metadata = "BINARY_OR_SKIPPED", (), (), (), {}
            sensitive = bool(self.SENSITIVE.search(path.name))
            if not sensitive and size <= self.MAX_TEXT_BYTES and path.suffix.casefold() in self.TEXT_SUFFIXES:
                try:
                    if raw.startswith(b"\xef\xbb\xbf"):
                        raise UnicodeError("UTF8_BOM_NOT_ALLOWED")
                    text = raw.decode("utf-8")
                    encoding = "UTF-8"
                    if path.suffix.casefold() == ".py":
                        tree = ast.parse(text, filename=relative)
                        symbol_items, import_items, call_items = [], [], []
                        for node in ast.walk(tree):
                            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                                symbol_items.append({"name": node.name, "kind": type(node).__name__, "line": node.lineno})
                            elif isinstance(node, ast.Import):
                                import_items.extend({"module": alias.name, "line": node.lineno} for alias in node.names)
                            elif isinstance(node, ast.ImportFrom):
                                import_items.append({"module": "." * node.level + (node.module or ""), "line": node.lineno})
                            elif isinstance(node, ast.Call):
                                try: call_items.append({"target": ast.unparse(node.func), "line": node.lineno})
                                except Exception: pass
                        symbols, imports, calls = tuple(symbol_items), tuple(import_items), tuple(call_items)
                except (UnicodeError, UnicodeDecodeError, SyntaxError) as error:
                    encoding = "INVALID_UTF8" if not isinstance(error, SyntaxError) else "UTF-8"
                    metadata = {"parse_error": f"{type(error).__name__}: {error}"}
                    diagnostics.append(Diagnostic(relative, "DEGRADED", type(error).__name__).to_dict())
            elif sensitive:
                metadata = {"redacted": True}
            identifier = "file:" + hashlib.sha256(relative.encode("utf-8")).hexdigest()[:20]
            module = ".".join(Path(relative).with_suffix("").parts) if path.suffix.casefold() == ".py" else None
            records.append(FileRecord(identifier, path.name, relative, self._classify(relative, mapping), size, digest, encoding, module, symbols, imports, calls, metadata))
        return tuple(records), tuple(diagnostics)
