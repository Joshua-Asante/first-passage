"""S5 io-mount release (fix card 2026-09-30, amendments A1/A2).

Each work's checkpoint io tmpfs pair is bound to the work's guardian unit
(``BindsTo`` + ``After``), so the system manager stops the pair when that unit
ends. The guardian unit's main process is the guardian itself, so the unit
ends only after ``_run_n1_worker`` returns or raises into
``_guardian_self_failure`` -- after ``retain_checkpoint_capture`` on a
committed work and after ``_archive_part_a_for_inspection`` on an IN_DOUBT
one.

A fake system manager applies ``BindsTo`` the way systemd does: when a unit
ends, every active unit bound to it stops. A fake output mount serves bytes
only while its mount unit is active (an unmounted path has no files). The
guardian's end is simulated where the real unit ends: after
``_run_n1_worker`` returns, or after the guardian's own failure path.
"""

import inspect
from pathlib import Path
from types import SimpleNamespace

import pytest

from test_campaign_n2 import (
    FINAL,
    INITIAL,
    SERVICE_UID,
    WORKER_UID,
    _enrollment,
    _ExitDocker,
    _part_a_document,
    _run_g5_work,
    _WorkerCampaigns,
)
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution.protocol import sha256

MOUNT_KEYS = {'What', 'Where', 'Type', 'Options', 'DefaultDependencies'}
OUTPUT_LIMIT = 10**7


class _Manager:
    """The system manager's unit table, with BindsTo stop propagation."""

    def __init__(self, log):
        self.log = log
        self.units = {}
        self.live_after_start = []

    def start(self, campaigns, unit, properties):
        assert not self.active(unit), unit
        self.units[unit] = {'properties': dict(properties), 'active': True}
        self.log.append(('start', unit))
        self.live_after_start.append(len(self.live_mounts()))

    def unit_ends(self, unit):
        """``unit`` became inactive; systemd stops every unit bound to it."""
        self.log.append(('end', unit))
        if unit in self.units:
            self.units[unit]['active'] = False
        for name, row in self.units.items():
            if row['active'] and unit in row['properties'].get('BindsTo', ()):
                row['active'] = False
                self.log.append(('stop', name))

    def active(self, unit):
        return self.units.get(unit, {}).get('active', False)

    def live_mounts(self):
        return sorted(
            name for name, row in self.units.items() if row['active'] and name.endswith('.mount')
        )


class _Campaigns(_WorkerCampaigns):
    """The worker-supervision store surface for one work, logging each call in
    order into the shared log and tracking the work's own state."""

    def __init__(self, log, *, work_id, phase, progression, crash_on=None):
        super().__init__(progression)
        self.log = log
        self.work_id = work_id
        self.phase = phase
        self.crash_on = crash_on
        self.work_state = 'RUNNING'
        self.staged = []
        self.captures = []

    def state(self):
        state = super().state()
        state['profile'] = {'orchestration_cpu_ns': {self.phase: 20 * 10**9}}
        state['works'][0].update(work_id=self.work_id, phase=self.phase, state=self.work_state)
        return state

    def _crash(self, name):
        if self.crash_on == name:
            self.log.append(('crash', name))
            raise RuntimeError('injected crash in ' + name)

    def stage_checkpoint_artifact(self, attempt, role, raw, *, checkpoint='N1'):
        self.log.append(('stage', role))
        self.staged.append((checkpoint, role, raw))
        return sha256(raw)

    def retain_checkpoint_capture(self, *args, **kwargs):
        self.log.append(('retain_checkpoint_capture', self.work_id))
        self.captures.append(kwargs)
        self.work_state = 'CAPTURED'

    def retain_checkpoint_attestation(self, *args, **kwargs):
        self._crash('retain_checkpoint_attestation')
        self.log.append(('retain_checkpoint_attestation', self.work_id))

    def settle_work(self, attempt, work_id, observed):
        self.log.append(('settle', work_id))
        return super().settle_work(attempt, work_id, observed)

    def record_work_transition(self, attempt, work_id, raw, expected_revision):
        result = super().record_work_transition(attempt, work_id, raw, expected_revision)
        self.work_state = self.transitions[-1]
        self.log.append(('transition', self.transitions[-1]))
        return result


def _guardian(
    tmp_path, monkeypatch, manager, *, work_id, checkpoint, served, document,
    progression, exit_code=0, crash_on=None,
):
    """One guardian unit's life: ``_run_n1_worker`` inside it, the guardian's
    own failure path on a raise (campaign_guardian_main's except), then the
    unit ends because its main process ended."""
    from c1_rail.qualification.execution import files, protocol, signing

    log = manager.log
    enrollment = _enrollment(work_id)
    io = supervisor.checkpoint_io_paths(enrollment)
    payload_slice = enrollment['scopes']['payload_slice']
    body = {
        'Image': 'img',
        'User': str(WORKER_UID) + ':' + str(WORKER_UID),
        'Entrypoint': ['e'],
        'Cmd': ['c'],
        'HostConfig': {'CgroupParent': payload_slice, 'Binds': ['a:/input:ro']},
    }
    docker = _ExitDocker(body, exit_code=exit_code)
    clock_bytes = encoded(
        {
            'schema': 'qualification_campaign_clock/v1',
            'boot_id': 'b',
            'boottime_ns': 10**12,
            'utc': '2026-09-23T00:00:00Z',
        }
    )
    result = encoded(
        {
            'payload_sha256': 'p' * 64,
            'payload_byte_length': 7,
            'plan_sha256': 'q' * 64,
            'worker_image_digest': 'img',
            'runtime_manifest_sha256': 'r' * 64,
            'container_id': 'c' * 64,
        }
    )

    def read_regular(root, name, *, limit):
        # An unmounted path holds none of the tmpfs files.
        assert Path(root) == Path(io['out_path'])
        log.append(('read_out', name))
        if not manager.active(io['out_unit']) or name not in served:
            raise FileNotFoundError(name)
        return served[name]

    def write_input(enrollment_arg, files_arg):
        assert manager.active(io['in_unit'])
        log.append(('write_in', work_id))
        return 0

    def capture(*args, **kwargs):
        # The real capture reads the staged campaign limits from the input mount.
        assert manager.active(io['in_unit'])
        log.append(('read_in', 'campaign-limits.json'))
        return result, SimpleNamespace(document=document)

    monkeypatch.setattr(supervisor, 'observe_campaign_clock', lambda: clock_bytes)
    monkeypatch.setattr(supervisor, 'DockerControl', lambda: docker)
    monkeypatch.setattr(supervisor, '_worker_input_files', lambda *a, **k: ([], b'plan'))
    monkeypatch.setattr(supervisor, '_guardian_bus_call', manager.start)
    monkeypatch.setattr(supervisor, '_write_worker_input', write_input)
    monkeypatch.setattr(supervisor, 'worker_container_body', lambda *a, **k: body)
    monkeypatch.setattr(
        supervisor, '_process_cgroup', lambda pid='self': '/' + payload_slice + '/c'
    )
    monkeypatch.setattr(supervisor, '_payload_processes', lambda group: ['4242'])
    monkeypatch.setattr(
        supervisor,
        '_process_identity',
        lambda pid: (99, WORKER_UID, '/' + payload_slice + '/c', 'python3', '/x'),
    )
    monkeypatch.setattr(supervisor, '_pre_exec_init', lambda comm: False)
    monkeypatch.setattr(supervisor, '_interpreter_image', lambda *a: False)
    monkeypatch.setattr(
        supervisor,
        '_read_counter',
        lambda path: (b'usage_usec 0\n' if path.name == 'cpu.stat' else b'oom 0\noom_kill 0\n'),
    )
    monkeypatch.setattr(supervisor.time, 'sleep', lambda seconds: None)
    monkeypatch.setattr(files, 'read_regular', read_regular)
    monkeypatch.setattr(protocol, 'decode_frame', lambda raw, limit: b'payload')
    monkeypatch.setattr(supervisor, '_capture_result_document', capture)
    monkeypatch.setattr(signing, 'sign_checkpoint_attestation', lambda *a, **k: b'attestation')
    verified = SimpleNamespace(profile=SimpleNamespace(sha256='s' * 64))
    context = SimpleNamespace(
        profile=SimpleNamespace(output_byte_limit=OUTPUT_LIMIT, worker_uid=WORKER_UID),
        config={'execution_credential': 'cred', 'service_uid': SERVICE_UID},
        release=encoded({'service_id': 'svc'}),
        keys=lambda: {},
        _context=lambda digest, at: verified,
    )
    runtime = SimpleNamespace(
        parent=tmp_path / (payload_slice[:-6].split('-')[0] + '.slice'),
        observation=lambda *a: b'{}',
    )
    campaigns = _Campaigns(
        log, work_id=work_id, phase=checkpoint, progression=progression, crash_on=crash_on
    )
    state = campaigns.state()
    role = {'N1': 'n1_worker', 'N2': 'n2_worker', 'PART_A': 'part_a_worker'}[checkpoint]
    failure = None
    try:
        supervisor._run_n1_worker(
            context,
            campaigns,
            runtime,
            state,
            state['works'][0],
            enrollment,
            {'work_id': work_id, 'role': role},
            checkpoint=checkpoint,
        )
    except Exception as raised:  # campaign_guardian_main's own failure path
        failure = raised
        supervisor._guardian_self_failure(None, campaigns, enrollment, 'a1', work_id, raised)
    finally:
        in_flight = manager.live_mounts()
        manager.unit_ends(enrollment['scopes']['guardian_unit'])
    return SimpleNamespace(
        campaigns=campaigns, io=io, enrollment=enrollment, failure=failure, in_flight=in_flight,
    )


def _served(initial=INITIAL, final=FINAL, frame=b'frame'):
    served = {'result.frame': frame, 'part-a-initial.jsonl': initial, 'part-a-final.jsonl': final}
    return {name: raw for name, raw in served.items() if raw is not None}


def _assert_bound_pair(manager, run):
    """Each io mount unit carries exactly BindsTo/After on the work's guardian
    unit on top of the unchanged mount properties."""
    guardian = run.enrollment['scopes']['guardian_unit']
    pairs = ((run.io['in_unit'], run.io['in_path']), (run.io['out_unit'], run.io['out_path']))
    for unit, where in pairs:
        properties = manager.units[unit]['properties']
        assert set(properties) == MOUNT_KEYS | {'BindsTo', 'After'}, sorted(properties)
        assert properties['BindsTo'] == [guardian] and properties['After'] == [guardian]
        assert properties['Where'] == where
        assert (properties['What'], properties['Type']) == ('tmpfs', 'tmpfs')
        assert properties['DefaultDependencies'] is False
    assert manager.units[run.io['out_unit']]['properties']['Options'] == (
        'rw,size=%d,uid=%d,gid=%d,mode=0755' % (OUTPUT_LIMIT, WORKER_UID, WORKER_UID)
    )
    # Zero staged bytes (the harness stages none): the unchanged headroom formula.
    assert manager.units[run.io['in_unit']]['properties']['Options'] == (
        'rw,size=%d,uid=%d,gid=%d,mode=0755' % (65536, SERVICE_UID, SERVICE_UID)
    )


def test_io_pairs_are_bound_to_the_guardian_and_bounded_by_the_works_in_flight(
    tmp_path, monkeypatch
):
    """Test (1): across N1, N2 and Part A works in sequence plus one
    exact-receipt signing retry, every io mount unit starts bound to its
    work's guardian unit, the live pairs never exceed one per in-flight work,
    and none is live once every work has settled."""
    log = []
    manager = _Manager(log)
    runs = []
    for work_id, checkpoint, progression in (
        ('n1work', 'N1', 'BOUND'),
        ('n2work', 'N2', 'N2_READY'),
    ):
        run = _guardian(
            tmp_path, monkeypatch, manager, work_id=work_id, checkpoint=checkpoint,
            served={'result.frame': b'frame'}, document={'observations': {}},
            progression=progression,
        )
        assert run.failure is None and run.campaigns.transitions == ['COMPLETED']
        runs.append(run)
        assert manager.live_mounts() == []

    # The exact-receipt retry is a g5 work: its unit starts through the same
    # manager, bound to its own guardian, and it creates no io mount.
    class _RedirectBus:
        def __init__(self, inner):
            self.inner = inner

        def setattr(self, target, name, value, *rest):
            if target is supervisor and name == '_guardian_bus_call':
                value = manager.start
            return self.inner.setattr(target, name, value, *rest)

        def __getattr__(self, name):
            return getattr(self.inner, name)

    before = set(manager.units)
    _, _, commits, transitions = _run_g5_work(
        tmp_path, _RedirectBus(monkeypatch), progression='N2_READY', parent='n2g5'
    )
    assert transitions == ['COMPLETED'] and len(commits) == 1
    started = set(manager.units) - before
    assert started and not any(name.endswith('.mount') for name in started), started
    manager.unit_ends('fpq-guardian.service')
    assert manager.live_mounts() == []

    run = _guardian(
        tmp_path, monkeypatch, manager, work_id='pawork', checkpoint='PART_A',
        served=_served(), document=_part_a_document(), progression='PART_A_READY',
    )
    assert run.failure is None and run.campaigns.transitions == ['COMPLETED']
    runs.append(run)

    for run in runs:
        # While its guardian lived the work held exactly its own pair.
        assert run.in_flight == sorted([run.io['in_unit'], run.io['out_unit']])
        _assert_bound_pair(manager, run)
    # One work in flight at a time: never more than one pair live.
    assert max(manager.live_after_start) <= 2
    assert manager.live_mounts() == []


@pytest.mark.parametrize(
    'exit_code,served,expected',
    [
        (137, _served(final=None, frame=None), [('part_a_initial_prefix', INITIAL)]),
        (0, _served(frame=None), [('part_a_initial_prefix', INITIAL), ('part_a_final', FINAL)]),
    ],
    ids=['abnormal-exit', 'absent-frame'],
)
def test_in_doubt_inspection_copy_is_staged_before_the_pair_is_released(
    tmp_path, monkeypatch, exit_code, served, expected
):
    """Test (2): on an abnormal-exit (or absent-frame) Part A work the
    inspection archive stages the artifacts byte-for-byte from the live mount
    before the guardian unit can end, the work is IN_DOUBT, and the pair is
    released when the guardian unit ends."""
    log = []
    manager = _Manager(log)
    run = _guardian(
        tmp_path, monkeypatch, manager, work_id='pawork', checkpoint='PART_A',
        served=served, document=_part_a_document(), progression='PART_A_READY',
        exit_code=exit_code,
    )
    assert run.campaigns.staged == [('PART_A', role, raw) for role, raw in expected]
    names = {role: name for name, role in supervisor.PART_A_ARTIFACT_ROLES.items()}
    for role, raw in expected:
        assert raw == served[names[role]]  # the pre-release mount bytes
    assert run.campaigns.transitions == ['IN_DOUBT'] and run.campaigns.captures == []
    end = log.index(('end', run.enrollment['scopes']['guardian_unit']))
    stages = [i for i, entry in enumerate(log) if entry[0] == 'stage']
    assert stages and max(stages) < log.index(('transition', 'IN_DOUBT')) < end
    for unit in (run.io['in_unit'], run.io['out_unit']):
        assert log.index(('stop', unit)) > end
    assert not [entry for entry in log[end:] if entry[0] in ('read_out', 'read_in', 'write_in')]
    assert manager.live_mounts() == []
    _assert_bound_pair(manager, run)


@pytest.mark.parametrize('crash_on', [None, 'retain_checkpoint_attestation'])
def test_capture_precedes_release_and_a_crash_after_capture_stays_recoverable(
    tmp_path, monkeypatch, crash_on
):
    """Test (3): the pair is released only when the guardian unit ends, which
    follows ``retain_checkpoint_capture``; no mount is read after the capture.
    A crash between the capture and the release leaves the retained capture
    and the work's CAPTURED state as they were (no IN_DOUBT over a captured
    work, no second capture) and the pair still stops with the guardian."""
    log = []
    manager = _Manager(log)
    run = _guardian(
        tmp_path, monkeypatch, manager, work_id='n1work', checkpoint='N1',
        served={'result.frame': b'frame'}, document={'observations': {}},
        progression='BOUND', crash_on=crash_on,
    )
    capture = log.index(('retain_checkpoint_capture', 'n1work'))
    end = log.index(('end', run.enrollment['scopes']['guardian_unit']))
    assert capture < end
    for unit in (run.io['in_unit'], run.io['out_unit']):
        assert log.index(('stop', unit)) > end
    reads = [i for i, entry in enumerate(log) if entry[0] in ('read_out', 'read_in', 'write_in')]
    assert reads and max(reads) < capture
    assert len(run.campaigns.captures) == 1
    if crash_on is None:
        assert run.failure is None and run.campaigns.transitions == ['COMPLETED']
    else:
        assert isinstance(run.failure, RuntimeError)
        # The guardian's failure path never marks a captured work IN_DOUBT; the
        # retained capture is the durable fact recovery reads.
        assert run.campaigns.transitions == [] and run.campaigns.work_state == 'CAPTURED'
        assert run.campaigns.events[-1] == 'FAILURE'
    assert manager.live_mounts() == []
    _assert_bound_pair(manager, run)


def test_recovery_retry_and_cleanup_never_read_the_io_mounts():
    """Guard for test (3)'s recoverability: recovery, the runtime's owned
    cleanup, the guardian's failure path and the g5/retry path read the store
    only -- none names the io mounts, so the mounts' lifetime cannot change
    what they decide."""
    for function in (
        supervisor._recover_campaign_work,
        supervisor.LinuxCampaignRuntime.cleanup,
        supervisor._run_n1_g5,
        supervisor._guardian_self_failure,
    ):
        source = inspect.getsource(function)
        for token in ('checkpoint_io_paths', 'in_path', 'out_path', 'in_unit', 'out_unit'):
            assert token not in source, (function.__name__, token)
