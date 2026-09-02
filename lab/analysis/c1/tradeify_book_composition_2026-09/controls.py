"""Controls for the three-leg grid.

(A) Shuffled-Aegis control: MNQ x1 + Aegis x{2,3} where every Aegis trade is moved to a
    different Aegis trade-date drawn by permuting trade-dates WITHIN each calendar year
    (clock times kept). Drift, trade count and per-year P&L are preserved; the day-to-day
    co-movement with MNQ is destroyed. If the shuffled books match the real ones, Aegis's
    benefit is "any positive-drift filler", not diversification. 5 permutations, seeded.
(B) Aegis-only on its EXCLUDED regime, 2020-02-24 -> 2022-07-31 (the window the grid cannot
    see because MNQ/MYM start 2022), at x2/x3/x4, both tiers.
(C) Daily P&L co-movement diagnostics on the common window: pairwise correlations and the
    joint-loss-day frequency vs independence.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book_grid as bg  # noqa: E402
from mc.preflight import firm_kwargs as _firm_kwargs  # noqa: E402

N_SIMS = 1000
PERMS = (11, 22, 33, 44, 55)


def shuffle_aegis_trades(trades, seed):
    rng = np.random.default_rng(seed)
    by_year = {}
    for t in trades:
        by_year.setdefault(t["exit_date"].year, []).append(t)
    out = []
    for year, ts in by_year.items():
        dates = sorted({t["exit_date"] for t in ts})
        n = len(dates)
        # DERANGEMENT, not a plain permutation: rng.permutation leaves ~1 date mapped to
        # itself per draw (E[fixed points] = 1 for any n), which silently preserves some
        # original MNQ/Aegis alignment in a control whose whole purpose is to destroy it.
        # Rejection-sample until no fixed point remains. Fixed 2026-09-02 (Codex review,
        # PR #260). n < 2 cannot be deranged -- left as identity and reported.
        perm = list(rng.permutation(n))
        if n >= 2:
            tries = 0
            while any(perm[i] == i for i in range(n)) and tries < 10_000:
                perm = list(rng.permutation(n))
                tries += 1
            if any(perm[i] == i for i in range(n)):
                raise RuntimeError(f"no derangement found for year {year} (n={n})")
        mapping = {dates[i]: dates[perm[i]] for i in range(n)}
        for t in ts:
            nd = mapping[t["exit_date"]]
            shift = nd - t["exit_date"]
            nt = dict(t)
            nt["entry_time"] = t["entry_time"] + shift
            nt["exit_time"] = t["exit_time"] + shift
            nt["entry_date"] = t["entry_date"] + shift
            nt["exit_date"] = nd
            out.append(nt)
    out.sort(key=lambda t: t["entry_time"])
    return out


def cell(legs_trades, sizing, tier, window, tag):
    legs = list(legs_trades)
    daily = {leg: bg.daily_per_contract(tr) for leg, tr in legs_trades.items()}
    path, low, date_index, active, tb = bg.build_cell(legs, daily, legs_trades, sizing, *window)
    fkw = _firm_kwargs(tier, consistency=bg.TIERS[tier])
    boot = bg.bootstrap(path, low, fkw, active, N_SIMS, bg.SEEDS, True)
    mid = path.shape[0] // 2
    h1 = bg.bootstrap(path[:mid], low[:mid], fkw, active, N_SIMS, bg.SEEDS, True)
    h2 = bg.bootstrap(path[mid:], low[mid:], fkw, active, N_SIMS, bg.SEEDS, True)
    roll = bg.rolling_starts(path, low, fkw, True)
    return {"tag": tag, "sizing": sizing, "tier": tier, "window": list(window),
            "boot": boot, "h1": h1, "h2": h2, "rolling": roll,
            "weekly_coverage": round(bg.weekly_coverage(tb, *window), 3)}


def job(kind, sizing, tier, seed):
    mnq = bg.load_trades(os.path.join(bg.DOWNLOADS, bg.LEG_FILES["mnq"]))
    aeg = bg.load_trades(os.path.join(bg.DOWNLOADS, bg.LEG_FILES["aegis"]))
    if kind == "shuffled":
        aeg_w = bg.slice_trades(aeg, *bg.WINDOW)
        sh = shuffle_aegis_trades(aeg_w, seed)
        return cell({"mnq": mnq, "aegis": sh}, sizing, tier, bg.WINDOW, f"shuffled seed {seed}")
    if kind == "real":
        return cell({"mnq": mnq, "aegis": aeg}, sizing, tier, bg.WINDOW, "real")
    if kind == "h1_regime":
        return cell({"aegis": aeg}, sizing, tier, ("2020-02-24", "2022-07-31"), "aegis 2020-02..2022-07")
    raise ValueError(kind)


def comovement():
    tr = {leg: bg.load_trades(os.path.join(bg.DOWNLOADS, bg.LEG_FILES[leg])) for leg in ("mnq", "mym", "aegis")}
    idx = pd.bdate_range(*bg.WINDOW)
    d = pd.DataFrame({leg: bg.daily_per_contract(t).reindex(idx, fill_value=0.0) for leg, t in tr.items()})
    out = {"corr_all_days": d.corr().round(3).to_dict()}
    active = d[(d != 0).any(axis=1)]
    out["corr_active_days"] = active.corr().round(3).to_dict()
    # joint loss days vs independence, per pair
    pairs = {}
    for a, b in (("mnq", "mym"), ("mnq", "aegis"), ("mym", "aegis")):
        la, lb = (d[a] < 0), (d[b] < 0)
        both = float((la & lb).mean()); indep = float(la.mean() * lb.mean())
        pairs[f"{a}-{b}"] = {"p_both_lose": round(both, 4), "p_independent": round(indep, 4),
                             "ratio": round(both / indep, 2) if indep > 0 else None}
    out["joint_loss_days"] = pairs
    out["per_leg"] = {leg: {"trade_days": int((d[leg] != 0).sum()), "mean_pc_per_trade_day": round(float(d[leg][d[leg] != 0].mean()), 2),
                            "worst_day_pc": round(float(d[leg].min()), 2), "skew_active": round(float(d[leg][d[leg] != 0].skew()), 3)}
                      for leg in d}
    return out


def main():
    jobs = []
    for tier in bg.TIERS:
        for k in (2, 3):
            jobs.append(("real", {"mnq": 1, "aegis": k}, tier, 0))
            for s in PERMS:
                jobs.append(("shuffled", {"mnq": 1, "aegis": k}, tier, s))
        for k in (2, 3, 4):
            jobs.append(("h1_regime", {"aegis": k}, tier, 0))
    res = Parallel(n_jobs=3, verbose=5)(delayed(job)(*j) for j in jobs)
    co = comovement()
    os.makedirs(bg.DATA, exist_ok=True)
    with open(os.path.join(bg.DATA, "controls.json"), "w") as fh:
        json.dump({"results": res, "comovement": co}, fh, indent=1, default=str)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(co, indent=1))
    for r in res:
        b = r["boot"]
        print(f"{r['tier'][:16]:16} {bg.label(r['sizing']):14} {r['tag']:24} bust {b['bust_pct']:6.2f} pass {b['pass_pct']:6.2f} "
              f"unres {b['unresolved_pct']:5.2f} med {b['median_days_to_pass']}  h1 {r['h1']['bust_pct']:6.2f}  h2 {r['h2']['bust_pct']:6.2f}  "
              f"roll {r['rolling']['pass_pct']:.0f}/{r['rolling']['bust_pct']:.0f}/{r['rolling']['unresolved_pct']:.0f}")


if __name__ == "__main__":
    main()
