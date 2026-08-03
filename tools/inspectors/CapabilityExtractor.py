#!/usr/bin/env python3
"""
CapabilityExtractor — извлекает высокоуровневые возможности из модели проекта.
Использует все артефакты (PhysicalMap, EntityMap, ImportMap, RegistrationAST, CallGraph, LinkMap, DependencyModel)
и строит реестр возможностей с доказательствами и статусом LOCKED.
"""

import json
from pathlib import Path
from collections import defaultdict

ROOT = Path.cwd()
OUT_JSON = ROOT / "CapabilityRegistry.json"
OUT_MD = ROOT / "CapabilityRegistry.md"

# Загружаем артефакты
def load_json(name):
    path = ROOT / name
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return None

physical_map = load_json("Inspector0_PhysicalMap.json")
entity_map = load_json("Inspector1_EntityMap.json")
import_map = load_json("Inspector2_ImportMap.json")
reg_map = load_json("Inspector3_RegistrationAST.json")
call_graph = load_json("Inspector4_CallGraph.json")
link_map = load_json("LinkMap.json")
dep_model = load_json("DependencyModel.json")

if not entity_map or not dep_model:
    print("Ошибка: не найден Inspector1_EntityMap.json или DependencyModel.json")
    exit(1)

# Строим карты
# Имя сущности -> список файлов, где она определена
entity_files = defaultdict(set)
for entry in entity_map["payload"]:
    file_id = entry["id"]
    for cls in entry.get("classes", []):
        entity_files[cls["name"]].add(file_id)
    for func in entry.get("functions", []):
        entity_files[func["name"]].add(file_id)

# Имя сущности -> список вызывающих файлов (из CallGraph)
callers = defaultdict(set)
for entry in call_graph["payload"]:
    file_id = entry["id"]
    for call in entry.get("calls", []):
        callee = call.get("callee")
        if callee:
            callers[callee].add(file_id)

# Имя сущности -> список импортирующих файлов (из ImportMap)
importers = defaultdict(set)
for entry in import_map["payload"]:
    file_id = entry["id"]
    for imp in entry.get("imports", []):
        module = imp.get("module")
        if module:
            importers[module].add(file_id)

# Регистрации: функция -> файл
registrations = defaultdict(list)
for entry in reg_map["payload"]:
    file_id = entry["id"]
    for reg in entry.get("registrations", []):
        func = reg.get("function")
        if func:
            registrations[func].append({"file": file_id, "line": reg.get("line")})

# Определяем возможности на основе ключевых компонентов
# Каждая возможность: имя, список ключевых компонентов (имя сущности), список дополнительных артефактов (пути)
CAPABILITY_DEFINITIONS = {
    "Project Memory": {
        "components": ["MemoryFacadeV2", "MemoryOrchestrator", "SemanticMemory", "MemoryReplay", "ProjectHistory"],
        "artifacts": ["A_07_MEMORY", "USER_MEMORY.md", "session_history.jsonl"],
        "dependencies": ["ExecutionRegistry", "ProjectPassport", "SearchEngine"]
    },
    "Smart Routing": {
        "components": ["SmartDispatcherV2", "DispatcherBridge", "RouterIntegration", "ProviderManager"],
        "artifacts": ["A_02_MANAGERS", "A_03_ORCHESTRATION"],
        "dependencies": ["ExecutionRegistry", "DepartmentRegistry"]
    },
    "Image Generation": {
        "components": ["ImageDepartment", "VisionDepartment", "VisionEngine", "ComfyUIBridge"],
        "artifacts": ["A_04_AGENTS/ImageDepartment", "A_04_AGENTS/VisionDepartment"],
        "dependencies": ["Memory", "Routing"]
    },
    "Task Execution": {
        "components": ["TaskRunner", "ExecutionPolicy", "RecipeExecutor", "ExecutorFactory"],
        "artifacts": ["A_02_MANAGERS/TaskRunner"],
        "dependencies": ["Routing", "Memory"]
    },
    "Semantic Search": {
        "components": ["SearchEngine", "CatalogManager", "ReferenceResolver", "SemanticReasoningEngine"],
        "artifacts": ["A_07_MEMORY/semantic_memory.py"],
        "dependencies": ["Memory"]
    },
    "Architecture Governance": {
        "components": ["ProjectPassport", "ArchitectureLock", "ExecutionRegistry", "GoalsRegistry"],
        "artifacts": ["A_00_ARCHITECTURE", "A_07_CONFIG"],
        "dependencies": []
    },
    "Audit Pipeline": {
        "components": ["Inspector0_PhysicalMap", "Inspector1_EntityMap", "Inspector2_ImportMap", "Inspector3_RegistrationAST", "Inspector4_CallGraph", "LinkMapBuilder", "DependencyModelBuilder"],
        "artifacts": ["Inspector0_PhysicalMap.json", "Inspector1_EntityMap.json", "Inspector2_ImportMap.json", "Inspector3_RegistrationAST.json", "Inspector4_CallGraph.json", "LinkMap.json", "DependencyModel.json"],
        "dependencies": []
    }
}

# Проверяем каждую возможность
capabilities = {}
for name, definition in CAPABILITY_DEFINITIONS.items():
    # Проверяем наличие всех компонентов
    present_components = []
    for comp in definition["components"]:
        if comp in entity_files:
            present_components.append(comp)
        # Дополнительно проверяем, есть ли компонент как вызываемый или импортируемый
        elif comp in callers or comp in importers:
            present_components.append(comp)
    # Если хотя бы половина компонентов присутствует, считаем возможность реализованной
    threshold = len(definition["components"]) * 0.5
    if len(present_components) >= threshold:
        # Собираем доказательства (файлы, где определены компоненты)
        evidence_files = set()
        for comp in present_components:
            evidence_files.update(entity_files.get(comp, set()))
        # Добавляем артефакты, которые существуют в проекте
        present_artifacts = []
        for art in definition["artifacts"]:
            if (ROOT / art).exists():
                present_artifacts.append(art)
            # Проверяем в PhysicalMap
            elif physical_map and any(item["relative_path"] == art for item in physical_map["payload"]):
                present_artifacts.append(art)
        # Проверяем зависимости (наличие компонентов)
        present_deps = []
        for dep in definition["dependencies"]:
            if dep in entity_files or dep in callers or dep in importers:
                present_deps.append(dep)
        # Если все компоненты на месте, статус LOCKED, иначе PARTIAL
        status = "LOCKED" if len(present_components) == len(definition["components"]) else "PARTIAL"
        capabilities[name] = {
            "status": status,
            "components": present_components,
            "evidence_files": list(evidence_files),
            "artifacts": present_artifacts,
            "dependencies": present_deps,
            "missing_components": [comp for comp in definition["components"] if comp not in present_components]
        }

# Генерируем отчёт
def generate_markdown():
    md_lines = []
    md_lines.append("=" * 60)
    md_lines.append("BUTLER CAPABILITY REGISTRY")
    md_lines.append("=" * 60)
    md_lines.append("")
    for name, info in capabilities.items():
        md_lines.append(f"## {name}")
        md_lines.append(f"**Status**: {info['status']}")
        md_lines.append("")
        md_lines.append("**Components**:")
        for comp in info['components']:
            md_lines.append(f"- {comp}")
        md_lines.append("")
        if info['evidence_files']:
            md_lines.append("**Evidence files**:")
            for f in info['evidence_files'][:10]:
                md_lines.append(f"- {f}")
            if len(info['evidence_files']) > 10:
                md_lines.append(f"... and {len(info['evidence_files']) - 10} more")
        md_lines.append("")
        if info['artifacts']:
            md_lines.append("**Artifacts**:")
            for art in info['artifacts']:
                md_lines.append(f"- {art}")
        md_lines.append("")
        if info['dependencies']:
            md_lines.append("**Dependencies**:")
            for dep in info['dependencies']:
                md_lines.append(f"- {dep}")
        md_lines.append("")
        if info['missing_components']:
            md_lines.append("**Missing components**:")
            for comp in info['missing_components']:
                md_lines.append(f"- {comp}")
        md_lines.append("")
    md_lines.append("## DO NOT BUILD AGAIN")
    md_lines.append("The following capabilities are LOCKED and should not be rebuilt:")
    for name, info in capabilities.items():
        if info['status'] == "LOCKED":
            md_lines.append(f"- {name}")
    md_lines.append("")
    return "\n".join(md_lines)

# Сохраняем JSON
OUT_JSON.write_text(json.dumps(capabilities, ensure_ascii=False, indent=2), encoding="utf-8")
# Сохраняем Markdown
OUT_MD.write_text(generate_markdown(), encoding="utf-8")

print("STATUS  : SUCCESS")
print(f"REGISTRY: {OUT_JSON.name}")
print(f"REPORT  : {OUT_MD.name}")
print(f"CAPABILITIES: {len(capabilities)}")
