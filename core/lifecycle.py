#!/usr/bin/env python3
"""
Strategy Authorization Lifecycle — per-strategy sizing multiplier.
=================================================================
The AUTHORIZATION axis (separate from the LOCKED parameter axis). A strategy's
capital authorization is always-revocable and graded; this module owns the
ratified tier -> multiplier ladder and the per-strategy authorization state.

The lifecycle multiplier is a per-strategy risk-authorization haircut applied at
the **risk_pct layer** (dd_protection.calculate_protection), compounding
MULTIPLICATIVELY with the DD scale:

    risk_pct_live[k] = BASE_RISK[k] x DD_SCALE x lifecycle_multiplier[k]

It MULTIPLIES against BASE_RISK/DD_SCALE/DD_TRIGGER — it never edits them
(axis-separation invariant; ADR section-4 trigger 3).

Canonical values:  docs/methodology/strategy_lifecycle.md (Call 2)
Decision record:   docs/adr/2026-07-10-strategies-never-locked-lifecycle-governance.md

Phase-2 code scope (this file): items 1-2 = the ladder + a read-only state
loader. Writing state (a Call-1 tier demotion) is item 3, not built here — a
human hand-edits lifecycle_state.json in the interim.
"""

from pathlib import Path

from lib.validation import load_strict_json

# Ratified tier ladder (operator, 2026-07-10; strategy_lifecycle.md Call 2).
# A change here is a GOVERNANCE change (fresh ADR + strategy_lifecycle.md), never
# a silent code edit — the _validate_ladder() pin below enforces that.
TIER_MULTIPLIER = {
    "AUTHORIZED": 1.00,
    "WATCH-1":    0.50,
    "WATCH-2":    0.25,
    "RETIRED":    0.00,
}
DEFAULT_TIER = "AUTHORIZED"
STRATEGY_KEYS = frozenset({"Guardian", "Striker", "Aegis", "Striker NAS100"})

# Authorization ladder, most- to least-authorized. Demotions step DOWN this list.
_LADDER_ORDER = ["AUTHORIZED", "WATCH-1", "WATCH-2", "RETIRED"]

# Call-4 beta-death control (ratified 2026-07-10; strategy_lifecycle.md Call 4).
# "De-authorized" = any leg with multiplier < 1.0 (WATCH-1/WATCH-2/RETIRED). A
# RETIRED leg is maximally degraded, so it counts toward correlated-degradation.
BETA_SOFT_FLAG_COUNT = 2     # >= 2 of N legs de-authorized -> soft flag (interim review + cohesion read)
BETA_DEATH_COUNT = 3         # >= 3 of N legs de-authorized -> autonomous portfolio de-risk + operator GO/NO-GO
BETA_DEATH_DERISK = 0.50     # portfolio-wide beta-level multiplier when beta-death fires

# Per-strategy authorization state (tier assignments). Runtime state, gitignored
# and local-only like accounts.json / dd_protection_state.json. An ABSENT file ==
# every strategy AUTHORIZED @ 1.0x (the live reality as of 2026-07-10).
STATE_FILE = Path(__file__).parent / "lifecycle_state.json"


def load_lifecycle_state() -> dict:
    """Load per-strategy tier assignments; {} when no state file exists."""
    if STATE_FILE.exists():
        state = load_strict_json(STATE_FILE)
        if not isinstance(state, dict):
            raise ValueError("Lifecycle state must be a JSON object")
        unknown = set(state) - STRATEGY_KEYS
        if unknown:
            raise ValueError(f"Unknown lifecycle strategies: {sorted(unknown)}")
        invalid = {key: tier for key, tier in state.items() if tier not in TIER_MULTIPLIER}
        if invalid:
            raise ValueError(
                f"Invalid lifecycle tiers: {invalid}; valid tiers: {sorted(TIER_MULTIPLIER)}"
            )
        return state
    return {}


def _multipliers_from_state(strategy_keys, state: dict) -> dict:
    """Pure mapper: each key's authorization tier -> its multiplier.

    Unlisted strategies default to AUTHORIZED (1.0x). An unrecognized tier string
    is a HARD error — a bad tier must never silently size a position (repo
    no-silent-fallback philosophy; axis-integrity, ADR section-4 trigger 3).
    """
    out = {}
    for k in strategy_keys:
        tier = state.get(k, DEFAULT_TIER)
        if tier not in TIER_MULTIPLIER:
            raise ValueError(
                f"Unknown lifecycle tier {tier!r} for strategy {k!r}. "
                f"Valid tiers: {sorted(TIER_MULTIPLIER)}."
            )
        out[k] = TIER_MULTIPLIER[tier]
    return out


def get_lifecycle_multipliers(strategy_keys) -> dict:
    """Per-strategy lifecycle multipliers from the current on-disk state."""
    return _multipliers_from_state(strategy_keys, load_lifecycle_state())


# ── Call 4 — beta-death control ───────────────────────────────

def beta_death_assessment(multipliers: dict) -> dict:
    """Ratified Call-4 logic over the per-leg multipliers.

    Counts legs in a de-authorized tier (multiplier < 1.0). At >= BETA_SOFT_FLAG_COUNT
    it raises a soft flag (interim review + cohesion read); at >= BETA_DEATH_COUNT it
    autonomously de-risks the WHOLE portfolio by BETA_DEATH_DERISK and raises an operator
    GO/NO-GO on full shared-beta shutdown (the shutdown itself is NOT autonomous — Call 5).
    """
    n_legs = len(multipliers)
    watch_count = sum(1 for m in multipliers.values() if m < 1.0)
    beta_death = watch_count >= BETA_DEATH_COUNT
    return {
        "n_legs": n_legs,
        "watch_count": watch_count,
        "soft_flag": watch_count >= BETA_SOFT_FLAG_COUNT,
        "beta_death": beta_death,
        "portfolio_multiplier": BETA_DEATH_DERISK if beta_death else 1.0,
        "operator_go_nogo": beta_death,
    }


def get_effective_multipliers(strategy_keys, _state_override=None) -> dict:
    """Final per-strategy sizing multiplier = per-leg lifecycle x portfolio beta de-risk.

    This is what the live sizing path consumes. It composes the per-leg authorization
    haircut with the Call-4 portfolio-wide beta de-risk (applied to EVERY leg when
    >= BETA_DEATH_COUNT legs are de-authorized). Behavior-neutral when all AUTHORIZED
    (per-leg 1.0x, beta 1.0x). `_state_override` is a test seam only.
    """
    state = load_lifecycle_state() if _state_override is None else _state_override
    per_leg = _multipliers_from_state(strategy_keys, state)
    beta = beta_death_assessment(per_leg)["portfolio_multiplier"]
    return {k: m * beta for k, m in per_leg.items()}


# ── Call 1 — decay signal + tier transitions ──────────────────

def decay_breach(rolling_pf: float, baseline_pf: float, pf_sigma: float,
                 k_sigma: float = 1.0) -> bool:
    """True iff rolling live PF is BELOW [baseline PF - k_sigma * sigma] (ratified k=1.0).

    A single-window breach; demotion requires 2 consecutive breaches (caller-tracked).
    Strict `<`: sitting exactly on the floor is not yet a breach.
    """
    return rolling_pf < (baseline_pf - k_sigma * pf_sigma)


def next_tier_down(tier: str) -> str:
    """Next tier down the full ladder; RETIRED is the floor. Operator-confirmed use
    (autonomous demotion must go through autonomous_demote, which caps at WATCH-2)."""
    if tier not in _LADDER_ORDER:
        raise ValueError(f"Unknown tier {tier!r}. Valid: {_LADDER_ORDER}.")
    i = _LADDER_ORDER.index(tier)
    return _LADDER_ORDER[min(i + 1, len(_LADDER_ORDER) - 1)]


def autonomous_demote(tier: str) -> str:
    """Autonomous demotion. Call 5: automation may move authorization DOWN only and may
    NEVER auto-RETIRE — WATCH-2 -> RETIRED is operator-gated, so the autonomous floor is
    WATCH-2. RETIRED (operator-set) never auto-changes."""
    if tier not in _LADDER_ORDER:
        raise ValueError(f"Unknown tier {tier!r}. Valid: {_LADDER_ORDER}.")
    if tier in ("AUTHORIZED", "WATCH-1"):
        return next_tier_down(tier)
    return tier  # WATCH-2 / RETIRED: no autonomous move


# ── MVD self-check (runs at import) ───────────────────────────

def _validate_ladder():
    """Pin the ratified ladder + the down-only invariant.

    A. Spec pin — TIER_MULTIPLIER matches the 2026-07-10 ratified values. A drift
       is a governance change (fresh ADR + strategy_lifecycle.md), not a code edit.
    B. Down-only invariant — every multiplier lies in [0.0, 1.0]. Authorization may
       only ever DE-risk; no lifecycle tier may size a position UP (Call 5:
       "automation moves authorization down only; always round down, never up").
    """
    expected = {"AUTHORIZED": 1.00, "WATCH-1": 0.50, "WATCH-2": 0.25, "RETIRED": 0.00}
    if TIER_MULTIPLIER != expected:
        raise AssertionError(
            f"MVD spec drift: lifecycle TIER_MULTIPLIER {TIER_MULTIPLIER} != ratified "
            f"{expected}. A change needs a fresh ADR + strategy_lifecycle.md update, "
            f"not a code edit."
        )
    if not all(0.0 <= m <= 1.0 for m in TIER_MULTIPLIER.values()):
        raise AssertionError(
            f"lifecycle multipliers must lie in [0.0, 1.0] (down-only authorization): "
            f"{TIER_MULTIPLIER}"
        )
    # C. Call-4 beta-death control constants pinned (ratified 2026-07-10).
    if (BETA_SOFT_FLAG_COUNT, BETA_DEATH_COUNT, BETA_DEATH_DERISK) != (2, 3, 0.50):
        raise AssertionError(
            f"MVD spec drift: Call-4 beta constants "
            f"({BETA_SOFT_FLAG_COUNT}, {BETA_DEATH_COUNT}, {BETA_DEATH_DERISK}) != ratified "
            f"(2, 3, 0.50). A change needs a fresh ADR + strategy_lifecycle.md update."
        )
    # D. Ladder order and the multiplier table must cover exactly the same tiers.
    if set(_LADDER_ORDER) != set(TIER_MULTIPLIER):
        raise AssertionError(
            f"_LADDER_ORDER {_LADDER_ORDER} and TIER_MULTIPLIER keys "
            f"{sorted(TIER_MULTIPLIER)} disagree."
        )


_validate_ladder()
