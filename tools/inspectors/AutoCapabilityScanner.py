#!/usr/bin/env python3
"""
AutoCapabilityScanner — автоматически строит реестр возможностей проекта.
Использует все артефакты и семантические маркеры для группировки доказательств.
Не требует ручных списков.
"""

import json
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path.cwd()
OUT_JSON = ROOT / "AUTO_CAPABILITY_REGISTRY.json"
OUT_MD = ROOT / "AUTO_CAPABILITY_REGISTRY.md"

def load_artifact(name):
    filenames = {
        "PhysicalMap": "Inspector0_PhysicalMap.json",
        "EntityMap": "Inspector1_EntityMap.json",
        "ImportMap": "Inspector2_ImportMap.json",
        "RegistrationAST": "Inspector3_RegistrationAST.json",
        "CallGraph": "Inspector4_CallGraph.json",
        "LinkMap": "LinkMap.json",
        "DependencyModel": "DependencyModel.json",
    }
    path = ROOT / filenames.get(name, "")
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return None

def search_in_file_paths(physical_map, keyword):
    evidence = []
    if not physical_map:
        return evidence
    for item in physical_map.get("payload", []):
        rel_path = item.get("relative_path", "")
        if keyword.lower() in rel_path.lower():
            evidence.append(rel_path)
    return evidence

def search_in_entity_map(entity_map, keyword):
    evidence = {"classes": [], "functions": []}
    if not entity_map:
        return evidence
    for entry in entity_map.get("payload", []):
        file_id = entry["id"]
        for cls in entry.get("classes", []):
            if keyword.lower() in cls["name"].lower():
                evidence["classes"].append(f"{cls['name']} (file: {file_id})")
        for func in entry.get("functions", []):
            if keyword.lower() in func["name"].lower():
                evidence["functions"].append(f"{func['name']} (file: {file_id})")
    return evidence

def search_in_import_map(import_map, keyword):
    evidence = []
    if not import_map:
        return evidence
    for entry in import_map.get("payload", []):
        file_id = entry["id"]
        for imp in entry.get("imports", []):
            module = imp.get("module", "")
            if keyword.lower() in module.lower():
                evidence.append(f"{module} (file: {file_id})")
    return evidence

def search_in_registration_ast(reg_map, keyword):
    evidence = []
    if not reg_map:
        return evidence
    for entry in reg_map.get("payload", []):
        file_id = entry["id"]
        for reg in entry.get("registrations", []):
            func = reg.get("function", "")
            if keyword.lower() in func.lower():
                evidence.append(f"{func} (file: {file_id})")
    return evidence

def search_in_call_graph(call_graph, keyword):
    evidence = []
    if not call_graph:
        return evidence
    for entry in call_graph.get("payload", []):
        file_id = entry["id"]
        for call in entry.get("calls", []):
            callee = call.get("callee", "")
            if keyword.lower() in callee.lower():
                evidence.append(f"{callee} (file: {file_id})")
    return evidence

def search_in_link_map(link_map, keyword):
    evidence = {"source": [], "target": []}
    if not link_map:
        return evidence
    for link in link_map.get("payload", []):
        source = link.get("source")
        target = link.get("target")
        if source and keyword.lower() in str(source).lower():
            evidence["source"].append(f"{source} (type: {link['type']})")
        if target and keyword.lower() in str(target).lower():
            evidence["target"].append(f"{target} (type: {link['type']})")
    return evidence

def search_in_dependency_model(dep_model, keyword):
    evidence = []
    if not dep_model:
        return evidence
    for node_id, node_info in dep_model.get("nodes", {}).items():
        if keyword.lower() in str(node_id).lower():
            evidence.append(f"node: {node_id}")
    return evidence

# Расширенный список семантических маркеров
MARKERS = [
    "memory", "semantic", "history", "change_request",
    "dispatcher", "router", "bridge", "provider",
    "image", "vision", "artist", "comfy",
    "runner", "executor", "task", "recipe", "policy",
    "search", "catalog", "reference", "resolver",
    "passport", "lock", "registry", "manifest", "guardian",
    "inspector", "map", "builder", "linkmap", "dependency",
    "core", "orchestrator", "bootstrap", "kernel",
    "department", "agent",
    "storage", "store", "archive",
    "log", "logger", "report",
    "config", "schema",
    "genie", "watch",
    "runtime", "loop",
    "chat", "message", "event",
    "validator", "validate", "check",
    "generate", "generator",
    "workflow", "pipeline",
    "contract", "interface",
    "adapter", "bridge", "factory", "builder"
]

def main():
    # Загружаем артефакты
    artifacts = {
        "PhysicalMap": load_artifact("PhysicalMap"),
        "EntityMap": load_artifact("EntityMap"),
        "ImportMap": load_artifact("ImportMap"),
        "RegistrationAST": load_artifact("RegistrationAST"),
        "CallGraph": load_artifact("CallGraph"),
        "LinkMap": load_artifact("LinkMap"),
        "DependencyModel": load_artifact("DependencyModel"),
    }

    # Собираем доказательства для каждого маркера
    capability_evidence = {}
    for marker in MARKERS:
        evidence = {}
        file_paths = search_in_file_paths(artifacts["PhysicalMap"], marker)
        if file_paths:
            evidence["file_paths"] = file_paths
        entity_evidence = search_in_entity_map(artifacts["EntityMap"], marker)
        if entity_evidence["classes"]:
            evidence["classes"] = entity_evidence["classes"]
        if entity_evidence["functions"]:
            evidence["functions"] = entity_evidence["functions"]
        imports = search_in_import_map(artifacts["ImportMap"], marker)
        if imports:
            evidence["imports"] = imports
        registrations = search_in_registration_ast(artifacts["RegistrationAST"], marker)
        if registrations:
            evidence["registrations"] = registrations
        calls = search_in_call_graph(artifacts["CallGraph"], marker)
        if calls:
            evidence["calls"] = calls
        link_evidence = search_in_link_map(artifacts["LinkMap"], marker)
        if link_evidence["source"]:
            evidence["link_sources"] = link_evidence["source"]
        if link_evidence["target"]:
            evidence["link_targets"] = link_evidence["target"]
        nodes = search_in_dependency_model(artifacts["DependencyModel"], marker)
        if nodes:
            evidence["dependency_nodes"] = nodes
        if evidence:
            # Считаем общее количество доказательств
            total_evidence = sum(len(v) for v in evidence.values())
            capability_evidence[marker] = {
                "evidence": evidence,
                "total_evidence": total_evidence
            }

    # Фильтруем только те, у которых достаточно доказательств (например, >= 5)
    locked_capabilities = {}
    for marker, info in capability_evidence.items():
        if info["total_evidence"] >= 5:
            locked_capabilities[marker] = info

    # Генерируем отчёт
    md_lines = []
    md_lines.append("=" * 60)
    md_lines.append("AUTO CAPABILITY REGISTRY")
    md_lines.append("=" * 60)
    md_lines.append("")
    md_lines.append(f"Total capabilities detected: {len(locked_capabilities)}")
    md_lines.append("")
    md_lines.append("## LOCKED CAPABILITIES")
    md_lines.append("The following capabilities have sufficient evidence and are considered implemented:")
    for marker, info in sorted(locked_capabilities.items(), key=lambda x: x[1]["total_evidence"], reverse=True):
        md_lines.append(f"### {marker.title()}")
        md_lines.append(f"- Evidence count: {info['total_evidence']}")
        for category, items in info["evidence"].items():
            md_lines.append(f"- {category}:")
            for item in items[:5]:
                md_lines.append(f"  - {item}")
            if len(items) > 5:
                md_lines.append(f"  ... and {len(items) - 5} more")
        md_lines.append("")
    md_lines.append("## DO NOT BUILD AGAIN")
    md_lines.append("Do not rebuild any of the above capabilities.")
    md_lines.append("")

    # Сохраняем JSON
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(locked_capabilities, f, ensure_ascii=False, indent=2)

    # Сохраняем MD
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))

    print("STATUS  : SUCCESS")
    print(f"JSON    : {OUT_JSON.name}")
    print(f"REPORT  : {OUT_MD.name}")
    print(f"CAPABILITIES: {len(locked_capabilities)}")

if __name__ == "__main__":
    main()
