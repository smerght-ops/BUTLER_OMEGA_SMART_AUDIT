#!/usr/bin/env python3
"""
DependencyModelBuilder — строит модель зависимостей (узлы + рёбра) из LinkMap.
Не использует графовые библиотеки. Только JSON. Не делает выводов.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Set

class DependencyModelBuilder:
    SCHEMA = "dependency_model"
    SCHEMA_VERSION = "1.0"
    GENERATOR = "DependencyModelBuilder"
    GENERATOR_VERSION = "1.0"

    def __init__(self, linkmap_path: str, output_path: str):
        self.linkmap_path = Path(linkmap_path)
        self.output_path = Path(output_path)
        self.nodes: Dict[str, Dict] = {}
        self.edges: List[Dict] = []
        self.metadata: Dict = {}

    def load_linkmap(self) -> Dict:
        try:
            with open(self.linkmap_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"ERROR: Cannot load {self.linkmap_path}: {e}", file=sys.stderr)
            sys.exit(1)

    def build(self):
        linkmap = self.load_linkmap()
        links = linkmap.get("payload", [])

        # Собираем узлы: каждый уникальный идентификатор становится узлом
        for link in links:
            source = link.get("source")
            target = link.get("target")
            if source and source not in self.nodes:
                self.nodes[source] = {"id": source, "type": "file"}  # можно уточнить тип позже
            if target and target not in self.nodes:
                # Определяем тип узла по виду target: если содержит точку, считаем модулем/классом/функцией
                if "." in target:
                    # может быть класс или функция, пока метим как "entity"
                    self.nodes[target] = {"id": target, "type": "entity"}
                else:
                    self.nodes[target] = {"id": target, "type": "module"}

        # Строим рёбра
        for link in links:
            source = link.get("source")
            target = link.get("target")
            link_type = link.get("type")
            metadata = link.get("metadata", {})
            self.edges.append({
                "source": source,
                "target": target,
                "relation": link_type,
                "metadata": metadata
            })

        # Статистика
        total_nodes = len(self.nodes)
        total_edges = len(self.edges)

        self.metadata = {
            "schema": self.SCHEMA,
            "schema_version": self.SCHEMA_VERSION,
            "generator": self.GENERATOR,
            "generator_version": self.GENERATOR_VERSION,
            "generated_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "input": {
                "linkmap": str(self.linkmap_path)
            },
            "statistics": {
                "total_nodes": total_nodes,
                "total_edges": total_edges,
            }
        }

        output = {
            "metadata": self.metadata,
            "nodes": self.nodes,
            "edges": self.edges,
        }

        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"ERROR: Failed to write output: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"STATUS  : SUCCESS")
        print(f"OUTPUT  : {self.output_path}")
        print(f"NODES   : {total_nodes}")
        print(f"EDGES   : {total_edges}")
        print(f"ERRORS  : 0")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python DependencyModelBuilder.py <linkmap.json> <output.json>")
        sys.exit(1)
    linkmap_path = sys.argv[1]
    output_path = sys.argv[2]
    builder = DependencyModelBuilder(linkmap_path, output_path)
    builder.build()
