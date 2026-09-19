"""S2 accounting development tests; OS counters here are simulated."""
from pathlib import Path
import base64
import json

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.store import ExecutionStore
from c1_rail.qualification.journal_snapshot import parse_campaign_budget_snapshot
from test_campaign_budget import (ATTEMPT, clock, profile, request, contract_budget,
    snap, start, observation)


@pytest.fixture(autouse=True)
def simulated_control_timer(monkeypatch):
    # These are Windows-capable persistence tests, never kernel-limit evidence.
    from contextlib import nullcontext
    from c1_rail.qualification.execution import campaign_supervisor
    monkeypatch.setattr(campaign_supervisor, 'controller_cpu_guard', nullcontext)


def metered(tmp_path, *, started=True):
    config = profile()
    config['schema'] = 'qualification_campaign_budget_profile/v2'
    config['orchestration_cpu_ns'] = {name: 10 for name in config['phases']}
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    store.begin_admission(request(), encoded(config), encoded(clock()))
    store.bind_budget(ATTEMPT, contract_budget(), expected_revision=snap(store)['authority_revision'])
    if started:
        start(store)
    return store


def measured(cpu=20, t=11, charge=10):
    doc = json.loads(observation(cpu=cpu, t=t))
    doc.update(schema='qualification_campaign_observation/v2', orchestration_charge_cpu_ns=charge, termination_known=True)
    return encoded(doc)


def test_settlement_reserves_full_phase_and_charges_measured_plus_installed_controller_bound(tmp_path):
    store = metered(tmp_path)
    assert snap(store)['reserved_cpu_ns'] == 60
    raw = measured()
    first = store.settle_work(ATTEMPT, 'admission', raw)
    result = json.loads(first)
    assert result['schema'] == 'qualification_campaign_budget_snapshot/v3'
    assert result['settled_cpu_ns'] == 30
    assert result['remaining_cpu_ns'] == 999_999_970
    assert store.settle_work(ATTEMPT, 'admission', raw) == first
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT) == first
    saved = json.loads(base64.b64decode(result['works'][0]['observation_bytes_b64']))
    assert saved['cpu_ns'] == 20
    assert saved['orchestration_charge_cpu_ns'] == 10


@pytest.mark.parametrize('charge', [0, 9, 11, True])
def test_caller_cannot_discount_or_replace_installed_orchestration_charge(tmp_path, charge):
    store = metered(tmp_path)
    before = store.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError):
        store.settle_work(ATTEMPT, 'admission', measured(charge=charge))
    assert store.budget_snapshot(ATTEMPT) == before


def test_unknown_work_counter_spends_full_reservation_and_bars_authority(tmp_path):
    store = metered(tmp_path)
    store.settle_work(ATTEMPT, 'admission', measured(cpu=None))
    result = snap(store)
    assert result['settled_cpu_ns'] == 60
    assert result['state'] == 'BUDGET_UNCERTAIN'


def test_measured_and_controller_sum_cannot_overrun_phase(tmp_path):
    store = metered(tmp_path)
    store.settle_work(ATTEMPT, 'admission', measured(cpu=51))
    assert snap(store)['settled_cpu_ns'] == 61
    assert snap(store)['state'] == 'BUDGET_EXHAUSTED'


def test_settled_recovery_compares_raw_counter_and_preserves_charge(tmp_path):
    from test_campaign_recovery import capture
    store = metered(tmp_path)
    capture(store, t=11)
    store.settle_work(ATTEMPT, 'admission', measured(t=12))
    before = snap(store)['works'][0]['observation_bytes_b64']
    store.recover_work(ATTEMPT, 'admission', measured(t=13))
    assert snap(store)['state'] == 'BOUND'
    assert snap(store)['settled_cpu_ns'] == 30
    assert snap(store)['works'][0]['observation_bytes_b64'] == before
    store.recover_work(ATTEMPT, 'admission', measured(cpu=21, t=14))
    assert snap(store)['state'] == 'BUDGET_UNCERTAIN'
    assert snap(store)['settled_cpu_ns'] == 30


def test_version_labels_cannot_reinterpret_new_charge_as_old_counter(tmp_path):
    store = metered(tmp_path)
    store.settle_work(ATTEMPT, 'admission', measured())
    result = snap(store)
    for old in ('qualification_campaign_budget_snapshot/v1', 'qualification_campaign_budget_snapshot/v2'):
        result['schema'] = old
        with pytest.raises(ValueError):
            parse_campaign_budget_snapshot(encoded(result))


def test_new_profile_rejects_missing_or_out_of_phase_orchestration_bounds(tmp_path):
    from c1_rail.qualification.execution.profile import parse_campaign_budget_profile
    config = profile()
    config.update(schema='qualification_campaign_budget_profile/v2',
                  orchestration_cpu_ns={phase: 10 for phase in config['phases']})
    for changed in (dict(config, orchestration_cpu_ns={}),
                    dict(config, orchestration_cpu_ns=dict(config['orchestration_cpu_ns'], ADMISSION=61))):
        with pytest.raises(ValueError):
            parse_campaign_budget_profile(encoded(changed))
    config['schema'] = 'qualification_campaign_budget_profile/v1'
    with pytest.raises(ValueError):
        parse_campaign_budget_profile(encoded(config))


def test_old_observation_cannot_bypass_new_profile_charge(tmp_path):
    store = metered(tmp_path)
    with pytest.raises(ValueError):
        store.settle_work(ATTEMPT, 'admission', observation())
    assert snap(store)['reserved_cpu_ns'] == 60


def test_old_profile_cannot_accept_new_observation_fields(tmp_path):
    from test_campaign_budget import opened
    store = opened(tmp_path)
    start(store)
    with pytest.raises(ValueError):
        store.settle_work(ATTEMPT, 'admission', measured())


@pytest.mark.parametrize('with_recovery_barrier',[False,True])
def test_linked_retry_charges_its_own_bound_without_changing_fixed_intent(tmp_path,with_recovery_barrier):
    from test_campaign_budget import transition
    from test_campaign_recovery import capture
    from c1_rail.qualification.execution.protocol import sha256
    store = metered(tmp_path)
    store.settle_work(ATTEMPT, 'admission', measured())
    transition(store, 'admission', 'COMPLETED', 12)
    def reserve(work, t, parent=None):
        raw = dict(limits=profile()['phases']['SEAL'], clock=clock(t), input_sha256=sha256(b'x'))
        if parent is not None:
            raw['signing_retry_of'] = parent
        return store.reserve_work(ATTEMPT, work, 'SEAL', encoded(raw),
            expected_revision=snap(store)['authority_revision'])
    def observed(work, t):
        doc = json.loads(observation(work, cpu=20, t=t))
        doc.update(schema='qualification_campaign_observation/v2', orchestration_charge_cpu_ns=10, termination_known=True)
        return encoded(doc)
    reserve('seal', 13)
    start(store, 'seal', 14)
    capture(store, 'seal', 15)
    transition(store, 'seal', 'SIGNING_INTENT', 16, dict(intent_id='fixed',
        payload_bytes_b64='eA==', key_id='key', signing_at_utc='2026-09-19T00:00:00Z'))
    store.recover_work(ATTEMPT, 'seal', observed('seal', 17))
    token = snap(store)['authority_head']
    if with_recovery_barrier:
        store.claim_supervision_control(ATTEMPT,'seal','RECOVERY_OWNER',encoded(clock(18)),recovery_owner_token=RECOVERY_TOKEN)
        store.recover_work(ATTEMPT,'seal',observed('seal',19),recovery_owner_token=RECOVERY_TOKEN)
        store.complete_recovery(ATTEMPT,'seal',recovery_completion(store,t=20,work_id='seal'),recovery_owner_token=RECOVERY_TOKEN)
    reserve('retry', 21, 'seal')
    start(store, 'retry', 22)
    store.settle_work(ATTEMPT, 'retry', observed('retry', 23))
    transition(store, 'retry', 'COMPLETED', 24)
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['settled_cpu_ns'] == 90
    assert result['authority_head'] == token
    assert result['schema'] == 'qualification_campaign_budget_snapshot/' + ('v4' if with_recovery_barrier else 'v3')
    intent = next(w for w in result['works'] if w['work_id'] == 'seal')
    assert intent['state'] == 'SIGNING_INTENT'


def test_supervisor_manifest_is_fixed_role_and_rejects_client_command_or_counters():
    from c1_rail.qualification.execution.campaign_supervisor import parse_work_manifest
    raw = dict(schema='qualification_campaign_work_manifest/v1', attempt_id=ATTEMPT,
               work_id='probe', role='probe_g5', probe='noop')
    assert parse_work_manifest(encoded(raw))['role'] == 'probe_g5'
    for change in ({'command': 'anything'}, {'cpu_ns': 0}, {'role': '/bin/sh'}, {'probe': 'custom-code'}):
        with pytest.raises(ValueError):
            parse_work_manifest(encoded(dict(raw, **change)))


def test_trusted_cgroup_counter_parser_aggregates_kernel_values_and_rejects_loss():
    from c1_rail.qualification.execution.campaign_supervisor import parse_cgroup_counters
    observed = parse_cgroup_counters(b'usage_usec 120\nuser_usec 90\nsystem_usec 30\n',
        b'2048\n', b'low 0\nhigh 0\nmax 2\noom 1\noom_kill 1\noom_group_kill 1\n')
    assert observed == {'cpu_ns': 120000, 'memory_peak_bytes': 2048, 'oom_events': 1}
    for raw in (b'', b'usage_usec -1\n', b'usage_usec 1\nusage_usec 2\n'):
        with pytest.raises(ValueError):
            parse_cgroup_counters(raw, b'2048', b'oom 0\noom_kill 0\n')


def test_unit_binding_requires_manager_owned_guardian_and_same_campaign_memory_parent():
    from c1_rail.qualification.execution.campaign_supervisor import work_enrollment
    first = work_enrollment('host1', ATTEMPT, 'admission')
    second = work_enrollment('host1', ATTEMPT, 'probe')
    other = work_enrollment('host1', 'other-attempt', 'admission')
    assert first['campaign_slice'] == second['campaign_slice']
    assert first['work_slice'] != second['work_slice']
    assert first['campaign_slice'] != other['campaign_slice']
    assert first['guardian_unit'].endswith('.service')
    assert first['payload_slice'].startswith(first['work_slice'].removesuffix('.slice') + '-')
    with pytest.raises(ValueError):
        work_enrollment('host1', '../../escape', 'admission')


def test_diagnostic_release_binds_phase_profile_without_activating_statistics(tmp_path):
    from bundle_fixture import build_bundle
    from c1_rail.qualification.execution.release_schema import parse_release
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', diagnostic=True)
    release = parse_release(case['release'])
    assert release['schema'] == 'qualification_execution_release/v3'
    assert release['dispatch_enabled'] is False
    assert release['profile']['supported_checkpoints'] == []
    assert release['campaign_budget_profile']['installed_profile_sha256'] == release['profile_sha256']
    changed = dict(release['campaign_budget_profile'], installed_profile_sha256='f' * 64)
    with pytest.raises(ValueError):
        parse_release(encoded(dict(release, campaign_budget_profile=changed)))


def admission_case(tmp_path, *, with_case=False):
    from bundle_fixture import build_bundle
    from c1_rail.qualification.execution.admission import verify_bundle
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
    from test_contract import NOW
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', diagnostic=True)
    context = verify_bundle(case['root'], case['release'], case['keys'], NOW)
    plan = derive_campaign_plan_from_context(context)
    raw = encoded(dict(schema='qualification_campaign_request/v2', operation='SUBMIT_E1',
        attempt_id=case['attempt_id'], request_id='diagnostic', bundle_sha256=context.bundle_sha256))
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    budget_profile = json.loads(case['release'])['campaign_budget_profile']
    state = json.loads(store.begin_admission(raw, encoded(budget_profile), encoded(clock())))
    state = json.loads(store.record_work_transition(context.attempt_id, 'admission', encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=context.attempt_id,
        work_id='admission', state='START_INTENT', clock=clock(),
        data=dict(campaign_scope_id='parent-1', work_scope_id='scope-admission'))),
        expected_revision=state['authority_revision']))
    observed = json.loads(measured())
    observed.update(attempt_id=context.attempt_id, cpu_ns=0,
        orchestration_charge_cpu_ns=20_000_000_000)
    result=(store, raw, context, plan, encoded(observed), NOW)
    return (*result, case) if with_case else result


def test_metered_admission_receipt_custody_and_charge_are_atomic_and_retry_exact(tmp_path):
    store, raw, context, plan, counters, now = admission_case(tmp_path)
    result = store.finish_diagnostic_admission(raw, context, plan, counters, now=now)
    assert result['receipt']['state'] == 'ADMITTED_DIAGNOSTIC'
    assert result['receipt']['dispatch_enabled'] is False
    assert result['settled_cpu_ns'] == 20_000_000_000
    assert store.finish_diagnostic_admission(raw, context, plan, counters, now=now)['receipt'] == result['receipt']
    reopened = CampaignStore(ExecutionStore(store.store.path))
    assert reopened.diagnostic_status(context.attempt_id)['receipt'] == result['receipt']
    assert reopened.objects(context.attempt_id)['plan'] == plan
    assert json.loads(reopened.budget_snapshot(context.attempt_id))['start_clock'] == clock()


def test_admission_overrun_commits_refusal_and_never_creates_receipt(tmp_path):
    store, raw, context, plan, counters, now = admission_case(tmp_path)
    changed = json.loads(counters)
    changed['cpu_ns'] = 120_000_000_000
    result = store.finish_diagnostic_admission(raw, context, plan, encoded(changed), now=now)
    assert result['state'] == 'BUDGET_EXHAUSTED'
    assert result['receipt'] is None
    reopened = CampaignStore(ExecutionStore(store.store.path))
    assert reopened.diagnostic_status(context.attempt_id)['state'] == 'BUDGET_EXHAUSTED'
    assert reopened.objects(context.attempt_id) == {}


def test_preparation_commits_owned_scope_before_launch_and_cannot_relaunch(tmp_path):
    from c1_rail.qualification.execution.campaign_supervisor import prepare_campaign_work
    store = metered(tmp_path, started=False)
    manifest = encoded(dict(schema='qualification_campaign_work_manifest/v1', attempt_id=ATTEMPT,
        work_id='admission', role='admission', probe='noop'))
    enrollment = prepare_campaign_work(store, ATTEMPT, 'admission', host_run_id='host1',
        manifest_bytes=manifest, clock_bytes=encoded(clock(13)))
    reopened = CampaignStore(ExecutionStore(store.store.path))
    work = next(w for w in snap(reopened)['works'] if w['work_id'] == 'admission')
    assert work['state'] == 'START_INTENT'
    assert reopened.objects(ATTEMPT)['supervision_admission'] == encoded(enrollment)
    with pytest.raises(ValueError):
        prepare_campaign_work(store, ATTEMPT, 'admission', host_run_id='host1',
            manifest_bytes=manifest, clock_bytes=encoded(clock(14)))


def test_guardian_unit_spec_binds_payload_lifetime_and_limits_controller_process():
    from c1_rail.qualification.execution.campaign_supervisor import guardian_unit_spec, work_enrollment
    enrollment = work_enrollment('host1', ATTEMPT, 'probe')
    spec = guardian_unit_spec(enrollment, attempt_id=ATTEMPT, work_id='probe',
        code_root='/opt/qualification', interpreter='/opt/ops/bin/python', uid=61001,
        orchestration_cpu_ns=20_000_000_000, remaining_wall_ns=20_000_000_000)
    service = spec['guardian']
    assert service['Slice'] == enrollment['work_slice']
    assert service['KillMode'] == 'control-group'
    assert service['Restart'] == 'no'
    assert service['TasksMax'] == 1
    assert service['LimitCPU'] == 13
    assert spec['payload']['BindsTo'] == [enrollment['guardian_unit']]
    assert spec['payload']['After'] == [enrollment['guardian_unit']]
    assert service['ExecStart'][0] == '/opt/ops/bin/python'
    with pytest.raises(ValueError):
        guardian_unit_spec(enrollment, attempt_id=ATTEMPT, work_id='probe',
            code_root='/opt/qualification', interpreter='/opt/ops/bin/python', uid=0,
            orchestration_cpu_ns=20_000_000_000, remaining_wall_ns=20_000_000_000)


def test_recovery_commits_uncertainty_before_cleanup_failure(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    store = metered(tmp_path, started=False)
    manifest = encoded(dict(schema='qualification_campaign_work_manifest/v1', attempt_id=ATTEMPT,
        work_id='admission', role='admission', probe='noop'))
    enrollment = supervisor.prepare_campaign_work(store, ATTEMPT, 'admission', host_run_id='host1',
        manifest_bytes=manifest, clock_bytes=encoded(clock(13)))
    class InterruptedRuntime:
        def observation(self, state, work, enrollment):
            return encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=ATTEMPT,
                work_id='admission', clock=clock(14), cpu_ns=None,
                campaign_scope_id=enrollment['scopes']['campaign_slice'],
                work_scope_id=enrollment['scopes']['payload_slice'], memory_peak_bytes=50,
                oom_events=0, orchestration_charge_cpu_ns=10, termination_known=False))
        def cleanup(self, enrollment):
            durable = snap(CampaignStore(ExecutionStore(store.store.path)))
            assert durable['state'] == 'BUDGET_UNCERTAIN'
            assert durable['settled_cpu_ns'] == 60
            assert durable['works'][0]['state'] == 'IN_DOUBT'
            raise OSError('simulated owned cleanup failure')
    context = SimpleNamespace(store=store.store, campaign_runtime=InterruptedRuntime(), recovery_issues={})
    reservation = base64.b64decode(snap(store)['works'][0]['reservation_bytes_b64'])
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(14)))
    result = json.loads(supervisor.recover_campaign_work(context, reservation, attempt_id=ATTEMPT, work_id='admission'))
    assert result['state'] == 'BUDGET_UNCERTAIN'
    assert context.recovery_issues[ATTEMPT + ':admission'] == 'CLEANUP_PENDING'
    reopened = CampaignStore(ExecutionStore(store.store.path))
    assert snap(reopened)['settled_cpu_ns'] == 60


def test_service_persists_intent_before_delegating_admission_and_never_resamples_retry(tmp_path, monkeypatch):
    from test_campaign_admission import running, message
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    instance, case = running(tmp_path, monkeypatch, diagnostic=True)
    instance.config = {'host_run_id': 'host1'}
    from contextlib import nullcontext
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    request_doc = json.loads(message(case))
    request_doc['schema'] = 'qualification_campaign_request/v2'
    request_bytes = encoded(request_doc)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock()))
    def forbidden(*args, **kwargs):
        raise AssertionError('unmetered verification or repeated execution')
    monkeypatch.setattr(instance, '_context', forbidden)
    def queued(context, reservation_bytes, manifest_bytes):
        campaigns = CampaignStore(context.store)
        state = json.loads(campaigns.budget_snapshot(case['attempt_id']))
        assert state['state'] == 'PROVISIONAL'
        assert state['start_clock'] == clock()
        assert campaigns.row(case['attempt_id'])['request_bytes'] == request_bytes
        assert json.loads(manifest_bytes)['role'] == 'admission'
        return encoded(campaigns.diagnostic_status(case['attempt_id']))
    monkeypatch.setattr(supervisor, 'run_campaign_work', queued)
    first = json.loads(instance.handle_request(1001, request_bytes))
    assert first['state'] == 'PROVISIONAL' and first['receipt'] is None
    monkeypatch.setattr(supervisor, 'run_campaign_work', forbidden)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', forbidden)
    assert json.loads(instance.handle_request(1001, request_bytes)) == first
    with pytest.raises(ValueError):
        instance.handle_request(1001, message(case))

def test_resource_boundary_is_closed_installed_configuration():
    from c1_rail.qualification.execution.profile import CAMPAIGN_RESOURCE_SCOPE
    assert CAMPAIGN_RESOURCE_SCOPE['schema'] == 'qualification_campaign_resource_scope/v1'
    assert CAMPAIGN_RESOURCE_SCOPE['platform'] == 'shared_daemons_outside_scope_excluded'
    assert CAMPAIGN_RESOURCE_SCOPE['memory'] == 'shared_host_parent_conservative'
    assert CAMPAIGN_RESOURCE_SCOPE['control_calls'] == 3


def test_manager_message_has_only_fixed_guardian_and_owned_auxiliaries():
    from c1_rail.qualification.execution.campaign_supervisor import manager_start_arguments, work_enrollment, guardian_unit_spec
    scopes = work_enrollment('host1', ATTEMPT, 'probe')
    spec = guardian_unit_spec(scopes, attempt_id=ATTEMPT, work_id='probe',
        code_root='/opt/qualification', interpreter='/opt/ops/bin/python', uid=61001,
        orchestration_cpu_ns=20_000_000_000, remaining_wall_ns=20_000_000_000)
    args = manager_start_arguments(scopes, spec)
    assert args[:2] == [scopes['guardian_unit'], 'fail']
    assert '/opt/qualification/bootstrap.py' in args
    assert args.count(scopes['payload_slice']) >= 2
    assert 'Delegate' not in args
    assert spec['guardian']['LimitCPU'] == 13

def test_launch_setup_failure_durably_spends_reservation_before_return(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    store = metered(tmp_path, started=False)
    context = SimpleNamespace(store=store.store, config={'host_run_id': 'host1'}, recovery_issues={})
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(14)))
    class MissingHost:
        def __init__(self, context):
            raise OSError('installed common memory parent unavailable')
    monkeypatch.setattr(supervisor, 'LinuxCampaignRuntime', MissingHost)
    manifest = encoded(dict(schema='qualification_campaign_work_manifest/v1', attempt_id=ATTEMPT,
        work_id='admission', role='admission', probe='noop'))
    reservation = base64.b64decode(snap(store)['works'][0]['reservation_bytes_b64'])
    with pytest.raises(OSError):
        supervisor.run_campaign_work(context, reservation, manifest)
    result = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['state'] == 'BUDGET_UNCERTAIN'
    assert result['works'][0]['state'] == 'IN_DOUBT'
    assert result['settled_cpu_ns'] == 60
    assert context.recovery_issues[ATTEMPT + ':admission'] == 'CLEANUP_PENDING'

@pytest.mark.parametrize('void_first', [False, True])
def test_new_charge_matches_independent_model_across_void_and_reopen(tmp_path, void_first):
    from lifecycle_model import CampaignBudgetModel
    from test_campaign_recovery import void_request, NOW
    model=CampaignBudgetModel(1_000_000_000,60,overhead=10)
    store=metered(tmp_path)
    model.apply('intent')
    if void_first:
        store.void(void_request(),now=NOW); model.apply('void')
    store.recover_work(ATTEMPT,'admission',measured())
    model.apply('recover',charge=20)
    if not void_first:
        store.void(void_request(),now=NOW); model.apply('void')
    actual=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert actual['settled_cpu_ns']==model.charge==30
    assert actual['remaining_cpu_ns']==model.remaining
    assert actual['validity']==model.validity=='VOID'
    assert actual['works'][0]['state']==model.state=='IN_DOUBT'

def test_diagnostic_admission_cannot_substitute_frozen_budget(tmp_path):
    store, raw, context, plan, counters, now=admission_case(tmp_path)
    changed=json.loads(plan)
    changed['budget']['maximum_cpu_seconds']+=1
    before=store.budget_snapshot(context.attempt_id)
    with pytest.raises(ValueError):
        store.finish_diagnostic_admission(raw,context,encoded(changed),counters,now=now)
    assert store.budget_snapshot(context.attempt_id)==before


def test_empty_diagnostic_history_is_unknown_without_creating_tables(tmp_path):
    store=CampaignStore(ExecutionStore(tmp_path/'journal.sqlite'))
    with pytest.raises(KeyError):
        store.diagnostic_status('missing')


def test_pending_void_authenticates_under_admission_and_commits_charge_without_receipt(tmp_path):
    from composition_fixture import signed_approval
    from c1_rail.qualification.execution.protocol import sha256
    store,raw,context,plan,counters,now,case=admission_case(tmp_path,with_case=True)
    subject=encoded(dict(attempt_id=context.attempt_id,reason='stop',contract_sha256=context.contract.contract_sha256))
    approval=signed_approval(subject,case['private']['test-freeze'],key_id='test-freeze',
        scope='VOID_QUALIFICATION_ATTEMPT',contract_sha256=context.contract.contract_sha256)
    cancel=encoded(dict(schema='qualification_campaign_request/v2',operation='VOID',
        attempt_id=context.attempt_id,reason='stop',operator_approval_bytes=base64.b64encode(approval).decode()))
    pending=store.queue_diagnostic_void(cancel)
    assert json.loads(pending)['validity']=='VALID'
    assert store.queue_diagnostic_void(cancel)==pending
    result=store.finish_diagnostic_admission(raw,context,plan,counters,now=now,trusted_keys=case['keys'])
    assert result['validity']=='VOID' and result['receipt'] is None
    assert result['settled_cpu_ns']==20_000_000_000
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert reopened.void_retry(cancel) is not None
    assert reopened.diagnostic_status(context.attempt_id)['receipt'] is None

def test_control_slot_is_durable_and_cannot_restart_with_a_fresh_runtime(tmp_path):
    store=metered(tmp_path)
    raw=store.claim_supervision_control(ATTEMPT,'admission','START_CLIENT',encoded(clock(12)))
    assert json.loads(raw)['data']=={'slot':'START_CLIENT'}
    reopened=CampaignStore(ExecutionStore(store.store.path))
    with pytest.raises(ValueError):
        reopened.claim_supervision_control(ATTEMPT,'admission','START_CLIENT',encoded(clock(13)))
    with pytest.raises(ValueError):
        reopened.claim_supervision_control(ATTEMPT,'admission','EXTRA_CLIENT',encoded(clock(13)))

def test_postsettlement_unknown_termination_invalidates_authority_without_recharging(tmp_path):
    store=metered(tmp_path)
    store.settle_work(ATTEMPT,'admission',measured())
    raw=json.loads(measured(t=12)); raw['termination_known']=False
    result=json.loads(store.recover_work(ATTEMPT,'admission',encoded(raw)))
    assert result['settled_cpu_ns']==30
    assert result['state']=='BUDGET_UNCERTAIN'

def test_binding_fresh_authenticated_clock_refuses_before_planning(tmp_path):
    config=profile(); config['schema']='qualification_campaign_budget_profile/v2'
    config['orchestration_cpu_ns']={phase:10 for phase in config['phases']}
    store=CampaignStore(ExecutionStore(tmp_path/'journal.sqlite'))
    store.begin_admission(request(),encoded(config),encoded(clock()))
    start(store)
    state=snap(store)
    late=encoded(clock(20_000_000_000))
    result=json.loads(store.bind_budget(ATTEMPT,contract_budget(),expected_revision=state['authority_revision'],clock_bytes=late))
    assert result['state']=='BUDGET_EXHAUSTED'
    assert result['last_clock']==json.loads(late)
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT)==encoded(result)


@pytest.mark.parametrize('settled', [False, True])
@pytest.mark.parametrize('void_first', [False, True])
def test_unknown_termination_is_sticky_across_duplicate_recovery_void_and_true(tmp_path, settled, void_first):
    from test_campaign_recovery import capture, void_request, NOW
    store=metered(tmp_path)
    capture(store,t=11)
    if settled:
        store.settle_work(ATTEMPT,'admission',measured(t=12))
    if void_first:
        store.void(void_request(),now=NOW)
    raw=json.loads(measured(t=13)); raw['termination_known']=False
    first=store.recover_work(ATTEMPT,'admission',encoded(raw))
    assert store.recover_work(ATTEMPT,'admission',encoded(raw))==first
    store.recover_work(ATTEMPT,'admission',measured(t=14))
    if not void_first:
        store.void(void_request(),now=NOW)
    state=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert state['state']=='BUDGET_UNCERTAIN'
    assert state['validity']=='VOID'
    assert state['settled_cpu_ns']==30


@pytest.mark.parametrize('value', [0,1,None,'true'])
def test_termination_known_requires_strict_boolean(tmp_path,value):
    store=metered(tmp_path)
    raw=json.loads(measured()); raw['termination_known']=value
    with pytest.raises(ValueError):
        store.settle_work(ATTEMPT,'admission',encoded(raw))
    assert snap(store)['settled_cpu_ns']==0


def test_spent_recovery_slot_refuses_before_any_counter_or_cleanup(tmp_path,monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    store=metered(tmp_path)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    class ForbiddenRuntime:
        def observation(self,*args): raise AssertionError('spent slot inspected counters')
        def cleanup(self,*args): raise AssertionError('spent slot attempted cleanup')
    context=SimpleNamespace(store=store.store,campaign_runtime=ForbiddenRuntime(),recovery_issues={})
    monkeypatch.setattr(supervisor,'observe_campaign_clock',lambda:encoded(clock(13)))
    raw=base64.b64decode(snap(store)['works'][0]['reservation_bytes_b64'])
    with pytest.raises(ValueError,match='control slot already spent'):
        supervisor.recover_campaign_work(context,raw,attempt_id=ATTEMPT,work_id='admission')


def test_interrupted_recovery_claim_blocks_new_reservation_after_reopen(tmp_path):
    # Regression for the frozen packet's demonstrated positive-authority window.
    from test_campaign_recovery import capture
    from c1_rail.qualification.execution.protocol import sha256
    store=metered(tmp_path)
    capture(store,t=11)
    store.settle_work(ATTEMPT,'admission',measured(t=12))
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(13)))
    reopened=CampaignStore(ExecutionStore(store.store.path))
    before=snap(reopened)
    reservation=encoded(dict(limits=profile()['phases']['N1'],clock=clock(14),input_sha256=sha256(b'probe')))
    with pytest.raises(ValueError,match='recovery pending'):
        reopened.reserve_work(ATTEMPT,'after-crash','N1',reservation,expected_revision=before['authority_revision'])
    assert snap(reopened)['settled_cpu_ns']==30
    assert len(snap(reopened)['works'])==1


RECOVERY_TOKEN=b'R'*32


def recovery_completion(store, t=15, work_id='admission'):
    from c1_rail.qualification.execution.protocol import sha256
    state=snap(store)
    recovery=next(r for r in state['recoveries'] if r['work_id']==work_id)
    cleanup=encoded(dict(schema='qualification_campaign_supervision_event/v1',attempt_id=ATTEMPT,
        work_id=work_id,kind='CLEANUP',clock=clock(t),data={'status':'ABSENT'}))
    store.retain_supervision_event(cleanup)
    return encoded(dict(schema='qualification_campaign_recovery_completion/v1',attempt_id=ATTEMPT,
        work_id=work_id,claim_sha256=recovery['claim_sha256'],
        observations_sha256=sha256(base64.b64decode(recovery['observations_bytes_b64'])),
        cleanup_event_sha256=sha256(cleanup),clock=clock(t)))


def test_successful_recovery_completion_releases_only_barrier_preserving_charge_and_token(tmp_path):
    from test_campaign_recovery import capture
    from c1_rail.qualification.execution.protocol import sha256
    store=metered(tmp_path); capture(store,t=11)
    store.settle_work(ATTEMPT,'admission',measured(t=12))
    before=snap(store)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(13)),recovery_owner_token=RECOVERY_TOKEN)
    store.recover_work(ATTEMPT,'admission',measured(t=14),recovery_owner_token=RECOVERY_TOKEN)
    blocked=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert blocked['recoveries'][0]['completion_bytes_b64'] is None
    completed=recovery_completion(store)
    result=store.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=RECOVERY_TOKEN)
    assert store.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=RECOVERY_TOKEN)==result
    after=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert after['schema']=='qualification_campaign_budget_snapshot/v4'
    assert after['state']=='BOUND' and after['settled_cpu_ns']==30
    assert after['authority_head']==before['authority_head']
    assert after['works'][0]['observation_bytes_b64']==before['works'][0]['observation_bytes_b64']
    raw=encoded(dict(limits=profile()['phases']['N1'],clock=clock(16),input_sha256=sha256(b'probe')))
    assert json.loads(store.reserve_work(ATTEMPT,'new','N1',raw,expected_revision=after['authority_revision']))['works'][-1]['state']=='RESERVED'
    with pytest.raises(ValueError,match='slot already spent'):
        store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(17)),recovery_owner_token=RECOVERY_TOKEN)



def test_runtime_authority_rejects_pending_recovery_snapshot(tmp_path):
    from c1_rail.qualification.execution.campaign_supervisor import _assert_authority
    store=metered(tmp_path)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    with pytest.raises(ValueError,match='recovery pending'):
        _assert_authority(snap(store))


def test_adapter_completes_owned_recovery_only_after_durable_facts_and_absence(tmp_path,monkeypatch):
    from types import SimpleNamespace
    from test_campaign_recovery import capture
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    store=metered(tmp_path,started=False)
    manifest=encoded(dict(schema='qualification_campaign_work_manifest/v1',attempt_id=ATTEMPT,
        work_id='admission',role='admission',probe='noop'))
    enrollment=supervisor.prepare_campaign_work(store,ATTEMPT,'admission',host_run_id='host1',
        manifest_bytes=manifest,clock_bytes=encoded(clock(12)))
    capture(store,t=13)
    raw=json.loads(measured(t=14));raw.update(campaign_scope_id=enrollment['scopes']['campaign_slice'],work_scope_id=enrollment['scopes']['payload_slice'])
    class Runtime:
        def observation(self,*args):
            assert snap(CampaignStore(ExecutionStore(store.store.path)))['recoveries'][0]['completion_bytes_b64'] is None
            return encoded(raw)
        def cleanup(self,*args):
            durable=snap(CampaignStore(ExecutionStore(store.store.path)))
            assert durable['settled_cpu_ns']==30
            assert durable['recoveries'][0]['observations_bytes_b64'] is not None
            assert durable['recoveries'][0]['completion_bytes_b64'] is None
    context=SimpleNamespace(store=store.store,campaign_runtime=Runtime(),recovery_issues={})
    monkeypatch.setattr(supervisor,'observe_campaign_clock',lambda:encoded(clock(14)))
    reservation=base64.b64decode(snap(store)['works'][0]['reservation_bytes_b64'])
    result=json.loads(supervisor.recover_campaign_work(context,reservation,attempt_id=ATTEMPT,work_id='admission'))
    assert result['recoveries'][0]['completion_bytes_b64'] is not None
    assert snap(CampaignStore(ExecutionStore(store.store.path)))==result


def test_reopen_rejects_missing_recovery_claim_object(tmp_path):
    import sqlite3
    from c1_rail.qualification.execution.protocol import sha256
    store=metered(tmp_path)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    role='supervision_control_'+sha256(encoded(['admission','RECOVERY_OWNER']))
    with sqlite3.connect(store.store.path) as connection:
        connection.execute('DELETE FROM full_campaign_objects WHERE attempt_id=? AND role=?',(ATTEMPT,role))
    with pytest.raises(ValueError,match='recovery claim'):
        ExecutionStore(store.store.path)


@pytest.mark.parametrize('target', ['RUNNING','CAPTURED','SIGNING_INTENT','SIGNED','COMPLETED'])
def test_pending_recovery_blocks_each_positive_work_transition(tmp_path,target):
    from test_campaign_budget import transition
    from test_campaign_recovery import capture
    store=metered(tmp_path)
    if target in ('SIGNING_INTENT','SIGNED','COMPLETED'):
        capture(store,t=11)
    data={}
    if target=='CAPTURED': data={'capture_bytes_b64':'eA=='}
    if target in ('SIGNING_INTENT','SIGNED'):
        intent=dict(intent_id='fixed',payload_bytes_b64='eA==',key_id='test',signing_at_utc=clock()['utc'])
        if target=='SIGNED': transition(store,'admission','SIGNING_INTENT',12,intent)
        else: data=intent
    if target=='SIGNED': data={'candidate_bytes_b64':'eA=='}
    if target=='COMPLETED': store.settle_work(ATTEMPT,'admission',measured(t=12))
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(13)))
    before=store.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError,match='recovery pending'):
        transition(store,'admission',target,14,data)
    assert store.budget_snapshot(ATTEMPT)==before


@pytest.mark.parametrize('slot',['START_OWNER','START_CLIENT'])
def test_pending_recovery_blocks_launch_control_claim(tmp_path,slot):
    store=metered(tmp_path)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    with pytest.raises(ValueError,match='recovery pending'):
        store.claim_supervision_control(ATTEMPT,'admission',slot,encoded(clock(13)))


def test_pending_recovery_blocks_first_authenticated_binding(tmp_path):
    config=profile(); config.update(schema='qualification_campaign_budget_profile/v2',orchestration_cpu_ns={p:10 for p in config['phases']})
    store=CampaignStore(ExecutionStore(tmp_path/'journal.sqlite'))
    store.begin_admission(request(),encoded(config),encoded(clock()))
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    with pytest.raises(ValueError,match='recovery pending'):
        store.bind_budget(ATTEMPT,contract_budget(),expected_revision=snap(store)['authority_revision'])
    assert snap(store)['budget'] is None


def test_pending_recovery_refuses_new_diagnostic_receipt_but_historical_receipt_remains(tmp_path):
    store,raw,context,plan,counters,now=admission_case(tmp_path)
    attempt=context.attempt_id
    store.claim_supervision_control(attempt,'admission','RECOVERY_OWNER',encoded(clock(13)),recovery_owner_token=RECOVERY_TOKEN)
    assert store.finish_diagnostic_admission(raw,context,plan,counters,now=now)['receipt'] is None
    assert 'diagnostic_receipt' not in store.objects(attempt)
    # Historical identity is readable and the provisional request cannot be
    # re-admitted through the dormant route to bypass its barrier.
    with pytest.raises(ValueError): store.admit(raw,context,plan,now=now)
    assert store.diagnostic_status(attempt)['historical'] is True


def test_claim_and_barrier_rollback_together_before_commit(tmp_path,monkeypatch):
    store=metered(tmp_path); before=store.budget_snapshot(ATTEMPT)
    original=store._save_budget
    def interrupted(*args,**kwargs):
        original(*args,**kwargs)
        raise RuntimeError('death before commit')
    with monkeypatch.context() as patch:
        patch.setattr(store,'_save_budget',interrupted)
        with pytest.raises(RuntimeError):
            store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert reopened.budget_snapshot(ATTEMPT)==before
    reopened.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    assert snap(reopened)['recoveries'][0]['completion_bytes_b64'] is None


def test_active_recovery_claim_refuses_outer_transaction_before_any_effect(tmp_path):
    store=metered(tmp_path);before=store.budget_snapshot(ATTEMPT)
    with store.store.transaction():
        with pytest.raises(ValueError,match='independent'):
            store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    assert store.budget_snapshot(ATTEMPT)==before


def test_competing_recovery_claimants_get_one_durable_owner(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    store=metered(tmp_path)
    def claim(token):
        try:
            store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=token)
            return 'claimed'
        except ValueError: return 'refused'
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(claim,[b'A'*32,b'B'*32]))
    assert sorted(results)==['claimed','refused']
    assert len(snap(CampaignStore(ExecutionStore(store.store.path)))['recoveries'])==1


@pytest.mark.parametrize('void_first',[False,True])
@pytest.mark.parametrize('unknown',['memory','termination','none'])
def test_recovery_completion_cannot_clear_uncertainty_or_void(tmp_path,void_first,unknown):
    from test_campaign_recovery import capture,void_request,NOW
    store=metered(tmp_path);capture(store,t=11)
    store.settle_work(ATTEMPT,'admission',measured(t=12))
    if void_first: store.void(void_request(),now=NOW)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(13)),recovery_owner_token=RECOVERY_TOKEN)
    observed=json.loads(measured(t=14))
    if unknown=='memory': observed['memory_peak_bytes']=None
    if unknown=='termination': observed['termination_known']=False
    store.recover_work(ATTEMPT,'admission',encoded(observed),recovery_owner_token=RECOVERY_TOKEN)
    if not void_first: store.void(void_request(),now=NOW)
    completed=recovery_completion(store)
    store.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=RECOVERY_TOKEN)
    state=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert state['validity']=='VOID' and state['settled_cpu_ns']==30
    assert state['state']==('BOUND' if unknown=='none' else 'BUDGET_UNCERTAIN')
    assert state['recoveries'][0]['completion_bytes_b64'] is not None


def test_crash_after_facts_requires_original_owner_and_no_unfunded_continuation(tmp_path):
    from test_campaign_recovery import capture
    store=metered(tmp_path);capture(store,t=11)
    store.settle_work(ATTEMPT,'admission',measured(t=12))
    before=snap(store)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(13)),recovery_owner_token=RECOVERY_TOKEN)
    store.recover_work(ATTEMPT,'admission',measured(t=14),recovery_owner_token=RECOVERY_TOKEN)
    reopened=CampaignStore(ExecutionStore(store.store.path)); completed=recovery_completion(reopened)
    with pytest.raises(ValueError,match='owner differs'):
        reopened.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=b'X'*32)
    with pytest.raises(ValueError,match='slot already spent'):
        reopened.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(15)),recovery_owner_token=b'X'*32)
    state=snap(reopened)
    assert state['remaining_cpu_ns']==before['remaining_cpu_ns']
    assert state['recoveries'][0]['completion_bytes_b64'] is None


def test_legacy_recovery_claim_stays_readable_but_blocks_new_authority(tmp_path):
    from c1_rail.qualification.execution.protocol import sha256
    from test_campaign_budget import reserve
    store=metered(tmp_path)
    raw=encoded(dict(schema='qualification_campaign_supervision_event/v1',attempt_id=ATTEMPT,
        work_id='admission',kind='CONTROL',clock=clock(12),data={'slot':'RECOVERY_OWNER'}))
    role='supervision_control_'+sha256(encoded(['admission','RECOVERY_OWNER']))
    with store.store.transaction() as connection:
        connection.execute('INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',(ATTEMPT,role,sha256(raw),len(raw),raw))
    reopened=CampaignStore(ExecutionStore(store.store.path))
    assert snap(reopened)['schema']=='qualification_campaign_budget_snapshot/v3'
    with pytest.raises(ValueError,match='recovery pending'): reserve(reopened)


def test_completion_requires_claim_bound_committed_observation_and_durable_absence(tmp_path):
    from test_campaign_recovery import capture
    store=metered(tmp_path);capture(store,t=11)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    store.recover_work(ATTEMPT,'admission',measured(t=13),recovery_owner_token=RECOVERY_TOKEN)
    completed=json.loads(recovery_completion(store,t=14))
    for name in ('claim_sha256','observations_sha256','cleanup_event_sha256'):
        altered=dict(completed);altered[name]='f'*64
        with pytest.raises(ValueError):
            store.complete_recovery(ATTEMPT,'admission',encoded(altered),recovery_owner_token=RECOVERY_TOKEN)
    assert snap(store)['recoveries'][0]['completion_bytes_b64'] is None


def test_one_completed_recovery_does_not_clear_another_pending_owner(tmp_path):
    from test_campaign_recovery import capture
    from test_campaign_budget import reserve,transition
    store=metered(tmp_path);capture(store,t=11)
    store.settle_work(ATTEMPT,'admission',measured(t=12));transition(store,'admission','COMPLETED',13)
    reserve(store,t=14)
    other=next(w['work_id'] for w in snap(store)['works'] if w['work_id']!='admission')
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(15)),recovery_owner_token=RECOVERY_TOKEN)
    store.claim_supervision_control(ATTEMPT,other,'RECOVERY_OWNER',encoded(clock(15)),recovery_owner_token=b'B'*32)
    store.recover_work(ATTEMPT,'admission',measured(t=16),recovery_owner_token=RECOVERY_TOKEN)
    store.complete_recovery(ATTEMPT,'admission',recovery_completion(store,t=17),recovery_owner_token=RECOVERY_TOKEN)
    with pytest.raises(ValueError,match='recovery pending'): start(store,other,t=18)


def test_reserved_negative_abort_remains_available_after_recovery_facts(tmp_path):
    from test_campaign_budget import transition
    store=metered(tmp_path,started=False)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    store.recover_work(ATTEMPT,'admission',encoded(clock(13)),recovery_owner_token=RECOVERY_TOKEN)
    transition(store,'admission','ABORTED',14)
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['state']=='ABORTED'


def test_independent_model_matches_pending_and_completed_recovery(tmp_path):
    from lifecycle_model import CampaignBudgetModel
    from test_campaign_budget import transition
    from test_campaign_recovery import capture
    model=CampaignBudgetModel(1_000_000_000,60,overhead=10)
    store=metered(tmp_path)
    assert model.apply('intent'); assert model.apply('running'); assert model.apply('capture')
    capture(store,t=11)
    assert model.apply('recovery_claim')
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    assert model.apply('recover',charge=20)
    store.recover_work(ATTEMPT,'admission',measured(t=13),recovery_owner_token=RECOVERY_TOKEN)
    assert not model.apply('complete')
    with pytest.raises(ValueError): transition(store,'admission','COMPLETED',14)
    assert model.apply('recovery_complete')
    store.complete_recovery(ATTEMPT,'admission',recovery_completion(store,t=14),recovery_owner_token=RECOVERY_TOKEN)
    assert model.apply('complete')
    transition(store,'admission','COMPLETED',15)
    result=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert result['settled_cpu_ns']==model.charge==30
    assert result['remaining_cpu_ns']==model.remaining
    assert result['works'][0]['state']==model.state=='COMPLETED'
    assert not model.apply('recovery_claim')
    with pytest.raises(ValueError,match='slot already spent'):
        store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(16)),recovery_owner_token=b'X'*32)
    assert model.recovery_pending is snap(store)['recoveries'][0]['continuation_required'] is True
    assert not model.apply('recovery_complete')


def test_unknown_first_counter_completes_barrier_but_never_restores_authority(tmp_path):
    from test_campaign_recovery import capture
    store=metered(tmp_path); capture(store,t=11)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    store.recover_work(ATTEMPT,'admission',measured(cpu=None,t=13),recovery_owner_token=RECOVERY_TOKEN)
    store.complete_recovery(ATTEMPT,'admission',recovery_completion(store,t=14),recovery_owner_token=RECOVERY_TOKEN)
    state=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert state['state']=='BUDGET_UNCERTAIN' and state['settled_cpu_ns']==60
    assert state['recoveries'][0]['completion_bytes_b64'] is not None


def test_insufficient_continuation_allowance_never_reuses_spent_owner(tmp_path):
    from c1_rail.qualification.execution.protocol import sha256
    config=profile()
    config['schema']='qualification_campaign_budget_profile/v2'
    for limit in config['phases'].values(): limit['cpu_ns']=80_000_000
    config['orchestration_cpu_ns']={phase:10_000_000 for phase in config['phases']}
    store=CampaignStore(ExecutionStore(tmp_path/'journal.sqlite'))
    store.begin_admission(request(),encoded(config),encoded(clock()))
    store.bind_budget(ATTEMPT,contract_budget(),expected_revision=snap(store)['authority_revision'])
    for index,phase in enumerate(p for p in config['phases'] if p!='ADMISSION'):
        raw=encoded(dict(limits=config['phases'][phase],clock=clock(11),input_sha256=sha256(b'probe')))
        store.reserve_work(ATTEMPT,'work'+str(index),phase,raw,expected_revision=snap(store)['authority_revision'])
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    before=snap(store)
    assert before['remaining_cpu_ns']==40_000_000 < config['phases']['RESULT']['cpu_ns']
    raw=encoded(dict(limits=config['phases']['RESULT'],clock=clock(13),input_sha256=sha256(b'probe')))
    with pytest.raises(ValueError,match='recovery pending'):
        store.reserve_work(ATTEMPT,'continuation','RESULT',raw,expected_revision=before['authority_revision'])
    with pytest.raises(ValueError,match='slot already spent'):
        store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(13)),recovery_owner_token=b'X'*32)
    assert snap(store)==before


def test_spent_completed_recovery_requires_funded_continuation_before_new_authority(tmp_path):
    from test_campaign_recovery import capture
    from test_campaign_budget import reserve
    store=metered(tmp_path);capture(store,t=11)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    store.recover_work(ATTEMPT,'admission',measured(t=13),recovery_owner_token=RECOVERY_TOKEN)
    completion=recovery_completion(store,t=14)
    store.complete_recovery(ATTEMPT,'admission',completion,recovery_owner_token=RECOVERY_TOKEN)
    saved=snap(store)['recoveries'][0]['completion_bytes_b64']
    with pytest.raises(ValueError,match='slot already spent'):
        store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(15)),recovery_owner_token=b'X'*32)
    reopened=CampaignStore(ExecutionStore(store.store.path))
    # Replaying an old completion is historical; it cannot resolve this new need.
    reopened.complete_recovery(ATTEMPT,'admission',completion,recovery_owner_token=RECOVERY_TOKEN)
    with pytest.raises(ValueError,match='recovery pending'): reserve(reopened,t=16)
    assert snap(reopened)['recoveries'][0]['completion_bytes_b64']==saved
    assert snap(reopened)['settled_cpu_ns']==30



def test_reserved_recovery_then_start_then_spent_request_blocks_without_active_runtime(tmp_path,monkeypatch):
    from types import SimpleNamespace
    from test_campaign_recovery import void_request,NOW
    from test_campaign_budget import reserve
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    store=metered(tmp_path,started=False)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(11)),recovery_owner_token=RECOVERY_TOKEN)
    store.recover_work(ATTEMPT,'admission',encoded(clock(12)),recovery_owner_token=RECOVERY_TOKEN)
    completed=recovery_completion(store,t=13)
    store.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=RECOVERY_TOKEN)
    # Exact history does not manufacture a fresh barrier.
    store.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=RECOVERY_TOKEN)
    start(store,t=14)
    saved=snap(store)
    def forbidden(*args): raise AssertionError('denied recovery constructed active runtime')
    monkeypatch.setattr(supervisor,'LinuxCampaignRuntime',forbidden)
    monkeypatch.setattr(supervisor,'observe_campaign_clock',lambda:encoded(clock(15)))
    context=SimpleNamespace(store=store.store,recovery_issues={})
    raw=base64.b64decode(saved['works'][0]['reservation_bytes_b64'])
    with pytest.raises(ValueError,match='slot already spent'):
        supervisor.recover_campaign_work(context,raw,attempt_id=ATTEMPT,work_id='admission')
    reopened=CampaignStore(ExecutionStore(store.store.path))
    state=snap(reopened)
    assert state['recoveries'][0]['continuation_required'] is True
    assert state['recoveries'][0]['completion_bytes_b64']==saved['recoveries'][0]['completion_bytes_b64']
    assert state['reserved_cpu_ns']==saved['reserved_cpu_ns']==60
    reopened.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=RECOVERY_TOKEN)
    with pytest.raises(ValueError,match='recovery pending'): reserve(reopened,t=16)
    reopened.settle_work(ATTEMPT,'admission',measured(t=16))
    reopened.void(void_request(),now=NOW)
    reopened.complete_recovery(ATTEMPT,'admission',completed,recovery_owner_token=RECOVERY_TOKEN)
    final=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert final['validity']=='VOID' and final['settled_cpu_ns']==30
    assert final['recoveries'][0]['continuation_required'] is True


@pytest.mark.parametrize('corruption',['old_version','missing_barrier','wrong_bool','unknown_field'])
def test_snapshot_cannot_strip_or_reinterpret_recovery_barrier(tmp_path,corruption):
    store=metered(tmp_path)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    state=snap(store)
    if corruption=='old_version': state['schema']='qualification_campaign_budget_snapshot/v3'
    elif corruption=='missing_barrier': state.pop('recoveries')
    elif corruption=='wrong_bool': state['recoveries'][0]['continuation_required']=0
    else: state['recoveries'][0]['clear']=True
    with pytest.raises(ValueError): parse_campaign_budget_snapshot(encoded(state))


@pytest.mark.parametrize('malformed',[None,[],0])
def test_recovery_snapshot_rejects_nonobject_facts_with_validation_error(tmp_path,malformed):
    store=metered(tmp_path)
    store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(12)))
    state=snap(store)
    state['recoveries'][0]['observations_bytes_b64']=base64.b64encode(encoded(malformed)).decode()
    with pytest.raises(ValueError): parse_campaign_budget_snapshot(encoded(state))



def test_recovery_committed_after_client_claim_prevents_physical_spawn(tmp_path,monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from c1_rail.qualification.execution import runtime as installed
    store=metered(tmp_path)
    context=SimpleNamespace(store=store.store)
    adapter=supervisor.LinuxCampaignRuntime.__new__(supervisor.LinuxCampaignRuntime);adapter.context=context
    original=CampaignStore.claim_supervision_control
    def raced(self,attempt,work,slot,clock_bytes,**kwargs):
        result=original(self,attempt,work,slot,clock_bytes,**kwargs)
        if slot=='START_CLIENT':
            original(self,attempt,work,'RECOVERY_OWNER',encoded(clock(13)))
        return result
    monkeypatch.setattr(CampaignStore,'claim_supervision_control',raced)
    monkeypatch.setattr(supervisor,'observe_campaign_clock',lambda:encoded(clock(14)))
    monkeypatch.setattr(installed,'installed_code_root',lambda:Path('/opt/test'))
    def forbidden(*args,**kwargs): raise AssertionError('physical spawn after recovery committed')
    monkeypatch.setattr(supervisor.subprocess,'Popen',forbidden)
    with pytest.raises(ValueError,match='recovery pending'):
        adapter._control(['fixed-command'],enrollment={'attempt_id':ATTEMPT,'work_id':'admission'})


def test_recovery_committed_after_container_creation_prevents_physical_start(tmp_path,monkeypatch):
    from types import SimpleNamespace
    from test_campaign_budget import transition
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from c1_rail.qualification.execution.protocol import sha256
    store=metered(tmp_path,started=False)
    manifest=dict(schema='qualification_campaign_work_manifest/v1',attempt_id=ATTEMPT,work_id='probe',role='probe_worker',probe='noop')
    raw=encoded(dict(limits=profile()['phases']['N1'],clock=clock(11),input_sha256=sha256(encoded(manifest))))
    store.reserve_work(ATTEMPT,'probe','N1',raw,expected_revision=snap(store)['authority_revision'])
    enrollment=supervisor.prepare_campaign_work(store,ATTEMPT,'probe',host_run_id='host1',manifest_bytes=encoded(manifest),clock_bytes=encoded(clock(12)))
    transition(store,'probe','RUNNING',13)
    state=snap(store);work=next(w for w in state['works'] if w['work_id']=='probe')
    body=dict(Image='sha256:'+'a'*64,User='61001',Entrypoint=['fixed'],Cmd=['noop'],HostConfig={'CgroupParent':enrollment['scopes']['payload_slice']})
    class Docker:
        def call(self,method,path,body_arg=None):
            if path=='/info': return {'CgroupDriver':'systemd'}
            if '/create?' in path:return {'Id':'f'*64}
            if path.endswith('/json'):
                store.claim_supervision_control(ATTEMPT,'probe','RECOVERY_OWNER',encoded(clock(14)))
                return dict(Image=body['Image'],Config=body,HostConfig=body['HostConfig'])
            raise AssertionError('physical Docker start after recovery committed')
    monkeypatch.setattr(supervisor,'DockerControl',Docker)
    monkeypatch.setattr(supervisor,'probe_container_body',lambda *args:body)
    monkeypatch.setattr(supervisor,'observe_campaign_clock',lambda:encoded(clock(14)))
    with pytest.raises(ValueError,match='recovery pending'):
        supervisor._run_probe(SimpleNamespace(),store,SimpleNamespace(),state,work,enrollment,manifest)



def test_launch_first_finishes_bounded_request_before_recovery_claim_commits(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    from test_campaign_budget import reserve
    store=metered(tmp_path)
    requested=Event();effects=[]
    def recover():
        requested.set()
        store.claim_supervision_control(ATTEMPT,'admission','RECOVERY_OWNER',encoded(clock(13)))
    with ThreadPoolExecutor(max_workers=1) as pool:
        with store.launch_gate(ATTEMPT,'admission',lambda:encoded(clock(12))):
            effects.append('start request accepted')
            future=pool.submit(recover)
            assert requested.wait(2)
            assert not future.done()
        future.result(timeout=5)
    assert effects==['start request accepted']
    with pytest.raises(ValueError,match='recovery pending'): reserve(store,t=14)


def test_expired_serialized_dispatch_commits_terminal_clock_without_external_effect(tmp_path):
    store=metered(tmp_path);effects=[]
    with pytest.raises(ValueError,match='dispatch deadline'):
        with store.launch_gate(ATTEMPT,'admission',lambda:encoded(clock(20_000_000_000))):
            effects.append('started')
    state=snap(CampaignStore(ExecutionStore(store.store.path)))
    assert not effects and state['state']=='BUDGET_EXHAUSTED'
    assert state['last_clock']==clock(20_000_000_000)


@pytest.mark.parametrize('failure',['lost_ack','commit','persistent'])
def test_external_start_survives_failure_as_owned_spent_uncertain_work(tmp_path,monkeypatch,failure):
    import sqlite3
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from c1_rail.qualification.execution import runtime as installed
    from c1_rail.qualification.execution.protocol import sha256
    store=metered(tmp_path,started=False)
    effects={'starts':0,'injected':False}
    original_connect=store.store._connect
    class Connection:
        def __init__(self):self.inner=original_connect()
        def __getattr__(self,name):return getattr(self.inner,name)
        def execute(self,sql,*args):
            if sql=='COMMIT' and effects['starts'] and (failure=='persistent' or (failure=='commit' and not effects['injected'])):
                effects['injected']=True
                raise sqlite3.OperationalError('commit failed after physical start')
            return self.inner.execute(sql,*args)
    monkeypatch.setattr(store.store,'_connect',Connection)
    class Runtime(supervisor.LinuxCampaignRuntime):
        def __init__(self,context):self.context=context
        def start(self,state,work,enrollment):self._control(['fixed-command'],enrollment=enrollment)
        def observation(self,state,work,enrollment):
            raw=json.loads(measured(cpu=None,t=14));raw.update(campaign_scope_id=enrollment['scopes']['campaign_slice'],
                work_scope_id=enrollment['scopes']['payload_slice'],termination_known=False)
            return encoded(raw)
        def cleanup(self,enrollment):
            durable=snap(CampaignStore(ExecutionStore(store.store.path)))
            assert durable['state']=='BUDGET_UNCERTAIN'
            assert durable['recoveries'][0]['completion_bytes_b64'] is None
    context=SimpleNamespace(store=store.store,config={'host_run_id':'host1'},recovery_issues={})
    context.campaign_runtime=Runtime(context)
    monkeypatch.setattr(supervisor,'observe_campaign_clock',lambda:encoded(clock(14)))
    monkeypatch.setattr(installed,'installed_code_root',lambda:Path('/opt/test'))
    class Process:
        returncode=None
        def __init__(self,*args,**kwargs): effects['starts']+=1
        def communicate(self,**kwargs):
            if failure=='lost_ack':raise OSError('start accepted but acknowledgement lost')
            self.returncode=0
            return b'o "/org/freedesktop/systemd1/job/42"\n',b''
        def kill(self):self.returncode=-9
    monkeypatch.setattr(supervisor.subprocess,'Popen',Process)
    manifest=encoded(dict(schema='qualification_campaign_work_manifest/v1',attempt_id=ATTEMPT,work_id='admission',role='admission',probe='noop'))
    reservation=base64.b64decode(snap(store)['works'][0]['reservation_bytes_b64'])
    with pytest.raises((OSError,sqlite3.Error)) as failure_info:
        supervisor.run_campaign_work(context,reservation,manifest)
    reopened=CampaignStore(ExecutionStore(store.store.path));state=snap(reopened)
    if failure=='persistent':
        from test_campaign_budget import reserve
        assert failure_info.value.__context__ is not None or failure_info.value.__cause__ is not None
        assert state['works'][0]['state']=='START_INTENT'
        assert state['reserved_cpu_ns']==60 and state['settled_cpu_ns']==0
        assert 'supervision_admission' in reopened.objects(ATTEMPT)
        with pytest.raises(ValueError,match='dispatch pending'): reserve(reopened,t=15)
        return
    assert state['state']=='BUDGET_UNCERTAIN' and state['works'][0]['state']=='IN_DOUBT'
    assert state['settled_cpu_ns']==60
    objects=reopened.objects(ATTEMPT)
    assert 'supervision_admission' in objects
    assert 'supervision_control_'+sha256(encoded(['admission','START_CLIENT'])) in objects
    supervisor.run_campaign_work(context,reservation,manifest)
    assert effects['starts']==1


def test_dispatch_samples_clock_inside_serialized_decision(tmp_path):
    store=metered(tmp_path);samples=[]
    def current_clock():
        assert getattr(store.store._local,'connection',None) is not None
        samples.append('under lock')
        return encoded(clock(20_000_000_000))
    with pytest.raises(ValueError,match='dispatch deadline'):
        with store.launch_gate(ATTEMPT,'admission',current_clock):
            pytest.fail('expired request reached physical effect')
    assert samples==['under lock']
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['state']=='BUDGET_EXHAUSTED'


def test_control_spawns_under_gate_but_waits_outside_store_transaction(tmp_path,monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from c1_rail.qualification.execution import runtime as installed
    store=metered(tmp_path);effects=[]
    adapter=supervisor.LinuxCampaignRuntime.__new__(supervisor.LinuxCampaignRuntime)
    adapter.context=SimpleNamespace(store=store.store)
    class Process:
        returncode=0
        def __init__(self,*args,**kwargs):
            assert getattr(store.store._local,'connection',None) is not None
            effects.append('spawn')
        def communicate(self,**kwargs):
            assert getattr(store.store._local,'connection',None) is None
            effects.append('wait')
            return b'o "/org/freedesktop/systemd1/job/42"\n',b''
    def forbidden(*args,**kwargs):raise AssertionError('run waits for a child inside the gate')
    monkeypatch.setattr(supervisor.subprocess,'run',forbidden)
    monkeypatch.setattr(supervisor.subprocess,'Popen',Process)
    monkeypatch.setattr(installed,'installed_code_root',lambda:Path('/opt/test'))
    monkeypatch.setattr(supervisor,'observe_campaign_clock',lambda:encoded(clock(12)))
    adapter._control(['fixed-command'],enrollment={'attempt_id':ATTEMPT,'work_id':'admission'})
    assert effects==['spawn','wait']


def test_physical_start_without_acknowledgement_blocks_reopen_until_live_owner_ack(tmp_path):
    from test_campaign_budget import reserve
    store=metered(tmp_path); before=snap(store)
    with store.launch_gate(ATTEMPT,'admission',lambda:encoded(clock(12))) as permit:
        pass # Simulated start request accepted; no acknowledgement committed yet.
    reopened=CampaignStore(ExecutionStore(store.store.path))
    with pytest.raises(ValueError,match='dispatch pending'): reserve(reopened,t=13)
    reopened.acknowledge_dispatch(ATTEMPT,'admission','guardian',permit['token'],lambda:encoded(clock(14)))
    assert snap(reopened)['authority_head']==before['authority_head']
    reserve(reopened,t=15)


@pytest.mark.parametrize('interruption', ['recovery', 'void', 'terminal'])
def test_late_dispatch_ack_clears_only_own_marker_without_restoring_authority(tmp_path, interruption):
    from test_campaign_recovery import void_request, NOW
    from test_campaign_budget import reserve
    store = metered(tmp_path)
    with store.launch_gate(ATTEMPT, 'admission', lambda: encoded(clock(12))) as permit:
        pass
    if interruption == 'recovery':
        store.claim_supervision_control(ATTEMPT, 'admission', 'RECOVERY_OWNER', encoded(clock(13)))
    elif interruption == 'void':
        store.void(void_request(), now=NOW)
    else:
        store.settle_work(ATTEMPT, 'admission', measured(cpu=None, t=13))
    before = snap(store)
    store.acknowledge_dispatch(ATTEMPT, 'admission', 'guardian', permit['token'], lambda: encoded(clock(14)))
    after = snap(CampaignStore(ExecutionStore(store.store.path)))
    assert after['dispatches'][0]['acknowledged_clock'] == clock(14)
    for key in ('state', 'validity', 'authority_head', 'settled_cpu_ns', 'reserved_cpu_ns', 'recoveries'):
        assert after[key] == before[key]
    with pytest.raises(ValueError): reserve(store, t=15)


def test_dispatch_ack_requires_own_token_and_cannot_relaunch_or_resample_replay(tmp_path):
    from test_campaign_budget import reserve
    store = metered(tmp_path)
    with store.launch_gate(ATTEMPT, 'admission', lambda: encoded(clock(12))) as permit:
        pass
    for role, token in [('payload', permit['token']), ('guardian', b'x' * 32)]:
        with pytest.raises(ValueError, match='dispatch owner'):
            store.acknowledge_dispatch(ATTEMPT, 'admission', role, token, lambda: encoded(clock(13)))
    with pytest.raises(ValueError, match='dispatch pending'): reserve(store, t=13)
    first = store.acknowledge_dispatch(ATTEMPT, 'admission', 'guardian', permit['token'], lambda: encoded(clock(14)))
    def forbidden(): raise AssertionError('historical acknowledgement must not sample a new clock')
    assert store.acknowledge_dispatch(ATTEMPT, 'admission', 'guardian', permit['token'], forbidden) == first
    with pytest.raises(ValueError, match='already spent'):
        with store.launch_gate(ATTEMPT, 'admission', lambda: encoded(clock(15))):
            pytest.fail('relaunch')


def test_guardian_job_reply_does_not_wait_for_guardian_ack_waiter(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from c1_rail.qualification.execution import runtime as installed
    store = metered(tmp_path)
    waiting = Event()
    adapter = supervisor.LinuxCampaignRuntime.__new__(supervisor.LinuxCampaignRuntime)
    adapter.context = SimpleNamespace(store=store.store)
    original_snapshot = store.budget_snapshot
    def snapshot(attempt):
        raw = original_snapshot(attempt)
        if json.loads(raw)['dispatches'][0]['acknowledged_clock'] is None:
            waiting.set()
        return raw
    monkeypatch.setattr(store, 'budget_snapshot', snapshot)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(12)))
    monkeypatch.setattr(installed, 'installed_code_root', lambda: Path('/opt/test'))
    futures = []
    with ThreadPoolExecutor(max_workers=1) as pool:
        class Process:
            returncode = 0
            def __init__(self, *args, **kwargs):
                futures.append(pool.submit(supervisor._await_dispatch_ack, store, ATTEMPT, 'admission', 10**9))
            def communicate(self, **kwargs):
                assert getattr(store.store._local, 'connection', None) is None
                assert waiting.wait(2)
                assert not futures[0].done()  # Job queued; guardian application still waiting.
                return b'o "/org/freedesktop/systemd1/job/42"\n', b''
        monkeypatch.setattr(supervisor.subprocess, 'Popen', Process)
        adapter._control(['fixed-command'], enrollment={'attempt_id': ATTEMPT, 'work_id': 'admission'})
        result = futures[0].result(timeout=2)
    assert result['dispatches'][0]['acknowledged_clock'] == clock(12)


@pytest.mark.parametrize('interrupt', ['recovery', 'void', 'deadline'])
def test_guardian_wait_stops_at_revocation_or_original_deadline(tmp_path, monkeypatch, interrupt):
    from test_campaign_recovery import void_request, NOW
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    store = metered(tmp_path)
    with store.launch_gate(ATTEMPT, 'admission', lambda: encoded(clock(12))): pass
    if interrupt == 'recovery':
        store.claim_supervision_control(ATTEMPT, 'admission', 'RECOVERY_OWNER', encoded(clock(13)))
    elif interrupt == 'void':
        store.void(void_request(), now=NOW)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(20)))
    with pytest.raises(ValueError, match='revoked|deadline'):
        supervisor._await_dispatch_ack(store, ATTEMPT, 'admission', 20)
    assert snap(store)['dispatches'][0]['acknowledged_clock'] is None


@pytest.mark.parametrize('corruption', ['omit', 'old_version', 'role', 'owner', 'duplicate', 'unknown_field'])
def test_dispatch_snapshot_is_closed_and_cannot_strip_pending_marker(tmp_path, corruption):
    store = metered(tmp_path)
    with store.launch_gate(ATTEMPT, 'admission', lambda: encoded(clock(12))): pass
    state = snap(store)
    if corruption == 'omit': state.pop('dispatches')
    elif corruption == 'old_version': state['schema'] = 'qualification_campaign_budget_snapshot/v3'
    elif corruption == 'role': state['dispatches'][0]['role'] = 'arbitrary'
    elif corruption == 'owner': state['dispatches'][0]['owner_sha256'] = None
    elif corruption == 'duplicate': state['dispatches'].append(state['dispatches'][0])
    else: state['dispatches'][0]['clear'] = True
    with pytest.raises(ValueError): parse_campaign_budget_snapshot(encoded(state))


@pytest.mark.parametrize('operation', ['binding', 'receipt', 'control', 'capture', 'running', 'runtime'])
def test_pending_dispatch_blocks_positive_authority(tmp_path, operation):
    from c1_rail.qualification.execution.campaign_supervisor import _assert_authority
    store, raw, context, plan, counters, now = admission_case(tmp_path)
    attempt = context.attempt_id
    with store.launch_gate(attempt, 'admission', lambda: encoded(clock(11))): pass
    before = store.budget_snapshot(attempt)
    if operation == 'receipt':
        assert store.finish_diagnostic_admission(raw, context, plan, counters, now=now)['receipt'] is None
    else:
        with pytest.raises(ValueError, match='dispatch pending'):
            state = json.loads(before)
            if operation == 'binding':
                store.bind_budget(attempt, encoded(json.loads(plan)['budget']), expected_revision=state['authority_revision'])
            elif operation == 'control':
                store.claim_supervision_control(attempt, 'admission', 'START_CLIENT', encoded(clock(12)))
            elif operation == 'runtime':
                _assert_authority(state)
            else:
                store.record_work_transition(attempt, 'admission', encoded(dict(
                    schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id='admission',
                    state='CAPTURED' if operation == 'capture' else 'RUNNING', clock=clock(12),
                    data={'capture_bytes_b64':'eA=='} if operation == 'capture' else {})),
                    expected_revision=state['authority_revision'])
    assert store.budget_snapshot(attempt) == before
    assert 'diagnostic_receipt' not in store.objects(attempt)


@pytest.mark.parametrize('ack', [b'', b'o "/wrong/job/42"\n', b's "ready"\n'])
def test_untrusted_job_reply_keeps_dispatch_pending(tmp_path, monkeypatch, ack):
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from c1_rail.qualification.execution import runtime as installed
    store = metered(tmp_path)
    adapter = supervisor.LinuxCampaignRuntime.__new__(supervisor.LinuxCampaignRuntime)
    adapter.context = SimpleNamespace(store=store.store)
    class Process:
        returncode = 0
        def __init__(self, *args, **kwargs): pass
        def communicate(self, **kwargs): return ack, b''
    monkeypatch.setattr(supervisor.subprocess, 'Popen', Process)
    monkeypatch.setattr(installed, 'installed_code_root', lambda: Path('/opt/test'))
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(12)))
    with pytest.raises(ValueError, match='job acknowledgement'):
        adapter._control(['fixed-command'], enrollment={'attempt_id':ATTEMPT, 'work_id':'admission'})
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['dispatches'][0]['acknowledged_clock'] is None



def test_client_wait_subtracts_spawn_time_from_original_deadline(tmp_path, monkeypatch):
    from types import SimpleNamespace
    from c1_rail.qualification.execution import campaign_supervisor as supervisor
    from c1_rail.qualification.execution import runtime as installed
    store = metered(tmp_path)
    initial = snap(store)
    work = initial['works'][0]
    reserved = json.loads(base64.b64decode(work['reservation_bytes_b64']))
    deadline = min(initial['deadline_boottime_ns'], reserved['clock']['boottime_ns'] + work['limits']['wall_ns'])
    adapter = supervisor.LinuxCampaignRuntime.__new__(supervisor.LinuxCampaignRuntime)
    adapter.context = SimpleNamespace(store=store.store)
    spawned = []
    class Process:
        returncode = 0
        def __init__(self, *args, **kwargs): spawned.append(True)
        def communicate(self, *, timeout):
            assert timeout == 10 / 10**9  # Only ten nanoseconds remain after simulated spawn.
            return b'o "/org/freedesktop/systemd1/job/42"\n', b''
    monkeypatch.setattr(supervisor.subprocess, 'Popen', Process)
    monkeypatch.setattr(installed, 'installed_code_root', lambda: Path('/opt/test'))
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(deadline - 10 if spawned else 12)))
    adapter._control(['fixed-command'], enrollment={'attempt_id':ATTEMPT, 'work_id':'admission'})
