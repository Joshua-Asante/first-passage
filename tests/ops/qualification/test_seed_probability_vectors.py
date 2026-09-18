"""Independent exact vectors; mechanics consistency only, never execution authority.

Seed constants were transcribed from SHA-256 of the literal ASCII preimages in
seed_consumer_vectors.json, without importing domain_seed or seed_input. Binomial
cutoffs below follow the integer coefficients (1,4,6,4,1)/16 at n=4,p=1/2.
"""
import json
from decimal import Decimal
from pathlib import Path
from random import Random

import pytest

from c1_rail.qualification.regime import domain_seed
from c1_rail.qualification.seed_identity import seed_input
from test_orchestration import contract

VECTORS = json.loads((Path(__file__).parent / 'execution/fixtures/seed_consumer_vectors.json').read_bytes())
FIELDS = ('root', 'stage', 'population', 'panel_index', 'path_index', 'purpose', 'synthetic')


def expected(**address):
    return next(row['seed'] for row in VECTORS if all(row[key] == value for key, value in address.items()))


@pytest.mark.parametrize('vector', VECTORS, ids=[
    f"{v['root']}-{v['synthetic']}-{v['stage']}-{v['population']}-{v['panel_index']}-{v['purpose']}-{v['path_index']}"
    for v in VECTORS])
def test_exact_seed_and_retained_identity_vector(vector):
    address = {key: vector[key] for key in FIELDS}
    assert domain_seed(**address) == vector['seed']
    if vector['root'] == 'test':
        value = seed_input(contract(), **{key: value for key, value in address.items() if key != 'root'})
        row = json.loads(value.canonical_bytes)
        assert row['seed'] == vector['seed']
        assert row['source_session_ids_sha256'] == {
            'FULL': '0473ef2dc0d324ab659d3580c1134e9d812035905c4781fdd6d529b0c6860e13',
            'H1': '0eb5b8d6f81bc677da8a08567cc4fa9a06a57e9ec8da85ed73a7f62727996002',
            'H2': 'a8950f05d3443e7921e7ec6fbe06c8febe40966a5db58b15f767a995d561290b',
        }[vector['population']]


@pytest.mark.parametrize('synthetic', [False, True])
@pytest.mark.parametrize('stage', ['n1', 'n2', 'n3'])
def test_runner_consumes_exact_probe_and_population_seeds(stage, synthetic):
    from c1_rail.qualification.runner import SyntheticStageRequest, _run_stage
    from test_runner import STATE, result
    calls = []
    request = SyntheticStageRequest(stage, (('FULL', 1), ('H1', 1), ('H2', 1)), 2, 'test', 100.)
    _run_stage(request, lambda **kw: (calls.append(kw) or result([0, 0])),
               initial_state=STATE, synthetic=synthetic, timer=lambda: 0.)
    actual = [row['seed'] for row in calls]
    assert actual == [
        expected(root='test', synthetic=synthetic, stage=name, population=pop,
                 panel_index=None, path_index=0, purpose='path')
        for name, pop in [('probe', 'FULL'), (stage, 'FULL'), (stage, 'H1'), (stage, 'H2')]]

    if stage in ('n1', 'n2'):
        from c1_rail.qualification.orchestration import _stage_seeds
        frozen = contract()
        for spec in frozen.stage_specs.values():
            spec.population_counts = {name: (1,) for name in spec.population_counts}
        assert [json.loads(item.canonical_bytes)['seed'] for item in
                _stage_seeds(frozen, stage, synthetic)] == actual[1:]


@pytest.mark.parametrize('synthetic', [False, True])
def test_part_a_consumes_exact_pilot_outer_inner_and_expansion_seeds(monkeypatch, synthetic):
    from c1_rail.qualification import part_a
    from test_part_a import request, run
    observed = []
    def record(seed):
        observed.append(seed)
        return Random(seed)
    monkeypatch.setattr(part_a, 'Random', record)
    output = run(request(root_rng_namespace='test'), internal_domain=synthetic)
    assert output.expanded and len(output.panels) == 4
    addresses = [('probe', 0, 'probe', index) for index in (0, 1)]
    addresses += [('n2', panel, purpose, index) for panel in range(4)
                  for purpose, index in [('outer', 0), ('path', 0), ('path', 1)]]
    assert observed == [expected(root='test', synthetic=synthetic, stage=stage,
        population='FULL', panel_index=panel, purpose=purpose, path_index=index)
        for stage, panel, purpose, index in addresses]
    from c1_rail.qualification.orchestration import _part_a_seeds
    plans = _part_a_seeds(contract(), synthetic)
    assert [json.loads(plan.canonical_bytes)['seed'] for plan in plans] == observed[2:]


def test_representative_benchmark_consumes_exact_outer_and_inner_seeds(monkeypatch):
    from c1_rail.qualification import benchmark_part_a
    observed = []
    def record(seed):
        observed.append(seed)
        return Random(seed)
    monkeypatch.setattr(benchmark_part_a, 'Random', record)
    benchmark_part_a.benchmark_part_a(horizon_sessions=5, seed=7)
    assert observed == [expected(root='representative-part-a-benchmark:7', purpose=purpose)
                        for purpose in ('outer', 'path')]


@pytest.mark.parametrize('stage', ['n2', 'n3'])
@pytest.mark.parametrize('failures,fast,status', [(1, 3, 'PASS'), (2, 2, 'FAILURE'), (1, 2, 'FAILURE')])
def test_exact_binomial_cutoffs_reach_stage_consumers(stage, failures, fast, status):
    from c1_rail.qualification.adjudication import DecisionRules, adjudicate_stage
    from test_adjudication import stage as run
    rules = DecisionRules(Decimal('.5'), Decimal('.3125'), Decimal('.5'), 200)
    decision = adjudicate_stage(run(stage, 4, failures, fast), rules)
    assert decision.cutoffs == (('FULL', 1), ('H1', 1), ('H2', 1), ('SPEED', 3))
    assert decision.status == status


@pytest.mark.parametrize('ceiling,cutoff,status', [('.25', 1, 'CONTINUE'), ('.249999999999999999', 0, 'FAILURE')])
def test_exact_screen_cutoff_reaches_stage_consumer(ceiling, cutoff, status):
    from c1_rail.qualification.adjudication import DecisionRules, adjudicate_stage
    from test_adjudication import stage
    decision = adjudicate_stage(stage('n1', 4, 1, 3),
        DecisionRules(Decimal(ceiling), Decimal('.05'), Decimal('.5'), 200))
    assert decision.cutoffs == (('FULL', cutoff), ('H1', cutoff), ('H2', cutoff))
    assert decision.status == status
