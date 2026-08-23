#!/usr/bin/env python3
"""Q-ORBPOS-1 POSITIVE CONTROL v2 -- CORRECTED bucket-construction method.

Frozen design: POSITIVE_CONTROL_METHOD_FIX.md sections 2-3, written and
committed BEFORE this file was run. Do not change ASSOC_ALPHA,
MIN_SEPARATION_PP, the anchored-threshold construction, or the synthetic
design parameters after seeing a result -- see that document's §3f.

Two things are reused byte-for-byte from the existing, already-verified
pipeline (no new pipeline logic beyond the anchored threshold + print-level
association test):
  - `_imported_run_evalseq_orb_intraday.py` (harness: panel, MC engine, gate
    thresholds, firm rules) -- imported as H, unchanged.
  - `run_orbpos_tff_probe.py` (Implementation A's reused pieces:
    add_publication_lag, daily_label_from_weekly, blocks_for_label,
    gate_check_bucket, classify_direction, CUTOFF, WINDOWS,
    MIN_W1_PREBREAK_PRINTS, K) -- imported as A, unchanged.

New in this file: `build_classifier_anchored` (the frozen-post-break-threshold
construction) and `print_level_association` (the Fisher's-exact +
separation-floor pass/fail criterion + supplementary point-biserial
correlation), plus a synthetic-series generator parameterized so the SAME
corrected pipeline can be run on both the primary d=2.0 design and a new
pure-noise (Type-I sanity) variant in one execution.

$0 / K=0 -- no real economic/positioning/price-external data used or
referenced by value anywhere in this file. Writes only to this directory.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import _imported_run_evalseq_orb_intraday as H  # noqa: E402  (harness, unchanged)
import run_orbpos_tff_probe as A  # noqa: E402  (Implementation A -- reused pipeline pieces, unchanged)

# ---------------------------------------------------------------------------
# FROZEN PARAMETERS -- see POSITIVE_CONTROL_METHOD_FIX.md §3 for full design
# reasoning. Committed before this script was run; not tuned after seeing
# results.
# ---------------------------------------------------------------------------
SYNTH_START = "2020-08-04"
SYNTH_END = "2026-07-15"
CUTOFF = A.CUTOFF
WINDOWS = A.WINDOWS
MIN_W1_PREBREAK_PRINTS = A.MIN_W1_PREBREAK_PRINTS
K = A.K

# primary (positive-control) synthetic design -- IDENTICAL to POSITIVE_CONTROL.md
MU_PRE = 0.0
MU_POST = 2.0
SIGMA = 1.0
SEED = 20260823
COHENS_D = (MU_POST - MU_PRE) / SIGMA

# Type-I / null sanity-check design (bonus, new) -- pure noise, no true
# regime difference. Seed is a deterministic +1 increment of the already-
# frozen primary seed -- not searched, not chosen after looking at a result.
SEED_NULL = SEED + 1
MU_PRE_NULL = 0.0
MU_POST_NULL = 0.0

# corrected pass/fail criterion (replaces DATE_CORR_HIGH_FLOOR/LOW_CEIL)
ASSOC_ALPHA = 0.01
MIN_SEPARATION_PP = 0.35


# ============================================================================
# Synthetic series construction (parameterized version of the original
# build_synthetic_tff_like_df, so the same corrected pipeline can be run on
# both the primary design and the null variant in one execution)
# ============================================================================

def build_synthetic_df(mu_pre: float, mu_post: float, sigma: float, seed: int) -> pd.DataFrame:
    dates = pd.date_range(start=SYNTH_START, end=SYNTH_END, freq="W-TUE")
    assert dates[0] == pd.Timestamp(SYNTH_START), "date grid must start exactly on SYNTH_START"
    assert (dates.weekday == 1).all(), "all synthetic report dates must be Tuesdays (weekday==1)"

    rng = np.random.default_rng(seed)
    eps = rng.normal(loc=0.0, scale=1.0, size=len(dates))
    mu = np.where(dates < CUTOFF, mu_pre, mu_post)
    extremity = mu + sigma * eps

    df = pd.DataFrame({"report_date": dates})
    df = A.add_publication_lag(df)  # reused unchanged
    df["extremity_lf"] = extremity
    df["true_regime"] = np.where(dates < CUTOFF, "PRE", "POST")
    return df


# ============================================================================
# NEW: anchored (frozen-post-break) causal threshold classifier
# ============================================================================

def build_classifier_anchored(df: pd.DataFrame, window: int) -> dict:
    """Same roll_W construction as A.build_classifier. Threshold differs only
    in HOW it is aggregated over time: for prints with available_date <
    CUTOFF, identical expanding-causal median to the original A.build_classifier
    (byte-identical computation). For prints with available_date >= CUTOFF,
    the threshold is FROZEN at the value the expanding median had already
    reached at the last valid pre-break print -- never updated further. See
    POSITIVE_CONTROL_METHOD_FIX.md §3a for the causal argument."""
    extremity = df["extremity_lf"]
    roll_W = extremity.rolling(window, min_periods=window).mean()
    running_median = roll_W.expanding(min_periods=1).median()
    valid = roll_W.notna()

    pre_mask = (df["available_date"] < CUTOFF).to_numpy()
    valid_np = valid.to_numpy()
    pre_valid_positions = np.flatnonzero(pre_mask & valid_np)

    threshold = running_median.copy()
    if len(pre_valid_positions) == 0:
        # No valid pre-break print under this window at all -- degenerate
        # input; fall back to the pure expanding median so the Ambiguous-hold
        # sparsity trigger (not a crash) is what reports this upstream.
        i_freeze = None
        frozen_value = None
    else:
        i_freeze = int(pre_valid_positions[-1])
        frozen_value = float(running_median.iloc[i_freeze])
        post_mask = ~pre_mask
        threshold[post_mask] = frozen_value

    label = pd.Series("WARMUP", index=df.index)
    label[valid & (roll_W > threshold)] = "HIGHER"
    label[valid & (roll_W <= threshold)] = "LOWER"

    # Independent spot-check of the PRE-break segment's expanding median
    # (identical mechanic/discipline to A.build_classifier's own spot-check;
    # the post-break segment is deliberately constant, nothing to spot-check
    # there beyond confirming it equals frozen_value everywhere).
    valid_pos_pre = pre_valid_positions
    spot_pos = valid_pos_pre[:: max(1, len(valid_pos_pre) // 5)][:5] if len(valid_pos_pre) else np.array([], dtype=int)
    spot_ok = True
    for pos in spot_pos:
        seen = roll_W.to_numpy()[: pos + 1]
        seen_valid = seen[~np.isnan(seen)]
        expect = float(np.median(seen_valid))
        got = float(running_median.iloc[pos])
        if not np.isclose(expect, got, rtol=1e-9, atol=1e-9):
            spot_ok = False
    post_mask_np = ~pre_mask
    post_valid_thresholds = threshold[valid & pd.Series(post_mask_np, index=df.index)].to_numpy()
    freeze_ok = bool(
        frozen_value is None
        or len(post_valid_thresholds) == 0
        or np.allclose(post_valid_thresholds, frozen_value, rtol=1e-9, atol=1e-9)
    )

    # Degenerate-threshold check restricted to the PRE-break segment only --
    # the post-break segment is INTENTIONALLY constant under this design
    # (that is the fix, not a defect), so checking degeneracy across the
    # whole series would always spuriously fire.
    pre_medians = threshold[valid & pd.Series(pre_mask, index=df.index)].to_numpy()
    degenerate_pre = bool(len(pre_medians) > 0 and float(np.nanstd(pre_medians)) == 0.0)

    return dict(
        window=window, roll_W=roll_W, threshold=threshold, label=label, valid=valid,
        i_freeze=i_freeze, frozen_value=frozen_value,
        spotcheck_pass=bool(spot_ok and freeze_ok), n_spot_checked=int(len(spot_pos)),
        n_warmup=int((label == "WARMUP").sum()), n_higher=int((label == "HIGHER").sum()),
        n_lower=int((label == "LOWER").sum()), degenerate_threshold=degenerate_pre,
    )


# ============================================================================
# NEW: print-level, base-rate-aware association test (replaces A.date_correlation)
# ============================================================================

def print_level_association(df: pd.DataFrame, label: pd.Series, roll_W: pd.Series) -> dict:
    """Print-level (not day-level ffill'd -- avoids pseudoreplication) 2x2
    test: label(HIGHER/LOWER) x era(PRE/POST). Replaces A.date_correlation's
    fixed 75%/40% day-level thresholds with a Fisher's-exact test +
    minimum-separation floor (POSITIVE_CONTROL_METHOD_FIX.md §3b), plus a
    supplementary (non-gating) point-biserial correlation (§3c)."""
    era_post = (df["available_date"] >= CUTOFF).to_numpy()
    lab = label.to_numpy()
    higher = lab == "HIGHER"
    lower = lab == "LOWER"

    n_higher = int(higher.sum())
    n_lower = int(lower.sum())
    if n_higher == 0 or n_lower == 0:
        return dict(
            n_higher=n_higher, n_lower=n_lower,
            frac_higher_post=float("nan"), frac_lower_post=float("nan"),
            fisher_p=float("nan"), separation_pp=float("nan"),
            point_biserial_r=float("nan"), point_biserial_p=float("nan"),
            corrected_pass=False,
        )

    frac_higher_post = float(era_post[higher].mean())
    frac_lower_post = float(era_post[lower].mean())
    n11 = int((higher & era_post).sum())
    n10 = int((higher & ~era_post).sum())
    n01 = int((lower & era_post).sum())
    n00 = int((lower & ~era_post).sum())
    table = [[n11, n10], [n01, n00]]
    _, fisher_p = stats.fisher_exact(table, alternative="two-sided")

    valid_mask = label.isin(["HIGHER", "LOWER"]).to_numpy()
    roll_vals = roll_W.to_numpy()[valid_mask]
    era_vals = era_post[valid_mask].astype(float)
    if len(np.unique(era_vals)) < 2 or np.nanstd(roll_vals) == 0:
        pb_r, pb_p = float("nan"), float("nan")
    else:
        pb_r, pb_p = stats.pointbiserialr(era_vals, roll_vals)

    separation = frac_higher_post - frac_lower_post
    corrected_pass = bool(fisher_p < ASSOC_ALPHA and separation >= MIN_SEPARATION_PP)

    return dict(
        n_higher=n_higher, n_lower=n_lower,
        frac_higher_post=frac_higher_post, frac_lower_post=frac_lower_post,
        contingency_table=dict(higher_post=n11, higher_pre=n10, lower_post=n01, lower_pre=n00),
        fisher_p=float(fisher_p), separation_pp=float(separation),
        point_biserial_r=float(pb_r), point_biserial_p=float(pb_p),
        corrected_pass=corrected_pass,
    )


def ground_truth_accuracy(df: pd.DataFrame, label: pd.Series) -> dict:
    """Optional cross-check (not gating): print-level label-vs-known-synthetic-
    regime accuracy, split by true era -- mirrors POSITIVE_CONTROL.md §3a's
    diagnostic table, for the corrected classifier."""
    truth = df["true_regime"].to_numpy()
    lab = label.to_numpy()
    non_warmup = lab != "WARMUP"
    pre = non_warmup & (truth == "PRE")
    post = non_warmup & (truth == "POST")
    pre_correct = int((lab[pre] == "LOWER").sum())
    post_correct = int((lab[post] == "HIGHER").sum())
    overall_correct = pre_correct + post_correct
    n_pre, n_post = int(pre.sum()), int(post.sum())
    n_total = n_pre + n_post
    return dict(
        n_total=n_total, overall_accuracy=(overall_correct / n_total if n_total else float("nan")),
        n_pre=n_pre, pre_correct=pre_correct,
        pre_accuracy=(pre_correct / n_pre if n_pre else float("nan")),
        n_post=n_post, post_correct=post_correct,
        post_accuracy=(post_correct / n_post if n_post else float("nan")),
    )


# ============================================================================
# One full corrected-pipeline pass over a synthetic design variant
# ============================================================================

def run_variant(name: str, mu_pre: float, mu_post: float, sigma: float, seed: int,
                 full_idx: pd.DatetimeIndex, panel_full_k1: pd.DataFrame, thr, fkw,
                 t0: float) -> dict:
    print("\n" + "#" * 100)
    print(f"VARIANT: {name}  (mu_pre={mu_pre}, mu_post={mu_post}, sigma={sigma}, seed={seed}, "
          f"Cohen's d={(mu_post - mu_pre) / sigma:.2f})")
    print("#" * 100)

    synth = build_synthetic_df(mu_pre, mu_post, sigma, seed)
    n_prebreak_prints = int((synth["available_date"] < CUTOFF).sum())
    sparsity_trigger_1 = n_prebreak_prints < MIN_W1_PREBREAK_PRINTS
    print(f"  n_rows={len(synth)}  n_prebreak_prints={n_prebreak_prints}  "
          f"sparsity_trigger={'FIRES' if sparsity_trigger_1 else 'no'}")

    windows_report = {}
    for wname, wsize in WINDOWS.items():
        print(f"\n--- {wname} (window={wsize} prints) ---")
        clf = build_classifier_anchored(synth, wsize)
        print(f"  [classifier] WARMUP={clf['n_warmup']} HIGHER={clf['n_higher']} LOWER={clf['n_lower']} "
              f"i_freeze={clf['i_freeze']} frozen_value={clf['frozen_value']:.4f} "
              f"spotcheck={'PASS' if clf['spotcheck_pass'] else 'FAIL'} "
              f"degenerate_pre={'YES' if clf['degenerate_threshold'] else 'no'}")

        assoc = print_level_association(synth, clf["label"], clf["roll_W"])
        print(f"  [assoc] n_higher={assoc['n_higher']} n_lower={assoc['n_lower']} "
              f"frac_higher_post={assoc['frac_higher_post']:.1%} frac_lower_post={assoc['frac_lower_post']:.1%} "
              f"separation={assoc['separation_pp']:+.1%} fisher_p={assoc['fisher_p']:.3g} "
              f"point_biserial_r={assoc['point_biserial_r']:.3f} (p={assoc['point_biserial_p']:.3g}) "
              f"corrected_pass={'YES' if assoc['corrected_pass'] else 'NO'}")

        gt = ground_truth_accuracy(synth, clf["label"])
        print(f"  [ground-truth] overall={gt['overall_accuracy']:.1%} "
              f"pre_correct(LOWER)={gt['pre_accuracy']:.1%} (n={gt['n_pre']}) "
              f"post_correct(HIGHER)={gt['post_accuracy']:.1%} (n={gt['n_post']})")

        daily_label = A.daily_label_from_weekly(synth, clf["label"], full_idx)
        gate_higher = A.gate_check_bucket(panel_full_k1, daily_label, "HIGHER", thr, fkw)
        gate_lower = A.gate_check_bucket(panel_full_k1, daily_label, "LOWER", thr, fkw)
        direction = A.classify_direction(gate_higher, gate_lower)
        print(f"  [gate] HIGHER cushion pass={gate_higher['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_higher['cushion']['gate_pass'] else 'FAIL'}  |  "
              f"LOWER cushion pass={gate_lower['cushion']['pass_pct']:.2f}% "
              f"gate={'PASS' if gate_lower['cushion']['gate_pass'] else 'FAIL'}  "
              f"direction={direction}  (elapsed {time.time()-t0:.0f}s)")

        windows_report[wname] = dict(
            window_prints=wsize,
            classifier=dict(n_warmup=clf["n_warmup"], n_higher=clf["n_higher"], n_lower=clf["n_lower"],
                             i_freeze=clf["i_freeze"], frozen_value=clf["frozen_value"],
                             spotcheck_pass=clf["spotcheck_pass"], degenerate_threshold=clf["degenerate_threshold"]),
            association=assoc,
            ground_truth_accuracy=gt,
            gate={"HIGHER": gate_higher, "LOWER": gate_lower},
            direction=direction,
        )

    n_corrected_pass = sum(1 for w in windows_report.values() if w["association"]["corrected_pass"])
    directions = [w["direction"] for w in windows_report.values()]
    signed_directions = {d for d in directions if d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT")}
    direction_same_sign_every_window = (
        len(signed_directions) == 1 and all(d in ("HIGHER_CLEARS_LOWER_DOES_NOT", "LOWER_CLEARS_HIGHER_DOES_NOT") for d in directions)
    )
    any_w1_ambiguous = sparsity_trigger_1 or windows_report["W1"]["classifier"]["degenerate_threshold"]

    if any_w1_ambiguous:
        verdict = "AMBIGUOUS-HOLD"
    elif (n_corrected_pass >= 2) and direction_same_sign_every_window:
        verdict = "ACCEPT (corrected method RECOVERS the relationship)"
    else:
        verdict = "REJECT (corrected method does NOT recover the relationship)"

    summary = dict(
        n_prebreak_published_prints=n_prebreak_prints,
        sparsity_trigger_1=bool(sparsity_trigger_1),
        corrected_association_windows_passing=n_corrected_pass,
        corrected_association_fires_at_ge2_of_3=bool(n_corrected_pass >= 2),
        directions_by_window={wn: w["direction"] for wn, w in windows_report.items()},
        direction_same_sign_every_window=bool(direction_same_sign_every_window),
        w1_ambiguous_hold_fired=bool(any_w1_ambiguous),
        verdict=verdict,
    )
    print(f"\n  ==> {name} VERDICT: {verdict}")
    print(f"      corrected association clears >=2/3?  {n_corrected_pass}/3")
    print(f"      direction same sign every window?  {direction_same_sign_every_window}  ({summary['directions_by_window']})")

    return dict(
        design=dict(mu_pre=mu_pre, mu_post=mu_post, sigma=sigma, seed=seed,
                    cohens_d=(mu_post - mu_pre) / sigma),
        n_rows=len(synth), windows=windows_report, summary=summary,
    )


# ============================================================================
# main
# ============================================================================

def main():
    t0 = time.time()
    report: dict = {
        "corrected_method": True,
        "cutoff": str(CUTOFF.date()),
        "K": K,
        "windows_tff_prints": WINDOWS,
        "assoc_alpha": ASSOC_ALPHA,
        "min_separation_pp": MIN_SEPARATION_PP,
    }

    print("=" * 100)
    print("Q-ORBPOS-1 POSITIVE CONTROL v2 -- CORRECTED (anchored-threshold) bucket construction")
    print("=" * 100)

    # ---------------------------------------------------------------- harness + panel (reused unchanged)
    inst = H.make_inst()
    panel_pkl = H.resolve_panel()
    df_panel = pd.read_pickle(panel_pkl)
    piv, meta = H.ol.session_panel(df_panel, inst)
    bt = H.ol.orb_backtest(piv, meta, inst, or_bars=2)
    recon = H.orb_days_with_excursion(piv, meta, inst, entry_bar="include")
    H.assert_mirror_matches_engine(recon, bt)
    print(f"Control B PASS -- n={len(recon)} triggering days  "
          f"recon date span {recon['date'].min().date()} -> {recon['date'].max().date()}")

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
        print(f"  k={k}  bust={r['bust_pct']:.2f}%  published={PUBLISHED[k]:.2f}%  "
              f"delta={delta:+.2f}pp  {'PASS' if ok else 'FAIL'}")
    report["fidelity_control"] = control
    report["fidelity_control_pass_k1"] = bool(flat_ok_k1)
    if not flat_ok_k1:
        print("\nSTOPPING -- fidelity control did not reproduce published bust rate. Not proceeding.")
        (HERE / "results_orbpos_positive_control_v2_anchored.json").write_text(json.dumps(report, indent=2, default=str))
        return 2

    full_idx = pd.bdate_range(recon["date"].min(), recon["date"].max())
    panel_full_k1 = H.build_k_panel(recon, K)

    # ---------------------------------------------------------------- primary positive-control variant
    report["positive_control"] = run_variant(
        "PRIMARY (d=2.00 positive control)", MU_PRE, MU_POST, SIGMA, SEED,
        full_idx, panel_full_k1, thr, fkw, t0,
    )

    # ---------------------------------------------------------------- bonus Type-I / null variant
    report["null_check"] = run_variant(
        "BONUS Type-I check (pure noise, mu_pre=mu_post=0)", MU_PRE_NULL, MU_POST_NULL, SIGMA, SEED_NULL,
        full_idx, panel_full_k1, thr, fkw, t0,
    )

    print("\n" + "=" * 100)
    print("FINAL SUMMARY")
    print("=" * 100)
    print(f"  PRIMARY (d=2.0)   verdict: {report['positive_control']['summary']['verdict']}")
    print(f"  NULL (d=0.0)      verdict: {report['null_check']['summary']['verdict']}")

    out = HERE / "results_orbpos_positive_control_v2_anchored.json"
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"\n[write] {out}")
    print(f"[time ] total elapsed {time.time()-t0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
