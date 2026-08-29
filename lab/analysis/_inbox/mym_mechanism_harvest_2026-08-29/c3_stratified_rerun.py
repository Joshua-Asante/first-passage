"""Corrected stratified re-run of MYM candidate 3 (bar-volume regime -> next-bar range)
against the same S2-shaped cross-series $0 increment test used for candidates 2/4.

WHY THIS REPLACES c3_volume_regime.py's marginal comparison:

The original script computed two MARGINAL conditional rates -- P(y=1|bias_new=1) vs
P(y=1|bias_hist=1) -- and diffed them, exactly the same shape as the flaw found and
corrected in c2_c4_increment_falsifiers.py -> c2_c4_stratified_rerun.py. It does not
test whether above-ToD-median volume ADDS information BEYOND the bar's own already-
elevated range: two correlated predictors (same-bar volume and same-bar range have a
same-bar Spearman correlation the MNQ sibling campaign measured at 0.88) can show
near-identical marginal rates while one still carries large incremental information a
marginal comparison cannot see -- or, as happened twice already in the c2_c4 correction,
the marginal comparison can even get the SIGN backwards.

This ports the same fix: STRATIFY on bias_hist (the bar's own already-elevated range,
the "mundane same-series comparator" the original script correctly identified as the
right null but then compared to marginally instead of within-stratum), then measure
bias_new's (volume's) lift WITHIN each stratum held fixed.

Reuses c3_volume_regime.py's own tod_ratio() and load_bars() unchanged -- verified
correct, not the source of the flaw -- and its own bias_new/bias_hist/y definitions are
carried over exactly. Only the aggregation step changes.

Run from lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/ (same directory as the
original c3_volume_regime.py, so the load_sessions import resolves).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from load_sessions import PANEL, load_bars

HERE = Path(__file__).resolve().parent
TOD_WINDOW = 20  # trailing same-slot occurrences (~1 month of that exact 15m slot) -- unchanged
CI_BLOCK, CI_DRAWS, BOOT_SEED = 96, 4000, 20260829  # unchanged from c3_volume_regime.py
NULL_SEED = BOOT_SEED + 1000  # distinct from the original bootstrap seed
MIN_LIFT_FLOOR = 0.02  # 2pp -- same threshold convention as c2_c4_stratified_rerun.py
SCORED_CACHE = HERE / "c3_stratified_frame.csv"
RESULTS_JSON = HERE / "c3_stratified_results.json"


def tod_ratio(values: np.ndarray, slot: np.ndarray, window: int) -> np.ndarray:
    """Unchanged from c3_volume_regime.py: values[t] / trailing-median(values at the
    same slot, strictly prior `window` occurrences). NaN until a slot has `window`
    prior observations."""
    n = len(values)
    out = np.full(n, np.nan)
    by_slot: dict[int, list[float]] = {}
    for t in range(n):
        s = int(slot[t])
        hist = by_slot.get(s, [])
        if len(hist) >= window:
            med = float(np.median(hist[-window:]))
            if med > 0:
                out[t] = values[t] / med
        hist.append(float(values[t]))
        by_slot[s] = hist
    return out


def make_bias_biashist_y(bars):
    """Bias/bias_hist/y construction -- IDENTICAL to c3_volume_regime.py's main().

    bias_new[t]  = 1{ vol_ratio[t]   > 1 }   (this bar's volume above its own ToD-median)
    bias_hist[t] = 1{ rng_ratio[t]   > 1 }   (this bar's OWN range already elevated --
                   the mundane same-series comparator; stratify on this)
    y[t]         = 1{ rng_ratio[t+1] > 1 }   (next bar's range above its own ToD-median)
    """
    vol = bars["volume"].to_numpy(dtype=float)
    rng = (bars["high"] - bars["low"]).to_numpy(dtype=float)
    slot = bars["minute"].to_numpy(dtype=int)
    n = len(bars)

    vol_ratio = tod_ratio(vol, slot, TOD_WINDOW)
    rng_ratio = tod_ratio(rng, slot, TOD_WINDOW)

    bias_new = np.full(n, np.nan)
    valid_v = ~np.isnan(vol_ratio)
    bias_new[valid_v] = (vol_ratio[valid_v] > 1.0).astype(float)

    bias_hist = np.full(n, np.nan)
    valid_r = ~np.isnan(rng_ratio)
    bias_hist[valid_r] = (rng_ratio[valid_r] > 1.0).astype(float)

    y = np.full(n, np.nan)
    y[:-1] = np.where(~np.isnan(rng_ratio[1:]), (rng_ratio[1:] > 1.0).astype(float), np.nan)

    return bias_new, bias_hist, y


def stratified_lifts(bias: np.ndarray, bprime: np.ndarray, y: np.ndarray):
    """For each bprime stratum s in {0,1}: lift_s = P(y=1|bias=1,bprime=s) - P(y=1|bias=0,bprime=s)."""
    scored = (~np.isnan(bias)) & (~np.isnan(bprime)) & (~np.isnan(y))
    b = bias[scored].astype(int)
    bp = bprime[scored].astype(int)
    yy = y[scored].astype(int)

    def rate(mask):
        return (float(yy[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)

    lifts, counts = {}, {}
    for s in (0, 1):
        s_mask = bp == s
        hi = rate(s_mask & (b == 1))
        lo = rate(s_mask & (b == 0))
        lift = (hi[0] - lo[0]) if (hi[1] > 0 and lo[1] > 0) else None
        lifts[s] = lift
        counts[s] = dict(hi=hi, lo=lo)
    return lifts, counts, scored, b, bp, yy


def min_stratified_lift(b: np.ndarray, bp: np.ndarray, yy: np.ndarray) -> float:
    """The bootstrap-resampled statistic: min over populated strata of the lift."""
    vals = []
    for s in (0, 1):
        s_mask = bp == s
        hi_mask, lo_mask = s_mask & (b == 1), s_mask & (b == 0)
        if hi_mask.any() and lo_mask.any():
            vals.append(float(yy[hi_mask].mean() - yy[lo_mask].mean()))
    return min(vals) if vals else float("nan")


def block_bootstrap_min_lift(b, bp, yy, n_boot, block, seed):
    """Circular block bootstrap on the minimum stratified lift -- same block=96
    (~1 M15 session) scheme c3_volume_regime.py's own CI already used.

    NOT a null-calibrated p-value (flagged on review, PR #205 / this retrofit):
    this resamples the OBSERVED (b, bp, y) jointly, so the bootstrap distribution
    stays centered on the observed min-lift. `p_lift_le_0` is a percentile-CI-style
    tail probability, not a Type-I probability under a true zero-association null.
    Kept for continuity (disclose, don't erase). Report `circular_shift_null_min_lift`
    as the significance figure."""
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


def circular_shift_null_p(y, fixed_mask, other_label, draws=4000, seed=44):
    """Null-calibrated one-sided p-value: does `other_label` carry information
    about y within `fixed_mask`, beyond what a decorrelated version of the same
    two series would produce by chance?

    Circularly shifts `other_label`'s FULL series (not just the `fixed_mask`
    subset) by a random offset each draw, so `other_label`'s own autocorrelation
    /persistence structure is exactly preserved (a rotation, not an i.i.d.
    reshuffle) while its pairing with (y, fixed_mask) is destroyed -- the same
    circular-shift/surrogate logic this codebase already uses for block-shuffle
    and IAAFT nulls elsewhere (see `iaaft_battery.py`), applied here to a
    cross-series lift statistic instead of an autocorrelation statistic. Reports
    the fraction of null draws whose within-stratum lift is >= the observed lift
    (one-sided, Type-I-controlled under H0: no association).

    Copied from the reviewed MYM sibling `c24_joint_gate.py` (PR #205, commit
    f9db9ec).
    """
    rng = np.random.default_rng(seed)
    N = len(y)
    hi0 = fixed_mask & (other_label == 1)
    lo0 = fixed_mask & (other_label == 0)
    if not (hi0.any() and lo0.any()):
        return np.array([]), float("nan"), float("nan")
    observed = float(y[hi0].mean() - y[lo0].mean())
    draws_out = []
    for _ in range(draws):
        shift = rng.integers(1, N)
        shifted = np.roll(other_label, shift)
        hi = fixed_mask & (shifted == 1)
        lo = fixed_mask & (shifted == 0)
        if hi.any() and lo.any():
            draws_out.append(float(y[hi].mean() - y[lo].mean()))
    draws_out = np.array(draws_out)
    p_ge_obs = (1 + int((draws_out >= observed).sum())) / (len(draws_out) + 1)
    return draws_out, p_ge_obs, observed


def circular_shift_null_min_lift(b, bp, yy, draws, seed):
    """Null-calibrated one-sided p on the SAME statistic `block_bootstrap_min_lift`
    reports: min over populated strata of the within-stratum lift.

    Circularly shifts the NEW predictor `b` (preserving its own autocorrelation)
    while holding `(bp, y)` fixed -- destroying the pairing under test, same
    surrogate-shift logic as `circular_shift_null_p`. Reports the fraction of
    null min-lifts >= the observed min-lift.
    """
    rng = np.random.default_rng(seed)
    N = len(yy)
    observed = min_stratified_lift(b, bp, yy)
    if not np.isfinite(observed):
        return np.array([]), float("nan"), float("nan")
    draws_out = []
    for _ in range(draws):
        shift = rng.integers(1, N)
        shifted = np.roll(b, shift)
        v = min_stratified_lift(shifted, bp, yy)
        if np.isfinite(v):
            draws_out.append(v)
    draws_out = np.array(draws_out)
    p_ge_obs = (1 + int((draws_out >= observed).sum())) / (len(draws_out) + 1)
    return draws_out, p_ge_obs, observed


def write_scored_cache(b, bp, yy):
    """Persist the scored (bias, bias_hist, y) series so a later follow-up
    does not need vendor bars. Written only when we built from bars."""
    import csv
    with SCORED_CACHE.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["bias_volume", "bias_own_range", "y"])
        for i in range(len(yy)):
            w.writerow([int(b[i]), int(bp[i]), int(yy[i])])


def load_scored_cache():
    if not SCORED_CACHE.exists():
        return None
    import csv
    with SCORED_CACHE.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return None
    b = np.array([int(r["bias_volume"]) for r in rows], dtype=int)
    bp = np.array([int(r["bias_own_range"]) for r in rows], dtype=int)
    yy = np.array([int(r["y"]) for r in rows], dtype=int)
    return b, bp, yy


def main():
    prior = json.loads(RESULTS_JSON.read_text()) if RESULTS_JSON.exists() else {}
    cached = load_scored_cache()
    from_bars = PANEL.exists()

    if from_bars:
        bars = load_bars()
        bars = bars[bars["session"] < bars["session"].max()]  # drop trailing truncated day -- unchanged
        n = len(bars)
        print(f"bars: {n} (from {PANEL})")
        bias, bprime, y = make_bias_biashist_y(bars)
        lifts, counts, scored, b, bp, yy = stratified_lifts(bias, bprime, y)
        print(f"n_scored={int(scored.sum())}")
        write_scored_cache(b, bp, yy)
        print(f"wrote {SCORED_CACHE.name} ({int(scored.sum())} scored rows) for future no-bar reruns")
        frame_source = f"{PANEL.name} (n={int(scored.sum())})"
        recompute_boot = True
    elif cached is not None:
        b, bp, yy = cached
        lifts, counts, scored, b, bp, yy = stratified_lifts(
            b.astype(float), bp.astype(float), yy.astype(float))
        print(f"loaded {SCORED_CACHE.name} (n_scored={int(scored.sum())}; no vendor bars)")
        frame_source = f"{SCORED_CACHE.name} (n={int(scored.sum())})"
        recompute_boot = True
    else:
        print(f"vendor bars absent ({PANEL}) and no {SCORED_CACHE.name}; "
              "cannot compute circular-shift null p this run")
        print("preserving original bootstrap figures; null-calibrated p left uncomputed")
        out = dict(prior)
        out["min_lift_null_calibrated"] = dict(
            p_ge_obs=None, observed=None, n_draws=CI_DRAWS, seed=NULL_SEED,
            frame_source="UNCOMPUTED — no vendor bars, no scored-frame cache",
            n_scored_null=None,
        )
        out["strata_null_calibrated_p"] = {"0": None, "1": None}
        RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str))
        print("\nWrote c3_stratified_results.json (null p UNCOMPUTED; original bootstrap preserved)")
        return

    strata_null_p = {}
    for s in (0, 1):
        if lifts[s] is not None:
            _, p_null, _obs = circular_shift_null_p(yy, bp == s, b, draws=CI_DRAWS, seed=300 + s)
            strata_null_p[s] = p_null

    _, p_null_min, obs_min = circular_shift_null_min_lift(b, bp, yy, CI_DRAWS, NULL_SEED)

    if recompute_boot:
        lo, hi, mean_boot, n_valid, p_le0 = block_bootstrap_min_lift(
            b, bp, yy, CI_DRAWS, CI_BLOCK, BOOT_SEED)
        populated_lifts = [l for l in lifts.values() if l is not None]
        increment_exists = len(populated_lifts) > 0 and all(l > MIN_LIFT_FLOOR for l in populated_lifts)
        verdict = "INCREMENT" if (lo > 0 and increment_exists) else (
            "NO-INCREMENT" if hi < 0 else "AMBIGUOUS (CI straddles 0)")
        n_scored_out = int(scored.sum())
    else:
        lo, hi = prior["min_lift_bootstrap"]["ci"]
        mean_boot = prior["min_lift_bootstrap"]["mean"]
        n_valid = prior["min_lift_bootstrap"]["n_valid"]
        p_le0 = prior["min_lift_bootstrap"]["p_lift_le_0"]
        increment_exists = prior["increment_exists_threshold_check"]
        verdict = prior["verdict"]
        n_scored_out = prior["n_scored"]

    for s in (0, 1):
        c = counts[s]
        print(f"  stratum bias_hist(own-range)={s}: P(y=1|volume=1)={c['hi'][0]:.4f}(n={c['hi'][1]})  "
              f"P(y=1|volume=0)={c['lo'][0]:.4f}(n={c['lo'][1]})  lift={lifts[s]}")
        if s in strata_null_p:
            print(f"    circular-shift null p(null_lift>=observed) [null-calibrated] = {strata_null_p[s]:.5f}")
    print(f"  min-stratified-lift bootstrap: mean={mean_boot:.4f}  CI=[{lo:+.4f},{hi:+.4f}]  "
          f"p(lift<=0)={p_le0:.4f} [NOT null-calibrated]  VERDICT={verdict}")
    print(f"  min-stratified-lift circular-shift null p(null>=obs) [null-calibrated] = {p_null_min:.5f}  "
          f"(obs={obs_min:.4f})")

    out = dict(
        n_scored=n_scored_out,
        strata=lifts,
        strata_counts={str(s): counts[s] for s in counts},
        min_lift_bootstrap=dict(ci=[lo, hi], mean=mean_boot, n_valid=n_valid, p_lift_le_0=p_le0),
        min_lift_null_calibrated=dict(
            p_ge_obs=p_null_min, observed=obs_min, n_draws=CI_DRAWS, seed=NULL_SEED,
            frame_source=frame_source, n_scored_null=int(len(yy)),
        ),
        strata_null_calibrated_p={str(s): strata_null_p.get(s) for s in (0, 1)},
        increment_exists_threshold_check=bool(increment_exists),
        verdict=verdict,
    )
    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote c3_stratified_results.json")
    print("Compare against c3_results.json (the original marginal-comparison run) --")
    print("do NOT overwrite it; cite both in the corrected Notice-log entry.")


if __name__ == "__main__":
    main()
