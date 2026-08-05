from A_01_CORE.council_runtime import CouncilContract, CouncilLimits, CouncilMode, CouncilRuntime
from A_01_CORE.resource_awareness import ResourceSnapshot
from A_01_CORE.runtime_contracts import CancellationToken


class FixedResources:
    def __init__(self, ram=32 * 1024**3):
        self.ram = ram

    def snapshot(self):
        return ResourceSnapshot("now", 8, self.ram, self.ram, None, {"ollama": True})


class Provider:
    def execute_employee(self, employee, system_prompt, user_content):
        return {"status": "ok", "text": f"{employee}:{user_content}", "model": employee}


def test_all_council_modes_have_bounded_worker_counts():
    runtime = CouncilRuntime(provider=Provider(), resources=FixedResources())
    expected = {"SINGLE": 1, "DUAL_REVIEW": 2, "COUNCIL_3": 3, "COUNCIL_5": 5, "LOCAL_ONLY": 1}
    for mode in CouncilMode:
        result = runtime.run(CouncilContract("question", mode=mode))
        assert result["ok"] is True
        assert result["actual_workers"] == expected[mode.value]
        assert result["judge"]["verdict"] == "PASS"


def test_ram_fallback_reduces_council_size():
    runtime = CouncilRuntime(provider=Provider(), resources=FixedResources(ram=3 * 1024**3))
    result = runtime.run(CouncilContract("question", mode=CouncilMode.COUNCIL_5))
    assert result["actual_workers"] == 1
    assert "RAM_FALLBACK:5->1" in result["fallback"]


def test_worker_limit_is_enforced():
    runtime = CouncilRuntime(provider=Provider(), resources=FixedResources())
    contract = CouncilContract("question", mode=CouncilMode.COUNCIL_5, limits=CouncilLimits(max_workers=2))
    result = runtime.run(contract)
    assert result["actual_workers"] == 2
    assert "WORKER_LIMIT:5->2" in result["fallback"]


def test_token_limit_returns_controlled_failure():
    runtime = CouncilRuntime(provider=Provider(), resources=FixedResources())
    contract = CouncilContract("long answer", limits=CouncilLimits(max_tokens=1))
    result = runtime.run(contract)
    assert result["ok"] is False
    assert result["error"] == "TOKEN_LIMIT_EXCEEDED"
    assert result["judge"]["verdict"] == "FAIL_RECOMMENDED"


def test_pre_cancelled_council_does_not_call_provider():
    class ForbiddenProvider:
        def execute_employee(self, **kwargs):
            raise AssertionError("provider called after cancellation")

    token = CancellationToken()
    token.cancel("operator")
    result = CouncilRuntime(provider=ForbiddenProvider(), resources=FixedResources()).run(
        CouncilContract("question"), cancellation_token=token,
    )
    assert result["status"] == "CANCELLED"
    assert result["actual_workers"] == 0


def test_cost_limit_is_enforced():
    runtime = CouncilRuntime(provider=Provider(), resources=FixedResources())
    limits = CouncilLimits(max_cost=0.0001, cost_per_1000_tokens=1.0)
    result = runtime.run(CouncilContract("question", limits=limits))
    assert result["error"] == "COST_LIMIT_EXCEEDED"
