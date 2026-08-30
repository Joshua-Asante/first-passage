"""Independent adversarial refuter stage before sandbox promotion (SPEC S5).

Runs *after* ``validate_promotion_packet`` Pass. Catches residual confabulation
classes the schema alone cannot: missing on-disk artifacts, self-test path
absence, and ceiling re-read drift between validate and promote.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from discovery.promotion_packet import (
    ValidationResult,
    _is_finite_real,
    load_ceilings,
    validate_promotion_packet,
)

# Gates where the declared hurdle is a ceiling (lower measured is better).
_CEILING_GATES = frozenset({"survivor_bust"})


def refute_promotion_packet(
    packet: dict[str, Any] | str | Path,
    *,
    repo_root: str | Path,
    ceilings_path: str | Path | None = None,
) -> ValidationResult:
    """Adversarial checks independent of the validator's parse pass.

    Requires ``validate_promotion_packet`` to Pass first; then re-reads ceilings,
    verifies every cited artifact/self-test path exists under ``repo_root``, and
    confirms gate measured_value clears hurdle_value in declared units (no
    cross-unit reinterpretation).
    """
    if isinstance(packet, (str, Path)):
        raw = json.loads(Path(packet).read_text(encoding="utf-8"))
    else:
        raw = packet

    base = validate_promotion_packet(
        raw, ceilings_path=ceilings_path, repo_root=repo_root
    )
    if not base.ok:
        return ValidationResult(
            decision="Fail",
            reasons=("refuter:precondition_validate_fail",) + base.reasons,
        )

    reasons: list[str] = []
    root = Path(repo_root)

    # Re-read ceilings at promote time (hard config; detect mid-flight edit games).
    try:
        ceilings = load_ceilings(ceilings_path)
    except (OSError, ValueError) as exc:
        return ValidationResult(
            decision="Fail", reasons=(f"refuter:ceilings_unreadable:{exc}",)
        )

    sandbox = raw["sandbox"]
    if int(sandbox["micro_size_contracts"]) > int(ceilings["max_micro_size_contracts"]):
        reasons.append("refuter:ceiling:micro_size_contracts")
    if float(sandbox["loss_budget_usd"]) > float(ceilings["max_loss_budget_usd"]):
        reasons.append("refuter:ceiling:loss_budget_usd")
    if int(sandbox["attempt_budget"]) > int(ceilings["max_attempt_budget"]):
        reasons.append("refuter:ceiling:attempt_budget")
    if int(sandbox["concurrency_slots"]) > int(ceilings["max_concurrency"]):
        reasons.append("refuter:ceiling:concurrency")

    for claim in raw["claims"]:
        ap = claim["artifact_path"]
        if not (root / ap).is_file():
            reasons.append(f"refuter:artifact_missing:{ap}")

    for att in raw["gate_attestations"]:
        ap = att["artifact_path"]
        if not (root / ap).is_file():
            reasons.append(f"refuter:artifact_missing:{ap}")
        # Same-units numeric clearance — no unit conversion allowed here.
        # No explicit float() cast: it raises OverflowError on a JSON-supplied
        # magnitude beyond a C double's range (e.g. 10**1000), which would
        # crash the refuter on an adversarial packet instead of failing it
        # cleanly (Codex review, PR #221). int/float compare exactly without
        # casting (CPython), so the raw values are used as-is below.
        measured = att["measured_value"]
        hurdle = att["hurdle_value"]
        gate_id = att["gate_id"]
        # Any comparison against NaN is False, so a NaN/inf measured or
        # hurdle would otherwise sail through both the > and < branches below
        # unrejected (Codex review, PR #218) -- reject non-finite values
        # outright rather than let a bad comparison read as "clears the gate".
        if not (_is_finite_real(measured) and _is_finite_real(hurdle)):
            reasons.append(f"refuter:gate_non_finite:{gate_id}")
        elif gate_id in _CEILING_GATES:
            if measured > hurdle:
                reasons.append(f"refuter:gate_fail:{gate_id}")
        elif measured < hurdle:
            reasons.append(f"refuter:gate_fail:{gate_id}")

    st = raw["self_tests"]
    for key in ("positive_path", "negative_path"):
        rel = st[key]
        if not (root / rel).is_file():
            reasons.append(f"refuter:self_test_missing:{rel}")

    if reasons:
        return ValidationResult(decision="Fail", reasons=tuple(reasons))
    return ValidationResult(decision="Pass", reasons=())
