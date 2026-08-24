"""C1 sizing host — Python REFERENCE implementation (oracle for the NT8 port).

Implements the frozen spec docs/spec/c1_nt8_sizing_host_impl.md (B2, GO ADR
2026-07-17-c1-rail-build-account-registration-go.md) exactly:

    r_eff   = BASE_RISK[leg] x DD_SCALE(dd_state) x M_lifecycle(tier)
    qty     = min(floor(E_firm*r_eff / (SL_pts*$/pt)), floor(cap/(1+pyr%/100)))
    add     = floor(executed_base * pyr%/100)

This module is the listener's sizing reference when the rail is armed
(Option C, adopted 2026-07-18 — see docs/spec/c1_nt8_sizing_host_impl.md).
No book is deployed. ops/c1_rail/c1_rail_listener.py runs
C1SizingHostReference directly on the TV->CrossTrade->Tradovate rail; the
NinjaScript port is a dormant fallback and was never built. The sizing law
remains proven against the committed F2 oracle
(lab/analysis/q_rail_1_2026-07/f2_floors.json), which the B6 dry-fire gate
(PASSED 2026-07-20) matched exactly.

Fail-safe doctrine (spec §5/§6): ANY unreadable/malformed state input —
missing file, bad JSON, unlisted leg key, unknown tier — halts entry/add
sizing for that signal (qty 0, no submit). The reference NEVER falls through
to a default multiplier. This deliberately diverges from core/lifecycle.py's
absent-state default (AUTHORIZED, 1.0x), which is safe only for the
read-only display surface: a live rail must fail toward zero size.

Relation to tests/rail_crosstrade/translator.py (P5 golden-path infra): that
layer formats an order INTENT into a CrossTrade key=value payload and carries
a qty it is given; this module is the thing that COMPUTES the qty. They
compose (host output -> translator input); neither replaces the other.

Sizing constants are consumed from a JSON mirror (c1_sizing_constants.json,
same shape the .NET host will read — it cannot import Python at trade time).
generate_constants() derives that mirror from production sources
(firm_rules.FIRM_RULES + dd_protection.BASE_RISK + the spec §2.1 leg map);
tests pin mirror == production so drift is mechanical to catch (M-9 shape).
"""
from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Standalone-run bootstrap (same pattern as ops/cli.py): resolve core-layer
# flat modules when run outside pytest's pythonpath config.
# parents[2] = repo root (this file lives under ops/c1_rail/).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_RAIL_DIR = Path(__file__).resolve().parent
for _p in (str(_REPO_ROOT / "core"), str(_RAIL_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dd_protection import BASE_RISK, calculate_protection  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from lifecycle import TIER_MULTIPLIER  # noqa: E402

# Spec §2.1 — leg_id mapping table (venue-edition constants mirror the locked
# Pine inputs: pyramidSize 750/1000, mymPointValue 0.50 / mnqPointValue 2.00).
#
# `cap_alloc` — this leg's SHARE of the firm's ACCOUNT-AGGREGATE contract cap
# (added 2026-07-22; operator-approved static split). Tradeify's limit is per
# ACCOUNT, not per instrument: "Your combined position must stay within your
# account's contract limit, counted at 10 micros = 1 mini" (help.tradeify.co
# article 10495868; 100K = 8 mini / 80 micro per article 12268167). MFFU
# publishes the consequence explicitly — exceeding it "can result in a BREACH
# of the trading account" (article 13286542).
#
# Before this split the host applied the FULL `cap_firm` to EACH leg, so the
# 2-leg book could compute MYM 76 + MNQ 77 = 153 micros against an 80 limit
# (1.91x). That was not theoretical: on the pinned venue-edition exports MYM is
# cap-bound in 93% of trades (40/43), 22.1% of DJ30 trades carry a simultaneous
# NAS position, and the observed max combined position was 98 micros
# (2025-10-14 12:15 = MYM 76 + MNQ 22). WATCH-1 0.50x does NOT rescue it: the
# haircut scales `r_eff`, while the cap branch is invariant to it.
#
# Split chosen on the efficient frontier of (cap_mym + cap_mnq == cap_firm)
# subject to combined max <= cap_firm: 69/11 -> MYM base 8 + add 60 = 68,
# MNQ base 1 + add 10 = 11, combined 79 <= 80. MYM is favoured because it is
# granularity-tolerant and carries the size; MNQ already zero-floors at wide
# stops (the documented NOT-M8 case). Locked Pine pyramid ratios (750%/1000%)
# are untouched — this allocates a firm constant, never a locked parameter.
#
# UPGRADE PATH (not a permanent ceiling): when the host gains verified live
# position truth, this static split relaxes to a runtime headroom check. Same
# re-add shape as the 2026-07-19 CrossTrade Account Manager trigger.
LEG_MAP: dict[str, dict] = {
    "dj30_mym": {
        "leg_key": "Striker",
        "pyr_pct": 750.0,
        "dollars_per_pt": 0.50,
        "cap_alloc": 69,
    },
    "nas100_mnq": {
        "leg_key": "Striker NAS100",
        "pyr_pct": 1000.0,
        "dollars_per_pt": 2.00,
        "cap_alloc": 11,
    },
}

_SIGNAL_TYPES = frozenset({"entry", "add", "exit", "flat"})
_REQUIRED_PAYLOAD_FIELDS = ("leg_id", "signal_type", "bar_time", "close",
                            "stop_dist_pts")


def generate_constants(tier: str) -> dict:
    """Derive the c1_sizing_constants.json mirror from production sources.

    This is the re-pin mechanism (spec §2.3): run it, write the JSON, commit
    the delta alongside any firm_rules/locked-Pine change. Tests assert the
    generated values equal production so a stale mirror is caught mechanically.
    """
    firm = FIRM_RULES[tier]
    return {
        "tier": tier,
        "E_firm": firm["starting_balance"],
        "cap_firm": firm["micro_contract_cap"],
        "cost_per_side_usd": firm["cost_per_side_usd"],
        "leg_map": {
            leg_id: {
                "leg_key": leg["leg_key"],
                "base_risk": BASE_RISK[leg["leg_key"]],
                "pyr_pct": leg["pyr_pct"],
                "dollars_per_pt": leg["dollars_per_pt"],
                "cap_alloc": leg["cap_alloc"],
            }
            for leg_id, leg in LEG_MAP.items()
        },
    }


@dataclass(frozen=True)
class SizingDecision:
    """Audit record for one processed signal (spec §3 Phase-3 audit log row)."""
    leg_id: str
    signal_type: str
    qty_out: int
    submit: bool
    halt: bool
    halt_reason: str | None = None
    floored: bool = False
    leg_key: str | None = None
    dd_scale: float | None = None
    lifecycle_multiplier: float | None = None
    r_eff: float | None = None
    risk_dollars: float | None = None
    per_contract: float | None = None
    qty_base_raw: int | None = None
    reserve_cap: int | None = None


class _StateError(Exception):
    """Internal: any unreadable/invalid state input (drives the halt path)."""


def _load_json(path: Path, label: str) -> dict:
    if not path.exists():
        raise _StateError(f"{label} missing: {path.name}")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise _StateError(f"{label} unreadable ({path.name}): {exc}") from exc
    if not isinstance(obj, dict):
        raise _StateError(f"{label} malformed ({path.name}): not a JSON object")
    return obj


@dataclass
class C1SizingHostReference:
    """File-contract twin of the NT8 host: three state paths in, decisions out.

    `open_leg_state` holds the **broker-confirmed** base qty per leg between
    entry and add (spec §2.2 + monitoring ADR 2026-07-22 M1 §2.7). The add is
    sized off the ACTUAL filled base, never re-derived and never seeded from
    intended entry quantity. Call ``confirm_executed_base`` after durable
    broker evidence; ``clear_executed_base`` only after broker-confirmed flat.
    """
    lifecycle_state_path: Path
    dd_state_path: Path
    constants_path: Path
    open_leg_state: dict[str, int] = field(default_factory=dict)

    def confirm_executed_base(self, leg_key: str, qty: int) -> None:
        """Record broker-confirmed base fill qty (add sizing input)."""
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError(
                f"confirmed base qty must be positive int, got {qty!r}")
        self.open_leg_state[leg_key] = qty

    def clear_executed_base(self, leg_key: str) -> None:
        """Drop confirmed base after broker-confirmed flatness."""
        self.open_leg_state.pop(leg_key, None)

    # ── state readers (each raises _StateError -> halt) ──────────────────

    def _read_constants(self) -> dict:
        c = _load_json(Path(self.constants_path), "constants")
        for key in ("E_firm", "cap_firm", "leg_map"):
            if key not in c:
                raise _StateError(f"constants malformed: missing '{key}'")
        return c

    def _read_lifecycle_multiplier(self, leg_key: str) -> float:
        state = _load_json(Path(self.lifecycle_state_path), "lifecycle state")
        if leg_key not in state:
            # Spec §5: NO fall-through to AUTHORIZED for an unlisted leg —
            # deliberate divergence from core/lifecycle.py's read-only default.
            raise _StateError(
                f"lifecycle state ({Path(self.lifecycle_state_path).name}) has "
                f"no entry for {leg_key!r}; live sizing never defaults a tier")
        tier = state[leg_key]
        if tier not in TIER_MULTIPLIER:
            raise _StateError(
                f"unknown lifecycle tier {tier!r} for {leg_key!r}; "
                f"valid: {sorted(TIER_MULTIPLIER)}")
        return TIER_MULTIPLIER[tier]

    def _read_dd_scale(self, current_equity: float) -> float:
        state = _load_json(Path(self.dd_state_path), "dd state")
        peak = state.get("peak_equity")
        if not isinstance(peak, (int, float)) or not math.isfinite(peak) or peak <= 0:
            raise _StateError(
                f"dd state ({Path(self.dd_state_path).name}) has invalid "
                f"peak_equity: {peak!r}")
        # Ratchet peak with current equity (no phantom DD on a new high), then
        # reuse dd_protection.calculate_protection for the ULP threshold → scale
        # (docs/adr/2026-05-10-dd-protection-ulp-rounding.md). Do not re-implement
        # the round(..., 6) compare here.
        effective_peak = max(float(peak), float(current_equity))
        return float(
            calculate_protection(float(current_equity), effective_peak)["multiplier"]
        )

    # ── the sizing law (spec §2.2) ────────────────────────────────────────

    def process_signal(self, payload: dict, current_equity: float) -> SizingDecision:
        leg_id = str(payload.get("leg_id", "<absent>"))
        signal_type = str(payload.get("signal_type", "<absent>"))

        def _halt(reason: str) -> SizingDecision:
            return SizingDecision(leg_id=leg_id, signal_type=signal_type,
                                  qty_out=0, submit=False, halt=True,
                                  halt_reason=reason)

        for fld in _REQUIRED_PAYLOAD_FIELDS:
            if fld not in payload:
                return _halt(f"payload missing required field {fld!r}")
        if signal_type not in _SIGNAL_TYPES:
            return _halt(f"unknown signal_type {signal_type!r}; "
                         f"valid: {sorted(_SIGNAL_TYPES)}")
        if leg_id not in LEG_MAP:
            return _halt(f"unknown leg_id {leg_id!r}; valid: {sorted(LEG_MAP)}")
        leg_key = LEG_MAP[leg_id]["leg_key"]

        if signal_type in ("exit", "flat"):
            # Bookkeeping only — exits/EOD/DD-closes are the strategy's own
            # orders + CrossTrade Account Manager, never this host's.
            # Do NOT clear confirmed base here: flatness must be
            # broker-confirmed (monitoring ADR M1 §2.7) before
            # clear_executed_base / ExecutionStateStore.clear_leg.
            return SizingDecision(leg_id=leg_id, signal_type=signal_type,
                                  qty_out=0, submit=False, halt=False,
                                  leg_key=leg_key)

        try:
            constants = self._read_constants()
            leg_const = constants["leg_map"].get(leg_id)
            if leg_const is None:
                raise _StateError(f"constants leg_map has no entry for {leg_id!r}")
            lifecycle_m = self._read_lifecycle_multiplier(leg_key)
            dd_scale = self._read_dd_scale(current_equity)
        except _StateError as exc:
            return _halt(str(exc))

        base_risk = float(leg_const["base_risk"])
        pyr_pct = float(leg_const["pyr_pct"])
        dollars_per_pt = float(leg_const["dollars_per_pt"])
        e_firm = float(constants["E_firm"])
        cap_firm = float(constants["cap_firm"])
        r_eff = base_risk * dd_scale * lifecycle_m

        if signal_type == "entry":
            stop_dist_pts = float(payload["stop_dist_pts"])
            risk_dollars = e_firm * r_eff
            per_contract = stop_dist_pts * dollars_per_pt
            qty_base_raw = (math.floor(risk_dollars / per_contract)
                            if per_contract > 0 else 0)
            # Cap is ACCOUNT-AGGREGATE (see LEG_MAP): this leg gets its
            # allocated share, never the whole account cap. Fail toward the
            # conservative side — a missing cap_alloc is a state defect, and the
            # host's doctrine is halt-to-zero rather than fall back to a
            # permissive default (which here would mean the old 1.91x breach).
            if "cap_alloc" not in leg_const:
                return _halt(f"constants leg_map[{leg_id!r}] has no cap_alloc")
            cap_alloc = float(leg_const["cap_alloc"])
            if cap_alloc > cap_firm:
                return _halt(
                    f"cap_alloc {cap_alloc:g} exceeds account cap {cap_firm:g}")
            reserve_cap = math.floor(cap_alloc / (1 + pyr_pct / 100))
            qty_out = min(qty_base_raw, reserve_cap)
            # Intended qty is NOT executed base — confirm_executed_base only
            # after broker evidence (monitoring ADR M1 §2.7 / §5).
            return SizingDecision(
                leg_id=leg_id, signal_type=signal_type, qty_out=qty_out,
                submit=qty_out > 0, halt=False, floored=qty_out == 0,
                leg_key=leg_key, dd_scale=dd_scale,
                lifecycle_multiplier=lifecycle_m, r_eff=r_eff,
                risk_dollars=risk_dollars, per_contract=per_contract,
                qty_base_raw=qty_base_raw, reserve_cap=reserve_cap)

        # signal_type == "add"
        executed_base = self.open_leg_state.get(leg_key)
        if executed_base is None:
            return _halt(f"add for {leg_key!r} with no tracked executed base "
                         f"(no prior entry this position); never re-derive")
        qty_out = math.floor(executed_base * (pyr_pct / 100))
        return SizingDecision(
            leg_id=leg_id, signal_type=signal_type, qty_out=qty_out,
            submit=qty_out > 0, halt=False, floored=qty_out == 0,
            leg_key=leg_key, dd_scale=dd_scale,
            lifecycle_multiplier=lifecycle_m, r_eff=r_eff)
