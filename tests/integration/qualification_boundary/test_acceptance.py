"""Actual launch -> capture -> G5 assertions; no outcome or process doubles."""
import json
from concurrent.futures import ThreadPoolExecutor
import pytest


@pytest.mark.parametrize('idle,completion,verdict',[(True,'COMPLETE','FAIL'),(False,'PARTIAL','NONE')])
def test_real_n1_retains_exact_adjudicated_capture(real_boundary,idle,completion,verdict):
    boundary=real_boundary
    bundle=boundary.prepare(idle=idle); attempt=bundle['attempt_id']
    reserved=boundary.submit(bundle)
    state=boundary.wait(attempt)
    assert state['launch_intent_count']==1 and state['attestation_count']==1
    inspection=boundary.inspect(state['container_id'])
    assert len(boundary.starts(state['container_id']))==1
    assert inspection['Image']==boundary.image and inspection['State']['Status']=='exited'
    receipt=boundary.assess(attempt)
    status=boundary.status(attempt)
    assert status['completion']==completion and status['verdict']==verdict
    result=json.loads(boundary.fetch(attempt,status['result_sha256']))
    assert result['completion']==completion and result['verdict']==verdict
    assert len(result['outputs'])==5
    for row in result['outputs']:
        raw=boundary.fetch(attempt,row['sha256'])
        import hashlib
        assert hashlib.sha256(raw).hexdigest()==row['sha256']
    boundary.restart()
    retry=boundary.assess(attempt)
    assert retry['receipt']==receipt['receipt'] and retry['historical'] is True
    assert boundary.status(attempt)['launch_intent_count']==1
    assert len(boundary.starts(state['container_id']))==1


def test_concurrent_duplicate_submit_reserves_and_launches_once(real_boundary):
    boundary=real_boundary; bundle=boundary.prepare(idle=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        receipts=list(pool.map(lambda _:boundary.submit(bundle),range(2)))
    assert receipts[0]['execution_id']==receipts[1]['execution_id']
    state=boundary.wait(bundle['attempt_id'])
    assert state['launch_intent_count']==1 and state['attestation_count']==1
    assert len(boundary.starts(state['container_id']))==1


@pytest.mark.parametrize('operation',['COMPLETE_CHECKPOINT','SIGN','SET_VERDICT'])
def test_public_client_cannot_supply_execution_authority(real_boundary,operation):
    response=real_boundary.raw_request(dict(operation=operation,attempt_id='fabricated'))
    assert response['ok'] is False
    assert response['error']=='UNKNOWN_OPERATION'


@pytest.mark.parametrize('operation,fields',[
    ('STORE_ARTIFACT',dict(role='n1_result',bytes_b64='e30=')),
    ('STORE_RESULT',dict(envelope_bytes_b64='e30=')),
    ('COMMIT_N1_RESULT',dict(envelope_sha256='f'*64,authentication_bytes='e30=')),
])
def test_real_client_uid_cannot_enter_g5_acceptance(real_boundary,operation,fields):
    response=real_boundary.raw_request(dict(operation=operation,attempt_id='fabricated',**fields))
    assert response==dict(ok=False,error='PEER_NOT_AUTHORIZED')
