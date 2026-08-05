#!/usr/bin/env python3
"""
DiscoveryEngine v3 (fixed) — кластеризация сущностей с ограничением глубины.
"""

import json
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

def build_entity_graph():
    artifacts = {
        "PhysicalMap": load_artifact("PhysicalMap"),
        "EntityMap": load_artifact("EntityMap"),
        "ImportMap": load_artifact("ImportMap"),
        "RegistrationAST": load_artifact("RegistrationAST"),
        "CallGraph": load_artifact("CallGraph"),
        "LinkMap": load_artifact("LinkMap"),
        "DependencyModel": load_artifact("DependencyModel"),
    }
    graph = defaultdict(set)
    entity_metadata = defaultdict(lambda: {"types": [], "sources": []})
    file_paths = {}  # file_id -> relative_path

    # PhysicalMap: файлы
    if artifacts["PhysicalMap"]:
        for item in artifacts["PhysicalMap"]["payload"]:
            file_id = str(item["id"])
            rel_path = item["relative_path"]
            file_paths[file_id] = rel_path
            entity_metadata[file_id]["types"].append("file")
            entity_metadata[file_id]["sources"].append("PhysicalMap")

    # EntityMap: классы и функции
    if artifacts["EntityMap"]:
        for entry in artifacts["EntityMap"]["payload"]:
            file_id = str(entry["id"])
            for cls in entry.get("classes", []):
                name = cls["name"]
                entity_metadata[name]["types"].append("class")
                entity_metadata[name]["sources"].append(f"EntityMap (file: {file_id})")
                graph[name].add(file_id)
                graph[file_id].add(name)
            for func in entry.get("functions", []):
                name = func["name"]
                entity_metadata[name]["types"].append("function")
                entity_metadata[name]["sources"].append(f"EntityMap (file: {file_id})")
                graph[name].add(file_id)
                graph[file_id].add(name)

    # ImportMap
    if artifacts["ImportMap"]:
        for entry in artifacts["ImportMap"]["payload"]:
            file_id = str(entry["id"])
            for imp in entry.get("imports", []):
                module = imp.get("module", "")
                if module:
                    graph[file_id].add(module)
                    graph[module].add(file_id)

    # RegistrationAST
    if artifacts["RegistrationAST"]:
        for entry in artifacts["RegistrationAST"]["payload"]:
            file_id = str(entry["id"])
            for reg in entry.get("registrations", []):
                func = reg.get("function", "")
                if func:
                    graph[file_id].add(func)
                    graph[func].add(file_id)

    # CallGraph
    if artifacts["CallGraph"]:
        for entry in artifacts["CallGraph"]["payload"]:
            file_id = str(entry["id"])
            for call in entry.get("calls", []):
                callee = call.get("callee", "")
                if callee:
                    graph[file_id].add(callee)
                    graph[callee].add(file_id)

    # LinkMap
    if artifacts["LinkMap"]:
        for link in artifacts["LinkMap"]["payload"]:
            source = str(link.get("source", ""))
            target = str(link.get("target", ""))
            if source and target:
                graph[source].add(target)
                graph[target].add(source)

    # DependencyModel
    if artifacts["DependencyModel"]:
        for edge in artifacts["DependencyModel"].get("edges", []):
            source = str(edge.get("source", ""))
            target = str(edge.get("target", ""))
            if source and target:
                graph[source].add(target)
                graph[target].add(source)

    return graph, entity_metadata, file_paths

def find_cluster(query, graph, max_depth=3):
    """Находит связный кластер с ограничением глубины."""
    query_words = set(query.lower().split())
    seed_nodes = set()
    for node in graph:
        node_lower = node.lower()
        if all(word in node_lower for word in query_words):
            seed_nodes.add(node)
    if not seed_nodes:
        return set()

    visited = set()
    frontier = set(seed_nodes)
    for _ in range(max_depth):
        if not frontier:
            break
        new_frontier = set()
        for node in frontier:
            if node in visited:
                continue
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    new_frontier.add(neighbor)
        frontier = new_frontier
    visited.update(frontier)
    return visited

def main():
    if len(sys.argv) < 2:
        print("Usage: python DiscoveryEngine_v3_fixed.py <query>")
        sys.exit(1)
    query = sys.argv[1]

    print("Building entity graph...")
    graph, metadata, file_paths = build_entity_graph()
    print(f"Graph built: {len(graph)} nodes.")

    print(f"\nSearching for cluster for '{query}'...")
    cluster = find_cluster(query, graph, max_depth=2)  # ограничиваем глубину

    if not cluster:
        print("No cluster found.")
        return

    # Фильтруем: оставляем только те узлы, которые есть в metadata или file_paths
    entities = []
    for node in cluster:
        if node in metadata or node in file_paths:
            entities.append(node)

    # Группируем
    classes = []
    functions = []
    files = []
    others = []
    for node in entities:
        info = metadata.get(node, {})
        if "class" in info.get("types", []):
            classes.append(node)
        elif "function" in info.get("types", []):
            functions.append(node)
        elif "file" in info.get("types", []):
            files.append(node)
        else:
            others.append(node)

    print("\n" + "="*60)
    print(f"CAPABILITY: {query.title()}")
    print("="*60)
    print(f"Total entities: {len(entities)}")
    if classes:
        print(f"Classes: {', '.join(classes[:10])}" + ("..." if len(classes)>10 else ""))
    if functions:
        print(f"Functions: {', '.join(functions[:10])}" + ("..." if len(functions)>10 else ""))
    if files:
        print(f"Files: {', '.join(file_paths.get(f, f) for f in files[:10])}" + ("..." if len(files)>10 else ""))
    if others:
        print(f"Other: {', '.join(others[:10])}" + ("..." if len(others)>10 else ""))

    print(f"\nEvidence (sample):")
    for node in list(entities)[:15]:
        info = metadata.get(node, {})
        if info:
            types = ', '.join(info.get("types", []))
            sources = ', '.join(info.get("sources", []))
            print(f"  - {node} ({types}) — sources: {sources}")
        elif node in file_paths:
            print(f"  - {node} -> {file_paths[node]}")

    # Вердикт
    if len(entities) >= 10:
        verdict = "LOCKED"
    elif len(entities) >= 3:
        verdict = "PARTIAL"
    else:
        verdict = "ABSENT"
    print(f"\nVerdict: {verdict} (total entities: {len(entities)})")
    if verdict == "LOCKED":
        print("Do not build again.")

if __name__ == "__main__":
    main()
