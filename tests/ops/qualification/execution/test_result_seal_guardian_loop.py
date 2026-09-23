"""The guardian loops of the RESULT and SEAL units supervise to the unit's exit.

``run_result_g5`` and ``run_seal_unit`` were copied from S3's ``_run_n1_g5``
with its per-iteration ``_assert_authority``, which admits only PROVISIONAL and
BOUND. RESULT and SEAL work runs from the statistical state its commit rides
(``COMMIT_PREDECESSOR_STATES``; SEAL from the committed PASS outcome), so that
check refused the phase's own live state on the first iteration, before any
unit ran to completion. Once the commit state enum lands, the commit can also
move the snapshot to RESULT_COMMITTED_*/SEALED_PASS while the unit is still
returning; as in #461, that ends identity supervision but not the wait for the
unit to leave its cgroup (a populated slice has no final CPU sample).

The fakes stand in for the store, the Linux runtime and the unit bus; the
kernel is reduced to the unit cgroup's ``cgroup.events`` file.
"""
import base64
import json
from contextlib import contextmanager
from pathlib import PurePosixPath
from types import SimpleNamespace

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_result, campaign_seal
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution import runtime

LINUX_INTERPRETER = '/opt/ops/bin/python'
LINUX_CODE_ROOT = '/opt/qualification'
PAYLOAD_SLICE = 'fpq-camp-work.slice'
START_NS = 10**12
WALL_NS = 60 * 10**9


class Kernel:
    """Wall time and the unit cgroup. The unit commits after ``commit_after``
    sleeps and exits after ``exit_after`` sleeps (``None``: never)."""

    def __init__(self, group, exit_after):
        self.now = START_NS
        self.sleeps = 0
        self.exit_after = exit_after
        self.group = group
        group.mkdir(parents=True)
        (group / 'cgroup.procs').write_text('')
        self.set_populated(1)
        self.on_sleep = []

    def set_populated(self, value):
        (self.group / 'cgroup.events').write_text(f'populated {value}\nfrozen 0\n')

    def populated(self):
        text = (self.group / 'cgroup.events').read_text()
        return int(text.split('populated ')[1].split()[0])

    def clock(self):
        return encoded({'schema': 'qualification_campaign_clock/v1', 'boot_id': 'boot0',
                        'boottime_ns': self.now, 'utc': '2026-09-23T00:00:00Z'})

    def sleep(self, seconds):
        self.sleeps += 1
        self.now += int(seconds * 10**9)
        for hook in self.on_sleep:
            hook(self.sleeps)
        if self.exit_after is not None and self.sleeps >= self.exit_after:
            self.set_populated(0)


class Campaigns:
    def __init__(self):
        self.store = SimpleNamespace(transaction=self._transaction)

    @contextmanager
    def _transaction(self):
        yield None

    @contextmanager
    def launch_gate(self, attempt_id, work_id, clock, role):
        yield {'token': 'tok'}

    def acknowledge_dispatch(self, *args):
        pass

    @staticmethod
    def _raw(value):
        return base64.b64decode(value)

    @staticmethod
    def _work(state, work_id):
        return {'work_id': work_id, 'phase': state['phase'], 'state': 'SIGNED'}


def fake_store(base, family):
    """A ResultStore/SealStore stand-in whose campaign state the test drives."""

    class Store:
        state_name = None
        settled = []
        transitions = []

        def __init__(self, campaigns):
            self.campaigns = campaigns

        def _state(self):
            return {'attempt_id': 'att1', 'state': Store.state_name, 'validity': 'VALID',
                    'authority_revision': 7, 'last_clock': {}, 'works': [],
                    'phase': Store.phase}

        def result_state_bytes(self, attempt_id):
            return encoded(self._state())

        def retain_result_supervision_event(self, raw):
            pass

        def settle_result_work(self, attempt_id, work_id, observed):
            Store.settled.append(observed)
            return encoded(self._state())

        def record_result_transition(self, attempt_id, work_id, raw, expected_revision):
            Store.transitions.append(json.loads(raw)['state'])
            return encoded(self._state())

        _completion_states = base._completion_states
        _commit_progressions = base._commit_progressions

        def _result_family(self, connection, attempt_id):
            return {'state': family}

        def _seal_family(self, connection, attempt_id):
            return family

    return Store


def run(tmp_path, monkeypatch, *, phase, start, committed=None, commit_after=1, exit_after=3):
    parent = tmp_path / 'fpq.slice'
    suffix = '-result-g5.service' if phase == 'RESULT' else '-seal.service'
    group = parent / 'fpq-camp.slice' / PAYLOAD_SLICE / (PAYLOAD_SLICE[:-6] + suffix)
    kernel = Kernel(group, exit_after)
    observed_populated = []

    class Runtime:
        def __init__(self):
            self.parent = parent

        def observation(self, state, work, enrollment):
            observed_populated.append(kernel.populated())
            return b'{}'

    if phase == 'RESULT':
        store = fake_store(campaign_result.ResultStore, 'COMMITTED')
        monkeypatch.setattr(campaign_result, 'ResultStore', store)
        entry = campaign_result.run_result_g5
    else:
        store = fake_store(campaign_seal.SealStore, 'SEALED')
        monkeypatch.setattr(campaign_seal, 'SealStore', store)
        entry = campaign_seal.run_seal_unit
    store.state_name, store.phase = start, phase
    store.settled, store.transitions = [], []
    if committed is not None:
        def commit(sleeps):
            if sleeps == commit_after:
                store.state_name = committed
        kernel.on_sleep.append(commit)

    monkeypatch.setattr(supervisor, 'observe_campaign_clock', kernel.clock)
    monkeypatch.setattr(supervisor.time, 'sleep', kernel.sleep)
    monkeypatch.setattr(supervisor, '_guardian_bus_call', lambda *a: None)
    monkeypatch.setattr(supervisor.sys, 'executable', LINUX_INTERPRETER)
    monkeypatch.setattr(runtime, 'installed_code_root', lambda: PurePosixPath(LINUX_CODE_ROOT))
    reservation = base64.b64encode(encoded({'clock': json.loads(kernel.clock())})).decode()
    state = {'attempt_id': 'att1', 'deadline_boottime_ns': START_NS + WALL_NS,
             'profile': {'orchestration_cpu_ns': {phase: 10**9}}}
    work = {'work_id': 'w1', 'phase': phase, 'reservation_bytes_b64': reservation,
            'limits': {'cpu_ns': 30 * 10**9, 'wall_ns': WALL_NS}}
    enrollment = {'scopes': {'payload_slice': PAYLOAD_SLICE,
                             'guardian_unit': 'fpq-guardian.service'}}
    context = SimpleNamespace(config={'g5_uid': 1234, 'seal_probe_uid': 1235})
    entry(context, Campaigns(), Runtime(), state, work, enrollment, manifest={})
    return kernel, store, observed_populated


@pytest.mark.parametrize('start', campaign_result.COMMIT_PREDECESSOR_STATES)
def test_result_unit_is_supervised_from_its_statistical_predecessor(
        tmp_path, monkeypatch, start):
    # Frozen bytes: the commit leaves the snapshot on its predecessor.
    kernel, store, observed = run(tmp_path, monkeypatch, phase='RESULT', start=start)
    assert observed == [0]
    assert store.settled == [b'{}']
    assert store.transitions == ['COMPLETED']
    assert kernel.sleeps == 3


def test_seal_unit_is_supervised_from_the_committed_pass(tmp_path, monkeypatch):
    kernel, store, observed = run(tmp_path, monkeypatch, phase='SEAL',
                                  start=campaign_result.SEAL_ELIGIBLE_STATE)
    assert observed == [0]
    assert store.settled == [b'{}']
    assert kernel.sleeps == 3


@pytest.mark.parametrize('phase,start,committed', [
    ('RESULT', 'FULL_PASS_READY', 'RESULT_COMMITTED_PASS'),
    ('RESULT', 'N2_FAILED', 'RESULT_COMMITTED_FAIL'),
    ('SEAL', 'RESULT_COMMITTED_PASS', 'SEALED_PASS'),
])
def test_commit_while_the_unit_runs_settles_only_after_the_cgroup_empties(
        tmp_path, monkeypatch, phase, start, committed):
    # Post-seam: the commit moves the snapshot while the driver still returns.
    kernel, store, observed = run(tmp_path, monkeypatch, phase=phase, start=start,
                                  committed=committed, commit_after=1, exit_after=3)
    assert observed == [0], 'the settlement observation sampled a still-populated unit'
    assert store.settled == [b'{}']
    assert kernel.sleeps == 3


def test_a_committed_unit_that_never_exits_is_observed_at_the_bound(tmp_path, monkeypatch):
    kernel, store, observed = run(tmp_path, monkeypatch, phase='RESULT',
                                  start='FULL_PASS_READY', committed='RESULT_COMMITTED_PASS',
                                  exit_after=None)
    assert observed == [1]
    assert kernel.now >= START_NS + WALL_NS + campaign_result.UNIT_STOP_GRACE_NS
    assert kernel.now < START_NS + WALL_NS + campaign_result.UNIT_STOP_GRACE_NS + 10**9


@pytest.mark.parametrize('phase,start', [('RESULT', 'BUDGET_UNCERTAIN'), ('SEAL', 'ABORTED')])
def test_an_authority_ended_campaign_still_stops_supervision(
        tmp_path, monkeypatch, phase, start):
    with pytest.raises(ValueError, match='terminal or invalidated'):
        run(tmp_path, monkeypatch, phase=phase, start=start)
