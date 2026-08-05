#!/usr/bin/env python3
"""
ButlerCapabilityAggregator — выделяет высокоуровневые возможности из графа зависимостей.
Использует DependencyModel для кластеризации сущностей по связям.
Группирует в функциональные блоки (capabilities) и выдаёт отчёт.
"""

import json
from pathlib import Path
from collections import defaultdict, deque

ROOT = Path.cwd()
OUT_MD = ROOT / "BUTLER_CAPABILITIES.md"

def load_json(name):
    path = ROOT / name
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except:
        return None

# Загружаем артефакты
dep_model = load_json("DependencyModel.json")
entity_map = load_json("Inspector1_EntityMap.json")
reg_map = load_json("Inspector3_RegistrationAST.json")
call_graph = load_json("Inspector4_CallGraph.json")
import_map = load_json("Inspector2_ImportMap.json")
link_map = load_json("LinkMap.json")

if not dep_model or not entity_map:
    print("Ошибка: не найден DependencyModel.json или Inspector1_EntityMap.json")
    exit(1)

# Строим граф: узлы — сущности (имена классов/функций/модулей), рёбра — связи
graph = defaultdict(set)

# Добавляем рёбра из DependencyModel (edges)
for edge in dep_model.get("edges", []):
    source = edge.get("source")
    target = edge.get("target")
    if source and target:
        graph[source].add(target)
        graph[target].add(source)  # неориентированный для кластеризации

# Добавляем рёбра из CallGraph (вызовы) — они уже есть в DependencyModel, но добавим для полноты
for entry in call_graph.get("payload", []):
    file_id = entry["id"]
    for call in entry.get("calls", []):
        callee = call.get("callee")
        if callee:
            # Связываем файл с вызываемой сущностью
            graph[file_id].add(callee)
            graph[callee].add(file_id)

# Добавляем рёбра из ImportMap (импорты) — также для полноты
for entry in import_map.get("payload", []):
    file_id = entry["id"]
    for imp in entry.get("imports", []):
        module = imp.get("module")
        if module:
            graph[file_id].add(module)
            graph[module].add(file_id)

# Кластеризация: ищем компоненты связности (connected components)
visited = set()
clusters = []

def bfs(start):
    queue = deque([start])
    component = []
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        component.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                queue.append(neighbor)
    return component

for node in graph:
    if node not in visited:
        cluster = bfs(node)
        if len(cluster) > 1:  # игнорируем изолированные узлы
            clusters.append(cluster)

# Сортируем кластеры по размеру (убывание)
clusters.sort(key=len, reverse=True)

# Определяем имена кластеров на основе семантических маркеров
# Загружаем список маркеров из SEMANTIC_MARKERS (можно расширять)
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
}

def name_cluster(cluster):
    """Подбирает имя для кластера на основе частоты маркеров."""
    marker_count = defaultdict(int)
    for node in cluster:
        node_lower = node.lower()
        for marker, keywords in MARKERS.items():
            for kw in keywords:
                if kw.lower() in node_lower:
                    marker_count[marker] += 1
                    break
    if marker_count:
        best = max(marker_count, key=marker_count.get)
        return best.title()
    # Если ничего не найдено, берём самый центральный узел (по количеству связей)
    # Или просто "Cluster"
    return "Other"

# Формируем отчёт
md_lines = []
md_lines.append("=" * 60)
md_lines.append("BUTLER CAPABILITIES (Aggregated)")
md_lines.append("=" * 60)
md_lines.append("")

for i, cluster in enumerate(clusters[:30]):  # покажем первые 30 кластеров
    name = name_cluster(cluster)
    md_lines.append(f"## {name} (size: {len(cluster)})")
    # Покажем первые 20 элементов кластера
    for node in cluster[:20]:
        md_lines.append(f"- {node}")
    if len(cluster) > 20:
        md_lines.append(f"... and {len(cluster) - 20} more")
    md_lines.append("")

md_lines.append("## ALREADY IMPLEMENTED")
md_lines.append("The following capabilities are already present and should not be rebuilt:")
for i, cluster in enumerate(clusters[:30]):
    name = name_cluster(cluster)
    md_lines.append(f"- {name} (size: {len(cluster)})")
md_lines.append("")

md_lines.append("## DO NOT BUILD AGAIN")
md_lines.append("Do not rebuild any of the above capabilities.")
md_lines.append("")

# Сохраняем
OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
print(f"Отчёт сохранён: {OUT_MD}")
print(f"Total clusters found: {len(clusters)}")
print("Просмотр: Get-Content BUTLER_CAPABILITIES.md -Encoding UTF8")
