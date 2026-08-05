# -*- coding: utf-8 -*-

"""
BUTLER OMEGA SMART
Semantic Reasoning Engine V2
ROADMAP 6.0 / Stage 1.3

LOCAL FIRST.
Graph reasoning over semantic_graph.json.
"""

from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Set
import json


ROOT = Path.cwd()
GRAPH_FILE = ROOT / "A_07_MEMORY" / "semantic_graph.json"


@dataclass
class ReasoningPath:
    start: str
    end: str
    depth: int
    score: float
    path: List[Dict[str, Any]]


class SemanticReasoningEngineV2:

    def __init__(self, graph_file: Path = GRAPH_FILE):
        self.graph_file = graph_file
        self.edges = []
        self.load()

    def load(self):
        if not self.graph_file.exists():
            self.edges = []
            return

        data = json.loads(
            self.graph_file.read_text(encoding="utf-8-sig")
        )

        self.edges = data.get("graph", [])

    def _neighbors(self, node: str):
        result = []

        for e in self.edges:
            source = e.get("source")
            target = e.get("target")
            relation = e.get("relation")
            weight = float(e.get("weight", 1.0))

            if source == node:
                result.append({
                    "from": source,
                    "relation": relation,
                    "to": target,
                    "weight": weight,
                    "direction": "out"
                })

            if target == node:
                result.append({
                    "from": target,
                    "relation": "reverse:" + relation,
                    "to": source,
                    "weight": weight * 0.8,
                    "direction": "in"
                })

        return result

    def explain_paths(self, start: str, max_depth: int = 3):
        results = []
        visited: Set[str] = set()

        def walk(node, depth, score, path):
            if depth >= max_depth:
                return

            visited.add(node)

            for step in self._neighbors(node):
                nxt = step["to"]

                if nxt in visited:
                    continue

                new_path = path + [step]
                new_score = score * float(step["weight"])

                results.append(
                    ReasoningPath(
                        start=start,
                        end=nxt,
                        depth=depth + 1,
                        score=round(new_score, 4),
                        path=new_path
                    )
                )

                walk(nxt, depth + 1, new_score, new_path)

            visited.discard(node)

        walk(start, 0, 1.0, [])

        results.sort(key=lambda x: (x.depth, -x.score, x.end))
        return [asdict(r) for r in results]

    def related(self, start: str, max_depth: int = 3, limit: int = 10):
        paths = self.explain_paths(start, max_depth=max_depth)
        return paths[:limit]

    def best(self, start: str, max_depth: int = 3):
        paths = self.explain_paths(start, max_depth=max_depth)
        return paths[0] if paths else None

    def explain_text(self, start: str, max_depth: int = 3):
        paths = self.explain_paths(start, max_depth=max_depth)

        lines = []
        lines.append("=" * 70)
        lines.append("SEMANTIC REASONING V2")
        lines.append("=" * 70)
        lines.append(f"START : {start}")
        lines.append(f"DEPTH : {max_depth}")
        lines.append(f"PATHS : {len(paths)}")
        lines.append("-" * 70)

        for p in paths:
            lines.append(f"END={p['end']} | depth={p['depth']} | score={p['score']}")

            for step in p["path"]:
                lines.append(
                    f"  {step['from']} --{step['relation']}--> {step['to']}"
                )

            lines.append("-" * 70)

        return "\n".join(lines)


if __name__ == "__main__":

    engine = SemanticReasoningEngineV2()

    for q in ["крыша", "ремонт", "автобус", "MB100D"]:
        print(engine.explain_text(q, max_depth=3))
        print()
