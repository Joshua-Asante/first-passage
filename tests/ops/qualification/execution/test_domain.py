"""V2 enrollment separates actual signing authorities, including key aliases."""
from dataclasses import replace
import hashlib

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from c1_rail.qualification.contract import TrustedApprovalKey
from c1_rail.qualification.trust_domain import validate_qualification_trust_domain
from test_trust_domain import case, signed, NOW


def v2_case():
    doc, policy, private, keys = case()
    for role in ('result', 'seal', 'execution'):
        generated = Ed25519PrivateKey.generate()
        keys[role] = TrustedApprovalKey(role, generated.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw), 'TEST_ONLY')
        doc[role + '_key_ids'] = [role]
    doc.update(schema='qualification_trust_domain/v2', execution_service_id='fixture-service',
               execution_release_sha256='a' * 64,
               policy_sha256='b' * 64,
               required_attested_checkpoints=['N1', 'N2', 'PART_A'])
    doc['required_artifact_roles'] = sorted([*doc['required_artifact_roles'],'qualification_policy','execution_release'])
    doc['trusted_key_sha256'] = {key: hashlib.sha256(value.public_key).hexdigest()
                                 for key, value in keys.items()}
    return doc, policy, private, keys


def validate(values):
    doc, policy, private, keys = values
    return validate_qualification_trust_domain(*signed(doc, private), keys, policy=policy, now=NOW)


def test_v2_domain_binds_execution_authority_and_full_required_checkpoint_set():
    domain = validate(v2_case())
    assert domain.execution_key_ids == ('execution',)
    assert domain.required_attested_checkpoints == ('N1', 'N2', 'PART_A')


@pytest.mark.parametrize('first,second', [
    ('freeze', 'result'), ('freeze', 'seal'), ('freeze', 'execution'),
    ('result', 'seal'), ('result', 'execution'), ('seal', 'execution')])
@pytest.mark.parametrize('alias', [False, True])
def test_roles_cannot_share_ids_or_public_key_bytes(first, second, alias):
    values = v2_case()
    doc, _, _, keys = values
    original = doc[first + '_key_ids'][0]
    target = doc[second + '_key_ids'][0]
    if alias:
        keys[target] = replace(keys[original], key_id=target)
        doc['trusted_key_sha256'][target] = doc['trusted_key_sha256'][original]
    else:
        doc[second + '_key_ids'] = [original]
        del doc['trusted_key_sha256'][target]
    with pytest.raises(ValueError, match='role.*separation|public.key.*separation'):
        validate(values)


@pytest.mark.parametrize('checkpoints', [['N1'], ['N1', 'N2'], ['N2', 'N1', 'PART_A']])
def test_n1_release_cannot_weaken_eventual_e1_attestation_requirement(checkpoints):
    values = v2_case()
    values[0]['required_attested_checkpoints'] = checkpoints
    with pytest.raises(ValueError, match='checkpoint'):
        validate(values)
