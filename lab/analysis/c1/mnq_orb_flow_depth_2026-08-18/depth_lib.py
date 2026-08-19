"""MNQFLOW-1-DEPTH — statistic core. Pure functions, no I/O, no book access.

Implements PREREG §2/§7 exactly (synthetic harness, §9 step 4):
  S3   A_depth = (Σ bid_0..9 − Σ ask_0..9) / (Σ bid_0..9 + Σ ask_0..9)
  S3'  A_L1 on level-0 only (parent construct formula)
  S2   full-range systematic sample: round(i × 254/29) for i = 0..29
  S5   session-block bootstrap 95% CI (10,000 reps, seed 20260818)
  S6   within-session sign-shuffle placebo (1,000 reps, same seed)
  S8   ratio = abs(A_depth diff) / abs(A_L1 subsample diff); EPS_RATIO floor
  §7   verdict gates W6 → W1b in frozen precedence

A session is represented as a float array whose element 0 is the TRIGGER's mean A
and elements 1.. are that session's CONTROL mean A values. Windows with no usable
quote contribute NO element (NO-DATA / uncovered) — never a 0.0.
"""
from __future__ import annotations

from typing import Mapping, Sequence, TypeVar

import numpy as np

SEED = 20260818
N_BOOT = 10_000
N_PLACEBO = 1_000
EPS_RATIO = 0.001
COV_MIN = 0.90
N_LEVELS = 10
PARENT_N = 255
SAMPLE_K = 30
SAMPLE_SPAN = 254  # round(i * SAMPLE_SPAN / (SAMPLE_K - 1))

# §2.3 control-selection frozen constants
CONTROL_K = 5
CONTROL_MIN = 2
TOD_TOLERANCE_MIN = 30.0
MIN_SEP_MIN = 15.0

T = TypeVar("T")


# --------------------------------------------------------------------------- S3 / S3'
def book_imbalance(bid_sizes, ask_sizes) -> float:
    """(sum bid − sum ask) / (sum bid + sum ask); nan when the book is empty."""
    b = float(np.asarray(bid_sizes, float).sum())
    a = float(np.asarray(ask_sizes, float).sum())
    tot = b + a
    if tot <= 0.0:
        return float("nan")
    return (b - a) / tot


def _level_sizes(quote: Mapping[str, float] | None, side: str) -> list[float]:
    """Extract size_00..size_09 from a Databento-shaped mapping; missing → 0."""
    if quote is None:
        return [0.0] * N_LEVELS
    out: list[float] = []
    for i in range(N_LEVELS):
        key = f"{side}_sz_{i:02d}"
        raw = quote.get(key, 0.0)
        out.append(0.0 if raw is None else float(raw))
    return out


def a_depth(
    quote: Mapping[str, float] | None = None,
    *,
    bid_sizes=None,
    ask_sizes=None,
) -> float:
    """10-level size-weighted imbalance (S3)."""
    if bid_sizes is not None or ask_sizes is not None:
        if bid_sizes is None or ask_sizes is None:
            raise ValueError("bid_sizes and ask_sizes must both be provided")
        return book_imbalance(bid_sizes, ask_sizes)
    return book_imbalance(_level_sizes(quote, "bid"), _level_sizes(quote, "ask"))


def a_l1(
    quote: Mapping[str, float] | None = None,
    *,
    bid_sizes=None,
    ask_sizes=None,
) -> float:
    """Level-0 imbalance only (S3') — matches parent asym(bid0, ask0)."""
    if bid_sizes is not None or ask_sizes is not None:
        if bid_sizes is None or ask_sizes is None:
            raise ValueError("bid_sizes and ask_sizes must both be provided")
        b = np.asarray(bid_sizes, float).ravel()
        a = np.asarray(ask_sizes, float).ravel()
        if b.size == 0 or a.size == 0:
            return float("nan")
        return book_imbalance([float(b[0])], [float(a[0])])
    bids = _level_sizes(quote, "bid")
    asks = _level_sizes(quote, "ask")
    return book_imbalance([bids[0]], [asks[0]])


def signed_imbalance(value: float, side: str) -> float:
    """Asymmetry signed toward the breakout direction (parent S3 convention)."""
    if side not in ("long", "short"):
        raise ValueError(f"side must be 'long' or 'short', got {side!r}")
    if not np.isfinite(value):
        return float("nan")
    return float(value) if side == "long" else float(-value)


def window_mean(values) -> float | None:
    """Mean over finite values in a 60s window. Empty / all-degenerate → None (NO-DATA)."""
    v = np.asarray(values, float).ravel()
    v = v[np.isfinite(v)]
    if v.size == 0:
        return None
    return float(v.mean())


# --------------------------------------------------------------------------- S8
def agreement_stats(
    depth_diff: float, l1_diff: float
) -> tuple[float | None, bool]:
    """ratio and sign_agree (S8). ratio is None when abs(l1_diff) < EPS_RATIO."""
    if abs(l1_diff) < EPS_RATIO:
        ratio: float | None = None
    else:
        ratio = abs(depth_diff) / abs(l1_diff)
    sign_agree = bool(np.sign(depth_diff) == np.sign(l1_diff))
    return ratio, sign_agree


# --------------------------------------------------------------------------- S2
def systematic_sample_indices(
    n: int = PARENT_N, k: int = SAMPLE_K
) -> tuple[int, ...]:
    """Full-range systematic sample: round(i × (n−1)/(k−1)) for i = 0..k−1.

    Uses Python builtin round (half-to-even), not numpy.
    """
    if k < 2:
        raise ValueError(f"k must be >= 2, got {k}")
    if n < k:
        raise ValueError(f"n={n} must be >= k={k}")
    span = n - 1
    return tuple(round(i * span / (k - 1)) for i in range(k))


def take_systematic_sample(chrono_list: Sequence[T]) -> tuple[T, ...]:
    """Apply S2 indices to a chronologically-ordered parent trigger list."""
    n = len(chrono_list)
    idxs = systematic_sample_indices(n=n, k=SAMPLE_K)
    return tuple(chrono_list[i] for i in idxs)


# --------------------------------------------------------------------------- S5 / S6 (parent idiom)
def assemble_sessions(pairs):
    """[(trigger_A, [control_A, ...]), ...] -> (sessions, no_trig, no_ctrl).

    NON-FINITE VALUES ARE DROPPED HERE (load-bearing — see parent flow_lib).
    """
    sessions, no_trig, no_ctrl = [], 0, 0
    for tA, cA in pairs:
        t_ok = tA is not None and np.isfinite(tA)
        c_ok = [x for x in cA if x is not None and np.isfinite(x)]
        if not t_ok:
            no_trig += 1
            continue
        if not c_ok:
            no_ctrl += 1
            continue
        sessions.append(np.array([float(tA)] + [float(x) for x in c_ok], float))
    return sessions, no_trig, no_ctrl


def _pad(sessions: list[np.ndarray]):
    """Ragged sessions -> (padded matrix, lengths). Element 0 of each row is the trigger."""
    if len(sessions) == 0:
        raise ValueError("no sessions")
    lens = np.array([len(s) for s in sessions], int)
    if np.any(lens < 2):
        raise ValueError("every session needs a trigger and >=1 control")
    for i, s in enumerate(sessions):
        if not np.isfinite(s).all():
            raise ValueError(
                f"session {i} carries a non-finite value; uncovered windows must be "
                f"dropped by assemble_sessions, never padded into a row"
            )
    width = int(lens.max())
    M = np.full((len(sessions), width), np.nan)
    for i, s in enumerate(sessions):
        M[i, : len(s)] = s
    return M, lens


def _stat_from_choice(M, lens, j):
    """Statistic when element j[i] plays the trigger role in session i."""
    rows = np.arange(M.shape[0])
    trig = M[rows, j]
    tot = np.nansum(M, axis=1)
    ctrl_sum = tot - trig
    ctrl_n = lens - 1
    return float(trig.mean() - ctrl_sum.sum() / ctrl_n.sum())


def observed_stat(sessions: list[np.ndarray]) -> float:
    M, lens = _pad(sessions)
    return _stat_from_choice(M, lens, np.zeros(len(sessions), int))


def means(sessions: list[np.ndarray]) -> tuple[float, float]:
    """(mean A_trigger, mean A_control)."""
    M, lens = _pad(sessions)
    trig = M[:, 0]
    ctrl_sum = np.nansum(M, axis=1) - trig
    return float(trig.mean()), float(ctrl_sum.sum() / (lens - 1).sum())


def session_block_bootstrap(
    sessions: list[np.ndarray],
    n: int = N_BOOT,
    seed: int = SEED,
    q=(2.5, 97.5),
) -> tuple[float, float]:
    """95% CI on the statistic, resampling whole sessions with replacement (S5)."""
    M, lens = _pad(sessions)
    rng = np.random.default_rng(seed)
    N = len(sessions)
    trig = M[:, 0]
    ctrl_sum = np.nansum(M, axis=1) - trig
    ctrl_n = lens - 1
    stats = np.empty(n)
    for r in range(n):
        idx = rng.integers(0, N, N)
        stats[r] = trig[idx].mean() - ctrl_sum[idx].sum() / ctrl_n[idx].sum()
    lo, hi = np.percentile(stats, q)
    return float(lo), float(hi)


def within_session_placebo(
    sessions: list[np.ndarray],
    n: int = N_PLACEBO,
    seed: int = SEED,
) -> np.ndarray:
    """Sign-shuffle: permute trigger/control label WITHIN each session (S6).

    Returns n placebo statistics. Reported alongside the depth CI; not a §7 gate.
    """
    M, lens = _pad(sessions)
    rng = np.random.default_rng(seed)
    N = len(sessions)
    stats = np.empty(n)
    for r in range(n):
        j = (rng.random(N) * lens).astype(int)
        stats[r] = _stat_from_choice(M, lens, j)
    return stats


# --------------------------------------------------------------------------- §2.3 controls
def select_controls(
    trigger_tod_min: float,
    candidate_tod_mins: Sequence[float],
    *,
    min_sep_min: float = MIN_SEP_MIN,
    tod_tolerance_min: float = TOD_TOLERANCE_MIN,
    k: int = CONTROL_K,
    floor: int = CONTROL_MIN,
) -> tuple[int, ...] | None:
    """Deterministic §2.3 control selection on session-clock minutes.

    Candidates are already same-session. Eligibility: |tod − trigger| ≤ tolerance
    AND |tod − trigger| ≥ min_sep. Take the k closest in absolute ToD distance;
    ties broken by earliest session-clock time. Shortfall below ``floor`` → None.
    """
    eligible: list[tuple[float, float, int]] = []
    for i, tod in enumerate(candidate_tod_mins):
        dist = abs(float(tod) - float(trigger_tod_min))
        if dist < min_sep_min:
            continue
        if dist > tod_tolerance_min:
            continue
        # sort key: (abs distance, earliest clock time, stable index)
        eligible.append((dist, float(tod), i))
    eligible.sort(key=lambda t: (t[0], t[1], t[2]))
    chosen = [idx for _, _, idx in eligible[:k]]
    if len(chosen) < floor:
        return None
    return tuple(chosen)


# --------------------------------------------------------------------------- §7
def verdict(
    coverage: float,
    l1_diff: float,
    depth_diff: float,
    ci: tuple[float, float],
    *,
    ratio: float | None = None,
    sign_agree: bool | None = None,
) -> str:
    """PREREG §7 gate table, precedence exactly as frozen: W6 → W5 → W4 → W3 → W2/W1a/W1b."""
    if coverage < COV_MIN:
        return "VOID-COVERAGE"
    if abs(l1_diff) < EPS_RATIO:
        return "VOID-RATIO-UNDEFINED"

    if ratio is None or sign_agree is None:
        computed_ratio, computed_agree = agreement_stats(depth_diff, l1_diff)
        if ratio is None:
            ratio = computed_ratio
        if sign_agree is None:
            sign_agree = computed_agree

    if not sign_agree:
        return "FALSIFIED-DEPTH-DILUTES-OR-REVERSES"

    lo, hi = ci
    if lo <= 0.0 <= hi:
        return "AMBIGUOUS-UNDERPOWERED"

    # ratio is defined here (W5 already exited); assert for type checkers
    assert ratio is not None
    if 0.5 <= ratio <= 2.0:
        return "RESOLVED-CONSISTENT"
    if ratio > 2.0:
        return "RESOLVED-DEPTH-AMPLIFIED"
    return "RESOLVED-DEPTH-ATTENUATED"
