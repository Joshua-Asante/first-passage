"""R4 timing/memory dry-run for the Q-VOLREGIME-1 L5 pilot (C2-C4 compute bound).

SYNTHETIC DATA ONLY. Touches no vendor panel, computes no outcome-bearing
statistic, reads no real L5 result. Measures one null-replicate's work as
specified in DESIGN.md 4.2-4.4:

  step 1  OLS residualization of log-volume on the full baseline feature set
          (global, whole panel)
  step 2  causal reconstruction pass: pseudo_log_volume = fitted + rotated
          residual, then a trailing same-slot rolling threshold recomputed
          from the reconstructed values (vectorized per slot)
  step 3  pseudo_bias_volume via the instrument's own comparator
  step 4  fold-local scoring: for each of n_folds expanding purged folds, fit
          baseline and augmented (L2 logistic, C fixed) and score OOS

Panel shape mirrors the real frames: MNQ 135,958 / MYM 139,605 scored rows,
96 M15 slots/day, ~9-10 folds, ~12 baseline features.

REPORTS CPU TIME, NOT JUST WALL TIME (Codex PR #258, P2). A core-hour budget
divided across N workers is only meaningful in CPU-seconds: if a replicate's
BLAS already spreads across threads, wall time understates core time and the
divide-by-N-workers arithmetic double-counts the same cores. This script pins
every numerical thread pool to 1 by default so wall and CPU time coincide, and
prints both so the gap is visible rather than assumed away. Run with
--native-threads to measure the unpinned behaviour for comparison.

Also reports PEAK WORKING SET for one worker process, so a concurrent-worker
memory bound can be computed rather than asserted.
"""
from __future__ import annotations

import argparse
import os
import sys

# Thread pinning must happen BEFORE numpy/sklearn import to take effect.
_PIN = "--native-threads" not in sys.argv
if _PIN:
    for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ[_var] = "1"

import time  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402

N_ROWS = 139_605          # MYM scored frame (l3_results.json)
N_SLOTS = 96              # M15 slots per 24h
N_FOLDS = 10              # DESIGN 3.4: floor((span_months - 12) / 6)
N_BASE_FEATURES = 12      # range, bias_range, 4 range lags, calendar controls
TRAIL_N = 20              # MYM trailing same-slot window
SETUP_FRAC = 12 / 71.0    # 12-month setup period out of ~71 months


def peak_working_set_mb() -> float | None:
    """Peak working set of THIS process, in MB. Windows-native; None elsewhere."""
    try:
        import ctypes
        from ctypes import wintypes

        class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        counters = PROCESS_MEMORY_COUNTERS()
        counters.cb = ctypes.sizeof(counters)
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        # K32GetProcessMemoryInfo (kernel32) is the modern export; psapi.dll's
        # GetProcessMemoryInfo is the legacy path. Try both before giving up.
        for fn in (getattr(ctypes.windll.kernel32, "K32GetProcessMemoryInfo", None),
                   getattr(ctypes.windll.psapi, "GetProcessMemoryInfo", None)):
            if fn is None:
                continue
            # argtypes/restype are load-bearing: without them the pseudo-handle
            # (-1) is truncated and the call silently reports failure.
            fn.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
                           wintypes.DWORD]
            fn.restype = wintypes.BOOL
            if fn(handle, ctypes.byref(counters), counters.cb):
                return counters.PeakWorkingSetSize / 1024**2
        return None
    except Exception:
        return None


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
    """One null replicate. Returns a (meaningless, synthetic) Brier delta."""
    # --- step 1: global OLS residualization of log-volume on baseline features
    coef, *_ = np.linalg.lstsq(X, df["log_volume"].to_numpy(), rcond=None)
    fitted = X @ coef
    resid = df["log_volume"].to_numpy() - fitted

    # --- step 2: global day-level rotation of residual vectors, then causal
    #             reconstruction of pseudo-volume
    n_days = int(df["day"].max()) + 1
    shift = int(rng.integers(1, n_days))
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

    # --- step 4: fold-local scoring, baseline and augmented
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--native-threads", action="store_true",
                        help="do NOT pin BLAS/OMP thread pools to 1")
    parser.add_argument("--reps", type=int, default=3)
    args = parser.parse_args()

    print(f"cores visible      : {os.cpu_count()}")
    print(f"thread pools pinned: {'no (native)' if args.native_threads else 'yes (1 thread)'}")

    df = make_panel()
    X = df[[f"x{j}" for j in range(N_BASE_FEATURES)]].to_numpy()
    y = df["y"].to_numpy()
    folds = build_folds(len(df))
    print(f"panel              : {len(df):,} rows, {N_BASE_FEATURES} base features, "
          f"{len(folds)} folds")
    print(f"train sizes        : {[len(tr) for tr, _ in folds]}")

    rng = np.random.default_rng(1)
    one_replicate(df, X, y, folds, rng)  # warm-up, not counted

    results = {}
    for label, fit_base in (("full (baseline refit per replicate)", True),
                            ("baseline cached (volume-free model is rotation-invariant)", False)):
        walls, cpus = [], []
        for _ in range(args.reps):
            w0, c0 = time.perf_counter(), time.process_time()
            one_replicate(df, X, y, folds, rng, fit_baseline=fit_base)
            walls.append(time.perf_counter() - w0)
            cpus.append(time.process_time() - c0)
        wall, cpu = float(np.median(walls)), float(np.median(cpus))
        results[fit_base] = (wall, cpu)
        print(f"\n{label}")
        print(f"  wall {wall:.3f} s   CPU {cpu:.3f} s   "
              f"CPU/wall = {cpu/wall:.2f} threads-worth")
        print(f"  -> budget unit for core-hours: {cpu:.3f} core-seconds/replicate")

    peak = peak_working_set_mb()
    print(f"\npeak working set (1 worker process): "
          f"{f'{peak:,.0f} MB' if peak else 'unavailable on this platform'}")
    if peak:
        for workers in (6, 64):
            print(f"  {workers} concurrent workers -> ~{peak*workers/1024:,.1f} GB resident")

    print("\nNOTE: multiply CPU-seconds (not wall) by replicate counts for a")
    print("core-hour budget; see rightsize_arithmetic.py for the budget table.")


if __name__ == "__main__":
    main()
