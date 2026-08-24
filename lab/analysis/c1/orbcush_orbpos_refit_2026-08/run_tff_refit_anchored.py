#!/usr/bin/env python3
"""Q-ORBPOS-1 re-test under the corrected (anchored) date-correlation method.

Trigger / governance: see `run_meanr_refit_anchored.py`'s module docstring --
same operator GO, same source fix (`POSITIVE_CONTROL_METHOD_FIX.md`), same
two-axis reporting discipline.

Candidate: CFTC TFF Leveraged-Funds |net %OI| positioning-extremity classifier
vs ORB-MNQ-1's 2021-09-28 break -- the SAME classifier `run_orbpos_tff_probe.py`
(Q-ORBPOS-1, FALSIFIED) built and tested under the broken expanding-median
method. Unlike mean-R, this candidate needs NO new adapter: TFF's positioning
value is an external state variable (not the strategy's own realized outcome),
so `build_classifier_anchored` and `print_level_association` in
`run_orbpos_positive_control_v2_anchored.py` were already written generically
enough to apply directly to TFF's own `extremity_lf`/`available_date` frame --
this script only swaps the synthetic input for a fresh, real CFTC pull.

Everything reused byte-for-byte:
  - `run_orbpos_tff_probe.py` (as `A`): `pull_mnq_tff`, `add_publication_lag`,
    `build_extremity_series`, `confirm_mnq_standalone_line`, `WINDOWS`
    ({4,13,26} weekly prints), `CUTOFF`, `K`, `daily_label_from_weekly`,
    `gate_check_bucket`, `classify_direction`, `MIN_W1_PREBREAK_PRINTS`.
  - `run_orbpos_positive_control_v2_anchored.py` (as `V2`): `build_classifier_anchored`,
    `print_level_association`, `ASSOC_ALPHA`, `MIN_SEPARATION_PP`.
  - `_imported_run_evalseq_orb_intraday.py` (via `A.H`): the harness.

`ground_truth_accuracy` is NOT run here -- it requires a known synthetic
`true_regime` column that does not exist (and cannot exist) for real
positioning data; the whole point of this test is that the true regime-driver
is unknown.

Does NOT edit: `Q-ORBPOS-1-closure-falsified.md`, `POSITIVE_CONTROL.md`,
`POSITIVE_CONTROL_METHOD_FIX.md`, or `ops/instruments/MNQ.md`.

$0/K=0 -- diagnostic/explanatory re-measurement, same class as Q-ORBPOS-1
itself. One live network pull (cftc.gov Socrata public API, free, no key),
identical to the original probe. Writes only to this directory.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ORBPOS_DIR = HERE.parent / "q_orbpos_1_2026-08"
if str(ORBPOS_DIR) not in sys.path:
    sys.path.insert(0, str(ORBPOS_DIR))

import run_orbpos_tff_probe as A  # noqa: E402  (imported unchanged)
import run_orbpos_positive_control_v2_anchored as V2  # noqa: E402  (the frozen fix; imported unchanged)

CUTOFF = A.CUTOFF
WINDOWS = A.WINDOWS
K = A.K
ASSOC_ALPHA = V2.ASSOC_ALPHA
MIN_SEPARATION_PP = V2.MIN_SEPARATION_PP


def main() -> int:
    t0 = time.time()
    report: dict = {"cutoff": str(CUTOFF.date()), "K": K, "windows_tff_prints": WINDOWS,
                     "assoc_alpha": ASSOC_ALPHA, "min_separation_pp": MIN_SEPARATION_PP}

    print("=" * 100)
    print("Q-ORBPOS-1 REFIT -- CFTC TFF positioning-extremity under the corrected (anchored) method")
    print("=" * 100)

    print("\n--- live re-confirmation: MNQ standalone TFF line ---")
    line_check = A.confirm_mnq_standalone_line()
    print(f"  MNQ code={line_check['mnq_code']}  name={line_check['mnq_name']!r}")
    report["mnq_standalone_line_check"] = line_check

    print("\n--- fresh CFTC TFF pull (Socrata, free, no key) ---")
    tff = A.pull_mnq_tff()
    tff = A.add_publication_lag(tff)
    tff = A.build_extremity_series(tff)
    print(f"  n_rows={len(tff)}  first={tff['report_date'].min().date()}  last={tff['report_date'].max().date()}")
    max_xcheck = float(tff["net_pct_oi_crosscheck_delta"].max())
    print(f"  %OI derived-vs-published cross-check: max |delta|={max_xcheck:.3f}pp")
    report["pull"] = dict(n_rows=len(tff), first_report_date=str(tff["report_date"].min().date()),
                           last_report_date=str(tff["report_date"].max().date()),
                           max_crosscheck_delta_pp=max_xcheck)

    n_prebreak = int((tff["available_date"] < CUTOFF).sum())
    sparsity_trigger = n_prebreak < A.MIN_W1_PREBREAK_PRINTS
    print(f"  prebreak prints available: {n_prebreak}  sparsity trigger: {'FIRES' if sparsity_trigger else 'no'}")
    report["n_prebreak_published_prints"] = n_prebreak
    report["ambiguous_hold_trigger_1_prebreak_sparsity"] = bool(sparsity_trigger)

    H = A.H
    inst = H.make_inst()
    panel_pkl = H.resolve_panel()
    df_panel = pd.read_pickle(panel_pkl)
    piv, meta = H.ol.session_panel(df_panel, inst)
    bt = H.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"[ctrl ] Control B mirror PASS -- n={len(recon)} triggering days")
    report["n_triggering_days"] = len(recon)
    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())

    thr = H.load_scoring_thresholds()
    H.assert_engine_ready(H.TIER)
    fkw_base = H.firm_kwargs(H.TIER, inactivity_off=True, consistency=H.CONSISTENCY_FRAC)
    if fkw_base["dd_lock_offset_usd"] == H.LOCK_AS_PUBLISHED:
        fkw = dict(fkw_base, dd_lock_offset_usd=H.LOCK_UNREACHABLE)
    else:
        fkw = dict(fkw_base)
    assert fkw["profit_target"] == H.TARGET
    assert fkw["starting_equity"] == H.START
    assert fkw["trailing_dd_pct"] == -H.DD / H.START

    print("\n" + "=" * 100)
    print("(1) FIDELITY CONTROL -- flat policy, m=1.0, full panel, k=1/k=2")
    print("=" * 100)
    PUBLISHED = {1: 67.67, 2: 77.01}
    TOL_PP = 2.0
    control, flat_ok_k1 = {}, True
    for k in (1, 2):
        panel_full_k = H.build_k_panel(recon, k)
        bpnl, blow = H.blocks_from_panel(panel_full_k)
        r = H.run_policy_orb(bpnl, blow, H.pol_const(1.0), use_intraday=True,
                              horizon=thr.horizon, seeds=thr.seeds, n_paths=thr.sims_per_seed)
        delta = r["bust_pct"] - PUBLISHED[k]
        ok = abs(delta) <= TOL_PP
        if k == 1:
            flat_ok_k1 = ok
        control[k] = dict(bust_pct=r["bust_pct"], pass_pct=r["pass_pct"], published=PUBLISHED[k],
                           delta_pp=delta, within_tol=ok)
        print(f"  k={k}  bust={r['bust_pct']:.2f}%  published={PUBLISHED[k]:.2f}%  delta={delta:+.2f}pp  "
              f"{'PASS' if ok else 'FAIL'}")
    report["fidelity_control"] = control
    report["fidelity_control_pass_k1"] = bool(flat_ok_k1)
    if not flat_ok_k1:
        print("STOPPING -- fidelity control failed.")
        (HERE / "results_tff_refit_anchored.json").write_text(json.dumps(report, indent=2, default=str))
        return 2

    panel_full_k1 = H.build_k_panel(recon, K)

    windows_report = {}
    for wname, wsize in WINDOWS.items():
        print("\n" + "=" * 100)
        print(f"{wname} -- window={wsize} weekly prints")
        print("=" * 100)

        clf = V2.build_classifier_anchored(tff, wsize)
        print(f"[classifier] WARMUP={clf['n_warmup']} HIGHER={clf['n_higher']} LOWER={clf['n_lower']} "
              f"i_freeze={clf['i_freeze']} frozen_value={clf['frozen_value']} "
              f"spotcheck={'PASS' if clf['spotcheck_pass'] else 'FAIL'} "
              f"degenerate_pre={'YES' if clf['degenerate_threshold'] else 'no'}")

        assoc = V2.print_level_association(tff, clf["label"], clf["roll_W"])
        print(f"[assoc] n_higher={assoc['n_higher']} n_lower={assoc['n_lower']} "
              f"frac_higher_post={assoc['frac_higher_post']:.1%} frac_lower_post={assoc['frac_lower_post']:.1%} "
              f"separation={assoc['separation_pp']:+.1%} fisher_p={assoc['fisher_p']:.3g} "
              f"point_biserial_r={assoc['point_biserial_r']:.3f} (p={assoc['point_biserial_p']:.3g}) "
              f"corrected_pass={'YES' if assoc['corrected_pass'] else 'NO'}")

        daily_label = A.daily_label_from_weekly(tff, clf["label"], full_idx)
        gate_higher = A.gate_check_bucket(panel_full_k1, daily_label, "HIGHER", thr, fkw)
        gate_lower = A.gate_check_bucket(panel_full_k1, daily_label, "LOWER", thr, fkw)
        direction = A.classify_direction(gate_higher, gate_lower)
        print(f"[gate] HIGHER cushion pass={gate_higher['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['cushion']['gate_pass'] else 'FAIL'}  |  "
              f"LOWER cushion pass={gate_lower['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['cushion']['gate_pass'] else 'FAIL'}  direction={direction}  "
              f"(elapsed {time.time()-t0:.0f}s)")

        windows_report[wname] = dict(
            window_prints=wsize,
            classifier=dict(n_warmup=clf["n_warmup"], n_higher=clf["n_higher"], n_lower=clf["n_lower"],
                             i_freeze=clf["i_freeze"], frozen_value=clf["frozen_value"],
                             spotcheck_pass=clf["spotcheck_pass"], degenerate_threshold=clf["degenerate_threshold"]),
            association=assoc,
            gate={"HIGHER": gate_higher, "LOWER": gate_lower},
            direction=direction,
        )

    report["windows"] = windows_report

    n_corrected_pass = sum(1 for w in windows_report.values() if w["association"]["corrected_pass"])
    directions = [w["direction"] for w in windows_report.values()]
    signed = {d for d in directions if d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT")}
    direction_stable = len(signed) == 1 and all(
        d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT") for d in directions
    )

    report["summary"] = dict(
        corrected_association_windows_passing=n_corrected_pass,
        corrected_association_fires_at_ge2_of_3=bool(n_corrected_pass >= 2),
        directions_by_window={wn: w["direction"] for wn, w in windows_report.items()},
        direction_same_sign_every_window=bool(direction_stable),
    )

    print("\n" + "=" * 100)
    print("SUMMARY -- TWO AXES REPORTED SEPARATELY (per POSITIVE_CONTROL_METHOD_FIX.md Sec6.3)")
    print("=" * 100)
    print(f"  AXIS 1 -- corrected date-correlation-equivalent clears (>=2 of 3)?  {n_corrected_pass}/3  -> "
          f"{'FIRES' if n_corrected_pass >= 2 else 'does not fire'}")
    print(f"  AXIS 2 -- gate-clearance direction same sign, every window?  {'YES' if direction_stable else 'NO'}  "
          f"({report['summary']['directions_by_window']})")

    out = HERE / "results_tff_refit_anchored.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
