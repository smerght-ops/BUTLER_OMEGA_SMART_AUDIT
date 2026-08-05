from A_03_ORCHESTRATION.semantic_layer import SemanticLayer
from A_07_MEMORY.profile_manager import load_profile

class ChatRouterMirror:

    def __init__(self):
        self.semantic = SemanticLayer()

    def route(self, text: str):

        profile = load_profile()

        decision = self.semantic.classify(text)

        user_name = profile.get("user_name", {}).get("name", {}).get("value")

        route = decision["route"]

        # MIRROR LOGIC (не влияет на фабрику)
        return {
            "input": text,
            "route": route,
            "reason": decision["reason"],
            "memory": {
                "active": bool(user_name),
                "user": user_name
            },
            "mode": "MIRROR_ONLY"
        }


if __name__ == "__main__":
    test = ChatRouterMirror()
    print(test.route("нарисуй кота"))
