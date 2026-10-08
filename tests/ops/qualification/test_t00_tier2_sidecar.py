"""T00 Tier-2 attribution sidecar (card 2026-10-08 §3.3-§3.4; admission addendum items 2 and 4).

Synthetic fixtures and TEST_ONLY keys only: the sidecar changes no sealed output, is served only
under the diagnostic evidence class, reconciles to the combined record, and the diagnostic receipt
stays a sealed, non-qualification, non-screen ValidatedSourceContract.
"""
import json
import os
import shutil

import pytest

from c1_signal_daemon.book_protocol import FillTiming, OrderIntent, Side
from c1_rail.qualification.contract import (
    DIAGNOSTIC_EVIDENCE_CLASS, DIAGNOSTIC_PURPOSE, DIAGNOSTIC_SCOPE, SOURCE_EVIDENCE_CLASS, SOURCE_REFUSALS,
    ValidatedSourceContract, canonical_json_bytes,
)
from c1_rail.qualification.replay import LOT_KINDS, Instrument, ReplayDeadlineFailure
from c1_rail.book_policy import BOOK_LEGS
from mc.simulation import EvaluationState
from test_replay import PartialBroker, engine, entry, first_entry, path_session, striker_entry_then_add
from test_source_contract import NOW, _held_orb, build_source_case, refused

GIT = pytest.mark.skipif(shutil.which('git') is None, reason='the screen authority needs git')
SCREEN = pytest.mark.skipif(os.name != 'nt' or shutil.which('git') is None,
                            reason='the screen gate needs git and the msvcrt run lock')
FLAT3 = [(100, 100, 100, 100)] * 3


# ---- BookReplay level: synthetic scenarios ----------------------------------------------------

def _striker_add(a, b):
    if len(a.bars) == 1:
        return entry(a, b)
    if len(a.bars) == 2:
        return [OrderIntent('add', a.leg_id, 'add', Side.BUY, 1, timing=FillTiming.THIS_CLOSE)]
    return []


def _aegis_at(n):
    return lambda a, b: entry(a, b, side=Side.SELL) if len(a.bars) == n else []


def _partial_takeover(replay):
    normal = replay._flatten

    def partial(k, bar, reason):
        if reason == 'capacity_takeover_close':
            replay._submit(k, [OrderIntent('partial', k, 'flat', Side.SELL, 1, timing=FillTiming.THIS_CLOSE,
                                           reason=reason)], bar)
        else:
            normal(k, bar, reason)
    replay._flatten = partial


def _withhold_flatten(replay):
    replay._flatten = lambda *args: None


def _last_close(session, instant, k):
    return dict(session.source.bars[-1].bars)[k].close


FEES = {s.leg_id: Instrument(1, 2, 0, 0.75) for s in BOOK_LEGS}
PROTECTED = EvaluationState(100000, 98000, 100000, 1, 0)


def _protected_sizing(k, a, p):
    return dict(lifecycle_tier='AUTHORIZED', **(dict(risk_dollars=700, per_contract_risk=4, cap_alloc=80)
                                                if k == 'dj30_mym_p250' else {}))


SCENARIOS = {
    'close_entry': (dict(emitters={'orb_mnq_v7': first_entry}), lambda: (path_session(),), None),
    'moving_fees_add': (dict(emitters={'dj30_mym_p250': striker_entry_then_add, 'orb_mnq_v7': first_entry},
                             instruments=FEES, quotes=_last_close),
                        lambda: (path_session(prices=[(100, 100, 100, 100), (100, 106, 94, 103), (103, 104, 90, 92)]),
                                 path_session(1, prices=[(92, 95, 88, 94), (94, 99, 93, 97)])), None),
    'takeover': (dict(emitters={'aegis_6j': _aegis_at(2), 'dj30_mym_p250': first_entry}),
                 lambda: (path_session(prices=FLAT3),), None),
    'protected_takeover_add': (dict(emitters={'dj30_mym_p250': _striker_add, 'aegis_6j': _aegis_at(3)},
                                    state=PROTECTED, sizing=_protected_sizing),
                               lambda: (path_session(prices=FLAT3 + FLAT3[:1]),), None),
    'partial_takeover_refused': (dict(emitters={'dj30_mym_p250': first_entry, 'aegis_6j': _aegis_at(2)}),
                                 lambda: (path_session(prices=FLAT3),), _partial_takeover),
    'mode_change': (dict(emitters={'orb_mnq_v7': lambda a, b: entry(a, b) if len(a.bars) % 3 == 1 else []},
                         instruments={s.leg_id: Instrument(1, 100, 0, 0) for s in BOOK_LEGS},
                         quotes=lambda *args: 80),
                    lambda: (path_session(prices=[(100, 100, 100, 100), (100, 100, 80, 80)]),
                             path_session(1, prices=[(100, 100, 100, 100), (100, 100, 80, 80)])), None),
    'partial_add': (dict(emitters={'dj30_mym_p250': striker_entry_then_add}, broker_factory=PartialBroker),
                    lambda: (path_session(prices=FLAT3),), None),
    'deadline': (dict(emitters={'orb_mnq_v7': first_entry}), lambda: (path_session(),), _withhold_flatten),
}


def _run(name, sidecar):
    kwargs, path, setup = SCENARIOS[name]
    replay, _ = engine(**kwargs)
    if setup is not None:
        setup(replay)
    if sidecar:
        replay.enable_attribution()
    try:
        result, failed = replay.run(path()), False
    except ReplayDeadlineFailure as exc:
        result, failed = exc.result, True
    return replay, result, failed


def _session_events(result):
    """Events split at each session_mode event (one per session, logged first)."""
    groups = []
    for event in result.events:
        if event.kind == 'session_mode':
            groups.append([])
        groups[-1].append(event)
    return groups


def _total(by_leg):
    return sum(by_leg[k][kind] for k in by_leg for kind in LOT_KINDS)


@pytest.mark.parametrize('name', sorted(SCENARIOS))
def test_sidecar_off_and_on_give_identical_replay_output(name):
    off_engine, off, off_failed = _run(name, False)
    _, on, on_failed = _run(name, True)
    assert off_engine._attribution is None
    assert on == off and on_failed is off_failed
    assert on.events == off.events and on.sessions == off.sessions


def _realized_by_leg_kind(replay, events, lots):
    """Realized P&L net of commission by (leg, lot kind), from fill events alone: an exit's P&L and
    commission belong to the lot named by its entry_fill_id (``lots`` carries across sessions)."""
    total = {(s.leg_id, kind): 0.0 for s in BOOK_LEGS for kind in LOT_KINDS}
    for event in events:
        if event.kind != 'fill':
            continue
        fill = json.loads(event.detail)
        if fill['kind'] in LOT_KINDS:
            lots[fill['fill_id']] = fill
            total[(event.leg_id, fill['kind'])] -= fill['commission']
            continue
        lot = lots[fill['entry_fill_id']]
        direction = 1 if lot['side'] == Side.BUY.value else -1
        realized = ((fill['price'] - lot['price']) * direction * fill['qty']
                    * replay.instruments[event.leg_id].pointvalue)
        total[(event.leg_id, lot['kind'])] += realized - fill['commission']
    return total


@pytest.mark.parametrize('name', sorted(SCENARIOS))
def test_per_leg_sums_reconcile_to_combined_record_and_fill_events(name):
    replay, result, _ = _run(name, True)
    sidecar = replay.attribution()
    assert len(sidecar) == len(result.sessions) == len(_session_events(result))
    lots = {}
    for row, record, events in zip(sidecar, result.sessions, _session_events(result)):
        assert (row['occurrence'], row['source_session_id']) == (record.occurrence, record.source_session_id)
        assert row['session_mode'] == events[0].detail
        assert _total(row['close']['cash']) == pytest.approx(record.pnl, abs=1e-9)
        low = row['low']
        assert low['value'] == record.intraday_low
        assert _total(low['cash']) + _total(low['mark']) == pytest.approx(record.intraday_low, abs=1e-9)
        fills = [(e.leg_id, json.loads(e.detail)) for e in events if e.kind == 'fill']
        assert _total(row['close']['commission']) == pytest.approx(sum(f['commission'] for _, f in fills))
        for k, leg in row['legs'].items():
            assert sum(row['close']['commission'][k].values()) == pytest.approx(
                sum(f['commission'] for leg_id, f in fills if leg_id == k))
            for kind in LOT_KINDS:
                assert leg['filled'][kind] == sum(f['qty'] for leg_id, f in fills if leg_id == k and f['kind'] == kind)
            refusals = [e.detail for e in events if e.kind == 'refused' and e.leg_id == k]
            assert [r['outcome'] for r in leg['requests'] if r['outcome'] != 'admitted'] == refusals
        expected = _realized_by_leg_kind(replay, events, lots)
        for k in row['legs']:
            for kind in LOT_KINDS:
                assert row['close']['cash'][k][kind] == pytest.approx(expected[(k, kind)], abs=1e-9), (k, kind)


def test_sidecar_records_policy_capacity_takeover_and_forced_closes():
    replay, _, _ = _run('takeover', True)
    legs = replay.attribution()[0]['legs']
    striker, aegis = legs['dj30_mym_p250'], legs['aegis_6j']
    assert striker['requests'][0] | {'capacity_before': None} == {
        'kind': 'entry', 'requested': 1, 'policy': 20, 'admitted': 20, 'outcome': 'admitted',
        'lifecycle_tier': 'AUTHORIZED', 'capacity_before': None, 'capacity_reason': 'within cap',
        'micro_requested': 20, 'cap_only_policy': 22, 'cap_binds': False,
        'sizing_inputs': {'cap_alloc': '80', 'per_contract_risk': '35', 'risk_dollars': '700'}}
    assert aegis['requests'][0]['takeover'] | {'reason': None} == {
        'displaced': ['dj30_mym_p250'], 'cancel_acked': ['dj30_mym_p250'], 'admitted': True, 'reason': None}
    assert (aegis['takeovers_won'], striker['takeovers_displaced'], aegis['capacity_refusals']) == (1, 1, 0)
    assert striker['forced_closes']['capacity_takeover_close'] | {'pnl': 0.0} == {
        'count': 1, 'qty': 20, 'pnl': 0.0, 'commission': 0.0}

    replay, _, _ = _run('partial_takeover_refused', True)
    legs = replay.attribution()[0]['legs']
    assert (legs['aegis_6j']['takeovers_refused'], legs['aegis_6j']['capacity_refusals']) == (1, 1)

    replay, _, _ = _run('close_entry', True)
    assert replay.attribution()[0]['legs']['orb_mnq_v7']['forced_closes']['scheduled_flatten']['count'] == 1


def test_cap_term_is_recorded_from_the_production_call():
    replay, _, _ = _run('takeover', True)            # risk term 700/35 = 20 under the cap term
    row = replay.attribution()[0]['legs']['dj30_mym_p250']['requests'][0]
    assert (row['policy'], row['cap_only_policy'], row['cap_binds']) == (20, 22, False)
    replay, _, _ = _run('protected_takeover_add', True)   # risk term above the cap term
    rows = replay.attribution()[0]['legs']['dj30_mym_p250']['requests']
    assert (rows[0]['policy'], rows[0]['cap_only_policy'], rows[0]['cap_binds']) == (22, 22, True)
    assert 'cap_binds' not in rows[1]                      # adds have no cap term
    replay, _, _ = _run('close_entry', True)               # fixed-size leg: not recorded
    assert 'cap_binds' not in replay.attribution()[0]['legs']['orb_mnq_v7']['requests'][0]


def test_deadline_failure_records_each_legs_open_quantity():
    replay, result, failed = _run('deadline', True)
    rows = replay.attribution()
    assert failed and rows[-1]['low']['where'] in ('open', 'segment', 'bar_close', 'deadline')
    opened = rows[-1]['open_at_deadline']
    edge = dict(result.sessions[-1].end_edge.positions)
    assert {k: v['position'] for k, v in opened.items()} == edge and edge['orb_mnq_v7'] > 0
    assert opened['orb_mnq_v7']['lots'] == {'entry': edge['orb_mnq_v7'], 'add': 0}
    assert all(v['position'] == 0 for k, v in opened.items() if k != 'orb_mnq_v7')
    replay, _, _ = _run('close_entry', True)               # twin: a settled session has none
    assert 'open_at_deadline' not in replay.attribution()[0]


def test_protected_adds_are_attributed_by_lot_kind():
    replay, result, _ = _run('protected_takeover_add', True)
    row = replay.attribution()[0]
    striker = row['legs']['dj30_mym_p250']
    assert row['session_mode'] == 'protected'
    assert (striker['filled'], striker['fills']) == ({'entry': 22, 'add': 55}, {'entry': 1, 'add': 1})
    assert [r['policy'] for r in striker['requests']] == [22, 55]
    assert 'sizing_inputs' in striker['requests'][0] and 'sizing_inputs' not in striker['requests'][1]
    replay, _, _ = _run('moving_fees_add', True)
    rows = replay.attribution()
    assert any(r['close']['cash']['dj30_mym_p250']['add'] != 0 for r in rows)
    assert any(r['low']['mark']['dj30_mym_p250']['add'] != 0 or r['low']['cash']['dj30_mym_p250']['add'] != 0
               for r in rows)


def test_sidecar_is_off_by_default_and_must_be_enabled_before_the_run():
    replay, _, _ = _run('close_entry', False)
    with pytest.raises(ValueError, match='not enabled'):
        replay.attribution()
    with pytest.raises(ValueError, match='before the single run'):
        replay.enable_attribution()


def test_sidecar_result_is_a_detached_copy():
    replay, _, _ = _run('close_entry', True)
    first = replay.attribution()
    first[0]['legs'].clear()
    assert replay.attribution()[0]['legs']


# ---- contract: purpose, scope and evidence class ----------------------------------------------

def _diagnostic_bytes(case):
    return canonical_json_bytes({**case.document, 'purpose': DIAGNOSTIC_PURPOSE})


def _diagnostic(case):
    raw = _diagnostic_bytes(case)
    return case.validate(contract_bytes=raw, approval=case.approval(scope=DIAGNOSTIC_SCOPE, subject=raw))


@pytest.fixture
def case(tmp_path, monkeypatch):
    from c1_rail.qualification import production_source
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    return build_source_case(tmp_path, monkeypatch)


def test_each_scope_accepts_only_its_own_contract(case):
    receipt = _diagnostic(case)
    assert type(receipt) is ValidatedSourceContract and receipt.evidence_class == DIAGNOSTIC_EVIDENCE_CLASS
    assert case.validate().evidence_class == SOURCE_EVIDENCE_CLASS                               # twin
    raw = _diagnostic_bytes(case)
    refused('approval scope does not match', lambda: case.validate(
        contract_bytes=raw, approval=case.approval(scope='APPROVE_T00_SOURCE_CONTRACT', subject=raw)))
    refused('approval scope does not match', lambda: case.validate(approval=case.approval(scope=DIAGNOSTIC_SCOPE)))


@pytest.mark.parametrize('purpose', ['T00_DIAGNOSTIC', ['T00_DIAGNOSTIC_ATTRIBUTION'], None])
def test_unknown_or_non_text_purpose_is_refused(case, purpose):
    raw = canonical_json_bytes({**case.document, 'purpose': purpose})
    refused('SOURCE_CONTRACT_FIELDS', lambda: case.validate(
        contract_bytes=raw, approval=case.approval(scope=DIAGNOSTIC_SCOPE, subject=raw)))


def test_diagnostic_refusals_are_the_source_refusals(case):
    assert {'SCREEN', 'MONTE_CARLO', 'DECISION_RULES'} <= set(SOURCE_REFUSALS)
    raw = canonical_json_bytes({**case.document, 'purpose': DIAGNOSTIC_PURPOSE,
                                'refusals': [r for r in SOURCE_REFUSALS if r != 'SCREEN']})
    refused('SOURCE_CONTRACT_FIELDS', lambda: case.validate(
        contract_bytes=raw, approval=case.approval(scope=DIAGNOSTIC_SCOPE, subject=raw)))


# ---- ProductionSource: the gated method ---------------------------------------------------------

def _path(source, n=3):
    from c1_rail.qualification.paths import PathAssembler
    return PathAssembler(source.path_start_date).assemble((source.sessions[:n],), horizon_sessions=n)


def _spy_engine(monkeypatch):
    from c1_rail.qualification.production_source import ProductionSource
    calls, real = [], ProductionSource._engine

    def spy(self, schedule_quotes):
        calls.append(real(self, schedule_quotes))
        return calls[-1]
    monkeypatch.setattr(ProductionSource, '_engine', spy)
    return calls


def test_diagnostic_source_is_sealed_and_sidecar_leaves_sealed_output_identical(tmp_path, monkeypatch):
    from c1_rail.qualification import production_source
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    _held_orb(monkeypatch)
    case = build_source_case(tmp_path, monkeypatch)
    source = production_source.ProductionSource.build(_diagnostic(case), artifact_root=case.root)
    assert source.evidence_class == DIAGNOSTIC_EVIDENCE_CLASS
    path = _path(source)
    plain = source.replay_bracket(path)
    engines = _spy_engine(monkeypatch)
    side = source.replay_bracket_with_sidecar(path)
    assert type(plain) is type(side.bracket) is production_source.SourceOnlyBracket
    assert side.bracket == plain and side.schema == 't00_tier2_attribution/v1'
    for name in ('r1', 'r2'):
        sealed, other = getattr(side.bracket, name), getattr(plain, name)
        assert (sealed.sessions, sealed.events_sha256, sealed.consumed_intrabar_splits, sealed.deadline_failure) == (
            other.sessions, other.events_sha256, other.consumed_intrabar_splits, other.deadline_failure)
        assert sealed.evidence_class == DIAGNOSTIC_EVIDENCE_CLASS and sealed.consumed_intrabar_splits
        rows = getattr(side, name)
        assert len(rows) == len(sealed.sessions)
        for row, record in zip(rows, sealed.sessions):
            assert _total(row['close']['cash']) == pytest.approx(record.pnl, abs=1e-9)
            assert row['low']['value'] == record.intraday_low
    assert len(engines) == 2 and [e.schedule_quotes.run for e in engines] == ['R1', 'R2']
    assert all(e._attribution is not None for e in engines)
    assert type(source.replay(path)) is production_source.SourceOnlyReplay
    refused('SOURCE_ONLY_NOT_QUALIFICATION', lambda: source.verify_for(source.contract))


def test_sidecar_is_refused_under_the_source_class_before_any_engine(case, monkeypatch):
    from c1_rail.qualification import production_source
    source = production_source.ProductionSource.build(case.validate(), artifact_root=case.root)
    engines = _spy_engine(monkeypatch)
    refused('DIAGNOSTIC_SIDECAR_REFUSED', lambda: source.replay_bracket_with_sidecar(_path(source)))
    assert engines == []
    assert type(source.replay_bracket(_path(source))) is production_source.SourceOnlyBracket   # twin


def test_sidecar_is_refused_for_a_qualification_source(tmp_path):
    from composition_fixture import build_verified_composition
    source = build_verified_composition(tmp_path / 'f1').source
    refused('DIAGNOSTIC_SIDECAR_REFUSED', lambda: source.replay_bracket_with_sidecar(()))


def test_a_relabelled_diagnostic_receipt_is_not_served(case, monkeypatch):
    """A source-class receipt and source relabelled in place are refused before any engine."""
    from c1_rail.qualification import production_source
    receipt = case.validate()
    source = production_source.ProductionSource.build(receipt, artifact_root=case.root)
    object.__setattr__(receipt, 'evidence_class', DIAGNOSTIC_EVIDENCE_CLASS)
    object.__setattr__(source, 'evidence_class', DIAGNOSTIC_EVIDENCE_CLASS)
    engines = _spy_engine(monkeypatch)
    with pytest.raises(ValueError, match='changed'):
        source.replay_bracket_with_sidecar(_path(source))
    assert engines == []


def test_p7_driver_refuses_a_diagnostic_receipt(tmp_path, monkeypatch):
    import base64
    from c1_rail.qualification import p7_driver, p7_evidence, production_source
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    case = build_source_case(tmp_path / 'case', monkeypatch)
    raw = _diagnostic_bytes(case)
    files = {'registry': json.dumps({k: base64.b64encode(v).decode() for k, v in case.public_keys.items()}),
             'path': json.dumps({'sessions': list(case.document['populations']['FULL'][:2])})}
    for name, text in files.items():
        (tmp_path / name).write_text(text, encoding='utf-8')

    def run(contract, approval):
        (tmp_path / 'contract').write_bytes(contract)
        (tmp_path / 'approval').write_bytes(approval)
        argv = ['code', tmp_path / 'contract', tmp_path / 'approval', tmp_path / 'registry', case.root,
                tmp_path / 'path', 'out']
        return p7_driver._run(p7_evidence, [str(a) for a in argv])
    with pytest.raises(p7_evidence.P7Refusal, match='P7_PURPOSE_MISMATCH'):
        run(raw, case.approval(scope=DIAGNOSTIC_SCOPE, subject=raw))
    # Twin: a source receipt passes the class check and reaches the replay (then the absent
    # bootstrap recorder, which only the pinned bootstrap supplies).
    with pytest.raises(AttributeError, match='ports'):
        run(case.contract_bytes(), case.approval())


@GIT
def test_screen_authority_class_check_holds_even_if_the_r3c_pin_named_the_diagnostic_digest(
        tmp_path, monkeypatch):
    from test_screen_authority import Screen
    from c1_rail.qualification import screen_authority
    screen = Screen(tmp_path, monkeypatch)
    auth = screen.validate()
    diagnostic = _diagnostic(screen.case)
    source = screen.receipt
    # Site 1 (validation): the pin and the document both name the diagnostic digest.
    screen.receipt = diagnostic
    doc = {**screen.authority, 'source': {'contract_sha256': diagnostic.contract_sha256}}
    with pytest.raises(screen_authority.ScreenAuthorityError, match='source evidence class'):
        screen.validate(doc=doc, receipt=diagnostic)
    # Site 2 (every use): the bound receipt relabelled in place is refused by the class term
    # before the receipt's own snapshot check; twin: unrelabelled, the source checks pass.
    screen.receipt = source
    screen.patch()
    with pytest.raises(screen_authority.ScreenAuthorityError, match='SCREEN_BOOTSTRAP_MISMATCH'):
        screen_authority.require_validated_screen_authority(auth, source_contract=source, now=NOW)
    object.__setattr__(source, 'evidence_class', DIAGNOSTIC_EVIDENCE_CLASS)
    with pytest.raises(screen_authority.ScreenAuthorityError, match='SCREEN_SOURCE_MISMATCH'):
        screen_authority.require_validated_screen_authority(auth, source_contract=source, now=NOW)


@GIT
def test_screen_authority_refuses_a_diagnostic_receipt(tmp_path, monkeypatch):
    from test_screen_authority import Screen
    from c1_rail.qualification import screen_authority
    screen = Screen(tmp_path, monkeypatch)
    auth = screen.validate()
    diagnostic = _diagnostic(screen.case)
    with pytest.raises(screen_authority.ScreenAuthorityError, match='SCREEN_SOURCE_MISMATCH'):
        screen_authority.require_validated_screen_authority(auth, source_contract=diagnostic, now=NOW)
    with pytest.raises(screen_authority.ScreenAuthorityError, match='SCREEN_SOURCE_MISMATCH'):
        screen.validate(receipt=diagnostic)


@SCREEN
def test_screen_bracket_engines_carry_no_sidecar(tmp_path, monkeypatch):
    from test_production_source import _ready, _screen
    from c1_rail.qualification import screen_authority
    screen, auth, source, path = _screen(tmp_path, monkeypatch)
    engines = _spy_engine(monkeypatch)
    with _ready(screen, auth):
        epoch = screen_authority.screen_epoch(source, authority=auth)
        result = screen_authority.screen_bracket(source, path, authority=auth, epoch=epoch)
    assert len(engines) == 2 and all(e._attribution is None for e in engines)
    assert not any('sidecar' in name or 'attribution' in name for name in vars(result))
    refused('DIAGNOSTIC_SIDECAR_REFUSED', lambda: source.replay_bracket_with_sidecar(path))


def test_replay_bracket_with_sidecar_does_not_change_the_sealed_functions():
    from test_production_source import SEALED_SOURCE_SHA256, _sealed_source_sha256
    assert _sealed_source_sha256() == SEALED_SOURCE_SHA256
