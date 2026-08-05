import threading
import time

from A_01_CORE.task_scheduler import ResourceManager, TaskGraph, TaskScheduler, WorkspaceIsolation
from A_01_CORE.runtime_contracts import CancellationToken


def step(order, depends=(), read_only=True, action="inspect"):
    return {
        "order": order,
        "depends_on": list(depends),
        "read_only": read_only,
        "action": action,
        "arguments": {"workspace": "test-workspace", "read_only": read_only},
    }


def test_task_graph_builds_dependency_layers():
    layers = TaskGraph([step(1), step(2), step(3, (1, 2))]).layers()
    assert [[item["order"] for item in layer] for layer in layers] == [[1, 2], [3]]


def test_task_graph_infers_template_dependencies():
    second = step(2)
    second["arguments"]["input"] = "{{step_1.output}}"
    layers = TaskGraph([step(1), second]).layers()
    assert [[item["order"] for item in layer] for layer in layers] == [[1], [2]]


def test_task_graph_rejects_cycles():
    try:
        TaskGraph([step(1, (2,)), step(2, (1,))]).layers()
    except ValueError as exc:
        assert "CYCLE" in str(exc)
    else:
        raise AssertionError("cyclic graph accepted")


def test_independent_read_only_steps_execute_in_parallel():
    scheduler = TaskScheduler(max_workers=2)
    barrier = threading.Barrier(2)

    def worker(item):
        barrier.wait(timeout=1)
        return item["order"]

    result = scheduler.execute_layer([step(1), step(2)], worker, CancellationToken())
    assert result == [1, 2]


def test_write_steps_are_always_sequential():
    scheduler = TaskScheduler(max_workers=2)
    active = 0
    maximum = 0
    lock = threading.Lock()

    def worker(item):
        nonlocal active, maximum
        with lock:
            active += 1
            maximum = max(maximum, active)
        time.sleep(0.01)
        with lock:
            active -= 1
        return item["order"]

    scheduler.execute_layer(
        [step(1, read_only=False, action="write_file"), step(2, read_only=False, action="write_file")],
        worker,
        CancellationToken(),
    )
    assert maximum == 1


def test_mutating_action_cannot_claim_read_only():
    assert WorkspaceIsolation.is_read_only(step(1, read_only=True, action="delete_file")) is False


def test_resource_manager_allows_readers_and_excludes_writer():
    resources = ResourceManager()
    entered = []
    release = threading.Event()

    def reader():
        with resources.lease("shared", read_only=True):
            entered.append("reader")
            release.wait(timeout=1)

    thread = threading.Thread(target=reader)
    thread.start()
    while not entered:
        time.sleep(0.001)
    writer_entered = []

    def writer():
        with resources.lease("shared", read_only=False):
            writer_entered.append(True)

    writer_thread = threading.Thread(target=writer)
    writer_thread.start()
    time.sleep(0.01)
    assert writer_entered == []
    release.set()
    thread.join(timeout=1)
    writer_thread.join(timeout=1)
    assert writer_entered == [True]


def test_pre_cancelled_scheduler_does_not_execute():
    token = CancellationToken()
    token.cancel("operator")
    try:
        TaskScheduler().execute_layer([step(1)], lambda _: None, token)
    except RuntimeError as exc:
        assert "TASK_CANCELLED" in str(exc)
    else:
        raise AssertionError("cancelled scheduler executed")
