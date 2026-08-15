"""MSL-C2 Stage G0 — London-range failed-extension fade (MGC).

Harness only. Real-panel path PnL is gated by explore GO (see run_construct_g0.py).
Unit tests use synthetic fixtures — no vendor bars required.

Frozen geometry: lab/archive/msl_c2_mgc_2026-08/PREREG_G0.md
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np

# ---- FROZEN (PREREG_G0) ------------------------------------------------------
K_INTRINSIC = 1
DSR_FLOOR = 0.650
RANDOM_SEED = 20260812
PLACEBO_REPS = 1000
N_BOOT = 10_000

TICK = 0.10  # MGC mintick
POINT_VALUE = 10.0  # USD per 1.0 price point
RT_USD = 4.12
FOUR_X_RT_USD = 16.48
STOP_BUFFER_TICKS = 1  # frozen center; {0,1,2} are robustness probes only

# Session windows in America/New_York minute-of-day (inclusive)
LONDON_OPEN_MIN = 3 * 60  # 03:00
LONDON_CLOSE_MIN = 8 * 60 + 19  # 08:19
PROBE_OPEN_MIN = 8 * 60 + 20  # 08:20
PROBE_CLOSE_MIN = 15 * 60 + 59  # 15:59
FLAT_MIN = 16 * 60  # 16:00 ET flat

IS_END = np.datetime64("2025-08-31")  # IS = session date < 2025-09-01
CONFIRM_START = np.datetime64("2025-09-01")
CONFIRM_END = np.datetime64("2026-08-12")

MGC_PANEL_REL = "core/data/bar_data/MGC_M15.csv"
MGC_SHA256 = "88da9f1597daca5c6a118fa4539a117aba5ea4255d81e7475fd7029987caf3f3"

TNEC_LIMBS = ("N-ACT", "N-SURV", "N-EDGE", "N-SHAPE", "N-SIZE")


@dataclass(frozen=True)
class CheapFalsifierResult:
    verdict: str
    detail: str
    rt_usd: float
    four_x_rt_usd: float


def cheap_falsifier_freeze_ok() -> CheapFalsifierResult:
    """Record-only: Stage-1 already PASSed cost-law / adjacency / delete unpaid."""
    return CheapFalsifierResult(
        verdict="CHEAP_FALSIFIER_OK",
        detail=(
            "STAGE1 PASS: cost-law $160 ≫ $16.48; adjacency not R8/Guardian-transfer; "
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


def r_from_pts(pts: float, stop_dist_pts: float, *, rt_usd: float = RT_USD) -> float:
    """Net R: (pnl_usd − RT) / stop_usd with qty=1."""
    if not (np.isfinite(stop_dist_pts) and stop_dist_pts > 0):
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
    if stop_dist <= 0 or not np.isfinite(stop_dist):
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


def _levels_valid(hi: float, lo: float) -> bool:
    return np.isfinite(hi) and np.isfinite(lo) and hi > lo


def find_failed_extension_signal(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
    ref_hi: float,
    ref_lo: float,
) -> dict | None:
    """First probe-window failed-extension reclaim → entry at next open.

    Returns dict with entry_i, fade_side (+1 long / -1 short), sweep_extreme,
    reclaim_i — or None.
    """
    if not _levels_valid(ref_hi, ref_lo):
        return None
    n = len(close)
    probe = (minutes >= PROBE_OPEN_MIN) & (minutes <= PROBE_CLOSE_MIN)
    swept_up = False
    swept_dn = False
    sweep_hi = float("-inf")
    sweep_lo = float("inf")
    for t in range(n):
        if not probe[t]:
            continue
        h = float(high[t])
        lo_ = float(low[t])
        c = float(close[t])
        if h > ref_hi:
            swept_up = True
            sweep_hi = max(sweep_hi, h)
        if lo_ < ref_lo:
            swept_dn = True
            sweep_lo = min(sweep_lo, lo_)
        # Failed upside → SHORT reclaim
        if swept_up and c < ref_hi:
            entry_i = t + 1
            if entry_i >= n:
                return None
            if not probe[entry_i] and minutes[entry_i] >= FLAT_MIN:
                return None
            return {
                "entry_i": entry_i,
                "reclaim_i": t,
                "fade_side": -1,
                "sweep_extreme": sweep_hi,
                "ref_hi": ref_hi,
                "ref_lo": ref_lo,
            }
        # Failed downside → LONG reclaim
        if swept_dn and c > ref_lo:
            entry_i = t + 1
            if entry_i >= n:
                return None
            if not probe[entry_i] and minutes[entry_i] >= FLAT_MIN:
                return None
            return {
                "entry_i": entry_i,
                "reclaim_i": t,
                "fade_side": +1,
                "sweep_extreme": sweep_lo,
                "ref_hi": ref_hi,
                "ref_lo": ref_lo,
            }
    return None


def _stop_target_for_fade(
    entry: float,
    fade_side: int,
    ref_hi: float,
    ref_lo: float,
    sweep_extreme: float,
    *,
    buffer_ticks: int = STOP_BUFFER_TICKS,
) -> tuple[float, float, float]:
    buf = buffer_ticks * TICK
    if fade_side < 0:  # short
        stop_level = max(ref_hi, sweep_extreme) + buf
        stop_dist = stop_level - entry
        target_level = entry - stop_dist
    else:  # long
        stop_level = min(ref_lo, sweep_extreme) - buf
        stop_dist = entry - stop_level
        target_level = entry + stop_dist
    return stop_level, target_level, stop_dist


def build_trade_from_signal(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    signal: dict,
    *,
    mode: str = "fade",
) -> dict | None:
    """mode: 'fade' | 'flip'. Same reclaim; flip = opposite side, same stop_dist."""
    entry_i = int(signal["entry_i"])
    entry = float(open_[entry_i])
    fade_side = int(signal["fade_side"])
    stop_level, target_level, stop_dist = _stop_target_for_fade(
        entry,
        fade_side,
        float(signal["ref_hi"]),
        float(signal["ref_lo"]),
        float(signal["sweep_extreme"]),
    )
    if not (np.isfinite(stop_dist) and stop_dist > 0):
        return None
    if mode == "fade":
        side = fade_side
        sl, tl = stop_level, target_level
    elif mode == "flip":
        side = -fade_side
        # Preserve stop_dist magnitude; mirror levels about entry
        if side > 0:
            sl = entry - stop_dist
            tl = entry + stop_dist
        else:
            sl = entry + stop_dist
            tl = entry - stop_dist
    else:
        raise ValueError(f"unknown mode: {mode}")
    pts, kind, sd = path_pts_stop_target_flat(
        entry, side, sl, tl, high, low, close, entry_i
    )
    if not np.isfinite(pts) or not np.isfinite(sd) or sd <= 0:
        return None
    return {
        "entry_i": entry_i,
        "side": side,
        "mode": mode,
        "pts": pts,
        "kind": kind,
        "stop_dist": sd,
        "R": r_from_pts(pts, sd),
        "fade_side": fade_side,
    }


def london_hl(high: np.ndarray, low: np.ndarray, minutes: np.ndarray) -> tuple[float, float]:
    mask = (minutes >= LONDON_OPEN_MIN) & (minutes <= LONDON_CLOSE_MIN)
    if not np.any(mask):
        return float("nan"), float("nan")
    return float(np.max(high[mask])), float(np.min(low[mask]))


def rth_hl(high: np.ndarray, low: np.ndarray, minutes: np.ndarray) -> tuple[float, float]:
    """Probe-window H/L — used as DELETE sham reference (prior day RTH)."""
    mask = (minutes >= PROBE_OPEN_MIN) & (minutes <= PROBE_CLOSE_MIN)
    if not np.any(mask):
        return float("nan"), float("nan")
    return float(np.max(high[mask])), float(np.min(low[mask]))


def simulate_session(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
    *,
    ref_hi: float,
    ref_lo: float,
    mode: str = "fade",
) -> list[dict]:
    """k=1: at most one trade per session."""
    sig = find_failed_extension_signal(
        open_, high, low, close, minutes, ref_hi, ref_lo
    )
    if sig is None:
        return []
    trade = build_trade_from_signal(
        open_, high, low, close, sig, mode=mode
    )
    return [trade] if trade is not None else []


def simulate_constrained(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
) -> list[dict]:
    hi, lo = london_hl(high, low, minutes)
    return simulate_session(
        open_, high, low, close, minutes, ref_hi=hi, ref_lo=lo, mode="fade"
    )


def simulate_delete_sham(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
    prior_rth_hi: float,
    prior_rth_lo: float,
) -> list[dict]:
    """DELETE: London replaced by prior Globex-day RTH H/L."""
    return simulate_session(
        open_,
        high,
        low,
        close,
        minutes,
        ref_hi=prior_rth_hi,
        ref_lo=prior_rth_lo,
        mode="fade",
    )


def simulate_flip_join(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    minutes: np.ndarray,
) -> list[dict]:
    hi, lo = london_hl(high, low, minutes)
    return simulate_session(
        open_, high, low, close, minutes, ref_hi=hi, ref_lo=lo, mode="flip"
    )


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
    """Older/newer IS halves by session-date median split."""
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
    """PASS iff constrained mean net R > sham (strict). NaN ⇒ not PASS."""
    if not (np.isfinite(constrained_mean) and np.isfinite(sham_mean)):
        return False
    return constrained_mean > sham_mean


def flip_pass(fade_mean: float, flip_mean: float) -> bool:
    """PASS iff fade mean net R > flip (strict). NaN ⇒ not PASS."""
    if not (np.isfinite(fade_mean) and np.isfinite(flip_mean)):
        return False
    return fade_mean > flip_mean
