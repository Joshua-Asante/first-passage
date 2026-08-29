"""Candidate 1 -- daily-range-state-persistence on MNQ (full trading-day TR).

Reuses the FROZEN corrected-null battery verbatim:
  docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
Reference implementation copied byte-for-byte in method (not import, since GC/CL's
module lives outside this scratch dir and is instrument-specific) from:
  lab/analysis/_inbox/rangestate_corrected_2026-08/run_corrected_null.py
  lab/analysis/_inbox/rangestate_gc_2026-08/run_s1a.py

New instrument extension: MNQ is not GC(code=1) or CL(code=2). Assigns X_code=3,
disjoint from every burned seed block in the frozen spec's own inventory (linear
blocks 20260818+i and +5000/+6000/.../+12000; scalars 101/303/777/424242/555/
20260818-21; pilot 990000-990119) because those all key off GC/CL's own code
values inside the [20260818, X_code, i] triple -- a third X_code cannot collide
with a seed block that only ever combined with X_code in {1,2}. This is a NEW
LEAF under an unmodified frozen spec, not an amendment to it.

Object: TR_d = Wilder's True Range on the FULL trading-day OHLC (18:00 ET d-1 ->
17:00 ET d), matching GC/CL's own full-day (not RTH-only) daily bar. No roll
exclusion (see data_lib module docstring). No weekend filter needed (see same).
bias_d = 1{TR_d >= P80(TR_{d-60..d-1})}; y_{d+1} = 1{TR_{d+1} > P50(TR_{d-59..d})}.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data_lib import load_raw, daily_ohlc, wilders_tr  # noqa: E402

BASE_SEED = 20260818
X_CODE_MNQ = 3
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50
CI_BLOCK, CI_DRAWS, CI_SEED = 60, 4000, 42
N_FLOOR_POP, N_FLOOR_COND = 400, 100
YEAR_MIN_NCOND = 20
IAAFT_ITER = 100
ACF_LAGS = 60
TOL_MED, TOL_P95 = 0.04, 0.07
SIGNED_LAGS = (1, 2, 3, 5, 10, 20, 60)


def normal_scores(x: np.ndarray) -> np.ndarray:
    n = len(x)
    ranks = np.empty(n, dtype=float)
    ranks[np.argsort(x, kind="stable")] = np.arange(1, n + 1)
    return norm.ppf(ranks / (n + 1))


def iaaft(z: np.ndarray, rng: np.random.Generator, n_iter: int) -> np.ndarray:
    n = len(z)
    z_sorted = np.sort(z)
    target_amp = np.abs(np.fft.rfft(z))
    s = rng.permutation(z)
    for _ in range(n_iter):
        spec = np.fft.rfft(s)
        phases = np.angle(spec)
        s = np.fft.irfft(target_amp * np.exp(1j * phases), n)
        ranks = np.empty(n, dtype=int)
        ranks[np.argsort(s, kind="stable")] = np.arange(n)
        s = z_sorted[ranks]
    return s


def acf(x: np.ndarray, max_lag: int) -> np.ndarray:
    xc = x - x.mean()
    denom = float(np.dot(xc, xc))
    return np.array([float(np.dot(xc[:-k], xc[k:]) / denom) for k in range(1, max_lag + 1)])


def rolling_percentile_strict_prior(tr: np.ndarray, window: int, q: float) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(tr)
    out = np.full(n, np.nan)
    if n > window:
        wins = sliding_window_view(tr, window)
        out[window:] = np.percentile(wins[: n - window], q * 100, axis=1)
    return out


def rolling_percentile_through_today(tr: np.ndarray, window: int, q: float) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(tr)
    out = np.full(n, np.nan)
    if n >= window:
        wins = sliding_window_view(tr, window)
        out[window - 1:] = np.percentile(wins, q * 100, axis=1)
    return out


def block_bootstrap_ci_conditional(bias, y, block, n, seed, q=(2.5, 97.5)):
    rng = np.random.default_rng(seed)
    N = len(bias)
    eff_block = block if N >= block + 1 else max(1, N // 2)
    nblocks = int(np.ceil(N / eff_block))
    pool = np.arange(0, N)
    stats = []
    for _ in range(n):
        st = rng.choice(pool, size=nblocks)
        idx = (st[:, None] + np.arange(eff_block)[None, :]) % N
        idx = idx.ravel()[:N]
        bb, yy = bias[idx], y[idx]
        m = bb == 1
        if m.any():
            stats.append(float(yy[m].mean()))
    stats = np.asarray(stats)
    lo, hi = np.percentile(stats, q)
    return float(lo), float(hi)


def schreiber_end_match_trim(tr: np.ndarray, max_frac: float = 0.02):
    """Schreiber-Schmitz end-matching: FFT-based IAAFT implicitly treats the
    series as circular, so a large wraparound jump (x[0] vs x[n-1]) injects
    spurious high-frequency power into the target spectrum, degrading rank-ACF
    fidelity. Search trims from the END (0..max_frac*n samples) for the one
    minimizing the wraparound discontinuity |x[0] - x[n-1-k]|; return the
    trimmed series and how many points were dropped."""
    n = len(tr)
    max_trim = int(np.floor(max_frac * n))
    best_k, best_gap = 0, abs(tr[0] - tr[-1])
    for k in range(1, max_trim + 1):
        gap = abs(tr[0] - tr[n - 1 - k])
        if gap < best_gap:
            best_gap, best_k = gap, k
    trimmed = tr[: n - best_k] if best_k > 0 else tr
    return trimmed, best_k, best_gap


def build_tr():
    df = load_raw()
    daily = daily_ohlc(df)
    tr_full = wilders_tr(daily)
    valid = tr_full.dropna()
    return valid.to_numpy(), valid.index


def pipeline_stat(tr: np.ndarray):
    bias_thresh = rolling_percentile_strict_prior(tr, WINDOW, Q_BIAS)
    bias = (tr >= bias_thresh).astype(float)
    bias[np.isnan(bias_thresh)] = np.nan
    ref = rolling_percentile_through_today(tr, WINDOW, Q_REF)
    y = np.full(len(tr), np.nan)
    y[:-1] = (tr[1:] > ref[:-1]).astype(float)
    y[np.isnan(ref)] = np.nan
    scored = (~np.isnan(bias)) & (~np.isnan(y))
    b, yy = bias[scored].astype(int), y[scored].astype(int)
    m = b == 1
    obs = float(yy[m].mean()) if m.any() else float("nan")
    return obs, float(b.mean()), float(yy.mean()), scored, b, yy


def real_measurement(tr, idx):
    obs, f_bias1, p_up, scored, b, yy = pipeline_stat(tr)
    n_scored = int(scored.sum())
    n_cond = int(b.sum())
    days_s = idx[scored]
    lo, hi = block_bootstrap_ci_conditional(b, yy, CI_BLOCK, CI_DRAWS, CI_SEED)
    cond_idx = np.where(b == 1)[0]
    h = len(cond_idx) // 2
    y_cond_ordered = yy[cond_idx]
    halves = (float(y_cond_ordered[:h].mean()), float(y_cond_ordered[h:].mean())) if len(cond_idx) >= 2 else (np.nan, np.nan)
    years = np.array([d.year for d in days_s[b == 1]])
    by_year = {}
    for yr in sorted(set(years)):
        sel = years == yr
        by_year[int(yr)] = dict(n=int(sel.sum()), rate=float(y_cond_ordered[sel].mean()))
    limbs = dict(
        L1_n_floor=bool(n_scored >= N_FLOOR_POP and n_cond >= N_FLOOR_COND),
        L2_ci_lb=bool(lo > 0.50),
        L3_halves=bool(halves[0] > 0.50 and halves[1] > 0.50),
    )
    valid_years = {yr: v for yr, v in by_year.items() if v["n"] >= YEAR_MIN_NCOND}
    n_valid = len(valid_years)
    n_pass = sum(1 for v in valid_years.values() if v["rate"] > 0.50)
    if n_valid < 7:
        l4 = dict(n_valid=n_valid, n_pass=n_pass, required=None, verdict="AMBIGUOUS")
    else:
        required = n_valid - 2
        l4 = dict(n_valid=n_valid, n_pass=n_pass, required=required,
                  verdict="PASS" if n_pass >= required else "FAIL")
    return dict(obs=obs, f_bias1=f_bias1, p_up_unconditional=p_up,
                n_scored=n_scored, n_cond=n_cond, ci=(lo, hi), halves=halves,
                by_year=by_year, limbs=limbs, l4=l4)


def run_surrogates(tr, obs, M, seed_offset, tag, n_iter=IAAFT_ITER):
    z = normal_scores(tr)
    real_spear_acf = acf(rankdata(tr), ACF_LAGS)
    tr_sorted = np.sort(tr)
    rates = []
    spear_mismatch = []
    for i in range(M):
        rng = np.random.default_rng([BASE_SEED, X_CODE_MNQ, seed_offset + i])
        z_s = iaaft(z, rng, n_iter)
        ranks = np.empty(len(z_s), dtype=int)
        ranks[np.argsort(z_s, kind="stable")] = np.arange(len(z_s))
        tr_s = tr_sorted[ranks]
        assert np.array_equal(np.sort(tr_s), tr_sorted), "multiset identity violated"
        s_spear_acf = acf(rankdata(tr_s), ACF_LAGS)
        spear_mismatch.append(float(np.max(np.abs(s_spear_acf - real_spear_acf))))
        r, _, _, _, _, _ = pipeline_stat(tr_s)
        rates.append(r)
    rates = np.array(rates)
    spear_mm = np.array(spear_mismatch)
    diag = dict(
        M=M, iterations=n_iter, domain="normal-scores",
        seed_policy=f"default_rng([{BASE_SEED}, {X_CODE_MNQ}, {seed_offset}+i])",
        spearman_acf_mismatch=dict(med=float(np.median(spear_mm)), p95=float(np.percentile(spear_mm, 95)),
                                    max=float(spear_mm.max())),
        tolerance=dict(med_limit=TOL_MED, p95_limit=TOL_P95, gating_domain="spearman-rank-acf"),
        gate="PASS" if (np.median(spear_mm) <= TOL_MED and np.percentile(spear_mm, 95) <= TOL_P95) else "FAIL",
    )
    diag_path = HERE / f"diagnostics_MNQ_{tag}.json"
    diag_path.write_text(json.dumps(diag, indent=1))
    p_upper = (1 + int((rates >= obs).sum())) / (M + 1)
    p_lower = (1 + int((rates <= obs).sum())) / (M + 1)
    pct_obs = float((rates < obs).mean() * 100)
    return dict(diag=diag, rates=rates.tolist(), p_upper=p_upper, p_lower=p_lower, pct_obs=pct_obs)


def main():
    tr, idx = build_tr()
    print(f"n valid TR days: {len(tr)}  span {idx.min()} -> {idx.max()}")
    meas = real_measurement(tr, idx)
    print(f"obs gateHit = {meas['obs']:.4f}  n_scored={meas['n_scored']} n_cond={meas['n_cond']}")
    print(f"CI={meas['ci']}  halves={meas['halves']}  limbs={meas['limbs']}  L4={meas['l4']}")

    # Pilot verification (spec D6: implementation + adversarial verification on PILOT
    # seeds only, before the official block is drawn).
    pilot = run_surrogates(tr, meas["obs"], M=200, seed_offset=990000, tag="pilot")
    print(f"\nPILOT (M=200): gate={pilot['diag']['gate']} "
          f"med={pilot['diag']['spearman_acf_mismatch']['med']:.4f} "
          f"p95={pilot['diag']['spearman_acf_mismatch']['p95']:.4f} "
          f"p_upper={pilot['p_upper']:.4f} p_lower={pilot['p_lower']:.4f} pct={pilot['pct_obs']:.1f}")

    official_iter = IAAFT_ITER
    ladder_note = None
    if pilot["diag"]["gate"] != "PASS":
        print("PILOT DIAGNOSTIC GATE FAIL at iter=100 -> escalation ladder step 1: iter=500 (same pilot seeds).")
        pilot2 = run_surrogates(tr, meas["obs"], M=200, seed_offset=990000, tag="pilot_iter500", n_iter=500)
        print(f"PILOT@iter500 (M=200): gate={pilot2['diag']['gate']} "
              f"med={pilot2['diag']['spearman_acf_mismatch']['med']:.4f} "
              f"p95={pilot2['diag']['spearman_acf_mismatch']['p95']:.4f}")
        if pilot2["diag"]["gate"] != "PASS":
            print("PILOT@iter500 STILL FAIL -> escalation ladder step 2: Schreiber end-matching trim (<=2% of record).")
            trimmed, trim_k, trim_gap = schreiber_end_match_trim(tr, max_frac=0.02)
            print(f"end-match search: best trim k={trim_k} (of max {int(0.02*len(tr))}), "
                  f"wraparound gap={trim_gap:.4f} (untrimmed gap={abs(tr[0]-tr[-1]):.4f})")
            trim_result = dict(trim_k=trim_k, trim_gap=trim_gap, untrimmed_gap=float(abs(tr[0] - tr[-1])))
            if trim_k == 0:
                print("Trim search found NO offset within 2% of record improving the wraparound "
                      "discontinuity -> escalation ladder exhausted. VOID per spec §3 CASE V.")
                out = dict(measurement=meas, pilot=pilot, pilot_iter500=pilot2, trim_search=trim_result,
                           official=None,
                           verdict="VOID (spec CASE V) -- diagnostic-gate FAIL at iter=100 and iter=500; "
                                   "Schreiber end-matching trim search found no improving offset within "
                                   "2% of record. Per spec, this VOIDs the L5 attribution limb: no p_upper/"
                                   "p_lower may be quoted. Pre-named remedy (a different surrogate class, "
                                   "e.g. ARFIMA/FGN or GARCH-fitted) is a fresh design decision (O5), out "
                                   "of scope for this Notice-phase session.")
                (HERE / "candidate1_results.json").write_text(json.dumps(out, indent=1, default=str))
                return
            pilot3 = run_surrogates(trimmed, meas["obs"], M=200, seed_offset=990000, tag="pilot_trimmed", n_iter=100)
            print(f"PILOT@trimmed (M=200): gate={pilot3['diag']['gate']} "
                  f"med={pilot3['diag']['spearman_acf_mismatch']['med']:.4f} "
                  f"p95={pilot3['diag']['spearman_acf_mismatch']['p95']:.4f}")
            if pilot3["diag"]["gate"] != "PASS":
                print("PILOT@trimmed STILL FAIL -> escalation ladder exhausted. VOID per spec §3 CASE V.")
                out = dict(measurement=meas, pilot=pilot, pilot_iter500=pilot2, trim_search=trim_result,
                           pilot_trimmed=pilot3, official=None,
                           verdict="VOID (spec CASE V) -- diagnostic-gate FAIL at iter=100, iter=500, and "
                                   "after Schreiber end-matching trim. Escalation ladder exhausted; no "
                                   "p_upper/p_lower may be quoted.")
                (HERE / "candidate1_results.json").write_text(json.dumps(out, indent=1, default=str))
                return
            tr = trimmed  # use the passing trimmed series for the official draw
        official_iter = 500
        ladder_note = "escalated to iter=500 after iter=100 pilot diagnostic-gate FAIL (spec §1 escalation ladder step 1)"

    # Official (single execution, frozen seed block 0..999).
    official = run_surrogates(tr, meas["obs"], M=1000, seed_offset=0, tag="official", n_iter=official_iter)
    print(f"\nOFFICIAL (M=1000): gate={official['diag']['gate']} "
          f"med={official['diag']['spearman_acf_mismatch']['med']:.4f} "
          f"p95={official['diag']['spearman_acf_mismatch']['p95']:.4f} "
          f"p_upper={official['p_upper']:.4f} p_lower={official['p_lower']:.4f} pct={official['pct_obs']:.1f}")

    presence_pass = meas["limbs"]["L1_n_floor"] and meas["limbs"]["L2_ci_lb"] and meas["limbs"]["L3_halves"] \
        and (meas["l4"]["verdict"] == "PASS")
    if official["diag"]["gate"] != "PASS":
        verdict = "VOID-PENDING-LADDER"
    elif meas["l4"]["verdict"] == "AMBIGUOUS":
        verdict = "AMBIGUOUS"
    elif presence_pass:
        verdict = "SIGNAL-EXCESS" if official["p_upper"] <= 0.05 else "SIGNAL-GENERIC"
    else:
        driving = [k for k, v in (("L1", meas["limbs"]["L1_n_floor"]), ("L2", meas["limbs"]["L2_ci_lb"]),
                                  ("L3", meas["limbs"]["L3_halves"]), ("L4", meas["l4"]["verdict"] == "PASS")) if not v]
        verdict = f"NULL (driving: {','.join(driving)})"

    print(f"\nVERDICT: {verdict}")
    out = dict(measurement=meas, pilot=pilot, official=official, verdict=verdict, ladder_note=ladder_note)
    (HERE / "candidate1_results.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
