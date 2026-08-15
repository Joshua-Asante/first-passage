#!/usr/bin/env python3
"""
universe_gate.py — Gen-2 §8 universe-level correction orchestrator.

Turns a closed discovery manifest + the Stage-4 K-candidate OOS return matrix +
the campaign's pre-registered thresholds into a per-family verdict {promote|reject}
and a "which nulls remain alive" ledger. Orchestrates VETTED PRIMITIVES ONLY:

  * SPA / StepM  (universe-level data-snooping)  ->  arch.bootstrap
  * DSR          (deflated Sharpe under K)       ->  deflated_sharpe.py (sibling)
  * PBO          (backtest-overfit probability)  ->  skfolio CombinatorialPurgedCV

Nothing here re-implements a bootstrap, a normal-null, SPA, or CPCV — the subtle
correctness lives in the library (strategy-validation SKILL.md §8 "do not
reimplement"). Research-venv-only (arch + skfolio are NOT in pyproject.toml, per
the databento-research-stack ADR isolation rule).

The verdict is ALWAYS a hand-off to the strategies-never-locked lifecycle admission
(CANDIDATE) — never an auto-deploy, never an order (R6 = NO-GO).

Stage-4 return-matrix contract (operator-approved 2026-07-12, gate-orchestrator
handoff §0.5(B) option (i)):
  a CSV/parquet with a timestamp index column (`timestamp`, ISO8601 OOS bars),
  one column per candidate (any header; order preserved as the candidate id), and
  exactly one `benchmark` column (the zero-edge / buy-hold series on the same
  index). Values are per-period returns. Stage-4 (Score) must emit this file; the
  gate reads candidate columns as the K-model set and `benchmark` as the SPA
  benchmark. A single candidate column + `benchmark` is also the input the sibling
  temporal-consistency battery (Track B) consumes.

Usage (research venv; lab on PYTHONPATH)
----------------------------------------
  PYTHONPATH=lab python -m research_utils.universe_gate \
      --manifest discovery_manifests/<run_id>.json \
      --returns <run_id>_returns.csv \
      --prereg docs/briefs/pre-registration/<CAMP-ID>-preregistration.md
  PYTHONPATH=lab python -m research_utils.universe_gate --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# Canonical lab research primitives (lab->lab imports; lab is on PYTHONPATH).
from research_utils.deflated_sharpe import (  # noqa: E402
    deflated_sharpe as _ds_deflated,
    expected_max_sharpe as _ds_expected_max,
    moments_from_returns as _ds_moments,
)
from research_utils.prereg_paths import DISC_CAMP_0_PREREG  # noqa: E402

# arch / skfolio are heavy, research-venv-only; import lazily so `--help` and the
# threshold/matrix helpers work even where they are absent, and the science paths
# fail loudly with a clear message.
try:
    from arch.bootstrap import SPA, StepM  # type: ignore
    _ARCH_OK = True
except ImportError:  # pragma: no cover - env-dependent
    _ARCH_OK = False

try:
    from skfolio.model_selection import CombinatorialPurgedCV  # type: ignore
    _SKFOLIO_OK = True
except ImportError:  # pragma: no cover - env-dependent
    _SKFOLIO_OK = False


# ============================================================ thresholds

@dataclass(frozen=True)
class Thresholds:
    """Pre-registered gate thresholds, READ from a campaign pre-registration file
    (never hardcoded here — that read-from-file rule is what stops the gate drifting
    from the ratified campaign defaults)."""

    alpha: float
    dsr_min: float
    pbo_max: float
    consistency_min: int
    consistency_years: int


def load_thresholds_from_prereg(path) -> Thresholds:
    """Parse the frozen §3 summary line of a campaign pre-registration, e.g.
    '**alpha = 0.05. DSR threshold = 0.95. PBO ceiling = 0.5. Consistency = 5/7.**'.
    Raises ValueError if any threshold is absent — no silent default."""
    text = Path(path).read_text(encoding="utf-8")

    def _num(pattern: str, label: str) -> str:
        m = re.search(pattern, text)
        if not m:
            raise ValueError(
                f"pre-registration {path} has no parseable {label} threshold "
                f"(expected the frozen §3 summary line); refusing to guess a default."
            )
        return m.group(1)

    alpha = float(_num(r"(?:α|alpha)\s*=\s*([0-9]*\.?[0-9]+)", "alpha"))
    dsr_min = float(_num(r"DSR threshold\s*=\s*([0-9]*\.?[0-9]+)", "DSR"))
    pbo_max = float(_num(r"PBO ceiling\s*=\s*([0-9]*\.?[0-9]+)", "PBO"))
    cm = re.search(r"Consistency\s*=\s*(\d+)\s*/\s*(\d+)", text)
    if not cm:
        raise ValueError(f"pre-registration {path} has no parseable Consistency = k/Y.")
    return Thresholds(
        alpha=alpha,
        dsr_min=dsr_min,
        pbo_max=pbo_max,
        consistency_min=int(cm.group(1)),
        consistency_years=int(cm.group(2)),
    )


# ============================================================ block size

def acf_block_size(series, max_lag: int | None = None) -> int:
    """Smallest lag at which the series autocorrelation first falls inside the 95%
    white-noise band (+/- 1.96/sqrt(n)), rounded up — the frozen block-size rule.
    This deliberately REPLACES the arch sqrt(T) default (SKILL.md §8a / campaign
    pre-reg §4). Returns >= 1 (iid -> 1)."""
    x = np.asarray(series, dtype=float)
    x = x[np.isfinite(x)]
    n = x.size
    if n < 8:
        return 1
    if max_lag is None:
        max_lag = min(n - 1, max(10, int(np.sqrt(n)) * 3))
    x = x - x.mean()
    denom = np.dot(x, x)
    if denom <= 0:
        return 1
    band = 1.96 / np.sqrt(n)
    for lag in range(1, max_lag + 1):
        r = np.dot(x[:-lag], x[lag:]) / denom
        if abs(r) <= band:
            return lag
    return max_lag


# ============================================================ matrix I/O

@dataclass(frozen=True)
class ReturnsMatrix:
    returns: np.ndarray          # (T, K) per-period candidate returns
    benchmark: np.ndarray        # (T,) benchmark (zero-edge) returns
    candidate_ids: list          # length K, column order preserved
    index: list                  # length T, the timestamp labels


def load_returns_matrix(path) -> ReturnsMatrix:
    """Load the Stage-4 K-candidate OOS return matrix (see module docstring for the
    contract). First column = timestamp index; exactly one `benchmark` column; all
    other columns = candidates in file order."""
    p = Path(path)
    if p.suffix.lower() in (".parquet", ".pq"):
        import pandas as pd  # local import: parquet path only
        df = pd.read_parquet(p)
        index = list(df.index.astype(str)) if df.index.name else list(df.iloc[:, 0].astype(str))
    else:
        import csv as _csv
        with open(p, newline="") as fh:
            rows = [r for r in _csv.reader(fh) if r]
        if len(rows) < 2:
            raise ValueError(f"{path}: need a header + at least one data row.")
        header = [h.strip() for h in rows[0]]
        data = rows[1:]
        import pandas as pd
        df = pd.DataFrame(data, columns=header)
        index = list(df[header[0]].astype(str))
        df = df.drop(columns=[header[0]]).apply(lambda c: c.astype(float))

    cols = list(df.columns)
    bench_cols = [c for c in cols if str(c).strip().lower() == "benchmark"]
    if len(bench_cols) != 1:
        raise ValueError(
            f"{path}: Stage-4 contract requires exactly one 'benchmark' column "
            f"(found {len(bench_cols)}). Columns: {cols}"
        )
    bench = bench_cols[0]
    cand_ids = [str(c) for c in cols if c != bench]
    if not cand_ids:
        raise ValueError(f"{path}: no candidate columns beside 'benchmark'.")
    returns = df[cand_ids].to_numpy(dtype=float)
    benchmark = df[bench].to_numpy(dtype=float)
    return ReturnsMatrix(returns=returns, benchmark=benchmark,
                         candidate_ids=cand_ids, index=index)


# ============================================================ vetted-primitive runners

def _sharpe_cols(returns: np.ndarray) -> np.ndarray:
    """Per-column per-observation Sharpe (mean/std, ddof=1)."""
    mean = returns.mean(axis=0)
    sd = returns.std(axis=0, ddof=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        sr = np.where(sd > 0, mean / sd, 0.0)
    return sr


def run_spa(benchmark, models, block_size: int, better_cutoff: float,
            reps: int = 1000, seed=None):
    """arch SPA (White Reality Check / Hansen SPA). Returns (consistent p-value,
    list of better-model column indices at `better_cutoff`). Frames returns as
    losses (lower = better) so the null 'benchmark not inferior to any model'
    rejects when a model out-earns the benchmark. `better_cutoff` is the pre-registered
    alpha, threaded in — never hardcoded."""
    if not _ARCH_OK:
        raise RuntimeError("arch is not importable — run under .venv-research.")
    bench_loss = -np.asarray(benchmark, dtype=float)
    model_loss = -np.asarray(models, dtype=float)
    spa = SPA(bench_loss, model_loss, block_size=block_size,
              bootstrap="stationary", reps=reps, seed=seed)
    spa.compute()
    pv = spa.pvalues
    try:
        p = float(pv["consistent"])
    except (KeyError, TypeError, ValueError):
        p = float(np.asarray(pv)[1])
    try:
        better = [int(i) for i in np.atleast_1d(spa.better_models(better_cutoff))]
    except Exception:
        better = []
    return p, better


def run_stepm(benchmark, models, block_size: int, size: float, reps: int = 1000, seed=None):
    """arch StepM (Romano-Wolf): FWER-controlled superior set. Returns column indices."""
    if not _ARCH_OK:
        raise RuntimeError("arch is not importable — run under .venv-research.")
    bench_loss = -np.asarray(benchmark, dtype=float)
    model_loss = -np.asarray(models, dtype=float)
    stepm = StepM(bench_loss, model_loss, size=size, block_size=block_size,
                  bootstrap="stationary", reps=reps, seed=seed)
    stepm.compute()
    superior = stepm.superior_models
    out = []
    for s in np.atleast_1d(superior):
        try:
            out.append(int(s))
        except (TypeError, ValueError):
            # arch may return column labels ("model.3"); pull the trailing int.
            m = re.search(r"(\d+)$", str(s))
            if m:
                out.append(int(m.group(1)))
    return out


def run_dsr_gate(best_returns, cumulative_k: int, var_trials: float, dsr_min: float):
    """DSR on the selected candidate. Delegates every statistic to deflated_sharpe.py;
    K = cumulative-family trial count, V = across-trials Sharpe variance."""
    sr, n, skew, kurt = _ds_moments(list(np.asarray(best_returns, dtype=float)))
    sr0 = _ds_expected_max(cumulative_k, max(var_trials, 1e-12))
    dsr = _ds_deflated(sr, n, skew, kurt, sr0)
    return {"dsr": dsr, "passed": dsr >= dsr_min, "sr": sr, "sr0": sr0, "n": n}


def pbo_via_cpcv(returns: np.ndarray, n_folds: int = 10, n_test_folds: int = 8,
                 purged_size: int = 0, embargo_size: int = 0) -> float:
    """Probability of Backtest Overfitting over skfolio CombinatorialPurgedCV paths.
    Per split: rank configs IS (train) vs OOS (test); PBO = fraction of splits where
    the IS-best config lands in the OOS bottom half. skfolio generates the purged /
    embargoed splits (leakage control lives in the library); the rank tally is the
    §8c estimator, not a reimplemented cross-validator."""
    if not _SKFOLIO_OK:
        raise RuntimeError("skfolio is not importable — run under .venv-research.")
    T, K = returns.shape
    if T < n_folds or K < 2:
        return float("nan")
    cv = CombinatorialPurgedCV(n_folds=n_folds, n_test_folds=n_test_folds,
                               purged_size=purged_size, embargo_size=embargo_size)
    X = returns
    y = np.zeros(T)
    bottom_half = 0
    n_splits = 0

    def _flat(idx):
        # skfolio returns the test set as a LIST of per-fold index arrays (shape
        # (n_test_folds, fold_len)); the train set is a flat array. Normalize both
        # to a unique 1-D row-index vector.
        if isinstance(idx, (list, tuple)):
            idx = np.concatenate([np.asarray(f).ravel() for f in idx])
        return np.unique(np.asarray(idx).ravel().astype(int))

    for train_idx, test_idx in cv.split(X, y):
        tr, te = _flat(train_idx), _flat(test_idx)
        if tr.size < 2 or te.size < 2:
            continue
        is_sr = _sharpe_cols(returns[tr])
        oos_sr = _sharpe_cols(returns[te])
        best = int(np.argmax(is_sr))
        # OOS rank fraction of the IS-best: 1/K (worst) .. 1.0 (best).
        oos_rank = (np.argsort(np.argsort(oos_sr))[best] + 1) / K
        # Structural median split (bottom half) from the LdP PBO definition — this
        # 0.5 is "half", NOT the pbo_max threshold (which lives in Thresholds).
        if oos_rank <= 0.5:
            bottom_half += 1
        n_splits += 1
    if n_splits == 0:
        return float("nan")
    return bottom_half / n_splits


# ============================================================ verdict

@dataclass
class GateVerdict:
    promote: bool
    spa_pvalue: float
    dsr: float
    pbo: float
    best_id: str
    best_index: int
    better_models: list
    superior_set: list
    gate_results: dict            # {'spa':bool, 'dsr':bool, 'pbo':bool}
    nulls_alive: list             # gates a candidate has NOT yet cleared
    detail: dict = field(default_factory=dict)


def run_universe_gate(*, returns, benchmark, candidate_ids, cumulative_k: int,
                      thresholds: Thresholds, block_size: int | None = None,
                      var_trials: float | None = None,
                      seed=None, reps: int = 1000, run_pbo: bool = True) -> GateVerdict:
    """Orchestrate SPA + DSR + PBO into a {promote|reject} verdict. `promote` iff SPA
    rejects (best beats benchmark) AND DSR >= dsr_min AND (PBO < pbo_max where config
    selection occurred). Verdict hands to lifecycle admission, never deploys.

    `var_trials` (V, the across-trial Sharpe variance DSR's SR0 consumes): pass an
    explicit value to PIN it. Default (None) is the theoretical null-sampling
    variance `1/n` on the selected candidate's finite OOS trade count, per
    `docs/adr/2026-07-12-dsr-k-rule-and-variance-floor-supersession.md` (the
    winning V-estimator; module default flipped 2026-08-15, gate-stack audit R5).
    The empirical `Var(col_sr, ddof=1)` estimator is no longer the default —
    it is biased upward at realistic K_SPA and collapses to 0.0 at K_SPA=1."""
    returns = np.asarray(returns, dtype=float)
    benchmark = np.asarray(benchmark, dtype=float)
    T, K = returns.shape

    if block_size is None:
        # ACF-derived on the pooled candidate series; never sqrt(T).
        block_size = acf_block_size(returns.mean(axis=1))

    # Selected candidate = IS-best (max in-sample Sharpe) — the winner of the search.
    col_sr = _sharpe_cols(returns)
    best_index = int(np.argmax(col_sr))
    best_id = candidate_ids[best_index]

    # 8a — universe correction.
    spa_p, better = run_spa(benchmark, returns, block_size=block_size,
                            better_cutoff=thresholds.alpha, reps=reps, seed=seed)
    superior = []
    if len(better) > 1:
        superior = run_stepm(benchmark, returns, block_size=block_size,
                             size=thresholds.alpha, reps=reps, seed=seed)
    spa_pass = spa_p < thresholds.alpha

    # 8b — deflated Sharpe on the selected candidate.
    if var_trials is None:
        n_sel = int(np.isfinite(returns[:, best_index]).sum())
        var_trials = 1.0 / max(n_sel, 1)
    dsr_info = run_dsr_gate(returns[:, best_index], cumulative_k, var_trials, thresholds.dsr_min)
    dsr_pass = dsr_info["passed"]

    # 8c — PBO via CPCV (selection occurred: best-of-K).
    pbo = pbo_via_cpcv(returns) if run_pbo else float("nan")
    pbo_pass = (not run_pbo) or (not np.isnan(pbo) and pbo < thresholds.pbo_max)

    gate_results = {"spa": bool(spa_pass), "dsr": bool(dsr_pass), "pbo": bool(pbo_pass)}
    promote = bool(spa_pass and dsr_pass and pbo_pass)
    nulls_alive = [g for g, ok in gate_results.items() if not ok]

    return GateVerdict(
        promote=promote,
        spa_pvalue=spa_p,
        dsr=dsr_info["dsr"],
        pbo=pbo,
        best_id=best_id,
        best_index=best_index,
        better_models=[candidate_ids[i] for i in better if 0 <= i < K],
        superior_set=[candidate_ids[i] for i in superior if 0 <= i < K],
        gate_results=gate_results,
        nulls_alive=nulls_alive,
        detail={
            "block_size": block_size,
            "cumulative_k": cumulative_k,
            "var_trials": var_trials,
            "sr": dsr_info["sr"],
            "sr0": dsr_info["sr0"],
            "n": dsr_info["n"],
            "n_candidates": K,
            "n_obs": T,
        },
    )


# ============================================================ self-test (calibration gate)

def self_test(*, thresholds: Thresholds, seed_ok: bool = True,
              var_trials: float | None = None) -> dict:
    """Wire the planted-overfit / planted-real controls from lab/validation_selftest
    into the gate. A correct gate REJECTS the pure-noise family and PROMOTES the
    injected-edge family. Returns {'negative': GateVerdict, 'positive': GateVerdict}.
    A gate that cannot discriminate is miscalibrated and must not land.

    `var_trials`: forwarded to `run_universe_gate` (None = module default `1/n`
    on the selected candidate's finite trade count; pass a pinned value to
    calibrate a campaign's frozen V-rule instead)."""
    # The extracted Gen-1 planted controls (lab/validation_selftest.py). Clean
    # lab->lab import now that universe_gate lives in lab/ (same import the sibling
    # DSR-gate test tests/test_validation_selftest_dsr_gate.py uses).
    from validation_selftest import (generate_negative_control,
                                      generate_positive_control)

    def _verdict(ctrl) -> GateVerdict:
        mat = np.column_stack(ctrl.trial_returns)          # (n_trades, n_trials)
        bench = np.zeros(mat.shape[0])                     # zero-edge benchmark
        ids = [f"trial_{i:04d}" for i in range(mat.shape[1])]
        return run_universe_gate(
            returns=mat, benchmark=bench, candidate_ids=ids,
            cumulative_k=mat.shape[1], thresholds=thresholds, seed=12345,
            var_trials=var_trials,
        )

    neg = generate_negative_control(n_trials=50, n_trades=300, seed=42)
    # A clearly-planted edge so "planted-real must be promoted" is unambiguous; the
    # control-strength kwargs are test-fixture choices, NOT campaign thresholds.
    pos = generate_positive_control(n_trials=30, n_trades=300, edge=0.02, vol=0.005, seed=7)
    return {"negative": _verdict(neg), "positive": _verdict(pos)}


# ============================================================ CLI

def _run_from_manifest(args) -> GateVerdict:
    manifest = json.loads(Path(args.manifest).read_text())
    thresholds = load_thresholds_from_prereg(args.prereg)
    rm = load_returns_matrix(args.returns)
    cumulative_k = args.cumulative_k if args.cumulative_k is not None else int(manifest.get("K", rm.returns.shape[1]))
    bs = args.block_size if args.block_size is not None else None
    return run_universe_gate(
        returns=rm.returns, benchmark=rm.benchmark, candidate_ids=rm.candidate_ids,
        cumulative_k=cumulative_k, thresholds=thresholds, block_size=bs,
        var_trials=args.var_trials, seed=args.seed,
    )


def _print_verdict(v: GateVerdict) -> None:
    print(f"[gate]  SPA p={v.spa_pvalue:.4f}  DSR={v.dsr:.4f}  PBO={v.pbo:.4f}")
    print(f"[gate]  gates: {v.gate_results}   nulls_alive: {v.nulls_alive}")
    print(f"[gate]  selected candidate: {v.best_id}  (better={len(v.better_models)}, "
          f"superior_set={len(v.superior_set)})")
    tag = "PROMOTE -> lifecycle admission (CANDIDATE)" if v.promote else "REJECT (nulls remain alive)"
    print(f"[gate]  VERDICT: {tag}")
    print("[gate]  (verdict is a hand-off to strategy-validation / lifecycle admission, "
          "NOT an order — R6 = NO-GO)")


def main():
    ap = argparse.ArgumentParser(description="Gen-2 §8 universe-gate orchestrator.")
    ap.add_argument("--manifest", help="Closed discovery_manifests/<run_id>.json")
    ap.add_argument("--returns", help="Stage-4 K-candidate OOS return matrix (CSV/parquet).")
    ap.add_argument("--prereg", help="Campaign pre-registration (thresholds source).")
    ap.add_argument("--cumulative-k", type=int, default=None,
                    help="Override cumulative-family K (else read from the manifest).")
    ap.add_argument("--block-size", type=int, default=None,
                    help="Stage-5 bound block size (else ACF-derived; never sqrt(T)).")
    ap.add_argument("--var-trials", type=float, default=None,
                    help="V: PIN the across-trial Sharpe variance DSR's SR0 consumes "
                         "(e.g. 1/n_trades). Default: 1/n on the selected candidate's "
                         "finite OOS trade count (gate-stack audit R5).")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--self-test", action="store_true",
                    help="Run the planted-noise/planted-edge calibration gate and exit.")
    ap.add_argument("--prereg-for-self-test", default=None,
                    help="Thresholds file for --self-test (default: DISC-CAMP-0 pre-reg).")
    args = ap.parse_args()

    if args.self_test:
        prereg = args.prereg_for_self_test or DISC_CAMP_0_PREREG
        thr = load_thresholds_from_prereg(prereg)
        res = self_test(thresholds=thr, var_trials=args.var_trials)
        print("[self-test] NEGATIVE (planted noise) — must REJECT:")
        _print_verdict(res["negative"])
        print("[self-test] POSITIVE (planted edge) — must PROMOTE:")
        _print_verdict(res["positive"])
        ok = (res["negative"].promote is False) and (res["positive"].promote is True)
        print(f"[self-test] DISCRIMINATES: {ok}")
        sys.exit(0 if ok else 1)

    if not (args.manifest and args.returns and args.prereg):
        ap.error("provide --manifest, --returns and --prereg (or --self-test).")
    _print_verdict(_run_from_manifest(args))


if __name__ == "__main__":
    main()
