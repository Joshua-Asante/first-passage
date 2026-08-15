"""Q-TNEC-CON-3 Stage-0 — HTF-native 5m compression break (frozen PREREG_G0).

Harness only. Real-panel path PnL is gated by explore GO (see run_construct_g0.py).
Unit tests use synthetic fixtures — no vendor bars required.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

# ---- FROZEN (PREREG_G0) ------------------------------------------------------
HTF_MINUTES = 5
RT_PT = 1.41
K_NARROW = 2
NARROW_MULT = 1.0
MEDIAN_SESSIONS = 20
K_INTRINSIC = 1
DSR_FLOOR = 0.650
RANDOM_SEED = 20260810
PLACEBO_REPS = 1000
RTH_OPEN_MIN = 9 * 60 + 30
RTH_CLOSE_MIN = 16 * 60
FIRST_PER_SESSION = True

TNEC_LIMBS = ("N-ACT", "N-SURV", "N-EDGE", "N-SHAPE", "N-SIZE")

MNQ_PARQUET_REL = (
    "lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet"
)


@dataclass(frozen=True)
class CheapFalsifierResult:
    verdict: str
    detail: str
    long_mean_r: float
    short_mean_r: float


def cheap_falsifier_freeze_ok() -> CheapFalsifierResult:
    """Record-only: parent already ran panel falsifier (see ADMISSION_FALSIFIER_LOG)."""
    return CheapFalsifierResult(
        verdict="CHEAP_FALSIFIER_OK",
        detail=(
            "parent panel falsifier: coverage 91.6%; not both-arms CI<0 under "
            "HTF-native 5m / structural stop / first-per-session; see "
            "ADMISSION_FALSIFIER_LOG.md"
        ),
        long_mean_r=0.0625,
        short_mean_r=-0.0350,
    )


def format_tnec_verdict(
    limbs: dict[str, str] | None = None,
    *,
    bust: str = "U",
    p_pass: str = "U",
    mu_disclosed: str = "U",
) -> str:
    resolved = {k: "U" for k in TNEC_LIMBS}
    if limbs:
        for k, v in limbs.items():
            if k not in resolved:
                raise KeyError(f"unknown TNEC limb: {k}")
            resolved[k] = v
    limb_s = " ".join(resolved[k] for k in TNEC_LIMBS)
    return f"{limb_s} | {bust} | {p_pass} | {mu_disclosed}"


def g0_freeze_verdict_template() -> str:
    return format_tnec_verdict()


def r_from_pts(pts: float, stop_dist: float, rt_pt: float = RT_PT) -> float:
    return (pts - rt_pt) / stop_dist


def settle_side_at_t(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    t: int,
    med_rng: float,
    *,
    k_narrow: int = K_NARROW,
    narrow_mult: float = NARROW_MULT,
) -> tuple[int, float, float]:
    """After bar t closes: side, quiet_hi, quiet_lo. Bars ≤ t only."""
    if not (np.isfinite(med_rng) and med_rng > 0):
        return 0, float("nan"), float("nan")
    start = t - k_narrow
    end_comp = t - 1
    if start < 0 or t >= len(close):
        return 0, float("nan"), float("nan")
    for i in range(start, end_comp + 1):
        rng = high[i] - low[i]
        if rng <= 0 or rng > narrow_mult * med_rng:
            return 0, float("nan"), float("nan")
    quiet_hi = float(np.max(high[start : end_comp + 1]))
    quiet_lo = float(np.min(low[start : end_comp + 1]))
    if quiet_hi <= quiet_lo:
        return 0, float("nan"), float("nan")
    mid = 0.5 * (quiet_hi + quiet_lo)
    c_brk = float(close[t])
    up = c_brk > quiet_hi and c_brk > mid
    dn = c_brk < quiet_lo and c_brk < mid
    if up and not dn:
        return +1, quiet_hi, quiet_lo
    if dn and not up:
        return -1, quiet_hi, quiet_lo
    return 0, float("nan"), float("nan")


def path_pts_structural(
    entry: float,
    side: int,
    stop_level: float,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
) -> tuple[float, str, float]:
    stop_dist = abs(entry - stop_level)
    if stop_dist <= 0:
        return float("nan"), "invalid", float("nan")
    n = len(high)
    for j in range(start, n):
        if side > 0 and low[j] <= stop_level:
            return -stop_dist, "stop", stop_dist
        if side < 0 and high[j] >= stop_level:
            return -stop_dist, "stop", stop_dist
    pts = side * (float(close[n - 1]) - entry)
    return pts, "flat", stop_dist


def session_median_range(ranges_by_session: list[np.ndarray], sid: int) -> float:
    if sid < MEDIAN_SESSIONS:
        return float("nan")
    chunks = ranges_by_session[sid - MEDIAN_SESSIONS : sid]
    parts = [c[c > 0] for c in chunks if len(c)]
    if not parts:
        return float("nan")
    return float(np.median(np.concatenate(parts)))


def simulate_session_trades(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    med_rng: float,
) -> list[dict]:
    """First settle only → enter next open; structural stop; session-flat."""
    if not np.isfinite(med_rng) or len(open_) < K_NARROW + 2:
        return []
    n = len(open_)
    for t in range(K_NARROW, n - 1):
        side, q_hi, q_lo = settle_side_at_t(high, low, close, t, med_rng)
        if side == 0:
            continue
        entry_i = t + 1
        entry = float(open_[entry_i])
        stop_level = q_lo if side > 0 else q_hi
        pts, kind, stop_dist = path_pts_structural(
            entry, side, stop_level, high, low, close, entry_i
        )
        if not np.isfinite(pts) or not np.isfinite(stop_dist) or stop_dist <= 0:
            return []
        return [
            {
                "entry_i": entry_i,
                "side": side,
                "pts": pts,
                "kind": kind,
                "R": r_from_pts(pts, stop_dist),
                "stop_dist": stop_dist,
            }
        ]
    return []


def score_arm_rs(rs: Iterable[float]) -> dict:
    arr = np.asarray(list(rs), dtype=float)
    if len(arr) == 0:
        return {"n": 0, "mean_R": float("nan"), "wr": float("nan")}
    return {
        "n": int(len(arr)),
        "mean_R": float(arr.mean()),
        "wr": float((arr > 0).mean()),
    }


def explore_go_present(here) -> bool:
    from pathlib import Path

    return (Path(here) / "EXPLORE_GO.md").is_file()
