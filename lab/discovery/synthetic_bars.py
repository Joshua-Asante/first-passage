"""Synthetic GC-like 1h bars with an injectable known motif edge.

Offline only — no Databento. Random-walk + intraday vol U-shape; optional
planted motif that is followed by a signed forward move of controllable
per-trade Sharpe and occurrence count (for Stage-2/4 e2e promote/reject proofs).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

# Globex gold maintenance-ish hour excluded from the 1h grid (UTC).
MAINTENANCE_HOUR_UTC = 21
SESSION_HOURS_UTC = tuple(h for h in range(0, 24) if h != MAINTENANCE_HOUR_UTC)


@dataclass(frozen=True)
class MotifSpec:
    """Planted motif: shape (length m) + forward horizon + per-trade edge params."""

    shape: np.ndarray
    horizon: int
    direction: int  # +1 / -1
    per_trade_sr: float
    trade_vol: float
    period: int  # bars between plant attempts
    max_oos_trades: int | None = None  # None = fill all period slots


@dataclass(frozen=True)
class SyntheticBars:
    bars: pd.DataFrame  # index=UTC timestamps; columns open/high/low/close/ret
    is_mask: np.ndarray
    oos_mask: np.ndarray
    motif: MotifSpec | None
    plant_indices: np.ndarray  # bar indices where motif starts


def _hour_grid(start: str, end: str) -> pd.DatetimeIndex:
    """Weekday 1h UTC grid excluding the maintenance hour."""
    full = pd.date_range(start, end, freq="h", tz="UTC")
    mask = (full.dayofweek < 5) & np.isin(full.hour, SESSION_HOURS_UTC)
    return full[mask]


def _u_shape_vol(hours: np.ndarray, base: float = 0.001) -> np.ndarray:
    """Intraday vol U-shape (higher at session edges)."""
    # Map hour to [0,1] distance from midday.
    x = np.abs(hours.astype(float) - 12.0) / 12.0
    return base * (0.7 + 0.9 * x)


def generate_synthetic_bars(
    *,
    seed: int = 0,
    is_start: str = "2010-01-01",
    is_end: str = "2018-12-31",
    oos_start: str = "2019-05-06",
    oos_end: str = "2026-07-01",
    start_price: float = 1200.0,
    motif: MotifSpec | None = None,
    plant_in_oos_only: bool = False,
) -> SyntheticBars:
    """Build a driftless GC-like 1h series; optionally plant a motif edge."""
    rng = np.random.default_rng(seed)
    idx_is = _hour_grid(is_start, is_end)
    idx_oos = _hour_grid(oos_start, oos_end)
    idx = idx_is.append(idx_oos)
    n = len(idx)
    hours = idx.hour.to_numpy()
    vol = _u_shape_vol(hours)
    noise = rng.normal(0.0, 1.0, size=n) * vol
    # Vol-normalize hygiene target: returns already U-shaped; price via cumsum.
    close = start_price * np.exp(np.cumsum(noise))
    plant_indices: list[int] = []

    if motif is not None:
        shape = np.asarray(motif.shape, dtype=float)
        m = shape.size
        h = int(motif.horizon)
        edge_mean = motif.per_trade_sr * motif.trade_vol * float(motif.direction)
        is_n = len(idx_is)
        regions = []
        if not plant_in_oos_only:
            regions.append(("is", 0, is_n))
        regions.append(("oos", is_n, n))
        for region_name, lo, hi in regions:
            count = 0
            limit = motif.max_oos_trades if region_name == "oos" else None
            t = lo + m
            while t + h < hi:
                if (t - lo) % motif.period == 0:
                    if limit is not None and count >= limit:
                        break
                    # Overwrite the trailing m-bar return path to match z-shape
                    # in price space (level-free): apply shape as return increments.
                    seg = shape * motif.trade_vol
                    # Place shape on returns ending at t-1; impulse after t-1.
                    start = t - m
                    if start < lo:
                        t += motif.period
                        continue
                    noise[start:t] = seg
                    # Forward edge realized over horizon as equal increments.
                    noise[t : t + h] = edge_mean / h + rng.normal(
                        0.0, motif.trade_vol / max(h, 1), size=h
                    )
                    plant_indices.append(start)
                    count += 1
                    t += max(motif.period, m + h)
                else:
                    t += 1
        close = start_price * np.exp(np.cumsum(noise))

    open_ = np.concatenate([[start_price], close[:-1]])
    high = np.maximum(open_, close) * (1.0 + 0.0002)
    low = np.minimum(open_, close) * (1.0 - 0.0002)
    ret = np.concatenate([[0.0], np.diff(close) / close[:-1]])
    bars = pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "ret": ret},
        index=idx,
    )
    is_mask = np.zeros(n, dtype=bool)
    is_mask[: len(idx_is)] = True
    oos_mask = ~is_mask
    return SyntheticBars(
        bars=bars,
        is_mask=is_mask,
        oos_mask=oos_mask,
        motif=motif,
        plant_indices=np.asarray(plant_indices, dtype=int),
    )


def default_motif_shape(m: int = 30, seed: int = 1) -> np.ndarray:
    """Deterministic z-scored motif template (unit variance)."""
    rng = np.random.default_rng(seed)
    raw = np.linspace(-1.0, 1.0, m) + 0.15 * rng.normal(size=m)
    raw = raw - raw.mean()
    sd = raw.std(ddof=1)
    return raw / sd if sd > 0 else raw
