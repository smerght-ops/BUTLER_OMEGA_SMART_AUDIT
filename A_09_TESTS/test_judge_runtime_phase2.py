from A_01_CORE.judge_runtime import Confidence, Evidence, JudgeRuntime, ValidationRule


def test_judge_passes_success_with_verified_evidence():
    result = JudgeRuntime().evaluate(
        {"ok": True, "error": None},
        [Evidence("test", "artifact exists", True, verified=True)],
    )
    assert result["verdict"] == "PASS"
    assert result["confidence"]["score"] >= 0.85


def test_judge_warns_when_success_has_no_verified_evidence():
    result = JudgeRuntime().evaluate({"ok": True, "error": None})
    assert result["verdict"] == "WARNING"
    assert result["warnings"][0]["rule"] == "verified_evidence"


def test_judge_recommends_failure_for_executor_failure():
    result = JudgeRuntime().evaluate({"ok": False, "error": "boom"})
    assert result["verdict"] == "FAIL_RECOMMENDED"
    assert any(item["rule"] == "executor_success" for item in result["failures"])


def test_custom_validation_rule_is_enforced():
    rule = ValidationRule("answer", lambda result, _: result.get("answer") == 42, "wrong answer")
    result = JudgeRuntime().evaluate({"ok": True, "error": None, "answer": 0}, rules=[rule])
    assert result["verdict"] == "FAIL_RECOMMENDED"


def test_model_evaluation_uses_injected_provider():
    class Provider:
        def execute_employee(self, **kwargs):
            assert kwargs["employee"] == "chat"
            return {"text": "WARNING"}

    result = JudgeRuntime(model_provider=Provider()).evaluate(
        {"ok": True, "error": None},
        [Evidence("test", "checked", True, verified=True)],
        use_model=True,
    )
    assert result["model_assessment"] == "WARNING"


def test_confidence_rejects_out_of_range_score():
    try:
        Confidence(1.1)
    except ValueError as exc:
        assert "between 0 and 1" in str(exc)
    else:
        raise AssertionError("out-of-range confidence accepted")
