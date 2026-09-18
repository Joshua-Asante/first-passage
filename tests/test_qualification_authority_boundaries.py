"""Legacy APIs cannot issue active authority after the protected v2 cutover."""
import pytest
from c1_rail.qualification import seal,orchestration


@pytest.mark.parametrize('operation',['authenticate','claim','commit','seal','production','executor'])
def test_legacy_active_entrypoints_require_execution_attestation(operation):
    with pytest.raises(ValueError,match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        if operation=='authenticate':
            seal.authenticate_result(None,b'{}',trusted_keys={},now=None,trust_domain=None)
        elif operation=='claim':
            seal.authenticated_result_claim(None,trusted_keys={},now=None,trust_domain=None)
        elif operation=='commit':
            seal.commit_authenticated_result(None,None,trusted_keys={},now=None,trust_domain=None)
        elif operation=='seal':
            seal.seal_e1_pass(None,b'{}',sealed_utc=None,trusted_keys={},now=None,
                result_trusted_keys={},attempt_store=None,trust_domain=None)
        elif operation=='executor':
            from c1_rail.qualification.production import ProductionExecutor
            ProductionExecutor(None,None,None)
        else:
            orchestration.run_production_e1(None,source=None,store=None,preflight=None,
                exact_depth_approval_bytes=b'',trusted_keys={},now=None)
