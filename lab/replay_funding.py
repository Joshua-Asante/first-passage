"""replay_funding.py — exact conservative funding evidence for a candidate execution.

A chronological replay needs a small, isolated arithmetic proof that a supplied
candidate execution sits strictly inside a fully funded interior. This helper
is that proof only: it separates the arithmetic witness from the caller's
order lifecycle, price formation and accounting. A submission-time positive
witness cannot authorize a later fill after a price gap — the caller must
establish fresh facts (a new `FundingFacts`) at each candidate fill.

Scope note (handoff docs/briefs/handoffs/2026-09-05-claude-funding-evidence.md):
this module performs no I/O, holds no state, and does not touch any broker,
order, sizing or admission path. `OUTSIDE_PROVEN_DOMAIN` means only that this
proof does not apply to the supplied facts — it never means reject, clip,
liquidate, cancel or accept an order. The caller alone is responsible for
verifying attestations, consistent currency units, complete prior accounting,
order ownership and the current execution-point mark.

Supported interior: known state; established execution price; `LONG`;
`requested_quantity == 1`; `margin_ratio == 1`; `open_quantity == 0`; no
competing entry (`competing_entry_count == 0`, where a competing entry is any
submitted request with a zero reservation). Everything else returns
`OUTSIDE_PROVEN_DOMAIN` with the first-matching reason, in this fixed
precedence: UNKNOWN_STATE, UNESTABLISHED_EXECUTION_PRICE,
UNSUPPORTED_SIDE_MARGIN_QUANTITY, EXISTING_POSITION, COMPETING_ENTRY, then the
arithmetic (NON_POSITIVE_CUSHION on a zero/negative surplus).

Arithmetic (exact, Decimal, independent of the caller's ambient Decimal
context — see `_EXACT_ARITHMETIC_CONTEXT`):

    cash_after_cost       = cash_before - execution_cost
    funding_basis         = max(execution_price, current_mark)
    required_at_basis     = requested_quantity * point_value * funding_basis
    surplus               = cash_after_cost - required_at_basis
    post_fill_margin_cushion = cash_after_cost
                               - requested_quantity * point_value * execution_price

`execution_price` already includes slippage; `execution_cost` is the total
known cost for this candidate execution — callers must not add a duplicate
slippage charge on top of it.
"""

from dataclasses import dataclass
from decimal import Context, Decimal, localcontext
from enum import Enum
from typing import Optional

# A fixed, generously high-precision context used for every arithmetic step so
# the returned witnesses cannot change with the caller's ambient
# decimal.getcontext() precision or rounding mode (frozen behavior contract
# §3). Comparisons (`==`, `!=`, `>`, `max`) are exact in the decimal module
# regardless of context and need no such override.
_EXACT_ARITHMETIC_CONTEXT = Context(prec=200)

_SUPPORTED_DIRECTION = "LONG"


class FundingStatus(str, Enum):
    """Outcome of an `assess_funding` call."""

    PROVEN_POSITIVE_CUSHION = "PROVEN_POSITIVE_CUSHION"
    OUTSIDE_PROVEN_DOMAIN = "OUTSIDE_PROVEN_DOMAIN"
    INVALID_INPUT = "INVALID_INPUT"


class FundingReason(str, Enum):
    """Reason code paired with every `FundingStatus`."""

    UNKNOWN_STATE = "UNKNOWN_STATE"
    UNESTABLISHED_EXECUTION_PRICE = "UNESTABLISHED_EXECUTION_PRICE"
    UNSUPPORTED_SIDE_MARGIN_QUANTITY = "UNSUPPORTED_SIDE_MARGIN_QUANTITY"
    EXISTING_POSITION = "EXISTING_POSITION"
    COMPETING_ENTRY = "COMPETING_ENTRY"
    POSITIVE_CUSHION = "POSITIVE_CUSHION"
    NON_POSITIVE_CUSHION = "NON_POSITIVE_CUSHION"
    INVALID_INPUT = "INVALID_INPUT"


@dataclass(frozen=True)
class FundingFacts:
    """Caller-supplied facts for one candidate execution. Invented/test facts only —
    never populate this from a live account, capture or campaign export."""

    cash_before: Decimal
    point_value: Decimal
    execution_price: Decimal
    current_mark: Decimal
    execution_cost: Decimal
    margin_ratio: Decimal
    requested_quantity: int
    open_quantity: int
    competing_entry_count: int
    direction: str
    known_state: bool
    execution_price_established: bool


@dataclass(frozen=True)
class FundingAssessment:
    """Result of one `assess_funding` call. Witness fields are `None` for
    `INVALID_INPUT` and every `OUTSIDE_PROVEN_DOMAIN` reason reached before the
    arithmetic step; `NON_POSITIVE_CUSHION` retains its arithmetic witnesses."""

    status: FundingStatus
    reason: FundingReason
    cash_after_cost: Optional[Decimal]
    funding_basis: Optional[Decimal]
    required_at_basis: Optional[Decimal]
    surplus: Optional[Decimal]
    post_fill_margin_cushion: Optional[Decimal]


def _is_plain_int(value: object) -> bool:
    """True only for an actual `int` — excludes `bool` (an `int` subclass),
    `float` and `fractions.Fraction`."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_finite_decimal(value: object) -> bool:
    """True only for an actual finite `Decimal` — no float/int coercion, no
    NaN/Infinity."""
    return isinstance(value, Decimal) and value.is_finite()


def _shape_is_valid(facts: FundingFacts) -> bool:
    """Field-level type and sign validation (frozen behavior contract §2)."""
    decimal_fields = (
        facts.cash_before,
        facts.point_value,
        facts.execution_price,
        facts.current_mark,
        facts.execution_cost,
        facts.margin_ratio,
    )
    if not all(_is_finite_decimal(value) for value in decimal_fields):
        return False
    if facts.point_value <= 0 or facts.execution_price <= 0 or facts.current_mark <= 0:
        return False
    if facts.execution_cost < 0 or facts.margin_ratio < 0:
        return False

    int_fields = (facts.requested_quantity, facts.open_quantity, facts.competing_entry_count)
    if not all(_is_plain_int(value) and value >= 0 for value in int_fields):
        return False

    if not isinstance(facts.direction, str):
        return False
    if not isinstance(facts.known_state, bool) or not isinstance(
        facts.execution_price_established, bool
    ):
        return False

    return True


def _invalid_input() -> FundingAssessment:
    return FundingAssessment(
        status=FundingStatus.INVALID_INPUT,
        reason=FundingReason.INVALID_INPUT,
        cash_after_cost=None,
        funding_basis=None,
        required_at_basis=None,
        surplus=None,
        post_fill_margin_cushion=None,
    )


def _outside_domain(reason: FundingReason) -> FundingAssessment:
    return FundingAssessment(
        status=FundingStatus.OUTSIDE_PROVEN_DOMAIN,
        reason=reason,
        cash_after_cost=None,
        funding_basis=None,
        required_at_basis=None,
        surplus=None,
        post_fill_margin_cushion=None,
    )


def assess_funding(facts: FundingFacts) -> FundingAssessment:
    """Return the exact conservative funding witness for one candidate execution.

    Pure and side-effect-free: no I/O, no mutation of `facts` or any external
    state, no broker/order action of any kind. `OUTSIDE_PROVEN_DOMAIN` means
    only that this proof does not cover the supplied facts.
    """
    if not isinstance(facts, FundingFacts) or not _shape_is_valid(facts):
        return _invalid_input()

    if not facts.known_state:
        return _outside_domain(FundingReason.UNKNOWN_STATE)
    if not facts.execution_price_established:
        return _outside_domain(FundingReason.UNESTABLISHED_EXECUTION_PRICE)
    if (
        facts.direction != _SUPPORTED_DIRECTION
        or facts.margin_ratio != Decimal(1)
        or facts.requested_quantity != 1
    ):
        return _outside_domain(FundingReason.UNSUPPORTED_SIDE_MARGIN_QUANTITY)
    if facts.open_quantity != 0:
        return _outside_domain(FundingReason.EXISTING_POSITION)
    if facts.competing_entry_count != 0:
        return _outside_domain(FundingReason.COMPETING_ENTRY)

    with localcontext(_EXACT_ARITHMETIC_CONTEXT):
        quantity = Decimal(facts.requested_quantity)
        cash_after_cost = facts.cash_before - facts.execution_cost
        funding_basis = max(facts.execution_price, facts.current_mark)
        required_at_basis = quantity * facts.point_value * funding_basis
        surplus = cash_after_cost - required_at_basis
        post_fill_margin_cushion = (
            cash_after_cost - quantity * facts.point_value * facts.execution_price
        )

    if surplus > 0:
        status = FundingStatus.PROVEN_POSITIVE_CUSHION
        reason = FundingReason.POSITIVE_CUSHION
    else:
        status = FundingStatus.OUTSIDE_PROVEN_DOMAIN
        reason = FundingReason.NON_POSITIVE_CUSHION

    return FundingAssessment(
        status=status,
        reason=reason,
        cash_after_cost=cash_after_cost,
        funding_basis=funding_basis,
        required_at_basis=required_at_basis,
        surplus=surplus,
        post_fill_margin_cushion=post_fill_margin_cushion,
    )
