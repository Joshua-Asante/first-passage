"""Positive control for the joint-surrogation null (joint_iaaft.py) -- Phase 1
self-verification, mirroring the frozen spec's own AR(1) positive control
(docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md §1:
"20 zero-mechanism AR(1) replicates each scored against its own IAAFT band ->
1/20 at p_upper <= 0.05 ... vs the invalidated block-shuffle's 20/20
false-clear"). That precedent is exactly why this check exists BEFORE any
real-data scoring: a null design that always clears (or never clears) is
worthless regardless of how principled its derivation sounds on paper.

Two synthetic scenarios, same generative family, N_REPS replicates each:

  NULL scenario (H0 true by construction): overnight_t and rth_t are both
  driven by a SHARED AR(1) regime factor plus independent own-series AR(1)
  idiosyncratic noise -- exactly the "mundane shared regime, no genuine
  transmission" story this design exists to null out. Expected: the joint-
  surrogation null's p_upper should reject (p_upper <= 0.05) at close to the
  nominal 5% rate across replicates.

  ALTERNATIVE scenario (H1 true by construction): identical generative
  process, PLUS a genuine same-day incremental term (rth_t gets an extra
  additive contribution from a component of overnight_t NOT explained by
  the shared regime) -- a real transmission effect layered on top of the
  same mundane confound. Expected: the joint-surrogation null should reject
  at a materially higher rate than the null scenario (power).

Deliberately smaller than a final scored run (M=200 not 1000, n_iter=50 not
100, N_REPS=20 matching the frozen spec's own replicate count) -- this is a
$0 design-verification pass, not Phase 3 execution; K is not spent.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from joint_iaaft import generate_joint_surrogates  # noqa: E402

N_DAYS = 1500          # matches real Q-RANGEXFER-1 panel order of magnitude
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50   # SAME convention as candidate2_overnight_rth_transfer.py
M_SANITY = 200          # smaller than a final M=1000 scored run
N_ITER_SANITY = 50      # smaller than the frozen spec's own 100 (measured-sufficient there)
N_REPS = 20             # matches the frozen spec's own AR(1) positive-control replicate count
ALPHA = 0.05


def rolling_pct_strict_prior(x, window, q):
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(x)
    out = np.full(n, np.nan)
    if n > window:
        wins = sliding_window_view(x, window)
        out[window:] = np.percentile(wins[: n - window], q * 100, axis=1)
    return out


def score_min_stratified_lift(overnight, rth, window=WINDOW, q_bias=Q_BIAS, q_ref=Q_REF):
    """Reproduces candidate2_overnight_rth_transfer.py's exact bias/bias_prime/y
    construction and min-stratified-lift statistic, generalized to take raw
    (overnight, rth) series directly -- usable on real data (as a byte-check
    against the known committed figures) or on any synthetic/surrogate pair."""
    n = len(overnight)
    bias = (overnight >= rolling_pct_strict_prior(overnight, window, q_bias)).astype(float)
    bias[np.isnan(rolling_pct_strict_prior(overnight, window, q_bias))] = np.nan

    bias_prime = (rth >= rolling_pct_strict_prior(rth, window, q_bias)).astype(float)
    bias_prime[np.isnan(rolling_pct_strict_prior(rth, window, q_bias))] = np.nan
    bias_prime_shifted = np.full(n, np.nan)
    bias_prime_shifted[1:] = bias_prime[:-1]

    ref = rolling_pct_strict_prior(rth, window, q_ref)
    y = (rth > ref).astype(float)
    y[np.isnan(ref)] = np.nan

    scored = (~np.isnan(bias)) & (~np.isnan(bias_prime_shifted)) & (~np.isnan(y))
    b = bias[scored].astype(int)
    bp = bias_prime_shifted[scored].astype(int)
    yy = y[scored].astype(int)

    vals = []
    for s in (0, 1):
        m = bp == s
        hi_mask, lo_mask = m & (b == 1), m & (b == 0)
        if hi_mask.any() and lo_mask.any():
            vals.append(float(yy[hi_mask].mean() - yy[lo_mask].mean()))
    min_lift = min(vals) if vals else float("nan")
    return min_lift, int(scored.sum())


def gen_ar1(n, phi, sigma, rng):
    x = np.empty(n)
    x[0] = rng.normal(0, sigma / np.sqrt(1 - phi ** 2))
    for t in range(1, n):
        x[t] = phi * x[t - 1] + rng.normal(0, sigma)
    return x


def synth_pair(n, rng, transmission_strength=0.0):
    """NULL (transmission_strength=0): shared AR(1) regime + independent own
    AR(1) idiosyncratic noise on each channel -- mundane co-movement only.
    ALTERNATIVE (transmission_strength>0): adds a genuine same-day
    incremental term from a component of `overnight` orthogonal to the
    shared regime into `rth`, over and above the mundane confound."""
    regime = gen_ar1(n, phi=0.85, sigma=1.0, rng=rng)
    idio1 = gen_ar1(n, phi=0.3, sigma=1.0, rng=rng)
    idio2 = gen_ar1(n, phi=0.3, sigma=1.0, rng=rng)
    overnight = regime + idio1
    rth = regime + idio2
    if transmission_strength > 0:
        # genuine transmission: rth gets an extra push from idio1 (the part of
        # `overnight` NOT shared with rth's own regime/idiosyncratic terms) --
        # a real same-day incremental effect, not just shared-regime co-movement.
        rth = rth + transmission_strength * idio1
    # map to strictly-positive "range-like" values (exp transform), matching
    # the real construct's own domain -- avoids negative "ranges" that would
    # never occur in real bar data and could interact oddly with percentile
    # thresholds near 0.
    return np.exp(overnight * 0.3), np.exp(rth * 0.3)


def run_scenario(name, transmission_strength, seed_base):
    rejects = 0
    p_uppers = []
    for rep in range(N_REPS):
        rng_data = np.random.default_rng([seed_base, 900, rep])
        overnight, rth = synth_pair(N_DAYS, rng_data, transmission_strength)
        obs, n_scored = score_min_stratified_lift(overnight, rth)
        if not np.isfinite(obs):
            print(f"  rep {rep}: obs undefined (insufficient scored days), skipped")
            continue
        pairs, diag = generate_joint_surrogates(overnight, rth, M_SANITY,
                                                 seed_base=seed_base + 7000, code=rep)
        null_lifts = []
        for x1_s, x2_s in pairs:
            lift_s, _ = score_min_stratified_lift(x1_s, x2_s)
            if np.isfinite(lift_s):
                null_lifts.append(lift_s)
        null_lifts = np.asarray(null_lifts)
        p_upper = (1 + int((null_lifts >= obs).sum())) / (len(null_lifts) + 1)
        p_uppers.append(p_upper)
        rejects += int(p_upper <= ALPHA)
        gate_flag = "" if diag["gate"] == "PASS" else "  [DIAGNOSTIC GATE FAIL]"
        print(f"  rep {rep}: obs={obs:+.4f}  n_scored={n_scored}  p_upper={p_upper:.4f}"
              f"  crosscorr0(real)={diag['crosscorr0']['real']:.3f}{gate_flag}")
    rate = rejects / len(p_uppers) if p_uppers else float("nan")
    print(f"\n[{name}] reject rate at alpha={ALPHA}: {rejects}/{len(p_uppers)} = {rate:.3f}\n")
    return rate, p_uppers


def main():
    print("=== NULL scenario (H0 true: shared regime only, no genuine transmission) ===")
    null_rate, null_ps = run_scenario("NULL", transmission_strength=0.0, seed_base=20260830)

    print("=== ALTERNATIVE scenario (H1 true: genuine transmission on top of the same confound) ===")
    # transmission_strength chosen to be a MODERATE, not overwhelming, effect --
    # power at a moderate effect size is the informative check, not power at an
    # effect so large any test would find it.
    alt_rate, alt_ps = run_scenario("ALTERNATIVE", transmission_strength=0.6, seed_base=20260831)

    print("=== VERDICT ===")
    print(f"NULL false-positive rate: {null_rate:.3f} (target: close to {ALPHA})")
    print(f"ALTERNATIVE power: {alt_rate:.3f} (target: materially > {ALPHA} and > null rate)")
    size_ok = null_rate <= 3 * ALPHA  # generous band -- N_REPS=20 gives coarse resolution
    power_ok = alt_rate > null_rate + 0.15
    print(f"Size control acceptable (null_rate <= {3*ALPHA:.2f}): {size_ok}")
    print(f"Power acceptable (alt_rate exceeds null_rate by >0.15): {power_ok}")
    print(f"POSITIVE CONTROL: {'PASS' if (size_ok and power_ok) else 'FAIL -- design needs revision before Phase 2 review'}")


if __name__ == "__main__":
    main()
