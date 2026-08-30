"""Bounded promotion-lane packet validator (SPEC S5 / ADR 2026-08-07).

``validate_promotion_packet`` enforces: same-units schemas at parse, freeze-commit
hash match, artifact-only claims (prose carries nothing), and sandbox ceilings
read from ``promotion_ceilings.json`` at promotion time.

Promotion/demotion event shapes are stubs for the future S4 EventLedger wire —
do not force ``dry_run=false``; ledger append lands when M1 is ``RESOLVED``.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, TypedDict

from discovery.k_ledger_check import verify_manifest_backing
from research_utils.axis_screen import CAP, floor_at_k

Decision = Literal["Pass", "Fail"]

SCHEMA_VERSION = "s5.v1"
CEILINGS_PATH = Path(__file__).resolve().parent / "promotion_ceilings.json"

# Gate → required unit token (M-20 same-units; wrong-units §R class).
GATE_REQUIRED_UNITS: dict[str, str] = {
    "stage2_cost_law": "bp_per_event",
    "survivor_bust": "pct",
    "confirm_power": "probability",
    "dsr_floor": "annualized_sharpe",
}

ALLOWED_CLAIM_UNITS = frozenset(
    {
        "bp_per_event",
        "pct",
        "probability",
        "annualized_sharpe",
        "usd",
        "contracts",
        "count",
    }
)

# Fields that may never carry evidentiary prose on a claim object.
_FORBIDDEN_PROSE_KEYS = frozenset(
    {"prose", "narrative", "judgment", "commentary", "notes", "rationale"}
)


class PromotionEvent(TypedDict):
    """Stub promotion record for S4 EventLedger (wire when M1 RESOLVED).

    Do not append to the live rail ledger from this module — attended-only and
    per-session GO stand; unattended-loop authorization is a separate ADR.
    """

    event_type: Literal["promotion"]
    candidate_id: str
    freeze_commit: str
    sandbox: dict[str, Any]
    packet_sha256: str
    operator_budget_approval_id: str
    ts_utc: str


class DemotionEvent(TypedDict):
    """Stub demotion record — universal + instant (SPEC S5)."""

    event_type: Literal["demotion"]
    candidate_id: str
    reason: str
    prior_tier: str
    ts_utc: str


@dataclass(frozen=True)
class ValidationResult:
    decision: Decision
    reasons: tuple[str, ...] = field(default_factory=tuple)

    @property
    def ok(self) -> bool:
        return self.decision == "Pass"


def load_ceilings(path: str | Path | None = None) -> dict[str, Any]:
    """Load hard ceilings config (read at promotion time)."""
    p = Path(path) if path is not None else CEILINGS_PATH
    raw = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("ceilings file must be a JSON object")
    required = (
        "max_micro_size_contracts",
        "max_loss_budget_usd",
        "max_attempt_budget",
        "max_concurrency",
    )
    missing = [k for k in required if k not in raw]
    if missing:
        raise ValueError(f"ceilings file missing keys: {missing}")
    return raw


def _fail(*reasons: str) -> ValidationResult:
    return ValidationResult(decision="Fail", reasons=tuple(reasons))


def _pass() -> ValidationResult:
    return ValidationResult(decision="Pass", reasons=())


def validate_promotion_packet(
    packet: dict[str, Any] | str | Path,
    *,
    ceilings_path: str | Path | None = None,
    repo_root: str | Path | None = None,
) -> ValidationResult:
    """Validate a promotion packet → Pass | Fail.

    Schema + same-units + freeze-commit match + artifact-only + ceilings.
    Does not promote; call ``promotion_refuter.refute_promotion_packet`` before
    any sandbox admit.
    """
    if isinstance(packet, (str, Path)):
        raw = json.loads(Path(packet).read_text(encoding="utf-8"))
    else:
        raw = packet
    if not isinstance(raw, dict):
        return _fail("packet_not_object")

    reasons: list[str] = []

    if raw.get("schema_version") != SCHEMA_VERSION:
        reasons.append("schema_version")

    for key in (
        "candidate_id",
        "freeze_commit",
        "observed_freeze_commit",
        "sandbox",
        "claims",
        "gate_attestations",
        "self_tests",
        "operator_budget_approval_id",
    ):
        if key not in raw:
            reasons.append(f"missing:{key}")

    if reasons:
        return _fail(*reasons)

    freeze = raw["freeze_commit"]
    observed = raw["observed_freeze_commit"]
    if not isinstance(freeze, str) or not freeze.strip():
        reasons.append("freeze_commit_empty")
    if not isinstance(observed, str) or not observed.strip():
        reasons.append("observed_freeze_commit_empty")
    if isinstance(freeze, str) and isinstance(observed, str) and freeze != observed:
        reasons.append("freeze_commit_mismatch")

    if not isinstance(raw["candidate_id"], str) or not raw["candidate_id"].strip():
        reasons.append("candidate_id_empty")
    if (
        not isinstance(raw["operator_budget_approval_id"], str)
        or not raw["operator_budget_approval_id"].strip()
    ):
        reasons.append("operator_budget_approval_id_empty")

    sandbox = raw["sandbox"]
    if not isinstance(sandbox, dict):
        reasons.append("sandbox_not_object")
        return _fail(*reasons)

    try:
        ceilings = load_ceilings(ceilings_path)
    except (OSError, ValueError) as exc:
        return _fail(f"ceilings_unreadable:{exc}")

    reasons.extend(_check_sandbox_ceilings(sandbox, ceilings))

    # Optional K-ledger backing check (Rule-0 finding 2026-08-19): when a packet
    # declares which register_search run backs it, verify that run is CLOSED
    # with recorded results before promotion. `discovery_run_id` is not in the
    # required-keys list above -- omitting it keeps today's status quo for
    # packets that predate this check or aren't backed by lab/discovery mining
    # (schema_version is unchanged; this is additive, not a new required field).
    #
    # K-conditional floor cross-check (root-cause finding 2026-08-29): backing
    # confirms a manifest exists and is closed, but says nothing about whether
    # the DSR floor implied by ITS K was ever cleared -- floor_at_k(K) rises
    # fast enough that a backed-but-uncorrected candidate at K above the
    # reachable band (floor_at_k(K) > CAP) can otherwise ride the same
    # unaudited-self-report gap admission_schema.py closes at open time. When
    # that's the case, require a `dsr_floor` gate_attestation whose
    # `hurdle_value` is at least that K's floor -- reusing the attestation slot
    # promotion_packet already validates below, not a new field.
    run_id = raw.get("discovery_run_id")
    required_dsr_floor: float | None = None
    if run_id is not None:
        if not isinstance(run_id, str) or not run_id.strip():
            reasons.append("discovery_run_id_empty")
        else:
            ledger_result = verify_manifest_backing(run_id)
            if not ledger_result.ok:
                reasons.append(f"discovery_run_id_unbacked:{','.join(ledger_result.reasons)}")
            else:
                k = ledger_result.manifest["K"]
                # Deep-lane manifests carry their own confirm_years-conditioned
                # floor in deep_admission (register_search's own charter §2.2
                # computation) -- floor_at_k's default 6.5-year assumption
                # understates the true hurdle for a shorter confirm horizon
                # (e.g. K=10 at confirm_years=3.25 -> floor 1.79, not the
                # default-years 1.265). Reuse the manifest's own recorded
                # value rather than recomputing with the wrong horizon.
                deep_admission = ledger_result.manifest.get("deep_admission")
                if isinstance(deep_admission, dict) and "floor_at_k" in deep_admission:
                    floor = deep_admission["floor_at_k"]
                else:
                    floor = floor_at_k(int(k))
                if floor > CAP:
                    required_dsr_floor = floor

    claims = raw["claims"]
    if not isinstance(claims, list) or not claims:
        reasons.append("claims_empty")
    else:
        for i, claim in enumerate(claims):
            reasons.extend(_check_claim(claim, i))

    attestations = raw["gate_attestations"]
    if not isinstance(attestations, list) or not attestations:
        reasons.append("gate_attestations_empty")
    else:
        for i, att in enumerate(attestations):
            reasons.extend(_check_attestation(att, i))

    if required_dsr_floor is not None and isinstance(attestations, list):
        reasons.extend(_check_k_conditional_floor(attestations, required_dsr_floor))

    reasons.extend(_check_self_tests(raw["self_tests"]))

    # Optional: when repo_root given, require cited artifacts to exist on disk.
    if repo_root is not None and not reasons:
        root = Path(repo_root)
        for claim in claims if isinstance(claims, list) else []:
            if isinstance(claim, dict):
                ap = claim.get("artifact_path")
                if isinstance(ap, str) and ap and not (root / ap).is_file():
                    reasons.append(f"artifact_missing:{ap}")
                rc = claim.get("reexecute_command")
                # command is a string; path existence checked by refuter
                _ = rc
        for att in attestations if isinstance(attestations, list) else []:
            if isinstance(att, dict):
                ap = att.get("artifact_path")
                if isinstance(ap, str) and ap and not (root / ap).is_file():
                    reasons.append(f"artifact_missing:{ap}")

    if reasons:
        return _fail(*reasons)
    return _pass()


def _check_sandbox_ceilings(
    sandbox: dict[str, Any], ceilings: dict[str, Any]
) -> list[str]:
    reasons: list[str] = []
    try:
        micro = int(sandbox["micro_size_contracts"])
        loss = float(sandbox["loss_budget_usd"])
        attempts = int(sandbox["attempt_budget"])
        concurrency = int(sandbox["concurrency_slots"])
    except (KeyError, TypeError, ValueError):
        return ["sandbox_fields_invalid"]

    if micro < 1:
        reasons.append("micro_size_nonpositive")
    if loss <= 0:
        reasons.append("loss_budget_nonpositive")
    if attempts < 1:
        reasons.append("attempt_budget_nonpositive")
    if concurrency < 1:
        reasons.append("concurrency_nonpositive")

    if micro > int(ceilings["max_micro_size_contracts"]):
        reasons.append("ceiling:micro_size_contracts")
    if loss > float(ceilings["max_loss_budget_usd"]):
        reasons.append("ceiling:loss_budget_usd")
    if attempts > int(ceilings["max_attempt_budget"]):
        reasons.append("ceiling:attempt_budget")
    if concurrency > int(ceilings["max_concurrency"]):
        reasons.append("ceiling:concurrency")
    return reasons


def _check_claim(claim: Any, index: int) -> list[str]:
    prefix = f"claim[{index}]"
    if not isinstance(claim, dict):
        return [f"{prefix}:not_object"]
    reasons: list[str] = []
    prose_hits = _FORBIDDEN_PROSE_KEYS & set(claim)
    if prose_hits:
        reasons.append(f"{prefix}:prose_keys:{sorted(prose_hits)}")
    for key in ("claim_id", "metric", "value", "unit", "artifact_path", "reexecute_command"):
        if key not in claim:
            reasons.append(f"{prefix}:missing:{key}")
    unit = claim.get("unit")
    if unit is not None and unit not in ALLOWED_CLAIM_UNITS:
        reasons.append(f"{prefix}:unit_unknown:{unit}")
    ap = claim.get("artifact_path")
    if isinstance(ap, str):
        if not ap.strip():
            reasons.append(f"{prefix}:artifact_path_empty")
        elif ap.startswith(("http://", "https://", "memory:", "chat:")):
            reasons.append(f"{prefix}:artifact_not_reexecutable_path")
    cmd = claim.get("reexecute_command")
    if isinstance(cmd, str) and not cmd.strip():
        reasons.append(f"{prefix}:reexecute_command_empty")
    if "value" in claim and not isinstance(claim["value"], (int, float)):
        reasons.append(f"{prefix}:value_not_numeric")
    return reasons


def _check_attestation(att: Any, index: int) -> list[str]:
    prefix = f"attestation[{index}]"
    if not isinstance(att, dict):
        return [f"{prefix}:not_object"]
    reasons: list[str] = []
    prose_hits = _FORBIDDEN_PROSE_KEYS & set(att)
    if prose_hits:
        reasons.append(f"{prefix}:prose_keys:{sorted(prose_hits)}")
    for key in (
        "gate_id",
        "units",
        "measured_value",
        "hurdle_value",
        "basis",
        "artifact_path",
    ):
        if key not in att:
            reasons.append(f"{prefix}:missing:{key}")
    gate_id = att.get("gate_id")
    units = att.get("units")
    if gate_id is not None and units is not None:
        required = GATE_REQUIRED_UNITS.get(gate_id)
        if required is not None and units != required:
            reasons.append(f"{prefix}:units_mismatch:want_{required}:got_{units}")
        if units not in ALLOWED_CLAIM_UNITS:
            reasons.append(f"{prefix}:unit_unknown:{units}")
    ap = att.get("artifact_path")
    if ap is not None:
        if not isinstance(ap, str) or not ap.strip():
            reasons.append(f"{prefix}:artifact_path_empty")
    basis = att.get("basis")
    if basis is not None:
        if not isinstance(basis, str) or not basis.strip():
            reasons.append(f"{prefix}:basis_empty")
        elif basis in ("present_day", "present_day_convenience", "convenience"):
            reasons.append(f"{prefix}:basis_forbidden:{basis}")
    if "measured_value" in att and not isinstance(att["measured_value"], (int, float)):
        reasons.append(f"{prefix}:measured_value_not_numeric")
    if "hurdle_value" in att and not isinstance(att["hurdle_value"], (int, float)):
        reasons.append(f"{prefix}:hurdle_value_not_numeric")
    return reasons


def _check_k_conditional_floor(attestations: list[Any], required_floor: float) -> list[str]:
    """Require a `dsr_floor` attestation at or above the backing manifest's
    K-conditional floor when that floor exceeds CAP (root-cause finding
    2026-08-29). A missing attestation means the DSR-conditional correction
    this K requires was never even claimed; a present-but-understated one
    means the claim used a stale or wrong-K hurdle -- both are refuse reasons,
    same as any other wrong-units/wrong-basis §R defect this module catches.
    """
    dsr_attestations = [
        att
        for att in attestations
        if isinstance(att, dict) and att.get("gate_id") == "dsr_floor"
    ]
    if not dsr_attestations:
        return [f"discovery_run_id_k_conditional_floor_missing:{required_floor:.4f}"]
    reasons: list[str] = []
    for att in dsr_attestations:
        hurdle = att.get("hurdle_value")
        measured = att.get("measured_value")
        # NaN/inf pass `isinstance(x, (int, float))` and any comparison against
        # NaN is False -- both a NaN/inf hurdle AND a NaN/inf measured_value
        # would otherwise sail through unrejected: a finite-but-fake hurdle
        # paired with a NaN measured value satisfies "hurdle >= floor" while
        # never declaring a real measured Sharpe (Codex review, PR #218,
        # second pass -- _check_attestation and promotion_refuter's own
        # measured<hurdle comparison are equally NaN-blind). math.isfinite
        # rejects NaN, +inf, and -inf alike on both fields.
        if (
            not isinstance(hurdle, (int, float))
            or not math.isfinite(hurdle)
            or not isinstance(measured, (int, float))
            or not math.isfinite(measured)
            or hurdle < required_floor - 1e-9
        ):
            reasons.append(
                f"discovery_run_id_k_conditional_floor_understated:"
                f"{hurdle!r}:{required_floor:.4f}"
            )
    return reasons


def _check_self_tests(self_tests: Any) -> list[str]:
    if not isinstance(self_tests, dict):
        return ["self_tests_missing"]
    reasons: list[str] = []
    for key in ("positive_path", "negative_path", "same_invocation_id"):
        if key not in self_tests:
            reasons.append(f"self_tests:missing:{key}")
    if reasons:
        return reasons
    pos = self_tests["positive_path"]
    neg = self_tests["negative_path"]
    inv = self_tests["same_invocation_id"]
    if not isinstance(pos, str) or not pos.strip():
        reasons.append("self_tests:positive_path_empty")
    if not isinstance(neg, str) or not neg.strip():
        reasons.append("self_tests:negative_path_empty")
    if pos == neg:
        reasons.append("self_tests:positive_negative_identical")
    if not isinstance(inv, str) or not inv.strip():
        reasons.append("self_tests:same_invocation_id_empty")
    return reasons
