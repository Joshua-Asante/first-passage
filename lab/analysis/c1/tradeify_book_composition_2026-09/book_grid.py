"""Three-leg Tradeify book composition grid: ORB-MNQ recon x ORB-MYM x Aegis-6J1,
integer contracts per leg, Tradeify_Select_100K and Tradeify_Growth_100K.

Engine reuse (no barrier logic reimplemented): core/mc/simulation.py::simulate_path /
run_seed, core/mc/preflight.py::firm_kwargs / summarize_outcomes. The intraday-honest
channel is the timestamp-sequenced sweep-line from
lab/analysis/c1/aegis_orbmnq_combined_book_2026-08-26/followup_s10_bar_level_and_compounding.py
(build_intraday_low_sequenced), generalised to N legs -- a trade-level construction
from each leg's OWN TradingView adverse-excursion figures, NOT a bar-level replay.

Inputs (operator-supplied TradingView "List of Trades" exports, NOT committed):
  mnq    ORB-MNQ-1_recon_v7_..._70648.csv   qty 2 constant (base 2 + scale-in 2); v8/v8.1
                                             carry identical trades (v8 byte-identical,
                                             v8.1 differs only in Signal labels)
  mym    ORB-MYM-1_v0.4_..._74611.csv       both directions, base 3 + scale-in 3; 9 rows
                                             exit "Margin call" at qty 1 (TV capital artifact)
  mym_v03 ORB-MYM-1_v0.3_..._f7482.csv      long-only qty 2, the export MYM.md M9 measured
  aegis  Aegis_6J1_..._76620.csv            the SANCTIONED 1-tick/side panel (6J.md J12);
                                             qty 4-8 (equity compounding), single entry per
                                             trade -> per-contract normalisation is exact

Per-contract unit: every trade's Net PnL and Adverse Excursion are divided by that
trade's own quantity. For MNQ/MYM (base and add share one qty) "k contracts" then
means base k + add k, exactly what the same construct at qty=k realises.

Cap arithmetic: 6J counts 10 micro-equivalents (operator-adopted convention, combined
RESULTS §8 H1); MNQ/MYM 1 each. Eval cap 80, funded start 30.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "core"))

from mc.simulation import HORIZON_CAP, run_seed, simulate_path  # noqa: E402
from mc.preflight import firm_kwargs as _firm_kwargs, summarize_outcomes  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402

DOWNLOADS = r"C:\Users\joshu\Downloads"
DATA = os.path.join(HERE, "data")

LEG_FILES = {
    "mnq": "ORB-MNQ-1_recon_v7_CME_MINI_MNQ1!_2026-08-31_70648.csv",
    "mym": "ORB-MYM-1_v0.4_CBOT_MINI_MYM1!_2026-08-26_74611.csv",
    "mym_v03": "ORB-MYM-1_v0.3_CBOT_MINI_MYM1!_2026-08-25_f7482.csv",
    "aegis": "Aegis_6J1_CME_6J1!_2026-08-02_76620.csv",
}
MICRO_EQ = {"mnq": 1, "mym": 1, "mym_v03": 1, "aegis": 10}
TIERS = {"Tradeify_Select_100K": 0.40, "Tradeify_Growth_100K": None}  # consistency frac
SEEDS = (42, 123, 2026)
EVAL_PRICE, RESET_PRICE = 265.0, 169.0

# Common window: latest start among the three primary legs (MYM v0.4 2022-08-01) to the
# earliest end (Aegis 76620 2026-07-01). Halves split at the business-day midpoint.
WINDOW = ("2022-08-01", "2026-07-01")
ALT_WINDOW = ("2022-01-03", "2026-07-01")  # for the mym_v03 reference cells


# ---------------------------------------------------------------------------
# Raw export -> per-contract trade records
# ---------------------------------------------------------------------------

def load_trades(path: str) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    by: dict[str, dict] = {}
    for r in rows:
        by.setdefault(r["Trade number"], {})[r["Type"].split()[0]] = r
    out = []
    for tn, sides in by.items():
        e, x = sides.get("Entry"), sides.get("Exit")
        if e is None or x is None:
            raise ValueError(f"{path} trade {tn}: missing Entry or Exit row")
        qty = float(e["Size (qty)"])
        if abs(qty - float(x["Size (qty)"])) > 1e-9:
            raise ValueError(f"{path} trade {tn}: entry/exit qty mismatch")
        mae = float(x["Adverse excursion USD"])
        if mae > 0:
            raise ValueError(f"{path} trade {tn}: positive adverse excursion {mae}")
        et, xt = pd.Timestamp(e["Date and time"]), pd.Timestamp(x["Date and time"])
        out.append({
            "trade_number": tn,
            "entry_time": et, "exit_time": xt,
            "entry_date": pd.Timestamp(et.date()), "exit_date": pd.Timestamp(xt.date()),
            "qty": qty, "side": e["Type"].split()[1],
            "net_pnl_per_contract": float(x["Net PnL USD"]) / qty,
            "mae_per_contract": mae / qty,
            "signal_entry": e["Signal"], "signal_exit": x["Signal"],
        })
    out.sort(key=lambda t: t["entry_time"])
    return out


def daily_per_contract(trades: list[dict]) -> pd.Series:
    s = pd.Series({}, dtype=float)
    acc: dict = {}
    for t in trades:
        acc[t["exit_date"]] = acc.get(t["exit_date"], 0.0) + t["net_pnl_per_contract"]
    s = pd.Series(acc, dtype=float).sort_index()
    return s


def slice_trades(trades, start, end):
    start, end = pd.Timestamp(start), pd.Timestamp(end)
    return [t for t in trades if start <= t["exit_date"] <= end]


# ---------------------------------------------------------------------------
# Sweep-line intraday floor (ported from followup_s10, N legs)
# ---------------------------------------------------------------------------

def build_intraday_low_sequenced(trades_by_leg, leg_contracts, date_index):
    day_opens, day_closes, day_carries = {}, {}, {}
    for leg, trades in trades_by_leg.items():
        k = leg_contracts[leg]
        if k == 0:
            continue
        for t in trades:
            scaled = {"entry_time": t["entry_time"], "exit_time": t["exit_time"],
                      "net_pnl": t["net_pnl_per_contract"] * k, "mae": t["mae_per_contract"] * k}
            day_opens.setdefault(t["entry_date"], []).append(scaled)
            day_closes.setdefault(t["exit_date"], []).append(scaled)
            # Open at the START of every day after the entry day, INCLUDING the exit day
            # (`[1:]`, not `[1:-1]`): on its exit day a multi-day trade is already open when
            # the session begins, so its MAE is achievable before its close event books the
            # realized P&L. Slicing `[1:-1]` left the exit day's floor blind to that MAE
            # whenever MAE was worse than net P&L -- 6 of the 8 multi-day trades across these
            # three legs. Fixed 2026-09-02 (Codex review, PR #260); the same off-by-one is
            # present in the 2026-08-26 campaign's own followup_s10 this was ported from.
            for day in pd.date_range(t["entry_date"], t["exit_date"], freq="D")[1:]:
                day_carries.setdefault(day, []).append(scaled)
    all_days = set(day_opens) | set(day_closes) | set(day_carries)
    low_by_day, realized_by_day = {}, {}
    for day in all_days:
        opens, closes, carries = day_opens.get(day, []), day_closes.get(day, []), day_carries.get(day, [])
        events = [(t["entry_time"], 0, id(t), t) for t in opens] + [(t["exit_time"], 1, id(t), t) for t in closes]
        events.sort(key=lambda e: (e[0], e[1]))
        open_trades = {id(t): t for t in carries}
        realized = 0.0
        min_floor = realized + sum(o["mae"] for o in open_trades.values())
        for _tm, kind, tid, t in events:
            if kind == 0:
                open_trades[tid] = t
            else:
                realized += t["net_pnl"]
                open_trades.pop(tid, None)
            min_floor = min(min_floor, realized + sum(o["mae"] for o in open_trades.values()))
        low_by_day[day] = min_floor
        realized_by_day[day] = sum(t["net_pnl"] for t in closes)
    n = len(date_index)
    low = np.zeros(n); realized = np.zeros(n)
    for i, day in enumerate(date_index):
        if day in low_by_day:
            low[i] = low_by_day[day]; realized[i] = realized_by_day[day]
    return np.minimum(low, 0.0), realized


# ---------------------------------------------------------------------------
# Cell construction and scoring
# ---------------------------------------------------------------------------

def build_cell(legs, daily, trades, sizing: dict, start, end):
    date_index = pd.bdate_range(start=start, end=end)
    active = [leg for leg in legs if sizing.get(leg, 0) > 0]
    path = np.zeros((len(date_index), len(active)))
    for j, leg in enumerate(active):
        path[:, j] = daily[leg].reindex(date_index, fill_value=0.0).to_numpy(dtype=float) * sizing[leg]
    tb = {leg: slice_trades(trades[leg], start, end) for leg in active}
    low, realized = build_intraday_low_sequenced(tb, sizing, date_index)
    worst = float(np.abs(realized - path.sum(axis=1)).max())
    if worst > 0.05:
        raise AssertionError(f"reconstruction mismatch ${worst:.4f} for {sizing}")
    return path, low, date_index, active, tb


def weekly_coverage(trades_by_leg, start, end) -> float:
    weeks = pd.period_range(pd.Timestamp(start), pd.Timestamp(end), freq="W-FRI")
    covered = set()
    for trades in trades_by_leg.values():
        for t in trades:
            covered.add(t["exit_date"].to_period("W-FRI"))
    return len(covered & set(weeks)) / max(len(weeks), 1)


def bootstrap(path, low, fkw, strats, n_sims, seeds, use_intraday: bool):
    n_days, n_legs = path.shape
    n_weeks = n_days // 5
    usable = n_weeks * 5
    blocks = path[:usable].reshape(n_weeks, 5, n_legs)
    ib = low[:usable].reshape(n_weeks, 5, 1) if use_intraday else None
    res = [run_seed(s, n_sims, blocks, 1.0, 1.0, horizon=HORIZON_CAP, strats=tuple(strats),
                    firm_kwargs=fkw, intraday_blocks=ib) for s in seeds]
    summ = summarize_outcomes(res, n_sims)
    days = [d for r in res for d in r["days_to_pass"]]
    n_paths = n_sims * len(seeds)
    bust, pas = summ["headline_bust"], summ["pass_rate"]
    attr = {}
    for r in res:
        for k, v in r["bust_attribution"].items():
            attr[k] = attr.get(k, 0) + v
    return {
        "bust_pct": round(bust * 100, 3), "pass_pct": round(pas * 100, 3),
        "unresolved_pct": round(summ["rates"]["horizon_cap"] * 100, 3),
        "inactivity_pct": round(summ["rates"]["bust_inactivity"] * 100, 3),
        "median_days_to_pass": (float(np.median(days)) if days else None),
        "p75_days_to_pass": (float(np.percentile(days, 75)) if days else None),
        "se_bust_pp": round(100 * math.sqrt(max(bust * (1 - bust), 1e-12) / n_paths), 3),
        "se_pass_pp": round(100 * math.sqrt(max(pas * (1 - pas), 1e-12) / n_paths), 3),
        "n_paths": n_paths, "n_weeks": int(n_weeks),
        "bust_attribution": attr,
    }


def rolling_starts(path, low, fkw, use_intraday: bool):
    n = path.shape[0]
    outcomes = {"pass": 0, "bust": 0, "unresolved": 0}
    days = []
    for s in range(n):
        sub = path[s:]
        kw = dict(fkw)
        if use_intraday:
            kw["intraday_low"] = low[s:]
        o, d, _mdd, _c = simulate_path(sub, 1.0, 1.0, n - s, **kw)
        if o == "pass":
            outcomes["pass"] += 1; days.append(d)
        elif o.startswith("bust"):
            outcomes["bust"] += 1
        else:
            outcomes["unresolved"] += 1
    tot = n
    return {
        "pass_pct": round(100 * outcomes["pass"] / tot, 2),
        "bust_pct": round(100 * outcomes["bust"] / tot, 2),
        "unresolved_pct": round(100 * outcomes["unresolved"] / tot, 2),
        "median_days_to_pass": (float(np.median(days)) if days else None),
        "n_starts": tot,
    }


def realized_single(path, low, fkw, use_intraday):
    kw = dict(fkw)
    if use_intraday:
        kw["intraday_low"] = low
    o, d, mdd, _ = simulate_path(path, 1.0, 1.0, path.shape[0], **kw)
    return {"outcome": o, "day": int(d), "max_dd_pct": round(mdd * 100, 3)}


def fee_metrics(pass_pct, bust_pct):
    resolved = pass_pct + bust_pct
    if resolved <= 0:
        return None
    p = pass_pct / resolved
    if p <= 0:
        return {"p_pass_resolved": 0.0, "expected_fee_to_first_pass": None}
    return {"p_pass_resolved": round(p, 4),
            "expected_fee_to_first_pass": round(EVAL_PRICE + RESET_PRICE * (1 - p) / p, 0),
            "p_at_least_one_pass_in_2": round(1 - (1 - p) ** 2, 4)}


def score_cell(args):
    """Worker entry: one (sizing, tier) cell. Re-imports the engine in the worker;
    attests the geometry it actually used."""
    sizing, tier, n_sims, window, stage, legs_in = args
    legs = list(legs_in)
    trades = {leg: load_trades(os.path.join(DOWNLOADS, LEG_FILES[leg])) for leg in legs if sizing.get(leg, 0) > 0}
    daily = {leg: daily_per_contract(trades[leg]) for leg in trades}
    start, end = window
    path, low, date_index, active, tb = build_cell(legs, daily, trades, sizing, start, end)
    fkw = _firm_kwargs(tier, consistency=TIERS[tier])
    out = {
        "sizing": sizing, "tier": tier, "window": list(window), "active_legs": active,
        "n_days": int(path.shape[0]),
        "geometry_attest": {"dd_lock_offset_usd": fkw.get("dd_lock_offset_usd"),
                             "trailing_dd_pct": fkw.get("trailing_dd_pct"),
                             "consistency_frac": fkw.get("consistency_frac")},
        "micro_eq": int(sum(MICRO_EQ[l] * sizing[l] for l in active)),
        "weekly_coverage": round(weekly_coverage(tb, start, end), 4),
        "realized_full": {"eod": realized_single(path, low, fkw, False),
                          "intraday": realized_single(path, low, fkw, True)},
        "rolling": {"eod": rolling_starts(path, low, fkw, False),
                    "intraday": rolling_starts(path, low, fkw, True)},
        "boot_intraday": bootstrap(path, low, fkw, active, n_sims, SEEDS, True),
    }
    if stage == "final":
        out["boot_eod"] = bootstrap(path, low, fkw, active, n_sims, SEEDS, False)
    # both halves (intraday), same seeds, same n_sims for screen; finals use n_sims too
    mid_i = path.shape[0] // 2
    mid = date_index[mid_i]
    out["halves"] = {"split_date": str(mid.date())}
    for name, (a, b) in (("h1", (0, mid_i)), ("h2", (mid_i, path.shape[0]))):
        sub_path, sub_low = path[a:b], low[a:b]
        out["halves"][name] = bootstrap(sub_path, sub_low, fkw, active, n_sims, SEEDS, True)
    out["fee"] = fee_metrics(out["boot_intraday"]["pass_pct"], out["boot_intraday"]["bust_pct"])
    return out


def sizing_grid(k_mnq, k_mym, k_aegis, mym_key="mym"):
    cells = []
    for a, b, c in itertools.product(k_mnq, k_mym, k_aegis):
        if a == 0 and b == 0 and c == 0:
            continue
        cells.append({"mnq": a, mym_key: b, "aegis": c})
    return cells


def label(sizing):
    return "+".join(f"{k}x{v}" for k, v in sizing.items() if v > 0)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("smoke", "screen", "final", "alt"), default="screen")
    ap.add_argument("--n-sims", type=int, default=None)
    ap.add_argument("--jobs", type=int, default=7)
    ap.add_argument("--finalists", type=str, default=None, help="JSON list of sizing dicts for --stage final")
    a = ap.parse_args(argv)
    os.makedirs(DATA, exist_ok=True)

    if a.stage == "smoke":
        t0 = time.time()
        r = score_cell(({"mnq": 1, "mym": 1, "aegis": 0}, "Tradeify_Growth_100K", a.n_sims or 200, WINDOW, "screen", ("mnq", "mym", "aegis")))
        print(json.dumps(r, indent=1, default=str)[:3000])
        print(f"elapsed {time.time() - t0:.1f}s")
        return

    from joblib import Parallel, delayed

    if a.stage == "screen":
        n_sims = a.n_sims or 1000
        cells = sizing_grid((0, 1, 2), (0, 1, 2), (0, 1, 2, 3, 4))
        jobs = [(s, tier, n_sims, WINDOW, "screen", ("mnq", "mym", "aegis")) for s in cells for tier in TIERS]
        out_path = os.path.join(DATA, "grid_screen.json")
    elif a.stage == "alt":
        n_sims = a.n_sims or 1000
        cells = [{"mnq": 0, "mym_v03": 1, "aegis": 0}, {"mnq": 1, "mym_v03": 1, "aegis": 0},
                 {"mnq": 1, "mym_v03": 1, "aegis": 2}, {"mnq": 0, "mym_v03": 2, "aegis": 0},
                 {"mnq": 1, "mym_v03": 0, "aegis": 0}]
        jobs = [(s, tier, n_sims, ALT_WINDOW, "screen", ("mnq", "mym_v03", "aegis")) for s in cells for tier in TIERS]
        out_path = os.path.join(DATA, "grid_alt_mym_v03.json")
    else:
        n_sims = a.n_sims or 10_000
        cells = json.loads(a.finalists)
        legs = ("mnq", "mym_v03", "aegis") if any("mym_v03" in c for c in cells) else ("mnq", "mym", "aegis")
        win = ALT_WINDOW if "mym_v03" in legs else WINDOW
        jobs = [(s, tier, n_sims, win, "final", legs) for s in cells for tier in TIERS]
        out_path = os.path.join(DATA, "grid_final.json")

    t0 = time.time()
    print(f"{a.stage}: {len(jobs)} cells, n_sims={n_sims} x {len(SEEDS)} seeds, jobs={a.jobs}", flush=True)
    results = Parallel(n_jobs=a.jobs, verbose=5)(delayed(score_cell)(j) for j in jobs)
    with open(out_path, "w") as fh:
        json.dump({"stage": a.stage, "n_sims": n_sims, "seeds": SEEDS, "elapsed_s": round(time.time() - t0, 1),
                   "results": results}, fh, indent=1, default=str)
    print(f"wrote {out_path} in {time.time() - t0:.0f}s")
    for r in sorted(results, key=lambda r: (r["tier"], -r["boot_intraday"]["pass_pct"])):
        b = r["boot_intraday"]
        print(f"{r['tier'][:16]:16} {label(r['sizing']):22} bust {b['bust_pct']:6.2f}  pass {b['pass_pct']:6.2f}  "
              f"unres {b['unresolved_pct']:5.2f}  med {b['median_days_to_pass']}  "
              f"h1 {r['halves']['h1']['bust_pct']:6.2f}/{r['halves']['h1']['pass_pct']:6.2f}  "
              f"h2 {r['halves']['h2']['bust_pct']:6.2f}/{r['halves']['h2']['pass_pct']:6.2f}  cov {r['weekly_coverage']:.2f}")


if __name__ == "__main__":
    main()
