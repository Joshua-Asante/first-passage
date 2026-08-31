"""Presence battery (L1-L3) for Q-RANGEXFER-1's five hypotheses.

Rule 0: read before writing this script --
  lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/candidate1_range_persistence.py
    (frozen source of L1/L2/L3's own mechanics: L1 = n_scored>=N_FLOOR_POP AND
    n_cond>=N_FLOOR_COND; L2 = block-bootstrap CI lower bound > threshold; L3 =
    BOTH chronological halves of the scored panel individually clear the same
    threshold. Candidate 1's own L3 orders the CONDITIONAL (predictor==1) rows
    chronologically and checks each half's outcome RATE > 0.50 -- a single-series
    rate-vs-baseline test. This construct's own statistic is a LIFT (hi-rate minus
    lo-rate across a predictor split, or the min of two such lifts across
    bias_dayhist strata for the two parent hypotheses) -- there is no single-group
    "rate vs 0.50" analogue. Adopted interpretation, disclosed for review: L3 here
    splits the SCORED PANEL (all rows entering that hypothesis's own lift
    statistic, already restricted per the hypothesis -- see RESTRICTIONS below)
    chronologically at the midpoint by trading_day, then recomputes that
    hypothesis's own lift statistic (min-stratified for the two parents; a single
    hi-lo lift for the three restricted hypotheses) independently within each
    half. This is the natural generalization of "does the effect hold up in both
    halves of history" to a two-group-difference statistic and is flagged here as
    an interpretive judgment call, not a frozen-text-literal instruction --
    candidate1's own halves convention does not transfer verbatim to an S2-shaped
    two-series lift design (the same class of non-transfer PR #224 already found
    once on this exact panel, see byyear_l4.py's own finding 4).
  docs/briefs/pre-registration/Q-RANGEXFER-1-verdict-preregistration.md SSA/SSB/SSF/SSG
    (frozen constants and limb definitions this script implements verbatim: L1
    N_FLOOR_POP=400/N_FLOOR_COND=100; L2 block-bootstrap CI lower bound on the
    minimum stratified incremental lift > 0, block=20 trading days, draws=4000,
    seed=42 -- NOTE this diverges from every existing exploratory script's own ad
    hoc bootstrap seed/block (c2_c4_stratified_rerun.py used block=60,
    seed=20260829; candidate24_joint_gate.py's block_bootstrap_p used seed=100+s
    etc.) -- those are NOT the frozen L2 construction and are not reused here; L3
    both chronological halves lift>0).
  lab/analysis/_inbox/rangexfer_byyear_l4_2026-08-30/byyear_l4.py
    (the exact per-hypothesis panel-restriction convention this script reuses
    verbatim -- confirmed by that script's own docstring to reproduce the brief's
    cited pooled figures exactly; RESTRICTIONS below mirror its five branches).
  docs/briefs/Q-RANGEXFER-1-overnight-range-gap-magnitude-transfer.md SS0/SS4/SS6
    (per-hypothesis "already measured" figures used as a pooled-statistic
    cross-check before trusting this script's own restriction logic).

RESTRICTIONS (mirrors byyear_l4.py exactly):
  H-RANGEXFER-1        MNQ candidate24_joint_frame.csv, full panel, predictor=bias_overnight,
                        stratify_by=bias_dayhist (min-stratified lift, two populated strata)
  H-RANGEXFER-1.a       MNQ frame restricted to bias_overnight==0 (overnight-calm),
                        predictor=bias_gap (single hi-lo lift, no further stratification --
                        PR #224 finding 4 explicitly investigated and rejected further
                        day-history stratification here as computing a different, uncited
                        statistic)
  H-RANGEXFER-1-MYM     MYM c24_joint_frame.csv, full panel, predictor=bias_overnight,
                        stratify_by=bias_dayhist
  H-RANGEXFER-1.a-MYM   MYM frame restricted to bias_overnight==0, predictor=bias_gap
  H-RANGEXFER-1.b-MYM   MYM frame restricted to bias_dayhist==0 (bprime=0), predictor=bias_gap

Environment precondition (Codex PR #226 finding 4 on the sibling closure-path
plan): this script runs on the git-tracked cached joint frames only (no vendor
bars needed) -- same data source byyear_l4.py already used and pooled-figure
verified. The MYM cache is 1,304 rows (three days shorter than the frozen
1,307-day panel candidate2/4's original bootstrap ran on -- MYM_M15.csv is
present and hash-verified in THIS worktree this session, but this script does
not rebuild from it; it reads the committed cache to stay directly comparable
to byyear_l4.py's own L4 figures, which used the same cache). Disclosed, not
silently assumed away.

No K spent: re-derives L1-L3 from already-scored, already-cited panels: no
fresh look at real outcome data beyond what the brief's own pooled figures
already used.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
MNQ_FRAME = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"
MYM_FRAME = HERE.parent / "mym_mechanism_harvest_2026-08-29" / "c24_joint_frame.csv"

# Frozen constants (pre-registration SSA / SSF.1 / SSG.1 -- verbatim, not re-tuned).
N_FLOOR_POP = 400
N_FLOOR_COND = 100
CI_BLOCK = 20      # trading days
CI_DRAWS = 4000
CI_SEED = 42


def _year_free_chrono_halves(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ordered = df.sort_values("trading_day").reset_index(drop=True)
    h = len(ordered) // 2
    return ordered.iloc[:h], ordered.iloc[h:]


def _single_lift(df: pd.DataFrame, predictor: str, outcome: str = "y") -> tuple[float | None, int, int]:
    hi = df.loc[df[predictor] == 1, outcome]
    lo = df.loc[df[predictor] == 0, outcome]
    if len(hi) == 0 or len(lo) == 0:
        return None, len(hi), len(lo)
    return float(hi.mean() - lo.mean()), len(hi), len(lo)


def _min_stratified_lift(df: pd.DataFrame, predictor: str, stratify_by: str,
                          outcome: str = "y") -> tuple[float | None, dict]:
    lifts = {}
    n_cond_by_stratum = {}
    for s in sorted(df[stratify_by].unique()):
        sub = df[df[stratify_by] == s]
        lift, n_hi, n_lo = _single_lift(sub, predictor, outcome)
        if lift is not None:
            lifts[int(s)] = lift
            n_cond_by_stratum[int(s)] = n_hi
    if not lifts:
        return None, n_cond_by_stratum
    return min(lifts.values()), n_cond_by_stratum


def _block_bootstrap_ci_single(df: pd.DataFrame, predictor: str, outcome: str,
                                block: int, draws: int, seed: int) -> tuple[float, float, float, int]:
    """Circular day-block bootstrap CI on the single hi-lo lift statistic.
    Resamples (predictor, outcome) pairs jointly as contiguous chronological
    blocks with replacement -- same scheme as every existing exploratory
    script's own block-bootstrap, but at the FROZEN pre-registration
    block/draws/seed, not any script's own ad hoc choice."""
    ordered = df.sort_values("trading_day").reset_index(drop=True)
    pred = ordered[predictor].to_numpy()
    out = ordered[outcome].to_numpy()
    n = len(ordered)
    rng = np.random.default_rng(seed)
    nblocks = int(np.ceil(n / block))
    vals = []
    for _ in range(draws):
        st = rng.integers(0, n, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % n
        idx = idx.ravel()[:n]
        p, o = pred[idx], out[idx]
        hi_mask, lo_mask = p == 1, p == 0
        if hi_mask.any() and lo_mask.any():
            vals.append(float(o[hi_mask].mean() - o[lo_mask].mean()))
    vals = np.asarray(vals)
    lo_ci, hi_ci = np.percentile(vals, [2.5, 97.5])
    return float(lo_ci), float(hi_ci), float(vals.mean()), int(len(vals))


def _block_bootstrap_ci_min_stratified(df: pd.DataFrame, predictor: str, stratify_by: str,
                                        outcome: str, block: int, draws: int,
                                        seed: int) -> tuple[float, float, float, int]:
    """Same resampling scheme as _block_bootstrap_ci_single, but the resampled
    statistic per draw is the MIN across stratify_by strata (matching
    min_stratified_lift's own definition), so the CI is on the same statistic
    L4 and the brief's own pooled figures cite -- not the CI of a single
    stratum."""
    ordered = df.sort_values("trading_day").reset_index(drop=True)
    pred = ordered[predictor].to_numpy()
    out = ordered[outcome].to_numpy()
    strat = ordered[stratify_by].to_numpy()
    n = len(ordered)
    rng = np.random.default_rng(seed)
    nblocks = int(np.ceil(n / block))
    vals = []
    strata_vals = sorted(np.unique(strat).tolist())
    for _ in range(draws):
        st = rng.integers(0, n, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % n
        idx = idx.ravel()[:n]
        p, o, s = pred[idx], out[idx], strat[idx]
        lifts = []
        for sv in strata_vals:
            m = s == sv
            hi_mask, lo_mask = m & (p == 1), m & (p == 0)
            if hi_mask.any() and lo_mask.any():
                lifts.append(float(o[hi_mask].mean() - o[lo_mask].mean()))
        if lifts:
            vals.append(min(lifts))
    vals = np.asarray(vals)
    lo_ci, hi_ci = np.percentile(vals, [2.5, 97.5])
    return float(lo_ci), float(hi_ci), float(vals.mean()), int(len(vals))


def evaluate_parent(label: str, df: pd.DataFrame, predictor: str, stratify_by: str) -> dict:
    n_scored = len(df)
    obs_lift, n_cond_by_stratum = _min_stratified_lift(df, predictor, stratify_by)
    n_cond_total = int((df[predictor] == 1).sum())

    l1 = bool(n_scored >= N_FLOOR_POP and n_cond_total >= N_FLOOR_COND)

    lo, hi, mean_boot, n_valid = _block_bootstrap_ci_min_stratified(
        df, predictor, stratify_by, "y", CI_BLOCK, CI_DRAWS, CI_SEED)
    l2 = bool(lo > 0)

    half1, half2 = _year_free_chrono_halves(df)
    lift1, _ = _min_stratified_lift(half1, predictor, stratify_by)
    lift2, _ = _min_stratified_lift(half2, predictor, stratify_by)
    l3 = bool(lift1 is not None and lift2 is not None and lift1 > 0 and lift2 > 0)

    return dict(
        label=label, n_scored=n_scored, n_cond_total=n_cond_total,
        n_cond_by_stratum=n_cond_by_stratum, observed_min_stratified_lift=obs_lift,
        L1_n_floor=l1,
        L2=dict(ci=[lo, hi], mean=mean_boot, n_valid_draws=n_valid, pass_=l2),
        L3=dict(half1_n=len(half1), half2_n=len(half2), half1_lift=lift1, half2_lift=lift2, pass_=l3),
        presence_pass=bool(l1 and l2 and l3),
    )


def evaluate_restricted(label: str, df: pd.DataFrame, restrict_col: str, restrict_val: int,
                         predictor: str) -> dict:
    sub = df[df[restrict_col] == restrict_val].copy()
    n_scored = len(sub)
    obs_lift, n_hi, n_lo = _single_lift(sub, predictor)

    l1 = bool(n_scored >= N_FLOOR_POP and n_hi >= N_FLOOR_COND)

    lo, hi, mean_boot, n_valid = _block_bootstrap_ci_single(
        sub, predictor, "y", CI_BLOCK, CI_DRAWS, CI_SEED)
    l2 = bool(lo > 0)

    half1, half2 = _year_free_chrono_halves(sub)
    lift1, _, _ = _single_lift(half1, predictor)
    lift2, _, _ = _single_lift(half2, predictor)
    l3 = bool(lift1 is not None and lift2 is not None and lift1 > 0 and lift2 > 0)

    return dict(
        label=label, restriction=f"{restrict_col}=={restrict_val}",
        n_scored=n_scored, n_cond=n_hi, n_ref=n_lo, observed_lift=obs_lift,
        L1_n_floor=l1,
        L2=dict(ci=[lo, hi], mean=mean_boot, n_valid_draws=n_valid, pass_=l2),
        L3=dict(half1_n=len(half1), half2_n=len(half2), half1_lift=lift1, half2_lift=lift2, pass_=l3),
        presence_pass=bool(l1 and l2 and l3),
    )


def main() -> None:
    mnq = pd.read_csv(MNQ_FRAME)
    mym = pd.read_csv(MYM_FRAME)

    # Pooled-figure cross-check before trusting the restriction logic (same
    # discipline byyear_l4.py's own docstring applied) -- printed, not asserted,
    # so a mismatch is visible rather than silently masked.
    print("=== Pooled-figure cross-check (must match the brief's own SS0/SS4 citations) ===")
    chk_mnq_on, _ = _min_stratified_lift(mnq, "bias_overnight", "bias_dayhist")
    chk_mym_on, _ = _min_stratified_lift(mym, "bias_overnight", "bias_dayhist")
    chk_mnq_gap, n_hi, n_lo = _single_lift(mnq[mnq["bias_overnight"] == 0], "bias_gap")
    chk_mym_gap, _, _ = _single_lift(mym[mym["bias_overnight"] == 0], "bias_gap")
    chk_mym_bp0, _, _ = _single_lift(mym[mym["bias_dayhist"] == 0], "bias_gap")
    print(f"MNQ overnight min-stratified lift: {chk_mnq_on:+.4f} (brief cites +0.5774/+0.3870 by stratum, min~+0.3870)")
    print(f"MYM overnight min-stratified lift: {chk_mym_on:+.4f} (brief cites +0.3178/+0.2207, min~+0.2207)")
    print(f"MNQ gap (overnight-calm) lift: {chk_mnq_gap:+.4f} n={n_hi}/{n_lo} (brief cites +0.1053 n=175/973)")
    print(f"MYM gap (overnight-calm) lift: {chk_mym_gap:+.4f} (brief cites +0.0848 n=991)")
    print(f"MYM gap (bprime=0) lift: {chk_mym_bp0:+.4f} (brief cites +0.1404, byyear_l4.py reproduced +0.1394)")
    print()

    results = {}
    results["H-RANGEXFER-1"] = evaluate_parent(
        "H-RANGEXFER-1", mnq, "bias_overnight", "bias_dayhist")
    results["H-RANGEXFER-1.a"] = evaluate_restricted(
        "H-RANGEXFER-1.a", mnq, "bias_overnight", 0, "bias_gap")
    results["H-RANGEXFER-1-MYM"] = evaluate_parent(
        "H-RANGEXFER-1-MYM", mym, "bias_overnight", "bias_dayhist")
    results["H-RANGEXFER-1.a-MYM"] = evaluate_restricted(
        "H-RANGEXFER-1.a-MYM", mym, "bias_overnight", 0, "bias_gap")
    results["H-RANGEXFER-1.b-MYM"] = evaluate_restricted(
        "H-RANGEXFER-1.b-MYM", mym, "bias_dayhist", 0, "bias_gap")

    print("=== L1-L3 presence battery ===")
    for hyp, r in results.items():
        print(f"\n[{hyp}]")
        print(f"  n_scored={r['n_scored']}  observed_lift={r.get('observed_min_stratified_lift', r.get('observed_lift')):+.4f}")
        print(f"  L1 (n-floor): {r['L1_n_floor']}")
        print(f"  L2 (CI lower bound > 0): {r['L2']['pass_']}  CI={r['L2']['ci']}")
        print(f"  L3 (both halves lift>0): {r['L3']['pass_']}  half1={r['L3']['half1_lift']}  half2={r['L3']['half2_lift']}")
        print(f"  PRESENCE (L1 AND L2 AND L3): {r['presence_pass']}")

    (HERE / "presence_l1_l3_results.json").write_text(json.dumps(results, indent=2, default=str))
    print(f"\nWrote {HERE / 'presence_l1_l3_results.json'}")


if __name__ == "__main__":
    main()
