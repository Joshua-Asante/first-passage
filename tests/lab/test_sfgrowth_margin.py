"""Synthetic F9 accounting cases; no exports or portfolio scoring."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from itertools import permutations

import pytest

from research_utils.sfgrowth_margin import MarginFill, check_concurrent_margin


T = datetime(2026, 1, 5, tzinfo=timezone.utc)


def fill(identity, tranche, hour, kind, quantity):
    return MarginFill(identity, tranche, T + timedelta(hours=hour), kind, quantity)


def check(legs, limit=100, margins=None, expected=None):
    return check_concurrent_margin(
        legs,
        initial_margin_by_leg=margins if margins is not None else dict.fromkeys(legs, 10),
        equity_limit=limit,
        expected_fill_ids_by_leg=(
            expected if expected is not None
            else {leg: tuple(f.fill_id for f in rows) for leg, rows in legs.items()}
        ),
    )


def closed(tranche, start, end, quantity):
    return [fill(tranche + ':in', tranche, start, 'entry', quantity),
            fill(tranche + ':out', tranche, end, 'exit', quantity)]


def test_overlapping_adds_two_legs():
    legs = {'a': closed('base', 0, 4, 3) + closed('add', 1, 3, 2),
            'b': closed('base', 0, 4, 4) + closed('add', 2, 3, 1)}
    result = check(legs, limit=149, margins={'a': 10, 'b': 20})
    assert result.status == 'EXCLUDED'
    assert result.peak_quantity_by_leg == {'a': 5, 'b': 5}
    assert result.required_margin == 150


def test_separate_peaks_still_sum_across_legs():
    result = check({'a': closed('a', 0, 1, 3), 'b': closed('b', 2, 3, 4)})
    assert result.required_margin == 70


def test_separated_tranches_do_not_sum_within_leg():
    result = check({'a': closed('a', 0, 1, 3) + closed('b', 2, 3, 4)})
    assert result.peak_quantity_by_leg == {'a': 4}


@pytest.mark.parametrize('rows', list(permutations(
    closed('base', 0, 1, 3) + closed('add', 1, 1, 2))))
def test_tied_exit_entry_and_zero_duration_are_order_independent(rows):
    result = check({'a': rows})
    assert result.status == 'PASS'
    assert result.peak_quantity_by_leg == {'a': 5}


def test_partial_exits_only_release_matched_tranche():
    rows = [fill('in', 'base', 0, 'entry', 5), fill('partial', 'base', 1, 'exit', 2),
            *closed('add', 2, 3, 4), fill('rest', 'base', 4, 'exit', 3)]
    assert check({'a': rows}).peak_quantity_by_leg == {'a': 7}


@pytest.mark.parametrize('missing', ['entry', 'exit', 'both'])
def test_missing_fill_is_void_even_if_remaining_book_balances(missing):
    rows = closed('base', 0, 2, 3)
    kept = [] if missing == 'both' else [f for f in rows if f.kind != missing]
    result = check({'a': kept}, expected={'a': ('base:in', 'base:out')})
    assert result.status == 'VOID'
    assert result.required_margin is None
    assert result.peak_quantity_by_leg is None
    assert result.reason


@pytest.mark.parametrize('quantity', [-1, float('nan'), float('inf'), 0, 1.5, True, None, '2'])
def test_invalid_quantities_are_void(quantity):
    assert check({'a': closed('base', 0, 1, quantity)}).status == 'VOID'


@pytest.mark.parametrize(('limit', 'status'), [('49.99', 'EXCLUDED'), ('50', 'PASS'), ('50.01', 'PASS')])
def test_margin_threshold_is_strict(limit, status):
    assert check({'a': closed('base', 0, 1, 5)}, limit=Decimal(limit)).status == status


def test_decimal_margin_has_no_rounding_slack():
    result = check({'a': closed('base', 0, 1, 3)}, limit=Decimal('0.2999999999999999999999999999'),
                   margins={'a': Decimal('0.1')})
    assert result.status == 'EXCLUDED'


@pytest.mark.parametrize('timestamp', [None, '2026-01-05', T.replace(tzinfo=None)])
def test_missing_or_invalid_timestamp_is_void(timestamp):
    rows = closed('base', 0, 1, 2)
    rows[0] = replace(rows[0], timestamp=timestamp)
    assert check({'a': rows}).status == 'VOID'


def test_equivalent_timezones_tie():
    rows = closed('a', 0, 1, 2) + closed('b', 1, 2, 3)
    rows[2] = replace(rows[2], timestamp=rows[2].timestamp.astimezone(timezone(timedelta(hours=-5))))
    assert check({'a': rows}).peak_quantity_by_leg == {'a': 5}


@pytest.mark.parametrize('rows', [
    closed('a', 2, 1, 2),
    [fill('in', 'a', 0, 'entry', 2), fill('out', 'b', 1, 'exit', 2)],
    [fill('in', 'a', 0, 'entry', 2), fill('out', 'a', 1, 'exit', 3)],
    [fill('in', 'a', 0, 'entry', 2), fill('out', 'a', 1, 'exit', 1)],
    [fill('in', 'a', 0, 'entry', 2)],
    closed('a', 0, 1, 2) + closed('a', 2, 3, 2),
    [fill('in', 'a', 0, 'buy', 2), fill('out', 'a', 1, 'exit', 2)],
])
def test_unresolvable_accounting_is_void(rows):
    assert check({'a': rows}).status == 'VOID'


@pytest.mark.parametrize('margins', [{}, {'a': -1}, {'a': float('nan')}, {'a': 0}, {'a': True}, {'a': 10, 'b': 10}])
def test_invalid_or_incomplete_margin_is_void(margins):
    assert check({'a': closed('base', 0, 1, 2)}, margins=margins).status == 'VOID'


@pytest.mark.parametrize('limit', [None, 0, -1, float('nan'), float('inf'), True])
def test_invalid_equity_limit_is_void(limit):
    assert check({'a': closed('base', 0, 1, 2)}, limit=limit).status == 'VOID'


def test_explicit_empty_nonbaseline_leg_can_contribute_zero():
    result = check({'a': [], 'b': closed('b', 0, 1, 2)})
    assert result.peak_quantity_by_leg == {'a': 0, 'b': 2}


@pytest.mark.parametrize('expected', [{}, {'a': ('base:in',)}, {'a': ('base:in', 'base:out', 'base:out')}])
def test_incomplete_or_duplicate_inventory_is_void(expected):
    assert check({'a': closed('base', 0, 1, 2)}, expected=expected).status == 'VOID'


def test_invalid_leg_container_is_void():
    assert check_concurrent_margin({'a': None}, initial_margin_by_leg={'a': 10},
                                   equity_limit=100, expected_fill_ids_by_leg={'a': ()}).status == 'VOID'


def test_invalid_accounting_overrides_margin_exclusion():
    assert check({'a': closed('a', 0, 1, 100), 'b': closed('b', 2, 1, 1)}).status == 'VOID'
