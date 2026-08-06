from A_02_MANAGERS.department_registry import COMPONENTS, DEPARTMENTS, instantiate_departments, routable_specs
from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2
from A_03_ORCHESTRATION.butler_harness import ButlerHarness


def test_dispatcher_matches_canonical_registry():
    dispatcher = SmartDispatcherV2()
    assert [dispatcher._dept_name(item) for item in dispatcher.departments] == [name for name, _ in routable_specs()]


def test_all_production_departments_have_runner_and_contract():
    instances = instantiate_departments()
    assert len(instances) == len(DEPARTMENTS) + 1
    assert all(callable(item.can_handle) and callable(item.execute) for item in instances)


def test_goal_manager_not_misclassified_and_names_unique():
    assert "GOAL_MANAGER" not in DEPARTMENTS
    assert COMPONENTS["GOAL_MANAGER"]["component_type"] == "MANAGER"
    assert COMPONENTS["GOAL_MANAGER"]["routable"] is True
    assert len(DEPARTMENTS) == len(set(DEPARTMENTS))


def test_all_department_calls_use_gateway_source():
    import inspect
    source = inspect.getsource(SmartDispatcherV2._execute_department)
    assert "department_gateway.execute" in source
    assert "harness.execute" in source
    assert "except TypeError" not in source


def test_department_type_error_is_not_retried():
    class Gateway:
        calls = 0

        def execute(self, *args, **kwargs):
            self.calls += 1
            raise TypeError("department failure")

    class Harness:
        def execute(self, department_name, task, executor, **kwargs):
            executor()

    class Department:
        name = "TEST"

    dispatcher = SmartDispatcherV2.__new__(SmartDispatcherV2)
    dispatcher.department_gateway = Gateway()
    dispatcher.harness = Harness()
    dispatcher.audio_engine = None

    try:
        dispatcher._execute_department(Department(), "query", context={"cr_name": "CR.json"})
    except TypeError:
        pass
    else:
        raise AssertionError("Department TypeError must propagate")
    assert dispatcher.department_gateway.calls == 1


def test_harness_rejects_missing_change_request_before_execution():
    calls = []
    result = ButlerHarness().execute("TEST", "query", lambda: calls.append(True))
    assert result["pipeline_status"] == "MISSING_CHANGE_REQUEST"
    assert result["metadata"]["diagnostics"]["code"] == "CR_REQUIRED"
    assert calls == []
