"""Tradeify fixed-book protection and sizing law for offline replay — Track B.

Owner of the values: docs/notes/2026-09-10-tradeify-protection-selection.md
(the operator-accepted book and policy) and the Track B umbrella
docs/briefs/handoffs/2026-09-10-track-b-qualify-accepted-book-umbrella.md
(TB-S1 (A)-(F), D-B7, D-B8, D-B10, D-B11, D-B14). This module is the
executable expression of those rules for replay and offline tests. It is NOT
a `POLICY_REGISTRY` row: the 1%/40% instance stays a threaded candidate
value until TB-D0 lands the admitting ADR (D-B11; core/dd_geometry.py
lines 88-91). The frozen FXIFY-C2 literals in core/dd_protection.py are not
read, not edited and not re-expressed here — `calculate_protection` is
hard-wired to DD_TRIGGER=0.015 and cannot evaluate a 1% trigger, so the
threshold compare is re-stated below with the same ULP rounding
(docs/adr/2026-05-10-dd-protection-ulp-rounding.md).

Rules (each with the selection-note / umbrella sentence it implements):

* Trigger: ``protected = round((peak - equity) / peak, 6) >= 0.01`` on the
  combined account's own running equity peak. "Re-evaluate daily ... no latch".
* Timing: the mode for weekday D is computed once from the settled close of
  the prior trading day (TB-S1 (B)); intraday equity never changes it; a loss
  that first crosses the trigger is not retroactively reduced.
* Quantities (TB-S1, ruled O-1/O-5/O-6): Striker scales risk before its floor
  and cap; Aegis scales fixed quantity; Vanguard uses quantity-floor and is
  disabled below AUTHORIZED. Adds derive from confirmed base with per-leg
  rounding. ORB base stays one micro and protected adds are refused. Call-4
  remains off-rail. Candidate calculations do not admit or deploy the policy.
* No policy -> halt (TB-S1 (A)): nothing here defaults a trigger or scale.

Integer arithmetic uses exact rationals so the D-B10 floor can never be
moved by a binary64 product (the #332 hazard).
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
for _p in (str(_REPO_ROOT / "core"), str(_REPO_ROOT / "ops")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dd_geometry import POLICY_REGISTRY, ProtectionPolicy  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from lib.validation import require_finite_number  # noqa: E402
from lifecycle import TIER_MULTIPLIER  # noqa: E402
from c1_signal_daemon.book_protocol import Mode, Side  # noqa: E402

TIER = "Tradeify_Select_100K"
ACCOUNT_MICRO_CAP: int = int(FIRM_RULES[TIER]["micro_contract_cap"])  # 80

CANDIDATE_TRIGGER = "0.01"
CANDIDATE_SCALE = "0.40"
CANDIDATE_PROVENANCE = (
    "CANDIDATE - unadmitted; operator selection 2026-09-10 "
    "(docs/notes/2026-09-10-tradeify-protection-selection.md); admission only "
    "via umbrella D-B11 (TB-P2 ADR, TB-D0 registry row after TB-E1)"
)


class PolicyAbsent(RuntimeError):
    """No explicit protection policy was supplied: the sizing path halts."""


def candidate_book_protection_policy() -> ProtectionPolicy:
    """The threaded candidate value. Never inserted into POLICY_REGISTRY here.

    ``reference_mode="trailing"``: the selection measures drawdown against the
    account's own RUNNING equity peak (a ratcheting %-of-peak floor), which is
    dd_geometry's "trailing" geometry. The eval's ``dd_type`` is
    ``trailing_locking`` with an unreachable lock offset (core/firm_rules.py),
    so the locking mode degenerates to trailing for this instance.
    """
    return ProtectionPolicy(
        reference_mode="trailing",
        trigger=float(Fraction(CANDIDATE_TRIGGER)),
        scale=float(Fraction(CANDIDATE_SCALE)),
        provenance=CANDIDATE_PROVENANCE,
    )


class PolicyMismatch(RuntimeError):
    """A policy other than the fixed 1%/40% trailing instance was threaded: halt."""


def require_policy(policy: ProtectionPolicy | None) -> ProtectionPolicy:
    """Only the fixed instance is executable here (D-B4 (a), D-B11): a different
    trigger, scale or reference mode would move the risk-control boundary, so it
    halts instead of being honoured."""
    if policy is None:
        raise PolicyAbsent(
            "no protection policy supplied; the book sizing path halts rather "
            "than defaulting a trigger/scale (TB-S1 (A))")
    if not isinstance(policy, ProtectionPolicy):
        raise PolicyAbsent(f"policy must be a ProtectionPolicy, got {type(policy).__name__}")
    if (Fraction(str(policy.trigger)) != Fraction(CANDIDATE_TRIGGER)
            or Fraction(str(policy.scale)) != Fraction(CANDIDATE_SCALE)
            or policy.reference_mode != "trailing"):
        raise PolicyMismatch(
            f"policy ({policy.reference_mode}, trigger={policy.trigger}, scale={policy.scale}) "
            f"is not the fixed book instance (trailing, {CANDIDATE_TRIGGER}, {CANDIDATE_SCALE}); halting")
    return policy


def drawdown_from_peak(equity: float, peak: float) -> float:
    equity = require_finite_number(equity, field="equity", minimum=0.0)
    peak = require_finite_number(peak, field="peak", strictly_positive=True)
    return (peak - equity) / peak if equity < peak else 0.0


def is_protected(equity: float, peak: float, policy: ProtectionPolicy | None) -> bool:
    """Selection-note formula, ULP rounding before the compare."""
    policy = require_policy(policy)
    return round(drawdown_from_peak(equity, peak), 6) >= policy.trigger


# ── the fixed book ───────────────────────────────────────────────────────

MICRO_EQUIVALENT: dict[str, int] = {"6J": 10, "MGC": 1, "MYM": 1, "MNQ": 1}


class ProtectedRule(str, Enum):
    SCALE = "scale"                          # floor(scale x normal) per tier
    BASE_FIXED_ADDS_OFF = "base_fixed_adds_off"  # ORB: base unchanged, adds not placed


@dataclass(frozen=True)
class LegSpec:
    leg_id: str
    symbol: str
    order_symbol: str          # provisional continuous-contract notation (TB-S3 (B))
    entry_side: Side           # D-B7 allowed_entry_side
    priority: int              # D-B8: 1 = highest (Aegis)
    protected_rule: ProtectedRule
    normal_base_values: tuple[int, ...]   # every base quantity the captured setting can reach
    add_pct: int               # pyramid add as % of the base (0 = no adds)
    add_rounding: str          # "floor" (Pine math.floor) | "round" (Pine math.round) | "none"
    max_adds: int
    pine_sha256: str
    lifecycle_key: str

    @property
    def micro_equiv(self) -> int:
        return MICRO_EQUIVALENT[self.symbol]

    def normal_add(self, base: int) -> int:
        """The captured Pine's add quantity for a given base (0 when no adds)."""
        if self.add_pct == 0 or self.max_adds == 0:
            return 0
        raw = Fraction(base * self.add_pct, 100)
        if self.add_rounding == "floor":
            return int(math.floor(raw))
        if self.add_rounding == "round":
            # Pine math.round: half away from zero.
            return int(math.floor(raw + Fraction(1, 2)))
        raise ValueError(f"unknown add_rounding {self.add_rounding!r}")


# Order = D-B8 priority (Aegis 6J -> Striker MYM -> Vanguard MGC -> ORB MNQ).
# Sources: selection note "Selected book" table; phase1_config.json pine_sha256;
# each captured export's observed quantities (parity harness) for the base
# ladders. Striker's ladder is the Pine law min(floor($700 / (stop x $0.50)),
# floor(80 / 3.5)) = 1..22; Vanguard's cap-2 law reaches 1 or 2; Aegis' cap-8
# law reaches 1..8 in Pine but the rail expresses the captured 8-contract
# setting as a fixed quantity (TB-S1 (F)).
BOOK_LEGS: tuple[LegSpec, ...] = (
    LegSpec("aegis_6j", "6J", "6J1!", Side.SELL, 1, ProtectedRule.SCALE,
            normal_base_values=(8,), add_pct=0, add_rounding="none", max_adds=0,
            pine_sha256="db78ecba95ae78aca14501a5eaccfda2a42164d83cac12321cb7f293a9adca7c",
            lifecycle_key="Aegis 6J"),
    LegSpec("dj30_mym_p250", "MYM", "MYM1!", Side.BUY, 2, ProtectedRule.SCALE,
            normal_base_values=tuple(range(1, 23)), add_pct=250, add_rounding="floor",
            max_adds=1,
            pine_sha256="712cf395396568ce22ae43f1f15b085eaba23acf1b85502abb92129f277fffd7",
            lifecycle_key="Striker MYM p250"),
    LegSpec("vanguard_mgc", "MGC", "MGC1!", Side.BUY, 3, ProtectedRule.SCALE,
            normal_base_values=(1, 2), add_pct=80, add_rounding="round", max_adds=2,
            pine_sha256="af26899ca94bb0e9ee26d09e0176b6b94bba2f5da252399ce4d899fe7e3bad15",
            lifecycle_key="Vanguard MGC"),
    LegSpec("orb_mnq_v7", "MNQ", "MNQ1!", Side.BUY, 4, ProtectedRule.BASE_FIXED_ADDS_OFF,
            normal_base_values=(1,), add_pct=100, add_rounding="round", max_adds=2,
            pine_sha256="176c4f70c67d58053c4d3b8170d0a9be3733bc6b76b1e2f928bd7a877be052a3",
            lifecycle_key="ORB MNQ v7"),
)
LEG_BY_ID: dict[str, LegSpec] = {leg.leg_id: leg for leg in BOOK_LEGS}
RETIRED_LEG_IDS = frozenset({"dj30_mym", "nas100_mnq"})  # never reused (TB-S3 (B))


def leg(leg_id: str) -> LegSpec:
    if leg_id in RETIRED_LEG_IDS:
        raise KeyError(f"{leg_id!r} is a retired leg id; the fixed book uses {sorted(LEG_BY_ID)}")
    try:
        return LEG_BY_ID[leg_id]
    except KeyError:
        raise KeyError(f"unknown leg_id {leg_id!r}; fixed book: {sorted(LEG_BY_ID)}") from None


# ── quantities ───────────────────────────────────────────────────────────

def as_mode(mode) -> Mode:
    """Accept a Mode or its serialized value; anything else halts (never 'normal' by default)."""
    if isinstance(mode, Mode):
        return mode
    try:
        return Mode(mode)
    except (ValueError, TypeError):
        raise ValueError(f"unknown protection mode {mode!r}; valid: {[m.value for m in Mode]}") from None


def lifecycle_multiplier(tier: str) -> Fraction:
    if tier not in TIER_MULTIPLIER:
        raise ValueError(f"unknown lifecycle tier {tier!r}; valid: {sorted(TIER_MULTIPLIER)}")
    return Fraction(str(TIER_MULTIPLIER[tier]))


def _positive_risk(value: object, field_name: str) -> Fraction:
    """Preserve rational/decimal inputs; reject bool, strings and nonfinite data."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction, Decimal)):
        raise ValueError(f"{field_name} must be a positive finite risk number")
    try:
        result = Fraction(str(value)) if isinstance(value, float) else Fraction(value)
    except (ValueError, OverflowError) as exc:
        raise ValueError(f"{field_name} must be a positive finite risk number") from exc
    if result <= 0:
        raise ValueError(f"{field_name} must be a positive finite risk number")
    return result


def add_quantity(leg_id: str, confirmed_base: int, *, mode: Mode,
                 policy: ProtectionPolicy | None, lifecycle_tier: str) -> int:
    """Per-tier add from confirmed base, never from intended or normal add size.

    The caller must obtain base evidence from the execution owner; this pure
    function neither verifies broker evidence nor reserves account capacity.
    A nonzero lifecycle haircut has already affected the executed base and
    must not be applied a second time. Current zero-authorization/mode gates
    still refuse new adds without resizing the carried base.
    """
    spec = leg(leg_id)
    require_policy(policy)
    mode = as_mode(mode)
    multiplier = lifecycle_multiplier(lifecycle_tier)
    if type(confirmed_base) is not int or not 0 <= confirmed_base <= max(spec.normal_base_values):
        raise ValueError(f"{leg_id}: invalid confirmed base {confirmed_base!r}")
    if confirmed_base == 0 or multiplier == 0 or spec.max_adds == 0:
        return 0
    if leg_id in {"vanguard_mgc", "orb_mnq_v7"}:
        if lifecycle_tier != "AUTHORIZED" or mode is Mode.PROTECTED:
            return 0
    return spec.normal_add(confirmed_base)


def entry_quantities(leg_id: str, *, mode: Mode, policy: ProtectionPolicy | None,
                     lifecycle_tier: str, normal_base: int | None = None,
                     risk_dollars: object = None, per_contract_risk: object = None,
                     cap_alloc: int | None = None) -> tuple[int, int]:
    """Requested base and prospective add *assuming a complete base fill*.

    Striker requires unscaled risk dollars, per-contract risk and an explicit
    allocation. A rounded normal quantity cannot recover those inputs. For
    an actual add, call add_quantity with the confirmed base instead of using
    this prospective tuple.
    """
    spec = leg(leg_id)
    require_policy(policy)
    mode = as_mode(mode)
    lifecycle = lifecycle_multiplier(lifecycle_tier)
    scale = Fraction(CANDIDATE_SCALE) if mode is Mode.PROTECTED else Fraction(1)
    if leg_id == "dj30_mym_p250":
        if normal_base is not None and (type(normal_base) is not int or not 0 <= normal_base <= 22):
            raise ValueError("Striker normal_base diagnostic must be an integer in 0..22")
        risk = _positive_risk(risk_dollars, "risk_dollars")
        denominator = _positive_risk(per_contract_risk, "per_contract_risk")
        if type(cap_alloc) is not int or not 0 <= cap_alloc <= ACCOUNT_MICRO_CAP:
            raise ValueError("cap_alloc must be an explicit integer within the account cap")
        risk_term = risk * scale * lifecycle / denominator
        cap_term = Fraction(cap_alloc) / (1 + Fraction(spec.add_pct, 100))
        base = min(math.floor(risk_term), math.floor(cap_term))
    elif leg_id == "vanguard_mgc":
        if type(normal_base) is not int or normal_base not in spec.normal_base_values:
            raise ValueError("vanguard_mgc requires normal_base 1 or 2")
        base = math.floor(normal_base * scale) if lifecycle_tier == "AUTHORIZED" else 0
    else:
        fixed_base = spec.normal_base_values[0]
        if normal_base is not None and (type(normal_base) is not int or normal_base != fixed_base):
            raise ValueError(f"{leg_id}: normal_base must equal fixed quantity {fixed_base}")
        applied_scale = Fraction(1) if leg_id == "orb_mnq_v7" else scale
        base = math.floor(fixed_base * applied_scale * lifecycle)
    return base, add_quantity(leg_id, base, mode=mode, policy=policy,
                              lifecycle_tier=lifecycle_tier)


def leg_quantities(leg_id: str, normal_base: int, *, mode: Mode, policy: ProtectionPolicy | None,
                   lifecycle_tier: str = "AUTHORIZED", risk_dollars: object = None,
                   per_contract_risk: object = None, cap_alloc: int | None = None) -> tuple[int, int]:
    """Compatibility for offline callers; Striker requires explicit risk inputs.

    New account consumers use entry_quantities with explicit authorization.
    The legacy normal-integer-only Striker callback now fails closed.
    """
    spec = leg(leg_id)
    if type(normal_base) is not int or normal_base not in spec.normal_base_values:
        raise ValueError(f"{leg_id}: normal base {normal_base!r} outside captured ladder")
    return entry_quantities(leg_id, normal_base=normal_base, mode=mode, policy=policy,
                            lifecycle_tier=lifecycle_tier, risk_dollars=risk_dollars,
                            per_contract_risk=per_contract_risk, cap_alloc=cap_alloc)


# ── timing: prior-close mode selection ───────────────────────────────────

@dataclass
class BookProtectionClock:
    """Mode for a session from the prior settled close; peak = account's own EOD peak.

    The initial state is FROZEN by the caller (TB-S1 (B)): equity and peak as
    of the run's start (pristine for TB-E1 screening; the B7 snapshot's
    historical_eod_peak for TB-E2). No run may start without one.
    """

    policy: ProtectionPolicy
    initial_equity: float
    initial_peak: float
    peak: float = field(init=False)
    last_close_equity: float = field(init=False)
    last_settled_date: date | None = field(init=False, default=None)
    _mode_next: Mode = field(init=False)
    history: list[dict] = field(init=False, default_factory=list)

    def __post_init__(self) -> None:
        self.policy = require_policy(self.policy)
        eq = require_finite_number(self.initial_equity, field="initial_equity", strictly_positive=True)
        pk = require_finite_number(self.initial_peak, field="initial_peak", strictly_positive=True)
        if pk < eq:
            raise ValueError("initial_peak must be >= initial_equity")
        self.peak = pk
        self.last_close_equity = eq
        self._mode_next = Mode.PROTECTED if is_protected(eq, pk, self.policy) else Mode.NORMAL

    def settle(self, session_date: date, close_equity: float) -> Mode:
        """Record a settled close; returns the mode that governs the NEXT session."""
        if self.last_settled_date is not None and session_date <= self.last_settled_date:
            raise ValueError(f"settle dates must advance: {session_date} <= {self.last_settled_date}")
        eq = require_finite_number(close_equity, field="close_equity", minimum=0.0)
        self.peak = max(self.peak, eq)          # EOD peak ratchet
        self.last_close_equity = eq
        self.last_settled_date = session_date
        protected = is_protected(eq, self.peak, self.policy)
        self._mode_next = Mode.PROTECTED if protected else Mode.NORMAL   # no latch
        self.history.append({
            "date": session_date.isoformat(), "equity": eq, "peak": self.peak,
            "dd_from_peak": round(drawdown_from_peak(eq, self.peak), 6),
            "mode_next": self._mode_next.value,
        })
        return self._mode_next

    def mode_for(self, session_date: date) -> Mode:
        """Mode governing `session_date`: from the last settle strictly before it."""
        if self.last_settled_date is not None and session_date <= self.last_settled_date:
            raise ValueError(f"{session_date} is not after the last settled close "
                             f"{self.last_settled_date}; intraday equity never changes the mode")
        return self._mode_next

    def snapshot(self) -> dict:
        """Serialized state; ``mode_next`` is the Mode's value — pass it back through ``as_mode``."""
        return {"peak": self.peak, "last_close_equity": self.last_close_equity,
                "last_settled_date": (self.last_settled_date.isoformat()
                                      if self.last_settled_date else None),
                "mode_next": self._mode_next.value}


# ── governance self-checks used by tests ─────────────────────────────────

def frozen_surfaces_untouched() -> dict:
    """The candidate never lands in the registry; dd_protection constants stay pinned."""
    import dd_protection  # noqa: WPS433 (import-time MVD pins the constants)
    return {
        "DD_TRIGGER": dd_protection.DD_TRIGGER,
        "DD_SCALE": dd_protection.DD_SCALE,
        "registry_empty": len(POLICY_REGISTRY) == 0,
    }
