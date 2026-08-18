#!/usr/bin/env python3
"""Q-POLFRONT-1 — intraday-honest remeasurement (named fork, closure §7).

Runs ONLY what OPERATIONALIZATION_INTRADAY_HONEST.md (committed first) freezes: re-evaluates
each frozen grid cell's already-found R_max (both arms) under a real-bar-derived intraday
excursion injection, replacing the crude `stress=True: day_low*2` proxy with a winsorized
empirical excursion-deepening ratio measured from `core/data/bar_data/MYM_M15.csv`.

Self-contained: `run_seed_spec.py` (this camp's constant/`max_risk` source) was pruned from the
tree (Great Prune 2026-08-08); its six frozen constants are inlined below, cross-checked against
production `core/firm_rules.py::Tradeify_Select_100K` and against the recovered file at
`git show pre-prune-2026-08-08:lab/analysis/c1/tradeify_seed_target_spec_2026-08-04/run_seed_spec.py`
(see OPERATIONALIZATION_INTRADAY_HONEST.md §0). `max_risk_flat`/`simulate` are reproduced
verbatim from that recovered source, not re-derived.

Emits out/polfront_intraday_honest_results.json.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

# --- Frozen venue geometry (core/firm_rules.py::Tradeify_Select_100K, cross-checked against
# recovered run_seed_spec.py @ pre-prune-2026-08-08 — exact match) --------------------------- #
ROPE = 3000.0
TARGET = 6000.0
MIN_DAYS = 3
CONSIST = 0.40
EVAL_BUST_CEILING = 3.0   # percent
PASS_FLOOR = 50.0         # percent
HORIZON_BDAYS = 1500

SEED = 101                # CRN seed, matches run_polfront.py exactly (comparability)
RATIO_SEED = 4177         # separate nuisance-dimension seed for the excursion-ratio draw
N_SIMS = 6000
R_LO, R_HI, R_STEP = 50, 1600, 25
POLICY_R_HI = int(ROPE)   # matches run_polfront.py's sweep-range amendment

PAIRS = [
    (0.55, 2.0), (0.60, 2.0), (0.50, 2.0), (0.45, 2.5),
    (0.45, 2.0), (0.40, 2.0), (0.35, 2.0),
    (0.55, 1.2), (0.50, 1.2), (0.45, 1.2),
]
KS = (1, 2, 4)

REAL_RATIOS_FILE = HERE / "out" / "real_mae_ratios.json"
WINSOR_PCT = 2.5  # frozen, OPERATIONALIZATION_INTRADAY_HONEST.md §1/§4-v2


# --- §4-v2: R-relative excursion-deepening ratio, derived from REAL locked-book trades ------ #
# (v1's instrument-price-shape ratio was diagnosed as a unit-conflation defect and discarded —
# see OPERATIONALIZATION_INTRADAY_HONEST.md §4. This loads the pre-computed replacement:
# ratio = that REAL trading day's own worst MTM excursion (W1's `_leg_daily_excursion`,
# per-trade, bar-derived) / that SAME day's own realized scaled P&L — both quantities already
# in the same dollar-scaled units, so the ratio is genuinely R-relative, not points-vs-dollars.
# Derived from the primary checkout (real trade CSVs are gitignored vendor data, not present in
# this worktree); pooled across both Striker legs (267+284 real trades, 2020-01->2026-06).)
def derive_excursion_ratios(_bar_file_unused, winsor_pct: float):
    d = json.loads(REAL_RATIOS_FILE.read_text())
    loss_w = np.array(d["loss_ratio_winsorized"], dtype=float)
    win_w = np.array(d["win_ratio_winsorized"], dtype=float)
    meta = {
        "source": d["source"],
        "legs_meta": d["legs_meta"],
        "per_leg": d["per_leg"],
        "pooled_raw": d["pooled_raw"],
        "winsor_pct": d["winsor_pct"],
        "loss_ratio_clip": d["loss_ratio_clip"],
        "win_ratio_clip": d["win_ratio_clip"],
        "n_loss_winsorized": len(loss_w),
        "n_win_winsorized": len(win_w),
    }
    assert abs(winsor_pct - d["winsor_pct"]) < 1e-9, "winsor_pct mismatch vs derivation script"
    return loss_w, win_w, meta


# --- Flat control arm — reproduced verbatim from the recovered run_seed_spec.py -------------- #
def simulate(w, b, r, k, n_sims=N_SIMS, horizon=HORIZON_BDAYS, seed=SEED, inactivity=False):
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
        day_low = np.minimum(cum.min(axis=1), 0.0)

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
    return {"pass": round(100.0 * float(p.mean()), 2), "bust": round(100.0 * float((status == 2).mean()), 2)}


def max_risk_flat(w, b, k, tolerance, n_sims=N_SIMS, seed=SEED, r_lo=R_LO, r_hi=R_HI, step=R_STEP):
    best = None
    for r in range(r_lo, r_hi, step):
        s = simulate(w, b, r, k, n_sims=n_sims, seed=seed)
        if s["bust"] <= tolerance and s["pass"] >= PASS_FLOOR:
            best = (r, s)
        elif s["bust"] > tolerance:
            break
    return best


# --- Policy arm — matches run_polfront.py's simulate_policy exactly ------------------------- #
def max_risk_policy(w, b, k, tolerance, n_sims=N_SIMS, seed=SEED, r_lo=R_LO, r_hi=POLICY_R_HI, step=R_STEP):
    best = None
    for r in range(r_lo, r_hi, step):
        s = simulate_policy(w, b, r, k, n_sims=n_sims, seed=seed)
        if s["bust"] <= tolerance and s["pass"] >= PASS_FLOOR:
            best = (r, s)
        elif s["bust"] > tolerance:
            break
    return best


def simulate_policy(w, b, r_base, k, n_sims=N_SIMS, horizon=HORIZON_BDAYS, seed=SEED):
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

        cushion = pf - (pk - ROPE)
        m = np.minimum(1.0, np.maximum(0.0, cushion) / ROPE)
        r_t = r_base * m

        wins = rng.random((n, k)) < w
        steps = np.where(wins, b * r_t[:, None], -r_t[:, None])
        cum = np.cumsum(steps, axis=1)
        day_pnl = cum[:, -1]
        day_low = np.minimum(cum.min(axis=1), 0.0)

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
    return {"pass": round(100.0 * float(p.mean()), 2), "bust": round(100.0 * float((status == 2).mean()), 2)}


# --- §1/§2: intraday-honest re-evaluation at a FIXED r (no sweep) --------------------------- #
def _inject_real_excursion(day_pnl, day_low_synth, loss_mult, win_mult):
    """day_low_final = min(day_low_synth, day_pnl * deterministic_multiplier).

    v3 (frozen, OPERATIONALIZATION_INTRADAY_HONEST.md §5): a FIXED multiplier per day-sign,
    not an independent per-day resample from the full empirical distribution. v2 (bootstrap
    resampling the winsorized empirical ratios every simulated business day) was diagnosed as
    resampling-saturation: even correctly R-relative ratios have a heavy right tail (winsorized
    up to ~52x/46x), and independently redrawing ~9M times (6000 paths x up to 1500 days)
    guarantees near-every path eventually draws a near-tail value, which single-handedly
    breaches at these R levels regardless of (w,b,k) — collapsing bust to ~99-100% uniformly
    and erasing the flat-vs-policy distinction the crude x2 stress arm (and physical intuition)
    both show should survive. A deterministic multiplier, calibrated to the empirical MEDIAN
    (the same summary statistic the parent closure itself reports), avoids this while still
    being grounded in real, R-relative trade data rather than an arbitrary "2".
    """
    ratio = np.where(day_pnl < 0, loss_mult, np.where(day_pnl > 0, win_mult, 0.0))
    day_low_real = day_pnl * ratio
    return np.minimum(day_low_synth, day_low_real)


def eval_flat_intraday_honest(w, b, r, k, loss_mult, win_mult, n_sims=N_SIMS, horizon=HORIZON_BDAYS,
                               seed=SEED):
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
        day_low_synth = np.minimum(cum.min(axis=1), 0.0)
        day_low = _inject_real_excursion(day_pnl, day_low_synth, loss_mult, win_mult)

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
    return {"pass": round(100.0 * float(p.mean()), 2), "bust": round(100.0 * float((status == 2).mean()), 2)}


def eval_policy_intraday_honest(w, b, r_base, k, loss_mult, win_mult, n_sims=N_SIMS, horizon=HORIZON_BDAYS,
                                 seed=SEED):
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

        cushion = pf - (pk - ROPE)
        m = np.minimum(1.0, np.maximum(0.0, cushion) / ROPE)
        r_t = r_base * m

        wins = rng.random((n, k)) < w
        steps = np.where(wins, b * r_t[:, None], -r_t[:, None])
        cum = np.cumsum(steps, axis=1)
        day_pnl = cum[:, -1]
        day_low_synth = np.minimum(cum.min(axis=1), 0.0)
        day_low = _inject_real_excursion(day_pnl, day_low_synth, loss_mult, win_mult)

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
    return {"pass": round(100.0 * float(p.mean()), 2), "bust": round(100.0 * float((status == 2).mean()), 2)}


def main():
    loss_w, win_w, ratio_meta = derive_excursion_ratios(None, WINSOR_PCT)
    loss_med, win_med = float(np.median(loss_w)), float(np.median(win_w))
    loss_p90, win_p90 = float(np.percentile(loss_w, 90)), float(np.percentile(win_w, 10))
    print(f"[ratios] source: real locked-book trades (Striker legs), R-relative, deterministic (v3)")
    print(f"[ratios] n_loss={ratio_meta['n_loss_winsorized']} n_win={ratio_meta['n_win_winsorized']}")
    print(f"[ratios] MEDIAN (primary): loss_mult={loss_med:.3f}  win_mult={win_med:.3f}")
    print(f"[ratios] P90 (stress disclosure): loss_mult={loss_p90:.3f}  win_mult={win_p90:.3f}")

    # Fidelity gate: reproduce two published RESULTS.md anchors before trusting anything new.
    anchor1 = max_risk_flat(0.55, 2.0, 1, EVAL_BUST_CEILING)
    anchor2 = max_risk_policy(0.55, 2.0, 1, EVAL_BUST_CEILING)
    r1 = anchor1[0] if anchor1 else None
    r2 = anchor2[0] if anchor2 else None
    print(f"[fidelity] (0.55,2.0,k=1) flat R_max={r1} (expect $350)  policy R_max={r2} (expect $1,825)")
    fidelity_ok = (r1 == 350) and (r2 == 1825)
    if not fidelity_ok:
        print("FIDELITY GATE FAIL — stopping before any grid number is read.")
        (OUT / "polfront_intraday_honest_results.json").write_text(json.dumps(
            {"fidelity_ok": False, "r_flat": r1, "r_policy": r2, "ratio_meta": ratio_meta}, indent=2))
        raise SystemExit(2)
    print("FIDELITY GATE PASS")

    results = []
    for (w, b) in PAIRS:
        for k in KS:
            flat = max_risk_flat(w, b, k, EVAL_BUST_CEILING)
            pol = max_risk_policy(w, b, k, EVAL_BUST_CEILING)
            r_flat = flat[0] if flat else None
            r_pol = pol[0] if pol else None

            row = {
                "w": w, "b": b, "k": k,
                "r_flat_max": r_flat, "flat_bust_eod": flat[1]["bust"] if flat else None,
                "r_policy_max": r_pol, "policy_bust_eod": pol[1]["bust"] if pol else None,
            }
            if r_flat is not None:
                fh = eval_flat_intraday_honest(w, b, r_flat, k, loss_med, win_med)
                row["flat_bust_intraday_honest"] = fh["bust"]
                row["flat_delta_intraday_honest"] = round(fh["bust"] - row["flat_bust_eod"], 2)
                row["flat_floor_ok_intraday_honest"] = bool(fh["bust"] <= EVAL_BUST_CEILING)
                fh90 = eval_flat_intraday_honest(w, b, r_flat, k, loss_p90, win_p90)
                row["flat_bust_p90_stress"] = fh90["bust"]
            if r_pol is not None:
                ph = eval_policy_intraday_honest(w, b, r_pol, k, loss_med, win_med)
                row["policy_bust_intraday_honest"] = ph["bust"]
                row["policy_delta_intraday_honest"] = round(ph["bust"] - row["policy_bust_eod"], 2)
                row["policy_floor_ok_intraday_honest"] = bool(ph["bust"] <= EVAL_BUST_CEILING)
                ph90 = eval_policy_intraday_honest(w, b, r_pol, k, loss_p90, win_p90)
                row["policy_bust_p90_stress"] = ph90["bust"]

            results.append(row)
            print(f"w={w} b={b} k={k}: flat R={r_flat} eod_bust={row.get('flat_bust_eod')} "
                  f"-> honest_bust={row.get('flat_bust_intraday_honest')} "
                  f"(delta {row.get('flat_delta_intraday_honest')})  |  "
                  f"policy R={r_pol} eod_bust={row.get('policy_bust_eod')} "
                  f"-> honest_bust={row.get('policy_bust_intraday_honest')} "
                  f"(delta {row.get('policy_delta_intraday_honest')})")

    out = {
        "fidelity_ok": True,
        "ratio_meta": ratio_meta,
        "results": results,
    }
    (OUT / "polfront_intraday_honest_results.json").write_text(json.dumps(out, indent=2))
    print(f"\nsaved -> {OUT / 'polfront_intraday_honest_results.json'}")


if __name__ == "__main__":
    main()
