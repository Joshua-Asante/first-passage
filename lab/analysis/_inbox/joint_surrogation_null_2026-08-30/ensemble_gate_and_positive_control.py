"""Ensemble/percentile-based goodness-of-fit diagnostic for the ARFIMA(1,d,0)
+ Gaussian-copula (innovation_link) joint surrogation null in
longmemory_copula.py, PLUS the full positive control that actually arbitrates
whether the design is usable -- per this session's task brief.

BACKGROUND (read longmemory_copula.py in full before reading this file): that
module was scored against a FIXED per-draw tolerance (max|surrogate_ACF -
real_ACF| over lags 1..30, med<=0.04/p95<=0.07) borrowed unmodified from the
IAAFT-battery context (iaaft_battery.py / joint_iaaft.py), and FAILED it. But
the module's own indirect-inference / simulated-method-of-moments calibration
(estimate_phi_d_simulated) showed the MEAN surrogate ACF across many draws
tracks the real ACF within ~0.02-0.07 at every lag -- i.e. correctly specified
ON AVERAGE. A fixed per-draw tolerance cannot distinguish "wrong model" from
"right model, one unlucky draw at n=1487 for a d~0.4-0.46 near-nonstationary
process" -- both produce the same FAIL. This file replaces that diagnostic
with a standard simulation-based goodness-of-fit check (Step 1) and, more
importantly, tests the actual operating characteristics of the resulting
procedure with a positive control (Step 2) and a disclosed exploratory-only
run against real data (Step 3).

STEP 1 -- ensemble/percentile diagnostic
-----------------------------------------
Generate M>=100 surrogate draws. For each lag k in 1..min(30,n//3), take the
surrogate ACF's OWN distribution across the M draws (its 2.5/97.5 percentile
band) and check whether the REAL series' ACF at lag k falls inside it. Report
the fraction of lags in-band, per channel. Same idea for the lag-0 cross-
correlation (single band, single check, since that is the one cross-channel
quantity this model class targets -- see longmemory_copula.py's own "WHAT
THIS NULL ACTUALLY TESTS" section: a lag-0 Gaussian-copula link, not a lagged
cross-correlation function).

THRESHOLD, chosen and justified BEFORE looking at the result: under a
correctly-specified model, each individual lag is (by construction of a
95% band) expected to miss about 5% of the time -- with 30 roughly-
independent-ish tests, ~1-2 misses out of 30 is the "typical" outcome for a
perfect model, not 0. But adjacent lags of a long-memory / near-nonstationary
series are themselves strongly autocorrelated, so misses will tend to cluster
rather than behave like 30 independent Bernoulli(0.05) draws, and the bands
are themselves estimated from a finite M (~100-120) surrogate draws, adding
percentile-estimation noise to the band edges. Both effects push the
"typical miss count under a correct model" above the naive ~1.5/30. We
therefore set the pass bar at >=80% of lags in-band (i.e. tolerate up to 6/30
misses per channel) -- generous enough to absorb clustering + finite-M noise,
but still a real bar (a materially misspecified model, like the VAR(p)
construction RESULTS.md already measured at own-ACF mismatch 3x the old
tolerance, would not come close to clearing 80%). This threshold is fixed
here, before the number below is computed, and is not adjusted afterward.

STEP 2 -- positive control (the real arbiter)
-----------------------------------------------
Two synthetic ~1500-day scenarios built directly on the fitted real-data
ARFIMA(1,d,0) filters (psi1, psi2) and the real-data-implied rho_innov,
cached by _fit_real_params.py, so the synthetic scenarios reproduce the real
panel's own long-memory ACF shape and lag-0 cross-correlation as closely as
practical:

  NULL:  z1_t, z2_t drawn from EXACTLY the innovation_link generative model
  itself (temporally-white, contemporaneously-correlated Gaussian innovations
  e1,e2 filtered through the real-fitted psi1,psi2) -- "a shared persistent
  process with no genuine extra same-day transmission beyond it," where the
  shared persistence + constant same-day linear link IS the null's own
  assumed structure. This checks the procedure's SIZE when its own model is
  exactly true (a standard simulation-based-calibration self-consistency
  check) -- necessary but NOT sufficient on its own (a design that always
  agrees with itself is uninformative about power).

  ALTERNATIVE: identical to NULL, PLUS a genuine incremental same-day effect
  that the null's linear Gaussian-copula model class CANNOT express: on days
  where channel-1's own normal-score realization is in its top quintile
  (mirroring the real stage-1 statistic's own P80 overnight-bias threshold),
  channel-2's normal score gets an added constant boost. A Gaussian copula
  has zero tail dependence by construction, so this is a real "beyond the
  null's own model class" mechanism, not just a bigger version of the same
  linear correlation the null already contains -- this is what makes the
  power check non-circular (the null and alternative differ in *functional
  form* of the linkage, not merely in a parameter the null model already
  fits).

Both scenarios' raw values are produced via the module's own
`_remap_to_raw` against the REAL x1,x2 arrays, so the marginal distributions
(heavily right-skewed range data) match the real panel exactly; only the
DEPENDENCE structure differs between NULL and ALTERNATIVE.

For each replicate: compute the actual Q-RANGEXFER-1 stage-1 statistic (the
min-stratified-lift from candidate2_overnight_rth_transfer.py, reproduced
here verbatim from positive_control.py's own `score_min_stratified_lift`,
already used for exactly this purpose in the prior VAR(p)/IAAFT positive
control), generate M>=100 surrogate draws, compute p_upper, and record
whether p_upper<=0.05.

COMPUTE-BUDGET SIMPLIFICATION (disclosed): the per-replicate surrogate draws
are generated with phi1/d1/phi2/d2 FIXED to the real-fitted values (skipping
the expensive per-replicate SMM re-calibration grid search). This is
appropriate here because the positive control's purpose is to test the
GATE/STATISTIC/REJECTION-RATE machinery given a known-correct dynamics model,
not to re-validate the calibration step itself (already checked separately,
see longmemory_copula.py's own docstring/run log) -- re-fitting (phi,d) fresh
per replicate would cost ~30x more compute for a question this design
doesn't need answered here.

STEP 3 -- exploratory-only real-data illustration
----------------------------------------------------
Run the SAME construction once against the real candidate24_joint_frame.csv
and report p_upper for the real observed stage-1 statistic. Explicitly NOT a
scored Phase-3 verdict.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from longmemory_copula import (  # noqa: E402
    acf, rankdata, ar1_fracdiff_weights, _pair_innovation_link, _remap_to_raw,
    _simulate_channel_from_psi, generate_joint_surrogates,
)
from positive_control import rolling_pct_strict_prior  # noqa: E402

CSV = HERE.parent / "mnq_dailygeom_notice_2026-08-29" / "candidate24_joint_frame.csv"
FIT_CACHE = HERE / "_real_fit_cache.json"

WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50   # SAME as candidate2_overnight_rth_transfer.py
ALPHA = 0.05
IN_BAND_FRAC_THRESHOLD = 0.80   # chosen + justified in module docstring, BEFORE seeing results


def score_min_stratified_lift(overnight, rth, window=WINDOW, q_bias=Q_BIAS, q_ref=Q_REF):
    """Verbatim logic from positive_control.py's own function of the same
    name (which itself reproduces candidate2_overnight_rth_transfer.py's
    exact bias/bias_prime/y construction) -- not re-derived here."""
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


# ---------------------------------------------------------------------------
# STEP 1 -- ensemble/percentile diagnostic
# ---------------------------------------------------------------------------

def ensemble_percentile_gate(x1, x2, psi1, psi2, rho_innov, M, seed_base, code, J, burn, lags):
    n = len(x1)
    r1, r2 = rankdata(x1), rankdata(x2)
    real_acf1 = acf(r1, lags)
    real_acf2 = acf(r2, lags)
    real_crosscorr0 = float(np.corrcoef(r1, r2)[0, 1])

    surr_acf1 = np.empty((M, lags))
    surr_acf2 = np.empty((M, lags))
    surr_crosscorr0 = np.empty(M)
    for i in range(M):
        rng = np.random.default_rng([seed_base, code, i])
        x1_s, x2_s = _pair_innovation_link(x1, x2, psi1, psi2, J, burn, rng, rho_innov)
        s_r1, s_r2 = rankdata(x1_s), rankdata(x2_s)
        surr_acf1[i] = acf(s_r1, lags)
        surr_acf2[i] = acf(s_r2, lags)
        surr_crosscorr0[i] = np.corrcoef(s_r1, s_r2)[0, 1]

    lo1, hi1 = np.percentile(surr_acf1, [2.5, 97.5], axis=0)
    lo2, hi2 = np.percentile(surr_acf2, [2.5, 97.5], axis=0)
    in_band1 = (real_acf1 >= lo1) & (real_acf1 <= hi1)
    in_band2 = (real_acf2 >= lo2) & (real_acf2 <= hi2)
    frac1 = float(in_band1.mean())
    frac2 = float(in_band2.mean())

    lo_c, hi_c = np.percentile(surr_crosscorr0, [2.5, 97.5])
    crosscorr_in_band = bool(lo_c <= real_crosscorr0 <= hi_c)

    gate_passed = bool(frac1 >= IN_BAND_FRAC_THRESHOLD and frac2 >= IN_BAND_FRAC_THRESHOLD
                        and crosscorr_in_band)

    return dict(
        M=M, lags=lags, threshold=IN_BAND_FRAC_THRESHOLD,
        frac_in_band_channel1=frac1, frac_in_band_channel2=frac2,
        crosscorr_in_band=crosscorr_in_band,
        real_crosscorr0=real_crosscorr0, crosscorr_band=[float(lo_c), float(hi_c)],
        per_lag_channel1=dict(real=real_acf1.tolist(), band_lo=lo1.tolist(), band_hi=hi1.tolist(),
                               in_band=in_band1.tolist()),
        per_lag_channel2=dict(real=real_acf2.tolist(), band_lo=lo2.tolist(), band_hi=hi2.tolist(),
                               in_band=in_band2.tolist()),
        gate_passed=gate_passed,
    )


# ---------------------------------------------------------------------------
# STEP 2 -- positive control
# ---------------------------------------------------------------------------

def synth_pair(x1_real, x2_real, psi1, psi2, J, burn, rng, rho_innov, transmission_boost=0.0):
    """NULL (transmission_boost=0): x1_s,x2_s are one honest draw from the
    innovation_link generative model itself (shared long-memory dynamics +
    constant lag-0 Gaussian-copula link) -- "no genuine extra same-day
    transmission beyond" that shared structure.

    ALTERNATIVE (transmission_boost>0): identical, PLUS a genuine incremental
    same-day effect defined on the SAME conditioning variable the real
    stage-1 statistic actually uses -- trailing-60-day P80 overnight-range
    bias (bias_overnight_d = 1{on_range_d >= P80(on_range_{d-60..d-1})}),
    not a marginal/population quantile of the innovation (an earlier probe
    using a marginal-quantile boost on the normal-score barely moved the
    scored statistic at all: mean lift ~0.43-0.46 flat across boost 0.5-2.5,
    because trailing-window bias and population-quantile bias pick out
    materially different day-sets under long memory -- sustained regimes
    mean a population-top-quintile day is often NOT a trailing-top-quintile
    day. Tying the boost to the actual conditioning variable is what makes
    this a direct test of whether the ensemble/positive-control machinery
    can detect a real effect on exactly the dimension the real test scores).
    On days flagged by that trailing rule, x2_s (RTH range) is scaled up by
    a factor (1+transmission_boost) -- a genuine, mechanism-shaped, physically
    interpretable same-day transmission (bigger overnight range -> bigger RTH
    range same day, beyond the shared regime + linear copula link alone)."""
    n = len(x1_real)
    e1 = rng.standard_normal(n + burn)
    e2 = rho_innov * e1 + np.sqrt(max(0.0, 1 - min(abs(rho_innov), 1.0) ** 2)) * rng.standard_normal(n + burn)
    z1 = _simulate_channel_from_psi(psi1, n, burn, e1)
    z2 = _simulate_channel_from_psi(psi2, n, burn, e2)
    x1_s = _remap_to_raw(z1, x1_real)
    x2_s = _remap_to_raw(z2, x2_real)
    if transmission_boost > 0:
        thresh = rolling_pct_strict_prior(x1_s, WINDOW, Q_BIAS)
        extreme = (x1_s >= thresh) & ~np.isnan(thresh)
        x2_s = x2_s * (1.0 + transmission_boost * extreme.astype(float))
    return x1_s, x2_s


def run_scenario(name, x1_real, x2_real, psi1, psi2, rho_innov, transmission_boost, n_reps, M,
                  J, burn, seed_base):
    rejects, p_uppers, obs_list = 0, [], []
    for rep in range(n_reps):
        rng_data = np.random.default_rng([seed_base, 900, rep])
        x1_rep, x2_rep = synth_pair(x1_real, x2_real, psi1, psi2, J, burn, rng_data, rho_innov,
                                     transmission_boost=transmission_boost)
        obs, n_scored = score_min_stratified_lift(x1_rep, x2_rep)
        if not np.isfinite(obs):
            print(f"  [{name}] rep {rep}: obs undefined, skipped")
            continue
        pairs, diag = generate_joint_surrogates(
            x1_rep, x2_rep, M=M, seed_base=seed_base + 5000, code=rep, method="innovation_link",
            phi1=psi1_phi, d1=psi1_d, phi2=psi2_phi, d2=psi2_d, J=J, burn=burn,
        )
        null_lifts = []
        for xs1, xs2 in pairs:
            lift_s, _ = score_min_stratified_lift(xs1, xs2)
            if np.isfinite(lift_s):
                null_lifts.append(lift_s)
        null_lifts = np.asarray(null_lifts)
        p_upper = (1 + int((null_lifts >= obs).sum())) / (len(null_lifts) + 1)
        p_uppers.append(p_upper)
        obs_list.append(obs)
        rejects += int(p_upper <= ALPHA)
        print(f"  [{name}] rep {rep}: obs={obs:+.4f} n_scored={n_scored} n_surr={len(null_lifts)} "
              f"p_upper={p_upper:.4f}")
    rate = rejects / len(p_uppers) if p_uppers else float("nan")
    print(f"[{name}] reject rate @alpha={ALPHA}: {rejects}/{len(p_uppers)} = {rate:.3f}  "
          f"(mean obs={np.mean(obs_list):+.4f})\n")
    return rate, p_uppers, obs_list


def main():
    df = pd.read_csv(CSV)
    x1 = df["on_range"].to_numpy()
    x2 = df["rth_range"].to_numpy()
    n = len(x1)
    fit = json.loads(FIT_CACHE.read_text())
    global psi1_phi, psi1_d, psi2_phi, psi2_d
    psi1_phi, psi1_d = fit["phi1"], fit["d1"]
    psi2_phi, psi2_d = fit["phi2"], fit["d2"]
    rho_innov = fit["rho_innov_clipped"]
    J, burn = fit["J"], fit["burn"]
    lags = fit["lags"]
    print(f"n={n} lags={lags} phi1={psi1_phi:.4f} d1={psi1_d:.4f} phi2={psi2_phi:.4f} d2={psi2_d:.4f} "
          f"rho_innov={rho_innov:.4f} J={J} burn={burn}")

    psi1 = ar1_fracdiff_weights(psi1_phi, psi1_d, J)
    psi2 = ar1_fracdiff_weights(psi2_phi, psi2_d, J)

    # ---------------- STEP 1: ensemble/percentile diagnostic on REAL data ----------------
    print("\n" + "=" * 70)
    print("STEP 1 -- ensemble/percentile diagnostic (real data, M=120)")
    t0 = time.time()
    gate = ensemble_percentile_gate(x1, x2, psi1, psi2, rho_innov, M=120, seed_base=42, code=1,
                                     J=J, burn=burn, lags=lags)
    print(f"  ({time.time()-t0:.1f}s)")
    print(f"  frac_in_band channel1 (on_range)  = {gate['frac_in_band_channel1']:.3f}")
    print(f"  frac_in_band channel2 (rth_range) = {gate['frac_in_band_channel2']:.3f}")
    print(f"  crosscorr0 real={gate['real_crosscorr0']:.4f}  band={gate['crosscorr_band']}  "
          f"in_band={gate['crosscorr_in_band']}")
    print(f"  threshold={gate['threshold']}  GATE PASSED = {gate['gate_passed']}")

    # ---------------- STEP 2: positive control ----------------
    print("\n" + "=" * 70)
    print("STEP 2 -- positive control")
    N_REPS, M_PC = 20, 100
    null_rate, null_ps, null_obs = run_scenario("NULL", x1, x2, psi1, psi2, rho_innov,
                                                 transmission_boost=0.0, n_reps=N_REPS, M=M_PC,
                                                 J=J, burn=burn, seed_base=20260830)

    # transmission_boost=0.4 (a 40% RTH-range scale-up specifically on days
    # flagged by the SAME trailing-P80 overnight-bias rule the real stage-1
    # statistic conditions on): chosen from a small pre-registered-in-spirit
    # probe (10 reps/scenario, M=100, boost in {0.2,0.3,0.4,0.6}; NULL
    # rejected 0/10, boost=0.2/0.3/0.4/0.6 rejected 2/4/6/6 out of 10) BEFORE
    # this final N_REPS=20 run -- picked as the smallest probed value giving
    # a clearly-detectable (>=50%) reject rate, i.e. a moderate, not
    # maximal, effect. A first probe attempt using a marginal-quantile boost
    # (see synth_pair docstring) barely moved the statistic at all (flat
    # 0.43-0.46 across boost 0.5-2.5) and was abandoned in favor of tying the
    # boost to the actual trailing conditioning variable the real statistic
    # uses -- disclosed in synth_pair's own docstring, not silently dropped.
    boost = 0.4
    alt_rate, alt_ps, alt_obs = run_scenario("ALTERNATIVE", x1, x2, psi1, psi2, rho_innov,
                                              transmission_boost=boost, n_reps=N_REPS, M=M_PC,
                                              J=J, burn=burn, seed_base=20260831)

    size_ok = null_rate <= 0.15   # generous band given N_REPS=20 coarse resolution (3x nominal)
    power_ok = alt_rate >= null_rate + 0.30
    print("=== POSITIVE CONTROL VERDICT ===")
    print(f"NULL false-positive rate: {null_rate:.3f} (target: close to {ALPHA})")
    print(f"ALTERNATIVE power: {alt_rate:.3f} (target: materially > null rate)")
    print(f"size_ok (null_rate<=0.15): {size_ok}   power_ok (alt_rate>=null_rate+0.30): {power_ok}")

    # ---------------- STEP 3: exploratory-only real-data p_upper ----------------
    print("\n" + "=" * 70)
    print("STEP 3 -- EXPLORATORY ONLY, NOT A SCORED VERDICT -- real data p_upper")
    obs_real, n_scored_real = score_min_stratified_lift(x1, x2)
    pairs_real, diag_real = generate_joint_surrogates(
        x1, x2, M=120, seed_base=99, code=0, method="innovation_link",
        phi1=psi1_phi, d1=psi1_d, phi2=psi2_phi, d2=psi2_d, J=J, burn=burn,
    )
    real_null_lifts = []
    for xs1, xs2 in pairs_real:
        lift_s, _ = score_min_stratified_lift(xs1, xs2)
        if np.isfinite(lift_s):
            real_null_lifts.append(lift_s)
    real_null_lifts = np.asarray(real_null_lifts)
    p_upper_real = (1 + int((real_null_lifts >= obs_real).sum())) / (len(real_null_lifts) + 1)
    print(f"  real observed stage-1 stat = {obs_real:+.4f} (n_scored={n_scored_real})")
    print(f"  surrogate null lift: mean={real_null_lifts.mean():+.4f} "
          f"sd={real_null_lifts.std():.4f} n={len(real_null_lifts)}")
    print(f"  p_upper (EXPLORATORY ONLY) = {p_upper_real:.4f}")

    out = dict(
        n=n, lags=lags,
        gate=gate,
        positive_control=dict(
            n_reps=N_REPS, M=M_PC, alpha=ALPHA,
            null_rate=null_rate, null_p_uppers=null_ps,
            alt_rate=alt_rate, alt_p_uppers=alt_ps, transmission_boost=boost,
            size_ok=size_ok, power_ok=power_ok,
        ),
        exploratory_real=dict(
            obs=obs_real, n_scored=n_scored_real, p_upper=p_upper_real,
            note="EXPLORATORY ONLY -- not a certified Phase 3 result",
        ),
    )
    (HERE / "ensemble_gate_and_positive_control_results.json").write_text(json.dumps(out, indent=2))
    print("\nWrote ensemble_gate_and_positive_control_results.json")


if __name__ == "__main__":
    main()
