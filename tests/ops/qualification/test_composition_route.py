"""Signed TEST_ONLY composition through real source, journal, replay and G5."""
import base64
import json

import pytest
from cryptography.hazmat.primitives import serialization

from composition_result_fixture import retained_result_envelope,sha
from c1_rail.qualification.contract import canonical_json_bytes


def _result_signature(setup,*,scope,subject,attempt_id,key_id,private_key=None):
    payload={'scope':scope,'subject_sha256':subject,
        'contract_sha256':setup.contract.contract_sha256,
        'trust_domain_sha256':setup.domain.sha256,'attempt_id':attempt_id,
        'issued_utc':'2026-09-15T19:00:00Z','expires_utc':'2026-09-16T19:00:00Z'}
    schema=('qualification_result_authentication/v1' if scope=='ATTEST_E1_RESULT'
            else 'e1_qualification_seal/v1')
    private=private_key or setup.private_keys[key_id]
    return canonical_json_bytes({'schema':schema,'payload':payload,
        'signature':{'algorithm':'Ed25519','key_id':key_id,
            'value_b64':base64.b64encode(private.sign(canonical_json_bytes(payload))).decode()}})


def _result_key(setup,key_id,scope,private_key=None):
    from c1_rail.qualification.seal import TrustedResultKey
    raw=(private_key or setup.private_keys[key_id]).public_key().public_bytes(
        serialization.Encoding.Raw,serialization.PublicFormat.Raw)
    return {key_id:TrustedResultKey(key_id,raw,'TEST_ONLY',(scope,))}


def _preflight(setup,tmp_path):
    from composition_fixture import signed_approval
    from test_contract import NOW
    from c1_rail.qualification.preflight import exact_depth_subject,validate_e1_preflight
    from c1_rail.qualification.attempt import AttemptStore
    attempt='TEST_ONLY-composition-attempt'
    approval=signed_approval(exact_depth_subject(setup.contract,attempt_id=attempt),
        setup.private_keys['test-freeze'],key_id='test-freeze',scope='APPROVE_E1_EXACT_DEPTH',
        contract_sha256=setup.contract.contract_sha256)
    preflight=validate_e1_preflight(setup.contract,attempt_id=attempt,
        output_root=tmp_path/'TEST_ONLY-outputs',exact_depth_approval_bytes=approval,
        trusted_keys=setup.trusted_keys,now=NOW,trust_domain=setup.domain)
    store=AttemptStore.open(tmp_path/'TEST_ONLY-journal.sqlite',campaign_id=attempt,
        contract_digest=setup.contract.contract_sha256,trust_domain_sha256=setup.domain.sha256,
        boot_id='TEST_ONLY-boot-1',now=NOW)
    return preflight,store,approval


def test_signed_composition_uses_real_source_dispatch_replay_and_g5_across_reopen(tmp_path,record_property):
    from composition_fixture import build_verified_composition
    from test_contract import NOW
    from c1_rail.qualification.orchestration import _run_composition_e1,run_production_e1
    from c1_rail.qualification.runtime_inventory import collect_runtime_inventory
    from c1_rail.qualification.result_adjudication import frozen_adjudicator
    from c1_rail.qualification.attempt import AttemptStore
    from c1_rail.qualification.seal import (validate_result_envelope,authenticate_result,
        commit_authenticated_result,e1_seal_payload,seal_e1_pass)
    input_root=tmp_path/'TEST_ONLY-inputs'
    setup=build_verified_composition(input_root)
    record_property('synthetic_contract_sha256',setup.contract.contract_sha256)
    record_property('synthetic_trust_domain_sha256',setup.domain.sha256)
    record_property('synthetic_retained_input_sha256',json.dumps(
        {role:sha(raw) for role,raw in setup.retained_source_bytes.items()},sort_keys=True))
    preflight,store,approval=_preflight(setup,tmp_path)
    with pytest.raises((TypeError,ValueError),match='production|operator|OPERATOR'):
        run_production_e1(setup.contract,source=setup.source,store=store,preflight=preflight,
            exact_depth_approval_bytes=approval,trusted_keys=setup.trusted_keys,now=lambda:NOW)
    execution=_run_composition_e1(setup.contract,source=setup.source,store=store,preflight=preflight,
        exact_depth_approval_bytes=approval,trusted_keys=setup.trusted_keys,now=lambda:NOW)
    assert execution.synthetic and execution.passed
    assert execution.trust_domain_sha256==setup.domain.sha256
    assert [row['checkpoint'] for row in store.checkpoints() if row['state']=='COMPLETED']==[
        'N1','CUTOFF','N2','PART_A']
    assert len(execution.path_outcomes['N2']['FULL'])==60
    assert all(len(rows)==60 for rows in execution.path_outcomes['PART_B'].values())
    assert len(execution.path_outcomes['PART_A']['REGIME'])==4
    inventory=collect_runtime_inventory(setup.contract,
        loaded_modules=setup.current_loaded_modules(),retained_source_bytes=setup.retained_source_bytes,
        artifact_root=input_root)
    adjudicator=frozen_adjudicator(setup.contract,retained_source_bytes=setup.retained_source_bytes,
        runtime_inventory=inventory)
    raw,runtime=retained_result_envelope(setup.contract,execution,store,preflight)
    arguments=dict(path_outcomes=execution.path_outcomes,path_inventory_bytes=execution.path_inventory_bytes,
        attempt_store=store,runtime_load_trace_bytes=runtime,preflight_receipt=preflight,
        exact_depth_approval_bytes=approval,exact_depth_trusted_keys=setup.trusted_keys,approval_now=NOW,
        stage_input_sha256=dict(execution.stage_input_sha256),adjudicator=adjudicator,
        trust_domain=setup.domain)
    foreign=json.loads(raw);foreign['trust_domain_sha256']='0'*64
    with pytest.raises(ValueError,match='domain'):
        validate_result_envelope(setup.contract,canonical_json_bytes(foreign),**arguments)
    result=validate_result_envelope(setup.contract,raw,**arguments)
    # Matching key IDs and a cryptographically valid signature cannot substitute
    # a key whose public bytes differ from the signed domain's enrollment.
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    replacement=Ed25519PrivateKey.generate()
    substituted_auth=_result_signature(setup,scope='ATTEST_E1_RESULT',subject=result.result_sha256,
        attempt_id=store.campaign_id,key_id='test-producer',private_key=replacement)
    with pytest.raises(ValueError):
        authenticate_result(result,substituted_auth,
            trusted_keys=_result_key(setup,'test-producer','ATTEST_E1_RESULT',replacement),
            now=NOW,trust_domain=setup.domain)
    assert store.result('TB_E1') is None
    producer_keys=_result_key(setup,'test-producer','ATTEST_E1_RESULT')
    authentication=_result_signature(setup,scope='ATTEST_E1_RESULT',subject=result.result_sha256,
        attempt_id=store.campaign_id,key_id='test-producer')
    authenticated=authenticate_result(result,authentication,trusted_keys=producer_keys,now=NOW,
        trust_domain=setup.domain)
    wrong_attempt=_result_signature(setup,scope='ATTEST_E1_RESULT',subject=result.result_sha256,
        attempt_id='different-attempt',key_id='test-producer')
    with pytest.raises(ValueError):
        authenticate_result(result,wrong_attempt,trusted_keys=producer_keys,now=NOW,
            trust_domain=setup.domain)
    committed_receipt=commit_authenticated_result(store,authenticated,trusted_keys=producer_keys,now=NOW,
        trust_domain=setup.domain)
    committed_events=store.events()
    assert commit_authenticated_result(store,authenticated,trusted_keys=producer_keys,now=NOW,
        trust_domain=setup.domain)==committed_receipt
    assert store.events()==committed_events
    reopened=AttemptStore.open(store.path,campaign_id=store.campaign_id,
        contract_digest=setup.contract.contract_sha256,trust_domain_sha256=setup.domain.sha256,
        boot_id='TEST_ONLY-boot-2',now=NOW)
    assert reopened.result('TB_E1')['manifest_bytes']==raw
    reopened_events=reopened.events()
    assert commit_authenticated_result(reopened,authenticated,trusted_keys=producer_keys,now=NOW,
        trust_domain=setup.domain)==committed_receipt
    assert reopened.events()==reopened_events
    seal_payload=e1_seal_payload(authenticated,sealed_utc=NOW)
    record=_result_signature(setup,scope='SEAL_E1_PASS',subject=sha(seal_payload),
        attempt_id=store.campaign_id,key_id='test-seal')
    substituted_seal=_result_signature(setup,scope='SEAL_E1_PASS',subject=sha(seal_payload),
        attempt_id=store.campaign_id,key_id='test-seal',private_key=replacement)
    with pytest.raises(ValueError):
        seal_e1_pass(authenticated,substituted_seal,sealed_utc=NOW,
            trusted_keys=_result_key(setup,'test-seal','SEAL_E1_PASS',replacement),now=NOW,
            result_trusted_keys=producer_keys,attempt_store=reopened,trust_domain=setup.domain)
    sealed=seal_e1_pass(authenticated,record,sealed_utc=NOW,
        trusted_keys=_result_key(setup,'test-seal','SEAL_E1_PASS'),now=NOW,
        result_trusted_keys=producer_keys,attempt_store=reopened,trust_domain=setup.domain)
    assert seal_e1_pass(authenticated,record,sealed_utc=NOW,
        trusted_keys=_result_key(setup,'test-seal','SEAL_E1_PASS'),now=NOW,
        result_trusted_keys=producer_keys,attempt_store=reopened,trust_domain=setup.domain)==sealed
    record_property('synthetic_result_sha256',result.result_sha256)
    record_property('synthetic_seal_sha256',sha(sealed))
    record_property('synthetic_runtime_inventory_sha256',sha(runtime))
    record_property('synthetic_reopened_event_head',reopened.status()['event_head'])
    payload=json.loads(sealed)['payload']
    assert payload['trust_domain_sha256']==setup.domain.sha256
    assert all(payload[name] is False for name in (
        'grants_activation','grants_admission','grants_deployment','grants_n3'))
    with pytest.raises((TypeError,ValueError)):
        authenticate_result(result,authentication,trusted_keys=producer_keys,now=NOW)


def test_real_composition_receipt_failure_survives_reopen_without_another_dispatch(tmp_path,monkeypatch):
    """Inject only a persistence failure after genuine signed-source N1 replay."""
    from composition_fixture import build_verified_composition
    from test_contract import NOW
    from c1_rail.qualification.attempt import AttemptStore,TransitionError
    from c1_rail.qualification.orchestration import _run_composition_e1
    setup=build_verified_composition(tmp_path/'TEST_ONLY-inputs')
    preflight,store,approval=_preflight(setup,tmp_path)
    receipts=[]
    def disk_failure(self,checkpoint,dispatch,receipt,*,now):
        assert self is store and checkpoint=='N1'
        receipts.append(json.loads(receipt))
        raise OSError('TEST_ONLY receipt persistence failure')
    with monkeypatch.context() as fault:
        fault.setattr(AttemptStore,'complete_checkpoint',disk_failure)
        with pytest.raises(OSError,match='receipt persistence failure'):
            _run_composition_e1(setup.contract,source=setup.source,store=store,preflight=preflight,
                exact_depth_approval_bytes=approval,trusted_keys=setup.trusted_keys,now=lambda:NOW)
    assert len(receipts)==1
    assert receipts[0]['trust_domain_sha256']==setup.domain.sha256
    n1=next(row for row in store.checkpoints() if row['checkpoint']=='N1')
    assert n1['state']=='STARTED_IN_DOUBT' and n1['receipt_bytes'] is None
    dispatch_digest=n1['dispatch_event_digest']
    reopened=AttemptStore.open(store.path,campaign_id=store.campaign_id,
        contract_digest=setup.contract.contract_sha256,trust_domain_sha256=setup.domain.sha256,
        boot_id='TEST_ONLY-boot-after-disk-failure',now=NOW)
    checkpoints_before=reopened.checkpoints()
    events_before=reopened.events()
    with pytest.raises(TransitionError,match='already dispatched'):
        _run_composition_e1(setup.contract,source=setup.source,store=reopened,preflight=preflight,
            exact_depth_approval_bytes=approval,trusted_keys=setup.trusted_keys,now=lambda:NOW)
    assert reopened.checkpoints()==checkpoints_before
    assert reopened.events()==events_before
    assert next(row for row in reopened.checkpoints() if row['checkpoint']=='N1')[
        'dispatch_event_digest']==dispatch_digest
    assert reopened.result('TB_E1') is None


def test_signed_composition_rejects_retained_bytes_and_import_alias_substitution(tmp_path,monkeypatch):
    import sys
    from composition_fixture import build_verified_composition
    from c1_rail.qualification.production_source import ProductionSource
    from c1_rail.qualification.runtime_inventory import collect_runtime_inventory
    root=tmp_path/'TEST_ONLY-inputs'
    setup=build_verified_composition(root)
    preflight,store,approval=_preflight(setup,tmp_path)
    for role in ('orb_runtime_port','effective_settings_successor','orb_mnq_v7_panel'):
        path=root/setup.fixture.paths[role]
        original=path.read_bytes()
        try:
            path.write_bytes(original+b'\nTEST_ONLY-substitution')
            with pytest.raises(ValueError):
                ProductionSource._build_composition(setup.contract,artifact_root=root)
        finally:
            path.write_bytes(original)
        assert store.stage('TB_E1')['state']=='UNRESERVED'
    modules=setup.current_loaded_modules()
    canonical=modules['qualification_runner']
    with monkeypatch.context() as alias:
        alias.setitem(sys.modules,'ops.c1_rail.qualification.orchestration',canonical)
        with pytest.raises(ValueError,match='alias'):
            collect_runtime_inventory(setup.contract,loaded_modules=modules,
                retained_source_bytes=setup.retained_source_bytes,artifact_root=root)
    assert store.stage('TB_E1')['state']=='UNRESERVED'


def test_independently_signed_composition_domains_cannot_be_crosswired(tmp_path):
    from composition_fixture import build_verified_composition
    from test_contract import NOW
    from c1_rail.qualification.orchestration import _run_composition_e1
    first=build_verified_composition(tmp_path/'first'/'TEST_ONLY-inputs')
    p1,s1,a1=_preflight(first,tmp_path/'first')
    second=build_verified_composition(tmp_path/'second'/'TEST_ONLY-inputs')
    p2,s2,a2=_preflight(second,tmp_path/'second')
    assert first.domain.sha256!=second.domain.sha256
    for source,store,preflight,approval,keys in (
        (second.source,s1,p1,a1,first.trusted_keys),
        (first.source,s2,p1,a1,first.trusted_keys),
        (first.source,s1,p2,a2,second.trusted_keys),
    ):
        with pytest.raises(ValueError):
            _run_composition_e1(first.contract,source=source,store=store,preflight=preflight,
                exact_depth_approval_bytes=approval,trusted_keys=keys,now=lambda:NOW)
        assert s1.stage('TB_E1')['state']==s2.stage('TB_E1')['state']=='UNRESERVED'
        assert s1.result('TB_E1') is s2.result('TB_E1') is None


def test_signed_approval_expiry_preserves_completed_n1_without_later_dispatch(tmp_path):
    from datetime import timedelta
    from composition_fixture import build_verified_composition
    from test_contract import NOW
    from c1_rail.qualification.orchestration import _run_composition_e1
    from c1_rail.qualification.attempt import AttemptStore
    setup=build_verified_composition(tmp_path/'TEST_ONLY-inputs')
    preflight,store,approval=_preflight(setup,tmp_path)

    def clock():
        completed=any(row['checkpoint']=='N1' and row['state']=='COMPLETED'
                      for row in store.checkpoints())
        return NOW+timedelta(days=2) if completed else NOW

    with pytest.raises(ValueError,match='approval is not valid at verification time'):
        _run_composition_e1(setup.contract,source=setup.source,store=store,preflight=preflight,
            exact_depth_approval_bytes=approval,trusted_keys=setup.trusted_keys,now=clock)
    checkpoints=store.checkpoints()
    assert next(row for row in checkpoints if row['checkpoint']=='N1')['state']=='COMPLETED'
    assert all(row['state']=='PENDING' for row in checkpoints if row['checkpoint']!='N1')
    assert store.result('TB_E1') is None
    reopened=AttemptStore.open(store.path,campaign_id=store.campaign_id,
        contract_digest=setup.contract.contract_sha256,trust_domain_sha256=setup.domain.sha256,
        boot_id='TEST_ONLY-expired-reopen',now=NOW+timedelta(days=2))
    assert reopened.checkpoints()==checkpoints


def test_preflight_refuses_replacement_enrolled_key_bytes_before_reserving_root(tmp_path):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from composition_fixture import build_verified_composition,signed_approval
    from test_contract import NOW
    from c1_rail.qualification.contract import TrustedApprovalKey
    from c1_rail.qualification.preflight import exact_depth_subject,validate_e1_preflight
    setup=build_verified_composition(tmp_path/'TEST_ONLY-inputs')
    replacement=Ed25519PrivateKey.generate()
    public=replacement.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
    approval=signed_approval(exact_depth_subject(setup.contract,attempt_id='TEST_ONLY-replaced'),
        replacement,key_id='test-freeze',scope='APPROVE_E1_EXACT_DEPTH',
        contract_sha256=setup.contract.contract_sha256)
    root=tmp_path/'must-not-be-reserved'
    with pytest.raises(ValueError,match='key'):
        validate_e1_preflight(setup.contract,attempt_id='TEST_ONLY-replaced',output_root=root,
            exact_depth_approval_bytes=approval,
            trusted_keys={'test-freeze':TrustedApprovalKey('test-freeze',public,'TEST_ONLY')},
            now=NOW,trust_domain=setup.domain)
    assert not root.exists()
