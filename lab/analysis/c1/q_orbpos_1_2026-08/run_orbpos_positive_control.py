#!/usr/bin/env python3
"""Q-ORBPOS-1 POSITIVE CONTROL -- apparatus-validity check, not a candidate-mechanism test.

Purpose (per operator task, 2026-08-23): the three real economic candidates tested
against ORB-MNQ-1's 2021-09-28 cushion-sizing gate-clearance break (trailing
volatility, trailing mean-R, CFTC TFF Leveraged-Funds positioning-extremity) all
came back FALSIFIED under the identical three-window bucket-split +
gate-clearance-direction pipeline. Before trusting those three nulls as
apparatus-VALID (i.e. "the pipeline would have caught a real signal if one were
there"), this script runs the IDENTICAL pipeline on a SYNTHETIC classifier
constructed to be KNOWN, by design, to correlate strongly with the true
pre/post-2021-09-28 split -- but not deterministically. This is a check on the
apparatus, not a new economic claim. No real economic/positioning data is used
here; nothing in this file consumes K or needs fresh pre-registration ceremony
(same reasoning as the Ambiguous-hold/diagnostic class of question the parent
brief itself is -- this is one further rung down, a pure methodology probe).

============================================================================
FROZEN SYNTHETIC DESIGN -- written down BEFORE this script is run, and NOT
changed after seeing any result. This block is the pre-registration for this
positive control.
============================================================================

Date range: weekly Tuesdays from 2020-08-04 (the real TFF classifier's own
first available print date, per Q-ORBPOS-1 Phase 1 / RESULTS.md) through
2026-07-15 (ORB-MNQ-1's own price-panel end, `PANEL_END` in
run_orbpos_tff_probe.py). Both endpoints fall on a Tuesday-anchored weekly grid
(2020-08-04 and 2021-09-28 -- the real break date -- are themselves Tuesdays;
verified via the stdlib `datetime` module before writing this file). This
reproduces the real classifier's pre-break print count exactly (45 prints
before 2021-09-28), so the positive control faces the identical "how much
pre-break history exists" constraint the real TFF candidate faced -- no
generosity is smuggled in via a larger or more favorably-shaped sample.

Construction: a two-state Gaussian step process, published at the same weekly
cadence and under the same causal publication-lag convention
(`add_publication_lag`, reused UNCHANGED from Implementation A -- Tuesday
snapshot, Friday-of-that-week publication) as the real TFF pull:

    extremity_synthetic[i] = MU_POST if report_date[i] >= CUTOFF else MU_PRE
                              + SIGMA * eps[i],   eps[i] ~ iid N(0, 1)

    MU_PRE  = 0.0
    MU_POST = 2.0     (Cohen's d = (MU_POST - MU_PRE) / SIGMA = 2.0 -- a "large"
                        effect size in the conventional sense, but NOT
                        deterministic: a single raw weekly draw still lands on
                        the "wrong side" of the population midpoint (1.0) with
                        probability Phi(-d/2) = Phi(-1.0) ~= 15.9%, per the
                        standard equal-variance two-Gaussian overlap formula)
    SIGMA   = 1.0
    SEED    = 20260823  (today's date at authoring time, np.random.default_rng)

This is deliberately a PERSISTENT LEVEL SHIFT (a step function once, at the
known real break date), not a transient burst and not a trend -- the same
"regime state persists for months on either side of the break" shape §2.4 of
the real pre-registration argued TFF's weekly cadence was well-suited to
detect. No other structure (autocorrelation, drift, seasonality) is added;
adding any would make this a *less* clean positive control, not a more
realistic one, since the point is to isolate whether the PIPELINE recovers a
known step-change, not whether it is robust to nuisance structure.

Everything downstream of this synthetic series -- the causal rolling-window
classifier, the expanding-causal-median bucket split, the daily label mapping,
the date-correlation check, the per-bucket block construction, and the
cushion-sizing gate-clearance check at k=1 -- is reused by direct import from
`run_orbpos_tff_probe.py` (Implementation A of the real TFF round) and from the
unchanged harness `_imported_run_evalseq_orb_intraday.py`. This script adds NO
new pipeline logic of its own beyond generating the synthetic series and
gluing it into the identical downstream call sequence Implementation A used.
This is intentional: the object under test here is the PIPELINE's own
recovery behavior, not a fourth independent implementation of it.

No parameter above (MU_PRE, MU_POST, SIGMA, SEED, date range) is changed after
this script has been run once. If the result is a REJECT, that is reported as
a finding about the pipeline, not treated as license to re-roll the seed or
widen the separation until a SUPPORTED verdict appears -- doing so would be
exactly the "best-of-K" pattern this repo already has a graveyard for
(`lesson_snag_best_of_k_anchor_graveyard.md`).

$0 / K=0 -- no live network access, no CFTC/TFF/COT data read or referenced by
value anywhere in this file. Writes only to this directory.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _imported_run_evalseq_orb_intraday as H  # noqa: E402  (harness, unchanged)
import run_orbpos_tff_probe as A  # noqa: E402  (Implementation A -- reused pipeline, unchanged)

# ---------------------------------------------------------------------------
# FROZEN SYNTHETIC-DESIGN PARAMETERS (see module docstring -- do not tune post-hoc)
# ---------------------------------------------------------------------------
SYNTH_START = "2020-08-04"   # real TFF classifier's own first available print date
SYNTH_END = "2026-07-15"     # ORB-MNQ-1's own price-panel end (A.PANEL_END)
MU_PRE = 0.0
MU_POST = 2.0
SIGMA = 1.0
SEED = 20260823
COHENS_D = (MU_POST - MU_PRE) / SIGMA

CUTOFF = A.CUTOFF                       # 2021-09-28, identical real break date
WINDOWS = A.WINDOWS                     # {"W1": 4, "W2": 13, "W3": 26}, identical
DATE_CORR_HIGH_FLOOR = A.DATE_CORR_HIGH_FLOOR   # 0.75
DATE_CORR_LOW_CEIL = A.DATE_CORR_LOW_CEIL       # 0.40
MIN_W1_PREBREAK_PRINTS = A.MIN_W1_PREBREAK_PRINTS  # 4
K = A.K                                 # 1


# ============================================================================
# Synthetic series construction (the ONLY new logic in this file)
# ============================================================================

def build_synthetic_tff_like_df() -> pd.DataFrame:
    """Builds a weekly, Tuesday-anchored synthetic classifier DataFrame shaped
    exactly like the real TFF pull's downstream contract: a `report_date`
    column and an `extremity_lf`-equivalent column (named `extremity_lf` here
    too, so it drops into `A.build_classifier` unchanged), plus `available_date`
    via `A.add_publication_lag` reused byte-for-byte."""
    dates = pd.date_range(start=SYNTH_START, end=SYNTH_END, freq="W-TUE")
    assert dates[0] == pd.Timestamp(SYNTH_START), "date grid must start exactly on SYNTH_START"
    assert (dates.weekday == 1).all(), "all synthetic report dates must be Tuesdays (weekday==1)"

    rng = np.random.default_rng(SEED)
    eps = rng.normal(loc=0.0, scale=1.0, size=len(dates))
    mu = np.where(dates < CUTOFF, MU_PRE, MU_POST)
    extremity = mu + SIGMA * eps

    df = pd.DataFrame({"report_date": dates})
    df = A.add_publication_lag(df)  # reused unchanged -- Tuesday snapshot -> Friday publish
    df["extremity_lf"] = extremity
    df["true_regime"] = np.where(dates < CUTOFF, "PRE", "POST")
    return df


# ============================================================================
# main -- identical call sequence to Implementation A's main(), Phase-1 swapped
# ============================================================================

def main():
    t0 = time.time()
    report: dict = {
        "positive_control": True,
        "cutoff": str(CUTOFF.date()),
        "K": K,
        "windows_tff_prints": WINDOWS,
        "min_w1_prebreak_prints_floor": MIN_W1_PREBREAK_PRINTS,
        "synthetic_design": dict(
            start=SYNTH_START, end=SYNTH_END, mu_pre=MU_PRE, mu_post=MU_POST,
            sigma=SIGMA, seed=SEED, cohens_d=COHENS_D,
        ),
    }

    print("=" * 100)
    print("Q-ORBPOS-1 POSITIVE CONTROL -- synthetic two-regime classifier, IDENTICAL pipeline")
    print("=" * 100)
    print(f"  design: N({MU_PRE},{SIGMA}^2) pre-break / N({MU_POST},{SIGMA}^2) post-break, "
          f"Cohen's d={COHENS_D:.2f}, seed={SEED}")
    print(f"  single-draw misclassification rate vs population midpoint (Phi(-d/2)): "
          f"{100 * float(0.5 * (1 + __import__('math').erf(-(COHENS_D / 2) / np.sqrt(2)))):.1f}%")

    # ---------------------------------------------------------------- synthetic Phase 1 (replaces real TFF pull)
    print("\n--- synthetic classifier construction (replaces Phase 1 CFTC pull) ---")
    synth = build_synthetic_tff_like_df()
    print(f"  n_rows={len(synth)}  first report_date={synth['report_date'].min().date()}  "
          f"last report_date={synth['report_date'].max().date()}")
    report["synthetic_pull_equivalent"] = dict(
        n_rows=len(synth), first_report_date=str(synth["report_date"].min().date()),
        last_report_date=str(synth["report_date"].max().date()),
    )

    n_prebreak_prints = int((synth["available_date"] < CUTOFF).sum())
    print(f"  independent synthetic prints available BEFORE the {CUTOFF.date()} break: {n_prebreak_prints}")
    report["n_prebreak_published_prints"] = n_prebreak_prints
    sparsity_trigger_1 = n_prebreak_prints < MIN_W1_PREBREAK_PRINTS
    print(f"  Sec4-equivalent Ambiguous-hold trigger 1 (W1 sparsity, floor={MIN_W1_PREBREAK_PRINTS}): "
          f"{'FIRES' if sparsity_trigger_1 else 'does not fire'}")
    report["ambiguous_hold_trigger_1_prebreak_sparsity"] = bool(sparsity_trigger_1)

    # ---------------------------------------------------------------- data + Control B mirror (reused harness, unchanged)
    print("\n--- ORB-MNQ-1 own panel + Control B mirror (harness reused unchanged) ---")
    inst = H.make_inst()
    panel_pkl = H.resolve_panel()
    df_panel = pd.read_pickle(panel_pkl)
    print(f"  panel: {panel_pkl}")
    print(f"  rows={len(df_panel):,}  span={df_panel['et'].min()} -> {df_panel['et'].max()}")

    piv, meta = H.ol.session_panel(df_panel, inst)
    bt = H.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"  Control B PASS -- n={len(recon)} triggering days  "
          f"recon date span {recon['date'].min().date()} -> {recon['date'].max().date()}")
    report["n_triggering_days"] = len(recon)

    thr = H.load_scoring_thresholds()
    print(f"\n[gate ] {thr.source_path}")
    print(f"[gate ] horizon={thr.horizon}  seeds={thr.seeds}  sims/seed={thr.sims_per_seed}  "
          f"eval_bust_ceiling={thr.eval_bust_ceiling:.1%}  pass_floor={thr.pass_floor:.0%}")
    report["gate_thresholds"] = dict(eval_bust_ceiling_pct=thr.eval_bust_ceiling * 100.0,
                                      pass_floor_pct=thr.pass_floor * 100.0, horizon=thr.horizon,
                                      seeds=list(thr.seeds), sims_per_seed=thr.sims_per_seed)

    H.assert_engine_ready(H.TIER)
    fkw_base = H.firm_kwargs(H.TIER, inactivity_off=True, consistency=H.CONSISTENCY_FRAC)
    if fkw_base["dd_lock_offset_usd"] == H.LOCK_AS_PUBLISHED:
        fkw = dict(fkw_base, dd_lock_offset_usd=H.LOCK_UNREACHABLE)
        print("[firm ] FIRM_RULES still ships the as-published lock; overriding to unreachable (matches published headline).")
    else:
        fkw = dict(fkw_base)
        print(f"[firm ] FIRM_RULES already ships dd_lock_offset_usd={fkw_base['dd_lock_offset_usd']:,.0f} (no override needed).")
    assert fkw["profit_target"] == H.TARGET
    assert fkw["starting_equity"] == H.START
    assert fkw["trailing_dd_pct"] == -H.DD / H.START

    # ---------------------------------------------------------------- fidelity control (reused harness, unchanged)
    print("\n--- FIDELITY CONTROL: flat policy, m=1.0, full panel, k=1/k=2 (reused day_loop_intraday) ---")
    PUBLISHED = {1: 67.67, 2: 77.01}
    TOL_PP = 2.0
    control = {}
    flat_ok_k1 = True
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
        print(f"  k={k}  bust={r['bust_pct']:.2f}%  pass={r['pass_pct']:.2f}%  published={PUBLISHED[k]:.2f}%  "
              f"delta={delta:+.2f}pp  {'PASS' if ok else 'FAIL'}  (elapsed {time.time()-t0:.0f}s)")
    report["fidelity_control"] = control
    report["fidelity_control_pass_k1"] = bool(flat_ok_k1)
    if not flat_ok_k1:
        print("\nSTOPPING -- fidelity control at k=1 did not reproduce the published intraday-honest bust "
              "rate within tolerance. Not proceeding to the synthetic classifier on an unvalidated harness.")
        (HERE / "results_orbpos_positive_control.json").write_text(json.dumps(report, indent=2, default=str))
        return 2

    # ---------------------------------------------------------------- Phase 2 (reused A.* functions, unchanged): classifier + gate, per window
    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    panel_full_k1 = H.build_k_panel(recon, K)
    print(f"\n[panel] business-day span: {full_idx[0].date()} -> {full_idx[-1].date()}  n_days={len(full_idx)}")

    windows_report = {}
    for wname, wsize in WINDOWS.items():
        print("\n" + "=" * 100)
        print(f"{wname} -- rolling window = {wsize} synthetic weekly prints")
        print("=" * 100)

        clf = A.build_classifier(synth, wsize)
        print(f"[classifier] n_prints_total={len(synth)}  WARMUP={clf['n_warmup']}  "
              f"HIGHER={clf['n_higher']}  LOWER={clf['n_lower']}  "
              f"expanding-median spot-check ({clf['n_spot_checked']} pts): "
              f"{'PASS' if clf['spotcheck_pass'] else 'FAIL'}  "
              f"degenerate-threshold: {'YES' if clf['degenerate_threshold'] else 'no'}")

        daily_label = A.daily_label_from_weekly(synth, clf["label"], full_idx)
        dc = A.date_correlation(daily_label)
        print(f"[date-corr] HIGHER bucket: n_days={dc['n_higher_days']}  "
              f"post-cutoff frac={dc['frac_higher_days_post_cutoff']:.1%}  (need >= {DATE_CORR_HIGH_FLOOR:.0%})")
        print(f"[date-corr] LOWER  bucket: n_days={dc['n_lower_days']}  "
              f"post-cutoff frac={dc['frac_lower_days_post_cutoff']:.1%}  (need <= {DATE_CORR_LOW_CEIL:.0%})")
        print(f"[date-corr] window condition: {'FIRES (pass)' if dc['date_corr_pass'] else 'does not fire (fail)'}")

        gate_higher = A.gate_check_bucket(panel_full_k1, daily_label, "HIGHER", thr, fkw)
        gate_lower = A.gate_check_bucket(panel_full_k1, daily_label, "LOWER", thr, fkw)
        print(f"[gate] HIGHER  n_blocks={gate_higher['meta']['n_blocks']}  "
              f"flat: bust={gate_higher['flat']['bust_pct']:.2f}% pass={gate_higher['flat']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['flat']['gate_pass'] else 'FAIL'}  |  "
              f"cushion: bust={gate_higher['cushion']['bust_pct']:.2f}% pass={gate_higher['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['cushion']['gate_pass'] else 'FAIL'}")
        print(f"[gate] LOWER   n_blocks={gate_lower['meta']['n_blocks']}  "
              f"flat: bust={gate_lower['flat']['bust_pct']:.2f}% pass={gate_lower['flat']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['flat']['gate_pass'] else 'FAIL'}  |  "
              f"cushion: bust={gate_lower['cushion']['bust_pct']:.2f}% pass={gate_lower['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['cushion']['gate_pass'] else 'FAIL'}   (elapsed {time.time()-t0:.0f}s)")

        direction = A.classify_direction(gate_higher, gate_lower)
        print(f"[direction] {wname}: {direction}")

        windows_report[wname] = dict(
            window_prints=wsize,
            classifier=dict(n_prints_total=len(synth), n_warmup=clf["n_warmup"], n_higher=clf["n_higher"],
                             n_lower=clf["n_lower"], spotcheck_pass=clf["spotcheck_pass"],
                             degenerate_threshold=clf["degenerate_threshold"]),
            date_correlation=dc,
            gate={"HIGHER": gate_higher, "LOWER": gate_lower},
            direction=direction,
        )

    report["windows"] = windows_report

    # ---------------------------------------------------------------- verdict assertion (identical Sec4/Sec6-shaped logic)
    n_date_corr_pass = sum(1 for w in windows_report.values() if w["date_correlation"]["date_corr_pass"])
    directions = [w["direction"] for w in windows_report.values()]
    signed_directions = {d for d in directions if d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT")}
    direction_same_sign_every_window = (
        len(signed_directions) == 1 and all(d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT") for d in directions)
    )
    any_w1_ambiguous = sparsity_trigger_1 or windows_report["W1"]["classifier"]["degenerate_threshold"]

    if any_w1_ambiguous:
        verdict = "AMBIGUOUS-HOLD"
    elif (n_date_corr_pass >= 2) and direction_same_sign_every_window:
        verdict = "ACCEPT (pipeline RECOVERS the known synthetic relationship)"
    else:
        verdict = "REJECT (pipeline FAILS to recover the known synthetic relationship)"

    report["summary"] = dict(
        date_correlation_windows_passing=n_date_corr_pass,
        date_correlation_fires_at_ge2_of_3=bool(n_date_corr_pass >= 2),
        directions_by_window={wn: w["direction"] for wn, w in windows_report.items()},
        direction_same_sign_every_window=bool(direction_same_sign_every_window),
        w1_ambiguous_hold_fired=bool(any_w1_ambiguous),
        verdict=verdict,
    )

    print("\n" + "=" * 100)
    print("POSITIVE-CONTROL VERDICT (same Accept/Reject shape as H-ORBPOS's own §4)")
    print("=" * 100)
    print(f"  date-correlation clears (a)/(b) at >=2 of 3 windows?  {n_date_corr_pass}/3  -> "
          f"{'YES' if n_date_corr_pass >= 2 else 'NO'}")
    print(f"  gate-clearance direction same sign at every window, no exceptions?  "
          f"{'YES' if direction_same_sign_every_window else 'NO'}  (per-window: {report['summary']['directions_by_window']})")
    print(f"  Ambiguous-hold-equivalent (W1 sparsity or degenerate threshold)?  {'FIRES' if any_w1_ambiguous else 'does not fire'}")
    print(f"\n  ==> POSITIVE CONTROL: {verdict}")

    out = HERE / "results_orbpos_positive_control.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
