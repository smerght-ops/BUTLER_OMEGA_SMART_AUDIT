# -*- coding: utf-8 -*-

"""
BUTLER OMEGA SMART

Semantic Relations Engine V1

ROADMAP 6.0
Stage 1.2

LOCAL FIRST
"""

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class Relation:

    source:str
    relation:str
    target:str
    weight:float=1.0


class SemanticRelationsEngine:

    GRAPH_FILE=Path(__file__).parent/"semantic_graph.json"

    def __init__(self):

        self.relations=[]
        self.load()

    def add(self,source,relation,target,weight=1.0):

        self.relations.append(
            Relation(
                source,
                relation,
                target,
                weight
            )
        )

    def outgoing(self,node):

        return [
            r for r in self.relations
            if r.source==node
        ]

    def incoming(self,node):

        return [
            r for r in self.relations
            if r.target==node
        ]

    def neighbours(self,node):

        s=set()

        for r in self.relations:

            if r.source==node:
                s.add(r.target)

            if r.target==node:
                s.add(r.source)

        return sorted(s)

    def load(self):

        if not self.GRAPH_FILE.exists():
            return

        data=json.loads(
            self.GRAPH_FILE.read_text(
                encoding="utf-8-sig"
            )
        )

        self.relations=[]

        for r in data.get("graph",[]):

            self.relations.append(Relation(**r))

    def save(self):

        data={
            "version":"1.0",
            "graph":[r.__dict__ for r in self.relations]
        }

        self.GRAPH_FILE.write_text(
            json.dumps(data,ensure_ascii=False,indent=4),
            encoding="utf-8"
        )


if __name__=="__main__":

    g=SemanticRelationsEngine()

    print(f"Relations loaded : {len(g.relations)}")

    print("="*70)
    print("SEMANTIC RELATIONS")
    print("="*70)

    print()

    print("Neighbours(крыша)")
    print(g.neighbours("крыша"))

    print()

    print("Outgoing(ремонт)")

    for r in g.outgoing("ремонт"):
        print(r)

    print()

    print("Incoming(автобус)")

    for r in g.incoming("автобус"):
        print(r)
