"""Pure N1 input derivation shared by capture and evidence reconstruction."""
import hashlib

from .contract import canonical_json_bytes, parse_canonical_json, _sha256, _text
from .seed_identity import seed_input
from .policy import _document


def derive_n1_plan(contract, *, policy, execution_release_sha256, attempt_id,
                   exact_depth_approval_sha256):
    _text(attempt_id, label='attempt')
    _sha256(execution_release_sha256, label='release')
    _sha256(exact_depth_approval_sha256, label='depth approval')
    resolved = _document(policy)
    original = parse_canonical_json(contract.canonical_bytes, label='contract')
    sha = lambda raw: hashlib.sha256(raw).hexdigest()
    def seed(stage, population, index):
        return parse_canonical_json(seed_input(contract,stage=stage,population=population,
            panel_index=None,path_index=index,synthetic=contract.trust_domain.permits_synthetic).canonical_bytes,label='seed')
    depths, seeds, proofs = [], [], []
    for population in resolved['stage_populations']['N1']:
        counts = contract.stage_specs['N1'].population_counts[population]
        if type(counts) is not tuple or len(counts) != 1 or type(counts[0]) is not int or counts[0] <= 0:
            raise ValueError('single exact N1 depth required')
        depths.append({'population':population,'depth':counts[0]})
        seeds.extend(seed('n1',population,index) for index in range(counts[0]))
        proofs.append(dict(population=population,horizon_sessions=len(contract.populations[population]),
                           source_session_ids_sha256=sha(canonical_json_bytes(list(contract.populations[population])))))
    return canonical_json_bytes(dict(schema='qualification_checkpoint_plan/v2',checkpoint='N1',attempt_id=attempt_id,
        contract_sha256=contract.contract_sha256,trust_domain_sha256=contract.trust_domain_sha256,
        policy_sha256=policy.sha256,execution_release_sha256=execution_release_sha256,
        authority_class=contract.trust_domain.authority_class,exact_depth_approval_sha256=exact_depth_approval_sha256,
        depths=depths,horizon_sessions=contract.replay.horizon_sessions,
        initial_state_sha256=sha(canonical_json_bytes(original['initial_state'])),
        replay_sha256=sha(canonical_json_bytes(original['replay'])),budget=original['replay']['budget'],
        mechanics_version='tb-s2-rng-v2',seed_inputs=seeds,source_proofs=proofs,probe=seed('probe','FULL',0)))
