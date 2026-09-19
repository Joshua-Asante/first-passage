"""Private campaign supervision adapters; no alternate persistence authority.

The public wire never accepts commands, paths, cgroup names or counters. Scope
names are derived from installed host enrollment and durable attempt/work IDs.
"""
from datetime import datetime, timezone
from pathlib import Path
import sys
import subprocess
import sqlite3
import re
import time

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .campaign_budget import clock, integer
from .protocol import fields, identity, sha256

from .campaign_funding import WORK_ROLES, PROBES, WORK_PHASES


def parse_work_manifest(raw):
    doc = fields(parse_canonical_json(raw, label='campaign work manifest'),
                 {'schema', 'attempt_id', 'work_id', 'role', 'probe'})
    if (doc['schema'] != 'qualification_campaign_work_manifest/v1'
            or doc['role'] not in WORK_ROLES or doc['probe'] not in PROBES):
        raise ValueError('installed fixed role and probe required')
    identity(doc['attempt_id']); identity(doc['work_id'])
    if doc['role'] == 'admission' and (doc['work_id'] != 'admission' or doc['probe'] != 'noop'):
        raise ValueError('fixed admission operation required')
    if doc['probe'] == 'intent' and doc['role'] != 'probe_seal':
        raise ValueError('fixed harmless intent is only a seal-role probe')
    return doc


def work_enrollment(host_run_id, attempt_id, work_id):
    """Stable system-manager identities exist before any process can start."""
    from tools.qualification_verification.container_ownership import campaign_scopes
    return campaign_scopes(host_run_id, attempt_id, work_id)


def observe_campaign_clock():
    if sys.platform != 'linux' or not hasattr(time, 'CLOCK_BOOTTIME'):
        raise ValueError('trusted Linux BOOTTIME clock required')
    result = dict(schema='qualification_campaign_clock/v1',
                  boot_id=Path('/proc/sys/kernel/random/boot_id').read_text(encoding='ascii').strip(),
                  boottime_ns=time.clock_gettime_ns(time.CLOCK_BOOTTIME),
                  utc=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))
    raw = encoded(result)
    clock(raw)
    return raw


def _kernel_pairs(raw):
    if type(raw) is not bytes or len(raw) > 65536:
        raise ValueError('bounded kernel counter bytes required')
    result = {}
    for line in raw.decode('ascii').splitlines():
        parts = line.split()
        if len(parts) != 2 or parts[0] in result or not parts[1].isascii() or not parts[1].isdigit():
            raise ValueError('malformed kernel counter')
        result[parts[0]] = integer(int(parts[1]))
    return result


def parse_cgroup_counters(cpu_stat, memory_peak, memory_events):
    """The parent supplies aggregate peak/OOM; payload supplies measured CPU."""
    cpu = _kernel_pairs(cpu_stat)
    events = _kernel_pairs(memory_events)
    peak = memory_peak.decode('ascii').strip()
    if 'usage_usec' not in cpu or not {'oom', 'oom_kill'} <= events.keys() or not peak.isascii() or not peak.isdigit():
        raise ValueError('complete cgroup CPU/parent memory counters required')
    return dict(cpu_ns=integer(cpu['usage_usec'] * 1000), memory_peak_bytes=integer(int(peak)),
                oom_events=max(events['oom'], events['oom_kill'], events.get('oom_group_kill', 0)))


def parse_enrollment(raw):
    from .protocol import decode_base64
    doc = fields(parse_canonical_json(raw, label='supervision enrollment'), {
        'schema', 'host_run_id', 'attempt_id', 'work_id', 'manifest_bytes_b64', 'scopes'})
    if doc['schema'] != 'qualification_campaign_supervision/v1':
        raise ValueError('supervision enrollment schema required')
    manifest = parse_work_manifest(decode_base64(doc['manifest_bytes_b64']))
    if (manifest['attempt_id'] != doc['attempt_id'] or manifest['work_id'] != doc['work_id']
            or doc['scopes'] != work_enrollment(doc['host_run_id'], doc['attempt_id'], doc['work_id'])):
        raise ValueError('supervision ownership binding differs')
    return doc


def prepare_campaign_work(campaigns, attempt, work_id, *, host_run_id, manifest_bytes, clock_bytes):
    import base64
    manifest = parse_work_manifest(manifest_bytes)
    if manifest['attempt_id'] != attempt or manifest['work_id'] != work_id:
        raise ValueError('manifest work binding differs')
    scopes = work_enrollment(host_run_id, attempt, work_id)
    enrollment = dict(schema='qualification_campaign_supervision/v1', host_run_id=host_run_id,
        attempt_id=attempt, work_id=work_id, manifest_bytes_b64=base64.b64encode(manifest_bytes).decode('ascii'),
        scopes=scopes)
    with campaigns.store.transaction() as connection:
        state = campaigns._budget(connection, attempt)
        work = campaigns._work(state, work_id)
        expected_phase = WORK_PHASES[manifest['role']]
        if work['phase'] != expected_phase:
            raise ValueError('installed role phase differs')
        if manifest['role'] != 'admission' and campaigns._retry_parent(work) is None and work['input_sha256'] != sha256(manifest_bytes):
            raise ValueError('reserved fixed manifest differs')
        if work['state'] != 'RESERVED':
            raise ValueError('started work cannot relaunch')
        campaigns.retain_supervision(attempt, work_id, encoded(enrollment))
        campaigns.claim_supervision_control(attempt, work_id, 'START_OWNER', clock_bytes)
        state = parse_canonical_json(campaigns.record_work_transition(attempt, work_id, encoded(dict(
            schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id=work_id,
            state='START_INTENT', clock=clock(clock_bytes), data=dict(
                campaign_scope_id=scopes['campaign_slice'], work_scope_id=scopes['payload_slice']))),
            expected_revision=state['authority_revision']), label='prepared work')
    # This refusal is outside the transaction: an expired deadline stays durable.
    if state['state'] not in ('PROVISIONAL', 'BOUND') or state['validity'] != 'VALID':
        raise ValueError('terminal campaign cannot launch')
    return enrollment


def guardian_unit_spec(enrollment, *, attempt_id, work_id, code_root, interpreter,
                       uid, orchestration_cpu_ns, remaining_wall_ns):
    """Fixed command and independent lifecycle properties; no caller command slot.

    One controller process, no child processes/threads, so its process CPU limit
    bounds the charged control scope. Payloads live in the separate bound slice.
    The one-second margin is charged conservatively for the second-granular
    RLIMIT_CPU termination; actual enforcement must also be checked on the host.
    """
    from pathlib import PurePosixPath
    identity(attempt_id); identity(work_id)
    integer(uid, positive=True); integer(orchestration_cpu_ns, positive=True)
    integer(remaining_wall_ns, positive=True)
    from .profile import CAMPAIGN_RESOURCE_SCOPE as policy
    helper_seconds = policy['control_calls'] * (policy['control_cpu_seconds'] + policy['cpu_granularity_seconds'])
    if orchestration_cpu_ns % 10**9 or orchestration_cpu_ns < (helper_seconds + 2) * 10**9 or remaining_wall_ns < 1000:
        raise ValueError('kernel-enforceable controller CPU/wall ceiling required')
    for value in (code_root, interpreter):
        path = PurePosixPath(value)
        if not path.is_absolute() or '..' in path.parts or str(path) != value:
            raise ValueError('installed absolute runtime paths required')
    cpu_seconds = orchestration_cpu_ns // 10**9 - helper_seconds - policy['cpu_granularity_seconds']
    return dict(guardian=dict(Type='exec', User=str(uid), Slice=enrollment['work_slice'],
        Restart='no', KillMode='control-group', KillSignal=9, SendSIGKILL=True,
        TimeoutStopUSec=1_000_000, RuntimeMaxUSec=remaining_wall_ns // 1000,
        LimitCPU=cpu_seconds, LimitCPUSoft=cpu_seconds, TasksMax=1,
        OOMPolicy='kill', NoNewPrivileges=True, CPUAccounting=True, MemoryAccounting=True,
        Wants=[enrollment['payload_slice']],
        Environment=[name+'='+value for name,value in policy['controller_environment'].items()],
        ExecStart=[interpreter, '-I', str(PurePosixPath(code_root) / 'bootstrap.py'),
                   'campaign_guardian', '--attempt', attempt_id, '--work', work_id]),
        work=dict(CPUAccounting=True, MemoryAccounting=True),
        payload=dict(BindsTo=[enrollment['guardian_unit']], After=[enrollment['guardian_unit']],
                     CPUAccounting=True, MemoryAccounting=True))


def parse_supervision_event(raw):
    doc = fields(parse_canonical_json(raw, label='supervision event'),
                 {'schema', 'attempt_id', 'work_id', 'kind', 'clock', 'data'})
    if doc['schema'] != 'qualification_campaign_supervision_event/v1':
        raise ValueError('supervision event schema required')
    identity(doc['attempt_id']); identity(doc['work_id']); clock(encoded(doc['clock']))
    if doc['kind'] == 'CONTROL':
        fields(doc['data'], {'slot'})
        if doc['data']['slot'] not in ('START_OWNER', 'START_CLIENT', 'RECOVERY_OWNER'):
            raise ValueError('installed one-use control slot required')
    elif doc['kind'] == 'CLEANUP':
        fields(doc['data'], {'status'})
        if doc['data']['status'] not in ('ABSENT', 'PENDING'):
            raise ValueError('cleanup outcome required')
    elif doc['kind'] == 'PROCESS':
        fields(doc['data'], {'pid', 'start_ticks', 'uid', 'cgroup'})
        integer(doc['data']['pid'], positive=True); integer(doc['data']['start_ticks'])
        integer(doc['data']['uid'], positive=True)
        _absolute_cgroup(doc['data']['cgroup'])
    elif doc['kind'] == 'CONTAINER':
        from .protocol import digest
        fields(doc['data'], {'container_id', 'name', 'role', 'cgroup_parent'})
        digest(doc['data']['container_id']); identity(doc['data']['name'])
        identity(doc['data']['cgroup_parent'])
        if doc['data']['role'] not in WORK_ROLES:
            raise ValueError('installed role required')
    else:
        raise ValueError('unsupported supervision event')
    return doc


def _absolute_cgroup(value):
    from pathlib import PurePosixPath
    if (type(value) is not str or not value.startswith('/') or '..' in PurePosixPath(value).parts
            or str(PurePosixPath(value)) != value or value == '/'):
        raise ValueError('owned absolute cgroup path required')
    return value


def _retain_event(campaigns, attempt, work_id, kind, data):
    raw = encoded(dict(schema='qualification_campaign_supervision_event/v1',
        attempt_id=attempt, work_id=work_id, kind=kind,
        clock=parse_canonical_json(observe_campaign_clock(), label='clock'), data=data))
    campaigns.retain_supervision_event(raw)
    return raw


def _recover_campaign_work(context, reservation_bytes, *, attempt_id, work_id, recovery_owner_token):
    """Standalone durable recovery, then owned cleanup; never wraps recovery."""
    from .campaign_store import CampaignStore
    from .protocol import decode_base64
    campaigns = CampaignStore(context.store)
    state = parse_canonical_json(campaigns.recovery_budget_snapshot(attempt_id, work_id, recovery_owner_token), label='recovery budget')
    work = campaigns._work(state, work_id)
    if decode_base64(work['reservation_bytes_b64']) != reservation_bytes:
        raise ValueError('recovery reservation identity differs')
    if work['state'] == 'RESERVED':
        campaigns.recover_work(attempt_id, work_id, observe_campaign_clock(), recovery_owner_token=recovery_owner_token)
        cleanup = _retain_event(campaigns, attempt_id, work_id, 'CLEANUP', {'status': 'ABSENT'})
        return _complete_recovery(campaigns, attempt_id, work_id, cleanup, recovery_owner_token)
    enrollment = parse_enrollment(campaigns.objects(attempt_id)['supervision_' + work_id])
    runtime = None
    try:
        runtime = getattr(context, 'campaign_runtime', None) or LinuxCampaignRuntime(context)
        observed = runtime.observation(state, work, enrollment)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        observed = encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=attempt_id,
            work_id=work_id, clock=clock(observe_campaign_clock()),
            campaign_scope_id=enrollment['scopes']['campaign_slice'],
            work_scope_id=enrollment['scopes']['payload_slice'], cpu_ns=None,
            memory_peak_bytes=None, oom_events=None, termination_known=False,
            orchestration_charge_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']]))
    result = campaigns.recover_work(attempt_id, work_id, observed, recovery_owner_token=recovery_owner_token)
    # At this boundary another connection sees terminal uncertainty/no-redraw.
    try:
        if runtime is None:
            raise ValueError('owned runtime unavailable')
        runtime.cleanup(enrollment)
        outcome = 'ABSENT'
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        outcome = 'PENDING'
        context.recovery_issues[attempt_id + ':' + work_id] = 'CLEANUP_PENDING'
        failed = parse_canonical_json(observed, label='failed termination evidence')
        failed['termination_known'] = False
        failed['clock'] = clock(observe_campaign_clock())
        result = campaigns.recover_work(attempt_id, work_id, encoded(failed), recovery_owner_token=recovery_owner_token)
    cleanup = _retain_event(campaigns, attempt_id, work_id, 'CLEANUP', {'status': outcome})
    if outcome == 'ABSENT':
        return _complete_recovery(campaigns, attempt_id, work_id, cleanup, recovery_owner_token)
    return result


def _complete_recovery(campaigns, attempt, work_id, cleanup_bytes, token):
    state = parse_canonical_json(campaigns.recovery_budget_snapshot(attempt, work_id, token), label='recovered budget')
    row = next(r for r in state['recoveries'] if r['work_id'] == work_id)
    cleanup = parse_supervision_event(cleanup_bytes)
    from .protocol import decode_base64
    completion = encoded(dict(schema='qualification_campaign_recovery_completion/v1',
        attempt_id=attempt, work_id=work_id, claim_sha256=row['claim_sha256'],
        observations_sha256=sha256(decode_base64(row['observations_bytes_b64'])),
        cleanup_event_sha256=sha256(cleanup_bytes), clock=cleanup['clock']))
    return campaigns.complete_recovery(attempt, work_id, completion, recovery_owner_token=token)


def run_campaign_work(context, reservation_bytes, input_manifest_bytes):
    """Start one enrolled installed guardian; retries never issue another start."""
    from .campaign_store import CampaignStore
    from .protocol import decode_base64
    campaigns = CampaignStore(context.store)
    manifest = parse_work_manifest(input_manifest_bytes)
    attempt, work_id = manifest['attempt_id'], manifest['work_id']
    state = parse_canonical_json(campaigns.budget_snapshot(attempt), label='work budget')
    work = campaigns._work(state, work_id)
    if decode_base64(work['reservation_bytes_b64']) != reservation_bytes:
        raise ValueError('work reservation identity differs')
    if work['state'] != 'RESERVED':
        return encoded(campaigns.diagnostic_status(attempt))
    enrollment = prepare_campaign_work(campaigns, attempt, work_id,
        host_run_id=context.config['host_run_id'], manifest_bytes=input_manifest_bytes,
        clock_bytes=observe_campaign_clock())
    try:
        runtime = getattr(context, 'campaign_runtime', None) or LinuxCampaignRuntime(context)
        runtime.start(state, work, enrollment)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, sqlite3.Error) as launch_error:
        try:
            recover_campaign_work(context, reservation_bytes, attempt_id=attempt, work_id=work_id)
        except BaseException as recovery_error:
            raise recovery_error from launch_error
        raise
    return encoded(campaigns.diagnostic_status(attempt))

def _unit_properties(properties):
    result = [str(len(properties))]
    for name, value in properties.items():
        result.append(name)
        if name == 'ExecStart':
            result.extend(['a(sasb)', '1', value[0], str(len(value)), *value, 'false'])
        elif type(value) is bool:
            result.extend(['b', str(value).lower()])
        elif type(value) is int:
            result.extend(['i' if name == 'KillSignal' else 't', str(value)])
        elif type(value) is list:
            result.extend(['as', str(len(value)), *value])
        elif type(value) is str:
            result.extend(['s', value])
        else:
            raise ValueError('unsupported installed unit property')
    return result


def manager_start_arguments(scopes, specification):
    return [scopes['guardian_unit'], 'fail', *_unit_properties(specification['guardian']), '2',
            scopes['work_slice'], *_unit_properties(specification['work']),
            scopes['payload_slice'], *_unit_properties(specification['payload'])]


def host_slice(host_run_id):
    from tools.qualification_verification.container_ownership import campaign_host_slice
    return campaign_host_slice(host_run_id)


def _process_cgroup(pid='self'):
    rows = Path('/proc/' + str(pid) + '/cgroup').read_text(encoding='ascii').splitlines()
    if len(rows) != 1 or not rows[0].startswith('0::'):
        raise ValueError('unified cgroup v2 membership required')
    return _absolute_cgroup(rows[0][3:])


def _host_path(host_run_id):
    # Verify observed membership, not an assumed system-manager path alone.
    current = Path(_process_cgroup())
    name = host_slice(host_run_id)
    for candidate in (current, *current.parents):
        if candidate.name == name:
            return Path('/sys/fs/cgroup') / str(candidate).lstrip('/')
    raise ValueError('service must already belong to installed shared memory parent')


def _scope_path(parent, name):
    identity(name)
    if not name.endswith('.slice'):
        raise ValueError('slice identity required')
    pieces = name[:-6].split('-')
    # Each systemd slice name encodes its complete parent chain. The first
    # component has already been obtained from actual process membership.
    if pieces[0] + '.slice' != parent.name:
        raise ValueError('scope is not beneath observed host parent')
    result = parent
    for size in range(2, len(pieces) + 1):
        result = result / ('-'.join(pieces[:size]) + '.slice')
    return result


def _read_counter(path):
    with path.open('rb') as stream:
        raw = stream.read(65537)
    if len(raw) > 65536:
        raise ValueError('kernel counter exceeds bound')
    return raw


class LinuxCampaignRuntime:
    """Fixed Linux adapter. It performs no campaign calculation in a daemon.

    The administrator starts qexec under a persistent host slice with the signed
    memory limit. All campaigns conservatively observe this common parent,
    including shared qexec/launch clients. Counters are never reset per work.
    """
    def __init__(self, context):
        if sys.platform != 'linux':
            raise ValueError('Linux campaign supervision required')
        self.context = context
        self.parent = _host_path(context.config['host_run_id'])
        import json
        from .files import read_regular
        from .runtime import protected_path
        enrollment_path = Path(context.config['data_root']).parent / 'campaign-host.json'
        protected_path(enrollment_path)
        installed = json.loads(read_regular(enrollment_path.parent, enrollment_path.name, limit=65536))
        if (installed['schema'] != 'qualification_campaign_host/v1'
                or installed['host_run_id'] != context.config['host_run_id']
                or installed['scope'] != self.parent.name or installed['profile_sha256'] != context.profile.sha256
                or installed['memory_bytes'] != context.profile.memory_bytes):
            raise ValueError('activated common memory profile identity differs')
        if (self.parent / 'memory.max').read_text().strip() != str(context.profile.memory_bytes):
            raise ValueError('installed common memory limit differs')
        if (self.parent / 'memory.swap.max').read_text().strip() != '0':
            raise ValueError('common scope must disable swap')
        if (self.parent / 'memory.oom.group').read_text().strip() != '1':
            raise ValueError('common scope requires group OOM termination')

    def _control(self, command, *, enrollment):
        import subprocess
        from .campaign_store import CampaignStore
        CampaignStore(self.context.store).claim_supervision_control(enrollment['attempt_id'],
            enrollment['work_id'], 'START_CLIENT', observe_campaign_clock())
        # Helpers inherit the already enforced common memory parent. Their hard
        # process CPU bound plus one-second granularity is fully charged.
        import os
        from .runtime import installed_code_root
        campaigns = CampaignStore(self.context.store)
        process = None
        try:
            with campaigns.launch_gate(enrollment['attempt_id'], enrollment['work_id'], observe_campaign_clock) as permit:
                process = subprocess.Popen(['/usr/bin/prlimit', '--cpu=1:1', '--', sys.executable, '-I',
                    str(installed_code_root() / 'bootstrap.py'), 'campaign_control', str(os.getpid()), *command],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    env={'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8'})
            # Never wait for this child while holding the journal transaction.
            wait_clock = clock(observe_campaign_clock())
            if (wait_clock['boot_id'] != permit['clock']['boot_id'] or wait_clock['boottime_ns'] is None
                    or wait_clock['boottime_ns'] < permit['clock']['boottime_ns']
                    or wait_clock['boottime_ns'] >= permit['deadline_boottime_ns']):
                raise ValueError('original client acknowledgement deadline or clock differs')
            remaining_ns = permit['deadline_boottime_ns'] - wait_clock['boottime_ns']
            stdout, stderr = process.communicate(timeout=min(8, remaining_ns / 10**9))
        except BaseException:
            if process is not None and process.returncode is None:
                try:
                    process.kill()
                    process.communicate(timeout=2)
                except (OSError, subprocess.SubprocessError):
                    pass  # Original failure drives durable recovery; no success claim.
            raise
        if process.returncode != 0 or len(stdout) > 65536 or len(stderr) > 65536:
            raise ValueError('bounded system-manager operation failed')
        if re.fullmatch(rb'o "/org/freedesktop/systemd1/job/[0-9]+"\n?', stdout) is None:
            raise ValueError('system-manager job acknowledgement differs')
        campaigns.acknowledge_dispatch(enrollment['attempt_id'], enrollment['work_id'],
            'guardian', permit['token'], observe_campaign_clock)
        return stdout

    def start(self, state, work, enrollment):
        from .runtime import installed_code_root
        current = clock(observe_campaign_clock())
        reservation = parse_canonical_json(__import__('base64').b64decode(work['reservation_bytes_b64']), label='reservation')
        deadline = min(state['deadline_boottime_ns'],
                       reservation['clock']['boottime_ns'] + work['limits']['wall_ns'])
        if current['boot_id'] != state['start_clock']['boot_id'] or deadline <= current['boottime_ns']:
            raise ValueError('original deadline or boot differs')
        spec = guardian_unit_spec(enrollment['scopes'], attempt_id=state['attempt_id'], work_id=work['work_id'],
            code_root=str(installed_code_root()), interpreter=sys.executable,
            uid=self.context.config['service_uid'],
            orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']],
            remaining_wall_ns=deadline - current['boottime_ns'])
        from tools.qualification_verification.container_ownership import CAMPAIGN_BUS_START
        self._control([*CAMPAIGN_BUS_START, *manager_start_arguments(enrollment['scopes'], spec)], enrollment=enrollment)

    def observation(self, state, work, enrollment):
        # A live/unavailable payload is never represented by a final CPU sample.
        # Recovery consequently spends the reservation before destructive cleanup.
        cpu = peak = oom = None
        terminated = False
        try:
            peak_raw = _read_counter(self.parent / 'memory.peak')
            events_raw = _read_counter(self.parent / 'memory.events')
            values = parse_cgroup_counters(b'usage_usec 0\n', peak_raw, events_raw)
            peak, oom = values['memory_peak_bytes'], values['oom_events']
            payload = _scope_path(self.parent, enrollment['scopes']['payload_slice'])
            payload_absent = not payload.exists() or _kernel_pairs(_read_counter(payload / 'cgroup.events')).get('populated') == 0
            rows = DockerControl().owned(enrollment)
            if len(rows) > 1:
                raise ValueError('ambiguous owned container inventory')
            container_absent = True
            for row in rows:
                details = DockerControl().call('GET', '/containers/' + row['Id'] + '/json')
                container_absent &= not bool(details['State']['Running'] or details['State']['Pid']
                    or details['State'].get('Paused') or details['State'].get('Restarting'))
            terminated = payload_absent and container_absent
            if terminated and payload.exists():
                cpu = parse_cgroup_counters(_read_counter(payload / 'cpu.stat'), peak_raw, events_raw)['cpu_ns']
        except (OSError, ValueError):
            pass
        return encoded(dict(schema='qualification_campaign_observation/v2', attempt_id=state['attempt_id'],
            work_id=work['work_id'], clock=clock(observe_campaign_clock()),
            campaign_scope_id=enrollment['scopes']['campaign_slice'],
            work_scope_id=enrollment['scopes']['payload_slice'], cpu_ns=cpu,
            memory_peak_bytes=peak, oom_events=oom, termination_known=terminated,
            orchestration_charge_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']]))

    def cleanup(self, enrollment):
        import os
        import signal
        from .campaign_store import CampaignStore
        scopes = enrollment['scopes']
        work_group = _scope_path(self.parent, scopes['work_slice'])
        docker = DockerControl()
        rows = docker.owned(enrollment)
        if len(rows) > 1:
            raise ValueError('ambiguous owned probe container inventory')
        populated = work_group.exists() and _kernel_pairs(_read_counter(work_group / 'cgroup.events')).get('populated') != 0
        details_by_id = {}
        for row in rows:
            details = docker.call('GET', '/containers/' + row['Id'] + '/json')
            if details['Name'] != '/fpqs2-' + sha256(encoded(enrollment)):
                raise ValueError('cleanup container enrollment differs')
            details_by_id[row['Id']] = details
        if not populated and not any(details['State']['Running'] or details['State']['Pid']
                or details['State'].get('Paused') or details['State'].get('Restarting') for details in details_by_id.values()):
            return  # Historical absence inspection launches no controller/client.
        guardian = work_group / scopes['guardian_unit']
        if guardian.exists():
            pids = _read_counter(guardian / 'cgroup.procs').decode('ascii').splitlines()
            if len(pids) > 1:
                raise ValueError('single guardian membership differs')
            for value in pids:
                pid = int(value)
                descriptor = os.pidfd_open(pid)
                try:
                    actual = Path('/sys/fs/cgroup') / _process_cgroup(pid).lstrip('/')
                    if actual != guardian:
                        raise ValueError('guardian PID escaped owned scope')
                    signal.pidfd_send_signal(descriptor, signal.SIGKILL)
                finally:
                    os.close(descriptor)
        for row in rows:
            details = docker.call('GET', '/containers/' + row['Id'] + '/json')
            expected_name = '/fpqs2-' + sha256(encoded(enrollment))
            image = parse_canonical_json(self.context.release, label='release')['worker_image_digest']
            if details['Name'] != expected_name or details['Image'] != image:
                raise ValueError('cleanup container identity differs')
            if details['State']['Running']:
                docker.call('POST', '/containers/' + row['Id'] + '/kill?signal=KILL')
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            live_scope = work_group.exists() and _kernel_pairs(_read_counter(work_group / 'cgroup.events')).get('populated') != 0
            live_container = False
            for row in rows:
                details = docker.call('GET', '/containers/' + row['Id'] + '/json')
                live_container |= bool(details['State']['Running'] or details['State']['Pid'])
            if not live_scope and not live_container:
                return
            time.sleep(.025)
        raise ValueError('owned process absence remains uncertain')


class DockerControl:
    """Finite fixed lifecycle HTTP requests, no image build/archive/exec port."""
    def call(self, method, path, body=None, *, raw=False):
        import http.client
        import socket
        class Connection(http.client.HTTPConnection):
            def connect(self):
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.settimeout(5)
                self.sock.connect('/var/run/docker.sock')
        connection = Connection('localhost', timeout=5)
        payload = None if body is None else encoded(body)
        if payload is not None and len(payload) > 65536:
            raise ValueError('Docker lifecycle request exceeds installed bound')
        try:
            connection.request(method, '/v1.48' + path, body=payload,
                               headers={'Content-Type': 'application/json'})
            response = connection.getresponse()
            content = response.read(65537)
            if response.status not in (200, 201, 204, 304) or len(content) > 65536:
                raise ValueError('bounded Docker lifecycle operation failed')
            if raw:
                return content
            import json
            return json.loads(content) if content else None
        except http.client.HTTPException as exc:
            raise ValueError('Docker lifecycle response unavailable') from exc
        finally:
            connection.close()

    def owned(self, enrollment):
        from urllib.parse import quote
        import json
        filters = {'label': ['fp.s2.host=' + enrollment['host_run_id'],
                             'fp.s2.attempt=' + enrollment['attempt_id'],
                             'fp.s2.work=' + enrollment['work_id']]}
        return self.call('GET', '/containers/json?all=1&filters=' + quote(json.dumps(filters), safe=''))

def _kernel_kill_timer(clock_id, duration_ns, *, absolute):
    """Install a kernel SIGKILL timer using the supported host ABI."""
    import ctypes
    import platform
    import signal
    if sys.platform != 'linux' or platform.machine() != 'x86_64':
        raise ValueError('supported Linux x86_64 timer ABI required')
    class Event(ctypes.Structure):
        _fields_ = [('value', ctypes.c_void_p), ('signo', ctypes.c_int),
                    ('notify', ctypes.c_int), ('padding', ctypes.c_byte * 48)]
    class Timespec(ctypes.Structure):
        _fields_ = [('seconds', ctypes.c_long), ('nanoseconds', ctypes.c_long)]
    class TimerSpec(ctypes.Structure):
        _fields_ = [('interval', Timespec), ('value', Timespec)]
    libc = ctypes.CDLL('libc.so.6', use_errno=True)
    timer = ctypes.c_void_p()
    event = Event(None, signal.SIGKILL, 0)
    specification = TimerSpec(Timespec(0, 0), Timespec(*divmod(duration_ns, 10**9)))
    if libc.timer_create(clock_id, ctypes.byref(event), ctypes.byref(timer)):
        raise OSError(ctypes.get_errno(), 'kernel BOOTTIME timer_create failed')
    if libc.timer_settime(timer, int(absolute), ctypes.byref(specification), None):
        raise OSError(ctypes.get_errno(), 'kernel absolute deadline failed')
    return libc, timer


def arm_boottime_deadline(deadline_ns):
    """Independent wall termination includes suspend and Python stopping."""
    return _kernel_kill_timer(time.CLOCK_BOOTTIME, deadline_ns, absolute=True)


from contextlib import contextmanager


@contextmanager
def controller_cpu_guard():
    """Bound the current shared-qexec admission handler, including journal IO.

    SIGKILL terminates the service if its handler consumes the installed CPU
    allowance. Other campaign guardians have independent system-manager lives.
    """
    import ctypes
    from .profile import CAMPAIGN_RESOURCE_SCOPE
    if sys.platform != 'linux':
        raise ValueError('Linux controller CPU timer required')
    libc, timer = _kernel_kill_timer(time.CLOCK_THREAD_CPUTIME_ID,
        CAMPAIGN_RESOURCE_SCOPE['control_cpu_seconds'] * 10**9, absolute=False)
    try:
        _, wall_timer = _kernel_kill_timer(time.CLOCK_BOOTTIME,
            CAMPAIGN_RESOURCE_SCOPE['control_wall_seconds'] * 10**9, absolute=False)
    except BaseException:
        libc.timer_delete(timer)
        raise
    try:
        yield
    finally:
        wall_error = libc.timer_delete(wall_timer)
        cpu_error = libc.timer_delete(timer)
        if wall_error or cpu_error:
            raise OSError(ctypes.get_errno(), 'controller timer retirement failed')


def _transition(campaigns, attempt, work_id, target, data):
    state = parse_canonical_json(campaigns.budget_snapshot(attempt), label='work transition budget')
    return parse_canonical_json(campaigns.record_work_transition(attempt, work_id, encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id=work_id,
        state=target, clock=clock(observe_campaign_clock()), data=data)),
        expected_revision=state['authority_revision']), label='work transition result')


def _assert_authority(state):
    from .campaign_budget import recovery_pending, dispatch_pending
    if recovery_pending(state):
        raise ValueError('campaign recovery pending')
    if dispatch_pending(state):
        raise ValueError('campaign dispatch pending')
    if state['state'] not in ('PROVISIONAL', 'BOUND') or state['validity'] != 'VALID':
        raise ValueError('campaign is terminal or invalidated')


def _await_dispatch_ack(campaigns, attempt, work_id, deadline):
    """Called only after the guardian's absolute timer has been installed.

    StartTransientUnit replies with a queued job, independent of this wait.
    No journal lock is held while sleeping and no new allowance is granted.
    """
    from .campaign_budget import recovery_pending
    while True:
        state = parse_canonical_json(campaigns.budget_snapshot(attempt), label='dispatch acknowledgement')
        if recovery_pending(state) or state['validity'] != 'VALID' or state['state'] not in ('PROVISIONAL', 'BOUND'):
            raise ValueError('guardian authority revoked while awaiting dispatch acknowledgement')
        row = next((r for r in state.get('dispatches', ()) if r['work_id'] == work_id and r['role'] == 'guardian'), None)
        if row is None:
            raise ValueError('durable guardian dispatch required')
        current = clock(observe_campaign_clock())
        if current['boot_id'] != state['start_clock']['boot_id'] or current['boottime_ns'] is None or current['boottime_ns'] >= deadline:
            raise ValueError('original guardian dispatch deadline expired')
        if row['acknowledged_clock'] is not None:
            _assert_authority(state)
            return state
        time.sleep(min(0.01, (deadline - current['boottime_ns']) / 10**9))


def guardian_main():
    import argparse
    import base64
    import os
    import resource
    from .runtime import load_instance, measure_runtime, installed_code_root
    from .release import parse_instance
    from .service import ExecutionService
    from .campaign_store import CampaignStore
    from .protocol import decode_base64
    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--work', required=True)
    args = parser.parse_args()
    identity(args.attempt); identity(args.work)
    config = parse_instance(encoded(load_instance(installed_code_root() / 'qualification-installation/supervisor.json')))
    if os.geteuid() != config['service_uid']:
        raise ValueError('guardian OS role differs')
    context = ExecutionService(config)
    if context.profile.values['schema'] != 'qualification_execution_profile/v3':
        raise ValueError('diagnostic guardian requires fresh installed revision')
    campaigns = CampaignStore(context.store)
    state = parse_canonical_json(campaigns.budget_snapshot(args.attempt), label='guardian budget')
    work = campaigns._work(state, args.work)
    enrollment = parse_enrollment(campaigns.objects(args.attempt)['supervision_' + args.work])
    manifest = parse_work_manifest(decode_base64(enrollment['manifest_bytes_b64']))
    reservation_bytes = decode_base64(work['reservation_bytes_b64'])
    reservation = parse_canonical_json(reservation_bytes, label='guardian reservation')
    runtime = LinuxCampaignRuntime(context)
    now_clock = clock(observe_campaign_clock())
    deadline = min(state['deadline_boottime_ns'], reservation['clock']['boottime_ns'] + work['limits']['wall_ns'])
    if now_clock['boot_id'] != state['start_clock']['boot_id'] or now_clock['boottime_ns'] >= deadline:
        recover_campaign_work(context, reservation_bytes, attempt_id=args.attempt, work_id=args.work)
        return
    arm_boottime_deadline(deadline)
    state = _await_dispatch_ack(campaigns, args.attempt, args.work, deadline)
    _assert_authority(state)
    if state['profile'] != parse_canonical_json(context.release, label='release')['campaign_budget_profile']:
        raise ValueError('installed immutable budget profile differs')
    own_group = Path('/sys/fs/cgroup') / _process_cgroup().lstrip('/')
    expected_parent = _scope_path(runtime.parent, enrollment['scopes']['work_slice'])
    if own_group != expected_parent / enrollment['scopes']['guardian_unit']:
        raise ValueError('guardian effective cgroup membership differs')
    if (own_group / 'pids.max').read_text().strip() != '1':
        raise ValueError('single-process controller enforcement required')
    spec = guardian_unit_spec(enrollment['scopes'], attempt_id=args.attempt, work_id=args.work,
        code_root=str(installed_code_root()), interpreter=sys.executable, uid=os.geteuid(),
        orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']], remaining_wall_ns=deadline-now_clock['boottime_ns'])
    if resource.getrlimit(resource.RLIMIT_CPU) != (spec['guardian']['LimitCPU'], spec['guardian']['LimitCPU']):
        raise ValueError('guardian effective hard CPU limit differs')
    stat_fields = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
    _retain_event(campaigns, args.attempt, args.work, 'PROCESS',
        dict(pid=os.getpid(), start_ticks=int(stat_fields[19]), uid=os.geteuid(), cgroup=_process_cgroup()))
    try:
        measure_runtime(installed_code_root(), 'supervisor', context.release)
        if DockerControl().call('GET', '/info')['CgroupDriver'] != 'systemd':
            raise ValueError('installed Docker cgroup driver differs')
        state = _transition(campaigns, args.attempt, args.work, 'RUNNING', {})
        _assert_authority(state)
        if manifest['role'] == 'admission':
            from .admission import verify_retained_bundle
            from .plan import derive_campaign_plan_from_context
            from ..source_admission import admit_source
            request_bytes = campaigns.row(args.attempt)['request_bytes']
            request = parse_canonical_json(request_bytes, label='original request')
            verified = context._context(request['bundle_sha256'], at=datetime.now(timezone.utc))
            contract = parse_canonical_json(verified.contract.canonical_bytes, label='authenticated contract')
            state = parse_canonical_json(campaigns.bind_budget(args.attempt, encoded(contract['replay']['budget']),
                expected_revision=state['authority_revision'], clock_bytes=observe_campaign_clock()), label='bound budget')
            _assert_authority(state)
            arm_boottime_deadline(min(state['deadline_boottime_ns'], deadline))
            admitted = admit_source(verified.contract, artifact_root=verified.bundle_dir, policy=verified.policy)
            proof = encoded(dict(source_admission_b64=base64.b64encode(admitted.source_admission_bytes).decode(),
                                 legality_b64=base64.b64encode(admitted.legality_bytes).decode()))
            state = _transition(campaigns, args.attempt, args.work, 'CAPTURED',
                                dict(capture_bytes_b64=base64.b64encode(proof).decode()))
            _assert_authority(state)
            plan = derive_campaign_plan_from_context(verified)
            published_at = datetime.now(timezone.utc)
            verified = verify_retained_bundle(verified.retained_bundle_index, verified.retained_bytes,
                                              context.release, context.keys(), published_at)
            observed = runtime.observation(state, work, enrollment)
            campaigns.finish_diagnostic_admission(request_bytes, verified, plan, observed, now=published_at, trusted_keys=context.keys())
        else:
            _run_probe(context, campaigns, runtime, state, work, enrollment, manifest)
    except BaseException:
        # Durable uncertainty/no-redraw precedes cleanup; systemd's independent
        # BindsTo interlock also retires payload if SIGKILL prevents this handler.
        recover_campaign_work(context, reservation_bytes, attempt_id=args.attempt, work_id=args.work)
        raise


def probe_container_body(context, enrollment, manifest):
    role = manifest['role']
    if role not in WORK_ROLES[1:]:
        raise ValueError('installed harmless probe role required')
    config = context.config
    uid = {'probe_worker': context.profile.worker_uid, 'probe_g5': config['g5_uid'],
           'probe_result': config['g5_uid'], 'probe_seal': config['seal_probe_uid']}[role]
    image = parse_canonical_json(context.release, label='installed release')['worker_image_digest']
    return dict(Image=image, User=str(uid) + ':' + str(uid), WorkingDir='/tmp',
        Entrypoint=['/opt/ops/bin/python', '-I', '/opt/qualification/bootstrap.py', 'campaign_probe'],
        Cmd=['--probe', manifest['probe']], AttachStdout=False, AttachStderr=False, Tty=False,
        Labels={'fp.s2.host': enrollment['host_run_id'], 'fp.s2.attempt': enrollment['attempt_id'],
                'fp.s2.work': enrollment['work_id'], 'fp.s2.role': role},
        HostConfig=dict(NetworkMode='none', ReadonlyRootfs=True, CapDrop=['ALL'],
            SecurityOpt=['no-new-privileges:true'], IpcMode='private', PidMode='',
            RestartPolicy={'Name': 'no', 'MaximumRetryCount': 0}, PidsLimit=context.profile.pids_limit,
            Memory=context.profile.memory_bytes, MemorySwap=context.profile.memory_bytes,
            CgroupParent=enrollment['scopes']['payload_slice'],
            LogConfig={'Type': 'none', 'Config': {}},
            Tmpfs={'/tmp': 'rw,noexec,nosuid,nodev,size=' + str(context.profile.scratch_bytes)}))


def _run_probe(context, campaigns, runtime, state, work, enrollment, manifest):
    from .protocol import digest
    if manifest['probe'] == 'controller_cpu':
        while True:
            sum(range(10000))
    docker = DockerControl()
    if docker.call('GET', '/info')['CgroupDriver'] != 'systemd':
        raise ValueError('installed Docker cgroup driver differs; no automatic switch')
    name = 'fpqs2-' + sha256(encoded(enrollment))
    body = probe_container_body(context, enrollment, manifest)
    container = digest(docker.call('POST', '/containers/create?name=' + name, body)['Id'])
    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'CONTAINER', dict(
        container_id=container, name=name, role=manifest['role'], cgroup_parent=enrollment['scopes']['payload_slice']))
    row = docker.call('GET', '/containers/' + container + '/json')
    if (row['Image'] != body['Image'] or row['Config']['User'] != body['User']
            or row['Config']['Entrypoint'] != body['Entrypoint'] or row['Config']['Cmd'] != body['Cmd']
            or row['HostConfig']['CgroupParent'] != enrollment['scopes']['payload_slice']):
        raise ValueError('effective fixed container configuration differs')
    with campaigns.launch_gate(state['attempt_id'], work['work_id'], observe_campaign_clock, role='payload') as permit:
        docker.call('POST', '/containers/' + container + '/start')
    campaigns.acknowledge_dispatch(state['attempt_id'], work['work_id'],
        'payload', permit['token'], observe_campaign_clock)
    payload = _scope_path(runtime.parent, enrollment['scopes']['payload_slice'])
    budget_cpu = work['limits']['cpu_ns'] - state['profile']['orchestration_cpu_ns'][work['phase']]
    seen_pids = set()
    stopping = False
    while True:
        if not stopping:
            _assert_authority(parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='current probe authority'))
        row = docker.call('GET', '/containers/' + container + '/json')
        if row['State']['Running']:
            pid = row['State']['Pid']
            actual = Path('/sys/fs/cgroup') / _process_cgroup(pid).lstrip('/')
            if not actual.is_relative_to(payload) or actual == payload:
                raise ValueError('running container escaped payload accounting')
            for pid_text in (actual / 'cgroup.procs').read_text().splitlines():
                try:
                    stat_fields = Path('/proc/' + pid_text + '/stat').read_text().rsplit(')', 1)[1].split()
                    birth = int(stat_fields[19])
                    status = Path('/proc/' + pid_text + '/status').read_text()
                    uid = int(next(line for line in status.splitlines() if line.startswith('Uid:')).split()[1])
                except FileNotFoundError:
                    continue
                if str(uid) != body['User'].split(':')[0]:
                    raise ValueError('effective role UID differs')
                if (pid_text, birth) not in seen_pids:
                    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PROCESS',
                        dict(pid=int(pid_text), start_ticks=birth, uid=uid, cgroup=_process_cgroup(pid_text)))
                    seen_pids.add((pid_text, birth))
            if not stopping and _kernel_pairs(_read_counter(payload / 'cpu.stat')).get('usage_usec', 0) * 1000 >= budget_cpu:
                _transition(campaigns, state['attempt_id'], work['work_id'], 'IN_DOUBT', {})
                docker.call('POST', '/containers/' + container + '/kill?signal=KILL')
                stopping = True
                # Final actual usage is retained only after verified absence.
            time.sleep(.025)
            continue
        if row['State']['Pid'] != 0:
            raise ValueError('container termination has no process absence proof')
        break
    state = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='probe final state')
    work = campaigns._work(state, work['work_id'])
    capture = encoded(dict(schema='qualification_campaign_probe_capture/v1',
                           container_id=container, exit_code=row['State']['ExitCode'], role=manifest['role']))
    if work['state'] == 'RUNNING' and row['State']['ExitCode'] == 0 and campaigns._retry_parent(work) is None:
        import base64
        state = _transition(campaigns, state['attempt_id'], work['work_id'], 'CAPTURED',
                            dict(capture_bytes_b64=base64.b64encode(capture).decode()))
    if manifest['probe'] == 'intent':
        import base64
        state = _transition(campaigns, state['attempt_id'], work['work_id'], 'SIGNING_INTENT',
            dict(intent_id=work['work_id']+'-intent', payload_bytes_b64=base64.b64encode(b'S2 harmless fixed intent').decode(),
                 key_id='TEST_ONLY_NO_CREDENTIAL', signing_at_utc=clock(observe_campaign_clock())['utc']))
    observed = runtime.observation(state, work, enrollment)
    state = parse_canonical_json(campaigns.settle_work(state['attempt_id'], work['work_id'], observed), label='probe settlement')
    if state['state'] == 'BOUND' and state['validity'] == 'VALID':
        if row['State']['ExitCode'] == 0 and manifest['probe'] != 'intent':
            _transition(campaigns, state['attempt_id'], work['work_id'], 'COMPLETED', {})
        elif row['State']['ExitCode'] != 0:
            _transition(campaigns, state['attempt_id'], work['work_id'], 'ABORTED', {})
    docker.call('DELETE', '/containers/' + container + '?v=1')


def recover_campaign_work(context, reservation_bytes, *, attempt_id, work_id):
    """One bounded recovery owner; destructive retries need an unspent slot."""
    from .campaign_store import CampaignStore
    import secrets
    with controller_cpu_guard():
        token = secrets.token_bytes(32)
        CampaignStore(context.store).claim_supervision_control(attempt_id, work_id,
            'RECOVERY_OWNER', observe_campaign_clock(), recovery_owner_token=token)
        return _recover_campaign_work(context, reservation_bytes, attempt_id=attempt_id, work_id=work_id,
                                      recovery_owner_token=token)
