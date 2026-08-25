#!/usr/bin/env python3
"""Q-ICT-1MEXEC-1 Stage 2 -- cost-law screen (the frozen design's own cheapest,
first kill point; PREREG Sec8: "Stage 2 is deliberately first and cheap: the
cost-law screen at the Tradeify basis kills or clears the construct before any
DSR machinery runs, and it is where D5 and H-OD-1 both died.").

Falsifier F1 (PREREG Sec4): Stage-2 gross edge vs MNQ hurdle, Tradeify $0.91
basis, < 4.0x -> FALSIFIED at Stage 2. Campaign closes; Stages 3-8 never run.

Cost basis: FLAT per-contract commission (Tradeify $0.91/side), NOT
`harness_1m.py`'s own COMM_PCT (a 0.002%-of-notional model inherited from the
ORIGINAL Pine strategy-tester config -- superseded for THIS campaign by
PREREG Sec3's explicit "Cost basis (binding): Tradeify $0.91/side" row).
Round-trip cost in price units: 2*$0.91/$2-per-point + 2*1 tick*0.25 =
0.91 + 0.50 = 1.41 pt -- independently matches the already-established
"1.41-pt basis" figure cited in `ops/instruments/MNQ.md`'s MNQPOOL-1 entry,
which used the identical Tradeify/MNQ cost structure. Bulenox $0.61 basis
reported alongside, non-binding, per PREREG Sec3.

Convention: edge/cost ratio = mean(gross_R) / mean(cost_R) over the tradeable
population >= 4.0 (PREREG Sec3 "Cost-law bar: 4.0x, convention edge/mean_cost_R").

$0/K=1 (this campaign's sole bound candidate). Writes only to this directory.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CASCADE_DIR = HERE.parent.parent.parent / "archive" / "ict_cascade_2026-06-18"
for p in (CASCADE_DIR, HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import harness_1m as H1M  # noqa: E402  (Trade / r_gross imported unchanged)
from build_1m_trades import build_all_trades  # noqa: E402

MNQ_POINT_VALUE_USD = 2.0
MINTICK = 0.25

# Tradeify (LOCKED / binding) and Bulenox (REPORT-ONLY) round-trip cost bases,
# in price points -- PREREG Sec3.
BASES = {
    "tradeify_binding": dict(cost_per_side_usd=0.91, slip_ticks_rt=2),
    "bulenox_report_only": dict(cost_per_side_usd=0.61, slip_ticks_rt=2),
}


def cost_price_flat(cost_per_side_usd: float, slip_ticks_rt: int) -> float:
    """Flat per-contract round-trip cost, in PRICE POINTS (not yet divided by
    any trade's stop_dist)."""
    comm_pt = (2.0 * cost_per_side_usd) / MNQ_POINT_VALUE_USD
    slip_pt = slip_ticks_rt * MINTICK
    return comm_pt + slip_pt


def cost_r_flat(stop_dist: float, cost_per_side_usd: float, slip_ticks_rt: int) -> float:
    """Flat per-contract round-trip cost, in R, for one trade's own stop_dist."""
    if stop_dist is None or (isinstance(stop_dist, float) and np.isnan(stop_dist)) or stop_dist <= 0:
        return float("nan")
    return cost_price_flat(cost_per_side_usd, slip_ticks_rt) / stop_dist


def apply_tradeability_floor_flat(trades, cost_per_side_usd: float, slip_ticks_rt: int, mintick=MINTICK):
    """PREREG-1M's own ledger-F8 tradeability floor (`stop_dist < max(1 mintick,
    cost)` -> drop), re-derived at the FLAT Tradeify/Bulenox cost basis this
    campaign uses -- `harness_1m.apply_tradeability_floor` can't be reused
    directly, because it prices `cost` from that module's own COMM_PCT (the
    original Pine's 0.002%-of-notional model, superseded for this campaign by
    PREREG Sec3's flat per-contract basis). Same structure, correct cost model.
    Returns (kept_trades, n_dropped)."""
    floor = max(1.0 * mintick, cost_price_flat(cost_per_side_usd, slip_ticks_rt))
    kept = [t for t in trades if t.stop_dist >= floor]
    return kept, len(trades) - len(kept), floor


def main(argv=None) -> int:
    parquet_path = HERE / "mnq_1m.parquet"
    if not parquet_path.exists():
        print(f"ABORT: {parquet_path} not found -- run the databento pull first.")
        return 2

    bars = pd.read_parquet(parquet_path)
    ts_col = bars["ts_event"] if "ts_event" in bars.columns else bars.index
    print(f"[data] {parquet_path}  rows={len(bars):,}  "
          f"span={pd.to_datetime(ts_col.min())} -> {pd.to_datetime(ts_col.max())}")

    trades, diag = build_all_trades(bars)
    print(f"[chain] {json.dumps(diag, indent=2)}")

    if not trades:
        print("STOPPING -- zero trades survive the frozen chain + arm filters. "
              "No cost-law ratio can be computed. This IS a Stage-2-adjacent result: "
              "the construct produces no admissible entries on the full panel.")
        out = HERE / "results_stage2_costlaw.json"
        out.write_text(json.dumps({"diag": diag, "n_trades": 0, "verdict": "NO_TRADES"}, indent=2))
        return 1

    report = {"diag": diag, "n_trades": len(trades), "bases": {}}
    for basis_name, cfg in BASES.items():
        tradeable, n_dropped_floor, floor = apply_tradeability_floor_flat(
            trades, cfg["cost_per_side_usd"], cfg["slip_ticks_rt"])
        print(f"\n[{basis_name}] tradeability floor={floor:.4f}pt  "
              f"dropped {n_dropped_floor}/{len(trades)} trades below it "
              f"(stop_dist < max(1 mintick, round-trip cost) -- PREREG ledger F8)")

        gross = np.array([H1M.r_gross(t) for t in tradeable], dtype=float)
        # Invariant: a stop-hit trade is exit_price==stop_price by construction,
        # so r_gross == exactly -1.0; nothing in this simulation can produce a
        # gross R below -1 (a violation caught a real bug this session -- a
        # missing tradeability floor let razor-thin stop_dist trades inflate an
        # ordinary flat-deadline exit into an implausible R-multiple).
        finite_gross = gross[~np.isnan(gross)]
        if len(finite_gross) and finite_gross.min() < -1.0001:
            n_bad = int((finite_gross < -1.0001).sum())
            raise AssertionError(
                f"[{basis_name}] INVARIANT VIOLATED: {n_bad}/{len(finite_gross)} trades have "
                f"gross R < -1.0 (min={finite_gross.min():.2f}) -- a stop-hit trade cannot exceed "
                f"R=-1 by construction. Do not trust this run's verdict; find the exit-price bug "
                f"before re-running."
            )
        cost = np.array([cost_r_flat(t.stop_dist, cfg["cost_per_side_usd"], cfg["slip_ticks_rt"])
                          for t in tradeable], dtype=float)
        valid = ~(np.isnan(gross) | np.isnan(cost) | np.isinf(cost))
        n_valid = int(valid.sum())
        mean_gross = float(np.mean(gross[valid])) if n_valid else float("nan")
        mean_cost = float(np.mean(cost[valid])) if n_valid else float("nan")
        median_cost = float(np.median(cost[valid])) if n_valid else float("nan")
        ratio = mean_gross / mean_cost if (n_valid and mean_cost > 0) else float("nan")
        net_r = gross[valid] - cost[valid] if n_valid else np.array([])
        hurdle_4x_median = 4.0 * median_cost

        print(f"\n[{basis_name}] n_valid={n_valid}  mean_gross_R={mean_gross:.4f}  "
              f"mean_cost_R={mean_cost:.4f}  median_cost_R={median_cost:.4f}  "
              f"ratio(edge/cost)={ratio:.3f}  hurdle(4x median)={hurdle_4x_median:.4f}  "
              f"mean_net_R={float(np.mean(net_r)) if len(net_r) else float('nan'):.4f}  "
              f"pct_net_positive={float(np.mean(net_r > 0)) * 100 if len(net_r) else float('nan'):.1f}%")

        report["bases"][basis_name] = dict(
            tradeability_floor_pt=floor, n_dropped_below_floor=n_dropped_floor,
            n_valid=n_valid, mean_gross_r=mean_gross, mean_cost_r=mean_cost,
            median_cost_r=median_cost, ratio_edge_over_cost=ratio,
            hurdle_4x_median_cost=hurdle_4x_median,
            mean_net_r=float(np.mean(net_r)) if len(net_r) else float("nan"),
            pct_net_positive=float(np.mean(net_r > 0)) * 100 if len(net_r) else float("nan"),
        )

    tradeify_ratio = report["bases"]["tradeify_binding"]["ratio_edge_over_cost"]
    f1_fires = not (tradeify_ratio >= 4.0) if not np.isnan(tradeify_ratio) else True
    verdict = "FALSIFIED_F1" if f1_fires else "STAGE2_CLEAR"
    report["verdict"] = verdict
    report["f1_fires"] = bool(f1_fires)

    print("\n" + "=" * 100)
    print(f"STAGE 2 VERDICT (Tradeify $0.91 binding basis): edge/cost ratio = {tradeify_ratio:.3f}  "
          f"(need >= 4.0)  ->  {verdict}")
    if f1_fires:
        print("F1 FIRES -- FALSIFIED at Stage 2. Per the frozen falsifier table, Stages 3-8 never run.")
    print("=" * 100)

    out = HERE / "results_stage2_costlaw.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    return 0 if not f1_fires else 1


if __name__ == "__main__":
    raise SystemExit(main())
