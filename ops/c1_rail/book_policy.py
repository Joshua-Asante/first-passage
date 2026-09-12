"""Tradeify fixed-book protection, capacity and sizing rules — Track B.

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
* Quantities (TB-S1 (C), D-B10 floor): protected size for Aegis / Vanguard /
  Striker MYM = floor(0.40 x normal) per tier, incl. every add tier; ORB base
  stays 1 micro and ORB adds are not placed while protected. Lifecycle tiers
  (D-B14 (a)) compound multiplicatively before the floor.
* Carried positions (TB-S1 (D)): a position open at a transition keeps its
  size; never a resize order; resting ORB adds are cancelled on activation.
* Capacity (TB-S1 (E), D-B8): micro-equivalents 6J=10, MGC/MYM/MNQ=1; the
  account cap (80) counts confirmed positions plus reservations; refuse, never
  clip; only the top-priority leg (Aegis) may displace lower-priority whole
  legs, lowest first, through an atomic fail-closed takeover.
* No policy -> halt (TB-S1 (A)): nothing here defaults a trigger or scale.

Integer arithmetic uses exact rationals so the D-B10 floor can never be
moved by a binary64 product (the #332 hazard).
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import Iterable

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

def lifecycle_multiplier(tier: str) -> Fraction:
    if tier not in TIER_MULTIPLIER:
        raise ValueError(f"unknown lifecycle tier {tier!r}; valid: {sorted(TIER_MULTIPLIER)}")
    return Fraction(str(TIER_MULTIPLIER[tier]))


def scaled_quantity(normal_qty: int, *, mode: Mode, policy: ProtectionPolicy | None,
                    lifecycle_tier: str = "AUTHORIZED") -> int:
    """D-B10: floor(normal x scale x lifecycle), exact rationals, never a float floor."""
    policy = require_policy(policy)
    if not isinstance(normal_qty, int) or normal_qty < 0:
        raise ValueError(f"normal_qty must be a non-negative int, got {normal_qty!r}")
    scale = Fraction(CANDIDATE_SCALE) if mode is Mode.PROTECTED else Fraction(1)
    if mode is Mode.PROTECTED and Fraction(str(policy.scale)) != scale:
        raise ValueError(f"policy scale {policy.scale} is not the fixed {CANDIDATE_SCALE}")
    return int(math.floor(Fraction(normal_qty) * scale * lifecycle_multiplier(lifecycle_tier)))


def leg_quantities(leg_id: str, normal_base: int, *, mode: Mode, policy: ProtectionPolicy | None,
                   lifecycle_tier: str = "AUTHORIZED") -> tuple[int, int]:
    """(base, add) contracts the leg may place today for a captured normal base.

    ORB: base unchanged (1 micro), adds 0 while protected. Others: every tier
    floored from its own normal value (TB-S1 (C) 'including every add tier').
    """
    spec = leg(leg_id)
    if normal_base not in spec.normal_base_values:
        raise ValueError(f"{leg_id}: normal base {normal_base} not in the captured ladder "
                         f"{spec.normal_base_values}")
    policy = require_policy(policy)
    normal_add = spec.normal_add(normal_base)
    if spec.protected_rule is ProtectedRule.BASE_FIXED_ADDS_OFF:
        base = scaled_quantity(normal_base, mode=Mode.NORMAL, policy=policy,
                               lifecycle_tier=lifecycle_tier)
        if mode is Mode.PROTECTED:
            return base, 0
        add = scaled_quantity(normal_add, mode=Mode.NORMAL, policy=policy,
                              lifecycle_tier=lifecycle_tier)
        return base, add
    base = scaled_quantity(normal_base, mode=mode, policy=policy, lifecycle_tier=lifecycle_tier)
    add = scaled_quantity(normal_add, mode=mode, policy=policy, lifecycle_tier=lifecycle_tier)
    return base, add


@dataclass(frozen=True)
class QuantityRow:
    leg_id: str
    normal_base: int
    normal_add: int
    lifecycle_tier: str
    mode: Mode
    base: int
    add: int


def quantity_table(policy: ProtectionPolicy | None,
                   lifecycle_tiers: Iterable[str] = ("AUTHORIZED", "WATCH-1", "WATCH-2")
                   ) -> list[QuantityRow]:
    """The explicit integer table (TB-S1 (C)) — every leg, ladder value, tier, mode."""
    policy = require_policy(policy)
    rows: list[QuantityRow] = []
    for spec in BOOK_LEGS:
        for nb in spec.normal_base_values:
            for tier in lifecycle_tiers:
                for mode in (Mode.NORMAL, Mode.PROTECTED):
                    b, a = leg_quantities(spec.leg_id, nb, mode=mode, policy=policy,
                                          lifecycle_tier=tier)
                    rows.append(QuantityRow(spec.leg_id, nb, spec.normal_add(nb), tier, mode, b, a))
    return rows


def reachable_quantity_menu(policy: ProtectionPolicy | None) -> dict[str, dict[str, set[int]]]:
    """Distinct reachable (leg -> kind -> quantities), the input to TB-R2's export menu."""
    menu: dict[str, dict[str, set[int]]] = {}
    for row in quantity_table(policy):
        kinds = menu.setdefault(row.leg_id, {"base": set(), "add": set()})
        if row.base > 0:
            kinds["base"].add(row.base)
        if row.base > 0 and row.add > 0:
            kinds["add"].add(row.add)
    return menu


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
        return {"peak": self.peak, "last_close_equity": self.last_close_equity,
                "last_settled_date": (self.last_settled_date.isoformat()
                                      if self.last_settled_date else None),
                "mode_next": self._mode_next.value}


# ── carried positions ─────────────────────────────────────────────────────

def transition_cancels(previous: Mode, new: Mode, resting_orb_adds: Iterable[str]) -> list[str]:
    """TB-S1 (D): entering PROTECTED cancels resting ORB adds; nothing is ever resized."""
    if previous is not Mode.PROTECTED and new is Mode.PROTECTED:
        return list(resting_orb_adds)
    return []


# ── capacity ─────────────────────────────────────────────────────────────

class CapacityError(RuntimeError):
    pass


@dataclass(frozen=True)
class TakeoverPlan:
    requester: str
    contracts: int
    displaced: tuple[str, ...]      # lowest priority first, whole legs


@dataclass(frozen=True)
class CapacityDecision:
    admitted: bool
    reason: str
    micro_used_before: int
    micro_requested: int
    takeover: TakeoverPlan | None = None


@dataclass
class Takeover:
    """Atomic, fail-closed priority takeover (TB-S1 (E), TB-S3 (E), D-B8).

    Sequence per displaced leg: cancel pending -> broker cancel ack -> close
    -> broker-confirmed ZERO position. Only when every displaced leg is acked
    and confirmed flat does the ledger reconcile and admit the requester. Any
    unacked cancel, partial/rejected/unknown/timed-out close refuses the
    requester; the ledger never admits an order that could exceed the cap if a
    displaced order later fills.
    """

    plan: TakeoverPlan
    state: str = "pending"            # pending | admitted | refused
    cancel_acked: set[str] = field(default_factory=set)
    closed_confirmed: set[str] = field(default_factory=set)
    confirmed_positions: dict[str, int] = field(default_factory=dict)   # every broker-reported position
    events: list[dict] = field(default_factory=list)
    refuse_reason: str | None = None

    def _event(self, kind: str, **detail) -> None:
        self.events.append({"kind": kind, "requester": self.plan.requester, **detail})

    def ack_cancel(self, leg_id: str) -> None:
        self._require_pending()
        self._require_displaced(leg_id)
        self.cancel_acked.add(leg_id)
        self._event("capacity_takeover_cancel_ack", leg_id=leg_id)

    def confirm_close(self, leg_id: str, confirmed_position: int) -> None:
        self._require_pending()
        self._require_displaced(leg_id)
        if confirmed_position < 0:
            raise CapacityError("confirmed position must be >= 0")
        self.confirmed_positions[leg_id] = confirmed_position   # broker truth is kept even on refusal
        if leg_id not in self.cancel_acked:
            self.fail(leg_id, "close reported before the leg's cancel was acknowledged")
            return
        if confirmed_position != 0:
            self.fail(leg_id, f"close not flat: broker-confirmed position {confirmed_position}")
            return
        self.closed_confirmed.add(leg_id)
        self._event("capacity_takeover_close_confirmed", leg_id=leg_id)

    def fail(self, leg_id: str, reason: str) -> None:
        self._require_pending()
        self.state = "refused"
        self.refuse_reason = f"{leg_id}: {reason}"
        self._event("capacity_takeover_refused", leg_id=leg_id, reason=reason)

    def complete(self) -> bool:
        return (self.state == "pending"
                and set(self.plan.displaced) <= self.cancel_acked
                and set(self.plan.displaced) <= self.closed_confirmed)

    def _require_pending(self) -> None:
        if self.state != "pending":
            raise CapacityError(f"takeover already {self.state}")

    def _require_displaced(self, leg_id: str) -> None:
        if leg_id not in self.plan.displaced:
            raise CapacityError(f"{leg_id!r} is not a displaced leg of this takeover")


@dataclass
class CapacityLedger:
    """Durable micro-equivalent ledger: confirmed positions + outstanding reservations."""

    cap: int = ACCOUNT_MICRO_CAP
    confirmed: dict[str, int] = field(default_factory=dict)   # leg_id -> contracts
    reserved: dict[str, int] = field(default_factory=dict)    # leg_id -> contracts
    events: list[dict] = field(default_factory=list)
    _takeover: Takeover | None = field(default=None, init=False)

    # -- accounting -------------------------------------------------------
    @staticmethod
    def micro_of(leg_id: str, contracts: int) -> int:
        return leg(leg_id).micro_equiv * contracts

    def leg_micro(self, leg_id: str) -> int:
        return self.micro_of(leg_id, self.confirmed.get(leg_id, 0) + self.reserved.get(leg_id, 0))

    def micro_used(self) -> int:
        return sum(self.leg_micro(l) for l in set(self.confirmed) | set(self.reserved))

    def _event(self, kind: str, **detail) -> None:
        self.events.append({"kind": kind, **detail})

    # -- requests ---------------------------------------------------------
    def request(self, leg_id: str, contracts: int) -> CapacityDecision:
        spec = leg(leg_id)
        if not isinstance(contracts, int) or contracts <= 0:
            raise CapacityError(f"contracts must be a positive int, got {contracts!r}")
        if self._takeover is not None and self._takeover.state == "pending":
            return CapacityDecision(False, "takeover in progress", self.micro_used(),
                                    self.micro_of(leg_id, contracts))
        used = self.micro_used()
        need = self.micro_of(leg_id, contracts)
        if used + need <= self.cap:
            self.reserved[leg_id] = self.reserved.get(leg_id, 0) + contracts
            self._event("capacity_reserved", leg_id=leg_id, contracts=contracts,
                        micro_used=self.micro_used())
            return CapacityDecision(True, "within cap", used, need)
        # Refuse, never clip. Only the top-priority leg may displace.
        if spec.priority != 1:
            self._event("capacity_refused", leg_id=leg_id, contracts=contracts,
                        micro_used=used, micro_requested=need)
            return CapacityDecision(False, "would exceed the account cap; refused (not clipped)",
                                    used, need)
        # Displace whole lower-priority legs from the lowest priority upward.
        displaced: list[str] = []
        freed = 0
        for other in sorted(BOOK_LEGS, key=lambda s: -s.priority):
            if other.priority <= spec.priority:
                continue
            held = self.leg_micro(other.leg_id)
            if held == 0:
                continue
            if used - freed + need <= self.cap:
                break
            displaced.append(other.leg_id)
            freed += held
        if used - freed + need > self.cap:
            self._event("capacity_refused", leg_id=leg_id, contracts=contracts,
                        micro_used=used, micro_requested=need, reason="cap unreachable")
            return CapacityDecision(False, "cap unreachable even after displacing every "
                                    "lower-priority leg", used, need)
        plan = TakeoverPlan(leg_id, contracts, tuple(displaced))
        self._event("capacity_takeover_planned", leg_id=leg_id, displaced=list(displaced))
        return CapacityDecision(False, "takeover required before admission", used, need,
                                takeover=plan)

    def begin_takeover(self, plan: TakeoverPlan) -> Takeover:
        if self._takeover is not None and self._takeover.state == "pending":
            raise CapacityError("a takeover is already pending")
        self._takeover = Takeover(plan)
        self._takeover._event("capacity_takeover_begin", displaced=list(plan.displaced))
        return self._takeover

    def settle_takeover(self) -> CapacityDecision:
        """Reconcile after the broker confirmations; admits the requester or refuses."""
        t = self._takeover
        if t is None:
            raise CapacityError("no takeover to settle")
        used = self.micro_used()
        need = self.micro_of(t.plan.requester, t.plan.contracts)
        if t.state == "refused" or not t.complete():
            if t.state == "pending":
                t.fail(t.plan.requester, "settle called before every displaced leg was "
                                         "cancel-acked and confirmed flat")
            # Fail closed for the requester, but never discard broker truth: an
            # acknowledged cancel has released that leg's reservation, and a
            # reported position (flat or partial) is the leg's exposure now.
            for leg_id in t.cancel_acked:
                self.reserved.pop(leg_id, None)
            for leg_id, pos in t.confirmed_positions.items():
                self.confirmed[leg_id] = pos
            self.events.extend(t.events)
            self._event("capacity_requester_refused", leg_id=t.plan.requester,
                        reason=t.refuse_reason, reconciled=sorted(t.confirmed_positions))
            self._takeover = None
            return CapacityDecision(False, f"takeover refused: {t.refuse_reason}",
                                    self.micro_used(), need)
        for leg_id in t.plan.displaced:
            self.reserved.pop(leg_id, None)
            self.confirmed.pop(leg_id, None)
        used_after = self.micro_used()
        if used_after + need > self.cap:
            t.state = "refused"
            t.refuse_reason = "cap still exceeded after reconciliation"
            self.events.extend(t.events)
            self._takeover = None
            return CapacityDecision(False, t.refuse_reason, used_after, need)
        self.reserved[t.plan.requester] = self.reserved.get(t.plan.requester, 0) + t.plan.contracts
        t.state = "admitted"
        t._event("capacity_takeover_admitted", contracts=t.plan.contracts,
                 micro_used=self.micro_used())
        self.events.extend(t.events)
        self._takeover = None
        return CapacityDecision(True, "admitted after confirmed takeover", used_after, need)

    # -- broker truth -----------------------------------------------------
    def confirm_fill(self, leg_id: str, contracts: int) -> None:
        """A reserved entry/add filled (fully or partially) — move reservation to confirmed."""
        leg(leg_id)
        if contracts <= 0 or contracts > self.reserved.get(leg_id, 0):
            raise CapacityError(f"{leg_id}: fill {contracts} exceeds reservation "
                                f"{self.reserved.get(leg_id, 0)}")
        self.reserved[leg_id] -= contracts
        self.confirmed[leg_id] = self.confirmed.get(leg_id, 0) + contracts
        self._event("capacity_fill_confirmed", leg_id=leg_id, contracts=contracts)

    def release_reservation(self, leg_id: str, contracts: int | None = None) -> None:
        leg(leg_id)
        held = self.reserved.get(leg_id, 0)
        if contracts is not None and (not isinstance(contracts, int) or contracts <= 0):
            raise CapacityError(f"release contracts must be a positive int, got {contracts!r}")
        rel = held if contracts is None else contracts
        if rel > held:
            raise CapacityError(f"{leg_id}: release {rel} exceeds reservation {held}")
        self.reserved[leg_id] = held - rel
        self._event("capacity_reservation_released", leg_id=leg_id, contracts=rel)

    def confirm_position(self, leg_id: str, contracts: int) -> None:
        """Reconcile the confirmed position to broker truth (exits, flattens, restarts)."""
        leg(leg_id)
        if contracts < 0:
            raise CapacityError("confirmed position must be >= 0")
        self.confirmed[leg_id] = contracts
        self._event("capacity_position_confirmed", leg_id=leg_id, contracts=contracts)


# ── governance self-checks used by tests ─────────────────────────────────

def frozen_surfaces_untouched() -> dict:
    """The candidate never lands in the registry; dd_protection constants stay pinned."""
    import dd_protection  # noqa: WPS433 (import-time MVD pins the constants)
    return {
        "DD_TRIGGER": dd_protection.DD_TRIGGER,
        "DD_SCALE": dd_protection.DD_SCALE,
        "registry_empty": len(POLICY_REGISTRY) == 0,
    }
