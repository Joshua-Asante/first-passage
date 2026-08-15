"""Cost hurdles for HARV-2026-001 — empirical MES specs → window-return bp.

Single-RT: full-window (close-to-close) mechanism expression.
2-RT: envelope-capturable C expression (two session round-trips).
"""
from __future__ import annotations

from dataclasses import dataclass

# CME MES specs (verify at pull time; do not trust ballpark alone).
MES_MULTIPLIER = 5.0  # $5 per index point
MES_TICK_SIZE = 0.25  # index points
MES_TICK_VALUE = MES_MULTIPLIER * MES_TICK_SIZE  # $1.25

# Operator-verifyable commission+slippage assumption (RT = open+close).
# Conservative automation-friendly prop: ~$0.50–1.00/side + 1 tick slip/side.
COMMISSION_PER_SIDE_USD = 0.62  # typical micro RT commission half
SLIPPAGE_TICKS_PER_SIDE = 1.0


@dataclass(frozen=True)
class CostHurdle:
    notional_usd: float
    rt_cost_usd: float
    rt_cost_bp: float
    hurdle_1x_bp: float
    hurdle_4x_bp: float
    n_round_trips: int


def mes_rt_cost_usd(
    commission_per_side: float = COMMISSION_PER_SIDE_USD,
    slip_ticks_per_side: float = SLIPPAGE_TICKS_PER_SIDE,
) -> float:
    slip = slip_ticks_per_side * MES_TICK_VALUE
    return 2.0 * (commission_per_side + slip)


def hurdle_from_price(
    mes_price: float,
    n_round_trips: int,
    *,
    commission_per_side: float = COMMISSION_PER_SIDE_USD,
    slip_ticks_per_side: float = SLIPPAGE_TICKS_PER_SIDE,
) -> CostHurdle:
    """Express RT cost as bps of notional at `mes_price`."""
    notional = mes_price * MES_MULTIPLIER
    rt = mes_rt_cost_usd(commission_per_side, slip_ticks_per_side)
    total = rt * n_round_trips
    bp = (total / notional) * 10_000.0
    return CostHurdle(
        notional_usd=notional,
        rt_cost_usd=rt,
        rt_cost_bp=bp / n_round_trips,
        hurdle_1x_bp=bp,
        hurdle_4x_bp=4.0 * bp,
        n_round_trips=n_round_trips,
    )


def report_hurdles(mes_price: float) -> dict[str, CostHurdle]:
    return {
        "single_rt": hurdle_from_price(mes_price, 1),
        "two_rt": hurdle_from_price(mes_price, 2),
    }


if __name__ == "__main__":
    # Mid-panel ballpark price; Wave 1 overwrites with panel median close.
    for name, h in report_hurdles(5000.0).items():
        print(
            f"{name}: notional=${h.notional_usd:,.0f} "
            f"RT=${h.rt_cost_usd:.2f} → {h.hurdle_1x_bp:.2f}bp "
            f"(4×={h.hurdle_4x_bp:.2f}bp)"
        )
