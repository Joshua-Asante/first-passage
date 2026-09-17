"""Cryptographic TEST_ONLY trust domains, never qualification authority."""
import base64
from dataclasses import replace
from datetime import datetime,timezone,timedelta
import hashlib

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from c1_rail.qualification.contract import TrustedApprovalKey,canonical_json_bytes
from c1_rail.qualification.trust_domain import (
    QualificationWorkloadPolicy,PortRuntimePin,_composition_test_trust_policy,
    validate_qualification_trust_domain,production_trust_domain,require_validated_trust_domain)

NOW=datetime(2026,9,15,20,tzinfo=timezone.utc)
PORTS={'aegis_runtime_port':'aegis_6j','striker_runtime_port':'dj30_mym_p250',
       'vanguard_runtime_port':'vanguard_mgc','orb_runtime_port':'orb_mnq_v7'}


def case():
    counts={'LEGALITY':{},'N1':{p:(2,) for p in ('FULL','H1','H2')},'N2':{'FULL':(2,)},
        'PART_B':{p:(2,) for p in ('H1','H2')},'PART_A':{'REGIME':(2,4)},
        'N3':{p:(2,) for p in ('FULL','H1','H2')}}
    workload=QualificationWorkloadPolicy(counts,5,5,6,2,4,2)
    pins={leg:PortRuntimePin(leg,hashlib.sha256(role.encode()).hexdigest(),'b'*64) for role,leg in PORTS.items()}
    historical={role:pins[leg].runtime_sha256 for role,leg in PORTS.items()}
    code={role:'fp_qualification_port_'+leg for role,leg in PORTS.items()}
    policy=_composition_test_trust_policy(accepted_historical_pins=historical,
        required_artifact_roles=tuple(sorted(historical)),runtime_code_roles=code,
        port_runtime_pins=pins,effective_settings_sha256='c'*64,workload_policy=workload)
    doc={'schema':'qualification_trust_domain/v1','domain_id':'fixture-domain',
        'authority_class':'TEST_ONLY','permits_synthetic':True,
        'freeze_key_ids':['test'],'result_key_ids':['test'],'seal_key_ids':['test'],
        'accepted_historical_pins':historical,'required_artifact_roles':sorted(historical),
        'runtime_code_roles':code,'port_runtime_pins':{
            leg:{'leg_id':leg,'runtime_sha256':pin.runtime_sha256,'pine_sha256':pin.pine_sha256}
            for leg,pin in pins.items()},'effective_settings_sha256':'c'*64,
        'workload_policy':{'stage_population_depths':{s:{p:list(v) for p,v in populations.items()} for s,populations in counts.items()},
            'horizon_sessions':5,'inner_block_sessions':5,'outer_months':6,
            'part_a_initial_panels':2,'part_a_expanded_panels':4,'part_a_paths_per_population_per_panel':2}}
    private=Ed25519PrivateKey.generate()
    keys={'test':TrustedApprovalKey('test',private.public_key().public_bytes(
        serialization.Encoding.Raw,serialization.PublicFormat.Raw),'TEST_ONLY')}
    doc['trusted_key_sha256']={'test':hashlib.sha256(keys['test'].public_key).hexdigest()}
    return doc,policy,private,keys


def signed(doc,private,scope='BIND_QUALIFICATION_TRUST_DOMAIN'):
    raw=canonical_json_bytes(doc);digest=hashlib.sha256(raw).hexdigest()
    payload={'schema':'qualification_approval_payload/v1','scope':scope,
        'subject_sha256':digest,'contract_sha256':digest,'authority_class':doc['authority_class'],
        'issued_at':'2026-09-15T19:00:00Z','expires_at':'2026-09-16T19:00:00Z'}
    approval=canonical_json_bytes({'schema':'qualification_approval/v1','payload':payload,
        'signature':{'algorithm':'Ed25519','key_id':'test',
                     'value_b64':base64.b64encode(private.sign(canonical_json_bytes(payload))).decode()}})
    return raw,approval


def validate(doc,policy,private,keys):
    return validate_qualification_trust_domain(*signed(doc,private),keys,policy=policy,now=NOW)


def test_signed_test_domain_is_immutable_and_rejected_at_production_boundary():
    doc,policy,private,keys=case();domain=validate(doc,policy,private,keys)
    assert require_validated_trust_domain(domain) is domain
    assert domain.workload_policy.stage_population_depths['PART_A']['REGIME']==(2,4)
    assert domain.port_runtime_pins['aegis_6j'].leg_id=='aegis_6j'
    with pytest.raises(TypeError):domain.runtime_code_roles['new']='x'
    with pytest.raises(ValueError,match='authority|synthetic'):
        production_trust_domain(*signed(doc,private),keys,now=NOW)


@pytest.mark.parametrize('mutation',[
    lambda d:d.update(extra=True),lambda d:d.update(permits_synthetic=False),
    lambda d:d['required_artifact_roles'].pop(),lambda d:d['runtime_code_roles'].pop('orb_runtime_port'),
    lambda d:d['runtime_code_roles'].update(orb_runtime_port='wrong_name'),
    lambda d:d['port_runtime_pins']['orb_mnq_v7'].update(runtime_sha256='d'*64),
    lambda d:d.update(effective_settings_sha256='d'*64),
    lambda d:d['workload_policy'].update(horizon_sessions=True),
    lambda d:d['workload_policy']['stage_population_depths'].update(EXTRA={}),
    lambda d:d['workload_policy']['stage_population_depths']['N1'].update(FULL=[0]),
    lambda d:d['workload_policy'].update(part_a_paths_per_population_per_panel=1),
])
def test_malformed_or_policy_downgraded_domain_is_rejected(mutation):
    doc,policy,private,keys=case();mutation(doc)
    with pytest.raises(ValueError):validate(doc,policy,private,keys)


def test_noncanonical_bytes_wrong_scope_key_and_revocation_are_rejected():
    doc,policy,private,keys=case();raw,approval=signed(doc,private)
    with pytest.raises(ValueError):validate_qualification_trust_domain(raw+b' ',approval,keys,policy=policy,now=NOW)
    with pytest.raises(ValueError,match='scope'):
        validate_qualification_trust_domain(*signed(doc,private,'FREEZE_F1'),keys,policy=policy,now=NOW)
    with pytest.raises(ValueError,match='revoked'):
        validate(doc,policy,private,{'test':replace(keys['test'],revoked_at=NOW-timedelta(seconds=1))})
    with pytest.raises(ValueError,match='strong|key|signature'):
        validate(doc,policy,private,{'test':replace(keys['test'],public_key=b'\0'*32)})
    with pytest.raises(ValueError,match='authority'):
        validate(doc,policy,private,{'test':replace(keys['test'],authority_class='OPERATOR')})


def test_replaced_domain_is_not_an_issued_validation_receipt():
    doc,policy,private,keys=case();domain=validate(doc,policy,private,keys)
    with pytest.raises((TypeError,ValueError)):
        require_validated_trust_domain(replace(domain,domain_id='changed'))


@pytest.mark.parametrize('mutate',[
    lambda d:object.__setattr__(d,'domain_id','changed'),
    lambda d:object.__setattr__(d.workload_policy,'horizon_sessions',10),
    lambda d:object.__setattr__(d.port_runtime_pins['aegis_6j'],'runtime_sha256','d'*64),
])
def test_same_object_nested_mutation_does_not_preserve_issued_authority(mutate):
    doc,policy,private,keys=case();domain=validate(doc,policy,private,keys)
    mutate(domain)
    with pytest.raises(ValueError,match='changed'):require_validated_trust_domain(domain)


def operator_case():
    from c1_rail.qualification.trust_domain import PRODUCTION_TRUST_POLICY
    doc,_,private,keys=case();policy=PRODUCTION_TRUST_POLICY
    doc.update(authority_class='OPERATOR',permits_synthetic=False,
        accepted_historical_pins=dict(policy.accepted_historical_pins),
        required_artifact_roles=list(policy.required_roles),runtime_code_roles=dict(policy.required_code_roles),
        port_runtime_pins={leg:{'leg_id':leg,'runtime_sha256':p.runtime_sha256,'pine_sha256':p.pine_sha256}
                           for leg,p in policy.port_runtime_pins.items()})
    doc['workload_policy'].update(horizon_sessions=500,inner_block_sessions=5,
        part_a_initial_panels=100,part_a_expanded_panels=200)
    doc['workload_policy']['stage_population_depths']['PART_A']['REGIME']=[100,200]
    keys={'test':replace(keys['test'],authority_class='OPERATOR')}
    return doc,policy,private,keys


def test_operator_domain_binds_signed_depths_without_compiling_proposed_depths():
    doc,policy,private,keys=operator_case()
    domain=production_trust_domain(*signed(doc,private),keys,now=NOW)
    assert domain.workload_policy.stage_population_depths['N1']['FULL']==(2,)
    # This verifies the declaration only. Frozen contract and exact-depth
    # approval must agree before any workload can execute.
    assert require_validated_trust_domain(domain) is domain


def test_production_structural_panel_downgrade_is_rejected_even_with_operator_signature():
    doc,policy,private,keys=operator_case()
    doc['workload_policy'].update(part_a_initial_panels=2,part_a_expanded_panels=4)
    doc['workload_policy']['stage_population_depths']['PART_A']['REGIME']=[2,4]
    with pytest.raises(ValueError,match='100/200'):
        production_trust_domain(*signed(doc,private),keys,now=NOW)


def test_generic_validator_cannot_replace_compiled_production_policy():
    doc,policy,private,keys=operator_case()
    with pytest.raises(ValueError,match='compiled production policy'):
        validate_qualification_trust_domain(*signed(doc,private),keys,
            policy=replace(policy,production_workload_required=False),now=NOW)


def test_wrong_signing_key_cannot_validate_matching_declared_key_id():
    doc,policy,private,keys=case()
    with pytest.raises(ValueError,match='signature'):
        validate(doc,policy,Ed25519PrivateKey.generate(),keys)


@pytest.mark.parametrize('field,value',[('outer_months',3),('inner_block_sessions',20)])
def test_production_accepted_block_structure_cannot_be_downgraded(field,value):
    doc,policy,private,keys=operator_case()
    doc['workload_policy'][field]=value
    with pytest.raises(ValueError,match='6 months.*5 sessions'):
        production_trust_domain(*signed(doc,private),keys,now=NOW)


@pytest.mark.parametrize('field,value',[
    ('production_workload_required',False),('authority_class','TEST_ONLY'),
    ('permits_synthetic',True),('required_code_roles',{}),
    ('accepted_historical_pins',{}),('required_roles',()),
])
def test_compiled_policy_same_object_mutation_is_rejected_before_validation(field,value):
    from c1_rail.qualification.trust_domain import PRODUCTION_TRUST_POLICY
    doc,policy,private,keys=operator_case()
    if field=='production_workload_required':
        doc['workload_policy'].update(part_a_initial_panels=2,part_a_expanded_panels=4)
        doc['workload_policy']['stage_population_depths']['PART_A']['REGIME']=[2,4]
    original=getattr(policy,field)
    try:
        object.__setattr__(policy,field,value)
        with pytest.raises(ValueError,match='compiled production policy changed'):
            production_trust_domain(*signed(doc,private),keys,now=NOW)
    finally:object.__setattr__(PRODUCTION_TRUST_POLICY,field,original)


def test_compiled_policy_nested_pin_mutation_is_rejected():
    doc,policy,private,keys=operator_case()
    pin=policy.port_runtime_pins['aegis_6j'];original=pin.runtime_sha256
    try:
        object.__setattr__(pin,'runtime_sha256','d'*64)
        with pytest.raises(ValueError,match='compiled production policy changed'):
            production_trust_domain(*signed(doc,private),keys,now=NOW)
    finally:object.__setattr__(pin,'runtime_sha256',original)


@pytest.mark.parametrize('mutable_field',['domain','approval'])
def test_mutable_input_buffer_cannot_become_issuance_baseline(mutable_field):
    doc,policy,private,keys=case();raw,approval=signed(doc,private)
    with pytest.raises(TypeError,match='immutable bytes'):
        validate_qualification_trust_domain(bytearray(raw) if mutable_field=='domain' else raw,
            bytearray(approval) if mutable_field=='approval' else approval,keys,policy=policy,now=NOW)


@pytest.mark.parametrize('fingerprints',[{}, {'test':'a'*64}, {'test':'a'*64,'extra':'b'*64}])
def test_signed_key_fingerprint_inventory_must_be_exact_and_match_actual_keys(fingerprints):
    doc,policy,private,keys=case();doc['trusted_key_sha256']=fingerprints
    with pytest.raises(ValueError,match='key.*fingerprint'):
        validate(doc,policy,private,keys)


def test_same_id_new_public_key_and_valid_new_signature_cannot_replace_pinned_key():
    doc,policy,private,keys=case()
    replacement=Ed25519PrivateKey.generate()
    public=replacement.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw)
    with pytest.raises(ValueError,match='key.*fingerprint'):
        validate(doc,policy,replacement,{'test':replace(keys['test'],public_key=public)})


def test_consuming_key_check_binds_public_bytes_and_detects_receipt_mutation():
    from c1_rail.qualification.trust_domain import require_trusted_domain_key
    doc,policy,private,keys=case();domain=validate(doc,policy,private,keys)
    assert require_trusted_domain_key(domain,'test',keys['test'].public_key) is None
    with pytest.raises(ValueError,match='key.*fingerprint'):
        require_trusted_domain_key(domain,'test',b'\x01'*32)
    with pytest.raises(ValueError,match='key.*fingerprint'):
        require_trusted_domain_key(domain,'unknown',keys['test'].public_key)
    object.__setattr__(domain,'trusted_key_sha256',{'test':'d'*64})
    with pytest.raises(ValueError,match='changed'):
        require_trusted_domain_key(domain,'test',keys['test'].public_key)
