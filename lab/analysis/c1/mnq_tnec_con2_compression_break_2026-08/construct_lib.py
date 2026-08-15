"""Q-TNEC-CON-2 Stage-0 — compression→expansion break (frozen PREREG_G0).

Harness only. Real-panel path PnL is gated by explore GO (see run_construct_g0.py).
Unit tests use synthetic fixtures — no vendor bars required.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

# ---- FROZEN (PREREG_G0) ------------------------------------------------------
GATE_G = 10.0
RT_PT = 1.41
K_NARROW = 2
NARROW_MULT = 1.0
MEDIAN_SESSIONS = 20
K_INTRINSIC = 1
DSR_FLOOR = 0.650
RANDOM_SEED = 20260809
PLACEBO_REPS = 1000
RTH_OPEN_MIN = 9 * 60 + 30
RTH_CLOSE_MIN = 16 * 60

EM1_EDGE_R = 0.40
EM1_PRED_PT = GATE_G * EM1_EDGE_R + RT_PT
NEDGE_PRED_PT = RT_PT
EM1_WR_BAR = (1.0 + EM1_EDGE_R + RT_PT / GATE_G) / 2.0
NEDGE_WR_BAR = (1.0 + RT_PT / GATE_G) / 2.0

TNEC_LIMBS = ("N-ACT", "N-SURV", "N-EDGE", "N-SHAPE", "N-SIZE")

MNQ_DBN_DEFAULT = "ohlcv-1m_continuous_b1fa4ae6b7ba9af2.dbn"
MNQ_PARQUET_REL = (
    "lab/analysis/c1/mnq_selection_ceiling_allbars_2026-08/_mnq_1m.parquet"
)


@dataclass(frozen=True)
class CheapFalsifierResult:
    em1_pred_pt: float
    nedge_pred_pt: float
    em1_wr_bar: float
    nedge_wr_bar: float
    verdict: str
    detail: str


def arithmetic_bars() -> dict[str, float]:
    return {
        "em1_pred_pt": EM1_PRED_PT,
        "nedge_pred_pt": NEDGE_PRED_PT,
        "em1_wr_bar": EM1_WR_BAR,
        "nedge_wr_bar": NEDGE_WR_BAR,
        "gate_g": GATE_G,
        "rt_pt": RT_PT,
    }


def cheap_falsifier_freeze_ok() -> CheapFalsifierResult:
    """Record-only: parent already ran panel falsifier (see ADMISSION_FALSIFIER_LOG)."""
    bars = arithmetic_bars()
    return CheapFalsifierResult(
        em1_pred_pt=bars["em1_pred_pt"],
        nedge_pred_pt=bars["nedge_pred_pt"],
        em1_wr_bar=bars["em1_wr_bar"],
        nedge_wr_bar=bars["nedge_wr_bar"],
        verdict="CHEAP_FALSIFIER_OK",
        detail=(
            "parent panel falsifier: both-arm CI straddles 0 under generous "
            "K_NARROW=2 / NARROW_MULT=1.0; see ADMISSION_FALSIFIER_LOG.md"
        ),
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


def r_from_pts(pts: float, stop_pt: float = GATE_G, rt_pt: float = RT_PT) -> float:
    return (pts - rt_pt) / stop_pt


def path_pts_session_flat(
    entry: float,
    side: int,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
    stop_pt: float = GATE_G,
) -> tuple[float, str]:
    n = len(high)
    stop_level = entry - side * stop_pt
    for j in range(start, n):
        if side > 0:
            hit_stop = low[j] <= stop_level
        else:
            hit_stop = high[j] >= stop_level
        if hit_stop:
            return -stop_pt, "stop"
    return side * (close[n - 1] - entry), "flat"


def session_median_range(ranges_by_session: list[np.ndarray], sid: int) -> float:
    if sid < MEDIAN_SESSIONS:
        return float("nan")
    chunks = ranges_by_session[sid - MEDIAN_SESSIONS : sid]
    parts = [c[c > 0] for c in chunks if len(c)]
    if not parts:
        return float("nan")
    return float(np.median(np.concatenate(parts)))


def break_side_at_t(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    t: int,
    med_rng: float,
    *,
    k_narrow: int = K_NARROW,
    narrow_mult: float = NARROW_MULT,
) -> int:
    """Causal signal at open of bar t (bars ≤ t-1 only). +1 long / -1 short / 0."""
    if not (np.isfinite(med_rng) and med_rng > 0):
        return 0
    start = t - 1 - k_narrow
    end_comp = t - 2
    brk = t - 1
    if start < 0 or brk < 0 or brk >= len(close):
        return 0
    for i in range(start, end_comp + 1):
        rng = high[i] - low[i]
        if rng <= 0 or rng > narrow_mult * med_rng:
            return 0
    quiet_hi = float(np.max(high[start : end_comp + 1]))
    quiet_lo = float(np.min(low[start : end_comp + 1]))
    if quiet_hi <= quiet_lo:
        return 0
    c_brk = float(close[brk])
    up = c_brk > quiet_hi
    dn = c_brk < quiet_lo
    if up and not dn:
        return +1
    if dn and not up:
        return -1
    return 0


def _exit_bar(
    entry: float,
    side: int,
    high: np.ndarray,
    low: np.ndarray,
    start: int,
    stop_pt: float,
) -> int:
    n = len(high)
    stop_level = entry - side * stop_pt
    for j in range(start, n):
        if side > 0 and low[j] <= stop_level:
            return j
        if side < 0 and high[j] >= stop_level:
            return j
    return n - 1


def simulate_session_trades(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    med_rng: float,
    stop_pt: float = GATE_G,
) -> list[dict]:
    trades: list[dict] = []
    pos_end = -1
    n = len(open_)
    for t in range(K_NARROW + 1, n):
        if t <= pos_end:
            continue
        side = break_side_at_t(high, low, close, t, med_rng)
        if side == 0:
            continue
        pts, kind = path_pts_session_flat(
            float(open_[t]), side, high, low, close, t, stop_pt=stop_pt
        )
        exit_bar = _exit_bar(float(open_[t]), side, high, low, t, stop_pt)
        trades.append(
            {
                "entry_i": t,
                "side": side,
                "pts": pts,
                "kind": kind,
                "R": r_from_pts(pts, stop_pt),
                "exit_i": exit_bar,
            }
        )
        pos_end = exit_bar
    return trades


def score_arm_rs(rs: Iterable[float]) -> dict:
    arr = np.asarray(list(rs), dtype=float)
    if len(arr) == 0:
        return {"n": 0, "mean_R": float("nan"), "wr": float("nan")}
    return {
        "n": int(len(arr)),
        "mean_R": float(arr.mean()),
        "wr": float((arr > 0).mean()),
    }


def g0_freeze_verdict_template() -> str:
    return format_tnec_verdict()


def explore_go_present(here) -> bool:
    from pathlib import Path

    return (Path(here) / "EXPLORE_GO.md").is_file()
