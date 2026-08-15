"""MGC cost hurdle — generalize HARV-0 ``cost_hurdle.py`` to MGC tick economics.

MGC tick value = $1.00 (CME micro gold). Cost-law kill = expectancy < 4× RT hurdle
(strategy-validation §2). Constants are frozen campaign inputs, not retuned here.
"""
from __future__ import annotations

from dataclasses import dataclass

# CME MGC specs (micro gold).
MGC_MULTIPLIER = 10.0  # $10 per $1/oz
MGC_TICK_SIZE = 0.10  # $0.10/oz
MGC_TICK_VALUE = 1.00  # $1.00 per tick (multiplier * tick_size)

COMMISSION_PER_SIDE_USD = 0.62
SLIPPAGE_TICKS_PER_SIDE = 1.0
COST_LAW_MULTIPLE = 4.0


@dataclass(frozen=True)
class MgcCostHurdle:
    notional_usd: float
    rt_cost_usd: float
    rt_cost_frac: float
    hurdle_1x_frac: float
    hurdle_4x_frac: float


def mgc_rt_cost_usd(
    commission_per_side: float = COMMISSION_PER_SIDE_USD,
    slip_ticks_per_side: float = SLIPPAGE_TICKS_PER_SIDE,
) -> float:
    slip = slip_ticks_per_side * MGC_TICK_VALUE
    return 2.0 * (commission_per_side + slip)


def hurdle_from_price(
    mgc_price: float,
    *,
    commission_per_side: float = COMMISSION_PER_SIDE_USD,
    slip_ticks_per_side: float = SLIPPAGE_TICKS_PER_SIDE,
) -> MgcCostHurdle:
    """Express one round-trip cost as a fraction of notional at ``mgc_price``."""
    notional = mgc_price * MGC_MULTIPLIER
    rt = mgc_rt_cost_usd(commission_per_side, slip_ticks_per_side)
    frac = rt / notional if notional > 0 else float("inf")
    return MgcCostHurdle(
        notional_usd=notional,
        rt_cost_usd=rt,
        rt_cost_frac=frac,
        hurdle_1x_frac=frac,
        hurdle_4x_frac=COST_LAW_MULTIPLE * frac,
    )


def passes_cost_law(mean_trade_return: float, hurdle: MgcCostHurdle) -> bool:
    """True iff mean per-trade simple return clears the 4× RT hurdle."""
    return mean_trade_return >= hurdle.hurdle_4x_frac
