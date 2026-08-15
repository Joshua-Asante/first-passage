"""EM corridor + DSR-cap + TNEC N-EDGE admission schema (SPEC S6 / TNEC-1).

Machine-generated refusal at ``register_search open`` — a candidate outside the
ratified eval mechanism-shape corridor, or whose DSR band is empty at catalogue
size, is refused before any spend ($0 / K=0).

> **Superseded-in-part-by** ``docs/adr/2026-08-08-edge-cohort-correction-and-necessity-retarget.md``
> §8 / ``docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md`` (TNEC-1, ``RATIFIED``):
> **EM1** re-typed to necessity via **N-EDGE** (net expectancy > 0 after Req-5 costs + CI
> excluding 0 + DSR ≥ ``floor_at_k``); 0.40R retained as **disclosure only** (frequency
> inversion). **D1/D2** demoted to recorded preferences (report, never gate). EM0 / EM2–EM5
> unchanged as remaining gates. Score intake edge against TNEC N-EDGE, not the historical
> EM1 0.40R kill.

Constants and arithmetic are owned by:
  - EM screen: ``docs/spec/2026-08-05-eval-mechanism-shape-screen.md`` (RATIFIED; EM1 row
    historical — see supersession banner above)
  - Cap / power: ``research_utils.axis_screen`` (harvest-intake ADR §5 freeze)
  - N-EDGE / intake: ``docs/spec/2026-08-08-tradeify-necessary-conditions-target-spec.md``
  - Optional D1/D2 (disclosure only): ``docs/spec/2026-08-06-mnq-daily-cadence-tight-daily-loss-target-spec.md``
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, Literal, Optional

from research_utils.axis_screen import CAP, POWER_MIN, clause_n_power, floor_at_k

Decision = Literal["ADMIT", "REFUSE"]

# EM1 inversion floor — disclosure arithmetic only (TNEC-1). Historical intake kill retired.
EM1_EDGE_FLOOR_R = 0.40

# EM2 ≤1%-bust frontier (edge → max risk USD) — eval_slow_archetype_2026-08-04 §4.2
# Interpolate down, never up (EM screen §2 EM2). Published cells void as provenance; principle stands.
EM2_FRONTIER: tuple[tuple[float, float], ...] = (
    (0.49, 250.0),
    (0.65, 275.0),
    (0.85, 325.0),
)

REASON_CAP_EM0 = "Cap/EM0"
REASON_POWER = "power"
REASON_EM1 = "EM1"  # retained for callers; never appended post–TNEC-1
REASON_EM2 = "EM2"
REASON_EM3 = "EM3"
REASON_EM4 = "EM4"
REASON_EM5 = "EM5"
REASON_D1 = "D1"  # retained for callers; never appended post–TNEC-1
REASON_D2 = "D2"  # retained for callers; never appended post–TNEC-1
REASON_N_EDGE = "N-EDGE"
REASON_K_MISMATCH = "K_mismatch"


@dataclass
class EMAdmission:
    """Declared EM / TNEC limbs for a campaign-open admission check.

    ``catalogue_k`` is EM0 (must match the registered search-space size).
    EM1 (``em1_edge_r``) and ``d1`` / ``d2`` are **disclosure only** — recorded in
    the summary, never refuse reasons (TNEC-1).
    N-EDGE fields (``n_edge_*``) are scored only when supplied; any failing limb
    refuses with ``N-EDGE``.
    EM2 is scored only when its numeric fields are supplied (N-SIZE principle).
    EM3/EM4/EM5 are booleans (refuse when explicitly False).
    ``n_events`` + ``delta_over_sigma`` enable the confirm-power clause when both set.
    """

    catalogue_k: int
    em1_edge_r: Optional[float] = None
    em2_risk_usd: Optional[float] = None
    em2_measured_edge_r: Optional[float] = None
    em3_independence_and_stops: Optional[bool] = None
    em4_weekly_cadence: Optional[bool] = None
    em5_session_slot_legal: Optional[bool] = None
    d1: Optional[bool] = None
    d2: Optional[bool] = None
    n_events: Optional[int] = None
    delta_over_sigma: Optional[float] = None
    # TNEC-1 N-EDGE — net > 0 after Req-5 costs, CI excludes 0, DSR ≥ floor_at_k
    n_edge_net_expectancy: Optional[float] = None
    n_edge_ci_excludes_zero: Optional[bool] = None
    n_edge_dsr: Optional[float] = None


@dataclass(frozen=True)
class AdmissionResult:
    decision: Decision
    reasons: tuple[str, ...]
    summary: dict[str, Any]

    @property
    def admitted(self) -> bool:
        return self.decision == "ADMIT"


def em2_risk_ceiling(measured_edge_r: float) -> float:
    """Edge-indexed EM2 dollar ceiling — interpolate down, never above the top cell."""
    if measured_edge_r <= 0:
        return 0.0
    e0, r0 = EM2_FRONTIER[0]
    if measured_edge_r <= e0:
        return r0 * (measured_edge_r / e0)
    for (ea, ra), (eb, rb) in zip(EM2_FRONTIER, EM2_FRONTIER[1:]):
        if measured_edge_r <= eb:
            t = (measured_edge_r - ea) / (eb - ea)
            return ra + t * (rb - ra)
    return EM2_FRONTIER[-1][1]


def load_admission(path: str | Path) -> EMAdmission:
    """Load an admission JSON object into ``EMAdmission``."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("admission file must be a JSON object")
    allowed = {f.name for f in fields(EMAdmission)}
    unknown = set(raw) - allowed
    if unknown:
        raise ValueError(f"admission file has unknown keys: {sorted(unknown)}")
    if "catalogue_k" not in raw:
        raise ValueError("admission file missing required field 'catalogue_k'")
    return EMAdmission(**{k: raw[k] for k in allowed if k in raw})


def _disclosure_record(admission: EMAdmission) -> dict[str, Any]:
    """EM1 / D1 / D2 are recorded preferences — never refuse reasons (TNEC-1)."""
    out: dict[str, Any] = {}
    if admission.em1_edge_r is not None:
        edge = float(admission.em1_edge_r)
        out["em1_edge_r"] = edge
        out["em1_below_inversion_floor"] = edge < EM1_EDGE_FLOOR_R
    if admission.d1 is not None:
        out["d1"] = admission.d1
    if admission.d2 is not None:
        out["d2"] = admission.d2
    return out


def evaluate_admission(
    admission: EMAdmission,
    *,
    registered_k: int,
) -> AdmissionResult:
    """Return ADMIT or REFUSE with reason codes (SPEC S6 + TNEC-1).

    Refuses when ``floor_at_k(K) > CAP`` (empty DSR band; K≥4 at current Cap),
    when confirm-power inputs are supplied and power < ``POWER_MIN``, when a
    supplied N-EDGE limb fails, or when any remaining EM gate limb fails
    (EM0 / EM2–EM5). EM1 and D1/D2 are disclosure-only and never refuse.
    Does not spend K and does not write a manifest.
    """
    reasons: list[str] = []
    floor = floor_at_k(registered_k)
    power: Optional[float] = None

    if admission.catalogue_k != registered_k:
        reasons.append(REASON_K_MISMATCH)

    if floor > CAP:
        reasons.append(REASON_CAP_EM0)

    if admission.n_events is not None and admission.delta_over_sigma is not None:
        if (
            not isinstance(admission.n_events, int)
            or isinstance(admission.n_events, bool)
            or admission.n_events <= 0
        ):
            reasons.append(REASON_POWER)
        else:
            power = clause_n_power(admission.n_events, float(admission.delta_over_sigma))
            if power < POWER_MIN:
                reasons.append(REASON_POWER)

    # TNEC-1 N-EDGE — scored when supplied; replaces EM1 as the edge intake kill
    n_edge_fail = False
    if admission.n_edge_net_expectancy is not None:
        if float(admission.n_edge_net_expectancy) <= 0:
            n_edge_fail = True
    if admission.n_edge_ci_excludes_zero is False:
        n_edge_fail = True
    if admission.n_edge_dsr is not None:
        if float(admission.n_edge_dsr) < floor:
            n_edge_fail = True
    if n_edge_fail:
        reasons.append(REASON_N_EDGE)

    # EM1 / D1 / D2 — disclosure only (recorded below; never append to reasons)

    if admission.em2_risk_usd is not None:
        if admission.em2_measured_edge_r is None:
            reasons.append(REASON_EM2)
        else:
            ceiling = em2_risk_ceiling(float(admission.em2_measured_edge_r))
            if float(admission.em2_risk_usd) > ceiling:
                reasons.append(REASON_EM2)

    if admission.em3_independence_and_stops is False:
        reasons.append(REASON_EM3)
    if admission.em4_weekly_cadence is False:
        reasons.append(REASON_EM4)
    if admission.em5_session_slot_legal is False:
        reasons.append(REASON_EM5)

    decision: Decision = "REFUSE" if reasons else "ADMIT"
    summary = {
        "decision": decision,
        "reasons": list(reasons),
        "catalogue_k": admission.catalogue_k,
        "registered_k": registered_k,
        "floor_at_k": floor,
        "cap": CAP,
        "power": None if power is None else round(power, 6),
        "power_min": POWER_MIN,
        "limbs": asdict(admission),
        "disclosures": _disclosure_record(admission),
    }
    return AdmissionResult(decision=decision, reasons=tuple(reasons), summary=summary)
