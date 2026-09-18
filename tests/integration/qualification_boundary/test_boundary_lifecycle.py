"""Actual credential denial, service death, VOID and immutable retry evidence."""
import base64
import json
import os
from pathlib import Path
import subprocess
import time
import signal
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone

import pytest


def _checkpoint(boundary, bundle, expected_state):
    deadline=time.monotonic()+90
    while time.monotonic()<deadline:
        if boundary.checkpoint_receipt.exists():
            process=Path('/proc')/str(boundary.service.pid)/'status'
            stopped=next(line for line in process.read_text().splitlines() if line.startswith('State:'))
            if stopped.split()[1]=='T': break
        time.sleep(.05)
    else: pytest.fail('supervisor never reached actual process barrier')
    receipt=json.loads(boundary.checkpoint_receipt.read_bytes())
    assert receipt['pid']==boundary.service.pid
    journal=boundary.root/'data/journal.sqlite'
    with sqlite3.connect(journal.as_uri()+'?mode=ro',uri=True) as database:
        database.row_factory=sqlite3.Row
        before=dict(database.execute('SELECT * FROM executions WHERE attempt_id=?',
            (bundle['attempt_id'],)).fetchone())
    assert before['state']==expected_state
    return before,receipt,stopped


@pytest.mark.parametrize('checkpoint', ['record_container', 'start_and_capture', 'archive_capture'])
def test_real_prepublication_process_death_never_redraws(real_boundary, checkpoint):
    boundary=real_boundary
    bundle=boundary.prepare(idle=True)
    boundary.restart(checkpoint=checkpoint)
    with ThreadPoolExecutor(max_workers=1) as callers:
        response=callers.submit(boundary.submit,bundle)
        try:
            before,receipt,stopped=_checkpoint(boundary,bundle,{'record_container':'DISPATCHED',
                'start_and_capture':'START_INTENT','archive_capture':'RUNNING'}[checkpoint])
            assert receipt['checkpoint']==checkpoint
            from tools.qualification_verification import host
            host.save(boundary.output/(bundle['attempt_id']+'-process-interruption.json'),
                dict(checkpoint=checkpoint,execution_id=before['execution_id'],state=before['state'],
                     process_state=stopped,signal='SIGKILL',barrier=receipt))
        finally:
            boundary.service.kill(); boundary.service.wait(timeout=15)
        try: response.result(timeout=15)
        except subprocess.CalledProcessError: pass  # Lost acknowledgment is expected.
    boundary.restart()
    state=boundary.wait(bundle['attempt_id'],states=('IN_DOUBT',))
    assert state['execution_id']==before['execution_id'] and state['attestation_count']==0
    container=before['container_id'] or receipt['container_id']
    assert not boundary.inspect(container)['State']['Running']
    starts=boundary.starts(container)
    assert len(starts)==(1 if checkpoint=='archive_capture' else 0)
    assert state['launch_intent_count']==(0 if checkpoint=='record_container' else 1)
    events=boundary.events(bundle['attempt_id'])
    assert boundary.submit(bundle)['execution_id']==state['execution_id']
    assert boundary.events(bundle['attempt_id'])==events
    with pytest.raises(subprocess.CalledProcessError): boundary.assess(bundle['attempt_id'])
    assert 'result_sha256' not in boundary.status(bundle['attempt_id'])


def test_real_approval_expiry_between_intent_and_start_rejects_execution(real_boundary):
    boundary=real_boundary
    bundle=boundary.prepare(idle=True,depth_valid_seconds=60)
    attempt=bundle['attempt_id']
    boundary.restart(checkpoint='start_and_capture')
    with ThreadPoolExecutor(max_workers=1) as callers:
        response=callers.submit(boundary.submit,bundle)
        try:
            before,receipt,stopped=_checkpoint(boundary,bundle,'START_INTENT')
            assert receipt['checkpoint']=='start_and_capture'
            assert not boundary.starts(before['container_id'])
            expiry=datetime.fromisoformat(bundle['depth_expires_at'].replace('Z','+00:00'))
            time.sleep(max(0,(expiry-datetime.now(timezone.utc)).total_seconds())+.2)
            from tools.qualification_verification import host
            host.save(boundary.output/(attempt+'-prestart-expiry.json'),
                dict(execution_id=before['execution_id'],barrier=receipt,process_state=stopped,
                     depth_expires_at=bundle['depth_expires_at'],
                     resumed_at=datetime.now(timezone.utc).isoformat()))
        finally:
            boundary.service.send_signal(signal.SIGCONT)
        try: response.result(timeout=60)
        except subprocess.CalledProcessError: pass  # The process barrier can delay acknowledgment.
    failed=boundary.wait(attempt,states=('IN_DOUBT',))
    assert failed['execution_id']==before['execution_id']
    assert failed['attestation_count']==0 and failed['launch_intent_count']==1
    inspection=boundary.inspect(failed['container_id'])
    assert not inspection['State']['Running']
    started=datetime.fromisoformat(inspection['State']['StartedAt'].replace('Z','+00:00'))
    assert started>expiry and len(boundary.starts(failed['container_id']))==1
    events=boundary.events(attempt)
    assert any('approval is not valid at verification time' in row['data'].get('reason','') for row in events)
    boundary.restart()
    with pytest.raises(subprocess.CalledProcessError): boundary.submit(bundle)
    assert boundary.status(attempt)['execution_id']==failed['execution_id']
    assert boundary.events(attempt)==events
    with pytest.raises(subprocess.CalledProcessError): boundary.assess(attempt)
    assert 'result_sha256' not in boundary.status(attempt)


def test_captured_execution_survives_signer_denial_and_service_death(real_boundary):
    boundary=real_boundary
    bundle=boundary.prepare(idle=True); attempt=bundle['attempt_id']
    credential=Path(boundary.config['execution_credential'])
    original=credential.stat()
    # Root changes actual Linux ownership; no signer or capture producer is mocked.
    os.chown(credential,0,0)
    try:
        boundary.submit(bundle)
        captured=boundary.wait(attempt,states=('CAPTURED',))
        assert captured['attestation_count']==0 and captured['launch_intent_count']==1
        boundary.service.kill(); boundary.service.wait(timeout=15)
        # Recovery attempts signing synchronously before socket readiness.
        # Keeping access denied through this restart proves the attempt occurred.
        boundary.restart()
        pending=boundary.status(attempt)
        assert pending['state']=='CAPTURED' and pending['attestation_count']==0
        assert pending['recovery_issue']=='ATTESTATION_PENDING'
    finally:
        os.chown(credential,original.st_uid,original.st_gid)
    boundary.restart()
    recovered=boundary.wait(attempt)
    assert recovered['execution_id']==captured['execution_id']
    assert recovered['plan_sha256']==captured['plan_sha256']
    assert recovered['attestation_count']==1 and recovered['launch_intent_count']==1
    assert len(boundary.starts(recovered['container_id']))==1
    boundary.assess(attempt)


@pytest.mark.parametrize('committed',[False,True])
def test_real_void_prevents_new_acceptance_and_preserves_exact_retry(real_boundary,committed):
    boundary=real_boundary
    bundle=boundary.prepare(idle=True); attempt=bundle['attempt_id']
    boundary.submit(bundle); state=boundary.wait(attempt)
    first=boundary.assess(attempt) if committed else None
    reason='TEST_ONLY lifecycle cancellation'
    approval=boundary.admin('void-approval','--attempt',attempt,
        '--contract',bundle['contract_sha256'],'--reason',reason)
    response=json.loads(boundary.request('VOID',role='administrator',attempt_id=attempt,reason=reason,**approval))
    assert response['validity']=='VOID'
    boundary.restart()
    status=boundary.status(attempt)
    assert status['validity']=='VOID' and status['launch_intent_count']==1
    assert len(boundary.starts(state['container_id']))==1
    if committed:
        retry=boundary.assess(attempt)
        assert retry['receipt']==first['receipt'] and retry['historical'] is True
        assert retry['validity']=='VOID' and retry['current_policy_eligible'] is False
        original=boundary.fetch(attempt,status['authentication_sha256'])
        authentication=json.loads(original)
        authentication['signature']['value_b64']=base64.b64encode(b'x'*64).decode()
        from c1_rail.qualification.contract import canonical_json_bytes
        with pytest.raises(subprocess.CalledProcessError,match='returned non-zero') as failure:
            boundary.request('COMMIT_N1_RESULT',role='qg5',attempt_id=attempt,
                envelope_sha256=status['result_sha256'],
                authentication_bytes=base64.b64encode(canonical_json_bytes(authentication)).decode())
        assert 'idempotency conflict' in failure.value.stderr
        assert boundary.fetch(attempt,status['authentication_sha256'])==original
    else:
        with pytest.raises(subprocess.CalledProcessError): boundary.assess(attempt)
        assert 'result_sha256' not in boundary.status(attempt)


def test_real_running_worker_and_supervisor_death_never_redraw(real_boundary):
    boundary=real_boundary
    bundle=boundary.prepare(idle=True,fault='stop'); attempt=bundle['attempt_id']
    boundary.submit(bundle); running=boundary.wait(attempt,states=('RUNNING',))
    from tools.qualification_verification import host
    signal_sent=False
    deadline=time.monotonic()+60
    while time.monotonic()<deadline:
        inspection=boundary.inspect(running['container_id'])
        pid=inspection['State']['Pid']
        if pid:
            if not signal_sent:
                try: log=boundary.worker_log(running['execution_id'])
                except FileNotFoundError: log=b''
                if b'TEST_ONLY worker fault: stop\n' in log:
                    assert inspection['Id']==running['container_id']
                    host.run_owned(boundary.group,[boundary.manifest['host_config']['docker'],
                        '--host','unix:///var/run/docker.sock','kill','--signal=SIGSTOP',
                        running['container_id']],interpreter=boundary.python)
                    signal_sent=True
            process=Path('/proc')/str(pid)/'status'
            state=next(line for line in process.read_text().splitlines() if line.startswith('State:'))
            if signal_sent and state.split()[1]=='T': break
        time.sleep(.05)
    else: pytest.fail('signed synthetic worker did not reach its actual SIGSTOP checkpoint')
    assert b'TEST_ONLY worker fault: stop\n' in boundary.worker_log(running['execution_id'])
    host.save(boundary.output/(attempt+'-stopped-worker.json'),dict(container=inspection,pid=pid,
        process_state=state,signal='SIGSTOP',sender_uid=os.geteuid(),execution_id=running['execution_id']))
    boundary.service.kill(); boundary.service.wait(timeout=15)
    boundary.restart()
    stopped=boundary.wait(attempt,states=('IN_DOUBT',))
    assert stopped['execution_id']==running['execution_id'] and stopped['plan_sha256']==running['plan_sha256']
    assert stopped['attestation_count']==0 and stopped['launch_intent_count']==1
    assert boundary.inspect(stopped['container_id'])['State']['Running'] is False
    before=boundary.events(attempt)
    retry=boundary.submit(bundle)
    assert retry['state']=='IN_DOUBT' and retry['execution_id']==running['execution_id']
    assert boundary.events(attempt)==before and len(boundary.starts(stopped['container_id']))==1
    with pytest.raises(subprocess.CalledProcessError): boundary.assess(attempt)


@pytest.mark.parametrize('fault',['exit_zero','cpu','wall','memory'])
def test_real_worker_failure_has_no_attestation_acceptance_or_redraw(real_boundary,fault):
    boundary=real_boundary
    bundle=boundary.prepare(idle=True,fault=fault); attempt=bundle['attempt_id']
    boundary.submit(bundle)
    failed=boundary.wait(attempt,states=('IN_DOUBT','ABORTED'))
    assert failed['attestation_count']==0 and failed['launch_intent_count']==1
    inspection=boundary.inspect(failed['container_id'])
    log=boundary.worker_log(failed['execution_id'])
    assert ('TEST_ONLY worker fault: '+fault+'\n').encode() in log
    if fault=='exit_zero':
        assert inspection['State']['ExitCode']==0 and inspection['State']['OOMKilled'] is False
        assert any('frame' in row['data'].get('reason','').lower() for row in boundary.events(attempt))
    elif fault=='memory':
        oom_events=boundary.docker_events(failed['container_id'],'oom')
        boundary.docker_events(failed['container_id'],'kill')
        die_events=boundary.docker_events(failed['container_id'],'die')
        assert inspection['State']['OOMKilled'] is True
        assert inspection['State']['ExitCode']==137
        assert oom_events and die_events
        assert oom_events[-1]['timeNano'] <= die_events[-1]['timeNano']
    else:
        assert b'CPU/wall budget' in log and inspection['State']['ExitCode']!=0
    before=boundary.events(attempt)
    boundary.restart()
    assert boundary.submit(bundle)['execution_id']==failed['execution_id']
    assert boundary.events(attempt)==before and len(boundary.starts(failed['container_id']))==1
    with pytest.raises(subprocess.CalledProcessError): boundary.assess(attempt)
    assert 'result_sha256' not in boundary.status(attempt)


@pytest.mark.parametrize('committed',[False,True])
def test_real_approval_expiry_cannot_issue_new_authority_but_preserves_retry(real_boundary,committed):
    boundary=real_boundary
    bundle=boundary.prepare(idle=True,depth_valid_seconds=60); attempt=bundle['attempt_id']
    credential=Path(boundary.config['execution_credential'] if not committed else
        json.loads((boundary.installation/'g5.json').read_bytes())['result_credential'])
    original=credential.stat()
    if not committed: os.chown(credential,0,0)
    try:
        boundary.submit(bundle)
        captured=boundary.wait(attempt,states=('ATTESTED',) if committed else ('CAPTURED',))
        receipt=boundary.assess(attempt) if committed else None
        if committed: os.chown(credential,0,0)
        expiry=datetime.fromisoformat(bundle['depth_expires_at'].replace('Z','+00:00'))
        time.sleep(max(0,(expiry-datetime.now(timezone.utc)).total_seconds())+.2)
        boundary.restart()
        before=boundary.events(attempt)
        if committed:
            retry=boundary.assess(attempt)
            assert retry['receipt']==receipt['receipt'] and retry['historical'] is True
            assert retry['validity']=='VALID' and retry['current_policy_eligible'] is False
        else:
            pending=boundary.status(attempt)
            assert pending['state']=='CAPTURED' and pending['attestation_count']==0
            assert pending['recovery_issue']=='ATTESTATION_PENDING'
            with pytest.raises(subprocess.CalledProcessError): boundary.assess(attempt)
        assert boundary.events(attempt)==before
        assert len(boundary.starts(captured['container_id']))==1
        reason='TEST_ONLY fresh cancellation after expiry'
        approval=boundary.admin('void-approval','--attempt',attempt,
            '--contract',bundle['contract_sha256'],'--reason',reason)
        void=json.loads(boundary.request('VOID',role='administrator',attempt_id=attempt,reason=reason,**approval))
        assert void['validity']=='VOID'
    finally:
        os.chown(credential,original.st_uid,original.st_gid)

# TEST_ONLY caller: keep the original client/peer verification and frame limits.
# Only the in-flight COMMIT socket gets a longer initial deadline for SIGSTOP.
COMMIT_WAIT_DRIVER = r'''
import json
from pathlib import Path
import runpy
import socket
import sys
code, attempt, wait_seconds = Path(sys.argv[1]), sys.argv[2], float(sys.argv[3])
release = json.loads((code / 'qualification-installation/release.json').read_bytes())
if release['authority_class'] != 'TEST_ONLY' or release['production_execution']:
    raise SystemExit('commit wait driver requires TEST_ONLY installation')
sys.dont_write_bytecode = True
sys.path[:0] = [str(code / part) for part in ('ops', 'core', 'lab', 'governance', '')]
from c1_rail.qualification.execution import client
original_request, original_socket = client.request, socket.socket

class CommitSocket(socket.socket):
    def settimeout(self, seconds):
        if not getattr(self, '_configured', False):
            self._configured = True
            seconds = wait_seconds
        return super().settimeout(seconds)

def request(socket_path, operation, fields):
    if operation != 'COMMIT_N1_RESULT':
        return original_request(socket_path, operation, fields)
    socket.socket = CommitSocket
    try:
        return original_request(socket_path, operation, fields)
    finally:
        socket.socket = original_socket

client.request = request
sys.argv = [str(code / 'bootstrap.py'), 'g5', '--attempt-id', attempt]
runpy.run_path(sys.argv[0], run_name='__main__')
'''


def test_real_approval_expiry_during_commit_reconstruction_rejects_acceptance(real_boundary):
    from tools.qualification_verification import host
    boundary = real_boundary
    valid_seconds = 60
    bundle = boundary.prepare(idle=True, depth_valid_seconds=valid_seconds)
    attempt = bundle['attempt_id']
    boundary.restart(checkpoint='commit_authority')
    boundary.submit(bundle)
    attested = boundary.wait(attempt)
    original_events = boundary.events(attempt)
    original_starts = boundary.starts(attested['container_id'])
    assert len(original_starts) == 1
    command = boundary.identity('qg5', [boundary.python, '-I', '-c', COMMIT_WAIT_DRIVER,
        str(boundary.code), attempt, str(valid_seconds + 30)])
    with ThreadPoolExecutor(max_workers=1) as callers:
        response = callers.submit(host.run_owned, boundary.group, command,
            interpreter=boundary.python, timeout=valid_seconds + 90)
        try:
            before, receipt, stopped = _checkpoint(boundary, bundle, 'ATTESTED')
            assert receipt['checkpoint'] == 'commit_authority'
            assert receipt['container_id'] == attested['container_id']
            assert before['execution_id'] == attested['execution_id']
            expiry = datetime.fromisoformat(bundle['depth_expires_at'].replace('Z', '+00:00'))
            stopped_at = datetime.now(timezone.utc)
            assert stopped_at < expiry, 'approval must still be valid after actual reconstruction'
            time.sleep(max(0, (expiry - datetime.now(timezone.utc)).total_seconds()) + .2)
            host.save(boundary.output / (attempt + '-commit-authority-expiry.json'),
                dict(execution_id=before['execution_id'], barrier=receipt, process_state=stopped,
                    stopped_at=stopped_at.isoformat(), depth_expires_at=bundle['depth_expires_at'],
                    resumed_at=datetime.now(timezone.utc).isoformat()))
        finally:
            boundary.service.send_signal(signal.SIGCONT)
        with pytest.raises(subprocess.CalledProcessError) as rejected:
            unexpected = response.result(timeout=valid_seconds + 90)
            host.save(boundary.output / (attempt + '-unexpected-commit-response.json'), json.loads(unexpected))
    assert 'approval is not valid at verification time' in (rejected.value.stderr or '')
    after = boundary.status(attempt)
    assert after['state'] == 'ATTESTED' and after['execution_id'] == attested['execution_id']
    assert after['attestation_sha256'] == attested['attestation_sha256']
    assert after['attestation_count'] == 1 and after['launch_intent_count'] == 1
    assert 'result_sha256' not in after
    assert boundary.events(attempt) == original_events
    assert boundary.starts(after['container_id']) == original_starts
