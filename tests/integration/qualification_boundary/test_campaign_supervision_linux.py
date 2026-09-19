"""Targeted S2 OS evidence. Run alone, --workers 1, on an enrolled S2 host.

Simulated counters cannot satisfy these assertions. The last case intentionally
terminates the common memory group; its contamination requires a fresh host.
"""
import base64
import json
import os
from pathlib import Path
import sqlite3
import time
import pytest
from tools.qualification_verification import host
from c1_rail.qualification.execution.campaign_supervisor import work_enrollment, host_slice


def snapshot(boundary, attempt):
    with sqlite3.connect((boundary.root/'data/journal.sqlite').as_uri()+'?mode=ro',uri=True) as connection:
        row=connection.execute('SELECT snapshot_bytes FROM full_campaign_budgets WHERE attempt_id=?',(attempt,)).fetchone()
    return json.loads(row[0])


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
    assert boundary.diagnostic, 'FP_QUALIFICATION_S2=1 required; never upgrade N1 fixture'
    bundle=boundary.prepare(idle=True)
    request=dict(schema='qualification_campaign_request/v2',operation='SUBMIT_E1',
        request_id='diagnostic',attempt_id=bundle['attempt_id'],bundle_sha256=bundle['bundle_sha256'])
    reply=boundary.raw_request(request)
    assert reply['ok'], reply
    state=wait(boundary,bundle['attempt_id'],lambda s: s['works'][0]['state']=='COMPLETED' or s['state'].startswith('BUDGET_'))
    assert state['state']=='BOUND', state
    assert state['settled_cpu_ns']==20_000_000_000
    assert boundary.raw_request(request)['ok']
    return bundle['attempt_id']


def probe(boundary,attempt,work,role='probe_worker',kind='noop',retry=None):
    command=['/usr/bin/systemd-run','--system','--wait','--pipe','--collect',
        '--unit='+host_slice(boundary.root.name)[:-6]+'scheduler'+work+'.service',
        '--slice='+host_slice(boundary.root.name),'--uid='+str(boundary.roles['qexec']),
        '--property=LimitCPU=1','--property=TasksMax=2','--property=RuntimeMaxSec=15',
        '--',boundary.python,'-I',str(boundary.code/'tests/integration/qualification_boundary/campaign_driver.py'),
        '--attempt',attempt,'--work',work,'--role',role,'--probe',kind]
    if retry: command.extend(['--retry-of',retry])
    host.run_owned(boundary.group,command,interpreter=boundary.python,timeout=25)


def test_s2_sequential_roles_share_one_allowance(real_boundary):
    boundary=real_boundary
    attempt=admit(boundary)
    for work,role in [('one','probe_worker'),('two','probe_g5'),('three','probe_result'),('four','probe_seal')]:
        before=snapshot(boundary,attempt)
        probe(boundary,attempt,work,role)
        after=wait(boundary,attempt,lambda s:s['works'][-1]['state']=='COMPLETED')
        observed=json.loads(base64.b64decode(after['works'][-1]['observation_bytes_b64']))
        assert observed['cpu_ns']>0
        assert after['settled_cpu_ns']-before['settled_cpu_ns']==observed['cpu_ns']+20_000_000_000
        assert after['start_clock']==before['start_clock']
        assert after['deadline_boottime_ns']==before['deadline_boottime_ns']
    boundary.restart()
    assert snapshot(boundary,attempt)['settled_cpu_ns']==after['settled_cpu_ns']


def test_s2_two_descendants_exhaust_owned_cpu(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'descendants',kind='descendants')
    state=wait(boundary,attempt,lambda s:s['state'].startswith('BUDGET_') or s['state']=='IN_DOUBT')
    assert state['state']=='IN_DOUBT'
    assert state['works'][-1]['charge_cpu_ns']>=state['works'][-1]['limits']['cpu_ns']
    boundary.restart()
    assert snapshot(boundary,attempt)['works'][-1]['state']=='IN_DOUBT'


def test_s2_fixed_intent_retry_is_charged_separately(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'intent','probe_seal','intent')
    first=wait(boundary,attempt,lambda s:s['works'][-1]['state']=='SIGNING_INTENT' and s['works'][-1]['observation_bytes_b64'] is not None)
    parent=first['works'][-1]
    probe(boundary,attempt,'retry','probe_seal',retry='intent')
    after=wait(boundary,attempt,lambda s:s['works'][-1]['state']=='COMPLETED')
    assert after['settled_cpu_ns']>=first['settled_cpu_ns']+20_000_000_000
    assert after['works'][-2]==parent
    assert after['authority_head']==first['authority_head']


def test_s2_guardian_death_recovers_before_cleanup(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'wall',kind='wall')
    wait(boundary,attempt,lambda s:s['works'][-1]['state']=='RUNNING')
    scopes=work_enrollment(boundary.root.name,attempt,'wall')
    host.run(['/usr/bin/systemctl','kill','--signal=KILL',scopes['guardian_unit']])
    boundary.restart()
    state=snapshot(boundary,attempt)
    assert state['works'][-1]['state']=='IN_DOUBT'
    assert state['state']=='BUDGET_UNCERTAIN'
    assert state['works'][-1]['charge_cpu_ns']==state['works'][-1]['limits']['cpu_ns']


def test_s2_original_deadline_survives_service_downtime(real_boundary):
    boundary=real_boundary; attempt=admit(boundary)
    probe(boundary,attempt,'deadline',kind='wall')
    first=wait(boundary,attempt,lambda s:s['works'][-1]['state']=='RUNNING')
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
    assert 13_000_000_000<=int(facts['CPUUsageNSec'])<=14_000_000_000
    boundary.restart()
    assert snapshot(boundary,attempt)['works'][-1]['state']=='IN_DOUBT'


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
