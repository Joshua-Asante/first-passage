"""Atomic store consistency; service signature/UID authority is tested separately."""
import base64
from dataclasses import replace
import json
import pytest
from test_artifact_acceptance import captured_case
from test_contract import NOW
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.execution.store import ExecutionStore
from c1_rail.qualification.execution.files import archive_bytes
from c1_rail.qualification.execution import g5,store as store_module


@pytest.fixture
def assessed_inputs(tmp_path,monkeypatch,captured_case):
    context,case,original,artifacts,_=captured_case
    monkeypatch.setattr(store_module.uuid,'uuid4',lambda:'g5-fixture')
    monkeypatch.setattr(g5,'utc_now',lambda:NOW)
    store=ExecutionStore(tmp_path/'journal.sqlite')
    payload=json.loads(original)['payload']
    plan=artifacts[payload['plan_sha256']]
    request=encoded(dict(operation='SUBMIT_N1',attempt_id=context.attempt_id,bundle_sha256=context.bundle_sha256))
    record=store.reserve(request,plan,now=NOW)
    store.archive_object(record.execution_id,'context_contract',context.contract.canonical_bytes)
    record=store.record_container(record.execution_id,'c'*64,expected_revision=record.revision)
    record=store.record_start_intent(record.execution_id,expected_revision=record.revision,now=NOW)
    record=store.record_running(record.execution_id,expected_revision=record.revision,now=NOW)
    for raw in artifacts.values(): archive_bytes(store.archive_dir,raw)
    facts={key:payload[key] for key in ('service_id','profile_sha256','runtime_manifest_sha256','worker_image_digest',
        'authorized_at_utc','started_utc','completed_utc','artifacts','observations')}
    facts.update(schema='qualification_capture/v1',container_id='c'*64)
    record=store.record_capture(record.execution_id,encoded(facts),expected_revision=record.revision)
    payload_raw=store.get_captured_payload(record.execution_id)
    attestation=encoded(dict(schema='qualification_execution_attestation/v1',payload=json.loads(payload_raw),
        signature=dict(algorithm='Ed25519',key_id='test-execution',value_b64=base64.b64encode(
            case['private']['test-execution'].sign(payload_raw)).decode())))
    record=store.publish_attestation(record.execution_id,attestation,expected_revision=record.revision)
    snapshot=store.snapshot_for_assessment(context.attempt_id)
    evidence=g5.validate_n1_evidence(context,attestation,artifacts,expected_attempt_id=context.attempt_id,
        current_keys=case['keys'],expected_revision=record.revision,journal_snapshot_bytes=snapshot)
    for role,raw in evidence.output_bytes_by_role.items(): store.store_proposed_artifact(context.attempt_id,role,raw)
    payload=dict(schema='qualification_result_authentication_payload/v2',scope='ATTEST_E1_RESULT',authority_class='TEST_ONLY',
        attempt_id=context.attempt_id,contract_sha256=context.contract.contract_sha256,trust_domain_sha256=context.domain.sha256,
        journal_revision=record.revision,result_sha256=sha256(evidence.result_bytes))
    authentication=encoded(dict(schema='qualification_result_authentication/v2',payload=payload,
        signature=dict(algorithm='Ed25519',key_id='test-producer',value_b64=base64.b64encode(
            case['private']['test-producer'].sign(encoded(payload))).decode())))
    return store,context.attempt_id,evidence,authentication


def test_atomic_commit_retains_artifacts_and_exact_receipt_after_reopen_void(assessed_inputs):
    store,attempt,evidence,authentication=assessed_inputs
    before=json.loads(store.status(attempt))
    first=json.loads(store.commit_assessment(evidence,authentication,now=NOW))
    assert first['validity']=='VALID'
    assert first['receipt']['result_sha256']==sha256(evidence.result_bytes)
    assert json.loads(store.status(attempt))['revision']==before['revision']+1
    for raw in evidence.output_bytes_by_role.values(): assert store.fetch(attempt,sha256(raw))==raw
    reopened=ExecutionStore(store.path)
    retrieved=json.loads(reopened.commit_assessment(evidence,authentication,now=NOW))
    assert retrieved['receipt']==first['receipt']
    assert retrieved['historical'] is True
    assert first['historical'] is False
    reopened.void(attempt,'fixture cancellation',b'{"validated_fixture":true}',now=NOW)
    after=json.loads(reopened.status(attempt))
    retry=json.loads(reopened.commit_assessment(evidence,authentication,now=NOW))
    assert retry['receipt']==first['receipt']
    assert retry['validity']=='VOID'
    assert json.loads(reopened.status(attempt))==after


def test_changed_authentication_conflicts_after_void(assessed_inputs):
    store,attempt,evidence,authentication=assessed_inputs
    store.commit_assessment(evidence,authentication,now=NOW)
    store.void(attempt,'fixture cancellation',b'{"validated_fixture":true}',now=NOW)
    auth=json.loads(authentication)
    auth['signature']['value_b64']=base64.b64encode(b'x'*64).decode()
    with pytest.raises(ValueError,match='idempotency conflict'):
        store.commit_assessment(evidence,encoded(auth),now=NOW)


def test_stale_snapshot_cannot_first_commit(assessed_inputs):
    store,attempt,evidence,authentication=assessed_inputs
    store.void(attempt,'fixture cancellation',b'{"validated_fixture":true}',now=NOW)
    with pytest.raises(ValueError,match='VOID|snapshot'):
        store.commit_assessment(evidence,authentication,now=NOW)
    assert 'result_sha256' not in json.loads(store.status(attempt))


def test_hash_mismatch_cannot_first_commit(assessed_inputs):
    store,attempt,evidence,authentication=assessed_inputs
    with pytest.raises(ValueError,match='snapshot'):
        store.commit_assessment(replace(evidence,journal_snapshot_sha256='f'*64),authentication,now=NOW)
    assert 'result_sha256' not in json.loads(store.status(attempt))
