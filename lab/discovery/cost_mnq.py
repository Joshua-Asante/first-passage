"""MNQ cost hurdle — firm_rules commissions + CME micro tick economics.

D5 Stage-2 cost-law kill: mean gross trade return ≥ 4× RT cost as a fraction of
notional (strategy-validation §2; pre-reg §3). Commission comes from
``firm_rules.cost_per_side_usd`` (index-micro row); do not hardcode MGC/MES
dollars here.
"""
from __future__ import annotations

from dataclasses import dataclass

try:
    from firm_rules import FIRM_RULES
except ImportError:  # pragma: no cover
    from core.firm_rules import FIRM_RULES

# CME MNQ specs (proxy-discipline.md).
MNQ_MULTIPLIER = 2.0  # $2 per index point
MNQ_TICK_SIZE = 0.25
MNQ_TICK_VALUE = MNQ_MULTIPLIER * MNQ_TICK_SIZE  # $0.50

# firm_key is required (gate-stack audit R6). The cheapest-firm default
# `DEFAULT_FIRM_KEY = "Bulenox_100K"` was retired so a caller cannot inherit
# Bulenox $0.61/side silently. New work should prefer
# `cost_model.resolve_commission(firm_key, "MNQ")`; this module remains the
# citable basis for closed D5 / D5-RECOST figures (cost_model does not
# supersede it).
SLIPPAGE_TICKS_PER_SIDE = 1.0
COST_LAW_MULTIPLE = 4.0


@dataclass(frozen=True)
class MnqCostHurdle:
    firm_key: str
    notional_usd: float
    commission_per_side_usd: float
    rt_cost_usd: float
    rt_cost_frac: float
    hurdle_1x_frac: float
    hurdle_4x_frac: float


def commission_per_side(firm_key: str) -> float:
    cps = FIRM_RULES[firm_key].get("cost_per_side_usd")
    if cps is None:
        raise ValueError(f"{firm_key!r} has no cost_per_side_usd")
    return float(cps)


def mnq_rt_cost_usd(
    firm_key: str,
    slip_ticks_per_side: float = SLIPPAGE_TICKS_PER_SIDE,
) -> float:
    slip = slip_ticks_per_side * MNQ_TICK_VALUE
    return 2.0 * (commission_per_side(firm_key) + slip)


def hurdle_from_price(
    mnq_price: float,
    *,
    firm_key: str,
    slip_ticks_per_side: float = SLIPPAGE_TICKS_PER_SIDE,
) -> MnqCostHurdle:
    """Express one round-trip cost as a fraction of MNQ notional at ``mnq_price``."""
    cps = commission_per_side(firm_key)
    notional = mnq_price * MNQ_MULTIPLIER
    rt = mnq_rt_cost_usd(firm_key, slip_ticks_per_side)
    frac = rt / notional if notional > 0 else float("inf")
    return MnqCostHurdle(
        firm_key=firm_key,
        notional_usd=notional,
        commission_per_side_usd=cps,
        rt_cost_usd=rt,
        rt_cost_frac=frac,
        hurdle_1x_frac=frac,
        hurdle_4x_frac=COST_LAW_MULTIPLE * frac,
    )


def passes_cost_law(mean_trade_return: float, hurdle: MnqCostHurdle) -> bool:
    """True iff mean per-trade simple return clears the 4× RT hurdle."""
    return mean_trade_return >= hurdle.hurdle_4x_frac
