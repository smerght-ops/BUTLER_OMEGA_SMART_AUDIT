# -*- coding: utf-8 -*-

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from A_07_CONFIG.recipe_schema import (
    SCHEMA_VERSION,
    RECIPE_CONTRACT,
    STEP_CONTRACT,
    ALLOWED_ACTIONS,
    ACTION_CONTRACTS,
)


@dataclass
class ValidationResult:
    valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class RecipeValidator:
    """
    Universal declarative Recipe Validator v1.0.
    Uses A_07_CONFIG.recipe_schema as the single source of truth.
    """

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root if project_root else Path(__file__).resolve().parents[1]
        self.project_root = self.project_root.resolve()

    def validate(self, recipe: dict) -> ValidationResult:
        errors = []
        warnings = []

        if not isinstance(recipe, dict):
            return ValidationResult(False, ["Recipe must be a dictionary."], [])

        ok, msg = self._check_contract(recipe, RECIPE_CONTRACT.get("required", {}))
        if not ok:
            return ValidationResult(False, [f"Global schema error: {msg}"], [])

        if recipe.get("schema_version") != SCHEMA_VERSION:
            return ValidationResult(
                False,
                [f"Version mismatch: expected {SCHEMA_VERSION}, got {recipe.get('schema_version')}"],
                []
            )

        for idx, step in enumerate(recipe.get("steps", [])):
            prefix = f"Step {idx}"

            if not isinstance(step, dict):
                errors.append(f"{prefix}: Step must be a dictionary.")
                continue

            ok, msg = self._check_contract(step, STEP_CONTRACT.get("required", {}))
            if not ok:
                errors.append(f"{prefix}: {msg}")
                continue

            action = step["action"]

            if action not in ALLOWED_ACTIONS:
                errors.append(f"{prefix}: Forbidden action '{action}'.")
                continue

            contract = ACTION_CONTRACTS.get(action, {})

            if "required" in contract:
                ok, msg = self._check_contract(step, contract["required"])
                if not ok:
                    errors.append(f"{prefix} ({action}): {msg}")
                    continue

            if "one_of" in contract:
                ok, msg = self._check_one_of(step, contract["one_of"])
                if not ok:
                    errors.append(f"{prefix} ({action}): {msg}")
                    continue

            if "payload_contract" in contract:
                payload = step.get("payload")
                ok, msg = self._check_contract(
                    payload,
                    contract["payload_contract"].get("required", {})
                )
                if not ok:
                    errors.append(f"{prefix} ({action}) payload: {msg}")
                    continue

            target = step.get("target")
            if target:
                target_path, msg = self._resolve_inside_project(target)
                if target_path is None:
                    errors.append(f"{prefix} ({action}): {msg}")
                    continue

                if "payload_contract" in contract:
                    ok, err, warn = self._check_patch_context(target_path, step)
                    if not ok:
                        errors.append(f"{prefix}: {err}")
                    if warn:
                        warnings.append(f"{prefix}: {warn}")

        return ValidationResult(len(errors) == 0, errors, warnings)

    def _check_contract(self, data: dict, required_specs: dict) -> Tuple[bool, str]:

        if not isinstance(data, dict):
            return False, "Contract target must be a dictionary."

        for key, expected_type in required_specs.items():

            if key not in data:
                return False, f"Missing required field: '{key}'"

            if not isinstance(data[key], expected_type):
                return False, (
                    f"Field '{key}' must be {expected_type.__name__}, "
                    f"got {type(data[key]).__name__}"
                )

        return True, ""

    def _check_one_of(self, data: dict, options: list) -> Tuple[bool, str]:

        matched = []

        for option in options:
            if not isinstance(option, dict) or len(option) != 1:
                return False, "Invalid one_of contract declaration."

            key, expected_type = next(iter(option.items()))

            if key in data:
                if not isinstance(data[key], expected_type):
                    return False, (
                        f"Field '{key}' must be {expected_type.__name__}, "
                        f"got {type(data[key]).__name__}"
                    )
                matched.append(key)

        if len(matched) != 1:
            allowed = [next(iter(option.keys())) for option in options]
            return False, (
                f"XOR violation: expected exactly one of {allowed}, "
                f"got {matched}"
            )

        return True, ""

    def _resolve_inside_project(self, target: str):

        try:
            target_path = (self.project_root / target).resolve()
            target_path.relative_to(self.project_root)
            return target_path, ""
        except Exception:
            return None, f"Security violation: target escapes project root: {target}"

    def _check_patch_context(self, target_path: Path, step: dict):

        if not target_path.exists():
            return False, f"Target file does not exist: {step.get('target')}", ""

        try:
            content = target_path.read_text(encoding="utf-8")
        except Exception as exc:
            return False, f"Cannot read target file: {exc}", ""

        old_text = step["payload"]["old"]
        new_text = step["payload"]["new"]

        if old_text not in content:
            if new_text in content:
                return False, "Patch already applied.", "Redundant patch detected."
            return False, "Context mismatch: old block not found in target file.", ""

        return True, "", ""


if __name__ == "__main__":

    print("=" * 70)
    print("UNIVERSAL RECIPE VALIDATOR v1.0 SELF-TEST")
    print("=" * 70)

    validator = RecipeValidator()

    test_file = validator.project_root / "test_universal_dummy.txt"
    test_file.write_text("Butler Engine Active\nTarget block active\n", encoding="utf-8")

    good_recipe = {
        "schema_version": "1.0",
        "task_id": "TEST_DECLARATIVE_OK",
        "steps": [
            {
                "action": "patch",
                "target": "test_universal_dummy.txt",
                "payload": {
                    "old": "Target block active",
                    "new": "Target block active\nSubmodule: OK",
                },
            },
            {
                "action": "execute",
                "module": "A_07_MEMORY.STAGE1_ACCEPTANCE",
            },
        ],
    }

    bad_recipe = {
        "schema_version": "1.0",
        "task_id": "TEST_DECLARATIVE_BAD",
        "steps": [
            {
                "action": "execute",
                "module": "A_01_CORE",
                "command": "format c:",
            },
            {
                "action": "patch",
                "target": "test_universal_dummy.txt",
                "payload": {
                    "old": 123,
                    "new": "Hack",
                },
            },
            {
                "action": "compile",
                "target": "../../../Windows/System32/cmd.exe",
            },
        ],
    }

    result = validator.validate(good_recipe)
    print("[GOOD] VALID:", result.valid)
    print("[GOOD] ERRORS:", result.errors)
    print("[GOOD] WARNINGS:", result.warnings)

    print("-" * 70)

    result = validator.validate(bad_recipe)
    print("[BAD] VALID:", result.valid)
    print("[BAD] ERRORS:")
    for error in result.errors:
        print(" -", error)
    print("[BAD] WARNINGS:", result.warnings)

    if test_file.exists():
        test_file.unlink()

    print("=" * 70)
