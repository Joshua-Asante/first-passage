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
from .campaign_probe import READINESS_TOKEN


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


def payload_cpu_quota_usec(budget_cpu_ns, remaining_wall_ns):
    """Kernel rate bound: quota (CPU µs per wall second) × RuntimeMax ≤ payload budget.

    cgroup v2 has no cumulative CPU cap. The system manager enforces the rate
    (cpu.max on the payload slice) and the lifetime (RuntimeMaxUSec on the
    guardian, whose end retires the payload slice through BindsTo) without the
    guardian's Python, so their product bounds cumulative payload CPU whether or
    not the guardian ever polls again. Floor keeps the product at or below the
    budget; both inputs are existing limits, no profile constant is added.
    """
    if type(budget_cpu_ns) is not int or budget_cpu_ns <= 0:
        raise ValueError('positive payload CPU budget beyond the orchestration bound required')
    integer(budget_cpu_ns, positive=True); integer(remaining_wall_ns, positive=True)
    quota = budget_cpu_ns * 10**6 // remaining_wall_ns
    if quota <= 0:
        raise ValueError('payload CPU quota below manager resolution')
    return quota


def verify_payload_cpu_max(raw, *, remaining_wall_ns, budget_cpu_ns, quota_usec=None):
    """Refuse unless the realized cpu.max keeps rate × remaining lifetime ≤ budget.

    The manager writes max(quota × period ÷ 10⁶, 1 ms) with the period it chose;
    the derived quota is compared exactly when the deriving caller supplies it,
    and the bound is checked with the realized period either way.
    """
    integer(remaining_wall_ns, positive=True); integer(budget_cpu_ns, positive=True)
    if type(raw) is not bytes or len(raw) > 64:
        raise ValueError('bounded cpu.max bytes required')
    parts = raw.decode('ascii', 'replace').split()
    if len(parts) != 2 or not all(part.isascii() and part.isdigit() for part in parts):
        raise ValueError('payload slice has no finite realized CPU quota')
    realized, period = int(parts[0]), int(parts[1])
    if period <= 0 or realized <= 0:
        raise ValueError('payload slice has no finite realized CPU quota')
    if quota_usec is not None and realized != max(integer(quota_usec, positive=True) * period // 10**6, 1000):
        raise ValueError('realized payload CPU quota differs from derived rate')
    if realized * remaining_wall_ns > budget_cpu_ns * period:
        raise ValueError('realized payload CPU rate exceeds reservation over remaining lifetime')
    return realized, period


def guardian_deadline(state, work, reservation, argv_deadline_ns):
    """The guardian's argv deadline must be the durable reservation's own instant.

    bootstrap.py armed the kernel SIGKILL timer from that argv before any
    campaign import; a differing value is refused here on the recovery path.
    """
    integer(argv_deadline_ns, positive=True)
    deadline = min(state['deadline_boottime_ns'], reservation['clock']['boottime_ns'] + work['limits']['wall_ns'])
    if argv_deadline_ns != deadline:
        raise ValueError('guardian argv deadline differs from durable reservation')
    return deadline


def guardian_task_bound(manifest):
    """Probe guardians stay single-task (S2); a dispatch-work guardian spawns
    its own campaign_control children for the io mounts and the g5 unit (D2),
    bounded by the installed control_calls allowance."""
    return 1 + CAMPAIGN_CONTROL_TASKS if manifest['role'] in ('n1_worker', 'n1_g5') else 1


CAMPAIGN_CONTROL_TASKS = 2


def guardian_unit_spec(enrollment, *, attempt_id, work_id, code_root, interpreter,
                       uid, orchestration_cpu_ns, remaining_wall_ns, cpu_ns, deadline_boottime_ns,
                       tasks=1):
    """Fixed command and independent lifecycle properties; no caller command slot.

    One controller process, no child processes/threads, so its process CPU limit
    bounds the charged control scope. Payloads live in the separate bound slice,
    rate-limited by the manager so that quota × RuntimeMax never exceeds the
    reservation beyond the orchestration bound. The absolute deadline rides the
    fixed argv so bootstrap can arm it before the first campaign import. The
    one-second margin is charged conservatively for the second-granular
    RLIMIT_CPU termination; actual enforcement must also be checked on the host.
    """
    from pathlib import PurePosixPath
    identity(attempt_id); identity(work_id)
    integer(uid, positive=True); integer(orchestration_cpu_ns, positive=True)
    integer(remaining_wall_ns, positive=True); integer(cpu_ns, positive=True)
    integer(deadline_boottime_ns, positive=True)
    from .profile import CAMPAIGN_RESOURCE_SCOPE as policy
    helper_seconds = policy['control_calls'] * (policy['control_cpu_seconds'] + policy['cpu_granularity_seconds'])
    if orchestration_cpu_ns % 10**9 or orchestration_cpu_ns < (helper_seconds + 2) * 10**9 or remaining_wall_ns < 1000:
        raise ValueError('kernel-enforceable controller CPU/wall ceiling required')
    for value in (code_root, interpreter):
        path = PurePosixPath(value)
        if not path.is_absolute() or '..' in path.parts or str(path) != value:
            raise ValueError('installed absolute runtime paths required')
    cpu_seconds = orchestration_cpu_ns // 10**9 - helper_seconds - policy['cpu_granularity_seconds']
    quota = payload_cpu_quota_usec(cpu_ns - orchestration_cpu_ns, remaining_wall_ns)
    return dict(guardian=dict(Type='exec', User=str(uid), Slice=enrollment['work_slice'],
        Restart='no', KillMode='control-group', KillSignal=9, SendSIGKILL=True,
        TimeoutStopUSec=1_000_000, RuntimeMaxUSec=remaining_wall_ns // 1000,
        LimitCPU=cpu_seconds, LimitCPUSoft=cpu_seconds, TasksMax=tasks,
        OOMPolicy='kill', NoNewPrivileges=True, CPUAccounting=True, MemoryAccounting=True,
        Wants=[enrollment['payload_slice']],
        Environment=[name+'='+value for name,value in policy['controller_environment'].items()],
        ExecStart=[interpreter, '-I', str(PurePosixPath(code_root) / 'bootstrap.py'),
                   'campaign_guardian', '--attempt', attempt_id, '--work', work_id,
                   '--deadline-boottime-ns', str(deadline_boottime_ns)]),
        work=dict(CPUAccounting=True, MemoryAccounting=True),
        payload=dict(BindsTo=[enrollment['guardian_unit']], After=[enrollment['guardian_unit']],
                     CPUAccounting=True, MemoryAccounting=True, CPUQuotaPerSecUSec=quota))


SUPERVISION_EVENT_V1 = 'qualification_campaign_supervision_event/v1'
SUPERVISION_EVENT_V2 = 'qualification_campaign_supervision_event/v2'


def parse_supervision_event(raw):
    """Both event versions, each against its own closed shape.

    v1 is the pre-G3 journal contract, byte for byte: PROCESS/RESUMED carry no
    process image, and no PAYLOAD_EXIT kind exists. Every historical journal
    (runs through 35493582848) reopens against it unchanged. v2 is the G3
    evidence shape: PROCESS/RESUMED require the bounded image (comm always,
    exe possibly '' across the ptrace gate) and it alone carries PAYLOAD_EXIT.
    Producers emit v2 only; nothing new is ever written in v1.
    """
    doc = fields(parse_canonical_json(raw, label='supervision event'),
                 {'schema', 'attempt_id', 'work_id', 'kind', 'clock', 'data'})
    if doc['schema'] not in (SUPERVISION_EVENT_V1, SUPERVISION_EVENT_V2):
        raise ValueError('supervision event schema required')
    image = doc['schema'] == SUPERVISION_EVENT_V2
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
        fields(doc['data'], {'pid', 'start_ticks', 'uid', 'cgroup', 'comm', 'exe'} if image
               else {'pid', 'start_ticks', 'uid', 'cgroup'})
        integer(doc['data']['pid'], positive=True); integer(doc['data']['start_ticks'])
        integer(doc['data']['uid'], positive=True)
        _absolute_cgroup(doc['data']['cgroup'])
        if image:
            _bounded_image(doc['data']['comm'], doc['data']['exe'])
    elif doc['kind'] == 'CONTAINER':
        from .protocol import digest
        fields(doc['data'], {'container_id', 'name', 'role', 'cgroup_parent'})
        digest(doc['data']['container_id']); identity(doc['data']['name'])
        identity(doc['data']['cgroup_parent'])
        if doc['data']['role'] not in WORK_ROLES:
            raise ValueError('installed role required')
    elif doc['kind'] == 'DEADLINE':
        # The argv instant the guardian verified against its durable reservation.
        fields(doc['data'], {'deadline_boottime_ns'})
        integer(doc['data']['deadline_boottime_ns'], positive=True)
    elif doc['kind'] == 'RESUMED':
        # Retained once per SIGUSR1 send, so a future lethal send is attributable
        # after the fact: each event carries its ordinal (send_count) and the
        # boottime of that send, plus the target's Threads/SigBlk/SigCgt read at
        # the send -- a healthy send shows the readiness block still armed
        # (SigBlk bit 9) and the no-op handler installed (SigCgt bit 9). v2's
        # comm is the probe's readiness token: the send only ever happens after
        # the payload itself declared it armed.
        from .protocol import digest
        if image:
            fields(doc['data'], {'container_id', 'pid', 'comm', 'exe', 'send_count',
                                 'send_boottime_ns', 'threads', 'sig_blk', 'sig_cgt'})
            digest(doc['data']['container_id']); integer(doc['data']['pid'], positive=True)
            integer(doc['data']['send_count'], positive=True)
            integer(doc['data']['send_boottime_ns'], positive=True)
            integer(doc['data']['threads'], positive=True)
            if doc['data']['comm'] != READINESS_TOKEN:
                raise ValueError('resume readiness token required')
            _bounded_image(doc['data']['comm'], doc['data']['exe'])
            _bounded_hex_mask(doc['data']['sig_blk'])
            _bounded_hex_mask(doc['data']['sig_cgt'])
        else:
            fields(doc['data'], {'container_id', 'pid'})
            digest(doc['data']['container_id']); integer(doc['data']['pid'], positive=True)
    elif doc['kind'] == 'PROCESS_UNOBSERVED':
        # Why a settled work never completed: no alive-verified identity was retained.
        from .protocol import digest
        fields(doc['data'], {'container_id', 'exit_code'})
        digest(doc['data']['container_id']); integer(doc['data']['exit_code'])
    elif doc['kind'] == 'PAYLOAD_EXIT':
        # Docker's terminal State for the payload container, retained on every
        # settlement path (credited, non-credited and PROCESS_UNOBSERVED alike) so
        # a non-zero exit is attributable after the fact. v2 only: no v1 journal
        # ever contained one.
        from .protocol import digest
        if not image:
            raise ValueError('payload exit requires the v2 supervision event schema')
        fields(doc['data'], {'container_id', 'exit_code', 'oom_killed', 'finished_at'})
        digest(doc['data']['container_id']); integer(doc['data']['exit_code'])
        if type(doc['data']['oom_killed']) is not bool:
            raise ValueError('payload OOM-killed flag required')
        finished_at = doc['data']['finished_at']
        if type(finished_at) is not str or not 0 < len(finished_at) <= 64:
            raise ValueError('bounded payload finish instant required')
    elif doc['kind'] == 'FAILURE':
        # A guardian's own exception, recorded before it exits without self-recovering.
        fields(doc['data'], {'reason'})
        if type(doc['data']['reason']) is not str or not doc['data']['reason'] or len(doc['data']['reason']) > 4096:
            raise ValueError('bounded guardian failure reason required')
    else:
        raise ValueError('unsupported supervision event')
    return doc


def _absolute_cgroup(value):
    from pathlib import PurePosixPath
    if (type(value) is not str or not value.startswith('/') or '..' in PurePosixPath(value).parts
            or str(PurePosixPath(value)) != value or value == '/'):
        raise ValueError('owned absolute cgroup path required')
    return value


COMM_LIMIT = 64    # the kernel's TASK_COMM_LEN is 16; a margin, never unbounded
EXE_LIMIT = 4096   # PATH_MAX; '' when the ptrace read gate refuses a foreign-UID link
INTERPRETER_NAME = 'python'  # the fixed entrypoint's basename (/opt/ops/bin/python)


def _bounded_image(comm, exe):
    """The retained process image: comm is always present; exe may be ''."""
    if type(comm) is not str or not 0 < len(comm) <= COMM_LIMIT:
        raise ValueError('bounded process comm required')
    if type(exe) is not str or len(exe) > EXE_LIMIT:
        raise ValueError('bounded process exe path required')
    return comm, exe


def _bounded_hex_mask(value):
    """A /proc/<pid>/status signal mask: up to 16 lowercase hex digits."""
    if type(value) is not str or re.fullmatch('[0-9a-f]{1,16}', value) is None:
        raise ValueError('bounded signal mask required')
    return value


def _pre_exec_init(comm):
    """runc's own init ('runc:[2:INIT]') between its UID drop and execve: not the payload."""
    return comm.startswith('runc:[')


def _interpreter_image(comm, exe):
    """True once the observed image is the exec'd interpreter or the probe's
    readiness token (the interpreter after arming the resume handshake).

    exe is authoritative when readable (own-UID processes); across UIDs the
    ptrace gate refuses the link and comm -- the basename the kernel set at
    execve, or the token the probe renamed itself to -- decides. Neither ever
    names runc's pre-exec init.
    """
    from pathlib import PurePosixPath
    if _pre_exec_init(comm):
        return False
    if comm == READINESS_TOKEN:
        return True
    return (PurePosixPath(exe).name if exe else comm).startswith(INTERPRETER_NAME)


def _retain_event(campaigns, attempt, work_id, kind, data):
    # v2 only: the guardian never writes a predecessor-shape event (S2-G5 R2).
    raw = encoded(dict(schema=SUPERVISION_EVENT_V2,
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
    return _launch(context, campaigns, state, work, enrollment, reservation_bytes)


def _launch(context, campaigns, state, work, enrollment, reservation_bytes):
    """Physical start of one durably prepared work; failure takes the R1 recovery path."""
    attempt, work_id = state['attempt_id'], work['work_id']
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


def launch_prepared_campaign_work(context, reservation_bytes, enrollment_bytes):
    """Consume one committed funded intent; START_OWNER is never claimed again.

    Only the live producer holding the materialized reservation reaches this
    tail. Runtime construction, the physical start and the R1 launch_gate ->
    acknowledge_dispatch sequence all follow the funding commit. The absolute
    campaign deadline is armed only for this tail and retired on every exit.
    """
    from .campaign_store import CampaignStore
    from .protocol import decode_base64
    campaigns = CampaignStore(context.store)
    enrollment = parse_enrollment(enrollment_bytes)
    attempt, work_id = enrollment['attempt_id'], enrollment['work_id']
    state = parse_canonical_json(campaigns.budget_snapshot(attempt), label='prepared work budget')
    work = campaigns._work(state, work_id)
    if decode_base64(work['reservation_bytes_b64']) != reservation_bytes:
        raise ValueError('work reservation identity differs')
    if work['state'] != 'START_INTENT' or work['observation_bytes_b64'] is not None:
        raise ValueError('materialized start intent required; no relaunch')
    reservation = parse_canonical_json(reservation_bytes, label='materialized reservation')
    deadline = min(state['deadline_boottime_ns'], reservation['clock']['boottime_ns'] + work['limits']['wall_ns'])
    with owned_boottime_deadline(deadline):
        return _launch(context, campaigns, state, work, enrollment, reservation_bytes)

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
        # Beside release.json: the run root is not readable by the service identity.
        enrollment_path = Path(context.config['installation_root']) / 'campaign-host.json'
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
        # memory.oom.group is owned by the system manager: it rewrites the
        # attribute on every realization and sets 1 only for OOMPolicy=kill
        # service/scope units (the guardian's own single-task cgroup), never for
        # a slice, and Docker's delegated container scope keeps 0. A payload OOM
        # is therefore a single-process kill: the guardian's poll reads this
        # parent's hierarchical memory.events and stops the payload on the first
        # oom_kill increment (campaign_supervisor._run_probe); BindsTo retires
        # the payload only when the guardian unit itself ends. The slice carries
        # the limit and the never-reset counters; settlement retains the facts.

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
            # The manager's or control child's refusal text is the only diagnostic.
            raise ValueError('bounded system-manager operation failed (exit ' + str(process.returncode) + '): '
                             + stderr[-300:].decode('utf-8', 'replace').strip())
        if re.fullmatch(rb'o "/org/freedesktop/systemd1/job/[0-9]+"\n?', stdout) is None:
            raise ValueError('system-manager job acknowledgement differs: ' + stdout[-200:].decode('utf-8', 'replace').strip())
        campaigns.acknowledge_dispatch(enrollment['attempt_id'], enrollment['work_id'],
            'guardian', permit['token'], observe_campaign_clock)
        return stdout

    def start(self, state, work, enrollment):
        from .protocol import decode_base64
        from .runtime import installed_code_root
        current = clock(observe_campaign_clock())
        reservation = parse_canonical_json(__import__('base64').b64decode(work['reservation_bytes_b64']), label='reservation')
        deadline = min(state['deadline_boottime_ns'],
                       reservation['clock']['boottime_ns'] + work['limits']['wall_ns'])
        if current['boot_id'] != state['start_clock']['boot_id'] or deadline <= current['boottime_ns']:
            raise ValueError('original deadline or boot differs')
        remaining_wall_ns = deadline - current['boottime_ns']
        orchestration_cpu_ns = state['profile']['orchestration_cpu_ns'][work['phase']]
        spec = guardian_unit_spec(enrollment['scopes'], attempt_id=state['attempt_id'], work_id=work['work_id'],
            code_root=str(installed_code_root()), interpreter=sys.executable,
            uid=self.context.config['service_uid'],
            orchestration_cpu_ns=orchestration_cpu_ns,
            remaining_wall_ns=remaining_wall_ns, cpu_ns=work['limits']['cpu_ns'],
            deadline_boottime_ns=deadline,
            tasks=guardian_task_bound(parse_work_manifest(decode_base64(enrollment['manifest_bytes_b64']))))
        from tools.qualification_verification.container_ownership import CAMPAIGN_BUS_START
        self._control([*CAMPAIGN_BUS_START, *manager_start_arguments(enrollment['scopes'], spec)], enrollment=enrollment)
        # The payload slice is ordered After the guardian and pulled in by its
        # Wants, so it is not realized when this queued-job reply returns; the
        # realized cpu.max is verified from inside the live guardian, before any
        # payload process exists (guardian_main -> _verify_payload_quota).

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


PAYLOAD_REALIZE_SECONDS = 5
RESUME_SIGNAL_SENDS = 25
# campaign_funding._funding_gate's refusal while a sibling work's bootstrap claim is
# open; the only snapshot refusal the guardian's poll re-polls through (bounded).
FUNDING_PENDING_REFUSAL = 'campaign funding pending; current authority unavailable'
FUNDING_PENDING_GRACE_SECONDS = 5.0


def _realized_payload_cpu_max(payload):
    """Bounded wait for the manager to realize the payload slice, then its cpu.max bytes."""
    deadline = time.monotonic() + PAYLOAD_REALIZE_SECONDS
    while not (payload / 'cpu.max').exists():
        if time.monotonic() >= deadline:
            raise ValueError('payload slice CPU quota was not realized: ' + str(payload))
        time.sleep(0.02)
    return _read_counter(payload / 'cpu.max')


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
def owned_boottime_deadline(deadline_ns):
    """Absolute deadline owned by one shared-qexec tail; retired in finally.

    A completed or failed request leaves no timer that could kill later work.
    This covers only the active launch tail. The guardian's own lifetime is
    covered from its first instruction by the kernel timer that bootstrap.py
    arms from the fixed argv deadline before any campaign import (formerly R4),
    re-armed and cross-checked against the durable reservation in guardian_main.
    """
    import ctypes
    libc, timer = arm_boottime_deadline(deadline_ns)
    try:
        yield
    finally:
        if libc.timer_delete(timer):
            raise OSError(ctypes.get_errno(), 'owned deadline retirement failed')


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
    # bootstrap.py already armed the absolute kernel SIGKILL timer from this value.
    parser.add_argument('--deadline-boottime-ns', required=True, type=int)
    args = parser.parse_args()
    identity(args.attempt); identity(args.work)
    config = parse_instance(encoded(load_instance(installed_code_root() / 'qualification-installation/supervisor.json')))
    if os.geteuid() != config['service_uid']:
        raise ValueError('guardian OS role differs')
    context = ExecutionService(config)
    if context.profile.values['schema'] not in ('qualification_execution_profile/v3', 'qualification_execution_profile/v4', 'qualification_execution_profile/v5'):
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
    try:
        deadline = guardian_deadline(state, work, reservation, args.deadline_boottime_ns)
    except ValueError as mismatch:
        # The armed argv instant is not this reservation's: durable uncertainty, then exit.
        _guardian_self_failure(context, campaigns, enrollment, args.attempt, args.work, mismatch)
        raise
    if now_clock['boot_id'] != state['start_clock']['boot_id'] or now_clock['boottime_ns'] >= deadline:
        _guardian_self_failure(context, campaigns, enrollment, args.attempt, args.work,
                               ValueError('original deadline reached before guardian dispatch'))
        return
    # Kept beside the bootstrap timer: a second absolute timer at the same
    # instant is harmless and this one survives any future bootstrap change.
    arm_boottime_deadline(deadline)
    _retain_event(campaigns, args.attempt, args.work, 'DEADLINE', dict(deadline_boottime_ns=deadline))
    state = _await_dispatch_ack(campaigns, args.attempt, args.work, deadline)
    _assert_authority(state)
    if state['profile'] != parse_canonical_json(context.release, label='release')['campaign_budget_profile']:
        raise ValueError('installed immutable budget profile differs')
    own_group = Path('/sys/fs/cgroup') / _process_cgroup().lstrip('/')
    expected_parent = _scope_path(runtime.parent, enrollment['scopes']['work_slice'])
    if own_group != expected_parent / enrollment['scopes']['guardian_unit']:
        raise ValueError('guardian effective cgroup membership differs')
    if (own_group / 'pids.max').read_text().strip() != str(guardian_task_bound(manifest)):
        raise ValueError('single-process controller enforcement required')
    spec = guardian_unit_spec(enrollment['scopes'], attempt_id=args.attempt, work_id=args.work,
        code_root=str(installed_code_root()), interpreter=sys.executable, uid=os.geteuid(),
        orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']],
        remaining_wall_ns=deadline-now_clock['boottime_ns'], cpu_ns=work['limits']['cpu_ns'],
        deadline_boottime_ns=deadline, tasks=guardian_task_bound(manifest))
    if resource.getrlimit(resource.RLIMIT_CPU) != (spec['guardian']['LimitCPU'], spec['guardian']['LimitCPU']):
        raise ValueError('guardian effective hard CPU limit differs')
    stat_fields = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()
    comm, exe = _process_image('self')
    _retain_event(campaigns, args.attempt, args.work, 'PROCESS',
        dict(pid=os.getpid(), start_ticks=int(stat_fields[19]), uid=os.geteuid(), cgroup=_process_cgroup(),
             comm=comm, exe=exe))
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
        elif manifest['role'] == 'n1_worker':
            _verify_payload_quota(runtime, enrollment, state, work, deadline)
            _run_n1_worker(context, campaigns, runtime, state, work, enrollment, manifest)
        elif manifest['role'] == 'n1_g5':
            _run_n1_g5(context, campaigns, runtime, state, work, enrollment, manifest)
        else:
            _verify_payload_quota(runtime, enrollment, state, work, deadline)
            _run_probe(context, campaigns, runtime, state, work, enrollment, manifest)
    except BaseException as failure:
        # The guardian never recovers its own work (that would SIGKILL itself
        # mid-cleanup and strand a spent recovery slot): commit uncertainty,
        # retain the cause, retire the payload, and re-raise. systemd's BindsTo
        # interlock retires the payload slice and the service recovers with an
        # unspent slot.
        _guardian_self_failure(context, campaigns, enrollment, args.attempt, args.work, failure)
        raise


CHECKPOINT_IO_ROOT = Path('/var/lib/fpq')


def _mount_unit_name(path):
    """systemd's mount-unit name for an absolute path (the fixed escape)."""
    from pathlib import PurePosixPath
    path = str(path)
    pure = PurePosixPath(path)
    if not pure.is_absolute() or str(pure) != path:
        raise ValueError('absolute io mount path required')
    return '-'.join(part.replace('-', '\\x2d') for part in pure.parts[1:]) + '.mount'


def checkpoint_io_paths(enrollment):
    """The work's fixed io mount paths and units, derived from the enrollment.

    POSIX strings by construction: the unit-name escape and the bind spellings
    must not depend on the host process's Path flavour.
    """
    token = sha256(encoded(enrollment))[:24]
    base = '/var/lib/fpq/fpq-' + token
    return dict(in_path=base + '/in', out_path=base + '/out',
                in_unit=_mount_unit_name(base + '/in'), out_unit=_mount_unit_name(base + '/out'))


def _guardian_bus_call(campaigns, unit, properties):
    """The guardian's own fixed systemd call through the campaign_control child.

    Same fixed command, prlimit isolation and parent-death wiring as the
    service-side start; no START_CLIENT claim -- the guardian is already the
    authorized supervisor of this work, and every call is bounded by its own
    LimitCPU plus the installed control_calls allowance.
    """
    import os
    import subprocess
    from .runtime import installed_code_root
    from tools.qualification_verification.container_ownership import CAMPAIGN_BUS_START
    # The unit's properties arrive as the same dict the service-side start uses;
    # _unit_properties performs the ssa(sv) encoding for both.
    arguments = [unit, 'fail', *_unit_properties(properties), '0']
    process = subprocess.Popen(['/usr/bin/prlimit', '--cpu=1:1', '--', sys.executable, '-I',
        str(installed_code_root() / 'bootstrap.py'), 'campaign_control', str(os.getpid()),
        *CAMPAIGN_BUS_START, *arguments],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8'})
    stdout, stderr = process.communicate(timeout=15)
    if process.returncode != 0 or len(stdout) > 65536 or len(stderr) > 65536:
        raise ValueError('bounded system-manager operation failed (exit ' + str(process.returncode) + '): '
                         + stderr[-300:].decode('utf-8', 'replace').strip())
    if re.fullmatch(rb'o "/org/freedesktop/systemd1/job/[0-9]+"\n?', stdout) is None:
        raise ValueError('system-manager job acknowledgement differs: ' + stdout[-200:].decode('utf-8', 'replace').strip())
    return stdout


def _io_mount_properties(where, *, size_bytes, uid, mode):
    return dict(What='tmpfs', Where=where, Type='tmpfs',
                Options='rw,size=%d,uid=%d,gid=%d,mode=0%o' % (size_bytes, uid, uid, mode),
                DefaultDependencies=False)


def _guardian_signal_unit(unit, signal_name):
    """The qg5 unit's resume channel -- the analogue of the probe's docker-kill
    SIGUSR1. A fixed manager command over a prlimit'd child; the polkit rule
    authorizes the host-prefixed unit and no argument is caller-supplied."""
    import os
    import subprocess
    from .runtime import installed_code_root
    # campaign_control refuses anything but StartTransientUnit, so the signal
    # rides systemctl's own manager path (polkit manage-units, host prefix).
    result = subprocess.run(['/usr/bin/systemctl', '--system', '--no-ask-password',
                             'kill', '--signal=' + signal_name, unit],
                            stdin=subprocess.DEVNULL, capture_output=True, timeout=10)
    if result.returncode != 0:
        raise ValueError('unit signal failed: ' + result.stderr.decode('utf-8', 'replace')[-300:])


def g5_unit_spec(enrollment, *, attempt_id, work_id, code_root, interpreter, g5_uid,
                 orchestration_cpu_ns, remaining_wall_ns, cpu_ns):
    """D2: the metered qg5 transient unit under the work's payload slice.

    Bounds derive from the N1_G5 phase exactly as ``guardian_unit_spec`` derives
    the guardian's from its own; the unit dies with the guardian (BindsTo) and
    its cgroup lies inside the enrolled payload slice, so the store's identity
    rule binds its retained PROCESS events like any supervised payload.
    """
    from pathlib import PurePosixPath
    identity(attempt_id); identity(work_id)
    integer(g5_uid, positive=True); integer(orchestration_cpu_ns, positive=True)
    integer(remaining_wall_ns, positive=True); integer(cpu_ns, positive=True)
    from .profile import CAMPAIGN_RESOURCE_SCOPE as policy
    helper_seconds = policy['control_calls'] * (policy['control_cpu_seconds'] + policy['cpu_granularity_seconds'])
    cpu_seconds = max(1, (cpu_ns - orchestration_cpu_ns) // 10**9 - helper_seconds)
    quota = payload_cpu_quota_usec(cpu_ns - orchestration_cpu_ns, remaining_wall_ns)
    for value in (code_root, interpreter):
        path = PurePosixPath(value)
        if not path.is_absolute() or '..' in path.parts or str(path) != value:
            raise ValueError('installed absolute runtime paths required')
    return dict(g5=dict(Type='exec', User=str(g5_uid), Slice=enrollment['payload_slice'],
        BindsTo=[enrollment['guardian_unit']], After=[enrollment['guardian_unit']],
        Restart='no', KillMode='control-group', KillSignal=9, SendSIGKILL=True,
        TimeoutStopUSec=1_000_000, RuntimeMaxUSec=max(1, remaining_wall_ns // 1000),
        LimitCPU=cpu_seconds, LimitCPUSoft=cpu_seconds, TasksMax=16,
        OOMPolicy='kill', NoNewPrivileges=True, CPUAccounting=True, MemoryAccounting=True,
        CPUQuotaPerSecUSec=quota,
        Environment=[name + '=' + value for name, value in policy['controller_environment'].items()],
        ExecStart=[interpreter, '-I', str(PurePosixPath(code_root) / 'bootstrap.py'),
                   'g5', '--attempt-id', attempt_id, '--campaign-work', work_id]))


def worker_container_body(context, enrollment, manifest):
    """D3: the probe's fixed container body extended with the work's io binds."""
    body = probe_container_body(context, enrollment, manifest)
    io = checkpoint_io_paths(enrollment)
    return dict(body,
        Entrypoint=['/opt/ops/bin/python', '-I', '/opt/qualification/bootstrap.py', 'worker'],
        Cmd=['--execution-id', manifest['work_id'], '--input', '/input', '--output', '/output',
             '--campaign-limits', 'campaign-limits.json'],
        # Unlike the harmless probes, the real worker's refusal text is the only
        # way to attribute a non-zero exit; bounded json logging, never streamed
        # as capture (the output mount is the capture path).
        HostConfig=dict(body['HostConfig'],
            Binds=[io['in_path'] + ':/input:ro', io['out_path'] + ':/output:rw'],
            LogConfig={'Type': 'json-file', 'Config': {'max-size': '2m', 'max-file': '1'}}))


def _worker_input_files(context, campaigns, state, work):
    """The work's staged input manifest: plan, limits, installation, bundle."""
    from .files import read_regular
    from .protocol import decode_base64
    from ..checkpoint_plan import derive_checkpoint_plan
    attempt = state['attempt_id']
    plan_bytes = derive_checkpoint_plan(campaigns.retained_object(attempt, 'plan'), 'N1', None)
    objects = campaigns.objects(attempt)
    release = read_regular(Path(context.config['installation_root']), 'release.json', limit=16 * 1024 * 1024)
    keys = read_regular(Path(context.config['installation_root']), 'keys.json', limit=1024 * 1024)
    reservation = parse_canonical_json(decode_base64(work['reservation_bytes_b64']), label='reservation')
    deadline = min(state['deadline_boottime_ns'], reservation['clock']['boottime_ns'] + work['limits']['wall_ns'])
    now_clock = clock(observe_campaign_clock())
    remaining_wall_ns = max(10**9, deadline - now_clock['boottime_ns'])
    limits = encoded(dict(schema='qualification_campaign_work_limits/v1', attempt_id=attempt,
        work_id=work['work_id'], phase='N1',
        limits=dict(cpu_ns=work['limits']['cpu_ns'] - state['profile']['orchestration_cpu_ns'][work['phase']],
                    wall_ns=remaining_wall_ns, memory_bytes=work['limits']['memory_bytes']),
        orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']],
        deadline_boottime_ns=deadline))
    files = [('', 'plan.json', plan_bytes), ('', 'campaign-limits.json', limits),
             ('installation', 'release.json', release), ('installation', 'keys.json', keys),
             ('bundle', 'index.json', objects['bundle_index'])]
    # Every retained bundle member lands at the path its own index declares, so
    # the worker's verify_bundle reads exactly the admitted original layout.
    index = parse_canonical_json(objects['bundle_index'], label='bundle index')
    for entry in index['entries']:
        raw = objects.get('context_' + entry['role'])
        if raw is None:
            raise ValueError('retained bundle member absent: ' + entry['role'])
        files.append(('bundle', entry['path'], raw))
    return files, plan_bytes


def _write_worker_input(enrollment, files):
    """Write the manifest into the mounted input tmpfs; the manager owns the
    mountpoint creation, so this runs only after the mount units exist."""
    in_root = Path(checkpoint_io_paths(enrollment)['in_path'])
    staged = 0
    for directory, name, raw in files:
        staged += len(raw)
        target = in_root / directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(raw)
            stream.flush()
            import os
            os.fsync(stream.fileno())
        target.chmod(0o444)
    return staged


def _capture_result_document(context, campaigns, state, work, enrollment, manifest, container_row,
                             payload_bytes, plan_bytes, staged_bytes, started_at, finished_at, authorized):
    import base64
    from .store import instant
    from .evidence import parse_worker_result
    staged_limits = parse_canonical_json((Path(checkpoint_io_paths(enrollment)['in_path']) / 'campaign-limits.json').read_bytes(),
                                          label='staged campaign limits')['limits']
    # The caller already decoded the mounted frame; payload_bytes is the
    # worker's canonical document exactly as archived.
    captured = parse_worker_result(payload_bytes, context=context, execution_id=manifest['work_id'],
                                   plan_bytes=plan_bytes, campaign_limits=staged_limits)
    image = parse_canonical_json(context.installed_release, label='release')['worker_image_digest']
    from .runtime import observe_runtime
    result = encoded(dict(schema='qualification_campaign_checkpoint_result/v1',
        attempt_id=state['attempt_id'], checkpoint='N1', work_id=manifest['work_id'],
        campaign_id=campaigns.row(state['attempt_id'])['campaign_id'],
        plan_sha256=sha256(plan_bytes), plan_byte_length=len(plan_bytes),
        payload_sha256=sha256(payload_bytes), payload_byte_length=len(payload_bytes),
        worker_execution_id=manifest['work_id'], container_id=container_row['Id'],
        worker_image_digest=image,
        runtime_manifest_sha256=sha256(encoded(parse_canonical_json(context.installed_release, label='release')['runtime_manifests']['worker'])),
        capture=dict(exit_code=container_row['State']['ExitCode'],
                     oom_killed=bool(container_row['State']['OOMKilled']),
                     started_utc=started_at, completed_utc=finished_at,
                     authorized_at_utc=authorized, campaign_scope_id=enrollment['scopes']['campaign_slice'],
                     work_scope_id=enrollment['scopes']['payload_slice'],
                     payload_slice=enrollment['scopes']['payload_slice']),
        limits=dict(cpu_ns=work['limits']['cpu_ns'], wall_ns=work['limits']['wall_ns'],
                    memory_bytes=work['limits']['memory_bytes'],
                    orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']]),
        observations=dict(exit_code=container_row['State']['ExitCode'],
                          oom_killed=bool(container_row['State']['OOMKilled']),
                          **captured.document['observations']),
        created_utc=instant(__import__('datetime').datetime.now(__import__('datetime').timezone.utc))))
    return result, captured




def _run_n1_worker(context, campaigns, runtime, state, work, enrollment, manifest):
    """The genuine N1 compute work: container with identity + handshake, capture
    from the bounded output mount, byte-for-byte archive, attestation, CAPTURED,
    settlement -- the probe's supervision loop with the real worker payload."""
    import base64
    from .protocol import digest
    docker = DockerControl()
    if docker.call('GET', '/info')['CgroupDriver'] != 'systemd':
        raise ValueError('installed Docker cgroup driver differs; no automatic switch')
    io = checkpoint_io_paths(enrollment)
    files, plan_bytes = _worker_input_files(context, campaigns, state, work)
    staged_bytes = sum(len(raw) for _, _, raw in files)
    output_bound = context.profile.output_byte_limit
    # The manager creates the mountpoints; only then may the guardian stage
    # into the input tmpfs (it cannot mkdir under /var/lib itself).
    _guardian_bus_call(campaigns, io['in_unit'],
                       _io_mount_properties(io['in_path'],
                                            # Page rounding and directory entries need real
                                            # headroom over the staged byte total or the writes
                                            # fail with EAGAIN on a full tmpfs.
                                            size_bytes=staged_bytes + staged_bytes // 2 + 65536,
                                            uid=context.config['service_uid'], mode=0o755))
    _guardian_bus_call(campaigns, io['out_unit'],
                       _io_mount_properties(io['out_path'], size_bytes=output_bound,
                                            uid=context.profile.worker_uid, mode=0o755))
    _write_worker_input(enrollment, files)
    name = 'fpqs2-' + sha256(encoded(enrollment))
    body = worker_container_body(context, enrollment, manifest)
    container = digest(docker.call('POST', '/containers/create?name=' + name, body)['Id'])
    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'CONTAINER', dict(
        container_id=container, name=name, role=manifest['role'],
        cgroup_parent=enrollment['scopes']['payload_slice']))
    row = docker.call('GET', '/containers/' + container + '/json')
    if (row['Image'] != body['Image'] or row['Config']['User'] != body['User']
            or row['Config']['Entrypoint'] != body['Entrypoint'] or row['Config']['Cmd'] != body['Cmd']
            or row['HostConfig']['CgroupParent'] != enrollment['scopes']['payload_slice']
            or row['HostConfig']['Binds'] != body['HostConfig']['Binds']):
        raise ValueError('effective fixed container configuration differs')
    seen_pids = {}
    resume_sends = 0
    oom_baseline = int(_kernel_pairs(_read_counter(runtime.parent / 'memory.events')).get('oom_kill', 0))
    stopping = False
    docker_lagging = 0
    budget_cpu = work['limits']['cpu_ns'] - state['profile']['orchestration_cpu_ns'][work['phase']]
    started_at = authorized = finished_at = None
    with campaigns.launch_gate(state['attempt_id'], work['work_id'], observe_campaign_clock, role='payload') as permit:
        authorized = clock(observe_campaign_clock())['utc']
        docker.call('POST', '/containers/' + container + '/start')
    campaigns.acknowledge_dispatch(state['attempt_id'], work['work_id'],
        'payload', permit['token'], observe_campaign_clock)
    payload_slice = _scope_path(runtime.parent, enrollment['scopes']['payload_slice'])
    while True:
        row = docker.call('GET', '/containers/' + container + '/json')
        if row['State']['Running']:
            started_at = row['State']['StartedAt']
            pid = row['State']['Pid']
            init_image = None
            try:
                actual = Path('/sys/fs/cgroup') / _process_cgroup(pid).lstrip('/')
                members = _payload_processes(actual)
                usage = _kernel_pairs(_read_counter(payload_slice / 'cpu.stat')).get('usage_usec', 0) * 1000
            except OSError:
                if docker.call('GET', '/containers/' + container + '/json')['State']['Running']:
                    docker_lagging += 1
                    if docker_lagging > 20:
                        raise
                else:
                    docker_lagging = 0
                time.sleep(.05)
                continue
            for pid_text in members:
                observed_identity = _process_identity(pid_text)
                if observed_identity is None:
                    continue
                birth, uid, cgroup, comm, exe = observed_identity
                if str(uid) != body['User'].split(':')[0]:
                    raise ValueError('effective role UID differs')
                if _pre_exec_init(comm):
                    continue
                if seen_pids.get((pid_text, birth)) != comm:
                    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PROCESS',
                        dict(pid=int(pid_text), start_ticks=birth, uid=uid, cgroup=cgroup, comm=comm, exe=exe))
                    seen_pids[(pid_text, birth)] = comm
                if pid_text == str(pid):
                    init_image = (comm, exe)
            # The probe's readiness handshake, verbatim: send SIGUSR1 only once
            # the worker renames itself to the fixed token (the bootstrap-level
            # block is verified before any compute import), re-sending within
            # the bounded window while the wait is unconsumed.
            if (not stopping and resume_sends < RESUME_SIGNAL_SENDS
                    and init_image is not None and _interpreter_image(*init_image)
                    and init_image[0] == READINESS_TOKEN):
                signals = _signal_state(str(pid))
                if signals is not None:
                    try:
                        docker.call('POST', '/containers/' + container + '/kill?signal=SIGUSR1')
                    except ValueError:
                        if docker.call('GET', '/containers/' + container + '/json')['State']['Running']:
                            raise
                    else:
                        _retain_event(campaigns, state['attempt_id'], work['work_id'], 'RESUMED',
                                      dict(container_id=container, pid=int(pid), comm=init_image[0],
                                           exe=init_image[1], send_count=resume_sends + 1,
                                           send_boottime_ns=clock(observe_campaign_clock())['boottime_ns'],
                                           threads=signals[0], sig_blk=signals[1], sig_cgt=signals[2]))
                        resume_sends += 1
            # Overrun or OOM: durable uncertainty first, then the kill; the final
            # facts are retained only after verified absence by the settlement.
            if not stopping and (usage >= budget_cpu or int(_kernel_pairs(
                    _read_counter(runtime.parent / 'memory.events')).get('oom_kill', 0)) > oom_baseline):
                _transition(campaigns, state['attempt_id'], work['work_id'], 'IN_DOUBT', {})
                docker.call('POST', '/containers/' + container + '/kill?signal=KILL')
                stopping = True
            time.sleep(.2)
            continue
        if row['State']['Pid'] != 0:
            raise ValueError('container termination has no process absence proof')
        finished_at = row['State']['FinishedAt']
        break
    exit_code = integer(row['State']['ExitCode'])
    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PAYLOAD_EXIT',
                  dict(container_id=container, exit_code=exit_code, oom_killed=row['State']['OOMKilled'],
                       finished_at=row['State']['FinishedAt']))
    if not seen_pids:
        _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PROCESS_UNOBSERVED',
                      dict(container_id=container, exit_code=exit_code))
        raise ValueError('payload exited before any alive-verified process identity; completion refused')
    state = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='worker final state')
    work = campaigns._work(state, work['work_id'])
    if exit_code != 0:
        # The bounded worker log is the only attribution for a refusal the
        # output mount cannot carry; it is retained as the failure reason.
        tail = ''
        try:
            tail = docker.call('GET', '/containers/' + container
                               + '/logs?stdout=1&stderr=1&tail=40', raw=True).decode('utf-8', 'replace')
        except ValueError:
            pass
        if work['state'] == 'RUNNING':
            _transition(campaigns, state['attempt_id'], work['work_id'], 'IN_DOUBT', {})
        _retain_event(campaigns, state['attempt_id'], work['work_id'], 'FAILURE',
                      dict(reason=('worker exited ' + str(exit_code) + ': '
                                   + tail[-3600:].strip())[:4096]))
        observed = runtime.observation(state, work, enrollment)
        parse_canonical_json(campaigns.settle_work(state['attempt_id'], work['work_id'], observed), label='settlement')
        docker.call('DELETE', '/containers/' + container + '?v=1')
        return
    # The capture: exactly the archived bytes from the bounded output mount.
    # parse_worker_result binds against the verified bundle context (the same
    # revalidation the admission branch performs), never the service object.
    from datetime import datetime, timezone
    verified = context._context(parse_canonical_json(
        campaigns.row(state['attempt_id'])['request_bytes'], label='original request')['bundle_sha256'],
        at=datetime.now(timezone.utc))
    from .files import read_regular
    from .protocol import decode_frame
    raw_frame = read_regular(Path(io['out_path']), 'result.frame', limit=output_bound)
    # The archived payload is the worker's canonical document exactly as framed
    # (the frame is transport, like the N1_ONLY stdout capture).
    payload_bytes = decode_frame(raw_frame, limit=max(1, len(raw_frame)))
    result, captured = _capture_result_document(verified, campaigns, state, work, enrollment, manifest,
                                                row, payload_bytes, plan_bytes, staged_bytes,
                                                started_at, finished_at, authorized)
    capture_transition = encoded(dict(
        schema='qualification_campaign_work_transition/v1', attempt_id=state['attempt_id'],
        work_id=work['work_id'], state='CAPTURED', clock=clock(observe_campaign_clock()),
        data=dict(capture_bytes_b64=base64.b64encode(result).decode('ascii'))))
    campaigns.retain_checkpoint_capture(state['attempt_id'], work['work_id'], result, payload_bytes,
                                        capture_transition)
    # The attestation signs exactly the archived capture, with the service's
    # enrolled execution credential; the store verifies custody on retain.
    from .signing import sign_checkpoint_attestation
    budget_state = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='capture budget')
    parsed_result = parse_canonical_json(result, label='checkpoint result')
    attestation_payload = dict(
        schema='qualification_campaign_checkpoint_attestation_payload/v1',
        scope='ATTEST_CAMPAIGN_CHECKPOINT', attempt_id=state['attempt_id'], checkpoint='N1',
        work_id=manifest['work_id'], result_sha256=sha256(result),
        payload_sha256=parsed_result['payload_sha256'],
        payload_byte_length=parsed_result['payload_byte_length'],
        plan_sha256=parsed_result['plan_sha256'], execution_release_sha256=sha256(context.release),
        profile_sha256=verified.profile.sha256,
        service_id=parse_canonical_json(context.release, label='release')['service_id'],
        worker_image_digest=parsed_result['worker_image_digest'],
        runtime_manifest_sha256=parsed_result['runtime_manifest_sha256'],
        container_id=parsed_result['container_id'],
        capture=dict(exit_code=exit_code, oom_killed=bool(row['State']['OOMKilled']),
                     campaign_scope_id=enrollment['scopes']['campaign_slice'],
                     work_scope_id=enrollment['scopes']['payload_slice'],
                     payload_slice=enrollment['scopes']['payload_slice']),
        observations=dict(exit_code=exit_code, oom_killed=bool(row['State']['OOMKilled']),
                          **captured.document['observations']),
        authorized_at_utc=authorized, started_utc=started_at, completed_utc=finished_at,
        campaign_revision=budget_state['authority_revision'])
    attestation = sign_checkpoint_attestation(attestation_payload, context=verified,
        credential_reference=context.config['execution_credential'], current_keys=context.keys())

    def _verify(attempt, result_raw, payload_raw, attestation_raw):
        from .g5 import verify_checkpoint_attestation
        verify_checkpoint_attestation(attestation_raw, context=verified, current_keys=context.keys())
        if (parse_canonical_json(attestation_raw, label='attestation')['payload']['result_sha256']
                != sha256(result_raw) or parse_canonical_json(result_raw, label='result')['payload_sha256']
                != sha256(payload_raw)):
            raise ValueError('checkpoint attestation capture binding differs')

    campaigns.retain_checkpoint_attestation(state['attempt_id'], attestation, verify=_verify)
    state = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='attested state')
    work = campaigns._work(state, work['work_id'])
    observed = runtime.observation(state, work, enrollment)
    state = parse_canonical_json(campaigns.settle_work(state['attempt_id'], work['work_id'], observed), label='settlement')
    if state['state'] == 'BOUND' and state['validity'] == 'VALID':
        _transition(campaigns, state['attempt_id'], work['work_id'], 'COMPLETED', {})
    docker.call('DELETE', '/containers/' + container + '?v=1')


def _run_n1_g5(context, campaigns, runtime, state, work, enrollment, manifest):
    """The metered qg5 unit (D2): start under the payload slice, supervise its
    identities, and settle. The assessment itself is the unit's own work over
    the service socket; credit follows the persisted candidate, never the
    unit's exit status alone."""
    from .protocol import decode_base64
    from .runtime import installed_code_root
    deadline = min(state['deadline_boottime_ns'],
                   parse_canonical_json(decode_base64(work['reservation_bytes_b64']), label='reservation')['clock']['boottime_ns']
                   + work['limits']['wall_ns'])
    now_clock = clock(observe_campaign_clock())
    remaining_wall_ns = deadline - now_clock['boottime_ns']
    spec = g5_unit_spec(enrollment['scopes'], attempt_id=state['attempt_id'], work_id=work['work_id'],
        code_root=str(installed_code_root()), interpreter=sys.executable,
        g5_uid=context.config['g5_uid'],
        orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']],
        remaining_wall_ns=remaining_wall_ns, cpu_ns=work['limits']['cpu_ns'])
    unit = enrollment['scopes']['payload_slice'][:-6] + '-g5.service'
    with campaigns.launch_gate(state['attempt_id'], work['work_id'], observe_campaign_clock, role='payload') as permit:
        _guardian_bus_call(campaigns, unit, spec['g5'])
    campaigns.acknowledge_dispatch(state['attempt_id'], work['work_id'],
        'payload', permit['token'], observe_campaign_clock)
    group = _scope_path(runtime.parent, enrollment['scopes']['payload_slice']) / unit
    seen = {}
    resumed = 0
    while True:
        current = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='current g5 authority')
        if current['state'] in ('N2_READY', 'N1_FAILED'):
            # The assessment commit's own terminal outcome: the supervised end.
            break
        _assert_authority(current)
        if not group.exists() or _kernel_pairs(_read_counter(group / 'cgroup.events')).get('populated') == 0:
            break
        init_image = None
        for pid_text in _payload_processes(group):
            observed_identity = _process_identity(pid_text)
            if observed_identity is None:
                continue
            birth, uid, cgroup, comm, exe = observed_identity
            if uid != context.config['g5_uid']:
                raise ValueError('g5 unit role UID differs')
            if seen.get(pid_text) != comm:
                _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PROCESS',
                    dict(pid=int(pid_text), start_ticks=birth, uid=uid, cgroup=cgroup, comm=comm, exe=exe))
                seen[pid_text] = comm
            init_image = (comm, exe)
        # The readiness handshake, the probe's shape: send only after the unit's
        # main renamed itself to the fixed token; the unit identity (the unit
        # name's digest) stands in for the container id in the retained event.
        if (resumed < RESUME_SIGNAL_SENDS and init_image is not None
                and _interpreter_image(*init_image) and init_image[0] == READINESS_TOKEN):
            signals = _signal_state(next(iter(seen)))
            if signals is not None:
                try:
                    _guardian_signal_unit(unit, 'SIGUSR1')
                except (OSError, ValueError):
                    pass
                else:
                    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'RESUMED',
                        dict(container_id=sha256(unit.encode('ascii')), pid=int(next(iter(seen))), comm=init_image[0],
                             exe=init_image[1], send_count=resumed + 1,
                             send_boottime_ns=clock(observe_campaign_clock())['boottime_ns'],
                             threads=signals[0], sig_blk=signals[1], sig_cgt=signals[2]))
                    resumed += 1
        time.sleep(.2)
    state = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='g5 final state')
    work = campaigns._work(state, work['work_id'])
    parent = campaigns._retry_parent(work)
    intent_held = False
    with context.store.transaction() as connection:
        intent_held = connection.execute(
            'SELECT 1 FROM full_campaign_checkpoint_intents WHERE attempt_id=?',
            (state['attempt_id'],)).fetchone() is not None
    if work['state'] == 'RUNNING' and parent is None and not intent_held:
        # The unit ended with no persisted candidate anywhere: durable
        # uncertainty. An intent-bearing work (T1 done, T2 pending) and a
        # redelivery retry settle instead -- their outcome is the signing
        # window's, not an uncertain launch.
        _transition(campaigns, state['attempt_id'], work['work_id'], 'IN_DOUBT', {})
        state = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='g5 in-doubt')
        work = campaigns._work(state, work['work_id'])
    observed = runtime.observation(state, work, enrollment)
    state = parse_canonical_json(campaigns.settle_work(state['attempt_id'], work['work_id'], observed), label='g5 settlement')
    work = campaigns._work(state, work['work_id'])
    if parent is not None:
        _transition(campaigns, state['attempt_id'], work['work_id'], 'COMPLETED', {})
    elif (work['state'] == 'SIGNED' and state['validity'] == 'VALID'
            and state['state'] in ('BOUND', 'N2_READY', 'N1_FAILED')):
        _transition(campaigns, state['attempt_id'], work['work_id'], 'COMPLETED', {})
    if parent is not None and state['state'] == 'BOUND' and state['validity'] == 'VALID':
        # The redelivered retry settled: finalize the interrupted signing with
        # the persisted candidate through the service's own commit path (the
        # caller-finalizes-after-retry order the store's serialization rule
        # demands -- SIGNED never precedes the retry's settlement).
        with context.store.transaction() as connection:
            row = connection.execute('SELECT candidate_bytes FROM full_campaign_checkpoint_intents '
                                     'WHERE attempt_id=?', (state['attempt_id'],)).fetchone()
        if row is not None:
            import base64 as _b64
            candidate = bytes(row[0])
            core = parse_canonical_json(candidate, label='persisted candidate')
            request = dict(schema='qualification_campaign_request/v2',
                operation='COMMIT_CHECKPOINT_ASSESSMENT', attempt_id=state['attempt_id'],
                checkpoint='N1', work_id=parent,
                candidate_bytes_b64=_b64.b64encode(candidate).decode('ascii'),
                artifacts=[dict(role=item['role'], sha256=item['sha256'])
                           for item in core['artifacts']])
            from .campaign_protocol import parse_campaign_request
            context._commit_checkpoint(campaigns, state['attempt_id'],
                                       parse_campaign_request(encoded(request)))


def probe_container_body(context, enrollment, manifest):
    role = manifest['role']
    if role not in WORK_ROLES[1:]:
        raise ValueError('installed harmless probe role required')
    config = context.config
    uid = {'probe_worker': context.profile.worker_uid, 'probe_g5': config['g5_uid'],
           'probe_result': config['g5_uid'], 'probe_seal': config['seal_probe_uid'],
           'n1_worker': context.profile.worker_uid, 'n1_g5': config['g5_uid']}[role]
    from .profile import CAMPAIGN_RESOURCE_SCOPE
    image = parse_canonical_json(context.release, label='installed release')['worker_image_digest']
    return dict(Image=image, User=str(uid) + ':' + str(uid), WorkingDir='/tmp',
        # Belt, not the fix: the same thread limits the controller environment
        # imposes, so the payload's compute stack (OpenBLAS inside numpy) builds
        # no pool at import; the bootstrap-level block is the actual safety net.
        # The docker create API takes Env as a list of K=V strings, exactly like
        # the guardian unit's Environment (run 35548558302: a dict is refused
        # and no container is ever created).
        Env=[name + '=' + value for name, value in CAMPAIGN_RESOURCE_SCOPE['controller_environment'].items()],
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


def _guardian_self_failure(context, campaigns, enrollment, attempt, work_id, failure):
    """The guardian's own exception path: commit uncertainty, never self-recover.

    A guardian that called recover_campaign_work on its own work would claim the
    one-use RECOVERY_OWNER slot and then have LinuxCampaignRuntime.cleanup SIGKILL
    every pid in the guardian cgroup -- itself -- before _complete_recovery ran,
    leaving an incomplete recovery row and a spent slot that permanently blocks
    the attempt. Instead: best-effort mark IN_DOUBT (no slot), retain the cause,
    best-effort retire the payload container, and let the caller re-raise. BindsTo
    retires the payload slice on exit and the service's own recovery -- with an
    unspent slot -- proves absence of the whole work group.
    """
    try:
        state = parse_canonical_json(campaigns.budget_snapshot(attempt), label='guardian failure budget')
        if campaigns._work(state, work_id)['state'] in ('START_INTENT', 'RUNNING'):
            _transition(campaigns, attempt, work_id, 'IN_DOUBT', {})
    except (OSError, ValueError, RuntimeError, sqlite3.Error):
        pass  # A terminal or unreadable work is already durable; never mask the original failure.
    try:
        reason = (type(failure).__name__ + ': ' + str(failure))[:4096] or type(failure).__name__
        _retain_event(campaigns, attempt, work_id, 'FAILURE', dict(reason=reason))
    except (OSError, ValueError, RuntimeError, sqlite3.Error):
        pass
    try:
        DockerControl().call('POST', '/containers/fpqs2-' + sha256(encoded(enrollment)) + '/kill?signal=KILL')
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
        pass  # No container yet, already gone, or BindsTo will retire the slice on exit.


def _verify_payload_quota(runtime, enrollment, state, work, deadline_ns):
    """Before any payload process exists: a finite manager rate that cannot
    exceed the payload budget over the remaining original lifetime."""
    payload = _scope_path(runtime.parent, enrollment['scopes']['payload_slice'])
    remaining_wall_ns = deadline_ns - clock(observe_campaign_clock())['boottime_ns']
    if remaining_wall_ns <= 0:
        raise ValueError('original deadline reached before payload start')
    return verify_payload_cpu_max(_realized_payload_cpu_max(payload), remaining_wall_ns=remaining_wall_ns,
        budget_cpu_ns=work['limits']['cpu_ns'] - state['profile']['orchestration_cpu_ns'][work['phase']])


def _payload_processes(group):
    return _read_counter(group / 'cgroup.procs').decode('ascii').split()


def _process_image(pid_text):
    """(comm, exe) of a live process; raises FileNotFoundError once it is gone.

    /proc/<pid>/comm is world-readable and names runc's init ('runc:[2:INIT]')
    until execve replaces it with the entrypoint's basename. /proc/<pid>/exe is
    ptrace-gated: readable for the guardian's own UID, refused (EACCES) for the
    payload's distinct UID -- then exe is '' and comm alone carries the image.
    """
    import os
    comm = Path('/proc/' + pid_text + '/comm').read_text().rstrip('\n')[:COMM_LIMIT]
    try:
        exe = os.readlink('/proc/' + pid_text + '/exe')[:EXE_LIMIT]
    except OSError:
        exe = ''  # EACCES across UIDs (or a zombie's dropped mm): never a liveness fact
    return comm, exe


def _process_identity(pid_text):
    """(start_ticks, uid, cgroup, comm, exe) read while the process is alive; None once it is gone."""
    try:
        stat_fields = Path('/proc/' + pid_text + '/stat').read_text().rsplit(')', 1)[1].split()
        status = Path('/proc/' + pid_text + '/status').read_text()
        cgroup = _process_cgroup(pid_text)
        comm, exe = _process_image(pid_text)
    except FileNotFoundError:
        return None
    uid = int(next(line for line in status.splitlines() if line.startswith('Uid:')).split()[1])
    return int(stat_fields[19]), uid, cgroup, comm, exe


def _signal_state(pid_text):
    """(Threads, SigBlk, SigCgt) of a live process; None once it is gone.

    Read at each resume send: a healthy send has the readiness block still
    armed on the leader -- SigBlk bit 9 set (SIGUSR1 blocked, inherited by
    every thread) and SigCgt bit 9 set (the no-op handler installed by
    bootstrap before any thread existed). That is the evidence the mechanism
    question needs when a send turns out lethal.

    A dead or exiting target reports None, for every payload role: a zombie
    (/proc state Z, its tables already zeroed) or an all-zero SigBlk/SigCgt/
    SigIgn triple cannot be a live payload -- bootstrap installs the handler
    before anything else and only block_resume_signal writes the readiness
    token, so a token-bearing comm is causally downstream of a nonzero SigCgt.
    Nothing is sent into, and no RESUMED image is retained for, such a
    target; the invariant then holds for every retained send without
    tolerating a dead image.
    """
    try:
        status = Path('/proc/' + pid_text + '/status').read_text()
        fields = dict(line.split(':', 1) for line in status.splitlines()
                      if line.split(':', 1)[0] in ('Threads', 'SigBlk', 'SigCgt', 'SigIgn', 'State'))
        state = fields['State'].strip().split()[0]
        blk = _bounded_hex_mask(fields['SigBlk'].strip())
        cgt = _bounded_hex_mask(fields['SigCgt'].strip())
        ign = _bounded_hex_mask(fields['SigIgn'].strip())
        # The causal gate, per the coordinator's ruling: a token-bearing comm
        # is downstream of the installed no-op handler, so a live target of a
        # resume ALWAYS shows SigCgt bit 9. A mid-exit target flushes its
        # caught handlers (cgt) before its blocked mask (blk) -- run
        # 35730345707's g5retry send#12 showed blk still 0x200 with cgt 0 --
        # so cgt-bit-9 clear, a zombie state, or an all-zero triple each mean
        # the target is gone: no send, no retained image.
        if (state == 'Z' or not (int(blk, 16) or int(cgt, 16) or int(ign, 16))
                or not int(cgt, 16) & (1 << 9)):
            return None
        return (int(fields['Threads'].strip()), blk, cgt)
    except (OSError, ValueError, KeyError, IndexError):
        return None


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
    seen_pids = {}  # (pid_text, start_ticks) -> the comm each retained PROCESS carried
    resume_sends = 0
    stopping = False
    docker_lagging = 0
    # Stop-on-OOM baseline. memory.oom.group is 1 only on the guardian's own
    # single-task cgroup; the Docker-delegated container scope keeps 0, so a
    # payload OOM kills exactly one victim while the container init survives and
    # the payload would otherwise run on to its CPU or wall bound. The parent
    # slice's hierarchical memory.events counts every descendant victim, so an
    # increment over this baseline is the plan's stop-on-OOM: settle uncertainty,
    # stop the payload, and let settlement retain the OOM facts.
    oom_baseline = int(_kernel_pairs(_read_counter(runtime.parent / 'memory.events')).get('oom_kill', 0))
    # The guardian's own CPU is charged against its LimitCPU (13 s of the 20 s
    # orchestration bound): a 25 ms loop with a full snapshot parse per turn
    # starved a 100 s two-descendant probe (S2 run 35456732049, killed at
    # 13.026 s). Poll at 200 ms and re-read authority once per second. The
    # cumulative bound is the manager's (cpu.max × RuntimeMax); this poll is
    # the early stop and the accounting path, never the enforcement.
    authority_checked = 0.0
    funding_pending_since = None
    while True:
        if not stopping and time.monotonic() - authority_checked >= 1.0:
            try:
                current = campaigns.budget_snapshot(state['attempt_id'])
            except ValueError as refusal:
                # A sibling work's claim_scheduler_bootstrap -> materialize window
                # closes the campaign's funding projection for a moment and the
                # store refuses every snapshot meanwhile (PR #436 review A4). That
                # is the sibling's transient, not this work's authority: re-poll
                # next turn, bounded by a short grace. Any other refusal (VOID,
                # recovery, dispatch) still fails closed exactly as before, and
                # _transition keeps its own unguarded read.
                if str(refusal) != FUNDING_PENDING_REFUSAL:
                    raise
                if funding_pending_since is None:
                    funding_pending_since = time.monotonic()
                elif time.monotonic() - funding_pending_since > FUNDING_PENDING_GRACE_SECONDS:
                    raise
            else:
                funding_pending_since = None
                _assert_authority(parse_canonical_json(current, label='current probe authority'))
                authority_checked = time.monotonic()
        row = docker.call('GET', '/containers/' + container + '/json')
        if row['State']['Running']:
            pid = row['State']['Pid']
            try:
                actual = Path('/sys/fs/cgroup') / _process_cgroup(pid).lstrip('/')
                escaped = not actual.is_relative_to(payload) or actual == payload
                members = [] if escaped else _payload_processes(actual)
                usage = _kernel_pairs(_read_counter(payload / 'cpu.stat')).get('usage_usec', 0) * 1000
            except OSError:
                # The container exited between this inspect and the /proc or cgroup
                # read, so its pid/cgroup entries vanished. Re-inspect: a genuinely
                # live container with unreadable accounting is a real fault, but an
                # exited one takes the ordinary absence path on the next turn -- it
                # must never raise into guardian_main's failure handler. Docker's
                # Running flag can briefly lag the cgroup scope's removal (run
                # 35482452099 work 'unseen4': the scope directory was gone while
                # inspect still said running): tolerate that bounded lag, then
                # treat a persistently unreadable running container as the fault
                # it is.
                if docker.call('GET', '/containers/' + container + '/json')['State']['Running']:
                    docker_lagging += 1
                    if docker_lagging > 20:  # ~1 s at this 50 ms cadence
                        raise
                else:
                    docker_lagging = 0
                time.sleep(.05)
                continue
            if escaped:
                raise ValueError('running container escaped payload accounting')
            init_image = None  # the init pid's (comm, exe) as read THIS turn
            for pid_text in members:
                observed_identity = _process_identity(pid_text)
                if observed_identity is None:
                    continue
                birth, uid, cgroup, comm, exe = observed_identity
                if str(uid) != body['User'].split(':')[0]:
                    raise ValueError('effective role UID differs')
                if _pre_exec_init(comm):
                    # runc's init has already dropped to the payload UID but not yet
                    # exec'd the entrypoint (a window of tens of ms after Running):
                    # it is the runtime, not the payload, so it is neither an
                    # identity nor a resume target. Poll again.
                    continue
                if seen_pids.get((pid_text, birth)) != comm:
                    # A new (pid, birth) is an alive-verified identity; a changed
                    # comm for a known one is the probe's readiness declaration
                    # (python... -> the token), which itself proves the handshake
                    # was reached and is retained as its own PROCESS event.
                    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PROCESS',
                        dict(pid=int(pid_text), start_ticks=birth, uid=uid, cgroup=cgroup, comm=comm, exe=exe))
                    seen_pids[(pid_text, birth)] = comm
                if pid_text == str(pid):
                    init_image = (comm, exe)
            # Startup handshake: bootstrap.py installs the no-op SIGUSR1 handler
            # and blocks the signal for the payload roles before any import can
            # spawn threads (OpenBLAS's pool inside the numpy import), and the
            # probe then renames itself to the fixed readiness token. The
            # guardian sends ONLY once it reads the token back from
            # /proc/<pid>/comm -- never into the interpreter-startup or
            # thread-spawning windows before the block exists (the unblocked
            # sibling there takes a fatal-default group exit, exit 138, run
            # 35543486564). The image gate is kept as a harmless second
            # condition (never runc); the exact instant the probe consumes the
            # signal in sigtimedwait is still unobservable, so USR1 is re-sent
            # for a bounded window from the first eligible send (the probe
            # collapses the pending duplicates); every send is retained as its
            # own RESUMED event with its ordinal, boottime and the target's
            # Threads/SigBlk/SigCgt, so a future lethal send is attributable.
            if (not stopping and resume_sends < RESUME_SIGNAL_SENDS
                    and init_image is not None and _interpreter_image(*init_image)
                    and init_image[0] == READINESS_TOKEN):
                signals = _signal_state(str(pid))
                if signals is not None:
                    try:
                        docker.call('POST', '/containers/' + container + '/kill?signal=SIGUSR1')
                    except ValueError:
                        if docker.call('GET', '/containers/' + container + '/json')['State']['Running']:
                            raise
                    else:
                        _retain_event(campaigns, state['attempt_id'], work['work_id'], 'RESUMED',
                                      dict(container_id=container, pid=int(pid), comm=init_image[0],
                                           exe=init_image[1], send_count=resume_sends + 1,
                                           send_boottime_ns=clock(observe_campaign_clock())['boottime_ns'],
                                           threads=signals[0], sig_blk=signals[1], sig_cgt=signals[2]))
                        resume_sends += 1
            if not stopping and (usage >= budget_cpu or int(_kernel_pairs(
                    _read_counter(runtime.parent / 'memory.events')).get('oom_kill', 0)) > oom_baseline):
                # Overrun or OOM: durable uncertainty first, then stop the payload;
                # the final actual usage/OOM facts are retained only after verified
                # absence, by the settlement below.
                _transition(campaigns, state['attempt_id'], work['work_id'], 'IN_DOUBT', {})
                docker.call('POST', '/containers/' + container + '/kill?signal=KILL')
                stopping = True
            time.sleep(.2)
            continue
        if row['State']['Pid'] != 0:
            raise ValueError('container termination has no process absence proof')
        break
    exit_code = integer(row['State']['ExitCode'])
    # Docker's terminal State, retained before any settlement decision on every
    # path (credited, non-credited, PROCESS_UNOBSERVED): a non-zero exit is then
    # attributable after the fact instead of indistinguishable from a crash.
    _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PAYLOAD_EXIT',
                  dict(container_id=container, exit_code=exit_code, oom_killed=row['State']['OOMKilled'],
                       finished_at=row['State']['FinishedAt']))
    if not seen_pids:
        # Identity gate: no alive-verified UID/cgroup was ever retained for this
        # work, so nothing may be credited. The refusal takes the R1 recovery
        # path (measured settlement, IN_DOUBT); the retained reason survives it.
        _retain_event(campaigns, state['attempt_id'], work['work_id'], 'PROCESS_UNOBSERVED',
                      dict(container_id=container, exit_code=exit_code))
        raise ValueError('payload exited before any alive-verified process identity; completion refused')
    # A non-zero exit (e.g. the shared-memory OOM kill) still settles its measured
    # observation -- which retains the OOM and drives the campaign terminal -- but
    # is never credited: CAPTURED/SIGNING_INTENT/COMPLETED below are gated on
    # exit_code == 0, and a started work has no legal ABORTED transition.
    state = parse_canonical_json(campaigns.budget_snapshot(state['attempt_id']), label='probe final state')
    work = campaigns._work(state, work['work_id'])
    capture = encoded(dict(schema='qualification_campaign_probe_capture/v1',
                           container_id=container, exit_code=exit_code, role=manifest['role']))
    if work['state'] == 'RUNNING' and exit_code == 0 and campaigns._retry_parent(work) is None:
        import base64
        state = _transition(campaigns, state['attempt_id'], work['work_id'], 'CAPTURED',
                            dict(capture_bytes_b64=base64.b64encode(capture).decode()))
    if manifest['probe'] == 'intent' and exit_code == 0:
        import base64
        state = _transition(campaigns, state['attempt_id'], work['work_id'], 'SIGNING_INTENT',
            dict(intent_id=work['work_id']+'-intent', payload_bytes_b64=base64.b64encode(b'S2 harmless fixed intent').decode(),
                 key_id='TEST_ONLY_NO_CREDENTIAL', signing_at_utc=clock(observe_campaign_clock())['utc']))
    if exit_code != 0 and work['state'] == 'RUNNING' and campaigns._retry_parent(work) is None:
        # PR #436 review A2: a non-credited exit must not sit as a settled RUNNING
        # work under a VALID campaign (the store would still accept CAPTURED on
        # it, and only an unrelated restart flipped it). Durable uncertainty
        # BEFORE the measured settlement, as the overrun/OOM stop already does.
        # A linked signing retry has no legal negative transition for a started
        # work (only restart recovery ABORTs it), so it keeps the settle-only shape.
        state = _transition(campaigns, state['attempt_id'], work['work_id'], 'IN_DOUBT', {})
    observed = runtime.observation(state, work, enrollment)
    state = parse_canonical_json(campaigns.settle_work(state['attempt_id'], work['work_id'], observed), label='probe settlement')
    if state['state'] == 'BOUND' and state['validity'] == 'VALID' and exit_code == 0 and manifest['probe'] != 'intent':
        _transition(campaigns, state['attempt_id'], work['work_id'], 'COMPLETED', {})
    docker.call('DELETE', '/containers/' + container + '?v=1')


def recover_campaign_work(context, reservation_bytes, *, attempt_id, work_id):
    """One bounded recovery owner; destructive retries need an unspent slot.

    A work still RESERVED with no enrollment and no recovery row never reached
    START_INTENT and so produced no OS effect (prepare_campaign_work commits the
    enrollment and the START_INTENT transition atomically). Spending the one-use
    RECOVERY_OWNER slot to record its absence is noise that would block a later
    genuine recovery, so refuse before the claim and report status instead; a
    legacy recovery row on such a work is not noise and keeps the spent-slot
    refusal. The same status-only skip holds for SETTLED work (completed, or
    uncertainty already settled by an observation) whose recovery already
    completed with no continuation need: a service restart must not manufacture
    a second recovery for finished history -- re-claiming would flip the
    completed row to continuation_required and bar the attempt's positive
    authority for good. Unsettled work keeps today's deliberate unfunded
    barrier: a genuine new destructive need after a completed recovery still
    finds the spent slot and refuses.
    """
    from .campaign_store import CampaignStore
    import secrets
    campaigns = CampaignStore(context.store)
    with campaigns.store.transaction() as connection:
        state = campaigns._budget(connection, attempt_id)
        work = campaigns._work(state, work_id)
        enrolled = connection.execute(
            'SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role=?',
            (attempt_id, 'supervision_' + work_id)).fetchone() is not None
        recovered = next((r for r in state.get('recoveries', ()) if r['work_id'] == work_id), None)
    settled = work['state'] == 'COMPLETED' or work['observation_bytes_b64'] is not None
    if work['state'] == 'RESERVED' and not enrolled and recovered is None:
        return encoded(campaigns.diagnostic_status(attempt_id))
    if (settled and recovered is not None and recovered['completion_bytes_b64'] is not None
            and not recovered['continuation_required']):
        return encoded(campaigns.diagnostic_status(attempt_id))
    with controller_cpu_guard():
        token = secrets.token_bytes(32)
        campaigns.claim_supervision_control(attempt_id, work_id,
            'RECOVERY_OWNER', observe_campaign_clock(), recovery_owner_token=token)
        return _recover_campaign_work(context, reservation_bytes, attempt_id=attempt_id, work_id=work_id,
                                      recovery_owner_token=token)
