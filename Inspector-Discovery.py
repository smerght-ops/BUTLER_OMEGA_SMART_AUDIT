#!/usr/bin/env python3
"""
UltimateRealityDiscovery (any) — полный поиск по проекту для запрошенной capability.
Собирает все доказательства из всех артефактов: файлы, классы, функции, импорты,
вызовы, регистрации, связи, JSON, паспорты, манифесты. Группирует в единую capability.
Использует логику OR для ключевых слов.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict, deque

ROOT = Path.cwd()

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

def find_entities_by_keywords(keywords, entity_map, physical_map):
    """Находит сущности, чьи имена содержат хотя бы одно ключевое слово."""
    entities = set()
    for entry in entity_map.get("payload", []):
        file_id = entry["id"]
        file_path = None
        if physical_map:
            for item in physical_map["payload"]:
                if str(item["id"]) == str(file_id):
                    file_path = item["relative_path"]
                    break
        for cls in entry.get("classes", []):
            name = cls["name"]
            if any(kw.lower() in name.lower() for kw in keywords):
                entities.add((name, "class", file_id, file_path))
        for func in entry.get("functions", []):
            name = func["name"]
            if any(kw.lower() in name.lower() for kw in keywords):
                entities.add((name, "function", file_id, file_path))
    return entities

def collect_entity_evidence(entity_name, artifacts):
    evidence = defaultdict(set)
    if artifacts["ImportMap"]:
        for entry in artifacts["ImportMap"]["payload"]:
            for imp in entry.get("imports", []):
                module = imp.get("module", "")
                if entity_name.lower() in module.lower():
                    evidence["imports"].add((module, entry["id"]))
    if artifacts["CallGraph"]:
        for entry in artifacts["CallGraph"]["payload"]:
            for call in entry.get("calls", []):
                callee = call.get("callee", "")
                if entity_name.lower() in callee.lower():
                    evidence["calls"].add((callee, entry["id"]))
    if artifacts["RegistrationAST"]:
        for entry in artifacts["RegistrationAST"]["payload"]:
            for reg in entry.get("registrations", []):
                func = reg.get("function", "")
                if entity_name.lower() in func.lower():
                    evidence["registrations"].add((func, entry["id"]))
    if artifacts["LinkMap"]:
        for link in artifacts["LinkMap"]["payload"]:
            source = str(link.get("source", ""))
            target = str(link.get("target", ""))
            if entity_name.lower() in source.lower() or entity_name.lower() in target.lower():
                evidence["links"].add((json.dumps(link, ensure_ascii=False, sort_keys=True), None))
    if artifacts["DependencyModel"]:
        for node_id in artifacts["DependencyModel"].get("nodes", {}).keys():
            if entity_name.lower() in str(node_id).lower():
                evidence["dependency_nodes"].add((str(node_id), None))
    return evidence

def build_capability_cluster(keywords, artifacts):
    entity_map = artifacts["EntityMap"]
    physical_map = artifacts["PhysicalMap"]
    if not entity_map:
        return None
    entities = find_entities_by_keywords(keywords, entity_map, physical_map)
    if not entities:
        return None

    all_evidence = defaultdict(set)
    all_files = set()
    for entity, etype, file_id, file_path in entities:
        all_files.add((file_id, file_path))
        ev = collect_entity_evidence(entity, artifacts)
        for key in ev:
            all_evidence[key].update(ev[key])

    # Строим граф связей для объединения сущностей
    graph = defaultdict(set)
    if artifacts["LinkMap"]:
        for link in artifacts["LinkMap"]["payload"]:
            source = str(link.get("source", ""))
            target = str(link.get("target", ""))
            if any(entity == source or entity == target for entity, _, _, _ in entities):
                graph[source].add(target)
                graph[target].add(source)
    if artifacts["DependencyModel"]:
        for edge in artifacts["DependencyModel"].get("edges", []):
            source = str(edge.get("source", ""))
            target = str(edge.get("target", ""))
            if any(entity == source or entity == target for entity, _, _, _ in entities):
                graph[source].add(target)
                graph[target].add(source)

    start_nodes = {entity for entity, _, _, _ in entities}
    visited = set()
    cluster_nodes = set()
    for node in start_nodes:
        if node not in visited:
            queue = deque([node])
            while queue:
                n = queue.popleft()
                if n in visited:
                    continue
                visited.add(n)
                if n in start_nodes or any(n in graph.get(s, set()) for s in start_nodes):
                    cluster_nodes.add(n)
                    for neighbor in graph.get(n, []):
                        if neighbor not in visited:
                            queue.append(neighbor)

    final_entities = set()
    for entity, etype, file_id, file_path in entities:
        if entity in cluster_nodes:
            final_entities.add((entity, etype, file_id, file_path))

    return final_entities, all_evidence, all_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python UltimateRealityDiscovery.py <query>")
        sys.exit(1)
    query = sys.argv[1]
    keywords = [w.lower() for w in query.split()]

    artifacts = {
        "PhysicalMap": load_artifact("PhysicalMap"),
        "EntityMap": load_artifact("EntityMap"),
        "ImportMap": load_artifact("ImportMap"),
        "RegistrationAST": load_artifact("RegistrationAST"),
        "CallGraph": load_artifact("CallGraph"),
        "LinkMap": load_artifact("LinkMap"),
        "DependencyModel": load_artifact("DependencyModel"),
    }
    if not artifacts["EntityMap"]:
        print("EntityMap not found.")
        return

    print(f"Searching for capability: {query}")
    result = build_capability_cluster(keywords, artifacts)

    if result is None:
        print("No capability found.")
        return

    cluster, evidence, files = result

    print("\n" + "="*60)
    print(f"CAPABILITY: {query.upper()}")
    print("="*60)
    total_evidence = sum(len(v) for v in evidence.values()) + len(cluster)
    print(f"TOTAL EVIDENCE: {total_evidence}")
    if total_evidence >= 10:
        print("STATUS: LOCKED")
        print("DO NOT BUILD AGAIN")
    elif total_evidence >= 5:
        print("STATUS: PARTIAL")
    else:
        print("STATUS: ABSENT")
    print()

    print("FILES:")
    for file_id, file_path in sorted(files):
        if file_path:
            print(f"  - {file_path} (id: {file_id})")
        else:
            print(f"  - file id: {file_id}")
    print()

    print("CLASSES:")
    for entity, etype, file_id, file_path in sorted(cluster):
        if etype == "class":
            print(f"  - {entity} (file: {file_id})")
    print()

    print("FUNCTIONS:")
    for entity, etype, file_id, file_path in sorted(cluster):
        if etype == "function":
            print(f"  - {entity} (file: {file_id})")
    print()

    for category, items in sorted(evidence.items()):
        if not items:
            continue
        print(f"{category.upper()}:")
        for item in sorted(items)[:20]:
            if isinstance(item, tuple):
                if len(item) == 2:
                    print(f"  - {item[0]} (file: {item[1]})")
                else:
                    print(f"  - {item[0]}")
            else:
                print(f"  - {item}")
        if len(items) > 20:
            print(f"  ... and {len(items) - 20} more")
        print()

    print("RECOMMENDATION:")
    if total_evidence >= 10:
        print("  - This capability is fully implemented. Do not build again.")
    elif total_evidence >= 5:
        print("  - This capability is partially implemented. Consider extending existing components.")
    else:
        print("  - This capability is not yet implemented. You may build it from scratch.")

if __name__ == "__main__":
    main()
