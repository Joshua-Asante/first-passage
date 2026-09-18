"""Actual credential denial, service death, VOID and immutable retry evidence."""
import base64
import json
import os
from pathlib import Path
import subprocess

import pytest


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
