"""Generated OPERATOR-schema signatures exercise semantics, never execution."""
import hashlib
import json
import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from c1_rail.qualification.contract import canonical_json_bytes as encode, TrustedApprovalKey, validate_frozen_contract
from c1_rail.qualification.trust_domain import production_trust_domain
from semantic_fixture import semantic_case
from test_contract import _operator_domain, _observed, _approval, NOW


def sha(raw): return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def operator_semantic_case():
    doc, policy, _ = semantic_case()
    old, private, keys = _operator_domain(doc)
    domain_doc = json.loads(old.canonical_bytes)
    for role in ('result','execution'):
        key = Ed25519PrivateKey.generate()
        keys[role] = TrustedApprovalKey(role,key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw),'OPERATOR')
        domain_doc[role+'_key_ids'] = [role]
    domain_doc.update(schema='qualification_trust_domain/v2',execution_service_id='unit-service',
        execution_release_sha256='a'*64,policy_sha256=policy.sha256,required_attested_checkpoints=['N1','N2','PART_A'])
    for role,digest in (('qualification_policy',policy.sha256),('execution_release','a'*64)):
        domain_doc['required_artifact_roles'].append(role)
        doc['artifacts'].append(dict(role=role,path='reviewed/'+role+'.bin',sha256=digest,producer='owner:'+role,authority_class='PRODUCTION_REVIEWED'))
        doc['dependencies'].append(dict(consumer_role=role,requires_roles=[]))
        next(row for row in doc['dependencies'] if row['consumer_role']=='qualification_runner')['requires_roles'].append(role)
        doc['runtime_load_trace'].append(dict(role=role,sha256=digest))
        doc['role_owners'].append(dict(role=role,owner='owner:'+role))
    domain_doc['required_artifact_roles'].sort()
    domain_doc['trusted_key_sha256'] = {name:sha(key.public_key) for name,key in keys.items()}
    raw = encode(domain_doc)
    domain = production_trust_domain(raw,_approval(raw,private,key_id='test',scope='BIND_QUALIFICATION_TRUST_DOMAIN'),keys,now=NOW)
    doc['trust_domain_sha256'] = domain.sha256
    doc['approval_policy']['freeze_key_ids'] = ['test']
    doc['result_plan']['adjudicator_closure_sha256'] = sha(encode(dict(schema='qualification-adjudicator-closure/v1',
        sources={row['role']:row['sha256'] for row in doc['runtime_load_trace']})))
    return doc,policy,domain,private,keys


def validate(case):
    doc,policy,domain,private,keys = case
    raw = encode(doc)
    return validate_frozen_contract(raw,_approval(raw,private,key_id='test'),keys,_observed(doc),
        now=NOW,trust_domain=domain,qualification_policy_bytes=policy.canonical_bytes)


def test_signed_operator_schema_reaches_v2_semantics(operator_semantic_case):
    result = validate(operator_semantic_case)
    assert result.policy_sha256 == operator_semantic_case[1].sha256
    assert result.initial_state.original_basis == 100000


def test_resigned_wrong_product_reaches_semantic_rejection(operator_semantic_case):
    for field in ('original_basis','current_equity','historical_eod_peak'):
        operator_semantic_case[0]['initial_state'][field] = '50000'
    with pytest.raises(ValueError,match='PRODUCT_BASIS_MISMATCH'): validate(operator_semantic_case)


def test_resigned_role_override_cannot_define_acceptance(operator_semantic_case):
    operator_semantic_case[0]['result_plan']['required_output_roles'] = ['private-result']
    with pytest.raises(ValueError,match='result_plan|result plan|RESULT_PLAN'): validate(operator_semantic_case)


def test_policy_bytes_are_required_at_v2_g1(operator_semantic_case):
    doc,_,domain,private,keys = operator_semantic_case
    raw = encode(doc)
    with pytest.raises(ValueError,match='POLICY_BYTES_REQUIRED'):
        validate_frozen_contract(raw,_approval(raw,private,key_id='test'),keys,_observed(doc),now=NOW,trust_domain=domain)
