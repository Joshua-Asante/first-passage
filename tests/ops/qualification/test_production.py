from decimal import Decimal
from types import SimpleNamespace

import pytest

from c1_rail.qualification.production import _stage_request, _initial_state, _part_a_request


def _issued_driver(tmp_path):
    from composition_fixture import build_verified_composition
    from test_contract import NOW
    from c1_rail.qualification.attempt import AttemptStore
    from c1_rail.qualification.production import _composition_executor
    setup=build_verified_composition(tmp_path/'TEST_ONLY-inputs')
    store=AttemptStore.open(tmp_path/'TEST_ONLY-journal.sqlite',campaign_id='TEST_ONLY-driver',
        contract_digest=setup.contract.contract_sha256,trust_domain_sha256=setup.domain.sha256,
        boot_id='TEST_ONLY-driver-boot',now=NOW)
    return _composition_executor(setup.contract,setup.source,store),setup,store


def contract():
    specs={name:SimpleNamespace(exact_depth=depth) for name,depth in
           [('N1',73),('N2',811),('PART_B',811),('N3',913)]}
    part=SimpleNamespace(paths_per_population_per_panel=127,initial_panels=100,expanded_panels=200,
        percentile=Decimal('.05'),percentile_method='INVERSE_ECDF_LEFT',
        expansion_center_p5=Decimal('.95'),expansion_tolerance=Decimal('.01'))
    return SimpleNamespace(stage_specs=specs,replay=SimpleNamespace(horizon_sessions=500,
        inner_block_sessions=5,outer_months=6,root_rng_namespace='frozen-example',part_a=part),
        initial_state=SimpleNamespace(original_basis=Decimal('100000'),current_equity=Decimal('101000'),
        historical_eod_peak=Decimal('102000'),prior_trade_days=8,prior_max_day_profit=Decimal('321')))


def test_production_requests_derive_approved_depths_without_proposal_constants():
    frozen=contract()
    assert _stage_request(frozen,'n1',12.).depths==(('FULL',73),('H1',73),('H2',73))
    assert _stage_request(frozen,'n2',12.).depths==(('FULL',811),('H1',811),('H2',811))
    with pytest.raises(ValueError,match='E1'):
        _stage_request(frozen,'n3',12.)


def test_initial_state_preserves_approved_nonpristine_history():
    state=_initial_state(contract())
    assert (state.original_basis,state.current_equity,state.historical_eod_peak,
            state.prior_trade_days,state.prior_max_day_profit)==(100000,101000,102000,8,321)


def test_production_part_a_maps_only_supported_frozen_percentile():
    from datetime import date
    frozen=contract()
    request=_part_a_request(frozen,date(2030,1,7),12.)
    assert request.depth==127 and request.percentile_method=='nearest_rank'
    frozen.replay.part_a.percentile_method='OTHER'
    with pytest.raises(ValueError,match='percentile'):
        _part_a_request(frozen,date(2030,1,7),12.)


def test_deadline_exception_still_checks_final_cpu_and_memory_budget(monkeypatch):
    from c1_rail.qualification.production import ProductionExecutor
    from c1_rail.qualification.replay import ReplayDeadlineFailure
    from c1_rail.qualification.runner import NeedsContext
    driver=object.__new__(ProductionExecutor)
    calls=[]
    def budget(self):
        calls.append(True)
        if len(calls)==2:
            raise NeedsContext('memory budget exceeded')
        return 5.
    def replay(path):
        raise ReplayDeadlineFailure(None)
    monkeypatch.setattr(ProductionExecutor,'_budget',budget)
    driver.source=SimpleNamespace(replay=replay)
    with pytest.raises(NeedsContext,match='memory budget'):
        driver._replay(())
    assert len(calls)==2


def test_new_executor_cannot_reuse_issued_checkpoint_capability(tmp_path):
    from datetime import datetime,timezone
    from c1_rail.qualification.attempt import AttemptStore,AttemptConflict
    from c1_rail.qualification.production import _composition_executor
    from composition_fixture import build_verified_composition
    setup=build_verified_composition(tmp_path/'TEST_ONLY-inputs')
    domain=setup.domain
    now=datetime(2026,9,15,tzinfo=timezone.utc)
    store=AttemptStore.open(tmp_path/'attempt.sqlite',campaign_id='isolated-test',
        contract_digest=setup.contract.contract_sha256,trust_domain_sha256=domain.sha256,boot_id='test-boot',now=now)
    store.reserve('TB_E1',b'{"fixture":true}',now=now)
    claim=store.claimed_reservation('TB_E1')
    store.start_once('TB_E1',claim,now=now)
    claim=store.claimed_reservation('TB_E1')
    dispatch=store.start_checkpoint_once('N1',claim,b'{"fixture":true}',now=now)
    def isolated_driver():
        return _composition_executor(setup.contract,setup.source,store)
    isolated_driver()._admit(dispatch,'N1')
    with pytest.raises(AttemptConflict,match='freshly issued'):
        isolated_driver()._admit(dispatch,'N1')


def test_signed_test_domain_cannot_enter_public_production_executor():
    from test_trust_domain import case,validate
    from c1_rail.qualification.contract import ValidatedFrozenContract
    from c1_rail.qualification.production import ProductionExecutor
    doc,policy,private,keys=case()
    domain=validate(doc,policy,private,keys)
    frozen=object.__new__(ValidatedFrozenContract)
    object.__setattr__(frozen,'trust_domain',domain)
    object.__setattr__(frozen,'approval',SimpleNamespace(authority_class='TEST_ONLY'))
    with pytest.raises(TypeError,match='operator-validated'):
        ProductionExecutor(frozen,object(),object())


def test_executor_refuses_reconstructed_domain_before_dispatch(tmp_path):
    from dataclasses import replace
    driver,setup,store=_issued_driver(tmp_path)
    driver._trust_domain=replace(setup.domain)
    with pytest.raises(ValueError,match='trust domain'):
        driver._checked_domain()
    assert store.stage('TB_E1')['state']=='UNRESERVED'


def test_executor_rechecks_issued_domain_identity_after_construction(tmp_path):
    from test_trust_domain import case,validate
    driver,setup,store=_issued_driver(tmp_path)
    first=setup.domain;second=validate(*case())
    assert driver._checked_domain() is first
    driver._trust_domain=second
    with pytest.raises(ValueError,match='trust domain'):
        driver._checked_domain()


def test_executor_refuses_mutated_issued_contract_before_consuming_dispatch(tmp_path):
    driver,setup,store=_issued_driver(tmp_path)
    budget=setup.contract.replay.budget
    original=budget.maximum_memory_bytes
    try:
        object.__setattr__(budget,'maximum_memory_bytes',original+1)
        with pytest.raises(ValueError,match='changed|mutat'):
            driver._checked_domain()
        assert store.stage('TB_E1')['state']=='UNRESERVED'
    finally:
        object.__setattr__(budget,'maximum_memory_bytes',original)
    assert driver._checked_domain() is setup.domain


def test_executor_rejects_source_replacement_before_dispatch(tmp_path):
    driver,setup,store=_issued_driver(tmp_path)
    calls=[]
    driver.source=SimpleNamespace(verify_for=lambda contract:calls.append('verify'),
                                  replay=lambda path:calls.append('replay'))
    with pytest.raises(ValueError,match='executor inputs'):
        driver._admit(object(),'N1')
    assert calls==[] and store.stage('TB_E1')['state']=='UNRESERVED'


def test_executor_state_and_cached_provider_cannot_be_reconfigured(tmp_path):
    driver,setup,store=_issued_driver(tmp_path)
    with pytest.raises(ValueError,match='already initialized'):
        driver._initialize(setup.contract,setup.source,store,setup.domain)
    initial=driver.initial_state
    with pytest.raises(AttributeError):
        driver.initial_state=SimpleNamespace(current_equity=999999)
    with pytest.raises(AttributeError):
        object.__setattr__(driver,'_provider',lambda **kw:None)
    object.__setattr__(initial,'current_equity',999999)
    assert driver.initial_state.current_equity==float(setup.contract.initial_state.current_equity)
    assert store.stage('TB_E1')['state']=='UNRESERVED'
