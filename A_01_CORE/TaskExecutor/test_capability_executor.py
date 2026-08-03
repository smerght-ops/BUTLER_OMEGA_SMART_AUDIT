import unittest

from A_01_CORE.TaskExecutor.capability_executor import CapabilityExecutor
from A_01_CORE.TaskExecutor.execution_context import ExecutionContext


class ExecutionContextTests(unittest.TestCase):
    def test_step_template_resolution(self):
        context = ExecutionContext()
        context.record(1, {"capability_id": "demo"}, {"ok": True, "department": "DEMO", "error": None}, "hello")
        self.assertEqual("hello", context.resolve("{{step_1.output}}"))
        self.assertEqual("value=hello", context.resolve("value={{step_1.output}}"))

    def test_missing_capability_stops_before_execution(self):
        plan = {
            "steps": [{
                "order": 1,
                "department": "UNKNOWN",
                "action": "not_registered",
                "status": "missing_capability",
            }]
        }
        result = CapabilityExecutor().execute(plan)
        self.assertFalse(result["ok"])
        self.assertEqual("missing_capability", result["metadata"]["status"])
        self.assertEqual([], result["metadata"]["history"])

    def test_typed_artifact_is_recorded(self):
        context = ExecutionContext()
        context.record(
            1,
            {"capability_id": "demo", "artifacts": {"output": "summary", "type": "summary"}},
            {"ok": True, "department": "DEMO", "error": None},
            __file__,
        )
        self.assertEqual("summary", context.artifacts[0]["name"])
        self.assertEqual("summary", context.artifacts[0]["type"])


if __name__ == "__main__":
    unittest.main()
