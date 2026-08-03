# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CRITICAL_INFRASTRUCTURE = {
    "base_department.py": "Базовый контракт всех отделов BaseDepartment",
    "manifest_loader.py": "Загрузчик системного манифеста",
    "smart_dispatcher_v2.py": "Центральный маршрутизатор",
    "dispatcher_bridge_v2.py": "Связующий мост оркестрации",
    "model_registry.py": "Реестр локальных моделей"
}

def normalize_to_module(file_path_str: str) -> str:
    fixed = file_path_str.replace("/", os.sep).replace("\\", os.sep)
    p = Path(fixed)

    if p.is_absolute():
        try:
            p = p.relative_to(ROOT)
        except ValueError:
            return ""

    return ".".join(p.with_suffix("").parts)

def evaluate_risk_level(count: int, is_infra: bool) -> str:
    if is_infra:
        return "CRITICAL_INFRASTRUCTURE"

    if count <= 2:
        return "LOW"

    if count <= 5:
        return "MEDIUM"

    if count <= 10:
        return "HIGH"

    return "CRITICAL"

def analyze_file_impact(file_path_str: str):
    reverse_path = ROOT / "A_07_CONFIG" / "dependency_reverse.json"
    cache_path = ROOT / "A_07_CONFIG" / "impact_cache.json"

    if not reverse_path.exists():
        print("ERROR: dependency_reverse.json not found. Run project_guardian.py first.")
        raise SystemExit(1)

    reverse_graph = json.loads(reverse_path.read_text(encoding="utf-8"))

    target_module = normalize_to_module(file_path_str)
    filename = Path(file_path_str).name

    affected_modules = reverse_graph.get(target_module, [])
    affected_count = len(affected_modules)

    is_infra = filename in CRITICAL_INFRASTRUCTURE
    risk = evaluate_risk_level(affected_count, is_infra)

    requires_rollback = risk in {
        "HIGH",
        "CRITICAL",
        "CRITICAL_INFRASTRUCTURE"
    }

    cache_data = {
        "target_file": filename,
        "target_module": target_module,
        "risk_level": risk,
        "affected_count": affected_count,
        "affected_modules": affected_modules,
        "requires_rollback": requires_rollback
    }

    cache_path.write_text(
        json.dumps(cache_data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=" * 70)
    print("PROJECT IMPACT ANALYZER")
    print("=" * 70)
    print(f"FILE   : {filename}")
    print(f"MODULE : {target_module}")
    print(f"RISK   : {risk}")

    if is_infra:
        print(f"DETAIL : {CRITICAL_INFRASTRUCTURE[filename]}")

    print("-" * 70)
    print("AFFECTED MODULES:")

    if affected_modules:
        for mod in sorted(affected_modules):
            print(f"  -> {mod}")

    if not affected_modules:
        print("  NONE")

    print("-" * 70)
    print("RECOMMENDATION:")

    if requires_rollback:
        print("  CREATE ROLLBACK POINT BEFORE CHANGE")

    if not requires_rollback:
        print("  CHANGE ALLOWED IN SANDBOX")

    print("=" * 70)
    print(f"SAVED: {cache_path}")

if __name__ == "__main__":
    analyze_file_impact("A_04_AGENTS/base_department.py")