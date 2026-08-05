from A_03_ORCHESTRATION.semantic_layer import SemanticLayer
from A_01_CORE.memory_core import MemoryCore

class CoreOrchestrator:

    def __init__(self):
        self.semantic = SemanticLayer()
        self.memory = MemoryCore()

    def process(self, input_text: str, file_hint: str = None, session_history=None, task_id=None):

        # 1. SEMANTIC ANALYSIS
        decision = self.semantic.classify(file_hint or input_text)
        route = decision["route"]

        # 2. MEMORY BUILD
        memory_block = self.memory.build_memory_packet(session_history, task_id)

        # 3. FINAL CONTEXT PACK
        context = {
            "route": route,
            "reason": decision["reason"],
            "user": memory_block["user"],
            "task": memory_block["task_id"],
            "session_active": bool(session_history),
            "preferences": memory_block["preferences"]
        }

        return self._route(context)

    def _route(self, context: dict):

        route = context["route"]

        if route == "ARCHIVE":
            return {"action": "archive", "context": context}

        if route == "QUARANTINE":
            return {"action": "quarantine", "context": context}

        if route == "RUNNER":
            return {"action": "execute", "context": context}

        if route == "DISPATCHER":
            return {"action": "dispatch", "context": context}

        return {"action": "fallback", "context": context}


if __name__ == "__main__":
    core = CoreOrchestrator()
    print(core.process("нарисуй кота"))
