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
competing entry (`competing_entry_count == 0`; competing entries are all
submitted requests contending for the same admission, including but not
limited to any with a zero reservation). Everything else returns
`OUTSIDE_PROVEN_DOMAIN` with the first-matching reason, in this fixed
precedence: UNKNOWN_STATE, UNESTABLISHED_EXECUTION_PRICE,
UNSUPPORTED_SIDE_MARGIN_QUANTITY, EXISTING_POSITION, COMPETING_ENTRY, then the
arithmetic (NON_POSITIVE_CUSHION on a zero/negative surplus, or
ARITHMETIC_LIMIT — handoff §3.1 — if an exact witness cannot be produced;
see below).

Arithmetic (exact, Decimal, independent of the caller's ambient Decimal
context — see `_exact_add`/`_exact_subtract`/`_exact_multiply`):

    cash_after_cost       = cash_before - execution_cost
    funding_basis         = max(execution_price, current_mark)
    required_at_basis     = requested_quantity * point_value * funding_basis
    surplus               = cash_after_cost - required_at_basis
    post_fill_margin_cushion = cash_after_cost
                               - requested_quantity * point_value * execution_price

`execution_price` already includes slippage; `execution_cost` is the total
known cost for this candidate execution — callers must not add a duplicate
slippage charge on top of it.

Precision and exponent bounds for every step are derived from the actual
operands (their stored coefficient digit counts and exponents) rather than a
fixed cap. A zero operand is returned as the other operand unchanged instead
of letting decimal's ideal-exponent rule for `x +/- 0`
(`min(exponent(x), exponent(0))`) force a compact, large-exponent `x` to
materialize an astronomically large coefficient for no numeric benefit — the
same reasoning applies to two equal-exponent operands, whose exact difference
is cheap regardless of magnitude because no realignment is needed. Finite,
shape-valid operands do not guarantee a representable or safely materializable
result Decimal (handoff §3.1): if an exact witness's exponent would exceed
Decimal's native representable range, or its exact coefficient would need
more digits than a bounded arithmetic-resource ceiling
(`_MAX_EXACT_PRECISION`), the step is preflighted to fail before it is
attempted, and `assess_funding` returns `OUTSIDE_PROVEN_DOMAIN` /
`ARITHMETIC_LIMIT` with every witness `None` — a defined non-proof outcome,
never a rounded substitute or a broker action.
"""

import decimal
from dataclasses import dataclass
from decimal import Decimal, Inexact, localcontext
from enum import Enum
from typing import Optional

# A resource ceiling on the exact coefficient precision a single step may
# require. Decimal's native Emax/Emin already bound representable exponents;
# this bounds the *span* between two operands' exponents, which can be huge
# (and so require an equally huge coefficient to add/subtract exactly) even
# when both operands' own exponents are individually well within range.
_MAX_EXACT_PRECISION = 1_000_000

_SUPPORTED_DIRECTION = "LONG"


class _ArithmeticLimit(Exception):
    """Raised internally when an exact witness would exceed Decimal's native
    result range or `_MAX_EXACT_PRECISION`. Caught only by `assess_funding`,
    which translates it to `OUTSIDE_PROVEN_DOMAIN` / `ARITHMETIC_LIMIT`."""


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
    ARITHMETIC_LIMIT = "ARITHMETIC_LIMIT"
    INVALID_INPUT = "INVALID_INPUT"


@dataclass(frozen=True)
class FundingFacts:
    """Caller-supplied facts for one candidate execution — a reusable, pure
    data contract, not a fixture. This module's own tests and public
    examples populate it with invented values only; an authorized caller may
    later supply its own private facts here, subject to the same no-I/O,
    no-broker-action boundary this module holds everywhere else."""

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
    `INVALID_INPUT` and every `OUTSIDE_PROVEN_DOMAIN` reason reached before
    the arithmetic finishes exactly; `NON_POSITIVE_CUSHION` retains its
    arithmetic witnesses."""

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


def _require_bounded_exponent(exponent: int) -> None:
    """Preflight an exponent against Decimal's native representable range,
    raising `_ArithmeticLimit` before any allocation is attempted rather than
    letting the arithmetic itself raise `decimal.Overflow`."""
    if exponent > decimal.MAX_EMAX or exponent < decimal.MIN_EMIN:
        raise _ArithmeticLimit()


def _bounded_context(prec: int) -> decimal.Context:
    """A context sized to exactly `prec` digits, spanning Decimal's full
    native exponent range, that fails loudly (traps `Inexact`) rather than
    silently discarding a significant digit. `Rounded` is left untrapped:
    it fires whenever a coefficient is rounded to fit `prec`, including when
    the discarded digits are all zero and the value is unchanged, so trapping
    it would reject exact results (handoff §3.1)."""
    ctx = decimal.Context(prec=prec, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN)
    ctx.traps[Inexact] = True
    return ctx


def _exact_add(a: Decimal, b: Decimal) -> Decimal:
    """Exact `a + b`, with precision and exponent bounds sized to these two
    operands only. A zero operand short-circuits to the other operand as-is
    (see module docstring); two operands sharing an exponent are cheap by
    construction, since no realignment is needed regardless of magnitude."""
    if b == 0:
        return a
    if a == 0:
        return b

    a_exponent = a.as_tuple().exponent
    b_exponent = b.as_tuple().exponent
    low = min(a_exponent, b_exponent)
    high = max(a.adjusted(), b.adjusted()) + 2  # +1 for a possible carry digit, +1 to size a length
    _require_bounded_exponent(low)
    _require_bounded_exponent(high)

    needed_precision = high - low
    if needed_precision > _MAX_EXACT_PRECISION:
        raise _ArithmeticLimit()

    try:
        with localcontext(_bounded_context(needed_precision)):
            return a + b
    except (Inexact, decimal.Overflow, MemoryError) as exc:
        raise _ArithmeticLimit() from exc


def _exact_subtract(a: Decimal, b: Decimal) -> Decimal:
    """Exact `a - b`; see `_exact_add` for the sizing and zero-operand rules."""
    return _exact_add(a, b.copy_negate())


def _exact_multiply(*factors: Decimal) -> Decimal:
    """Exact product of two or more Decimals, with precision and exponent
    bounds sized to these operands only. Any zero factor short-circuits to
    exact zero."""
    if any(factor == 0 for factor in factors):
        return Decimal(0)

    exponents = [factor.as_tuple().exponent for factor in factors]
    digit_counts = [len(factor.as_tuple().digits) for factor in factors]
    total_exponent = sum(exponents)
    total_digits = sum(digit_counts)
    _require_bounded_exponent(total_exponent)
    _require_bounded_exponent(total_exponent + total_digits)  # +1 headroom for a carry digit

    if total_digits > _MAX_EXACT_PRECISION:
        raise _ArithmeticLimit()

    try:
        with localcontext(_bounded_context(total_digits)):
            result = factors[0]
            for factor in factors[1:]:
                result = result * factor
            return result
    except (Inexact, decimal.Overflow, MemoryError) as exc:
        raise _ArithmeticLimit() from exc


def _exact_arithmetic(facts: FundingFacts):
    """Compute the five arithmetic witnesses exactly, sizing each step's
    precision and exponent bounds to its own operands (`_exact_add`,
    `_exact_subtract`, `_exact_multiply`) instead of a fixed cap. Raises
    `_ArithmeticLimit` — caught only by `assess_funding` — if any step's
    exact result is not representable or not safely materializable.
    """
    quantity = Decimal(facts.requested_quantity)
    cash_after_cost = _exact_subtract(facts.cash_before, facts.execution_cost)
    funding_basis = max(facts.execution_price, facts.current_mark)
    required_at_basis = _exact_multiply(quantity, facts.point_value, funding_basis)
    surplus = _exact_subtract(cash_after_cost, required_at_basis)
    post_fill_margin_cushion = _exact_subtract(
        cash_after_cost, _exact_multiply(quantity, facts.point_value, facts.execution_price)
    )
    return (
        cash_after_cost,
        funding_basis,
        required_at_basis,
        surplus,
        post_fill_margin_cushion,
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

    try:
        (
            cash_after_cost,
            funding_basis,
            required_at_basis,
            surplus,
            post_fill_margin_cushion,
        ) = _exact_arithmetic(facts)
    except _ArithmeticLimit:
        return _outside_domain(FundingReason.ARITHMETIC_LIMIT)

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
