"""Characterize `family_skewed_gamma`, fit to the real c1 book, over N=50 realizations.

STATUS: scoping construction, not part of Q-GEOFIT-1. $0.00 spend, zero K. See
`family_skewed_gamma.py`'s module docstring for the design decision (preserve the win-branch tail,
do not cap) this characterization exists to honor.

===============================================================================
PRE-DECLARATION
===============================================================================

This is NOT a pass/fail test against the real book's realized bust rate (4.7433%) -- that question
(does an i.i.d. family reproduce it) was already answered by the TRUE marginals in
`geofit_iid_sufficiency_power_2026-08-15` (MARGINALS-SUFFICIENT, N=50). This step asks a different
question: what does the actual PARAMETRIC family (needed because a future grid must sweep a
continuous range, not just the one real-book-anchored point) produce, and how wide is its spread,
given the operator decision to preserve rather than cap the win tail.

N=50 realizations (seeds 20260815100-20260815149), same tier/geometry/engine as both prior probes.
Reports mean, sd, and the 10th/50th/90th percentiles of headline_bust across realizations -- the
spread is the deliverable, not a single number.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]
_SIBLING = _ROOT / "lab" / "analysis" / "c1" / "geofit_iid_sufficiency_power_2026-08-15"
_RECONCILE = _ROOT / ".claude" / "skills" / "trade-csv-reconcile" / "scripts"
for _p in (_ROOT / "core", _ROOT / "lab", str(_RECONCILE), str(_SIBLING), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import family_skewed_gamma as F  # noqa: E402

ACCOUNT = 100_000.0
N_BDAYS = 1692
TIER = "Tradeify_Select_100K"
UNREACHABLE = 1_000_000.0
N_REALIZATIONS = 50
SEED_BASE = 20260815100


def real_c1_daily() -> np.ndarray:
    sys.argv = [sys.argv[0]]
    import run_class_s_c1_scoring as S

    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    print(f"[characterize] c1 panel {meta['panel_span']} n_bdays={meta['n_bdays']}", flush=True)
    return panel.sum(axis=1).to_numpy(dtype=float) * (ACCOUNT / S.ACCOUNT)


def score_one(params: dict, seed: int, thr) -> dict:
    import firm_rules

    prior = firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"]
    firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        import run_class_s_c1_regime_gate as R

        s = F.draw_series(params, seed, N_BDAYS)
        active = s[s != 0]
        m = active - active.mean()
        skew = float((m**3).mean() / (m**2).mean() ** 1.5)
        t0 = time.time()
        r = R.run_partition_mc(s, TIER, thr)
        return {
            "seed": seed,
            "headline_bust": float(r["headline_bust"]),
            "pass_rate": float(r["pass_rate"]),
            "realized_skew": skew,
            "realized_max_win": float(active[active > 0].max()) if (active > 0).any() else None,
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
        print(f"[characterize] PHASE0: gate ceilings drifted: {thr}", file=sys.stderr)
        return 3

    daily = real_c1_daily()
    active = daily[daily != 0.0]
    params = F.fit_family(active)
    print(f"[characterize] fit: {json.dumps({k: round(v, 4) if isinstance(v, float) else v for k, v in params.items()})}", flush=True)

    seeds = [SEED_BASE + i for i in range(N_REALIZATIONS)]
    print(f"[characterize] running {N_REALIZATIONS} realizations (seeds {seeds[0]}-{seeds[-1]})",
          flush=True)

    try:
        from joblib import Parallel, delayed
        res = Parallel(n_jobs=7, prefer="processes", verbose=10)(
            delayed(score_one)(params, sd, thr) for sd in seeds
        )
    except ImportError:
        res = [score_one(params, sd, thr) for sd in seeds]

    bad = [r for r in res if r["geometry_offset_used"] != UNREACHABLE]
    if bad:
        print(f"[characterize] GEOMETRY GUARD TRIPPED on {len(bad)} runs", file=sys.stderr)
        return 4

    bust = np.array([r["headline_bust"] for r in res])
    skew = np.array([r["realized_skew"] for r in res])
    maxw = np.array([r["realized_max_win"] for r in res])
    pcts = {p: float(np.percentile(bust, p)) for p in (10, 25, 50, 75, 90)}

    print(f"[characterize] bust mean={bust.mean():.4%} sd={bust.std(ddof=1):.4%} "
          f"min={bust.min():.4%} max={bust.max():.4%}", flush=True)
    print(f"[characterize] percentiles: " + " ".join(f"p{p}={v:.4%}" for p, v in pcts.items()),
          flush=True)
    print(f"[characterize] realized skew mean={skew.mean():.3f} (real book: +3.633)", flush=True)
    print(f"[characterize] realized max-win-per-realization mean={maxw.mean():.0f} "
          f"(real observed max: 4972)", flush=True)

    out = {
        "status": "scoping construction, follow-up to geofit_skew_probe_2026-07-25 + geofit_iid_sufficiency_power_2026-08-15; NOT part of the closed study",
        "design_decision": "win-branch tail PRESERVED, not capped (operator directed 2026-08-15) -- see family_skewed_gamma.py docstring",
        "real_bust_reference": 0.047433,
        "real_book_skew_reference": 3.6332326168850386,
        "real_book_max_win_reference": 4971.88121682013,
        "tier": TIER,
        "geometry": "CORRECTED (dd_lock_offset_usd -> 1e6)",
        "n_sims_per_seed": thr.sims_per_seed,
        "n_realizations": N_REALIZATIONS,
        "seed_base": SEED_BASE,
        "fitted_params": params,
        "bust_mean": float(bust.mean()),
        "bust_sd": float(bust.std(ddof=1)),
        "bust_min": float(bust.min()),
        "bust_max": float(bust.max()),
        "bust_percentiles": pcts,
        "realized_skew_mean": float(skew.mean()),
        "realized_max_win_mean": float(maxw.mean()),
        "runs": res,
    }
    (_HERE / "characterize.json").write_text(
        json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8"
    )
    print(f"[written] {_HERE / 'characterize.json'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
