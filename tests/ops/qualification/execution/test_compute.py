"""Compare real retained-source replay with PR415 mechanics; no outcome doubles."""
import importlib
import json

import pytest


@pytest.mark.parametrize('idle', [False, True])
def test_extracted_n1_matches_original_ordered_outcomes_and_decision(tmp_path, idle):
    compute = importlib.import_module('c1_rail.qualification.execution.compute')
    budget = importlib.import_module('c1_rail.qualification.execution.budget')
    from composition_fixture import build_verified_composition
    from c1_rail.qualification.production import _composition_executor
    from c1_rail.qualification.attempt import AttemptStore
    from c1_rail.qualification.adjudication import DecisionRules, adjudicate_stage
    from test_contract import NOW
    setup = build_verified_composition(tmp_path / 'source', idle=idle)
    contract = setup.contract
    store = AttemptStore.open(tmp_path / 'legacy.sqlite', campaign_id='parity-fixture',
        contract_digest=contract.contract_sha256, trust_domain_sha256=setup.domain.sha256,
        boot_id='test', now=NOW)
    store.reserve('TB_E1', b'{"fixture":true}', now=NOW)
    store.start_once('TB_E1', store.claimed_reservation('TB_E1'), now=NOW)
    dispatch = store.start_checkpoint_once('N1', store.claimed_reservation('TB_E1'), b'{"fixture":true}', now=NOW)
    old = _composition_executor(contract, setup.source, store).run_stage('n1', dispatch)
    new = compute.run_n1_compute(contract, setup.source, budget.BudgetGuard.from_contract(contract))
    # Probe/elapsed durations are nondeterministic diagnostics; all outcomes and
    # their order, source path diagnostics and domain discrimination must agree.
    assert (new.stage, new.populations, new.synthetic) == (old.stage, old.populations, old.synthetic)
    rules = contract.replay.decision_rules
    decision = adjudicate_stage(new, DecisionRules(rules.failure_ceiling, rules.alpha,
        rules.speed_target, rules.speed_horizon_sessions))
    assert decision.status == ('FAILURE' if idle else 'CONTINUE')
    if idle:
        assert all(row.status == 'UNRESOLVED' for _, rows in new.populations for row in rows)


@pytest.mark.parametrize('meter', ['wall', 'cpu', 'memory'])
def test_budget_rejects_exhaustion_without_reset(monkeypatch, meter):
    module = importlib.import_module('c1_rail.qualification.execution.budget')
    from c1_rail.qualification.runner import NeedsContext
    from types import SimpleNamespace
    readings = dict(wall=0, cpu=0, memory=0)
    monkeypatch.setattr(module, 'perf_counter_ns', lambda: readings['wall'])
    monkeypatch.setattr(module, 'process_time_ns', lambda: readings['cpu'])
    monkeypatch.setattr(module, 'peak_memory_bytes', lambda: readings['memory'])
    guard = module.BudgetGuard(SimpleNamespace(maximum_wall_seconds=1, maximum_cpu_seconds=1,
                                               maximum_memory_bytes=100))
    assert guard.remaining_wall_seconds() == 1
    readings[meter] = 101 if meter == 'memory' else 1000000001
    with pytest.raises(NeedsContext, match='budget'):
        guard.check_and_measure()

