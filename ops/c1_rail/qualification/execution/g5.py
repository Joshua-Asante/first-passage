"""Fresh G5 verification reconstructs every artifact from authenticated capture.

This library does not establish process isolation or commit journal state.
"""
from datetime import datetime,timezone
from dataclasses import replace
from ..contract import parse_canonical_json, canonical_json_bytes as encoded
from ..evidence import InspectedEvidence,build_n1_evidence,compare_n1_evidence
from ..journal_snapshot import parse_assessment_snapshot
from .admission import verify_bundle
from .evidence import parse_worker_result
from .protocol import ValidatedEvidence,positive,sha256,fields,parse_execution_attestation,utc_instant
from .verification import verify_execution,verify_role_signature


def utc_now():
    return datetime.now(timezone.utc)


def validate_n1_evidence(context,attestation_bytes,artifacts,*,expected_attempt_id,current_keys,
                         expected_revision,journal_snapshot_bytes):
    positive(expected_revision)
    snapshot=parse_assessment_snapshot(journal_snapshot_bytes)
    if snapshot['campaign_revision']!=expected_revision:
        raise ValueError('assessment snapshot revision differs')
    current=verify_bundle(context.bundle_dir,context.installed_release,current_keys,utc_now())
    if current.bundle_sha256!=context.bundle_sha256 or current.attempt_id!=expected_attempt_id:
        raise ValueError('current original context differs')
    if current.domain.authority_class!='TEST_ONLY':
        raise ValueError('N1_ONLY release forbids production execution')
    inspected = _inspect_capture(current,attestation_bytes,artifacts,expected_attempt_id=expected_attempt_id,
        current_keys=current_keys,expected_revision=expected_revision,journal_snapshot_bytes=journal_snapshot_bytes)
    doc=parse_canonical_json(inspected.envelope_bytes,label='reconstructed result')
    return ValidatedEvidence(inspected.envelope_bytes,sha256(attestation_bytes),
        doc['checkpoint_assessment']['decision'],expected_revision,inspected.output_bytes_by_role,
        sha256(journal_snapshot_bytes))


def _inspect_capture(current,attestation_bytes,artifacts,*,expected_attempt_id,current_keys,
                     expected_revision,journal_snapshot_bytes):
    verified=verify_execution(attestation_bytes,artifacts,context=current,
        expected_attempt_id=expected_attempt_id,current_keys=current_keys)
    payload=parse_canonical_json(attestation_bytes,label='attestation')['payload']
    if expected_revision<=payload['capture_revision']:
        raise ValueError('assessment requires published attestation revision')
    captured=parse_worker_result(verified.worker_result_bytes,context=current,
        execution_id=verified.execution_id,plan_bytes=verified.plan_bytes)
    for name,value in captured.document['observations'].items():
        if payload['observations'][name]!=value:
            raise ValueError('captured and attested observations differ')
    inspected=build_n1_evidence(contract=current.contract,policy=current.policy,
        worker_result_bytes=verified.worker_result_bytes,plan_bytes=verified.plan_bytes,
        execution_attestation_bytes=attestation_bytes,journal_snapshot_bytes=journal_snapshot_bytes,
        installed_release_bytes=current.installed_release)
    # Validate the full closed shape even for our own builder's output.
    compare_n1_evidence(inspected,expected=inspected)
    return inspected


def inspect_historical_n1(bundle_dir,installed_release,current_keys,*,result_bytes,authentication_bytes,
                          attestation_bytes,artifacts,output_bytes_by_role,expected_attempt_id):
    """Read-only historical integrity, never fresh acceptance or signing.

    Revocation and current expiry govern eligibility separately. Original public
    keys must still match the retained signed release/domain exactly; clearing
    current revocation here permits inspection of previously committed bytes.
    """
    keys = {name:replace(key,revoked_at=None) for name,key in current_keys.items()}
    payload = parse_execution_attestation(attestation_bytes)['payload']
    context = verify_bundle(bundle_dir,installed_release,keys,utc_instant(payload['authorized_at_utc']))
    doc = parse_canonical_json(result_bytes,label='historical result')
    inspected = _inspect_capture(context,attestation_bytes,artifacts,expected_attempt_id=expected_attempt_id,
        current_keys=keys,expected_revision=doc['journal_revision'],
        journal_snapshot_bytes=output_bytes_by_role['attempt_journal'])
    compare_n1_evidence(InspectedEvidence(result_bytes,output_bytes_by_role),expected=inspected)
    auth = fields(parse_canonical_json(authentication_bytes,label='historical authentication'),{'schema','payload','signature'})
    expected = dict(schema='qualification_result_authentication_payload/v2',scope='ATTEST_E1_RESULT',
        authority_class=context.domain.authority_class,attempt_id=expected_attempt_id,
        contract_sha256=context.contract.contract_sha256,trust_domain_sha256=context.domain.sha256,
        journal_revision=doc['journal_revision'],result_sha256=sha256(result_bytes))
    if auth['schema'] != 'qualification_result_authentication/v2' or encoded(auth['payload']) != encoded(expected):
        raise ValueError('historical result authentication differs')
    verify_role_signature(auth,context=context,current_keys=keys,role='result')


def validate_result_envelope_v2(context,result_bytes,*,attestations,artifacts,output_bytes_by_role,
                                expected_attempt_id,current_keys,expected_revision,journal_snapshot_bytes):
    doc=parse_canonical_json(result_bytes,label='proposed result')
    if type(doc) is not dict or doc.get('schema')!='qualification_result_envelope/v2':
        raise ValueError('EXECUTION_ATTESTATION_REQUIRED')
    stages=doc.get('stage_results')
    if (doc.get('verdict')=='PASS' or type(stages) is not list or
            any(type(row) is not dict for row in stages) or
            [row.get('stage') for row in stages]!=['LEGALITY','N1'] or
            type(attestations) is not dict or set(attestations)!={'N1'}):
        raise ValueError('UNSUPPORTED_ATTESTED_CHECKPOINT_SET')
    expected=validate_n1_evidence(context,attestations['N1'],artifacts,
        expected_attempt_id=expected_attempt_id,current_keys=current_keys,expected_revision=expected_revision,
        journal_snapshot_bytes=journal_snapshot_bytes)
    compare_n1_evidence(InspectedEvidence(result_bytes,output_bytes_by_role),
        expected=InspectedEvidence(expected.result_bytes,expected.output_bytes_by_role))
    return expected
def authenticate_n1_evidence(context, attestation_bytes, artifacts, *, expected_attempt_id,
                             current_keys, expected_revision, journal_snapshot_bytes, credential_reference):
    import base64
    from .credentials import load_credential
    evidence = validate_n1_evidence(context, attestation_bytes, artifacts,
        expected_attempt_id=expected_attempt_id, current_keys=current_keys, expected_revision=expected_revision,
        journal_snapshot_bytes=journal_snapshot_bytes)
    key_id, authority, key = load_credential(credential_reference)
    if (authority != context.domain.authority_class or key_id not in context.domain.result_key_ids
            or key_id not in current_keys
            or key.public_key().public_bytes_raw() != current_keys[key_id].public_key):
        raise ValueError('G5 credential enrollment differs')
    payload = dict(schema='qualification_result_authentication_payload/v2', scope='ATTEST_E1_RESULT',
        authority_class=authority, attempt_id=expected_attempt_id, contract_sha256=context.contract.contract_sha256,
        trust_domain_sha256=context.domain.sha256, journal_revision=expected_revision,
        result_sha256=sha256(evidence.result_bytes))
    authentication = encoded(dict(schema='qualification_result_authentication/v2', payload=payload,
        signature=dict(algorithm='Ed25519', key_id=key_id,
            value_b64=base64.b64encode(key.sign(encoded(payload))).decode('ascii'))))
    return evidence, authentication





def accept_n1(socket_path,*,attempt_id):
    import base64
    import os
    from pathlib import Path
    import tempfile
    from .client import request
    from .files import read_regular,relative_parts
    from .keys import load_keys
    from .runtime import load_instance,installed_code_root
    config=fields(load_instance(installed_code_root()/'qualification-installation/g5.json'),
        {'installation_root','socket_path','g5_uid','scratch_root','result_credential'})
    if str(socket_path)!=config['socket_path'] or os.geteuid()!=config['g5_uid']:
        raise ValueError('protected G5 identity/socket differs')
    release=read_regular(Path(config['installation_root']),'release.json',limit=16*1024*1024)
    authority=parse_canonical_json(release,label='release')['authority_class']
    keys=load_keys(read_regular(Path(config['installation_root']),'keys.json',limit=1024*1024),authority_class=authority)
    def call(operation,**values):
        return request(socket_path,operation,dict(attempt_id=attempt_id,**values))
    status=parse_canonical_json(call('STATUS'),label='status')
    historical=bool(status.get('result_sha256'))
    if not historical and (status['validity']!='VALID' or status['state']!='ATTESTED'):
        raise ValueError('VALID ATTESTED execution required')
    def fetch(digest_value):
        raw=call('FETCH',object_sha256=digest_value)
        if sha256(raw)!=digest_value: raise ValueError('fetched object identity differs')
        return raw
    attestation=fetch(status['attestation_sha256'])
    payload=parse_execution_attestation(attestation)['payload']
    index_raw=fetch(payload['retained_bundle_sha256'])
    index=parse_canonical_json(index_raw,label='bundle index')
    artifacts={item['sha256']:fetch(item['sha256']) for item in payload['artifacts']}
    with tempfile.TemporaryDirectory(dir=config['scratch_root']) as directory:
        root=Path(directory)
        (root/'index.json').write_bytes(index_raw)
        for item in index['entries']:
            relative_parts(item['path'])
            path=root/item['path']
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as output: output.write(fetch(item['sha256']))
        if historical:
            result=fetch(status['result_sha256'])
            authentication=fetch(status['authentication_sha256'])
            receipt=fetch(status['receipt_sha256'])
            doc=parse_canonical_json(result,label='historical result')
            outputs={item['role']:fetch(item['sha256']) for item in doc['outputs']}
            inspect_historical_n1(root,release,keys,result_bytes=result,authentication_bytes=authentication,
                attestation_bytes=attestation,artifacts=artifacts,output_bytes_by_role=outputs,expected_attempt_id=attempt_id)
            saved=fields(parse_canonical_json(receipt,label='historical receipt'),{'schema','attempt_id','execution_id',
                'result_sha256','authentication_sha256','cutoff_sha256','commit_event_sha256','committed_at_utc'})
            if (saved['schema']!='qualification_assessment_receipt/v1' or saved['attempt_id']!=attempt_id
                    or saved['execution_id']!=payload['execution_id'] or saved['result_sha256']!=sha256(result)
                    or saved['authentication_sha256']!=sha256(authentication)
                    or saved['cutoff_sha256']!=status['cutoff_sha256']):
                raise ValueError('historical receipt binding differs')
            response=call('COMMIT_N1_RESULT',envelope_sha256=sha256(result),
                authentication_bytes=base64.b64encode(authentication).decode())
            if encoded(parse_canonical_json(response,label='retry')['receipt'])!=receipt:
                raise ValueError('historical receipt changed')
            return response
        context=verify_bundle(root,release,keys,utc_now())
        snapshot=call('SNAPSHOT')
        revision=parse_assessment_snapshot(snapshot)['campaign_revision']
        evidence,authentication=authenticate_n1_evidence(context,attestation,artifacts,
            expected_attempt_id=attempt_id,current_keys=keys,expected_revision=revision,journal_snapshot_bytes=snapshot,
            credential_reference=config['result_credential'])
        for role,raw in evidence.output_bytes_by_role.items():
            stored=parse_canonical_json(call('STORE_ARTIFACT',role=role,bytes_b64=base64.b64encode(raw).decode()),label='artifact receipt')
            if stored!={'artifact_sha256':sha256(raw)}: raise ValueError('stored artifact identity differs')
        proposed=parse_canonical_json(call('STORE_RESULT',envelope_bytes_b64=base64.b64encode(evidence.result_bytes).decode()),label='proposal')
        if proposed!={'envelope_sha256':sha256(evidence.result_bytes)}: raise ValueError('stored envelope identity differs')
        return call('COMMIT_N1_RESULT',envelope_sha256=sha256(evidence.result_bytes),
                    authentication_bytes=base64.b64encode(authentication).decode())


def main():
    import argparse
    from pathlib import Path
    import sys
    from .files import read_regular
    from .runtime import load_instance,measure_runtime,installed_code_root
    parser=argparse.ArgumentParser()
    parser.add_argument('--attempt-id',required=True)
    args=parser.parse_args()
    config=load_instance(installed_code_root()/'qualification-installation/g5.json')
    release=read_regular(Path(config['installation_root']),'release.json',limit=16*1024*1024)
    measure_runtime(installed_code_root(),'g5',release)
    sys.stdout.buffer.write(accept_n1(Path(config['socket_path']),attempt_id=args.attempt_id))
