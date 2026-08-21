"""Q-CAPFLOW-1 Cap-spend — statistic core + Cap verdict gates.

Feature: R2FLOW-style signed aggressor sum on [OR_start, t_trigger).
Statistic: Pearson ρ(A, R) with CAPA-shaped W0–W5 gates (ρ, not mean-Δ).
Pure functions; no I/O; no book access.
"""
from __future__ import annotations

from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import numpy as np

SEED = 20260808
N_BOOT = 10_000
N_PLACEBO = 1_000
COV_MIN = 0.90
N_MIN = 30
MAG_FLOOR = 0.02
OR_OPEN = time(9, 30)  # OPEN_TOD_US — ORB engine OR open
ET = ZoneInfo("America/New_York")


def or_start_ns(session_day: date) -> int:
    """UTC nanoseconds for ORB OR open (09:30 ET) on the trigger's session day."""
    t = datetime.combine(session_day, OR_OPEN, tzinfo=ET)
    return int(t.timestamp() * 1e9)


def pearson_rho(a: np.ndarray, r: np.ndarray) -> float:
    a = np.asarray(a, float)
    r = np.asarray(r, float)
    mask = np.isfinite(a) & np.isfinite(r)
    a, r = a[mask], r[mask]
    if a.size < 2:
        return float("nan")
    if np.std(a) == 0.0 or np.std(r) == 0.0:
        return float("nan")
    return float(np.corrcoef(a, r)[0, 1])


def mean_split_delta(a: np.ndarray, r: np.ndarray) -> float:
    """Disclosure twin: mean(A | R ≥ median) − mean(A | R < median). Not a gate."""
    a = np.asarray(a, float)
    r = np.asarray(r, float)
    mask = np.isfinite(a) & np.isfinite(r)
    a, r = a[mask], r[mask]
    if a.size < 2:
        return float("nan")
    med = float(np.median(r))
    hi = a[r >= med]
    lo = a[r < med]
    if hi.size == 0 or lo.size == 0:
        return float("nan")
    return float(hi.mean() - lo.mean())


def session_suff_stats(a: np.ndarray, r: np.ndarray) -> tuple[int, float, float, float, float, float]:
    a = np.asarray(a, float)
    r = np.asarray(r, float)
    mask = np.isfinite(a) & np.isfinite(r)
    a, r = a[mask], r[mask]
    n = int(a.size)
    if n == 0:
        return 0, 0.0, 0.0, 0.0, 0.0, 0.0
    return (
        n,
        float(a.sum()),
        float(r.sum()),
        float(np.dot(a, a)),
        float(np.dot(r, r)),
        float(np.dot(a, r)),
    )


def pearson_rho_from_suff(
    n: int, sa: float, sr: float, sa2: float, sr2: float, sar: float
) -> float:
    if n < 2:
        return float("nan")
    num = sar - (sa * sr) / n
    da = sa2 - (sa * sa) / n
    dr = sr2 - (sr * sr) / n
    if da <= 0.0 or dr <= 0.0:
        return float("nan")
    return float(num / np.sqrt(da * dr))


def _pool_suff(
    rows: list[tuple[int, float, float, float, float, float]],
) -> tuple[int, float, float, float, float, float]:
    n = sa = sr = sa2 = sr2 = sar = 0.0
    for row in rows:
        n += row[0]
        sa += row[1]
        sr += row[2]
        sa2 += row[3]
        sr2 += row[4]
        sar += row[5]
    return int(n), sa, sr, sa2, sr2, sar


def session_block_bootstrap_rho(
    sessions: list[tuple[np.ndarray, np.ndarray]],
    n: int = N_BOOT,
    seed: int = SEED,
    q=(2.5, 97.5),
) -> tuple[float, float]:
    """95% CI on Pearson ρ, resampling whole sessions with replacement."""
    if not sessions:
        return float("nan"), float("nan")
    base = [session_suff_stats(a, r) for a, r in sessions]
    rng = np.random.default_rng(seed)
    n_s = len(base)
    stats = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, n_s, n_s)
        pooled = _pool_suff([base[j] for j in idx])
        stats[i] = pearson_rho_from_suff(*pooled)
    lo, hi = np.nanpercentile(stats, q)
    return float(lo), float(hi)


def within_session_r_shuffle_placebo(
    sessions: list[tuple[np.ndarray, np.ndarray]],
    n: int = N_PLACEBO,
    seed: int = SEED,
) -> np.ndarray:
    """Shuffle R within each session; recompute pooled ρ."""
    if not sessions:
        return np.array([])
    a_list = [np.asarray(a, float) for a, _ in sessions]
    r_work = [np.asarray(r, float).copy() for _, r in sessions]
    fixed_a = [(int(a.size), float(a.sum()), float(np.dot(a, a))) for a in a_list]
    rng = np.random.default_rng(seed)
    stats = np.empty(n)
    for i in range(n):
        n_tot = 0
        sa = sr = sa2 = sr2 = sar = 0.0
        for j, a in enumerate(a_list):
            rr = r_work[j]
            rng.shuffle(rr)
            nj, saj, sa2j = fixed_a[j]
            n_tot += nj
            sa += saj
            sa2 += sa2j
            sr += float(rr.sum())
            sr2 += float(np.dot(rr, rr))
            sar += float(np.dot(a, rr))
        stats[i] = pearson_rho_from_suff(n_tot, sa, sr, sa2, sr2, sar)
    return stats


def halves_rho(
    sessions: list[tuple[np.ndarray, np.ndarray]],
    session_dates: list[date],
) -> tuple[float, float]:
    if not sessions:
        return float("nan"), float("nan")
    order = sorted(range(len(session_dates)), key=lambda i: session_dates[i])
    mid = len(order) // 2
    h1, h2 = order[:mid], order[mid:]
    if not h1 or not h2:
        return float("nan"), float("nan")

    def _rho(idxs: list[int]) -> float:
        a = np.concatenate([sessions[i][0] for i in idxs])
        r = np.concatenate([sessions[i][1] for i in idxs])
        return pearson_rho(a, r)

    return _rho(h1), _rho(h2)


def signed_aggressor_sum(
    ts_ns: np.ndarray,
    size: np.ndarray,
    side: np.ndarray,
    t0_ns: int,
    t1_ns: int,
) -> float | None:
    """A = Σ size·(+1 B, −1 A) on prints in [t0_ns, t1_ns).

    Returns None when no B/A print falls in the window (uncovered — never 0.0).
    Side codes other than B/A are ignored.
    """
    ts_ns = np.asarray(ts_ns, dtype=np.int64)
    size = np.asarray(size, dtype=float)
    side = np.asarray(side)
    if t1_ns <= t0_ns:
        return None
    lo = int(np.searchsorted(ts_ns, int(t0_ns), side="left"))
    hi = int(np.searchsorted(ts_ns, int(t1_ns), side="left"))
    if hi <= lo:
        return None
    a = 0.0
    n_ba = 0
    for i in range(lo, hi):
        s = str(side[i])
        if s == "B":
            a += float(size[i])
            n_ba += 1
        elif s == "A":
            a -= float(size[i])
            n_ba += 1
    if n_ba == 0:
        return None
    return float(a)


def assemble_trigger_sessions(
    pairs: list[tuple[float | None, float | None, date]],
) -> tuple[list[tuple[np.ndarray, np.ndarray]], list[date], int]:
    """Group covered (A, R) by session date for bootstrap / placebo / halves.

    Returns (sessions, session_dates, n_dropped_uncovered).
    Each session is (A_array, R_array) of finite pairs that day.
    """
    by_day: dict[date, list[tuple[float, float]]] = {}
    dropped = 0
    for a, r, d in pairs:
        ok_a = a is not None and np.isfinite(a)
        ok_r = r is not None and np.isfinite(r)
        if not (ok_a and ok_r):
            dropped += 1
            continue
        by_day.setdefault(d, []).append((float(a), float(r)))
    sessions: list[tuple[np.ndarray, np.ndarray]] = []
    dates: list[date] = []
    for d in sorted(by_day):
        rows = by_day[d]
        sessions.append(
            (np.array([x[0] for x in rows], float), np.array([x[1] for x in rows], float))
        )
        dates.append(d)
    return sessions, dates, dropped


def verdict_capflow(
    ci: tuple[float, float],
    observed: float,
    placebo: np.ndarray,
    coverage: float,
    n_covered: int,
    h1_rho: float,
    h2_rho: float,
) -> str:
    """PREREG §5 precedence: W0 → W1 → W2 → W3 → W4a/W4b → W5."""
    if n_covered < N_MIN:
        return "VOID-POWER"
    if coverage < COV_MIN:
        return "VOID-COVERAGE"
    lo, hi = ci
    if not (np.isfinite(lo) and np.isfinite(hi) and np.isfinite(observed)):
        return "FALSIFIED"
    if lo <= 0.0 <= hi:
        return "FALSIFIED"
    p95 = float(np.percentile(np.abs(placebo), 95))
    if abs(observed) <= p95:
        return "FALSIFIED"
    if abs(observed) < MAG_FLOOR:
        return "AMBIGUOUS-HOLD"
    if not (np.isfinite(h1_rho) and np.isfinite(h2_rho)):
        return "AMBIGUOUS-HOLD"
    if (h1_rho > 0) != (h2_rho > 0):
        return "AMBIGUOUS-HOLD"
    return "RESOLVED"


def cap_spent(verdict: str) -> bool:
    return verdict == "RESOLVED"
