"""R2a compact funding persistence; no OS enforcement claims."""
import json
import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.store import ExecutionStore
from test_campaign_budget import ATTEMPT, profile, clock, request, contract_budget, snap, start
from test_campaign_scheduler import schedule


def enrolled(tmp_path):
    config=profile()
    config.update(schema='qualification_campaign_budget_profile/v3',
        funding_intents='qualification_campaign_funding/v1',
        orchestration_cpu_ns={p:10 for p in config['phases']})
    store=CampaignStore(ExecutionStore(tmp_path/'journal.sqlite'))
    store.begin_admission(request(),encoded(config),encoded(clock()))
    store.bind_budget(ATTEMPT,contract_budget(),expected_revision=snap(store)['authority_revision'])
    return store


def claim(store,raw=None,t=11):
    return store.claim_scheduler_bootstrap(raw or schedule(),encoded(clock(t)))


def test_fresh_profile_enrolls_exact_v7_projection(tmp_path):
    store=enrolled(tmp_path)
    with store.store.transaction() as c:
        assert c.execute('PRAGMA user_version').fetchone()[0]==7
    assert json.loads(store.scheduler_status(ATTEMPT))['remaining_cpu_ns']==snap(store)['remaining_cpu_ns']
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT)==store.budget_snapshot(ATTEMPT)


def test_claim_funds_once_without_snapshot_decode_then_transfer_does_not_double_charge(tmp_path,monkeypatch):
    store=enrolled(tmp_path)
    before=store.budget_snapshot(ATTEMPT)
    original=store._budget
    monkeypatch.setattr(store,'_budget',lambda *a,**kw:pytest.fail('unfunded history decoding'))
    token,status=claim(store)
    assert len(token)==32
    assert json.loads(status)['reserved_cpu_ns']==120
    assert claim(store,t=12)[0] is None
    monkeypatch.setattr(store,'_budget',original)
    with pytest.raises(ValueError,match='funding'):
        store.budget_snapshot(ATTEMPT)
    with store.store.transaction() as c:
        assert c.execute('SELECT snapshot_bytes FROM full_campaign_budgets WHERE attempt_id=?',(ATTEMPT,)).fetchone()[0]==before
    reservation,enrollment=store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    assert json.loads(reservation)['limits']['cpu_ns']==60
    assert json.loads(enrollment)['work_id']=='worker'
    after=snap(store)
    assert after['reserved_cpu_ns']==120
    assert next(w for w in after['works'] if w['work_id']=='worker')['state']=='START_INTENT'
    assert claim(store,t=12)[0] is None
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT)==store.budget_snapshot(ATTEMPT)


def test_owner_loss_reopen_blocks_current_export_and_positive_authority(tmp_path):
    store=enrolled(tmp_path)
    claim(store)
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert claim(reopened,t=12)[0] is None
    with pytest.raises(ValueError,match='funding'):
        reopened.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError,match='owner'):
        reopened.materialize_scheduler_bootstrap(ATTEMPT,'worker',b'x'*32,'host1')


@pytest.mark.parametrize('change',[{'probe':'cpu'},{'role':'probe_g5'},{'signing_retry_of':'parent'}])
def test_compact_identity_conflict(tmp_path,change):
    store=enrolled(tmp_path); claim(store)
    with pytest.raises(ValueError,match='identity conflict'):
        claim(store,schedule(**change))


def test_terminal_clock_refusal_is_durable_without_history_decode(tmp_path,monkeypatch):
    store=enrolled(tmp_path)
    deadline=snap(store)['deadline_boottime_ns']
    monkeypatch.setattr(store,'_budget',lambda *a,**kw:pytest.fail('unfunded decode'))
    token,status=claim(store,t=deadline)
    assert token is None
    assert json.loads(status)['state']=='BUDGET_EXHAUSTED'
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert json.loads(reopened.scheduler_status(ATTEMPT))['state']=='BUDGET_EXHAUSTED'
    with pytest.raises(ValueError,match='funding'):
        reopened.budget_snapshot(ATTEMPT)


def test_old_profile_does_not_lazy_enroll(tmp_path):
    from test_campaign_supervision import metered
    store=metered(tmp_path)
    with pytest.raises(ValueError,match='fresh'):
        claim(store)
    with store.store.transaction() as c:
        assert c.execute('PRAGMA user_version').fetchone()[0]==6

@pytest.mark.parametrize('field,value',[('extra',1),('reserved_cpu_ns',True),('recovery_pending',0),('signing_work_ids',['a','b']),('state','FAKE')])
def test_compact_parser_rejects_malformed_authority_before_claim(tmp_path,field,value):
    store=enrolled(tmp_path)
    with store.store.transaction() as c:
        doc=json.loads(c.execute('SELECT body FROM full_campaign_funding').fetchone()[0])
        doc[field]=value
        c.execute('UPDATE full_campaign_funding SET body=?',(encoded(doc),))
    with pytest.raises(ValueError): claim(store)


def test_deleted_enrolled_projection_refuses_export_and_reopen(tmp_path):
    store=enrolled(tmp_path)
    with store.store.transaction() as c:
        c.execute('DELETE FROM full_campaign_funding_works')
        c.execute('DELETE FROM full_campaign_funding')
    with pytest.raises(ValueError,match='funding'):
        store.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError,match='funding'):
        ExecutionStore(store.store.path)


def test_pending_status_is_compact_and_does_not_decode_history(tmp_path,monkeypatch):
    store=enrolled(tmp_path); claim(store)
    monkeypatch.setattr(store,'_budget',lambda *a,**k:pytest.fail('decode'))
    status=store.diagnostic_status(ATTEMPT)
    assert status['state']=='METERED_INSPECTION_REQUIRED'
    assert status['reserved_cpu_ns']==120
    assert not status['current_policy_eligible']


def test_pending_void_preserves_debit_then_transfer_remains_invalid(tmp_path):
    from test_campaign_budget import NOW
    store=enrolled(tmp_path); token,_=claim(store)
    void=encoded(dict(schema='qualification_campaign_request/v1',operation='VOID',attempt_id=ATTEMPT,reason='stop',operator_approval_bytes='eA=='))
    store.void(void,now=NOW)
    reopened=CampaignStore(ExecutionStore(store.store.path))
    status=json.loads(reopened.scheduler_status(ATTEMPT))
    assert status['validity']=='VOID' and status['reserved_cpu_ns']==120
    reopened.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    assert snap(reopened)['validity']=='VOID'
    assert snap(reopened)['reserved_cpu_ns']==120


def test_materialization_failure_rolls_back_claim_transfer(tmp_path,monkeypatch):
    store=enrolled(tmp_path); token,_=claim(store)
    original=store._save_budget
    def fail(*a,**kw):
        original(*a,**kw)
        raise RuntimeError('crash')
    monkeypatch.setattr(store,'_save_budget',fail)
    with pytest.raises(RuntimeError): store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    assert json.loads(store.scheduler_status(ATTEMPT))['pending']
    monkeypatch.setattr(store,'_save_budget',original)
    store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    assert snap(store)['reserved_cpu_ns']==120


def test_insufficient_allowance_refuses_without_history_decode(tmp_path,monkeypatch):
    config=profile()
    config.update(schema='qualification_campaign_budget_profile/v3',funding_intents='qualification_campaign_funding/v1',
        orchestration_cpu_ns={p:10 for p in config['phases']})
    for limit in config['phases'].values(): limit['cpu_ns']=80_000_000
    store=CampaignStore(ExecutionStore(tmp_path/'journal.sqlite'))
    store.begin_admission(request(),encoded(config),encoded(clock()))
    store.bind_budget(ATTEMPT,contract_budget(),expected_revision=snap(store)['authority_revision'])
    for index in range(11):
        state=snap(store)
        store.reserve_work(ATTEMPT,'g5-'+str(index),'N1_G5',encoded(dict(limits=config['phases']['N1_G5'],clock=clock(11),input_sha256='d'*64)),expected_revision=state['authority_revision'])
    assert snap(store)['remaining_cpu_ns']==40_000_000
    ExecutionStore(store.store.path)
    monkeypatch.setattr(store,'_budget',lambda *a,**k:pytest.fail('decode'))
    token,status=claim(store)
    assert token is None and json.loads(status)['state']=='BUDGET_EXHAUSTED'
    ExecutionStore(store.store.path)

@pytest.mark.parametrize('action',['settle','recover','abort'])
def test_pending_negative_facts_commit_without_refund_or_current_export(tmp_path,action):
    from test_campaign_supervision import measured
    from test_campaign_budget import transition
    store=enrolled(tmp_path)
    if action=='settle': start(store)
    token,_=claim(store)
    if action=='settle':
        store.settle_work(ATTEMPT,'admission',measured())
        store.settle_work(ATTEMPT,'admission',measured())
        expected=60
    elif action=='recover':
        store.recover_work(ATTEMPT,'admission',encoded(clock(12)))
        store.recover_work(ATTEMPT,'admission',encoded(clock(12)))
        expected=120
    else:
        with store.store.transaction() as c: revision=store._budget(c,ATTEMPT)['authority_revision']
        store.record_work_transition(ATTEMPT,'admission',encoded(dict(schema='qualification_campaign_work_transition/v1',
            attempt_id=ATTEMPT,work_id='admission',state='ABORTED',clock=clock(12),data={})),expected_revision=revision)
        expected=120
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert json.loads(reopened.scheduler_status(ATTEMPT))['reserved_cpu_ns']==expected
    with pytest.raises(ValueError,match='funding'): reopened.budget_snapshot(ATTEMPT)


@pytest.mark.parametrize('field,value',[('input_sha256','f'*64),('claimed_event_head','f'*64),('claimed_authority_head','f'*64)])
def test_bootstrap_provenance_corruption_rejected_on_reopen(tmp_path,field,value):
    store=enrolled(tmp_path); claim(store)
    with store.store.transaction() as c:
        doc=json.loads(c.execute('SELECT body FROM full_campaign_bootstraps').fetchone()[0]); doc[field]=value
        c.execute('UPDATE full_campaign_bootstraps SET body=?',(encoded(doc),))
    with pytest.raises(ValueError,match='funding'): ExecutionStore(store.store.path)


def test_materialize_after_negative_clock_does_not_regress_or_restore_authority(tmp_path):
    store=enrolled(tmp_path); token,_=claim(store)
    store.recover_work(ATTEMPT,'admission',encoded(clock(12)))
    store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    assert snap(store)['last_clock']==clock(12)
    assert snap(store)['reserved_cpu_ns']==120
    ExecutionStore(store.store.path)


def test_funded_profile_cannot_activate_old_release(tmp_path):
    from bundle_fixture import build_bundle
    from c1_rail.qualification.execution.profile import funded_diagnostic_execution_profile
    from c1_rail.qualification.execution.protocol import sha256
    from c1_rail.qualification.execution.release_schema import parse_release
    case=build_bundle(tmp_path/'staged',capability='FULL_E1')
    doc=json.loads(case['release'])
    doc['profile']=funded_diagnostic_execution_profile(encoded(doc['profile']))
    doc['profile_sha256']=sha256(encoded(doc['profile']))
    with pytest.raises(ValueError,match='funding|persistence'):
        parse_release(encoded(doc))


def test_mixed_service_restart_notices_pending_without_auto_materialization(tmp_path):
    from types import SimpleNamespace
    from c1_rail.qualification.execution.service import ExecutionService
    store=enrolled(tmp_path); claim(store)
    service=object.__new__(ExecutionService)
    service.store=store.store
    service.profile=SimpleNamespace(values={'schema':'qualification_execution_profile/v3'})
    service.recover_service()
    assert service.recovery_issues[ATTEMPT+':funding']=='FUNDING_PENDING'
    assert json.loads(store.scheduler_status(ATTEMPT))['pending']


def test_actual_recovery_adapter_cleans_materialized_work_while_bootstrap_pending(tmp_path,monkeypatch):
    import base64
    from contextlib import nullcontext
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as sup
    store=enrolled(tmp_path)
    manifest=encoded(dict(schema='qualification_campaign_work_manifest/v1',attempt_id=ATTEMPT,work_id='admission',role='admission',probe='noop'))
    enrollment=sup.prepare_campaign_work(store,ATTEMPT,'admission',host_run_id='host1',manifest_bytes=manifest,clock_bytes=encoded(clock()))
    reservation=base64.b64decode(snap(store)['works'][0]['reservation_bytes_b64'])
    claim(store)
    cleaned=[]
    class Runtime:
        def observation(self,state,work,enrolled):
            return encoded(dict(schema='qualification_campaign_observation/v2',attempt_id=ATTEMPT,work_id='admission',
                clock=clock(12),campaign_scope_id=enrolled['scopes']['campaign_slice'],work_scope_id=enrolled['scopes']['payload_slice'],
                cpu_ns=20,memory_peak_bytes=50,oom_events=0,termination_known=True,orchestration_charge_cpu_ns=10))
        def cleanup(self,enrolled): cleaned.append(enrolled['work_id'])
    monkeypatch.setattr(sup,'controller_cpu_guard',nullcontext)
    monkeypatch.setattr(sup,'observe_campaign_clock',lambda:encoded(clock(12)))
    context=SimpleNamespace(store=store.store,campaign_runtime=Runtime(),recovery_issues={})
    sup.recover_campaign_work(context,reservation,attempt_id=ATTEMPT,work_id='admission')
    assert cleaned==['admission'] and context.recovery_issues=={}
    with store.store.transaction() as c:
        state=store._budget(c,ATTEMPT)
        assert state['recoveries'][0]['completion_bytes_b64'] is not None
    assert json.loads(store.scheduler_status(ATTEMPT))['pending']
    ExecutionStore(store.store.path)


def test_concurrent_duplicates_allocate_one_live_owner(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    store=enrolled(tmp_path); barrier=Barrier(2)
    def contender():
        local=CampaignStore(ExecutionStore(store.store.path)); barrier.wait()
        return claim(local)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(lambda _:contender(),range(2)))
    assert sum(token is not None for token,status in results)==1
    assert {json.loads(status)['reserved_cpu_ns'] for token,status in results}=={120}


def test_materialized_start_still_checks_original_expired_clock(tmp_path):
    store=enrolled(tmp_path); token,_=claim(store)
    store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    deadline=snap(store)['deadline_boottime_ns']
    with pytest.raises(ValueError,match='deadline|terminal'):
        with store.launch_gate(ATTEMPT,'worker',lambda:encoded(clock(deadline))):
            pytest.fail('expired physical dispatch')
    assert snap(store)['state']=='BUDGET_EXHAUSTED'


@pytest.mark.parametrize('void_first',[False,True])
def test_sqlite_ordered_void_race_matches_independent_funding_model(tmp_path,void_first):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier,Event
    from lifecycle_model import FundingIntentModel
    from test_campaign_budget import NOW
    store=enrolled(tmp_path); ready=Barrier(2); first_done=Event()
    model=FundingIntentModel(1_000_000_000,60,60)
    void=encoded(dict(schema='qualification_campaign_request/v1',operation='VOID',attempt_id=ATTEMPT,reason='stop',operator_approval_bytes='eA=='))
    def scheduler():
        local=CampaignStore(ExecutionStore(store.store.path)); ready.wait()
        if void_first: assert first_done.wait(20)
        result=claim(local)
        if not void_first: first_done.set()
        return result
    def cancel():
        local=CampaignStore(ExecutionStore(store.store.path)); ready.wait()
        if not void_first: assert first_done.wait(20)
        result=local.void(void,now=NOW)
        if void_first: first_done.set()
        return result
    with ThreadPoolExecutor(max_workers=2) as pool:
        scheduled=pool.submit(scheduler); cancelled=pool.submit(cancel)
        token,_=scheduled.result(timeout=30); cancelled.result(timeout=30)
    if void_first: model.void()
    assert model.claim()==(token is not None)
    if not void_first: model.void()
    assert claim(store)[0] is None and model.claim() is False
    actual=json.loads(store.scheduler_status(ATTEMPT))
    assert actual['reserved_cpu_ns']==model.reserved
    assert actual['pending']==model.pending
    assert actual['validity']==('VALID' if model.valid else 'VOID')
    if token:
        assert model.materialize()
        store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert snap(reopened)['reserved_cpu_ns']==model.reserved
    assert not model.can_publish


def test_negative_write_cannot_recreate_deleted_funding_authority(tmp_path):
    store=enrolled(tmp_path)
    with store.store.transaction() as c:
        before=c.execute('SELECT snapshot_bytes FROM full_campaign_budgets').fetchone()[0]
        c.execute('DELETE FROM full_campaign_funding_works'); c.execute('DELETE FROM full_campaign_funding')
    with pytest.raises(ValueError,match='funding'):
        store.recover_work(ATTEMPT,'admission',encoded(clock(12)))
    with store.store.transaction() as c:
        assert c.execute('SELECT snapshot_bytes FROM full_campaign_budgets').fetchone()[0]==before
        assert c.execute('SELECT count(*) FROM full_campaign_funding').fetchone()[0]==0


def test_terminal_overlay_does_not_erase_newer_negative_clock(tmp_path):
    store=enrolled(tmp_path)
    deadline=snap(store)['deadline_boottime_ns']
    claim(store,t=deadline)
    store.recover_work(ATTEMPT,'admission',encoded(clock(deadline+1)))
    with store.store.transaction() as c:
        doc=store._funding(c,ATTEMPT)
        assert doc['last_clock']==clock(deadline+1)
        assert doc['terminal_overlay'] is not None
    with pytest.raises(ValueError,match='funding'): store.budget_snapshot(ATTEMPT)
    ExecutionStore(store.store.path)


def test_materialization_never_reconstructs_unrelated_attempt(tmp_path,monkeypatch):
    store=enrolled(tmp_path)
    other=json.loads(request()); other['attempt_id']='other'
    store.begin_admission(encoded(other),encoded(profile()),encoded(clock()))
    token,_=claim(store)
    original=store._budget
    def own_only(connection,attempt):
        assert attempt==ATTEMPT, 'unrelated campaign charged to this owner'
        return original(connection,attempt)
    monkeypatch.setattr(store,'_budget',own_only)
    store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')


def test_v7_upgrade_preserves_existing_history_and_rejects_downgrade(tmp_path):
    from test_campaign_supervision import metered
    store=metered(tmp_path); historical=store.budget_snapshot(ATTEMPT)
    config=profile(); config.update(schema='qualification_campaign_budget_profile/v3',funding_intents='qualification_campaign_funding/v1',orchestration_cpu_ns={p:10 for p in config['phases']})
    fresh=json.loads(request()); fresh['attempt_id']='fresh'
    store.begin_admission(encoded(fresh),encoded(config),encoded(clock()))
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert reopened.budget_snapshot(ATTEMPT)==historical
    with pytest.raises(ValueError,match='fresh'): claim(reopened)
    with store.store.transaction() as c: c.execute('PRAGMA user_version=6')
    with pytest.raises(ValueError,match='layout'): ExecutionStore(store.store.path)


@pytest.mark.parametrize('table,identity_field',[('full_campaign_funding','attempt_id'),('full_campaign_bootstraps','work_id')])
def test_compact_row_identity_mismatch_refuses_before_history(tmp_path,table,identity_field):
    store=enrolled(tmp_path); claim(store)
    with store.store.transaction() as c:
        doc=json.loads(c.execute('SELECT body FROM '+table).fetchone()[0]); doc[identity_field]='different'
        c.execute('UPDATE '+table+' SET body=?',(encoded(doc),))
    with pytest.raises(ValueError,match='funding'): claim(store)


def test_claim_cannot_point_to_a_valid_but_ineligible_historical_head(tmp_path):
    store=enrolled(tmp_path); claim(store)
    with store.store.transaction() as c:
        first=c.execute('SELECT sha256 FROM full_campaign_budget_events ORDER BY sequence LIMIT 1').fetchone()[0]
        doc=json.loads(c.execute('SELECT body FROM full_campaign_bootstraps').fetchone()[0])
        doc.update(claimed_event_head=first,claimed_authority_head=first)
        c.execute('UPDATE full_campaign_bootstraps SET body=?',(encoded(doc),))
    with pytest.raises(ValueError,match='funding'): ExecutionStore(store.store.path)


def test_compact_fixed_signing_retry_preserves_parent_authority_and_own_charge(tmp_path):
    from test_campaign_budget import transition,observation
    from test_campaign_recovery import capture
    from c1_rail.qualification.execution.protocol import sha256
    store=enrolled(tmp_path)
    raw=schedule(work_id='seal',role='probe_seal')
    token,_=claim(store,raw)
    _,enrollment=store.materialize_scheduler_bootstrap(ATTEMPT,'seal',token,'host1')
    capture(store,'seal',12)
    transition(store,'seal','SIGNING_INTENT',13,dict(intent_id='fixed',payload_bytes_b64='eA==',key_id='key',signing_at_utc='2026-09-19T00:00:00Z'))
    scope=json.loads(enrollment)['scopes']
    observed=json.loads(observation('seal',cpu=20,t=14))
    observed.update(schema='qualification_campaign_observation/v2',orchestration_charge_cpu_ns=10,termination_known=True,
        campaign_scope_id=scope['campaign_slice'],work_scope_id=scope['payload_slice'])
    store.settle_work(ATTEMPT,'seal',encoded(observed))
    before=snap(store)
    retry=schedule(work_id='retry',role='probe_seal',signing_retry_of='seal')
    retry_token,_=claim(store,retry,t=15)
    reservation,_=store.materialize_scheduler_bootstrap(ATTEMPT,'retry',retry_token,'host1')
    after=snap(store)
    assert json.loads(reservation)['input_sha256']==sha256(b'x')
    assert after['authority_head']==before['authority_head']
    assert after['reserved_cpu_ns']==before['reserved_cpu_ns']+60
    assert claim(store,retry,t=16)[0] is None
    with pytest.raises(ValueError,match='signing parent'):
        claim(store,schedule(work_id='another',role='probe_seal',signing_retry_of='seal'),t=16)
    ExecutionStore(store.store.path)


@pytest.mark.parametrize('damage',['missing_work','stale_work','stale_campaign','orphan_pending','missing_intent'])
def test_negative_write_never_repairs_compact_predecessor(tmp_path,damage):
    store=enrolled(tmp_path)
    if damage in ('orphan_pending','missing_intent'): claim(store)
    with store.store.transaction() as c:
        before=bytes(c.execute('SELECT snapshot_bytes FROM full_campaign_budgets').fetchone()[0])
        if damage=='missing_work': c.execute('DELETE FROM full_campaign_funding_works')
        elif damage=='missing_intent': c.execute('DELETE FROM full_campaign_bootstraps')
        elif damage=='orphan_pending':
            doc=store._funding(c,ATTEMPT); doc['bootstrap_pending_work_id']=None
            c.execute('UPDATE full_campaign_funding SET body=?',(encoded(doc),))
        else:
            table='full_campaign_funding_works' if damage=='stale_work' else 'full_campaign_funding'
            doc=json.loads(c.execute('SELECT body FROM '+table).fetchone()[0])
            if damage=='stale_work': doc['settled']=True
            else: doc['remaining_cpu_ns']-=1
            c.execute('UPDATE '+table+' SET body=?',(encoded(doc),))
        damaged=[tuple(row) for row in c.execute('SELECT body FROM full_campaign_funding')]
    with pytest.raises(ValueError,match='funding'):
        store.recover_work(ATTEMPT,'admission',encoded(clock(12)))
    with store.store.transaction() as c:
        assert bytes(c.execute('SELECT snapshot_bytes FROM full_campaign_budgets').fetchone()[0])==before
        assert [tuple(row) for row in c.execute('SELECT body FROM full_campaign_funding')]==damaged


def test_funded_profile_cannot_survive_removed_v7_enrollment(tmp_path):
    store=enrolled(tmp_path)
    with store.store.transaction() as c:
        for table in ('full_campaign_bootstraps','full_campaign_funding_works','full_campaign_funding'):
            c.execute('DROP TABLE '+table)
        c.execute('PRAGMA user_version=6')
    with pytest.raises(ValueError,match='funding'):
        store.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError,match='funding'):
        store.recover_work(ATTEMPT,'admission',encoded(clock(12)))
    with pytest.raises(ValueError,match='funding'):
        ExecutionStore(store.store.path)


def test_materialized_intent_loss_rejects_reopen_and_negative_write(tmp_path):
    store=enrolled(tmp_path); token,_=claim(store)
    store.materialize_scheduler_bootstrap(ATTEMPT,'worker',token,'host1')
    assert claim(store)[0] is None
    with store.store.transaction() as c:
        c.execute('DELETE FROM full_campaign_bootstraps')
    with pytest.raises(ValueError,match='funding'):
        ExecutionStore(store.store.path)
    with pytest.raises(ValueError,match='funding'):
        store.recover_work(ATTEMPT,'admission',encoded(clock(12)))
