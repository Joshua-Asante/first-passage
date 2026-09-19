"""R2b private scheduling through the warm service: real SQLite, simulated clocks/OS adapters.

Recovered byte-for-byte from commit 1ef91be (SHA-256 a49c7cd7...) and adapted to
the accepted R2a interface: the proposed ``prepare_scheduled_work`` became the
service route ``handle_request(service_uid, request)`` -> ``claim_scheduler_bootstrap``
-> ``materialize_scheduler_bootstrap`` -> ``launch_prepared_campaign_work``;
``parse_schedule_request`` is ``campaign_funding.parse_request``;
``scoped_boottime_deadline`` is ``owned_boottime_deadline``. Original assertions are
kept; where R2a made a pre-funding fact compact (terminal overlay, pending intent)
the compact projection is asserted instead. No Linux enforcement is claimed here.
"""
import base64
import json
import sys
import threading
from contextlib import nullcontext
from types import SimpleNamespace

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_funding as funding
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.service import ExecutionService
from c1_rail.qualification.execution.store import ExecutionStore
from scheduler_fixture import schedule
from test_campaign_budget import ATTEMPT, NOW, clock, snap, start, profile, request, contract_budget
from test_campaign_funding import enrolled

SERVICE_UID = 123


def work(state, work_id):
    return next(w for w in state['works'] if w['work_id'] == work_id)


class Timers:
    """Fake kernel timer ABI: every armed absolute deadline must be retired."""
    def __init__(self):
        self.armed = []
        self.retired = []

    def arm(self, deadline):
        self.armed.append(deadline)
        return SimpleNamespace(timer_delete=lambda timer: self.retired.append(timer) or 0), deadline


class Runtime:
    """Records construction; asserts the funded intent is durable before it."""
    constructed = []

    def __init__(self, context):
        state = CampaignStore(context.store).budget_snapshot(ATTEMPT)
        pending = [w for w in json.loads(state)['works'] if w['state'] == 'START_INTENT' and w['work_id'] != 'admission']
        assert len(pending) == 1, 'construction before one durable start intent'
        Runtime.constructed.append(pending[0]['work_id'])

    def start(self, state, work, enrollment):
        pass


def warm(store, monkeypatch, *, runtime=Runtime, t=11, eligible=True):
    """The already-running installed service; nothing is constructed per request."""
    Runtime.constructed = []
    service = object.__new__(ExecutionService)
    service.store = store.store
    service.config = {'host_run_id': 'host1', 'service_uid': SERVICE_UID}
    service.profile = SimpleNamespace(values={'schema': 'qualification_execution_profile/v4'})
    service.dispatch_lock = threading.Lock()
    service.recovery_issues = {}
    service.schedule_eligible = eligible
    timers = Timers()
    monkeypatch.setattr(supervisor, 'controller_cpu_guard', nullcontext)
    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(t)))
    monkeypatch.setattr(supervisor, 'arm_boottime_deadline', timers.arm)
    monkeypatch.setattr(supervisor, 'LinuxCampaignRuntime', runtime)
    service.timers = timers
    return service


def submit(service, raw=None):
    return json.loads(service.handle_request(SERVICE_UID, raw or schedule()))


def test_intent_reservation_and_one_use_owner_precede_construction_and_survive_reopen(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    prepared = submit(service)
    assert prepared['schema'] == 'qualification_campaign_status/v2'
    assert Runtime.constructed == ['worker']
    assert work(snap(store), 'worker')['state'] == 'START_INTENT'
    assert snap(store)['reserved_cpu_ns'] == 120
    with store.store.transaction() as c:
        row = c.execute('SELECT request_bytes, body FROM full_campaign_bootstraps WHERE attempt_id=? AND work_id=?', (ATTEMPT, 'worker')).fetchone()
    assert bytes(row[0]) == schedule() and json.loads(row[1])['state'] == 'MATERIALIZED'
    objects = store.objects(ATTEMPT)
    assert any(json.loads(raw).get('data', {}).get('slot') == 'START_OWNER' and json.loads(raw)['work_id'] == 'worker'
               for raw in objects.values())
    assert service.timers.armed == service.timers.retired and len(service.timers.armed) == 1
    reopened = CampaignStore(ExecutionStore(store.store.path))
    service.store = reopened.store
    duplicate = submit(service)
    assert duplicate['schema'] == 'qualification_campaign_scheduler_status/v1' and duplicate['historical'] is True
    assert Runtime.constructed == ['worker']
    assert len(service.timers.armed) == 1
    assert snap(reopened)['reserved_cpu_ns'] == 120
    assert snap(reopened)['start_clock'] == snap(store)['start_clock']


@pytest.mark.parametrize('change', [{'probe': 'cpu'}, {'role': 'probe_g5'}, {'signing_retry_of': 'other'}])
def test_nonidentical_request_cannot_reuse_work_identity(tmp_path, monkeypatch, change):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    submit(service)
    before = store.budget_snapshot(ATTEMPT)
    with pytest.raises(ValueError, match='identity conflict'):
        submit(service, schedule(**change))
    assert store.budget_snapshot(ATTEMPT) == before
    assert Runtime.constructed == ['worker']


def test_failed_commit_leaves_no_partially_funded_owner(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    before = store.budget_snapshot(ATTEMPT)
    original = funding._put
    def failed(connection, table, *args, **kwargs):
        original(connection, table, *args, **kwargs)
        if table == 'full_campaign_funding':
            raise RuntimeError('crash before outer commit')
    monkeypatch.setattr(funding, '_put', failed)
    with pytest.raises(RuntimeError, match='crash'):
        submit(service)
    assert store.budget_snapshot(ATTEMPT) == before
    with store.store.transaction() as c:
        assert c.execute('SELECT count(*) FROM full_campaign_bootstraps').fetchone()[0] == 0
    assert not json.loads(store.scheduler_status(ATTEMPT))['pending']
    assert Runtime.constructed == [] and service.timers.armed == []
    monkeypatch.setattr(funding, '_put', original)
    assert submit(service)['schema'] == 'qualification_campaign_status/v2'
    assert Runtime.constructed == ['worker']


def test_crash_after_materialization_keeps_intent_and_duplicate_historical(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    monkeypatch.setattr(supervisor, 'launch_prepared_campaign_work', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('crash after commit')))
    with pytest.raises(RuntimeError, match='crash after commit'):
        submit(service)
    reopened = CampaignStore(ExecutionStore(store.store.path))
    assert work(snap(reopened), 'worker')['state'] == 'START_INTENT'
    assert snap(reopened)['reserved_cpu_ns'] == 120
    assert not json.loads(reopened.scheduler_status(ATTEMPT))['pending']
    service.store = reopened.store
    assert submit(service)['schema'] == 'qualification_campaign_scheduler_status/v1'
    assert Runtime.constructed == []
    # Positive authority obeys the R1 barriers: the interrupted intent settles
    # only through bounded recovery, which then bars every further claim.
    reservation = base64.b64decode(work(snap(reopened), 'worker')['reservation_bytes_b64'])
    class Observed:
        def observation(self, state, w, enrollment):
            return encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=ATTEMPT, work_id='worker',
                clock=clock(12), campaign_scope_id=enrollment['scopes']['campaign_slice'],
                work_scope_id=enrollment['scopes']['payload_slice'], cpu_ns=None, memory_peak_bytes=None,
                oom_events=None, termination_known=False, orchestration_charge_cpu_ns=10))
        def cleanup(self, enrollment):
            pass
    context = SimpleNamespace(store=reopened.store, campaign_runtime=Observed(), recovery_issues={})
    supervisor.recover_campaign_work(context, reservation, attempt_id=ATTEMPT, work_id='worker')
    assert work(snap(reopened), 'worker')['state'] == 'IN_DOUBT'
    refused = submit(service, schedule(work_id='another'))
    assert refused['schema'] == 'qualification_campaign_scheduler_status/v1' and refused['state'] == 'BUDGET_UNCERTAIN'
    assert Runtime.constructed == []


def test_expiry_discovery_commits_without_preparation(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    deadline = snap(store)['deadline_boottime_ns']
    service = warm(store, monkeypatch, t=deadline)
    status = submit(service)
    assert status['schema'] == 'qualification_campaign_scheduler_status/v1'
    assert status['state'] == 'BUDGET_EXHAUSTED' and not status['pending']
    assert Runtime.constructed == [] and service.timers.armed == []
    with store.store.transaction() as c:
        assert not any(w['work_id'] == 'worker' for w in store._budget(c, ATTEMPT)['works'])
        assert c.execute('SELECT count(*) FROM full_campaign_bootstraps').fetchone()[0] == 0
    reopened = CampaignStore(ExecutionStore(store.store.path))
    assert json.loads(reopened.scheduler_status(ATTEMPT)) == status
    assert submit(service) == status


def _recovery_pending(store):
    store.claim_supervision_control(ATTEMPT, 'admission', 'RECOVERY_OWNER', encoded(clock(11)), recovery_owner_token=b'r' * 32)


def _void(store):
    store.void(encoded(dict(schema='qualification_campaign_request/v1', operation='VOID', attempt_id=ATTEMPT,
                            reason='stop', operator_approval_bytes='eA==')), now=NOW)


def _exhausted(tmp_path):
    config = profile()
    config.update(schema='qualification_campaign_budget_profile/v3', funding_intents='qualification_campaign_funding/v1',
                  orchestration_cpu_ns={p: 10 for p in config['phases']})
    for limit in config['phases'].values():
        limit['cpu_ns'] = 80_000_000
    store = CampaignStore(ExecutionStore(tmp_path / 'journal.sqlite'))
    store.begin_admission(request(), encoded(config), encoded(clock()))
    store.bind_budget(ATTEMPT, contract_budget(), expected_revision=snap(store)['authority_revision'])
    for index in range(11):
        store.reserve_work(ATTEMPT, 'g5-' + str(index), 'N1_G5', encoded(dict(limits=config['phases']['N1_G5'],
            clock=clock(11), input_sha256='d' * 64)), expected_revision=snap(store)['authority_revision'])
    assert snap(store)['remaining_cpu_ns'] < 80_000_000
    return store


@pytest.mark.parametrize('case', ['changed_boot', 'backward_clock', 'insufficient_cpu', 'void', 'recovery_pending', 'dispatch_pending'])
def test_refusals_precede_construction_and_lifecycle_effects(tmp_path, monkeypatch, case):
    store = _exhausted(tmp_path) if case == 'insufficient_cpu' else enrolled(tmp_path)
    t = 9 if case == 'backward_clock' else 11
    service = warm(store, monkeypatch, t=t)
    if case == 'changed_boot':
        monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: encoded(clock(11, boot='boot-2')))
    elif case == 'void':
        _void(store)
    elif case == 'recovery_pending':
        _recovery_pending(store)
    gate = nullcontext()
    if case == 'dispatch_pending':
        start(store)
        gate = store.launch_gate(ATTEMPT, 'admission', lambda: encoded(clock(11)))
    with gate:
        if case in ('recovery_pending', 'dispatch_pending'):
            with pytest.raises(ValueError, match='pending'):
                submit(service)
        else:
            status = submit(service)
            assert status['schema'] == 'qualification_campaign_scheduler_status/v1' and not status['pending']
            assert status['state'] == {'changed_boot': 'BUDGET_UNCERTAIN', 'backward_clock': 'BUDGET_UNCERTAIN',
                                       'insufficient_cpu': 'BUDGET_EXHAUSTED', 'void': 'BOUND'}[case]
            assert status['validity'] == ('VOID' if case == 'void' else 'VALID')
    assert Runtime.constructed == [] and service.timers.armed == []
    with store.store.transaction() as c:
        assert c.execute('SELECT count(*) FROM full_campaign_bootstraps').fetchone()[0] == 0
        assert not any(w['work_id'] == 'worker' for w in store._budget(c, ATTEMPT)['works'])
    ExecutionStore(store.store.path)


def test_repeated_runtime_construction_failure_gets_one_funded_tail(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    calls = []
    def fail(context):
        w = work(snap(store), 'worker')
        assert w['state'] == 'START_INTENT'
        calls.append(w['work_id'])
        raise ValueError('construction failed')
    service = warm(store, monkeypatch, runtime=fail)
    # Unknown construction prevents observation: retain R1 recovery barrier.
    monkeypatch.setattr(supervisor, 'recover_campaign_work', lambda *a, **kw: None)
    with pytest.raises(ValueError, match='construction failed'):
        submit(service)
    assert submit(service)['historical'] is True
    assert calls == ['worker']
    assert snap(store)['reserved_cpu_ns'] == 120
    assert work(snap(store), 'worker')['state'] == 'START_INTENT'
    assert service.timers.armed == service.timers.retired and len(service.timers.armed) == 1
    reopened = CampaignStore(ExecutionStore(store.store.path))
    service.store = reopened.store
    assert submit(service)['historical'] is True
    assert calls == ['worker'] and snap(reopened)['reserved_cpu_ns'] == 120


def test_concurrent_identical_requests_fund_one_producer_and_one_tail(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    barrier = Barrier(2)
    def contender():
        barrier.wait()
        return submit(service)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: contender(), range(2)))
    schemas = sorted(result['schema'] for result in results)
    assert schemas == ['qualification_campaign_scheduler_status/v1', 'qualification_campaign_status/v2']
    assert Runtime.constructed == ['worker']
    assert len(service.timers.armed) == 1 and service.timers.armed == service.timers.retired
    with store.store.transaction() as c:
        assert c.execute('SELECT count(*) FROM full_campaign_bootstraps').fetchone()[0] == 1
    from c1_rail.qualification.execution.protocol import sha256
    owner = 'supervision_control_' + sha256(encoded(['worker', 'START_OWNER']))
    assert sum(role == owner for role in store.objects(ATTEMPT)) == 1
    assert snap(store)['reserved_cpu_ns'] == 120


@pytest.mark.parametrize('peer', [0, 124])
def test_private_schedule_rejects_other_peers_before_store_access(peer):
    service = object.__new__(ExecutionService)
    service.config = {'service_uid': SERVICE_UID}
    with pytest.raises(ValueError, match='PEER_NOT_AUTHORIZED'):
        service.handle_request(peer, schedule())


def test_private_schedule_requires_execution_capable_release_before_store_access(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch, eligible=False)
    service.store = None
    with pytest.raises(ValueError, match='execution-capable'):
        submit(service)
    assert Runtime.constructed == []


@pytest.mark.parametrize('change', [{'extra': 'x'}, {'role': 'admission'}, {'probe': 'unknown'}, {'work_id': ''},
                                    {'signing_retry_of': False}, {'work_id': 'w' * 1100}])
def test_closed_private_request_validation(change):
    with pytest.raises(ValueError):
        funding.parse_request(schedule(**change))


def test_first_request_performs_no_campaign_import(tmp_path, monkeypatch):
    """Every campaign-specific module is loaded at service startup, never on a first request."""
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    class NoFirstRequestImport:
        def find_spec(self, name, path=None, target=None):
            raise ImportError('first-request import: ' + name)
    monkeypatch.setattr(sys, 'meta_path', [NoFirstRequestImport(), *sys.meta_path])
    import importlib
    with pytest.raises(ImportError, match='first-request import'):
        importlib.import_module('r2b_never_loaded_module')
    assert submit(service)['schema'] == 'qualification_campaign_status/v2'
    assert submit(service)['historical'] is True
    assert Runtime.constructed == ['worker']


def test_shared_service_absolute_timer_is_retired_on_failure(monkeypatch):
    retired = []
    libc = SimpleNamespace(timer_delete=lambda timer: retired.append(timer) or 0)
    monkeypatch.setattr(supervisor, 'arm_boottime_deadline', lambda deadline: (libc, deadline))
    with pytest.raises(RuntimeError):
        with supervisor.owned_boottime_deadline(77):
            raise RuntimeError('failed')
    assert retired == [77]


def test_owned_timer_leaves_nothing_after_success_and_historical_duplicate(tmp_path, monkeypatch):
    retired = []
    libc = SimpleNamespace(timer_delete=lambda timer: retired.append(timer) or 0)
    monkeypatch.setattr(supervisor, 'arm_boottime_deadline', lambda deadline: (libc, deadline))
    with supervisor.owned_boottime_deadline(78):
        pass
    assert retired == [78]
    failing = SimpleNamespace(timer_delete=lambda timer: 1)
    monkeypatch.setattr(supervisor, 'arm_boottime_deadline', lambda deadline: (failing, deadline))
    with pytest.raises(OSError, match='retirement'):
        with supervisor.owned_boottime_deadline(79):
            pass
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    submit(service)
    armed = list(service.timers.armed)
    assert submit(service)['historical'] is True
    assert service.timers.armed == armed and service.timers.retired == armed


def test_launch_tail_consumes_only_a_materialized_intent(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    token, _ = store.claim_scheduler_bootstrap(schedule(), encoded(clock(11)))
    reservation, enrollment = store.materialize_scheduler_bootstrap(ATTEMPT, 'worker', token, 'host1')
    with pytest.raises(ValueError, match='reservation identity'):
        supervisor.launch_prepared_campaign_work(service, reservation + b' ', enrollment)
    assert Runtime.constructed == []
    supervisor.launch_prepared_campaign_work(service, reservation, enrollment)
    assert Runtime.constructed == ['worker']
    assert service.timers.armed == service.timers.retired == [min(snap(store)['deadline_boottime_ns'], 11 + 10**9)]
    objects = store.objects(ATTEMPT)
    from c1_rail.qualification.execution.protocol import sha256
    assert sum(role == 'supervision_control_' + sha256(encoded(['worker', 'START_OWNER'])) for role in objects) == 1


class Observed:
    """Simulated recovery adapter: a terminated payload with known counters."""
    def __init__(self):
        self.cleaned = []

    def observation(self, state, w, enrollment):
        return encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=ATTEMPT, work_id=w['work_id'],
            clock=clock(12), campaign_scope_id=enrollment['scopes']['campaign_slice'],
            work_scope_id=enrollment['scopes']['payload_slice'], cpu_ns=20, memory_peak_bytes=50,
            oom_events=0, termination_known=True, orchestration_charge_cpu_ns=10))

    def cleanup(self, enrollment):
        self.cleaned.append(enrollment['work_id'])


def test_restart_auto_recovers_interrupted_funded_work_and_never_materializes(tmp_path, monkeypatch):
    """Operator ruling 2026-09-19: funded work interrupted by a restart is recovered, not left for manual disposition."""
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    monkeypatch.setattr(supervisor, 'launch_prepared_campaign_work', lambda *a, **k: (_ for _ in ()).throw(RuntimeError('crash after commit')))
    with pytest.raises(RuntimeError):
        submit(service)
    assert work(snap(store), 'worker')['state'] == 'START_INTENT'
    service.campaign_runtime = Observed()
    service.store = ExecutionStore(store.store.path)
    service.recover_service()
    reopened = CampaignStore(ExecutionStore(store.store.path))
    assert service.campaign_runtime.cleaned == ['worker']
    assert not any(value == 'RECOVERY_PENDING' for value in service.recovery_issues.values())
    assert work(snap(reopened), 'worker')['state'] == 'IN_DOUBT'
    assert snap(reopened)['state'] == 'IN_DOUBT'
    assert work(snap(reopened), 'worker')['charge_cpu_ns'] == 30  # measured 20 + installed orchestration bound 10
    assert Runtime.constructed == []
    # No redraw: a later claim is refused historically, exactly as after in-process recovery.
    service.store = reopened.store
    assert submit(service, schedule(work_id='another'))['schema'] == 'qualification_campaign_scheduler_status/v1'
    assert Runtime.constructed == []


def test_restart_reports_pending_intent_and_leaves_it_unmaterialized(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    token, _ = store.claim_scheduler_bootstrap(schedule(), encoded(clock(11)))
    service.campaign_runtime = Observed()
    service.recover_service()
    assert service.recovery_issues[ATTEMPT + ':funding'] == 'FUNDING_PENDING'
    assert json.loads(store.scheduler_status(ATTEMPT))['pending']
    with store.store.transaction() as c:
        assert json.loads(c.execute('SELECT body FROM full_campaign_bootstraps').fetchone()[0])['state'] == 'PENDING'
        assert [w['work_id'] for w in store._budget(c, ATTEMPT)['works']] == ['admission']
    assert service.campaign_runtime.cleaned == [] and Runtime.constructed == []
    with pytest.raises(ValueError, match='funding'):
        store.budget_snapshot(ATTEMPT)
    ExecutionStore(store.store.path)


def test_persistence_only_installation_still_resumes_nothing(tmp_path, monkeypatch):
    store = enrolled(tmp_path)
    service = warm(store, monkeypatch)
    service.profile = SimpleNamespace(values={'schema': 'qualification_execution_profile/v3'})
    service.campaign_runtime = Observed()
    service.recover_service()
    assert service.recovery_issues == {ATTEMPT + ':funding': 'FUNDING_RUNTIME_NOT_ENABLED'}
    assert service.campaign_runtime.cleaned == []


def test_transport_child_moves_one_bounded_frame_without_campaign_imports(monkeypatch):
    import importlib.util
    import socket
    from pathlib import Path
    from c1_rail.qualification.execution.protocol import encode_frame
    from c1_rail.qualification.execution.transport import receive
    path = Path(__file__).resolve().parents[4] / 'tests/integration/qualification_boundary/private_route.py'
    spec = importlib.util.spec_from_file_location('private_route', path)
    route = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(route)
    frame = route.schedule_frame(json.loads(schedule()))
    assert frame[4:] == schedule() and len(frame) <= route.FRAME_LIMIT + 4
    with pytest.raises(ValueError):
        route.schedule_frame(dict(schema='qualification_campaign_request/v2', operation='STATUS', attempt_id=ATTEMPT))
    with pytest.raises(ValueError):
        route.schedule_frame(json.loads(schedule(work_id='w' * 1100)))
    reply = encoded(dict(ok=True, data_b64=''))
    client, server = socket.socketpair()
    def serve():
        with server:
            server.settimeout(10)
            received = receive(server, limit=route.FRAME_LIMIT)
            assert received == schedule()
            server.sendall(encode_frame(reply, limit=route.REPLY_LIMIT))
    worker = threading.Thread(target=serve)
    worker.start()
    with client:
        assert route.exchange(client, frame, timeout=10) == reply
    worker.join(10)
    with pytest.raises(ValueError):
        route.exchange(client, b'x' * 2000, timeout=1)
    source = path.read_text(encoding='utf-8')
    assert 'campaign_store' not in source and 'campaign_supervisor' not in source and 'campaign_funding' not in source
