"""V2 preflight binds service-owned output identity, never client paths."""
import importlib
import json
import pytest
from c1_rail.qualification.execution.admission import verify_bundle
from c1_rail.qualification.execution.plan import derive_n1_plan
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.execution.store import ExecutionStore
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from bundle_fixture import build_bundle
from test_contract import NOW


def test_v2_preflight_binds_reserved_execution_and_original_approval(tmp_path):
    case=build_bundle(tmp_path/'bundle',idle=True)
    context=verify_bundle(case['root'],case['release'],case['keys'],NOW)
    plan=derive_n1_plan(context.contract,attempt_id=context.attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)
    store=ExecutionStore(tmp_path/'journal.sqlite')
    record=store.reserve(encoded(dict(operation='SUBMIT_N1',attempt_id=context.attempt_id,
        bundle_sha256=context.bundle_sha256)),plan,now=NOW)
    module=importlib.import_module('c1_rail.qualification.execution.preflight')
    raw=module.build_binding(context,record,plan)
    doc=json.loads(raw)
    assert doc['schema']=='e1_preflight_binding/v2' and 'output_root' not in doc
    assert doc['output_identity']==dict(service_id='test-service',execution_id=record.execution_id,checkpoint='N1')
    assert doc['plan_sha256']==sha256(plan)
    assert doc['exact_depth_approval_sha256']==context.exact_depth_approval.approval_sha256
    assert doc['bundle_sha256']==context.bundle_sha256
    mutated=json.loads(plan); mutated['attempt_id']='foreign'
    with pytest.raises(ValueError): module.build_binding(context,record,encoded(mutated))


def test_client_path_preflight_cannot_reserve_v2_output(tmp_path):
    from c1_rail.qualification.preflight import validate_e1_preflight
    case=build_bundle(tmp_path/'bundle',idle=True)
    with pytest.raises(ValueError,match='SERVICE_OWNED_PREFLIGHT_REQUIRED'):
        validate_e1_preflight(case['contract'],attempt_id=case['attempt_id'],output_root=tmp_path/'client-output',
            exact_depth_approval_bytes=case['payloads']['exact_depth_approval'],trusted_keys=case['keys'],now=NOW,
            trust_domain=case['contract'].trust_domain)
    assert not (tmp_path/'client-output').exists()
