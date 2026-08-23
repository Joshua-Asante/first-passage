#!/usr/bin/env python3
"""DL-2 (M6A-PDHPDL) -- prereg Sec6 steps 1-2: pulls (already landed) + TRAIN
+ nomination, ONLY. Never reads the M6A.FUT confirm partition -- there is no
code path in this package that can (stitch.py hardcodes 6A.FUT/TRAIN_START/
TRAIN_END; no confirm symbol or window appears anywhere in this directory).
Confirm read (step 3) is a separate, deliberate, one-shot action gated on its
own operator go -- prereg Sec5: "Reading confirm during iteration ... One
nominee, one read, ever."

Run (repo root):
    PYTHONPATH=lab python lab/analysis/dl2_m6a_pdhpdl_2026-08-22/run_train.py
"""
from __future__ import annotations

import json
import sys

from stitch import load_train_stitched
from variants import VARIANTS
from engine import build_sessions, is_roll_session_map, trading_calendar, simulate_variant
from score import score_variant, spa_universe, m16_slip_gate


def main() -> int:
    print("[load] stitching TRAIN partition (6A.FUT, 2010-06-06 -> 2019-01-01) ...")
    stitched, roll_days_utc = load_train_stitched()
    print(f"[load] stitched bars: {len(stitched):,}  UTC roll days: {len(roll_days_utc)}")

    sessions = build_sessions(stitched)
    is_roll = is_roll_session_map(sessions, roll_days_utc)
    session_dates = trading_calendar(sessions)
    nonroll_dates = [d for d in session_dates if not is_roll[d]]
    n_roll_sessions = sum(1 for d in session_dates if is_roll[d])
    print(f"[load] Globex sessions in TRAIN window: {len(session_dates)}"
          f"  ({session_dates[0]} .. {session_dates[-1]})"
          f"  roll sessions (entries excluded): {n_roll_sessions}")

    results = {}
    trades_by_variant = {}
    print("\n[score] TRAIN results (all 10 frozen variants, iteration-legal):")
    header = f"{'V':>2} {'LB':>2} {'drift':>13} {'style':>13} {'R':>4} {'n':>5} {'net_annSR':>10} {'trades/wk':>9} {'stop_ticks':>10} {'ratio':>6}"
    print(header)
    print("-" * len(header))
    for var in VARIANTS:
        trades = simulate_variant(sessions, session_dates, nonroll_dates, is_roll, var)
        trades_by_variant[var.v] = trades
        res = score_variant(trades, session_dates)
        results[var.v] = res
        cl = res.cost_law
        print(f"{var.v:>2} {var.lookback:>2} {var.drift:>13} {var.entry_style:>13} "
              f"{var.target_r:>4.1f} {res.n_trades:>5} {res.net_annsr:>10.4f} "
              f"{res.cadence_per_week:>9.3f} {cl['median_stop_ticks']:>10.1f} {cl['ratio']:>6.2f}")

    nominee_v = max(results, key=lambda v: results[v].net_annsr)
    nominee = results[nominee_v]
    nominee_var = next(v for v in VARIANTS if v.v == nominee_v)

    # Tie check (prereg Sec6: "no fallback" -- an exact argmax tie is a
    # NEEDS_CONTEXT case per the handoff's own Sec0.5, not a coin-flip).
    top_sr = nominee.net_annsr
    ties = [v for v in results if results[v].net_annsr == top_sr]
    if len(ties) > 1:
        print(f"\n[TIE] variants {ties} are tied at net_annSR={top_sr:.6f} -- NEEDS_CONTEXT, not resolved here.")
        return 2

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
    slip_trades = simulate_variant(sessions, session_dates, nonroll_dates, is_roll, nominee_var, extra_slip_ticks=1)
    m16 = m16_slip_gate(slip_trades, session_dates)
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
        "campaign": "DL2-M6A-PDHPDL",
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
        "train_window": {"start": "2010-06-06", "end": "2019-01-01",
                          "n_sessions": len(session_dates), "n_roll_sessions": n_roll_sessions},
    }
    out_path = "lab/archive/dl2_m6a_pdhpdl_2026-08-22/train_results.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2, default=float)
    print(f"\n[done] wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
