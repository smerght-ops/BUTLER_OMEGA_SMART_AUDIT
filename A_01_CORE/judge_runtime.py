"""Evidence-based evaluation of one executor result."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Iterable, Mapping


class JudgeVerdict(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL_RECOMMENDED = "FAIL_RECOMMENDED"


@dataclass(frozen=True)
class Evidence:
    source: str
    claim: str
    value: Any
    verified: bool = False
    kind: str = "observation"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Confidence:
    score: float
    basis: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("confidence score must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {"score": self.score, "basis": list(self.basis)}


@dataclass(frozen=True)
class ValidationRule:
    name: str
    check: Callable[[Mapping[str, Any], tuple[Evidence, ...]], bool]
    failure: str
    required: bool = True


class JudgeRuntime:
    """Evaluate a structured result without becoming an execution owner."""

    def __init__(self, model_provider=None):
        self._model_provider = model_provider

    @staticmethod
    def _evidence(values: Iterable[Evidence | Mapping[str, Any]]) -> tuple[Evidence, ...]:
        normalized = []
        for value in values or ():
            if isinstance(value, Evidence):
                normalized.append(value)
            elif isinstance(value, Mapping):
                normalized.append(Evidence(
                    source=str(value.get("source") or value.get("department") or "runtime"),
                    claim=str(value.get("claim") or value.get("step") or "execution observation"),
                    value=value.get("value", value.get("ok")),
                    verified=bool(value.get("verified", value.get("ok") is True)),
                    kind=str(value.get("kind") or "execution"),
                ))
        return tuple(normalized)

    @staticmethod
    def default_rules() -> tuple[ValidationRule, ...]:
        return (
            ValidationRule("mapping_result", lambda result, _: isinstance(result, Mapping), "result is not a mapping"),
            ValidationRule("boolean_ok", lambda result, _: isinstance(result.get("ok"), bool), "result.ok is not boolean"),
            ValidationRule(
                "error_consistency",
                lambda result, _: not (result.get("ok") is True and result.get("error") not in (None, "")),
                "successful result contains an error",
            ),
            ValidationRule(
                "executor_success",
                lambda result, _: result.get("ok") is True,
                "executor reported failure",
            ),
        )

    def evaluate(
        self,
        result: Mapping[str, Any],
        evidence: Iterable[Evidence | Mapping[str, Any]] = (),
        rules: Iterable[ValidationRule] | None = None,
        use_model: bool = False,
    ) -> dict[str, Any]:
        evidence_items = self._evidence(evidence)
        failures = []
        warnings = []
        for rule in tuple(rules or self.default_rules()):
            try:
                passed = bool(rule.check(result, evidence_items))
            except Exception as exc:
                passed = False
                failure = f"{rule.failure}: {type(exc).__name__}"
            else:
                failure = rule.failure
            if not passed:
                (failures if rule.required else warnings).append({"rule": rule.name, "reason": failure})

        verified = sum(item.verified for item in evidence_items)
        if not failures and not verified:
            warnings.append({"rule": "verified_evidence", "reason": "no verified evidence supplied"})

        verdict = JudgeVerdict.FAIL_RECOMMENDED if failures else (
            JudgeVerdict.WARNING if warnings else JudgeVerdict.PASS
        )
        basis = [item["rule"] for item in failures + warnings] or ["all rules passed", "verified evidence"]
        confidence = Confidence(
            score=1.0 if failures else (0.75 if warnings else min(1.0, 0.85 + verified * 0.03)),
            basis=tuple(basis),
        )

        model_assessment = None
        if use_model:
            provider = self._model_provider
            if provider is None:
                from A_02_MANAGERS.smart_dispatcher import get_chat_provider
                provider = get_chat_provider()
            response = provider.execute_employee(
                employee="chat",
                system_prompt="Return only PASS, WARNING, or FAIL_RECOMMENDED.",
                user_content=f"Evaluate result={dict(result)!r}; evidence={[item.to_dict() for item in evidence_items]!r}",
            )
            candidate = str(response.get("text") or "").strip().upper()
            model_assessment = candidate if candidate in {item.value for item in JudgeVerdict} else "UNAVAILABLE"

        return {
            "verdict": verdict.value,
            "confidence": confidence.to_dict(),
            "evidence": [item.to_dict() for item in evidence_items],
            "failures": failures,
            "warnings": warnings,
            "model_assessment": model_assessment,
        }
