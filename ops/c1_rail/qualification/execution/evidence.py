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


def encode_worker_result(context, execution_id, plan_bytes, run, observations, *, admitted):
    admitted.source.verify_for(context.contract)
    plan = json.loads(plan_bytes)
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


def parse_worker_result(raw, *, context, execution_id, plan_bytes, campaign_limits=None):
    """Validate one captured worker result.

    ``campaign_limits`` (FULL_E1 only, D3) supplies the work's remaining phase
    limits; the observations are then compared against those limits instead of
    the contract maxima, exactly as the phase-limited guard enforced them. The
    N1_ONLY path keeps the contract maxima (``None`` here).
    """
    if type(raw) is not bytes or len(raw) > context.profile.output_byte_limit:
        raise ValueError('bounded captured result required')
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
    plan = json.loads(plan_bytes)
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
        outcomes = []
        for row in rows:
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
            outcomes.append(outcome)
        populations.append((population['population'], tuple(outcomes)))
    if encoded(doc['path_inventory']) != encoded(path_inventory(plan, doc['populations'])):
        raise ValueError('captured path inventory differs')
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
    return CapturedN1(tuple(populations), doc)
