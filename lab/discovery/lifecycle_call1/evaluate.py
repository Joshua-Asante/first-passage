"""Per-window Call-1 decay evaluation — calls core.lifecycle.decay_breach."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

try:
    from lifecycle import decay_breach
except ImportError:  # pragma: no cover
    from core.lifecycle import decay_breach

# PLACEHOLDER pending 2026-08-08 review pre-registration — NOT a ratified threshold.
# Logged clearly so it cannot be mistaken for a frozen constant.
MIN_TRADE_COUNT = 30
MIN_TRADE_COUNT_NOTE = (
    "MIN_TRADE_COUNT=30 is a provisional placeholder pending 2026-08-08 "
    "pre-registration; not a ratified Call-1 threshold "
    "(docs/methodology/strategy_lifecycle.md Call 1 provisional-until-data)."
)

# Ratified Call-1 k (strategy_lifecycle.md); decay_breach default matches.
K_SIGMA = 1.0

WindowOutcome = Literal["BREACH", "CLEAR", "AMBIGUOUS"]


@dataclass(frozen=True)
class WindowEvaluation:
    outcome: WindowOutcome
    breached: bool
    floor: float | None
    rolling_pf: float | None
    trade_count: int
    baseline_pf: float
    pf_sigma: float
    k_sigma: float
    ambiguous_reason: str | None = None


def evaluate_window(
    rolling_pf: float | None,
    trade_count: int,
    baseline_pf: float,
    pf_sigma: float,
    *,
    k_sigma: float = K_SIGMA,
    min_trade_count: int = MIN_TRADE_COUNT,
) -> WindowEvaluation:
    """Map one review window to BREACH | CLEAR | AMBIGUOUS.

    Thin data (``trade_count < min_trade_count``) or ``rolling_pf is None`` →
    AMBIGUOUS with ``breached=False`` (contributes no breach to the consecutive
    counter). Otherwise calls ``lifecycle.decay_breach`` — the inequality is
    never reimplemented here.
    """
    # Floor is report-only; breach itself is owned by decay_breach (never inlined).
    haircut = k_sigma * pf_sigma
    floor = float(baseline_pf) + float(-haircut)

    if rolling_pf is None:
        return WindowEvaluation(
            outcome="AMBIGUOUS",
            breached=False,
            floor=floor,
            rolling_pf=None,
            trade_count=trade_count,
            baseline_pf=baseline_pf,
            pf_sigma=pf_sigma,
            k_sigma=k_sigma,
            ambiguous_reason="rolling_pf is None",
        )
    if trade_count < min_trade_count:
        return WindowEvaluation(
            outcome="AMBIGUOUS",
            breached=False,
            floor=floor,
            rolling_pf=float(rolling_pf),
            trade_count=trade_count,
            baseline_pf=baseline_pf,
            pf_sigma=pf_sigma,
            k_sigma=k_sigma,
            ambiguous_reason=(
                f"trade_count {trade_count} < MIN_TRADE_COUNT {min_trade_count} "
                f"({MIN_TRADE_COUNT_NOTE})"
            ),
        )

    breached = bool(
        decay_breach(float(rolling_pf), float(baseline_pf), float(pf_sigma), k_sigma)
    )
    return WindowEvaluation(
        outcome="BREACH" if breached else "CLEAR",
        breached=breached,
        floor=floor,
        rolling_pf=float(rolling_pf),
        trade_count=trade_count,
        baseline_pf=baseline_pf,
        pf_sigma=pf_sigma,
        k_sigma=k_sigma,
        ambiguous_reason=None,
    )
