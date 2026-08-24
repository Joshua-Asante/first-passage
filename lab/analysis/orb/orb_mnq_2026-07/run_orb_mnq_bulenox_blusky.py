#!/usr/bin/env python3
"""ORB-MNQ-1 payability at Bulenox_100K / BluSky_Premium_100K / MFFU_Rapid_100K — intraday-honest
re-score (MFFU added 2026-08-24 on operator GO, same methodology, no special-casing needed --
MFFU's dd_lock_offset_usd already ships unreachable in FIRM_RULES, unlike Tradeify's pre-2026-08-04
shipped value).

Operator GO (2026-08-24): "GO on ORB-MNQ-1 at Bulenox/BluSky". Reuses the T2 intraday-honest
derivation (docs/adr/2026-08-03-orb-mnq-repark-payability-falsified.md, R2 -- construct
unfalsified elsewhere) and the R1 generalization pattern
(lab/analysis/c1/firm_model_repair_r1_7tier_2026-08-23/run_r1_bulenox_blusky_intraday.py) --
which showed the same intraday-honest engine is firm-agnostic via
discovery.prop_survivor_scoring.run_tier_remc(firm_key=...).

What this reuses verbatim (not re-derived): orb_lib.orb_backtest as the arbiter,
core.mc.simulation.simulate_path via run_tier_remc, discovery.prop_survivor_scoring's
paired_blocks_from_daily / run_tier_remc / score_part_a / _consistency_frac / load_scoring_
thresholds -- the SAME frozen gate (bust <=3.0% AND pass>=50%) T2/R1 both scored against.

What this adds: the per-day (pnl, intraday_low) excursion derivation
(orb_days_with_excursion + its two engine-matching controls) copied from
lab/analysis/orb/orb_mnq_2026-07/run_t2_intraday_bust.py (retrieved via
`git show pre-prune-2026-08-08:...` -- pruned from the working tree, not deleted from history),
re-costed per target firm (Bulenox $0.61/side, BluSky $0.95/side -- own round-trip cost, not
Tradeify's $0.91/side) rather than hand-rolled.

Cost: $0. No pull. Panel already cached (_mnq_15m.pkl, primary checkout).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parents[3]
ORB_LIB_DIR = ROOT / "lab" / "analysis" / "orb" / "orb_universe_2026-06-22"
for _p in (ROOT / "core", ROOT / "lab", ORB_LIB_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import orb_lib as ol  # noqa: E402
from firm_rules import FIRM_RULES  # noqa: E402
from mc.preflight import assert_engine_ready  # noqa: E402
from discovery.prop_survivor_scoring import (  # noqa: E402
    _consistency_frac,
    assert_intraday_channel_nonvacuous,
    load_scoring_thresholds,
    paired_blocks_from_daily,
    run_tier_remc,
    score_part_a,
)

# ---------------------------------------------------------------- data location
_PRIMARY = Path(r"C:/Users/joshu/multi_firm_operations")
PANEL_CANDIDATES = (
    ROOT / "lab" / "analysis" / "orb" / "orb_mnq_2026-07" / "_mnq_15m.pkl",
    _PRIMARY / "lab" / "analysis" / "orb" / "orb_mnq_2026-07" / "_mnq_15m.pkl",
)

ET = "America/New_York"
MNQ_USD_PER_PT = 2.0
SLIP_TICK_USD = 0.50
CLOSE_TOD_CORRECT = 15 * 60 + 45

TARGET_FIRMS = ("Bulenox_100K", "BluSky_Premium_100K", "MFFU_Rapid_100K")
K_GRID = (1, 2, 3)
NONVAC_HORIZON = 400
NONVAC_SIMS = 200


def resolve_panel() -> Path:
    for p in PANEL_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError(
        "cached MNQ 15m panel not found; looked in:\n  " + "\n  ".join(str(p) for p in PANEL_CANDIDATES)
    )


def rt_cost_pt_for(firm_key: str) -> float:
    side = float(FIRM_RULES[firm_key]["cost_per_side_usd"])
    return 2.0 * (side + SLIP_TICK_USD) / MNQ_USD_PER_PT


def make_inst(firm_key: str) -> "ol.Instrument":
    rt = rt_cost_pt_for(firm_key)
    return ol.Instrument(
        name=f"mnq_{firm_key.lower()}_correct_clock",
        path=Path("(in-memory)"),
        loader="none",
        feed="databento",
        tick=0.25,
        spread_pt=0.25,
        rt_cost_pt=rt,
        open_tod=ol.OPEN_TOD_US,
        close_tod=CLOSE_TOD_CORRECT,
        tz=ET,
        note=f"native MNQ.v.0 15m; close_tod=15:45; {firm_key} ${FIRM_RULES[firm_key]['cost_per_side_usd']:.2f}/side + 1 tick slip",
    )


# --------------------------------------------------------- derivation (verbatim from T2,
# retrieved pre-prune, re-costed per firm via inst.rt_cost_pt -- no logic changed)
def orb_days_with_excursion(piv, meta, inst: "ol.Instrument", *, or_bars: int = 2, entry_bar: str = "include") -> pd.DataFrame:
    if entry_bar not in ("include", "exclude"):
        raise ValueError(f"entry_bar must be 'include' or 'exclude', got {entry_bar!r}")

    o, h, l, c = piv["open"], piv["high"], piv["low"], piv["close"]
    tods = sorted([t for t in c.columns if inst.open_tod <= t <= inst.close_tod])
    or_tods, rest_tods = tods[:or_bars], tods[or_bars:]
    rth_close = meta["rth_close"]
    rt = inst.rt_cost_pt

    rows = []
    for day in c.index:
        or_hi = h.loc[day, or_tods].max()
        or_lo = l.loc[day, or_tods].min()
        if not np.isfinite(or_hi) or not np.isfinite(or_lo):
            continue
        rng = or_hi - or_lo
        if rng <= 0:
            continue

        side = None
        entry_t = None
        for t in rest_tods:
            bh, bl, bo = h.loc[day, t], l.loc[day, t], o.loc[day, t]
            if not np.isfinite(bh):
                continue
            up, dn = bh >= or_hi, bl <= or_lo
            if up and dn:
                side = "long" if bo <= (or_hi + or_lo) / 2 else "short"
                entry_t = t
                break
            if up:
                side, entry_t = "long", t
                break
            if dn:
                side, entry_t = "short", t
                break
        if side is None:
            continue

        entry = or_hi if side == "long" else or_lo
        cl = rth_close.loc[day]
        if side == "long":
            stopped = bool(l.loc[day, rest_tods].min() <= or_lo)
            exit_px = or_lo if stopped else cl
            pnl_pt = exit_px - entry
        else:
            stopped = bool(h.loc[day, rest_tods].max() >= or_hi)
            exit_px = or_hi if stopped else cl
            pnl_pt = entry - exit_px

        if stopped:
            worst_pt = pnl_pt
        else:
            if entry_bar == "include":
                held = [t for t in rest_tods if t >= entry_t]
            else:
                held = [t for t in rest_tods if t > entry_t]
            extreme = (l.loc[day, held].min() if side == "long" else h.loc[day, held].max()) if held else np.nan
            if np.isfinite(extreme):
                worst_pt = float(extreme) - entry if side == "long" else entry - float(extreme)
                worst_pt = min(worst_pt, pnl_pt)
            else:
                worst_pt = pnl_pt

        rows.append(
            {
                "date": pd.Timestamp(day),
                "R": (pnl_pt - rt) / rng,
                "range_pt": rng,
                "side": side,
                "stopped": stopped,
                "entry_tod": entry_t,
                "pnl_usd_1lot": (pnl_pt - rt) * MNQ_USD_PER_PT,
                "low_usd_1lot": min(0.0, worst_pt - rt) * MNQ_USD_PER_PT,
            }
        )

    out = pd.DataFrame(rows)
    out["year"] = out["date"].dt.year
    return out


def assert_mirror_matches_engine(recon: pd.DataFrame, bt: dict) -> None:
    n_r, n_e = len(recon), len(bt["R"])
    assert n_r == n_e, f"mirror n={n_r} != engine n={n_e}"
    assert np.allclose(recon["R"].to_numpy(), np.asarray(bt["R"], float)), "R diverges"
    assert np.allclose(recon["range_pt"].to_numpy(), np.asarray(bt["range"], float)), "range diverges"
    assert (recon["side"].to_numpy() == np.asarray(bt["side"])).all(), "side diverges"
    assert (recon["stopped"].to_numpy() == np.asarray(bt["stopped"], bool)).all(), "stopped diverges"
    assert (recon["entry_tod"].to_numpy() == np.asarray(bt["entry_tod"])).all(), "entry_tod diverges"


def assert_excursion_invariants(recon: pd.DataFrame, rt_pt: float) -> dict:
    low = recon["low_usd_1lot"].to_numpy()
    pnl = recon["pnl_usd_1lot"].to_numpy()
    stopped = recon["stopped"].to_numpy()

    assert (low <= 0.0).all(), "intraday_low must be <= 0"
    assert (low <= pnl + 1e-9).all(), "intraday_low must dominate realized P&L"
    assert np.allclose(low[stopped], pnl[stopped]), "stopped days must have low == pnl"
    floor = -(recon["range_pt"].to_numpy() + rt_pt) * MNQ_USD_PER_PT
    assert (low >= floor - 1e-6).all(), "excursion breached the structural stop floor"

    held = ~stopped
    gap = pnl[held] - low[held]
    return {
        "n_days": int(len(recon)),
        "n_stopped": int(stopped.sum()),
        "n_held_to_close": int(held.sum()),
        "worst_realized_day_usd_1lot": float(pnl.min()),
        "worst_intraday_day_usd_1lot": float(low.min()),
    }


def daily_series(recon: pd.DataFrame, k: int) -> tuple[np.ndarray, np.ndarray]:
    """Full bdate_range daily pnl/low series scaled by k, non-trade days flat.

    Same reindex(bdays).fillna(0.0) convention T2/Q-COMPOSE-1 use.
    """
    idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    pnl = recon.set_index("date")["pnl_usd_1lot"].groupby(level=0).sum().reindex(idx).fillna(0.0)
    low = recon.set_index("date")["low_usd_1lot"].groupby(level=0).sum().reindex(idx).fillna(0.0)
    return pnl.to_numpy() * k, low.to_numpy() * k


def main() -> int:
    smoke_sims = int(sys.argv[1]) if len(sys.argv) > 1 else None
    thr = load_scoring_thresholds()
    print("=" * 100)
    print("ORB-MNQ-1 payability -- Bulenox_100K / BluSky_Premium_100K, intraday-honest")
    print("=" * 100)
    print(
        f"[gate ] bust<={thr.eval_bust_ceiling:.1%} AND pass>={thr.pass_floor:.0%} | "
        f"horizon {thr.horizon} | seeds {thr.seeds} | {thr.sims_per_seed:,} sims/seed"
    )

    panel_pkl = resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data ] {panel_pkl}")
    print(f"[data ] rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    report: dict = {"date": "2026-08-24", "gate": {"bust_ceiling": thr.eval_bust_ceiling, "pass_floor": thr.pass_floor}, "firms": {}}

    for firm_key in TARGET_FIRMS:
        t_firm0 = time.time()
        rt = rt_cost_pt_for(firm_key)
        side = FIRM_RULES[firm_key]["cost_per_side_usd"]
        cons = _consistency_frac(firm_key)
        print(f"\n{'=' * 100}\n[firm ] {firm_key}  cost_per_side=${side:.2f}  rt_cost_pt={rt:.3f}  consistency_frac={cons}")
        assert_engine_ready(firm_key)

        inst = make_inst(firm_key)
        piv, meta = ol.session_panel(df, inst)
        bt = ol.orb_backtest(piv, meta, inst, or_bars=2)
        recon = orb_days_with_excursion(piv, meta, inst, entry_bar="include")

        assert_mirror_matches_engine(recon, bt)
        print(f"[ctrl ] mirror-vs-engine PASS n={len(recon)}")
        inv = assert_excursion_invariants(recon, rt)
        print(
            f"[ctrl ] invariants PASS -- n_days={inv['n_days']} stopped={inv['n_stopped']} "
            f"held={inv['n_held_to_close']} worst_realized=${inv['worst_realized_day_usd_1lot']:,.2f} "
            f"worst_intraday=${inv['worst_intraday_day_usd_1lot']:,.2f}"
        )

        firm_report: dict = {
            "cost_per_side_usd": side,
            "rt_cost_pt": rt,
            "consistency_frac": cons,
            "derivation": inv,
            "k": {},
        }

        # non-vacuity guard at k=1 (short horizon)
        pnl1, low1 = daily_series(recon, 1)
        thr_nv = thr
        blocks_p_nv, blocks_l_nv = paired_blocks_from_daily(pnl1, low1)
        nv = assert_intraday_channel_nonvacuous(
            blocks_p_nv, blocks_l_nv, thresholds=thr_nv, firm_key=firm_key, n_sims=NONVAC_SIMS, horizon=NONVAC_HORIZON
        )
        print(
            f"[ctrl ] non-vacuity OK -- eod bust={nv['eod']['headline_bust']:.4f} "
            f"real(intraday) bust={nv['real']['headline_bust']:.4f}"
        )
        firm_report["nonvacuity"] = {
            "eod_bust": float(nv["eod"]["headline_bust"]),
            "real_bust": float(nv["real"]["headline_bust"]),
        }

        print(f"{'k':>2} {'bust':>9} {'pass':>9} {'medDays':>9} {'PartA':>7}")
        for k in K_GRID:
            pnl_k, low_k = daily_series(recon, k)
            blocks_p, blocks_l = paired_blocks_from_daily(pnl_k, low_k)
            t0 = time.time()
            run = run_tier_remc(
                firm_key, blocks_p, thr, n_sims=(smoke_sims or thr.sims_per_seed), consistency=cons, intraday_blocks=blocks_l
            )
            wall = time.time() - t0
            verdict = score_part_a(run, thr)
            med_days = float(np.median(run["days_to_pass"])) if run.get("days_to_pass") else float("nan")
            print(
                f"{k:>2} {run['headline_bust']:>8.2%} {run['pass_rate']:>8.2%} "
                f"{med_days:>9.0f} {('PASS' if verdict else 'FAIL'):>7}  ({wall:.0f}s)"
            )
            firm_report["k"][k] = {
                "headline_bust": float(run["headline_bust"]),
                "pass_rate": float(run["pass_rate"]),
                "median_days_to_pass": med_days,
                "clears_part_a": bool(verdict),
            }
        report["firms"][firm_key] = firm_report
        print(f"[firm ] {firm_key} done in {time.time() - t_firm0:.0f}s")

    dest = _HERE / "run_orb_mnq_bulenox_blusky_report.json"
    dest.write_text(json.dumps(report, indent=2, default=float) + "\n", encoding="utf-8")
    print(f"\n[write] {dest}")

    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    any_pass = False
    for firm_key in TARGET_FIRMS:
        for k in K_GRID:
            c = report["firms"][firm_key]["k"][k]
            tag = "PASS" if c["clears_part_a"] else "FAIL"
            if c["clears_part_a"]:
                any_pass = True
            print(f"  {firm_key:22s} k={k}  bust={c['headline_bust']:.2%}  pass={c['pass_rate']:.2%}  {tag}")
    print(f"\nAny (firm,k) clears both frozen limbs: {any_pass}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
