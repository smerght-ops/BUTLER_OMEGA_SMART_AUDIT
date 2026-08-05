#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

ROOT = Path.cwd()
OUT_JSON = ROOT / "CAPABILITY_REGISTRY_V2.json"
OUT_MD = ROOT / "CAPABILITY_REGISTRY_V2.md"

FILES = {
    "physical": "Inspector0_PhysicalMap.json",
    "entity": "Inspector1_EntityMap.json",
    "import": "Inspector2_ImportMap.json",
    "registration": "Inspector3_RegistrationAST.json",
    "call": "Inspector4_CallGraph.json",
    "link": "LinkMap.json",
    "dependency": "DependencyModel.json",
}

CAPABILITIES = {
    "PROJECT_MEMORY": {
        "title": "Память проекта",
        "need_any": [
            "MemoryFacadeV2", "MemoryOrchestrator", "SemanticMemory",
            "MemoryReplay", "ProjectHistory", "USER_MEMORY.md",
            "session_history.jsonl"
        ]
    },
    "SMART_ROUTING": {
        "title": "Маршрутизация запросов",
        "need_any": [
            "SmartDispatcherV2", "DispatcherBridge", "dispatcher_bridge_v2.py",
            "RouterIntegration", "ProviderManager", "DepartmentRegistry"
        ]
    },
    "IMAGE_GENERATION": {
        "title": "Генерация изображений",
        "need_any": [
            "ImageDepartment", "VisionDepartment", "VisionEngine",
            "ComfyUIBridge", "generate_image", "check_comfyui"
        ]
    },
    "TEXT_AND_CODING": {
        "title": "Текстовый и кодовый департаменты",
        "need_any": [
            "TextDepartment", "CodingDepartment", "CodeHandler",
            "DeepSeek", "Codestral"
        ]
    },
    "SEARCH_AND_REFERENCE": {
        "title": "Поиск, каталог и resolver",
        "need_any": [
            "CatalogManager", "ReferenceResolver", "HybridResolver",
            "SearchDepartment", "SemanticSearchEngine", "rebuild_search_index"
        ]
    },
    "EXECUTION_ENGINE": {
        "title": "Исполнение задач и рецептов",
        "need_any": [
            "TaskRunner", "RecipeExecutor", "RecipeBuilder",
            "RecipeValidator", "ExecutionPolicy", "ExecutorFactory",
            "ExecutionRegistry"
        ]
    },
    "PROJECT_PASSPORT": {
        "title": "Паспорт и состояние проекта",
        "need_any": [
            "project_passport.json", "ProjectPassportLoader",
            "PassportCommandHandler", "passport_summary",
            "get_passport_string"
        ]
    },
    "GUARDIANS": {
        "title": "Стражи и защитные контуры",
        "need_any": [
            "A_09_GUARDIANS", "genie_guardian.ps1",
            "FrozenCoreGuard", "IntegrationTestGuard",
            "memory_guardian", "run_guardian"
        ]
    },
    "AUDIT_PIPELINE": {
        "title": "Инспекторский аудит проекта",
        "need_any": [
            "Inspector0_PhysicalMap.json",
            "Inspector1_EntityMap.json",
            "Inspector2_ImportMap.json",
            "Inspector3_RegistrationAST.json",
            "Inspector4_CallGraph.json",
            "LinkMap.json",
            "DependencyModel.json"
        ]
    },
    "BUTLER_OS": {
        "title": "Butler OS / рабочий контур",
        "need_any": [
            "A_10_BUTLER_OS", "ButlerOSAdapter",
            "ButlerInteractiveChat", "ButlerSystem"
        ]
    },
    "AGENT_DEPARTMENTS": {
        "title": "Агентные департаменты",
        "need_any": [
            "BaseDepartment", "ArchiveDepartment", "AudioDepartment",
            "DocumentsDepartment", "MemoryDepartment", "VideoDepartment",
            "ProjectDocumentationDepartment"
        ]
    },
    "ARCHITECTURE_GOVERNANCE": {
        "title": "Архитектурное управление",
        "need_any": [
            "ARCHITECTURE_LOCK.json", "architecture_manifest.json",
            "RuntimeCapabilityRegistry", "GoalsRegistryDiscoveryAgent",
            "RegistryValidator", "ManifestLoader"
        ]
    }
}

def load_json(path):
    p = ROOT / path
    if not p.exists():
        return None
    for enc in ("utf-8", "utf-8-sig"):
        try:
            return json.loads(p.read_text(encoding=enc))
        except Exception:
            pass
    return None

def collect_search_blob():
    parts = []

    for rel in FILES.values():
        data = load_json(rel)
        if data:
            parts.append(json.dumps(data, ensure_ascii=False))

    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue

        s = str(p)
        if "\\__pycache__\\" in s or "\\.git\\" in s or "\\venv\\" in s.lower():
            continue
        if "A_00_AVARIYKA" in s or "A_00_HISTORY" in s or "A_00_ARCHIVE_BACKUPS" in s:
            continue

        if p.suffix.lower() in [".py", ".json", ".md", ".ps1", ".txt"]:
            try:
                rel = str(p.relative_to(ROOT))
                parts.append(rel)
                txt = p.read_text(encoding="utf-8", errors="ignore")
                parts.append(txt[:5000])
            except Exception:
                pass

    return "\n".join(parts)

def find_evidence(blob, markers):
    found = []
    low = blob.lower()

    for m in markers:
        if m.lower() in low:
            found.append(m)

    return found

def main():
    blob = collect_search_blob()

    registry = {
        "metadata": {
            "schema": "capability_registry",
            "version": "2.0",
            "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "root": str(ROOT)
        },
        "capabilities": []
    }

    for cap_id, spec in CAPABILITIES.items():
        evidence = find_evidence(blob, spec["need_any"])
        score = len(evidence)
        total = len(spec["need_any"])

        if score == 0:
            status = "MISSING"
        elif score < max(2, total // 3):
            status = "PARTIAL"
        else:
            status = "LOCKED"

        registry["capabilities"].append({
            "id": cap_id,
            "title": spec["title"],
            "status": status,
            "evidence_count": score,
            "required_markers": total,
            "evidence": evidence,
            "do_not_build_again": status == "LOCKED"
        })

    OUT_JSON.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")

    md = []
    md.append("# BUTLER CAPABILITY REGISTRY V2\n")
    md.append("## Что уже есть и что нельзя строить повторно\n")

    for cap in registry["capabilities"]:
        mark = "✅" if cap["status"] == "LOCKED" else ("⚠️" if cap["status"] == "PARTIAL" else "❌")
        md.append(f"## {mark} {cap['title']}")
        md.append(f"- id: `{cap['id']}`")
        md.append(f"- status: `{cap['status']}`")
        md.append(f"- evidence: `{cap['evidence_count']}` / `{cap['required_markers']}`")
        md.append(f"- do_not_build_again: `{cap['do_not_build_again']}`")
        if cap["evidence"]:
            md.append("- доказательства:")
            for e in cap["evidence"]:
                md.append(f"  - `{e}`")
        md.append("")

    md.append("## DO NOT BUILD AGAIN\n")
    for cap in registry["capabilities"]:
        if cap["do_not_build_again"]:
            md.append(f"- {cap['title']} / `{cap['id']}`")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    locked = sum(1 for c in registry["capabilities"] if c["status"] == "LOCKED")
    partial = sum(1 for c in registry["capabilities"] if c["status"] == "PARTIAL")
    missing = sum(1 for c in registry["capabilities"] if c["status"] == "MISSING")

    print("STATUS  : SUCCESS")
    print(f"JSON    : {OUT_JSON.name}")
    print(f"REPORT  : {OUT_MD.name}")
    print(f"LOCKED  : {locked}")
    print(f"PARTIAL : {partial}")
    print(f"MISSING : {missing}")

if __name__ == "__main__":
    main()
