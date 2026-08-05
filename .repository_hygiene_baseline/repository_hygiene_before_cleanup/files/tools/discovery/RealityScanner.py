#!/usr/bin/env python3
"""
RealityScanner — простой сканер для проверки существования подсистем.
Использует все артефакты (PhysicalMap, EntityMap, ImportMap, RegistrationAST, CallGraph, LinkMap, DependencyModel)
и отвечает на вопрос: есть ли уже в проекте то, что я ищу?
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path.cwd()

def load_artifact(name):
    """Загружает артефакт по имени."""
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
    """Ищет ключевое слово в путях файлов из PhysicalMap."""
    evidence = []
    if not physical_map:
        return evidence
    for item in physical_map.get("payload", []):
        rel_path = item.get("relative_path", "")
        if keyword.lower() in rel_path.lower():
            evidence.append(rel_path)
    return evidence

def search_in_entity_map(entity_map, keyword):
    """Ищет ключевое слово в именах классов и функций из EntityMap."""
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
    """Ищет ключевое слово в модулях импорта из ImportMap."""
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
    """Ищет ключевое слово в регистрациях из RegistrationAST."""
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
    """Ищет ключевое слово в вызываемых функциях из CallGraph."""
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
    """Ищет ключевое слово в связях из LinkMap."""
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
    """Ищет ключевое слово в узлах DependencyModel."""
    evidence = []
    if not dep_model:
        return evidence
    for node_id, node_info in dep_model.get("nodes", {}).items():
        if keyword.lower() in str(node_id).lower():
            evidence.append(f"node: {node_id}")
    return evidence

def main():
    if len(sys.argv) < 2:
        print("Usage: python RealityScanner.py <keyword>")
        sys.exit(1)

    keyword = sys.argv[1]

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

    # Собираем доказательства
    evidence = {}

    file_paths = search_in_file_paths(artifacts["PhysicalMap"], keyword)
    if file_paths:
        evidence["File paths"] = file_paths

    entity_evidence = search_in_entity_map(artifacts["EntityMap"], keyword)
    if entity_evidence["classes"]:
        evidence["Classes"] = entity_evidence["classes"]
    if entity_evidence["functions"]:
        evidence["Functions"] = entity_evidence["functions"]

    imports = search_in_import_map(artifacts["ImportMap"], keyword)
    if imports:
        evidence["Imports"] = imports

    registrations = search_in_registration_ast(artifacts["RegistrationAST"], keyword)
    if registrations:
        evidence["Registrations"] = registrations

    calls = search_in_call_graph(artifacts["CallGraph"], keyword)
    if calls:
        evidence["Calls"] = calls

    link_evidence = search_in_link_map(artifacts["LinkMap"], keyword)
    if link_evidence["source"]:
        evidence["Link sources"] = link_evidence["source"]
    if link_evidence["target"]:
        evidence["Link targets"] = link_evidence["target"]

    nodes = search_in_dependency_model(artifacts["DependencyModel"], keyword)
    if nodes:
        evidence["Dependency nodes"] = nodes

    # Выводим результат
    print("=" * 60)
    print(f"REALITY SCANNER: searching for '{keyword}'")
    print("=" * 60)

    if not evidence:
        print(f"No evidence found for '{keyword}'.")
    else:
        print(f"Evidence found for '{keyword}':")
        for category, items in evidence.items():
            print(f"\n{category}:")
            for item in items[:20]:  # покажем первые 20
                print(f"  - {item}")
            if len(items) > 20:
                print(f"  ... and {len(items) - 20} more")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
