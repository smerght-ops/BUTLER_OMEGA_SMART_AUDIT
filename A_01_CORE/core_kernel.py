from pathlib import Path
import json

from A_03_ORCHESTRATION.semantic_layer import SemanticLayer

class CoreKernel:

    def __init__(self):
        self.semantic = SemanticLayer()

    def process_file(self, file_path: str):
        result = self.semantic.classify(file_path)

        route = result["route"]
        reason = result["reason"]

        return {
            "input": file_path,
            "route": route,
            "reason": reason
        }

    def safe_route(self, file_path: str):
        decision = self.process_file(file_path)

        if decision["route"] in ["ARCHIVE", "QUARANTINE"]:
            return decision

        return decision
