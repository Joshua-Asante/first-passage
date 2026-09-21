"""Targeted S2 OS evidence. Run alone, --workers 1, on an enrolled S2 host.

Simulated counters cannot satisfy these assertions. The last case intentionally
terminates the common memory group; its contamination requires a fresh host.
Every probe goes through the warm installed service's funded private route via
the forked transport child; no per-request scheduler process exists.
"""
import base64
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import time
import pytest
from tools.qualification_verification import host
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_supervisor import (
    DockerControl, _scope_path, work_enrollment, host_slice)
from c1_rail.qualification.execution.protocol import sha256

CPU_GRANULARITY_NS = 1_000_000_000  # CAMPAIGN_RESOURCE_SCOPE cpu_granularity_seconds


def snapshot(boundary, attempt):
    with sqlite3.connect((boundary.root/'data/journal.sqlite').as_uri()+'?mode=ro',uri=True) as connection:
        row=connection.execute('SELECT snapshot_bytes FROM full_campaign_budgets WHERE attempt_id=?',(attempt,)).fetchone()
    return json.loads(row[0])


def work(state, work_id):
    """Select by explicit identity; works are stored sorted by work_id, never by age."""
    return next(w for w in state['works'] if w['work_id']==work_id)


def has_work(state, work_id):
    return any(w['work_id']==work_id for w in state['works'])


def wait(boundary,attempt,predicate,seconds=330):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        value=snapshot(boundary,attempt)
        if predicate(value):
            host.save(boundary.output/(attempt+'-budget.json'),value)
            return value
        time.sleep(.1)
    raise AssertionError('bounded real supervision wait expired')


def boottime_ns():
    return time.clock_gettime_ns(time.CLOCK_BOOTTIME)


def work_deadline(state,work_id):
    """The instant the service put on the guardian argv and the guardian re-derives."""
    row=work(state,work_id)
    reservation=json.loads(base64.b64decode(row['reservation_bytes_b64']))
    return min(state['deadline_boottime_ns'],reservation['clock']['boottime_ns']+row['limits']['wall_ns'])


def supervision_events(boundary,attempt,kind=None,work_id=None):
    with sqlite3.connect((boundary.root/'data/journal.sqlite').as_uri()+'?mode=ro',uri=True) as connection:
        rows=[json.loads(bytes(row[0])) for row in connection.execute(
            "SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role GLOB 'supervision_event_*'",(attempt,))]
    return [row for row in rows if (kind is None or row['kind']==kind) and (work_id is None or row['work_id']==work_id)]


def payload_process_events(boundary,attempt,work_id):
    """Alive-verified PROCESS identities INSIDE the work's payload slice.

    The guardian retains its own startup identity under the same kind/work_id
    (cgroup = the guardian unit, outside the payload slice); that event proves
    the guardian, never the payload. Payload identity is proven by an observed
    cgroup component matching the enrolled payload slice (the container scope
    beneath it) -- run 35482452099 retained both kinds for one work.
    """
    marker='/'+work_enrollment(boundary.root.name,attempt,work_id)['payload_slice']+'/'
    return [e for e in supervision_events(boundary,attempt,'PROCESS',work_id)
        if marker in e['data']['cgroup']]


INTERPRETER_NAME='python'  # the fixed entrypoint's basename
READINESS_TOKEN='fpq-armed'  # campaign_probe.READINESS_TOKEN: comm after the block is armed


def interpreter_image(event):
    """A retained PROCESS image: the interpreter's own comm until the probe
    renames itself to the readiness token (after block_resume_signal armed the
    block and handler); never runc's init, whose comm names 'runc:['.

    exe is authoritative when the guardian could read the link (its own UID:
    the admission guardian); the payload runs as a distinct UID, so the ptrace
    gate refuses /proc/<pid>/exe there and exe is '' -- comm then carries the
    image. A PROCESS carrying the token proves the probe reached the handshake.
    """
    comm,exe=event['data']['comm'],event['data']['exe']
    assert isinstance(comm,str) and comm and not comm.startswith('runc:['), event
    assert isinstance(exe,str), event
    if comm!=READINESS_TOKEN:
        name=exe.rsplit('/',1)[-1] if exe else comm
        assert name.startswith(INTERPRETER_NAME), event
    return comm,exe


def resumed_image(event):
    """Every retained SIGUSR1 send: comm IS the readiness token (the send only
    ever happens after the payload declared itself armed), and the per-send
    facts are present -- ordinal, boottime, the target's Threads, and the
    signal masks of a healthy send: SigBlk bit 9 set (SIGUSR1 blocked, the
    bootstrap-level mask every thread inherited) and SigCgt bit 9 set (the
    no-op handler installed before any thread existed) -- the S2-G5 addendum's
    mechanism evidence."""
    comm,exe=event['data']['comm'],event['data']['exe']
    assert comm==READINESS_TOKEN, event
    assert isinstance(exe,str), event
    assert isinstance(event['data']['send_count'],int) and event['data']['send_count']>=1, event
    assert isinstance(event['data']['send_boottime_ns'],int) and event['data']['send_boottime_ns']>0, event
    assert isinstance(event['data']['threads'],int) and event['data']['threads']>=1, event
    for mask in ('sig_blk','sig_cgt'):
        assert isinstance(event['data'][mask],str) and event['data'][mask], event
    # The handler is the safety fact: with SIGUSR1 caught, complete_signal's
    # fatal branch is closed on every send, whatever the blocked mask reads.
    assert int(event['data']['sig_cgt'],16)&(1<<9), event  # SIGUSR1 caught
    # The blocked mask is NOT invariant across sends: while the payload sleeps in
    # sigtimedwait the kernel temporarily removes the awaited set from its
    # blocked mask (do_sigtimedwait: tsk->blocked &= ~mask, the original kept in
    # real_blocked) so the arrival wakes it, and /proc/<pid>/status reports that
    # temporary mask. The first send is the one that lands during the wait, so
    # its SigBlk may read 0; every later send finds the restored process-wide
    # block (run 35552151992: send 1 SigBlk=0 / SigCgt=0x202 on all eight
    # payloads, sends 2-25 SigBlk=0x200).
    if event['data']['send_count']>1:
        assert int(event['data']['sig_blk'],16)&(1<<9), event  # SIGUSR1 blocked
    return comm,exe


def identity_retained(boundary,attempt,work_id):
    """Completion credit requires a supervisor-retained, alive-verified PROCESS
    identity: a payload-scope identity for container-supervised probe works; the
    admission work has no container, so its guardian IS the supervised process.
    Every retained identity carries the exec'd interpreter image (G3)."""
    if work_id=='admission':
        events=supervision_events(boundary,attempt,'PROCESS',work_id)
    else:
        events=payload_process_events(boundary,attempt,work_id)
    assert events,'no alive-verified PROCESS event retained for '+attempt+':'+work_id
    for event in events:
        comm,exe=interpreter_image(event)
        if work_id=='admission':
            assert exe, event  # the guardian reads its own link; only foreign UIDs are refused
    for event in supervision_events(boundary,attempt,'RESUMED',work_id):
        resumed_image(event)
    return events


def payload_exit_retained(boundary,attempt,work_id):
    """Docker's terminal State for the work's container, retained by the guardian
    on every settlement path; bound to the retained CONTAINER event."""
    containers=[e['data']['container_id'] for e in supervision_events(boundary,attempt,'CONTAINER',work_id)]
    exits=[e['data'] for e in supervision_events(boundary,attempt,'PAYLOAD_EXIT',work_id)]
    assert len(containers)==1 and len(exits)==1, (containers,exits)
    assert exits[0]['container_id']==containers[0], (containers,exits)
    assert isinstance(exits[0]['exit_code'],int) and isinstance(exits[0]['oom_killed'],bool), exits
    assert isinstance(exits[0]['finished_at'],str) and exits[0]['finished_at'], exits
    return exits[0]


def unit_facts(unit,properties):
    values=host.run(['/usr/bin/systemctl','show',unit,'--property='+','.join(properties)])
    return dict(line.split('=',1) for line in values.splitlines())


def scope_group(boundary,scopes,key):
    """Absolute cgroup directory of one enrolled scope beneath the host slice."""
    parent=Path('/sys/fs/cgroup')/host_slice(boundary.root.name)
    if key=='guardian_unit':
        return _scope_path(parent,scopes['work_slice'])/scopes['guardian_unit']
    return _scope_path(parent,scopes[key])


def admit(boundary):
    """The local admin client in the existing client role is the only submitter."""
    assert boundary.diagnostic, 'FP_QUALIFICATION_S2=1 required; never upgrade N1 fixture'
    bundle=boundary.prepare(idle=True)
    fields=dict(schema='qualification_campaign_request/v2',request_id='diagnostic',
        attempt_id=bundle['attempt_id'],bundle_sha256=bundle['bundle_sha256'])
    first=json.loads(boundary.request('SUBMIT_E1',**fields))
    assert first['schema']=='qualification_campaign_status/v2', first
    state=wait(boundary,bundle['attempt_id'],lambda s: work(s,'admission')['state']=='COMPLETED' or s['state'].startswith('BUDGET_'))
    assert state['state']=='BOUND', state
    assert state['settled_cpu_ns']==20_000_000_000
    assert json.loads(boundary.request('SUBMIT_E1',**fields))['schema']=='qualification_campaign_status/v2'
    identity_retained(boundary,bundle['attempt_id'],'admission')
    # The argv deadline bootstrap armed is the one the guardian verified against the store.
    deadlines=[e['data']['deadline_boottime_ns'] for e in supervision_events(boundary,bundle['attempt_id'],'DEADLINE','admission')]
    assert deadlines==[work_deadline(state,'admission')], deadlines
    return bundle['attempt_id']


def schedule_document(attempt,work_id,role='probe_worker',kind='noop',retry=None):
    return dict(schema='qualification_campaign_schedule_request/v1',attempt_id=attempt,
        work_id=work_id,role=role,probe=kind,signing_retry_of=retry)


def probe(boundary,attempt,work_id,role='probe_worker',kind='noop',retry=None):
    reply=boundary.schedule(schedule_document(attempt,work_id,role,kind,retry))
    assert reply['ok'], reply
    return reply


def test_s2_sequential_roles_share_one_allowance(real_boundary):
    boundary=real_boundary
    attempt=admit(boundary)
    images={}
    for work_id,role in [('one','probe_worker'),('two','probe_g5'),('three','probe_result'),('four','probe_seal')]:
        before=snapshot(boundary,attempt)
        probe(boundary,attempt,work_id,role)
        after=wait(boundary,attempt,lambda s:has_work(s,work_id) and work(s,work_id)['state']=='COMPLETED')
        observed=json.loads(base64.b64decode(work(after,work_id)['observation_bytes_b64']))
        assert observed['cpu_ns']>0
        assert after['settled_cpu_ns']-before['settled_cpu_ns']==observed['cpu_ns']+20_000_000_000
        assert after['start_clock']==before['start_clock']
        assert after['deadline_boottime_ns']==before['deadline_boottime_ns']
        # G3: the retained payload identity and the resume both name the exec'd
        # interpreter, and the credited path retains docker's clean exit.
        identity_retained(boundary,attempt,work_id)
        exit_facts=payload_exit_retained(boundary,attempt,work_id)
        assert exit_facts['exit_code']==0 and not exit_facts['oom_killed'], exit_facts
        images[work_id]=dict(
            process=[(e['data']['pid'],e['data']['comm'],e['data']['exe']) for e in payload_process_events(boundary,attempt,work_id)],
            resumed=[(e['data']['pid'],e['data']['comm'],e['data']['exe']) for e in supervision_events(boundary,attempt,'RESUMED',work_id)],
            payload_exit=exit_facts)
    images['admission']=[(e['data']['pid'],e['data']['comm'],e['data']['exe'])
        for e in supervision_events(boundary,attempt,'PROCESS','admission')]
    host.save(boundary.output/(attempt+'-payload-images.json'),images)
    boundary.restart()
    assert snapshot(boundary,attempt)['settled_cpu_ns']==after['settled_cpu_ns']


def test_s2_two_descendants_exhaust_owned_cpu(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'descendants',kind='descendants')
    scopes=work_enrollment(boundary.root.name,attempt,'descendants')
    # The manager rate-limits the payload slice to budget/wall (cpu.max), so two
    # burners reach the payload budget no earlier than the original deadline.
    # Either the guardian's early stop lands in the last granule (IN_DOUBT with
    # the measured charge) or its absolute timer ends it first and BindsTo
    # retires the payload; recovery then spends the reservation. Both outcomes
    # leave the work IN_DOUBT with a charge at or above the reservation.
    end=time.monotonic()+330
    while time.monotonic()<end:
        state=snapshot(boundary,attempt)
        facts=unit_facts(scopes['guardian_unit'],['ActiveState','Result','ExecMainStatus'])
        if (state['state'].startswith('BUDGET_') or facts['ActiveState'] in ('failed','inactive')
                or (state['state']=='IN_DOUBT' and work(state,'descendants')['observation_bytes_b64'] is not None)):
            break
        time.sleep(.5)
    else:
        raise AssertionError('bounded descendants wait expired')
    # G3: whenever the guardian itself settled the work (its overrun stop landed
    # before its absolute timer), docker's terminal State for the stopped payload
    # was retained before that settlement -- a stopped payload never exits 0. On
    # the timer path the guardian died mid-loop and no settlement exists to bind.
    settled_by_guardian=work(state,'descendants')['observation_bytes_b64'] is not None
    exit_facts=None
    if settled_by_guardian:
        exit_facts=payload_exit_retained(boundary,attempt,'descendants')
        assert exit_facts['exit_code']!=0, exit_facts
    identity_retained(boundary,attempt,'descendants')
    host.save(boundary.output/(attempt+'-descendants-facts.json'),dict(facts=facts,state=state['state'],
        settled_by_guardian=settled_by_guardian,payload_exit=exit_facts))
    boundary.restart()
    state=snapshot(boundary,attempt)
    assert work(state,'descendants')['state']=='IN_DOUBT'
    assert work(state,'descendants')['charge_cpu_ns']>=work(state,'descendants')['limits']['cpu_ns']
    assert state['state'] in ('IN_DOUBT','BUDGET_EXHAUSTED','BUDGET_UNCERTAIN'), state['state']


def test_s2_fixed_intent_retry_is_charged_separately(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'intent','probe_seal','intent')
    first=wait(boundary,attempt,lambda s:has_work(s,'intent') and work(s,'intent')['state']=='SIGNING_INTENT' and work(s,'intent')['observation_bytes_b64'] is not None)
    parent=work(first,'intent')
    probe(boundary,attempt,'retry','probe_seal',retry='intent')
    after=wait(boundary,attempt,lambda s:has_work(s,'retry') and work(s,'retry')['state']=='COMPLETED')
    assert after['settled_cpu_ns']>=first['settled_cpu_ns']+20_000_000_000
    assert work(after,'intent')==parent
    assert after['authority_head']==first['authority_head']


def test_s2_guardian_death_recovers_before_cleanup(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'wall',kind='wall')
    wait(boundary,attempt,lambda s:has_work(s,'wall') and work(s,'wall')['state']=='RUNNING')
    scopes=work_enrollment(boundary.root.name,attempt,'wall')
    host.run(['/usr/bin/systemctl','kill','--signal=KILL',scopes['guardian_unit']])
    boundary.restart()
    state=snapshot(boundary,attempt)
    assert work(state,'wall')['state']=='IN_DOUBT'
    assert state['state']=='BUDGET_UNCERTAIN'
    assert work(state,'wall')['charge_cpu_ns']==work(state,'wall')['limits']['cpu_ns']


def test_s2_original_deadline_survives_service_downtime(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'deadline',kind='wall')
    first=wait(boundary,attempt,lambda s:has_work(s,'deadline') and work(s,'deadline')['state']=='RUNNING')
    host.run(['/usr/bin/systemctl','kill','--signal=KILL',host_slice(boundary.root.name)[:-6]+'supervisor.service'])
    time.sleep(305)
    boundary.restart()
    state=snapshot(boundary,attempt)
    assert state['start_clock']==first['start_clock']
    assert state['deadline_boottime_ns']==first['deadline_boottime_ns']
    assert state['state'] in ('BUDGET_EXHAUSTED','BUDGET_UNCERTAIN')


def test_s2_kernel_bounds_guardian_cpu_before_recovery(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'controller','probe_seal','controller_cpu')
    scopes=work_enrollment(boundary.root.name,attempt,'controller')
    deadline=time.monotonic()+40
    while time.monotonic()<deadline:
        values=host.run(['/usr/bin/systemctl','show',scopes['guardian_unit'],
            '--property=ActiveState,CPUUsageNSec,ExecMainStatus,LimitCPU,LimitCPUSoft'])
        facts=dict(line.split('=',1) for line in values.splitlines())
        if facts['ActiveState']=='failed': break
        time.sleep(.1)
    host.save(boundary.output/(attempt+'-guardian-limit.json'),facts)
    assert facts['ActiveState']=='failed' and facts['ExecMainStatus']=='9'
    assert facts['LimitCPU']==facts['LimitCPUSoft']=='13'
    # RLIMIT_CPU is enforced by the kernel on its own tick; the manager's
    # CPUUsageNSec is a separate cgroup sample taken after the kill and can sit
    # a few ms under the limit (run 35463688322: 12.998549 s). Allow one
    # scheduler tick below, never above the granularity margin.
    assert 13_000_000_000-10_000_000<=int(facts['CPUUsageNSec'])<=14_000_000_000
    boundary.restart()
    assert work(snapshot(boundary,attempt),'controller')['state']=='IN_DOUBT'


def test_s2_private_route_is_service_peer_only_and_bounded_in_framing(real_boundary):
    """Actual SO_PEERCRED: a client-role peer never reaches the store; oversize frames die in framing."""
    boundary=real_boundary; attempt=admit(boundary)
    before=snapshot(boundary,attempt)
    refused=boundary.schedule(schedule_document(attempt,'foreign'),role='qclient')
    assert refused['ok'] is False and refused['error']=='PEER_NOT_AUTHORIZED', refused
    with pytest.raises(ValueError):
        boundary.raw_request(schedule_document(attempt,'foreign'))
    with pytest.raises(ValueError):
        boundary.schedule(dict(schedule_document(attempt,'foreign'),work_id='w'*2000))
    assert snapshot(boundary,attempt)==before
    assert not has_work(before,'foreign')
    host.save(boundary.output/(attempt+'-private-route-refusals.json'),dict(peer=refused))


def test_s2_warm_service_starts_one_guardian_per_work_with_no_scheduler_unit(real_boundary):
    """No per-request scheduler unit or driver; duplicates are historical; one guardian start, common hierarchy."""
    boundary=real_boundary; attempt=admit(boundary)
    scopes=work_enrollment(boundary.root.name,attempt,'once')
    first=probe(boundary,attempt,'once')
    assert json.loads(base64.b64decode(first['data_b64']))['schema']=='qualification_campaign_status/v2', first
    # The guardian transient unit is garbage-collected within a sub-second of
    # completion, so sample its slice/restart facts while it is still realized
    # rather than after COMPLETED (an empty read is the GC race, not a fault).
    facts={}
    live_deadline=time.monotonic()+330
    while time.monotonic()<live_deadline:
        values=host.run(['/usr/bin/systemctl','show',scopes['guardian_unit'],'--property=NRestarts,Slice,ControlGroup'])
        facts=dict(line.split('=',1) for line in values.splitlines())
        if facts.get('Slice')==scopes['work_slice']: break
        if work(snapshot(boundary,attempt),'once')['state']=='COMPLETED': break
        time.sleep(.02)
    duplicate=probe(boundary,attempt,'once')
    assert json.loads(base64.b64decode(duplicate['data_b64']))['schema']=='qualification_campaign_scheduler_status/v1', duplicate
    after=wait(boundary,attempt,lambda s:has_work(s,'once') and work(s,'once')['state']=='COMPLETED')
    prefix=host_slice(boundary.root.name)[:-6]
    units=host.run(['/usr/bin/systemctl','list-units','--all','--no-legend','--plain',prefix+'*'])
    assert 'scheduler' not in units, units
    assert not list((boundary.code/'tests/integration/qualification_boundary').glob('*driver*.py'))
    dispatches=[row for row in after['dispatches'] if row['work_id']=='once' and row['role']=='guardian']
    assert len(dispatches)==1 and dispatches[0]['acknowledged_clock'] is not None
    # Slice/NRestarts are corroborating; the unit may already be GC'd (empty read).
    assert facts.get('NRestarts') in ('0','')
    assert facts.get('Slice') in (scopes['work_slice'],'')
    assert facts.get('ControlGroup','')=='' or ('/'+host_slice(boundary.root.name)) in facts['ControlGroup']
    owner_role='supervision_control_'+sha256(encoded(['once','START_OWNER']))
    with sqlite3.connect((boundary.root/'data/journal.sqlite').as_uri()+'?mode=ro',uri=True) as connection:
        owners=connection.execute('SELECT count(*) FROM full_campaign_objects WHERE attempt_id=? AND role=?',(attempt,owner_role)).fetchone()[0]
        intents=connection.execute('SELECT work_id FROM full_campaign_bootstraps WHERE attempt_id=?',(attempt,)).fetchall()
    assert owners==1 and [row[0] for row in intents]==['once']
    host.save(boundary.output/(attempt+'-warm-route.json'),dict(first=first,duplicate=duplicate,units=units,facts=facts,control_objects=owners))


UNOBSERVED_EXIT_ATTEMPTS = 10


def _owned_container(work_id):
    """(id, docker lifecycle state) of the one owned container, or (None, None).

    The listing shows the container from `docker create` onward, so its first
    sighting is usually the 'created' phase -- before the guardian ever starts
    or observes it.
    """
    from urllib.parse import quote
    filters={'label':['fp.s2.work='+work_id]}
    rows=DockerControl().call('GET','/containers/json?all=1&filters='+quote(json.dumps(filters),safe=''))
    return (rows[0]['Id'],rows[0]['State']) if rows else (None,None)


def _kill_before_observation(boundary,attempt,work_id):
    """Kill the owned container while it is RUNNING, racing the guardian's first poll.

    The kill must not fire at the 'created' sighting: docker rejects a kill of a
    created container (409 no-op -- run 35476561750's unguarded version failed
    exactly there), and stopping there would systematically hand the race to the
    guardian, which only observes once the container runs. Waits for 'running',
    kills within one poll tick (~1 ms cadence), and treats an 'exited' sighting
    as a lost attempt.

    A lost attempt is one where the guardian retained a PAYLOAD-scope identity
    (cgroup inside the payload slice) -- never the guardian's own startup
    PROCESS event, which every attempt retains under the same kind/work_id (run
    35482452099 discarded four won races that way).

    Returns the container id when the guardian settled the work without ever
    retaining a payload identity; None when the guardian observed it first (that
    work then settles without completion credit and the caller retries).
    """
    docker=DockerControl()
    probe(boundary,attempt,work_id)
    container=None
    end=time.monotonic()+30
    def kill(cid):
        try:
            docker.call('POST','/containers/'+cid+'/kill?signal=KILL')
        except ValueError:
            pass  # Exited between the sighting and the kill: this attempt lost.
    while time.monotonic()<end:
        container,state=_owned_container(work_id)
        if container is not None:
            if state=='running':
                kill(container); break
            if state=='exited':
                break  # Ran and ended before the kill could land; a lost attempt.
            # 'created': the guardian has not started it yet; keep the race open.
        time.sleep(.001)
    else:
        raise AssertionError('owned container never reached a running state')
    # The guardian settles a non-zero exit by committing its OBSERVATION while the
    # work state itself stays RUNNING -- the IN_DOUBT transition lands at restart
    # recovery (settle_work never transitions work state; run 35482452099's
    # 'unseen5' sat settled-RUNNING and timed out a state-only predicate). So the
    # settled predicate is the observation, plus the two terminal work states.
    def settled(s):
        row=work(s,work_id)
        return row['state'] in ('COMPLETED','IN_DOUBT') or row['observation_bytes_b64'] is not None
    try:
        state=wait(boundary,attempt,settled,seconds=120)
    except AssertionError:
        # Timeout diagnostics BEFORE any restart/cleanup alters the durable view.
        scopes=work_enrollment(boundary.root.name,attempt,work_id)
        diagnostics=dict(state=snapshot(boundary,attempt),events=[
            dict(kind=e['kind'],utc=e['clock']['utc'],data=e['data'])
            for e in supervision_events(boundary,attempt,None,work_id)],
            unit_facts=unit_facts(scopes['guardian_unit'],['ActiveState','Result','ExecMainStatus','SubState']))
        try:
            diagnostics['container']=docker.call('GET','/containers/'+container+'/json')
        except ValueError:
            diagnostics['container']='unavailable'
        host.save(boundary.output/(attempt+'-unobserved-timeout.json'),diagnostics)
        raise
    if payload_process_events(boundary,attempt,work_id):
        return None  # The guardian observed the payload before the host kill landed.
    assert work(state,work_id)['state']=='IN_DOUBT' or work(state,work_id)['observation_bytes_b64'] is not None, state
    return container


def recovery_row(state,work_id):
    return next((r for r in state.get('recoveries',()) if r['work_id']==work_id),None)


def test_s2_probe_that_exits_before_observation_never_completes(real_boundary):
    """A container that exits before any alive-verified identity is retained is never
    credited, and the guardian's own exception leaves no incomplete recovery row."""
    boundary=real_boundary
    # One probe work per phase per campaign ('compute phase already reserved'), so
    # each shot is a FRESH ADMIT (run 35478031666: the guarded no-op kill let the
    # guardian observe unseen0 to COMPLETED and the unseen1 retry was refused).
    for index in range(UNOBSERVED_EXIT_ATTEMPTS):
        attempt=admit(boundary)
        work_id='unseen'+str(index)
        container=_kill_before_observation(boundary,attempt,work_id)
        if container is not None: break
    else:
        raise AssertionError('the guardian observed every container before the host kill landed')
    state=snapshot(boundary,attempt)
    row=work(state,work_id)
    transitions=[json.loads(base64.b64decode(t))['state'] for t in row['transitions']]
    assert not {'CAPTURED','COMPLETED','SIGNING_INTENT'}&set(transitions), transitions
    # No PAYLOAD identity was ever retained; the guardian's own startup PROCESS
    # event exists for every attempt and must not satisfy any identity proof.
    assert payload_process_events(boundary,attempt,work_id)==[]
    assert supervision_events(boundary,attempt,'PROCESS',work_id), 'guardian self-identity expected'
    assert supervision_events(boundary,attempt,'RESUMED',work_id)==[]
    reasons=[e['data'] for e in supervision_events(boundary,attempt,'PROCESS_UNOBSERVED',work_id)]
    # The guardian recorded its own failure and did NOT self-recover: no completed
    # recovery row it authored, and its one-use RECOVERY_OWNER slot is unspent. The
    # refusal is retained as PROCESS_UNOBSERVED when the guardian reached its
    # absence path, or as a FAILURE when it crashed even earlier (run 35482452099
    # 'unseen4': the docker scope vanished mid-read before any identity).
    failures=[e['data']['reason'] for e in supervision_events(boundary,attempt,'FAILURE',work_id)]
    assert failures and all(isinstance(r,str) and r for r in failures), failures
    if reasons:
        assert len(reasons)==1 and reasons[0]['container_id']==container, reasons
    assert row['state']=='IN_DOUBT' and row['observation_bytes_b64'] is None
    assert recovery_row(state,work_id) is None
    # On restart the service recovers with an unspent slot: the recovery COMPLETES
    # (no continuation_required, no permanent block) and settles the work.
    boundary.restart()
    after=snapshot(boundary,attempt)
    settled=work(after,work_id)
    assert settled['state']=='IN_DOUBT' and settled['observation_bytes_b64'] is not None
    completed_recovery=recovery_row(after,work_id)
    assert completed_recovery is not None
    assert completed_recovery['completion_bytes_b64'] is not None
    assert not completed_recovery['continuation_required']
    assert after['state'] in ('IN_DOUBT','BUDGET_UNCERTAIN','BUDGET_EXHAUSTED'), after['state']
    # Every work this suite has completed so far carries a retained alive-verified identity.
    with sqlite3.connect((boundary.root/'data/journal.sqlite').as_uri()+'?mode=ro',uri=True) as connection:
        attempts=[r[0] for r in connection.execute('SELECT attempt_id FROM full_campaign_budgets')]
    completed=[(a,w['work_id']) for a in attempts for w in snapshot(boundary,a)['works'] if w['state']=='COMPLETED']
    assert completed
    for completed_attempt,completed_work in completed:
        identity_retained(boundary,completed_attempt,completed_work)
    host.save(boundary.output/(attempt+'-unobserved-exit.json'),dict(work_id=work_id,container=container,
        attempts=index+1,refusal='PROCESS_UNOBSERVED' if reasons else 'FAILURE',reasons=reasons,failures=failures,
        transitions=transitions,
        recovery_completed=completed_recovery['completion_bytes_b64'] is not None,completed_with_identity=len(completed)))


def _payload_cpu_stat(payload):
    values=dict(line.split() for line in (payload/'cpu.stat').read_text().splitlines())
    return int(values['usage_usec'])*1000, values


def test_s2_payload_cpu_is_kernel_bounded_without_guardian(real_boundary):
    """With the guardian stopped, cpu.max × RuntimeMax on the payload slice still bounds cumulative payload CPU."""
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'unpolled',kind='descendants')
    state=wait(boundary,attempt,lambda s:has_work(s,'unpolled') and work(s,'unpolled')['state']=='RUNNING')
    scopes=work_enrollment(boundary.root.name,attempt,'unpolled')
    payload=scope_group(boundary,scopes,'payload_slice')
    row=work(state,'unpolled')
    budget_cpu_ns=row['limits']['cpu_ns']-state['profile']['orchestration_cpu_ns'][row['phase']]
    deadline=work_deadline(state,'unpolled')
    end=time.monotonic()+60
    while time.monotonic()<end:
        if (payload.exists() and 'populated 1' in (payload/'cgroup.events').read_text()
                and supervision_events(boundary,attempt,'RESUMED','unpolled')):
            break
        time.sleep(.1)
    else:
        raise AssertionError('payload never populated and resumed')
    quota,period=(payload/'cpu.max').read_text().split()
    assert quota!='max'
    # The realized rate over the whole work wall stays within budget plus one granule.
    assert int(quota)*row['limits']['wall_ns']<=(budget_cpu_ns+CPU_GRANULARITY_NS)*int(period)
    assert [e['data']['deadline_boottime_ns'] for e in supervision_events(boundary,attempt,'DEADLINE','unpolled')]==[deadline]
    # The RESUMED event records the guardian's SEND, not the probe's receipt, and
    # the bounded re-sends that normally cover a send lost before the probe's
    # block_resume_signal() arm cannot run once the guardian is stopped. Runs
    # 35476561750/35478031666 lost the resume (kernel default-ignore for an
    # unhandled signal to the PID-1 init) and the init timed out at 30 s; run
    # 35482452099 then showed a single >=150 ms interval of interpreter startup
    # (0.272->0.553 s) satisfying the old one-interval heuristic. Readiness is
    # therefore proven by TWO independent host facts before the STOP: (a) the
    # guardian has alive-verified at least three PAYLOAD-scope identities in the
    # container scope -- the init plus both burner children, which exist only
    # after the init actually consumed the resume and forked; and (b) cpu.stat
    # grew by >=150 ms in each of two consecutive >=1 s intervals, which a
    # decaying interpreter burst cannot produce (startup totals under 0.6 s).
    burn_deadline=time.monotonic()+90
    prior=None; intervals=0; ready_identities=0
    while time.monotonic()<burn_deadline:
        ready_identities=len(payload_process_events(boundary,attempt,'unpolled'))
        try: usage,stat=_payload_cpu_stat(payload)
        except (OSError,KeyError,ValueError): usage=None
        if usage is not None:
            if prior is not None and time.monotonic()-prior[0]>=1.0:
                intervals=intervals+1 if usage-prior[1]>=150_000_000 else 0
                prior=(time.monotonic(),usage)
            elif prior is None:
                prior=(time.monotonic(),usage)
        if ready_identities>=3 and intervals>=2:
            break
        time.sleep(.2)
    else:
        raise AssertionError('payload burners never started consuming their quota: identities=%d intervals=%d'
            %(ready_identities,intervals))
    baseline_ns,baseline_stat=_payload_cpu_stat(payload)
    baseline_identities=payload_process_events(boundary,attempt,'unpolled')
    host.run(['/usr/bin/systemctl','kill','--signal=STOP',scopes['guardian_unit']])
    stopped_at=boottime_ns()
    peak=baseline_ns; samples=0; populated=0; final_stat=baseline_stat
    end=time.monotonic()+340
    while time.monotonic()<end:
        try:
            usage,final_stat=_payload_cpu_stat(payload)
            peak=max(peak,usage); samples+=1
            if 'populated 1' in (payload/'cgroup.events').read_text(): populated+=1
        except (OSError,KeyError,ValueError):
            pass
        facts=unit_facts(scopes['guardian_unit'],['ActiveState','Result','ExecMainStatus','RuntimeMaxUSec'])
        if facts['ActiveState'] in ('failed','inactive'): break
        time.sleep(1)
    else:
        raise AssertionError('stopped guardian never ended')
    ended_at=boottime_ns()
    window_ns=ended_at-stopped_at
    # Container exit facts before the restart's recovery cleanup can retire them
    # (the probe's LogConfig is 'none', so no container stderr exists to retain).
    exit_id,exit_state=_owned_container('unpolled')
    container_exit='absent'
    if exit_id is not None:
        try:
            container_exit=DockerControl().call('GET','/containers/'+exit_id+'/json')['State']
        except ValueError:
            container_exit='unavailable'
    host.save(boundary.output/(attempt+'-payload-bound.json'),dict(cpu_max=quota+' '+period,budget_cpu_ns=budget_cpu_ns,
        baseline_payload_cpu_ns=baseline_ns,baseline_payload_identities=len(baseline_identities),
        peak_payload_cpu_ns=peak,samples=samples,populated_samples=populated,
        window_ns=window_ns,final_cpu_stat=final_stat,container_exit=container_exit,
        deadline_boottime_ns=deadline,stopped_at=stopped_at,ended_at=ended_at,facts=facts))
    assert facts['ActiveState']=='failed' and facts['ExecMainStatus']=='9', facts
    assert stopped_at<deadline<=ended_at<=deadline+15_000_000_000
    # The load-bearing property is the kernel UPPER bound: with the guardian
    # stopped, cumulative payload CPU never exceeds the reservation plus one
    # granule. The three discriminating facts below prove the bound was actually
    # exercised by runnable descendants rather than by an early-exiting payload:
    # the slice stayed populated for the whole stopped window, the kernel kept
    # throttling the burners (nr_throttled>0), and cumulative CPU kept growing at
    # no less than a single burner's floor under the slice rate (>=0.15 of the
    # window; the quota is a ceiling the kernel enforces, never a guarantee
    # under host contention).
    assert peak<=budget_cpu_ns+CPU_GRANULARITY_NS, peak
    # Every sample saw a populated slice except possibly the last one, which can
    # race the BindsTo retirement in the same instant the loop observes the unit
    # failing; and the samples cover the whole stopped window.
    assert populated>=samples-1 and samples>=window_ns//1_200_000_000, (populated,samples,window_ns)
    assert int(final_stat['nr_throttled'])>0, final_stat
    assert peak>=baseline_ns+(15*window_ns)//100, (peak,baseline_ns,window_ns)
    boundary.restart()
    after=snapshot(boundary,attempt)
    settled=work(after,'unpolled')
    assert settled['state']=='IN_DOUBT'
    observed=json.loads(base64.b64decode(settled['observation_bytes_b64']))
    if observed['cpu_ns'] is None:
        assert settled['charge_cpu_ns']==row['limits']['cpu_ns']  # reservation spent; payload retired by BindsTo
    else:
        assert observed['cpu_ns']<=budget_cpu_ns+CPU_GRANULARITY_NS
        assert settled['charge_cpu_ns']==observed['cpu_ns']+20_000_000_000
    assert after['state'] in ('IN_DOUBT','BUDGET_UNCERTAIN','BUDGET_EXHAUSTED'), after['state']


STOPPER='''import json,os,signal,sys,time
from pathlib import Path
group=Path(sys.argv[1]); end=time.monotonic()+float(sys.argv[2])
while time.monotonic()<end:
    try: pids=(group/'cgroup.procs').read_text().split()
    except OSError: pids=[]
    for pid in pids:
        try: comm=Path('/proc/'+pid+'/comm').read_text().strip()
        except OSError: continue
        # Stop only the exec'd interpreter. The manager's forked child carries
        # comm 'systemd' until the manager renames it '(python)' and then
        # execve sets 'python'; a stop in the first window freezes a pre-exec
        # child, the manager never sees the exec, and TimeoutStartSec kills the
        # unit with Result=timeout 90 s later (run 35555309697). Match the
        # interpreter basename exactly, never "anything without a parenthesis".
        if comm!=sys.argv[3]: continue
        os.kill(int(pid),signal.SIGSTOP)
        facts={}
        for name in ('comm','cmdline','timers','status'):
            try: facts[name]=Path('/proc/'+pid+'/'+name).read_bytes().decode('utf-8','replace')
            except OSError as exc: facts[name]=repr(exc)
        print(json.dumps(dict(pid=int(pid),stopped_boottime_ns=time.clock_gettime_ns(time.CLOCK_BOOTTIME),facts=facts)))
        sys.exit(0)
    time.sleep(.0005)
sys.exit(3)
'''


def test_s2_deadline_kills_guardian_before_bootstrap_completes(real_boundary):
    """A guardian stopped at its first instructions still ends at the original deadline: never RUNNING, no payload."""
    boundary=real_boundary; attempt=admit(boundary)
    scopes=work_enrollment(boundary.root.name,attempt,'late')
    guardian_group=scope_group(boundary,scopes,'guardian_unit')
    stopper=subprocess.Popen([sys.executable,'-I','-c',STOPPER,str(guardian_group),'120','python'],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    try:
        probe(boundary,attempt,'late',kind='wall')
        out,err=stopper.communicate(timeout=120)
    finally:
        if stopper.poll() is None: stopper.kill()
    assert stopper.returncode==0, err[-2000:]
    stopped=json.loads(out)
    pid=stopped['pid']
    state=snapshot(boundary,attempt)
    deadline=work_deadline(state,'late')
    assert work(state,'late')['state']=='START_INTENT', work(state,'late')['state']
    assert not [e for e in supervision_events(boundary,attempt,None,'late') if e['kind']!='CONTROL']
    # Hold the guardian stopped until shortly before its original deadline, then
    # let it run. It arms the pre-import absolute timer (deadline still ~1.2 s
    # future, so no immediate refusal) and is SIGKILLed by that timer at the
    # deadline -- before RuntimeMax (which is relative to unit activation and
    # therefore strictly later), before any payload exists and before the work
    # can leave START_INTENT. How far into guardian_main it gets first is
    # host-speed dependent: run 35486413008 reached the argv verification
    # (DEADLINE event) and died in the dispatch-ack wait; runs 35476561750 /
    # 35478031666 / 35482452099 died still importing. Neither DEADLINE nor the
    # guardian's own startup PROCESS identity is authority or payload activity.
    while boottime_ns()<deadline-1_200_000_000:
        time.sleep(min(1,(deadline-1_200_000_000-boottime_ns())/10**9))
    resumed_at=boottime_ns()
    os.kill(pid,signal.SIGCONT)
    end=time.monotonic()+30
    while time.monotonic()<end:
        facts=unit_facts(scopes['guardian_unit'],['ActiveState','Result','ExecMainStatus','RuntimeMaxUSec','NRestarts'])
        if facts['ActiveState'] in ('failed','inactive'): break
        time.sleep(.05)
    else:
        raise AssertionError('guardian outlived its original deadline')
    ended_at=boottime_ns()
    payload=scope_group(boundary,scopes,'payload_slice')
    payload_state='absent' if not payload.exists() else (payload/'cgroup.events').read_text()
    late_kinds=sorted({e['kind'] for e in supervision_events(boundary,attempt,None,'late')})
    host.save(boundary.output/(attempt+'-deadline-before-bootstrap.json'),dict(stopped=stopped,deadline_boottime_ns=deadline,
        resumed_at=resumed_at,ended_at=ended_at,facts=facts,payload=payload_state,supervision_kinds=late_kinds))
    # Killed by the process's own absolute timer (Result=signal), not by the manager's later RuntimeMax (timeout).
    assert facts['ActiveState']=='failed' and facts['ExecMainStatus']=='9' and facts['Result']=='signal', facts
    assert facts['NRestarts']=='0'
    assert resumed_at<deadline<=ended_at<=deadline+5_000_000_000
    after=snapshot(boundary,attempt)
    assert work(after,'late')['state']=='START_INTENT'
    # No payload observation, resume, refusal, cleanup or failure ran; the timer
    # ended the guardian before any authority or payload activity.
    assert not {'RESUMED','PROCESS_UNOBSERVED','CLEANUP','FAILURE'}&set(late_kinds), late_kinds
    assert set(late_kinds)<={'DEADLINE','PROCESS','CONTROL'}, late_kinds
    assert 'populated 1' not in payload_state
    boundary.restart()
    final=snapshot(boundary,attempt)
    assert work(final,'late')['state']=='IN_DOUBT'
    assert work(final,'late')['charge_cpu_ns']==work(final,'late')['limits']['cpu_ns']
    assert final['state'] in ('BUDGET_EXHAUSTED','BUDGET_UNCERTAIN','IN_DOUBT'), final['state']
    assert final['deadline_boottime_ns']==state['deadline_boottime_ns'] and final['start_clock']==state['start_clock']


def test_s2_shared_memory_oom_is_retained_last(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'memory',kind='memory')
    parent=Path('/sys/fs/cgroup')/host_slice(boundary.root.name)
    deadline=time.monotonic()+30
    while time.monotonic()<deadline:
        events=dict(line.split() for line in (parent/'memory.events').read_text().splitlines())
        if int(events['oom_kill']): break
        time.sleep(.1)
    assert int(events['oom_kill'])>0
    host.save(boundary.output/'s2-memory-facts.json',dict(events=events,peak=(parent/'memory.peak').read_text()))
    boundary.restart()
    state=snapshot(boundary,attempt)
    assert state['oom_events']>0
    # The OOM ends the campaign from either side of a genuine race: the settle
    # path derives a budget terminal, and the guardian's stop-on-OOM (first
    # memory.events increment -> durable IN_DOUBT before the kill, the same
    # shape as the overrun stop) ends it IN_DOUBT when the stop lands first --
    # the kernel kills this probe's single-process victim at the same instant
    # the increment becomes visible to the poll (run 35492219418). The retained
    # OOM facts are the load-bearing assertion either way; this mirrors the
    # overrun stop's accepted outcome set in the two-descendants case.
    assert state['state'] in ('BUDGET_EXHAUSTED','BUDGET_UNCERTAIN','IN_DOUBT'), state['state']
