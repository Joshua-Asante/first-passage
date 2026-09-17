"""Retained synthetic input generation exercises real byte parsers, never authority."""
import hashlib
import pytest

from composition_fixture import build_artifacts
from c1_rail.qualification.production_source import (
    decode_admitted_csv, parse_historical_admission, parse_source_calendar,
    parse_population_index, parse_schedule_execution_evidence, parse_startup_policy,
)


def test_complete_live_runtime_can_bind_adjudicator(tmp_path, monkeypatch):
    from composition_fixture import build_verified_composition
    from c1_rail.qualification.result_adjudication import frozen_adjudicator
    setup = build_verified_composition(tmp_path)
    bound = frozen_adjudicator(setup.contract, retained_source_bytes=setup.retained_source_bytes,
                              runtime_inventory=setup.runtime_inventory)
    bound.verify_for(setup.contract)
    import sys
    targets = [
        (sys.modules['c1_rail.qualification.runner'], 'evaluate_replay'),
        (sys.modules['c1_rail.qualification.replay'].BookReplay, 'run'),
        (sys.modules['c1_rail.qualification.production'].ProductionExecutor, 'run_stage'),
        (sys.modules['c1_rail.qualification.seal'], 'seal_e1_pass'),
        (sys.modules['fp_qualification_port_orb_mnq_v7'].Adapter, 'on_bar'),
    ]
    for owner, name in targets:
        with monkeypatch.context() as changed:
            changed.setattr(owner, name, lambda *args, **kwargs: None)
            with pytest.raises(ValueError, match='runtime dependency'):
                bound.verify_for(setup.contract)
        bound.verify_for(setup.contract)


def test_retained_fixture_is_self_consistent_and_uses_actual_source_schemas(tmp_path):
    fixture = build_artifacts(tmp_path)
    raw = fixture.payloads
    admission = parse_historical_admission(raw['step3_admission_contract'], raw['step3_independent_acceptance'])
    panels = tuple((leg, decode_admitted_csv(raw[leg+'_panel'], digest)) for leg,digest in admission.panels)
    assert len(panels)==4 and len(panels[0][1])>100
    digests = {role:hashlib.sha256(value).hexdigest() for role,value in raw.items()}
    clock, tail = parse_source_calendar(raw['source_calendar'], artifact_digests=digests)
    index = parse_population_index(raw['population_index'], populations=fixture.populations)
    index.validate_calendar(clock)
    index.validate_provider_generation(panels, expected_binding=fixture.source_binding)
    assert tail and len(index.expected_source_dates)>130
    assert parse_startup_policy(raw['source_startup_policy']).path_start_date.year==2030
    assert parse_schedule_execution_evidence(raw['schedule_execution_evidence'])
    assert all((tmp_path/fixture.paths[role]).read_bytes()==value for role,value in raw.items())
    from composition_fixture import PORT_ROLES
    identity=fixture.identity_fields()
    assert identity['effective_settings_sha256']==digests['effective_settings_successor']
    assert all(identity['port_runtime_pins'][leg]['runtime_sha256']==digests[role] for leg,role in PORT_ROLES.items())


def test_genuine_test_key_g1_contract_cannot_enter_production_source(tmp_path):
    """TEST_ONLY signature verification never grants accepted source identities."""
    from composition_fixture import build_verified_composition
    from c1_rail.qualification.production_source import ProductionSource, ProductionSourceNeedsContext
    contract=build_verified_composition(tmp_path).contract
    assert contract.approval.authority_class=='TEST_ONLY'
    with pytest.raises((ProductionSourceNeedsContext,ValueError,TypeError),match='operator|OPERATOR|production|domain'):
        ProductionSource.build(contract,artifact_root=tmp_path)


def test_internal_composition_routes_reject_unverified_caller_objects(tmp_path):
    from c1_signal_daemon.book_adapters import _load_composition_adapters
    from c1_rail.qualification.production_source import ProductionSource
    with pytest.raises((TypeError,ValueError),match='contract|G1|domain'):
        _load_composition_adapters(object(),retained_bytes={})
    with pytest.raises((TypeError,ValueError),match='contract|G1|domain'):
        ProductionSource._build_composition(object(),artifact_root=tmp_path)


def test_fixture_signed_domain_pins_three_distinct_role_keys(tmp_path):
    from composition_fixture import verified_domain
    domain,private,keys=verified_domain(build_artifacts(tmp_path))
    assert set(private)=={'test-freeze','test-producer','test-seal'}
    assert len({key.public_key for key in keys.values()})==3
    assert dict(domain.trusted_key_sha256)=={name:hashlib.sha256(key.public_key).hexdigest() for name,key in keys.items()}
    assert domain.freeze_key_ids==('test-freeze',)
    assert domain.result_key_ids==('test-producer',)
    assert domain.seal_key_ids==('test-seal',)


def test_fixture_domain_is_a_real_signed_immutable_test_receipt(tmp_path):
    from composition_fixture import verified_domain
    from c1_rail.qualification.trust_domain import require_validated_trust_domain
    fixture=build_artifacts(tmp_path).with_runtime_artifacts(tmp_path)
    domain,_,_=verified_domain(fixture)
    assert require_validated_trust_domain(domain) is domain
    assert domain.authority_class=='TEST_ONLY' and domain.permits_synthetic
    assert len(fixture.ordinary_modules)>40
    assert domain.runtime_code_roles['qualification_runner']=='c1_rail.qualification.orchestration'


def test_real_signed_g1_builds_only_the_internal_composition_source(tmp_path):
    from composition_fixture import build_verified_composition
    from c1_rail.qualification.production_source import ProductionSource
    from c1_signal_daemon.book_adapters import load_qualification_adapters
    verified=build_verified_composition(tmp_path)
    assert verified.contract.trust_domain is verified.domain
    verified.source.verify_for(verified.contract)
    assert len(verified.source.sessions)==len(verified.contract.populations['FULL'])
    assert len(verified.runtime_inventory.modules)==len(verified.loaded_modules)
    with pytest.raises(ValueError,match='production|OPERATOR'):
        ProductionSource.build(verified.contract,artifact_root=tmp_path)
    with pytest.raises(ValueError,match='production|OPERATOR'):
        load_qualification_adapters(verified.contract,retained_bytes=dict(verified.source.prepared.retained_bytes))


def test_fixture_ports_plant_a_passing_continuous_path_without_claiming_authority(tmp_path):
    """Validate workload design; this is deliberately not the G1 composition test."""
    from datetime import date
    from types import ModuleType
    from mc.simulation import EvaluationState
    from c1_signal_daemon.book_protocol import Mode
    from c1_signal_daemon.book_adapters import ADAPTERS
    from c1_rail.book_policy import candidate_book_protection_policy
    from c1_rail.qualification.panel import build_panel
    from c1_rail.qualification.paths import PathAssembler
    from c1_rail.qualification.replay import BookReplay, Instrument
    from c1_rail.qualification.runner import evaluate_replay
    from composition_fixture import PORT_ROLES
    import json
    fixture=build_artifacts(tmp_path)
    raw=fixture.payloads
    panels={leg:decode_admitted_csv(raw[leg+'_panel'],sha) for leg,sha in fixture.source_binding['panel_sha256'].items()}
    clock,_=parse_source_calendar(raw['source_calendar'],artifact_digests={r:hashlib.sha256(v).hexdigest() for r,v in raw.items()})
    report=build_panel(panels,schedules=dict(clock.schedules),expected_dates=tuple(day for day,_ in clock.schedules),active=lambda leg,instant:True)
    settings=json.loads(raw['effective_settings_successor'])
    adapters={}
    for leg,role in PORT_ROLES.items():
        module=ModuleType('fixture_'+leg)
        exec(compile(raw[role],role,'exec'),module.__dict__)
        adapters[leg]=module.build(mode=Mode.NORMAL,**settings[leg]['adapter'])
    instruments={s.leg_id:Instrument(s.mintick,s.pointvalue,1,.91,True) for s in ADAPTERS}
    initial=EvaluationState(100000,100000,100000,0,0)
    engine=BookReplay(adapters,instruments,policy=candidate_book_protection_policy(),initial_state=initial,
        sizing_inputs=lambda leg,action,pb:{'lifecycle_tier':'AUTHORIZED'},
        schedule_quotes=parse_schedule_execution_evidence(raw['schedule_execution_evidence']))
    path=PathAssembler(date(2030,1,7)).assemble((report.sessions[:5],),horizon_sessions=5)
    replay=engine.run(path)
    outcome=evaluate_replay(replay,initial_state=initial)
    assert outcome.status=='PASS'
    assert all(adapter.bar_count==20 for adapter in adapters.values())
    assert all(row.flat_before_deadline and row.end_edge.is_flat for row in replay.sessions)
