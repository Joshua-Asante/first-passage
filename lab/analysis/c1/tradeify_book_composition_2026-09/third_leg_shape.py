"""What shape must a third leg have to fit MNQ x1 + Aegis x2?

Stage `characterize`: what kills / slows the base book (per-leg daily P&L, worst k-day sums,
realized drawdown episodes, MNQ losing-day distribution, bust attribution).

Stage `sweep`: add a SYNTHETIC third leg with controlled shape to the real base book on the
real date index and re-score through the same engine chain (run_seed block bootstrap,
sweep-line intraday floor). Axes, all crossed:
  edge_r   expectancy per trade in R (loss = 1R)             {0.00, 0.15, 0.30}
  wr       win rate; mean win W = (edge + 1 - wr)/wr in R    {0.35, 0.55, 0.75}
  risk     dollars per 1R (the stop)                          {100, 200, 350}
  cadence  trades per week (1/day on fixed weekdays)          {2, 5}
  rho      Gaussian-copula coupling of the leg's outcome to MNQ's same-day P&L rank
           (rho<0: leg tends to win when MNQ loses)           {-0.3, 0.0, +0.3}
Winners give back Uniform(0.2, 0.6)R intraday before closing; losers touch the stop
(MAE = -1R) -- the shape-map generator's conventions (shape_feasibility_map_2026-08). Each
synthetic trade is entered 10:00 ET and closed 15:00 ET so the N-leg sweep-line can sequence
it against MNQ's and Aegis's real timestamps. Two panel realisations per cell, averaged.
The base book is re-scored at the same N and seeds so deltas are apples to apples.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book_grid as bg  # noqa: E402
from mc.preflight import firm_kwargs as _firm_kwargs  # noqa: E402

BASE = {"mnq": 1, "aegis": 2}
N_SIMS = 1000
REALISATIONS = (7, 8)
CADENCE_DAYS = {1: (0,), 2: (0, 2), 3: (0, 2, 4), 5: (0, 1, 2, 3, 4)}


def load_base():
    tr = {leg: bg.load_trades(os.path.join(bg.DOWNLOADS, bg.LEG_FILES[leg])) for leg in BASE}
    return tr


def synth_leg(edge_r, wr, risk, cadence, rho, mnq_daily, date_index, seed):
    rng = np.random.default_rng(seed)
    W = (edge_r + 1.0 - wr) / wr
    # MNQ daily P&L -> normal scores on MNQ trade days, 0 elsewhere
    m = mnq_daily.reindex(date_index, fill_value=0.0).to_numpy()
    z_m = np.zeros(len(m))
    act = m != 0
    if act.sum() > 2:
        r = rankdata(m[act]) / (act.sum() + 1.0)
        z_m[act] = norm.ppf(r)
    # Pass 1: a coupled score per trade day. Pass 2: EXACT win count by rank -- the top
    # round(wr * n) scores win, so the realized win fraction (and therefore the realized
    # edge, since W is fixed) equals the target up to rounding, and rho>0 still means the
    # leg tends to win when MNQ wins (positive realized correlation). Only the ORDER of
    # wins/losses varies across realisations, which is the thing that drives clusters.
    # (The first 2026-09-01 sweep, data/third_leg_sweep.json, drew per-trade Bernoulli
    # outcomes with an inverted copula sign and two shared seeds; its realized edge
    # wandered up to +/-0.15R from target per seed, coherently across whole win-rate rows.
    # Read that file's realized_edge_r / realized_corr_mnq columns, not its labels.)
    days = [(i, day) for i, day in enumerate(date_index) if day.weekday() in CADENCE_DAYS[cadence]]
    scores = np.empty(len(days))
    for j, (i, _day) in enumerate(days):
        eps = rng.standard_normal()
        scores[j] = rho * z_m[i] + math.sqrt(1 - rho * rho) * eps if act[i] else eps
    n_win = int(round(wr * len(days)))
    win_idx = set(np.argsort(-scores)[:n_win].tolist())
    trades = []
    for j, (i, day) in enumerate(days):
        if j in win_idx:
            pnl = risk * W
            mae = -risk * rng.uniform(0.2, 0.6)
        else:
            pnl = -risk
            mae = -risk
        et = pd.Timestamp(day.date()) + pd.Timedelta(hours=10)
        xt = pd.Timestamp(day.date()) + pd.Timedelta(hours=15)
        trades.append({"trade_number": str(i), "entry_time": et, "exit_time": xt,
                       "entry_date": pd.Timestamp(day.date()), "exit_date": pd.Timestamp(day.date()),
                       "qty": 1.0, "side": "synth", "net_pnl_per_contract": float(pnl),
                       "mae_per_contract": float(mae), "signal_entry": "synth", "signal_exit": "synth"})
    return trades, W


def score(trades_by_leg, sizing, tier, window, n_sims):
    legs = list(trades_by_leg)
    daily = {leg: bg.daily_per_contract(tr) for leg, tr in trades_by_leg.items()}
    path, low, date_index, active, tb = bg.build_cell(legs, daily, trades_by_leg, sizing, *window)
    fkw = _firm_kwargs(tier, consistency=bg.TIERS[tier])
    return bg.bootstrap(path, low, fkw, active, n_sims, bg.SEEDS, True), path, low, date_index, active


def sweep_cell(params, tier, seed, window):
    edge_r, wr, risk, cadence, rho = params
    tr = load_base()
    date_index = pd.bdate_range(*window)
    mnq_daily = bg.daily_per_contract(tr["mnq"])
    synth, W = synth_leg(edge_r, wr, risk, cadence, rho, mnq_daily, date_index, seed)
    tb = {"mnq": tr["mnq"], "aegis": tr["aegis"], "synth": synth}
    boot, path, low, di, active = score(tb, {**BASE, "synth": 1}, tier, window, N_SIMS)
    s = path[:, active.index("synth")]; m = path[:, active.index("mnq")]
    both = (s != 0) & (m != 0)
    corr = float(np.corrcoef(s[both], m[both])[0, 1]) if both.sum() > 10 else None
    realized_edge = float(np.mean([t["net_pnl_per_contract"] for t in synth])) / risk
    return {"params": {"edge_r": edge_r, "wr": wr, "W": round(W, 3), "risk": risk, "cadence": cadence, "rho": rho},
            "tier": tier, "seed": seed, "boot": boot, "realized_corr_mnq": corr,
            "realized_edge_r": round(realized_edge, 3), "n_trades": len(synth),
            "annual_drift_usd": round(float(sum(t["net_pnl_per_contract"] for t in synth)) / (len(date_index) / 252), 0)}


def base_cell(tier, window):
    tr = load_base()
    boot, path, low, di, active = score(tr, BASE, tier, window, N_SIMS)
    return {"tier": tier, "boot": boot}


def characterize(window):
    tr = load_base()
    di = pd.bdate_range(*window)
    daily = {leg: bg.daily_per_contract(tr[leg]).reindex(di, fill_value=0.0) * BASE[leg] for leg in BASE}
    comb = sum(daily.values())
    out = {"window": list(window), "n_days": len(di)}
    for name, s in (("mnq_x1", daily["mnq"]), ("aegis_x2", daily["aegis"]), ("book", comb)):
        a = s[s != 0]
        eq = s.cumsum()
        dd = eq - eq.cummax()
        # drawdown episodes
        in_dd = dd < 0
        episodes = []
        start = None
        for i, flag in enumerate(in_dd.to_numpy()):
            if flag and start is None:
                start = i
            if not flag and start is not None:
                episodes.append((start, i)); start = None
        if start is not None:
            episodes.append((start, len(di)))
        ep = sorted(((float(dd.iloc[a0:a1].min()), a1 - a0, str(di[a0].date())) for a0, a1 in episodes), key=lambda e: e[0])[:5]
        out[name] = {
            "trade_days": int((s != 0).sum()), "total_usd": round(float(s.sum()), 0),
            "per_year_usd": round(float(s.sum()) / (len(di) / 252), 0),
            "mean_active_day": round(float(a.mean()), 1), "sd_active_day": round(float(a.std()), 1),
            "worst_day": round(float(s.min()), 0), "best_day": round(float(s.max()), 0),
            "p_loss_day_given_active": round(float((a < 0).mean()), 3),
            "mean_loss_day": round(float(a[a < 0].mean()), 1), "mean_win_day": round(float(a[a > 0].mean()), 1),
            "worst_5d_sum": round(float(s.rolling(5).sum().min()), 0), "worst_10d_sum": round(float(s.rolling(10).sum().min()), 0),
            "worst_20d_sum": round(float(s.rolling(20).sum().min()), 0), "worst_60d_sum": round(float(s.rolling(60).sum().min()), 0),
            "max_dd_realized": round(float(dd.min()), 0),
            "worst_dd_episodes (depth, bdays, start)": ep,
            "skew_active": round(float(a.skew()), 2),
        }
    # what fraction of the book's worst 20-day windows is MNQ
    w = comb.rolling(20).sum(); i = int(np.nanargmin(w.to_numpy()))
    out["worst_20d_window"] = {"end": str(di[i].date()), "book": round(float(w.iloc[i]), 0),
                               "mnq": round(float(daily["mnq"].iloc[i - 19:i + 1].sum()), 0),
                               "aegis": round(float(daily["aegis"].iloc[i - 19:i + 1].sum()), 0)}
    # Growth: bust attribution and time-to-pass from grid_final
    try:
        fin = json.load(open(os.path.join(bg.DATA, "grid_final.json")))
        for r in fin["results"]:
            if r["sizing"] == {"mnq": 1, "mym": 0, "aegis": 2}:
                out[f"final_{r['tier']}"] = {"bust_attribution": r["boot_intraday"]["bust_attribution"],
                                             "median_days": r["boot_intraday"]["median_days_to_pass"],
                                             "p75_days": r["boot_intraday"]["p75_days_to_pass"],
                                             "bust": r["boot_intraday"]["bust_pct"], "pass": r["boot_intraday"]["pass_pct"]}
    except FileNotFoundError:
        pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("characterize", "sweep", "spot", "minimum"), default="characterize")
    ap.add_argument("--jobs", type=int, default=7)
    ap.add_argument("--tiers", default="Tradeify_Growth_100K")
    ap.add_argument("--spot", default=None, help="JSON list of params dicts for --stage spot")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    window = bg.WINDOW
    if a.stage == "characterize":
        c = characterize(window)
        print(json.dumps(c, indent=1, default=str))
        json.dump(c, open(os.path.join(bg.DATA, "base_characterization.json"), "w"), indent=1, default=str)
        return
    from joblib import Parallel, delayed
    tiers = a.tiers.split(",")
    global REALISATIONS
    if a.stage == "sweep":
        grid = list(itertools.product((0.0, 0.15, 0.30), (0.35, 0.55, 0.75), (100, 200, 350), (2, 5), (-0.3, 0.0, 0.3)))
        jobs = [(p, t, s) for p in grid for t in tiers for s in REALISATIONS]
        out_name = "third_leg_sweep.json"
    elif a.stage == "minimum":
        # exact-edge generator; the floor-finding grid + correlation checks at the frontier
        REALISATIONS = (7, 8, 9, 10, 11)
        grid = list(itertools.product((0.0, 0.05, 0.10, 0.15, 0.20), (0.35, 0.45, 0.55, 0.65, 0.75), (100, 200), (5,), (0.0,)))
        grid += list(itertools.product((0.10, 0.15), (0.45, 0.55, 0.75), (100, 200), (5,), (-0.3, 0.3)))
        grid += list(itertools.product((0.10, 0.15), (0.55, 0.75), (100, 200), (2,), (0.0,)))
        jobs = [(p, t, s) for p in grid for t in tiers for s in REALISATIONS]
        out_name = "third_leg_minimum.json"
    else:
        grid = [tuple(d[k] for k in ("edge_r", "wr", "risk", "cadence", "rho")) for d in json.loads(a.spot)]
        jobs = [(p, t, s) for p in grid for t in tiers for s in REALISATIONS]
        out_name = "third_leg_spot.json"
    print(f"{a.stage}: {len(jobs)} runs at {N_SIMS}x{len(bg.SEEDS)} paths", flush=True)
    base = {t: base_cell(t, window) for t in tiers}
    res = Parallel(n_jobs=a.jobs, verbose=5)(delayed(sweep_cell)(p, t, s, window) for p, t, s in jobs)
    json.dump({"base": base, "results": res, "n_sims": N_SIMS, "seeds": bg.SEEDS, "realisations": REALISATIONS},
              open(os.path.join(bg.DATA, out_name), "w"), indent=1, default=str)
    print("wrote", out_name)


if __name__ == "__main__":
    main()
