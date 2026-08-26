"""Follow-up analysis (2026-08-26b): H7, H8, and a proper both-halves
regime-robustness bootstrap for the flagship combined-book sizing.

Addresses three open hypotheses from RESULTS.md's original §8:

  H7 -- both equal-risk sizing ratios rested on a single historical worst
        day per leg. Recomputes the ratio from each leg's own
        block-bootstrap-resampled 95th-percentile drawdown instead, then
        re-runs the combined bootstrap at that corrected sizing.
  H8 -- the correlation/diversification benefit (original RESULTS.md S4)
        was only measured at 2.5:1/1.25:1 proxy ratios, not the actual
        ~13-30:1 flagship mix. Re-runs the real-vs-independence-null
        bootstrap at the actual flagship sizing.
  Regime robustness -- the original S5 was a single deterministic path per
        scenario, not a bootstrap. Replaces it with a genuine both-halves
        block-bootstrap (per docs/methodology/regime_robustness_gate.md):
        split the window in half, block-bootstrap WITHIN each half
        independently, require both to clear.

Reuses combined_sim.py (itself a thin wrapper around
core/mc/simulation.py::simulate_path/run_seed and
core/mc/preflight.py::firm_kwargs/summarize_outcomes) throughout. The only
new logic is an independent-per-leg block-bootstrap for the H8 null (a
minimal fork of run_seed: one shared RNG draw for all legs vs one
independent RNG stream per leg -- see run_seed_independent_legs) and a
plain-numpy 95th-percentile max-drawdown bootstrap for H7 (no barrier
logic -- pure cumulative peak-to-trough on resampled weekly blocks).

Uses the CORRECTED ORB-MNQ series throughout (sliced from the 6-year
export to match each Aegis window exactly), NOT the stale orbmnq_1yr.json/
orbmnq_3yr.json files, which are the original pre-H5/H6-correction data
kept only for the §1 reconciliation record.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import combined_sim as cs  # noqa: E402
from mc.simulation import simulate_path, HORIZON_CAP  # noqa: E402
from mc.preflight import firm_kwargs as _firm_kwargs, summarize_outcomes, OUTCOME_KEYS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DAILY = os.path.join(HERE, "data", "daily_pnl")
OUT_DIR = os.path.join(HERE, "data")

FIRM_KEY = "Tradeify_Select_100K"
CONSISTENCY = 0.40
SEEDS = (1, 2, 3, 4, 5)
N_SIMS = 2000


def load_corrected():
    aegis_1yr = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "aegis_1yr.json"))
    aegis_3yr = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "aegis_3yr.json"))
    orbmnq_6yr = cs.load_daily_pnl_per_contract(os.path.join(DAILY, "orbmnq_6yr.json"))
    orbmnq_1yr = orbmnq_6yr.loc[aegis_1yr.index.min():aegis_1yr.index.max()]
    orbmnq_3yr = orbmnq_6yr.loc[aegis_3yr.index.min():aegis_3yr.index.max()]
    return aegis_1yr, aegis_3yr, orbmnq_1yr, orbmnq_3yr


# ---------------------------------------------------------------------------
# H8 -- independence-null bootstrap at the real flagship sizing
# ---------------------------------------------------------------------------

def run_seed_independent_legs(seed, n_sims, blocks_by_leg, leg_order, dd_trigger, dd_scale, horizon, firm_kwargs):
    """Parallel of core.mc.simulation.run_seed, except each leg's weekly
    blocks are drawn from an INDEPENDENT rng stream (numpy SeedSequence
    substream per leg) instead of one shared index array for every leg --
    breaks real day-to-day alignment while preserving each leg's own
    marginal weekly-block distribution."""
    n_blocks = len(blocks_by_leg[leg_order[0]])
    blocks_per_sim = (horizon + 4) // 5
    rngs = {leg: np.random.default_rng((seed, i)) for i, leg in enumerate(leg_order)}
    outcomes = {k: 0 for k in OUTCOME_KEYS}
    days_to_pass, max_dds = [], []
    bust_attribution = {leg: 0 for leg in leg_order}
    for _ in range(n_sims):
        leg_paths = []
        for leg in leg_order:
            idx = rngs[leg].integers(0, n_blocks, blocks_per_sim)
            leg_paths.append(np.concatenate([blocks_by_leg[leg][i] for i in idx])[:horizon])
        path = np.stack(leg_paths, axis=1)
        outcome, day, max_dd, culprit = simulate_path(path, dd_trigger, dd_scale, horizon, **firm_kwargs)
        outcomes[outcome] += 1
        max_dds.append(max_dd)
        if outcome == "pass":
            days_to_pass.append(day)
        elif outcome in ("bust_daily", "bust_static", "bust_trailing") and culprit is not None:
            bust_attribution[leg_order[culprit]] += 1
    return {"outcomes": outcomes, "days_to_pass": days_to_pass, "max_dds": max_dds, "bust_attribution": bust_attribution}


def independence_null_sweep(leg_series, leg_contracts, start, end, firm_key=FIRM_KEY, consistency=CONSISTENCY,
                             n_sims=N_SIMS, seeds=SEEDS, horizon=HORIZON_CAP, dd_trigger=1.0, dd_scale=1.0):
    path, date_index, leg_order = cs.build_combined_path(leg_series, leg_contracts, start=start, end=end)
    n_days, n_legs = path.shape
    n_weeks = n_days // 5
    usable_days = n_weeks * 5
    blocks_full = path[:usable_days].reshape(n_weeks, 5, n_legs)
    blocks_by_leg = {leg: blocks_full[:, :, i] for i, leg in enumerate(leg_order)}
    fkw = _firm_kwargs(firm_key, consistency=consistency)
    seed_results = [run_seed_independent_legs(s, n_sims, blocks_by_leg, leg_order, dd_trigger, dd_scale, horizon, fkw) for s in seeds]
    summary = summarize_outcomes(seed_results, n_sims)
    summary["leg_order"] = leg_order
    summary["n_weeks_available"] = n_weeks
    return summary


def h8_run_pair(label, leg_series, leg_contracts, start, end):
    real = cs.bootstrap_block_sweep(leg_series, leg_contracts, firm_key=FIRM_KEY, consistency=CONSISTENCY, n_sims=N_SIMS, seeds=SEEDS, start=start, end=end)
    null = independence_null_sweep(leg_series, leg_contracts, start, end, firm_key=FIRM_KEY, consistency=CONSISTENCY, n_sims=N_SIMS, seeds=SEEDS)
    return {
        "label": label, "leg_contracts": leg_contracts, "start": str(start), "end": str(end),
        "real_headline_bust_pct": round(real["headline_bust"] * 100, 4),
        "null_headline_bust_pct": round(null["headline_bust"] * 100, 4),
        "bust_delta_pp_real_minus_null": round((real["headline_bust"] - null["headline_bust"]) * 100.0, 4),
        "n_weeks_available": real["n_weeks_available"], "n_seeds": real["n_seeds"], "sims_per_seed": real["sims_per_seed"],
    }


# ---------------------------------------------------------------------------
# H7 -- bootstrap-95th-percentile sizing ratio
# ---------------------------------------------------------------------------

def bootstrap_maxdd_percentile(series, horizon, pct=95, seeds=SEEDS, n_sims=N_SIMS):
    """Block-bootstrap (weekly blocks, with replacement) this leg's own
    per-contract daily P&L out to `horizon` days; return the requested
    percentile of the resulting max-drawdown (cumulative-equity peak-to-
    trough) distribution across all sims. Same block convention as
    core.mc.simulation.run_seed (5-day blocks); no barrier/firm logic --
    pure drawdown statistics for the sizing derivation."""
    vals = series.to_numpy(dtype=float)
    n_days = len(vals)
    n_weeks = n_days // 5
    usable = n_weeks * 5
    blocks = vals[:usable].reshape(n_weeks, 5)
    blocks_per_sim = (horizon + 4) // 5
    maxdds = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        for _ in range(n_sims):
            idx = rng.integers(0, n_weeks, blocks_per_sim)
            path = np.concatenate([blocks[i] for i in idx])[:horizon]
            cum = np.cumsum(path)
            peak = np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]
            maxdds.append((cum - peak).min())
    maxdds = np.asarray(maxdds)
    single_dd = float((np.cumsum(vals) - np.maximum.accumulate(np.cumsum(vals))).min())
    return {
        "n_paths": len(maxdds),
        "pct_dd": float(np.percentile(maxdds, 100 - pct)),
        "median_dd": float(np.median(maxdds)),
        "single_realized_dd": single_dd,
    }


def h7_derive_and_rerun(label, aegis_s, orbmnq_s, original_orbmnq_contracts):
    horizon = len(aegis_s)
    a = bootstrap_maxdd_percentile(aegis_s, horizon)
    o = bootstrap_maxdd_percentile(orbmnq_s, horizon)
    ratio_95 = abs(o["pct_dd"]) / abs(a["pct_dd"])
    aegis_contracts = 8.0 / 1.5  # unchanged: 6J cap-8 at the 1.5x tier, so 1.0x = 8/1.5
    orbmnq_contracts_95 = aegis_contracts / ratio_95
    sizing = {"aegis": round(aegis_contracts, 4), "orbmnq": round(orbmnq_contracts_95, 4)}
    sweep = cs.bootstrap_block_sweep({"aegis": aegis_s, "orbmnq": orbmnq_s}, sizing, start=aegis_s.index.min(), end=aegis_s.index.max())
    return {
        "horizon_days": horizon,
        "aegis_95th_dd_per_contract": round(a["pct_dd"], 2),
        "aegis_single_worst_day_dd_per_contract": round(a["single_realized_dd"], 2),
        "orbmnq_95th_dd_per_contract": round(o["pct_dd"], 2),
        "orbmnq_single_realized_dd_per_contract": round(o["single_realized_dd"], 2),
        "ratio_95th_aegis_to_orbmnq": round(ratio_95, 4),
        "sizing_H7_basis": sizing,
        "sizing_original_basis": {"aegis": round(aegis_contracts, 4), "orbmnq": original_orbmnq_contracts},
        "rerun_at_H7_sizing_headline_bust_pct": round(sweep["headline_bust"] * 100, 4),
        "rerun_at_H7_sizing_pass_rate_pct": round(sweep["pass_rate"] * 100, 4),
    }


# ---------------------------------------------------------------------------
# Regime robustness -- proper both-halves bootstrap
# ---------------------------------------------------------------------------

def regime_both_halves(label, aegis_s, orbmnq_s, sizing):
    mid = aegis_s.index[len(aegis_s.index) // 2]
    full = cs.bootstrap_block_sweep({"aegis": aegis_s, "orbmnq": orbmnq_s}, sizing, start=aegis_s.index.min(), end=aegis_s.index.max())
    h1 = cs.bootstrap_block_sweep({"aegis": aegis_s, "orbmnq": orbmnq_s}, sizing, start=aegis_s.index.min(), end=mid)
    h2 = cs.bootstrap_block_sweep({"aegis": aegis_s, "orbmnq": orbmnq_s}, sizing, start=mid, end=aegis_s.index.max())
    return {
        "sizing": sizing,
        "full_window_bust_pct": round(full["headline_bust"] * 100, 4), "full_n_weeks": full["n_weeks_available"],
        "h1_start": str(aegis_s.index.min()), "h1_end": str(mid),
        "h1_bust_pct": round(h1["headline_bust"] * 100, 4), "h1_n_weeks": h1["n_weeks_available"],
        "h2_start": str(mid), "h2_end": str(aegis_s.index.max()),
        "h2_bust_pct": round(h2["headline_bust"] * 100, 4), "h2_n_weeks": h2["n_weeks_available"],
        "both_halves_clear_3pct": bool(h1["headline_bust"] <= 0.03 and h2["headline_bust"] <= 0.03),
    }


if __name__ == "__main__":
    aegis_1yr, aegis_3yr, orbmnq_1yr, orbmnq_3yr = load_corrected()

    h8 = {}
    h8["1yr_flagship"] = h8_run_pair("1yr", {"aegis": aegis_1yr, "orbmnq": orbmnq_1yr}, {"aegis": 5.333333, "orbmnq": 0.18}, aegis_1yr.index.min(), aegis_1yr.index.max())
    h8["3yr_flagship"] = h8_run_pair("3yr", {"aegis": aegis_3yr, "orbmnq": orbmnq_3yr}, {"aegis": 5.333333, "orbmnq": 0.40}, aegis_3yr.index.min(), aegis_3yr.index.max())

    h7 = {}
    h7["1yr"] = h7_derive_and_rerun("1yr", aegis_1yr, orbmnq_1yr, 0.18)
    h7["3yr"] = h7_derive_and_rerun("3yr", aegis_3yr, orbmnq_3yr, 0.40)

    regime = {}
    regime["1yr"] = regime_both_halves("1yr", aegis_1yr, orbmnq_1yr, {"aegis": 5.333333, "orbmnq": 0.18})
    regime["3yr"] = regime_both_halves("3yr", aegis_3yr, orbmnq_3yr, {"aegis": 5.333333, "orbmnq": 0.40})

    out = {"h8_correlation_at_real_sizing": h8, "h7_bootstrap_sizing_ratio": h7, "regime_both_halves": regime}
    print(json.dumps(out, indent=2))
    with open(os.path.join(OUT_DIR, "followup_h7_h8_regime_results.json"), "w") as fh:
        json.dump(out, fh, separators=(",", ":"))
