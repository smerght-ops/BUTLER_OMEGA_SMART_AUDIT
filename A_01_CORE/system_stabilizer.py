import json
import time
from pathlib import Path

class SystemStabilizer:

    def __init__(self):
        self.state_file = Path(__file__).resolve().parent / "system_state.json"
        self.max_cycles = 5

    def load_state(self):
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        return {"cycle_count": 0, "last_action": None, "status": "OK"}

    def save_state(self, state):
        self.state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    def check_loop(self, action):

        state = self.load_state()

        if state["last_action"] == action:
            state["cycle_count"] += 1
        else:
            state["cycle_count"] = 0

        state["last_action"] = action

        if state["cycle_count"] >= self.max_cycles:
            state["status"] = "LOOP_DETECTED"
            self.save_state(state)
            return False, "LOOP BLOCKED"

        state["status"] = "OK"
        self.save_state(state)

        return True, "OK"

    def health_check(self, components: dict):

        report = {
            "core": components.get("core", True),
            "dispatcher": components.get("dispatcher", True),
            "semantic": components.get("semantic", True),
            "memory": components.get("memory", True),
            "factory": components.get("factory", True),
        }

        if not all(report.values()):
            return False, report

        return True, report

    def emergency_rollback(self, reason: str):

        rollback = {
            "timestamp": time.time(),
            "reason": reason,
            "action": "ROLLBACK_TRIGGERED"
        }

        rollback_file = Path(__file__).resolve().parent / "ROLLBACK_EVENT.json"
        rollback_file.write_text(json.dumps(rollback, ensure_ascii=False, indent=2), encoding="utf-8")

        return rollback


if __name__ == "__main__":
    s = SystemStabilizer()
    print(s.check_loop("dispatch"))
    print(s.health_check({}))
