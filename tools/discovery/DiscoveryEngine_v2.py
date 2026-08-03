#!/usr/bin/env python3
"""
DiscoveryEngine v2 — семантический движок на основе сущностей.
Строит индекс всех сущностей проекта из артефактов.
По запросу находит релевантные сущности и группирует их в возможности.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path.cwd()

# Загружаем артефакты
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

def build_entity_index():
    """Строит индекс сущностей из всех артефактов."""
    artifacts = {
        "PhysicalMap": load_artifact("PhysicalMap"),
        "EntityMap": load_artifact("EntityMap"),
        "ImportMap": load_artifact("ImportMap"),
        "RegistrationAST": load_artifact("RegistrationAST"),
        "CallGraph": load_artifact("CallGraph"),
        "LinkMap": load_artifact("LinkMap"),
        "DependencyModel": load_artifact("DependencyModel"),
    }

    entity_index = defaultdict(lambda: {"types": [], "sources": []})

    # PhysicalMap: файлы (как сущности)
    if artifacts["PhysicalMap"]:
        for item in artifacts["PhysicalMap"]["payload"]:
            rel_path = item.get("relative_path", "")
            if rel_path:
                entity_index[rel_path]["types"].append("file")
                entity_index[rel_path]["sources"].append("PhysicalMap")

    # EntityMap: классы и функции
    if artifacts["EntityMap"]:
        for entry in artifacts["EntityMap"]["payload"]:
            file_id = entry["id"]
            for cls in entry.get("classes", []):
                name = cls["name"]
                entity_index[name]["types"].append("class")
                entity_index[name]["sources"].append(f"EntityMap (file: {file_id})")
            for func in entry.get("functions", []):
                name = func["name"]
                entity_index[name]["types"].append("function")
                entity_index[name]["sources"].append(f"EntityMap (file: {file_id})")

    # ImportMap: модули
    if artifacts["ImportMap"]:
        for entry in artifacts["ImportMap"]["payload"]:
            file_id = entry["id"]
            for imp in entry.get("imports", []):
                module = imp.get("module", "")
                if module:
                    entity_index[module]["types"].append("module")
                    entity_index[module]["sources"].append(f"ImportMap (file: {file_id})")

    # RegistrationAST: регистрации (функции)
    if artifacts["RegistrationAST"]:
        for entry in artifacts["RegistrationAST"]["payload"]:
            file_id = entry["id"]
            for reg in entry.get("registrations", []):
                func = reg.get("function", "")
                if func:
                    entity_index[func]["types"].append("registration")
                    entity_index[func]["sources"].append(f"RegistrationAST (file: {file_id})")

    # CallGraph: вызываемые функции
    if artifacts["CallGraph"]:
        for entry in artifacts["CallGraph"]["payload"]:
            file_id = entry["id"]
            for call in entry.get("calls", []):
                callee = call.get("callee", "")
                if callee:
                    entity_index[callee]["types"].append("call")
                    entity_index[callee]["sources"].append(f"CallGraph (file: {file_id})")

    # LinkMap: источники и цели связей
    if artifacts["LinkMap"]:
        for link in artifacts["LinkMap"]["payload"]:
            source = str(link.get("source", ""))
            target = str(link.get("target", ""))
            if source:
                entity_index[source]["types"].append("link_source")
                entity_index[source]["sources"].append("LinkMap")
            if target:
                entity_index[target]["types"].append("link_target")
                entity_index[target]["sources"].append("LinkMap")

    # DependencyModel: узлы
    if artifacts["DependencyModel"]:
        for node_id in artifacts["DependencyModel"].get("nodes", {}).keys():
            entity_index[str(node_id)]["types"].append("dependency_node")
            entity_index[str(node_id)]["sources"].append("DependencyModel")

    return entity_index

def search_entities(query, entity_index):
    """Ищет сущности, чьи имена содержат слова запроса."""
    query_words = set(query.lower().split())
    results = []
    for entity, info in entity_index.items():
        entity_lower = entity.lower()
        # Проверяем, содержит ли имя сущности все слова запроса
        if all(word in entity_lower for word in query_words):
            results.append((entity, info))
    return results

def group_by_common_prefix(results, threshold=2):
    """Группирует сущности по общим частям имени (например, 'Memory')."""
    # Простая группировка: берём первую часть имени (до CamelCase или подчёркивания)
    groups = defaultdict(list)
    for entity, info in results:
        # Извлекаем первую часть имени (до заглавной буквы, подчёркивания или точки)
        parts = re.split(r'(?=[A-Z])|[_\.]', entity)
        if parts and parts[0]:
            prefix = parts[0].lower()
            groups[prefix].append((entity, info))
    # Фильтруем группы с количеством >= threshold
    return {prefix: items for prefix, items in groups.items() if len(items) >= threshold}

def main():
    if len(sys.argv) < 2:
        print("Usage: python DiscoveryEngine_v2.py <query>")
        sys.exit(1)
    query = sys.argv[1]

    print("Building entity index...")
    entity_index = build_entity_index()
    print(f"Entity index built: {len(entity_index)} entities.")

    print(f"\nSearching for '{query}'...")
    results = search_entities(query, entity_index)

    if not results:
        print("No entities found.")
        return

    # Группируем результаты по общим префиксам
    groups = group_by_common_prefix(results)
    if groups:
        print(f"Found {len(groups)} capability groups:")
        for prefix, items in sorted(groups.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n## {prefix.title()} ({len(items)} entities)")
            for entity, info in items[:10]:  # покажем первые 10
                types = ', '.join(info["types"])
                sources = ', '.join(info["sources"][:3])
                print(f"  - {entity} ({types}) — sources: {sources}")
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more.")
    else:
        # Если группы не образовались, выводим все результаты
        print(f"Found {len(results)} entities:")
        for entity, info in results[:20]:
            types = ', '.join(info["types"])
            sources = ', '.join(info["sources"][:3])
            print(f"  - {entity} ({types}) — sources: {sources}")
        if len(results) > 20:
            print(f"  ... and {len(results) - 20} more.")

    # Выносим вердикт на основе общего количества сущностей
    total_entities = len(results)
    if total_entities >= 5:
        verdict = "LOCKED"
    elif total_entities >= 2:
        verdict = "PARTIAL"
    else:
        verdict = "ABSENT"
    print(f"\nVerdict: {verdict} (total entities: {total_entities})")
    if verdict == "LOCKED":
        print("Do not build again.")

if __name__ == "__main__":
    main()
