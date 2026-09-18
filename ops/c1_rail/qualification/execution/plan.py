"""Active plan adapter over the shared pure N1 derivation."""
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
