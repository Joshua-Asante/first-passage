"""GROW-0 TRAIN/CONFIRM statistic and nomination gates.

Frozen scoring convention per the prereg §3: annualized Sharpe (sqrt(252)) of the daily net P&L
series, identical formula on TRAIN and CONFIRM. Nomination gates per prereg §6.1 step 4.
"""
from __future__ import annotations

import numpy as np

_TRADING_DAYS_PER_YEAR = 252
_TRADING_DAYS_PER_WEEK = 5.0


def annualized_sharpe(daily_pnl: np.ndarray) -> float:
    mean = daily_pnl.mean()
    sd = daily_pnl.std(ddof=0)
    return float(mean / sd * np.sqrt(_TRADING_DAYS_PER_YEAR))


def gate_a_passes(train_stat: float) -> bool:
    """Prereg §6.1 step 4(a): TRAIN net annSR > 0 (strict)."""
    return train_stat > 0.0


def gate_b_passes(train_pnl: np.ndarray) -> bool:
    """Prereg §6.1 step 4(b): TRAIN average weekly active-day cadence >= 1/week.

    An *average* floor over the full window, not a zero-tolerance-per-week rule
    (DL-1's own gate-2c convention, imported verbatim per the prereg).
    """
    n_days = train_pnl.shape[0]
    n_weeks = n_days / _TRADING_DAYS_PER_WEEK
    active_days = int(np.count_nonzero(train_pnl))
    return (active_days / n_weeks) >= 1.0
