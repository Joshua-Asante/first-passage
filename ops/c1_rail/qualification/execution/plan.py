"""Active N1 adapter and pure, non-authoritative campaign context adapter."""
from ..checkpoint_plan import derive_n1_plan as _derive
from ..seed_identity import seed_input, SeedInput
from ..policy import parse_policy
from ..policy_sources import build_qualification_policy


def derive_n1_plan(contract, *, attempt_id, exact_depth_approval_sha256):
    policy = parse_policy(build_qualification_policy())
    if contract.policy_sha256 != policy.sha256 or contract.trust_domain.policy_sha256 != policy.sha256:
        raise ValueError('POLICY_IDENTITY_MISMATCH')
    return _derive(contract,policy=policy,execution_release_sha256=contract.trust_domain.execution_release_sha256,
        attempt_id=attempt_id,exact_depth_approval_sha256=exact_depth_approval_sha256)


def derive_campaign_plan_from_context(context) -> bytes:
    """Compose retained verified inputs without IO, dispatch or persistence.

    Cross-binding checks detect mixed contexts, not signature freshness. Neither
    this function nor the resulting bytes is an execution authority boundary.
    """
    from .admission import ExecutionContext, _CONTEXT_ROLES
    from .release_schema import parse_release
    from .protocol import fields, identity, sha256
    from ..contract import require_validated_frozen_contract, parse_canonical_json
    from ..preflight import exact_depth_subject
    from ..checkpoint_plan import derive_campaign_plan, _campaign_seed_count

    if type(context) is not ExecutionContext:
        raise ValueError('verified ExecutionContext inputs required')
    release = parse_release(context.release.canonical_bytes)
    if release['authority_class'] != 'TEST_ONLY' or context.domain.authority_class != 'TEST_ONLY':
        raise ValueError('campaign planning requires TEST_ONLY authority')
    contract = require_validated_frozen_contract(context.contract)
    if (context.domain != contract.trust_domain
            or context.domain.sha256 != contract.trust_domain_sha256
            or context.domain.execution_release_sha256 != context.release.sha256
            or context.domain.execution_service_id != release['service_id']
            or context.policy.sha256 != release['qualification_policy_sha256']):
        raise ValueError('campaign context cross-binding differs')
    identity(context.attempt_id)
    index = fields(parse_canonical_json(context.retained_bundle_index, label='retained index'),
                   {'schema', 'attempt_id', 'entries'})
    if index['schema'] != 'qualification_retained_bundle/v1' or index['attempt_id'] != context.attempt_id:
        raise ValueError('campaign retained attempt binding differs')
    if type(index['entries']) is not list:
        raise ValueError('retained inventory required')
    roles, paths = [], set()
    total = len(context.retained_bundle_index)
    for row in index['entries']:
        fields(row, {'role', 'path', 'sha256', 'byte_length'})
        role = identity(row['role'])
        if type(row['path']) is not str or row['path'] in paths:
            raise ValueError('retained path binding differs')
        paths.add(row['path'])
        raw = context.retained_bytes.get(role)
        if (type(raw) is not bytes or type(row['byte_length']) is not int
                or row['byte_length'] != len(raw) or row['sha256'] != sha256(raw)):
            raise ValueError('retained bytes binding differs')
        total += len(raw)
        roles.append(role)
    if roles != sorted(set(roles)) or set(roles) != set(context.retained_bytes):
        raise ValueError('retained inventory binding differs')
    retained = context.retained_bytes
    by_role = {row['role']: row for row in index['entries']}
    if set(roles) != {artifact.role for artifact in contract.artifacts} | _CONTEXT_ROLES:
        raise ValueError('retained artifact inventory binding differs')
    for artifact in contract.artifacts:
        row = by_role[artifact.role]
        if row['path'] != artifact.path or row['sha256'] != artifact.sha256:
            raise ValueError('retained artifact binding differs from frozen contract')
    if sha256(retained['freeze_approval']) != contract.approval.approval_sha256:
        raise ValueError('freeze approval binding differs')
    expected = {'contract': contract.canonical_bytes, 'trust_domain': context.domain.canonical_bytes,
                'execution_release': context.release.canonical_bytes,
                'qualification_policy': context.policy.canonical_bytes}
    if any(retained.get(role) != raw for role, raw in expected.items()):
        raise ValueError('retained context binding differs')
    approval = context.exact_depth_approval
    approval_raw = retained.get('exact_depth_approval')
    if (type(approval_raw) is not bytes or sha256(approval_raw) != approval.approval_sha256
            or approval.authority_class != 'TEST_ONLY' or approval.scope != 'APPROVE_E1_EXACT_DEPTH'
            or approval.key_id not in context.domain.freeze_key_ids
            or approval.contract_sha256 != contract.contract_sha256
            or approval.subject_sha256 != sha256(exact_depth_subject(contract, attempt_id=context.attempt_id))):
        raise ValueError('exact-depth approval binding differs')
    profile = context.profile
    if total > profile.input_byte_limit:
        raise ValueError('retained bundle exceeds profile input limit')
    # Conservative allocation screen, not a measured resource guarantee. The
    # plan is an input artifact; N1 worker output/RPC limits grant no FULL_E1 route.
    if _campaign_seed_count(contract) * 4096 > min(profile.memory_bytes, contract.replay.budget.maximum_memory_bytes):
        raise ValueError('campaign inventory exceeds planning memory screen')
    raw = derive_campaign_plan(contract, policy=context.policy,
        execution_release_sha256=context.release.sha256, source_bundle_sha256=context.bundle_sha256,
        attempt_id=context.attempt_id, exact_depth_approval_sha256=approval.approval_sha256)
    if len(raw) > profile.input_byte_limit:
        raise ValueError('campaign plan exceeds profile input limit')
    return raw
