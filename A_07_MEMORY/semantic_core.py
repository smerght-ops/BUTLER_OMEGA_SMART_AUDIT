# -*- coding: utf-8 -*-
# TX_TEST

"""
BUTLER OMEGA SMART

Semantic Core

ROADMAP 6.0
Stage 1.3

Public API
"""

from A_07_MEMORY.semantic_reasoning_engine_v2 import SemanticReasoningEngineV2
from A_07_MEMORY.semantic_relations_engine import SemanticRelationsEngine
from A_07_MEMORY.semantic_query_parser import SemanticQueryParser


class SemanticCore:

    def __init__(self):

        self.reasoner = SemanticReasoningEngineV2()
        self.graph = SemanticRelationsEngine()
        self.parser = SemanticQueryParser()

    def analyze(self, query:str, depth:int=3):

        starts=self.parser.parse(query)

        all_paths=[]

        for node in starts:
            all_paths.extend(
                self.reasoner.explain_paths(
                    node,
                    max_depth=depth
                )
            )

        unique={}
        for p in all_paths:
            k=(p["start"],p["end"],p["depth"])
            if k not in unique:
                unique[k]=p

        paths=list(unique.values())

        tokens=sorted(set(
            starts +
            [p["end"] for p in paths]
        ))

        return {

            "query":query,

            "semantic_tokens":tokens,

            "paths":paths,

            "relations":[
                {
                    "end":p["end"],
                    "depth":p["depth"],
                    "score":p["score"]
                }
                for p in paths
            ],

            "best_match":
                paths[0]["end"]
                if paths else None
        }


if __name__=="__main__":

    core = SemanticCore()

    result = core.analyze("ремонт крыши автобуса")

    print("="*70)
    print("SEMANTIC CORE")
    print("="*70)

    print()

    print("TOKENS")

    for t in result["semantic_tokens"]:
        print(" ", t)

    print()

    print("PATHS")

    for p in result["paths"]:

        print("-"*70)

        print(
            f'{p["end"]} | depth={p["depth"]} | score={p["score"]}'
        )

        for s in p["path"]:
            print(" ", s)







