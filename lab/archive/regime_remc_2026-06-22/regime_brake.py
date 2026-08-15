"""Exogenous regime brake — pure logic (Q-REGIME-ADAPT-1.T2b, 2026-06-22).

The ONLY new mechanism on top of the locked decompound+MC: a per-day sizing
multiplier derived from an EXOGENOUS daily signal (VIX), applied lag-honestly,
forward-filled to the panel's business days, and multiplied into the decompounded
daily-P&L panel. The standard locked MC (dd_protection C2) then runs on the
braked panel — the brake "travels with" each week-block in the bootstrap.

Pure pandas/numpy — no decompound import, no VIX, no vendor data (so it is fully
synthetic-testable). Per the T2b pre-registration
(`docs/briefs/pre-registration/Q-REGIME-ADAPT-1-T2b-verdict-preregistration.md`).
"""
from __future__ import annotations

import pandas as pd


def regime_factor_series(signal, *, threshold, k_derisk, lag_days: int = 1,
                         comparison: str = "gt") -> pd.Series:
    """Per-date sizing factor from an exogenous signal, lag-honest.

    factor[t] = k_derisk if signal[t-lag_days] {>,<} threshold else 1.0.
    lag_days=1 → the sizing for day t uses the signal as of the PRIOR day's close
    (available at start-of-day t — non-look-ahead). A brake never boosts (k<1).
    """
    lagged = signal.shift(lag_days)
    if comparison == "gt":
        stressed = lagged > threshold
    elif comparison == "lt":
        stressed = lagged < threshold
    else:
        raise ValueError(f"comparison must be 'gt' or 'lt', got {comparison!r}")
    factor = pd.Series(1.0, index=signal.index)
    factor[stressed.fillna(False)] = float(k_derisk)
    return factor


def align_factor_to_panel(factor: pd.Series, panel_index) -> pd.Series:
    """Forward-fill the (trading-day) factor onto the panel's business days; days
    before the first known signal default to 1.0 (calm — no de-risk without a
    signal). Forward-fill = the live value persists across the indicator's gaps
    (e.g. US market holidays) until it next updates."""
    panel_index = pd.DatetimeIndex(panel_index)
    union = factor.index.union(panel_index)
    return factor.reindex(union).sort_index().ffill().reindex(panel_index).fillna(1.0)


def apply_regime_brake(panel: pd.DataFrame, factor_aligned: pd.Series) -> pd.DataFrame:
    """Scale every per-strategy P&L in row t by factor_aligned[t] (sizing scales
    P&L linearly). Order-independent w.r.t. the MC's dd_protection (both
    multiplicative), so pre-scaling the panel composes correctly."""
    return panel.mul(factor_aligned, axis=0)
