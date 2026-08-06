from A_02_MANAGERS.goal_manager import GoalManager
from A_02_MANAGERS.smart_dispatcher_v2 import SmartDispatcherV2


def test_goal_manager_command_reaches_manager_instead_of_empty_plan(tmp_path):
    dispatcher = SmartDispatcherV2()
    routed_manager = next(
        item for item in dispatcher.departments
        if dispatcher._dept_name(item) == "GOAL_MANAGER"
    )
    isolated_manager = GoalManager(tmp_path / "goals_registry.json")
    dispatcher.departments[dispatcher.departments.index(routed_manager)] = isolated_manager

    result = dispatcher.dispatch("goal create acceptance baseline regression")

    assert result["ok"] is True
    assert result["department"] == "GOAL_MANAGER"
    assert result["error"] is None
    assert result["text"] == "Цель создана: acceptance baseline regression"
    assert "No steps executed" not in str(result)
