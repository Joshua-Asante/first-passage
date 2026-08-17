#!/usr/bin/env python3
"""Q-POLFRONT-1 — policy-augmented seed-target frontier.

Runs ONLY what OPERATIONALIZATION.md (committed first) freezes:
frozen 30-cell grid (union of seed-target-spec sections A+D (w,b) pairs x k in {1,2,4}),
constant-R control vs cushion-proportional policy P_c (cap 1.0), common-random-numbers
seeding, quantized + intraday-sensitivity disclosure arms. Emits out/polfront_results.json.

Reuses lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/run_seed_spec.py's simulate()/
max_risk() UNMODIFIED for the control arm's admission search; a local stress variant of the
same day-loop (constant r, doubled within-day low) supplies the flat arm's disclosure-only
intraday-sensitivity number. The policy arm is a day-indexed generalization of the same
day-loop with a start-of-day-state multiplier (same technique as
lab/analysis/c1/q_evalseq_1_2026-08/run_evalseq.py's eval_sim_policy, ported to this harness's
per-day-not-per-trade-panel granularity).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SEED_SPEC_DIR = HERE.parent / "tradeify_seed_target_spec_2026-08-04"
sys.path.insert(0, str(SEED_SPEC_DIR))

from run_seed_spec import (  # noqa: E402
    ROPE, TARGET, MIN_DAYS, CONSIST,
    EVAL_BUST_CEILING, PASS_FLOOR, HORIZON_BDAYS,
    max_risk as max_risk_flat,
)

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

SEED = 101
N_SIMS = 6000
R_LO, R_HI, R_STEP = 50, 1600, 25          # flat arm: unchanged, matches the seed-spec's own range
POLICY_R_HI = int(ROPE)                     # policy arm: widened to the theoretical ceiling (see
                                             # OPERATIONALIZATION.md amendment — r_base >= ROPE
                                             # guarantees a single full-cushion losing trade alone
                                             # breaches, confirmed numerically: bust jumps to 83.7%
                                             # at r=ROPE for the fastest-crossing probed cell)
QUANTA = (25.0, 50.0, 85.0)

PAIRS = [
    (0.55, 2.0), (0.60, 2.0), (0.50, 2.0), (0.45, 2.5),  # sec A (T7)
    (0.45, 2.0), (0.40, 2.0), (0.35, 2.0),                # sec D additions
    (0.55, 1.2), (0.50, 1.2), (0.45, 1.2),                # sec D additions
]
KS = (1, 2, 4)


def simulate_flat_stress(w, b, r, k, n_sims=N_SIMS, horizon=HORIZON_BDAYS, seed=SEED):
    """Constant-r day loop, identical to run_seed_spec.simulate(duty=1.0, inactivity=False),
    with the within-day low excursion doubled before the bust test (exploratory stress read
    at an already-fixed r; not a re-sweep)."""
    rng = np.random.default_rng(seed)
    profit = np.zeros(n_sims)
    peak = np.zeros(n_sims)
    best_day = np.zeros(n_sims)
    tdays = np.zeros(n_sims, dtype=int)
    status = np.zeros(n_sims, dtype=np.int8)
    pass_bday = np.full(n_sims, -1, dtype=int)

    for bday in range(horizon):
        live = status == 0
        if not live.any():
            break
        n = int(live.sum())
        pf, pk = profit[live], peak[live]

        wins = rng.random((n, k)) < w
        steps = np.where(wins, b * r, -r)
        cum = np.cumsum(steps, axis=1)
        day_pnl = cum[:, -1]
        day_low = np.minimum(cum.min(axis=1), 0.0) * 2.0  # stress: doubled magnitude

        floor = pk - ROPE
        breach = np.minimum(pf + day_low, pf + day_pnl) <= floor

        pf_new = pf + day_pnl
        pk_new = np.maximum(pk, pf_new)
        bd_new = np.maximum(best_day[live], day_pnl)
        td_new = tdays[live] + 1

        passed = (
            (~breach) & (pf_new >= TARGET) & (td_new >= MIN_DAYS)
            & (bd_new <= CONSIST * np.maximum(pf_new, 1e-9))
        )

        st = np.zeros(n, dtype=np.int8)
        st[breach] = 2
        st[passed & ~breach] = 1

        stop = breach
        profit[live] = np.where(stop, pf, pf_new)
        peak[live] = np.where(stop, pk, pk_new)
        best_day[live] = np.where(stop, best_day[live], bd_new)
        tdays[live] = np.where(stop, tdays[live], td_new)

        idx = np.flatnonzero(live)
        status[idx] = st
        pass_bday[idx[st == 1]] = bday + 1

    p = status == 1
    return {"pass": round(100.0 * float(p.mean()), 2),
            "bust": round(100.0 * float((status == 2).mean()), 2)}


def simulate_policy(w, b, r_base, k, n_sims=N_SIMS, horizon=HORIZON_BDAYS, seed=SEED,
                     stress=False):
    """Day-indexed port of simulate() with a start-of-day cushion-proportional multiplier.

    r_t = r_base * min(1, max(0, cushion_t) / ROPE); cushion_t = profit_t - (peak_t - ROPE).
    inactivity=False and duty=1.0 throughout (matches the flat control's own config, per
    OPERATIONALIZATION.md). stress=True doubles the within-day low excursion magnitude
    (exploratory intraday-sensitivity arm; does not change day_pnl/close).
    """
    rng = np.random.default_rng(seed)
    profit = np.zeros(n_sims)
    peak = np.zeros(n_sims)
    best_day = np.zeros(n_sims)
    tdays = np.zeros(n_sims, dtype=int)
    status = np.zeros(n_sims, dtype=np.int8)  # 0 live, 1 pass, 2 bust
    pass_bday = np.full(n_sims, -1, dtype=int)

    for bday in range(horizon):
        live = status == 0
        if not live.any():
            break
        n = int(live.sum())
        pf, pk = profit[live], peak[live]

        cushion = pf - (pk - ROPE)
        m = np.minimum(1.0, np.maximum(0.0, cushion) / ROPE)
        r_t = r_base * m

        wins = rng.random((n, k)) < w
        steps = np.where(wins, b * r_t[:, None], -r_t[:, None])
        cum = np.cumsum(steps, axis=1)
        day_pnl = cum[:, -1]
        day_low = np.minimum(cum.min(axis=1), 0.0)
        if stress:
            day_low = day_low * 2.0

        floor = pk - ROPE
        breach = np.minimum(pf + day_low, pf + day_pnl) <= floor

        pf_new = pf + day_pnl
        pk_new = np.maximum(pk, pf_new)
        bd_new = np.maximum(best_day[live], day_pnl)
        td_new = tdays[live] + 1

        passed = (
            (~breach)
            & (pf_new >= TARGET)
            & (td_new >= MIN_DAYS)
            & (bd_new <= CONSIST * np.maximum(pf_new, 1e-9))
        )

        st = np.zeros(n, dtype=np.int8)
        st[breach] = 2
        st[passed & ~breach] = 1

        stop = breach
        profit[live] = np.where(stop, pf, pf_new)
        peak[live] = np.where(stop, pk, pk_new)
        best_day[live] = np.where(stop, best_day[live], bd_new)
        tdays[live] = np.where(stop, tdays[live], td_new)

        idx = np.flatnonzero(live)
        status[idx] = st
        pass_bday[idx[st == 1]] = bday + 1

    p = status == 1
    return {
        "pass": round(100.0 * float(p.mean()), 2),
        "bust": round(100.0 * float((status == 2).mean()), 2),
        "slow": round(100.0 * float((status == 0).mean()), 2),
        "med_bdays": float(np.nanmedian(pass_bday[p])) if p.any() else None,
    }


def max_risk_policy(w, b, k, tolerance, n_sims=N_SIMS, seed=SEED,
                     r_lo=R_LO, r_hi=POLICY_R_HI, step=R_STEP):
    best = None
    for r in range(r_lo, r_hi, step):
        s = simulate_policy(w, b, r, k, n_sims=n_sims, seed=seed)
        if s["bust"] <= tolerance and s["pass"] >= PASS_FLOOR:
            best = (r, s)
        elif s["bust"] > tolerance:
            break
    return best


def quantize(r, q):
    return (r // q) * q if r is not None else None


def main():
    results = []
    for (w, b) in PAIRS:
        for k in KS:
            flat = max_risk_flat(w, b, k, EVAL_BUST_CEILING, n_sims=N_SIMS, seed=SEED)
            pol = max_risk_policy(w, b, k, EVAL_BUST_CEILING, n_sims=N_SIMS, seed=SEED)

            r_flat = flat[0] if flat else None
            r_pol = pol[0] if pol else None
            row = {
                "w": w, "b": b, "k": k,
                "edge_R": round(w * b - (1 - w), 4),
                "r_flat_max": r_flat, "flat_pass": flat[1]["pass"] if flat else None,
                "flat_bust": flat[1]["bust"] if flat else None,
                "r_policy_max": r_pol, "policy_pass": pol[1]["pass"] if pol else None,
                "policy_bust": pol[1]["bust"] if pol else None,
            }
            row["policy_near_ceiling"] = bool(r_pol is not None and r_pol >= POLICY_R_HI - R_STEP)
            if r_flat is not None and r_pol is not None:
                row["ratio"] = round(r_pol / r_flat, 3)
                row["newly_admitted"] = False
            elif r_flat is None and r_pol is not None:
                row["ratio"] = None
                row["newly_admitted"] = True
            else:
                row["ratio"] = None
                row["newly_admitted"] = False

            # quantized disclosure arm (§5 mandatory)
            row["quantized"] = {}
            for q in QUANTA:
                qf, qp = quantize(r_flat, q), quantize(r_pol, q)
                row["quantized"][str(q)] = {
                    "r_flat_q": qf, "r_policy_q": qp,
                    "ratio_q": round(qp / qf, 3) if (qf and qp) else None,
                }

            # intraday-sensitivity disclosure arm (§5 mandatory; exploratory)
            row["intraday_stress"] = {}
            if r_flat is not None:
                fs = simulate_flat_stress(w, b, r_flat, k, n_sims=N_SIMS, seed=SEED)
                row["intraday_stress"]["flat_bust_stressed"] = fs["bust"]
                row["intraday_stress"]["flat_bust_delta"] = round(fs["bust"] - row["flat_bust"], 2)
            if r_pol is not None:
                ps = simulate_policy(w, b, r_pol, k, n_sims=N_SIMS, seed=SEED, stress=True)
                row["intraday_stress"]["policy_bust_stressed"] = ps["bust"]
                row["intraday_stress"]["policy_bust_delta"] = round(ps["bust"] - row["policy_bust"], 2)

            results.append(row)
            print(f"w={w} b={b} k={k}: flat ${r_flat} ({flat[1]['pass'] if flat else '-'}%/"
                  f"{flat[1]['bust'] if flat else '-'}%)  policy ${r_pol} "
                  f"({pol[1]['pass'] if pol else '-'}%/{pol[1]['bust'] if pol else '-'}%)  "
                  f"ratio={row['ratio']}  newly_admitted={row['newly_admitted']}")

    (OUT / "polfront_results.json").write_text(json.dumps(results, indent=2))
    print(f"\nsaved -> {OUT / 'polfront_results.json'}")


if __name__ == "__main__":
    main()
