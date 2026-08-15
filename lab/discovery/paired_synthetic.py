"""Paired GC/MGC synthetic 1h series — additive extension for Stage-7 proofs.

Shares one injected motif edge between a GC-like parent series and an MGC-like
micro series. Does **not** modify ``synthetic_bars.generate_synthetic_bars``.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from discovery.synthetic_bars import (
    MotifSpec,
    SyntheticBars,
    generate_synthetic_bars,
)


@dataclass(frozen=True)
class PairedSyntheticBars:
    """GC + MGC bar frames on a shared UTC grid (MGC may drop bars)."""

    gc: pd.DataFrame
    mgc: pd.DataFrame
    gc_grid: pd.DatetimeIndex
    oos_mask: np.ndarray
    plant_indices: np.ndarray
    bar_drop_frac: float
    gross_scale_mgc: float  # multiplicative gross degradation on MGC path


def generate_paired_gc_mgc(
    *,
    seed: int = 0,
    motif: MotifSpec | None = None,
    plant_in_oos_only: bool = True,
    bar_drop_frac: float = 0.0,
    gross_scale_mgc: float = 1.0,
    base_volume: float = 100.0,
    is_start: str = "2010-01-01",
    is_end: str = "2018-12-31",
    oos_start: str = "2019-05-06",
    oos_end: str = "2026-07-01",
) -> PairedSyntheticBars:
    """Build paired GC/MGC 1h series sharing one planted edge.

    ``gross_scale_mgc < 1`` degrades realized MGC gross (fill slippage in the
    return path). ``bar_drop_frac`` randomly drops that fraction of MGC bars
    (thin-market simulation) while GC keeps the full grid.
    """
    synth = generate_synthetic_bars(
        seed=seed,
        motif=motif,
        plant_in_oos_only=plant_in_oos_only,
        is_start=is_start,
        is_end=is_end,
        oos_start=oos_start,
        oos_end=oos_end,
    )
    gc = synth.bars.copy()
    gc["volume"] = base_volume + np.random.default_rng(seed + 11).normal(
        0.0, base_volume * 0.1, size=len(gc)
    )
    mgc = gc.copy()
    if gross_scale_mgc != 1.0:
        mgc["ret"] = mgc["ret"].to_numpy(dtype=float) * float(gross_scale_mgc)
        close = float(gc["close"].iloc[0]) * np.exp(np.cumsum(mgc["ret"].to_numpy()))
        mgc["close"] = close
        mgc["open"] = np.concatenate([[close[0]], close[:-1]])
        mgc["high"] = np.maximum(mgc["open"], mgc["close"]) * 1.0002
        mgc["low"] = np.minimum(mgc["open"], mgc["close"]) * 0.9998

    if bar_drop_frac > 0.0:
        rng = np.random.default_rng(seed + 17)
        n_drop = int(round(bar_drop_frac * len(mgc)))
        drop_idx = rng.choice(len(mgc), size=n_drop, replace=False)
        keep = np.ones(len(mgc), dtype=bool)
        keep[drop_idx] = False
        mgc = mgc.iloc[keep].copy()

    return PairedSyntheticBars(
        gc=gc,
        mgc=mgc,
        gc_grid=gc.index,
        oos_mask=synth.oos_mask,
        plant_indices=synth.plant_indices,
        bar_drop_frac=float(bar_drop_frac),
        gross_scale_mgc=float(gross_scale_mgc),
    )
