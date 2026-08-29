"""Corrected stratified re-run of MYM candidates 2 (overnight-range) and 4 (gap-magnitude)
against the D5 stage-1 $0 cheap falsifier
(docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md SS4).

WHY THIS REPLACES c2_c4_increment_falsifiers.py's run_one/conditional_rate_given:

The original script computed two MARGINAL conditional rates -- P(y=1 | bias_new=1) vs
P(y=1 | bias_hist=1) -- and diffed them. That does not test "does overnight-state
conditioning ADD information BEYOND matched day-session-history conditioning" the way
the spec's own language ("matched day-session-history CONDITIONING", "INCREMENT")
requires. Two correlated predictors can show near-identical marginal rates while one
still carries large incremental information (or vice versa) -- a marginal horse-race
does not isolate that.

The MNQ sibling campaign (candidate2_overnight_rth_transfer.py) used the correct design:
STRATIFY on bias_hist (bias'), then measure bias_new's lift WITHIN each stratum held
fixed. That is what "matched ... conditioning" means -- match on day-history state, then
ask whether overnight-state still moves the needle. This script ports that exact design
to MYM, reusing MYM's own load_sessions.py / iaaft_battery.py helpers so the underlying
bias/bias'/y definitions are UNCHANGED from the original script (verified equivalent to
MNQ's own definitions) -- only the aggregation step changes from "compare two marginals"
to "stratify and compare within each stratum".

Run from lab/analysis/_inbox/mym_mechanism_harvest_2026-08-29/ (same directory as the
original c2_c4_increment_falsifiers.py, so the sys.path-relative imports resolve).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from load_sessions import PANEL, load_bars, session_ohlc, rth_ohlc, overnight_ohlc
import iaaft_battery as B

HERE = Path(__file__).resolve().parent
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50
CI_BLOCK, CI_DRAWS, BOOT_SEED = 60, 4000, 20260829
NULL_SEED = BOOT_SEED + 1000  # distinct from the original bootstrap seed
MIN_LIFT_FLOOR = 0.02  # 2pp -- same "well above noise floor" threshold MNQ's script used
C24_FRAME = HERE / "c24_joint_frame.csv"
RESULTS_JSON = HERE / "c2_c4_stratified_results.json"


def build_frame():
    """Unchanged from c2_c4_increment_falsifiers.py -- same data, same series."""
    bars = load_bars()
    full = session_ohlc(bars)
    full = full[full["n_bars"] >= 20]
    rth = rth_ohlc(bars)
    on = overnight_ohlc(bars)
    idx = full.index
    rth = rth.reindex(idx)
    on = on.reindex(idx)

    rth_range = (rth["high"] - rth["low"]).to_numpy()
    on_range = (on["high"] - on["low"]).to_numpy()
    rth_open = rth["open"].to_numpy()
    rth_close = rth["close"].to_numpy()
    gap = np.full(len(idx), np.nan)
    gap[1:] = rth_open[1:] - rth_close[:-1]
    abs_gap = np.abs(gap)

    return dict(idx=idx, rth_range=rth_range, on_range=on_range, abs_gap=abs_gap)


def make_bias_biasprime_y(bias_source: np.ndarray, rth_range: np.ndarray):
    """Bias/bias'/y construction -- IDENTICAL in substance to both the original
    c2_c4_increment_falsifiers.py's bias/bias_hist and MNQ's candidate2 script's
    bias/bias_prime_shifted (confirmed equivalent by inspection during review).
    Kept as a single shared function so candidates 2 and 4 use one code path.

    bias_d  = 1{ bias_source_d      >= P80(trailing 60 bias_source, strict prior) }
    bprime_d= 1{ rth_range_{d-1}    >= P80(trailing 60 rth_range ending d-2) }   (yesterday's
              OWN RTH-range state, matched day-history -- shifted forward to align with day d)
    y_d     = 1{ rth_range_d        >  P50(trailing 60 rth_range ending d-1) }   (today's RTH
              range elevated vs its own trailing median, strictly causal)
    """
    n = len(rth_range)

    thresh_bias = B.rolling_pctl_strict_prior(bias_source, WINDOW, Q_BIAS)
    bias = (bias_source >= thresh_bias).astype(float)
    bias[np.isnan(thresh_bias)] = np.nan

    thresh_bp = B.rolling_pctl_strict_prior(rth_range, WINDOW, Q_BIAS)
    bprime_raw = (rth_range >= thresh_bp).astype(float)
    bprime_raw[np.isnan(thresh_bp)] = np.nan
    bprime = np.full(n, np.nan)
    bprime[1:] = bprime_raw[:-1]  # yesterday's state, aligned to today's row

    ref = B.rolling_pctl_strict_prior(rth_range, WINDOW, Q_REF)
    y = (rth_range > ref).astype(float)
    y[np.isnan(ref)] = np.nan

    return bias, bprime, y


def stratified_lifts(bias: np.ndarray, bprime: np.ndarray, y: np.ndarray):
    """For each bprime stratum s in {0,1}: lift_s = P(y=1|bias=1,bprime=s) - P(y=1|bias=0,bprime=s).
    Returns (lifts: dict[int, float|None], counts: dict[int, dict], scored_mask)."""
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
    """The statistic the bootstrap resamples: min over populated strata of
    P(y=1|bias=1,bprime=s) - P(y=1|bias=0,bprime=s). Matches MNQ's own reporting
    convention ("block-bootstrap ... on the MINIMUM stratified lift") -- the
    conservative read across both day-history states, not an average."""
    vals = []
    for s in (0, 1):
        s_mask = bp == s
        hi_mask, lo_mask = s_mask & (b == 1), s_mask & (b == 0)
        if hi_mask.any() and lo_mask.any():
            vals.append(float(yy[hi_mask].mean() - yy[lo_mask].mean()))
    return min(vals) if vals else float("nan")


def block_bootstrap_min_lift(b: np.ndarray, bp: np.ndarray, yy: np.ndarray,
                              n_boot: int, block: int, seed: int):
    """Circular day-block bootstrap on the minimum stratified lift, same block scheme
    as MYM's original paired_diff_bootstrap (block-of-60-days, resampled as contiguous
    blocks so day-to-day autocorrelation in the underlying series is preserved).

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


# Within-stratum circular-shift null (Codex PR #207 P1/P2).
# Enumerate every distinct rotation when the stratum is small enough that
# Monte-Carlo-with-replacement would invent precision beyond the rotation set.
_MAX_ENUMERATE_N = 2500


def roll_other_within_stratum(other_label, fixed_mask, k):
    """Rotate `other_label` only among `fixed_mask` rows, in time order.

    Preserves P(other | stratum) and leaves the complementary stratum untouched
    — the conditional null Codex required. Full-series roll then mask is wrong
    when the predictor is correlated with the conditioner.
    """
    out = np.asarray(other_label).copy()
    idx = np.flatnonzero(np.asarray(fixed_mask, dtype=bool))
    if idx.size:
        out[idx] = np.roll(out[idx], int(k))
    return out


def _stratum_circular_lifts(y_s, other_s):
    """Lift under every distinct circular rotation of `other_s`, identity included."""
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
    """Null-calibrated one-sided p: does `other_label` carry information about y
    *within* `fixed_mask` under a conditional zero-association null?

    Surrogate is a circular shift of `other_label` **inside the stratum only**
    (Codex P1). That keeps within-stratum class balance and the predictor's
    within-stratum autocorrelation, and does not import labels from the other
    conditioner state. Pairing with y inside the stratum is destroyed.

    When the stratum length is <= `_MAX_ENUMERATE_N`, every distinct rotation
    including the identity is enumerated and p = count(stat >= obs) / n_valid
    (Codex P2 — no with-replacement Monte Carlo on a smaller rotation set).
    Larger strata draw k uniformly from {0, …, n-1} (identity included) and
    use the +1 convention.
    """
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


def circular_shift_null_min_lift(b: np.ndarray, bp: np.ndarray, yy: np.ndarray,
                                 draws: int, seed: int):
    """Null-calibrated one-sided p on the SAME statistic `block_bootstrap_min_lift`
    reports: min over populated strata of the within-stratum lift.

    Independent within-stratum circular shifts of `b` (Codex P1). Because
    min(L0, L1) >= obs iff both stratum lifts are >= obs, the enumerated
    pair-null p is the product of the two one-stratum tail counts — no need
    to materialize n0*n1 draws. Identity included in each stratum.
    """
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


def scored_from_c24_cache(bias_col: str):
    """Fallback when vendor bars are absent: the sibling joint-gate script
    cached the same per-day (bias_overnight, bias_gap, bias_dayhist, y) series.
    That frame requires ALL three biases non-nan, so n is 3 days shorter than
    this script's original per-candidate scored set (1304 vs 1307). Disclosed
    at the call site; do not silently overwrite the original bootstrap numbers
    computed on n=1307."""
    if not C24_FRAME.exists():
        return None
    import csv
    with C24_FRAME.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    b = np.array([int(r[bias_col]) for r in rows], dtype=int)
    bp = np.array([int(r["bias_dayhist"]) for r in rows], dtype=int)
    yy = np.array([int(r["y"]) for r in rows], dtype=int)
    return b, bp, yy, len(rows), f"{C24_FRAME.name} (n={len(rows)}; orig scored n=1307)"


def run_one(label: str, b: np.ndarray, bp: np.ndarray, yy: np.ndarray,
            n_scored: int, frame_source: str, prior: dict | None = None):
    lifts, counts = {}, {}

    def rate(mask):
        return (float(yy[mask].mean()), int(mask.sum())) if mask.any() else (float("nan"), 0)

    for s in (0, 1):
        s_mask = bp == s
        hi = rate(s_mask & (b == 1))
        lo = rate(s_mask & (b == 0))
        lift = (hi[0] - lo[0]) if (hi[1] > 0 and lo[1] > 0) else None
        lifts[s] = lift
        counts[s] = dict(hi=hi, lo=lo)

    strata_null_p = {}
    for s in (0, 1):
        if lifts[s] is not None:
            _, p_null, _obs = circular_shift_null_p(yy, bp == s, b, draws=CI_DRAWS, seed=300 + s)
            strata_null_p[s] = p_null

    _, p_null_min, obs_min = circular_shift_null_min_lift(b, bp, yy, CI_DRAWS, NULL_SEED)

    # Preserve the original n=1307 bootstrap figures when we fell back to the
    # sibling joint-gate cache (n=1304). Recompute only when we have the
    # original scored series from vendor bars.
    if prior is not None and prior.get("min_lift_bootstrap"):
        boot = prior["min_lift_bootstrap"]
        lo, hi = boot["ci"]
        mean_boot, n_valid, p_le0 = boot["mean"], boot["n_valid"], boot["p_lift_le_0"]
        verdict = prior["verdict"]
        increment_exists = prior["increment_exists_threshold_check"]
        # Keep the AUTHORITATIVE stratum lifts/counts from the original run
        # (n=1307) when we only have the 1304-day cache for the null p.
        lifts = {int(k): v for k, v in prior["strata"].items()}
        counts = {int(k): v for k, v in prior["strata_counts"].items()}
        n_scored_out = prior["n_scored"]
        boot_source = "preserved from original n=1307 run (cache fallback)"
    else:
        lo, hi, mean_boot, n_valid, p_le0 = block_bootstrap_min_lift(
            b, bp, yy, CI_DRAWS, CI_BLOCK, BOOT_SEED)
        populated_lifts = [l for l in lifts.values() if l is not None]
        increment_exists = len(populated_lifts) > 0 and all(l > MIN_LIFT_FLOOR for l in populated_lifts)
        verdict = "INCREMENT" if (lo > 0 and increment_exists) else (
            "NO-INCREMENT" if hi < 0 else "AMBIGUOUS (CI straddles 0)")
        n_scored_out = n_scored
        boot_source = frame_source

    result = dict(
        label=label, n_scored=int(n_scored_out),
        strata=lifts,
        strata_counts={str(s): counts[s] for s in counts},
        min_lift_bootstrap=dict(ci=[lo, hi], mean=mean_boot, n_valid=n_valid, p_lift_le_0=p_le0,
                                source=boot_source),
        min_lift_null_calibrated=dict(
            p_ge_obs=p_null_min, observed=obs_min, n_draws=CI_DRAWS, seed=NULL_SEED,
            frame_source=frame_source, n_scored_null=int(n_scored),
            construction="within_stratum_circular_shift",
            includes_identity=True,
        ),
        strata_null_calibrated_p={str(s): strata_null_p.get(s) for s in (0, 1)},
        increment_exists_threshold_check=bool(increment_exists),
        verdict=verdict,
    )
    print(f"\n[{label}] n_scored={result['n_scored']}  null-frame={frame_source}")
    for s in (0, 1):
        c = counts[s]
        print(f"  stratum bprime={s}: P(y=1|bias=1)={c['hi'][0]:.4f}(n={c['hi'][1]})  "
              f"P(y=1|bias=0)={c['lo'][0]:.4f}(n={c['lo'][1]})  lift={lifts[s]}")
        if s in strata_null_p:
            print(f"    circular-shift null p(null_lift>=observed) [null-calibrated] = {strata_null_p[s]:.6g}")
    print(f"  min-stratified-lift bootstrap: mean={mean_boot:.4f}  CI=[{lo:+.4f},{hi:+.4f}]  "
          f"p(lift<=0)={p_le0:.4f} [NOT null-calibrated]  VERDICT={verdict}")
    print(f"  min-stratified-lift circular-shift null p(null>=obs) [null-calibrated] = {p_null_min:.6g}  "
          f"(obs={obs_min:.4f}, n_null={n_scored})")
    return result


def main():
    prior = {}
    if RESULTS_JSON.exists():
        prior = json.loads(RESULTS_JSON.read_text())

    from_bars = PANEL.exists()
    out = {}
    specs = (
        ("candidate2_overnight_range_STRATIFIED", "on_range", "bias_overnight"),
        ("candidate4_gap_magnitude_STRATIFIED", "abs_gap", "bias_gap"),
    )
    if from_bars:
        frame = build_frame()
        print(f"built frame from {PANEL} (vendor bars present)")
        for label, source_key, _bias_col in specs:
            bias, bprime, y = make_bias_biasprime_y(frame[source_key], frame["rth_range"])
            _lifts, _counts, scored, b, bp, yy = stratified_lifts(bias, bprime, y)
            out[label] = run_one(label, b, bp, yy, int(scored.sum()), f"{PANEL.name} (n={int(scored.sum())})")
    else:
        print(f"vendor bars absent ({PANEL}); falling back to {C24_FRAME.name}")
        for label, _source_key, bias_col in specs:
            cached = scored_from_c24_cache(bias_col)
            if cached is None:
                raise FileNotFoundError(
                    f"neither {PANEL} nor {C24_FRAME} present; cannot compute null p for {label}"
                )
            b, bp, yy, n, src = cached
            out[label] = run_one(label, b, bp, yy, n, src, prior=prior.get(label))

    RESULTS_JSON.write_text(json.dumps(out, indent=2, default=str))
    print("\nWrote c2_c4_stratified_results.json")
    print("Compare against c2_c4_results.json (the original marginal-comparison run) --")
    print("do NOT overwrite it; both should be cited in the corrected Notice-log entries.")


if __name__ == "__main__":
    main()
