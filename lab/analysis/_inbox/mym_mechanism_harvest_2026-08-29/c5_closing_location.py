"""Candidate 5 -- bar closing-location autocorrelation (M15, unconditional).

CLV_t = (close_t - low_t) / (high_t - low_t) in [0,1] -- where within its own H-L range
a bar closed. Question: is CLV serially correlated bar-to-bar, unconditional on level,
session anchor, or vol regime? Same-series, next-bar construction (CLV_t -> CLV_{t+1}),
so -- unlike candidates 2/3/4 -- this is NOT the cross-series common-regime confound;
it is structurally the same shape as candidate 1 (S1-role: one series predicting its
own next value), so the independent-series IAAFT battery is the right tool, reused
directly (not an increment test). No degenerate H==L bars on this panel (checked: 0 /
141,476), so CLV is well-defined everywhere -- the fine-tick 6J degenerate-OHLC failure
mode (lesson_bar_export_ohlc_degenerate_fine_tick) does not apply here.

Admission-route status: UNRESOLVED, per the user's brief -- flagged, not assumed. CLV
autocorrelation is a bar-SHAPE statistic, not a level/breakout/continuation construct
keyed to a reference level (distinct from every entry in MYM's DEAD table), but a
POSITIVE finding here ("bars that close strong are followed by bars that close strong")
carries an inherent directional-momentum flavor close to `intraday-momentum`
(Baltussen-class, ABSENT on modern MNQ) -- if it screens SIGNAL, whether it can be
pursued as an entry-role candidate without first clearing the single-instrument
index-futures directional-timing raised bar (docs/rejected_candidates.md) is a genuine
open governance question this Notice-phase screen does not resolve on its own
authority.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

from load_sessions import load_bars
import iaaft_battery as B

HERE = Path(__file__).resolve().parent
CI_BLOCK, CI_DRAWS, CI_SEED = 96, 4000, 42  # block ~1 session of M15 bars
M, SEED_BASE, CODE = 200, 20260829, 5
N_FLOOR_POP = 400


def main():
    bars = load_bars()
    bars = bars[bars["session"] < bars["session"].max()]
    h, l, c = bars["high"].to_numpy(), bars["low"].to_numpy(), bars["close"].to_numpy()
    clv_full = (c - l) / (h - l)
    n_full = len(clv_full)
    # trim once, upfront, to a 2/3/5/7-smooth length (fast FFT) -- see
    # iaaft_battery.fast_fft_trim docstring; every downstream stat (obs, CI,
    # halves, by-year, surrogate band) uses this SAME trimmed series so obs is
    # scored on exactly the value multiset the surrogates reorder.
    clv = B.fast_fft_trim(clv_full)
    n = len(clv)
    n_dropped = n_full - n
    ts_et = bars["ts_et"].to_numpy()[n_dropped:]  # same front-trim as fast_fft_trim
    print(f"bars: {n_full} -> trimmed {n} (dropped {n_dropped}, "
          f"{n_dropped/n_full*100:.2f}%) for fast FFT")
    print(f"CLV describe: mean={clv.mean():.4f} std={clv.std():.4f} "
          f"min={clv.min():.4f} max={clv.max():.4f}")

    # observed lag-1 Spearman autocorrelation
    x, y = clv[:-1], clv[1:]
    obs_rho = float(np.corrcoef(rankdata(x), rankdata(y))[0, 1])
    print(f"observed lag-1 Spearman rho(CLV_t, CLV_t+1) = {obs_rho:.5f}  n_pairs={n-1}")

    # block-bootstrap CI on the pair series
    rng = np.random.default_rng(CI_SEED)
    N = n - 1
    nblocks = int(np.ceil(N / CI_BLOCK))
    boots = []
    for _ in range(CI_DRAWS):
        st = rng.integers(0, N, size=nblocks)
        idx = (st[:, None] + np.arange(CI_BLOCK)[None, :]) % N
        idx = idx.ravel()[:N]
        xb, yb = x[idx], y[idx]
        boots.append(float(np.corrcoef(rankdata(xb), rankdata(yb))[0, 1]))
    boots = np.asarray(boots)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    print(f"block-bootstrap 95% CI = [{lo:.5f}, {hi:.5f}]")

    h_ = n // 2
    rho1 = float(np.corrcoef(rankdata(clv[:h_ - 1]), rankdata(clv[1:h_]))[0, 1])
    rho2 = float(np.corrcoef(rankdata(clv[h_:-1]), rankdata(clv[h_ + 1:]))[0, 1])
    print(f"halves: older={rho1:.5f}  newer={rho2:.5f}")

    # by-year stability (disclosure)
    years = np.array([t.year for t in ts_et])[:-1]
    by_year = {}
    for yr in sorted(set(years)):
        m = years == yr
        if m.sum() > 200:
            by_year[int(yr)] = float(np.corrcoef(rankdata(x[m]), rankdata(y[m]))[0, 1])
    print(f"by_year: { {k: round(v,4) for k,v in by_year.items()} }")

    # IAAFT diagnostic-gated null on CLV itself (already bounded [0,1]; normal_scores
    # handles the transform to an unbounded domain internally)
    surrogates, diag = B.generate_surrogates(clv, M, SEED_BASE, CODE, acf_lags=40)
    print(f"diagnostic gate: {diag['gate']}  med={diag['med']:.4f} p95={diag['p95']:.4f}")

    out = dict(n=n, obs_rho=obs_rho, ci=[lo, hi], halves=[rho1, rho2], by_year=by_year,
               diagnostics=diag)

    if diag["gate"] != "PASS":
        out["VERDICT"] = "VOID (diagnostic gate FAIL)"
        (HERE / "c5_results.json").write_text(json.dumps(out, indent=2))
        print("VERDICT:", out["VERDICT"])
        return

    surr_rhos = []
    for s in surrogates:
        xs, ys = s[:-1], s[1:]
        surr_rhos.append(float(np.corrcoef(rankdata(xs), rankdata(ys))[0, 1]))
    surr_rhos = np.array(surr_rhos)
    p_upper = (1 + int((surr_rhos >= obs_rho).sum())) / (M + 1)
    p_two_sided = (1 + int((np.abs(surr_rhos) >= abs(obs_rho)).sum())) / (M + 1)
    pct = float((surr_rhos < obs_rho).mean() * 100)
    print(f"surrogate rho band: mean={surr_rhos.mean():.5f} sd={surr_rhos.std():.5f} "
          f"p2.5={np.percentile(surr_rhos,2.5):.5f} p97.5={np.percentile(surr_rhos,97.5):.5f}")
    print(f"p_upper={p_upper:.4f}  p_two_sided={p_two_sided:.4f}  obs at {pct:.1f}th pct of band")

    # sign-agnostic presence gates: obs's OWN sign sets the direction every limb must
    # share (candidate 1's gates assumed a positive-persistence claim; this candidate's
    # real finding is negative/mean-reverting, so a sign-hardcoded gate would wrongly
    # read a robust, consistent, significant result as NULL).
    sign = 1.0 if obs_rho >= 0 else -1.0
    l1 = bool(n >= N_FLOOR_POP)
    l2 = bool(sign * lo > 0.0 and sign * hi > 0.0)  # CI entirely on obs's own side of 0
    l3 = bool(sign * rho1 > 0.0 and sign * rho2 > 0.0)
    presence = l1 and l2 and l3
    if presence:
        verdict = "SIGNAL-EXCESS" if p_two_sided <= 0.05 else "SIGNAL-GENERIC"
    else:
        driving = [k for k, v in (("L1", l1), ("L2", l2), ("L3", l3)) if not v]
        verdict = f"NULL (driving: {','.join(driving)})"

    out.update(dict(band=dict(mean=float(surr_rhos.mean()), sd=float(surr_rhos.std())),
                     p_upper=float(p_upper), p_two_sided=float(p_two_sided),
                     obs_percentile=float(pct),
                     limbs=dict(L1_n_floor=l1, L2_ci_excludes_0_same_sign=l2, L3_halves_same_sign=l3),
                     sign="negative" if sign < 0 else "positive",
                     VERDICT=verdict))
    (HERE / "c5_results.json").write_text(json.dumps(out, indent=2))
    print("VERDICT:", verdict)


if __name__ == "__main__":
    main()
