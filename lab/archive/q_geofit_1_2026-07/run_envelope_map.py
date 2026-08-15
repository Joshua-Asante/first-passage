"""Q-GEOFIT-1 — trailing-DD funding-envelope map (SIGNED / FROZEN 2026-07-25 / JA).

Brief: ``docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md`` (§2 grid, §4 H-GEOFIT,
§6 dispositions, §8 run protocol). Nothing here re-decides a frozen number: the floor is
parsed from the survivor-scoring pre-registration, the tier constants come from
``FIRM_RULES``, and the engine is the frozen ``run_partition_mc`` primitive.

What it does
------------
Sweeps 288 pre-declared synthetic daily-P&L profiles through the frozen MC engine at
CORRECTED ``trailing_locking`` geometry (``dd_lock_offset_usd -> 1_000_000.0``; restored
after) on ``Tradeify_Select_100K``, and records per cell whether the frozen floor
(bust <= 3.0% AND P(pass) >= 50%) clears.

Grid (§2, FROZEN — no post-hoc extension; a finer map is a fresh pre-registration):
  sigma_d  in {0.05, 0.10, 0.15, 0.20, 0.30, 0.45} % of account, on ACTIVE days
  mu/sigma in {0.00, 0.025, 0.05, 0.075, 0.10, 0.15} daily edge ratio, on ACTIVE days
  shape    in {gaussian, student_t4, trend_mix(p_win=0.35), meanrev_mix(p_win=0.65)}
  z        in {0.0, 0.4} fraction of zero-P&L days
  => 6 x 6 x 4 x 2 = 288 cells; seed = 20260724 + cell_index; length 1692 bdays.

Validation anchors (§2) run BEFORE the grid is interpreted:
  A1 engine reproduction — real c1 series at 1.00x and 0.50x, corrected geometry, must
     reproduce the published corrected busts within +/-0.15pp (4.74% / 0.11%).
  A2 profile sufficiency — the c1 series' fitted 4-tuple cell must predict the real bust
     within +/-0.5pp. A miss routes to AMBIGUOUS-PARAMETERIZATION (§6).

Interpretive readings declared here (the brief fixes the axes, not these mechanics):
  R1 mu and sigma are ACTIVE-day moments. sigma_d is explicitly active-day in §2, and
     mu/sigma is the ratio of the same distribution's moments. This is what makes §2's
     "mu/sigma 0.10 ~ annualized Sharpe ~1.6" identity hold (0.10 * sqrt(252) = 1.587).
     z then separately modulates cadence, which is its declared role.
  R2 Active-day draws are affinely standardized to hit (mu, sigma) exactly. The MC
     block-bootstraps the empirical series, so the EMPIRICAL moments are the effective
     cell parameters; without standardization the sampling error on mu (~0.03*sigma at
     n~1000) is the same size as the mu/sigma grid spacing (0.025) and would mislabel
     cells. Standardization is affine, so it preserves each shape's skew/kurtosis exactly.
  R3 The active-day mask uses an exact count (floor(N*(1-z))) via permutation, so the
     realized z equals the declared z rather than carrying binomial noise.
Each cell records nominal AND realized moments so R2/R3 are auditable after the fact.

Parallelism hazard guarded here
-------------------------------
With process-based workers, ``firm_rules`` is re-imported fresh in each child, so a patch
applied only in the parent would leave workers running DEFECTIVE geometry while producing
entirely plausible-looking numbers. Every worker therefore applies the patch itself and
returns the ``dd_lock_offset_usd`` it actually used; the parent asserts all 288 cells
report the unreachable value before writing any verdict.

Exit codes:
  0 — completed (verdict written)
  2 — NEEDS_CONTEXT (missing panel bytes / 1R guard)
  3 — Phase-0 / governance intactness failure
  4 — geometry guard tripped (a cell ran at non-corrected geometry)
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[2]
_SCORING = _ROOT / "lab" / "analysis" / "class_s_candidate1_scoring_2026-07-15"
for _p in (_ROOT / "core", _ROOT / "lab", str(_SCORING), str(_HERE)):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

BRIEF = "docs/briefs/Q-GEOFIT-1-trailing-dd-funding-envelope.md"
GATE_PREREG_REL = "docs/briefs/pre-registration/2026-07-13-prop-survivor-scoring-prereg.md"

# ---------------------------------------------------------------- frozen §2 grid
TIER = "Tradeify_Select_100K"
SECONDARY_TIER = "MFFU_Rapid_100K"
ACCOUNT = 100_000.0
N_BDAYS = 1692  # panel-equivalent (real c1 panel 2020-01-06 -> 2026-06-30)
UNREACHABLE = 1_000_000.0
DEFECTIVE_OFFSET = 100  # the on-disk FIRM_RULES value, restored in `finally`
CELL_SEED_BASE = 20260724

SIGMA_D_PCT = (0.05, 0.10, 0.15, 0.20, 0.30, 0.45)
MU_SIG = (0.00, 0.025, 0.05, 0.075, 0.10, 0.15)
SHAPES = ("gaussian", "student_t4", "trend_mix_p035", "meanrev_mix_p065")
Z_FRAC = (0.0, 0.4)

PRACTICALITY_CEILING = 0.10  # §2/§4: mu/sigma <= 0.10 is "practical"

# Published corrected-geometry pins for anchor A1 (§2).
ANCHOR_PINS = {"1.00x": 0.0474, "0.50x": 0.0011}
ANCHOR_TOL = 0.0015   # +/-0.15pp
PROFILE_TOL = 0.005   # +/-0.5pp


def cells() -> list[dict]:
    """Deterministic cell enumeration — index order fixes the per-cell seed."""
    out = []
    for i, (sd, ms, sh, z) in enumerate(
        itertools.product(SIGMA_D_PCT, MU_SIG, SHAPES, Z_FRAC)
    ):
        out.append(
            {
                "cell_index": i,
                "sigma_d_pct": sd,
                "mu_sigma": ms,
                "shape": sh,
                "z": z,
                "seed": CELL_SEED_BASE + i,
                "practical": ms <= PRACTICALITY_CEILING,
            }
        )
    return out


# ------------------------------------------------------- synthetic generation (§2)
def _draw_active(shape: str, n: int, rng: np.random.Generator) -> np.ndarray:
    """Unit-ish draw for one shape; standardized by the caller (R2)."""
    if shape == "gaussian":
        return rng.standard_normal(n)
    if shape == "student_t4":
        # nu=4 -> Var = nu/(nu-2) = 2; standardize to unit variance.
        return rng.standard_t(4, size=n) / np.sqrt(2.0)
    if shape in ("trend_mix_p035", "meanrev_mix_p065"):
        p = 0.35 if shape == "trend_mix_p035" else 0.65
        # Two-point law with mean 0, sd 1: W = sqrt((1-p)/p), L = -sqrt(p/(1-p)).
        w = np.sqrt((1.0 - p) / p)
        loss = -np.sqrt(p / (1.0 - p))
        return np.where(rng.random(n) < p, w, loss)
    raise ValueError(f"unknown shape {shape!r}")


def make_series(
    *, sigma_d_pct: float, mu_sigma: float, shape: str, z: float, seed: int,
    n_bdays: int = N_BDAYS, account: float = ACCOUNT,
) -> tuple[np.ndarray, dict]:
    """Build one cell's daily-P&L series. Returns (series, realized-moment record)."""
    rng = np.random.default_rng(seed)
    sigma = sigma_d_pct / 100.0 * account
    mu = mu_sigma * sigma

    n_active = int(np.floor(n_bdays * (1.0 - z)))
    if n_active < 5:
        raise ValueError(f"z={z} leaves {n_active} active days; need >=5 for a week-block")

    raw = _draw_active(shape, n_active, rng)
    pre = {"mean": float(raw.mean()), "std": float(raw.std(ddof=1))}
    # R2: affine standardization pins (mu, sigma) exactly, preserving shape.
    s = raw.std(ddof=1)
    if s <= 0:
        raise ValueError(f"degenerate draw for shape={shape} seed={seed}")
    active = mu + sigma * (raw - raw.mean()) / s

    series = np.zeros(n_bdays, dtype=float)
    # R3: exact-count mask via permutation (realized z == declared z).
    idx = rng.permutation(n_bdays)[:n_active]
    series[np.sort(idx)] = active

    realized = {
        "n_active": int(n_active),
        "z_realized": float((series == 0.0).mean()),
        "active_mean": float(active.mean()),
        "active_std": float(active.std(ddof=1)),
        "active_mu_sigma": float(active.mean() / active.std(ddof=1)),
        "active_win_frac": float((active > 0).mean()),
        "all_day_mean": float(series.mean()),
        "all_day_std": float(series.std(ddof=1)),
        "prestandardize": pre,
        "nominal_mu_usd": float(mu),
        "nominal_sigma_usd": float(sigma),
    }
    return series, realized


# ------------------------------------------------------------------ worker (§8.3)
def _score_cell(cell: dict, thr, tier: str, n_sims: int | None) -> dict:
    """Run one cell in a worker process. Applies the geometry patch LOCALLY."""
    import firm_rules  # re-imported fresh in the child process

    prior = firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"]
    firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        import run_class_s_c1_regime_gate as R

        series, realized = make_series(
            sigma_d_pct=cell["sigma_d_pct"], mu_sigma=cell["mu_sigma"],
            shape=cell["shape"], z=cell["z"], seed=cell["seed"],
        )
        t0 = time.time()
        r = R.run_partition_mc(series, tier, thr, n_sims=n_sims)
        floor_ok = (
            r["headline_bust"] <= thr.eval_bust_ceiling
            and r["pass_rate"] >= thr.pass_floor
        )
        # Geometry attestation — read back what the engine actually used.
        used = float(firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"])
        return {
            **cell,
            "tier": tier,
            "headline_bust": float(r["headline_bust"]),
            "pass_rate": float(r["pass_rate"]),
            "floor_ok": bool(floor_ok),
            "median_days": _median_days(r),
            "realized": realized,
            "geometry_offset_used": used,
            "wall_s": round(time.time() - t0, 1),
        }
    finally:
        firm_rules.FIRM_RULES[tier]["dd_lock_offset_usd"] = prior


def _median_days(r: dict) -> float | None:
    """Diagnostic median days-to-pass, when the summary exposes it."""
    summ = r.get("summary") or {}
    for key in ("median_days_to_pass", "median_days", "days_to_pass_median"):
        if key in summ and summ[key] is not None:
            return float(summ[key])
    return None


# ------------------------------------------------------------- profile fit (A2)
def fit_profile(daily: np.ndarray) -> dict:
    """Declared mechanical fit of a real series onto the §2 4-tuple family.

    Rule (declared here; the brief fixes the axes, not the estimator):
      z        = fraction of exactly-zero days
      sigma_d  = active-day sd, as % of account
      mu/sigma = active-day mean / active-day sd
      shape    = student_t4 if active-day excess kurtosis > 3.0; else the nearer
                 mixture when |win_frac - p| <= 0.10 for p in (0.35, 0.65); else gaussian
    """
    d = np.asarray(daily, dtype=float).reshape(-1)
    active = d[d != 0.0]
    sd = float(active.std(ddof=1))
    mean = float(active.mean())
    win = float((active > 0).mean())
    m = active - mean
    exkurt = float((m**4).mean() / (m**2).mean() ** 2 - 3.0)

    if exkurt > 3.0:
        shape = "student_t4"
    elif abs(win - 0.35) <= 0.10 or abs(win - 0.65) <= 0.10:
        shape = "trend_mix_p035" if abs(win - 0.35) <= abs(win - 0.65) else "meanrev_mix_p065"
    else:
        shape = "gaussian"

    return {
        "z": float((d == 0.0).mean()),
        "sigma_d_pct": sd / ACCOUNT * 100.0,
        "mu_sigma": mean / sd,
        "shape": shape,
        "active_win_frac": win,
        "active_excess_kurtosis": exkurt,
        "n_active": int(active.size),
        "n_days": int(d.size),
    }


def snap_to_grid(fit: dict) -> dict:
    """Nearest declared cell + explicit out-of-range flags (no grid extension, §5)."""
    def near(val, opts):
        return min(opts, key=lambda o: abs(o - val))

    sd = near(fit["sigma_d_pct"], SIGMA_D_PCT)
    ms = near(fit["mu_sigma"], MU_SIG)
    z = near(fit["z"], Z_FRAC)
    oor = {
        "sigma_d_pct": not (min(SIGMA_D_PCT) <= fit["sigma_d_pct"] <= max(SIGMA_D_PCT)),
        "mu_sigma": not (min(MU_SIG) <= fit["mu_sigma"] <= max(MU_SIG)),
        "z": not (min(Z_FRAC) <= fit["z"] <= max(Z_FRAC)),
    }
    for c in cells():
        if (
            c["sigma_d_pct"] == sd and c["mu_sigma"] == ms
            and c["shape"] == fit["shape"] and c["z"] == z
        ):
            return {"cell": c, "out_of_range": oor, "any_out_of_range": any(oor.values())}
    raise RuntimeError("snap failed — grid enumeration inconsistent")


# ------------------------------------------------------------------------ anchors
def run_anchors(thr, n_sims: int | None, out: dict) -> dict:
    """A1 engine reproduction + A2 profile sufficiency, on the real c1 series."""
    sys.argv = [sys.argv[0]]
    import firm_rules
    import run_class_s_c1_scoring as S
    import run_class_s_c1_regime_gate as R

    S.phase0_verify()
    for leg in S.C1_STRATS:
        S.resolve_panel_path(leg)
    panel, meta, _ = S.build_scaled_panel(
        S.C1_STRATS, S.C1_ALLOCS, expect_1r=dict(S.EXPECTED_1R)
    )
    book_200k = panel.sum(axis=1).to_numpy(dtype=float)
    daily_100k = book_200k * (ACCOUNT / S.ACCOUNT)
    print(f"[geofit] panel {meta['panel_span']} n_bdays={meta['n_bdays']}", flush=True)

    res: dict = {"panel_meta": meta, "A1": {}, "A2": {}}
    firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = UNREACHABLE
    try:
        for arm, mult in (("1.00x", 1.00), ("0.50x", 0.50)):
            t0 = time.time()
            r = R.run_partition_mc(daily_100k * mult, TIER, thr, n_sims=n_sims)
            pin = ANCHOR_PINS[arm]
            ok = abs(r["headline_bust"] - pin) <= ANCHOR_TOL
            res["A1"][arm] = {
                "headline_bust": float(r["headline_bust"]),
                "pass_rate": float(r["pass_rate"]),
                "published_pin": pin,
                "abs_delta_pp": round(abs(r["headline_bust"] - pin) * 100, 4),
                "ok": bool(ok),
                "wall_s": round(time.time() - t0, 1),
            }
            print(
                f"[geofit] A1 {arm}: bust={r['headline_bust']:.2%} vs pin {pin:.2%} "
                f"-> {'MATCH' if ok else 'MISMATCH'}",
                flush=True,
            )

        # A2 — fit the real series onto the declared family.
        fit = fit_profile(daily_100k)
        snap = snap_to_grid(fit)
        real_bust = res["A1"]["1.00x"]["headline_bust"]
        print(
            f"[geofit] A2 fit: sigma_d={fit['sigma_d_pct']:.4f}% mu/sig={fit['mu_sigma']:.4f} "
            f"z={fit['z']:.4f} shape={fit['shape']} "
            f"(out_of_range={snap['out_of_range']})",
            flush=True,
        )

        # Nearest declared cell (clamped where the fit is out of range).
        t0 = time.time()
        nearest = _score_cell(snap["cell"], thr, TIER, n_sims)
        nearest_resid = abs(nearest["headline_bust"] - real_bust)

        # Diagnostic: exact fitted 4-tuple, off-grid. Tells the re-scope whether the
        # FAMILY is sufficient once RANGES are widened — a different repair from a
        # richer family. Never counted as a grid cell.
        exact_cell = {
            "cell_index": -1, "sigma_d_pct": fit["sigma_d_pct"], "mu_sigma": fit["mu_sigma"],
            "shape": fit["shape"], "z": fit["z"], "seed": CELL_SEED_BASE - 1,
            "practical": fit["mu_sigma"] <= PRACTICALITY_CEILING,
        }
        exact = _score_cell(exact_cell, thr, TIER, n_sims)
        exact_resid = abs(exact["headline_bust"] - real_bust)

        res["A2"] = {
            "fit": fit,
            "snapped_cell": snap["cell"],
            "out_of_range": snap["out_of_range"],
            "any_out_of_range": snap["any_out_of_range"],
            "real_bust": real_bust,
            "nearest_cell_bust": nearest["headline_bust"],
            "nearest_residual_pp": round(nearest_resid * 100, 4),
            "nearest_ok": bool(nearest_resid <= PROFILE_TOL),
            "offgrid_exact_bust": exact["headline_bust"],
            "offgrid_exact_residual_pp": round(exact_resid * 100, 4),
            "offgrid_exact_ok": bool(exact_resid <= PROFILE_TOL),
            "wall_s": round(time.time() - t0, 1),
        }
        print(
            f"[geofit] A2 nearest-cell bust={nearest['headline_bust']:.2%} vs real "
            f"{real_bust:.2%} resid={nearest_resid * 100:.2f}pp -> "
            f"{'OK' if nearest_resid <= PROFILE_TOL else 'MISS'}",
            flush=True,
        )
        print(
            f"[geofit] A2 off-grid exact bust={exact['headline_bust']:.2%} "
            f"resid={exact_resid * 100:.2f}pp (diagnostic)",
            flush=True,
        )
    finally:
        firm_rules.FIRM_RULES[TIER]["dd_lock_offset_usd"] = DEFECTIVE_OFFSET

    res["anchors_hold"] = bool(
        all(a["ok"] for a in res["A1"].values()) and res["A2"]["nearest_ok"]
    )
    out["anchors"] = res
    return res


# --------------------------------------------------------------------- grid sweep
def run_grid(
    thr, n_sims: int | None, n_jobs: int, out: dict, limit: int | None,
    ckpt_path: Path | None = None,
) -> list[dict]:
    """Chunked + checkpointed sweep.

    The full grid is a multi-hour run at frozen sims, so results are flushed to a
    checkpoint after every chunk and completed cells are skipped on restart. This is
    purely operational (a machine sleep must not destroy the run) — it changes no
    frozen number, and every cell is still scored exactly once by seed.
    """
    grid = cells()
    if limit:
        grid = grid[:limit]

    done: dict[int, dict] = {}
    if ckpt_path and ckpt_path.exists():
        for r in json.loads(ckpt_path.read_text(encoding="utf-8")):
            done[int(r["cell_index"])] = r
        print(f"[geofit] checkpoint: {len(done)} cells already scored", flush=True)

    todo = [c for c in grid if c["cell_index"] not in done]
    print(f"[geofit] grid: {len(grid)} cells ({len(todo)} to run), n_jobs={n_jobs}, "
          f"n_sims={n_sims or thr.sims_per_seed}", flush=True)

    t0 = time.time()
    try:
        from joblib import Parallel, delayed
        have_joblib = True
    except ImportError:
        have_joblib = False

    chunk = max(1, n_jobs * 2)
    for i in range(0, len(todo), chunk):
        batch = todo[i:i + chunk]
        if have_joblib and n_jobs != 1:
            res = Parallel(n_jobs=n_jobs, prefer="processes")(
                delayed(_score_cell)(c, thr, TIER, n_sims) for c in batch
            )
        else:
            res = [_score_cell(c, thr, TIER, n_sims) for c in batch]
        for r in res:
            done[int(r["cell_index"])] = r
        if ckpt_path:
            ckpt_path.write_text(
                json.dumps(sorted(done.values(), key=lambda r: r["cell_index"]),
                           indent=2, default=str) + "\n",
                encoding="utf-8",
            )
        el = time.time() - t0
        n_done = i + len(batch)
        rem = el * (len(todo) - n_done) / max(n_done, 1)
        print(
            f"[geofit] {len(done)}/{len(grid)} cells  ({el / 60:.1f}m elapsed, "
            f"~{rem / 60:.0f}m remaining)",
            flush=True,
        )

    results = [done[c["cell_index"]] for c in grid if c["cell_index"] in done]
    print(f"[geofit] grid done in {(time.time() - t0) / 60:.1f}m", flush=True)

    bad = [r for r in results if r["geometry_offset_used"] != UNREACHABLE]
    out["geometry_guard"] = {
        "checked": len(results),
        "violations": len(bad),
        "ok": not bad,
        "expected_offset": UNREACHABLE,
    }
    out["cells"] = results
    return results


def adjudicate(out: dict) -> dict:
    """§6 dispositions — anchors first, then the practical-cell count (§4)."""
    res = out.get("cells", [])
    anchors = out.get("anchors", {})
    practical = [c for c in res if c["practical"]]
    clearers = [c for c in practical if c["floor_ok"]]
    diag_clearers = [c for c in res if not c["practical"] and c["floor_ok"]]

    if not out.get("geometry_guard", {}).get("ok", True):
        verdict = "INVALID — geometry guard tripped (cells ran at non-corrected geometry)"
    elif not anchors.get("anchors_hold", False):
        verdict = "AMBIGUOUS-PARAMETERIZATION"
    elif clearers:
        verdict = "RESOLVED-ENVELOPE-NONEMPTY"
    else:
        verdict = "FALSIFIED-ENVELOPE-EMPTY"

    # §4 states "192 practical / 96 diagnostic", but the declared predicate
    # (mu/sigma <= 0.10) yields 240/48 — the stated counts require a STRICT <0.10.
    # §2's prose settles it ("a persistent daily edge ratio ABOVE 0.10 ..."), so <=
    # is executed and the counts are recorded as an arithmetic slip. The accept rule
    # (>=1 clears) is unaffected UNLESS every clearer sits exactly on the disputed
    # boundary, which is flagged here rather than silently resolved.
    strict = [c for c in clearers if c["mu_sigma"] < PRACTICALITY_CEILING]
    boundary_only = bool(clearers) and not strict

    # Census over the DECLARED grid, independent of how many cells were scored — so a
    # closed-at-anchors run still reports the real 240/48 split rather than 0/0.
    declared = cells()
    n_declared_practical = sum(1 for c in declared if c["practical"])

    out["adjudication"] = {
        "verdict": verdict,
        "n_cells_scored": len(res),
        "n_practical_scored": len(practical),
        "n_practical_clearing": len(clearers),
        "n_diagnostic_clearing": len(diag_clearers),
        "ceiling_reading": {
            "executed_predicate": "mu_sigma <= 0.10",
            "n_declared_cells": len(declared),
            "n_declared_practical": n_declared_practical,
            "n_declared_diagnostic": len(declared) - n_declared_practical,
            "n_practical_per_brief_text": 192,
            "n_diagnostic_per_brief_text": 96,
            "brief_count_discrepancy": n_declared_practical != 192,
            "n_clearing_strictly_below_ceiling": len(strict),
            "verdict_sensitive_to_ceiling_reading": boundary_only,
        },
        "practical_clearers": [
            {k: c[k] for k in ("cell_index", "sigma_d_pct", "mu_sigma", "shape", "z",
                               "headline_bust", "pass_rate")}
            for c in clearers
        ],
    }
    return out["adjudication"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--mode", choices=("anchors", "grid", "all", "close"), default="all",
        help="close: adjudicate from cached anchors WITHOUT running the grid "
             "(the §6 verdict keys on the anchors, so an anchor miss is closeable alone)",
    )
    ap.add_argument("--n-sims", type=int, default=None, help="override sims/seed (frozen 10k)")
    ap.add_argument("--n-jobs", type=int, default=7)
    ap.add_argument("--limit", type=int, default=None, help="smoke: first N cells only")
    ap.add_argument("--out", type=Path, default=_HERE / "envelope.json")
    ap.add_argument("--ckpt", type=Path, default=_HERE / "grid_checkpoint.json",
                    help="incremental cell results; completed cells skipped on restart")
    ap.add_argument("--anchors-out", type=Path, default=_HERE / "anchors.json")
    args = ap.parse_args(argv)

    from discovery.prop_survivor_scoring import load_scoring_thresholds

    thr = load_scoring_thresholds(_ROOT / GATE_PREREG_REL)
    if thr.eval_bust_ceiling != 0.03 or thr.pass_floor != 0.5:
        print(f"[geofit] PHASE0: gate ceilings drifted: {thr}", file=sys.stderr)
        return 3

    out: dict = {
        "brief": BRIEF,
        "signature": "SIGNED / FROZEN: 2026-07-25 / JA",
        "gate_prereg": GATE_PREREG_REL,
        "geometry": "CORRECTED (dd_lock_offset_usd -> 1_000_000.0)",
        "tier": TIER,
        "floor": {"bust_ceiling": thr.eval_bust_ceiling, "pass_floor": thr.pass_floor},
        "grid_spec": {
            "sigma_d_pct": list(SIGMA_D_PCT), "mu_sigma": list(MU_SIG),
            "shapes": list(SHAPES), "z": list(Z_FRAC),
            "n_cells": len(cells()), "seed_base": CELL_SEED_BASE,
            "n_bdays": N_BDAYS, "practicality_ceiling": PRACTICALITY_CEILING,
        },
        "n_sims_per_seed": args.n_sims or thr.sims_per_seed,
    }

    if args.mode == "close":
        if not args.anchors_out.exists():
            print("[geofit] close requires a cached anchors.json", file=sys.stderr)
            return 2
        out["anchors"] = json.loads(args.anchors_out.read_text(encoding="utf-8"))
        out["grid_executed"] = False
        out["grid_not_run_reason"] = (
            "Validation anchors MISSED (§2), so §6 admits no envelope claim from any "
            "cell. Operator elected 2026-07-25 to close on the anchor evidence rather "
            "than spend ~8h scoring a surface that cannot be published as an envelope. "
            "The 288-cell grid remains declared and unrun; re-running it is a matter of "
            "executing this same frozen runner, not of re-deciding the grid."
        )
        adj = adjudicate(out)
        args.out.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
        print(f"\n[geofit] VERDICT: {adj['verdict']}  (grid not executed)", flush=True)
        print(f"[written] {args.out}", flush=True)
        return 0

    if args.mode in ("anchors", "all"):
        if args.anchors_out.exists() and args.mode == "all":
            out["anchors"] = json.loads(args.anchors_out.read_text(encoding="utf-8"))
            print("[geofit] anchors: reusing cached result", flush=True)
        else:
            try:
                run_anchors(thr, args.n_sims, out)
            except Exception as e:  # NEEDS_CONTEXT class — do not improvise
                print(f"[geofit] NEEDS_CONTEXT during anchors: {e}", file=sys.stderr)
                out["anchors"] = {"error": str(e), "anchors_hold": False}
                args.out.write_text(json.dumps(out, indent=2, default=str) + "\n",
                                    encoding="utf-8")
                return 2
            args.anchors_out.write_text(
                json.dumps(out["anchors"], indent=2, default=str) + "\n", encoding="utf-8"
            )

    if args.mode in ("grid", "all"):
        run_grid(thr, args.n_sims, args.n_jobs, out, args.limit, ckpt_path=args.ckpt)
        if not out["geometry_guard"]["ok"]:
            print("[geofit] GEOMETRY GUARD TRIPPED — refusing to write a verdict",
                  file=sys.stderr)
            args.out.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
            return 4

    adj = adjudicate(out)
    args.out.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"\n[geofit] VERDICT: {adj['verdict']}", flush=True)
    print(
        f"[geofit] practical clearing {adj['n_practical_clearing']}/"
        f"{adj['n_practical_scored']} scored "
        f"(of {adj['ceiling_reading']['n_declared_practical']} declared practical)",
        flush=True,
    )
    print(f"[written] {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
