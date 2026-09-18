"""Service-owned v2 preflight identity; it attests no execution or completion."""
from ..contract import canonical_json_bytes as encoded
from ..preflight import exact_depth_subject
from .admission import ExecutionContext
from .plan import derive_n1_plan
from .protocol import ExecutionRecord,identity,sha256


def build_binding(context,record,plan_bytes):
    if type(context) is not ExecutionContext or type(record) is not ExecutionRecord:
        raise ValueError('verified context and reserved service record required')
    expected=derive_n1_plan(context.contract,attempt_id=context.attempt_id,
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)
    if type(plan_bytes) is not bytes or plan_bytes!=expected or record.plan_sha256!=sha256(expected) or record.attempt_id!=context.attempt_id:
        raise ValueError('reserved preflight plan binding differs')
    return encoded(dict(schema='e1_preflight_binding/v2',attempt_id=context.attempt_id,
        contract_sha256=context.contract.contract_sha256,trust_domain_sha256=context.domain.sha256,
        execution_release_sha256=context.release.sha256,policy_sha256=context.policy.sha256,
        exact_depth_subject_sha256=sha256(exact_depth_subject(context.contract,attempt_id=context.attempt_id)),
        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
        bundle_sha256=context.bundle_sha256,plan_sha256=sha256(plan_bytes),
        output_identity=dict(service_id=identity(context.domain.execution_service_id),
            execution_id=identity(record.execution_id),checkpoint='N1')))
