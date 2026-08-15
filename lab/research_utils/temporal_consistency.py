#!/usr/bin/env python3
"""
temporal_consistency.py — Stage-6 temporal-consistency battery (Track B).

Four sub-tests on a single candidate's OOS edge series + timestamp index
(Stage-4 return-matrix contract: one candidate column + its timestamps):

  6a  sub-era sign consistency   — calendar-year sign count vs Thresholds
  6b  drop-top-year concentration — remaining edge > zero-edge gate
  6c  regime-slice survival      — external labels as TEST CONDITIONS only
  6d  own-edge CUSUM             — null via arch stationary block bootstrap

Thresholds and block size are REUSED from research_utils.universe_gate
(load_thresholds_from_prereg / acf_block_size) — never re-derived, never
hardcoded. CUSUM null uses arch.bootstrap.StationaryBootstrap (SKILL.md §8d /
"do not reimplement"); no hand-rolled IID null.

Research-venv-only (arch is NOT in pyproject.toml). Verdict hands to lifecycle
admission; never places an order (R6 = NO-GO).

Usage (research venv; lab on PYTHONPATH)
----------------------------------------
  PYTHONPATH=lab python -m research_utils.temporal_consistency \
      --returns <run>_returns.csv --candidate <id> \
      --prereg docs/briefs/pre-registration/<CAMP-ID>-preregistration.md
  PYTHONPATH=lab python -m research_utils.temporal_consistency --self-test
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# Canonical lab research primitives (lab->lab imports; lab is on PYTHONPATH).
from research_utils import universe_gate as _ug  # noqa: E402
from research_utils.prereg_paths import DISC_CAMP_0_PREREG  # noqa: E402

try:
    from arch.bootstrap import StationaryBootstrap  # type: ignore
    _ARCH_OK = True
except ImportError:  # pragma: no cover - env-dependent
    _ARCH_OK = False


# Re-export so callers / audits see the shared threshold + block-size path.
load_thresholds_from_prereg = _ug.load_thresholds_from_prereg
acf_block_size = _ug.acf_block_size
Thresholds = _ug.Thresholds


# ============================================================ helpers

def _year_of(ts) -> int:
    """Extract calendar year from an ISO8601-ish timestamp label."""
    s = str(ts)
    return int(s[:4])


def _year_sums(edge, timestamps) -> dict:
    """Sum edge by calendar year. Labels are grouping keys, not filters."""
    edge = np.asarray(edge, dtype=float)
    if len(edge) != len(timestamps):
        raise ValueError(
            f"edge length {len(edge)} != timestamps length {len(timestamps)}"
        )
    buckets: dict[int, float] = defaultdict(float)
    for e, ts in zip(edge, timestamps):
        if np.isfinite(e):
            buckets[_year_of(ts)] += float(e)
    return dict(sorted(buckets.items()))


def _cusum_stat(x) -> float:
    """Max |CUSUM| of demeaned per-period edge (confirmed Track-B convention)."""
    x = np.asarray(x, dtype=float).ravel()
    x = x[np.isfinite(x)]
    if x.size == 0:
        return 0.0
    demeaned = x - x.mean()
    return float(np.max(np.abs(np.cumsum(demeaned))))


# ============================================================ 6a

def sign_consistency(edge, timestamps, thresholds: Thresholds) -> dict:
    """6a — count OOS calendar years with positive summed edge.
    PASS iff positive_years >= thresholds.consistency_min and
    n_years >= thresholds.consistency_years (campaign Y bar)."""
    sums = _year_sums(edge, timestamps)
    n_years = len(sums)
    positive_years = sum(1 for v in sums.values() if v > 0)
    # Zero-edge gate for a year is v > 0 (strict); years with exactly 0 do not count.
    passed = (
        positive_years >= thresholds.consistency_min
        and n_years >= thresholds.consistency_years
    )
    return {
        "verdict": "PASS" if passed else "FAIL",
        "positive_years": positive_years,
        "n_years": n_years,
        "consistency_min": thresholds.consistency_min,
        "consistency_years": thresholds.consistency_years,
        "year_sums": sums,
    }


# ============================================================ 6b

def drop_top_year(edge, timestamps) -> dict:
    """6b — remove the single best calendar year; PASS iff remaining summed edge
    stays net-positive (> zero-edge / break-even gate)."""
    sums = _year_sums(edge, timestamps)
    if not sums:
        return {
            "verdict": "FAIL",
            "remaining_edge": 0.0,
            "dropped_year": None,
            "dropped_edge": 0.0,
        }
    dropped_year = max(sums, key=sums.get)
    dropped_edge = sums[dropped_year]
    remaining = sum(v for y, v in sums.items() if y != dropped_year)
    # Gate = zero-edge line (confirmed §0.5): remaining must stay net-positive.
    return {
        "verdict": "PASS" if remaining > 0 else "FAIL",
        "remaining_edge": float(remaining),
        "dropped_year": int(dropped_year),
        "dropped_edge": float(dropped_edge),
        "year_sums": sums,
    }


# ============================================================ 6c

def regime_slice_survival(edge, labels=None) -> dict:
    """6c — report edge per externally-supplied slice label; PASS iff every
    slice's summed edge is positive. Labels are TEST CONDITIONS, never filters
    (no series subsetting to a favorable regime — Q-REGIME-COND-1 scar).
    If labels is None → SKIPPED (not invent labels, not silent PASS)."""
    if labels is None:
        return {"verdict": "SKIPPED", "edge_per_slice": {}, "reason": "no_labels"}
    edge = np.asarray(edge, dtype=float)
    labels = np.asarray(labels)
    if len(edge) != len(labels):
        raise ValueError(
            f"edge length {len(edge)} != labels length {len(labels)}"
        )
    # Report edge per slice over the FULL series — never drop observations.
    per: dict = defaultdict(float)
    for e, lab in zip(edge, labels):
        if np.isfinite(e):
            per[lab] += float(e)
    edge_per_slice = {
        str(k): float(v)
        for k, v in sorted(per.items(), key=lambda kv: str(kv[0]))
    }
    if not edge_per_slice:
        return {"verdict": "FAIL", "edge_per_slice": {}, "reason": "empty"}
    passed = all(v > 0 for v in edge_per_slice.values())
    return {
        "verdict": "PASS" if passed else "FAIL",
        "edge_per_slice": edge_per_slice,
    }


# ============================================================ 6d

def edge_cusum(edge, *, block_size: int | None = None, reps: int = 1000,
               seed=None, alpha: float = 0.05) -> dict:
    """6d — CUSUM on the candidate's own edge; null via arch StationaryBootstrap
    at universe_gate.acf_block_size(edge). Statistic = max |CUSUM| of demeaned
    edge. TRIP (FAIL) if observed > (1-alpha) null quantile. Emits calibrated
    cusum_spec (decay-monitor artifact for admitted candidates)."""
    if not _ARCH_OK:
        raise RuntimeError("arch is not importable — run under .venv-research.")
    edge = np.asarray(edge, dtype=float).ravel()
    edge = edge[np.isfinite(edge)]
    if block_size is None:
        block_size = acf_block_size(edge)
    observed = _cusum_stat(edge)

    def _stat(x):
        return np.array([_cusum_stat(x)])

    bs = StationaryBootstrap(block_size, edge, seed=seed)
    null_stats = bs.apply(_stat, reps=reps).ravel()
    # Two-sided extreme: trip above the upper (1-alpha) quantile of the null.
    q = float(np.quantile(null_stats, 1.0 - alpha))
    tripped = observed > q
    cusum_spec = {
        "block_size": int(block_size),
        "alpha": float(alpha),
        "null_quantile": q,
        "null_mean": float(np.mean(null_stats)),
        "reps": int(reps),
        "statistic": "max_abs_cusum_demeaned",
    }
    return {
        "verdict": "FAIL" if tripped else "PASS",
        "observed_stat": float(observed),
        "cusum_spec": cusum_spec,
        "tripped": bool(tripped),
    }


# ============================================================ battery

@dataclass
class BatteryResult:
    overall: str                          # PASS | FAIL
    subtests: dict
    cusum_spec: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "overall": self.overall,
            "subtests": self.subtests,
            "cusum_spec": self.cusum_spec,
        }


def run_temporal_battery(edge, timestamps, thresholds: Thresholds, *,
                         labels=None, block_size: int | None = None,
                         reps: int = 1000, seed=None) -> dict:
    """Run 6a–6d; overall PASS iff every non-SKIPPED sub-test PASSes.
    SKIPPED (6c with no labels) does not fail the battery — it is recorded."""
    r6a = sign_consistency(edge, timestamps, thresholds)
    r6b = drop_top_year(edge, timestamps)
    r6c = regime_slice_survival(edge, labels=labels)
    # CUSUM alpha threads from the campaign alpha (not a hardcoded 0.05 in gate logic).
    r6d = edge_cusum(
        edge, block_size=block_size, reps=reps, seed=seed, alpha=thresholds.alpha,
    )
    sub = {"6a": r6a, "6b": r6b, "6c": r6c, "6d": r6d}
    active = [v["verdict"] for v in sub.values() if v["verdict"] != "SKIPPED"]
    overall = "PASS" if active and all(v == "PASS" for v in active) else "FAIL"
    return BatteryResult(
        overall=overall, subtests=sub, cusum_spec=r6d.get("cusum_spec", {}),
    ).as_dict()


def _planted_decaying_edge(n: int, rng: np.random.Generator) -> np.ndarray:
    """Linearly decaying expected edge that the block-bootstrap CUSUM can
    discriminate: early positive regime → late negative regime (the continuous
    linspace trend keeps ACF block-size so large that reshuffles preserve the
    ramp and the null tracks the observed; a two-regime decay is the form that
    trips under acf_block_size(edge) + StationaryBootstrap)."""
    half = n // 2
    return np.concatenate([
        rng.normal(0.04, 0.02, size=half),
        rng.normal(-0.04, 0.02, size=n - half),
    ])


# ============================================================ self-test

def self_test(*, thresholds: Thresholds, seed: int = 5, reps: int = 200) -> dict:
    """Planted-defect calibration: clean PASSes all four; each defect FAILS its
    target sub-test. A battery that cannot discriminate must not land."""
    rng = np.random.default_rng(seed)
    n_years = thresholds.consistency_years
    per_year = 20
    n = n_years * per_year

    def _stamps():
        from datetime import date, timedelta
        out = []
        for y in range(2019, 2019 + n_years):
            for i in range(per_year):
                d = date(y, 1, 1) + timedelta(days=int(i * 365 / per_year))
                out.append(d.isoformat())
        return out

    stamps = _stamps()
    labels_ab = np.array(["A", "B"] * (n // 2))
    if len(labels_ab) < n:
        labels_ab = np.append(labels_ab, "A")

    clean_edge = np.full(n, 0.02)
    clean = run_temporal_battery(
        clean_edge, stamps, thresholds, labels=labels_ab, seed=seed, reps=reps,
    )

    # 6b defect: one huge year, zeros elsewhere.
    conc = []
    for y in range(n_years):
        conc.append(np.full(per_year, 1.0 if y == 3 else 0.0))
    concentrated = run_temporal_battery(
        np.concatenate(conc), stamps, thresholds, labels=labels_ab, seed=seed, reps=reps,
    )

    # 6d defect: linearly decaying expected edge (two-regime form — see helper).
    decaying = run_temporal_battery(
        _planted_decaying_edge(n, rng), stamps, thresholds,
        labels=labels_ab, seed=seed, reps=reps,
    )

    # 6c defect: positive in one slice only.
    half = n // 2
    confined_edge = np.concatenate([np.full(half, 0.05), np.full(n - half, -0.02)])
    confined_labels = np.array(["A"] * half + ["B"] * (n - half))
    regime_confined = run_temporal_battery(
        confined_edge, stamps, thresholds, labels=confined_labels, seed=seed, reps=reps,
    )

    # 6a defect: only 4 of 7 years positive.
    chunks = []
    for y in range(n_years):
        chunks.append(np.full(per_year, 0.01 if y < 4 else -0.01))
    four_of_seven = run_temporal_battery(
        np.concatenate(chunks), stamps, thresholds, labels=labels_ab, seed=seed, reps=reps,
    )

    return {
        "clean": clean,
        "concentrated": concentrated,
        "decaying": decaying,
        "regime_confined": regime_confined,
        "four_of_seven": four_of_seven,
    }


# ============================================================ Stage-6 driver

def run_stage6(*, returns, benchmark, candidate_ids, candidate_index: int,
               timestamps, thresholds: Thresholds, cumulative_k: int,
               labels=None, seed=None, reps: int = 1000) -> dict:
    """Thin Stage-6 composer: universe_gate (8a/8b/8c) + temporal battery (6a–6d).
    Overall PASS only if both halves PASS/promote. Optional follow-on landed
    because Steps 2.1–2.5 landed cleanly."""
    edge = np.asarray(returns, dtype=float)[:, candidate_index]
    universe = _ug.run_universe_gate(
        returns=returns, benchmark=benchmark, candidate_ids=candidate_ids,
        cumulative_k=cumulative_k, thresholds=thresholds, seed=seed, reps=reps,
    )
    temporal = run_temporal_battery(
        edge, timestamps, thresholds, labels=labels, seed=seed, reps=reps,
    )
    stage6_pass = bool(universe.promote) and temporal["overall"] == "PASS"
    return {
        "overall": "PASS" if stage6_pass else "FAIL",
        "universe": {
            "promote": universe.promote,
            "gate_results": universe.gate_results,
            "nulls_alive": universe.nulls_alive,
            "best_id": universe.best_id,
        },
        "temporal": temporal,
    }


# ============================================================ CLI

def main():
    ap = argparse.ArgumentParser(description="Stage-6 temporal-consistency battery.")
    ap.add_argument("--returns", help="Stage-4 return matrix (CSV/parquet).")
    ap.add_argument("--candidate", help="Candidate column id to score.")
    ap.add_argument("--prereg", help="Campaign pre-registration (thresholds source).")
    ap.add_argument("--labels", default=None,
                    help="Optional CSV of regime labels aligned to the OOS index.")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--reps", type=int, default=1000)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--prereg-for-self-test", default=None)
    args = ap.parse_args()

    if args.self_test:
        prereg = args.prereg_for_self_test or DISC_CAMP_0_PREREG
        thr = load_thresholds_from_prereg(prereg)
        out = self_test(thresholds=thr, seed=args.seed or 5, reps=min(args.reps, 200))
        print(f"[self-test] clean overall={out['clean']['overall']} (must PASS)")
        print(f"[self-test] concentrated 6b={out['concentrated']['subtests']['6b']['verdict']} (must FAIL)")
        print(f"[self-test] decaying 6d={out['decaying']['subtests']['6d']['verdict']} (must FAIL)")
        print(f"[self-test] regime_confined 6c={out['regime_confined']['subtests']['6c']['verdict']} (must FAIL)")
        print(f"[self-test] four_of_seven 6a={out['four_of_seven']['subtests']['6a']['verdict']} (must FAIL)")
        ok = (
            out["clean"]["overall"] == "PASS"
            and out["concentrated"]["subtests"]["6b"]["verdict"] == "FAIL"
            and out["decaying"]["subtests"]["6d"]["verdict"] == "FAIL"
            and out["regime_confined"]["subtests"]["6c"]["verdict"] == "FAIL"
            and out["four_of_seven"]["subtests"]["6a"]["verdict"] == "FAIL"
        )
        print(f"[self-test] DISCRIMINATES: {ok}")
        sys.exit(0 if ok else 1)

    if not (args.returns and args.candidate and args.prereg):
        ap.error("provide --returns, --candidate, --prereg (or --self-test).")
    thr = load_thresholds_from_prereg(args.prereg)
    rm = _ug.load_returns_matrix(args.returns)
    if args.candidate not in rm.candidate_ids:
        raise SystemExit(f"candidate {args.candidate!r} not in {rm.candidate_ids}")
    idx = rm.candidate_ids.index(args.candidate)
    edge = rm.returns[:, idx]
    labels = None
    if args.labels:
        import csv as _csv
        with open(args.labels, newline="") as fh:
            rows = list(_csv.reader(fh))
        col = 0
        start = 1 if rows and not rows[0][0].replace(".", "", 1).lstrip("-").isdigit() else 0
        labels = np.array([r[col] for r in rows[start:]])
    result = run_temporal_battery(
        edge, rm.index, thr, labels=labels, seed=args.seed, reps=args.reps,
    )
    print(f"[battery] overall={result['overall']}")
    for k, v in result["subtests"].items():
        print(f"[battery]   {k}: {v['verdict']}")
    print(f"[battery] cusum_spec={result['cusum_spec']}")
    print("[battery] (verdict → lifecycle admission, NOT an order — R6 = NO-GO)")


if __name__ == "__main__":
    main()
