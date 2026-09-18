"""Retained-byte legality checks. Consistency here does not attest execution."""
import hashlib

from c1_rail.policy_fingerprint import normalized_geometry_bytes, validate_registry
from .contract import canonical_json_bytes, parse_canonical_json, _fields, _sha256
from .policy import _document


SOURCE_CHECKS = (
    'RETAINED_IDENTITIES', 'CALENDAR_POPULATION_PROVIDER_BINDING', 'COVERAGE',
    'SCHEDULE_EVIDENCE', 'COSTS', 'ADAPTER_SETTINGS_BINDING',
)


def geometry_role(runtime_code_roles) -> str:
    matches = [role for role, module in runtime_code_roles.items() if module == 'dd_geometry']
    if len(matches) != 1:
        raise ValueError('LEGALITY_GEOMETRY_ROLE: exactly one dd_geometry role required')
    return matches[0]


def verify_static_legality(*, contract_sha256, domain_sha256, policy,
                          geometry_bytes, expected_geometry_sha256) -> None:
    _document(policy)
    for label, value in [('contract', contract_sha256), ('domain', domain_sha256), ('geometry', expected_geometry_sha256)]:
        _sha256(value, label=label)
    if type(geometry_bytes) is not bytes or hashlib.sha256(geometry_bytes).hexdigest() != expected_geometry_sha256:
        raise ValueError('LEGALITY_GEOMETRY_DIGEST_MISMATCH')
    try:
        # The canonical AST validator distinguishes malformed bindings from a
        # well-formed registry whose contents violate pre-admission emptiness.
        normalized_geometry_bytes(geometry_bytes)
    except (ValueError, SyntaxError, UnicodeError) as exc:
        raise ValueError('LEGALITY_GEOMETRY_MALFORMED') from exc
    try:
        validate_registry(geometry_bytes, expected_rows={})
    except ValueError as exc:
        raise ValueError('LEGALITY_REGISTRY_NOT_EMPTY') from exc


def parse_source_admission(raw, *, contract_sha256, domain_sha256, policy):
    doc = _fields(parse_canonical_json(raw, label='source admission'), {
        'schema', 'contract_sha256', 'trust_domain_sha256', 'policy_sha256',
        'retained_roles', 'population_sha256', 'effective_settings_sha256', 'checks'}, label='source admission')
    if (doc['schema'] != 'qualification_source_admission/v1'
            or doc['contract_sha256'] != contract_sha256 or doc['trust_domain_sha256'] != domain_sha256
            or doc['policy_sha256'] != policy.sha256 or doc['checks'] != list(SOURCE_CHECKS)):
        raise ValueError('SOURCE_ADMISSION_BINDING_MISMATCH')
    _sha256(doc['effective_settings_sha256'], label='settings')
    for pop, digest in _fields(doc['population_sha256'], {'FULL', 'H1', 'H2'}, label='populations').items():
        _sha256(digest, label=pop)
    rows = doc['retained_roles']
    if type(rows) is not list or not rows:
        raise ValueError('SOURCE_ADMISSION_INVENTORY_MISMATCH')
    names = []
    for row in rows:
        _fields(row, {'role', 'sha256'}, label='retained role')
        if type(row['role']) is not str or not row['role']:
            raise ValueError('SOURCE_ADMISSION_INVENTORY_MISMATCH')
        names.append(row['role'])
        _sha256(row['sha256'], label='retained digest')
    if names != sorted(set(names)):
        raise ValueError('SOURCE_ADMISSION_INVENTORY_MISMATCH')
    return doc


def build_legality_record(*, contract_sha256, domain_sha256, policy, geometry_bytes,
                         expected_geometry_sha256, source_admission_bytes) -> bytes:
    verify_static_legality(contract_sha256=contract_sha256, domain_sha256=domain_sha256,
        policy=policy, geometry_bytes=geometry_bytes, expected_geometry_sha256=expected_geometry_sha256)
    admission = parse_source_admission(source_admission_bytes, contract_sha256=contract_sha256,
                                       domain_sha256=domain_sha256, policy=policy)
    if expected_geometry_sha256 not in {row['sha256'] for row in admission['retained_roles']}:
        raise ValueError('SOURCE_ADMISSION_GEOMETRY_MISSING')
    return canonical_json_bytes({
        'schema': 'qualification_legality_result/v1', 'contract_sha256': contract_sha256,
        'trust_domain_sha256': domain_sha256, 'policy_sha256': policy.sha256,
        'geometry_source_sha256': expected_geometry_sha256,
        'source_admission_sha256': hashlib.sha256(source_admission_bytes).hexdigest(),
        'check_id': 'PRE_ADMISSION_REGISTRY_EMPTY', 'status': 'PASS',
    })
