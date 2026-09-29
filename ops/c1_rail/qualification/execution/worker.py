"""Fixed N1 worker adapter; no journal, launcher or private-key imports."""

from datetime import datetime, timezone
from pathlib import Path

from ..contract import canonical_json_bytes, parse_canonical_json
from ..source_admission import admit_source
from .admission import verify_bundle
from .budget import BudgetGuard
from .compute import (
    PART_A_OUTCOME_STATUSES,
    run_n1_compute,
    run_n2_compute,
    run_part_a_compute,
)
from .evidence import PartAWorkerRun, encode_worker_result, parse_worker_result
from .files import read_regular
from .keys import load_keys
from .plan import derive_n1_plan
from ..checkpoint_plan import derive_checkpoint_plan
from .protocol import digest, encode_frame, fields, identity, sha256

BOOTSTRAP_BYTE_LIMIT = 16 * 1024 * 1024


def utc_now():
    return datetime.now(timezone.utc)


def run_worker(
    input_dir: Path, *, execution_id: str, campaign_limits=None, checkpoint='N1',
    output_dir=None,
) -> bytes:
    identity(execution_id)
    root = Path(input_dir)
    release = read_regular(root, 'installation/release.json', limit=BOOTSTRAP_BYTE_LIMIT)
    authority = parse_canonical_json(release, label='installed release')['authority_class']
    keys = load_keys(
        read_regular(root, 'installation/keys.json', limit=BOOTSTRAP_BYTE_LIMIT),
        authority_class=authority,
    )
    context = verify_bundle(root / 'bundle', release, keys, utc_now())
    if context.domain.authority_class != 'TEST_ONLY' or not context.domain.permits_synthetic:
        raise ValueError('N1_ONLY release forbids production execution')
    plan = read_regular(root, 'plan.json', limit=context.profile.input_byte_limit)
    staged = None
    if checkpoint == 'N2':
        from .plan import derive_campaign_plan_from_context

        predecessor = read_regular(
            root, 'predecessor-receipt.json', limit=BOOTSTRAP_BYTE_LIMIT
        )
        expected = derive_checkpoint_plan(
            derive_campaign_plan_from_context(context), 'N2', predecessor
        )
    elif checkpoint == 'PART_A':
        from .plan import derive_campaign_plan_from_context

        # S5 (W1): the guardian stages the committed joint N2 custody -- the
        # receipt, the assessment and the capture payload; the plan derives
        # from the staged receipt exactly as the N2 path derives its own.
        staged = {
            name: read_regular(
                root, 'predecessor-' + name + '.json', limit=BOOTSTRAP_BYTE_LIMIT
            )
            for name in PART_A_STAGED_ROLES
        }
        expected = derive_checkpoint_plan(
            derive_campaign_plan_from_context(context), 'PART_A', staged['receipt']
        )
    else:
        expected = derive_n1_plan(
            context.contract,
            attempt_id=context.attempt_id,
            exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256,
        )
    if plan != expected:
        raise ValueError('worker independently derived plan differs')
    admitted = admit_source(
        context.contract, artifact_root=context.bundle_dir, policy=context.policy
    )
    # Preserve the original starting point: after source admission, immediately
    # before provider construction (which includes all three source proofs).
    # FULL_E1 (D3): the phase-limited guard over the remaining N1 limits, never
    # a fresh contract allowance; N1_ONLY keeps the contract guard unchanged.
    budget = (
        PhaseBudgetGuard(campaign_limits)
        if campaign_limits is not None
        else BudgetGuard.from_contract(context.contract)
    )
    if checkpoint == 'PART_A':
        if output_dir is None:
            raise ValueError('PART_A requires the campaign output mount')
        run = run_part_a_body(
            context, plan, staged, admitted, budget, output_dir,
            measurement_override=None,
        )
    else:
        compute = run_n2_compute if checkpoint == 'N2' else run_n1_compute
        run = compute(context.contract, admitted.source, budget)
    observations = budget.check_and_measure()
    observations.pop('remaining_wall_seconds')
    raw = encode_worker_result(context, execution_id, plan, run, observations, admitted=admitted)
    captured = parse_worker_result(
        raw,
        context=context,
        execution_id=execution_id,
        plan_bytes=plan,
        campaign_limits=campaign_limits,
    )
    frame = encode_frame(raw, limit=context.profile.output_byte_limit)
    # Retain a real measurement after construction, validation and full framing.
    # Release the provisional buffers before serializing the updated document.
    del raw, frame
    observations = budget.check_and_measure()
    observations.pop('remaining_wall_seconds')
    captured.document['observations'] = observations
    frame = encode_frame(
        canonical_json_bytes(captured.document), limit=context.profile.output_byte_limit
    )
    # Stamping the measurement cannot include its own serialization cost in the
    # retained sample, but that final work must still satisfy every budget.
    budget.check_and_measure()
    return frame


# ---- S5 PART_A: staged predecessor custody and the SR-3 worker body ----------
#
# S5-D1/S5-D2 (packet section 0.5) with section 1a SR-3/SR-4: one PART_A
# operation reads the guardian's staged predecessor bytes, derives the N2 FULL
# baseline from the captured outcomes (never a passed-in number), runs the
# adapter once, and writes both prefix artifacts through one SR-4 writer.

PART_A_INITIAL_ARTIFACT = 'part-a-initial.jsonl'
PART_A_FINAL_ARTIFACT = 'part-a-final.jsonl'
PART_A_STAGED_ROLES = ('receipt', 'assessment', 'payload')


def write_part_a_artifact(directory, name, raw):
    """SR-4: the one S5-D1 artifact writer shared by the route and Stage 1c.

    Creates the named artifact exclusively, flushes and fsyncs it, then marks
    it read-only by convention. The initial-prefix artifact is written through
    the adapter's custody hook, before the adapter's own decision point and
    before any panel at or above the initial count is sampled; the final
    artifact is written after the computation returns. A custody failure
    propagates: no final artifact and no result follow it.
    """
    import os

    if name not in (PART_A_INITIAL_ARTIFACT, PART_A_FINAL_ARTIFACT):
        raise ValueError('closed Part A artifact names required')
    if type(raw) is not bytes:
        raise ValueError('Part A artifact bytes required')
    destination = Path(directory) / name
    with destination.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    destination.chmod(0o444)


def _part_a_staged_bytes(staged):
    """W1: the three staged predecessor byte strings, closed by role."""
    rows = fields(staged, set(PART_A_STAGED_ROLES))
    for raw in rows.values():
        if type(raw) is not bytes or not raw:
            raise ValueError('staged PART_A predecessor bytes required')
    return rows


def _verify_part_a_predecessor(plan_bytes, staged):
    """W1: bind the staged capture bytes through the receipt and the assessment.

    The staged assessment must hash to the receipt's ``assessment_sha256``, the
    staged payload to the assessment's capture digest, and the independently
    derived plan's predecessor block must name exactly these staged bytes; any
    mismatch refuses before any source admission or compute (the capture
    digest is bound transitively through the receipt and the assessment).
    """
    rows = _part_a_staged_bytes(staged)
    receipt = parse_canonical_json(rows['receipt'], label='staged N2 predecessor receipt')
    assessment = parse_canonical_json(
        rows['assessment'], label='staged N2 predecessor assessment'
    )
    if (
        type(receipt) is not dict
        or type(assessment) is not dict
        or receipt.get('schema') != 'qualification_campaign_checkpoint_receipt/v1'
        or receipt.get('checkpoint') != 'N2'
        or assessment.get('schema') != 'qualification_campaign_checkpoint_assessment/v1'
        or assessment.get('checkpoint') != 'N2'
        or assessment.get('decision') != 'CONTINUE'
    ):
        raise ValueError('staged N2 predecessor checkpoint documents differ')
    assessment_binding = receipt.get('assessment_sha256')
    digest(assessment_binding)
    capture = fields(
        assessment.get('capture'), {'result_sha256', 'payload_sha256', 'attestation_sha256'}
    )
    digest(capture['payload_sha256'])
    if sha256(rows['assessment']) != assessment_binding:
        raise ValueError('staged N2 assessment differs from the receipt binding')
    if sha256(rows['payload']) != capture['payload_sha256']:
        raise ValueError('staged N2 capture payload differs from the assessment binding')
    plan = parse_canonical_json(plan_bytes, label='PART_A plan')
    if (
        type(plan) is not dict
        or plan.get('checkpoint') != 'PART_A'
        or plan.get('predecessor')
        != {
            'checkpoint': 'N2',
            'receipt_sha256': sha256(rows['receipt']),
            'assessment_sha256': sha256(rows['assessment']),
        }
    ):
        raise ValueError('PART_A plan predecessor binding differs')
    return rows


def n2_full_outcomes_from_payload(payload_bytes):
    """S5-D2 (W2): the captured N2 FULL population's outcome statuses, in order.

    The full parse against the N2 plan cannot run here: deriving that plan
    needs the committed N1 receipt, which the PART_A input mount does not
    stage. This reads the canonical capture payload with a closed-field check
    instead (population FULL, stage N2, every status in the closed set) and
    returns the status tuple; the pass rate itself is derived inside
    ``run_part_a_compute``, never passed in as a number.
    """
    payload = fields(
        parse_canonical_json(payload_bytes, label='staged N2 capture payload'),
        {
            'schema',
            'execution_id',
            'plan_sha256',
            'source_admission',
            'legality',
            'populations',
            'path_inventory',
            'runtime_load_manifest',
            'observations',
        },
    )
    if payload['schema'] != 'qualification_worker_result/v1':
        raise ValueError('staged N2 capture payload schema differs')
    populations = payload['populations']
    if type(populations) is not list or not populations:
        raise ValueError('staged N2 capture populations required')
    row = fields(populations[0], {'population', 'stage', 'outcomes'})
    outcomes = row['outcomes']
    if (
        row['population'] != 'FULL'
        or row['stage'] != 'N2'
        or type(outcomes) is not list
        or not outcomes
    ):
        raise ValueError('captured N2 FULL population required')
    statuses = []
    for outcome in outcomes:
        fields(outcome, {'status', 'sessions_to_pass', 'failure_reason', 'diagnostics'})
        if outcome['status'] not in PART_A_OUTCOME_STATUSES:
            raise ValueError('captured N2 FULL outcome status differs')
        statuses.append(outcome['status'])
    return tuple(statuses)


def run_part_a_body(
    context, plan_bytes, staged, admitted, budget, output_dir,
    *, measurement_override=None,
):
    """SR-3 (section 1a): the one store-free PART_A worker body.

    ``run_worker`` calls this object for the PART_A checkpoint and the Stage 1c
    measurement calls the same object (P-7); the route never passes
    ``measurement_override`` (P-3). Source admission precedes this body, as
    for N1/N2 (``admitted`` is the route's single admission, and this body
    uses its source). Covers exactly the staged-predecessor checks (W1), the
    captured N2 FULL outcome parse (S5-D2), one adapter computation whose
    custody hook writes and fsyncs the initial-prefix artifact before the
    adapter's decision point, and the final artifact write. Returns the
    ``PartAWorkerRun``: the ``PartACompute`` beside the N2 FULL baseline this
    body derived from the staged statuses (W5a).
    """
    if output_dir is None:
        raise ValueError('PART_A output directory required')
    rows = _verify_part_a_predecessor(plan_bytes, staged)
    n2_full_outcomes = n2_full_outcomes_from_payload(rows['payload'])

    def prefix_to_custody(raw):
        write_part_a_artifact(output_dir, PART_A_INITIAL_ARTIFACT, raw)

    compute = run_part_a_compute(
        context.contract,
        admitted.source,
        budget,
        n2_full_outcomes=n2_full_outcomes,
        measurement_override=measurement_override,
        on_initial_prefix=prefix_to_custody,
    )
    write_part_a_artifact(output_dir, PART_A_FINAL_ARTIFACT, compute.final_panel_bytes)
    return PartAWorkerRun(
        compute=compute,
        n2_full_baseline={
            'passes': sum(status == 'PASS' for status in n2_full_outcomes),
            'paths': len(n2_full_outcomes),
        },
    )


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
    parser.add_argument('--checkpoint', choices=['N1', 'N2', 'PART_A'], default='N1')
    args = parser.parse_args()
    # S5 (W7): the PART_A checkpoint writes its two S5-D1 artifacts and the
    # result frame to the guardian-owned output mount; it refuses without it.
    if args.checkpoint == 'PART_A' and args.output is None:
        parser.error('--checkpoint PART_A requires --output')
    release = read_regular(
        Path(args.input), 'installation/release.json', limit=BOOTSTRAP_BYTE_LIMIT
    )
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
        document = parse_canonical_json(
            read_regular(Path(args.input), args.campaign_limits, limit=BOOTSTRAP_BYTE_LIMIT),
            label='campaign work limits',
        )
        limits = document['limits']
    frame = run_worker(
        Path(args.input),
        execution_id=args.execution_id,
        campaign_limits=limits,
        checkpoint=args.checkpoint,
        output_dir=Path(args.output) if args.output is not None else None,
    )
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

        self._remaining_wall_seconds = self.limits['wall_ns'] / 1e9
        self._process = time.process_time_ns
        self._monotonic = time.monotonic_ns
        self._start_cpu = self._process()
        self._start_wall = self._monotonic()

    def remaining_wall_seconds(self):
        """The compute stack's budgetSeconds probe; the measured remainder."""
        return self._remaining_wall_seconds

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
        self._remaining_wall_seconds = max(0.0, (self.limits['wall_ns'] - wall) / 1e9)
        return {
            'worker_compute_wall_ns': wall,
            'worker_cpu_ns': cpu,
            'worker_peak_memory_bytes': peak,
            'remaining_wall_seconds': self._remaining_wall_seconds,
        }
