# -*- coding: utf-8 -*-

from datetime import datetime
from pathlib import Path
import traceback

# Импортируем созданный и проверенный контур гвардов
from A_03_ORCHESTRATION.guards.frozen_core_guard import FrozenCoreGuard
from A_03_ORCHESTRATION.guards.rollback_guard import RollbackGuard
from A_03_ORCHESTRATION.guards.compile_guard import CompileGuard
from A_03_ORCHESTRATION.guards.integration_test_guard import IntegrationTestGuard
from A_03_ORCHESTRATION.observation_layer import ObservationLayer
from A_03_ORCHESTRATION.department_result import (
    RESULT_CONTROLLED_FAILURE,
    RESULT_INVALID,
    RESULT_NO_RESULT,
    RESULT_SUCCESS,
    validate_department_result,
)


class ButlerHarness:

    def __init__(self):
        self.version = "3.0_STABLE"
        self.observation = ObservationLayer()
        self.project_root = Path(__file__).resolve().parents[1]
        
        # Инициализируем обойму гвардов
        self.guards = [
            ("FrozenCore", FrozenCoreGuard()),
            ("Rollback", RollbackGuard()),
            ("Compile", CompileGuard()),
            ("IntegrationTest", IntegrationTestGuard())
        ]

    def validate(self, draft):
        """Обратная совместимость: базовая проверка артефакта постфактум."""
        return validate_department_result(draft, "UNKNOWN")["valid"]

    def commit(self, draft):
        return draft

    def execute(
        self,
        department_name,
        task,
        executor,
        auto_commit=True,
        cr_name=None,
    ):
        result = {
            "ok": False,
            "department": department_name,
            "model": None,
            "latency_ms": 0,
            "text": "",
            "error": None,
            "metadata": {},
            "draft": None,
            "validated": False,
            "committed": False,
            "timestamp": datetime.now().isoformat(),
            "pipeline_status": "PENDING",
            "result_outcome": "PENDING",
        }

        if not cr_name:
            result["pipeline_status"] = "MISSING_CHANGE_REQUEST"
            result["result_outcome"] = "GUARD_REJECTED"
            result["error"] = "An explicit Change Request is required for harness execution"
            result["metadata"]["diagnostics"] = {
                "code": "CR_REQUIRED",
                "resolution": "Pass cr_name explicitly from the runtime or test context",
            }
            return result

        # 1. Логируем старт пайплайна безопасности
        self.observation.record(
            source=department_name,
            event="HARNESS_V3_START",
            payload={"task": str(task), "cr_target": cr_name}
        )

        # Вычисляем путь к Change Request заявке от корня проекта
        cr_path = Path("A_00_ARCHITECTURE") / "CHANGE_REQUESTS" / cr_name

        # 2. ФАЗА ПРЕ-ФЛАЙТ КОНТРОЛЯ: ПОСЛЕДОВАТЕЛЬНЫЙ ПРОГОН ЦЕПОЧКИ ГВАРДОВ
        for guard_name, guard_instance in self.guards:
            try:
                guard_result = guard_instance.validate(cr_path)
                
                # Логируем атомарный проход каждого защитника в общую jsonl ленту
                self.observation.record(
                    source=f"Harness_Guard_{guard_name}",
                    event="GUARD_CHECK",
                    payload={"cr": cr_name, "result": guard_result}
                )

                if guard_result.get("status") == "REJECTED":
                    error_msg = f"Пайплайн заблокирован гвардом {guard_name}. Код: {guard_result.get('code')}. Причина: {guard_result.get('reason', 'Нет описания')}"
                    
                    self.observation.record(
                        source=department_name,
                        event="HARNESS_V3_REJECTED",
                        payload={"guard": guard_name, "code": guard_result.get("code")}
                    )
                    
                    result["pipeline_status"] = f"REJECTED_BY_{guard_name.upper()}"
                    result["error"] = error_msg
                    result["guard_code"] = guard_result.get("code")
                    result["result_outcome"] = "GUARD_REJECTED"
                    return result

            except Exception as ex:
                critical_error = f"Системный сбой внутри гварда {guard_name}: {str(ex)}"
                self.observation.record(
                    source=department_name,
                    event="HARNESS_GUARD_EXCEPTION",
                    payload={"guard": guard_name, "error": str(ex)}
                )
                result["pipeline_status"] = "SYSTEM_EXCEPTION"
                result["error"] = critical_error
                result["result_outcome"] = "EXCEPTION"
                result["metadata"]["diagnostics"] = {
                    "failure_source": f"Harness_Guard_{guard_name}",
                    "failure_stage": "pre_flight_guard",
                    "exception_type": type(ex).__name__,
                    "exception_message": str(ex),
                    "traceback": "\n".join(traceback.format_exc().strip().splitlines()[-10:]),
                }
                return result

        # 3. ФАЗА ИСПОЛНЕНИЯ (Допускается только при APPROVED от всех защитников)
        result["pipeline_status"] = "APPROVED_PRE_FLIGHT"
        
        try:
            draft = executor()
            result["draft"] = draft

            validation = validate_department_result(draft, department_name)
            result["result_outcome"] = validation["outcome"]
            result["metadata"]["result_validation"] = {
                "valid": validation["valid"],
                "outcome": validation["outcome"],
            }

            if validation["outcome"] == RESULT_NO_RESULT:
                self.observation.record(
                    source=department_name,
                    event="DEPARTMENT_NO_RESULT"
                )
                result["pipeline_status"] = RESULT_NO_RESULT
                result["error"] = validation["error"]
                return result

            if validation["outcome"] == RESULT_INVALID:
                self.observation.record(
                    source=department_name,
                    event="DEPARTMENT_INVALID_RESULT",
                    payload={"error": validation["error"]},
                )
                result["pipeline_status"] = RESULT_INVALID
                result["error"] = validation["error"]
                return result

            result["validated"] = True
            normalized = validation["normalized"]
            for key in (
                "ok", "department", "model", "latency_ms",
                "text", "error", "metadata"
            ):
                result[key] = normalized[key]

            if validation["outcome"] == RESULT_CONTROLLED_FAILURE:
                result["pipeline_status"] = RESULT_CONTROLLED_FAILURE
                if auto_commit:
                    result["commit_result"] = self.commit(normalized)
                    result["committed"] = True
                self.observation.record(
                    source=department_name,
                    event="DEPARTMENT_CONTROLLED_FAILURE",
                    payload={"error": normalized["error"]},
                )
                return result

            if auto_commit:
                result["commit_result"] = self.commit(normalized)
                result["committed"] = True
                result["pipeline_status"] = RESULT_SUCCESS

            self.observation.record(
                source=department_name,
                event="HARNESS_V3_SUCCESS",
                payload={"task": str(task)}
            )

            # [PASSPORT_ACTIVE_SYNC] Автоматическая фиксация живой системы
            if department_name == "SEARCH":
                try:
                    from A_07_CONFIG.project_passport_loader import ProjectPassportLoader
                    loader = ProjectPassportLoader()
                    loader.commit_proof("search_department_routing", "PROVEN")
                    loader.commit_proof("catalog_search_bridge", "PROVEN")
                    loader.commit_proof("4.24_active_sync_proof", "RUNNING_AUTOMATICALLY")
                    loader.evaluate_stage_transitions()
                except Exception as e:
                    print(f"[PASSPORT SYNC ERROR] {str(e)}")

            return result

        except Exception as ex:
            self.observation.record(
                source=department_name,
                event="EXECUTION_ERROR",
                payload={"error": str(ex)}
            )
            result["error"] = str(ex)
            result["pipeline_status"] = "EXECUTION_FAILED"
            result["result_outcome"] = "EXCEPTION"
            result["metadata"]["diagnostics"] = {
                "failure_source": department_name,
                "failure_stage": "department_execution",
                "exception_type": type(ex).__name__,
                "exception_message": str(ex),
                "traceback": "\n".join(traceback.format_exc().strip().splitlines()[-10:]),
            }
            return result


if __name__ == "__main__":
    import json
    harness = ButlerHarness()
    print("=== RUNTIME INTEGRATION TEST: BUTLER_HARNESS V3 ===")

    # Эмулируем работу абстрактного executor-а департамента
    def sample_executor():
        print(" -> [RUNNING] Executor транзакции запущен!")
        return {"status": "success", "payload": "data modified"}

    # Пробуем выполнить задачу. Так как бэкап router_integration.py сейчас старше 300с,
    # RollbackGuard обязан развернуть пайплайн до запуска sample_executor.
    print("\n[Пайплайн-Тест 1] Запуск execute() с существующим CR_000_TEST.json:")
    exec_result = harness.execute(
        department_name="ORCHESTRATION_TEST",
        task="Refactoring router integration layer",
        executor=sample_executor,
        cr_name="CR_000_TEST.json"
    )
    
    print("\nРезультат выполнения Harness Pipeline:")
    print(json.dumps(exec_result, indent=2, ensure_ascii=False))

