"""Canonical pure N1 inputs and non-authoritative full-campaign plans."""

import hashlib

from .contract import canonical_json_bytes, parse_canonical_json, _sha256, _text
from .seed_identity import seed_input
from .policy import _document


def derive_n1_plan(
    contract, *, policy, execution_release_sha256, attempt_id, exact_depth_approval_sha256
):
    _text(attempt_id, label='attempt')
    _sha256(execution_release_sha256, label='release')
    _sha256(exact_depth_approval_sha256, label='depth approval')
    resolved = _document(policy)
    original = parse_canonical_json(contract.canonical_bytes, label='contract')
    sha = lambda raw: hashlib.sha256(raw).hexdigest()

    def seed(stage, population, index):
        return parse_canonical_json(
            seed_input(
                contract,
                stage=stage,
                population=population,
                panel_index=None,
                path_index=index,
                synthetic=contract.trust_domain.permits_synthetic,
            ).canonical_bytes,
            label='seed',
        )

    depths, seeds, proofs = [], [], []
    for population in resolved['stage_populations']['N1']:
        counts = contract.stage_specs['N1'].population_counts[population]
        if (
            type(counts) is not tuple
            or len(counts) != 1
            or type(counts[0]) is not int
            or counts[0] <= 0
        ):
            raise ValueError('single exact N1 depth required')
        depths.append({'population': population, 'depth': counts[0]})
        seeds.extend(seed('n1', population, index) for index in range(counts[0]))
        proofs.append(
            dict(
                population=population,
                horizon_sessions=len(contract.populations[population]),
                source_session_ids_sha256=sha(
                    canonical_json_bytes(list(contract.populations[population]))
                ),
            )
        )
    return canonical_json_bytes(
        dict(
            schema='qualification_checkpoint_plan/v2',
            checkpoint='N1',
            attempt_id=attempt_id,
            contract_sha256=contract.contract_sha256,
            trust_domain_sha256=contract.trust_domain_sha256,
            policy_sha256=policy.sha256,
            execution_release_sha256=execution_release_sha256,
            authority_class=contract.trust_domain.authority_class,
            exact_depth_approval_sha256=exact_depth_approval_sha256,
            depths=depths,
            horizon_sessions=contract.replay.horizon_sessions,
            initial_state_sha256=sha(canonical_json_bytes(original['initial_state'])),
            replay_sha256=sha(canonical_json_bytes(original['replay'])),
            budget=original['replay']['budget'],
            mechanics_version='tb-s2-rng-v2',
            seed_inputs=seeds,
            source_proofs=proofs,
            probe=seed('probe', 'FULL', 0),
        )
    )


# Representation limits, not statistical depths or execution allowances. Check
# before allocating seed inventories; never silently truncate a frozen workload.
_CAMPAIGN_MAX_SEED_INPUTS = 100_000
_CAMPAIGN_MAX_BYTES = 64 * 1024 * 1024


def derive_checkpoint_plan(campaign_plan_bytes, checkpoint, predecessor_receipt_bytes):
    """Canonical bytes of one checkpoint's plan, sliced from the retained campaign plan.

    Pure and closed: `campaign_plan_bytes` must be the retained canonical campaign
    plan; the returned bytes are the canonical `n1` sub-document exactly as the
    campaign plan embeds it (byte-identical to ``derive_n1_plan`` for N1). A
    predecessor receipt is refused for N1 (there is no earlier checkpoint) and
    required-but-unsupported for any later checkpoint until its slice lands.
    """
    if type(campaign_plan_bytes) is not bytes or len(campaign_plan_bytes) > _CAMPAIGN_MAX_BYTES:
        raise ValueError('bounded retained campaign plan required')
    doc = parse_canonical_json(campaign_plan_bytes, label='retained campaign plan')
    if type(doc) is not dict or doc.get('schema') != 'qualification_campaign_plan/v1':
        raise ValueError('retained canonical campaign plan required')
    if checkpoint == 'N1':
        if predecessor_receipt_bytes is not None:
            raise ValueError('N1 has no predecessor receipt')
        raw = canonical_json_bytes(doc['n1'])
        if parse_canonical_json(raw, label='N1 sub-plan').get('checkpoint') != 'N1':
            raise ValueError('campaign plan N1 sub-document differs')
        return raw
    raise ValueError('unsupported checkpoint selection')


def _campaign_inputs(contract, policy, execution_release_sha256):
    from .contract import require_validated_frozen_contract
    from .policy import validate_contract_semantics

    require_validated_frozen_contract(contract)
    resolved = _document(policy)
    domain = contract.trust_domain
    if domain.authority_class != 'TEST_ONLY' or domain.permits_synthetic is not True:
        raise ValueError('campaign planning requires TEST_ONLY authority')
    if (
        contract.policy_sha256 != policy.sha256
        or domain.policy_sha256 != policy.sha256
        or domain.execution_release_sha256 != execution_release_sha256
    ):
        raise ValueError('campaign policy/release binding differs')
    original = parse_canonical_json(contract.canonical_bytes, label='contract')
    if original['schema'] != 'frozen_qualification_contract/v2':
        raise ValueError('campaign planning requires v2 frozen inputs')
    validate_contract_semantics(original, policy, workload_policy=domain.workload_policy)
    return original, resolved


def _campaign_seed_count(contract):
    budget = contract.replay.budget
    # The N1 probe appears in the inherited subplan and the checkpoint inventory.
    return (
        budget.n1_paths
        + budget.n2_paths
        + budget.part_a_expanded_paths
        + contract.replay.part_a.expanded_panels
        + 5
    )


def derive_campaign_plan(
    contract,
    *,
    policy,
    execution_release_sha256: str,
    source_bundle_sha256: str,
    attempt_id: str,
    exact_depth_approval_sha256: str,
) -> bytes:
    """Return bounded canonical planning bytes, never execution authority.

    Requires unchanged validator-issued frozen inputs for consistency. Signature
    freshness and authority consumption remain outside this pure planning API.
    """
    _text(attempt_id, label='attempt')
    if type(attempt_id) is not str or len(attempt_id) > 128:
        raise ValueError('bounded attempt identity required')
    for label, value in (
        ('release', execution_release_sha256),
        ('source bundle', source_bundle_sha256),
        ('depth approval', exact_depth_approval_sha256),
    ):
        _sha256(value, label=label)
    original, resolved = _campaign_inputs(contract, policy, execution_release_sha256)
    count = _campaign_seed_count(contract)
    if count > _CAMPAIGN_MAX_SEED_INPUTS:
        raise ValueError('campaign seed inventory exceeds representation limit')
    # Bound variable-length source identities/namespaces as well as entry count.
    # Each entry includes hashes, not a copied source session inventory.
    namespace_bytes = len(canonical_json_bytes(contract.replay.root_rng_namespace))
    if len(contract.canonical_bytes) + count * (namespace_bytes + 1024) > _CAMPAIGN_MAX_BYTES:
        raise ValueError('campaign plan exceeds representation byte limit')

    sha = lambda value: hashlib.sha256(canonical_json_bytes(value)).hexdigest()

    def seed(stage, population, index, *, panel=None, purpose='path'):
        return parse_canonical_json(
            seed_input(
                contract,
                stage=stage,
                population=population,
                panel_index=panel,
                path_index=index,
                synthetic=True,
                purpose=purpose,
            ).canonical_bytes,
            label='campaign seed',
        )

    from .policy import ATTESTED_CHECKPOINTS

    groups = [
        {'checkpoint': name, 'stages': resolved['checkpoint_groups'][name]}
        for name in ATTESTED_CHECKPOINTS
    ]
    n1 = parse_canonical_json(
        derive_n1_plan(
            contract,
            policy=policy,
            execution_release_sha256=execution_release_sha256,
            attempt_id=attempt_id,
            exact_depth_approval_sha256=exact_depth_approval_sha256,
        ),
        label='N1 plan',
    )
    depths, seeds, thresholds = [], [], []
    for stage in resolved['checkpoint_groups']['N2']:
        spec = contract.stage_specs[stage]
        thresholds.append(
            {
                'stage': stage,
                'exact_depth': spec.exact_depth,
                'max_failures_per_population': spec.max_failures_per_population,
            }
        )
        for population in resolved['stage_populations'][stage]:
            (depth,) = spec.population_counts[population]
            depths.append({'population': population, 'depth': depth, 'statistics_stage': stage})
            seeds.extend(seed('n2', population, index) for index in range(depth))
    part = contract.replay.part_a
    panels = [
        {
            'panel_index': panel,
            'outer_seed': seed('n2', 'FULL', 0, panel=panel, purpose='outer'),
            'path_seeds': [
                seed('n2', 'FULL', index, panel=panel)
                for index in range(part.paths_per_population_per_panel)
            ],
        }
        for panel in range(part.expanded_panels)
    ]
    replay = original['replay']
    doc = dict(
        schema='qualification_campaign_plan/v1',
        purpose='PLANNING_ONLY',
        target_capability='FULL_E1',
        authorizes_dispatch=False,
        authority_class='TEST_ONLY',
        attempt_id=attempt_id,
        contract_sha256=contract.contract_sha256,
        trust_domain_sha256=contract.trust_domain_sha256,
        policy_sha256=policy.sha256,
        execution_release_sha256=execution_release_sha256,
        source_bundle_sha256=source_bundle_sha256,
        exact_depth_approval_sha256=exact_depth_approval_sha256,
        initial_state_sha256=sha(original['initial_state']),
        replay_sha256=sha(replay),
        root_rng_namespace=replay['root_rng_namespace'],
        mechanics_version=n1['mechanics_version'],
        budget=replay['budget'],
        budget_sha256=sha(replay['budget']),
        checkpoint_groups=groups,
        cutoff={
            'checkpoint': 'CUTOFF',
            'stages': resolved['checkpoint_groups']['CUTOFF'],
            'thresholds': thresholds,
            'seed_inputs': [],
        },
        n1=n1,
        n2={'depths': depths, 'seed_inputs': seeds},
        part_a={
            'parameters': replay['part_a'],
            'initial_panel_range': [0, part.initial_panels],
            'potential_appended_panel_range': [part.initial_panels, part.expanded_panels],
            'potential_panels': panels,
        },
        probes=[
            {'checkpoint': 'N1', 'seed_inputs': [n1['probe']]},
            {'checkpoint': 'N2', 'seed_inputs': [seed('probe', 'FULL', 0)]},
            {
                'checkpoint': 'PART_A',
                'seed_inputs': [
                    seed('probe', 'FULL', index, panel=0, purpose='probe') for index in (0, 1)
                ],
            },
        ],
    )
    raw = canonical_json_bytes(doc)
    if len(raw) > _CAMPAIGN_MAX_BYTES:
        raise ValueError('campaign plan exceeds representation byte limit')
    return raw


def validate_campaign_plan(
    raw: bytes,
    *,
    contract,
    policy,
    execution_release_sha256: str,
    source_bundle_sha256: str,
    attempt_id: str,
    exact_depth_approval_sha256: str,
) -> dict:
    """Re-derive from frozen inputs and require exact canonical byte equality."""
    if type(raw) is not bytes or len(raw) > _CAMPAIGN_MAX_BYTES:
        raise ValueError('bounded campaign plan bytes required')
    expected = derive_campaign_plan(
        contract,
        policy=policy,
        execution_release_sha256=execution_release_sha256,
        source_bundle_sha256=source_bundle_sha256,
        attempt_id=attempt_id,
        exact_depth_approval_sha256=exact_depth_approval_sha256,
    )
    # Comparing bytes first rejects unknown fields, bool/int aliases, duplicate
    # keys and arbitrary nesting without parsing hostile declarations at all.
    if raw != expected:
        raise ValueError('campaign plan differs from canonical frozen inputs')
    return parse_canonical_json(expected, label='campaign plan')
