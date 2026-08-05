#!/usr/bin/env python3
"""
AutoCapabilityExtractor — автоматически извлекает возможности из графа зависимостей.
Использует семантические маркеры и связи для выделения функциональных кластеров.
"""

import json
from pathlib import Path
from collections import defaultdict, deque

ROOT = Path.cwd()
OUT_JSON = ROOT / "AutoCapabilityRegistry.json"
OUT_MD = ROOT / "AutoCapabilityRegistry.md"

def load_json(name):
    path = ROOT / name
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return None

# Загружаем артефакты
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

# Строим граф: узлы — имена сущностей (строки), рёбра — связи
graph = defaultdict(set)
file_entities = defaultdict(set)  # file -> list of entity names

# Из EntityMap: добавляем сущности и связываем их с файлами
for entry in entity_map["payload"]:
    file_id = str(entry["id"])
    for cls in entry.get("classes", []):
        name = cls["name"]
        file_entities[file_id].add(name)
        graph[name].add(file_id)
        graph[file_id].add(name)
    for func in entry.get("functions", []):
        name = func["name"]
        file_entities[file_id].add(name)
        graph[name].add(file_id)
        graph[file_id].add(name)

# Из CallGraph: добавляем связи вызовов
for entry in call_graph["payload"]:
    file_id = str(entry["id"])
    for call in entry.get("calls", []):
        callee = call.get("callee")
        if callee:
            graph[file_id].add(str(callee))
            graph[str(callee)].add(file_id)

# Из ImportMap: добавляем связи импортов
for entry in import_map["payload"]:
    file_id = str(entry["id"])
    for imp in entry.get("imports", []):
        module = imp.get("module")
        if module:
            graph[file_id].add(str(module))
            graph[str(module)].add(file_id)

# Из DependencyModel: добавляем все рёбра
for edge in dep_model.get("edges", []):
    source = edge.get("source")
    target = edge.get("target")
    if source is not None and target is not None:
        graph[str(source)].add(str(target))
        graph[str(target)].add(str(source))

# Расширенный список семантических маркеров (слово -> категория)
MARKERS = {
    "memory": ["memory", "Memory", "semantic", "history", "change_request"],
    "routing": ["dispatcher", "router", "bridge", "provider"],
    "image": ["image", "Image", "artist", "comfy", "vision"],
    "execution": ["runner", "executor", "task", "recipe", "policy"],
    "search": ["search", "catalog", "reference", "resolver"],
    "architecture": ["passport", "lock", "registry", "manifest", "guardian"],
    "audit": ["inspector", "map", "builder", "LinkMap", "Dependency"],
    "core": ["core", "orchestrator", "bootstrap", "kernel"],
    "agents": ["department", "agent", "Department"],
    "storage": ["storage", "store", "archive"],
    "logs": ["log", "logger", "report"],
    "config": ["config", "schema", "policy", "rule"],
    "guardian": ["guardian", "genie", "watch"],
    "runtime": ["runtime", "execution", "loop"],
    "communication": ["chat", "message", "event"],
    "validation": ["validator", "validate", "check"],
    "generation": ["generate", "generator", "artist", "comfy"],
    "resolver": ["resolver", "resolve"],
}

def get_marker_categories(name):
    """Возвращает список категорий для имени (строки)."""
    if not isinstance(name, str):
        return []
    lower = name.lower()
    cats = []
    for cat, keywords in MARKERS.items():
        for kw in keywords:
            if kw.lower() in lower:
                cats.append(cat)
                break
    return cats

# Для каждой категории извлекаем связные компоненты, содержащие сущности с этой категорией
capabilities = {}

for category in MARKERS.keys():
    # Находим все узлы, которые относятся к этой категории (сущности или файлы)
    category_nodes = set()
    for node in graph:
        if category in get_marker_categories(node):
            category_nodes.add(node)
    if not category_nodes:
        continue

    # BFS на подграфе, индуцированном category_nodes (и их соседями?)
    # Фактически, мы хотим кластеры, где все узлы имеют эту категорию.
    # Но мы можем расширить: если узел не имеет категории, но связан с категорийными узлами, он тоже может быть частью кластера.
    # Простой подход: рассматриваем только узлы с категорией.
    visited = set()
    clusters = []
    for node in category_nodes:
        if node not in visited:
            queue = deque([node])
            component = []
            while queue:
                current = queue.popleft()
                if current in visited:
                    continue
                visited.add(current)
                component.append(current)
                for neighbor in graph.get(current, []):
                    if neighbor in category_nodes and neighbor not in visited:
                        queue.append(neighbor)
            if len(component) >= 3:  # минимальный размер кластера
                clusters.append(component)

    if clusters:
        # Название возможности — название категории с заглавной
        cap_name = category.title()
        # Собираем все сущности из кластеров (уникальные)
        all_entities = set()
        for cluster in clusters:
            all_entities.update(cluster)
        # Фильтруем только сущности (не файлы) — имена, которые не похожи на ID файлов
        entities = [n for n in all_entities if isinstance(n, str) and not n.isdigit()]
        # Собираем файлы-доказательства (из file_entities)
        evidence_files = set()
        for entity in entities:
            for file_id, ents in file_entities.items():
                if entity in ents:
                    evidence_files.add(file_id)
        # Артефакты: ищем в PhysicalMap пути, которые содержат категорию
        artifacts = []
        if physical_map:
            for item in physical_map["payload"]:
                rel_path = item.get("relative_path", "")
                if category.lower() in rel_path.lower():
                    artifacts.append(rel_path)
        # Зависимости: другие категории, которые часто встречаются вместе
        # Пока пропустим
        capabilities[cap_name] = {
            "status": "LOCKED",  # если кластер существует, считаем LOCKED
            "components": list(entities),
            "evidence_files": list(evidence_files),
            "artifacts": list(artifacts),
            "dependencies": [],
            "missing_components": []
        }

# Генерируем отчёт
def generate_markdown():
    md_lines = []
    md_lines.append("=" * 60)
    md_lines.append("AUTO CAPABILITY REGISTRY")
    md_lines.append("=" * 60)
    md_lines.append("")
    for name, info in capabilities.items():
        md_lines.append(f"## {name}")
        md_lines.append(f"**Status**: {info['status']}")
        md_lines.append("")
        md_lines.append("**Components**:")
        for comp in info['components'][:15]:
            md_lines.append(f"- {comp}")
        if len(info['components']) > 15:
            md_lines.append(f"... and {len(info['components']) - 15} more")
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
            for art in info['artifacts'][:10]:
                md_lines.append(f"- {art}")
            if len(info['artifacts']) > 10:
                md_lines.append(f"... and {len(info['artifacts']) - 10} more")
        md_lines.append("")
        if info['dependencies']:
            md_lines.append("**Dependencies**:")
            for dep in info['dependencies']:
                md_lines.append(f"- {dep}")
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
