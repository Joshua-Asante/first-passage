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

Every arithmetic step is computed with exact Python-integer coefficient
arithmetic, never `decimal.Context`-bounded operations: each Decimal operand
is decomposed into its exact `(coefficient, exponent)` pair straight from
`as_tuple()` (no parsing, no rounding, no dependency on
`sys.get_int_max_str_digits()`), with insignificant trailing zero digits
stripped first (value-preserving) so a caller's own zero-padding never
inflates a later sizing estimate. Coefficients are combined with plain
integer add/multiply (which never rounds, regardless of magnitude), and the
result is rebuilt as a `Decimal` — reading its digit tuple back from
`Decimal(coefficient)` (exact and, like `as_tuple()`, independent of
`sys.get_int_max_str_digits()`, unlike `str(coefficient)`) and reassembling
via direct tuple construction, a form the constructor documents as unbound by
any context precision or exponent limit. This sidesteps an entire class of
bugs from trying to *estimate* a big-enough `decimal.Context(prec=...)` up
front: an estimate sized from operand digit counts or a `+2` carry-digit
margin is either too tight (silently rounds a valid result) or systematically
too loose (rejects a representable result, e.g. summing every factor's own
digit count overcounts a product whose actual width doesn't grow past its
widest operand, or comparing a raw exponent against `decimal.MIN_EMIN`
wrongly rejects an exact subnormal that a sufficiently-precise context could
still represent exactly, or checking an unnormalized coefficient's exponent
rejects a value whose insignificant trailing zeros would trim it back into
range).

Finite, shape-valid operands do not guarantee a representable or safely
materializable result Decimal (handoff §3.1/§3.2). Two independent limits
apply, both mapped to the same defined non-proof outcome:

  * every computed witness's *normalized* exponent is preflighted, after
    being computed exactly, against Decimal's true native ceiling on
    adjusted exponent (`decimal.MAX_EMAX`) and the most negative exponent
    representable by *any* legal context (`Emin=decimal.MIN_EMIN` at
    `prec=decimal.MAX_PREC`, i.e. the lowest `Context.Etiny()` decimal
    itself can ever produce) — see `_finalize`;
  * an add/subtract step's alignment work — the digit span its `10 **
    shift` scaling would need to construct, sized from the operands'
    *normalized* digit counts and exponents, never a padded estimate — is
    preflighted against a deterministic **1,000,000-digit work budget**
    (`_ARITHMETIC_WORK_BUDGET`, handoff §3.2) before that scaling is
    attempted, applied only after zero and exact-cancellation shortcuts, so
    a budget-sized result is never rejected merely because a speculative
    carry digit could push a loose estimate one digit over — see
    `_exact_add`.

Neither limit is a cap this module invents to substitute for Decimal's own
limits, and neither reads or mutates `sys.get_int_max_str_digits()` in any
way. When either is hit, or the underlying integer arithmetic itself
exhausts memory, `assess_funding` returns `OUTSIDE_PROVEN_DOMAIN` /
`ARITHMETIC_LIMIT` with every witness `None` — a defined non-proof outcome,
never a rounded substitute or a broker action.
"""

import decimal
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional

# The lowest exponent representable by ANY legal decimal.Context: Etiny() =
# Emin - prec + 1, minimized by pairing the most negative allowed Emin with
# the largest allowed prec. Below this, no context (however configured)
# could ever hold the value exactly — a genuine union-of-all-contexts floor,
# not a value this module chose.
_ABSOLUTE_MIN_EXPONENT = decimal.MIN_EMIN - decimal.MAX_PREC + 1

# Deterministic coefficient-work budget (handoff §3.2): the maximum digit
# span an add/subtract's alignment step may construct via `10 ** shift`,
# checked against the operands' *normalized* digit counts only — after
# zero/exact-cancellation shortcuts and trailing-zero stripping — so a
# compact operand at an astronomically large exponent never forces
# materializing an equally large aligned coefficient. Exposed as an
# injectable `_budget` keyword on `_exact_add`/`_exact_subtract` so tests can
# exercise the same algorithm cheaply at a tiny budget instead of
# constructing huge fixtures; `assess_funding` always uses this default.
_ARITHMETIC_WORK_BUDGET = 1_000_000

_SUPPORTED_DIRECTION = "LONG"


class _ArithmeticLimit(Exception):
    """Raised internally when an exact witness would exceed Decimal's native
    representable range, or the underlying integer arithmetic cannot be
    safely completed. Caught only by `assess_funding`, which translates it
    to `OUTSIDE_PROVEN_DOMAIN` / `ARITHMETIC_LIMIT`."""


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


def _normalized_coefficient_exponent(value: Decimal):
    """Exact `(signed coefficient, exponent, digit_count)` for a nonzero
    finite Decimal, read directly from its stored digit tuple — no string
    parsing, no context, no rounding, no `sys.get_int_max_str_digits()`
    dependency of any kind — with insignificant trailing zero digits
    stripped first (value-preserving: the exponent absorbs each trimmed
    zero) so a caller's own stored zero-padding never inflates a later
    alignment-span estimate or a native-range check (handoff §3.2)."""
    sign, digits, exponent = value.as_tuple()
    end = len(digits)
    while end > 1 and digits[end - 1] == 0:
        end -= 1
    exponent += len(digits) - end
    digits = digits[:end]

    coefficient = 0
    for digit in digits:
        coefficient = coefficient * 10 + digit
    if sign:
        coefficient = -coefficient
    return coefficient, exponent, len(digits)


def _finalize(coefficient: int, exponent: int) -> Decimal:
    """Build the exact `Decimal` for `coefficient * 10 ** exponent`,
    normalizing away insignificant trailing zero digits first (handoff
    §3.2) — so an unnormalized coefficient's padded exponent never trips the
    native-range check below for a value that is representable once trimmed
    — then preflighting the *normalized* result against Decimal's true
    native representable range (see module docstring) rather than a fixed
    cap this module invents. Digits are read back via `Decimal(coefficient)`
    (exact, and unlike `str(coefficient)` not subject to
    `sys.get_int_max_str_digits()`), never through string parsing."""
    if coefficient == 0:
        return Decimal(0)

    try:
        sign, digits, _ = Decimal(coefficient).as_tuple()
    except MemoryError as exc:
        raise _ArithmeticLimit() from exc

    end = len(digits)
    while end > 1 and digits[end - 1] == 0:
        end -= 1
    exponent += len(digits) - end
    digits = digits[:end]

    adjusted_exponent = exponent + len(digits) - 1
    if adjusted_exponent > decimal.MAX_EMAX or exponent < _ABSOLUTE_MIN_EXPONENT:
        raise _ArithmeticLimit()

    try:
        return Decimal((sign, digits, exponent))
    except MemoryError as exc:
        raise _ArithmeticLimit() from exc


def _exact_add(a: Decimal, b: Decimal, *, _budget: int = _ARITHMETIC_WORK_BUDGET) -> Decimal:
    """Exact `a + b` via aligned big-integer coefficients. A zero operand,
    or an operand that exactly cancels the other (`a == b.copy_negate()`,
    at any differing exponent), short-circuits before any alignment span is
    even computed. Otherwise the alignment span each operand's `10 **
    shift` scaling would need is preflighted against `_budget` (handoff
    §3.2) — sized from the operands' own normalized digit counts, not a
    padded estimate — before that scaling is attempted; a result that
    carries one digit beyond a budget-sized span is not preflighted away
    (`_finalize` alone governs native representability)."""
    if b == 0:
        return a
    if a == 0:
        return b
    if a == b.copy_negate():
        return Decimal(0)

    a_coefficient, a_exponent, a_digits = _normalized_coefficient_exponent(a)
    b_coefficient, b_exponent, b_digits = _normalized_coefficient_exponent(b)
    exponent = min(a_exponent, b_exponent)
    a_shift = a_exponent - exponent
    b_shift = b_exponent - exponent

    required_span = max(a_digits + a_shift, b_digits + b_shift)
    if required_span > _budget:
        raise _ArithmeticLimit()

    try:
        coefficient = a_coefficient * 10 ** a_shift + b_coefficient * 10 ** b_shift
    except MemoryError as exc:
        raise _ArithmeticLimit() from exc

    return _finalize(coefficient, exponent)


def _exact_subtract(a: Decimal, b: Decimal, *, _budget: int = _ARITHMETIC_WORK_BUDGET) -> Decimal:
    """Exact `a - b`. Exact-equality cancellation (`a == b`, at any
    differing exponent) shortcuts to zero before any alignment sizing —
    covering the case an upfront `+2`-padded estimate would otherwise price
    as real work. Otherwise delegates to `_exact_add`; `copy_negate` is a
    sign-flip only — the decimal module documents it as unaffected by
    context, so it never rounds regardless of `b`'s magnitude."""
    if a == b:
        return Decimal(0)
    return _exact_add(a, b.copy_negate(), _budget=_budget)


def _exact_multiply(*factors: Decimal) -> Decimal:
    """Exact product of two or more Decimals via big-integer coefficients
    and summed exponents — multiplication needs no alignment, so this is
    cheap regardless of any factor's magnitude. Any zero factor
    short-circuits to exact zero."""
    if any(factor == 0 for factor in factors):
        return Decimal(0)

    coefficient = 1
    exponent = 0
    try:
        for factor in factors:
            factor_coefficient, factor_exponent, _ = _normalized_coefficient_exponent(factor)
            coefficient *= factor_coefficient
            exponent += factor_exponent
    except MemoryError as exc:
        raise _ArithmeticLimit() from exc

    return _finalize(coefficient, exponent)


def _exact_arithmetic(facts: FundingFacts):
    """Compute the five arithmetic witnesses exactly via big-integer
    coefficient arithmetic (`_exact_add`/`_exact_subtract`/`_exact_multiply`)
    — never a `decimal.Context`-bounded operation. Raises `_ArithmeticLimit`
    — caught only by `assess_funding` — if any step's exact result is not
    representable or not safely materializable.
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
