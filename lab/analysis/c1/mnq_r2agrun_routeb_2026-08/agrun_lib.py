"""Q-R2AGRUN-1 Stage-G (G2) — statistic core. Pure functions; no I/O; no book access.

Implements PREREG_G0.md cell C1 exactly:
  feature A = signed aggressor-run trade-count (N_min=2)
  target r = 60 s mid return from run-completion time t
  promotion = Pearson ρ(A, r) with session-block CI / within-session r-shuffle placebo
"""
from __future__ import annotations

from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import numpy as np

SEED = 20260808
N_BOOT = 10_000
N_PLACEBO = 1_000
COV_MIN = 0.90
N_MIN = 2_000
MAG_FLOOR = 0.02
RUN_N_MIN = 2
HORIZON_S = 60
RTH_OPEN = time(9, 30)
RTH_LAST = time(15, 59)  # inclusive end for run close times
ET = ZoneInfo("America/New_York")

# Pre-registered EXPLORATION-window holiday / dark days (CME equity-index RTH closed).
# Same calendar as OFCHAN / R2VBUCK EXPLORATION (shared cache window).
EXCLUDED_SESSION_DATES: frozenset[date] = frozenset(
    {
        date(2026, 2, 16),  # Presidents Day
        date(2026, 4, 3),  # Good Friday
        date(2026, 5, 25),  # Memorial Day
        date(2026, 6, 19),  # Juneteenth
        date(2026, 7, 3),  # Independence Day observed
    }
)


def is_rth_session(session_day: date) -> bool:
    if session_day in EXCLUDED_SESSION_DATES:
        return False
    if session_day.weekday() >= 5:
        return False
    return True


def mid_price(bid_px: float, ask_px: float) -> float:
    return (float(bid_px) + float(ask_px)) / 2.0


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


def session_suff_stats(a: np.ndarray, r: np.ndarray) -> tuple[int, float, float, float, float, float]:
    """Return (n, Σa, Σr, Σa², Σr², Σar) for finite pairs — Pearson building blocks."""
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
    """Pearson ρ from pooled sufficient stats (identical to corrcoef on the concat)."""
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
    """95% CI on Pearson ρ, resampling whole sessions with replacement.

    Uses per-session sufficient statistics — algebraically identical to concatenating
    arrays each draw (avoids O(N_pairs × n_boot) copies on multi-million panels).
    """
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
    """Shuffle `r` within each session; recompute pooled ρ. Returns n placebo stats.

    Reuses fixed Σa/Σa² per session and in-place shuffles of working `r` buffers;
    same limbs as concat+corrcoef, without O(N) concatenation each draw.
    """
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


def _placebo_one_from_arrays(
    a_list: list[np.ndarray],
    r_list: list[np.ndarray],
    fixed_a: list[tuple[int, float, float]],
    seed_seq: np.random.SeedSequence,
) -> float:
    """One within-session r-shuffle placebo draw (independent SeedSequence child)."""
    rng = np.random.default_rng(seed_seq)
    n_tot = 0
    sa = sr = sa2 = sr2 = sar = 0.0
    for j, a in enumerate(a_list):
        rr = r_list[j].copy()
        rng.shuffle(rr)
        nj, saj, sa2j = fixed_a[j]
        n_tot += nj
        sa += saj
        sa2 += sa2j
        sr += float(rr.sum())
        sr2 += float(np.dot(rr, rr))
        sar += float(np.dot(a, rr))
    return pearson_rho_from_suff(n_tot, sa, sr, sa2, sr2, sar)


def within_session_r_shuffle_placebo_parallel(
    sessions: list[tuple[np.ndarray, np.ndarray]],
    n: int = N_PLACEBO,
    seed: int = SEED,
    workers: int = 1,
) -> np.ndarray:
    """Parallel placebo via SeedSequence(seed).spawn(n) — independent streams.

    Same within-session r-shuffle + pooled Pearson limb as the sequential helper;
    RNG is spawn-parallel rather than one sequentially-advanced Generator. Seed
    root remains ``seed`` (PREREG frozen).
    """
    if not sessions:
        return np.array([])
    if workers <= 1 or n < 4:
        return within_session_r_shuffle_placebo(sessions, n=n, seed=seed)

    a_list = [np.asarray(a, float) for a, _ in sessions]
    r_list = [np.asarray(r, float) for _, r in sessions]
    fixed_a = [(int(a.size), float(a.sum()), float(np.dot(a, a))) for a in a_list]
    children = np.random.SeedSequence(seed).spawn(n)

    # Thread pool: arrays stay shared; numpy releases GIL on shuffle/dot.
    from concurrent.futures import ThreadPoolExecutor

    stats = np.empty(n)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [
            pool.submit(_placebo_one_from_arrays, a_list, r_list, fixed_a, children[i])
            for i in range(n)
        ]
        for i, fut in enumerate(futs):
            stats[i] = fut.result()
    return stats


def halves_rho(
    sessions: list[tuple[np.ndarray, np.ndarray]],
    session_dates: list[date],
) -> tuple[float, float]:
    """Split by older/newer half of session dates; return (ρ_h1, ρ_h2)."""
    if not sessions:
        return float("nan"), float("nan")
    order = sorted(range(len(session_dates)), key=lambda i: session_dates[i])
    mid = len(order) // 2
    h1 = order[:mid]
    h2 = order[mid:]
    if not h1 or not h2:
        return float("nan"), float("nan")

    def _rho(idxs: list[int]) -> float:
        a = np.concatenate([sessions[i][0] for i in idxs])
        r = np.concatenate([sessions[i][1] for i in idxs])
        return pearson_rho(a, r)

    return _rho(h1), _rho(h2)


def verdict_g2(
    ci: tuple[float, float],
    observed: float,
    placebo: np.ndarray,
    coverage: float,
    n_retained: int,
    h1_rho: float,
    h2_rho: float,
) -> str:
    """PREREG §3 precedence: VOID-POWER → VOID-COVERAGE → CI → placebo → halves → magnitude."""
    if n_retained < N_MIN:
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
    if not (np.isfinite(h1_rho) and np.isfinite(h2_rho)):
        return "AMBIGUOUS-HOLD"
    if (h1_rho > 0) != (h2_rho > 0):
        return "AMBIGUOUS-HOLD"
    if abs(observed) < MAG_FLOOR:
        return "AMBIGUOUS-HOLD"
    return "PROMOTE"


def candidate_list(verdict: str, cell_id: str = "C1") -> list[str]:
    """Route B G2 emits 0 or 1 candidate IDs."""
    return [cell_id] if verdict == "PROMOTE" else []


def last_idx_at_or_before(ts_ns: np.ndarray, t_ns: int) -> int | None:
    i = np.searchsorted(ts_ns, t_ns, side="right") - 1
    if i < 0:
        return None
    return int(i)


def close_aggressor_runs(
    ts_ns: np.ndarray,
    side: np.ndarray,
    n_min: int = RUN_N_MIN,
) -> tuple[np.ndarray, np.ndarray]:
    """Walk prints in order; emit completed same-side aggressor runs with n_trades ≥ n_min.

    Side ``N`` (or any non-B/A) breaks the current run without starting a new one.
    Completion time = timestamp of the last trade in the run.
    Returns (end_ts_ns, signed_A) where A = +n_trades for B, −n_trades for A.
    """
    ends: list[int] = []
    feats: list[float] = []
    cur_side: str | None = None
    cur_n = 0
    cur_end = 0

    def _flush() -> None:
        nonlocal cur_side, cur_n, cur_end
        if cur_side is not None and cur_n >= n_min:
            sign = 1.0 if cur_side == "B" else -1.0
            ends.append(int(cur_end))
            feats.append(sign * float(cur_n))
        cur_side = None
        cur_n = 0
        cur_end = 0

    for t, sd in zip(ts_ns, side, strict=True):
        s = str(sd)
        if s not in ("B", "A"):
            _flush()
            continue
        if cur_side is None:
            cur_side = s
            cur_n = 1
            cur_end = int(t)
            continue
        if s == cur_side:
            cur_n += 1
            cur_end = int(t)
            continue
        # side flip — close prior run, start new
        _flush()
        cur_side = s
        cur_n = 1
        cur_end = int(t)

    _flush()
    return (
        np.asarray(ends, dtype=np.int64),
        np.asarray(feats, dtype=float),
    )


def rth_mask_ns(ts_ns: np.ndarray, session_day: date) -> np.ndarray:
    """Boolean mask: timestamps inside RTH 09:30–15:59 ET on session_day."""
    open_ns = int(
        datetime.combine(session_day, RTH_OPEN, tzinfo=ET).timestamp() * 1e9
    )
    last_excl = datetime.combine(session_day, time(16, 0), tzinfo=ET)
    last_ns = int(last_excl.timestamp() * 1e9)
    t = np.asarray(ts_ns, dtype=np.int64)
    return (t >= open_ns) & (t < last_ns)


def sample_pairs_for_day(
    ts_ns: np.ndarray,
    side: np.ndarray,
    bid_px: np.ndarray,
    ask_px: np.ndarray,
    session_day: date,
) -> tuple[np.ndarray, np.ndarray, int, int]:
    """Build retained (A, r) for one RTH session from aggressor runs.

    Eligible = completed runs with n_trades ≥ N_min whose end time t is inside RTH.
    Retained = eligible with finite A and valid mid at t and t+60s−.

    Returns (A, r, n_retained, n_eligible).
    """
    if not is_rth_session(session_day):
        return np.array([]), np.array([]), 0, 0
    if len(ts_ns) == 0:
        return np.array([]), np.array([]), 0, 0

    rth_mask = rth_mask_ns(ts_ns, session_day)
    if not rth_mask.any():
        return np.array([]), np.array([]), 0, 0

    ends, feats = close_aggressor_runs(
        ts_ns[rth_mask], side[rth_mask], n_min=RUN_N_MIN
    )
    n_eligible = int(len(ends))
    a_keep: list[float] = []
    r_keep: list[float] = []
    horizon_ns = HORIZON_S * 1_000_000_000
    for t_ns, a in zip(ends, feats, strict=True):
        i0 = last_idx_at_or_before(ts_ns, int(t_ns))
        i1 = last_idx_at_or_before(ts_ns, int(t_ns) + horizon_ns)
        if i0 is None or i1 is None:
            continue
        m0 = mid_price(float(bid_px[i0]), float(ask_px[i0]))
        m1 = mid_price(float(bid_px[i1]), float(ask_px[i1]))
        if not (np.isfinite(a) and np.isfinite(m0) and np.isfinite(m1) and m0 != 0.0):
            continue
        a_keep.append(float(a))
        r_keep.append(float((m1 - m0) / m0))
    return np.asarray(a_keep), np.asarray(r_keep), len(a_keep), n_eligible
