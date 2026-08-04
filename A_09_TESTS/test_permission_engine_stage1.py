import ast
from pathlib import Path
import unittest

from A_03_ORCHESTRATION.permission import (
    DepartmentExecutionGateway,
    PermissionDecision,
    PermissionRequest,
)


class RecordingEngine:
    def __init__(self, error=None):
        self.requests = []
        self.error = error

    def decide(self, request):
        self.requests.append(request)
        if self.error:
            raise self.error
        return PermissionDecision.ALLOW


class RecordingObservation:
    def __init__(self):
        self.rows = []

    def record(self, source, event, payload=None):
        self.rows.append((source, event, payload))


def gateway(engine=None):
    return DepartmentExecutionGateway(engine=engine, observation=RecordingObservation())


class PermissionEngineStage1Tests(unittest.TestCase):
    def test_allow_only_preserves_arguments_and_result(self):
        engine = RecordingEngine()

        class Department:
            NAME = "TEST"

            def execute(self, *args, **kwargs):
                return args, kwargs

        result = gateway(engine).execute(Department(), 1, "two", context={"x": 3})
        self.assertEqual(result, ((1, "two"), {"context": {"x": 3}}))
        self.assertEqual(len(engine.requests), 1)

    def test_department_exception_is_unchanged(self):
        error = RuntimeError("department failed")

        class Department:
            def execute(self):
                raise error

        with self.assertRaises(RuntimeError) as caught:
            gateway().execute(Department())
        self.assertIs(caught.exception, error)

    def test_engine_error_is_fail_open(self):
        class Department:
            def execute(self):
                return "executed"

        self.assertEqual(
            gateway(RecordingEngine(ValueError("engine failed"))).execute(Department()),
            "executed",
        )

    def test_duplicate_active_execution_has_one_decision(self):
        engine = RecordingEngine()
        boundary = gateway(engine)
        request = PermissionRequest.create("OUTER", "test")

        class Inner:
            def execute(self):
                return "ok"

        class Outer:
            def execute(self):
                return boundary.execute(Inner(), permission_request=request)

        self.assertEqual(boundary.execute(Outer(), permission_request=request), "ok")
        self.assertEqual(len(engine.requests), 1)

    def test_nested_execution_gets_new_id_and_parent_id(self):
        engine = RecordingEngine()
        boundary = gateway(engine)

        class Browser:
            NAME = "BROWSER"

            def execute(self):
                return "web"

        class Search:
            NAME = "SEARCH"

            def execute(self):
                return boundary.execute(Browser())

        self.assertEqual(boundary.execute(Search()), "web")
        outer, inner = engine.requests
        self.assertNotEqual(inner.execution_id, outer.execution_id)
        self.assertEqual(inner.parent_execution_id, outer.execution_id)

    def test_department_import_or_creation_makes_no_decision(self):
        engine = RecordingEngine()

        class Department:
            def execute(self):
                return None

        Department()
        gateway(engine)
        self.assertEqual(engine.requests, [])

    def test_known_production_calls_use_gateway(self):
        root = Path(__file__).resolve().parents[1]
        expected = {
            "A_01_CORE/TaskExecutor/capability_executor.py": 4,
            "A_02_MANAGERS/smart_dispatcher_v2.py": 2,
            "A_09_INTERFACE/voice_input.py": 1,
            "A_03_ORCHESTRATION/chat_router.py": 1,
            "A_04_AGENTS/SearchDepartment/runner.py": 1,
            "A_04_AGENTS/CodingDepartment/DISPATCHER.py": 1,
        }
        for relative, minimum in expected.items():
            tree = ast.parse((root / relative).read_text(encoding="utf-8"))
            gateway_calls = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "execute"
                and (
                    isinstance(node.func.value, ast.Call)
                    or "gateway" in ast.unparse(node.func.value).casefold()
                )
            ]
            self.assertGreaterEqual(len(gateway_calls), minimum, relative)


if __name__ == "__main__":
    unittest.main()
