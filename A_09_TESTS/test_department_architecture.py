from A_02_MANAGERS.department_registry import COMPONENTS, DEPARTMENTS, department_specs, instantiate_departments
from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2


def test_dispatcher_matches_canonical_registry():
    dispatcher = SmartDispatcherV2()
    assert [dispatcher._dept_name(item) for item in dispatcher.departments] == [name for name, _ in department_specs()]


def test_all_production_departments_have_runner_and_contract():
    instances = instantiate_departments()
    assert len(instances) == len(DEPARTMENTS)
    assert all(callable(item.can_handle) and callable(item.execute) for item in instances)


def test_goal_manager_not_misclassified_and_names_unique():
    assert "GOAL_MANAGER" not in DEPARTMENTS
    assert COMPONENTS["GOAL_MANAGER"]["component_type"] == "MANAGER"
    assert len(DEPARTMENTS) == len(set(DEPARTMENTS))


def test_all_department_calls_use_gateway_source():
    import inspect
    source = inspect.getsource(SmartDispatcherV2._execute_department)
    assert "department_gateway.execute" in source
    assert "harness.execute" in source
