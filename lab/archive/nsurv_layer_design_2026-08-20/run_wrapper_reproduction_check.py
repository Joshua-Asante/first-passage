#!/usr/bin/env python3
"""Q-NSURV-2 Phase 1 -- additive magnitude-resampling wrapper, reproduction check.

Frozen per docs/briefs/pre-registration/Q-NSURV-2-verdict-preregistration.md
(2026-08-20, corrected pre-Phase-1). Pure JSON-artifact consumption: this script
imports nothing from lab/discovery/ or core/, calls no simulation code, and draws
no fresh MC realizations. It only reads the two candidates' already-committed
fitted-family artifacts and checks whether a wrapper built purely from their
stored per-realization data can (A) echo each candidate's single-history headline
unchanged and (B) independently recompute the resampled-distribution statistics
already stored in each artifact, within a 2.0pp tolerance.

$0, K=0 -- no data pull, no core/lab/discovery touch, no live-risk surface.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "lab" / "CATALOG.md").is_file():
            return parent
    raise SystemExit("cannot locate repo root from " + str(Path(__file__)))


REPO = _repo_root()
OUT_DIR = Path(__file__).resolve().parent
TOL_PP = 2.0

C1_ARTIFACT = REPO / "lab/analysis/c1/geofit_skewed_family_construction_2026-08-15/characterize.json"
ORB_ARTIFACT = REPO / "lab/analysis/c1/orbmnq1_nsurv_magnitude_probe_2026-08-20/nsurv_magnitude_probe_results.json"


def percentile(values: list[float], q: float) -> float:
    """Linear-interpolation percentile, matching numpy.percentile's default method."""
    s = sorted(values)
    n = len(s)
    if n == 1:
        return s[0]
    pos = (q / 100.0) * (n - 1)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return s[lo] + (s[hi] - s[lo]) * frac


def band(values: list[float]) -> dict:
    return {
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
        "sd": statistics.pstdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
        "p10": percentile(values, 10),
        "p25": percentile(values, 25),
        "p50": percentile(values, 50),
        "p75": percentile(values, 75),
        "p90": percentile(values, 90),
    }


def main() -> int:
    report: dict = {"tol_pp": TOL_PP, "candidates": {}}
    overall_ok = True

    print("=" * 96)
    print("Q-NSURV-2 Phase 1 -- additive wrapper reproduction check")
    print("=" * 96)

    # ---------------------------------------------------------- candidate 1: c1 book
    c1 = json.loads(C1_ARTIFACT.read_text(encoding="utf-8"))
    c1_headline_A = float(c1["real_bust_reference"]) * 100.0  # fraction -> pct
    c1_bust_pct_runs = [float(r["headline_bust"]) * 100.0 for r in c1["runs"]]
    c1_band = band(c1_bust_pct_runs)
    c1_stored_mean_pct = float(c1["bust_mean"]) * 100.0
    c1_stored_sd_pct = float(c1["bust_sd"]) * 100.0
    c1_delta_mean = c1_band["mean"] - c1_stored_mean_pct
    c1_delta_sd = c1_band["sd"] - c1_stored_sd_pct
    c1_ok = abs(c1_delta_mean) <= TOL_PP and abs(c1_delta_sd) <= TOL_PP

    print(f"\n--- c1 book ---")
    print(f"  (A) single-history headline (echoed): bust={c1_headline_A:.4f}%")
    print(f"  (B) recomputed from runs[] (n={len(c1_bust_pct_runs)}): "
          f"mean={c1_band['mean']:.4f}%  sd={c1_band['sd']:.4f}%")
    print(f"      artifact's own stored summary:      mean={c1_stored_mean_pct:.4f}%  sd={c1_stored_sd_pct:.4f}%")
    print(f"      delta: mean={c1_delta_mean:+.4f}pp  sd={c1_delta_sd:+.4f}pp  "
          f"{'PASS' if c1_ok else 'FAIL'} (tol {TOL_PP}pp)")

    report["candidates"]["c1"] = {
        "headline_A_bust_pct": c1_headline_A,
        "recomputed_B": c1_band,
        "stored_B_mean_pct": c1_stored_mean_pct,
        "stored_B_sd_pct": c1_stored_sd_pct,
        "delta_mean_pp": c1_delta_mean,
        "delta_sd_pp": c1_delta_sd,
        "reproduction_ok": c1_ok,
    }
    overall_ok &= c1_ok

    # ---------------------------------------------------------- candidate 2: ORB-MNQ-1
    orb = json.loads(ORB_ARTIFACT.read_text(encoding="utf-8"))
    orb_headline_A = orb["real_single_history_cushion"]["intraday_honest"]
    orb_bust_runs = [float(r["bust_pct"]) for r in orb["runs"]]
    orb_pass_runs = [float(r["pass_pct"]) for r in orb["runs"]]
    orb_bust_band = band(orb_bust_runs)
    orb_pass_band = band(orb_pass_runs)
    stored_dist = orb["distribution"]
    orb_delta_bust_mean = orb_bust_band["mean"] - float(stored_dist["bust_mean"])
    orb_delta_pass_mean = orb_pass_band["mean"] - float(stored_dist["pass_mean"])
    orb_delta_pass_sd = orb_pass_band["sd"] - float(stored_dist["pass_sd"])
    orb_ok = (
        abs(orb_delta_bust_mean) <= TOL_PP
        and abs(orb_delta_pass_mean) <= TOL_PP
        and abs(orb_delta_pass_sd) <= TOL_PP
    )

    print(f"\n--- ORB-MNQ-1 ---")
    print(f"  (A) single-history headline (echoed): bust={orb_headline_A['bust_pct']:.4f}%  "
          f"pass={orb_headline_A['pass_pct']:.4f}%")
    print(f"  (B) recomputed from runs[] (n={len(orb_bust_runs)}): "
          f"bust_mean={orb_bust_band['mean']:.4f}%  pass_mean={orb_pass_band['mean']:.4f}%  "
          f"pass_sd={orb_pass_band['sd']:.4f}%")
    print(f"      artifact's own stored summary:      "
          f"bust_mean={stored_dist['bust_mean']:.4f}%  pass_mean={stored_dist['pass_mean']:.4f}%  "
          f"pass_sd={stored_dist['pass_sd']:.4f}%")
    print(f"      delta: bust_mean={orb_delta_bust_mean:+.4f}pp  pass_mean={orb_delta_pass_mean:+.4f}pp  "
          f"pass_sd={orb_delta_pass_sd:+.4f}pp  {'PASS' if orb_ok else 'FAIL'} (tol {TOL_PP}pp)")

    report["candidates"]["orb_mnq_1"] = {
        "headline_A": orb_headline_A,
        "recomputed_B_bust": orb_bust_band,
        "recomputed_B_pass": orb_pass_band,
        "stored_B_bust_mean": float(stored_dist["bust_mean"]),
        "stored_B_pass_mean": float(stored_dist["pass_mean"]),
        "stored_B_pass_sd": float(stored_dist["pass_sd"]),
        "delta_bust_mean_pp": orb_delta_bust_mean,
        "delta_pass_mean_pp": orb_delta_pass_mean,
        "delta_pass_sd_pp": orb_delta_pass_sd,
        "reproduction_ok": orb_ok,
    }
    overall_ok &= orb_ok

    # ---------------------------------------------------------- verdict
    print("\n" + "=" * 96)
    if not overall_ok:
        verdict = "FALSIFIED"
    elif c1_ok and orb_ok:
        verdict = "RESOLVED"
    else:
        verdict = "AMBIGUOUS-HOLD"
    print(f"VERDICT (mechanical, per §6): {verdict}")
    print("=" * 96)

    report["c1_reproduction_ok"] = c1_ok
    report["orb_mnq_1_reproduction_ok"] = orb_ok
    report["overall_reproduction_ok"] = overall_ok
    report["verdict"] = verdict

    out = OUT_DIR / "wrapper_reproduction_results.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"\n[write] {out}")

    return 0 if overall_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
