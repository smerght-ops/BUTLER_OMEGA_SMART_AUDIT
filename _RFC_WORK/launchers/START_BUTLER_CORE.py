import time

from A_01_CORE.system_stabilizer import SystemStabilizer
from A_07_MEMORY.self_healing_memory import SelfHealingMemory
from A_03_ORCHESTRATION.registry_brain import RegistryBrain
from A_03_ORCHESTRATION.message_network import MessageNetwork
from A_01_CORE.core_orchestrator import CoreOrchestrator
from A_01_CORE.execution_loop import ExecutionLoop


class BootstrapCore:

    def __init__(self):
        self.stabilizer = SystemStabilizer()
        self.memory = SelfHealingMemory()
        self.registry = RegistryBrain()
        self.network = MessageNetwork()
        self.core = CoreOrchestrator()
        self.loop = ExecutionLoop()

    def health_check(self):

        components = {
            "core": True,
            "dispatcher": True,
            "semantic": True,
            "memory": True,
            "factory": True,
            "network": True
        }

        ok, report = self.stabilizer.health_check(components)

        print("[BOOTSTRAP] HEALTH CHECK:", ok)
        print(report)

        return ok

    def init_system(self):

        print("[BOOTSTRAP] Initializing CORE SYSTEM...")

        # 1. MEMORY HEAL
        try:
            self.memory.auto_repair(
                "A_05_STORAGE/user_profile.json"
            )
            print("[OK] Memory initialized")
        except Exception as e:
            print("[WARN] Memory issue:", e)

        # 2. REGISTRY LOAD
        try:
            self.registry.load()
            print("[OK] Registry loaded")
        except Exception as e:
            print("[WARN] Registry issue:", e)

        # 3. NETWORK INIT
        try:
            self.network.read_queue()
            print("[OK] Message network ready")
        except Exception as e:
            print("[WARN] Network issue:", e)

        # 4. STABILITY CHECK
        self.health_check()

    def run(self):

        self.init_system()

        print("[BOOTSTRAP] STARTING EXECUTION LOOP...")

        try:
            self.loop.run(delay=1)
        except KeyboardInterrupt:
            print("[BOOTSTRAP] STOPPED MANUALLY")


if __name__ == "__main__":
    app = BootstrapCore()
    app.run()
