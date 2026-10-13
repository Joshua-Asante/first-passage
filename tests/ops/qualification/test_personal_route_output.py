"""Card B route output and fill lifecycle falsifiers."""
import json
import pytest
from test_personal_replay import fixture_inputs, adapters, signal, rewrite


FIELDS = {'leg', 'instrument', 'contract', 'entry_utc', 'exit_utc', 'side', 'quantity',
          'tranche_index', 'entry_price', 'initial_stop_level', 'delta_0', 'exit_price',
          'exit_kind', 'stop_fill_distance_b', 'net_pnl_usd', 'commission_usd', 'mae_usd', 'mfe_usd'}


def test_b8_actual_flat_fills_money_and_complete_schema(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    output = p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal))
    doc = json.loads(output)
    assert len(doc['trades']) == 3
    for trade in doc['trades']:
        assert set(trade) == FIELDS
        assert trade['quantity'] == 1 and trade['tranche_index'] == 0
        assert trade['entry_price'] == trade['exit_price'] == 100
        assert trade['delta_0'] == 10 and trade['stop_fill_distance_b'] == 0
        assert trade['mae_usd'] == trade['mfe_usd'] == 0
        assert trade['commission_usd'] == 2 and trade['net_pnl_usd'] == -2
    assert b'123456' not in output
    p.validate_route_output(doc)


@pytest.mark.parametrize('field', ['mae_usd', 'mfe_usd'])
def test_b9_absent_excursion_refuses(tmp_path, monkeypatch, field):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    doc = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    del doc['trades'][0][field]
    with pytest.raises(ValueError):
        p.validate_route_output(doc)


def test_b10_route_bytes_identical_and_exception_returns_no_output(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    plain = p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal))
    noop = p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal), bar_observer=lambda *a: 42)
    assert plain == noop
    def raising(*args):
        raise RuntimeError('observer refused')
    output = None
    with pytest.raises(RuntimeError, match='observer refused'):
        output = p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal), bar_observer=raising)
    assert output is None


@pytest.mark.parametrize('side,ohlc,stop', [('buy', [100,110,80,100], 90), ('sell', [100,120,90,100], 110)])
def test_b8_excursions_end_at_actual_stop_and_money_matches_native(side, ohlc, stop):
    from datetime import datetime, timezone, timedelta
    from c1_signal_daemon.book_protocol import OrderIntent, FillTiming, Bracket, Side
    from c1_signal_daemon.feed import Bar
    from c1_signal_daemon.tv_broker_emulator import TVBrokerEmulator
    from c1_rail.qualification.replay import RouteBroker
    ts = datetime(2026,1,5,20,tzinfo=timezone.utc)
    native = TVBrokerEmulator('vanguard_mgc', 1, 1, 1, 2)
    route = RouteBroker('vanguard_mgc', 1, 1, 1, 2, contract_at=lambda *a: '2026-03', symbol='MGC')
    intent = OrderIntent('entry', 'vanguard_mgc', 'entry', Side(side), 2,
                         timing=FillTiming.THIS_CLOSE, bracket=Bracket(stop=stop))
    entry_bar = Bar(ts,100,100,100,100)
    assert route.submit([intent], entry_bar) == native.submit([intent], entry_bar)
    next_bar = Bar(ts+timedelta(minutes=15), *ohlc)
    assert route.process_bar(next_bar) == native.process_bar(next_bar)
    assert route.closed_trades == native.closed_trades
    trade, = route.route_trades
    assert trade['mae_usd'] == -24 and trade['mfe_usd'] == 18
    assert trade['delta_0'] == 11 and trade['stop_fill_distance_b'] == 1
    assert trade['net_pnl_usd'] == native.closed_trades[0].net_pnl == -32
    assert trade['commission_usd'] == native.closed_trades[0].commission == 8


def test_b8_stop_entry_excludes_pre_entry_extreme_and_post_exit_extreme():
    from datetime import datetime, timezone, timedelta
    from c1_signal_daemon.book_protocol import OrderIntent, Bracket, Side
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.replay import RouteBroker
    ts = datetime(2026,1,5,20,tzinfo=timezone.utc)
    broker = RouteBroker('vanguard_mgc', 1, 1, 1, 0, contract_at=lambda *a: '2026-03', symbol='MGC')
    broker.submit([OrderIntent('entry', 'vanguard_mgc', 'entry', Side.BUY, 1,
        order_type='stop', price=105, bracket=Bracket(stop=90, limit=115))], Bar(ts,100,100,100,100))
    broker.process_bar(Bar(ts+timedelta(minutes=15),100,130,80,110))
    row, = broker.route_trades
    assert row['entry_price'] == 106 and row['exit_price'] == 115
    assert row['mae_usd'] == -1 and row['mfe_usd'] == 9
    assert row['stop_fill_distance_b'] == 0


def test_b8_initial_stop_first_placed_after_unprotected_bar():
    from datetime import datetime, timezone, timedelta
    from c1_signal_daemon.book_protocol import OrderIntent, Bracket, BracketAmend, Side, FillTiming
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.replay import RouteBroker
    ts = datetime(2026,1,5,20,tzinfo=timezone.utc)
    broker = RouteBroker('dj30_mym_p250', 1, 1, 0, 0, contract_at=lambda *a: '2026-03', symbol='MYM')
    broker.submit([OrderIntent('entry','dj30_mym_p250','entry',Side.BUY,1,timing=FillTiming.THIS_CLOSE)], Bar(ts,100,100,100,100))
    bar = Bar(ts+timedelta(minutes=15),100,110,80,100)
    broker.process_bar(bar)
    broker.submit([BracketAmend('dj30_mym_p250', Bracket(stop=95))], bar)
    broker.submit([BracketAmend('dj30_mym_p250', Bracket(stop=98))], bar)
    broker.process_bar(Bar(ts+timedelta(minutes=30),100,101,90,100))
    row, = broker.route_trades
    assert row['initial_stop_level'] == 95 and row['delta_0'] == 5
    assert row['mae_usd'] == -20 and row['mfe_usd'] == 10
    assert row['exit_price'] == 98


def test_p0_latch_timestamp_survives_without_account_figures_and_later_day_is_zero(tmp_path, monkeypatch):
    from pathlib import Path
    from test_personal_replay import digest
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    raw = b'10\n'
    Path(manifest['inputs']['e0']['path']).write_bytes(raw)
    manifest['inputs']['e0']['sha256'] = digest(raw)
    rewrite(manifest, 'tuple', lambda d: d['capital_anchor'].update(file_sha256=digest(raw)), monkeypatch)
    def next_day(d, key):
        row = json.loads(json.dumps(d[key][0]).replace('2026-01-05', '2026-01-06').replace('2026-01-04', '2026-01-05'))
        d[key].append(row)
    rewrite(manifest, 'schedule', lambda d: next_day(d, 'sessions'), monkeypatch)
    def source(d):
        next_day(d, 'sessions')
        next_day(d, 'splits')
    rewrite(manifest, 'source_bundle', source, monkeypatch)
    output = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert output['latch'] == {'utc': '2026-01-05T20:15:00+00:00', 'kind': 'personal_halt_latched'}
    assert output['days'][1] == {'account_date': '2026-01-06', 'net_pnl_usd': 0.0, 'fills': 0}
    assert not {'peak', 'equity', 'initial_equity', 'E_0'} & set(output['latch'])
