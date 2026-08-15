"""MSL-S2A Stage G0 — pullback-failure resumption (MCL).

Harness only. Real-panel path PnL is gated by explore GO (see run_construct_g0.py).
Unit tests use synthetic fixtures — no vendor bars required.

Frozen geometry: lab/analysis/c1/msl_s2a_mcl_2026-08/PREREG_G0.md
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

# ---- FROZEN (PREREG_G0) ------------------------------------------------------
K_INTRINSIC = 1
DSR_FLOOR = 0.650
RANDOM_SEED = 20260813
PLACEBO_REPS = 1000
N_BOOT = 10_000

TICK = 0.01  # MCL mintick
MIN_STOP_DIST = TICK  # skip sub-tick geometry (DELETE sham blow-up guard)
POINT_VALUE = 100.0  # USD per 1.00 price point ($1.00 / 0.01 tick)
RT_USD = 4.12
FOUR_X_RT_USD = 16.48
STOP_BUFFER_TICKS = 1  # frozen center; {0,1,2} are robustness probes only
RR = 3.0
IMPULSE_BARS = 4
PULLBACK_BARS = 3
LOOKBACK = IMPULSE_BARS + PULLBACK_BARS  # 7

SESSION_OPEN_MIN = 9 * 60  # 09:00 ET
FLAT_MIN = 14 * 60 + 30  # 14:30 ET
TRIGGER_OPEN_MIN = 10 * 60 + 45  # 10:45
TRIGGER_OPEN_MAX = 14 * 60  # 14:00 inclusive
LAST_ENTRY_OPEN_MIN = 14 * 60 + 15  # 14:15 open → flatten at 14:30

IS_END = np.datetime64("2025-06-30")  # IS = session date < 2025-07-01
CONFIRM_START = np.datetime64("2025-07-01")
CONFIRM_END = np.datetime64("2026-07-02")

MCL_PANEL_REL = "core/data/bar_data/MCL_M15.csv"
MCL_SHA256 = "5aa504567b943ff68506b8b5c21df293c5a553543fdf1ac606adeb0f5bfbbd23"

TNEC_LIMBS = ("N-ACT", "N-SURV", "N-EDGE", "N-SHAPE", "N-SIZE")
EXPLORE_QTY = 2  # design-point disclose only; R is per-contract

FOMC_DATES = frozenset(
    """
    2022-01-26 2022-03-16 2022-05-04 2022-06-15 2022-07-27 2022-09-21 2022-11-02 2022-12-14
    2023-02-01 2023-03-22 2023-05-03 2023-06-14 2023-07-26 2023-09-20 2023-11-01 2023-12-13
    2024-01-31 2024-03-20 2024-05-01 2024-06-12 2024-07-31 2024-09-18 2024-11-07 2024-12-18
    2025-01-29 2025-03-19 2025-05-07 2025-06-18 2025-07-30 2025-09-17 2025-11-05 2025-12-10
    2026-01-28 2026-03-18 2026-05-06 2026-06-17
    """.split()
)

ROLL_EXCLUDED = frozenset(
    """
    2022-01-18 2022-01-19 2022-01-20 2022-02-17 2022-02-18 2022-02-22
    2022-03-18 2022-03-21 2022-03-22 2022-04-18 2022-04-19 2022-04-20
    2022-05-18 2022-05-19 2022-05-20 2022-06-16 2022-06-17 2022-06-21
    2022-07-18 2022-07-19 2022-07-20 2022-08-18 2022-08-19 2022-08-22
    2022-09-16 2022-09-19 2022-09-20 2022-10-18 2022-10-19 2022-10-20
    2022-11-17 2022-11-18 2022-11-21 2022-12-16 2022-12-19 2022-12-20
    2023-01-18 2023-01-19 2023-01-20 2023-02-16 2023-02-17 2023-02-21
    2023-03-17 2023-03-20 2023-03-21 2023-04-18 2023-04-19 2023-04-20
    2023-05-18 2023-05-19 2023-05-22 2023-06-15 2023-06-16 2023-06-20
    2023-07-18 2023-07-19 2023-07-20 2023-08-18 2023-08-21 2023-08-22
    2023-09-18 2023-09-19 2023-09-20 2023-10-18 2023-10-19 2023-10-20
    2023-11-16 2023-11-17 2023-11-20 2023-12-15 2023-12-18 2023-12-19
    2024-01-18 2024-01-19 2024-01-22 2024-02-15 2024-02-16 2024-02-20
    2024-03-18 2024-03-19 2024-03-20 2024-04-18 2024-04-19 2024-04-22
    2024-05-17 2024-05-20 2024-05-21 2024-06-17 2024-06-18 2024-06-20
    2024-07-18 2024-07-19 2024-07-22 2024-08-16 2024-08-19 2024-08-20
    2024-09-18 2024-09-19 2024-09-20 2024-10-18 2024-10-21 2024-10-22
    2024-11-18 2024-11-19 2024-11-20 2024-12-17 2024-12-18 2024-12-19
    2025-01-16 2025-01-17 2025-01-21 2025-02-18 2025-02-19 2025-02-20
    2025-03-18 2025-03-19 2025-03-20 2025-04-17 2025-04-21 2025-04-22
    2025-05-16 2025-05-19 2025-05-20 2025-06-17 2025-06-18 2025-06-20
    2025-07-18 2025-07-21 2025-07-22 2025-08-18 2025-08-19 2025-08-20
    2025-09-18 2025-09-19 2025-09-22 2025-10-17 2025-10-20 2025-10-21
    2025-11-18 2025-11-19 2025-11-20 2025-12-17 2025-12-18 2025-12-19
    2026-01-15 2026-01-16 2026-01-20 2026-02-18 2026-02-19 2026-02-20
    2026-03-18 2026-03-19 2026-03-20 2026-04-17 2026-04-20 2026-04-21
    2026-05-15 2026-05-18 2026-05-19 2026-06-17 2026-06-18 2026-06-22
    """.split()
)


@dataclass(frozen=True)
class CheapFalsifierResult:
    verdict: str
    detail: str
    rt_usd: float
    four_x_rt_usd: float


def cheap_falsifier_freeze_ok() -> CheapFalsifierResult:
    return CheapFalsifierResult(
        verdict="CHEAP_FALSIFIER_OK",
        detail=(
            "STAGE1 PASS: cost-law $180 ≫ $16.48; adjacency not TAS/CONFIG-B/CON-5/slate-1; "
            "delete/flip declared unpaid until explore GO — see STAGE1.md / PREREG_G0.md"
        ),
        rt_usd=RT_USD,
        four_x_rt_usd=FOUR_X_RT_USD,
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


def explore_go_present(here) -> bool:
    return (Path(here) / "EXPLORE_GO.md").is_file()


def session_excluded(session_date) -> bool:
    key = str(session_date)
    return key in FOMC_DATES or key in ROLL_EXCLUDED


def r_from_pts(pts: float, stop_dist_pts: float, *, rt_usd: float = RT_USD) -> float:
    """Net R: (pnl_usd − RT) / stop_usd with qty=1. pts in price units."""
    if not (np.isfinite(stop_dist_pts) and stop_dist_pts >= MIN_STOP_DIST - 1e-12):
        return float("nan")
    pnl_usd = pts * POINT_VALUE
    stop_usd = stop_dist_pts * POINT_VALUE
    return (pnl_usd - rt_usd) / stop_usd


def path_pts_stop_target_flat(
    entry: float,
    side: int,
    stop_level: float,
    target_level: float,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    start: int,
) -> tuple[float, str, float]:
    """Stop-first same-bar; then target; else flat at last bar (session end)."""
    stop_dist = abs(entry - stop_level)
    if not (np.isfinite(stop_dist) and stop_dist >= MIN_STOP_DIST - 1e-12):
        return float("nan"), "invalid", float("nan")
    n = len(high)
    for j in range(start, n):
        if side > 0:
            hit_stop = float(low[j]) <= stop_level
            hit_tgt = float(high[j]) >= target_level
        else:
            hit_stop = float(high[j]) >= stop_level
            hit_tgt = float(low[j]) <= target_level
        if hit_stop:
            return -stop_dist, "stop", stop_dist
        if hit_tgt:
            return +stop_dist, "target", stop_dist
    pts = side * (float(close[n - 1]) - entry)
    return pts, "flat", stop_dist


def _impulse_pullback_slices(t: int) -> tuple[slice, slice]:
    i_sl = slice(t - LOOKBACK, t - PULLBACK_BARS)
    p_sl = slice(t - PULLBACK_BARS, t)
    return i_sl, p_sl


def _long_ok(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    t: int,
) -> bool:
    i_sl, p_sl = _impulse_pullback_slices(t)
    if not (float(close[t - PULLBACK_BARS - 1]) > float(open_[t - LOOKBACK])):
        return False
    if not (float(np.max(high[i_sl])) > float(np.max(high[p_sl]))):
        return False
    if not (float(np.min(low[p_sl])) < float(np.min(low[i_sl]))):
        return False
    if not (float(close[t]) > float(np.max(high[p_sl]))):
        return False
    return float(low[t]) >= float(np.min(low[p_sl]))


def _short_ok(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    t: int,
) -> bool:
    i_sl, p_sl = _impulse_pullback_slices(t)
    if not (float(close[t - PULLBACK_BARS - 1]) < float(open_[t - LOOKBACK])):
        return False
    if not (float(np.min(low[i_sl])) < float(np.min(low[p_sl]))):
        return False
    if not (float(np.max(high[p_sl])) > float(np.max(high[i_sl]))):
        return False
    if not (float(close[t]) < float(np.min(low[p_sl]))):
        return False
    return float(high[t]) <= float(np.max(high[p_sl]))


def _trigger_ok(minutes: np.ndarray, t: int) -> bool:
    if t < LOOKBACK:
        return False
    m = int(minutes[t])
    if m < TRIGGER_OPEN_MIN or m > TRIGGER_OPEN_MAX:
        return False
    entry_i = t + 1
    if entry_i >= len(minutes):
        return False
    return int(minutes[entry_i]) <= LAST_ENTRY_OPEN_MIN


def find_resumption_signal(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
) -> dict | None:
    """First valid pullback-failure resumption in session, or None.

    Both arms on the same trigger bar → skip the session (PREREG k=1 conflict).
    """
    n = len(close)
    for t in range(LOOKBACK, n):
        if not _trigger_ok(minutes, t):
            continue
        long_ok = _long_ok(open_, high, low, close, t)
        short_ok = _short_ok(open_, high, low, close, t)
        if long_ok and short_ok:
            return None
        if long_ok:
            return {"t": t, "entry_i": t + 1, "side": +1}
        if short_ok:
            return {"t": t, "entry_i": t + 1, "side": -1}
    return None


def _stop_target(entry: float, side: int, p_extreme: float) -> tuple[float, float, float]:
    buf = STOP_BUFFER_TICKS * TICK
    if side > 0:
        stop_level = p_extreme - buf
        stop_dist = entry - stop_level
        target_level = entry + RR * stop_dist
    else:
        stop_level = p_extreme + buf
        stop_dist = stop_level - entry
        target_level = entry - RR * stop_dist
    if not (np.isfinite(stop_dist) and stop_dist >= MIN_STOP_DIST - 1e-12):
        return float("nan"), float("nan"), float("nan")
    return stop_level, target_level, stop_dist


def build_trade_from_signal(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    signal: dict,
    *,
    mode: str = "resume",
) -> dict | None:
    """mode: 'resume' | 'flip'. Flip joins the pullback (opposite side, same stop_dist)."""
    t = int(signal["t"])
    entry_i = int(signal["entry_i"])
    entry = float(open_[entry_i])
    resume_side = int(signal["side"])
    _, p_sl = _impulse_pullback_slices(t)
    if resume_side > 0:
        p_extreme = float(np.min(low[p_sl]))
    else:
        p_extreme = float(np.max(high[p_sl]))
    stop_level, target_level, stop_dist = _stop_target(entry, resume_side, p_extreme)
    if not (np.isfinite(stop_dist) and stop_dist > 0):
        return None
    if mode == "resume":
        side = resume_side
        sl, tl = stop_level, target_level
    elif mode == "flip":
        side = -resume_side
        if side > 0:
            sl = entry - stop_dist
            tl = entry + RR * stop_dist
        else:
            sl = entry + stop_dist
            tl = entry - RR * stop_dist
    else:
        raise ValueError(f"unknown mode: {mode}")
    pts, kind, sd = path_pts_stop_target_flat(
        entry, side, sl, tl, high, low, close, entry_i
    )
    if not np.isfinite(pts) or not np.isfinite(sd) or sd <= 0:
        return None
    return {
        "t": t,
        "entry_i": entry_i,
        "minute": None,
        "side": side,
        "mode": mode,
        "pts": pts,
        "kind": kind,
        "stop_dist": sd,
        "R": r_from_pts(pts, sd),
        "resume_side": resume_side,
    }


def simulate_constrained(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
) -> list[dict]:
    sig = find_resumption_signal(open_, high, low, close, minutes)
    if sig is None:
        return []
    trade = build_trade_from_signal(open_, high, low, close, sig, mode="resume")
    if trade is None:
        return []
    trade["minute"] = int(minutes[int(sig["t"])])
    return [trade]


def simulate_flip_join(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
) -> list[dict]:
    sig = find_resumption_signal(open_, high, low, close, minutes)
    if sig is None:
        return []
    trade = build_trade_from_signal(open_, high, low, close, sig, mode="flip")
    if trade is None:
        return []
    trade["minute"] = int(minutes[int(sig["t"])])
    return [trade]


def unfiltered_trade_at(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
    t: int,
    side: int,
) -> dict | None:
    """DELETE sham: P-window stop at t, no impulse/failure filter."""
    if not _trigger_ok(minutes, t):
        return None
    if side not in (+1, -1):
        return None
    entry_i = t + 1
    entry = float(open_[entry_i])
    _, p_sl = _impulse_pullback_slices(t)
    p_extreme = float(np.min(low[p_sl])) if side > 0 else float(np.max(high[p_sl]))
    stop_level, target_level, stop_dist = _stop_target(entry, side, p_extreme)
    if not (np.isfinite(stop_dist) and stop_dist > 0):
        return None
    pts, kind, sd = path_pts_stop_target_flat(
        entry, side, stop_level, target_level, high, low, close, entry_i
    )
    if not np.isfinite(pts) or not np.isfinite(sd) or sd <= 0:
        return None
    return {
        "t": t,
        "entry_i": entry_i,
        "minute": int(minutes[t]),
        "side": side,
        "mode": "delete_sham",
        "pts": pts,
        "kind": kind,
        "stop_dist": sd,
        "R": r_from_pts(pts, sd),
        "resume_side": side,
    }


def eligible_trigger_indices(minutes: np.ndarray) -> list[int]:
    return [t for t in range(LOOKBACK, len(minutes)) if _trigger_ok(minutes, t)]


def score_arm_rs(rs: Iterable[float]) -> dict:
    arr = np.asarray(list(rs), dtype=float)
    if len(arr) == 0:
        return {"n": 0, "mean_R": float("nan"), "wr": float("nan")}
    return {
        "n": int(len(arr)),
        "mean_R": float(arr.mean()),
        "wr": float((arr > 0).mean()),
    }


def session_block_ci(
    blocks: Sequence[np.ndarray],
    n_boot: int = N_BOOT,
    seed: int = RANDOM_SEED,
) -> tuple[float, float]:
    kept = [a for a in blocks if len(a)]
    if len(kept) < 2:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    idx = np.arange(len(kept))
    boots = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        pick = rng.choice(idx, size=len(kept), replace=True)
        boots[i] = float(np.concatenate([kept[j] for j in pick]).mean())
    return float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975))


def halves_means(session_dates: Sequence, rs_by_session: Sequence[np.ndarray]) -> dict:
    if not session_dates:
        return {"older": float("nan"), "newer": float("nan")}
    dates = list(session_dates)
    mid = sorted(dates)[len(dates) // 2]
    older, newer = [], []
    for d, r in zip(dates, rs_by_session):
        if len(r) == 0:
            continue
        (older if d < mid else newer).extend(r.tolist())
    return {
        "older": float(np.mean(older)) if older else float("nan"),
        "newer": float(np.mean(newer)) if newer else float("nan"),
    }


def delete_pass(constrained_mean: float, sham_mean: float) -> bool:
    if not (np.isfinite(constrained_mean) and np.isfinite(sham_mean)):
        return False
    return constrained_mean > sham_mean


def flip_pass(resume_mean: float, flip_mean: float) -> bool:
    if not (np.isfinite(resume_mean) and np.isfinite(flip_mean)):
        return False
    return resume_mean > flip_mean
