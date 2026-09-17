from decimal import Decimal
from types import SimpleNamespace

import pytest

from c1_rail.qualification.model import PathOutcome
from c1_rail.qualification.result_adjudication import adjudicate_panel_inventory


def dispatcher_runtime(module, extra_modules=None):
    import hashlib
    import c1_rail.qualification.adjudication as adjudication
    import c1_rail.qualification.model as model
    import scripts.certification_power as certification
    from c1_rail.qualification.runtime_inventory import (
        DataBinding, ModuleObservation, RuntimeInventoryReceipt,
    )

    role_modules = {
        'qualification_adjudicator': module,
        'qualification_adjudication_rules': adjudication,
        'qualification_model': model,
        'qualification_certification_power': certification,
    }
    role_modules.update(extra_modules or {})
    retained = {role: __import__('pathlib').Path(value.__file__).read_bytes()
                for role, value in role_modules.items()}
    retained['another_runtime_role'] = b'retained'
    observations = tuple(ModuleObservation(
        role, value.__name__, str(__import__('pathlib').Path(value.__file__).resolve()),
        hashlib.sha256(retained[role]).hexdigest(), retained[role], (), ())
        for role, value in role_modules.items())
    runtime = tuple(sorted((role, hashlib.sha256(raw).hexdigest())
                           for role, raw in retained.items()))
    receipt = RuntimeInventoryReceipt(
        'a' * 64, observations,
        (DataBinding('another_runtime_role', 'retained.bin',
                     hashlib.sha256(retained['another_runtime_role']).hexdigest(),
                     retained['another_runtime_role']),), runtime)
    return retained, receipt


def spec():
    return SimpleNamespace(initial_panels=100, expanded_panels=200,
        paths_per_population_per_panel=20, percentile=Decimal('.05'),
        percentile_method='INVERSE_ECDF_LEFT', expansion_center_p5=Decimal('.95'),
        expansion_tolerance=Decimal('.01'), expansion_rule='INCLUSIVE_ABSOLUTE_DISTANCE',
        sanity_rule='P5_LE_FULL')


def evidence(passes):
    rows=[]
    inventory=[]
    for panel, count in enumerate(passes):
        for path in range(20):
            rows.append(PathOutcome('PASS', 4, None, ()) if path<count else
                        PathOutcome('FAILURE', None, 'synthetic', ()))
            inventory.append(dict(stage='PART_A', population='REGIME',
                                  panel_id=f'panel-{panel}', path_index=path))
    return tuple(rows), {'records': inventory}


def test_initial_close_call_requires_expansion_with_original_prefix():
    rows, inventory=evidence([19]*100)
    with pytest.raises(ValueError, match='expansion'):
        adjudicate_panel_inventory(rows,inventory,spec=spec(),full_pass_rate=Decimal('.97'))
    rows, inventory=evidence([19]*200)
    assert adjudicate_panel_inventory(rows,inventory,spec=spec(),full_pass_rate=Decimal('.97'))=='PASS'


def test_non_close_initial_percentile_forbids_extra_panels():
    rows,inventory=evidence([20]*200)
    with pytest.raises(ValueError,match='expansion'):
        adjudicate_panel_inventory(rows,inventory,spec=spec(),full_pass_rate=Decimal('1'))


def test_fifth_rank_and_full_sanity_use_actual_nested_outcomes():
    rows,inventory=evidence([18]*5+[20]*95)
    assert adjudicate_panel_inventory(rows,inventory,spec=spec(),full_pass_rate=Decimal('1'))=='FAIL'
    rows,inventory=evidence([20]*100)
    assert adjudicate_panel_inventory(rows,inventory,spec=spec(),full_pass_rate=Decimal('.99'))=='FAIL'


def test_panel_identity_cannot_be_reordered_within_block():
    rows,inventory=evidence([20]*100)
    inventory['records'][1]['panel_id']='another-panel'
    with pytest.raises(ValueError,match='panel'):
        adjudicate_panel_inventory(rows,inventory,spec=spec(),full_pass_rate=Decimal('1'))


def test_stage_mapping_allows_certified_failures_and_keeps_part_b_separate():
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    rules=SimpleNamespace(failure_ceiling=Decimal('.05'),alpha=Decimal('.05'),
        speed_target=Decimal('.5'),speed_horizon_sessions=200)
    contract=SimpleNamespace(replay=SimpleNamespace(decision_rules=rules,part_a=spec()))
    passed=PathOutcome('PASS',20,None,())
    failed=PathOutcome('FAILURE',None,'synthetic',())
    rows=(passed,)*933+(failed,)*37
    outcomes={'LEGALITY':{},'N1':{name:(passed,)*200 for name in ('FULL','H1','H2')},
              'N2':{'FULL':rows},'PART_B':{'H1':rows,'H2':(passed,)*932+(failed,)*38}}
    decisions=adjudicate_e1_outcomes(contract,outcomes,{'records':[]})
    assert decisions=={'LEGALITY':'PASS','N1':'PASS','N2':'PASS','PART_B':'FAIL'}


def test_n1_terminal_prefix_needs_no_later_draws():
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    rules=SimpleNamespace(failure_ceiling=Decimal('.05'),alpha=Decimal('.05'),
        speed_target=Decimal('.5'),speed_horizon_sessions=200)
    contract=SimpleNamespace(replay=SimpleNamespace(decision_rules=rules))
    rows=(PathOutcome('UNRESOLVED',None,'horizon_cap',()),)*200
    assert adjudicate_e1_outcomes(contract,{'LEGALITY':{},'N1':{name:rows for name in ('FULL','H1','H2')}},
                                 {'records':[]})=={'LEGALITY':'PASS','N1':'FAIL'}


@pytest.mark.parametrize('ceiling, expected', [
    ('0.0049999999999999999', 'FAIL'), ('0.005', 'PASS'),
])
def test_n1_preserves_exact_signed_decimal_cutoff(ceiling, expected):
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    rules = SimpleNamespace(failure_ceiling=Decimal(ceiling), alpha=Decimal('.05'),
                            speed_target=Decimal('.5'), speed_horizon_sessions=200)
    contract = SimpleNamespace(replay=SimpleNamespace(decision_rules=rules))
    rows = (PathOutcome('PASS', 1, None, ()),) * 199 + (PathOutcome('FAILURE', None, 'fixture', ()),)
    outcomes = {'LEGALITY': {}, 'N1': {name: rows for name in ('FULL', 'H1', 'H2')}}
    assert adjudicate_e1_outcomes(contract, outcomes, {'records': []})['N1'] == expected


@pytest.mark.parametrize('ceiling, expected', [
    ('0.049999999999999999', 'FAIL'), ('0.05', 'PASS'),
])
def test_confirmation_preserves_exact_signed_probabilities(ceiling, expected):
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    rules = SimpleNamespace(failure_ceiling=Decimal(ceiling), alpha=Decimal('.95'),
                            speed_target=Decimal('.5'), speed_horizon_sessions=200)
    contract = SimpleNamespace(replay=SimpleNamespace(decision_rules=rules))
    rows = (PathOutcome('PASS', 1, None, ()),)
    outcomes = {'LEGALITY': {}, 'N1': {name: rows for name in ('FULL', 'H1', 'H2')},
                'N2': {'FULL': rows}, 'PART_B': {'H1': rows, 'H2': rows}}
    decisions = adjudicate_e1_outcomes(contract, outcomes, {'records': []})
    assert decisions['N2'] == decisions['PART_B'] == expected


@pytest.mark.parametrize('when', ['before_freeze', 'after_freeze'])
def test_dispatcher_rejects_replaced_runner_evaluator(monkeypatch, when):
    import c1_rail.qualification.result_adjudication as module
    import c1_rail.qualification.runner as runner
    import hashlib
    retained, receipt = dispatcher_runtime(module, {'path_runner': runner})
    sources = {role: hashlib.sha256(raw).hexdigest() for role, raw in retained.items()}
    contract = SimpleNamespace(runtime_load_sha256=sources,
        adjudicator_sha256=module._closure_identity(sources), contract_sha256='a' * 64)
    dispatcher = None
    if when == 'after_freeze':
        dispatcher = module.frozen_adjudicator(contract, retained_source_bytes=retained, runtime_inventory=receipt)
    monkeypatch.setattr(runner, 'evaluate_replay', lambda *args, **kwargs: PathOutcome('PASS', 1, None, ()))
    with pytest.raises(ValueError, match='runtime dependency|runtime inventory'):
        if dispatcher:
            dispatcher.verify_for(contract)
        else:
            module.frozen_adjudicator(contract, retained_source_bytes=retained, runtime_inventory=receipt)


def test_dispatcher_binds_complete_retained_runtime_and_own_source():
    import hashlib
    import json
    from pathlib import Path
    import c1_rail.qualification.result_adjudication as module
    retained, runtime_inventory = dispatcher_runtime(module)
    sources={name:hashlib.sha256(raw).hexdigest() for name,raw in retained.items()}
    subject={'schema':'qualification-adjudicator-closure/v1','sources':sources}
    identity=hashlib.sha256(json.dumps(subject,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    contract=SimpleNamespace(runtime_load_sha256=sources,adjudicator_sha256=identity,contract_sha256='a'*64)
    with pytest.raises(ValueError, match='runtime inventory'):
        module.frozen_adjudicator(
            contract, retained_source_bytes=retained, runtime_inventory=None)
    dispatcher=module.frozen_adjudicator(
        contract,retained_source_bytes=retained,runtime_inventory=runtime_inventory)
    assert type(dispatcher) is module.FrozenAdjudicator
    assert dispatcher.identity_sha256==identity
    dispatcher.verify_for(contract)
    with pytest.raises(ValueError,match='source'):
        module.frozen_adjudicator(contract,retained_source_bytes={**retained,'another_runtime_role':b'changed'},
                                  runtime_inventory=runtime_inventory)
    with pytest.raises(ValueError,match='inventory'):
        module.frozen_adjudicator(contract,retained_source_bytes={'qualification_adjudicator':retained['qualification_adjudicator']},
                                  runtime_inventory=runtime_inventory)
    with pytest.raises(ValueError,match='contract'):
        dispatcher.verify_for(SimpleNamespace(**{**vars(contract),'contract_sha256':'b'*64}))


def test_dispatcher_refuses_entrypoint_replacement_after_freeze(monkeypatch):
    import hashlib
    import json
    from pathlib import Path
    import c1_rail.qualification.result_adjudication as module

    retained, runtime_inventory = dispatcher_runtime(module)
    sources = {name: hashlib.sha256(raw).hexdigest()
               for name, raw in retained.items()}
    subject = {'schema': 'qualification-adjudicator-closure/v1',
               'sources': sources}
    identity = hashlib.sha256(json.dumps(
        subject, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    contract = SimpleNamespace(runtime_load_sha256=sources,
        adjudicator_sha256=identity, contract_sha256='a' * 64)
    dispatcher = module.frozen_adjudicator(
        contract, retained_source_bytes=retained,
        runtime_inventory=runtime_inventory)

    monkeypatch.setattr(module, 'adjudicate_e1_outcomes',
                        lambda contract, outcomes, inventory: {'LEGALITY': 'PASS'})
    with pytest.raises(ValueError, match='entrypoint'):
        dispatcher.verify_for(contract)
    with pytest.raises(ValueError, match='entrypoint'):
        dispatcher({}, {})


def test_dispatcher_refuses_dependency_already_drifted_before_freeze(monkeypatch):
    import hashlib
    import json
    import c1_rail.qualification.result_adjudication as module

    retained, runtime_inventory = dispatcher_runtime(module)
    sources = {name: hashlib.sha256(raw).hexdigest()
               for name, raw in retained.items()}
    identity = hashlib.sha256(json.dumps({
        'schema': 'qualification-adjudicator-closure/v1', 'sources': sources,
    }, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    contract = SimpleNamespace(runtime_load_sha256=sources,
        adjudicator_sha256=identity, contract_sha256='a' * 64)
    monkeypatch.setattr(module, 'adjudicate_stage', lambda run, rules: None)

    with pytest.raises(ValueError, match='runtime inventory|dependency'):
        module.frozen_adjudicator(
            contract, retained_source_bytes=retained,
            runtime_inventory=runtime_inventory)


@pytest.mark.parametrize('when', ['before_freeze', 'after_freeze'])
@pytest.mark.parametrize('changed', [
    'entrypoint_code', 'binomial_helper', 'rules_constructor', 'decision_constructor',
])
def test_dispatcher_rejects_outcome_changing_executable_drift(monkeypatch, when, changed):
    """Retained bytes must bind live code, including transitive class methods.

    These fake contract/receipt objects exercise only the dispatcher boundary;
    they do not claim signed G1 or G5 authority.
    """
    import hashlib
    import json
    import c1_rail.qualification.adjudication as adjudication
    import c1_rail.qualification.result_adjudication as module
    import scripts.certification_power as certification

    retained, runtime_inventory = dispatcher_runtime(module)
    sources = {name: hashlib.sha256(raw).hexdigest()
               for name, raw in retained.items()}
    identity = hashlib.sha256(json.dumps({
        'schema': 'qualification-adjudicator-closure/v1', 'sources': sources,
    }, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    rules = SimpleNamespace(failure_ceiling=Decimal('.05'), alpha=Decimal('.05'),
                            speed_target=Decimal('.5'), speed_horizon_sessions=200)
    contract = SimpleNamespace(runtime_load_sha256=sources,
        adjudicator_sha256=identity, contract_sha256='a' * 64,
        replay=SimpleNamespace(decision_rules=rules))
    passed = PathOutcome('PASS', 20, None, ())
    failed = PathOutcome('FAILURE', None, 'synthetic', ())
    # Eleven failures exceed N1's ten-failure ceiling at depth 200.
    rows = (passed,) * 189 + (failed,) * 11
    outcomes = {'LEGALITY': {}, 'N1': {name: rows for name in ('FULL', 'H1', 'H2')}}
    affected_stage = 'N1'
    if changed == 'binomial_helper':
        outcomes['N1'] = {name: (passed,) * 200 for name in ('FULL', 'H1', 'H2')}
        outcomes['N2'] = {'FULL': (passed,) * 970}
        outcomes['PART_B'] = {name: (failed,) * 970 for name in ('H1', 'H2')}
        affected_stage = 'PART_B'
    inventory = {'records': []}
    assert module.adjudicate_e1_outcomes(contract, outcomes, inventory)[affected_stage] == 'FAIL'

    def freeze():
        return module.frozen_adjudicator(
            contract, retained_source_bytes=retained, runtime_inventory=runtime_inventory)

    dispatcher = freeze() if when == 'after_freeze' else None
    if dispatcher is not None:
        dispatcher.verify_for(contract)
        assert dispatcher(outcomes, inventory)[affected_stage] == 'FAIL'

    if changed == 'entrypoint_code':
        # Preserve the canonical function object, globals, owner and disk bytes.
        replacement = lambda contract, outcomes, inventory: {'LEGALITY': 'PASS', 'N1': 'PASS'}
        monkeypatch.setattr(module.adjudicate_e1_outcomes, '__code__', replacement.__code__)
    elif changed == 'binomial_helper':
        replacement = lambda n, ceiling=.05, alpha=.05: n
        monkeypatch.setattr(certification.max_certifying_busts, '__code__', replacement.__code__)
    elif changed == 'rules_constructor':
        def altered_rules(self, failure_ceiling, alpha, speed_target, speed_horizon_sessions):
            object.__setattr__(self, 'failure_ceiling', .99)
            object.__setattr__(self, 'alpha', alpha)
            object.__setattr__(self, 'speed_target', speed_target)
            object.__setattr__(self, 'speed_horizon_sessions', speed_horizon_sessions)
        monkeypatch.setattr(adjudication.DecisionRules, '__init__', altered_rules)
    else:
        def altered_decision(self, status, failure_counts, speed_successes, cutoffs):
            object.__setattr__(self, 'status', 'CONTINUE')
            object.__setattr__(self, 'failure_counts', failure_counts)
            object.__setattr__(self, 'speed_successes', speed_successes)
            object.__setattr__(self, 'cutoffs', cutoffs)
        monkeypatch.setattr(adjudication.StageDecision, '__init__', altered_decision)

    # Demonstrate a decision change through the actual implementation, so the
    # regression cannot pass by observing an irrelevant helper replacement.
    assert module.adjudicate_e1_outcomes(contract, outcomes, inventory)[affected_stage] == 'PASS'
    if when == 'before_freeze':
        with pytest.raises(ValueError):
            freeze()
    else:
        with pytest.raises(ValueError):
            dispatcher.verify_for(contract)
        with pytest.raises(ValueError):
            dispatcher(outcomes, inventory)


@pytest.mark.parametrize('failed_stage',['N1','N2','PART_B'])
def test_later_stage_evidence_after_failure_is_refused(failed_stage):
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    rules=SimpleNamespace(failure_ceiling=Decimal('.05'),alpha=Decimal('.05'),
        speed_target=Decimal('.5'),speed_horizon_sessions=200)
    contract=SimpleNamespace(replay=SimpleNamespace(decision_rules=rules,part_a=spec()))
    passed=PathOutcome('PASS',20,None,())
    failed=PathOutcome('FAILURE',None,'synthetic',())
    rows=(passed,)*970
    outcomes={'LEGALITY':{},'N1':{name:(passed,)*200 for name in ('FULL','H1','H2')},
              'N2':{'FULL':rows},'PART_B':{'H1':rows,'H2':rows}}
    if failed_stage=='N1':
        outcomes['N1']['H1']=(failed,)*200
    else:
        outcomes[failed_stage]['FULL' if failed_stage=='N2' else 'H1']=(failed,)*970
        outcomes['PART_A']={'REGIME':evidence([20]*100)[0]}
    with pytest.raises(ValueError,match='after failed'):
        adjudicate_e1_outcomes(contract,outcomes,{'records':[]})


@pytest.mark.parametrize('target,alpha,expected', [
    ('.500000000000000001', '.5', 'FAIL'),
    ('.5', '.499999999999999999', 'FAIL'),
    ('.5', '.5', 'PASS'),
])
def test_speed_confirmation_preserves_signed_decimal_boundary(target, alpha, expected):
    from c1_rail.qualification.result_adjudication import adjudicate_e1_outcomes
    rules = SimpleNamespace(failure_ceiling=Decimal('.9'), alpha=Decimal(alpha),
                            speed_target=Decimal(target), speed_horizon_sessions=200)
    contract = SimpleNamespace(replay=SimpleNamespace(decision_rules=rules))
    passed = (PathOutcome('PASS', 20, None, ()),)
    outcomes = {'LEGALITY': {}, 'N1': {p: passed for p in ('FULL', 'H1', 'H2')},
                'N2': {'FULL': passed}}
    assert adjudicate_e1_outcomes(contract, outcomes, {'records': []})['N2'] == expected
