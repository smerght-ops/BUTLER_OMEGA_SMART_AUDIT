from A_01_CORE.core_orchestrator import CoreOrchestrator

class FactoryCoreBridge:

    def __init__(self):
        self.core = CoreOrchestrator()

    def handle(self, input_text: str, file_path: str = None):

        decision = self.core.process(
            input_text=input_text,
            file_hint=file_path
        )

        action = decision["action"]

        # SAFE ROUTING LAYER (НЕ ЛОМАЕТ ФАБРИКУ)

        if action == "archive":
            return self._archive(decision)

        if action == "quarantine":
            return self._quarantine(decision)

        if action == "dispatch":
            return self._dispatch(decision)

        if action == "execute":
            return self._execute(decision)

        return self._fallback(decision)

    def _archive(self, decision):
        return {
            "status": "ARCHIVED",
            "route": decision
        }

    def _quarantine(self, decision):
        return {
            "status": "QUARANTINE",
            "route": decision
        }

    def _dispatch(self, decision):
        return {
            "status": "DISPATCHED",
            "route": decision
        }

    def _execute(self, decision):
        return {
            "status": "EXECUTED",
            "route": decision
        }

    def _fallback(self, decision):
        return {
            "status": "FALLBACK",
            "route": decision
        }


if __name__ == "__main__":
    bridge = FactoryCoreBridge()
    print(bridge.handle("нарисуй кота"))
