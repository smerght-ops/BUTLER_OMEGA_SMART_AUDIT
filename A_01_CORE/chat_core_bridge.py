from A_03_ORCHESTRATION.semantic_layer import SemanticLayer
from A_07_MEMORY.profile_manager import load_profile

class ChatCoreBridge:

    def __init__(self):
        self.semantic = SemanticLayer()

    def process(self, text: str, file_hint: str = None):

        # 1. загрузка памяти
        profile = load_profile()

        # 2. семантическое решение
        if file_hint:
            decision = self.semantic.classify(file_hint)
        else:
            decision = self.semantic.classify(text)

        route = decision["route"]

        # 3. memory injection decision
        memory_name = profile.get("user_name", {}).get("name", {}).get("value")

        return {
            "input": text,
            "route": route,
            "memory_active": bool(memory_name),
            "user": memory_name,
            "reason": decision["reason"]
        }
