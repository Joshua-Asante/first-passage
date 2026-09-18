"""Service dispatch over real store/context/signatures; no OS isolation claim."""
import base64
from datetime import datetime,timedelta
import json
import shutil
import pytest
from test_atomic_assessment import assessed_inputs,captured_case
from test_contract import NOW
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import service


@pytest.fixture
def dispatch(assessed_inputs,captured_case,monkeypatch):
    store,attempt,evidence,authentication=assessed_inputs
    context,case,*_=captured_case
    store.installation_dir.mkdir()
    (store.installation_dir/'release.json').write_bytes(context.installed_release)
    (store.installation_dir/'keys.json').write_bytes(encoded(dict(schema='qualification_trusted_keys/v1',keys=[
        dict(key_id=key.key_id,public_key_b64=base64.b64encode(key.public_key).decode(),
             authority_class=key.authority_class,revoked_at=None) for key in case['keys'].values()])))
    shutil.copytree(context.bundle_dir,store.path.parent/'bundles'/context.bundle_sha256)
    instance=object.__new__(service.ExecutionService)
    instance.store=store
    instance.roles={1001:'g5',1002:'client'}
    instance.profile=context.profile
    monkeypatch.setattr(service,'now',lambda:NOW)
    def call(operation,**fields):
        return instance.handle_request(1001,encoded(dict(operation=operation,attempt_id=attempt,**fields)))
    proposed=json.loads(call('STORE_RESULT',envelope_bytes_b64=base64.b64encode(evidence.result_bytes).decode()))
    request=dict(envelope_sha256=proposed['envelope_sha256'],authentication_bytes=base64.b64encode(authentication).decode())
    return store,attempt,evidence,authentication,instance,call,request


def test_public_dispatch_retry_after_expiry_and_void_preserves_receipt(dispatch,monkeypatch):
    store,attempt,_,_,instance,call,request=dispatch
    first=json.loads(call('COMMIT_N1_RESULT',**request))
    assert first['current_policy_eligible'] is True
    before=store.status(attempt)
    monkeypatch.setattr(service,'now',lambda:NOW+timedelta(days=365))
    retry=json.loads(call('COMMIT_N1_RESULT',**request))
    assert retry['receipt']==first['receipt'] and retry['historical'] is True
    assert retry['current_policy_eligible'] is False and retry['validity']=='VALID'
    assert store.status(attempt)==before
    store.void(attempt,'fixture cancellation',b'{"validated_fixture":true}',now=NOW)
    after=store.status(attempt)
    retry=json.loads(call('COMMIT_N1_RESULT',**request))
    assert retry['receipt']==first['receipt'] and retry['validity']=='VOID'
    assert retry['current_policy_eligible'] is False

    assert store.status(attempt)==after
    with pytest.raises(ValueError,match='PEER_NOT_AUTHORIZED'):
        instance.handle_request(1002,encoded(dict(operation='COMMIT_N1_RESULT',attempt_id=attempt,**request)))


def test_fresh_commit_after_expiry_rejects_without_acceptance(dispatch,monkeypatch):
    store,attempt,_,_,_,call,request=dispatch
    monkeypatch.setattr(service,'now',lambda:NOW+timedelta(days=365))
    with pytest.raises(ValueError): call('COMMIT_N1_RESULT',**request)
    assert 'result_sha256' not in json.loads(store.status(attempt))


@pytest.mark.parametrize('offset_us', [-1,0,1])
def test_commit_revalidates_approval_at_recorded_instant(dispatch,captured_case,monkeypatch,offset_us):
    store,attempt,_,_,_,call,request=dispatch
    _,case,*_=captured_case
    expiry=datetime.fromisoformat(json.loads(case['payloads']['exact_depth_approval'])['payload']['expires_at'].replace('Z','+00:00'))
    committed_at=expiry+timedelta(microseconds=offset_us)
    validate=service.validate_result_envelope_v2
    def delayed_validation(*args,**kwargs):
        evidence=validate(*args,**kwargs)
        monkeypatch.setattr(service,'now',lambda:committed_at)
        return evidence
    monkeypatch.setattr(service,'validate_result_envelope_v2',delayed_validation)
    before=store.status(attempt)
    if offset_us>=0:
        with pytest.raises(ValueError,match='approval'):
            call('COMMIT_N1_RESULT',**request)
        assert store.status(attempt)==before
        with pytest.raises(ValueError,match='published member'):
            store.fetch(attempt,request['envelope_sha256'])
    else:
        response=json.loads(call('COMMIT_N1_RESULT',**request))
        assert response['current_policy_eligible'] is True
        assert response['receipt']['committed_at_utc']==committed_at.isoformat().replace('+00:00','Z')
        monkeypatch.setattr(service,'now',lambda:expiry)
        retry=json.loads(call('COMMIT_N1_RESULT',**request))
        assert retry['receipt']==response['receipt'] and retry['historical'] is True
        assert retry['current_policy_eligible'] is False


def test_commit_reloads_revocation_after_reconstruction(dispatch,monkeypatch):
    store,attempt,_,_,_,call,request=dispatch
    validate=service.validate_result_envelope_v2
    def revoke_after_validation(*args,**kwargs):
        evidence=validate(*args,**kwargs)
        path=store.installation_dir/'keys.json'
        registry=json.loads(path.read_bytes())
        next(row for row in registry['keys'] if row['key_id']=='test-producer')['revoked_at']=NOW.isoformat().replace('+00:00','Z')
        path.write_bytes(encoded(registry))
        return evidence
    monkeypatch.setattr(service,'validate_result_envelope_v2',revoke_after_validation)
    before=store.status(attempt)
    with pytest.raises(ValueError,match='revok'):
        call('COMMIT_N1_RESULT',**request)
    assert store.status(attempt)==before


def test_changed_authentication_conflicts_on_historical_service_route(dispatch,monkeypatch):
    store,attempt,_,authentication,_,call,request=dispatch
    call('COMMIT_N1_RESULT',**request)
    monkeypatch.setattr(service,'now',lambda:NOW+timedelta(days=365))
    auth=json.loads(authentication)
    auth['signature']['value_b64']=base64.b64encode(b'x'*64).decode()
    request['authentication_bytes']=base64.b64encode(encoded(auth)).decode()
    with pytest.raises(ValueError,match='idempotency conflict'): call('COMMIT_N1_RESULT',**request)


def test_fresh_invalid_result_signature_rejects(dispatch):
    store,attempt,_,authentication,_,call,request=dispatch
    auth=json.loads(authentication)
    auth['signature']['value_b64']=base64.b64encode(b'x'*64).decode()
    request['authentication_bytes']=base64.b64encode(encoded(auth)).decode()
    with pytest.raises(ValueError,match='signature'): call('COMMIT_N1_RESULT',**request)
    assert 'result_sha256' not in json.loads(store.status(attempt))


def test_proposed_result_is_private_candidate_until_commit(dispatch):
    store,attempt,evidence,_,_,call,request=dispatch
    with pytest.raises(ValueError,match='published member'):
        store.fetch(attempt,request['envelope_sha256'])
    assert call('FETCH',object_sha256=request['envelope_sha256'])==evidence.result_bytes
    call('COMMIT_N1_RESULT',**request)
    assert store.fetch(attempt,request['envelope_sha256'])==evidence.result_bytes


def _void_request(dispatch, captured_case, current, *, mutation=None):
    from c1_rail.qualification.execution.protocol import sha256
    store,attempt,_,_,instance,_,_=dispatch
    context,case,*_=captured_case
    instance.roles[0]='operator'
    instance.recovery_issues={}
    reason='operator cancellation'
    subject=encoded(dict(attempt_id=attempt,reason=reason,contract_sha256=context.contract.contract_sha256))
    payload=dict(schema='qualification_approval_payload/v1',scope='VOID_QUALIFICATION_ATTEMPT',
        subject_sha256=sha256(subject),contract_sha256=context.contract.contract_sha256,authority_class='TEST_ONLY',
        issued_at=(current-timedelta(minutes=1)).isoformat().replace('+00:00','Z'),
        expires_at=(current+timedelta(minutes=1)).isoformat().replace('+00:00','Z'))
    if mutation=='expired': payload['expires_at']=current.isoformat().replace('+00:00','Z')
    if mutation=='subject': payload['subject_sha256']='f'*64
    key_id='test-producer' if mutation=='wrong_role' else 'test-freeze'
    if mutation in ('revoked','other_revoked'):
        path=store.installation_dir/'keys.json'
        registry=json.loads(path.read_bytes())
        revoked='test-freeze' if mutation=='revoked' else 'test-producer'
        next(row for row in registry['keys'] if row['key_id']==revoked)['revoked_at']=current.isoformat().replace('+00:00','Z')
        path.write_bytes(encoded(registry))
    approval=encoded(dict(schema='qualification_approval/v1',payload=payload,signature=dict(
        algorithm='Ed25519',key_id=key_id,value_b64=base64.b64encode(case['private'][key_id].sign(encoded(payload))).decode())))
    return encoded(dict(operation='VOID',attempt_id=attempt,reason=reason,
        operator_approval_bytes=base64.b64encode(approval).decode()))


@pytest.mark.parametrize('expired,other_revoked', [(False,False),(True,False),(True,True)])
def test_operator_void_uses_current_authority_and_survives_failed_cleanup(dispatch,captured_case,monkeypatch,expired,other_revoked):
    import subprocess
    store,attempt,_,_,instance,call,commit=dispatch
    first=json.loads(call('COMMIT_N1_RESULT',**commit))
    current=NOW+timedelta(days=365) if expired else NOW
    request=_void_request(dispatch,captured_case,current,mutation='other_revoked' if other_revoked else None)
    monkeypatch.setattr(service,'now',lambda:current)
    def failed_stop(*args,**kwargs): raise subprocess.SubprocessError('daemon unavailable')
    monkeypatch.setattr(service,'stop_owned_worker',failed_stop)
    response=json.loads(instance.handle_request(0,request))
    assert response['validity']=='VOID'
    status=json.loads(call('STATUS'))
    assert status['validity']=='VOID' and status['recovery_issue']=='CLEANUP_PENDING'
    retry=json.loads(call('COMMIT_N1_RESULT',**commit))
    assert retry['receipt']==first['receipt'] and retry['validity']=='VOID'
    assert retry['current_policy_eligible'] is False
    before=store.status(attempt)
    instance.recover_service()
    assert store.status(attempt)==before
    assert json.loads(call('STATUS'))['recovery_issue']=='CLEANUP_PENDING'


@pytest.mark.parametrize('mutation', ['expired','subject','revoked','wrong_role'])
def test_operator_void_still_requires_current_enrolled_authority(dispatch,captured_case,monkeypatch,mutation):
    store,attempt,_,_,instance,_,_=dispatch
    current=NOW+timedelta(days=365)
    request=_void_request(dispatch,captured_case,current,mutation=mutation)
    monkeypatch.setattr(service,'now',lambda:current)
    with pytest.raises(ValueError): instance.handle_request(0,request)
    assert json.loads(store.status(attempt))['validity']=='VALID'


def test_reservation_retains_admission_instant_for_later_cancellation(dispatch,captured_case,monkeypatch):
    import threading
    from types import SimpleNamespace
    from c1_rail.qualification.execution.store import ExecutionStore
    store,attempt,evidence,authentication,instance,call,commit=dispatch
    context,case,*_=captured_case
    fresh=ExecutionStore(store.path.with_name('reservation-only.sqlite'),installation_dir=store.installation_dir)
    instance.store=fresh
    instance.root=store.path.parent
    instance.installation=store.installation_dir
    instance.release=context.installed_release
    instance.authority='TEST_ONLY'
    instance.dispatch_lock=threading.Lock()
    # Unit dispatch scheduling only; this fixture claims no launched process.
    instance.executor=SimpleNamespace(submit=lambda *args:None)
    future=NOW+timedelta(days=365)
    clock=iter((NOW,future))
    monkeypatch.setattr(service,'now',lambda:next(clock))
    submission=json.loads(instance.handle_request(1002,encoded(dict(operation='SUBMIT_N1',attempt_id=attempt,bundle_sha256=context.bundle_sha256))))
    preflight=json.loads(fresh.fetch(attempt,submission['preflight_sha256']))
    assert preflight['schema']=='e1_preflight_binding/v2'
    assert preflight['output_identity']['execution_id']==submission['execution_id']
    new_dispatch=(fresh,attempt,evidence,authentication,instance,call,commit)
    request=_void_request(new_dispatch,captured_case,future)
    monkeypatch.setattr(service,'now',lambda:future)
    response=json.loads(instance.handle_request(0,request))
    assert response['validity']=='VOID' and response['launch_intent_count']==0
