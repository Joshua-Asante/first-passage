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


from dataclasses import dataclass

from discovery.grow0_dgp import draw_daily_pnl


@dataclass(frozen=True)
class PanelResult:
    nominee: int
    train_stat: float
    gate_a: bool
    gate_b: bool
    abandoned: bool
    confirm_stat: float | None
    clears: bool


def _score_all_variants(train_children, edge_variant_index):
    pnls = [
        draw_daily_pnl(train_children[i], edge=(i == edge_variant_index))
        for i in range(len(train_children))
    ]
    stats = [annualized_sharpe(p) for p in pnls]
    return pnls, stats


def run_panel(
    train_children,
    confirm_children,
    *,
    edge_variant_index: int | None,
    floor: float,
) -> PanelResult:
    """Prereg §6.1 steps 1-6 / §6.2: draw TRAIN for every variant, nominate by
    argmax (unconditional, no fallback), apply nomination gates on the nominee
    only, and -- if both gates pass -- draw an INDEPENDENT CONFIRM for the
    nominee and compare to ``floor``.
    """
    pnls, stats = _score_all_variants(train_children, edge_variant_index)
    nominee = int(max(range(len(stats)), key=lambda i: stats[i]))
    ga = gate_a_passes(stats[nominee])
    gb = gate_b_passes(pnls[nominee])
    if not (ga and gb):
        return PanelResult(
            nominee=nominee,
            train_stat=stats[nominee],
            gate_a=ga,
            gate_b=gb,
            abandoned=True,
            confirm_stat=None,
            clears=False,
        )
    confirm_pnl = draw_daily_pnl(
        confirm_children[nominee], edge=(nominee == edge_variant_index)
    )
    confirm_stat = annualized_sharpe(confirm_pnl)
    return PanelResult(
        nominee=nominee,
        train_stat=stats[nominee],
        gate_a=ga,
        gate_b=gb,
        abandoned=False,
        confirm_stat=confirm_stat,
        clears=confirm_stat >= floor,
    )


def run_panel_leaked(
    train_children,
    *,
    edge_variant_index: int | None,
    floor: float,
) -> PanelResult:
    """Prereg §6.3 RED-LEAK: identical to run_panel, except CONFIRM is the
    nominee's own winning TRAIN value replayed -- no independent draw at all.
    Deliberately violates the TRAIN/CONFIRM independence run_panel relies on.
    """
    pnls, stats = _score_all_variants(train_children, edge_variant_index)
    nominee = int(max(range(len(stats)), key=lambda i: stats[i]))
    ga = gate_a_passes(stats[nominee])
    gb = gate_b_passes(pnls[nominee])
    if not (ga and gb):
        return PanelResult(
            nominee=nominee,
            train_stat=stats[nominee],
            gate_a=ga,
            gate_b=gb,
            abandoned=True,
            confirm_stat=None,
            clears=False,
        )
    leaked_confirm_stat = stats[nominee]
    return PanelResult(
        nominee=nominee,
        train_stat=stats[nominee],
        gate_a=ga,
        gate_b=gb,
        abandoned=False,
        confirm_stat=leaked_confirm_stat,
        clears=leaked_confirm_stat >= floor,
    )
