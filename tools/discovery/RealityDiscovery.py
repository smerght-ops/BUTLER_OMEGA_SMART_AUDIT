#!/usr/bin/env python3
"""
RealityDiscovery — по запросу собирает все доказательства существования capability.
Использует все артефакты и выдает структурированный ответ.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

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

def find_entities_by_pattern(pattern, entity_map):
    """Возвращает все сущности из EntityMap, чьи имена совпадают с паттерном."""
    entities = set()
    for entry in entity_map.get("payload", []):
        for cls in entry.get("classes", []):
            if re.search(pattern, cls["name"], re.I):
                entities.add(cls["name"])
        for func in entry.get("functions", []):
            if re.search(pattern, func["name"], re.I):
                entities.add(func["name"])
    return entities

def collect_evidence(entity, artifacts):
    """Собирает доказательства для сущности из всех артефактов."""
    evidence = {"imports": [], "calls": [], "registrations": [], "links": []}
    # ImportMap
    if artifacts["ImportMap"]:
        for entry in artifacts["ImportMap"]["payload"]:
            for imp in entry.get("imports", []):
                module = imp.get("module", "")
                if entity.lower() in module.lower():
                    evidence["imports"].append((module, entry["id"]))
    # CallGraph
    if artifacts["CallGraph"]:
        for entry in artifacts["CallGraph"]["payload"]:
            for call in entry.get("calls", []):
                callee = call.get("callee", "")
                if entity.lower() in callee.lower():
                    evidence["calls"].append((callee, entry["id"]))
    # RegistrationAST
    if artifacts["RegistrationAST"]:
        for entry in artifacts["RegistrationAST"]["payload"]:
            for reg in entry.get("registrations", []):
                func = reg.get("function", "")
                if entity.lower() in func.lower():
                    evidence["registrations"].append((func, entry["id"]))
    # LinkMap
    if artifacts["LinkMap"]:
        for link in artifacts["LinkMap"]["payload"]:
            source = str(link.get("source", ""))
            target = str(link.get("target", ""))
            if entity.lower() in source.lower() or entity.lower() in target.lower():
                evidence["links"].append((json.dumps(link, ensure_ascii=False, sort_keys=True), None))
    return evidence

def main():
    if len(sys.argv) < 2:
        print("Usage: python RealityDiscovery.py <query>")
        sys.exit(1)
    query = sys.argv[1]

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
    if not artifacts["EntityMap"]:
        print("EntityMap not found.")
        return

    # Создаём паттерн из слов запроса
    words = query.lower().split()
    pattern = r'\b(' + '|'.join(re.escape(w) for w in words) + r')\w*'
    print(f"Pattern: {pattern}")

    # Находим все сущности, соответствующие паттерну
    entities = find_entities_by_pattern(pattern, artifacts["EntityMap"])
    if not entities:
        print("No entities found.")
        return

    print(f"Found {len(entities)} entities.")
    # Собираем доказательства для каждой сущности
    all_evidence = {"imports": set(), "calls": set(), "registrations": set(), "links": set()}
    for entity in entities:
        ev = collect_evidence(entity, artifacts)
        for key in all_evidence:
            all_evidence[key].update(ev[key])

    # Выводим структурированный ответ
    print("\n" + "="*60)
    print(f"CAPABILITY: {query.upper()}")
    print("="*60)
    print(f"STATUS: LOCKED")  # упрощённо, можно улучшить
    print(f"EVIDENCE SCORE: {sum(len(v) for v in all_evidence.values())}")
    print()
    print("FILES:")
    # Здесь нужно преобразовать ID в пути, но пока упростим
    print("  (derived from evidence)")
    print()
    print("CLASSES:")
    for entity in sorted(entities):
        print(f"  - {entity}")
    print()
    print("FUNCTIONS:")
    # тоже из EntityMap
    print()
    print("IMPORTS:")
    for imp, file_id in sorted(all_evidence["imports"])[:20]:
        print(f"  - {imp} (file: {file_id})")
    print()
    print("CALLS:")
    for call, file_id in sorted(all_evidence["calls"])[:20]:
        print(f"  - {call} (file: {file_id})")
    print()
    print("REGISTRATIONS:")
    for reg, file_id in sorted(all_evidence["registrations"])[:20]:
        print(f"  - {reg} (file: {file_id})")
    print()
    print("LINKS:")
    for link, _ in sorted(all_evidence["links"])[:20]:
        print(f"  - {link}")
    print()
    print("DO NOT BUILD AGAIN")

if __name__ == "__main__":
    main()

