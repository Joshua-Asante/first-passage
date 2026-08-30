"""Stratified re-run of MNQ candidate 3 (bar-volume regime -> next-bar range),
adding the within-stratum null-calibrated p that `candidate3_volume_regime.py`
never computed, and the own-range stratification RESULTS.md's prose already
cites (+20.6pp low-range / +25.6pp high-range) but whose generating code was
never committed -- this script is the first committed, re-runnable source for
that incremental-lift claim.

WHY THIS EXISTS (mirrors MYM's own c3_volume_regime.py -> c3_stratified_rerun.py
split, `lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/`, same rationale):
same-bar volume and same-bar range are highly correlated (Spearman 0.88, this
session's own RESULTS.md). A marginal ToD-matched lift for volume could be
entirely riding the trigger bar's own already-elevated range (the mundane
same-series persistence `daily-range-state-persistence`/`Q-RANGEXFER-1` already
document at other lags). Stratifying on the trigger bar's own range state and
measuring volume's lift WITHIN each stratum is the same design already applied
to MYM's candidate 3 and to MNQ/MYM candidates 2/4 (`c2_c4_stratified_rerun.py`).

Ports `circular_shift_null_p` / `circular_shift_null_min_lift` VERBATIM from
`c24_joint_gate.py` (MNQ) / `c3_stratified_rerun.py` (MYM) -- same within-stratum
circular-shift construction (Codex PR #207 P1/P2: rotate only within the fixed
stratum, enumerate all distinct rotations including identity when n is small).

Reuses `candidate3_volume_regime.py`'s own `rolling_pct_strict_prior_by_group`,
`load_raw`, `TRAIL_N`, `Q_BIAS` unchanged -- including its 2026-08-30 ToD-indexing
fix (each next bar compared against ITS OWN slot's threshold, not the trigger
bar's) -- and its own bias_tod/rng_thresh_tod construction is carried over
exactly. Only the aggregation step (stratify + null-calibrate) is new.

Run from lab/analysis/_inbox/mnq_dailygeom_notice_2026-08-29/ (same directory as
candidate3_volume_regime.py, so the import resolves).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw  # noqa: E402
from candidate3_volume_regime import (  # noqa: E402
    rolling_pct_strict_prior_by_group,
    TRAIL_N,
    Q_BIAS,
)

CI_BLOCK, CI_DRAWS, BOOT_SEED = 96, 4000, 20260830  # distinct from the base script's own seed
NULL_SEED = BOOT_SEED + 1000
MIN_LIFT_FLOOR = 0.02  # 2pp -- same convention as c2_c4_stratified_rerun.py / MYM's c3 rerun
RESULTS_JSON = HERE / "candidate3_stratified_results.json"

# Within-stratum circular-shift null -- verbatim port (Codex PR #207 P1/P2), same
# construction already used in candidate24_joint_gate.py (MNQ) and MYM's c3_stratified_rerun.py.
_MAX_ENUMERATE_N = 2500


def _stratum_circular_lifts(y_s, other_s):
    n = len(other_s)
    lifts = np.full(n, np.nan)
    for k in range(n):
        rolled = np.roll(other_s, k)
        hi = rolled == 1
        n_hi = int(hi.sum())
        if 0 < n_hi < n:
            lifts[k] = float(y_s[hi].mean() - y_s[~hi].mean())
    return lifts


def circular_shift_null_p(y, fixed_mask, other_label, draws=4000, seed=44):
    """Null-calibrated one-sided p under a within-stratum circular-shift null.
    Rotate `other_label` only inside `fixed_mask`; enumerate all distinct
    rotations (identity included) when n is small, else Monte Carlo draws."""
    y = np.asarray(y)
    fixed = np.asarray(fixed_mask, dtype=bool)
    other = np.asarray(other_label)
    y_s = y[fixed]
    o_s = other[fixed]
    n = len(o_s)
    hi0 = o_s == 1
    lo0 = o_s == 0
    if n < 2 or not (hi0.any() and lo0.any()):
        return np.array([]), float("nan"), float("nan")
    observed = float(y_s[hi0].mean() - y_s[lo0].mean())

    if n <= _MAX_ENUMERATE_N:
        lifts = _stratum_circular_lifts(y_s, o_s)
        valid = lifts[np.isfinite(lifts)]
        if valid.size == 0:
            return np.array([]), float("nan"), observed
        p_ge_obs = float((valid >= observed).sum()) / float(valid.size)
        return valid, p_ge_obs, observed

    rng = np.random.default_rng(seed)
    draws_out = []
    for _ in range(draws):
        rolled = np.roll(o_s, int(rng.integers(0, n)))
        hi = rolled == 1
        lo = rolled == 0
        if hi.any() and lo.any():
            draws_out.append(float(y_s[hi].mean() - y_s[lo].mean()))
    draws_out = np.asarray(draws_out)
    p_ge_obs = (1 + int((draws_out >= observed).sum())) / (len(draws_out) + 1)
    return draws_out, p_ge_obs, observed


def min_stratified_lift(b, bp, yy):
    vals = []
    for s in (0, 1):
        s_mask = bp == s
        hi_mask, lo_mask = s_mask & (b == 1), s_mask & (b == 0)
        if hi_mask.any() and lo_mask.any():
            vals.append(float(yy[hi_mask].mean() - yy[lo_mask].mean()))
    return min(vals) if vals else float("nan")


def circular_shift_null_min_lift(b, bp, yy, draws, seed):
    """Null-calibrated one-sided p on min-over-strata lift; within-stratum rolls.
    When both strata are small enough to fully enumerate, the exact joint tail
    is the PRODUCT of the two per-stratum tail counts -- this tests the SHARP
    joint null that both strata are simultaneously zero, not the disjunctive
    composite null a "both strata" claim needs (Codex PR #211 finding on the
    MYM gap-magnitude analogue). Disclosed as such below; the per-stratum p's
    (returned separately by the caller) are the authoritative figures for a
    composite ("either stratum") claim -- take max(), not this function's
    product-based figure, per that same correction."""
    observed = min_stratified_lift(b, bp, yy)
    if not np.isfinite(observed):
        return np.array([]), float("nan"), float("nan")

    tails = []
    n_valid = 1
    all_small = True
    for s in (0, 1):
        m = bp == s
        y_s, b_s = yy[m], b[m]
        n_s = len(b_s)
        if n_s < 2:
            return np.array([]), float("nan"), observed
        if n_s > _MAX_ENUMERATE_N:
            all_small = False
            break
        lifts = _stratum_circular_lifts(y_s, b_s)
        valid = lifts[np.isfinite(lifts)]
        if valid.size == 0:
            return np.array([]), float("nan"), observed
        tails.append(int((valid >= observed).sum()))
        n_valid *= int(valid.size)

    if all_small and len(tails) == 2:
        p_ge_obs = float(tails[0] * tails[1]) / float(n_valid)
        return np.array([]), p_ge_obs, observed

    rng = np.random.default_rng(seed)
    parts = []
    for s in (0, 1):
        m = bp == s
        parts.append((yy[m], b[m]))
    draws_out = []
    for _ in range(draws):
        vals = []
        ok = True
        for y_s, b_s in parts:
            n_s = len(b_s)
            rolled = np.roll(b_s, int(rng.integers(0, n_s)))
            hi, lo = rolled == 1, rolled == 0
            if not (hi.any() and lo.any()):
                ok = False
                break
            vals.append(float(y_s[hi].mean() - y_s[lo].mean()))
        if ok:
            draws_out.append(min(vals))
    draws_out = np.asarray(draws_out)
    p_ge_obs = (1 + int((draws_out >= observed).sum())) / (len(draws_out) + 1)
    return draws_out, p_ge_obs, observed


def block_bootstrap_min_lift(b, bp, yy, n_boot, block, seed):
    """Circular block bootstrap on the min stratified lift -- disclosure only,
    NOT null-calibrated (resamples the observed series; see the module docstrings
    this pattern is ported from for the full caveat). Report the circular-shift
    null p as the significance figure."""
    rng = np.random.default_rng(seed)
    N = len(yy)
    block = min(block, max(1, N // 2))
    nblocks = int(np.ceil(N / block))
    draws = []
    for _ in range(n_boot):
        st = rng.integers(0, N, size=nblocks)
        idx = (st[:, None] + np.arange(block)[None, :]) % N
        idx = idx.ravel()[:N]
        v = min_stratified_lift(b[idx], bp[idx], yy[idx])
        if np.isfinite(v):
            draws.append(v)
    draws = np.asarray(draws)
    lo, hi = np.percentile(draws, [2.5, 97.5])
    p_lift_le_0 = float((draws <= 0).mean())
    return float(lo), float(hi), float(draws.mean()), int(len(draws)), p_lift_le_0


def main():
    df = load_raw().reset_index(drop=True)
    n = len(df)
    vol = df["volume"].to_numpy(dtype=float)
    hi_, lo_ = df["high"].to_numpy(), df["low"].to_numpy()
    rng_bar = hi_ - lo_
    et_minute = df["et_minute"].to_numpy()
    print(f"n bars: {n}")

    # Identical construction to candidate3_volume_regime.py's ToD-matched design
    # (post-2026-08-30 fix): bias_tod[t] = this bar's volume above its own ToD
    # trailing median; y[t] = next bar's range above ITS OWN slot's threshold.
    thresh_vol_tod = rolling_pct_strict_prior_by_group(vol, et_minute, TRAIL_N, Q_BIAS)
    bias_tod = np.where(np.isnan(thresh_vol_tod), np.nan, (vol >= thresh_vol_tod).astype(float))

    rng_thresh_tod = rolling_pct_strict_prior_by_group(rng_bar, et_minute, TRAIL_N, 0.50)
    y = np.full(n, np.nan)
    y[:-1] = (rng_bar[1:] > rng_thresh_tod[1:]).astype(float)
    y[-1] = np.nan

    # NEW: bias_hist[t] = the TRIGGER bar's own range already elevated vs its own
    # ToD threshold -- the mundane same-series comparator to stratify on.
    bias_hist = np.where(np.isnan(rng_thresh_tod), np.nan, (rng_bar > rng_thresh_tod).astype(float))

    scored = (~np.isnan(bias_tod)) & (~np.isnan(bias_hist)) & (~np.isnan(y))
    b = bias_tod[scored].astype(int)
    bp = bias_hist[scored].astype(int)
    yy = y[scored].astype(int)
    n_scored = int(scored.sum())
    print(f"n_scored={n_scored}")

    def rate(mask):
        return (float(yy[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)

    lifts, counts, strata_null_p = {}, {}, {}
    for s in (0, 1):
        s_mask = bp == s
        hi = rate(s_mask & (b == 1))
        lo = rate(s_mask & (b == 0))
        lift = (hi[0] - lo[0]) if (hi[1] > 0 and lo[1] > 0) else None
        lifts[s] = lift
        counts[s] = dict(hi=hi, lo=lo)
        print(f"  stratum bias_hist(own-range)={s}: P(y=1|volume=1)={hi[0]:.4f}(n={hi[1]})  "
              f"P(y=1|volume=0)={lo[0]:.4f}(n={lo[1]})  lift={lift}")
        if lift is not None:
            _, p_null, _obs = circular_shift_null_p(yy, s_mask, b, draws=CI_DRAWS, seed=500 + s)
            strata_null_p[s] = p_null
            print(f"    circular-shift null p(null_lift>=observed) [null-calibrated] = {p_null:.5f}")

    lo, hi, mean_boot, n_valid, p_le0 = block_bootstrap_min_lift(b, bp, yy, CI_DRAWS, CI_BLOCK, BOOT_SEED)
    populated_lifts = [l for l in lifts.values() if l is not None]
    increment_exists = len(populated_lifts) > 0 and all(l > MIN_LIFT_FLOOR for l in populated_lifts)
    boot_verdict = "INCREMENT" if (lo > 0 and increment_exists) else (
        "NO-INCREMENT" if hi < 0 else "AMBIGUOUS (CI straddles 0)")
    print(f"  min-stratified-lift bootstrap: mean={mean_boot:.4f}  CI=[{lo:+.4f},{hi:+.4f}]  "
          f"p(lift<=0)={p_le0:.4f} [NOT null-calibrated]  VERDICT={boot_verdict}")

    _, p_null_min, obs_min = circular_shift_null_min_lift(b, bp, yy, CI_DRAWS, NULL_SEED)
    print(f"  min-stratified-lift circular-shift null p(null>=obs) [product-of-tails, "
          f"SHARP joint null only -- see docstring] = {p_null_min:.5f}  (obs={obs_min:.4f})")
    composite_p = max(strata_null_p.values()) if strata_null_p else float("nan")
    print(f"  composite (disjunctive, 'either stratum') null p = max(per-stratum p's) = {composite_p:.5f}")

    out = dict(
        n_scored=n_scored,
        strata=lifts,
        strata_counts={str(s): counts[s] for s in counts},
        min_lift_bootstrap=dict(ci=[lo, hi], mean=mean_boot, n_valid=n_valid, p_lift_le_0=p_le0,
                                 verdict=boot_verdict),
        min_lift_null_calibrated_product_sharp_joint=dict(
            p_ge_obs=p_null_min, observed=obs_min, n_draws=CI_DRAWS, seed=NULL_SEED,
            caveat="product-of-tails tests the SHARP joint null (both strata simultaneously "
                   "zero), not the disjunctive composite claim -- see docstring / PR #211",
        ),
        strata_null_calibrated_p={str(s): strata_null_p.get(s) for s in (0, 1)},
        composite_disjunctive_null_p_max_of_strata=composite_p,
        increment_exists_threshold_check=bool(increment_exists),
        frame_source="MNQ_M15.csv (live vendor bars, this run)",
        construction="within_stratum_circular_shift",
        includes_identity=True,
    )
    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str))
    print(f"\nWrote {RESULTS_JSON.name}")
    print("Compare against candidate3_results.json (the original naive/ToD-matched marginal run) --")
    print("do NOT overwrite it; cite both in the corrected Notice-log entry.")


if __name__ == "__main__":
    main()
