"""Recording journal tests; no source, approval authority or outcome execution."""
from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace as NS
import hashlib
import json

import pytest

from c1_rail.qualification.model import PathOutcome
from c1_rail.qualification.runner import StageRun
from c1_rail.qualification.part_a import SyntheticPanelResult, SyntheticPartAResult
from c1_rail.qualification.orchestration import _execute_e1, canonical_bytes


NOW=datetime(2026,9,15,tzinfo=timezone.utc)
PASS=PathOutcome('PASS',1,None,())
FAIL=PathOutcome('FAILURE',None,'fixture',())


def contract():
    def stage(name,pops,depth):
        return NS(name=name,population_counts={p:(depth,) for p in pops},exact_depth=depth,
                  max_failures_per_population=0,rng_namespace=name.lower())
    stages={'N1':stage('N1',('FULL','H1','H2'),10),'N2':stage('N2',('FULL',),100),
            'PART_B':stage('PART_B',('H1','H2'),100),'PART_A':stage('PART_A',('REGIME',),2)}
    part=NS(initial_panels=2,expanded_panels=4,paths_per_population_per_panel=2,
            percentile=Decimal('.05'),percentile_method='INVERSE_ECDF_LEFT',
            expansion_center_p5=Decimal('.95'),expansion_tolerance=Decimal('.01'))
    return NS(contract_sha256='a'*64,trust_domain_sha256='d'*64,stage_specs=stages,
        populations={'FULL':('a','b'),'H1':('a',),'H2':('b',)},
        replay=NS(root_rng_namespace='test',horizon_sessions=500,stages=stages,part_a=part,
                  decision_rules=NS(failure_ceiling=Decimal('.05'),alpha=Decimal('.05'),
                                    speed_target=Decimal('.5'),speed_horizon_sessions=200)))


class Store:
    campaign_id='test-attempt'
    contract_digest='a'*64
    trust_domain_sha256='d'*64
    def __init__(self):
        self.state='UNRESERVED';self.checkpoints={};self.log=[]
    def reserve(self,stage,binding_bytes,*,now):
        if self.state=='UNRESERVED':self.state='RESERVED';self.binding=binding_bytes
        elif self.binding!=binding_bytes:raise ValueError('binding conflict')
        self.log.append(('reserve',stage))
    def claimed_reservation(self,stage):
        return NS(stage=stage,state=self.state,campaign_id=self.campaign_id,
                  contract_digest=self.contract_digest,reservation_event_digest='b'*64,
                  binding_sha256=hashlib.sha256(self.binding).hexdigest())
    def start_once(self,stage,claim,*,now):
        if self.state!='RESERVED':raise ValueError('already dispatched')
        self.state='STARTED_IN_DOUBT';self.log.append(('start',stage))
    def verify_claim(self,claim,*,require_state):
        assert self.state==claim.state==require_state
        return claim
    def start_checkpoint_once(self,name,claim,binding,*,now):
        if name in self.checkpoints:raise ValueError('already dispatched')
        self.checkpoints[name]=NS(state='STARTED_IN_DOUBT',binding=binding)
        self.log.append(('dispatch',name))
        return NS(checkpoint=name,dispatch_event_digest=hashlib.sha256(name.encode()).hexdigest(),
                  binding_sha256=hashlib.sha256(binding).hexdigest())
    def complete_checkpoint(self,name,dispatch,receipt,*,now):
        assert self.checkpoints[name].state=='STARTED_IN_DOUBT'
        self.checkpoints[name].state='COMPLETED';self.checkpoints[name].receipt=receipt
        self.log.append(('complete',name));return receipt
    def consume_checkpoint_dispatch(self, dispatch):
        assert self.checkpoints[dispatch.checkpoint].state == 'STARTED_IN_DOUBT'
        return dispatch


class Executor:
    def __init__(self,store,fail=None,crash=None):self.store=store;self.fail=fail;self.crash=crash
    def run_stage(self,stage,dispatch):
        name=stage.upper()
        assert self.store.checkpoints[name].state=='STARTED_IN_DOUBT'
        self.store.log.append(('callback',name))
        if self.crash==name:raise RuntimeError('planted crash')
        depth=10 if stage=='n1' else 100
        rows=[]
        for p in ('FULL','H1','H2'):
            values=(PASS,)*depth
            if self.fail==name and p=='H1':values=(FAIL,)*depth
            rows.append((p,values))
        return StageRun(stage,tuple(rows),.01,.1,True)
    def run_part_a(self,dispatch,full_pass_rate):
        assert self.store.checkpoints['PART_A'].state=='STARTED_IN_DOUBT'
        assert full_pass_rate==Decimal(1)
        self.store.log.append(('callback','PART_A'))
        panels=tuple(SyntheticPanelResult(i,('a','b'),(PASS,PASS)) for i in range(2))
        return SyntheticPartAResult(panels,1,1,False,True,None,.01,.1,.1,True)


def run(store,executor,configuration=None,**kw):
    return _execute_e1(configuration or contract(),store=store,executor=executor,
        preflight_binding=canonical_bytes({'attempt_id':store.campaign_id,'contract_sha256':store.contract_digest,
                                           'trust_domain_sha256':'d'*64}),
        exact_depth_approval_sha256='c'*64,now=lambda:NOW,synthetic=True,**kw)


def test_dispatch_precedes_callbacks_and_joint_n2_has_no_part_b_redraw():
    store=Store();result=run(store,Executor(store))
    assert [x for x in store.log if x[0]=='callback']==[('callback','N1'),('callback','N2'),('callback','PART_A')]
    for name in ('N1','N2','PART_A'):
        assert store.log.index(('dispatch',name))<store.log.index(('callback',name))<store.log.index(('complete',name))
    assert result.decisions==(('LEGALITY','PASS'),('N1','PASS'),('N2','PASS'),('PART_B','PASS'),('PART_A','PASS'))
    inventory=json.loads(result.path_inventory_bytes)['records']
    assert len({r['seed_input_sha256'] for r in inventory})==len(inventory)
    assert len([r for r in inventory if r['stage']=='N2'])==100
    assert len([r for r in inventory if r['stage']=='PART_B'])==200


def test_trust_domain_is_bound_to_every_seed_plan_receipt_and_result():
    store=Store();result=run(store,Executor(store))
    assert result.trust_domain_sha256=='d'*64
    assert json.loads(result.path_inventory_bytes)['trust_domain_sha256']=='d'*64
    for checkpoint in store.checkpoints.values():
        plan=json.loads(checkpoint.binding)
        assert plan['trust_domain_sha256']=='d'*64
        assert all(seed['trust_domain_sha256']=='d'*64 for seed in plan['seed_inputs'])
        assert json.loads(checkpoint.receipt)['trust_domain_sha256']=='d'*64


def test_foreign_trust_domain_preflight_or_journal_cannot_dispatch():
    for target in ('preflight','journal'):
        store=Store()
        if target=='journal':store.trust_domain_sha256='e'*64
        with pytest.raises(ValueError,match='trust domain'):
            _execute_e1(contract(),store=store,executor=Executor(store),
                preflight_binding=canonical_bytes({'attempt_id':store.campaign_id,
                    'contract_sha256':store.contract_digest,
                    'trust_domain_sha256':('e' if target=='preflight' else 'd')*64}),
                exact_depth_approval_sha256='c'*64,now=lambda:NOW,synthetic=True)
        assert store.state=='UNRESERVED' and store.log==[]


@pytest.mark.parametrize('failure,callbacks',[('N1',['N1']),('N2',['N1','N2'])])
def test_failed_prefix_stops_later_dispatch(failure,callbacks):
    store=Store();result=run(store,Executor(store,fail=failure))
    assert [name for action,name in store.log if action=='callback']==callbacks
    assert result.passed is False
    assert 'PART_A' not in store.checkpoints


def test_crash_leaves_checkpoint_in_doubt_and_retry_cannot_draw_again():
    store=Store();executor=Executor(store,crash='N2')
    with pytest.raises(RuntimeError,match='planted'):run(store,executor)
    assert store.checkpoints['N2'].state=='STARTED_IN_DOUBT'
    before=sum(action=='callback' for action,_ in store.log)
    with pytest.raises(ValueError,match='already dispatched'):run(store,executor)
    assert sum(action=='callback' for action,_ in store.log)==before


def test_partial_depth_is_not_recorded_as_completed_or_replaced():
    class Short(Executor):
        def run_stage(self,stage,dispatch):
            value=super().run_stage(stage,dispatch)
            return StageRun(stage,tuple((p,rows[:-1]) for p,rows in value.populations),.01,.1,True)
    store=Store()
    with pytest.raises(ValueError,match='depth differs'):run(store,Short(store))
    assert store.checkpoints['N1'].state=='STARTED_IN_DOUBT'
    assert 'N2' not in store.checkpoints


def test_synthetic_callback_cannot_relabel_its_run_as_production():
    class WrongRoute(Executor):
        def run_stage(self,stage,dispatch):
            value=super().run_stage(stage,dispatch)
            return StageRun(stage,value.populations,.01,.1,False)
    store=Store()
    with pytest.raises(ValueError,match='authority route'):run(store,WrongRoute(store))
    assert store.checkpoints['N1'].state=='STARTED_IN_DOUBT'


def test_recording_executor_cannot_select_production_route_on_private_engine():
    store=Store()
    with pytest.raises(TypeError,match='concrete production executor'):
        _execute_e1(contract(),store=store,executor=Executor(store),
            preflight_binding=canonical_bytes({'attempt_id':store.campaign_id,
                                               'contract_sha256':store.contract_digest}),
            exact_depth_approval_sha256='c'*64,now=lambda:NOW,synthetic=False)
    assert store.state=='UNRESERVED' and store.log==[]


def test_part_a_dispatch_commits_maximal_streams_then_receipt_retains_actual_prefix():
    store=Store();result=run(store,Executor(store))
    plan=json.loads(store.checkpoints['PART_A'].binding)
    assert len(plan['seed_inputs'])==4*(1+2)
    assert {(r['panel_index'],r['purpose'],r['path_index']) for r in plan['seed_inputs']}=={
        (panel,purpose,index) for panel in range(4) for purpose,indices in [('outer',[0]),('path',[0,1])]
        for index in indices}
    receipt=json.loads(store.checkpoints['PART_A'].receipt)
    panels=receipt['extra']['panels']
    assert [p['panel_index'] for p in panels]==[0,1]
    assert all(p['source_session_ids']==['a','b'] for p in panels)
    assert len({p['panel_id'] for p in panels})==2
    assert receipt['stage_input_sha256']=={'PART_A':dict(result.stage_input_sha256)['PART_A']}


def test_checkpoint_receipt_input_digests_are_checkpoint_local():
    store=Store();result=run(store,Executor(store))
    expected={'N1':('N1',),'CUTOFF':(),'N2':('N2','PART_B'),'PART_A':('PART_A',)}
    inputs=dict(result.stage_input_sha256)
    for name,raw in result.checkpoint_receipts:
        assert json.loads(raw)['stage_input_sha256']=={stage:inputs[stage] for stage in expected[name]}


def test_public_production_route_rejects_recording_contract_before_dispatch():
    from c1_rail.qualification.orchestration import run_production_e1
    store=Store()
    with pytest.raises(ValueError,match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        run_production_e1(contract(),source=object(),store=store,preflight=object(),
            exact_depth_approval_bytes=b'',trusted_keys={},now=lambda:NOW)
    assert store.state=='UNRESERVED' and store.log==[]


def test_public_production_route_rejects_test_authority_before_dispatch():
    from c1_rail.qualification.contract import ValidatedFrozenContract
    from c1_rail.qualification.preflight import PreflightReceipt
    from c1_rail.qualification.orchestration import run_production_e1
    # Exact class alone grants no production authority. No signature is minted.
    fake=object.__new__(ValidatedFrozenContract)
    object.__setattr__(fake,'approval',NS(authority_class='TEST_ONLY'))
    receipt=PreflightReceipt('test-attempt','a'*64,'d'*64,'b'*64,NS(authority_class='TEST_ONLY'),'unused')
    store=Store()
    with pytest.raises(ValueError,match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        run_production_e1(fake,source=object(),store=store,preflight=receipt,
            exact_depth_approval_bytes=b'',trusted_keys={},now=lambda:NOW)
    assert store.state=='UNRESERVED' and store.log==[]


def test_part_a_expansion_keeps_initial_panel_prefix_and_recomputes_decision():
    config=contract();config.replay.part_a.expansion_center_p5=Decimal('.5')
    class Expanded(Executor):
        def run_part_a(self,dispatch,full_pass_rate):
            self.store.log.append(('callback','PART_A'))
            panels=tuple(SyntheticPanelResult(i,('a','b'),(PASS,FAIL) if i<2 else (PASS,PASS)) for i in range(4))
            # Controller derives verdict from retained paths, not these labels.
            return SyntheticPartAResult(panels,.5,.5,True,False,'wrong-label',.01,.1,.1,True)
    store=Store();result=run(store,Expanded(store),configuration=config)
    assert result.decisions[-1]==('PART_A','PASS')
    rows=dict(dict(result.outcomes)['PART_A'])['REGIME']
    assert rows[:4]==(PASS,FAIL,PASS,FAIL)
    assert len(json.loads(result.path_inventory_bytes)['records'])==30+300+8


def test_missing_required_expansion_refuses_receipt_without_more_draws():
    config=contract();config.replay.part_a.expansion_center_p5=Decimal(1)
    store=Store()
    with pytest.raises(ValueError,match='expansion decision'):
        run(store,Executor(store),configuration=config)
    assert store.checkpoints['PART_A'].state=='STARTED_IN_DOUBT'


def test_expired_authorization_before_n2_dispatch_does_not_invoke_it():
    calls=[]
    def authorize(instant):
        calls.append(1)
        if len(calls)==5:raise ValueError('expired approval')
    store=Store()
    with pytest.raises(ValueError,match='expired approval'):
        run(store,Executor(store),authorize=authorize)
    assert 'N2' not in store.checkpoints
    assert ('callback','N2') not in store.log


def test_each_durable_start_uses_its_authorized_instant():
    from datetime import timedelta
    authorized = []
    ticks = iter(NOW + timedelta(microseconds=n) for n in range(100))
    def authorize(instant):
        authorized.append(instant)
    class TimedStore(Store):
        def reserve(self, *args, now):
            assert now == authorized[-1]
            return super().reserve(*args, now=now)
        def start_once(self, *args, now):
            assert now == authorized[-1]
            return super().start_once(*args, now=now)
        def start_checkpoint_once(self, *args, now):
            assert now == authorized[-1]
            return super().start_checkpoint_once(*args, now=now)
    store = TimedStore()
    _execute_e1(contract(), store=store, executor=Executor(store),
        preflight_binding=canonical_bytes({'attempt_id':store.campaign_id,
            'contract_sha256':store.contract_digest, 'trust_domain_sha256':'d'*64}),
        exact_depth_approval_sha256='c'*64, now=lambda:next(ticks), synthetic=True,
        authorize=authorize)
    assert len(authorized) == 6


def test_receipt_write_failure_leaves_completed_work_in_doubt_not_rerunnable():
    class BrokenReceipt(Store):
        def complete_checkpoint(self,name,dispatch,receipt,*,now):
            raise OSError('disk failure')
    store=BrokenReceipt();executor=Executor(store)
    with pytest.raises(OSError,match='disk failure'):run(store,executor)
    assert store.checkpoints['N1'].state=='STARTED_IN_DOUBT'
    with pytest.raises(ValueError,match='already dispatched'):run(store,executor)
    assert store.log.count(('callback','N1'))==1


class G2Executor:
    """Synthetic callbacks assert dispatch in the real SQLite journal."""
    def __init__(self,store,fail=None,crash=None):
        self.store=store;self.calls=[];self.fixture=Executor(Store(),fail=fail,crash=crash)
    def run_stage(self,stage,dispatch):
        name=stage.upper()
        row=next(r for r in self.store.checkpoints() if r['checkpoint']==name)
        assert row['state']=='STARTED_IN_DOUBT'
        assert row['dispatch_event_digest']==dispatch.dispatch_event_digest
        self.store.consume_checkpoint_dispatch(dispatch)
        self.calls.append(name)
        self.fixture.store.checkpoints[name]=NS(state='STARTED_IN_DOUBT')
        return self.fixture.run_stage(stage,dispatch)
    def run_part_a(self,dispatch,full_pass_rate):
        row=next(r for r in self.store.checkpoints() if r['checkpoint']=='PART_A')
        assert row['state']=='STARTED_IN_DOUBT'
        self.store.consume_checkpoint_dispatch(dispatch)
        self.calls.append('PART_A')
        self.fixture.store.checkpoints['PART_A']=NS(state='STARTED_IN_DOUBT')
        return self.fixture.run_part_a(dispatch,full_pass_rate)


@pytest.mark.parametrize('failure,completed',[
    ('N1',('N1','CUTOFF')),('N2',('N1','CUTOFF','N2')),
    (None,('N1','CUTOFF','N2','PART_A'))])
def test_real_g2_journal_retains_complete_or_terminal_prefix(tmp_path,failure,completed):
    from c1_rail.qualification.attempt import AttemptStore,TransitionError
    store=AttemptStore.open(tmp_path/'attempt.sqlite',campaign_id='test-attempt',
        contract_digest='a'*64,trust_domain_sha256='d'*64,boot_id='fixture',now=NOW)
    executor=G2Executor(store,fail=failure)
    result=run(store,executor)
    rows=store.checkpoints()
    assert tuple(r['checkpoint'] for r in rows if r['state']=='COMPLETED')==completed
    for row in rows:
        if row['checkpoint'] in completed:
            receipt=json.loads(row['receipt_bytes'])
            assert receipt['synthetic'] is True
            assert receipt['dispatch_event_digest']==row['dispatch_event_digest']
        else:assert row['state']=='PENDING'
    assert store.stage('TB_E1')['state']=='STARTED_IN_DOUBT'  # external authentication still owed
    assert store.result('TB_E1') is None
    before=tuple(executor.calls)
    with pytest.raises(TransitionError,match='already dispatched'):run(store,executor)
    assert tuple(executor.calls)==before
    assert result.passed is (failure is None)


def test_real_g2_crash_reopen_preserves_dispatch_and_refuses_reexecution(tmp_path):
    from c1_rail.qualification.attempt import AttemptStore,TransitionError
    path=tmp_path/'attempt.sqlite'
    store=AttemptStore.open(path,campaign_id='test-attempt',contract_digest='a'*64,
        trust_domain_sha256='d'*64,boot_id='first',now=NOW)
    executor=G2Executor(store,crash='N2')
    with pytest.raises(RuntimeError,match='planted'):run(store,executor)
    inspected=AttemptStore.inspect(path)
    n2=next(row for row in inspected['checkpoints'] if row['checkpoint']=='N2')
    assert n2['state']=='STARTED_IN_DOUBT' and n2['receipt_bytes'] is None
    resumed=AttemptStore.open(path,campaign_id='test-attempt',contract_digest='a'*64,
        trust_domain_sha256='d'*64,boot_id='second',now=NOW)
    again=G2Executor(resumed)
    with pytest.raises(TransitionError,match='already dispatched'):run(resumed,again)
    assert again.calls==[]
