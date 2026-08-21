#!/usr/bin/env python3
"""DL-1 (MGC-ORC) -- prereg Sec6 steps 1-2: pulls (already landed) + TRAIN +
nomination, ONLY. Never reads the MGC.FUT confirm partition -- there is no
code path in this package that can (stitch.py hardcodes GC.FUT/TRAIN_START/
TRAIN_END; no confirm symbol or window appears anywhere in this directory).
Confirm read (step 3) is a separate, deliberate, one-shot action gated on its
own operator go -- prereg Sec5: "Reading confirm during iteration ... One
nominee, one read, ever."

Run (repo root, research venv with arch installed):
    PYTHONPATH=lab python lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/run_train.py
"""
from __future__ import annotations

import json
import sys

from stitch import load_train_stitched
from variants import VARIANTS
from engine import build_day_slices, compute_or, compute_drift, simulate_variant, trading_calendar
from score import score_variant, spa_universe, m16_slip_gate, cost_law_gate


def main() -> int:
    print("[load] stitching TRAIN partition (GC.FUT, 2010-06-06 -> 2019-01-01) ...")
    stitched, roll_dates = load_train_stitched()
    print(f"[load] stitched bars: {len(stitched):,}  roll days: {len(roll_dates)}")

    slices = build_day_slices(stitched)
    trading_dates = trading_calendar(slices)
    print(f"[load] trading dates in TRAIN window (CME calendar -- 08:30-15:55 ET sessions only,"
          f" Sunday-reopen dates excluded): {len(trading_dates)}"
          f"  ({trading_dates[0]} .. {trading_dates[-1]})")

    or30 = compute_or(slices, 30)
    or60 = compute_or(slices, 60)
    drift = compute_drift(slices)
    n_drift = sum(1 for v in drift.values() if v)
    print(f"[load] OR-30 sessions: {len(or30)}  OR-60 sessions: {len(or60)}"
          f"  drift-defined sessions: {n_drift}")

    results = {}
    trades_by_variant = {}
    print("\n[score] TRAIN results (all 10 frozen variants, iteration-legal):")
    header = f"{'V':>2} {'OR':>3} {'drift':>13} {'style':>8} {'R':>4} {'n':>5} {'net_annSR':>10} {'trades/wk':>9} {'stop_ticks':>10} {'ratio':>6}"
    print(header)
    print("-" * len(header))
    for var in VARIANTS:
        trades = simulate_variant(slices, or30, or60, drift, roll_dates, var)
        trades_by_variant[var.v] = trades
        res = score_variant(trades, trading_dates)
        results[var.v] = res
        cl = res.cost_law
        print(f"{var.v:>2} {var.or_minutes:>3} {var.drift:>13} {var.entry_style:>8} "
              f"{var.target_r:>4.1f} {res.n_trades:>5} {res.net_annsr:>10.4f} "
              f"{res.cadence_per_week:>9.3f} {cl['median_stop_ticks']:>10.1f} {cl['ratio']:>6.2f}")

    nominee_v = max(results, key=lambda v: results[v].net_annsr)
    nominee = results[nominee_v]
    nominee_var = next(v for v in VARIANTS if v.v == nominee_v)
    print(f"\n[nominate] argmax train net annSR -> V{nominee_v} "
          f"(net_annSR={nominee.net_annsr:.4f}, n={nominee.n_trades}) -- no fallback, no walk-down.")

    print("\n[gate 2a] cost-law: train net annSR > 0 AND ratio >= 4x at realized geometry")
    gate_a_annsr = nominee.net_annsr > 0.0
    gate_a_ratio = nominee.cost_law["passed"]
    gate_a = gate_a_annsr and gate_a_ratio
    print(f"          net_annSR>0: {gate_a_annsr}  ratio>=4x: {gate_a_ratio} "
          f"(ratio={nominee.cost_law['ratio']:.2f}, median_stop={nominee.cost_law['median_stop_ticks']:.1f} ticks)"
          f"  => {'PASS' if gate_a else 'FAIL'}")

    print("\n[gate 2b] SPA (Hansen) consistent p <= 0.10 vs zero benchmark, full 10-variant universe")
    daily_by_variant = {v: results[v].daily_pnl for v in results}
    spa = spa_universe(daily_by_variant)
    print(f"          p={spa['p_value']:.4f}  better_variants={spa['better_variants']}"
          f"  => {'PASS' if spa['passed'] else 'FAIL'}")

    print("\n[gate 2c] N-ACT: nominee cadence >= 1 trade/week")
    gate_c = nominee.cadence_per_week >= 1.0
    print(f"          cadence={nominee.cadence_per_week:.3f} trades/wk  => {'PASS' if gate_c else 'FAIL'}")

    print("\n[gate 2d] M-16: nominee train net annSR stays > 0 at +1 tick/side additional slip")
    slip_trades = simulate_variant(slices, or30, or60, drift, roll_dates, nominee_var, extra_slip_ticks=1)
    m16 = m16_slip_gate(slip_trades, trading_dates)
    print(f"          net_annSR(+1tick)={m16['net_annsr_plus1tick']:.4f}  => {'PASS' if m16['passed'] else 'FAIL'}")

    all_pass = gate_a and spa["passed"] and gate_c and m16["passed"]
    print("\n" + "=" * 60)
    if all_pass:
        print(f"VERDICT: V{nominee_v} clears all 4 nomination gates -- ELIGIBLE for confirm read (Sec6 step 3).")
        print("Confirm read is a separate action requiring its own explicit go -- not taken by this script.")
    else:
        print(f"VERDICT: ABANDONMENT -- V{nominee_v} (the nominee) fails at least one nomination gate.")
        print("Per prereg Sec4: dated, no strike, confirm partition stays unread.")
    print("=" * 60)

    out = {
        "nominee": nominee_v,
        "gates": {
            "2a_cost_law": {"annsr_positive": gate_a_annsr, "ratio_ge_4x": gate_a_ratio, "passed": gate_a,
                              "detail": nominee.cost_law},
            "2b_spa": spa,
            "2c_cadence": {"cadence_per_week": nominee.cadence_per_week, "passed": gate_c},
            "2d_m16_slip": m16,
        },
        "all_pass": all_pass,
        "verdict": "ELIGIBLE_FOR_CONFIRM_READ" if all_pass else "ABANDONMENT",
        "per_variant": {
            v: {"n_trades": r.n_trades, "net_annsr": r.net_annsr, "cadence_per_week": r.cadence_per_week,
                "cost_law": r.cost_law}
            for v, r in results.items()
        },
    }
    out_path = "lab/analysis/deep_lane/dl1_mgc_orc_2026-08-16/train_results.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"\n[done] wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
