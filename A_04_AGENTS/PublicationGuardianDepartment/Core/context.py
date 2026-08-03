from __future__ import annotations

import subprocess
import tarfile
import zipfile
import hashlib
from dataclasses import dataclass, replace
from pathlib import Path

from ..Contracts.models import PublicationRequest


@dataclass(frozen=True)
class PublicationFile:
    path: str
    content: bytes
    text: str | None


@dataclass(frozen=True)
class PublicationContext:
    request: PublicationRequest
    files: tuple[PublicationFile, ...]
    source: str
    git_integrity_ok: bool
    registered_inspectors: frozenset[str]

    def for_file(self, item: PublicationFile) -> "PublicationContext":
        return replace(self, files=(item,))


def build_context(request: PublicationRequest, registered: frozenset[str]) -> PublicationContext:
    mode = request.publication_mode.casefold()
    if mode == "git":
        files = _git_index_files(request)
        return PublicationContext(request, files, "git-index", True, registered)
    paths = request.metadata.get("paths") or list(request.staged_files)
    if not paths:
        raise ValueError("No publication objects supplied")
    root = Path(request.repository_root).resolve()
    files = []
    for raw_path in paths:
        path = Path(raw_path)
        if not path.is_absolute():
            path = root / path
        path = path.resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise PermissionError(f"Publication object escapes repository_root: {raw_path}") from exc
        if not path.is_file():
            raise OSError(f"Publication object is unavailable: {raw_path}")
        if mode == "zip" or path.suffix.casefold() == ".zip":
            files.extend(_zip_files(path))
        elif mode == "tar" or path.name.casefold().endswith((".tar", ".tar.gz", ".tgz")):
            files.extend(_tar_files(path))
        else:
            files.append(_make_file(path.name, path.read_bytes()))
    if not files:
        raise ValueError("Publication object contains no files")
    return PublicationContext(request, tuple(sorted(files, key=lambda item: item.path)), "file-export", True, registered)


def _run_git(root: Path, args: list[str]) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False, timeout=30,
    )
    if process.returncode:
        error = process.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(error or "Git command failed")
    return process.stdout


def _git_index_files(request: PublicationRequest) -> tuple[PublicationFile, ...]:
    root = Path(request.repository_root).resolve()
    if not root.is_dir():
        raise OSError("repository_root is unavailable")
    index_path = Path(_run_git(root, ["rev-parse", "--git-path", "index"]).decode("utf-8", errors="strict").strip())
    if not index_path.is_absolute():
        index_path = root / index_path
    before = _file_digest(index_path.resolve())
    raw = _run_git(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"])
    names = [item.decode("utf-8", errors="strict") for item in raw.split(b"\0") if item]
    requested = set(request.staged_files)
    if requested and requested != set(names):
        raise RuntimeError("staged_files does not match the current Git index")
    files = []
    for name in sorted(names):
        content = _run_git(root, ["show", f":{name}"])
        files.append(_make_file(name, content))
    after = _file_digest(index_path.resolve())
    if before != after:
        raise RuntimeError("Git index changed during inspection")
    if not files:
        raise RuntimeError("Git index contains no publication files")
    return tuple(files)


def _zip_files(path: Path) -> list[PublicationFile]:
    result = []
    seen = set()
    with zipfile.ZipFile(path) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if not info.is_dir():
                name = _safe_member_name(info.filename, seen)
                result.append(_make_file(info.filename, archive.read(info)))
    return result


def _tar_files(path: Path) -> list[PublicationFile]:
    result = []
    seen = set()
    with tarfile.open(path, "r:*") as archive:
        for member in sorted(archive.getmembers(), key=lambda item: item.name):
            if member.isfile():
                _safe_member_name(member.name, seen)
                stream = archive.extractfile(member)
                if stream is None:
                    raise OSError(f"Cannot read TAR member: {member.name}")
                result.append(_make_file(member.name, stream.read()))
    return result


def _safe_member_name(raw: str, seen: set[str]) -> str:
    normalized = raw.replace("\\", "/")
    path = Path(normalized)
    if path.is_absolute() or normalized.startswith("/") or ".." in path.parts:
        raise PermissionError(f"Unsafe archive member path: {raw}")
    folded = normalized.casefold()
    if folded in seen:
        raise RuntimeError(f"Duplicate archive member path: {raw}")
    seen.add(folded)
    return normalized


def _file_digest(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise RuntimeError("Git index is unavailable") from exc


def _make_file(path: str, content: bytes) -> PublicationFile:
    if b"\0" in content[:8192]:
        text = None
    else:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = None
    return PublicationFile(path.replace("\\", "/"), content, text)
