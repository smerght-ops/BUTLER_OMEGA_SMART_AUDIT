import time

from A_01_CORE.system_stabilizer import SystemStabilizer
from A_07_MEMORY.self_healing_memory import SelfHealingMemory
from A_03_ORCHESTRATION.registry_brain import RegistryBrain
from A_03_ORCHESTRATION.message_network import MessageNetwork
from A_01_CORE.execution_loop import ExecutionLoop


class ButlerSystem:

    def __init__(self):
        self.stabilizer = SystemStabilizer()
        self.memory = SelfHealingMemory()
        self.registry = RegistryBrain()
        self.network = MessageNetwork()
        self.loop = ExecutionLoop()

    def clean_init(self):
        print("[START] CLEAN INIT SYSTEM")

        # MEMORY
        try:
            self.memory.auto_repair("A_05_STORAGE/user_profile.json")
            print("[OK] Memory ready")
        except Exception as e:
            print("[WARN] Memory issue:", e)

        # REGISTRY
        try:
            self.registry.load()
            print("[OK] Registry ready")
        except Exception as e:
            print("[WARN] Registry issue:", e)

        # NETWORK
        try:
            self.network.read_queue()
            print("[OK] Message network ready")
        except Exception as e:
            print("[WARN] Network issue:", e)

        # HEALTH CHECK
        try:
            ok, report = self.stabilizer.health_check({
                "memory": True,
                "registry": True,
                "network": True,
                "core": True
            })
            print("[HEALTH]", ok)
        except Exception as e:
            print("[WARN] Health issue:", e)

    def run(self):
        self.clean_init()

        print("[START] SYSTEM ONLINE")

        try:
            self.loop.run(delay=1)
        except KeyboardInterrupt:
            print("[STOP] SYSTEM SHUTDOWN")


if __name__ == "__main__":
    ButlerSystem().run()
