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
import sqlite3
import time
import pytest
from tools.qualification_verification import host
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_supervisor import work_enrollment, host_slice
from c1_rail.qualification.execution.protocol import sha256


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
    # The guardian marks IN_DOUBT, kills the payload, then settles the measured
    # charge once absence is proven; the charge exists only after settlement.
    state=wait(boundary,attempt,lambda s:s['state'].startswith('BUDGET_') or
        (s['state']=='IN_DOUBT' and work(s,'descendants')['observation_bytes_b64'] is not None))
    assert state['state']=='IN_DOUBT'
    assert work(state,'descendants')['charge_cpu_ns']>=work(state,'descendants')['limits']['cpu_ns']
    boundary.restart()
    assert work(snapshot(boundary,attempt),'descendants')['state']=='IN_DOUBT'


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
    first=probe(boundary,attempt,'once')
    assert json.loads(base64.b64decode(first['data_b64']))['schema']=='qualification_campaign_status/v2', first
    duplicate=probe(boundary,attempt,'once')
    assert json.loads(base64.b64decode(duplicate['data_b64']))['schema']=='qualification_campaign_scheduler_status/v1', duplicate
    after=wait(boundary,attempt,lambda s:has_work(s,'once') and work(s,'once')['state']=='COMPLETED')
    scopes=work_enrollment(boundary.root.name,attempt,'once')
    prefix=host_slice(boundary.root.name)[:-6]
    units=host.run(['/usr/bin/systemctl','list-units','--all','--no-legend','--plain',prefix+'*'])
    assert 'scheduler' not in units, units
    assert not list((boundary.code/'tests/integration/qualification_boundary').glob('*driver*.py'))
    dispatches=[row for row in after['dispatches'] if row['work_id']=='once' and row['role']=='guardian']
    assert len(dispatches)==1 and dispatches[0]['acknowledged_clock'] is not None
    values=host.run(['/usr/bin/systemctl','show',scopes['guardian_unit'],'--property=NRestarts,Slice,ControlGroup'])
    facts=dict(line.split('=',1) for line in values.splitlines())
    assert facts['NRestarts']=='0'
    assert facts['Slice']==scopes['work_slice']
    assert facts['ControlGroup']=='' or ('/'+host_slice(boundary.root.name)) in facts['ControlGroup']
    owner_role='supervision_control_'+sha256(encoded(['once','START_OWNER']))
    with sqlite3.connect((boundary.root/'data/journal.sqlite').as_uri()+'?mode=ro',uri=True) as connection:
        owners=connection.execute('SELECT count(*) FROM full_campaign_objects WHERE attempt_id=? AND role=?',(attempt,owner_role)).fetchone()[0]
        intents=connection.execute('SELECT work_id FROM full_campaign_bootstraps WHERE attempt_id=?',(attempt,)).fetchall()
    assert owners==1 and [row[0] for row in intents]==['once']
    host.save(boundary.output/(attempt+'-warm-route.json'),dict(first=first,duplicate=duplicate,units=units,facts=facts,control_objects=owners))


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
