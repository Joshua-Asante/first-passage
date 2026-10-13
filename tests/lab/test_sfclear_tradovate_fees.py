"""Card C §§0.5/4: invented fees only; no private capture or real-data run."""
import ast
import copy
import csv
import hashlib
import importlib
import io
import json
from datetime import date
from pathlib import Path

import pytest

from discovery import sfgrowth_acceptance as scoring
from discovery.remc_series_builder import TRADE_LIST_COLUMNS


SYMBOLS = ('6J', 'MYM', 'MGC', 'MNQ')
COMPONENTS = ('commission', 'exchange', 'clearing', 'NFA')
SOURCE = hashlib.sha256(b'invented capture, not venue rates').hexdigest()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def document():
    return dict(schema='sfclear_tradovate_fees/v1', venue='Tradovate', plan='Free',
                unit='USD_per_side_per_contract', captured_utc='2000-01-01T00:00:00Z',
                source_sha256=SOURCE,
                rows=[dict(instrument=symbol, commission=str(i + 8),
                           exchange='2.5', clearing='1.25', NFA='0.25')
                      for i, symbol in enumerate(SYMBOLS)])


def encoded(doc):
    return json.dumps(doc).encode('utf-8')


def parse(doc=None, *, raw=None, **kwargs):
    # Deferred import makes each falsifier visibly red before the module exists.
    module = importlib.import_module('discovery.sfclear_tradovate_fees')
    raw = encoded(document() if doc is None else doc) if raw is None else raw
    return module.parse_snapshot(raw, expected_sha256=kwargs.get('expected_sha256', digest(raw)),
                                 expected_source_sha256=kwargs.get('expected_source_sha256', SOURCE))


@pytest.mark.parametrize('symbol', SYMBOLS)
def test_c1_independent_instrument_rates(symbol):
    doc = document()
    before = parse(doc)
    next(row for row in doc['rows'] if row['instrument'] == symbol)['commission'] = '32'
    after = parse(doc)
    for other in SYMBOLS:
        assert (before.rates_for(other) != after.rates_for(other)) == (other == symbol)
    with pytest.raises(ValueError):
        before.rates_for('MES')


def test_c2_per_side_is_never_halved():
    snapshot = parse()
    for i, symbol in enumerate(SYMBOLS):
        assert snapshot.rates_for(symbol) == dict(commission=float(i + 8), exchange=2.5,
                                                  clearing=1.25, NFA=.25)


@pytest.mark.parametrize('unit', ['USD_round_trip_per_contract', 'USD', None, 1])
def test_c2_other_units_refuse(unit):
    doc = document()
    doc['unit'] = unit
    with pytest.raises(ValueError):
        parse(doc)


def test_c2_round_trip_row_refuses():
    doc = document()
    doc['rows'][0]['unit'] = 'USD_round_trip_per_contract'
    with pytest.raises(ValueError):
        parse(doc)


@pytest.mark.parametrize('component', COMPONENTS)
def test_c3_missing_component_refuses(component):
    doc = document()
    del doc['rows'][0][component]
    with pytest.raises(ValueError):
        parse(doc)


@pytest.mark.parametrize('fault', ['extra_component', 'duplicate', 'missing', 'extra',
                                  'unknown', 'rows_object', 'row_scalar'])
def test_c3_closed_rows_refuse(fault):
    doc = document()
    rows = doc['rows']
    if fault == 'extra_component':
        rows[0]['rebate'] = '0'
    elif fault == 'duplicate':
        rows[-1] = copy.deepcopy(rows[0])
    elif fault == 'missing':
        rows.pop()
    elif fault == 'extra':
        rows.append(dict(rows[0], instrument='MES'))
    elif fault == 'unknown':
        rows[0]['instrument'] = 'MES'
    elif fault == 'rows_object':
        doc['rows'] = {}
    else:
        rows[0] = '6J'
    with pytest.raises(ValueError):
        parse(doc)


@pytest.mark.parametrize('field,value', [
    ('schema', 'v2'), ('venue', 'Tradeify'), ('plan', 'Paid'),
    ('captured_utc', '2026-10-12T12:00:00'), ('captured_utc', 'garbage'),
    ('captured_utc', '2026-10-12'), ('captured_utc', None),
    ('source_sha256', 'z' * 64), ('source_sha256', 'a' * 63),
])
def test_c4_metadata_refuses(field, value):
    doc = document()
    doc[field] = value
    with pytest.raises(ValueError):
        parse(doc)


def test_c4_identity_not_age_and_exact_snapshot_bytes():
    raw = encoded(document())
    snapshot = parse(raw=raw)
    assert snapshot.snapshot_sha256 == digest(raw)
    assert snapshot.captured_utc.year == 2000  # M-C4: frozen capture never expires.
    with pytest.raises(ValueError):
        parse(raw=raw + b' ', expected_sha256=digest(raw))
    doc = document()
    doc['rows'][0]['commission'] = '999'
    with pytest.raises(ValueError):
        parse(doc, expected_sha256=digest(raw))


def test_c5_source_identity_and_lookup_stability():
    with pytest.raises(ValueError):
        parse(expected_source_sha256='f' * 64)
    snapshot = parse()
    identity = (snapshot.snapshot_sha256, snapshot.source_sha256, snapshot.captured_utc)
    rates = snapshot.rates_for('6J')
    try:
        rates['commission'] = 900
    except TypeError:
        pass  # Either an immutable mapping or a defensive copy is safe.
    assert snapshot.rates_for('6J')['commission'] == 8
    assert identity == (snapshot.snapshot_sha256, snapshot.source_sha256, snapshot.captured_utc)


@pytest.mark.parametrize('field', ['expected_sha256', 'expected_source_sha256'])
@pytest.mark.parametrize('value', [None, 1, 'a' * 63, 'g' * 64])
def test_c5_expected_digest_must_be_hex(field, value):
    with pytest.raises(ValueError):
        parse(**{field: value})


@pytest.mark.parametrize('value', ['NaN', 'sNaN', 'Infinity', '-Infinity', '-1',
                                  '1e-9999', '1e9999', 1, 1.25, None, True,
                                  '', '1_0', ' 1 ', 'one'])
def test_c6_bad_number_refuses(value):
    doc = document()
    doc['rows'][0]['commission'] = value
    with pytest.raises(ValueError):
        parse(doc)


def test_c6_zero_and_decimal_exponent_are_valid():
    doc = document()
    doc['rows'][0].update(commission='0', exchange='1.25e1')
    assert parse(doc).rates_for('6J')['commission'] == 0.0
    assert parse(doc).rates_for('6J')['exchange'] == 12.5


@pytest.mark.parametrize('cost', [1, 1.5])
@pytest.mark.parametrize('symbol', SYMBOLS)
def test_c7_reference_addback_and_tradovate_deduction_once(tmp_path, cost, symbol):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=TRADE_LIST_COLUMNS)
    writer.writeheader()
    for number, qty, net, commission in [(1, 2, 81, 19), (2, 3, 173, 27)]:
        for kind, time in [('entry', '10:00'), ('exit', '11:00')]:
            row = dict.fromkeys(TRADE_LIST_COLUMNS, '0')
            row.update({'Trade number': str(number), 'Type': kind + ' long',
                        'Date and time': '2026-01-05 ' + time, 'Size (qty)': str(qty),
                        'Net PnL USD': str(net), 'Commission USD': str(commission),
                        'Adverse excursion USD': '8', 'Favorable excursion USD': '12'})
            writer.writerow(row)
    raw = out.getvalue().encode()
    path = tmp_path / 'invented.csv'
    path.write_bytes(raw)
    trades = scoring.read_export(path, expected_sha256=digest(raw), leg=symbol,
                                 export_tz='America/New_York', baseline=True)
    before = copy.deepcopy(trades)
    rates = parse().rates_for(symbol)
    result = scoring.daily_series(trades, [date(2026, 1, 5), date(2026, 1, 6)], rates, cost)
    # Independent literal oracle: (81+19)+(173+27), ten sides, invented all-in rate.
    rate = 12 + SYMBOLS.index(symbol)
    assert result[0].tolist() == [300 - cost * 10 * rate, -16 - cost * 10 * rate, 24]
    assert result[1].tolist() == [0, 0, 0]
    assert [t.trade.gross_usd for t in trades] == [100, 200]
    assert [t.trade.commission_usd for t in trades] == [19, 27]
    assert trades == before


def test_c8_tradeify_cost_terms_bytes_unchanged_at_cut():
    root = Path(__file__).resolve().parents[2]
    raw = (root / 'ops/c1_rail/qualification/production_source.py').read_bytes()
    source = raw.decode('utf-8')
    function = next(node for node in ast.parse(source).body
                    if isinstance(node, ast.FunctionDef) and node.name == '_cost_terms')
    # Pin only this contract: card B owns other functions in production_source.
    # Exact 45a32be364e7229b181e9b4b053ac9aedd78a6a8 text, no cross-layer import.
    assert digest(ast.get_source_segment(source, function).encode()) == (
        '62ca0a7f39de03089407dff2942b9ab1dfafbba1116dbc0a4bcd65253a829be0')


@pytest.mark.parametrize('raw', [b'{}', b'[]', b'null', b'not json', b'\xff',
                               b'{"schema":1,"schema":2}'])
def test_closed_json_refuses(raw):
    with pytest.raises(ValueError):
        parse(raw=raw)


@pytest.mark.parametrize('field', tuple(document()))
def test_missing_top_level_field_refuses(field):
    doc = document()
    del doc[field]
    with pytest.raises(ValueError):
        parse(doc)


def test_extra_top_level_field_refuses():
    with pytest.raises(ValueError):
        parse(dict(document(), round_trip=True))
