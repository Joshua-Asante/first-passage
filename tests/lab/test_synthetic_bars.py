"""Standalone tests for lab/discovery/synthetic_bars.py.

Its old tests went with the Stage-2/4 miner (Subtract, 2026-11-10). Kept per
recommendation 5 of the 2026-11-09 rulings.
"""
from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("pandas")

from discovery.synthetic_bars import (  # noqa: E402
    MAINTENANCE_HOUR_UTC,
    MotifSpec,
    default_motif_shape,
    generate_synthetic_bars,
)

SHORT = dict(is_start="2020-01-01", is_end="2020-03-31", oos_start="2020-05-04", oos_end="2020-06-30")


def _motif(**kw):
    base = dict(
        shape=default_motif_shape(m=10),
        horizon=5,
        direction=1,
        per_trade_sr=2.0,
        trade_vol=0.01,
        period=60,
    )
    base.update(kw)
    return MotifSpec(**base)


def test_same_seed_same_bars():
    a = generate_synthetic_bars(seed=7, **SHORT)
    b = generate_synthetic_bars(seed=7, **SHORT)
    c = generate_synthetic_bars(seed=8, **SHORT)
    assert a.bars.equals(b.bars)
    assert not a.bars["close"].equals(c.bars["close"])


def test_grid_masks_and_ohlc():
    sb = generate_synthetic_bars(seed=1, **SHORT)
    idx = sb.bars.index
    assert idx.is_monotonic_increasing and str(idx.tz) == "UTC"
    assert (idx.dayofweek < 5).all()
    assert not (idx.hour == MAINTENANCE_HOUR_UTC).any()
    assert sb.is_mask.sum() + sb.oos_mask.sum() == len(idx)
    assert not (sb.is_mask & sb.oos_mask).any()
    assert idx[sb.is_mask].max() < idx[sb.oos_mask].min()
    bars = sb.bars
    assert (bars["high"] >= bars[["open", "close"]].max(axis=1)).all()
    assert (bars["low"] <= bars[["open", "close"]].min(axis=1)).all()
    assert len(sb.plant_indices) == 0 and sb.motif is None


def test_planted_motif_moves_price_in_its_direction():
    for direction in (1, -1):
        motif = _motif(direction=direction)
        sb = generate_synthetic_bars(seed=3, motif=motif, **SHORT)
        assert len(sb.plant_indices) > 5
        close = sb.bars["close"].to_numpy()
        m, h = motif.shape.size, motif.horizon
        fwd = [np.log(close[s + m - 1 + h] / close[s + m - 1]) for s in sb.plant_indices]
        expected = motif.per_trade_sr * motif.trade_vol
        assert direction * np.mean(fwd) == pytest.approx(expected, rel=0.5)


def test_oos_only_plant_and_trade_cap():
    motif = _motif(max_oos_trades=3)
    sb = generate_synthetic_bars(seed=4, motif=motif, plant_in_oos_only=True, **SHORT)
    assert len(sb.plant_indices) == 3
    assert sb.oos_mask[sb.plant_indices].all()


def test_default_motif_shape_is_z_scored_and_deterministic():
    s = default_motif_shape(m=30, seed=1)
    assert s.shape == (30,)
    assert s.mean() == pytest.approx(0.0, abs=1e-12)
    assert s.std(ddof=1) == pytest.approx(1.0)
    assert np.array_equal(s, default_motif_shape(m=30, seed=1))
