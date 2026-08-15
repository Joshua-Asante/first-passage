"""ES-parent cost hurdle — FROZEN PASSIVE model for H-OD-1 Stage-2.

Pre-reg: docs/briefs/pre-registration/H-OD-1-ES-overnight-drift-preregistration.md
§2 (Execution/cost model row) + §R.1 (passive-vs-crossing table).

FROZEN model (do NOT substitute D5's ``cost_mnq.py`` crossing model):
  * slippage = 0.5 ES tick for the ENTIRE round trip (passive-both-sides),
    NOT 1 tick per side. 0.5 * 12.50 = $6.25 RT.
  * commission = ES-parent assumption (pre-reg §2: <= $3.00/side, <= 0.03bp,
    negligible but included), 2 sides.
  * notional = price * ES multiplier ($50), i.e. ES-PARENT notional (the
    confirm instrument). The MES micro cliff is a separate Stage-7 read.

RT_usd = 0.5*ES_TICK_VALUE + 2*commission_per_side.
"""
from __future__ import annotations

from dataclasses import dataclass

# CME ES specs.
ES_MULTIPLIER = 50.0  # $50 per index point
ES_TICK_SIZE = 0.25
ES_TICK_VALUE = ES_MULTIPLIER * ES_TICK_SIZE  # $12.50

# FROZEN passive model.
PASSIVE_SLIP_TICKS_RT = 0.5  # HALF a tick for the WHOLE round trip (not per side)
ES_PARENT_COMMISSION_PER_SIDE = 3.00  # pre-reg §2 conservative ES-parent assumption
COST_LAW_MULTIPLE = 4.0


@dataclass(frozen=True)
class EsCostHurdle:
    notional_usd: float
    commission_per_side_usd: float
    slip_usd_rt: float
    rt_cost_usd: float
    rt_cost_frac: float
    hurdle_1x_frac: float
    hurdle_4x_frac: float


def es_rt_cost_usd(
    commission_per_side: float = ES_PARENT_COMMISSION_PER_SIDE,
    slip_ticks_rt: float = PASSIVE_SLIP_TICKS_RT,
) -> float:
    """Round-trip $ cost: HALF-tick total slip + two commissions."""
    slip = slip_ticks_rt * ES_TICK_VALUE
    return slip + 2.0 * commission_per_side


def hurdle_from_price(
    es_price: float,
    *,
    commission_per_side: float = ES_PARENT_COMMISSION_PER_SIDE,
    slip_ticks_rt: float = PASSIVE_SLIP_TICKS_RT,
) -> EsCostHurdle:
    """One round-trip cost as a fraction of ES-parent notional at ``es_price``."""
    notional = es_price * ES_MULTIPLIER
    slip = slip_ticks_rt * ES_TICK_VALUE
    rt = slip + 2.0 * commission_per_side
    frac = rt / notional if notional > 0 else float("inf")
    return EsCostHurdle(
        notional_usd=notional,
        commission_per_side_usd=commission_per_side,
        slip_usd_rt=slip,
        rt_cost_usd=rt,
        rt_cost_frac=frac,
        hurdle_1x_frac=frac,
        hurdle_4x_frac=COST_LAW_MULTIPLE * frac,
    )


def passes_cost_law(mean_trade_return: float, hurdle: EsCostHurdle) -> bool:
    """True iff mean per-trade simple return clears the 4x RT hurdle."""
    return mean_trade_return >= hurdle.hurdle_4x_frac
