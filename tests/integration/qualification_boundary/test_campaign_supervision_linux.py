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


def identity_retained(boundary,attempt,work_id):
    """Completion credit requires a supervisor-retained, alive-verified PROCESS identity."""
    events=supervision_events(boundary,attempt,'PROCESS',work_id)
    assert events, 'no alive-verified PROCESS event retained for '+attempt+':'+work_id
    return events


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
    for work_id,role in [('one','probe_worker'),('two','probe_g5'),('three','probe_result'),('four','probe_seal')]:
        before=snapshot(boundary,attempt)
        probe(boundary,attempt,work_id,role)
        after=wait(boundary,attempt,lambda s:has_work(s,work_id) and work(s,work_id)['state']=='COMPLETED')
        observed=json.loads(base64.b64decode(work(after,work_id)['observation_bytes_b64']))
        assert observed['cpu_ns']>0
        assert after['settled_cpu_ns']-before['settled_cpu_ns']==observed['cpu_ns']+20_000_000_000
        assert after['start_clock']==before['start_clock']
        assert after['deadline_boottime_ns']==before['deadline_boottime_ns']
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
    host.save(boundary.output/(attempt+'-descendants-facts.json'),dict(facts=facts,state=state['state']))
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
    from urllib.parse import quote
    filters={'label':['fp.s2.work='+work_id]}
    rows=DockerControl().call('GET','/containers/json?all=1&filters='+quote(json.dumps(filters),safe=''))
    return rows[0]['Id'] if rows else None


def _kill_before_observation(boundary,attempt,work_id):
    """Kill the owned container the instant it exists, racing the guardian's first poll.

    Returns the container id when the guardian settled the work without ever
    retaining an identity for it; None when the guardian observed it first (that
    work then completes normally and the caller retries with a fresh work).
    """
    docker=DockerControl()
    probe(boundary,attempt,work_id)
    container=None
    end=time.monotonic()+30
    while time.monotonic()<end:
        container=_owned_container(work_id)
        if container is not None:
            docker.call('POST','/containers/'+container+'/kill?signal=KILL')
            break
        if supervision_events(boundary,attempt,'CONTAINER',work_id):
            container=supervision_events(boundary,attempt,'CONTAINER',work_id)[0]['data']['container_id']
            docker.call('POST','/containers/'+container+'/kill?signal=KILL')
            break
        time.sleep(.001)
    else:
        raise AssertionError('owned container never created')
    # The guardian, on its own exception, marks IN_DOUBT and exits WITHOUT settling
    # (no self-recovery: that would SIGKILL itself and strand a spent slot); the
    # service settles it on restart. So wait for the transition, not an observation.
    state=wait(boundary,attempt,lambda s:work(s,work_id)['state'] in ('COMPLETED','IN_DOUBT'),seconds=120)
    if supervision_events(boundary,attempt,'PROCESS',work_id):
        return None  # The guardian observed it before the host kill landed.
    assert work(state,work_id)['state']=='IN_DOUBT', state
    return container


def recovery_row(state,work_id):
    return next((r for r in state.get('recoveries',()) if r['work_id']==work_id),None)


def test_s2_probe_that_exits_before_observation_never_completes(real_boundary):
    """A container that exits before any alive-verified identity is retained is never
    credited, and the guardian's own exception leaves no incomplete recovery row."""
    boundary=real_boundary; attempt=admit(boundary)
    for index in range(UNOBSERVED_EXIT_ATTEMPTS):
        work_id='unseen'+str(index)
        container=_kill_before_observation(boundary,attempt,work_id)
        if container is not None: break
    else:
        raise AssertionError('the guardian observed every container before the host kill landed')
    state=snapshot(boundary,attempt)
    row=work(state,work_id)
    transitions=[json.loads(base64.b64decode(t))['state'] for t in row['transitions']]
    assert not {'CAPTURED','COMPLETED','SIGNING_INTENT'}&set(transitions), transitions
    assert supervision_events(boundary,attempt,'PROCESS',work_id)==[]
    assert supervision_events(boundary,attempt,'RESUMED',work_id)==[]
    reasons=[e['data'] for e in supervision_events(boundary,attempt,'PROCESS_UNOBSERVED',work_id)]
    assert len(reasons)==1 and reasons[0]['container_id']==container, reasons
    # The guardian recorded its own failure and did NOT self-recover: no completed
    # recovery row it authored, and its one-use RECOVERY_OWNER slot is unspent.
    failures=[e['data']['reason'] for e in supervision_events(boundary,attempt,'FAILURE',work_id)]
    assert failures and all(isinstance(r,str) and r for r in failures), failures
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
        attempts=index+1,reasons=reasons,failures=failures,transitions=transitions,
        recovery_completed=completed_recovery['completion_bytes_b64'] is not None,completed_with_identity=len(completed)))


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
    host.run(['/usr/bin/systemctl','kill','--signal=STOP',scopes['guardian_unit']])
    stopped_at=boottime_ns()
    peak=0; samples=0
    end=time.monotonic()+340
    while time.monotonic()<end:
        try:
            usage=int(dict(line.split() for line in (payload/'cpu.stat').read_text().splitlines())['usage_usec'])*1000
            peak=max(peak,usage); samples+=1
        except (OSError,KeyError,ValueError):
            pass
        facts=unit_facts(scopes['guardian_unit'],['ActiveState','Result','ExecMainStatus','RuntimeMaxUSec'])
        if facts['ActiveState'] in ('failed','inactive'): break
        time.sleep(1)
    else:
        raise AssertionError('stopped guardian never ended')
    ended_at=boottime_ns()
    host.save(boundary.output/(attempt+'-payload-bound.json'),dict(cpu_max=quota+' '+period,budget_cpu_ns=budget_cpu_ns,
        peak_payload_cpu_ns=peak,samples=samples,deadline_boottime_ns=deadline,stopped_at=stopped_at,ended_at=ended_at,facts=facts))
    assert facts['ActiveState']=='failed' and facts['ExecMainStatus']=='9', facts
    assert stopped_at<deadline<=ended_at<=deadline+15_000_000_000
    assert budget_cpu_ns//2<=peak<=budget_cpu_ns+CPU_GRANULARITY_NS, peak
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
        if comm.startswith('('): continue  # the manager's child before exec
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
    stopper=subprocess.Popen([sys.executable,'-I','-c',STOPPER,str(guardian_group),'120'],
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
    # deadline while still importing campaign code -- before RuntimeMax (which is
    # relative to unit activation and therefore strictly later) and before it can
    # reach guardian_main's own arm, its PROCESS/DEADLINE events or RUNNING.
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
    host.save(boundary.output/(attempt+'-deadline-before-bootstrap.json'),dict(stopped=stopped,deadline_boottime_ns=deadline,
        resumed_at=resumed_at,ended_at=ended_at,facts=facts,payload=payload_state))
    # Killed by the process's own absolute timer (Result=signal), not by the manager's later RuntimeMax (timeout).
    assert facts['ActiveState']=='failed' and facts['ExecMainStatus']=='9' and facts['Result']=='signal', facts
    assert facts['NRestarts']=='0'
    assert resumed_at<deadline<=ended_at<=deadline+5_000_000_000
    after=snapshot(boundary,attempt)
    assert work(after,'late')['state']=='START_INTENT'
    assert not [e for e in supervision_events(boundary,attempt,None,'late') if e['kind']!='CONTROL']
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
    assert state['state'] in ('BUDGET_EXHAUSTED','BUDGET_UNCERTAIN')
