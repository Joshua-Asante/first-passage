import ast
from contextlib import contextmanager
import hashlib
import json
import os
import shutil
import sys

import pytest

from c1_rail.qualification.production_source import (
    ProductionSource, ProductionSourceNeedsContext, decode_admitted_csv, parse_historical_admission,
    port_active_window, request_sizing_inputs,
    parse_startup_policy,
    parse_source_calendar,
    parse_schedule_execution_evidence,
    parse_population_index,
)


def index_binding():
    from c1_rail.qualification.model import LEG_IDS
    return {'panel_sha256':{leg:'a'*64 for leg in LEG_IDS}, 'port_sha256':{leg:'b'*64 for leg in LEG_IDS},
            'effective_settings_sha256':'c'*64, 'source_calendar_sha256':'d'*64,
            'slot_presence_rule':'QUALIFIED_GENERATION_UNION'}


def slot_provenance(slots):
    from c1_rail.qualification.model import LEG_IDS
    return {day:[{'instant':instant,'state':'PROVIDER_PRESENT','present_legs':list(LEG_IDS)} for instant in values]
            for day,values in slots.items()}


def test_csv_parses_exact_immutable_admitted_bytes_and_rejects_substitution():
    raw = b'time,open,high,low,close,volume\n2022-09-01T00:00:00Z,1,2,1,2,3\n'
    digest = hashlib.sha256(raw).hexdigest()
    bars = decode_admitted_csv(raw, digest)
    assert len(bars) == 1 and bars[0].close == 2
    with pytest.raises(ValueError, match='digest'):
        decode_admitted_csv(raw.replace(b',3', b',4'), digest)


def test_csv_epoch_or_naive_time_is_not_silently_reinterpreted():
    for timestamp in ('1661990400', '2022-09-01T00:00:00'):
        raw = f'time,open,high,low,close,volume\n{timestamp},1,2,1,2,3\n'.encode()
        with pytest.raises(ValueError):
            decode_admitted_csv(raw, hashlib.sha256(raw).hexdigest())


def admission():
    cases = {name: {'panel_sha256': 'a'*64, 'port_sha256': 'b'*64} for name in
             ('O-N', 'O-P', 'S-P', 'S-W1', 'S-W1P', 'S-W2', 'S-W2P', 'aegis_6j', 'vanguard_mgc')}
    raw = json.dumps({'schema': 'packet1-step3-evidence-admission-v1', 'review_status': 'PENDING_INDEPENDENT_REVIEW',
                      'cases': cases, 'interval_utc': ['2022-09-01T00:00:00Z', '2026-09-03T00:00:00Z'],
                      'evidence_index_sha256': 'c'*64}).encode()
    review = json.dumps({'schema': 'packet1-step3-review-approval-v1', 'decision': 'ACCEPTED',
                         'accepted_contract_sha256': hashlib.sha256(raw).hexdigest(), 'evidence_index_v4_sha256': 'c'*64}).encode()
    return raw, review


def test_separate_acceptance_preserves_pending_historical_receipt():
    raw, review = admission()
    parsed = parse_historical_admission(raw, review)
    assert dict(parsed.panels)['aegis_6j'] == 'a'*64
    assert parsed.interval_start.isoformat() == '2022-09-01T00:00:00+00:00'
    with pytest.raises(ValueError, match='review'):
        parse_historical_admission(raw, review.replace(b'ACCEPTED', b'PENDING'))


def test_source_cannot_be_caller_constructed_or_faked_by_synthetic_provider():
    with pytest.raises(ProductionSourceNeedsContext, match='concrete'):
        ProductionSource()


def test_accepted_port_windows_keep_striker_utc_and_vanguard_weekdays():
    from datetime import datetime, timezone
    from types import SimpleNamespace
    params = SimpleNamespace(use_session=True, sess_start_min=540, sess_end_min=1019)
    # Striker starts at 13UTC in both DST seasons, independently of ET.
    assert port_active_window('dj30_mym_p250', datetime(2024, 1, 2, 13, tzinfo=timezone.utc), params)
    assert not port_active_window('dj30_mym_p250', datetime(2024, 7, 2, 17, tzinfo=timezone.utc), params)
    assert not port_active_window('vanguard_mgc', datetime(2024, 7, 6, 15, tzinfo=timezone.utc), params)
    assert port_active_window('vanguard_mgc', datetime(2024, 7, 5, 15, tzinfo=timezone.utc), params)


def test_sizing_uses_unrounded_risk_stop_and_explicit_frozen_lifecycle_cap():
    from types import SimpleNamespace
    params = SimpleNamespace(account_size=100000., risk_per_trade_pct=.7, point_value=.5)
    action = SimpleNamespace(stop_dist_pts=70., qty=20)
    actual = request_sizing_inputs('dj30_mym_p250', action, params,
                                   lifecycle_tier='WATCH-1', cap_alloc=80)
    assert actual == {'lifecycle_tier': 'WATCH-1', 'risk_dollars': 700., 'per_contract_risk': 35., 'cap_alloc': 80}
    with pytest.raises(ValueError):
        request_sizing_inputs('dj30_mym_p250', action, params, lifecycle_tier=None, cap_alloc=80)
    # Adds derive only from the engine's confirmed base, not a recalculated stop.
    add = SimpleNamespace(kind='add', stop_dist_pts=0., qty=1)
    assert request_sizing_inputs('dj30_mym_p250', add, params, lifecycle_tier='AUTHORIZED', cap_alloc=80) == {'lifecycle_tier':'AUTHORIZED'}


def test_startup_policy_requires_every_proposed_field_and_refuses_splice_reset():
    from c1_rail.qualification.model import LEG_IDS
    plan = {'schema': 'qualification-source-startup/v1', 'initialization': 'FRESH_ONCE_CONTINUOUS',
            'positions': 'ZERO', 'working_orders': 'ZERO', 'splice_behavior': 'CARRY_ALL_STATE',
            'path_start_date': '2030-01-07', 'shared_account_cap_micro_equivalents': 80,
            'legs': {leg: {'paper_initial_capital': '100000', 'lifecycle_tier': 'AUTHORIZED',
                           'request_cap_micro_equivalents': 80} for leg in LEG_IDS}}
    parsed = parse_startup_policy(json.dumps(plan).encode())
    assert parsed.path_start_date.isoformat() == '2030-01-07'
    assert dict(parsed.paper_initial_capitals)['aegis_6j'] == 100000
    plan['splice_behavior'] = 'RESET_TO_SOURCE_SNAPSHOT'
    with pytest.raises(ValueError):
        parse_startup_policy(json.dumps(plan).encode())
    del plan['shared_account_cap_micro_equivalents']
    with pytest.raises(ValueError):
        parse_startup_policy(json.dumps(plan).encode())


def test_calendar_derives_earliest_v_and_preserves_unknown_vs_policy_denial():
    from c1_rail.qualification.model import LEG_IDS
    from c1_rail.qualification.clock import SourceDayStatus
    from datetime import date
    refs = {'hours': 'a'*64}
    fact = {'role': 'hours', 'sha256': 'a'*64}
    rows = [{'date': '2024-01-02', 'status': 'OPEN', 'reason': 'source-backed hours',
             'facts': [fact], 'venue_deadlines': {leg: {'instant': '2024-01-02T17:59:00Z', 'fact': fact} for leg in LEG_IDS}},
            {'date': '2024-01-03', 'status': 'policy_denied', 'reason': 'operator restriction', 'facts': [fact], 'venue_deadlines': {}},
            {'date': '2024-01-04', 'status': 'unknown', 'reason': 'unresolved source date', 'facts': [fact], 'venue_deadlines': {}}]
    raw = json.dumps({'schema': 'qualification-source-calendar/v1', 'coverage_start': '2024-01-02',
                      'coverage_end': '2024-01-04', 'tail_covered': False, 'sessions': rows}).encode()
    clock, tail = parse_source_calendar(raw, artifact_digests=refs)
    assert clock.schedule_for(date(2024, 1, 2)).own_flat_deadline.isoformat() == '2024-01-02T17:44:00+00:00'
    assert clock.disposition_for(date(2024, 1, 3)).status is SourceDayStatus.POLICY_DENIED
    assert clock.disposition_for(date(2024, 1, 4)).status is SourceDayStatus.UNKNOWN
    assert tail is False
    with pytest.raises(ValueError, match='fact'):
        parse_source_calendar(raw, artifact_digests={'hours':'b'*64})


def test_schedule_segments_reuse_replay_path_validation_and_require_exact_price():
    from datetime import datetime, timezone, date, timedelta
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import PathBar, SourceBar, SourceSession, SessionSchedule
    from c1_rail.qualification.replay import ReplayNeedsContext
    ts = datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc)
    split = ts + timedelta(minutes=10)
    values = {'open': 100., 'high': 100., 'low': 100., 'close': 100., 'volume': 0.}
    row = {'source_session_date': '2024-01-02', 'leg_id': 'aegis_6j', 'source_bar_time': ts.isoformat(),
           'interval_start': ts.isoformat(), 'instant': split.isoformat(), 'price': 100., 'prefix': values, 'suffix': values}
    raw = json.dumps({'schema': 'qualification-schedule-execution/v1', 'rows': [row]}).encode()
    evidence = parse_schedule_execution_evidence(raw)
    bar = Bar(ts, **values)
    source = SourceSession('2024-01-02', date(2024, 1, 2), (SourceBar(ts, (('aegis_6j', bar),)),),
                           SessionSchedule(ts, split, ts+timedelta(minutes=15)))
    from c1_rail.qualification.paths import PathAssembler
    path = PathAssembler(date(2030, 1, 7)).assemble(((source,),), horizon_sessions=1)
    splits = evidence.validate_split(path[0], path[0].bars[0], {'aegis_6j': bar}, split)
    assert splits['aegis_6j'].suffix.ts == split and splits['aegis_6j'].prefix_executes is True
    row['price'] = 101.
    bad = parse_schedule_execution_evidence(json.dumps({'schema': 'qualification-schedule-execution/v1', 'rows': [row]}).encode())
    with pytest.raises(ReplayNeedsContext, match='price'):
        bad.validate_split(path[0], path[0].bars[0], {'aegis_6j': bar}, split)


def test_factory_rejects_unverified_contract_before_loading_ports(tmp_path):
    with pytest.raises(ValueError,match='G1'):
        ProductionSource.build(object(),artifact_root=tmp_path)


def test_signed_fixture_factory_wires_fresh_adapters_and_continuous_proof(tmp_path):
    from composition_fixture import build_verified_composition
    from c1_rail.qualification.paths import PathAssembler
    verified=build_verified_composition(tmp_path)
    source=verified.source
    source.verify_for(verified.contract)
    before=verified.current_loaded_modules()
    path=PathAssembler(source.path_start_date).assemble(((source.sessions[1],),(source.sessions[0],),(source.sessions[1],)),horizon_sessions=3)
    replay=source.replay(path)
    assert len(replay.sessions)==3
    after=verified.current_loaded_modules()
    assert after['orb_runtime_port'] is not before['orb_runtime_port']
    edges,adjacent=source.proof((source.sessions[1],source.sessions[0]))
    assert len(edges)==3 and all(edge.is_flat for edge in edges) and adjacent==(True,)


def test_missing_retained_file_is_precise_context_gap_and_path_escape_refuses(tmp_path):
    from types import SimpleNamespace
    from c1_rail.qualification.production_source import _read_retained_artifacts
    with pytest.raises(ProductionSourceNeedsContext) as error:
        _read_retained_artifacts((SimpleNamespace(path='missing.csv', role='aegis_panel'),), tmp_path)
    assert error.value.gaps[0].code == 'RETAINED_ARTIFACT_MISSING'
    with pytest.raises(ValueError, match='escapes'):
        _read_retained_artifacts((SimpleNamespace(path='../escape.csv', role='aegis_panel'),), tmp_path)


def test_population_index_prevents_calendar_omission_and_reconstructs_exclusions():
    from datetime import date
    from types import SimpleNamespace
    from c1_rail.qualification.panel import Exclusion
    populations = {'FULL':('2024-01-02','2024-01-04'),'H1':('2024-01-02',),'H2':('2024-01-04',)}
    doc = {'schema':'qualification-population-index/v1',
           'expected_source_dates':['2024-01-02','2024-01-03','2024-01-04'],
           'expected_source_slots':{f'2024-01-{day:02}':[f'2024-01-{day:02}T15:00:00Z'] for day in (2,3,4)},
           'populations':{key:list(value) for key,value in populations.items()},
           'expected_exclusions':[{'source_date':'2024-01-03','reason':'policy_denied','detail':'frozen restriction'}]}
    doc.update(source_binding=index_binding(),slot_provenance=slot_provenance(doc['expected_source_slots']))
    index = parse_population_index(json.dumps(doc).encode(), populations=populations)
    complete = SimpleNamespace(schedules=tuple((date(2024,1,d),object()) for d in (2,3,4)))
    index.validate_calendar(complete)
    with pytest.raises(ValueError, match='calendar'):
        index.validate_calendar(SimpleNamespace(schedules=(complete.schedules[0],complete.schedules[-1])))
    sessions = tuple(SimpleNamespace(session_id=f'2024-01-{d:02}',source_session_date=date(2024,1,d)) for d in (2,4))
    exclusions = (Exclusion(date(2024,1,3),'policy_denied','frozen restriction'),)
    index.validate_coverage(sessions,exclusions)
    with pytest.raises(ValueError, match='exclusion'):
        index.validate_coverage(sessions,())
    with pytest.raises(ValueError, match='exclusion'):
        index.validate_coverage(sessions,(Exclusion(date(2024,1,3),'exchange_closed','frozen restriction'),))


def test_population_index_cannot_rename_deadline_failure_as_source_exclusion():
    populations = {'FULL':('2024-01-02',),'H1':('2024-01-02',),'H2':()}
    doc = {'schema':'qualification-population-index/v1', 'expected_source_dates':['2024-01-02','2024-01-03'],
           'expected_source_slots':{f'2024-01-{day:02}':[f'2024-01-{day:02}T15:00:00Z'] for day in (2,3)},
           'populations':{key:list(value) for key,value in populations.items()},
           'expected_exclusions':[{'source_date':'2024-01-03','reason':'own_flat_deadline','detail':'late'}]}
    doc.update(source_binding=index_binding(),slot_provenance=slot_provenance(doc['expected_source_slots']))
    with pytest.raises(ValueError, match='exclusion'):
        parse_population_index(json.dumps(doc).encode(), populations=populations)


def test_missing_fact_role_with_null_digest_cannot_claim_retained_provenance():
    from c1_rail.qualification.production_source import _fact
    for reference in ({'role':'unretained','sha256':None}, {'role':'','sha256':'a'*64},
                      {'role':'hours','sha256':'A'*64}, {'role':'hours','sha256':'short'}):
        with pytest.raises(ValueError, match='fact'):
            _fact(reference, {})


def test_striker_exact_risk_boundary_is_not_rounded_up_through_float():
    from decimal import Decimal
    from types import SimpleNamespace
    from c1_rail.book_policy import entry_quantities, candidate_book_protection_policy
    from c1_signal_daemon.book_protocol import Mode
    params=SimpleNamespace(account_size=Decimal('124.999999999999999999'),risk_per_trade_pct=Decimal('100'),point_value=Decimal('1'))
    action=SimpleNamespace(kind='entry',stop_dist_pts=Decimal('10'))
    values=request_sizing_inputs('dj30_mym_p250',action,params,lifecycle_tier='AUTHORIZED',cap_alloc=80)
    assert type(values['risk_dollars']) is Decimal
    assert entry_quantities('dj30_mym_p250',mode=Mode.PROTECTED,policy=candidate_book_protection_policy(),**values)[0]==4
    params.account_size=Decimal('125')
    values=request_sizing_inputs('dj30_mym_p250',action,params,lifecycle_tier='AUTHORIZED',cap_alloc=80)
    assert entry_quantities('dj30_mym_p250',mode=Mode.PROTECTED,policy=candidate_book_protection_policy(),**values)[0]==5
    params.account_size=Decimal('-1')
    with pytest.raises(ValueError,match='positive'):
        request_sizing_inputs('dj30_mym_p250',action,params,lifecycle_tier='AUTHORIZED',cap_alloc=80)


def test_provider_shared_absence_stays_diagnostic_but_consumed_omission_is_corruption():
    from datetime import datetime, date, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import LEG_IDS, SessionSchedule
    from c1_rail.qualification.panel import build_panel
    times = [f'2024-01-02T{hour}:00:00Z' for hour in ('00','15','16')]
    populations = {'FULL':['2024-01-02'],'H1':['2024-01-02'],'H2':[]}
    slots = {'2024-01-02':times}
    provenance = slot_provenance(slots)
    provenance['2024-01-02'].insert(2,{'instant':'2024-01-02T15:15:00Z','state':'PROVIDER_SHARED_ABSENCE','present_legs':[]})
    doc = {'schema':'qualification-population-index/v1','expected_source_dates':['2024-01-02'],
           'expected_source_slots':slots,'slot_provenance':provenance,'source_binding':index_binding(),
           'populations':populations,'expected_exclusions':[]}
    index = parse_population_index(json.dumps(doc).encode(),populations=populations)
    bars = tuple(Bar(datetime.fromisoformat(t.replace('Z','+00:00')),1,1,1,1) for t in times)
    panels = tuple((leg,bars) for leg in LEG_IDS)
    index.validate_provider_generation(panels,expected_binding=index_binding())
    schedule = SessionSchedule(datetime(2024,1,2,20,45,tzinfo=timezone.utc),datetime(2024,1,2,20,55,tzinfo=timezone.utc),datetime(2024,1,2,21,tzinfo=timezone.utc))
    report = build_panel(dict(panels),schedules={date(2024,1,2):schedule},expected_dates=(date(2024,1,2),),active=lambda leg,ts:ts.hour>=15)
    assert len(report.sessions)==1 and len(report.sessions[0].bars)==3 and not report.exclusions
    index.validate_coverage(report.sessions,report.exclusions)
    # The retained out-of-window midnight bar stays; no 15:15 bar is fabricated.
    assert [row.source_bar_time.hour for row in report.sessions[0].bars]==[0,15,16]
    with pytest.raises(ValueError,match='provenance'):
        index.validate_provider_generation(tuple((leg,bars[:-1]) for leg in LEG_IDS),expected_binding=index_binding())


def test_one_leg_union_gap_excludes_only_when_that_leg_is_active():
    from datetime import datetime, date, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import LEG_IDS, SessionSchedule
    from c1_rail.qualification.panel import build_panel
    ts=datetime(2024,1,2,15,tzinfo=timezone.utc)
    bars=(Bar(ts,1,1,1,1),)
    panels={leg:bars for leg in LEG_IDS};panels[LEG_IDS[0]]=()
    schedule=SessionSchedule(ts.replace(hour=20,minute=45),ts.replace(hour=20,minute=55),ts.replace(hour=21))
    args=dict(schedules={date(2024,1,2):schedule},expected_dates=(date(2024,1,2),))
    missing=build_panel(panels,active=lambda leg,t:True,**args)
    assert not missing.sessions and missing.exclusions[0].reason=='missing_active_bar'
    inactive=build_panel(panels,active=lambda leg,t:leg!=LEG_IDS[0],**args)
    assert len(inactive.sessions)==1 and len(inactive.sessions[0].bars[0].bars)==3


def test_supplied_schedule_validation_accepts_no_unused_quotes_and_binds_source():
    from datetime import datetime, timezone
    from c1_signal_daemon.feed import Bar
    ts=datetime(2024,1,2,20,45,tzinfo=timezone.utc)
    panels=(('aegis_6j',(Bar(ts,100,100,100,100,0),)),)
    empty=parse_schedule_execution_evidence(json.dumps({'schema':'qualification-schedule-execution/v1','rows':[]}).encode())
    empty.validate_supplied(panels)
    row={'source_session_date':'2024-01-02','leg_id':'aegis_6j','source_bar_time':ts.isoformat(),
         'interval_start':ts.isoformat(),'instant':ts.isoformat(),'price':100,'prefix':None,'suffix':None}
    def evidence():
        return parse_schedule_execution_evidence(json.dumps({'schema':'qualification-schedule-execution/v1','rows':[row]}).encode())
    evidence().validate_supplied(panels)
    row['price']=101
    with pytest.raises(ValueError,match='quote'):
        evidence().validate_supplied(panels)
    row['price']=100;row['source_bar_time']=ts.replace(minute=30).isoformat();row['interval_start']=row['source_bar_time']
    with pytest.raises(ValueError,match='source'):
        evidence().validate_supplied(panels)


def test_supplied_contradictory_split_refuses_even_without_exposure():
    from datetime import datetime, timedelta, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.replay import ReplayNeedsContext
    ts=datetime(2024,1,2,20,45,tzinfo=timezone.utc)
    values=dict(open=100,high=100,low=100,close=100,volume=0)
    row={'source_session_date':'2024-01-02','leg_id':'aegis_6j','source_bar_time':ts.isoformat(),
        'interval_start':ts.isoformat(),'instant':(ts+timedelta(minutes=10)).isoformat(),
        'price':100,'prefix':values,'suffix':values|{'close':101,'high':101}}
    evidence=parse_schedule_execution_evidence(json.dumps({'schema':'qualification-schedule-execution/v1','rows':[row]}).encode())
    with pytest.raises(ReplayNeedsContext,match='aggregate'):
        evidence.validate_supplied((('aegis_6j',(Bar(ts,100,100,100,100,0),)),))


def test_signed_flat_source_builds_and_replays_without_unused_quotes(monkeypatch,tmp_path):
    """Customize generated inputs before signing; production functions stay real."""
    import composition_fixture as fixture_module
    from c1_rail.qualification.paths import PathAssembler
    original_builder=fixture_module.build_artifacts
    def empty_evidence(root, **kwargs):
        fixture=original_builder(root, **kwargs)
        role='schedule_execution_evidence'
        fixture.payloads[role]=fixture_module.encoded({'schema':'qualification-schedule-execution/v1','rows':[]})
        review=json.loads(fixture.payloads[role+'_review'])
        review['artifact_sha256']=hashlib.sha256(fixture.payloads[role]).hexdigest()
        fixture.payloads[role+'_review']=fixture_module.encoded(review)
        for name in (role,role+'_review'):
            (root/fixture.paths[name]).write_bytes(fixture.payloads[name])
        return fixture
    monkeypatch.setattr(fixture_module,'build_artifacts',empty_evidence)
    verified=fixture_module.build_verified_composition(tmp_path,idle=True)
    source=verified.source
    path=PathAssembler(source.path_start_date).assemble((source.sessions[:5],),horizon_sessions=5)
    replay=source.replay(path)
    assert len(replay.sessions)==5
    assert all(row.fills==0 and row.flat_before_deadline and row.end_edge.is_flat for row in replay.sessions)


def test_supplied_nested_split_requires_retained_anchor_and_consistent_suffix():
    from datetime import datetime,timedelta,timezone
    from c1_signal_daemon.feed import Bar
    ts=datetime(2024,1,2,20,45,tzinfo=timezone.utc)
    values=dict(open=100,high=100,low=100,close=100,volume=0)
    def row(start,instant):
        return dict(source_session_date='2024-01-02',leg_id='aegis_6j',source_bar_time=ts.isoformat(),
            interval_start=(ts+timedelta(minutes=start)).isoformat(),instant=(ts+timedelta(minutes=instant)).isoformat(),
            price=100,prefix=values,suffix=values)
    panels=(('aegis_6j',(Bar(ts,**values),)),)
    def evidence(rows):
        return parse_schedule_execution_evidence(json.dumps({'schema':'qualification-schedule-execution/v1','rows':rows}).encode())
    with pytest.raises(ValueError,match='anchor'):
        evidence([row(5,10)]).validate_supplied(panels)
    evidence([row(5,10),row(0,5)]).validate_supplied(panels)


def test_empty_reviewed_evidence_is_unused_when_flat_but_fails_when_consumed():
    from test_replay import engine,closing_session,first_entry
    from c1_rail.qualification.replay import ReplayNeedsContext
    evidence=parse_schedule_execution_evidence(json.dumps({'schema':'qualification-schedule-execution/v1','rows':[]}).encode())
    flat,_=engine(quotes=evidence)
    result=flat.run((closing_session(),))
    assert result.sessions[0].fills==0 and result.sessions[0].flat_before_deadline
    exposed,_=engine({'orb_mnq_v7':first_entry},quotes=evidence)
    with pytest.raises(ReplayNeedsContext,match='missing reviewed'):
        exposed.run((closing_session(),))


def test_execution_snapshot_is_deep_and_preserves_primitive_and_container_types():
    from dataclasses import dataclass
    from types import MappingProxyType
    from c1_rail.qualification.production_source import _execution_snapshot
    @dataclass(frozen=True)
    class Nested:
        values: object
    value=Nested(MappingProxyType({'numbers':(1,2.0)}))
    baseline=_execution_snapshot(value)
    assert type(baseline) is bytes and len(baseline)==32
    object.__setattr__(value,'values',MappingProxyType({'numbers':(True,2.0)}))
    assert _execution_snapshot(value)!=baseline
    assert _execution_snapshot([1])!=_execution_snapshot((1,))
    assert _execution_snapshot(1)!=_execution_snapshot(1.0)
    assert _execution_snapshot({'a':1})!=_execution_snapshot(MappingProxyType({'a':1}))
    assert _execution_snapshot(('a','bc'))!=_execution_snapshot(('ab','c'))
    cycle=[];cycle.append(cycle)
    with pytest.raises(ValueError,match='cycle'):
        _execution_snapshot(cycle)


def test_source_verify_rejects_unissued_object_before_reading_contract():
    reconstructed=object.__new__(ProductionSource)
    with pytest.raises(ValueError,match='issued'):
        reconstructed.verify_for(object())


@pytest.mark.parametrize('name',('replay','replay_bracket','verify_for','proof'))
def test_source_does_not_allow_instance_execution_callback_overrides(name):
    source=object.__new__(ProductionSource)
    with pytest.raises(AttributeError):
        object.__setattr__(source,name,lambda *args,**kwargs:None)


def test_execution_snapshot_rejects_nested_evidence_callback_shadowing():
    from c1_rail.qualification.production_source import _execution_snapshot
    evidence=parse_schedule_execution_evidence(json.dumps({'schema':'qualification-schedule-execution/v1','rows':[]}).encode())
    before=_execution_snapshot(evidence)
    object.__setattr__(evidence,'split_bar',lambda *args:None)
    with pytest.raises(ValueError,match='integrity'):
        _execution_snapshot(evidence)


def test_execution_snapshot_covers_real_source_graph_and_shared_nested_bar():
    from datetime import date
    from c1_rail.qualification.benchmark import synthetic_source
    from c1_rail.qualification.production_source import _execution_snapshot
    source=synthetic_source(date(2024,1,2))
    shared=source.bars[0].bars[0][1]
    graph=(source,(shared,shared))
    baseline=_execution_snapshot(graph)
    object.__setattr__(shared,'volume',1.0)
    assert _execution_snapshot(graph)!=baseline


@pytest.mark.parametrize('mutation',('cost','quotes','bar','startup','adjacent','clock','sessions','copy'))
def test_issued_source_rejects_derived_state_mutation_and_reconstruction(tmp_path,mutation):
    from dataclasses import fields
    from types import MappingProxyType
    from composition_fixture import build_verified_composition
    source=build_verified_composition(tmp_path).source
    if mutation=='cost':
        leg,instrument=source._instruments[0]
        object.__setattr__(instrument,'commission_per_side',0.0)
    elif mutation=='quotes':
        object.__setattr__(source._quotes,'quotes',MappingProxyType({}))
    elif mutation=='bar':
        bar=source.sessions[0].bars[0].bars[0][1]
        object.__setattr__(bar,'close',bar.close+1)
    elif mutation=='startup':
        object.__setattr__(source.prepared.startup,'paper_initial_capitals',())
    elif mutation=='adjacent':
        object.__setattr__(source,'adjacent',tuple(1 for _ in source.adjacent))
    elif mutation=='clock':
        object.__setattr__(source.clock,'schedules',())
    elif mutation=='sessions':
        object.__setattr__(source,'sessions',list(source.sessions))
    else:
        clone=object.__new__(type(source))
        for field in fields(source):object.__setattr__(clone,field.name,getattr(source,field.name))
        source=clone
    with pytest.raises(ValueError,match='issued|changed|integrity'):
        source.verify_for(source.contract)


# ---- T00 step-1b Task 2: frozen bracket interface (packet §7) ----
# Case names carry the §7 "Required test update" item number (item1..item7).

def _evidence(rows=()):
    return parse_schedule_execution_evidence(json.dumps(
        {'schema': 'qualification-schedule-execution/v1', 'rows': list(rows)}).encode())


def _bracket(run):
    from c1_rail.qualification.production_source import ScheduleExecutionBracket
    return ScheduleExecutionBracket(_evidence()).for_run(run)


def _t2_bar_context(bar):
    from datetime import date
    from types import SimpleNamespace
    session = SimpleNamespace(occurrence=0, bars=(), source=SimpleNamespace(source_session_date=date(2024, 1, 2)))
    return session, SimpleNamespace(source_bar_time=bar.ts, bars=(('aegis_6j', bar),))


def test_t2_item1_frozen_types_have_exact_fields_immutability_and_validation():
    from dataclasses import FrozenInstanceError, fields
    from datetime import datetime, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import BracketReplayResult, ReplayResult, ScheduleExposure, ScheduleSplit
    for kind, names in ((ScheduleExposure, ('position', 'pending', 'reserved')),
                        (ScheduleSplit, ('prefix', 'suffix', 'prefix_executes')),
                        (BracketReplayResult, ('r1', 'r2'))):
        assert tuple(f.name for f in fields(kind)) == names
        assert kind.__dataclass_params__.frozen is True and kind.__slots__ == names
    exposure = ScheduleExposure(-2, True, 3)
    with pytest.raises(FrozenInstanceError):
        exposure.position = 1
    for bad in ((True, False, 0), (1, 0, 0), (1, False, True), (1, False, -1), (1.0, False, 0),
                (1, None, 0), (1, False, None), (1, 'yes', 0)):
        with pytest.raises(ValueError):
            ScheduleExposure(*bad)
    bar = Bar(datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc), 100, 100, 100, 100)
    class DerivedBar(Bar):
        pass
    split = ScheduleSplit(bar, bar, False)
    with pytest.raises(FrozenInstanceError):
        split.prefix_executes = True
    for bad in (((bar, bar), bar, True), (bar, None, True), (bar, bar, 0), (bar, bar, None),
                (DerivedBar(*vars(bar).values()), bar, True)):
        with pytest.raises(ValueError):
            ScheduleSplit(*bad)
    r1, r2 = ReplayResult((), ()), ReplayResult((), ())
    result = BracketReplayResult(r1, r2)
    assert (result.r1, result.r2) == (r1, r2) and result.r1 is r1 and result.r2 is r2
    with pytest.raises(FrozenInstanceError):
        result.r1 = r2
    for bad in ((r1, r1), (r1, None), ((), r2), (r1, ((), ()))):
        with pytest.raises(ValueError):
            BracketReplayResult(*bad)


def test_t2_item1_for_run_accepts_only_exact_ids_and_issues_fresh_providers():
    import inspect
    from datetime import datetime, timedelta, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import ScheduleExposure, ScheduleSplit
    from c1_rail.qualification.production_source import ScheduleExecutionBracket, ScheduleExecutionEvidence
    bracket = ScheduleExecutionBracket(_evidence())
    first, again, other = bracket.for_run('R1'), bracket.for_run('R1'), bracket.for_run('R2')
    assert all(type(p) is ScheduleExecutionEvidence for p in (first, again, other))
    assert len({id(first), id(again), id(other)}) == 3
    class Named(str):
        pass
    for bad in ('r1', 'R3', 'R1 ', ' R2', 'R12', '', None, 1, b'R1', Named('R1')):
        with pytest.raises(ValueError):
            bracket.for_run(bad)
    with pytest.raises(ValueError):
        ScheduleExecutionBracket(first)          # a run-local provider is not reviewed evidence
    for provider in (first, other, _evidence()):
        assert not hasattr(provider, 'observe_exposure') and not hasattr(provider, 'prefix_is_empty')
        for method in (provider.split_bar, provider.split_interval):
            parameter = inspect.signature(method).parameters['exposure']
            assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    # Every call is fresh: a placement in one provider is invisible to another.
    bar = Bar(datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc), 100, 120, 90, 110, 7)
    session, pb = _t2_bar_context(bar)
    instant = bar.ts + timedelta(minutes=10)
    for provider in (first, again):
        split = provider.split_bar(session, pb, instant, 'aegis_6j', exposure=ScheduleExposure(1, False, 0))
        assert type(split) is ScheduleSplit and provider(session, instant, 'aegis_6j') == 90
    with pytest.raises(TypeError):
        other.split_bar(session, pb, instant, 'aegis_6j')                 # legacy call shape
    from c1_rail.qualification.replay import ReplayNeedsContext
    with pytest.raises(ReplayNeedsContext, match='schedule instant'):
        other(session, instant, 'aegis_6j')


def test_t2_item1_retained_evidence_returns_executing_schedule_split():
    from datetime import datetime, timedelta, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import ScheduleExposure, ScheduleSplit
    start = datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc)
    instant = start + timedelta(minutes=10)
    values = {'open': 100., 'high': 100., 'low': 100., 'close': 100., 'volume': 0.}
    evidence = _evidence([{'source_session_date': '2024-01-02', 'leg_id': 'aegis_6j',
                           'source_bar_time': start.isoformat(), 'interval_start': start.isoformat(),
                           'instant': instant.isoformat(), 'price': 100., 'prefix': values, 'suffix': values}])
    session, pb = _t2_bar_context(Bar(start, **values))
    split = evidence.split_bar(session, pb, instant, 'aegis_6j', exposure=ScheduleExposure(0, True, 0))
    assert type(split) is ScheduleSplit and split.prefix_executes is True
    assert (split.prefix, split.suffix) == (Bar(start, **values), Bar(instant, **values))
    interval = evidence.split_interval(session, pb, Bar(start, **values), instant, 'aegis_6j',
                                       exposure=ScheduleExposure(1, False, 0))
    assert interval == split


def test_t2_item2_provider_places_the_ratified_two_run_table():
    from datetime import datetime, timedelta, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import ScheduleExposure
    bar = Bar(datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc), 100, 120, 90, 110, 7)  # 100 -> 90 -> 120 -> 110
    instant = bar.ts + timedelta(minutes=10)
    session, pb = _t2_bar_context(bar)
    table = [  # (run, exposure, boundary vertex price, prefix executes)
        ('R1', (1, False, 0), 90, True), ('R2', (1, False, 0), 120, True),        # long: adverse / favourable
        ('R1', (-3, False, 0), 120, True), ('R2', (-3, False, 0), 90, True),      # short
        ('R1', (0, True, 1), 110, True), ('R2', (0, True, 1), 100, False),        # pending only: fill / cancel
        ('R1', (0, True, 0), 110, True), ('R2', (0, True, 0), 100, False),
        ('R1', (2, True, 1), 90, True), ('R2', (2, True, 1), 120, True),          # position rule wins
        ('R1', (-1, True, 1), 120, True), ('R2', (-1, True, 1), 90, True),
    ]
    for run, exposure, price, executes in table:
        provider = _bracket(run)
        split = provider.split_bar(session, pb, instant, 'aegis_6j', exposure=ScheduleExposure(*exposure))
        assert (split.prefix.close, split.suffix.open, split.prefix_executes) == (price, price, executes)
        assert (split.prefix.ts, split.suffix.ts) == (bar.ts, instant)
        assert provider(session, instant, 'aegis_6j') == price


def test_t2_item5_provider_splits_the_current_suffix_and_stays_occurrence_local():
    from datetime import datetime, timedelta, timezone
    from types import SimpleNamespace
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import ScheduleExposure
    from c1_rail.qualification.replay import ReplayNeedsContext
    start = datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc)
    first, second = start + timedelta(minutes=5), start + timedelta(minutes=12)
    session, pb = _t2_bar_context(Bar(start, 100, 130, 90, 110, 3))
    provider = _bracket('R1')
    suffix = Bar(first, 95, 130, 95, 110, 0)              # retained suffix: 95 -> 130 -> 110
    split = provider.split_interval(session, pb, suffix, second, 'aegis_6j', exposure=ScheduleExposure(1, False, 0))
    assert (split.prefix.ts, split.prefix.open, split.prefix.close, split.suffix.close) == (first, 95, 95, 110)
    with pytest.raises(ReplayNeedsContext, match='already placed'):
        provider.split_interval(session, pb, suffix, second, 'aegis_6j', exposure=ScheduleExposure(1, False, 0))
    repeat = SimpleNamespace(occurrence=1, bars=(), source=session.source)
    again = provider.split_interval(repeat, pb, suffix, second, 'aegis_6j', exposure=ScheduleExposure(-1, False, 0))
    assert again.prefix.close == 130
    assert (provider(session, second, 'aegis_6j'), provider(repeat, second, 'aegis_6j')) == (95, 130)


def test_t2_item6_provider_refuses_missing_inactive_and_reservation_only_exposure():
    from datetime import datetime, timedelta, timezone
    from c1_signal_daemon.feed import Bar
    from c1_rail.qualification.model import ScheduleExposure
    from c1_rail.qualification.replay import ReplayNeedsContext
    bar = Bar(datetime(2024, 1, 2, 20, 45, tzinfo=timezone.utc), 100, 120, 90, 110, 7)
    instant = bar.ts + timedelta(minutes=10)
    session, pb = _t2_bar_context(bar)
    for provider in (_bracket('R1'), _bracket('R2'), _evidence()):
        for exposure, message in ((ScheduleExposure(0, False, 1), 'broker-pending'),
                                  (ScheduleExposure(2, False, 1), 'broker-pending'),
                                  (ScheduleExposure(0, False, 0), 'inactive'),
                                  (None, 'exposure'), ((0, True, 1), 'exposure')):
            with pytest.raises(ReplayNeedsContext, match=message):
                provider.split_bar(session, pb, instant, 'aegis_6j', exposure=exposure)
        if provider.run is not None:
            # No refused call reserved the placement key.
            provider.split_bar(session, pb, instant, 'aegis_6j', exposure=ScheduleExposure(0, True, 1))


def test_t2_item7_replay_bracket_builds_two_fresh_engines_with_separate_results(tmp_path, monkeypatch):
    import inspect
    import composition_fixture as fixture_module
    from c1_signal_daemon import book_adapters
    from c1_rail.qualification import replay as replay_module
    from c1_rail.qualification.model import BracketReplayResult, ReplayResult
    from c1_rail.qualification.paths import PathAssembler
    assert list(inspect.signature(ProductionSource.replay_bracket).parameters) == ['self', 'path']
    original_build = fixture_module.build_artifacts
    def holding(root, *, idle=False, port_transform=None):
        # TEST_ONLY: the fixture ORB holds its entry through the 15:55 intrabar flatten.
        def hold(leg, raw):
            if leg != 'orb_mnq_v7':
                return raw
            held = raw.replace(b'local.minute == 15 and self.position', b'local.minute == 59 and self.position')
            assert held != raw
            return held
        return original_build(root, idle=idle, port_transform=hold)
    monkeypatch.setattr(fixture_module, 'build_artifacts', holding)
    source = fixture_module.build_verified_composition(tmp_path).source
    path = PathAssembler(source.path_start_date).assemble((source.sessions[:3],), horizon_sessions=3)
    loads, engines = [], []
    load = book_adapters._load_domain_adapters
    def counting(contract, *, retained_bytes, domain):
        loads.append(load(contract, retained_bytes=retained_bytes, domain=domain))
        return loads[-1]
    class Recorded(replay_module.BookReplay):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            engines.append(self)
    monkeypatch.setattr(book_adapters, '_load_domain_adapters', counting)
    monkeypatch.setattr(replay_module, 'BookReplay', Recorded)
    result = source.replay_bracket(path)
    assert type(result) is BracketReplayResult
    assert type(result.r1) is ReplayResult and type(result.r2) is ReplayResult and result.r1 is not result.r2
    assert len(loads) == len(engines) == 2
    first, second = engines
    assert [e.schedule_quotes.run for e in engines] == ['R1', 'R2']
    assert first.schedule_quotes is not second.schedule_quotes and first.schedule_quotes is not source._quotes
    assert not set(map(id, first.adapters.values())) & set(map(id, second.adapters.values()))
    assert not set(map(id, first.brokers.values())) & set(map(id, second.brokers.values()))
    assert first.ledger is not second.ledger and first.clock is not second.clock
    assert first.events is not second.events and first._used and second._used
    # Each run consumed its own intrabar placement for every session's flatten.
    for engine in engines:
        placements = [key for key in engine.schedule_quotes._placed]
        assert [(occurrence, leg) for occurrence, leg, _ in placements] == [(0, 'orb_mnq_v7'), (1, 'orb_mnq_v7'), (2, 'orb_mnq_v7')]
        assert all(instant.minute == 55 for _, _, instant in placements)
    assert all(row.fills == 2 and row.flat_before_deadline and row.end_edge.is_flat for row in result.r1.sessions)
    # Flat retained bars: the bracket adds no signal, cost or price event.
    assert result.r1 == result.r2 == source.replay(path)


# ---- T05 owed qualification-path items (T00 P7 closure §7, step-1b return) ----
# A gated qualification build runs the source-only gates. The TEST_ONLY composition
# fixture is pinned by the S5 harness, so these cases rewrite its payloads before
# signing and select the gates for its domain; every guard itself runs unpatched.

REVIEWER = 'synthetic-composition-reviewer'


def _refused(code, call):
    with pytest.raises(ValueError) as error:
        call()
    assert code in str(error.value), str(error.value)


def _gated_composition(root, monkeypatch, *, transform=None, calendar_producer=None,
                       review_producer=REVIEWER, review_edit=None, port_transform=None):
    """Signed TEST_ONLY composition whose source artifacts satisfy the source gates.

    Returns a call that signs the contract and builds the source through the real
    ``_build_composition`` route (``build_verified_composition`` minus inventory)."""
    import composition_fixture as fixture_module
    from c1_rail.qualification import production_source
    from c1_rail.qualification.contract import ObservedBindings, canonical_json_bytes, validate_frozen_contract
    from test_contract import NOW
    from test_source_contract import REVIEW_SCOPES, SYNTHETIC_CALENDAR_PRODUCER, v2_review
    encoded, digest = fixture_module.encoded, fixture_module.digest

    def build(path):
        fixture = fixture_module.build_artifacts(path, port_transform=port_transform)
        payloads = fixture.payloads
        payloads['calendar_producer'] = (canonical_json_bytes(SYNTHETIC_CALENDAR_PRODUCER)
                                         if calendar_producer is None else calendar_producer)
        fact = {'role': 'calendar_producer', 'sha256': digest(payloads['calendar_producer'])}
        calendar, index = json.loads(payloads['source_calendar']), json.loads(payloads['population_index'])
        for row in calendar['sessions']:
            row['facts'] = [fact]
            for item in row['venue_deadlines'].values():
                item['fact'] = fact
        if transform is not None:
            transform(payloads, calendar, index, fixture.populations)
        payloads['source_calendar'] = encoded(calendar)
        index['source_binding']['source_calendar_sha256'] = digest(payloads['source_calendar'])
        payloads['population_index'] = encoded(index)
        binding = digest(encoded(index['source_binding']))
        for role in REVIEW_SCOPES:
            doc = json.loads(v2_review(role, digest(payloads[role]), reviewer=REVIEWER,
                                       binding_sha256=binding if role == 'population_index' else None))
            payloads[role + '_review'] = canonical_json_bytes(review_edit(role, doc) if review_edit else doc)
        for role in ('calendar_producer', 'source_calendar', 'population_index', *(r + '_review' for r in REVIEW_SCOPES)):
            (path / fixture.paths[role]).write_bytes(payloads[role])
        return fixture

    def signed():
        fixture = build(root).with_runtime_artifacts(root)
        domain, private, keys = fixture_module.verified_domain(fixture)
        doc = fixture_module.contract_document(fixture, domain)
        for row in (*doc['artifacts'], *doc['role_owners']):
            if row['role'].endswith('_review'):
                row['producer' if 'producer' in row else 'owner'] = review_producer
        raw = encoded(doc)
        approval = fixture_module.signed_approval(raw, private['test-freeze'], key_id='test-freeze', scope='FREEZE_F1')
        retained = {role: (root / path).read_bytes() for role, path in fixture.paths.items()}
        observed = ObservedBindings(artifact_sha256={fixture.paths[r]: digest(b) for r, b in retained.items()},
                                    runtime_load_sha256={r: digest(b) for r, b in retained.items()},
                                    effective_settings_sha256=digest(retained['effective_settings_successor']),
                                    orb_normal_base=1)
        contract = validate_frozen_contract(raw, approval, keys, observed, now=NOW, trust_domain=domain)
        return contract, production_source.ProductionSource._build_composition(contract, artifact_root=root)

    monkeypatch.setattr(production_source, '_source_gates_apply', lambda domain: True)
    return signed


def test_t05_source_gates_apply_to_every_domain_but_the_test_only_composition_profile():
    from types import SimpleNamespace
    import test_contract
    from test_trust_domain import case, validate
    from c1_rail.qualification.production_source import _source_gates_apply
    operator, _, _ = test_contract._operator_domain(test_contract._document())
    composition = validate(*case())
    assert (operator.authority_class, operator.permits_synthetic, _source_gates_apply(operator)) == ('OPERATOR', False, True)
    assert (composition.authority_class, composition.permits_synthetic, _source_gates_apply(composition)) == ('TEST_ONLY', True, False)
    assert _source_gates_apply(SimpleNamespace(authority_class='UNKNOWN', permits_synthetic=True))


def test_t05_gated_qualification_review_binds_an_independent_reviewer(tmp_path, monkeypatch):
    contract, source = _gated_composition(tmp_path, monkeypatch)()
    source.verify_for(contract)
    assert source.evidence_class == 'QUALIFICATION'
    producers = {row.role: row.producer for row in contract.artifacts}
    assert producers['source_calendar_review'] == REVIEWER != producers['source_calendar']


@pytest.mark.parametrize('defect,code', [
    ('self_certified', 'REVIEW_NOT_INDEPENDENT'),     # the reviewed artifact's producer signs the companion
    ('v1', 'scope/reviewer'),                         # a v1 companion carries no reviewer identity
])
def test_t05_gated_qualification_review_refuses_unidentified_or_self_review(tmp_path, monkeypatch, defect, code):
    def v1(role, doc):
        if role != 'source_calendar':
            return doc
        return {'schema': 'qualification-source-review/v1',
                **{key: doc[key] for key in ('artifact_role', 'artifact_sha256', 'scope', 'decision')}}
    build = _gated_composition(tmp_path, monkeypatch, review_producer=(
        'synthetic-composition-fixture' if defect == 'self_certified' else REVIEWER),
        review_edit=v1 if defect == 'v1' else None)
    _refused(code, build)


@pytest.mark.parametrize('defect,code', [
    ('fact_role', 'CALENDAR_FACT_ROLE'),               # another retained role at its true digest
    ('deadline_fact', 'CALENDAR_PRODUCER_MISMATCH'),   # the record states a 12:59 day the calendar omits
])
def test_t05_gated_qualification_calendar_binds_the_calendar_producer(tmp_path, monkeypatch, defect, code):
    from composition_fixture import digest
    from c1_rail.qualification.contract import canonical_json_bytes
    from test_source_contract import SYNTHETIC_CALENDAR_PRODUCER

    def other_role(payloads, calendar, index, populations):
        calendar['sessions'][0]['facts'] = [{'role': 'cost_model', 'sha256': digest(payloads['cost_model'])}]
    producer = canonical_json_bytes(dict(SYNTHETIC_CALENDAR_PRODUCER, venue_flat_dates_in_interval=['2024-01-02']))
    _refused(code, _gated_composition(tmp_path, monkeypatch, transform=other_role if defect == 'fact_role' else None,
                                      calendar_producer=producer if defect == 'deadline_fact' else None))


TAIL = '2024-08-30'                                              # the fixture's last source date
TRUNCATED = 'panel truncated at interval end: slots 09:00-16:00 ET'   # its indexed ET slot range


@pytest.mark.parametrize('case,code', [
    ('admitted', None),
    ('interior', 'SOURCE_TRUNCATION_INTERIOR'),
    ('unnamed_slots', 'SOURCE_TRUNCATION_REASON'),
    ('unrecorded_tail', 'CALENDAR_PRODUCER_MISMATCH'),
    ('stand_in', 'TRUNCATION_STAND_IN_RETIRED'),
])
def test_t05_gated_qualification_validates_source_truncated(tmp_path, monkeypatch, case, code):
    from c1_rail.qualification.contract import canonical_json_bytes
    from test_source_contract import SYNTHETIC_CALENDAR_PRODUCER
    reason = 'panel ended early' if case == 'unnamed_slots' else TRUNCATED
    status = 'policy_denied' if case == 'stand_in' else 'source_truncated'

    def truncate(payloads, calendar, index, populations):
        position = 5 if case == 'interior' else -1
        row = calendar['sessions'][position]
        assert case == 'interior' or row['date'] == TAIL
        calendar['sessions'][position] = dict(row, status=status, reason=reason, venue_deadlines={})
        index['expected_exclusions'] = [{'source_date': row['date'], 'reason': status, 'detail': reason}]
        full = [day for day in populations['FULL'] if day != row['date']]
        populations.update(FULL=full, H1=full[:(len(full) + 1) // 2], H2=full[(len(full) + 1) // 2:])
        index['populations'] = {name: list(values) for name, values in populations.items()}
    tail = {} if case == 'unrecorded_tail' else {'tail_disposition': {'date': TAIL, 'status': 'source_truncated'}}
    build = _gated_composition(tmp_path, monkeypatch, transform=truncate,
                               calendar_producer=canonical_json_bytes(dict(SYNTHETIC_CALENDAR_PRODUCER, **tail)))
    if code is not None:
        _refused(code, build)
        return
    contract, source = build()
    source.verify_for(contract)
    assert [(e.session_date.isoformat(), e.reason, e.detail) for e in source.exclusions] == [(TAIL, 'source_truncated', TRUNCATED)]
    assert TAIL not in contract.populations['FULL'] and TAIL not in {s.session_id for s in source.sessions}


# ---- P3-1 (2026-10-01 refute-first review): replay_bracket's deadline-failure branch ----

def _hold_orb_through_flatten(monkeypatch):
    """TEST_ONLY port: the fixture ORB keeps its entry into the 15:55 ET intrabar flatten."""
    import composition_fixture as fixture_module
    original = fixture_module.build_artifacts

    def holding(root, *, idle=False, port_transform=None):
        def hold(leg, raw):
            return raw if leg != 'orb_mnq_v7' else raw.replace(
                b'local.minute == 15 and self.position', b'local.minute == 59 and self.position')
        return original(root, idle=idle, port_transform=hold)
    monkeypatch.setattr(fixture_module, 'build_artifacts', holding)


def _withhold_r1_flatten(monkeypatch):
    """TEST_ONLY venue refusal: the R1 engine's brokers never confirm the scheduled flatten,
    so the real engine's own-flat deadline check raises; R2's brokers are honest."""
    from c1_signal_daemon import tv_broker_emulator
    from c1_rail.qualification.model import LEG_IDS
    built = []

    class Withholding(tv_broker_emulator.TVBrokerEmulator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.withhold = len(built) < len(LEG_IDS)     # the first engine built is R1's
            built.append(self)

        def submit(self, actions, bar):
            if self.withhold and any(getattr(a, 'reason', '') == 'scheduled_flatten' for a in actions):
                return []
            return super().submit(actions, bar)
    monkeypatch.setattr(tv_broker_emulator, 'TVBrokerEmulator', Withholding)
    return built


def test_p3_1_qualification_replay_bracket_keeps_a_real_deadline_failure_as_that_runs_result(tmp_path, monkeypatch):
    import composition_fixture as fixture_module
    from c1_rail.qualification.model import LEG_IDS, BracketReplayResult, ReplayResult
    from c1_rail.qualification.paths import PathAssembler
    _hold_orb_through_flatten(monkeypatch)
    source = fixture_module.build_verified_composition(tmp_path).source
    path = PathAssembler(source.path_start_date).assemble((source.sessions[:3],), horizon_sessions=3)
    built = _withhold_r1_flatten(monkeypatch)
    result = source.replay_bracket(path)
    assert len(built) == 2 * len(LEG_IDS)
    assert type(result) is BracketReplayResult and type(result.r1) is ReplayResult and result.r1 is not result.r2
    # R1 is T=infinity at its first session: a partial record, not a raised failure.
    assert [row.flat_before_deadline for row in result.r1.sessions] == [False]
    assert not result.r1.sessions[0].end_edge.is_flat
    assert [e.kind for e in result.r1.events].count('deadline_failure') == 1
    assert len(result.r2.sessions) == 3 and all(row.flat_before_deadline and row.end_edge.is_flat for row in result.r2.sessions)
    assert 'deadline_failure' not in {e.kind for e in result.r2.events}


def test_p3_1_source_only_replay_bracket_seals_a_real_deadline_failure(tmp_path, monkeypatch):
    from c1_rail.qualification import production_source
    from c1_rail.qualification.model import ReplayResult
    from c1_rail.qualification.paths import PathAssembler
    from test_source_contract import NOW, build_source_case
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    _hold_orb_through_flatten(monkeypatch)
    case = build_source_case(tmp_path, monkeypatch)
    source = production_source.ProductionSource.build(case.validate(), artifact_root=case.root)
    path = PathAssembler(source.path_start_date).assemble((source.sessions[:3],), horizon_sessions=3)
    _withhold_r1_flatten(monkeypatch)
    result = source.replay_bracket(path)
    assert type(result) is production_source.SourceOnlyBracket
    assert not isinstance(result.r1, ReplayResult) and not isinstance(result.r2, ReplayResult)
    assert (result.r1.deadline_failure, result.r2.deadline_failure) == (True, False)
    assert [(row.flat_before_deadline, row.end_flat) for row in result.r1.sessions] == [(False, False)]
    assert len(result.r2.sessions) == 3 and all(row.flat_before_deadline and row.end_flat for row in result.r2.sessions)
    # R1 consumed its first 15:55 ET split before the failure; R2 consumed one per session.
    assert len(result.r2.consumed_intrabar_splits) == 3
    assert result.r1.consumed_intrabar_splits == result.r2.consumed_intrabar_splits[:1]


# ---- P-B2: the gated screen capability (design 2026-10-02 §3.3; card §2.5, rows K5-K8) ----
# A synthetic source case, repository and screen authority from test_screen_authority.Screen;
# TEST_ONLY keys and fixtures only. The run lock is a msvcrt byte-range lock (card §3.4).

SCREEN = pytest.mark.skipif(os.name != 'nt' or shutil.which('git') is None,
                            reason='the screen gate needs git and the msvcrt run lock')
SCREEN_EXPIRES = '2026-09-15T21:00:00Z'   # one hour after NOW; r3c's own window is wider (row K2)

# inspect.getsource SHA-256 of the seven sealed functions at the P-B2 base 6629627, recorded
# before the build (row K7).
SEALED_SOURCE_SHA256 = {
    'replay': '33ec2fb7a2d19abcc52049d580d70e0b1af0e7d6ebc36d659c3ffcf739f9e4ba',
    'replay_bracket': '220c80607c58f360f6f3d9422970fc0f52d933e178bb50b6cceb986872e7d9e3',
    'proof': '853baa51b2f8f8e97b052081487b36f067d01d3e91b9378c2675f27a0ee8f2d1',
    '_seal': 'ca187f0cf29bce9942c42b9fd7ab9d2692c57fac6565d71149b58652f2add6a4',
    '_check_path': '494292efbc57ffe7ee7214ca4a51aa2060fbcb1b30ccd2db4bf991f2eb1cae2b',
    '_verify_integrity': '236201d4a555098a097b3b9c892d32caa5d92f9f03bed129dfdfeac461cd7b43',
    'verify_for': '50eebc21adfec880ead92687e4a1f09767bc0d3faaf630337e379d8b26ad96da',
}


def _sealed_source_sha256():
    import inspect
    from c1_rail.qualification import production_source
    owner = {'_seal': production_source}
    return {name: hashlib.sha256(inspect.getsource(getattr(owner.get(name, ProductionSource), name)).encode()).hexdigest()
            for name in SEALED_SOURCE_SHA256}


def _screen(tmp_path, monkeypatch):
    """A validated screen authority whose approval ends at SCREEN_EXPIRES, a source-only source
    built from its exact receipt, and a three-session path."""
    from c1_rail.qualification import production_source
    from c1_rail.qualification.contract import canonical_json_bytes
    from c1_rail.qualification.paths import PathAssembler
    from test_screen_authority import Screen
    from test_source_contract import NOW
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    screen = Screen(tmp_path, monkeypatch)
    raw = canonical_json_bytes(screen.authority)
    auth = screen.validate(approval=screen.approval(raw, expires_at=SCREEN_EXPIRES))
    source = ProductionSource.build(screen.receipt, artifact_root=screen.artifact_root)
    path = PathAssembler(source.path_start_date).assemble((source.sessions[:3],), horizon_sessions=3)
    return screen, auth, source, path


@contextmanager
def _ready(screen, auth):
    """screen.ready with a recorder whose loaded closure holds at open: every module already
    loaded counts as a recorded stdlib name (synthetic, as test_screen_authority.cover_loaded)."""
    from test_screen_authority import cover_loaded
    with screen.ready(auth) as run_dir:
        recorder = sys.p7_recorder
        recorder.first_party, recorder.third_party, recorder.ports, recorder.stdlib = {}, {}, {}, set()
        cover_loaded(recorder)
        yield run_dir


def sa():
    """The screen entry points' owner (screen_authority.screen_epoch/screen_bracket)."""
    from c1_rail.qualification import screen_authority
    return screen_authority


def _spy_engine(monkeypatch):
    calls, real = [], ProductionSource._engine

    def spy(self, schedule_quotes):
        calls.append(schedule_quotes)
        return real(self, schedule_quotes)
    monkeypatch.setattr(ProductionSource, '_engine', spy)
    return calls


def _touch(path, delta_ns):
    stat = path.stat()
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + delta_ns))


@SCREEN
def test_K5(tmp_path, monkeypatch):
    """Each K1-K4 and K6 refusal fires before any engine is built: a spy on _engine sees no call."""
    from datetime import timedelta
    import composition_fixture
    from c1_rail.qualification import production_source
    from test_source_contract import NOW
    # Built first: the composition's runtime inventory refuses a test-module _now seam.
    qualification = composition_fixture.build_verified_composition(tmp_path / 'f1').source
    screen, auth, source, path = _screen(tmp_path / 'screen', monkeypatch)
    other = ProductionSource.build(screen.case.validate(), artifact_root=screen.artifact_root)
    artifact = screen.artifact_root / auth.source_receipt.artifacts[0].path
    calls = _spy_engine(monkeypatch)
    with _ready(screen, auth):
        epoch = sa().screen_epoch(source, authority=auth)

        def call(src=source, ep=epoch):
            return sa().screen_bracket(src, path, authority=auth, epoch=ep)
        _refused('SCREEN_REQUIRES_SOURCE_RECEIPT', lambda: call(qualification))         # K1
        _refused('SCREEN_SOURCE_MISMATCH', lambda: call(other))                         # K1
        monkeypatch.setattr(production_source, '_now', lambda: NOW + timedelta(minutes=90))
        _refused('SCREEN_APPROVAL_EXPIRED', call)                                       # K2
        monkeypatch.setattr(production_source, '_now', lambda: NOW)
        recorder = sys.p7_recorder
        monkeypatch.delattr(sys, 'p7_recorder')
        _refused('SCREEN_BOOTSTRAP_MISMATCH', call)                                     # K3
        monkeypatch.setattr(sys, 'p7_recorder', recorder, raising=False)
        ledger = screen.ledger.read_bytes()
        screen.ledger.write_bytes(b'')
        _refused('SCREEN_RUN_UNBOUND', call)                                            # K4
        screen.ledger.write_bytes(ledger)
        _refused('SCREEN_EPOCH_REQUIRED', lambda: call(source, None))                   # K6
        _touch(artifact, 1_000_000_000)
        _refused('SCREEN_EPOCH_STALE', call)                                            # K6
        assert calls == []
        _touch(artifact, -1_000_000_000)
        assert type(call()).__name__ == 'ScreenBracket' and len(calls) == 2             # twin


@SCREEN
def test_K6(tmp_path, monkeypatch):
    """An r3c artifact file's mtime changes mid-epoch: the next call is stale; the epoch closes with
    the full check; a closed epoch serves nothing; a new epoch opens and serves again."""
    from test_screen_authority import cover_loaded
    screen, auth, source, path = _screen(tmp_path, monkeypatch)
    artifact = screen.artifact_root / auth.source_receipt.artifacts[0].path
    with _ready(screen, auth):
        epoch = sa().screen_epoch(source, authority=auth)
        assert sa().screen_bracket(source, path, authority=auth, epoch=epoch).deadline_failure == (False, False)
        _touch(artifact, 1_000_000_000)
        _refused('SCREEN_EPOCH_STALE', lambda: sa().screen_bracket(source, path, authority=auth, epoch=epoch))
        recorder = sys.p7_recorder
        recorder.first_party, recorder.third_party, recorder.ports, recorder.stdlib = {}, {}, {}, set()
        cover_loaded(recorder)
        assert sa().close_screen_epoch(epoch).closure_match
        _refused('SCREEN_EPOCH_REQUIRED', lambda: sa().screen_bracket(source, path, authority=auth, epoch=epoch))
        reopened = sa().screen_epoch(source, authority=auth)
        assert sa().screen_bracket(source, path, authority=auth, epoch=reopened).deadline_failure == (False, False)


@SCREEN
def test_K6_open_refuses_a_mismatched_loaded_closure(tmp_path, monkeypatch):
    """Codex r4179917167: a recorded first-party digest that differs from the loaded bytes refuses
    the epoch at open, before any engine is built (rows K5/K6); the matching twin opens."""
    from test_screen_authority import MODULE
    screen, auth, source, path = _screen(tmp_path, monkeypatch)
    calls = _spy_engine(monkeypatch)
    with _ready(screen, auth):
        recorder = sys.p7_recorder
        recorder.first_party = {'c1_rail.qualification.t00_screen_fixture': {
            'path': MODULE, 'sha256': hashlib.sha256(b'TEST_ONLY other bytes\n').hexdigest()}}
        _refused('SCREEN_EPOCH_STALE', lambda: sa().screen_epoch(source, authority=auth))
        assert calls == []
        recorder.first_party['c1_rail.qualification.t00_screen_fixture']['sha256'] = hashlib.sha256(
            (screen.repo / MODULE).read_bytes()).hexdigest()
        epoch = sa().screen_epoch(source, authority=auth)                                     # twin
        assert type(sa().screen_bracket(source, path, authority=auth, epoch=epoch)).__name__ == 'ScreenBracket'
        assert len(calls) == 2


def test_screen_entry_points_refuse_a_non_production_source(tmp_path, monkeypatch):
    """As ProductionSource methods they could serve only a ProductionSource; as screen_authority
    functions they refuse a duck-typed stand-in, even one carrying a real source-only receipt, before
    anything else: no integrity check and no engine (spy counts stay 0)."""
    from c1_rail.qualification import production_source
    from test_source_contract import NOW, build_source_case
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    calls = []

    class StandIn:  # pylint: disable=too-few-public-methods
        """TEST_ONLY: a ProductionSource look-alike."""
        contract = build_source_case(tmp_path, monkeypatch).validate()

        def _verify_integrity(self):
            calls.append('integrity')

        def _engine(self, provider):
            calls.append(provider)
    for call in (lambda: sa().screen_epoch(StandIn(), authority=None),
                 lambda: sa().screen_bracket(StandIn(), (), authority=None, epoch=None)):
        with pytest.raises(TypeError, match='SCREEN_REQUIRES_PRODUCTION_SOURCE'):
            call()
    assert calls == []


@SCREEN
def test_K7(tmp_path, monkeypatch):
    """With a valid authority and an open epoch, verify_for and replay_bracket on r3c still refuse
    qualification and return sealed types; the seven sealed functions keep their source text."""
    from c1_rail.qualification import production_source
    from c1_rail.qualification.model import BracketReplayResult
    screen, auth, source, path = _screen(tmp_path, monkeypatch)
    with _ready(screen, auth):
        epoch = sa().screen_epoch(source, authority=auth)
        _refused('SOURCE_ONLY_NOT_QUALIFICATION', lambda: source.verify_for(source.contract))
        assert type(source.replay_bracket(path)) is production_source.SourceOnlyBracket
        assert type(source.replay(path)) is production_source.SourceOnlyReplay
        assert type(sa().screen_bracket(source, path, authority=auth, epoch=epoch).bracket) is BracketReplayResult
    hashes = _sealed_source_sha256()
    assert hashes == SEALED_SOURCE_SHA256
    assert hashlib.sha256(b'def replay(self, path): ...\n').hexdigest() not in hashes.values()   # twin


@SCREEN
def test_K8(tmp_path, monkeypatch):
    """A path with a deadline in R2 only: per run, the wrapper's deadline flag and consumed splits
    equal the sealed SourceOnlyReplay's on the same path (twin: no deadline)."""
    from c1_signal_daemon import tv_broker_emulator
    from c1_rail.qualification.model import LEG_IDS
    _hold_orb_through_flatten(monkeypatch)
    screen, auth, source, path = _screen(tmp_path, monkeypatch)
    built, state = [], {'withhold_r2': False}

    class WithholdingR2(tv_broker_emulator.TVBrokerEmulator):
        """TEST_ONLY venue refusal: each bracket's second (R2) engine never confirms the flatten."""
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.withhold = state['withhold_r2'] and (len(built) // len(LEG_IDS)) % 2 == 1
            built.append(self)

        def submit(self, actions, bar):
            if self.withhold and any(getattr(a, 'reason', '') == 'scheduled_flatten' for a in actions):
                return []
            return super().submit(actions, bar)
    monkeypatch.setattr(tv_broker_emulator, 'TVBrokerEmulator', WithholdingR2)
    with _ready(screen, auth):
        epoch = sa().screen_epoch(source, authority=auth)
        for withhold, expected in ((False, (False, False)), (True, (False, True))):
            state['withhold_r2'] = withhold
            wrapped = sa().screen_bracket(source, path, authority=auth, epoch=epoch)
            sealed = source.replay_bracket(path)
            runs = (sealed.r1, sealed.r2)
            assert wrapped.deadline_failure == tuple(run.deadline_failure for run in runs) == expected
            assert wrapped.consumed_splits == tuple(run.consumed_intrabar_splits for run in runs)
            assert len(wrapped.consumed_splits[0]) == 3
            assert [len(r.sessions) for r in (wrapped.bracket.r1, wrapped.bracket.r2)] == [3, 1 if withhold else 3]


SCREEN_ONLY_MODULES = ('c1_rail.qualification.screen_authority', 'c1_rail.qualification.p7_evidence',
                       'c1_rail.qualification.t00_screen')


def _imported_modules(tree, package='c1_rail.qualification'):
    """Every module an Import/ImportFrom (relative resolved) or a constant import_module/__import__
    call in ``tree`` names; each from-imported name is also taken as a submodule."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            parts = package.split('.')
            base = '.'.join(parts[:len(parts) - node.level + 1]) if node.level else ''
            module = '.'.join(filter(None, (base, node.module)))
            yield module
            yield from (f'{module}.{alias.name}' for alias in node.names)
        elif (isinstance(node, ast.Call) and node.args and isinstance(node.args[0], ast.Constant)
              and getattr(node.func, 'attr', getattr(node.func, 'id', None)) in ('import_module', '__import__')):
            yield str(node.args[0].value)


def _screen_imports(tree):
    return sorted({name for name in _imported_modules(tree)
                   if any(name == banned or name.startswith(banned + '.') for banned in SCREEN_ONLY_MODULES)})


def test_production_source_imports_no_screen_module():
    """Codex r4180236028: production_source's closure is PRODUCTION_TRUST_POLICY's, so the screen
    entry lives in screen_authority and production_source imports no screen module in any form."""
    from c1_rail.qualification import production_source
    with open(production_source.__file__, encoding='utf-8') as handle:
        assert _screen_imports(ast.parse(handle.read())) == []
    planted = ast.parse('def f():\n    from .screen_authority import x\n    from . import p7_evidence\n'
                        'import c1_rail.qualification.t00_screen.journal\n'
                        'importlib.import_module("c1_rail.qualification.screen_authority")\n')  # twin
    assert _screen_imports(planted) == [
        'c1_rail.qualification.p7_evidence', 'c1_rail.qualification.screen_authority',
        'c1_rail.qualification.screen_authority.x', 'c1_rail.qualification.t00_screen.journal']


# ---- P-S2: startup policy v2 (successor build card 2026-10-10 §2.4, rows Y1-Y5) ----
# Synthetic policies and the TEST_ONLY composition fixture only; the sizing below is an
# arbitrary non-identity vector, not a proposed or ruled one.

SYNTHETIC_SIZING = {'aegis_6j': {'base': 4, 'adds': 'UNCHANGED'},
                    'dj30_mym_p250': {'risk_multiplier': '1/2', 'cap_reserve_multiplier': '1/2', 'adds': 'OFF'},
                    'vanguard_mgc': {'base_by_port': {'1': 0, '2': 1}, 'adds': 'UNCHANGED'},
                    'orb_mnq_v7': {'base': 0, 'adds': 'UNCHANGED'}}
# sha256(repr(ReplayResult)) of the fixture's five-session replay at the P-S2 base a6a4a76.
FIXTURE_REPLAY_SHA256 = 'c5beaa0204456287ec184d8793d4aa2da6d08565d704a4e030b5d15e58136bbe'
STARTUP_FIELDS = ('path_start_date', 'paper_initial_capitals', 'lifecycle_tiers',
                  'request_caps_micro_equivalents', 'shared_account_cap_micro_equivalents')


def _startup(schema='qualification-source-startup/v1', **extra):
    from c1_rail.qualification.model import LEG_IDS
    doc = {'schema': schema, 'initialization': 'FRESH_ONCE_CONTINUOUS',
           'positions': 'ZERO', 'working_orders': 'ZERO', 'splice_behavior': 'CARRY_ALL_STATE',
           'path_start_date': '2030-01-07', 'shared_account_cap_micro_equivalents': 80,
           'legs': {leg: {'paper_initial_capital': '100000', 'lifecycle_tier': 'AUTHORIZED',
                          'request_cap_micro_equivalents': 80} for leg in LEG_IDS}}
    doc.update(extra)
    return doc


def _v2(sizing=SYNTHETIC_SIZING):
    return _startup('qualification-source-startup/v2', sizing=json.loads(json.dumps(sizing)))


def _parse(doc):
    return parse_startup_policy(json.dumps(doc).encode())


def _five_session_replay(source):
    from c1_rail.qualification.paths import PathAssembler
    return source.replay(PathAssembler(source.path_start_date).assemble((source.sessions[:5],), horizon_sessions=5))


def test_Y1(tmp_path):
    """A v1 policy parses to today's fields plus the identity vector; the fixture replays as at base."""
    from c1_rail.book_policy import IDENTITY_SIZE_VECTOR
    from composition_fixture import build_verified_composition
    parsed = _parse(_startup())
    assert parsed.size_vector is IDENTITY_SIZE_VECTOR
    assert (parsed.path_start_date.isoformat(), parsed.shared_account_cap_micro_equivalents) == ('2030-01-07', 80)
    assert {v for _, v in parsed.lifecycle_tiers} == {'AUTHORIZED'}
    assert {v for _, v in parsed.request_caps_micro_equivalents} == {80}
    source = build_verified_composition(tmp_path).source
    assert source.prepared.startup.size_vector is IDENTITY_SIZE_VECTOR
    result = _five_session_replay(source)
    assert hashlib.sha256(repr(result).encode()).hexdigest() == FIXTURE_REPLAY_SHA256
    assert [row.fills for row in result.sessions] == [2] * 5   # twin: the digest covers real fills


def test_Y2():
    """A v2 policy parses to the validated vector; each v1 rule still refuses its own violation under v2."""
    from c1_rail.book_policy import validate_size_vector
    parsed, v1 = _parse(_v2()), _parse(_startup())
    assert parsed.size_vector == validate_size_vector(SYNTHETIC_SIZING) and not parsed.size_vector.is_identity
    assert all(getattr(parsed, name) == getattr(v1, name) for name in STARTUP_FIELDS)
    for key, value in (('initialization', 'RESET_DAILY'), ('positions', 'CARRIED'),
                       ('working_orders', 'CARRIED'), ('splice_behavior', 'RESET_TO_SOURCE_SNAPSHOT')):
        with pytest.raises(ValueError, match='fresh-once'):
            _parse({**_v2(), key: value})
    with pytest.raises(ValueError, match='80 micro-equivalent'):
        _parse({**_v2(), 'shared_account_cap_micro_equivalents': 79})
    with pytest.raises(ValueError, match='weekday'):
        _parse({**_v2(), 'path_start_date': '2030-01-05'})
    for key, value, reason in (('lifecycle_tier', 'PROBATION', 'AUTHORIZED only'),
                               ('request_cap_micro_equivalents', 8, 'per-request cap'),
                               ('paper_initial_capital', 100000, 'explicit decimal string'),
                               ('paper_initial_capital', '0', 'positive finite')):
        doc = _v2()
        doc['legs']['vanguard_mgc'][key] = value
        with pytest.raises(ValueError, match=reason):
            _parse(doc)
    doc = _v2()
    del doc['legs']['orb_mnq_v7']
    with pytest.raises(ValueError, match='four-leg'):
        _parse(doc)
    doc = _v2()
    doc['legs']['aegis_6j']['extra'] = 1
    with pytest.raises(ValueError, match='per-leg'):
        _parse(doc)
    with pytest.raises(ValueError, match='complete explicit startup policy fields'):
        _parse(_startup('qualification-source-startup/v3', sizing=SYNTHETIC_SIZING))


def test_Y3():
    """A bad v2 sizing is refused with validate_size_vector's reason; extra and missing fields refused."""
    from c1_rail.book_policy import validate_size_vector
    bad = [{**SYNTHETIC_SIZING, 'aegis_6j': {'base': 9, 'adds': 'UNCHANGED'}},
           {**SYNTHETIC_SIZING, 'dj30_mym_p250': {'risk_multiplier': '2/4', 'cap_reserve_multiplier': '1/2', 'adds': 'OFF'}},
           {**SYNTHETIC_SIZING, 'aegis_6j': {'base': 4.0, 'adds': 'UNCHANGED'}},
           {**SYNTHETIC_SIZING, 'orb_mnq_v7': {'base': 0}},
           {**SYNTHETIC_SIZING, 'orb_mnq_v7': {'base': 0, 'adds': 'UNCHANGED', 'extra': 1}},
           {k: v for k, v in SYNTHETIC_SIZING.items() if k != 'vanguard_mgc'},
           {**SYNTHETIC_SIZING, 'gold_mgc': {'base': 1, 'adds': 'UNCHANGED'}},
           [], None]
    for sizing in bad:
        with pytest.raises(ValueError) as expected:
            validate_size_vector(sizing)
        with pytest.raises(ValueError) as refused:
            _parse(_v2(sizing))
        assert str(refused.value) == str(expected.value)
    with pytest.raises(ValueError, match='complete explicit startup policy fields'):
        _parse({k: v for k, v in _v2().items() if k != 'sizing'})          # v2 without sizing
    with pytest.raises(ValueError, match='complete explicit startup policy fields'):
        _parse(_startup(sizing=SYNTHETIC_SIZING))                          # v1 with sizing
    with pytest.raises(ValueError, match='complete explicit startup policy fields'):
        _parse({**_v2(), 'extra': 1})
    assert _parse(_v2()).size_vector.as_mapping() == SYNTHETIC_SIZING      # twin


def _v2_composition(tmp_path, monkeypatch, sizing=SYNTHETIC_SIZING):
    """The TEST_ONLY composition with a v2 startup policy written before signing."""
    import composition_fixture as fixture_module
    original_builder = fixture_module.build_artifacts
    def v2_startup(root, **kwargs):
        fixture = original_builder(root, **kwargs)
        doc = json.loads(fixture.payloads['source_startup_policy'])
        assert doc['schema'] == 'qualification-source-startup/v1'
        doc.update(schema='qualification-source-startup/v2', sizing=sizing)
        fixture.payloads['source_startup_policy'] = fixture_module.encoded(doc)
        (root/fixture.paths['source_startup_policy']).write_bytes(fixture.payloads['source_startup_policy'])
        return fixture
    monkeypatch.setattr(fixture_module, 'build_artifacts', v2_startup)
    return fixture_module.build_verified_composition(tmp_path).source


def test_Y4(tmp_path, monkeypatch):
    """A synthetic source with a v2 policy passes its vector to every BookReplay it constructs."""
    from c1_rail.book_policy import IDENTITY_SIZE_VECTOR, validate_size_vector
    from c1_rail.qualification import replay as replay_module
    engines = []
    class Recorded(replay_module.BookReplay):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            engines.append(self)
    source = _v2_composition(tmp_path, monkeypatch)
    monkeypatch.setattr(replay_module, 'BookReplay', Recorded)
    expected = validate_size_vector(SYNTHETIC_SIZING)
    assert source.prepared.startup.size_vector == expected != IDENTITY_SIZE_VECTOR
    result = _five_session_replay(source)
    assert len(engines) == 1 and engines[0].size_vector is source.prepared.startup.size_vector
    # The fixture's only filling leg is ORB, off in this vector: every entry is refused.
    assert [row.fills for row in result.sessions] == [0] * 5
    assert any('zero policy quantity' in event.detail for event in result.events)


@SCREEN
def test_Y5(tmp_path, monkeypatch):
    """Regression row: the seven sealed methods keep their source text (test_K7 re-run as evidence)."""
    test_K7(tmp_path, monkeypatch)
