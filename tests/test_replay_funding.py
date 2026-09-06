"""Independent synthetic tests for lab/replay_funding.py.

Every expected value here is written from the handoff's frozen contract
(docs/briefs/handoffs/2026-09-05-claude-funding-evidence.md §4), computed by
hand or with a standalone decimal snippet — never by calling
`assess_funding` and asserting it against itself. All facts are invented;
none of this touches a real account, capture or campaign export.
"""

import dataclasses
import decimal
import sys
from decimal import Decimal
from fractions import Fraction

import pytest

from replay_funding import (
    _ABSOLUTE_MIN_EXPONENT,
    _ArithmeticLimit,
    _exact_add,
    _exact_subtract,
    _finalize,
    FundingAssessment,
    FundingFacts,
    FundingReason,
    FundingStatus,
    assess_funding,
)


def _facts(**overrides) -> FundingFacts:
    """Base invented fixture from the handoff's falsifier table §4, with overrides."""
    fields = dict(
        cash_before=Decimal("1000"),
        point_value=Decimal("5"),
        execution_price=Decimal("100"),
        current_mark=Decimal("99"),
        execution_cost=Decimal("3"),
        margin_ratio=Decimal("1"),
        requested_quantity=1,
        open_quantity=0,
        competing_entry_count=0,
        direction="LONG",
        known_state=True,
        execution_price_established=True,
    )
    fields.update(overrides)
    return FundingFacts(**fields)


# ---------------------------------------------------------------------------
# §4 falsifier table: base case + arithmetic witnesses
# ---------------------------------------------------------------------------


def test_base_case_positive_cushion():
    result = assess_funding(_facts())
    assert result.status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert result.reason == FundingReason.POSITIVE_CUSHION
    assert result.cash_after_cost == Decimal("997")
    assert result.funding_basis == Decimal("100")
    assert result.required_at_basis == Decimal("500")
    assert result.surplus == Decimal("497")
    assert result.post_fill_margin_cushion == Decimal("497")


def test_mark_above_execution_price_moves_surplus_not_cushion():
    """Distinguishes the mark-based conservative surplus from the post-fill cushion:
    raising the mark above the execution price worsens the surplus (funding_basis
    tracks the mark) but the post-fill cushion is anchored to execution_price only."""
    result = assess_funding(_facts(current_mark=Decimal("101")))
    assert result.funding_basis == Decimal("101")
    assert result.required_at_basis == Decimal("505")
    assert result.surplus == Decimal("492")
    assert result.post_fill_margin_cushion == Decimal("497")
    assert result.status == FundingStatus.PROVEN_POSITIVE_CUSHION


@pytest.mark.parametrize(
    "cash_before, expected_status, expected_reason, expected_surplus",
    [
        (Decimal("503"), FundingStatus.OUTSIDE_PROVEN_DOMAIN, FundingReason.NON_POSITIVE_CUSHION, Decimal("0")),
        (Decimal("503.01"), FundingStatus.PROVEN_POSITIVE_CUSHION, FundingReason.POSITIVE_CUSHION, Decimal("0.01")),
        (Decimal("502.99"), FundingStatus.OUTSIDE_PROVEN_DOMAIN, FundingReason.NON_POSITIVE_CUSHION, Decimal("-0.01")),
    ],
)
def test_zero_surplus_boundary(cash_before, expected_status, expected_reason, expected_surplus):
    """Frozen §4 boundary case: only cash and mark move; point value stays 5
    and execution cost stays 3 (the base fixture), so the execution-cost
    deduction is what brings cash from 503 to the 500 required-at-basis."""
    facts = _facts(
        cash_before=cash_before,
        current_mark=Decimal("100"),
    )
    result = assess_funding(facts)
    assert result.status == expected_status
    assert result.reason == expected_reason
    assert result.surplus == expected_surplus
    # A zero/negative surplus still retains its arithmetic witnesses.
    assert result.required_at_basis == Decimal("500")


def test_later_candidate_price_gap_does_not_mutate_prior_result():
    """A submission-time witness cannot authorize a later fill after a price
    gap; the caller must establish fresh facts, and the prior result stays put."""
    prior = assess_funding(_facts())
    assert prior.surplus == Decimal("497")

    later = assess_funding(_facts(execution_price=Decimal("201"), current_mark=Decimal("201")))
    assert later.status == FundingStatus.OUTSIDE_PROVEN_DOMAIN
    assert later.reason == FundingReason.NON_POSITIVE_CUSHION
    assert later.required_at_basis == Decimal("1005")
    assert later.surplus == Decimal("-8")

    # The earlier, already-returned assessment is untouched by the later call.
    assert prior.surplus == Decimal("497")
    assert prior.status == FundingStatus.PROVEN_POSITIVE_CUSHION


def test_cost_change_requires_new_assessment():
    zero_cost = assess_funding(_facts(execution_cost=Decimal("0")))
    assert zero_cost.surplus == Decimal("500")

    with_cost = assess_funding(_facts(execution_cost=Decimal("4")))
    assert with_cost.surplus == Decimal("496")


# ---------------------------------------------------------------------------
# §3 precedence: each domain miss in isolation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "overrides, expected_reason",
    [
        ({"known_state": False}, FundingReason.UNKNOWN_STATE),
        ({"execution_price_established": False}, FundingReason.UNESTABLISHED_EXECUTION_PRICE),
        ({"direction": "SHORT"}, FundingReason.UNSUPPORTED_SIDE_MARGIN_QUANTITY),
        ({"margin_ratio": Decimal("0.5")}, FundingReason.UNSUPPORTED_SIDE_MARGIN_QUANTITY),
        ({"requested_quantity": 0}, FundingReason.UNSUPPORTED_SIDE_MARGIN_QUANTITY),
        ({"requested_quantity": 2}, FundingReason.UNSUPPORTED_SIDE_MARGIN_QUANTITY),
        ({"open_quantity": 1}, FundingReason.EXISTING_POSITION),
        ({"competing_entry_count": 1}, FundingReason.COMPETING_ENTRY),
    ],
)
def test_each_domain_miss_in_isolation(overrides, expected_reason):
    result = assess_funding(_facts(**overrides))
    assert result.status == FundingStatus.OUTSIDE_PROVEN_DOMAIN
    assert result.reason == expected_reason
    assert result.surplus is None
    assert result.cash_after_cost is None
    assert result.funding_basis is None
    assert result.required_at_basis is None
    assert result.post_fill_margin_cushion is None


@pytest.mark.parametrize(
    "overrides, expected_reason",
    [
        (
            {"known_state": False, "execution_price_established": False},
            FundingReason.UNKNOWN_STATE,
        ),
        (
            {"execution_price_established": False, "direction": "SHORT"},
            FundingReason.UNESTABLISHED_EXECUTION_PRICE,
        ),
        (
            {"direction": "SHORT", "open_quantity": 1},
            FundingReason.UNSUPPORTED_SIDE_MARGIN_QUANTITY,
        ),
        (
            {"open_quantity": 1, "competing_entry_count": 1},
            FundingReason.EXISTING_POSITION,
        ),
    ],
)
def test_reason_precedence_stable_order(overrides, expected_reason):
    result = assess_funding(_facts(**overrides))
    assert result.status == FundingStatus.OUTSIDE_PROVEN_DOMAIN
    assert result.reason == expected_reason


# ---------------------------------------------------------------------------
# §2 invalid input: rejected before any positive proof
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "overrides",
    [
        {"execution_price": Decimal("NaN")},
        {"execution_price": Decimal("Infinity")},
        {"cash_before": Decimal("NaN")},
        {"current_mark": Decimal("-Infinity")},
        {"cash_before": 1000},  # int, not Decimal
        {"execution_price": 100.0},  # float, not Decimal
        {"point_value": "5"},  # str, not Decimal
        {"execution_price": Decimal("-100")},  # prices must be positive
        {"point_value": Decimal("0")},  # point value must be positive, not just nonnegative
        {"current_mark": Decimal("0")},
        {"execution_cost": Decimal("-1")},  # cost must be nonnegative
        {"margin_ratio": Decimal("-1")},  # margin ratio must be nonnegative
        {"requested_quantity": 1.0},  # float count
        {"requested_quantity": True},  # bool count
        {"requested_quantity": Fraction(1, 1)},  # fraction count
        {"open_quantity": -1},  # negative count
        {"competing_entry_count": -1},
        {"known_state": 1},  # truthy int, not bool
        {"execution_price_established": "true"},  # string, not bool
        {"direction": 123},  # non-string direction
    ],
)
def test_invalid_input_rejected(overrides):
    result = assess_funding(_facts(**overrides))
    assert result.status == FundingStatus.INVALID_INPUT
    assert result.reason == FundingReason.INVALID_INPUT
    assert result.surplus is None
    assert result.cash_after_cost is None
    assert result.funding_basis is None
    assert result.required_at_basis is None
    assert result.post_fill_margin_cushion is None


@pytest.mark.parametrize(
    "bad_facts",
    [
        None,
        "not a facts object",
        {"cash_before": Decimal("1000")},
        object(),
        42,
    ],
)
def test_wrong_facts_object_type_is_invalid(bad_facts):
    result = assess_funding(bad_facts)
    assert result.status == FundingStatus.INVALID_INPUT
    assert result.reason == FundingReason.INVALID_INPUT


# ---------------------------------------------------------------------------
# §3 immutability and Decimal-context independence
# ---------------------------------------------------------------------------


def test_repeated_calls_are_identical():
    facts = _facts()
    first = assess_funding(facts)
    second = assess_funding(facts)
    assert first == second


def test_facts_and_assessment_are_frozen():
    facts = _facts()
    result = assess_funding(facts)
    with pytest.raises(dataclasses.FrozenInstanceError):
        facts.cash_before = Decimal("0")  # type: ignore[misc]
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.surplus = Decimal("0")  # type: ignore[misc]


def test_context_independence_with_long_decimal_coefficients():
    """Expected witnesses below are hand-computed from the frozen formula
    (§3), independent of the implementation:

    cash_after_cost = 1000.000000000000000000000001 - 3.000000000000000000000002
                     = 996.999999999999999999999999
    funding_basis   = max(1, 1) = 1
    required_at_basis = 1 * 5.000000000000000000000003 * 1 = 5.000000000000000000000003
    surplus          = 996.999999999999999999999999 - 5.000000000000000000000003
                     = 991.999999999999999999999996
    post_fill_margin_cushion = 996.999999999999999999999999 - 1 * 5.000000000000000000000003 * 1
                     = 991.999999999999999999999996 (execution_price == funding_basis == 1 here)
    """
    facts = _facts(
        cash_before=Decimal("1000.000000000000000000000001"),
        point_value=Decimal("5.000000000000000000000003"),
        execution_price=Decimal("1"),
        current_mark=Decimal("1"),
        execution_cost=Decimal("3.000000000000000000000002"),
    )

    with decimal.localcontext() as ctx:
        ctx.prec = 2
        ctx.rounding = decimal.ROUND_DOWN
        low_precision_result = assess_funding(facts)

    with decimal.localcontext() as ctx:
        ctx.prec = 100
        ctx.rounding = decimal.ROUND_CEILING
        high_precision_result = assess_funding(facts)

    assert low_precision_result == high_precision_result
    assert low_precision_result.status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert low_precision_result.cash_after_cost == Decimal("996.999999999999999999999999")
    assert low_precision_result.funding_basis == Decimal("1")
    assert low_precision_result.required_at_basis == Decimal("5.000000000000000000000003")
    assert low_precision_result.surplus == Decimal("991.999999999999999999999996")
    assert low_precision_result.post_fill_margin_cushion == Decimal("991.999999999999999999999996")


def test_precision_beyond_a_fixed_cap_is_not_rounded_away():
    """Regression for a fixed-precision cap silently rounding a valid result:
    with cost 0 and point value/price/mark all 1, cash_before is 1 plus a
    surplus of exactly 1E-201 (a 1 after 200 zero fractional digits). Any
    context precision capped below ~202 significant digits rounds this
    surplus to zero; the helper must not impose such a cap.
    """
    cash_before = Decimal("1." + "0" * 200 + "1")
    facts = _facts(
        cash_before=cash_before,
        point_value=Decimal("1"),
        execution_price=Decimal("1"),
        current_mark=Decimal("1"),
        execution_cost=Decimal("0"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert result.reason == FundingReason.POSITIVE_CUSHION
    assert result.cash_after_cost == cash_before
    assert result.required_at_basis == Decimal("1")
    assert result.surplus == Decimal("1E-201")
    assert result.post_fill_margin_cushion == Decimal("1E-201")


def test_large_exponent_compact_operands_do_not_overflow():
    """Regression for a `decimal.Overflow` on a large-but-finite input: a
    fixed-`prec` context built without also widening `Emax`/`Emin` keeps a
    small default exponent bound, which a large operand exponent exceeds
    during arithmetic. Unlike the earlier version of this regression, every
    operand and every expected witness here is compact (coefficient "1" or
    "2") at a shared large exponent, so the expected values are written as
    literal Decimals — no million-digit-coefficient `Decimal(10**N)`
    conversion, which is itself slow independent of the helper under test.
    """
    facts = _facts(
        cash_before=Decimal("2E10000000"),
        point_value=Decimal("1"),
        execution_price=Decimal("1E10000000"),
        current_mark=Decimal("1E10000000"),
        execution_cost=Decimal("0"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert result.reason == FundingReason.POSITIVE_CUSHION
    assert result.cash_after_cost == Decimal("2E10000000")
    assert result.funding_basis == Decimal("1E10000000")
    assert result.required_at_basis == Decimal("1E10000000")
    assert result.surplus == Decimal("1E10000000")
    assert result.post_fill_margin_cushion == Decimal("1E10000000")


def test_compact_huge_exponent_zero_surplus_does_not_allocate_excessively():
    """Required regression (handoff §3.1 item 1): cash/price/mark all
    `1E1000000000000` with cost 0 and point value 1 is a compact input whose
    exact surplus is exactly zero. A naive implementation that realigns a
    zero-cost subtraction to a common exponent, or that allocates a fixed
    huge precision regardless of the operands, either materializes a
    trillion-digit coefficient (`MemoryError`/multi-minute hang) or fails
    outright; the operand-derived sizing here needs only a handful of digits
    because every operand shares the same exponent.
    """
    huge = Decimal("1E1000000000000")
    facts = _facts(
        cash_before=huge,
        point_value=Decimal("1"),
        execution_price=huge,
        current_mark=huge,
        execution_cost=Decimal("0"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.OUTSIDE_PROVEN_DOMAIN
    assert result.reason == FundingReason.NON_POSITIVE_CUSHION
    assert result.cash_after_cost == huge
    assert result.funding_basis == huge
    assert result.required_at_basis == huge
    assert result.surplus == Decimal("0")
    assert result.post_fill_margin_cushion == Decimal("0")


def test_beyond_native_product_range_returns_arithmetic_limit():
    """Required regression (handoff §3.1 item 2): the review's counter-example
    where every operand is individually representable and validation/domain
    checks all pass, but `point_value * funding_basis` has an adjusted
    exponent (~1.2E18) beyond Decimal's native `MAX_EMAX` (~1E18 on this
    platform). This is a defined non-proof outcome — `ARITHMETIC_LIMIT` with
    no witnesses — not a `decimal.Overflow` crash and not a rounded
    substitute.
    """
    exponent = "600000000000000000"
    facts = _facts(
        cash_before=Decimal(f"3E{exponent}"),
        execution_cost=Decimal(f"1E{exponent}"),
        point_value=Decimal(f"1E{exponent}"),
        execution_price=Decimal(f"1E{exponent}"),
        current_mark=Decimal(f"1E{exponent}"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.OUTSIDE_PROVEN_DOMAIN
    assert result.reason == FundingReason.ARITHMETIC_LIMIT
    assert result.cash_after_cost is None
    assert result.funding_basis is None
    assert result.required_at_basis is None
    assert result.surplus is None
    assert result.post_fill_margin_cushion is None


def test_subnormal_result_below_min_emin_is_not_falsely_rejected():
    """Required regression (review finding 1, head 7e82324): `point_value`'s
    own exponent sits well below `decimal.MIN_EMIN` — a genuine subnormal
    magnitude, not a normal-range value — but multiplied by a large
    `execution_price` the exact product's exponent lands comfortably inside
    the representable range. A design that checks (or rounds) an
    intermediate `quantity * point_value` step against a bound that isn't
    itself low enough would reject this even though the real product is
    fine; this module's exact big-integer multiply sums exponents directly
    with no intermediate step and no such bound at all.
    """
    point_value_exponent = decimal.MIN_EMIN - 10
    price_exponent = 15
    product_exponent = point_value_exponent + price_exponent  # decimal.MIN_EMIN + 5

    facts = _facts(
        cash_before=Decimal(f"2E{product_exponent}"),
        point_value=Decimal(f"1E{point_value_exponent}"),
        execution_price=Decimal(f"1E{price_exponent}"),
        current_mark=Decimal(f"1E{price_exponent}"),
        execution_cost=Decimal("0"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert result.reason == FundingReason.POSITIVE_CUSHION
    assert result.cash_after_cost == Decimal(f"2E{product_exponent}")
    assert result.required_at_basis == Decimal(f"1E{product_exponent}")
    assert result.surplus == Decimal(f"1E{product_exponent}")
    assert result.post_fill_margin_cushion == Decimal(f"1E{product_exponent}")


def test_identity_product_and_subtraction_at_max_emax_are_exact():
    """Required regression (review finding 2, head 7e82324): cash, price and
    mark all sit at `decimal.MAX_EMAX` itself — the true native exponent
    ceiling, not one below it — with an identity point_value/quantity. Both
    `point_value * funding_basis` and the final subtraction land exactly at
    the ceiling (adjusted exponent == MAX_EMAX) and are representable
    exactly. A preflight that adds speculative headroom (e.g. "+2" for a
    possible carry digit that a compact identity computation never
    produces) would reject this even though nothing overflows.
    """
    exponent = decimal.MAX_EMAX
    facts = _facts(
        cash_before=Decimal(f"2E{exponent}"),
        execution_cost=Decimal("0"),
        point_value=Decimal("1"),
        execution_price=Decimal(f"1E{exponent}"),
        current_mark=Decimal(f"1E{exponent}"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert result.reason == FundingReason.POSITIVE_CUSHION
    assert result.cash_after_cost == Decimal(f"2E{exponent}")
    assert result.funding_basis == Decimal(f"1E{exponent}")
    assert result.required_at_basis == Decimal(f"1E{exponent}")
    assert result.surplus == Decimal(f"1E{exponent}")
    assert result.post_fill_margin_cushion == Decimal(f"1E{exponent}")


def test_large_digit_count_identity_factors_are_not_overcounted():
    """Required regression (review finding 4, head 7e82324): quantity and
    execution_price/current_mark are identity (1), and point_value is a
    3,000-digit repunit matched by a same-width cash_before (its exact
    double — doubling an all-ones number never carries, since each digit is
    1*2=2), so every exact witness has at most 3,000 coefficient digits. A
    design that preflights precision from the SUM of every factor's own
    digit count (1 + 3000 + 1 = 3,002, inflated further by the identity
    factors that contribute nothing to the real result) instead of the
    actual product's digit count risks rejecting this even though the true
    result never grows past the widest operand. 3,000 digits is chosen to
    stay comfortably under Python's own default int-to-str conversion limit
    (see `test_arithmetic_is_independent_of_int_str_digit_limit_setting`
    below for that distinct, genuine boundary, which this module no longer
    depends on at all) so this test isolates the counting bug only.
    """
    point_value = Decimal("1" * 3000)
    cash_before = Decimal("2" * 3000)  # exactly 2 * point_value, digit-wise

    facts = _facts(
        cash_before=cash_before,
        point_value=point_value,
        execution_price=Decimal("1"),
        current_mark=Decimal("1"),
        execution_cost=Decimal("0"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert result.reason == FundingReason.POSITIVE_CUSHION
    assert result.required_at_basis == point_value
    assert result.surplus == point_value


def test_arithmetic_is_independent_of_int_str_digit_limit_setting():
    """Required correction (review finding 1, head 93b2754): this module's
    arithmetic must not read `sys.get_int_max_str_digits()` at all. A
    5,000-digit exact witness — comfortably past the interpreter's own
    default (4,300) and past the minimum allowed non-zero setting (640) —
    must return the identical result whether that setting is disabled (0),
    restricted to its minimum, or left at whatever it currently is. The
    setting is saved and restored around the assertions; this module itself
    never calls `sys.set_int_max_str_digits`.
    """
    point_value = Decimal("1" * 5000)
    cash_before = Decimal("2" * 5000)  # exactly 2 * point_value, digit-wise
    facts = _facts(
        cash_before=cash_before,
        point_value=point_value,
        execution_price=Decimal("1"),
        current_mark=Decimal("1"),
        execution_cost=Decimal("0"),
    )

    saved_limit = sys.get_int_max_str_digits()
    try:
        results = []
        for limit in (0, 640, saved_limit):
            sys.set_int_max_str_digits(limit)
            results.append(assess_funding(facts))
    finally:
        sys.set_int_max_str_digits(saved_limit)

    assert all(result == results[0] for result in results)
    assert results[0].status == FundingStatus.PROVEN_POSITIVE_CUSHION
    assert results[0].reason == FundingReason.POSITIVE_CUSHION
    assert results[0].required_at_basis == point_value
    assert results[0].surplus == point_value


def test_alignment_span_beyond_default_budget_returns_arithmetic_limit():
    """Required correction (review finding 3, head 93b2754): a nonzero cost
    against a compact cash value at an astronomically large exponent needs
    an aligned span far beyond the 1,000,000-digit default work budget
    (handoff §3.2). This must be rejected via the cheap pre-multiply span
    check — never by attempting to construct `10 ** shift` first, which is
    what the prior head reached for before any string-guard check fired
    when that guard's setting was 0.
    """
    facts = _facts(
        cash_before=Decimal("1E1000000000000"),
        execution_cost=Decimal("1"),
        point_value=Decimal("1"),
        execution_price=Decimal("1"),
        current_mark=Decimal("1"),
    )
    result = assess_funding(facts)
    assert result.status == FundingStatus.OUTSIDE_PROVEN_DOMAIN
    assert result.reason == FundingReason.ARITHMETIC_LIMIT
    assert result.cash_after_cost is None
    assert result.surplus is None


def test_normalization_at_absolute_min_exponent_boundary():
    """Required correction (review finding 2, head 93b2754): a product whose
    *unnormalized* exponent sits one position below the absolute
    representable floor, but whose exact value — after trimming an
    insignificant trailing zero — lands exactly on that floor, must be
    accepted. Reproduces the review's own compact literal counter-example
    (point_value 5E<floor>, price/mark .2, cash 2E<floor>, cost 0: product
    10E<floor-1>, representable exactly as 1E<floor>) directly against
    `_finalize`.
    """
    floor = _ABSOLUTE_MIN_EXPONENT
    result = _finalize(10, floor - 1)
    assert result == Decimal(f"1E{floor}")


def test_normalization_below_absolute_min_exponent_still_rejected():
    """The same coefficient one digit-position further out — no trailing
    zero available to trim away — is genuinely below the representable
    floor and must still return an arithmetic limit, confirming the fix
    normalizes rather than simply loosening the bound."""
    floor = _ABSOLUTE_MIN_EXPONENT
    with pytest.raises(_ArithmeticLimit):
        _finalize(11, floor - 1)


def test_budget_under_and_at_boundary_succeed_via_injected_budget():
    """§3.2 injected-budget coverage: a span exactly at the budget succeeds,
    as does a span comfortably under it. `999 + 1` has an aligned span of 3
    digits (the wider operand's own digit count; no shift needed since both
    share exponent 0) — a tiny private `_budget` keeps this cheap regardless
    of the real 1,000,000-digit default ('no huge fixtures', handoff §3.2).
    """
    a, b = Decimal("999"), Decimal("1")
    assert _exact_add(a, b, _budget=10) == Decimal("1000")
    assert _exact_add(a, b, _budget=3) == Decimal("1000")


def test_budget_over_boundary_returns_arithmetic_limit():
    """The same pair rejected once the injected budget can no longer hold
    the wider operand's own digit count."""
    with pytest.raises(_ArithmeticLimit):
        _exact_add(Decimal("999"), Decimal("1"), _budget=2)


def test_carry_headroom_is_not_preflighted_away():
    """§3.2: 'do not reject a budget-sized result solely because a
    speculative carry ... adds to an upper estimate.' The aligned span here
    (3 digits) exactly meets the injected budget, and the actual sum carries
    into a 4th digit (999 + 1 = 1000) — this must not be preflighted away by
    a padded estimate."""
    assert _exact_add(Decimal("999"), Decimal("1"), _budget=3) == Decimal("1000")


def test_zero_and_exact_cancellation_shortcuts_ignore_budget_entirely():
    """Zero operands and exact numeric cancellation (`a == b` for subtract,
    `a == -b` for add — at any differing exponent) must short-circuit
    before any alignment span is even computed. Proven here with an
    injected budget of 0, which would reject any real alignment work."""
    assert _exact_add(Decimal("5"), Decimal("0"), _budget=0) == Decimal("5")
    assert _exact_add(Decimal("0"), Decimal("5"), _budget=0) == Decimal("5")
    assert _exact_add(Decimal("5"), Decimal("-5.00"), _budget=0) == Decimal("0")
    assert _exact_subtract(Decimal("5"), Decimal("5.00"), _budget=0) == Decimal("0")
    assert _exact_subtract(Decimal("5.00"), Decimal("5"), _budget=0) == Decimal("0")


def test_module_exports_all_required_symbols():
    assert FundingFacts is not None
    assert FundingAssessment is not None
    required_reasons = {
        "UNKNOWN_STATE",
        "UNESTABLISHED_EXECUTION_PRICE",
        "UNSUPPORTED_SIDE_MARGIN_QUANTITY",
        "EXISTING_POSITION",
        "COMPETING_ENTRY",
        "POSITIVE_CUSHION",
        "NON_POSITIVE_CUSHION",
        "ARITHMETIC_LIMIT",
        "INVALID_INPUT",
    }
    assert {reason.name for reason in FundingReason} == required_reasons
    assert {status.name for status in FundingStatus} == {
        "PROVEN_POSITIVE_CUSHION",
        "OUTSIDE_PROVEN_DOMAIN",
        "INVALID_INPUT",
    }
