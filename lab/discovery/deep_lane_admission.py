"""deep_lane_admission.py — deep-iteration-lane charter §2.2 admission predicate.

Charter: docs/adr/2026-08-16-deep-iteration-lane-charter.md (Accepted 2026-08-16).
Build authorization: docs/adr/2026-08-22-grow-lane-build-authorization.md.

Charter §2.2 refuses a lane prereg at freeze unless all three conjuncts hold:
  (i)   K <= 33 -- M-19's Guardian-quality crossing, a hard literal (blocks the
        long-confirm back door: floor_at_k alone would admit K ~= 2000 on a
        6.5-year confirm).
  (ii)  floor_at_k(K, confirm_years) <= 2.0 -- the overfit-suspect-zone wall
        (M-19: SR > 2 is a forbidden move regardless of K).
  (iii) power >= POWER_MIN (0.50) against the campaign's own declared
        target_sr (Gaussian approx., se ~= 1/sqrt(years), per the charter's
        own §2.2(iii) text) -- a prereg whose target cannot clear its own
        floor at >=0.50 power is refused, not disclosed-and-waved-through.

This is a SEPARATE predicate from S6/admission_schema.py's mechanism-first
corridor (which refuses K>=4 against CAP=1.0 for one-shot channels). The two
never share a threshold and this module does not import from that one --
conflating them would be exactly the K-doctrine collision the 2026-08-22
dual-panel review found in GROW spec v1.

floor_at_k / POWER_MIN are reused verbatim from axis_screen.py (charter §0
Rule-0 citation) -- never re-derived here.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from research_utils.axis_screen import POWER_MIN, floor_at_k

Decision = "ADMIT | REFUSE"  # documentation only; see AdmissionResult.decision

# Charter §2.2(i) -- M-19 Guardian-quality crossing, hard literal.
K_CEILING = 33

# Charter §2.2(ii) -- M-19 overfit-suspect zone (SR > 2), hard literal.
FLOOR_CEILING = 2.0

REASON_K_ABOVE_CEILING = "K_ABOVE_CEILING"
REASON_FLOOR_ABOVE_CEILING = "FLOOR_ABOVE_CEILING"
REASON_POWER_BELOW_MIN = "POWER_BELOW_MIN"


@dataclass(frozen=True)
class DeepLaneAdmission:
    """Declared fields for a deep-lane campaign prereg's §2.2 predicate check.

    ``declared_k`` is the full variant budget (charter §2.2: "every variant
    available to be chosen counts" -- D-K1's "the wider exploration is the K"
    imported verbatim; retroactive/under-declared K voids the prereg, but that
    discipline is enforced at prereg-authoring time, not by this module).
    ``target_sr`` is the campaign's own design-target annualized Sharpe, named
    a priori in the prereg (charter §2.2(iii)) -- never fit to data.
    """

    declared_k: int
    confirm_years: float
    target_sr: float


@dataclass(frozen=True)
class AdmissionResult:
    decision: str
    reasons: tuple[str, ...]
    summary: dict[str, Any]

    @property
    def admitted(self) -> bool:
        return self.decision == "ADMIT"


def deep_lane_power(*, target_sr: float, floor_sr: float, years: float) -> float:
    """Gaussian-approx pass probability, charter §2.2(iii) verbatim.

    se ~= 1/sqrt(years) (annualized-Sharpe estimator SE, ignoring the
    skew/kurtosis correction terms floor_at_k's own DSR machinery already
    prices into ``floor_sr``); power = Phi((target_sr - floor_sr) * sqrt(years)).

    Reproduces the charter's own worked example exactly: target=1.83,
    floor=1.475 (K=33, 6.5y) -> power ~= 0.82; target == floor -> power == 0.50
    (boundary-admissible).
    """
    if years <= 0:
        raise ValueError("years must be positive")
    z = (target_sr - floor_sr) * math.sqrt(years)
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def evaluate_deep_admission(admission: DeepLaneAdmission) -> AdmissionResult:
    """Return ADMIT or REFUSE with reason codes for charter §2.2.

    All three conjuncts are evaluated (not short-circuited) so a prereg that
    fails on more than one axis sees every failing reason at once, matching
    the house style of admission_schema.evaluate_admission.
    """
    k = admission.declared_k
    if not isinstance(k, int) or isinstance(k, bool) or k < 1:
        raise ValueError("declared_k must be a positive int")
    if admission.confirm_years <= 0:
        raise ValueError("confirm_years must be positive")

    floor = floor_at_k(k, years=admission.confirm_years)
    power = deep_lane_power(
        target_sr=admission.target_sr, floor_sr=floor, years=admission.confirm_years
    )

    reasons: list[str] = []
    if k > K_CEILING:
        reasons.append(REASON_K_ABOVE_CEILING)
    if floor > FLOOR_CEILING:
        reasons.append(REASON_FLOOR_ABOVE_CEILING)
    if power < POWER_MIN:
        reasons.append(REASON_POWER_BELOW_MIN)

    decision = "REFUSE" if reasons else "ADMIT"
    summary = {
        "decision": decision,
        "reasons": list(reasons),
        "declared_k": k,
        "k_ceiling": K_CEILING,
        "confirm_years": admission.confirm_years,
        "floor_at_k": floor,
        "floor_ceiling": FLOOR_CEILING,
        "target_sr": admission.target_sr,
        "power": round(power, 6),
        "power_min": POWER_MIN,
    }
    return AdmissionResult(decision=decision, reasons=tuple(reasons), summary=summary)
