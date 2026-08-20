#!/usr/bin/env python3
"""THIRDS re-run of run_evalseq_orb_intraday.py's Section 4 (pol_cushion vs flat-k1/
flat-k2, intraday-honest, Tradeify_Select_100K survivor-scoring gate).

Purpose: run_evalseq_orb_intraday.py's halves (H1/H2) split found H2 (the modern-era
half, roughly 2022-12-09 -> 2026-07-15) clears the frozen ADR gate (bust<=3.0% AND
pass>=50%) for the first time, while H1 (2019-05-06 -> ~2022-12-08, includes the 2020
COVID crash + ORB's own documented dead-until-2021 years) badly fails it. This repo's
own convention for checking whether a two-way split result is boundary-luck (see
Q-WLEGB-1's "both halves and all thirds" pattern) is to re-run the SAME check on a
finer split and see whether the result survives.

This file does EXACTLY THAT and nothing else: it replaces the halves split with a
THIRDS split of the SAME `full_idx` business-day index, using the SAME block-boundary
discipline (Monday-anchored 5-day blocks built fresh per slice via blocks_from_panel,
so a block can never straddle a third boundary any more than the halves version let
one straddle the halves boundary -- both versions build blocks from
`panel_full.loc[panel_full.index.isin(<slice>)]`, a locally-reindexed slice, so
blocks_from_panel's own `i+5<=len(panel)` bound is relative to the slice, not the
full panel). Every other piece -- day_loop_intraday, build_paths_orb, run_policy_orb,
pol_cushion, pol_const, blocks_from_panel, build_k_panel, build_paired_blocks,
orb_days_with_excursion, the panel-loading/reconstruction code, the Control B mirror
check -- is imported UNCHANGED from run_evalseq_orb_intraday.py (same file, same
directory), not re-derived. Same thr.horizon / thr.seeds / thr.sims_per_seed
(TIER-derived, printed at runtime) and the same K_GRID=(1,2), CONSISTENCY_FRAC=0.40
as the halves run, so results are comparable apples-to-apples.

The Section-3 fidelity control (new day_loop_intraday flat-policy vs published
67.67%/77.01% intraday-honest bust anchors) and the Control G published-anchor check
are NOT re-run here -- they test the full-panel reconstruction pipeline, which is
identical code operating on the identical `recon` DataFrame this file also builds,
and already PASSED in the halves run earlier this session. Re-running them would
duplicate already-established evidence, not test anything new about the thirds
question. Control B (mirror recon vs orb_lib.orb_backtest) IS re-run below -- it is
near-zero-cost (a set of array equality asserts, no MC) and is the direct guarantee
that THIS file's `recon` is the same data the thirds split is being cut from.

$0/K=0. Writes only to this scratch directory. Touches no repo file.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent
if str(OUT_DIR) not in sys.path:
    sys.path.insert(0, str(OUT_DIR))

# Import everything from the already-verified halves harness, UNCHANGED. Importing
# (as opposed to running) this module only executes its module-level sys.path setup
# and def/class statements -- main() is guarded by `if __name__ == "__main__"` in
# that file, so importing it here never re-runs its own main().
import run_evalseq_orb_intraday as H  # noqa: E402

import orb_lib as ol  # noqa: E402  (already on sys.path via H's own module-level insert)


def main():
    t0 = time.time()
    report: dict = {}

    print("=" * 96)
    print("THIRDS re-run: Q-EVALSEQ-1 cushion policy on ORB-MNQ-1's intraday-honest construct")
    print("(same harness as run_evalseq_orb_intraday.py Section 4, split into 3 instead of 2)")
    print("=" * 96)

    thr = H.load_scoring_thresholds()
    print(f"[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}  "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%}  pass_floor={thr.pass_floor:.0%}")

    panel_pkl = H.resolve_panel()
    df = pd.read_pickle(panel_pkl)
    print(f"[data ] {panel_pkl}")
    print(f"[data ] rows={len(df):,}  span={df['et'].min()} -> {df['et'].max()}")

    inst = H.make_inst()
    piv, meta = ol.session_panel(df, inst)
    bt = ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")

    print("\n--- Control B (re-run, unchanged): mirror vs orb_lib.orb_backtest ---")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"  PASS -- n={len(recon)}")

    # ---------------------------------------------------------------- THIRDS split
    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    n = len(full_idx)
    c1 = n // 3
    c2 = 2 * n // 3
    thirds = {
        "T1": full_idx[:c1],
        "T2": full_idx[c1:c2],
        "T3": full_idx[c2:],
    }
    print(f"\n[split] {n} business days, cut1={c1} cut2={c2}  "
          f"T1={full_idx[0].date()}->{full_idx[c1-1].date()}  "
          f"T2={full_idx[c1].date()}->{full_idx[c2-1].date()}  "
          f"T3={full_idx[c2].date()}->{full_idx[-1].date()}")

    print("\n" + "=" * 96)
    print("POL_CUSHION -- three thirds, intraday-honest, vs flat-k1/flat-k2 controls, same thirds")
    print("=" * 96)

    cushion_report = {}
    gate_bust_ceiling = thr.eval_bust_ceiling  # 3.0% per ADR
    gate_pass_floor = thr.pass_floor            # 50% per ADR

    for third_name, third_idx in thirds.items():
        cushion_report[third_name] = {}
        for base_k in H.K_GRID:
            panel_full = H.build_k_panel(recon, base_k)
            panel_third = panel_full.loc[panel_full.index.isin(third_idx)]
            bpnl, blow = H.blocks_from_panel(panel_third)
            n_blocks = len(bpnl)

            flat = H.run_policy_orb(bpnl, blow, H.pol_const(1.0), use_intraday=True,
                                     horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
            cush = H.run_policy_orb(bpnl, blow, H.pol_cushion, use_intraday=True,
                                     horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)

            def _gate(bust_pct, pass_pct):
                return (bust_pct <= gate_bust_ceiling * 100.0) and (pass_pct >= gate_pass_floor * 100.0)

            flat_gate = _gate(flat["bust_pct"], flat["pass_pct"])
            cush_gate = _gate(cush["bust_pct"], cush["pass_pct"])
            delta = cush["bust_pct"] - flat["bust_pct"]

            cushion_report[third_name][f"base_k{base_k}"] = dict(
                n_blocks=n_blocks,
                flat_bust_pct=flat["bust_pct"], flat_pass_pct=flat["pass_pct"], flat_gate_pass=flat_gate,
                cushion_bust_pct=cush["bust_pct"], cushion_pass_pct=cush["pass_pct"], cushion_gate_pass=cush_gate,
                delta_bust_pp=delta,
            )
            print(f"  {third_name} base=k{base_k} (n_blocks={n_blocks})  "
                  f"flat: bust={flat['bust_pct']:.2f}% pass={flat['pass_pct']:.2f}% "
                  f"gate={'PASS' if flat_gate else 'FAIL'}  |  "
                  f"cushion(0.75x max): bust={cush['bust_pct']:.2f}% pass={cush['pass_pct']:.2f}% "
                  f"gate={'PASS' if cush_gate else 'FAIL'}  "
                  f"delta={delta:+.2f}pp  (elapsed {time.time()-t0:.0f}s)")

    report["cushion_thirds"] = cushion_report
    report["third_split"] = dict(
        n_bdays=n, cut1=c1, cut2=c2,
        t1_start=str(full_idx[0].date()), t1_end=str(full_idx[c1 - 1].date()),
        t2_start=str(full_idx[c1].date()), t2_end=str(full_idx[c2 - 1].date()),
        t3_start=str(full_idx[c2].date()), t3_end=str(full_idx[-1].date()),
    )
    report["gate"] = dict(bust_ceiling_pct=gate_bust_ceiling * 100.0, pass_floor_pct=gate_pass_floor * 100.0)

    out = OUT_DIR / "evalseq_orb_thirds_results.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
