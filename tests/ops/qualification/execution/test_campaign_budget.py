"""S1 trusted observations are simulated; no Linux enforcement is claimed."""
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from threading import Event

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.store import ExecutionStore

PHASES = ('ADMISSION', 'N1', 'N1_CAPTURE', 'N1_G5', 'N2', 'N2_CAPTURE',
          'N2_G5', 'PART_A', 'PART_A_CAPTURE', 'PART_A_G5', 'RESULT', 'SEAL')
ATTEMPT = 'budget-attempt'
NOW = datetime(2026, 9, 19, tzinfo=timezone.utc)


def clock(t=10, boot='boot-1'):
    return dict(schema='qualification_campaign_clock/v1', boot_id=boot,
                boottime_ns=t, utc='2026-09-19T00:00:00Z')


def profile():
    return dict(schema='qualification_campaign_budget_profile/v1',
                installed_profile_sha256='a' * 64, record_byte_limit=131072,
                phases={name: dict(cpu_ns=60, wall_ns=10**9, memory_bytes=100)
                        for name in PHASES})


def request():
    return encoded(dict(schema='qualification_campaign_request/v1', operation='SUBMIT_E1',
                        attempt_id=ATTEMPT, request_id='request-1', bundle_sha256='b' * 64))


def contract_budget():
    return encoded(dict(identity_sha256='c' * 64, maximum_cpu_seconds=1,
        maximum_wall_seconds=20, maximum_memory_bytes=100,
        n1_paths=1, n2_paths=1, part_a_initial_paths=1, part_a_expanded_paths=2, n3_paths=1))


def snap(store):
    return json.loads(store.budget_snapshot(ATTEMPT))


def opened(tmp_path, bind=True):
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    store.begin_admission(request(), encoded(profile()), encoded(clock()))
    if bind:
        store.bind_budget(ATTEMPT, contract_budget(), expected_revision=snap(store)['authority_revision'])
    return store


def reserve(store, work='n1', phase='N1', t=11):
    return store.reserve_work(ATTEMPT, work, phase,
        encoded(dict(limits=profile()['phases'][phase], clock=clock(t), input_sha256='d' * 64)),
        expected_revision=snap(store)['authority_revision'])


def transition(store, work, state, t=12, data=None):
    return store.record_work_transition(ATTEMPT, work,
        encoded(dict(schema='qualification_campaign_work_transition/v1',
                     attempt_id=ATTEMPT, work_id=work, state=state, clock=clock(t), data=data or {})),
        expected_revision=snap(store)['authority_revision'])


def observation(work='admission', cpu=20, t=11, boot='boot-1', **extra):
    return encoded(dict(schema='qualification_campaign_observation/v1', attempt_id=ATTEMPT,
        work_id=work, clock=clock(t, boot), campaign_scope_id='parent-1',
        work_scope_id='scope-' + work, cpu_ns=cpu, memory_peak_bytes=50, oom_events=0, **extra))


def start(store, work='admission', t=10):
    return transition(store, work, 'START_INTENT', t,
                      dict(campaign_scope_id='parent-1', work_scope_id='scope-' + work))


def test_provisional_admission_is_durable_before_contract_validation(tmp_path):
    store = opened(tmp_path, bind=False)
    before = store.budget_snapshot(ATTEMPT)
    assert snap(store)['state'] == 'PROVISIONAL'
    assert snap(store)['reserved_cpu_ns'] == 60
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT) == before
    assert store.begin_admission(request(), encoded(profile()), encoded(clock())) == before
    with pytest.raises(ValueError):
        store.begin_admission(request(), encoded(profile()), encoded(clock(20)))


def test_open_reservation_cannot_be_spent_twice():
    from c1_rail.qualification.execution.campaign_budget import remaining_cpu
    assert remaining_cpu(100, (20,), (60,)) == 20
    assert remaining_cpu(100, (20, 60), ()) == 20
    with pytest.raises(ValueError): remaining_cpu(True, (), ())


def test_admission_charges_and_deadline_survive_budget_binding(tmp_path):
    store = opened(tmp_path, bind=False)
    start(store)
    store.settle_work(ATTEMPT, 'admission', observation())
    store.bind_budget(ATTEMPT, contract_budget(), expected_revision=snap(store)['authority_revision'])
    result = snap(store)
    assert result['settled_cpu_ns'] == 20 and result['reserved_cpu_ns'] == 0
    assert result['deadline_boottime_ns'] == 20_000_000_010
    assert result['start_clock'] == clock()


def test_settlement_idempotency_conflict_and_lost_counter(tmp_path):
    store = opened(tmp_path)
    start(store)
    first = store.settle_work(ATTEMPT, 'admission', observation())
    assert store.settle_work(ATTEMPT, 'admission', observation()) == first
    with pytest.raises(ValueError): store.settle_work(ATTEMPT, 'admission', observation(cpu=21))
    reserve(store)
    start(store, 'n1', 11)
    store.settle_work(ATTEMPT, 'n1', observation('n1', None, 12))
    result = snap(store)
    assert result['settled_cpu_ns'] == 80 and result['reserved_cpu_ns'] == 0
    assert result['state'] == 'BUDGET_UNCERTAIN'
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT) == store.budget_snapshot(ATTEMPT)


@pytest.mark.parametrize('cpu,boot,t,want', [
    (61, 'boot-1', 12, 'BUDGET_EXHAUSTED'),
    (20, 'boot-2', 12, 'BUDGET_UNCERTAIN'),
    (20, 'boot-1', 9, 'BUDGET_UNCERTAIN'),
    (20, 'boot-1', 20_000_000_010, 'BUDGET_EXHAUSTED')])
def test_terminal_budget_facts_are_durable(tmp_path, cpu, boot, t, want):
    store = opened(tmp_path)
    start(store)
    store.settle_work(ATTEMPT, 'admission', observation(cpu=cpu, boot=boot, t=t))
    assert snap(store)['state'] == want
    with pytest.raises(ValueError): reserve(store)
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['state'] == want


@pytest.mark.parametrize('field,value', [('cpu_ns', True), ('memory_peak_bytes', -1),
    ('oom_events', False), ('work_id', 'other'), ('work_scope_id', 'wrong'),
    ('campaign_scope_id', 'wrong'), ('worker_cpu_ns', 1)])
def test_closed_attributed_observations_reject_without_changes(tmp_path, field, value):
    store = opened(tmp_path)
    start(store)
    before = store.budget_snapshot(ATTEMPT)
    obs = json.loads(observation())
    obs[field] = value
    with pytest.raises(ValueError): store.settle_work(ATTEMPT, 'admission', encoded(obs))
    assert store.budget_snapshot(ATTEMPT) == before


def test_outer_transaction_rollback_preserves_reservations(tmp_path):
    store = opened(tmp_path)
    before = store.budget_snapshot(ATTEMPT)
    with pytest.raises(RuntimeError):
        with store.store.transaction():
            reserve(store)
            raise RuntimeError('injected precommit failure')
    assert CampaignStore(ExecutionStore(store.store.path)).budget_snapshot(ATTEMPT) == before


def test_concurrent_reservation_uses_actual_sqlite_lock_and_revision(tmp_path):
    store = opened(tmp_path)
    revision = snap(store)['authority_revision']
    entered, release = Event(), Event()
    def first():
        with store.store.transaction():
            reserve(store)
            entered.set()
            assert release.wait(10)
    def second():
        other = CampaignStore(ExecutionStore(store.store.path))
        return other.reserve_work(ATTEMPT, 'n2', 'N2',
            encoded(dict(limits=profile()['phases']['N2'], clock=clock(11), input_sha256='e' * 64)),
            expected_revision=revision)
    with ThreadPoolExecutor(max_workers=2) as pool:
        a = pool.submit(first)
        assert entered.wait(10)
        b = pool.submit(second)
        release.set()
        a.result()
        with pytest.raises(ValueError): b.result()
    assert snap(store)['reserved_cpu_ns'] == 120


def test_dormant_campaign_cannot_acquire_budget(tmp_path, monkeypatch):
    from test_campaign_admission import running, message
    service, case = running(tmp_path, monkeypatch)
    raw = message(case)
    before = service.handle_request(1001, raw)
    store = CampaignStore(service.store)
    with pytest.raises(ValueError): store.begin_admission(raw, encoded(profile()), encoded(clock()))
    assert service.handle_request(1001, raw) == before


def test_shared_cap_covers_multiple_stages_and_outstanding_reservations(tmp_path):
    p = profile()
    for limits in p['phases'].values(): limits['cpu_ns'] = 60_000_000
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    store.begin_admission(request(), encoded(p), encoded(clock()))
    start(store)
    store.settle_work(ATTEMPT, 'admission', observation(cpu=20_000_000))
    store.bind_budget(ATTEMPT, contract_budget(), expected_revision=snap(store)['authority_revision'])
    for i in range(16):
        phase = 'N1' if i == 0 else 'N2_G5'
        store.reserve_work(ATTEMPT, 'work-' + str(i), phase,
            encoded(dict(limits=p['phases'][phase], clock=clock(12), input_sha256='d' * 64)),
            expected_revision=snap(store)['authority_revision'])
    assert snap(store)['remaining_cpu_ns'] == 20_000_000
    assert snap(store)['reserved_cpu_ns'] == 960_000_000
    store.reserve_work(ATTEMPT, 'one-too-many', 'N2_G5',
        encoded(dict(limits=p['phases']['N2_G5'], clock=clock(13), input_sha256='d' * 64)),
        expected_revision=snap(store)['authority_revision'])
    result = snap(store)
    assert result['state'] == 'BUDGET_EXHAUSTED'
    assert len(result['works']) == 17


@pytest.mark.parametrize('field,value,want', [('memory_peak_bytes', 101, 'BUDGET_EXHAUSTED'),
    ('oom_events', 1, 'BUDGET_EXHAUSTED'), ('memory_peak_bytes', None, 'BUDGET_UNCERTAIN')])
def test_common_memory_and_oom_are_fail_closed(tmp_path, field, value, want):
    store = opened(tmp_path)
    start(store)
    obs = json.loads(observation())
    obs[field] = value
    store.settle_work(ATTEMPT, 'admission', encoded(obs))
    assert snap(store)['state'] == want
    assert snap(CampaignStore(ExecutionStore(store.store.path)))['state'] == want


def test_invalid_profile_cannot_create_provisional_identity(tmp_path):
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    p = profile()
    del p['phases']['SEAL']
    with pytest.raises(ValueError): store.begin_admission(request(), encoded(p), encoded(clock()))
    with pytest.raises(KeyError): store.row(ATTEMPT)


def test_private_snapshot_rejects_invalid_nested_limits(tmp_path):
    from c1_rail.qualification.journal_snapshot import parse_campaign_budget_snapshot
    store = opened(tmp_path)
    value = snap(store)
    value['works'][0]['limits']['cpu_ns'] = True
    with pytest.raises(ValueError): parse_campaign_budget_snapshot(encoded(value))


# --- S2-G4: store-side invariants (A2 credit window, A9-3 work identities) ----


def test_settled_work_cannot_acquire_credit_after_its_observation(tmp_path):
    """S2-G4 A2: settlement closes the credit window. CAPTURED and SIGNING_INTENT
    on a work that already carries a settled observation, and COMPLETED without
    credit established before it, are refused by the store independently of the
    guardian (the admission and a linked signing retry keep their capture-less
    productions)."""
    store = opened(tmp_path)
    reserve(store, 'n1')
    start(store, 'n1')
    transition(store, 'n1', 'RUNNING')
    store.settle_work(ATTEMPT, 'n1', observation('n1', 5))
    with pytest.raises(ValueError, match='settled work cannot acquire credit'):
        transition(store, 'n1', 'CAPTURED', 15)
    with pytest.raises(ValueError, match='settled work cannot acquire credit'):
        transition(store, 'n1', 'SIGNING_INTENT', 15, dict(intent_id='i-1',
            payload_bytes_b64='eA==', key_id='key', signing_at_utc='2026-09-20T00:00:00Z'))
    with pytest.raises(ValueError, match='completion requires credit'):
        transition(store, 'n1', 'COMPLETED', 16)
    settled = next(w for w in snap(store)['works'] if w['work_id'] == 'n1')
    assert settled['state'] == 'RUNNING' and settled['observation_bytes_b64'] is not None
    # A work that never settled is not completed from RUNNING either: credit
    # (CAPTURED/SIGNED) must be established first.
    reserve(store, 'n2', 'N2')
    start(store, 'n2')
    transition(store, 'n2', 'RUNNING')
    with pytest.raises(ValueError, match='completion requires credit'):
        transition(store, 'n2', 'COMPLETED', 17)
    assert next(w for w in snap(store)['works'] if w['work_id'] == 'n2')['state'] == 'RUNNING'


@pytest.mark.parametrize('work_id', ['control_probe', 'event_probe', 'admission'])
def test_reserve_work_refuses_identities_that_collide_with_object_roles(tmp_path, work_id):
    """S2-G4 A9-3: 'supervision_' + work_id shares its namespace with the
    GLOB-queried 'supervision_control_*' / 'supervision_event_*' roles, and the
    service reserves the fixed 'admission' identity through begin_admission
    alone; every other producer is refused at this entry."""
    store = opened(tmp_path)
    with pytest.raises(ValueError, match='supervision object role|fixed work identity'):
        reserve(store, work_id)
    assert all(w['work_id'] != work_id for w in snap(store)['works'])
