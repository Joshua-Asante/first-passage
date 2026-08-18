"""Corrected-null re-score of S1a (GC) and S1b (CL) under the frozen class battery.

Spec (FROZEN, committed before any official scoring surrogate is drawn):
    docs/spec/2026-08-18-magnitude-persistence-corrected-null-battery.md
Incident: docs/notes/audits/2026-08-18-block-shuffle-placebo-does-not-control-for-tr-autocorrelation.md

Two-phase per instrument:
  Phase 1: generate all M surrogates (IAAFT, normal-scores domain), write DIAGNOSTICS to
           disk (rank-ACF/log-ACF fidelity, multiset asserts, tolerance-gate verdict)
           BEFORE any surrogate hit rate is computed.
  Phase 2: only if the diagnostic gate passed -- score every surrogate through the
           byte-identical frozen pipeline, compute the band, both one-sided p's, the
           corrected battery limbs L1-L5, and the typed verdict.

Modes:
  python run_corrected_null.py official         # frozen seeds [20260818, code, i]
  python run_corrected_null.py pilot            # verification seeds [20260818, code, 990000+i], M=200
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import norm, rankdata

HERE = Path(__file__).resolve().parent
GC_DIR = HERE.parent / "rangestate_gc_2026-08"
CL_DIR = HERE.parent / "rangestate_mcl_2026-08"
sys.path.insert(0, str(GC_DIR))
sys.path.insert(0, str(CL_DIR))
import run_s1a  # noqa: E402  (frozen GC pipeline)
import run_s1b  # noqa: E402  (frozen CL pipeline)

# ---- frozen spec constants (SPEC section 1-2) ----
BASE_SEED = 20260818
M_OFFICIAL, M_PILOT = 1000, 200
IAAFT_ITER = 100
ACF_LAGS = 60
TOL_MED, TOL_P95 = 0.04, 0.07
WINDOW, Q_BIAS, Q_REF = 60, 0.80, 0.50
CI_BLOCK, CI_DRAWS, CI_SEED = 60, 4000, 42
N_FLOOR_POP, N_FLOOR_COND = 400, 100
YEAR_MIN_NCOND = 20
SIGNED_LAGS = (1, 2, 3, 5, 10, 20, 60)

INSTRUMENTS = {
    "GC": dict(code=1, mod=run_s1a, obs=0.5299334811529933),
    "CL": dict(code=2, mod=run_s1b, obs=0.6282352941176471),
}


def normal_scores(x: np.ndarray) -> np.ndarray:
    """van der Waerden rank-Gaussianization (average ranks not needed: TR values
    are effectively continuous; ties broken by stable argsort order, disclosed)."""
    n = len(x)
    ranks = np.empty(n, dtype=float)
    ranks[np.argsort(x, kind="stable")] = np.arange(1, n + 1)
    return norm.ppf(ranks / (n + 1))


def iaaft(z: np.ndarray, rng: np.random.Generator, n_iter: int) -> np.ndarray:
    """IAAFT on the (Gaussianized) series z: iterate [impose target amplitude
    spectrum, keep phases] then [rank-remap onto sorted original z values].
    Returns a reordering of z's values matching z's linear spectrum."""
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


def fast_rolling_percentile_strict_prior(tr: np.ndarray, window: int, q: float) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(tr)
    out = np.full(n, np.nan)
    if n > window:
        wins = sliding_window_view(tr, window)          # wins[j] = tr[j:j+window]
        out[window:] = np.percentile(wins[: n - window], q * 100, axis=1)
    return out


def fast_rolling_percentile_through_today(tr: np.ndarray, window: int, q: float) -> np.ndarray:
    from numpy.lib.stride_tricks import sliding_window_view
    n = len(tr)
    out = np.full(n, np.nan)
    if n >= window:
        wins = sliding_window_view(tr, window)
        out[window - 1:] = np.percentile(wins, q * 100, axis=1)
    return out


def pipeline_stat(tr: np.ndarray) -> float:
    """The frozen statistic: P(y_{d+1}=1 | bias_d=1), fast path (asserted exact
    against the frozen loop functions on the real series at startup)."""
    bias_thresh = fast_rolling_percentile_strict_prior(tr, WINDOW, Q_BIAS)
    bias = (tr >= bias_thresh).astype(float)
    bias[np.isnan(bias_thresh)] = np.nan
    ref = fast_rolling_percentile_through_today(tr, WINDOW, Q_REF)
    y = np.full(len(tr), np.nan)
    y[:-1] = (tr[1:] > ref[:-1]).astype(float)
    y[np.isnan(ref)] = np.nan
    scored = (~np.isnan(bias)) & (~np.isnan(y))
    b, yy = bias[scored].astype(int), y[scored].astype(int)
    m = b == 1
    return float(yy[m].mean()) if m.any() else float("nan"), float(b.mean()), float(yy.mean())


def fidelity_assert(mod, tr: np.ndarray):
    """Fast path must be EXACT vs the frozen loop functions (spec: byte-identical pipeline)."""
    slow_b = mod.rolling_percentile_strict_prior(tr, WINDOW, Q_BIAS)
    fast_b = fast_rolling_percentile_strict_prior(tr, WINDOW, Q_BIAS)
    slow_r = mod.rolling_percentile_through_today(tr, WINDOW, Q_REF)
    fast_r = fast_rolling_percentile_through_today(tr, WINDOW, Q_REF)
    assert np.allclose(slow_b, fast_b, equal_nan=True, rtol=0, atol=0), "bias path mismatch"
    assert np.allclose(slow_r, fast_r, equal_nan=True, rtol=0, atol=0), "ref path mismatch"


def per_year_table(mod):
    """L4 input: per-year conditional rates from the ORIGINAL panel (real data)."""
    df = mod.load_clean()
    tr_full = mod.compute_tr_with_roll_exclusion(df)
    valid = tr_full.dropna()
    tr = valid.to_numpy()
    idx = valid.index
    bias_thresh = mod.rolling_percentile_strict_prior(tr, WINDOW, Q_BIAS)
    bias = (tr >= bias_thresh).astype(float)
    bias[np.isnan(bias_thresh)] = np.nan
    ref = mod.rolling_percentile_through_today(tr, WINDOW, Q_REF)
    y = np.full(len(tr), np.nan)
    y[:-1] = (tr[1:] > ref[:-1]).astype(float)
    y[np.isnan(ref)] = np.nan
    scored = (~np.isnan(bias)) & (~np.isnan(y))
    b, yy = bias[scored].astype(int), y[scored].astype(int)
    days = idx[scored]
    m = b == 1
    years = np.array([d.year for d in days[m]])
    ycond = yy[m]
    table = {}
    for yr in sorted(set(years)):
        sel = years == yr
        table[int(yr)] = dict(n=int(sel.sum()), rate=float(ycond[sel].mean()))
    # calm/crisis disclosure buckets: median of annual mean log-TR
    logtr = np.log(tr)
    yr_all = np.array([d.year for d in idx])
    ann_mean = {int(yr): float(logtr[yr_all == yr].mean()) for yr in sorted(set(yr_all))}
    med = float(np.median(list(ann_mean.values())))
    crisis = [yr for yr, v in ann_mean.items() if v > med]
    calm = [yr for yr, v in ann_mean.items() if v <= med]
    def bucket_rate(bucket):
        sel = np.isin(years, bucket)
        return dict(n=int(sel.sum()), rate=float(ycond[sel].mean()) if sel.any() else None)
    return table, dict(crisis_years=crisis, calm_years=calm,
                       crisis=bucket_rate(crisis), calm=bucket_rate(calm)), tr, valid


def eval_l4(table):
    valid_years = {yr: v for yr, v in table.items() if v["n"] >= YEAR_MIN_NCOND}
    n_valid = len(valid_years)
    n_pass = sum(1 for v in valid_years.values() if v["rate"] > 0.50)
    if n_valid < 7:
        return dict(n_valid=n_valid, n_pass=n_pass, required=None, verdict="AMBIGUOUS")
    required = n_valid - 2
    return dict(n_valid=n_valid, n_pass=n_pass, required=required,
                verdict="PASS" if n_pass >= required else "FAIL")


def run_instrument(name, cfg, mode):
    mod, code, obs = cfg["mod"], cfg["code"], cfg["obs"]
    M = M_OFFICIAL if mode == "official" else M_PILOT
    seed_offset = 0 if mode == "official" else 990000

    print(f"\n===== {name} ({mode}, M={M}) =====")
    year_tab, buckets, tr, valid = per_year_table(mod)
    fidelity_assert(mod, tr)
    print("pipeline fidelity assert: PASS (fast path exact vs frozen loops)")

    obs_check, f_bias1_real, p_up_real = pipeline_stat(tr)
    assert abs(obs_check - obs) < 1e-12, f"frozen obs mismatch: {obs_check} vs {obs}"

    z = normal_scores(tr)
    # FIX-2 (pre-official, adversarially verified on pilot seeds): the GATING diagnostic is
    # Spearman rank-ACF (ACF of mid-rank rankdata, biased estimator) -- the quantity the
    # frozen spec's 0.04/0.07 tolerance was calibrated on (spec's quoted 0.0295 GC reproduces
    # only under this reading). The z-domain ACF is retained as a non-gating AUXILIARY output
    # for pilot-comparability. Tolerances untouched.
    real_spear_acf = acf(rankdata(tr), ACF_LAGS)
    real_z_acf = acf(z, ACF_LAGS)
    real_log_acf = acf(np.log(tr), ACF_LAGS)
    tr_sorted = np.sort(tr)

    # ---- Phase 1: generate + diagnostics (written BEFORE any hit rate) ----
    surrogates = []
    spear_mismatch, z_mismatch, log_mismatch = [], [], []
    signed_dev = {k: [] for k in SIGNED_LAGS}
    for i in range(M):
        rng = np.random.default_rng([BASE_SEED, code, seed_offset + i])
        z_s = iaaft(z, rng, IAAFT_ITER)
        ranks = np.empty(len(z_s), dtype=int)
        ranks[np.argsort(z_s, kind="stable")] = np.arange(len(z_s))
        tr_s = tr_sorted[ranks]
        assert np.array_equal(np.sort(tr_s), tr_sorted), "multiset identity violated"
        s_spear_acf = acf(rankdata(tr_s), ACF_LAGS)
        s_z_acf = acf(z_s, ACF_LAGS)
        s_log_acf = acf(np.log(tr_s), ACF_LAGS)
        spear_mismatch.append(float(np.max(np.abs(s_spear_acf - real_spear_acf))))
        z_mismatch.append(float(np.max(np.abs(s_z_acf - real_z_acf))))
        log_mismatch.append(float(np.max(np.abs(s_log_acf - real_log_acf))))
        for k in SIGNED_LAGS:
            signed_dev[k].append(float(s_spear_acf[k - 1] - real_spear_acf[k - 1]))
        surrogates.append(tr_s)

    spear_mm = np.array(spear_mismatch)
    diag = dict(
        instrument=name, mode=mode, M=M, iterations=IAAFT_ITER, domain="normal-scores",
        seed_policy=f"default_rng([{BASE_SEED}, {code}, {seed_offset}+i])",
        multiset_asserts="PASS all",
        spearman_acf_mismatch=dict(med=float(np.median(spear_mm)),
                                   p95=float(np.percentile(spear_mm, 95)),
                                   max=float(spear_mm.max())),
        zdomain_acf_mismatch_auxiliary=dict(med=float(np.median(z_mismatch)),
                                            p95=float(np.percentile(z_mismatch, 95)),
                                            max=float(np.max(z_mismatch))),
        log_acf_mismatch=dict(med=float(np.median(log_mismatch)),
                              p95=float(np.percentile(log_mismatch, 95)),
                              max=float(np.max(log_mismatch))),
        signed_median_dev_spearman={k: float(np.median(v)) for k, v in signed_dev.items()},
        tolerance=dict(med_limit=TOL_MED, p95_limit=TOL_P95, gating_domain="spearman-rank-acf"),
        gate="PASS" if (np.median(spear_mm) <= TOL_MED and np.percentile(spear_mm, 95) <= TOL_P95)
             else "FAIL",
    )
    diag_path = HERE / f"diagnostics_{name}_{mode}.json"
    diag_path.write_text(json.dumps(diag, indent=1))
    print(f"diagnostics written: {diag_path.name}  gate={diag['gate']}  "
          f"spearman-ACF med={diag['spearman_acf_mismatch']['med']:.4f} "
          f"p95={diag['spearman_acf_mismatch']['p95']:.4f}")
    if diag["gate"] != "PASS":
        print("DIAGNOSTIC GATE FAIL -> escalation ladder owed (500 iter / end-matching) -> VOID if exhausted")
        return dict(instrument=name, VERDICT="VOID-PENDING-LADDER", diagnostics=diag)

    # ---- Phase 2: score ----
    rates, shares, pups = [], [], []
    for tr_s in surrogates:
        r, f1, pu = pipeline_stat(tr_s)
        rates.append(r); shares.append(f1); pups.append(pu)
    rates = np.array(rates)
    p_upper = (1 + int((rates >= obs).sum())) / (M + 1)
    p_lower = (1 + int((rates <= obs).sum())) / (M + 1)
    pct_obs = float((rates < obs).mean() * 100)

    l4 = eval_l4(year_tab)
    limbs = dict(
        L1_n_floor=True,  # carried verbatim from committed results (both instruments passed)
        L2_ci_lb=bool(name == "CL"),  # carried verbatim: GC 0.4545 FAIL, CL 0.5651 PASS
        L3_halves=True,   # carried verbatim: both passed
        L4_by_year=l4["verdict"],
        L5_attribution=("EXCESS" if p_upper <= 0.05 else "GENERIC"),
    )
    presence_pass = limbs["L1_n_floor"] and limbs["L2_ci_lb"] and limbs["L3_halves"] \
        and (l4["verdict"] == "PASS")
    if l4["verdict"] == "AMBIGUOUS":
        verdict = "AMBIGUOUS"
    elif presence_pass:
        verdict = "SIGNAL-EXCESS" if p_upper <= 0.05 else "SIGNAL-GENERIC"
    else:
        driving = [k for k, v in (("L2", limbs["L2_ci_lb"]), ("L3", limbs["L3_halves"]),
                                  ("L4", l4["verdict"] == "PASS"), ("L1", limbs["L1_n_floor"])) if not v]
        verdict = f"NULL (driving: {','.join(driving)})"
    flags = []
    if p_lower <= 0.05:
        flags.append("SUB-LINEAR")
    # FIX-1 (pre-official): p_att := p_upper (the attribution-typing p; the lower tail is
    # separately owned by SUB-LINEAR). Adjudicated in ADDENDUM-1 item 10.
    if 0.03 <= p_upper <= 0.07:
        flags.append("ATTRIBUTION-FRAGILE")
    if min(abs(p_upper - 0.05), abs(p_lower - 0.05)) <= 0.02:
        flags.append("BORDERLINE")

    out = dict(
        instrument=name, mode=mode, obs=obs, VERDICT=verdict, flags=flags,
        band=dict(mean=float(rates.mean()), sd=float(rates.std(ddof=1)),
                  pct=[float(np.percentile(rates, q)) for q in (2.5, 5, 50, 95, 97.5)],
                  M=M, iterations=IAAFT_ITER),
        p_upper=p_upper, p_lower=p_lower, obs_percentile=pct_obs,
        limbs=limbs, l4_detail=l4, per_year=year_tab, calm_crisis=buckets,
        sanity=dict(real_bias1_share=f_bias1_real, real_p_up=p_up_real,
                    surr_bias1_share_band=[float(np.percentile(shares, 2.5)), float(np.percentile(shares, 97.5))],
                    surr_p_up_band=[float(np.percentile(pups, 2.5)), float(np.percentile(pups, 97.5))]),
        diagnostics=diag,
    )
    print(f"obs={obs:.4f} sits at {pct_obs:.1f}th pct of band "
          f"[mean={out['band']['mean']:.4f}, p5={out['band']['pct'][1]:.4f}, p95={out['band']['pct'][3]:.4f}]")
    print(f"p_upper={p_upper:.4f}  p_lower={p_lower:.4f}  flags={flags}")
    print(f"per-year: { {k: round(v['rate'],3) for k,v in year_tab.items()} }")
    print(f"L4: {l4}")
    print(f"calm/crisis: crisis={buckets['crisis']} calm={buckets['calm']}")
    print(f"VERDICT: {verdict}")
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    assert mode in ("official", "pilot")
    results = {name: run_instrument(name, cfg, mode) for name, cfg in INSTRUMENTS.items()}
    (HERE / f"corrected_null_results_{mode}.json").write_text(
        json.dumps(results, indent=1, default=str))
    print(f"\nwrote corrected_null_results_{mode}.json")


if __name__ == "__main__":
    main()
