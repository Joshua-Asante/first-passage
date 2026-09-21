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


def run_worker(input_dir: Path, *, execution_id: str, campaign_limits=None) -> bytes:
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
    # FULL_E1 (D3): the phase-limited guard over the remaining N1 limits, never
    # a fresh contract allowance; N1_ONLY keeps the contract guard unchanged.
    budget = PhaseBudgetGuard(campaign_limits) if campaign_limits is not None \
        else BudgetGuard.from_contract(context.contract)
    run = run_n1_compute(context.contract, admitted.source, budget)
    observations = budget.check_and_measure()
    observations.pop('remaining_wall_seconds')
    raw = encode_worker_result(context, execution_id, plan, run, observations,admitted=admitted)
    captured = parse_worker_result(raw, context=context, execution_id=execution_id, plan_bytes=plan,
                                   campaign_limits=campaign_limits)
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
    # The campaign output mount (D3): present only for the guardian-launched
    # FULL_E1 worker. Its argv selects the probe's readiness handshake and the
    # mounted-file capture; without it the N1_ONLY stdout framing is exact.
    parser.add_argument('--output', choices=['/output'])
    parser.add_argument('--campaign-limits')
    args = parser.parse_args()
    release = read_regular(Path(args.input), 'installation/release.json', limit=BOOTSTRAP_BYTE_LIMIT)
    measure_runtime(installed_code_root(), 'worker', release)
    if args.output is not None or args.campaign_limits is not None:
        from .campaign_probe import await_resume, block_resume_signal
        # The bootstrap-level block is verified before any compute import runs;
        # the readiness token tells the guardian this payload is resume-able.
        block_resume_signal()
        if await_resume() is None:
            raise SystemExit('supervisor resume signal absent')
    limits = None
    if args.campaign_limits is not None:
        limits = parse_canonical_json(read_regular(Path(args.input), args.campaign_limits,
                                                   limit=BOOTSTRAP_BYTE_LIMIT), label='campaign work limits')
    frame = run_worker(Path(args.input), execution_id=args.execution_id, campaign_limits=limits)
    if args.output is None:
        sys.stdout.buffer.write(frame)
        sys.stdout.buffer.flush()
        return
    # The bounded output mount owned by the work: the frame lands as one file the
    # guardian reads after PAYLOAD_EXIT and archives byte-for-byte.
    destination = Path(args.output) / 'result.frame'
    with destination.open('xb') as stream:
        stream.write(frame)
        stream.flush()
        import os as _os
        _os.fsync(stream.fileno())
    destination.chmod(0o644)


from .campaign_probe import main as campaign_probe_main

class PhaseBudgetGuard:
    """The FULL_E1 worker's secondary bound (D3): the work's remaining phase limits.

    Not ``BudgetGuard.from_contract``: a campaign worker never re-derives a
    fresh full-campaign allowance. The guardian stages the remaining N1 limits
    (phase cpu_ns minus its orchestration charge, remaining wall, memory) with
    the input; this guard enforces exactly those and reports the same three
    observations the settlement compares.
    """

    def __init__(self, limits):
        from .protocol import fields, positive
        values = fields(limits, {'cpu_ns', 'wall_ns', 'memory_bytes'})
        for name in values:
            positive(values[name])
        self.limits = dict(values)
        import time
        self._process = time.process_time_ns
        self._monotonic = time.monotonic_ns
        self._start_cpu = self._process()
        self._start_wall = self._monotonic()

    def check_and_measure(self):
        cpu = self._process() - self._start_cpu
        wall = self._monotonic() - self._start_wall
        if cpu > self.limits['cpu_ns'] or wall >= self.limits['wall_ns']:
            raise ValueError('campaign work exceeded its remaining phase limits')
        try:
            import resource
            peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        except (ImportError, AttributeError):
            peak = 0
        if peak > self.limits['memory_bytes']:
            raise ValueError('campaign work exceeded its phase memory limit')
        return dict(worker_compute_wall_ns=wall, worker_cpu_ns=cpu,
                    worker_peak_memory_bytes=peak, remaining_wall_seconds=(self.limits['wall_ns'] - wall) / 1e9)
