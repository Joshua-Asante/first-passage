"""Skew probe — does adding a skew dimension close the Q-GEOFIT-1 A2 residual?

STATUS: scoping probe for a Q-GEOFIT-1 successor. **Not** part of Q-GEOFIT-1, which is
CLOSED `AMBIGUOUS-PARAMETERIZATION` (2026-07-25). This produces **no envelope, no grid,
no cells, and no candidate claim** — its only output is a methodological verdict on
whether a skewed family is sufficient to model trailing-DD survival. Zero K, $0.00 spend.
Named in that closure §8 as the cheapest next probe; operator-directed 2026-07-25.

===============================================================================
PRE-DECLARATION (fixed BEFORE any arm was run — no best-of-K family selection)
===============================================================================

Question: Q-GEOFIT-1 established that `(sigma_d, mu/sigma, shape, z)` mis-predicts the
real c1 bust by 23.63pp at an EXACT parameter match, and diagnosed the cause as the
family's lack of a skew / loss-tail dimension. Is that diagnosis right?

Reference: real c1 daily series, $100K basis, corrected geometry -> bust 4.7433%.

FOUR ARMS, each a single pre-declared construction (no variants, no tuning):

  A  symmetric_baseline   The Q-GEOFIT-1 family: student-t(nu=4), symmetric, affinely
                          standardized to c1's fitted active-day (mu, sigma). Reproduces
                          the closed study's finding as a control. Expected ~28.4%.

  B  skewed_gamma         The minimal addition of skew: draw a win with prob p_win and a
                          loss otherwise; win magnitude ~ Gamma matched to the WIN
                          branch's own (mean, sd); loss magnitude ~ Gamma matched to the
                          LOSS branch's own (mean, sd), negated. Five active-day
                          parameters (p_win, mu_w, sd_w, mu_l, sd_l) vs the original's
                          two. Gamma is positive-support and right-skewed, so the win and
                          loss tails are independently parameterized — exactly the
                          dimension the closed family lacked.

  C  empirical_shuffle    The REAL active-day values, permuted (identical marginal
                          distribution, exactly — same multiset), placed uniformly at the
                          real z. Adjudicates arm B: if the true marginals ALSO fail to
                          reproduce the real bust, then no i.i.d. family of any shape can
                          work, and the missing ingredient is serial structure, not skew.

  D  empirical_clustered  As C, but idle days are clustered into whole idle WEEKS instead
                          of scattered. Tests the direction and magnitude of R4 (the
                          undeclared zero-day placement law) at the real book's z.

All arms: z = c1's real zero-day fraction, n_bdays = 1692, tier Tradeify_Select_100K,
CORRECTED geometry (dd_lock_offset_usd -> 1e6), frozen engine (10k sims x seeds
42/123/2026, horizon 1500, Run-2 consistency-on, dd_protection OFF).

N_REALIZATIONS = 5 per arm, seeds fixed below. This is REQUIRED, not optional: the
Q-GEOFIT-1 adversarial audit measured per-cell series-realization noise at 0.55-1.09pp
sd, which EXCEEDS the +/-0.5pp tolerance, so a single realization cannot decide the
question. Decide on the arm MEAN; the sd is reported so the reader can see whether
realization noise swamps the call.

DECISION RULE (pre-declared):
  tolerance = +/-0.5pp on |arm_mean_bust - 4.7433%|, inherited from Q-GEOFIT-1 §2.

  SKEW-CONFIRMED      B within tolerance. The diagnosis holds: a skew/loss-tail
                      dimension is what the closed family was missing, and a successor
                      built on B's shape is worth pre-registering.
  SKEW-INSUFFICIENT   B outside tolerance. Then C adjudicates:
                        C within tolerance  -> the true marginals DO suffice; arm B's
                                               particular parametric form is wrong, but a
                                               richer i.i.d. family can still work.
                        C outside tolerance -> marginals are NOT sufficient at all; the
                                               residual is serial/within-week structure,
                                               and NO i.i.d. family will ever reproduce
                                               it. A successor must model block structure,
                                               which is a materially bigger re-scope.
  Arm D is diagnostic only and cannot change the verdict; it reports the placement effect.

Nothing here selects a strategy, consults candidate returns, or touches a frozen constant.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_GEOFIT = _ROOT / "lab" / "analysis" / "q_geofit_1_2026-07"
_SCORING = _ROOT / "lab" / "analysis" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_GEOFIT), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

ACCOUNT = 100_000.0
N_BDAYS = 1692
TIER = "Tradeify_Select_100K"
UNREACHABLE = 1_000_000.0
DEFECTIVE_OFFSET = 100
REAL_BUST = 0.047433
TOL = 0.005          # +/-0.5pp, inherited from Q-GEOFIT-1 §2
N_REALIZATIONS = 5
SEED_BASE = 20260725
ARMS = ("symmetric_baseline", "skewed_gamma", "empirical_shuffle", "empirical_clustered")


def real_c1_daily() -> np.ndarray:
    sys.argv = [sys.argv[0]]
    import run_class_s_c1_scoring as S

    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    print(f"[probe] c1 panel {meta['panel_span']} n_bdays={meta['n_bdays']}", flush=True)
    return panel.sum(axis=1).to_numpy(dtype=float) * (ACCOUNT / S.ACCOUNT)


def fit_stats(daily: np.ndarray) -> dict:
    a = daily[daily != 0.0]
    w, l = a[a > 0], a[a < 0]
    return {
        "z": float((daily == 0.0).mean()),
        "n_active": int(a.size),
        "mu": float(a.mean()),
        "sigma": float(a.std(ddof=1)),
        "p_win": float((a > 0).mean()),
        "win_mean": float(w.mean()), "win_sd": float(w.std(ddof=1)),
        "loss_mean": float(l.mean()), "loss_sd": float(l.std(ddof=1)),
    }


def _gamma(rng, mean: float, sd: float, n: int) -> np.ndarray:
    """Gamma matched to (mean, sd): k = mean^2/var, theta = var/mean."""
    var = sd * sd
    k = mean * mean / var
    theta = var / mean
    return rng.gamma(shape=k, scale=theta, size=n)


def _place(values: np.ndarray, n_bdays: int, rng, clustered: bool) -> np.ndarray:
    """Scatter active values across n_bdays. Uniform, or clustered into whole weeks."""
    out = np.zeros(n_bdays, dtype=float)
    n_act = values.size
    if not clustered:
        idx = np.sort(rng.permutation(n_bdays)[:n_act])
        out[idx] = values
        return out
    # Clustered: choose whole 5-day weeks to be ACTIVE until the budget is filled.
    n_weeks = n_bdays // 5
    need_weeks = int(np.ceil(n_act / 5))
    wk = rng.permutation(n_weeks)[:need_weeks]
    slots = np.concatenate([np.arange(w * 5, w * 5 + 5) for w in np.sort(wk)])[:n_act]
    out[slots] = values
    return out


def make_arm(arm: str, fit: dict, real_active: np.ndarray, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = fit["n_active"]
    if arm == "symmetric_baseline":
        raw = rng.standard_t(4, size=n) / np.sqrt(2.0)
        vals = fit["mu"] + fit["sigma"] * (raw - raw.mean()) / raw.std(ddof=1)
        return _place(vals, N_BDAYS, rng, clustered=False)
    if arm == "skewed_gamma":
        is_win = rng.random(n) < fit["p_win"]
        vals = np.empty(n, dtype=float)
        nw, nl = int(is_win.sum()), int((~is_win).sum())
        if nw:
            vals[is_win] = _gamma(rng, fit["win_mean"], fit["win_sd"], nw)
        if nl:
            vals[~is_win] = -_gamma(rng, abs(fit["loss_mean"]), fit["loss_sd"], nl)
        return _place(vals, N_BDAYS, rng, clustered=False)
    if arm in ("empirical_shuffle", "empirical_clustered"):
        vals = rng.permutation(real_active)
        return _place(vals, N_BDAYS, rng, clustered=(arm == "empirical_clustered"))
    raise ValueError(arm)


def score(arm: str, fit: dict, real_active: np.ndarray, seed: int, thr) -> dict:
    import firm_rules

    prior = firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"]
    firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        import run_class_s_c1_regime_gate as R

        s = make_arm(arm, fit, real_active, seed)
        a = s[s != 0]
        m = a - a.mean()
        t0 = time.time()
        r = R.run_partition_mc(s, TIER, thr)
        return {
            "arm": arm, "seed": seed,
            "headline_bust": float(r["headline_bust"]),
            "pass_rate": float(r["pass_rate"]),
            "skew": float((m**3).mean() / (m**2).mean() ** 1.5),
            "worst_day": float(a.min()),
            "z_realized": float((s == 0.0).mean()),
            "geometry_offset_used": float(firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"]),
            "wall_s": round(time.time() - t0, 1),
        }
    finally:
        firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = prior


def main() -> int:
    from discovery.prop_survivor_scoring import load_scoring_thresholds

    thr = load_scoring_thresholds(
        _ROOT / "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"
    )
    if thr.eval_bust_ceiling != 0.03 or thr.pass_floor != 0.5:
        print(f"[probe] PHASE0: gate ceilings drifted: {thr}", file=sys.stderr)
        return 3

    daily = real_c1_daily()
    fit = fit_stats(daily)
    real_active = daily[daily != 0.0].copy()
    print(f"[probe] fit {json.dumps({k: round(v, 4) for k, v in fit.items()})}", flush=True)

    jobs = [(arm, SEED_BASE + i) for arm in ARMS for i in range(N_REALIZATIONS)]
    print(f"[probe] {len(jobs)} runs = {len(ARMS)} arms x {N_REALIZATIONS} realizations",
          flush=True)

    try:
        from joblib import Parallel, delayed
        res = Parallel(n_jobs=7, prefer="processes", verbose=5)(
            delayed(score)(arm, fit, real_active, sd, thr) for arm, sd in jobs
        )
    except ImportError:
        res = [score(arm, fit, real_active, sd, thr) for arm, sd in jobs]

    bad = [r for r in res if r["geometry_offset_used"] != UNREACHABLE]
    if bad:
        print(f"[probe] GEOMETRY GUARD TRIPPED on {len(bad)} runs", file=sys.stderr)
        return 4

    summary = {}
    for arm in ARMS:
        b = np.array([r["headline_bust"] for r in res if r["arm"] == arm])
        sk = np.array([r["skew"] for r in res if r["arm"] == arm])
        wd = np.array([r["worst_day"] for r in res if r["arm"] == arm])
        summary[arm] = {
            "mean_bust": float(b.mean()), "sd_bust": float(b.std(ddof=1)),
            "min_bust": float(b.min()), "max_bust": float(b.max()),
            "mean_skew": float(sk.mean()), "mean_worst_day": float(wd.mean()),
            "residual_pp": round(abs(float(b.mean()) - REAL_BUST) * 100, 4),
            "within_tol": bool(abs(float(b.mean()) - REAL_BUST) <= TOL),
        }
        s = summary[arm]
        print(
            f"[probe] {arm:22s} bust={s['mean_bust']:7.2%} +/-{s['sd_bust']:.2%}  "
            f"resid={s['residual_pp']:6.2f}pp  skew={s['mean_skew']:+.2f}  "
            f"worst={s['mean_worst_day']:8.0f}  -> {'WITHIN' if s['within_tol'] else 'MISS'}",
            flush=True,
        )

    b_ok = summary["skewed_gamma"]["within_tol"]
    c_ok = summary["empirical_shuffle"]["within_tol"]
    if b_ok:
        verdict = "SKEW-CONFIRMED"
        note = ("A skew/loss-tail dimension is what the closed family lacked; a successor "
                "built on this shape is worth pre-registering.")
    elif c_ok:
        verdict = "SKEW-INSUFFICIENT / MARGINALS-SUFFICIENT"
        note = ("The true marginals DO reproduce the real bust, so an i.i.d. family can "
                "work — arm B's particular parametric form is wrong, not the approach.")
    else:
        verdict = "SKEW-INSUFFICIENT / SERIAL-STRUCTURE-BINDING"
        note = ("Even the exact empirical marginals fail. No i.i.d. family of any shape "
                "can reproduce this book; a successor must model within-week block "
                "structure. Materially bigger re-scope than the closure assumed.")

    out = {
        "status": "scoping probe for a Q-GEOFIT-1 successor; NOT part of the closed study",
        "real_bust": REAL_BUST, "tolerance_pp": TOL * 100,
        "n_realizations": N_REALIZATIONS, "seed_base": SEED_BASE,
        "tier": TIER, "geometry": "CORRECTED (dd_lock_offset_usd -> 1e6)",
        "n_sims_per_seed": thr.sims_per_seed,
        "fit": fit, "summary": summary, "runs": res,
        "verdict": verdict, "note": note,
        "placement_effect_pp": round(
            (summary["empirical_clustered"]["mean_bust"]
             - summary["empirical_shuffle"]["mean_bust"]) * 100, 4),
    }
    (_HERE / "probe.json").write_text(json.dumps(out, indent=2, default=str) + "\n",
                                     encoding="utf-8")
    print(f"\n[probe] VERDICT: {verdict}\n[probe] {note}", flush=True)
    print(f"[probe] R4 placement effect (clustered - uniform): "
          f"{out['placement_effect_pp']:+.2f}pp", flush=True)
    print(f"[written] {_HERE / 'probe.json'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
