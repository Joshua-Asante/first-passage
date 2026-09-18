"""Frozen resource limits must hold after the final kernel/proof work."""
import pytest

from c1_rail.qualification import orchestration, part_a, production, runner
from c1_rail.qualification.attempt import AttemptStore, TransitionError
from c1_rail.qualification.orchestration import _run_composition_e1
from composition_fixture import build_verified_composition
from test_composition_route import _preflight
from test_contract import NOW


@pytest.fixture(scope='module')
def budget_setup(tmp_path_factory):
    # Budget boundaries need a small genuine signed workload, not production
    # statistical power. At n=2, alpha=.95 admits zero failures (.95**2=.9025)
    # and two speed successes (.5**2=.25), through the actual adjudicator.
    return build_verified_composition(tmp_path_factory.mktemp('budget-inputs'),
                                      confirmation_depth=2, decision_alpha='0.95')


def _meters(monkeypatch):
    # Resource observations are deterministic; the production budget checks run.
    readings = {'cpu': 0, 'wall': 0, 'memory': 0}
    monkeypatch.setattr(production, 'process_time', lambda: readings['cpu'])
    monkeypatch.setattr(production, 'perf_counter', lambda: readings['wall'])
    monkeypatch.setattr(production, '_peak_memory_bytes', lambda: readings['memory'])
    return readings


@pytest.mark.parametrize('resource', ['cpu', 'wall'])
def test_issued_budget_origin_cannot_be_replaced(budget_setup, tmp_path, monkeypatch, resource):
    setup = budget_setup
    _, store, _ = _preflight(setup, tmp_path)
    readings = _meters(monkeypatch)
    executor = production._composition_executor(setup.contract, setup.source, store)
    binding = production._ISSUED_EXECUTORS[id(executor)]
    readings[resource] = getattr(setup.contract.replay.budget, f'maximum_{resource}_seconds') + 1
    # A producer may read the inventory, but cannot replace an issued record.
    with pytest.raises((TypeError, AttributeError)):
        production._ISSUED_EXECUTORS[id(executor)] = production._ExecutorBinding(
            binding.reference, binding.contract, binding.source, binding.store,
            binding.domain, readings['wall'], readings['cpu'])
    with pytest.raises(runner.NeedsContext, match='budget'):
        executor._budget()


def test_issued_budget_origin_cannot_be_mutated(budget_setup, tmp_path, monkeypatch):
    setup = budget_setup
    _, store, _ = _preflight(setup, tmp_path)
    readings = _meters(monkeypatch)
    executor = production._composition_executor(setup.contract, setup.source, store)
    binding = production._ISSUED_EXECUTORS[id(executor)]
    readings['wall'] = setup.contract.replay.budget.maximum_wall_seconds + 1
    with pytest.raises((TypeError, AttributeError)):
        object.__setattr__(binding, 'wall_start', readings['wall'])
    with pytest.raises(runner.NeedsContext, match='budget'):
        executor._budget()


def test_rebinding_inventory_cannot_reset_budget_or_reinitialize(budget_setup, tmp_path, monkeypatch):
    from types import MappingProxyType

    setup = budget_setup
    _, store, _ = _preflight(setup, tmp_path)
    readings = _meters(monkeypatch)
    executor = production._composition_executor(setup.contract, setup.source, store)
    binding = production._ISSUED_EXECUTORS[id(executor)]
    readings['cpu'] = setup.contract.replay.budget.maximum_cpu_seconds + 1
    forged = production._ExecutorBinding(binding.reference, binding.contract, binding.source,
        binding.store, binding.domain, readings['wall'], readings['cpu'])
    monkeypatch.setattr(production, '_ISSUED_EXECUTORS', MappingProxyType({id(executor): forged}))
    with pytest.raises(runner.NeedsContext, match='budget'):
        executor._budget()
    with pytest.raises(ValueError, match='already initialized'):
        executor._initialize(setup.contract, setup.source, store, setup.domain)


def _fast_replay(monkeypatch):
    """Replace expensive strategy/broker execution, preserving its typed output.

    Sampling, continuous proof construction, identity checks, the actual kernel,
    controller and SQLite stay real. N1/CPU also runs without this replacement.
    """
    from c1_rail.qualification.model import LEG_IDS, EdgeState, ReplayResult, SessionRecord
    from c1_rail.qualification.production_source import ProductionSource

    zero = tuple((leg, 0) for leg in LEG_IDS)
    edge = EdgeState(zero, zero, zero)

    def replay(self, path):
        self.verify_for(self.contract)
        return ReplayResult(tuple(SessionRecord(
            row.occurrence, row.path_session_date, row.source.session_id,
            2000., 0., 2, True, edge, edge) for row in path), ())

    monkeypatch.setattr(ProductionSource, 'replay', replay)


def _run(setup, store, preflight, approval):
    return _run_composition_e1(
        setup.contract, source=setup.source, store=store, preflight=preflight,
        exact_depth_approval_bytes=approval, trusted_keys=setup.trusted_keys,
        now=lambda: NOW)


def _after_last_evaluation(monkeypatch, store, checkpoint, after):
    module = part_a if checkpoint == 'PART_A' else runner
    evaluate = module.evaluate_replay
    # Signed budget-fixture depths: N1 and N2 FULL/H1/H2 each 3*2,
    # Part A two panels of two paths, each plus its disjoint probe.
    final_index = {'N1': 7, 'N2': 7, 'PART_A': 5}[checkpoint]
    count = 0

    def evaluate_then_observe(*args, **kwargs):
        nonlocal count
        result = evaluate(*args, **kwargs)
        active = next(row for row in store.checkpoints()
                      if row['state'] == 'STARTED_IN_DOUBT')['checkpoint']
        if active == checkpoint:
            count += 1
            if count == final_index:
                after()
        return result

    monkeypatch.setattr(module, 'evaluate_replay', evaluate_then_observe)


def _assert_uncompleted_after_reopen(setup, store, preflight, approval, checkpoint, readings):
    rows = store.checkpoints()
    target = next(row for row in rows if row['checkpoint'] == checkpoint)
    assert target['state'] == 'STARTED_IN_DOUBT'
    assert target['receipt_bytes'] is None
    index = [row['checkpoint'] for row in rows].index(checkpoint)
    assert all(row['state'] == 'PENDING' for row in rows[index + 1:])
    assert store.result('TB_E1') is None
    reopened = AttemptStore.open(
        store.path, campaign_id=store.campaign_id,
        contract_digest=setup.contract.contract_sha256,
        trust_domain_sha256=setup.domain.sha256, boot_id='budget-reopen', now=NOW)
    before = reopened.events()
    # Model a fresh process for journal recovery. The original process's peak
    # memory correctly remains over budget and would refuse before redispatch.
    readings.update(cpu=0, wall=0, memory=0)
    with pytest.raises(TransitionError, match='already dispatched'):
        _run(setup, reopened, preflight, approval)
    assert reopened.checkpoints() == rows
    assert reopened.events() == before
    assert reopened.result('TB_E1') is None


@pytest.mark.parametrize(('checkpoint', 'resource'), [
    ('N1', 'cpu'), ('N1', 'wall'), ('N2', 'memory'),
    ('PART_A', 'cpu'), ('PART_A', 'memory'), ('PART_A', 'wall'),
])
def test_final_kernel_overrun_cannot_complete_checkpoint(
        budget_setup, tmp_path, monkeypatch, checkpoint, resource):
    setup = budget_setup
    preflight, store, approval = _preflight(setup, tmp_path)
    if (checkpoint, resource) != ('N1', 'cpu'):
        _fast_replay(monkeypatch)
    readings = _meters(monkeypatch)
    budget = setup.contract.replay.budget
    limit = {'cpu': budget.maximum_cpu_seconds,
             'wall': budget.maximum_wall_seconds,
             'memory': budget.maximum_memory_bytes}[resource]

    def exceed():
        readings[resource] = limit + 1

    _after_last_evaluation(monkeypatch, store, checkpoint, exceed)
    with pytest.raises(runner.NeedsContext, match='budget'):
        _run(setup, store, preflight, approval)
    _assert_uncompleted_after_reopen(setup, store, preflight, approval, checkpoint, readings)


def test_final_kernel_within_frozen_limits_can_complete(budget_setup, tmp_path, monkeypatch):
    setup = budget_setup
    preflight, store, approval = _preflight(setup, tmp_path)
    _fast_replay(monkeypatch)
    readings = _meters(monkeypatch)
    budget = setup.contract.replay.budget

    def reach_allowed_limits():
        readings.update(cpu=budget.maximum_cpu_seconds,
                        wall=budget.maximum_wall_seconds - 1,
                        memory=budget.maximum_memory_bytes)

    _after_last_evaluation(monkeypatch, store, 'PART_A', reach_allowed_limits)
    execution = _run(setup, store, preflight, approval)
    assert execution.passed and execution.synthetic
    assert all(row['state'] == 'COMPLETED' for row in store.checkpoints())


def test_proof_exception_still_enforces_final_memory_budget(budget_setup, tmp_path, monkeypatch):
    from c1_rail.qualification.production_source import ProductionSource

    setup = budget_setup
    preflight, store, approval = _preflight(setup, tmp_path)
    _fast_replay(monkeypatch)
    readings = _meters(monkeypatch)
    proof = ProductionSource.proof

    def proof_then_fail(self, panel):
        proof(self, panel)
        readings['memory'] = setup.contract.replay.budget.maximum_memory_bytes + 1
        raise RuntimeError('TEST_ONLY proof failure after memory overrun')

    monkeypatch.setattr(ProductionSource, 'proof', proof_then_fail)
    with pytest.raises(runner.NeedsContext, match='memory budget'):
        _run(setup, store, preflight, approval)
    _assert_uncompleted_after_reopen(setup, store, preflight, approval, 'PART_A', readings)


@pytest.mark.parametrize(('checkpoint', 'boundary', 'resource'), [
    ('N1', 'adjudication', 'cpu'),
    ('PART_A', 'receipt_serialization', 'memory'),
])
def test_controller_tail_overrun_cannot_complete_checkpoint(
        budget_setup, tmp_path, monkeypatch, checkpoint, boundary, resource):
    setup = budget_setup
    preflight, store, approval = _preflight(setup, tmp_path)
    _fast_replay(monkeypatch)
    readings = _meters(monkeypatch)
    budget = setup.contract.replay.budget

    if boundary == 'adjudication':
        adjudicate = orchestration.adjudicate_e1_outcomes

        def adjudicate_then_exceed(*args, **kwargs):
            result = adjudicate(*args, **kwargs)
            if any(row['checkpoint'] == checkpoint and row['state'] == 'STARTED_IN_DOUBT'
                   for row in store.checkpoints()):
                readings[resource] = budget.maximum_cpu_seconds + 1
            return result

        monkeypatch.setattr(orchestration, 'adjudicate_e1_outcomes', adjudicate_then_exceed)
    else:
        serialize = orchestration.canonical_bytes

        def serialize_then_exceed(value):
            result = serialize(value)
            if (isinstance(value, dict) and value.get('schema') == 'e1_checkpoint_receipt/v1'
                    and value.get('checkpoint') == checkpoint):
                readings[resource] = budget.maximum_memory_bytes + 1
            return result

        monkeypatch.setattr(orchestration, 'canonical_bytes', serialize_then_exceed)

    with pytest.raises(runner.NeedsContext, match='budget'):
        _run(setup, store, preflight, approval)
    _assert_uncompleted_after_reopen(setup, store, preflight, approval, checkpoint, readings)


def test_final_inventory_serialization_overrun_cannot_return_execution(
        budget_setup, tmp_path, monkeypatch):
    setup = budget_setup
    preflight, store, approval = _preflight(setup, tmp_path)
    _fast_replay(monkeypatch)
    readings = _meters(monkeypatch)
    serialize = orchestration.canonical_bytes

    def serialize_then_exceed(value):
        result = serialize(value)
        if isinstance(value, dict) and value.get('schema') == 'qualification_path_inventory/v1':
            readings['wall'] = setup.contract.replay.budget.maximum_wall_seconds + 1
        return result

    monkeypatch.setattr(orchestration, 'canonical_bytes', serialize_then_exceed)
    with pytest.raises(runner.NeedsContext, match='budget'):
        _run(setup, store, preflight, approval)
    # Earlier receipts were completed within budget. Final assembly must still
    # refuse to return an execution; no authenticated result has been committed.
    assert all(row['state'] == 'COMPLETED' for row in store.checkpoints())
    assert store.result('TB_E1') is None
