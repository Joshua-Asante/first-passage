"""i.i.d.-sufficiency power-up -- N=50 for the `empirical_shuffle` arm only.

STATUS: scoping probe, follow-up to `geofit_skew_probe_2026-07-25`. **Not** part of Q-GEOFIT-1
(CLOSED `AMBIGUOUS-PARAMETERIZATION`, 2026-07-25) and **not** a re-open of it. Produces no envelope,
no grid, no cells, no candidate claim. $0.00 spend, zero K.

===============================================================================
PRE-DECLARATION (fixed before this ran)
===============================================================================

Question left open by `geofit_skew_probe_2026-07-25` (see its README, "What is NOT established"):
does the true empirical marginal distribution, drawn i.i.d. (`empirical_shuffle` arm), reproduce the
real c1 book's trailing-DD bust rate -- or is within-week serial structure load-bearing? At N=5 the
arm landed 0.87pp from target against a 0.50pp tolerance, but at 1.75 sigma (SE 0.50pp) that result
is neither a pass nor a miss -- underpowered, not ambiguous in the substantive sense.

The prior probe's own README computed the fix: "Resolving it needs roughly N >= 50 for
`empirical_shuffle` ... at its observed dispersion." N=50 is that number, not a new choice.

ARM: `empirical_shuffle` only. The `skewed_gamma` arm's own verdict (SKEW-CONFIRMED, 0.38 sigma from
target at N=5) is not near a decision boundary and is not re-run here; its flagged instability (raw
Gamma win-tail, sd 10.85%) is a DESIGN defect a successor family must fix, not a power problem this
probe corrects. Re-running it would not change its verdict and is out of scope.

DECISION RULE (pre-declared, inherited unchanged from the prior probe):
  tolerance = +/-0.5pp on |combined_mean_bust - 4.7433%|.
  Combined estimate = pooled mean over the original 5 realizations (probe.json, arm
  `empirical_shuffle`, seeds 20260725-20260729) plus 45 new realizations at seeds 20260815000-44,
  for N=50 total -- not a fresh N=50 replacing the original 5, so no realization is silently
  discarded.

  MARGINALS-SUFFICIENT   combined mean within tolerance. The true marginals DO reproduce the real
                          bust rate under i.i.d. resampling; a richer i.i.d. family (skew-aware) is
                          the correct successor shape, not a block-structure model.
  MARGINALS-INSUFFICIENT combined mean outside tolerance. Serial/within-week structure is load-
                          bearing for the trailing-DD bust probability; a successor must model block
                          structure -- a materially bigger re-scope than an i.i.d. family, however
                          shaped.

Nothing here selects a strategy, consults candidate returns, or touches a frozen constant.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]  # lab/analysis/c1/<slug>/ -- matches run_class_s_c1_scoring.py's own depth
_RECONCILE = _ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"
for _p in (_ROOT / "core", _ROOT / "lab", str(_RECONCILE), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

ACCOUNT = 100_000.0
N_BDAYS = 1692
TIER = "Tradeify_Select_100K"
UNREACHABLE = 1_000_000.0
DEFECTIVE_OFFSET = 100
REAL_BUST = 0.047433
TOL = 0.005  # +/-0.5pp, inherited unchanged from Q-GEOFIT-1 §2 / the prior probe

# Original probe's own 5 empirical_shuffle results (probe.json, arm=empirical_shuffle),
# transcribed here read-only for pooling -- not re-derived, not re-run.
ORIGINAL_N = 5
ORIGINAL_SEED_BASE = 20260725

N_NEW = 45  # brings the pooled total to 50, per the prior README's own N>=50 recommendation
NEW_SEED_BASE = 20260815000


def real_c1_daily() -> np.ndarray:
    sys.argv = [sys.argv[0]]
    import run_class_s_c1_scoring as S

    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    print(f"[power-up] c1 panel {meta['panel_span']} n_bdays={meta['n_bdays']}", flush=True)
    return panel.sum(axis=1).to_numpy(dtype=float) * (ACCOUNT / S.ACCOUNT)


def _place(values: np.ndarray, n_bdays: int, rng) -> np.ndarray:
    out = np.zeros(n_bdays, dtype=float)
    idx = np.sort(rng.permutation(n_bdays)[: values.size])
    out[idx] = values
    return out


def score_shuffle(real_active: np.ndarray, seed: int, thr) -> dict:
    import firm_rules

    prior = firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"]
    firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        import run_class_s_c1_regime_gate as R

        rng = np.random.default_rng(seed)
        vals = rng.permutation(real_active)
        s = _place(vals, N_BDAYS, rng)
        t0 = time.time()
        r = R.run_partition_mc(s, TIER, thr)
        return {
            "seed": seed,
            "headline_bust": float(r["headline_bust"]),
            "pass_rate": float(r["pass_rate"]),
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
        print(f"[power-up] PHASE0: gate ceilings drifted: {thr}", file=sys.stderr)
        return 3

    daily = real_c1_daily()
    real_active = daily[daily != 0.0].copy()
    print(f"[power-up] real_active n={real_active.size}, real_bust={REAL_BUST:.4%}", flush=True)

    seeds = [NEW_SEED_BASE + i for i in range(N_NEW)]
    print(f"[power-up] running {N_NEW} new empirical_shuffle realizations "
          f"(seeds {seeds[0]}-{seeds[-1]}), pooling with the original {ORIGINAL_N}", flush=True)

    try:
        from joblib import Parallel, delayed
        res = Parallel(n_jobs=7, prefer="processes", verbose=10)(
            delayed(score_shuffle)(real_active, sd, thr) for sd in seeds
        )
    except ImportError:
        res = [score_shuffle(real_active, sd, thr) for sd in seeds]

    bad = [r for r in res if r["geometry_offset_used"] != UNREACHABLE]
    if bad:
        print(f"[power-up] GEOMETRY GUARD TRIPPED on {len(bad)} runs", file=sys.stderr)
        return 4

    new_bust = np.array([r["headline_bust"] for r in res])
    print(f"[power-up] new-45 mean={new_bust.mean():.4%} sd={new_bust.std(ddof=1):.4%}", flush=True)

    out = {
        "status": "scoping probe, follow-up to geofit_skew_probe_2026-07-25; NOT part of the closed study",
        "question": "does empirical_shuffle (true marginals, i.i.d.) reproduce the real bust rate at adequate power?",
        "real_bust": REAL_BUST,
        "tolerance_pp": TOL * 100,
        "tier": TIER,
        "geometry": "CORRECTED (dd_lock_offset_usd -> 1e6)",
        "n_sims_per_seed": thr.sims_per_seed,
        "original_n": ORIGINAL_N,
        "original_seed_base": ORIGINAL_SEED_BASE,
        "original_note": "original 5 empirical_shuffle busts from geofit_skew_probe_2026-07-25/probe.json, pooled not re-run",
        "new_n": N_NEW,
        "new_seed_base": NEW_SEED_BASE,
        "new_runs": res,
        "new_mean_bust": float(new_bust.mean()),
        "new_sd_bust": float(new_bust.std(ddof=1)),
    }
    (_HERE / "power_up_new45.json").write_text(
        json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(f"[written] {_HERE / 'power_up_new45.json'}", flush=True)
    print("[power-up] NEXT: pool with the original 5 (see README.md) for the N=50 combined verdict.",
          flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
