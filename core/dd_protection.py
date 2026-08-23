#!/usr/bin/env python3
# Single-tier protection (validated 2026-04-17, revalidated 2026-04-23,
# re-anchored 2026-05-05 under 4-strategy lock, relaxed 2026-05-08 to C2 after
# bust_attribution_flip resolved as broker-feed-confirmed and same-date
# TradingView Pepperstone+OANDA re-export validated the panel pair):
#   - DD_TRIGGER 0.010 → 0.015, DD_SCALE held at 0.40
#   - C2 sweep evidence (per archive/docs/briefs/Q-DDP-1/): pass 98.09% / bust 0.36% /
#     p99 DD 4.73% on the 4-strategy Pepperstone panel — meets the lock
#     criteria (bust <1%, p99 DD <5%) and shortens median days-to-pass.
#   - Q-DDP-1 regime-robustness gate (criterion 5) failed for C2; the
#     2026-05-08 override accepts that risk on the strength of the broker-feed
#     resolution + median-pass-time benefit. See override note in
#     archive/docs/briefs/Q-DDP-1/recommendation.md.
#   - Equity tier deleted after Claude Code proved it was dead code under min semantics
#   - Do not change without re-running portfolio_mc
# See: docs/adr/2026-05-08-dd-trigger-c2-relock.md (C2 relock 1.5%/0.40×, canonical).
#      (Prior Notion 1.0%/0.40× "FINAL" page 346…be934cc is SUPERSEDED/archived.)
"""
DD Protection Scaler — FXIFY $200K Challenge
=============================================
Morning pre-market tool. Input current DXTrade equity,
get back the risk_pct to set on each TradingView strategy.

HISTORICAL-FIXTURE NOTE (2026-07-11,
docs/adr/2026-07-11-challenge-era-claims-rescope.md): the FXIFY framing
above (challenge target/limits, DXTrade equity, the display banner) is
retained as the historical anchor fixture — the venue closed 2026-07-10.
The DD *mechanism* (peak-DD trigger -> scale, plus the lifecycle
authorization haircut) is venue-agnostic and remains the live portfolio
risk control. Constants are frozen; the C2 calibration's days-to-pass
grounds are void with the venue — successor objective owed at the
2026-08-08 review (audit item D2). No executable line changed by the
re-scope.

CONCEPT-NOT-CONSTANT (2026-07-13,
docs/adr/2026-07-13-dd-protection-concept-not-constant.md): the mechanism
above is the invariant; (trigger, scale, reference_mode) are per-
(portfolio, firm-tier) variables owned by core/dd_geometry.py's
POLICY_REGISTRY. This module's DD_TRIGGER/DD_SCALE literals are the frozen
FXIFY-C2 *instance* (historical anchor fixture). The dd_geometry FXIFY-C2
seed row + import-time one-way pin were retired 2026-07-22 (substrate ADR
Phase 1); this module still never imports dd_geometry, and no executable
line changed here.

Rule: When portfolio DD from peak >= 1.5%, scale all risk to 0.40x.
      Clears automatically when equity returns to peak.

Usage:
    python dd_protection.py                  # show current status
    python dd_protection.py <equity>         # log equity and get today's risk levels
    python dd_protection.py --history        # show equity log
    python dd_protection.py --reset          # reset state (new challenge attempt)
"""

import sys
from datetime import datetime
from pathlib import Path

from lib.atomic_io import atomic_write_text
from lib.mvd import assert_guard_fired, assert_no_fallback
from lib.validation import dump_strict_json, load_strict_json, require_finite_number
from historical_challenge import (
    DAILY_LOSS_LIMIT_FRAC,
    PROFIT_TARGET_FRAC,
    STARTING_EQUITY,
    STATIC_DD_LIMIT_FRAC,
)
from firm_rules import base_risk_display
from lifecycle import (
    STRATEGY_KEYS,
    beta_death_assessment,
    get_effective_multipliers,
    get_lifecycle_multipliers,
)
# DD protection rule — single tier (retuned 2026-04-17, relaxed 2026-05-08
# from 0.010 to 0.015 after bust_attribution_flip closed broker-feed-confirmed
# + Q-DDP-1 C2 override on median-pass-time + risk-controls grounds)
# Venue-agnostic sizing law — c1 and calculate_protection consume these.
# Nothing below that is Phase-4-deletable may feed this block.
DD_TRIGGER = 0.015            # 1.5% DD from peak triggers scaling
DD_SCALE = 0.40               # multiply risk by 0.40x when triggered

# Locked allocations — derived from firm_rules._BASE_RISK (canonical slug dict).
# Display keys preserved for rail / lifecycle consumers. Do not re-literal here.
BASE_RISK = base_risk_display()

STATE_FILE = Path(__file__).parent / "dd_protection_state.json"

# Venue-agnostic reference equity for the boundary self-check.
# calculate_protection is scale-free in (equity, peak); this literal exists so
# the import-time MVD does not read a firm-derived global (Phase-4 deletion
# target lives below).
_MVD_REFERENCE_EQUITY = 200_000.0

# ── HISTORICAL CHALLENGE FIXTURE — closed FXIFY $200K semantics ──────────
# Opt-in reporting/CLI basis only. Sizing law above does not read these.
# Source: core/historical_challenge.py (substrate Phase 4; was FIRM_RULES["FXIFY"]).
PROFIT_TARGET = PROFIT_TARGET_FRAC
DAILY_LOSS_LIMIT = DAILY_LOSS_LIMIT_FRAC
STATIC_DD_LIMIT = STATIC_DD_LIMIT_FRAC
CHALLENGE_STATE_BASIS = STARTING_EQUITY

# ── State Management ──────────────────────────────────────────

def _default_state(basis: float | None = None) -> dict:
    basis = CHALLENGE_STATE_BASIS if basis is None else basis
    return {
        "starting_equity": basis,
        "peak_equity": basis,
        "last_equity": basis,
        "history": [],
    }


def _validate_state(state: object, *, expected_basis: float | None = None) -> dict:
    """Validate persisted DD state before it can influence sizing."""
    basis = CHALLENGE_STATE_BASIS if expected_basis is None else expected_basis
    required_keys = {"starting_equity", "peak_equity", "last_equity", "history"}
    if not isinstance(state, dict) or set(state) != required_keys:
        raise ValueError(
            f"DD state must be an object with exactly {sorted(required_keys)}"
        )

    starting = require_finite_number(
        state["starting_equity"], field="starting_equity", strictly_positive=True
    )
    peak = require_finite_number(
        state["peak_equity"], field="peak_equity", strictly_positive=True
    )
    last = require_finite_number(
        state["last_equity"], field="last_equity", strictly_positive=True
    )
    if starting != basis:
        raise ValueError(
            f"starting_equity must remain locked at {basis}, got {starting}"
        )
    if peak < max(starting, last):
        raise ValueError("peak_equity must be >= starting_equity and last_equity")

    history = state["history"]
    if not isinstance(history, list):
        raise ValueError("history must be a JSON array")
    history_keys = {"timestamp", "equity", "peak", "dd_from_peak", "multiplier"}
    for index, entry in enumerate(history):
        if not isinstance(entry, dict) or set(entry) != history_keys:
            raise ValueError(
                f"history[{index}] must contain exactly {sorted(history_keys)}"
            )
        if not isinstance(entry["timestamp"], str):
            raise ValueError(f"history[{index}].timestamp must be a string")
        datetime.fromisoformat(entry["timestamp"])
        entry_equity = require_finite_number(
            entry["equity"], field=f"history[{index}].equity", strictly_positive=True
        )
        entry_peak = require_finite_number(
            entry["peak"], field=f"history[{index}].peak", strictly_positive=True
        )
        if entry_peak < entry_equity:
            raise ValueError(f"history[{index}].peak must be >= equity")
        require_finite_number(
            entry["dd_from_peak"],
            field=f"history[{index}].dd_from_peak",
            minimum=0.0,
        )
        multiplier = require_finite_number(
            entry["multiplier"],
            field=f"history[{index}].multiplier",
            minimum=0.0,
        )
        if multiplier > 1.0:
            raise ValueError(f"history[{index}].multiplier must be <= 1.0")
    return state


def load_state(*, basis: float | None = None) -> dict:
    if STATE_FILE.exists():
        return _validate_state(load_strict_json(STATE_FILE), expected_basis=basis)
    return _default_state(basis)

def save_state(state: dict):
    # Atomic: a crash mid-write must never truncate the only copy of the state.
    atomic_write_text(STATE_FILE, dump_strict_json(state))

def reset_state(*, basis: float | None = None):
    save_state(_default_state(basis))
    resolved = CHALLENGE_STATE_BASIS if basis is None else basis
    print(f"State reset. Peak equity = ${resolved:,.2f}")

# ── Core Logic ────────────────────────────────────────────────

def calculate_protection(equity: float, peak: float, lifecycle=None) -> dict:
    """Determine active multiplier and scaled risk levels.

    `lifecycle` is an optional per-strategy authorization multiplier
    (BASE_RISK key -> float in [0.0, 1.0]). None means every strategy AUTHORIZED
    (1.0x) — byte-identical to the pre-lifecycle single-factor path (x1.0 is exact
    in IEEE754). The lifecycle factor is the risk_pct-layer authorization haircut;
    it compounds MULTIPLICATIVELY with the DD scale (a WATCH-1 leg in DD -> 0.20x)
    and MULTIPLIES against BASE_RISK/DD_SCALE — it never edits them (axis-separation,
    ADR 2026-07-10 section-4 trigger 3). See docs/methodology/strategy_lifecycle.md Call 2.
    """
    equity = require_finite_number(equity, field="equity", minimum=0.0)
    peak = require_finite_number(peak, field="peak", strictly_positive=True)
    dd_from_peak = (peak - equity) / peak if equity < peak else 0.0
    # ULP-precision rounding before threshold compare, see
    # docs/adr/2026-05-10-dd-protection-ulp-rounding.md
    dd_triggered = round(dd_from_peak, 6) >= DD_TRIGGER

    if dd_triggered:
        multiplier = DD_SCALE
        rule = f"DD PROTECTION (DD {dd_from_peak:.2%} ≥ {DD_TRIGGER:.1%})"
    else:
        multiplier = 1.0
        rule = "NONE — full risk"

    if lifecycle is None:
        lifecycle = {k: 1.0 for k in BASE_RISK}
    scaled_risk = {k: v * multiplier * lifecycle[k] for k, v in BASE_RISK.items()}

    return {
        "dd_from_peak": dd_from_peak,
        "dd_triggered": dd_triggered,
        "multiplier": multiplier,
        "rule": rule,
        "scaled_risk": scaled_risk,
        "lifecycle": lifecycle,
    }


# ── MVD self-check (runs at import) ───────────────────────────

def _validate_protection_rule():
    """MVD self-check, runs at module import. Two-layer defense:

    A. **Logic check** — boundary behavior is correct (guard fires when
       crossed, doesn't fire when not). Catches sign-flips, off-by-one in
       the comparison, wrong multiplier on trigger. Maps to methodology
       family Contract.

    B. **Spec pin** — current constants match the 2026-05-08 relocked values
       (`DD_TRIGGER = 0.015`, `DD_SCALE = 0.40`). The boundary check above
       scales with the constants and so cannot detect a value drift on its
       own. The pin forces any change to be a deliberate joint edit:
       constant + literal in this function + re-MC at the new config (per
       "any dd_protection constant change triggers re-MC" rule in the
       2026-04-24 ADR).

    Catches audit instance #3 (production-vs-memory drift, Rule 0 catalyst).
    """
    # --- A. Logic check: rule fires at its own trigger boundary ---
    epsilon = 0.0001
    eq_below = _MVD_REFERENCE_EQUITY * (1 - DD_TRIGGER + epsilon)  # DD just under
    eq_above = _MVD_REFERENCE_EQUITY * (1 - DD_TRIGGER - epsilon)  # DD just over

    below = calculate_protection(eq_below, _MVD_REFERENCE_EQUITY)
    above = calculate_protection(eq_above, _MVD_REFERENCE_EQUITY)

    fires_above = 1 if above["multiplier"] == DD_SCALE else 0
    assert_guard_fired(
        fires_above,
        label=f"dd_protection fires when DD crosses DD_TRIGGER={DD_TRIGGER:.2%}",
    )

    spurious_below = 1 if below["multiplier"] < 1.0 else 0
    assert_no_fallback(
        spurious_below,
        label=f"dd_protection silent when DD just under DD_TRIGGER={DD_TRIGGER:.2%}",
    )

    # --- B. Spec pin: constants match locked values per 2026-05-08 relock ---
    # Originally 2026-04-17 ADR at (0.010, 0.40); relaxed 2026-05-08 to
    # (0.015, 0.40) on the C2 override grounds (Q-DDP-1 sweep + bust-feed
    # broker confirmation). 4-strategy Pepperstone MC under the relaxed
    # constants: per Q-DDP-1 sweep_results.csv, C2 = 98.09% pass / 0.36% bust
    # / p99 DD 4.73% — both lock criteria (bust <1%, p99 DD <5%) clear. (That is
    # the C2-*adoption* sweep that justified DD_TRIGGER 0.010→0.015; the
    # dd_protection constants are unchanged since. The current 4-strategy
    # *headline* anchor — after the later 2026-05-14 / 2026-05-23 allocation
    # refreshes, which did NOT touch these constants — is 99.83% / 0.17% /
    # 4.37% per CLAUDE.md and docs/mc_anchor_history.md.)
    # Any future change to either constant must update both the constant AND
    # this literal pin in the same commit, tied to a re-MC run.
    if DD_TRIGGER != 0.015:
        raise AssertionError(
            f"MVD spec drift: DD_TRIGGER moved from locked 0.015 to {DD_TRIGGER}. "
            f"Re-run portfolio_mc and update the pin literal in the same commit."
        )
    if DD_SCALE != 0.40:
        raise AssertionError(
            f"MVD spec drift: DD_SCALE moved from locked 0.40 to {DD_SCALE}. "
            f"Re-run portfolio_mc and update the pin literal in the same commit."
        )


_validate_protection_rule()


# ── Display ───────────────────────────────────────────────────

def display_status(
    equity: float,
    peak: float,
    result: dict,
    is_update: bool = False,
    beta: dict = None,
    *,
    basis: float | None = None,
    profit_target_pct: float | None = None,
    static_dd_pct: float | None = None,
):
    """Print the dashboard."""
    basis = CHALLENGE_STATE_BASIS if basis is None else basis
    profit_target_pct = PROFIT_TARGET if profit_target_pct is None else profit_target_pct
    static_dd_pct = STATIC_DD_LIMIT if static_dd_pct is None else static_dd_pct
    pnl = equity - basis
    target_remaining = (basis * profit_target_pct) - pnl
    dd_from_start = (basis - equity) / basis if equity < basis else 0.0

    print()
    print("=" * 56)
    print("  FXIFY $200K CHALLENGE — DD PROTECTION STATUS")
    print("=" * 56)
    print()
    print(f"  Equity:        ${equity:>12,.2f}")
    print(f"  Peak:          ${peak:>12,.2f}")
    print(f"  P&L:           ${pnl:>12,.2f}  ({pnl/basis:>+.2%})")
    print(f"  DD from peak:  {result['dd_from_peak']:>12.2%}")
    print(f"  DD from start: {dd_from_start:>12.2%}  (limit: {static_dd_pct:.0%})")

    if target_remaining > 0:
        print(f"  To target:     ${target_remaining:>12,.2f}")
    else:
        print(f"  TARGET REACHED  ✓")

    print()

    # Safety warnings
    if dd_from_start >= 0.04:
        print("  ⚠️  DD > 4% FROM START — HALT ALL TRADING")
        print()
    elif dd_from_start >= 0.03:
        print("  ⚠️  DD > 3% FROM START — REVIEW BEFORE TRADING")
        print()

    # Active rule (DD protection) + authorization (lifecycle de-risk) — both honest,
    # so a lifecycle haircut can never masquerade as "full risk".
    deauth = {k: m for k, m in result.get("lifecycle", {}).items() if m < 1.0}
    if result['multiplier'] < 1.0:
        print(f"  ⚡ ACTIVE RULE: {result['rule']}")
        print(f"  ⚡ MULTIPLIER:  {result['multiplier']:.2f}x")
    elif not deauth:
        print(f"  ✅ {result['rule']}")
    if deauth:
        print("  🔻 AUTHORIZATION (lifecycle de-risk, incl. any beta): "
              + ", ".join(f"{k} {m:.2f}x" for k, m in deauth.items()))
    if beta and beta.get("beta_death"):
        print(f"  🛑 BETA-DEATH: {beta['watch_count']}/{beta['n_legs']} legs de-authorized"
              f" — portfolio de-risked to {beta['portfolio_multiplier']:.2f}x on EVERY leg.")
        print("     OPERATOR GO/NO-GO REQUIRED on full shared-beta shutdown (not autonomous).")
    elif beta and beta.get("soft_flag"):
        print(f"  ⚠ BETA SOFT FLAG: {beta['watch_count']}/{beta['n_legs']} legs de-authorized"
              f" — pull interim review + run the beta-cohesion check.")
    print()

    # Risk table
    print("  ┌────────────────┬──────────┬──────────┐")
    print("  │ Strategy       │   Base   │  Today   │")
    print("  ├────────────────┼──────────┼──────────┤")
    for name, base in BASE_RISK.items():
        scaled = result['scaled_risk'][name]
        marker = " ◀" if scaled != base else ""
        print(f"  │ {name:<14} │  {base:.2%}  │  {scaled:.2%}{marker:>2} │")
    print("  └────────────────┴──────────┴──────────┘")
    print()

    # TV input helper — show exact values to type
    if result['multiplier'] < 1.0:
        print("  Set in TradingView strategy inputs:")
        for name, risk in result['scaled_risk'].items():
            print(f"    {name}: risk_pct = {risk * 100:.2f}")
        print()
        print("  Restore to base when multiplier returns to 1.0x:")
        for name, base in BASE_RISK.items():
            print(f"    {name}: risk_pct = {base * 100:.2f}")
        print()


def display_history(state: dict):
    """Show equity log."""
    if not state["history"]:
        print("\nNo equity readings logged yet.\n")
        return

    print()
    print("  Date/Time              Equity        Peak     DD%     Mult")
    print("  " + "─" * 62)
    for entry in state["history"][-30:]:  # last 30 entries
        dt = entry["timestamp"][:16]
        eq = entry["equity"]
        pk = entry["peak"]
        dd = entry["dd_from_peak"]
        mult = entry["multiplier"]
        marker = " ⚡" if mult < 1.0 else ""
        print(f"  {dt}  ${eq:>11,.2f}  ${pk:>11,.2f}  {dd:>5.2%}  {mult:.2f}x{marker}")
    print()


# ── Main ──────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        confirm = input("Reset DD protection state? This clears peak equity and history. [y/N] ")
        if confirm.lower() == "y":
            reset_state()
        return

    state = load_state()

    if len(sys.argv) > 1 and sys.argv[1] == "--history":
        display_history(state)
        return

    if len(sys.argv) > 1:
        # Equity update mode
        try:
            equity = require_finite_number(
                float(sys.argv[1].replace(",", "").replace("$", "")),
                field="equity",
                strictly_positive=True,
            )
        except ValueError:
            print(f"Invalid equity value: {sys.argv[1]}")
            print("Usage: python dd_protection.py <equity>")
            sys.exit(1)

        # Sanity checks
        if equity <= 0:
            print("Equity must be positive.")
            sys.exit(1)
        if equity > CHALLENGE_STATE_BASIS * 1.5:
            print(f"Warning: ${equity:,.2f} is >50% above starting equity. Confirm? [y/N] ", end="")
            if input().lower() != "y":
                return

        # Update peak
        old_peak = state["peak_equity"]
        if equity > state["peak_equity"]:
            state["peak_equity"] = equity

        # Call-4 stays 4-leg (STRATEGY_KEYS). Living scaled_risk uses BASE_RISK.
        eff = get_effective_multipliers(STRATEGY_KEYS)
        beta = beta_death_assessment(get_lifecycle_multipliers(STRATEGY_KEYS))
        result = calculate_protection(
            equity, state["peak_equity"], {k: eff[k] for k in BASE_RISK}
        )

        # Log entry
        state["history"].append({
            "timestamp": datetime.now().isoformat(),
            "equity": equity,
            "peak": state["peak_equity"],
            "dd_from_peak": round(result["dd_from_peak"], 6),
            "multiplier": result["multiplier"],
        })
        state["last_equity"] = equity
        save_state(state)

        display_status(equity, state["peak_equity"], result, is_update=True, beta=beta)

        if equity > old_peak:
            print(f"  📈 New peak equity: ${equity:,.2f} (was ${old_peak:,.2f})")
            print()

    else:
        # Status mode — show current state without updating
        eff = get_effective_multipliers(STRATEGY_KEYS)
        beta = beta_death_assessment(get_lifecycle_multipliers(STRATEGY_KEYS))
        result = calculate_protection(
            state["last_equity"],
            state["peak_equity"],
            {k: eff[k] for k in BASE_RISK},
        )
        display_status(state["last_equity"], state["peak_equity"], result, beta=beta)


if __name__ == "__main__":
    main()
