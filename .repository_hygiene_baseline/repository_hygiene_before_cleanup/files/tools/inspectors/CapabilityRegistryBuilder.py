#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CAPABILITY REGISTRY BUILDER — полный самоаудит Butler.
Использует все существующие артефакты и строит формальный реестр возможностей.
Не создаёт новые инспекторы. Только анализ и документирование.
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict, Counter

ROOT = Path.cwd()
OUT_JSON = ROOT / "CapabilityRegistry.json"
OUT_MD = ROOT / "CapabilityRegistry.md"
OUT_FINDINGS = ROOT / "SelfAudit_Findings.json"

# Список всех артефактов, которые мы будем использовать
ARTIFACTS = {
    "PhysicalMap": "Inspector0_PhysicalMap.json",
    "EntityMap": "Inspector1_EntityMap.json",
    "ImportMap": "Inspector2_ImportMap.json",
    "RegistrationAST": "Inspector3_RegistrationAST.json",
    "CallGraph": "Inspector4_CallGraph.json",
    "LinkMap": "LinkMap.json",
    "DependencyModel": "DependencyModel.json",
    "ProjectPassport": "A_07_CONFIG/project_passport.json"
}

def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return None

def get_file_info(file_id, physical_map):
    """Возвращает информацию о файле по ID из PhysicalMap."""
    for item in physical_map.get("payload", []):
        if str(item.get("id")) == str(file_id):
            return item
    return None

def extract_capabilities_from_registrations(reg_map, physical_map):
    """Извлекает возможности из регистраций."""
    capabilities = {}
    for entry in reg_map.get("payload", []):
        file_id = entry["id"]
        file_info = get_file_info(file_id, physical_map)
        file_path = file_info["relative_path"] if file_info else f"id:{file_id}"
        for reg in entry.get("registrations", []):
            func = reg.get("function")
            if func:
                if func not in capabilities:
                    capabilities[func] = {
                        "name": func,
                        "type": reg.get("kind"),
                        "source_file": file_path,
                        "line": reg.get("line"),
                        "consumers": [],
                        "dependencies": []
                    }
    return capabilities

def extract_consumers_from_calls(call_graph, physical_map):
    """Строит карту потребителей (кто вызывает какую функцию)."""
    consumers = defaultdict(list)
    for entry in call_graph.get("payload", []):
        file_id = entry["id"]
        file_info = get_file_info(file_id, physical_map)
        file_path = file_info["relative_path"] if file_info else f"id:{file_id}"
        for call in entry.get("calls", []):
            callee = call.get("callee")
            if callee:
                consumers[callee].append({
                    "caller_file": file_path,
                    "context": call.get("context"),
                    "line": call.get("line")
                })
    return consumers

def extract_dependencies_from_imports(import_map, physical_map):
    """Строит карту зависимостей (какие модули импортируются)."""
    dependencies = defaultdict(list)
    for entry in import_map.get("payload", []):
        file_id = entry["id"]
        file_info = get_file_info(file_id, physical_map)
        file_path = file_info["relative_path"] if file_info else f"id:{file_id}"
        for imp in entry.get("imports", []):
            module = imp.get("module")
            if module:
                dependencies[module].append({
                    "importer_file": file_path,
                    "kind": imp.get("kind"),
                    "line": imp.get("line")
                })
    return dependencies

def analyze_passport(passport_data):
    """Анализирует Project Passport и возвращает список заявленных возможностей."""
    if not passport_data:
        return []
    # Предположим, что паспорт содержит список "capabilities" или "components"
    # Адаптируйте под реальную структуру вашего паспорта
    capabilities = passport_data.get("capabilities", []) or passport_data.get("components", [])
    return capabilities

def main():
    # Загружаем все артефакты
    data = {}
    for name, filename in ARTIFACTS.items():
        path = ROOT / filename
        data[name] = load_json(path)
        if data[name] is None:
            print(f"Warning: Could not load {filename}")

    # Проверяем, что основные артефакты загружены
    required = ["PhysicalMap", "EntityMap", "ImportMap", "RegistrationAST", "CallGraph", "LinkMap", "DependencyModel"]
    for req in required:
        if data.get(req) is None:
            print(f"ERROR: {req} is required but not loaded.")
            return

    physical_map = data["PhysicalMap"]
    reg_map = data["RegistrationAST"]
    call_graph = data["CallGraph"]
    import_map = data["ImportMap"]
    dep_model = data["DependencyModel"]
    passport = data.get("ProjectPassport")

    # 1. Извлекаем возможности из регистраций
    capabilities = extract_capabilities_from_registrations(reg_map, physical_map)

    # 2. Добавляем потребителей (из CallGraph)
    consumers = extract_consumers_from_calls(call_graph, physical_map)
    for func_name, consumers_list in consumers.items():
        if func_name in capabilities:
            capabilities[func_name]["consumers"] = consumers_list

    # 3. Добавляем зависимости (из ImportMap)
    dependencies = extract_dependencies_from_imports(import_map, physical_map)
    for module_name, deps_list in dependencies.items():
        # Пока не связываем модули с возможностями, но оставляем структуру
        pass

    # 4. Анализируем DependencyModel
    nodes = dep_model.get("nodes", {})
    edges = dep_model.get("edges", [])
    total_nodes = len(nodes)
    total_edges = len(edges)

    # 5. Анализируем Project Passport
    passport_capabilities = analyze_passport(passport)
    missing_from_passport = []
    for cap in passport_capabilities:
        if cap not in capabilities:
            missing_from_passport.append(cap)

    # 6. Формируем реестр
    registry = {
        "metadata": {
            "schema": "capability_registry",
            "version": "1.0",
            "generator": "CapabilityRegistryBuilder",
            "generated_utc": utc_now(),
            "source_artifacts": list(ARTIFACTS.values())
        },
        "capabilities": capabilities,
        "statistics": {
            "total_capabilities": len(capabilities),
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "passport_capabilities_count": len(passport_capabilities),
            "missing_from_passport": len(missing_from_passport)
        }
    }

    # Сохраняем JSON
    OUT_JSON.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")

    # Генерируем Markdown
    md_lines = []
    md_lines.append("# Capability Registry — Butler")
    md_lines.append(f"Generated: {registry['metadata']['generated_utc']}")
    md_lines.append(f"Total capabilities: {len(capabilities)}")
    md_lines.append("")
    md_lines.append("## Implemented capabilities")
    for name, info in sorted(capabilities.items()):
        md_lines.append(f"- **{name}** ({info['type']})")
        md_lines.append(f"  - Source: {info['source_file']} (line {info['line']})")
        md_lines.append(f"  - Consumers: {len(info['consumers'])}")
    md_lines.append("")
    md_lines.append("## Passport vs Reality")
    if missing_from_passport:
        md_lines.append("The following capabilities are declared in the passport but not found:")
        for cap in missing_from_passport:
            md_lines.append(f"- {cap}")
    else:
        md_lines.append("All passport capabilities are implemented.")
    md_lines.append("")
    md_lines.append("## Statistics")
    md_lines.append(f"- **Nodes in dependency model:** {total_nodes}")
    md_lines.append(f"- **Edges in dependency model:** {total_edges}")
    md_lines.append(f"- **Capabilities found:** {len(capabilities)}")
    md_lines.append(f"- **Capabilities declared in passport:** {len(passport_capabilities)}")
    md_lines.append(f"- **Missing from passport:** {len(missing_from_passport)}")
    md_lines.append("")
    md_lines.append("## Artifacts used")
    for name, filename in ARTIFACTS.items():
        md_lines.append(f"- {filename}")

    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")

    # Сохраняем Findings (расхождения)
    findings = {
        "metadata": {
            "generator": "CapabilityRegistryBuilder",
            "generated_utc": utc_now()
        },
        "findings": [
            {
                "rule": "MISSING_PASSPORT_CAPABILITY",
                "severity": "warning",
                "details": missing_from_passport
            }
        ]
    }
    OUT_FINDINGS.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")

    print("STATUS  : SUCCESS")
    print(f"REGISTRY: {OUT_JSON.name}")
    print(f"REPORT  : {OUT_MD.name}")
    print(f"FINDINGS: {OUT_FINDINGS.name}")
    print(f"CAPABILITIES: {len(capabilities)}")
    print(f"MISSING FROM PASSPORT: {len(missing_from_passport)}")

if __name__ == "__main__":
    main()
