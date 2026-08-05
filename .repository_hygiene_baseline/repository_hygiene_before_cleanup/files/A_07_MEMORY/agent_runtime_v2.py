# ==============================
# EXECUTION LAYER v2 HARDEN PATCH
# ==============================

import time
import hashlib
import json
from pathlib import Path

from A_07_MEMORY.agent_planner import AgentPlannerV2
from A_07_MEMORY.goal_loop_engine import GoalLoopEngine
from A_07_MEMORY.change_request_manager import ChangeRequestManager


class ExecutionMemoryV2:

    def __init__(self):
        self.executed = {}  # task_id -> metadata

    def register(self, task_id: str, phase: str):
        self.executed[task_id] = {
            "phase": phase,
            "count": self.executed.get(task_id, {}).get("count", 0) + 1,
            "last_seen": time.time()
        }

    def is_stuck(self, task_id: str) -> bool:
        meta = self.executed.get(task_id)
        if not meta:
            return False
        return meta["count"] >= 2  # HARD LOOP DETECT


class LoopOrchestratorV3_EXEC_V2:

    def __init__(self):
        self.planner = AgentPlannerV2()
        self.goal_engine = GoalLoopEngine()
        self.cr = ChangeRequestManager()
        self.exec_mem = ExecutionMemoryV2()

        self.max_ticks = 15
        self.stall_counter = 0
        self.max_stall = 3

        self.last_fingerprint = None

    def fingerprint(self, plan: dict) -> str:
        raw = json.dumps(plan, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode()).hexdigest()

    def detect_deadlock(self, fp: str) -> bool:
        if self.last_fingerprint == fp:
            self.stall_counter += 1
        else:
            self.stall_counter = 0

        self.last_fingerprint = fp
        return self.stall_counter >= self.max_stall

    def start(self):

        print("=== EXECUTION LAYER v2 HARDEN START ===")

        for tick in range(self.max_ticks):

            plan = self.planner.get_current_action_plan()

            task = plan.get("active_task")
            phase = plan.get("active_phase")

            if not task or task in ["UNKNOWN", "FIX_REGISTRY"]:
                print("[STOP] invalid state")
                break

            task_id = f"{phase}::{task}"

            print(f"\n[TICK {tick}] {task_id}")

            # ==========================
            # DEADLOCK DETECTION (GLOBAL STATE)
            # ==========================
            fp = self.fingerprint(plan)
            if self.detect_deadlock(fp):
                print("[DEADLOCK] global planner freeze detected -> forcing advance")
                self.planner.complete_task(task)
                self.goal_engine.run()
                continue

            # ==========================
            # TASK LOOP DETECTION (LOCAL)
            # ==========================
            if self.exec_mem.is_stuck(task_id):
                print(f"[LOOP BREAK] {task_id}")
                self.planner.complete_task(task)
                self.goal_engine.run()
                continue

            # ==========================
            # EXECUTION REGISTRATION
            # ==========================
            self.exec_mem.register(task_id, phase)

            # ==========================
            # CR TRANSACTION
            # ==========================
            result = self.cr.propose_change(f"EXEC_V2_{task_id}")

            print(f"[CR] {result['status']} | {result['lock_id']}")

            # ==========================
            # STATE ADVANCE RULES
            # ==========================
            if result["status"] in ["OK", "DEDUP"]:
                self.planner.complete_task(task)
                self.goal_engine.run()
            else:
                print("[FAIL] transaction rejected")
                break

            time.sleep(0.3)

        print("\n=== EXECUTION V2 HARDEN STOP ===")


if __name__ == "__main__":
    LoopOrchestratorV3_EXEC_V2().start()
