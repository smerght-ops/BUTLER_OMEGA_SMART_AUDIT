# -*- coding: utf-8 -*-

import time
import hashlib
import json
import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from A_07_MEMORY.agent_planner import AgentPlannerV2
from A_07_MEMORY.goal_loop_engine import GoalLoopEngine
from A_07_MEMORY.change_request_manager import ChangeRequestManager
from A_07_MEMORY.execution_registry import ExecutionRegistry
from A_03_ORCHESTRATION.butler_harness import ButlerHarness


class LocalFeedbackValidatorV2:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[1]

    def validate_file_syntax(self, relative_path: str) -> bool:
        target_file = self.project_root / relative_path
        if not target_file.exists():
            return False
        try:
            res = subprocess.run(
                ["python", "-m", "py_compile", str(target_file)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return res.returncode == 0
        except Exception:
            return False


class LoopOrchestratorV3_MASTER_TRUTH:

    def __init__(self):
        self.planner = AgentPlannerV2()
        self.validator = LocalFeedbackValidatorV2()
        self.goal_engine = GoalLoopEngine()
        self.cr = ChangeRequestManager()
        self.exec_registry = ExecutionRegistry() # Внедрение Master Registry
        self.harness = ButlerHarness() # Интеграция контура безопасности Runtime <-> Harness (Сценарий 2B)

        self.project_root = Path(__file__).resolve().parents[1]
        self.registry_path = self.project_root / "A_07_CONFIG" / "goals_registry.json"

        self.max_ticks = 10
        self.error_streak = 0
        self.max_error_streak = 3
        self.last_task = None
        self.last_hash = None

        self.CORE_FILES = [
            "A_07_MEMORY/agent_planner.py",
            "A_07_MEMORY/memory_facade.py",
            "A_07_MEMORY/change_request_manager.py",
            "A_07_MEMORY/execution_registry.py"
        ]

    def fingerprint(self, data: dict) -> str:
        raw = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def load_state(self) -> dict:
        if not self.registry_path.exists():
            return {}
        try:
            return json.loads(self.registry_path.read_text(encoding="utf-8-sig"))
        except Exception:
            return {}

    def check_system_integrity(self) -> bool:
        for rel_path in self.CORE_FILES:
            if not self.validator.validate_file_syntax(rel_path):
                print(f"[FAIL] INTEGRITY CRITICAL ERROR: {rel_path}")
                return False
        return True

    def start(self):
        print("=== HARDENED MASTER TRUTH RUNTIME V3.2 ONLINE ===")

        for tick in range(self.max_ticks):
            state = self.load_state()
            current_hash = self.fingerprint(state)

            if self.last_hash and self.last_hash == current_hash:
                self.error_streak += 1
                print(f"[WARNING] Стейт стагнирует! Счётчик: {self.error_streak}/{self.max_error_streak}")
            else:
                if self.error_streak > 0 and current_hash != self.last_hash:
                    self.error_streak = 0

            self.last_hash = current_hash

            if self.error_streak >= self.max_error_streak:
                print("[HALT] STATE RUNTIME LOCKOUT (STALL DETECTED)")
                break

            plan = self.planner.get_current_action_plan()
            task = plan.get("active_task")
            phase = plan.get("active_phase")

            if not task or task in ["UNKNOWN", "FIX_REGISTRY"] or phase == "CRITICAL_ERROR":
                print(f"[STOP] Цикл завершен. Все глобальные фазы закрыты. PHASE={phase}")
                break

            # ==========================================
            # MASTER REGISTRY GROUND TRUTH CHECK
            # ==========================================
            if self.exec_registry.is_done(phase, task):
                print(f"[REGISTRY_SKIP] {phase}::{task} уже верифицирован в глобальной памяти истинности.")
                print("[REGISTRY_SKIP] Принудительно продвигаем указатель планировщика.")
                self.planner.complete_task(task)
                self.goal_engine.run()
                continue

            if task == self.last_task:
                self.error_streak += 1
            else:
                self.error_streak = 0

            self.last_task = task

            if self.error_streak >= self.max_error_streak:
                print(f"[HALT] TASK REPETITION FAULT ON: {task}")
                break

            print(f"\n[TICK {tick}] PHASE={phase} -> EXEC TASK={task}")

            if not self.check_system_integrity():
                print("[HALT] Мутация заблокирована: повреждена кодовая база.")
                break

            # Точка интеграции Runtime ↔ Harness (Сценарий 2B)
            # Оборачиваем мутацию в executor и прогоняем через постоянный сервисный контракт
            def runtime_executor():
                return self.cr.propose_change(f"AUTOLOOP_{task}_EXEC")

            harness_res = self.harness.execute(
                department_name="RUNTIME_PLANNER",
                task=f"AUTOLOOP_{task}_EXEC",
                executor=runtime_executor,
                cr_name="CR_RUNTIME_AUTOMATION.json"
            )

            # Извлекаем результат выполнения, если Харнас дал зеленый свет
            if harness_res.get("committed") and harness_res.get("pipeline_status") == "SUCCESS":
                result = harness_res.get("commit_result")
            else:
                result = {"status": "FAIL", "accepted": False, "lock_id": "REJECTED"}
                print(f"[HARNESS_BLOCK] Транзакция заблокирована гвардами Харнаса! Статус: {harness_res.get('pipeline_status')}")

            print(f"[CONTRACT] LOCK_ID: {result.get('lock_id')} | STATUS: {result.get('status')} | ACCEPTED: {result.get('accepted')}")

            task_completed = False
            if result["status"] == "OK" and result["accepted"]:
                self.planner.complete_task(task)
                self.exec_registry.mark_done(phase, task) # Пишем в Источник Истины
                print(f"[STATE_ADVANCE] Задача {task} успешно закрыта и внесена в реестр.")
                task_completed = True
            elif result["status"] == "DEDUP":
                print(f"[STATE_SYNC] Найдено совпадение LOCK_ID={result['lock_id']}. Фиксация истины.")
                self.planner.complete_task(task)
                self.exec_registry.mark_done(phase, task) # Синхронизируем истину на диске
                task_completed = True
            else:
                print(f"[TRANSACTION_ERROR] Отмена продвижения. Контракт отклонен.")
                break

            if task_completed:
                self.goal_engine.run()

            time.sleep(0.5)

        print("\n=== DETERMINISTIC RUNTIME TERMINATED ===")


if __name__ == "__main__":
    LoopOrchestratorV3_MASTER_TRUTH().start()
