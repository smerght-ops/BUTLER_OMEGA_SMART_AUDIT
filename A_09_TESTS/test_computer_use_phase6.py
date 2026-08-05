from A_04_AGENTS.ComputerUseDepartment.runner import ComputerUseDepartment


class Backend:
    def screenshot_base64(self):
        return "cG5n"

    def windows(self):
        return [{"handle": 1, "title": "Editor"}]

    def clipboard_text(self):
        return "clipboard value"

    def foreground(self):
        return {"handle": 1, "title": "Editor", "platform_supported": True}


class Gateway:
    def __init__(self):
        self.calls = []

    def execute(self, department, query, context=None):
        self.calls.append((department.NAME, query, context))
        return {"ok": True, "text": "screen analysis", "error": None}


def department():
    return ComputerUseDepartment(backend=Backend(), gateway=Gateway(), vision=type("Vision", (), {"NAME": "VISION"})())


def test_screenshot_stays_in_memory_and_can_use_vision_gateway():
    instance = department()
    result = instance.execute("screenshot", {"action": "capture_screenshot", "analyze": True})
    assert result["ok"] is True
    assert result["metadata"]["image_base64"] == "cG5n"
    assert result["metadata"]["vision_analysis"]["text"] == "screen analysis"
    assert instance.gateway.calls[0][0] == "VISION"


def test_window_clipboard_and_navigation_reads():
    instance = department()
    windows = instance.execute("windows", {"action": "list_windows"})
    clipboard = instance.execute("clipboard", {"action": "read_clipboard"})
    navigation = instance.execute("foreground", {"action": "inspect_navigation"})
    assert windows["metadata"]["windows"][0]["title"] == "Editor"
    assert clipboard["text"] == "clipboard value"
    assert navigation["metadata"]["foreground"]["title"] == "Editor"
    assert all(item["metadata"]["read_only"] for item in (windows, clipboard, navigation))


def test_mutating_computer_commands_are_blocked():
    for query in ("click button", "type password", "press enter", "запусти программу", "закрой окно"):
        result = department().execute(query)
        assert result["ok"] is False
        assert result["error"] == "COMPUTER_USE_READ_ONLY_VIOLATION"


def test_unknown_action_is_fail_closed():
    result = department().execute("observe", {"action": "open_application"})
    assert result["ok"] is False
    assert result["error"] == "COMPUTER_USE_ACTION_NOT_ALLOWED"


def test_canonical_registries_include_computer_use():
    from A_02_MANAGERS.department_registry import DEPARTMENTS
    from tools.inspectors.CapabilityRegistry import CapabilityRegistry

    assert DEPARTMENTS["COMPUTER_USE"]["class"] == "ComputerUseDepartment"
    actions = CapabilityRegistry().actions_by_department("COMPUTER_USE")
    assert actions == ["capture_screenshot", "inspect_navigation", "list_windows", "read_clipboard"]
