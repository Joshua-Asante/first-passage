"""Retained cost bytes must be valid before becoming replay commissions."""
import json
from pathlib import Path

import pytest

import composition_fixture
from c1_rail.qualification.production_source import _cost_terms


def _schedule():
    path = Path(__file__).resolve().parents[3] / 'lab/analysis/c1/tradeify_seven_strategy_phase1_2026-09/tradeify_commission_schedule.json'
    return json.loads(path.read_bytes())


def _parse(payload):
    raw = payload if isinstance(payload, bytes) else composition_fixture.encoded(payload)
    return _cost_terms(raw)


def _build(tmp_path, monkeypatch, payload):
    # Replace the artifact before real domain/contract signing; all production
    # loading, schema parsing and instrument construction remain real.
    original = composition_fixture.build_artifacts
    def artifacts(root):
        fixture = original(root)
        raw = payload if isinstance(payload, bytes) else composition_fixture.encoded(payload)
        fixture.payloads['cost_model'] = raw
        (root / fixture.paths['cost_model']).write_bytes(raw)
        return fixture
    monkeypatch.setattr(composition_fixture, 'build_artifacts', artifacts)
    return composition_fixture.build_verified_composition(tmp_path).source


@pytest.mark.parametrize('amount', [True, False, 1, 1.82, None, [], {}, '', 'invalid', 'NaN', 'sNaN', 'Infinity', '-0.01', '1e9999999999999999999', '1e-9999'])
def test_cost_amount_must_be_explicit_finite_nonnegative_representable_decimal(amount):
    """Coercion or float underflow must never manufacture a cheaper commission."""
    payload = _schedule()
    payload['rows'][0]['round_trip_usd'] = amount
    with pytest.raises(ValueError):
        _parse(payload)


@pytest.mark.parametrize('replacement', [None, [], True, 'rows'])
def test_cost_document_requires_an_object(replacement):
    with pytest.raises(ValueError):
        _parse(replacement)


@pytest.mark.parametrize('field', ['source_url', 'page_date', 'observed_date', 'totals_include', 'rows'])
def test_cost_document_requires_all_capture_fields(field):
    payload = _schedule()
    del payload[field]
    with pytest.raises(ValueError):
        _parse(payload)


@pytest.mark.parametrize('field,value', [
    ('unexpected', 1), ('schema', 'other/v1'), ('source_url', None),
    ('page_date', 'not-a-date'), ('observed_date', True),
    ('totals_include', 'commission only'), ('rows', {}), ('rows', None),
])
def test_cost_capture_rejects_unknown_fields_and_unsupported_metadata(field, value):
    payload = _schedule()
    payload[field] = value
    with pytest.raises(ValueError):
        _parse(payload)


@pytest.mark.parametrize('row', [None, [], True, {}, {'symbol': '6J'},
    {'symbol': '6J', 'round_trip_usd': '6.20', 'per_side_usd': '0'},
    {'symbol': [], 'round_trip_usd': '6.20'},
    {'symbol': 'UNKNOWN', 'round_trip_usd': '6.20'}])
def test_cost_rows_require_closed_shape_and_supported_symbols(row):
    payload = _schedule()
    payload['rows'][0] = row
    with pytest.raises(ValueError):
        _parse(payload)


@pytest.mark.parametrize('operation', ['missing', 'duplicate', 'extra'])
def test_cost_rows_require_each_symbol_exactly_once(operation):
    payload = _schedule()
    if operation == 'missing':
        payload['rows'].pop()
    elif operation == 'duplicate':
        payload['rows'][1] = payload['rows'][0].copy()
    else:
        payload['rows'].append(payload['rows'][0].copy())
    with pytest.raises(ValueError):
        _parse(payload)


def test_cost_duplicate_json_fields_fail_before_replay():
    raw = composition_fixture.encoded(_schedule()).replace(b'"round_trip_usd":"6.20"', b'"round_trip_usd":"6.20","round_trip_usd":"0"')
    with pytest.raises(ValueError):
        _parse(raw)


def test_valid_cost_capture_derives_per_side_commissions(tmp_path, monkeypatch):
    source = _build(tmp_path, monkeypatch, _schedule())
    assert {leg: instrument.commission_per_side for leg, instrument in source._instruments} == {
        'aegis_6j': 3.10, 'orb_mnq_v7': .91, 'dj30_mym_p250': .91, 'vanguard_mgc': 1.06,
    }


def test_signed_source_rejects_boolean_cost_before_replay(tmp_path, monkeypatch):
    payload = _schedule()
    payload['rows'][0]['round_trip_usd'] = True
    with pytest.raises(ValueError):
        _build(tmp_path, monkeypatch, payload)


def test_cost_zero_and_subcent_precision_preserve_existing_qualification_semantics():
    payload = _schedule()
    payload['rows'][0]['round_trip_usd'] = '0'
    payload['rows'][1]['round_trip_usd'] = '1.823'
    costs = _parse(payload)
    assert costs['6J'] == 0
    assert costs['MNQ'] == .9115
