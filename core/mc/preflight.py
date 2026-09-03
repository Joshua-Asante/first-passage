"""Engine pre-flight for prop-tier re-MC (constraint D + F1 bucket-sum assertion).

Additive module, OFF the anchor import path — no anchor-path module imports it
(portfolio_mc / dd_protection / mc.modes / mc.simulation / mc.ingest). Mirrors the
core/dd_geometry.py precedent: it exists so the prop-portfolio program's re-MC
harnesses thread firm configs into the engine correctly-by-construction and read
its outcome buckets faithfully, instead of re-deriving the pattern (and
re-introducing the F1 headline-bust trap) in every one-off harness — as
lab/analysis/tradeify_futures3_remc_2026-07-11/run_tradeify_futures3_remc.py did
inline, without the bucket-sum assertion.

Discharges the two engine findings the ratified survivor-scoring recommendation
(docs/briefs/programs/2026-07-12-survivor-scoring-and-ddp-reframe-recommendation.md
§0 constraint D + §1 F1; scorecard G3) requires GREEN before any prop-tier re-MC:

  * Constraint D — firm configs with daily_loss_pct=None must thread into
    simulate_path without a TypeError. The import-time module constants in
    dd_protection / mc.modes / mc.simulation / scripts.inactivity_simulator are
    now None-tolerant (byte-identical under ACTIVE_FIRM=FXIFY); firm_kwargs()
    threads the None through at runtime, where simulate_path's daily-loss gate is
    already None-safe (core/mc/simulation.py:61-64).

  * F1 — the headline bust for a prop tier is daily+static+TRAILING. Reading
    compute_default_config()['bust_rate'] (daily+static only, mc/modes.py) reports
    ~0% for a trailing-geometry tier because every bust routes to bust_trailing.
    summarize_outcomes() aggregates all bust buckets AND asserts every seed's
    outcome buckets partition n_sims exactly (bucket-sum == sims_per_seed).

Governance: this module does NOT switch ACTIVE_FIRM, touch any locked parameter or
the MC anchor (99.83/0.17/4.37), or overturn R6 NO-GO. It is harness plumbing for
the greenfield prop-portfolio program, whose own live existence is gated by the
2026-11-08 four-firms-ADR §4 falsifier. F2 (fixed-$ vs %-of-peak faithfulness for
the `trailing` firms) is a modeling caveat this module does NOT correct — callers
must still label Bulenox/BluSky results optimistic-lower-bounds.
"""

from __future__ import annotations

from typing import Dict, Sequence, Tuple

import numpy as np

try:  # dual-import: works whether core/ is a package or flat on sys.path
    from ..dd_protection import DD_SCALE, DD_TRIGGER
    from ..firm_rules import FIRM_RULES
    from ..historical_challenge import HISTORICAL_CHALLENGE_BALANCE
    from .simulation import HORIZON_CAP, simulate_path
except ImportError:  # pragma: no cover - exercised via the flat-path harnesses
    from dd_protection import DD_SCALE, DD_TRIGGER
    from firm_rules import FIRM_RULES
    from historical_challenge import HISTORICAL_CHALLENGE_BALANCE
    from mc.simulation import HORIZON_CAP, simulate_path

# Canonical outcome partition produced by simulation.run_seed. Kept here so the
# F1 assertion fails loudly if the engine's bucket set ever changes without this
# module tracking it (the bucket-sum invariant is a statement about THIS set).
OUTCOME_KEYS: Tuple[str, ...] = (
    "pass",
    "bust_daily",
    "bust_static",
    "bust_trailing",
    "bust_inactivity",
    "horizon_cap",
)

# The three buckets that count as a real bust for a prop tier. bust_daily and
# bust_static stay in the sum for firms that have those limits (and so the same
# helper reproduces the FXIFY headline); bust_trailing is the one the naive
# compute_default_config() headline omits (F1).
BUST_KEYS: Tuple[str, ...] = ("bust_daily", "bust_static", "bust_trailing")

# Sentinel: inactivity disabled (**barrier-off**). Two claims, kept separate:
# (1) LEGALITY — a token weekly trade is compatible with surveyed firm activity
# rules (2026-08-05 sweep: no min-hold/scalping bar at Bulenox/MFFU/BluSky) — kept.
# (2) MITIGATION — automated barrier-defeating token trades remain UNDELIVERED at
# the execution layer (residual R8). ⚠ FU-1 (2026-08-05) authorizes one *manual*
# operator token trade by 2026-08-07 as lapse-prevention at the de-scoped venue;
# that is NOT the modelled automated mitigation. Barrier-ON limits are per-firm
# in firm_rules.py — do not transcribe percentages here. Every published inactivity-
# OFF figure is barrier-off. Matches the harness INACT_OFF idiom.
#
# ⚠ READ THIS BEFORE QUOTING ANY PROP-TIER BUST/PASS FIGURE (added 2026-09-03).
# `firm_kwargs` defaults `inactivity_off=True`, so **every published prop-tier
# bust/pass number in this repo assumes the barrier is OFF** unless its own file
# says otherwise — including the Part A figures, the A2 feasibility map, and the
# ORB campaign cells. That is a deliberate modelling choice, not an oversight:
# the operator maintains a standing weekly venue-idle token trade that satisfies
# the rule when the strategy itself has not fired (CLAUDE.md §Live-execution
# posture; one such trade executed 2026-08-12). The choice is PRICED, twice:
#   * lab/analysis/c1/c1_cadence_inactivity_2026-08-02   — 92.6-97.6% path death
#   * lab/analysis/orb/orb_mym_v04_riskbudget_2026-09-02 — §5c + inactivity_
#     barrier_check.json: 74.8-100% pure-inactivity failure across every cell
#     tested, including one at 39.7% trade-day density.
# So the inactivity-ON re-MC has been RUN and is degenerate: with the barrier on
# and no token trade, nearly every path dies of inactivity before its edge can
# express. Turning it on repo-wide would not refine the published pins, it would
# replace them with a measurement of the token-trade mitigation's absence. Do not
# re-litigate this as a fresh finding — the correct disclosure is this comment,
# stated where the figures are read.
#
# ⚠ AND the barrier is an UPPER BOUND, not a model of the venue rule. Tradeify's
# rule is ">=1 trade per Mon-Fri week" (art. 10468318), a per-week BUCKET;
# simulation.py counts ROLLING consecutive idle business days and fires at
# `inactivity_max_idle_days`. Those are not the same predicate. Every real
# violation trips the counter (5 idle bdays inside one Mon-Fri week is 5
# consecutive), so the barrier never MISSES a breach — but it also fires on
# calendars the venue permits. Measured 2026-09-03 against this engine: trades on
# Mon-wk1 / Fri-wk2 / Mon-wk3 / Fri-wk4 satisfies the venue in all four weeks and
# still returns `bust_inactivity` on day 6. Consequence: barrier-ON inactivity
# rates are conservative ceilings on true venue-inactivity risk, not estimates of
# it. Modelling the bucket rule faithfully is unspent work needing its own ADR;
# `ops/sentinel/activity_week.py` is the only surface that implements the real
# Mon-Fri bucket, and it is report-only.
INACTIVITY_OFF: int = HORIZON_CAP + 1


def firm_kwargs(
    firm_key: str,
    *,
    inactivity_off: bool = True,
    consistency: float | None = None,
    account: float | None = None,
    allow_unsourced_inactivity: bool = False,
) -> Dict[str, object]:
    """Build the simulate_path kwargs for a FIRM_RULES tier, None-safely.

    Threads daily_loss_pct through as None when the tier has no daily loss limit
    (constraint D), and dispatches on ``dd_type`` so the correct barrier geometry
    is expressed:

      * ``static``           -> static_dd_pct only (FXIFY-shaped fixed floor)
      * ``trailing``         -> trailing_dd_pct (%-of-peak; F2 optimistic for the
                                Bulenox/BluSky fixed-$ rules — caller labels it)
      * ``trailing_locking`` -> trailing_dd_pct + dd_lock_offset_usd (engine-
                                faithful fixed-$ EOD trail with lock; Tradeify/MFFU)

    ``account`` overrides the tier's ``starting_balance``. Every living prop
    tier must declare ``starting_balance`` — there is no $200K fallback
    (``BASELINE_BALANCE`` retired Phase 4). Pass ``account=`` explicitly for
    research bases that differ from the tier. ``consistency`` sets the eval
    consistency fraction (Run-2 gating); None runs consistency-off (Run-1).

    ``allow_unsourced_inactivity`` is the explicit override for an inactivity-ON
    run against a tier whose ``inactivity_rule_sourced`` is False. **Dormant by
    design at HEAD:** no shipped tier currently carries that flag (do not
    enumerate instances here — they drift; owner is ``core/firm_rules.py``).
    Absent the key ⇒ treated as sourced. The engine barrier is absorbing, so a
    wrong limit would silently decide the result — that is why the guard exists.
    Inactivity-OFF (the default; every published figure is **barrier-off**) never
    consults it. Per-firm barrier-ON idle limits live only in ``firm_rules.py``.
    """
    if firm_key not in FIRM_RULES:
        raise KeyError(
            f"{firm_key!r} not in FIRM_RULES; known keys: {sorted(FIRM_RULES)}"
        )
    f = FIRM_RULES[firm_key]

    if account is not None:
        bal = float(account)
    elif "starting_balance" in f:
        bal = float(f["starting_balance"])
    else:
        raise KeyError(
            f"{firm_key!r} has no starting_balance; pass account= explicitly "
            f"(historical $200K basis: historical_challenge.HISTORICAL_CHALLENGE_BALANCE="
            f"{HISTORICAL_CHALLENGE_BALANCE})"
        )
    dlp = f.get("daily_loss_pct")

    # Absorbing-barrier guard: a tier whose activity rule was never sourced must
    # not silently produce an inactivity figure. Absent the key => sourced (every
    # tier whose value cites a venue article). See the BluSky INACTIVITY RULE —
    # SOURCED block in firm_rules.py and ADR 2026-08-05b-blusky-inactivity-rule-sourced
    # (which supersedes the 2026-08-05 containment ADR).
    if not inactivity_off and not f.get("inactivity_rule_sourced", True):
        if not allow_unsourced_inactivity:
            raise ValueError(
                f"{firm_key!r} has inactivity_rule_sourced=False: its "
                f"inactivity_max_idle_days={f['inactivity_max_idle_days']} is NOT a "
                f"published activity rule (see the BluSky INACTIVITY RULE — SOURCED "
                f"block in firm_rules.py and ADR 2026-08-05b-blusky-inactivity-rule-sourced). "
                f"The engine treats this limit as an ABSORBING barrier, so running "
                f"inactivity-ON here reports an assumption as a measurement. Either "
                f"source the venue's real rule and set inactivity_rule_sourced=True, "
                f"or pass allow_unsourced_inactivity=True to declare explicitly that "
                f"the number is an assumption and label the result accordingly."
            )

    kwargs: Dict[str, object] = {
        "starting_equity": bal,
        "daily_loss_pct": (None if dlp is None else -dlp / 100),
        "profit_target": bal * (1 + f["profit_target_pct"] / 100),
        "min_trading_days": f["min_trading_days"],
        "inactivity_limit": (INACTIVITY_OFF if inactivity_off else f["inactivity_max_idle_days"]),
        "consistency_frac": consistency,
    }

    dd_type = f.get("dd_type", "static")
    if dd_type == "static":
        kwargs["dd_type"] = "static"
        kwargs["static_dd_pct"] = -f["max_dd_pct"] / 100
    elif dd_type == "trailing":
        kwargs["dd_type"] = "trailing"
        kwargs["trailing_dd_pct"] = -f["max_dd_pct"] / 100
    elif dd_type == "trailing_locking":
        if "dd_lock_offset_usd" not in f:
            raise ValueError(
                f"{firm_key!r} is dd_type=trailing_locking but has no "
                f"dd_lock_offset_usd; the fixed-$ lock point is undefined."
            )
        kwargs["dd_type"] = "trailing_locking"
        kwargs["trailing_dd_pct"] = -f["max_dd_pct"] / 100
        kwargs["dd_lock_offset_usd"] = float(f["dd_lock_offset_usd"])
    else:
        raise ValueError(
            f"{firm_key!r} has unknown dd_type {dd_type!r}; expected one of "
            f"'static' | 'trailing' | 'trailing_locking'."
        )
    return kwargs


def assert_engine_ready(firm_key: str) -> Dict[str, object]:
    """Constraint-D gate: prove ``firm_key`` threads into simulate_path cleanly.

    Builds firm_kwargs and runs one deterministic simulate_path over a synthetic
    zero-P&L path (no bust, no pass — just exercises every barrier branch and the
    daily-loss gate). Raises on any TypeError/KeyError the config would trigger;
    returns the built kwargs on success. Call this on each pre-registered tier
    before trusting its re-MC (recommendation §2.1 G3).
    """
    kwargs = firm_kwargs(firm_key)
    # 12 idle days × 3 synthetic legs: enough to walk the barrier branches; with
    # inactivity disabled it terminates at horizon_cap without raising.
    zero_path = np.zeros((12, 3), dtype=float)
    outcome, _day, _max_dd, _culprit = simulate_path(
        zero_path,
        dd_trigger=DD_TRIGGER,
        dd_scale=DD_SCALE,
        horizon=len(zero_path),
        **kwargs,
    )
    if outcome not in OUTCOME_KEYS:
        raise AssertionError(
            f"engine pre-flight for {firm_key!r} returned unknown outcome "
            f"{outcome!r}; expected one of {OUTCOME_KEYS}."
        )
    return kwargs


def summarize_outcomes(
    seeds_results: Sequence[dict],
    sims_per_seed: int,
) -> Dict[str, object]:
    """Aggregate run_seed outcomes into faithful headline rates (F1).

    For each seed asserts the outcome buckets (a) carry exactly OUTCOME_KEYS and
    (b) sum to ``sims_per_seed`` — the bucket-sum==1.0 invariant that catches a
    dropped/renamed bucket or a mis-seeded run before any verdict rests on it.
    Returns per-bucket mean rates plus ``headline_bust`` = mean(daily+static+
    trailing), which is the number a prop verdict must read — NOT
    compute_default_config()['bust_rate'].
    """
    if not seeds_results:
        raise ValueError("summarize_outcomes: seeds_results is empty")
    if sims_per_seed <= 0:
        raise ValueError(f"summarize_outcomes: sims_per_seed must be > 0, got {sims_per_seed}")

    expected = set(OUTCOME_KEYS)
    for i, r in enumerate(seeds_results):
        oc = r["outcomes"]
        if set(oc) != expected:
            raise AssertionError(
                f"seed[{i}] outcome keys {sorted(oc)} != canonical {sorted(expected)} "
                f"(engine bucket set drifted from preflight.OUTCOME_KEYS)."
            )
        total = sum(oc.values())
        if total != sims_per_seed:
            raise AssertionError(
                f"F1 bucket-sum violation: seed[{i}] outcome buckets sum to {total}, "
                f"expected {sims_per_seed}. Buckets must partition the sim count exactly."
            )

    rates = {
        k: float(np.mean([r["outcomes"][k] / sims_per_seed for r in seeds_results]))
        for k in OUTCOME_KEYS
    }
    headline_bust = float(sum(rates[k] for k in BUST_KEYS))
    return {
        "rates": rates,
        "headline_bust": headline_bust,
        "pass_rate": rates["pass"],
        "n_seeds": len(seeds_results),
        "sims_per_seed": sims_per_seed,
    }
