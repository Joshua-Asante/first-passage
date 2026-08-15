"""Q-TNEC-CON-4 Stage-0 — PDH/PDL RTH with-break (frozen PREREG_G0).

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
            "parent panel falsifier: coverage 88.0%; not both-arms CI<0 under "
            "PDH/PDL with-break / structural opposite-extreme stop / first-per-session; "
            "see ADMISSION_FALSIFIER_LOG.md"
        ),
        long_mean_r=-0.0048,
        short_mean_r=-0.0028,
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


def first_pdh_pdl_trade(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    pdh: float,
    pdl: float,
) -> list[dict]:
    """First close beyond PDH/PDL → enter next open; stop at opposite extreme."""
    if not (np.isfinite(pdh) and np.isfinite(pdl) and pdh > pdl):
        return []
    n = len(close)
    for t in range(n - 1):
        c = float(close[t])
        if c > pdh:
            side, stop_level = +1, pdl
        elif c < pdl:
            side, stop_level = -1, pdh
        else:
            continue
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
