"""Fixed N1 worker adapter; no journal, launcher or private-key imports."""
from datetime import datetime, timezone
from pathlib import Path

from ..contract import canonical_json_bytes, parse_canonical_json
from ..source_admission import admit_source
from .admission import verify_bundle
from .budget import BudgetGuard
from .compute import run_n1_compute
from .evidence import encode_worker_result, parse_worker_result
from .files import read_regular
from .keys import load_keys
from .plan import derive_n1_plan
from .protocol import encode_frame, identity

BOOTSTRAP_BYTE_LIMIT = 16 * 1024 * 1024


def utc_now():
    return datetime.now(timezone.utc)


def run_worker(input_dir: Path, *, execution_id: str) -> bytes:
    identity(execution_id)
    root = Path(input_dir)
    release = read_regular(root, 'installation/release.json', limit=BOOTSTRAP_BYTE_LIMIT)
    authority = parse_canonical_json(release, label='installed release')['authority_class']
    keys = load_keys(read_regular(root, 'installation/keys.json', limit=BOOTSTRAP_BYTE_LIMIT), authority_class=authority)
    context = verify_bundle(root / 'bundle', release, keys, utc_now())
    if context.domain.authority_class != 'TEST_ONLY' or not context.domain.permits_synthetic:
        raise ValueError('N1_ONLY release forbids production execution')
    plan = read_regular(root, 'plan.json', limit=context.profile.input_byte_limit)
    expected = derive_n1_plan(context.contract, attempt_id=context.attempt_id,
                             exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)
    if plan != expected:
        raise ValueError('worker independently derived plan differs')
    admitted = admit_source(context.contract,artifact_root=context.bundle_dir,policy=context.policy)
    # Preserve the original starting point: after source admission, immediately
    # before provider construction (which includes all three source proofs).
    budget = BudgetGuard.from_contract(context.contract)
    run = run_n1_compute(context.contract, admitted.source, budget)
    observations = budget.check_and_measure()
    observations.pop('remaining_wall_seconds')
    raw = encode_worker_result(context, execution_id, plan, run, observations,admitted=admitted)
    captured = parse_worker_result(raw, context=context, execution_id=execution_id, plan_bytes=plan)
    frame = encode_frame(raw, limit=context.profile.output_byte_limit)
    # Retain a real measurement after construction, validation and full framing.
    # Release the provisional buffers before serializing the updated document.
    del raw, frame
    observations = budget.check_and_measure()
    observations.pop('remaining_wall_seconds')
    captured.document['observations'] = observations
    frame = encode_frame(canonical_json_bytes(captured.document), limit=context.profile.output_byte_limit)
    # Stamping the measurement cannot include its own serialization cost in the
    # retained sample, but that final work must still satisfy every budget.
    budget.check_and_measure()
    return frame


def main():
    import argparse
    import sys
    from .runtime import measure_runtime, installed_code_root
    parser = argparse.ArgumentParser()
    parser.add_argument('--execution-id', required=True)
    parser.add_argument('--input', required=True, choices=['/input'])
    args = parser.parse_args()
    release = read_regular(Path(args.input), 'installation/release.json', limit=BOOTSTRAP_BYTE_LIMIT)
    measure_runtime(installed_code_root(), 'worker', release)
    sys.stdout.buffer.write(run_worker(Path(args.input), execution_id=args.execution_id))
    sys.stdout.buffer.flush()


from .campaign_probe import main as campaign_probe_main
