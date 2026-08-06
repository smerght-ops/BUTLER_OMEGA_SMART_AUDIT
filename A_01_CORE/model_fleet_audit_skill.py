"""Local model fleet audit governed by the existing SkillRuntime lifecycle."""

from __future__ import annotations

import ast
import hashlib
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from A_01_CORE.skill_runtime import SkillManager


MODEL_FLEET_AUDIT_SIGNATURE = (
    "model_locations.inspect",
    "model_metadata.collect",
    "model_missing.detect",
    "model_duplicates.detect",
    "evidence.collect",
)

MODEL_EXTENSIONS = {
    ".bin", ".ckpt", ".gguf", ".onnx", ".pt", ".pth",
    ".safetensors", ".tflite",
}


@dataclass(frozen=True)
class ConfiguredModelLocation:
    source: str
    path: str
    expected_files: tuple[str, ...] = ()


def discover_configured_locations(root: Path) -> list[ConfiguredModelLocation]:
    """Read model locations from existing engine configuration without import."""
    root = Path(root).resolve()
    relative = Path("A_03_ENGINES/Audio_Engine/whisper_engine.py")
    source = root / relative
    try:
        tree = ast.parse(source.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, SyntaxError):
        return []
    values = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in {"MODELS_PATH", "AVAILABLE_MODELS"}:
                try:
                    values[target.id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass
    configured = values.get("MODELS_PATH")
    if not isinstance(configured, str) or not configured.strip():
        return []
    model_path = Path(configured)
    if not model_path.is_absolute():
        model_path = root / model_path
    available = values.get("AVAILABLE_MODELS", [])
    expected = tuple(f"{name}.pt" for name in available if isinstance(name, str) and name)
    return [ConfiguredModelLocation(relative.as_posix(), str(model_path), expected)]


class ModelFleetAuditSkill:
    name = "model_fleet_audit_skill"
    signature = MODEL_FLEET_AUDIT_SIGNATURE

    def __init__(self, manager: SkillManager, root: Path | None = None,
                 locations: list[ConfiguredModelLocation] | None = None):
        self.manager = manager
        self.root = (root or Path(__file__).resolve().parents[1]).resolve()
        self.locations = list(locations) if locations is not None else discover_configured_locations(self.root)

    def propose(self, trace, provenance: str) -> dict:
        return self.manager.propose(
            "skill save model_fleet_audit_skill", self.signature, trace, provenance,
        )

    def approve(self, skill_id: str, approver: str) -> dict:
        return self.manager.approve(skill_id, approver)

    def execute(self) -> dict:
        active = self.manager.match_active(self.signature)
        if active is None:
            return self._result(False, "SKILL_NOT_ACTIVE", "INACTIVE", [], [], [], [])
        if not self.locations:
            return self._result(False, "MODEL_LOCATIONS_NOT_CONFIGURED", active["status"],
                                [], [], [], [])

        metadata = []
        missing = []
        errors = []
        location_results = []
        seen_paths = set()
        for location in self.locations:
            path = Path(location.path).resolve()
            entry = {**asdict(location), "path": str(path), "exists": path.exists()}
            location_results.append(entry)
            if not path.exists():
                missing.append({"path": str(path), "reason": "CONFIGURED_LOCATION_MISSING",
                                "source": location.source})
                continue
            for expected in location.expected_files:
                expected_path = path / expected if path.is_dir() else path.parent / expected
                if not expected_path.is_file():
                    missing.append({"path": str(expected_path), "reason": "EXPECTED_MODEL_MISSING",
                                    "source": location.source})
            candidates = [path] if path.is_file() else self._model_files(path)
            for model_path in candidates:
                resolved = str(model_path.resolve())
                if resolved in seen_paths:
                    continue
                seen_paths.add(resolved)
                try:
                    stat = model_path.stat()
                    metadata.append({
                        "path": resolved,
                        "name": model_path.name,
                        "extension": model_path.suffix.casefold(),
                        "size_bytes": stat.st_size,
                        "modified_ns": stat.st_mtime_ns,
                        "sha256": self._sha256(model_path),
                        "source": location.source,
                    })
                except OSError as exc:
                    errors.append({"path": resolved, "error": f"{type(exc).__name__}: {exc}"})

        by_digest = {}
        for model in metadata:
            by_digest.setdefault(model["sha256"], []).append(model["path"])
        duplicates = [
            {"sha256": digest, "paths": paths, "count": len(paths)}
            for digest, paths in sorted(by_digest.items()) if len(paths) > 1
        ]
        evidence = [
            {"source": "configured_locations", "verified": bool(self.locations),
             "count": len(self.locations)},
            {"source": "model_metadata", "verified": not errors,
             "count": len(metadata)},
            {"source": "missing_detection", "verified": True,
             "count": len(missing)},
            {"source": "duplicate_detection", "verified": True,
             "count": len(duplicates)},
        ]
        return self._result(not errors, "MODEL_METADATA_ERROR" if errors else None,
                            active["status"], location_results, metadata, missing,
                            duplicates, evidence=evidence, errors=errors)

    def _result(self, ok, error, lifecycle_status, locations, models, missing,
                duplicates, evidence=None, errors=None):
        health = "ERROR" if not ok else ("DEGRADED" if missing or duplicates else "PASS")
        return {
            "ok": bool(ok),
            "skill": self.name,
            "signature": list(self.signature),
            "lifecycle_status": lifecycle_status,
            "health": health,
            "summary": {
                "locations": len(locations), "models": len(models),
                "missing": len(missing), "duplicate_groups": len(duplicates),
                "errors": len(errors or []),
            },
            "locations": locations,
            "models": models,
            "missing": missing,
            "duplicates": duplicates,
            "evidence": list(evidence or []),
            "errors": list(errors or []),
            "error": error,
        }

    @staticmethod
    def _model_files(folder: Path) -> list[Path]:
        values = []
        for current, directories, files in os.walk(folder, followlinks=False):
            directories.sort()
            for name in sorted(files):
                path = Path(current) / name
                if path.suffix.casefold() in MODEL_EXTENSIONS:
                    values.append(path)
        return values

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()
