"""Q-TNEC-CON-5 Stage-0 — impulse→pullback→VWAP-reclaim (frozen PREREG_G0).

Harness only. Real-panel path PnL is gated by explore GO (see run_construct_g0.py).
Unit tests use synthetic fixtures — no vendor bars required.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

# ---- FROZEN (PREREG_G0) ------------------------------------------------------
RT_PT = 1.41
K_INTRINSIC = 1
DSR_FLOOR = 0.650
RANDOM_SEED = 20260811
PLACEBO_REPS = 1000
RTH_OPEN_MIN = 9 * 60 + 30
BIAS_END_MIN = 10 * 60
RTH_CLOSE_MIN = 16 * 60
BIAS_BARS = 30
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
            "parent panel falsifier: coverage 90.3%; not both-arms CI<0 under "
            "impulse-pullback-VWAP-reclaim / pullback-extreme stop / first-per-session; "
            "see ADMISSION_FALSIFIER_LOG.md"
        ),
        long_mean_r=0.0061,
        short_mean_r=-0.4268,
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


def session_vwap(high, low, close, volume) -> np.ndarray:
    tp = (high + low + close) / 3.0
    vol = np.maximum(volume.astype(float), 0.0)
    cum_pv = np.cumsum(tp * vol)
    cum_v = np.cumsum(vol)
    out = np.full_like(tp, np.nan, dtype=float)
    ok = cum_v > 0
    out[ok] = cum_pv[ok] / cum_v[ok]
    return out


def first_pullback_reclaim_trade(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    minute: np.ndarray,
) -> list[dict]:
    """First bias-side VWAP reclaim after pullback tag → next open; pullback stop."""
    n = len(close)
    if n < BIAS_BARS + 2:
        return []
    bias_mask = (minute >= RTH_OPEN_MIN) & (minute < BIAS_END_MIN)
    if int(bias_mask.sum()) < BIAS_BARS:
        return []
    bias_idx = np.flatnonzero(bias_mask)
    open_0930 = float(open_[bias_idx[0]])
    close_0959 = float(close[bias_idx[-1]])
    if close_0959 > open_0930:
        side = +1
    elif close_0959 < open_0930:
        side = -1
    else:
        return []

    vwap = session_vwap(high, low, close, volume)
    search_start = int(bias_idx[-1]) + 1
    if search_start >= n - 1:
        return []

    cleared = False
    tagged = False
    pull_ext = float("nan")

    for t in range(search_start, n - 1):
        vw = float(vwap[t])
        if not np.isfinite(vw):
            continue
        c = float(close[t])
        h = float(high[t])
        lo = float(low[t])

        if side > 0:
            if not cleared:
                if c > vw:
                    cleared = True
                continue
            if not tagged:
                if lo <= vw:
                    tagged = True
                    pull_ext = lo
                    if c > vw:
                        return _emit(open_, high, low, close, side, pull_ext, t)
                continue
            pull_ext = min(pull_ext, lo)
            if c > vw:
                return _emit(open_, high, low, close, side, pull_ext, t)
        else:
            if not cleared:
                if c < vw:
                    cleared = True
                continue
            if not tagged:
                if h >= vw:
                    tagged = True
                    pull_ext = h
                    if c < vw:
                        return _emit(open_, high, low, close, side, pull_ext, t)
                continue
            pull_ext = max(pull_ext, h)
            if c < vw:
                return _emit(open_, high, low, close, side, pull_ext, t)
    return []


def _emit(open_, high, low, close, side, stop_level, t) -> list[dict]:
    entry_i = t + 1
    entry = float(open_[entry_i])
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
