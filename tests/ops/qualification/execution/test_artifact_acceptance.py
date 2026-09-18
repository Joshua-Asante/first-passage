"""G5 library checks use signed fixture custody, not protected-execution evidence."""
import base64
import copy
import importlib
import json
import pytest
from bundle_fixture import build_bundle
from test_contract import NOW
from test_worker import stage_input
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.protocol import decode_frame,sha256
from c1_rail.qualification.journal_snapshot import encode_assessment_snapshot


@pytest.fixture(scope='module')
def captured_case(tmp_path_factory):
    root=tmp_path_factory.mktemp('g5-unit')
    case=build_bundle(root/'bundle',idle=True)
    context=stage_input(root,case)
    worker=importlib.import_module('c1_rail.qualification.execution.worker')
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(worker,'utc_now',lambda:NOW)
        raw=decode_frame(worker.run_worker(root,execution_id='g5-fixture'),limit=context.profile.output_byte_limit)
    plan=(root/'plan.json').read_bytes()
    doc=json.loads(raw)
    instant=NOW.isoformat().replace('+00:00','Z')
    payload=dict(schema='qualification_execution_attestation_payload/v1',scope='ATTEST_CHECKPOINT_EXECUTION',
        authority_class='TEST_ONLY',service_id=context.domain.execution_service_id,execution_id='g5-fixture',
        attempt_id=context.attempt_id,checkpoint='N1',contract_sha256=context.contract.contract_sha256,
        trust_domain_sha256=context.domain.sha256,exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
        execution_release_sha256=context.release.sha256,profile_sha256=context.profile.sha256,plan_sha256=sha256(plan),
        retained_bundle_sha256=context.bundle_sha256,runtime_manifest_sha256=context.release.runtime_sha256('worker'),
        worker_image_digest=context.release.document['worker_image_digest'],dispatch_event_sha256='a'*64,
        capture_event_sha256='b'*64,capture_revision=5,authorized_at_utc=instant,started_utc=instant,completed_utc=instant,
        completion='COMPLETED',artifacts=[dict(role=role,sha256=sha256(value),byte_length=len(value))
            for role,value in [('plan',plan),('worker_result',raw)]],
        observations=dict(exit_code=0,oom_killed=False,supervisor_wall_ns=1000000000,**doc['observations']))
    attestation=encoded(dict(schema='qualification_execution_attestation/v1',payload=payload,
        signature=dict(algorithm='Ed25519',key_id='test-execution',value_b64=base64.b64encode(
            case['private']['test-execution'].sign(encoded(payload))).decode())))
    snapshot=encode_assessment_snapshot(attempt_id=context.attempt_id,contract_sha256=context.contract.contract_sha256,
        trust_domain_sha256=context.domain.sha256,policy_sha256=context.policy.sha256,validity='VALID',campaign_revision=6,
        event_head='d'*64,executions=[dict(checkpoint='N1',execution_id='g5-fixture',execution_revision=6,state='ATTESTED',
            plan_sha256=sha256(plan),attestation_sha256=sha256(attestation))])
    return context,case,attestation,{sha256(plan):plan,sha256(raw):raw},snapshot


def inspect(captured_case,monkeypatch,**changes):
    context,case,attestation,artifacts,snapshot=captured_case
    g5=importlib.import_module('c1_rail.qualification.execution.g5')
    monkeypatch.setattr(g5,'utc_now',lambda:NOW)
    args=dict(expected_attempt_id=context.attempt_id,current_keys=case['keys'],expected_revision=6,journal_snapshot_bytes=snapshot)
    args.update(changes)
    return g5.validate_n1_evidence(context,attestation,artifacts,**args)


def test_reconstructs_all_five_real_artifact_roles(captured_case,monkeypatch):
    evidence=inspect(captured_case,monkeypatch)
    assert set(evidence.output_bytes_by_role)=={'attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace'}
    doc=json.loads(evidence.result_bytes)
    assert (doc['completion'],doc['verdict'])==('COMPLETE','FAIL')
    assert evidence.output_bytes_by_role['attempt_journal']==captured_case[-1]
    assert doc['stage_results'][1]['output_sha256']==sha256(evidence.output_bytes_by_role['n1_result'])


def test_current_snapshot_revision_must_match(captured_case,monkeypatch):
    with pytest.raises(ValueError,match='revision'):
        inspect(captured_case,monkeypatch,expected_revision=7)


@pytest.mark.parametrize('role',['attempt_journal','legality_result','n1_result','path_inventory','runtime_load_trace'])
def test_rehashed_artifact_substitution_rejected(captured_case,monkeypatch,role):
    evidence=inspect(captured_case,monkeypatch)
    outputs=dict(evidence.output_bytes_by_role)
    outputs[role]=b'{"unrelated":true}'
    doc=json.loads(evidence.result_bytes)
    entry=next(row for row in doc['outputs'] if row['role']==role)
    entry.update(sha256=sha256(outputs[role]),byte_length=len(outputs[role]))
    context,case,attestation,artifacts,snapshot=captured_case
    g5=importlib.import_module('c1_rail.qualification.execution.g5')
    with pytest.raises(ValueError,match='EVIDENCE_SEMANTIC_MISMATCH'):
        g5.validate_result_envelope_v2(context,encoded(doc),attestations={'N1':attestation},artifacts=artifacts,
            output_bytes_by_role=outputs,expected_attempt_id=context.attempt_id,current_keys=case['keys'],
            expected_revision=6,journal_snapshot_bytes=snapshot)


def test_coherent_valid_role_content_still_must_equal_captured_reconstruction(captured_case, monkeypatch):
    evidence = inspect(captured_case, monkeypatch)
    outputs = dict(evidence.output_bytes_by_role)
    stage = json.loads(outputs['n1_result'])
    # Keep the entire proposed schema and every linked digest consistent. Only
    # the claimed outcome-array identity differs from the real captured bytes.
    stage['outcome_array_sha256'] = 'f' * 64
    outputs['n1_result'] = encoded(stage)
    doc = json.loads(evidence.result_bytes)
    entry = next(row for row in doc['outputs'] if row['role'] == 'n1_result')
    entry.update(sha256=sha256(outputs['n1_result']), byte_length=len(outputs['n1_result']))
    doc['stage_results'][1]['output_sha256'] = sha256(outputs['n1_result'])
    context, case, attestation, artifacts, snapshot = captured_case
    g5 = importlib.import_module('c1_rail.qualification.execution.g5')
    with pytest.raises(ValueError, match='EVIDENCE_SEMANTIC_MISMATCH'):
        g5.validate_result_envelope_v2(context, encoded(doc), attestations={'N1': attestation},
            artifacts=artifacts, output_bytes_by_role=outputs, expected_attempt_id=context.attempt_id,
            current_keys=case['keys'], expected_revision=6, journal_snapshot_bytes=snapshot)


@pytest.mark.parametrize('change', ['v1', 'missing_attestation', 'full_pass', 'later_stage'])
def test_active_v2_consumer_rejects_legacy_or_unattested_full_campaign(captured_case, monkeypatch, change):
    evidence = inspect(captured_case, monkeypatch)
    context, case, attestation, artifacts, snapshot = captured_case
    doc = json.loads(evidence.result_bytes)
    attestations = {'N1': attestation}
    if change == 'v1': doc['schema'] = 'qualification_result_envelope/v1'
    elif change == 'missing_attestation': attestations = {}
    elif change == 'full_pass': doc.update(completion='COMPLETE', verdict='PASS')
    else: doc['stage_results'].append(dict(stage='N2', status='PASS'))
    g5 = importlib.import_module('c1_rail.qualification.execution.g5')
    with pytest.raises(ValueError, match='EXECUTION_ATTESTATION_REQUIRED|UNSUPPORTED_ATTESTED_CHECKPOINT_SET'):
        g5.validate_result_envelope_v2(context, encoded(doc), attestations=attestations,
            artifacts=artifacts, output_bytes_by_role=evidence.output_bytes_by_role,
            expected_attempt_id=context.attempt_id, current_keys=case['keys'],
            expected_revision=6, journal_snapshot_bytes=snapshot)


def test_historical_inspection_survives_expiry_without_new_authority(captured_case,monkeypatch):
    from datetime import timedelta
    from dataclasses import replace
    expected=inspect(captured_case,monkeypatch)
    context,case,attestation,artifacts,snapshot=captured_case
    g5=importlib.import_module('c1_rail.qualification.execution.g5')
    monkeypatch.setattr(g5,'utc_now',lambda:NOW+timedelta(days=365))
    keys={name:replace(key,revoked_at=NOW) for name,key in case['keys'].items()}
    payload=dict(schema='qualification_result_authentication_payload/v2',scope='ATTEST_E1_RESULT',authority_class='TEST_ONLY',
        attempt_id=context.attempt_id,contract_sha256=context.contract.contract_sha256,trust_domain_sha256=context.domain.sha256,
        journal_revision=6,result_sha256=sha256(expected.result_bytes))
    authentication=encoded(dict(schema='qualification_result_authentication/v2',payload=payload,
        signature=dict(algorithm='Ed25519',key_id='test-producer',value_b64=base64.b64encode(
            case['private']['test-producer'].sign(encoded(payload))).decode())))
    result=g5.inspect_historical_n1(context.bundle_dir,context.installed_release,keys,
        result_bytes=expected.result_bytes,authentication_bytes=authentication,attestation_bytes=attestation,
        artifacts=artifacts,output_bytes_by_role=expected.output_bytes_by_role,expected_attempt_id=context.attempt_id)
    assert result is None
    with pytest.raises(ValueError):
        g5.validate_n1_evidence(context,attestation,artifacts,expected_attempt_id=context.attempt_id,
            current_keys=keys,expected_revision=6,journal_snapshot_bytes=snapshot)


def test_bad_capture_cannot_reach_g5_credential_loading(captured_case,monkeypatch):
    context,case,attestation,artifacts,snapshot=captured_case
    g5=importlib.import_module('c1_rail.qualification.execution.g5')
    monkeypatch.setattr(g5,'utc_now',lambda:NOW)
    doc=json.loads(attestation)
    doc['signature']['value_b64']=base64.b64encode(b'x'*64).decode()
    with pytest.raises(ValueError,match='signature'):
        g5.authenticate_n1_evidence(context,encoded(doc),artifacts,expected_attempt_id=context.attempt_id,
            current_keys=case['keys'],expected_revision=6,journal_snapshot_bytes=snapshot,
            credential_reference='/nonexistent/must-not-be-opened')
