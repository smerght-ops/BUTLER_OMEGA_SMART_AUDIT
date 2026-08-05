from pathlib import Path

from A_01_CORE.event_bus import EventBus
from A_01_CORE.execution_journal import ExecutionJournal
from A_01_CORE.resource_awareness import ResourceAwareness, ResourceSnapshot
from A_01_CORE.runtime_contracts import (
    CancellationToken,
    ModelLease,
    ResourceLease,
    TaskContract,
    TaskResult,
    TaskState,
)
from A_01_CORE.runtime_query_api import RuntimeQueryAPI
from A_01_CORE.TaskExecutor.capability_executor import CapabilityExecutor


def test_task_contract_and_structured_result_are_portable():
    contract = TaskContract.from_plan({"goal": "test", "steps": []}, "task_test")
    result = TaskResult(contract.task_id, TaskState.COMPLETED, True, output="ok")
    assert contract.goal == "test"
    assert result.to_dict()["state"] == "completed"


def test_cancellation_token_and_leases_are_cooperative():
    token = CancellationToken()
    token.cancel("requested")
    assert token.is_cancelled and token.reason == "requested"
    lease = ResourceLease("cpu", "task_test")
    model = ModelLease("model", "task_test", provider="ollama", model="qwen")
    lease.release()
    model.release()
    assert not lease.active and not model.active


def test_event_bus_subscribe_publish_unsubscribe():
    received = []
    listener = EventBus.subscribe("phase1.test", received.append)
    EventBus.publish("phase1.test", {"ok": True})
    EventBus.unsubscribe("phase1.test", listener)
    EventBus.publish("phase1.test", {"ok": False})
    assert received == [{"ok": True}]


def test_execution_journal_and_runtime_query_are_read_only(tmp_path):
    journal = ExecutionJournal(tmp_path)
    journal.write("task_one", {"task_id": "task_one", "final_status": "completed"})

    class FixedResources(ResourceAwareness):
        def snapshot(self):
            return ResourceSnapshot("now", 4, 10, 20, None, {"ollama": False})

    api = RuntimeQueryAPI(tmp_path, resources=FixedResources())
    assert api.task("task_one")["final_status"] == "completed"
    assert api.tasks("completed")[0]["task_id"] == "task_one"
    assert api.status()["tasks"]["completed"] == 1


def test_capability_executor_accepts_contract_and_cancellation(tmp_path):
    executor = CapabilityExecutor.__new__(CapabilityExecutor)
    executor.root = Path(tmp_path)
    executor.journal = ExecutionJournal(tmp_path)
    executor.journal_dir = executor.journal.directory
    executor.registry = None
    executor.skill_memory = None
    executor.department_gateway = None
    token = CancellationToken()
    token.cancel("operator")
    contract = TaskContract.from_plan(
        {"goal": "cancel me", "steps": [{"order": 1, "action": "unused"}]},
        "task_cancelled",
    )
    result = executor.execute(contract, cancellation_token=token)
    assert result["ok"] is False
    assert result["metadata"]["structured_result"]["state"] == "cancelled"
    assert result["metadata"]["resource_lease"]["released_at"]
    assert executor.journal.load("task_cancelled")["final_status"] == "cancelled"
