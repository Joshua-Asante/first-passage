"""R4 timing dry-run for the Q-VOLREGIME-1 L5 pilot (C2-C4 compute bound).

SYNTHETIC DATA ONLY. Touches no vendor panel, computes no outcome-bearing
statistic, reads no real L5 result. Pure wall-clock measurement of one
null-replicate's work as specified in DESIGN.md 4.2-4.4:

  step 1  OLS residualization of log-volume on the full baseline feature set
          (global, whole panel)
  step 2  causal reconstruction pass: pseudo_log_volume = fitted + rotated
          residual, then a trailing same-slot rolling threshold recomputed
          from the reconstructed values (vectorized per slot)
  step 3  pseudo_bias_volume via the instrument's own comparator
  step 4  fold-local scoring: for each of n_folds expanding purged folds, fit
          baseline_1 and augmented_1 (L2 logistic, C fixed) and score OOS

Panel shape mirrors the real frames: MNQ 135,958 / MYM 139,605 scored rows,
96 M15 slots/day, ~9-10 folds, ~12 baseline features.
"""
from __future__ import annotations

import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

N_ROWS = 139_605          # MYM scored frame (l3_results.json)
N_SLOTS = 96              # M15 slots per 24h
N_FOLDS = 10              # DESIGN 3.4: floor((span_months - 12) / 6)
N_BASE_FEATURES = 12      # range, bias_range, 4 range lags, calendar controls
TRAIL_N = 20              # MYM trailing same-slot window
SETUP_FRAC = 12 / 71.0    # 12-month setup period out of ~71 months


def make_panel(seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = N_ROWS
    df = pd.DataFrame({
        "slot": np.arange(n) % N_SLOTS,
        "day": np.arange(n) // N_SLOTS,
        "log_volume": rng.normal(10.0, 0.8, n),
    })
    for j in range(N_BASE_FEATURES):
        df[f"x{j}"] = rng.normal(0.0, 1.0, n)
    df["y"] = (rng.random(n) < 0.5).astype(int)
    return df


def one_replicate(df: pd.DataFrame, X: np.ndarray, y: np.ndarray,
                  folds: list[tuple[np.ndarray, np.ndarray]],
                  rng: np.random.Generator, fit_baseline: bool = True) -> float:
    """One null replicate. Returns the (meaningless, synthetic) Brier delta."""
    # --- step 1: global OLS residualization of log-volume on baseline features
    coef, *_ = np.linalg.lstsq(X, df["log_volume"].to_numpy(), rcond=None)
    fitted = X @ coef
    resid = df["log_volume"].to_numpy() - fitted

    # --- step 2: global day-level rotation of residual vectors, then causal
    #             reconstruction of pseudo-volume
    n_days = int(df["day"].max()) + 1
    shift = int(rng.integers(1, n_days))
    resid_by_day = resid.reshape(-1, N_SLOTS) if len(resid) % N_SLOTS == 0 else None
    if resid_by_day is None:
        usable = (len(resid) // N_SLOTS) * N_SLOTS
        resid_by_day = resid[:usable].reshape(-1, N_SLOTS)
    rotated = np.roll(resid_by_day, shift, axis=0).reshape(-1)
    pseudo_log_vol = fitted[:len(rotated)] + rotated
    pseudo_vol = np.exp(pseudo_log_vol)

    # trailing same-slot threshold, recomputed causally from the reconstruction
    s = pd.Series(pseudo_vol)
    slot = df["slot"].to_numpy()[:len(pseudo_vol)]
    thresh = s.groupby(slot).transform(
        lambda v: v.shift(1).rolling(TRAIL_N, min_periods=TRAIL_N).median())

    # --- step 3: pseudo_bias_volume (MYM comparator: strict >)
    pseudo_bias = (pseudo_vol > thresh.to_numpy()).astype(float)
    pseudo_bias = np.nan_to_num(pseudo_bias)

    # --- step 4: fold-local scoring, baseline_1 and augmented_1
    Xa = np.column_stack([X[:len(pseudo_bias)], pseudo_bias])
    brier_base_num = brier_aug_num = 0.0
    n_scored = 0
    for tr, te in folds:
        tr = tr[tr < len(pseudo_bias)]
        te = te[te < len(pseudo_bias)]
        if len(tr) == 0 or len(te) == 0:
            continue
        if fit_baseline:
            mb = LogisticRegression(C=1.0, max_iter=200, solver="lbfgs")
            mb.fit(X[tr], y[tr])
            pb = mb.predict_proba(X[te])[:, 1]
            brier_base_num += float(np.sum((pb - y[te]) ** 2))
        ma = LogisticRegression(C=1.0, max_iter=200, solver="lbfgs")
        ma.fit(Xa[tr], y[tr])
        pa = ma.predict_proba(Xa[te])[:, 1]
        brier_aug_num += float(np.sum((pa - y[te]) ** 2))
        n_scored += len(te)
    return (brier_base_num - brier_aug_num) / max(n_scored, 1)


def build_folds(n: int) -> list[tuple[np.ndarray, np.ndarray]]:
    """Expanding purged/embargoed folds: 6-month test blocks after a 12-month
    training-only setup period. Embargo = 4 trading days ~= 4*96 bars."""
    setup_end = int(n * SETUP_FRAC)
    block = (n - setup_end) // N_FOLDS
    embargo = 4 * N_SLOTS
    folds = []
    for k in range(N_FOLDS):
        te_start = setup_end + k * block
        te_end = te_start + block
        tr_end = max(te_start - embargo, 0)
        folds.append((np.arange(0, tr_end), np.arange(te_start, min(te_end, n))))
    return folds


def main() -> None:
    import os
    print(f"cores: {os.cpu_count()}")
    df = make_panel()
    X = df[[f"x{j}" for j in range(N_BASE_FEATURES)]].to_numpy()
    y = df["y"].to_numpy()
    folds = build_folds(len(df))
    print(f"panel: {len(df):,} rows, {N_BASE_FEATURES} base features, "
          f"{len(folds)} folds")
    print("train sizes:", [len(tr) for tr, _ in folds])
    print("test sizes :", [len(te) for _, te in folds])

    rng = np.random.default_rng(1)
    # warm-up (JIT/BLAS threadpool spin-up), not counted
    one_replicate(df, X, y, folds, rng)

    for label, fit_base in (("full (baseline refit per replicate)", True),
                            ("baseline cached (volume-free model is invariant)", False)):
        times = []
        for _ in range(3):
            t0 = time.perf_counter()
            one_replicate(df, X, y, folds, rng, fit_baseline=fit_base)
            times.append(time.perf_counter() - t0)
        med = float(np.median(times))
        print(f"\n{label}: {med:.3f} s/replicate  (runs: "
              f"{', '.join(f'{t:.3f}' for t in times)})")

        for study, reps in (("C2 null-size", 4 * 100 * 4000),
                            ("C3 power (primary + half)", 4 * 100 * 4000 * 2)):
            core_hours = med * reps / 3600
            print(f"  {study:28s} {reps:>10,} replicates -> "
                  f"{core_hours:>10,.0f} core-hours ({core_hours/24:>7,.0f} core-days)")
        total = med * (4 * 100 * 4000 * 3) / 3600
        print(f"  {'C2+C3 total':28s} {4*100*4000*3:>10,} replicates -> "
              f"{total:>10,.0f} core-hours ({total/24:>7,.0f} core-days)")


if __name__ == "__main__":
    main()
