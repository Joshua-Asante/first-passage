import hashlib
import json

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
    left, right = evidence.validate_split(path[0], path[0].bars[0], {'aegis_6j': bar}, split)
    assert right['aegis_6j'].ts == split
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


@pytest.mark.parametrize('name',('replay','verify_for','proof'))
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
