"""Closed worker output serialization and fresh internal outcome reconstruction."""

from dataclasses import dataclass
import json

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from ..model import PathOutcome
from ..legality import parse_source_admission, build_legality_record, geometry_role
from .protocol import fields, sha256


@dataclass(frozen=True)
class CapturedN1:
    populations: tuple
    document: dict


@dataclass(frozen=True)
class CapturedPartA:
    """One captured PART_A result: panel objects plus the document (W5)."""

    panels: tuple
    document: dict


@dataclass(frozen=True)
class CapturedPartAPanel:
    """One captured panel row; ``part_a_panel_bytes`` re-encodes it exactly."""

    index: int
    source_session_ids: tuple
    outcomes: tuple


def outcome_record(row):
    if type(row) is not PathOutcome:
        raise TypeError('exact path outcome required')
    return dict(
        status=row.status,
        sessions_to_pass=row.sessions_to_pass,
        failure_reason=row.failure_reason,
        diagnostics=[list(pair) for pair in row.diagnostics],
    )


def _plan_stages(plan):
    """The per-population statistics stage: N1 plans pin N1; the joint N2 plan
    carries each population's statistics_stage (FULL->N2, H1/H2->PART_B)."""
    depths = plan.get('depths') if type(plan) is dict else None
    if type(depths) is not list:
        raise ValueError('plan depths required')
    stages = []
    for row in depths:
        if type(row) is not dict or row.get('population') not in ('FULL', 'H1', 'H2'):
            raise ValueError('plan population differs')
        stage = row.get('statistics_stage') if plan.get('checkpoint') == 'N2' else 'N1'
        if stage not in ('N1', 'N2', 'PART_B'):
            raise ValueError('plan statistics stage differs')
        stages.append(stage)
    return tuple(stages)


def path_inventory(plan, populations):
    stages = _plan_stages(plan)
    seeds = iter(plan['seed_inputs'])
    records = []
    for population, stage in zip(populations, stages):
        for index, row in enumerate(population['outcomes']):
            seed = next(seeds, None)
            if seed is None or (seed['population'], seed['path_index']) != (
                population['population'],
                index,
            ):
                raise ValueError('worker depth/order differs from plan')
            records.append(
                dict(
                    stage=stage,
                    population=population['population'],
                    path_index=index,
                    panel_id=None,
                    seed_input_sha256=sha256(encoded(seed)),
                    outcome_sha256=sha256(encoded(row)),
                )
            )
    if next(seeds, None) is not None:
        raise ValueError('worker depth differs from plan')
    return dict(
        schema='qualification_path_inventory/v1',
        trust_domain_sha256=plan['trust_domain_sha256'],
        records=records,
    )


def _part_a_plan_shape(plan):
    """The PART_A plan's frozen panel parameters (W5; never decision inputs)."""
    part = plan.get('part_a') if type(plan) is dict else None
    if type(part) is not dict:
        raise ValueError('plan part a vector required')
    parameters = part.get('parameters')
    depth = parameters.get('paths_per_population_per_panel') if type(parameters) is dict else None
    initial = parameters.get('initial_panels') if type(parameters) is dict else None
    if (
        type(depth) is not int
        or depth <= 0
        or type(initial) is not int
        or initial <= 0
        or type(part.get('potential_panels')) is not list
        or len(part['potential_panels']) < initial
        or any(type(row) is not dict for row in part['potential_panels'])
    ):
        raise ValueError('plan part a parameters differ')
    return initial, depth, part['potential_panels']


def _part_a_pilot(plan):
    """W5a: the PART_A probe identity -- the plan's probe seed-input digests.

    Shared by the encoder (which writes it beside the panels) and the parser
    (which refuses a missing or altered pilot against the same plan bytes).
    """
    seeds = plan.get('seed_inputs') if type(plan) is dict else None
    if type(seeds) is not list or not seeds:
        raise ValueError('plan part a probe seed inputs required')
    return dict(seed_input_sha256s=[sha256(encoded(seed)) for seed in seeds])


def _part_a_exact_percentiles(panels, *, spec, initial_panels):
    """The frozen INVERSE_ECDF_LEFT rank over exact Decimal panel pass rates.

    Exactly ``result_adjudication.adjudicate_panel_inventory``'s arithmetic
    (P2): the worker's reported ``initial_p5``/``final_p5`` floats must equal
    ``float`` of these exact values; a band is never admitted.
    """
    from decimal import Decimal, ROUND_CEILING

    if spec.percentile_method != 'INVERSE_ECDF_LEFT':
        raise ValueError('unsupported frozen percentile method')
    rates = [
        Decimal(sum(outcome.status == 'PASS' for outcome in panel.outcomes)) / len(panel.outcomes)
        for panel in panels
    ]

    def percentile(values):
        rank = int((spec.percentile * len(values)).to_integral_value(rounding=ROUND_CEILING))
        return sorted(values)[max(0, rank - 1)]

    return percentile(rates[:initial_panels]), percentile(rates)


def _part_a_panel_row(panel):
    """The canonical panel row shared by the artifact bytes and the document."""
    if type(panel) is dict:
        return fields(panel, {'index', 'source_session_ids', 'outcomes'})
    return dict(
        index=panel.index,
        source_session_ids=list(panel.source_session_ids),
        outcomes=[outcome_record(outcome) for outcome in panel.outcomes],
    )


def part_a_path_inventory(plan, panels):
    """The PART_A panel-major source-occurrence inventory, re-derived (W5a).

    ``panels`` are the computation's panel objects when encoding and captured
    panel rows when parsing; each record binds one path outcome to its panel
    index, its panel's source-occurrence digest and the plan's seed input at
    that exact panel/path address. ``panel_id`` is the digest of the plan's
    outer seed for that panel -- the hex-string identity the installed
    adjudicator keys PART_A panels by, unique by construction -- and the
    records carry population ``REGIME`` with the panel index beside it.
    """
    _, depth, potential = _part_a_plan_shape(plan)
    records = []
    for panel in panels:
        row = _part_a_panel_row(panel)
        index = row['index']
        if type(index) is not int or not 0 <= index < len(potential):
            raise ValueError('part a panel index differs from the plan')
        outer = potential[index].get('outer_seed')
        seeds = potential[index].get('path_seeds')
        if type(outer) is not dict or type(seeds) is not list or len(seeds) != depth:
            raise ValueError('part a panel seed vector differs from the plan')
        outcomes = row['outcomes']
        if type(outcomes) is not list or len(outcomes) != depth:
            raise ValueError('part a panel outcome depth differs from the plan')
        occurrence = sha256(encoded(list(row['source_session_ids'])))
        identity = sha256(encoded(outer))
        for path, outcome in enumerate(outcomes):
            records.append(
                dict(
                    stage='PART_A',
                    population='REGIME',
                    panel_id=identity,
                    panel_index=index,
                    path_index=path,
                    source_occurrence_sha256=occurrence,
                    seed_input_sha256=sha256(encoded(seeds[path])),
                    outcome_sha256=sha256(encoded(outcome)),
                )
            )
    return dict(
        schema='qualification_path_inventory/v1',
        trust_domain_sha256=plan['trust_domain_sha256'],
        records=records,
    )


def encode_worker_result(context, execution_id, plan_bytes, run, observations, *, admitted):
    admitted.source.verify_for(context.contract)
    plan = json.loads(plan_bytes)
    if type(plan) is dict and plan.get('checkpoint') == 'PART_A':
        return _encode_part_a_worker_result(
            context, execution_id, plan_bytes, plan, run, observations, admitted=admitted
        )
    stages = _plan_stages(plan)
    if run.stage not in ('n1', 'n2') or run.synthetic is not context.domain.permits_synthetic:
        raise ValueError('worker computation domain differs')
    if (plan.get('checkpoint') == 'N2') != (run.stage == 'n2'):
        raise ValueError('worker stage differs from plan checkpoint')
    populations = [
        dict(
            population=name,
            stage=stage if plan.get('checkpoint') == 'N2' else None,
            outcomes=[outcome_record(row) for row in rows],
        )
        for (name, rows), stage in zip(run.populations, stages)
    ]
    if plan.get('checkpoint') != 'N2':
        for population in populations:
            population.pop('stage')
    return encoded(
        dict(
            schema='qualification_worker_result/v1',
            execution_id=execution_id,
            plan_sha256=sha256(plan_bytes),
            source_admission=json.loads(admitted.source_admission_bytes),
            legality=json.loads(admitted.legality_bytes),
            populations=populations,
            runtime_load_manifest=[
                dict(role=role, sha256=digest)
                for role, _, digest in sorted(admitted.source.prepared.load_trace)
            ],
            path_inventory=path_inventory(plan, populations),
            observations=observations,
        )
    )


def _encode_part_a_worker_result(
    context, execution_id, plan_bytes, plan, run, observations, *, admitted
):
    """W5a: the PART_A worker-result document; ``populations`` becomes ``part_a``.

    ``run`` is the SR-3 body's ``PartAWorkerRun``: the computation beside the
    N2 FULL baseline the body itself derived from the staged capture (S5-D2).
    The pilot identity needs no transport -- it derives from the same plan
    bytes the body verified against its own independent derivation.
    """
    from .worker import PartAWorkerRun

    if (
        type(run) is not PartAWorkerRun
        or run.compute.result.synthetic is not context.domain.permits_synthetic
    ):
        raise ValueError('worker computation domain differs')
    compute = run.compute
    initial = _part_a_plan_shape(plan)[0]
    panels = [_part_a_panel_row(panel) for panel in compute.result.panels]
    if (
        compute.initial_panels != initial
        or compute.final_panels != len(panels)
        or len(panels) < initial
        or compute.expansion_required != (compute.final_panels > compute.initial_panels)
    ):
        raise ValueError('worker part a panel counts differ from the plan')
    return encoded(
        dict(
            schema='qualification_worker_result/v1',
            execution_id=execution_id,
            plan_sha256=sha256(plan_bytes),
            source_admission=json.loads(admitted.source_admission_bytes),
            legality=json.loads(admitted.legality_bytes),
            part_a=dict(
                initial_panels=compute.initial_panels,
                final_panels=compute.final_panels,
                expansion_required=compute.expansion_required,
                initial_prefix_sha256=sha256(compute.initial_panel_bytes),
                final_sha256=sha256(compute.final_panel_bytes),
                initial_p5=compute.result.initial_p5,
                final_p5=compute.result.final_p5,
                probe_seconds=compute.result.probe_seconds,
                predicted_seconds=compute.result.predicted_seconds,
                pilot=_part_a_pilot(plan),
                n2_full_baseline=run.n2_full_baseline,
                panels=panels,
            ),
            runtime_load_manifest=[
                dict(role=role, sha256=digest)
                for role, _, digest in sorted(admitted.source.prepared.load_trace)
            ],
            path_inventory=part_a_path_inventory(plan, compute.result.panels),
            observations=observations,
        )
    )


def parse_worker_result(raw, *, context, execution_id, plan_bytes, campaign_limits=None):
    """Validate one captured worker result.

    A PART_A plan takes the ``part_a`` branch (W5): the same common fields
    with ``populations`` replaced by the panel document. ``campaign_limits``
    (FULL_E1 only, D3) supplies the work's remaining phase
    limits; the observations are then compared against those limits instead of
    the contract maxima, exactly as the phase-limited guard enforced them. The
    N1_ONLY path keeps the contract maxima (``None`` here).
    """
    if type(raw) is not bytes or len(raw) > context.profile.output_byte_limit:
        raise ValueError('bounded captured result required')
    plan = json.loads(plan_bytes)
    if type(plan) is dict and plan.get('checkpoint') == 'PART_A':
        return _parse_part_a_worker_result(
            raw,
            context=context,
            execution_id=execution_id,
            plan_bytes=plan_bytes,
            plan=plan,
            campaign_limits=campaign_limits,
        )
    doc = fields(
        parse_canonical_json(raw, label='worker result'),
        {
            'schema',
            'execution_id',
            'plan_sha256',
            'source_admission',
            'legality',
            'runtime_load_manifest',
            'populations',
            'path_inventory',
            'observations',
        },
    )
    if (
        doc['schema'] != 'qualification_worker_result/v1'
        or doc['execution_id'] != execution_id
        or doc['plan_sha256'] != sha256(plan_bytes)
    ):
        raise ValueError('worker admission/execution/plan differs')
    _verify_worker_bindings(doc, context=context)
    joint = plan.get('checkpoint') == 'N2'
    stages = _plan_stages(plan)
    if type(doc['populations']) is not list or len(doc['populations']) != len(stages):
        raise ValueError('complete ordered worker populations required')
    populations = []
    for population, expected, stage in zip(doc['populations'], plan['depths'], stages):
        keys = {'population', 'outcomes'} | ({'stage'} if joint else set())
        fields(population, keys)
        rows = population['outcomes']
        if (
            population['population'] != expected['population']
            or (joint and population.get('stage') != stage)
            or type(rows) is not list
            or len(rows) != expected['depth']
        ):
            raise ValueError('worker population order/depth differs')
        outcomes = [_captured_outcome(row, context=context) for row in rows]
        populations.append((population['population'], tuple(outcomes)))
    if encoded(doc['path_inventory']) != encoded(path_inventory(plan, doc['populations'])):
        raise ValueError('captured path inventory differs')
    _verify_worker_observations(doc, context=context, campaign_limits=campaign_limits)
    return CapturedN1(tuple(populations), doc)


def _captured_outcome(row, *, context):
    """One closed outcome row and its frozen-horizon bound (N1/N2 and PART_A)."""
    fields(row, {'status', 'sessions_to_pass', 'failure_reason', 'diagnostics'})
    if type(row['status']) is not str or (
        row['failure_reason'] is not None and type(row['failure_reason']) is not str
    ):
        raise ValueError('closed outcome status/reason required')
    if type(row['diagnostics']) is not list or any(
        type(pair) is not list
        or len(pair) != 2
        or any(type(value) is not str for value in pair)
        for pair in row['diagnostics']
    ):
        raise ValueError('outcome string diagnostic pairs required')
    outcome = PathOutcome(
        row['status'],
        row['sessions_to_pass'],
        row['failure_reason'],
        tuple(tuple(pair) for pair in row['diagnostics']),
    )
    if (
        outcome.status == 'PASS'
        and outcome.sessions_to_pass > context.contract.replay.horizon_sessions
    ):
        raise ValueError('outcome beyond frozen horizon')
    return outcome


def _verify_worker_bindings(doc, *, context):
    """The admission and legality bindings every captured worker result carries."""
    admission_bytes = encoded(doc['source_admission'])
    admission = parse_source_admission(
        admission_bytes,
        contract_sha256=context.contract.contract_sha256,
        domain_sha256=context.domain.sha256,
        policy=context.policy,
    )
    expected_roles = [
        dict(role=row.role, sha256=row.sha256)
        for row in sorted(context.contract.artifacts, key=lambda row: row.role)
    ]
    if (
        admission['retained_roles'] != expected_roles
        or admission['effective_settings_sha256'] != context.contract.effective_settings_sha256
        or admission['population_sha256']
        != {
            pop: sha256(encoded(list(context.contract.populations[pop])))
            for pop in ('FULL', 'H1', 'H2')
        }
        or doc['runtime_load_manifest'] != expected_roles
    ):
        raise ValueError('worker source admission bindings differ')
    geometry = geometry_role(context.domain.runtime_code_roles)
    expected_legality = build_legality_record(
        contract_sha256=context.contract.contract_sha256,
        domain_sha256=context.domain.sha256,
        policy=context.policy,
        geometry_bytes=context.retained_bytes[geometry],
        expected_geometry_sha256=next(
            row.sha256 for row in context.contract.artifacts if row.role == geometry
        ),
        source_admission_bytes=admission_bytes,
    )
    if encoded(doc['legality']) != expected_legality:
        raise ValueError('worker legality differs')


def _verify_worker_observations(doc, *, context, campaign_limits):
    """The retained budget observations against the binding limits (D3)."""
    observations = fields(
        doc['observations'], {'worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'}
    )
    if any(type(value) is not int or value < 0 for value in observations.values()):
        raise ValueError('worker budget observations must be nonnegative integers')
    budget = context.contract.replay.budget
    if campaign_limits is None:
        budget_bound = (
            budget.maximum_wall_seconds * 1000000000,
            budget.maximum_cpu_seconds * 1000000000,
            budget.maximum_memory_bytes,
        )
    else:
        from .protocol import fields as _closed

        limits = _closed(campaign_limits, {'cpu_ns', 'wall_ns', 'memory_bytes'})
        budget_bound = (limits['wall_ns'], limits['cpu_ns'], limits['memory_bytes'])
    if (
        observations['worker_compute_wall_ns'] >= budget_bound[0]
        or observations['worker_cpu_ns'] > budget_bound[1]
        or observations['worker_peak_memory_bytes'] > budget_bound[2]
    ):
        raise ValueError('worker exceeded frozen budget')


def _parse_part_a_worker_result(
    raw, *, context, execution_id, plan_bytes, plan, campaign_limits
):
    """W5: the PART_A worker-result parse: closed keys, panel order, digests.

    The panel rows must run in index order from zero, each at the plan's frozen
    panel depth; the panel counts and the expansion fact must agree with each
    other and with the plan's initial panel count; the two artifact digests
    must be the digests of exactly the re-encoded initial prefix and the full
    panel vector; and the panel-major occurrence inventory must re-derive from
    the plan. W5a adds the probe identity (``pilot``: exactly the plan's probe
    seed-input digests, so a missing or altered pilot refuses) and the N2 FULL
    baseline the worker derived from the staged capture (a closed
    ``{'passes', 'paths'}`` pair; only its range is checkable here -- the value
    itself is G5's independent derivation, S5-D2). The G5 comparisons
    (tolerance, floor, FULL sanity) are ticket 2d and are not part of this
    document.
    """
    from math import isfinite

    from .compute import part_a_panel_bytes
    from .protocol import digest

    doc = fields(
        parse_canonical_json(raw, label='worker result'),
        {
            'schema',
            'execution_id',
            'plan_sha256',
            'source_admission',
            'legality',
            'runtime_load_manifest',
            'part_a',
            'path_inventory',
            'observations',
        },
    )
    if (
        doc['schema'] != 'qualification_worker_result/v1'
        or doc['execution_id'] != execution_id
        or doc['plan_sha256'] != sha256(plan_bytes)
    ):
        raise ValueError('worker admission/execution/plan differs')
    _verify_worker_bindings(doc, context=context)
    initial, depth, _ = _part_a_plan_shape(plan)
    # P1(b): every source occurrence must name an admitted session -- the
    # contract's frozen FULL population, the set the retained source covers.
    admitted = frozenset(context.contract.populations['FULL'])
    record = fields(
        doc['part_a'],
        {
            'initial_panels',
            'final_panels',
            'expansion_required',
            'initial_prefix_sha256',
            'final_sha256',
            'initial_p5',
            'final_p5',
            'probe_seconds',
            'predicted_seconds',
            'pilot',
            'n2_full_baseline',
            'panels',
        },
    )
    rows = record['panels']
    if type(rows) is not list or not rows:
        raise ValueError('complete ordered part a panels required')
    panels = []
    for expected_index, row in enumerate(rows):
        fields(row, {'index', 'source_session_ids', 'outcomes'})
        sessions = row['source_session_ids']
        if (
            type(row['index']) is not int
            or row['index'] != expected_index
            or type(sessions) is not list
            or not sessions
            or any(type(session) is not str or not session for session in sessions)
        ):
            raise ValueError('part a panel order or source occurrences differ')
        if any(session not in admitted for session in sessions):
            raise ValueError('part a source occurrence outside the admitted FULL population')
        outcomes = row['outcomes']
        if type(outcomes) is not list or len(outcomes) != depth:
            raise ValueError('part a panel depth differs from the plan')
        panels.append(
            CapturedPartAPanel(
                expected_index,
                tuple(sessions),
                tuple(_captured_outcome(outcome, context=context) for outcome in outcomes),
            )
        )
    initial_panels = record['initial_panels']
    final_panels = record['final_panels']
    if (
        type(initial_panels) is not int
        or type(final_panels) is not int
        or initial_panels != initial
        or final_panels != len(panels)
        or not 0 < initial_panels <= final_panels
        or type(record['expansion_required']) is not bool
        or record['expansion_required'] != (final_panels > initial_panels)
    ):
        raise ValueError('part a panel counts or expansion fact differ')
    for name in ('initial_p5', 'final_p5', 'probe_seconds', 'predicted_seconds'):
        if type(record[name]) is not float or not isfinite(record[name]):
            raise ValueError('finite part a measurement floats required')
    initial_p5, final_p5 = _part_a_exact_percentiles(
        panels, spec=context.contract.replay.part_a, initial_panels=initial_panels
    )
    if record['initial_p5'] != float(initial_p5) or record['final_p5'] != float(final_p5):
        raise ValueError('part a reported statistic differs')
    pilot = fields(record['pilot'], {'seed_input_sha256s'})
    seed_digests = pilot['seed_input_sha256s']
    if type(seed_digests) is not list or not seed_digests:
        raise ValueError('part a pilot seed digests required')
    for value in seed_digests:
        digest(value)
    if encoded(pilot) != encoded(_part_a_pilot(plan)):
        raise ValueError('part a pilot identity differs from the plan')
    baseline = fields(record['n2_full_baseline'], {'passes', 'paths'})
    if (
        type(baseline['passes']) is not int
        or type(baseline['paths']) is not int
        or baseline['paths'] <= 0
        or not 0 <= baseline['passes'] <= baseline['paths']
    ):
        raise ValueError('part a n2 full baseline out of range')
    digest(record['initial_prefix_sha256'])
    digest(record['final_sha256'])
    if sha256(part_a_panel_bytes(panels[:initial_panels])) != record['initial_prefix_sha256']:
        raise ValueError('part a initial prefix digest differs')
    if sha256(part_a_panel_bytes(panels)) != record['final_sha256']:
        raise ValueError('part a final digest differs')
    if encoded(doc['path_inventory']) != encoded(part_a_path_inventory(plan, panels)):
        raise ValueError('captured path inventory differs')
    _verify_worker_observations(doc, context=context, campaign_limits=campaign_limits)
    return CapturedPartA(tuple(panels), doc)
