"""Card B synthetic falsifiers; no private adapter or data loading."""
import json
from dataclasses import asdict
from datetime import timedelta, timezone

import pytest

from c1_rail.book_policy import PersonalP0Policy
from c1_rail.qualification.model import LEG_IDS
from c1_rail.qualification.replay import BookReplay
from mc.simulation import EvaluationState
from test_replay import engine, first_entry, path_session


def observed_engine(observer=None):
    original, adapters = engine({"orb_mnq_v7": first_entry})
    replay = BookReplay(adapters, original.instruments,
        policy=PersonalP0Policy(),
        initial_state=EvaluationState(100000, 100000, 100000, 0, 0),
        sizing_inputs=original.sizing_inputs,
        schedule_quotes=original.schedule_quotes, bar_observer=observer)
    return replay, adapters


def output_bytes(result):
    return json.dumps(asdict(result), default=str, sort_keys=True).encode()


def test_b10_observer_after_all_close_fills_once_in_fixed_order_same_instances():
    calls = []
    def observe(leg_id, close, strategy):
        assert strategy is adapters[leg_id]
        assert all(len(a.bars) == len(strategy.bars) for a in adapters.values())
        assert all(a.bars and a.bars[-1].ts == close - timedelta(minutes=15)
                   for a in adapters.values())
        assert close.tzinfo is timezone.utc
        if len(strategy.bars) == 1:
            assert any(e.fill and e.fill.kind == "entry"
                       for e in adapters["orb_mnq_v7"].feedback)
        calls.append((leg_id, close))
        return "ignored"
    replay, adapters = observed_engine(observe)
    session = path_session(prices=[(100, 100, 100, 100)] * 3)
    replay.run((session,))
    assert calls == [(leg, pb.source_bar_time + timedelta(minutes=15))
                     for pb in session.bars for leg in LEG_IDS]


def test_b10_noop_observer_preserves_output_bytes():
    session = path_session(prices=[(100, 100, 100, 100)] * 3)
    plain, _ = observed_engine()
    hooked, _ = observed_engine(lambda *args: object())
    assert output_bytes(plain.run((session,))) == output_bytes(hooked.run((session,)))


def test_b10_raising_observer_aborts_without_successful_result():
    def fail(*args):
        raise RuntimeError("synthetic observer failure")
    replay, _ = observed_engine(fail)
    result = None
    with pytest.raises(RuntimeError, match="synthetic observer failure"):
        result = replay.run((path_session(),))
    assert result is None


# Every input below is invented. Synthetic pins are patched before verification,
# never inferred by production code from the files it is checking.
import hashlib
import importlib
from pathlib import Path
from c1_rail.qualification.contract import canonical_json_bytes
from c1_signal_daemon.book_protocol import OrderIntent, Side, FillTiming, Bracket
from test_replay import Adapter


def personal_module():
    return importlib.import_module('c1_rail.qualification.personal_replay')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def fixture_inputs(tmp_path, monkeypatch, *, denied=False):
    p = personal_module()
    sizing = {
        'aegis_6j': {'base': 1, 'adds': 'UNCHANGED'},
        'dj30_mym_p250': {'risk_multiplier': '1/2', 'cap_reserve_multiplier': '1/2', 'adds': 'OFF'},
        'vanguard_mgc': {'base_by_port': {'1': 1, '2': 1}, 'adds': 'OFF'},
        'orb_mnq_v7': {'base': 0, 'adds': 'UNCHANGED'},
    }
    e0 = b'123456\n'
    tuple_doc = dict(schema='q-sfclear-1-sizing-tuple/v1', study='synthetic', rung='R1',
        status='synthetic', protection='P0', lifecycle_tier='AUTHORIZED',
        striker_risk_basis='synthetic', size_vector_hash_rule='synthetic',
        size_vector_sha256=digest(canonical_json_bytes(sizing)),
        prescreen_SHA256SUMS_sha256='1'*64, nonce='synthetic', paper_initial_capital=100000,
        book_legs=list(LEG_IDS), sizing=sizing,
        capital_anchor={'file': 'not/a/path: synthetic label', 'file_sha256': digest(e0), 'symbol': 'E_0'},
        cap_source=dict(code_source='synthetic', ruling='synthetic',
                        shared_account_cap_micro_equivalents=80, request_cap_micro_equivalents_each_leg=80),
        rule_max_contracts={**dict.fromkeys(LEG_IDS, 1), 'book_micro_equivalents': 4},
        derived_from=dict(R0_size_vector_sha256='2'*64, change_from_R0='synthetic', r3d_startup_policy_sha256='3'*64),
        ruling=dict(D4='synthetic', date='2026-01-05', source='synthetic', text='synthetic'))
    row = {'account_date': '2026-01-05', 'permission': 'DENIED' if denied else 'PERMITTED'}
    if denied:
        row.update(denial_reason='HOLIDAY', d19_status={})
    else:
        for name, value in [('opens', '2026-01-04T23:00:00Z'),
                            ('risk_add_cutoff', '2026-01-05T20:45:00Z'),
                            ('flatten_start', '2026-01-05T20:55:00Z'),
                            ('own_flat_deadline', '2026-01-05T21:00:00Z')]:
            row[name+'_utc'] = value
            row[name+'_local'] = value
    schedule = {'header': {'schema': 'sfclear_historical_schedule/v1'}, 'sessions': [row]}
    rolls = {'header': {'schema': 'sfclear_roll_dates/v1'}, 'contracts': [
        {'product': symbol, 'contract_month': '2026-03', 'g4_start_open_utc': '2026-03-01T23:00:00Z',
         'g4_start_open_local': '2026-03-01T23:00:00Z', 'g4_start_trade_date': '2026-03-02',
         'last_trade': '2026-03-03', 'on_seam_cycle': True,
         **({'first_notice': '2026-03-03'} if symbol == 'MGC' else {})}
        for symbol in ('6J', 'MGC')], 'seams': []}
    bars = []
    for minute in (0, 15, 30, 45):
        timestamp = f'2026-01-05T20:{minute:02}:00Z'
        bars.append({'utc': timestamp, 'legs': {leg: {'contract': '2026-03',
                     'ohlc': [100, 100, 100, 100]} for leg in LEG_IDS}})
    source = {'schema': 'sfclear_source_bundle/v1', 'sessions': [
        {'account_date': '2026-01-05', 'bars': bars}],
        'striker_risk_dollars': 20,
        'splits': [], 'data_exclusions': []}
    friction = {'schema': 'sfclear_reference_friction/v1', 'instruments': {
        leg: dict(mintick=1, pointvalue=1, slippage_ticks=0, commission_per_side=1,
                  orders_on_close=False) for leg in LEG_IDS}}
    docs = dict(tuple=tuple_doc, size_vector=sizing, source_bundle=source,
                schedule=schedule, roll_list=rolls, generator={'synthetic': True},
                calendar={'synthetic': True}, reference_friction=friction)
    artifacts = {}
    for role, doc in docs.items():
        raw = canonical_json_bytes(doc)
        path = tmp_path / (role+'.json')
        path.write_bytes(raw)
        artifacts[role] = {'path': str(path), 'sha256': digest(raw)}
    path = tmp_path / 'synthetic-e0.txt'
    path.write_bytes(e0)
    artifacts['e0'] = {'path': str(path), 'sha256': digest(e0)}
    for role, constant in [('tuple', 'TUPLE_SHA256'), ('schedule', 'SCHEDULE_SHA256'), ('roll_list', 'ROLL_SHA256')]:
        monkeypatch.setattr(p, constant, artifacts[role]['sha256'])
    manifest = {'schema': 'sfclear_replay_manifest/v1', 'routes': dict.fromkeys(LEG_IDS, 'PR'),
                'inputs': artifacts}
    return p, manifest


def rewrite(manifest, role, change, monkeypatch):
    path = Path(manifest['inputs'][role]['path'])
    doc = json.loads(path.read_bytes())
    change(doc)
    raw = canonical_json_bytes(doc)
    path.write_bytes(raw)
    manifest['inputs'][role]['sha256'] = digest(raw)
    if role in ('tuple', 'schedule', 'roll_list'):
        monkeypatch.setattr(personal_module(), {'tuple':'TUPLE_SHA256', 'schedule':'SCHEDULE_SHA256',
                            'roll_list':'ROLL_SHA256'}[role], digest(raw))


def adapters(emit=None):
    return {leg: Adapter(leg, emit) for leg in LEG_IDS}


def signal(a, bar):
    if len(a.bars) != 1:
        return []
    return [OrderIntent('entry', a.leg_id, 'entry', Side.SELL if a.leg_id == 'aegis_6j' else Side.BUY,
                        1, timing=FillTiming.THIS_CLOSE, bracket=Bracket(stop=110 if a.leg_id == 'aegis_6j' else 90),
                        stop_dist_pts=10)]


@pytest.mark.parametrize('role', ['tuple', 'size_vector', 'source_bundle', 'schedule', 'generator',
                                  'calendar', 'reference_friction', 'roll_list', 'e0'])
def test_b1_each_identity_refuses_before_adapter_construction(tmp_path, monkeypatch, role):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    path = Path(manifest['inputs'][role]['path'])
    path.write_bytes(b'654321\n' if role == 'e0' else path.read_bytes() + b' ')
    called = []
    with pytest.raises(ValueError, match='identity'):
        p.run_personal_replay(manifest, adapter_factory=lambda envelope: called.append(True))
    assert not called


@pytest.mark.parametrize('raw', [b'', b'0\n', b'-1\n', b'1.0\n', b'1\r\n', b'1\n\n', b' 1\n', b'1', b'\xef\xbb\xbf1\n'])
def test_b1_e0_strict_encoding(tmp_path, monkeypatch, raw):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    Path(manifest['inputs']['e0']['path']).write_bytes(raw)
    manifest['inputs']['e0']['sha256'] = digest(raw)
    rewrite(manifest, 'tuple', lambda d: d['capital_anchor'].update(file_sha256=digest(raw)), monkeypatch)
    with pytest.raises(ValueError, match='E_0'):
        p.verify_inputs(manifest)


def test_b1_bound_equity_and_single_read_missing_file(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    reads = []
    original = Path.read_bytes
    def once(path):
        reads.append(str(path))
        assert reads.count(str(path)) == 1
        return original(path)
    with monkeypatch.context() as m:
        m.setattr(Path, 'read_bytes', once)
        envelope = p.verify_inputs(manifest)
        replay = p.build_personal_replay(envelope, adapter_factory=lambda e: adapters())
        assert replay.initial_equity == replay.personal_peak == 123456
    assert set(reads) == {a['path'] for a in manifest['inputs'].values()}
    Path(manifest['inputs']['e0']['path']).unlink()
    with pytest.raises(ValueError, match='identity'):
        p.verify_inputs(manifest)


@pytest.mark.parametrize('mutation', ['legs', 'canonical', 'striker_adds', 'vanguard_adds', 'orb'])
def test_b2_tuple_constraints(tmp_path, monkeypatch, mutation):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    def change(d):
        if mutation == 'legs':
            d['book_legs'].pop()
        elif mutation == 'canonical':
            d['sizing']['dj30_mym_p250']['risk_multiplier'] = '2/4'
        elif mutation == 'orb':
            d['sizing']['orb_mnq_v7']['base'] = 1
        else:
            d['sizing']['dj30_mym_p250' if mutation == 'striker_adds' else 'vanguard_mgc']['adds'] = 'UNCHANGED'
        d['size_vector_sha256'] = digest(canonical_json_bytes(d['sizing']))
    rewrite(manifest, 'tuple', change, monkeypatch)
    with pytest.raises(ValueError):
        p.verify_inputs(manifest)


def test_b3_denied_keeps_zero_day_and_refusals(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch, denied=True)
    result = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert result['days'] == [{'account_date': '2026-01-05', 'net_pnl_usd': 0.0, 'fills': 0}]
    assert not result['trades']
    assert all(len(result['refusals'][leg]) == 1 for leg in LEG_IDS)


def test_b5_nonempty_split_refuses(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    rewrite(manifest, 'source_bundle', lambda d: d.update(splits=[{}]), monkeypatch)
    with pytest.raises(ValueError, match='splits'):
        p.verify_inputs(manifest)


@pytest.mark.parametrize('leg', ['aegis_6j', 'vanguard_mgc'])
def test_b6_exact_g4_boundary_refuses(tmp_path, monkeypatch, leg):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    symbol = '6J' if leg == 'aegis_6j' else 'MGC'
    rewrite(manifest, 'roll_list', lambda d: [row.update(g4_start_open_utc='2026-01-05T20:15:00Z')
                for row in d['contracts'] if row['product'] == symbol], monkeypatch)
    result = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert not [row for row in result['trades'] if row['leg'] == leg]
    assert result['refusals'][leg][0]['reason'] == 'G4 contract boundary'


def test_b7_zero_quantity_exactly_one_feedback_and_no_fill(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    strategies = adapters(signal)
    result = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: strategies))
    assert not [row for row in result['trades'] if row['leg'] == 'orb_mnq_v7']
    assert [e.detail for e in strategies['orb_mnq_v7'].feedback] == ['zero policy quantity']
    assert [r['reason'] for r in result['refusals']['orb_mnq_v7']] == ['zero policy quantity']


def test_b12_rs_refuses_before_load(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    for leg in LEG_IDS:
        manifest['routes'][leg] = 'RS'
        with pytest.raises(ValueError, match='PR'):
            p.verify_inputs(manifest)
        manifest['routes'][leg] = 'PR'


def test_b4_cutoff_strict_and_flatten_at_start(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    envelope = p.verify_inputs(manifest)
    from datetime import datetime
    before = datetime(2026, 1, 5, 20, 44, 59, tzinfo=timezone.utc)
    edge = before + timedelta(seconds=1)
    assert envelope.risk_refusal('aegis_6j', before) is None
    assert envelope.risk_refusal('aegis_6j', edge) == 'scheduled entry cutoff'
    doc = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert all(t['exit_utc'] == '2026-01-05T20:55:00+00:00' for t in doc['trades'])


def test_b11_personal_startup_cap_is_resolved_and_default_tradeify_unchanged(monkeypatch):
    from c1_rail.qualification.production_source import parse_startup_policy
    from c1_rail import book_policy as bp
    plan = {'schema': 'qualification-source-startup/v1', 'initialization': 'FRESH_ONCE_CONTINUOUS',
            'positions': 'ZERO', 'working_orders': 'ZERO', 'splice_behavior': 'CARRY_ALL_STATE',
            'path_start_date': '2026-01-05', 'shared_account_cap_micro_equivalents': 80,
            'legs': {leg: {'paper_initial_capital': '100000', 'lifecycle_tier': 'AUTHORIZED',
                    'request_cap_micro_equivalents': 80} for leg in LEG_IDS}}
    raw = canonical_json_bytes(plan)
    assert parse_startup_policy(raw) == parse_startup_policy(raw, tier=bp.TIER)
    monkeypatch.setitem(bp.FIRM_RULES['Personal_Tradovate'], 'micro_contract_cap', 7)
    plan['shared_account_cap_micro_equivalents'] = 7
    for row in plan['legs'].values():
        row['request_cap_micro_equivalents'] = 7
    assert parse_startup_policy(canonical_json_bytes(plan), tier='Personal_Tradovate').shared_account_cap_micro_equivalents == 7
    with pytest.raises(ValueError):
        parse_startup_policy(canonical_json_bytes(plan))


@pytest.mark.parametrize('leg', ['aegis_6j', 'vanguard_mgc'])
def test_b6_carried_at_g4_aborts_and_unlisted_price_jump_does_not_roll(tmp_path, monkeypatch, leg):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    def jump(d):
        d['sessions'][0]['bars'][1]['legs'][leg]['ohlc'] = [105]*4
    rewrite(manifest, 'source_bundle', jump, monkeypatch)
    plain = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert any(t['leg'] == leg for t in plain['trades'])
    symbol = '6J' if leg == 'aegis_6j' else 'MGC'
    rewrite(manifest, 'roll_list', lambda d: [row.update(g4_start_open_utc='2026-01-05T20:15:00Z')
                for row in d['contracts'] if row['product'] == symbol], monkeypatch)
    # Entry fills at the first close. Shift the boundary to the next open,
    # after that entry was admitted, to exercise the carried-position guard.
    rewrite(manifest, 'roll_list', lambda d: [row.update(g4_start_open_utc='2026-01-05T20:30:00Z')
                for row in d['contracts'] if row['product'] == symbol], monkeypatch)
    with pytest.raises(p.ReplayNeedsContext, match='G4 held'):
        p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal))


@pytest.mark.parametrize('leg', ['aegis_6j', 'vanguard_mgc'])
def test_b7_zero_base_or_zero_port_map_preserves_feedback(tmp_path, monkeypatch, leg):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    # A zero mapped Vanguard quantity (port count stays valid) is the shared
    # policy's zero-port case; OrderIntent itself forbids literal qty=0.
    size = json.loads(Path(manifest['inputs']['size_vector']['path']).read_bytes())
    if leg == 'aegis_6j':
        size[leg]['base'] = 0
    else:
        size[leg]['base_by_port']['1'] = 0
    rewrite(manifest, 'size_vector', lambda d: d.update(size), monkeypatch)
    rewrite(manifest, 'tuple', lambda d: d.update(sizing=size, size_vector_sha256=digest(canonical_json_bytes(size))), monkeypatch)
    strategies = adapters(signal)
    output = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: strategies))
    assert [e.detail for e in strategies[leg].feedback] == ['zero policy quantity']
    assert len(output['refusals'][leg]) == 1
    assert not [row for row in output['trades'] if row['leg'] == leg]


def test_b1_tuple_anchor_must_match_independent_e0_identity(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    rewrite(manifest, 'tuple', lambda d: d['capital_anchor'].update(file_sha256='f'*64), monkeypatch)
    with pytest.raises(ValueError, match='E_0 identity'):
        p.verify_inputs(manifest)


def test_verification_has_no_mutable_runtime_globals_after_a_personal_run(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.result_adjudication import _verify_retained_executable_modules
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal))
    # Restore only the three synthetic pins before comparing module definitions.
    monkeypatch.undo()
    row = SimpleNamespace(source_bytes=Path(p.__file__).read_bytes())
    _verify_retained_executable_modules({p.__name__: row}, {p.__name__}, set())


@pytest.mark.parametrize('version,expected', [
    (1, '91327833ad9d8c711fd098e3f5024d9b75afefd06ef5b882121199a6ead88ef8'),
    (2, 'fc5176cf1db2557143f28c77e08b8fb24ce5ca4f625bbaf359b270a103c862ca'),
])
def test_b11_startup_and_factory_bytes_equal_clean_07d90b0(version, expected, monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.production_source import parse_startup_policy, ProductionSource
    from c1_rail.book_policy import IDENTITY_SIZE_VECTOR
    import c1_signal_daemon.book_adapters as loaders
    plan = {'schema': 'qualification-source-startup/v1', 'initialization': 'FRESH_ONCE_CONTINUOUS',
            'positions': 'ZERO', 'working_orders': 'ZERO', 'splice_behavior': 'CARRY_ALL_STATE',
            'path_start_date': '2026-01-05', 'shared_account_cap_micro_equivalents': 80,
            'legs': {leg: {'paper_initial_capital': '100000', 'lifecycle_tier': 'AUTHORIZED',
                    'request_cap_micro_equivalents': 80} for leg in LEG_IDS}}
    if version == 2:
        plan.update(schema='qualification-source-startup/v2', sizing=dict(IDENTITY_SIZE_VECTOR.as_mapping(),
                    aegis_6j={'base': 7, 'adds': 'UNCHANGED'}))
    startup = parse_startup_policy(canonical_json_bytes(plan))
    assert digest(repr(startup).encode()) == expected
    original, strategies = engine({'orb_mnq_v7': first_entry})
    for strategy in strategies.values():
        strategy.params = SimpleNamespace()
    monkeypatch.setattr(loaders, '_load_domain_adapters', lambda *a, **k: SimpleNamespace(registry=strategies))
    source = SimpleNamespace(contract=SimpleNamespace(initial_state=SimpleNamespace(
        original_basis=100000, current_equity=100000, historical_eod_peak=100000,
        prior_trade_days=0, prior_max_day_profit=0)), prepared=SimpleNamespace(startup=startup,
        retained_bytes=()), _domain=None, _policy=None, _instruments=tuple(original.instruments.items()))
    replay = ProductionSource._engine(source, original.schedule_quotes)
    assert digest(output_bytes(replay.run((path_session(prices=[(100,100,100,100)]*3),)))) == 'b4ab6b7703e8cfb51c608daa7ab5150fcc3b4ce306e6e48696d9fd76fdafd9f6'
    personal = ProductionSource._engine(source, original.schedule_quotes, policy=PersonalP0Policy())
    assert personal.personal and personal.clock is None


def test_b1_derived_envelope_cannot_substitute_initial_equity(tmp_path, monkeypatch):
    from dataclasses import replace
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    envelope = p.verify_inputs(manifest)
    called = []
    with pytest.raises(ValueError, match='derived state'):
        p.build_personal_replay(replace(envelope, initial_equity=1), adapter_factory=lambda e: (called.append(True) or adapters()))
    assert not called


def test_b3_denied_without_market_bars_is_retained_as_zero_day(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch, denied=True)
    rewrite(manifest, 'source_bundle', lambda d: d['sessions'][0].update(bars=[]), monkeypatch)
    result = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert result['days'] == [{'account_date': '2026-01-05', 'net_pnl_usd': 0.0, 'fills': 0}]
    assert result['trades'] == []


@pytest.mark.parametrize('leg', ['aegis_6j', 'vanguard_mgc'])
@pytest.mark.parametrize('change_contract', [False, True])
def test_r1_pending_stop_is_cancelled_at_originating_roll(tmp_path, monkeypatch, leg, change_contract):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    symbol = p.SYMBOLS[leg]
    def roll(d):
        old = next(row for row in d['contracts'] if row['product'] == symbol)
        d['contracts'].append(dict(old, contract_month='2026-06'))
        old['g4_start_open_utc'] = '2026-01-05T20:30:00Z'
    rewrite(manifest, 'roll_list', roll, monkeypatch)
    def prices(d):
        for row in d['sessions'][0]['bars'][1 if change_contract else 2:]:
            row['legs'][leg]['ohlc'] = [80 if leg == 'aegis_6j' else 120]*4
            if change_contract:
                row['legs'][leg]['contract'] = '2026-06'
    rewrite(manifest, 'source_bundle', prices, monkeypatch)
    def emit(a, bar):
        if a.leg_id != leg or len(a.bars) != 1:
            return []
        return [OrderIntent('old-stop', leg, 'entry', Side.SELL if leg == 'aegis_6j' else Side.BUY,
                            1, 'stop', 90 if leg == 'aegis_6j' else 110,
                            bracket=Bracket(stop=130 if leg == 'aegis_6j' else 70), stop_dist_pts=40)]
    strategies = adapters(emit)
    result = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: strategies))
    assert result['trades'] == []
    assert not any(e.fill for e in strategies[leg].feedback)
    assert any(e.event == 'cancel' and e.order_id == 'old-stop' for e in strategies[leg].feedback)
    assert len(result['refusals'][leg]) == 1
    assert 'originating contract' in result['refusals'][leg][0]['reason']


@pytest.mark.parametrize('leg,key,value', [
    ('aegis_6j', 'base', 1.0), ('aegis_6j', 'base', True),
    ('orb_mnq_v7', 'base', 0.0), ('vanguard_mgc', 'base_by_port', {'1': 1.0, '2': 1}),
])
def test_r3_standalone_size_vector_numeric_alias_refuses(tmp_path, monkeypatch, leg, key, value):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    rewrite(manifest, 'size_vector', lambda d: d[leg].update({key: value}), monkeypatch)
    called = []
    with pytest.raises(ValueError, match='size vector identity'):
        p.run_personal_replay(manifest, adapter_factory=lambda e: (called.append(True) or adapters()))
    assert not called


def test_r3_output_size_identity_is_the_tuple_canonical_digest(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    path = Path(manifest['inputs']['size_vector']['path'])
    raw = json.dumps(json.loads(path.read_bytes()), indent=2).encode()
    path.write_bytes(raw)
    manifest['inputs']['size_vector']['sha256'] = digest(raw)
    result = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters()))
    tuple_doc = json.loads(Path(manifest['inputs']['tuple']['path']).read_bytes())
    assert result['input_identities']['size_vector'] == tuple_doc['size_vector_sha256']
    assert result['input_identities']['size_vector'] != digest(raw)


@pytest.mark.parametrize('personal,cap', [(True, 7), (True, 80), (False, 7), (False, 80)])
def test_r2_resolved_policy_reaches_every_startup_parse(tmp_path, monkeypatch, personal, cap):
    from composition_fixture import (build_artifacts, verified_domain, contract_document, signed_approval)
    from test_trust_domain import NOW
    from c1_rail.qualification.contract import validate_frozen_contract, ObservedBindings
    from c1_rail.qualification import production_source as ps
    from c1_rail import book_policy as bp
    monkeypatch.setitem(bp.FIRM_RULES['Personal_Tradovate'], 'micro_contract_cap', 7)
    fixture = build_artifacts(tmp_path, idle=True).with_runtime_artifacts(tmp_path)
    startup = json.loads(fixture.payloads['source_startup_policy'])
    startup['shared_account_cap_micro_equivalents'] = cap
    for row in startup['legs'].values():
        row['request_cap_micro_equivalents'] = cap
    raw = canonical_json_bytes(startup)
    fixture.payloads['source_startup_policy'] = raw
    (tmp_path / fixture.paths['source_startup_policy']).write_bytes(raw)
    domain, private, keys = verified_domain(fixture)
    raw = canonical_json_bytes(contract_document(fixture, domain))
    approval = signed_approval(raw, private['test-freeze'], key_id='test-freeze', scope='FREEZE_F1')
    observed = ObservedBindings(
        artifact_sha256={fixture.paths[r]: digest(b) for r, b in fixture.payloads.items()},
        runtime_load_sha256={r: digest(b) for r, b in fixture.payloads.items()},
        effective_settings_sha256=digest(fixture.payloads['effective_settings_successor']), orb_normal_base=1)
    contract = validate_frozen_contract(raw, approval, keys, observed, now=NOW, trust_domain=domain)
    seen, original = [], ps.parse_startup_policy
    def parse(raw, *, tier=None):
        seen.append(tier)
        return original(raw, tier=tier)
    monkeypatch.setattr(ps, 'parse_startup_policy', parse)
    policy = PersonalP0Policy() if personal else None
    def build():
        return ps.ProductionSource._build_composition(contract, artifact_root=tmp_path, policy=policy)
    if cap != (7 if personal else 80):
        with pytest.raises(ValueError, match='cap'):
            build()
        return
    source = build()
    assert len(seen) >= 3
    assert all(tier == ('Personal_Tradovate' if personal else bp.TIER) for tier in seen)
    assert source.prepared.startup.shared_account_cap_micro_equivalents == cap
    replay = source._engine(source._quotes)
    assert replay.personal is personal
    assert replay.ledger.cap == cap
    from c1_rail.book_policy import candidate_book_protection_policy
    override = candidate_book_protection_policy() if personal else PersonalP0Policy()
    with pytest.raises(ValueError, match='startup cap'):
        source._engine(source._quotes, policy=override)


@pytest.mark.parametrize('kind', ['entry', 'add', 'exit', 'flat'])
def test_r1_every_pending_order_binds_contract_and_cannot_fill_successor(kind):
    from datetime import datetime
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.replay import RouteBroker, ReplayNeedsContext
    start = datetime(2026, 1, 5, 20, tzinfo=timezone.utc)
    edge = start + timedelta(minutes=15)
    broker = RouteBroker('aegis_6j', mintick=1, pointvalue=1, slippage_ticks=0,
                         commission_per_side=1, symbol='6J',
                         contract_at=lambda leg, ts: '2026-03' if ts < edge else '2026-06')
    bar = Bar(start, 100, 100, 100, 100)
    if kind in ('exit', 'flat'):
        broker.submit([OrderIntent('held', 'aegis_6j', 'entry', Side.BUY, 1,
                                   timing=FillTiming.THIS_CLOSE, bracket=Bracket(stop=90))], bar)
    broker.submit([OrderIntent('pending', 'aegis_6j', kind,
                               Side.SELL if kind in ('exit', 'flat') else Side.BUY,
                               1, timing=FillTiming.NEXT_OPEN, bracket=Bracket(stop=90))], bar)
    assert 'pending' in broker.pending_order_ids()
    assert broker.order_contract('pending') == '2026-03'
    with pytest.raises(ReplayNeedsContext, match='originating contract'):
        broker.process_bar(Bar(edge, 120, 120, 120, 120))


def test_r1_close_admission_uses_originating_bar_contract(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    def roll(d):
        old = next(row for row in d['contracts'] if row['product'] == '6J')
        d['contracts'].append(dict(old, contract_month='2026-06'))
        old['g4_start_open_utc'] = '2026-01-05T20:15:00Z'
    rewrite(manifest, 'roll_list', roll, monkeypatch)
    def contracts(d):
        for row in d['sessions'][0]['bars'][1:]:
            row['legs']['aegis_6j']['contract'] = '2026-06'
    rewrite(manifest, 'source_bundle', contracts, monkeypatch)
    result = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert not any(t['leg'] == 'aegis_6j' for t in result['trades'])
    assert result['refusals']['aegis_6j'][0]['reason'] == 'G4 contract boundary'


def test_r4_indexed_contract_lookup_matches_multi_roll_scan(tmp_path, monkeypatch):
    from dataclasses import replace
    from types import MappingProxyType
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    def rolls(d):
        for row in tuple(d['contracts']):
            d['contracts'].extend(dict(row, contract_month=label) for label in ('2026-06', '2026-09'))
    rewrite(manifest, 'roll_list', rolls, monkeypatch)
    def contracts(d):
        for i, row in enumerate(d['sessions'][0]['bars']):
            for j, leg in enumerate(LEG_IDS):
                row['legs'][leg]['contract'] = ('2026-03', '2026-06', '2026-09')[(i+j) % 3]
    rewrite(manifest, 'source_bundle', contracts, monkeypatch)
    envelope = p.verify_inputs(manifest)
    def scan(self, leg, instant):
        candidates = [(ts, label) for (k, ts), label in self.contracts.items() if k == leg and ts <= instant]
        if not candidates:
            raise ValueError('missing contract fact')
        return max(candidates)[1]
    start = min(ts for _, ts in envelope.contracts)
    assert p._index_contracts(dict(reversed(tuple(envelope.contracts.items())))) == envelope.contract_index
    for leg in LEG_IDS:
        times, labels = envelope.contract_index[leg]
        assert times == tuple(sorted(times)) and len(times) == len(labels) == 4
        for minute in (-1, 0, 1, 14, 15, 16, 29, 30, 44, 45, 55, 60):
            instant = start + timedelta(minutes=minute)
            if minute < 0:
                with pytest.raises(ValueError, match='missing contract fact'):
                    envelope.contract_at(leg, instant)
            else:
                assert envelope.contract_at(leg, instant) == scan(envelope, leg, instant)
    with pytest.raises(ValueError, match='missing contract fact'):
        envelope.contract_at('missing-leg', start)
    with pytest.raises(TypeError):
        envelope.contract_index[LEG_IDS[0]] = ((), ())
    corrupted = replace(envelope, contract_index=MappingProxyType(dict.fromkeys(LEG_IDS, ((), ()))))
    with pytest.raises(ValueError, match='derived state'):
        p.build_personal_replay(corrupted, adapter_factory=lambda e: pytest.fail('unverified index reached factory'))
    actual = p.run_personal_replay(manifest, adapter_factory=lambda e: adapters())
    monkeypatch.setattr(p.VerifiedInputs, 'contract_at', scan)
    assert p.run_personal_replay(manifest, adapter_factory=lambda e: adapters()) == actual


def test_r4_90000_bars_four_legs_lookup_scale(record_property):
    import subprocess
    import sys
    # Bound the old quadratic implementation without leaving a runaway worker.
    code = '''
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from time import perf_counter
from c1_rail.qualification.personal_replay import VerifiedInputs, _index_contracts
from c1_rail.qualification.model import LEG_IDS
start = perf_counter()
t0 = datetime(2022, 9, 1, tzinfo=timezone.utc)
times = tuple(t0 + timedelta(minutes=15*i) for i in range(90000))
facts = {(leg, ts): str(i//1000+j) for j, leg in enumerate(LEG_IDS) for i, ts in enumerate(times)}
receipt = SimpleNamespace(contracts=facts, contract_index=_index_contracts(facts))
for j, leg in enumerate(LEG_IDS):
    for i, ts in enumerate(times):
        assert VerifiedInputs.contract_at(receipt, leg, ts) == str(i//1000+j)
print(perf_counter()-start)
'''
    result = subprocess.run([sys.executable, '-c', 'import sys; sys.path[:0] = '+repr(sys.path)+'\n'+code],
                            capture_output=True, text=True, timeout=5, check=True)
    elapsed = float(result.stdout)
    record_property('lookup_scale_seconds', elapsed)
    assert elapsed < 5


@pytest.mark.parametrize('kind', ['long', 'short', 'pending'])
def test_b5_r1_vertices_and_unexposed_not_split(tmp_path, monkeypatch, kind):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    leg = 'aegis_6j' if kind == 'short' else 'vanguard_mgc'
    def prices(d):
        d['sessions'][0]['bars'][-1]['legs'][leg]['ohlc'] = [100, 110, 90, 105]
    rewrite(manifest, 'source_bundle', prices, monkeypatch)
    def emit(a, bar):
        if a.leg_id != leg or len(a.bars) != 1:
            return []
        side = Side.SELL if kind == 'short' else Side.BUY
        return [OrderIntent('vertex', leg, 'entry', side, 1,
            order_type='stop' if kind == 'pending' else 'market',
            price=200 if kind == 'pending' else None,
            timing=FillTiming.THIS_CLOSE if kind != 'pending' else FillTiming.NEXT_OPEN,
            bracket=Bracket(stop=150 if kind == 'short' else 50), stop_dist_pts=50)]
    envelope = p.verify_inputs(manifest)
    replay = p.build_personal_replay(envelope, adapter_factory=lambda e: adapters(emit))
    from c1_rail.qualification.bracket import BracketScheduleQuotes
    assert isinstance(replay.schedule_quotes, BracketScheduleQuotes)
    if kind == 'pending':
        # Isolate the provider's pending-only branch; the book cutoff normally
        # cancels resting entries before flatten start.
        from c1_rail.qualification.model import ScheduleExposure
        session = envelope.path[0]
        pb = session.bars[-1]
        exposure = ScheduleExposure(position=0, pending=True, reserved=0)
        replay.schedule_quotes.split_bar(session, pb, session.source.schedule.flatten_start,
            leg, exposure=exposure)
    else:
        replay.run(envelope.path)
    rows = replay.schedule_quotes.placements
    assert [(r.leg_id, r.price) for r in rows] == [(leg, {'long':90, 'short':110, 'pending':105}[kind])]
    assert replay.schedule_quotes.run == 'R1'


def exclude_day(d):
    d['sessions'][0]['bars'] = []
    d['data_exclusions'] = [dict(account_date='2026-01-05', leg=LEG_IDS[0], reason='missing_active_bar')]


def test_b15_exclusion_zero_day(tmp_path, monkeypatch):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    rewrite(manifest, 'source_bundle', exclude_day, monkeypatch)
    doc = json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))
    assert doc['days'] == [dict(account_date='2026-01-05', net_pnl_usd=0.0, fills=0)]
    assert not doc['trades'] and not any(doc['refusals'].values())


@pytest.mark.parametrize('invalid', ['unlisted', 'bars', 'denied', 'reason', 'leg', 'duplicate', 'absent'])
def test_b16_b17_invalid_exclusion_refuses(tmp_path, monkeypatch, invalid):
    p, manifest = fixture_inputs(tmp_path, monkeypatch, denied=invalid == 'denied')
    def change(d):
        original = d['sessions'][0]['bars']
        exclude_day(d)
        row = d['data_exclusions'][0]
        if invalid == 'unlisted': d['data_exclusions'] = []
        elif invalid == 'bars': d['sessions'][0]['bars'] = original
        elif invalid == 'reason': row['reason'] = 'other'
        elif invalid == 'leg': row['leg'] = 'other'
        elif invalid == 'duplicate': d['data_exclusions'].append(dict(row))
        elif invalid == 'absent': row['account_date'] = '2026-01-06'
    rewrite(manifest, 'source_bundle', change, monkeypatch)
    with pytest.raises(ValueError):
        p.verify_inputs(manifest)


@pytest.mark.parametrize('leg,month', [('aegis_6j','2026-09'), ('vanguard_mgc','2026-12')])
def test_b18_post_seam_no_boundary_and_unknown_refuses(tmp_path, monkeypatch, leg, month):
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    rewrite(manifest, 'roll_list', lambda d: d['seams'].append(dict(product=p.SYMBOLS[leg],
        from_month='2026-03', to_month=month, switch_open_local='2026-01-04T18:00:00-05:00',
        switch_open_utc='2026-01-04T23:00:00Z', switch_trade_date='2026-01-05', last_trade='2026-03-03')), monkeypatch)
    def contract(d, value):
        for bar in d['sessions'][0]['bars']: bar['legs'][leg]['contract'] = value
    rewrite(manifest, 'source_bundle', lambda d: contract(d, month), monkeypatch)
    envelope = p.verify_inputs(manifest)
    assert envelope.rolls[(p.SYMBOLS[leg], month)] is None
    assert json.loads(p.run_personal_replay(manifest, adapter_factory=lambda e: adapters(signal)))['trades']
    rewrite(manifest, 'source_bundle', lambda d: contract(d, '2099-01'), monkeypatch)
    with pytest.raises(ValueError, match='contract'):
        p.verify_inputs(manifest)


@pytest.mark.parametrize('denied', [False, True])
def test_b19_b20_boundary_order_factory_once_state_untouched(tmp_path, monkeypatch, denied):
    from c1_signal_daemon.feed import Bar
    from c1_signal_daemon.book_protocol import Fill
    namespaces = {cls: frozenset(vars(cls)) for cls in (Bar, Fill)}
    p, manifest = fixture_inputs(tmp_path, monkeypatch)
    def schedule(d):
        first = d['sessions'][0]
        middle = json.loads(json.dumps(first).replace('2026-01-05','2026-01-06').replace('2026-01-04','2026-01-05'))
        last = json.loads(json.dumps(first).replace('2026-01-05','2026-01-07').replace('2026-01-04','2026-01-06'))
        if denied: middle = dict(account_date='2026-01-06', permission='DENIED', denial_reason='synthetic')
        d['sessions'] += [middle, last]
    rewrite(manifest, 'schedule', schedule, monkeypatch)
    def source(d):
        last = json.loads(json.dumps(d['sessions'][0]).replace('2026-01-05','2026-01-07'))
        # All subsequent sessions must cover their 18:00 ET opening.
        from datetime import datetime
        start = datetime(2026,1,6,23,tzinfo=timezone.utc)
        template = last['bars'][0]
        last['bars'] = [dict(utc=(start+timedelta(minutes=15*i)).isoformat(), legs=template['legs']) for i in range(88)]
        d['sessions'] += [dict(account_date='2026-01-06', bars=[]), last]
        if not denied: d['data_exclusions'] = [dict(account_date='2026-01-06',leg=LEG_IDS[0],reason='missing_active_bar')]
    rewrite(manifest, 'source_bundle', source, monkeypatch)
    strategies = adapters(signal)
    calls, factories, snapshots = [], [], {}
    for a in strategies.values(): a.sentinel = ['persistent']
    def factory(envelope):
        factories.append(envelope)
        return strategies
    def observe(leg, close, strategy):
        assert strategy is strategies[leg]
        assert strategy.sentinel == ['persistent']
        if close is None:
            assert strategy.__dict__ == snapshots[leg]
        else:
            # Bars and feedback records are immutable. deepcopy would cache
            # __slotnames__ on their classes and corrupt later integrity checks.
            snapshots[leg] = {key: list(value) if isinstance(value, list) else value
                              for key, value in strategy.__dict__.items()}
        calls.append((leg, close))
    p.run_personal_replay(manifest, adapter_factory=factory, bar_observer=observe)
    assert len(factories) == 1
    assert all(frozenset(vars(cls)) == keys for cls, keys in namespaces.items())
    assert [leg for leg, close in calls if close is None] == list(LEG_IDS)
    assert calls[16:20] == [(leg, None) for leg in LEG_IDS]
    assert len(calls) == (4+88+1)*4
    import ast
    tree = ast.parse(Path(p.__file__).read_text())
    assert not [n for n in ast.walk(tree) if isinstance(n, ast.Attribute) and n.attr in
                ('reset', 'clear', '__init__', '__dict__')]
