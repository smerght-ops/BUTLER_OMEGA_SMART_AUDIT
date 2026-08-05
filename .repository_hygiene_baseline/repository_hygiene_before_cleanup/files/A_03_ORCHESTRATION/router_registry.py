"""
Router Registry for Butler Omega
Maps route names from AgentRouter to target modules
Safe additive component
"""

class RouterRegistry:

    def __init__(self):
        self.routes = {
            "analysis": "Professor",
            "vision": "Vision_Engine",
            "memory": "SemanticSearchEngine",
            "generation": "ComfyUIBridge",
            "coder": "ProviderManager"
        }

    def get_target(self, route_name: str) -> str:
        return self.routes.get(route_name, "analysis")

if __name__ == "__main__":

    registry = RouterRegistry()
    test_routes = ["analysis", "vision", "memory", "generation", "coder", "unknown"]

    for r in test_routes:
        print(f"{r} -> {registry.get_target(r)}")


