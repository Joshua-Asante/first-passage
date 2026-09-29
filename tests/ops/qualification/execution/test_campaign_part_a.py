"""S5 Part A engine-adapter boundary tests (packet S5-D1/S5-D2 and section 1a).

Pure boundary cases run ``part_a._run_part_a`` directly with synthetic
providers and exact outcome vectors; adapter cases run
``compute.run_part_a_compute`` on the real TEST_ONLY composition fixture the
way ``test_compute.py`` builds it. The packet's third required assertion
(``part_a_worker_launch_count == 1``) needs the worker route and lives with
it, not here. Ticket 2c adds the worker-route boundary cases beside them: the
P-3/P-7/SR-6/SR-9 static facts and the W5 worker-result parse refusals.
"""
import ast
import importlib
import inspect
import json
from dataclasses import FrozenInstanceError, replace
from datetime import date
from decimal import Decimal, localcontext
from math import ceil
from pathlib import Path
from types import SimpleNamespace

import pytest

from bundle_fixture import build_bundle
from composition_fixture import build_verified_composition
from test_part_a import EDGE, STATE, request, source
from test_worker import part_a_stage_input
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.protocol import decode_frame, sha256
from c1_rail.qualification.execution import compute
from c1_rail.qualification.execution.budget import BudgetGuard
from c1_rail.qualification.model import ReplayResult, SessionRecord
from c1_rail.qualification.part_a import _run_part_a
from c1_rail.qualification.production_source import ProductionSource


def engine(req, *, pnl_for=None, full=1., on_initial_prefix=None,
           proof_calls=None, replay_calls=None):
    """``_run_part_a`` over the shared synthetic source with per-path pnl control.

    Reuse of the ``test_part_a`` providers: the pilot replay is call zero and
    call ``k >= 1`` is panel ``(k-1)//depth``, path ``(k-1)%depth`` -- the
    engine's own panel-major order. ``pnl`` 1200 passes, 0 stays UNRESOLVED.
    """
    if pnl_for is None:
        def pnl_for(panel, path):
            return 1200.
    seen = [0]

    def prove(panel):
        if proof_calls is not None:
            proof_calls.append(panel)
        return (EDGE,) * (len(panel) + 1), (True,) * (len(panel) - 1)

    def replay(path):
        index = seen[0]
        seen[0] += 1
        if replay_calls is not None:
            replay_calls.append(path)
        panel, path_index = (None, 0) if index == 0 else divmod(index - 1, req.depth)
        pnl = 1200. if panel is None else pnl_for(panel, path_index)
        return ReplayResult(tuple(SessionRecord(s.occurrence, s.path_session_date, s.source.session_id,
            pnl, min(pnl, 0.), int(pnl != 0), True, EDGE, EDGE) for s in path), ())

    return _run_part_a(req, source(), adjacent=(True,) * 11, covered_until=date(2025, 1, 1),
        proof_provider=prove, replay_provider=replay, initial_state=STATE,
        full_pass_rate=full, synthetic=True, timer=lambda: 0.,
        on_initial_prefix=on_initial_prefix)


def n2_full_statuses(contract):
    """The plain N2 FULL outcome input ticket 1 uses (S5-D2 transport is ticket 2).

    The tuple length is the frozen N2 depth, and its statuses are the ones
    S4's own N2 compute produces on this fixture (all PASS, pinned by the
    parity checks below).
    """
    return tuple('PASS' for _ in range(contract.stage_specs['N2'].exact_depth))


# ---- Pure engine boundary cases (packet S5-D1; exact outcome vectors) --------


def test_no_expansion_when_initial_p5_is_far_from_the_floor():
    result = engine(request(floor=0.5))
    assert not result.expanded and result.passed
    assert len(result.panels) == request().initial_panels
    assert result.initial_p5 == result.final_p5 == 1.0


def test_required_expansion_appends_panels_after_the_unchanged_prefix():
    initial_only = engine(request(max_panels=2))
    expanded = engine(request())
    assert initial_only.expanded is False and expanded.expanded is True
    assert [panel.index for panel in expanded.panels] == [0, 1, 2, 3]
    assert expanded.panels[:request().initial_panels] == initial_only.panels


def test_exact_tolerance_equality_expands_as_decimal():
    def half_rate(panel, path):
        return 1200. if path == 0 else 0.

    # The decision is Decimal: |0.5 - floor| == within_pp expands exactly.
    assert Decimal('0.5') - Decimal('0.49') == Decimal('0.01')
    assert Decimal('0.5') - Decimal('0.48') == Decimal('0.02') > Decimal('0.01')
    assert engine(request(floor=0.49, within_pp=.01), pnl_for=half_rate).expanded
    assert not engine(request(floor=0.48, within_pp=.01), pnl_for=half_rate).expanded


def test_below_floor_failure_without_expansion():
    result = engine(request(), pnl_for=lambda panel, path: 0.)
    assert not result.expanded and not result.passed
    assert len(result.panels) == 2
    assert result.failure_reason == 'below_floor'


def test_above_full_failure_is_refused():
    result = engine(request(), full=.9)
    assert not result.passed and result.failure_reason == 'p5_above_full'
    # The FULL sanity comparison applies after the required expansion.
    assert result.expanded and len(result.panels) == 4


def test_initial_prefix_bytes_survive_expansion_unchanged():
    custody = []
    result = engine(request(), on_initial_prefix=custody.append)
    initial_panel_bytes = compute.part_a_panel_bytes(custody[0])
    final_panel_bytes = compute.part_a_panel_bytes(result.panels)
    assert result.expanded and custody[0] == result.panels[:2]
    assert final_panel_bytes[:len(initial_panel_bytes)] == initial_panel_bytes


# ---- Prefix custody ordering (packet S5-D1, the finding-5 correction) --------


def test_custody_hook_runs_before_the_decision_and_any_appended_panel_sample():
    proof_calls, replay_calls, events = [], [], []

    def hook(panels):
        events.append((tuple(panel.index for panel in panels), panels,
                       len(proof_calls), len(replay_calls)))

    result = engine(request(), on_initial_prefix=hook,
                    proof_calls=proof_calls, replay_calls=replay_calls)
    # One call, exactly after the initial panels and before anything else:
    # pilot + both initial panels only, and the initial prefix it saw is the
    # one the result returns.
    assert len(events) == 1
    assert events[0] == ((0, 1), result.panels[:2], 3, 5)
    assert len(proof_calls) == 5 and len(replay_calls) == 9
    # The hook precedes the decision itself: it runs even when the decision
    # turns out negative, still before any appended panel could be sampled.
    quiet = []
    far = engine(request(floor=0.5), on_initial_prefix=lambda panels: quiet.append(panels),
                 proof_calls=proof_calls, replay_calls=replay_calls)
    assert not far.expanded and quiet == [far.panels]


def test_raising_custody_hook_yields_no_expansion_and_no_final_result():
    class CustodyRefused(RuntimeError):
        pass

    proof_calls, replay_calls = [], []

    def hook(panels):
        raise CustodyRefused('prefix custody writer failed')

    with pytest.raises(CustodyRefused):
        engine(request(), on_initial_prefix=hook,
               proof_calls=proof_calls, replay_calls=replay_calls)
    # The exception propagates with no appended panel sampled and no result.
    assert len(proof_calls) == 3 and len(replay_calls) == 5


# ---- Adapter gates (section 1a: SR-2, S5-D2, factory-built source) -----------


@pytest.mark.parametrize('authority_class,permits_synthetic,override', [
    ('OPERATOR', True, lambda: compute.PartAMeasurementOverride()),
    ('TEST_ONLY', False, lambda: compute.PartAMeasurementOverride()),
    ('TEST_ONLY', True, lambda: object()),
])
def test_measurement_gate_refuses_before_any_source_or_compute(
        authority_class, permits_synthetic, override):
    contract = SimpleNamespace(trust_domain=SimpleNamespace(
        authority_class=authority_class, permits_synthetic=permits_synthetic))
    verified, custody = [], []
    source_stub = SimpleNamespace(verify_for=lambda c: verified.append(c))

    with pytest.raises(ValueError, match='TEST_ONLY synthetic contract required'):
        compute.run_part_a_compute(contract, source_stub, None,
                                   n2_full_outcomes=('PASS',),
                                   measurement_override=override(),
                                   on_initial_prefix=custody.append)
    # The gate fires before the source type check (a TypeError would surface
    # otherwise), before verify_for and before prefix custody.
    assert verified == [] and custody == []


@pytest.mark.parametrize('outcomes', [
    (), ('PASS', 'UNKNOWN_STATUS'), ('pass',), ('PASS', None), ('PASS', True),
    ('PASS', ''), ['PASS'],
], ids=['empty', 'open-status', 'lowercase', 'none', 'bool', 'empty-string', 'list'])
def test_n2_full_outcomes_require_a_nonempty_closed_status_tuple(outcomes):
    contract = SimpleNamespace(trust_domain=SimpleNamespace(
        authority_class='TEST_ONLY', permits_synthetic=True))
    # A stand-in contract and source are never touched: the outcome refusal
    # precedes the source type check (TypeError) and verification.
    with pytest.raises(ValueError):
        compute.run_part_a_compute(contract, object(), None, n2_full_outcomes=outcomes)
    assert compute._part_a_full_pass_rate(('PASS', 'FAILURE')) == 0.5
    assert compute._part_a_full_pass_rate(('UNRESOLVED',)) == 0.0
    assert compute._part_a_full_pass_rate(('PASS', 'UNRESOLVED', 'FAILURE')) == 1 / 3


def test_adapter_requires_a_factory_built_source():
    contract = SimpleNamespace(trust_domain=SimpleNamespace(
        authority_class='TEST_ONLY', permits_synthetic=True))
    verified = []

    class Lookalike(ProductionSource):
        pass

    for bad in (SimpleNamespace(verify_for=lambda c: verified.append(c)),
                object.__new__(Lookalike)):
        with pytest.raises(TypeError, match='factory-built source required'):
            compute.run_part_a_compute(contract, bad, None, n2_full_outcomes=('PASS',))
    assert verified == []


# ---- P-2: the closed override value ------------------------------------------


def test_override_label_and_frozen_exactly_one_point_zero():
    override = compute.PartAMeasurementOverride()
    assert type(override.within_pp) is float and override.within_pp == 1.0
    assert override.label == 'TEST_ONLY_MEASUREMENT_FORCED_EXPANSION'
    assert override.label == compute.PART_A_MEASUREMENT_LABEL
    assert compute.PartAMeasurementOverride(within_pp=1.0) == override
    with pytest.raises(FrozenInstanceError):
        override.within_pp = 0.99


@pytest.mark.parametrize('value', [0.99, 0.0, 1, True, Decimal('1.0'), float('nan'), 1.0000001])
def test_override_refuses_every_value_except_exactly_one_point_zero(value):
    with pytest.raises(ValueError):
        compute.PartAMeasurementOverride(within_pp=value)
    assert compute.PartAMeasurementOverride(within_pp=1.0).within_pp == 1.0


# ---- Adapter on the real TEST_ONLY composition fixture -----------------------


def test_adapter_without_override_never_expands_on_the_composition_fixture(tmp_path):
    """Packet S5-D1/S5-D2 on the frozen (2, 4, 2) fixture: a panel rate is
    0, 0.5 or 1, never within 0.01 of 0.95, so no genuine campaign expands
    (packet section 0.1, finding F1)."""
    setup = build_verified_composition(tmp_path / 'source')
    contract, source_ = setup.contract, setup.source
    part = contract.replay.part_a
    assert (part.initial_panels, part.expanded_panels,
            part.paths_per_population_per_panel) == (2, 4, 2)
    custody = []
    out = compute.run_part_a_compute(contract, source_,
        BudgetGuard.from_contract(contract), n2_full_outcomes=n2_full_statuses(contract),
        on_initial_prefix=custody.append)
    final_panel_bytes = out.final_panel_bytes
    initial_panel_bytes = out.initial_panel_bytes
    expanded_panels = part.expanded_panels
    initial_panels = part.initial_panels
    expansion_required = out.expansion_required
    actual_panel_count = out.final_panels
    assert final_panel_bytes[:len(initial_panel_bytes)] == initial_panel_bytes
    assert actual_panel_count == (expanded_panels if expansion_required else initial_panels)
    # No expansion on this fixture: the final artifact is the initial prefix,
    # the run is a plain pass, and the prefix custody saw the returned bytes.
    assert expansion_required is False and out.measurement_forced is False
    assert final_panel_bytes == initial_panel_bytes
    assert len(custody) == 1 and custody[0] is initial_panel_bytes
    assert out.result.passed and out.result.failure_reason is None


def test_override_refuses_before_source_verification_and_before_any_output_file(
        tmp_path, monkeypatch):
    """P-1: an OPERATOR-domain contract with an override is refused at the
    gate, before ``verify_for`` runs and before any output file can exist."""
    setup = build_verified_composition(tmp_path / 'source')
    operator_domain = replace(setup.domain, authority_class='OPERATOR')
    operator_contract = replace(setup.contract, trust_domain=operator_domain)
    verified, custody = [], []
    original = ProductionSource.verify_for

    def spy(self, contract):
        verified.append(contract)
        return original(self, contract)

    monkeypatch.setattr(ProductionSource, 'verify_for', spy)
    out_dir = tmp_path / 'out'
    out_dir.mkdir()
    with pytest.raises(ValueError, match='TEST_ONLY synthetic contract required'):
        compute.run_part_a_compute(operator_contract, setup.source,
            BudgetGuard.from_contract(setup.contract), n2_full_outcomes=('PASS',),
            measurement_override=compute.PartAMeasurementOverride(),
            on_initial_prefix=custody.append)
    assert verified == [] and custody == []
    assert list(out_dir.rglob('*')) == []


def test_forced_override_expands_and_keeps_the_initial_prefix_bytes(tmp_path):
    """P-6: with within_pp forced to 1.0 the same fixture expands to the frozen
    expanded panel count, and the initial prefix is byte-identical to the
    unforced run's."""
    setup = build_verified_composition(tmp_path / 'source')
    contract, source_ = setup.contract, setup.source
    part = contract.replay.part_a
    plain = compute.run_part_a_compute(contract, source_,
        BudgetGuard.from_contract(contract), n2_full_outcomes=n2_full_statuses(contract))
    assert plain.expansion_required is False
    forced = compute.run_part_a_compute(contract, source_,
        BudgetGuard.from_contract(contract), n2_full_outcomes=n2_full_statuses(contract),
        measurement_override=compute.PartAMeasurementOverride())
    assert forced.measurement_forced is True
    assert forced.expansion_required is True
    assert (forced.initial_panels, forced.final_panels) == (part.initial_panels, part.expanded_panels)
    assert forced.initial_panel_bytes == plain.initial_panel_bytes
    assert forced.final_panel_bytes[:len(forced.initial_panel_bytes)] == forced.initial_panel_bytes
    assert forced.result.panels[:plain.final_panels] == plain.result.panels


def test_adapter_parity_with_exact_decimal_recomputation(tmp_path):
    """Packet S5-D2/section 3: the adapter's full pass rate, percentile and
    decision agree with an exact-Decimal recomputation from the same outcomes.
    Any disagreement is an engine-contract conflict, never a tolerance."""
    setup = build_verified_composition(tmp_path / 'source')
    contract, source_ = setup.contract, setup.source
    part = contract.replay.part_a
    outcomes = n2_full_statuses(contract)
    out = compute.run_part_a_compute(contract, source_,
        BudgetGuard.from_contract(contract), n2_full_outcomes=outcomes)

    def exact_p5(panels):
        rates = sorted(Decimal(panel.passes) / Decimal(len(panel.outcomes)) for panel in panels)
        rank = ceil(part.percentile * len(rates))
        return rates[max(0, rank - 1)]

    with localcontext() as ctx:
        ctx.prec = 60
        exact_initial = exact_p5(out.result.panels[:out.initial_panels])
        exact_final = exact_p5(out.result.panels)
        exact_full = Decimal(sum(status == 'PASS' for status in outcomes)) / Decimal(len(outcomes))
        expanded = (abs(exact_initial - part.expansion_center_p5) <= part.expansion_tolerance
                    and part.expanded_panels > part.initial_panels)
        reason = ('p5_above_full' if exact_final > exact_full
                  else 'below_floor' if exact_final < part.expansion_center_p5 else None)
    assert Decimal(str(out.full_pass_rate)) == exact_full
    assert out.full_pass_rate == float(exact_full)
    assert Decimal(str(out.result.initial_p5)) == exact_initial
    assert Decimal(str(out.result.final_p5)) == exact_final
    assert out.expansion_required == expanded
    assert out.result.failure_reason == reason
    assert out.result.passed == (reason is None)


# ---- Ticket 2c: the worker route boundary (P-3, P-7, SR-6, SR-9, W5) ---------


def _override_sites():
    """Every ops/ file naming PartAMeasurementOverride, split by use kind."""
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    root = Path(worker.__file__).resolve().parents[3]
    class_sites, call_sites = {}, {}
    for path in sorted(root.rglob('*.py')):
        tree = ast.parse(path.read_bytes(), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == 'PartAMeasurementOverride':
                class_sites.setdefault(path.relative_to(root).as_posix(), []).append(node.lineno)
            if isinstance(node, ast.Call):
                target = node.func
                name = (target.id if isinstance(target, ast.Name)
                        else target.attr if isinstance(target, ast.Attribute) else None)
                if name == 'PartAMeasurementOverride':
                    call_sites.setdefault(path.relative_to(root).as_posix(), []).append(node.lineno)
    return class_sites, call_sites


def test_compute_part_a_request_matches_the_gated_route_mapping(tmp_path):
    """R1 parity: the worker-closure copy of the request mapping equals
    ``production._part_a_request`` on the composition fixture contract.
    Placed before the module-scoped ``g5_chain`` fixture's first use: that
    fixture patches ``worker.utc_now`` for the rest of the module, and the
    composition build's runtime inventory refuses a patched role module."""
    from c1_rail.qualification.production import _part_a_request

    setup = build_verified_composition(tmp_path / 'source')
    contract, start = setup.contract, setup.source.path_start_date
    for budget in (12., 0.5):
        assert compute.part_a_request(contract, start, budget) == _part_a_request(contract, start, budget)
    assert compute.part_a_request(contract, start, 12.).initial_panels == contract.replay.part_a.initial_panels


def test_only_the_compute_adapter_may_name_the_part_a_measurement_override():
    """P-3: the override exists only as the compute adapter's TEST_ONLY seam.

    In ops/ the name may appear only as compute.py's ClassDef (or a call to
    it there); no dispatch or settlement route constructs one."""
    class_sites, call_sites = _override_sites()
    compute_path = 'c1_rail/qualification/execution/compute.py'
    assert set(class_sites) == {compute_path}
    assert set(call_sites) <= {compute_path}
    for module in ('worker.py', 'service.py', 'campaign_supervisor.py', 'g5.py',
                   'campaign_protocol.py'):
        assert 'c1_rail/qualification/execution/' + module not in call_sites


def test_run_part_a_body_is_compute_side_and_store_free():
    """P-7: the PART_A body runs behind the compute boundary with no campaign
    store or journal import, and run_worker routes the checkpoint through it."""
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    tree = ast.parse(inspect.getsource(worker))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module)
            imported.update(alias.name for alias in node.names)
    assert 'campaign_store' not in imported
    assert 'journal' not in imported
    assert not any('campaign_store' in name for name in imported)
    assert not any('journal' in name for name in imported)
    run_worker_def = next(node for node in tree.body
                          if isinstance(node, ast.FunctionDef) and node.name == 'run_worker')
    assert any(isinstance(node, ast.Name) and node.id == 'run_part_a_body'
               for node in ast.walk(run_worker_def))


def test_phase_budget_guard_measures_the_three_settlement_observations():
    """SR-6: the campaign guard reports exactly the three observations the
    settlement compares; it never re-derives a fresh contract allowance."""
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    guard = worker.PhaseBudgetGuard(
        {'cpu_ns': 3600 * 10**9, 'wall_ns': 3600 * 10**9, 'memory_bytes': 2**40})
    observed = guard.check_and_measure()
    assert set(observed) == {'worker_compute_wall_ns', 'worker_cpu_ns',
                             'worker_peak_memory_bytes', 'remaining_wall_seconds'}
    assert all(type(observed[name]) is int and observed[name] >= 0 for name in
               ('worker_compute_wall_ns', 'worker_cpu_ns', 'worker_peak_memory_bytes'))
    assert observed['worker_compute_wall_ns'] < 3600 * 10**9
    assert observed['worker_cpu_ns'] < 3600 * 10**9


@pytest.mark.parametrize('phrase', [
    'unnecessary expansion',
    'omitted expansion',
    'expansion_center_p5',
    'expansion_tolerance',
])
def test_the_part_a_body_names_no_expansion_justification(phrase):
    """SR-9: the worker body justifies no expansion decision; the criteria
    live in the frozen contract and the engine, never in the route."""
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    assert phrase not in inspect.getsource(worker.run_part_a_body)


def test_part_a_worker_result_parse_refuses_every_mutation(tmp_path, monkeypatch):
    """W5/W5a: the captured PART_A document from a real worker run refuses a
    swapped panel vector, an altered source occurrence, a wrong panel count, a
    wrong prefix digest, a forced expansion fact, a missing, altered or open
    pilot identity, and an N2 FULL baseline that is out of range or not two
    integers. One real PART_A run stages the document; every mutation is
    re-encoded and refused."""
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    evidence = importlib.import_module('c1_rail.qualification.execution.evidence')
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)
    context, pa, out, payload, assessment, receipt = part_a_stage_input(tmp_path, case, monkeypatch)
    frame = worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=out)
    doc = json.loads(decode_frame(frame, limit=context.profile.output_byte_limit))
    plan = (pa / 'plan.json').read_bytes()
    evidence.parse_worker_result(encoded(doc), context=context, execution_id='pawork',
                                 plan_bytes=plan)

    def swap_two_panels(document):
        rows = document['part_a']['panels']
        rows[0], rows[1] = rows[1], rows[0]

    def alter_one_source_session_id(document):
        document['part_a']['panels'][0]['source_session_ids'][0] += '-tampered'

    def wrong_final_panels(document):
        document['part_a']['final_panels'] += 1

    def altered_initial_prefix_digest(document):
        document['part_a']['initial_prefix_sha256'] = '0' * 64

    def forced_expansion_fact(document):
        document['part_a']['expansion_required'] = True

    def missing_pilot(document):
        del document['part_a']['pilot']

    def altered_pilot_digest(document):
        document['part_a']['pilot']['seed_input_sha256s'][0] = 'e' * 64

    def added_pilot_key(document):
        document['part_a']['pilot']['within_pp'] = 1.0

    def zero_path_baseline(document):
        document['part_a']['n2_full_baseline']['paths'] = 0

    def negative_pass_baseline(document):
        document['part_a']['n2_full_baseline']['passes'] = -1

    def above_path_baseline(document):
        baseline = document['part_a']['n2_full_baseline']
        baseline['passes'] = baseline['paths'] + 1

    def boolean_pass_baseline(document):
        document['part_a']['n2_full_baseline']['passes'] = True

    for name, mutate in (
        ('swap-two-panels', swap_two_panels),
        ('alter-one-source-session-id', alter_one_source_session_id),
        ('wrong-final-panels', wrong_final_panels),
        ('altered-initial-prefix-digest', altered_initial_prefix_digest),
        ('forced-expansion-fact', forced_expansion_fact),
        ('missing-pilot', missing_pilot),
        ('altered-pilot-digest', altered_pilot_digest),
        ('added-pilot-key', added_pilot_key),
        ('zero-path-baseline', zero_path_baseline),
        ('negative-pass-baseline', negative_pass_baseline),
        ('above-path-baseline', above_path_baseline),
        ('boolean-pass-baseline', boolean_pass_baseline),
    ):
        mutated = json.loads(json.dumps(doc))
        mutate(mutated)
        try:
            evidence.parse_worker_result(encoded(mutated), context=context,
                                         execution_id='pawork', plan_bytes=plan)
        except ValueError:
            continue
        raise AssertionError('the captured part a document accepted ' + name)


# ---- Ticket 2d / P1 / P2: the G5 PART_A reconstruction over a genuine chain ----
#
# One /v7 bundle drives the real worker three times (N1, joint N2, PART_A);
# each committed assessment is G5's own reconstruction of the previous
# capture, so the PART_A builder sees genuine predecessor custody. The
# capture families (result, attestation, snapshot) are fabricated over the
# real worker bytes with shape-only signatures: custody is the G5 driver's
# and the service's, never the builder's. Cases the (2, 4, 2) fixture cannot
# produce stand on the adjudicator directly and say so:
#   omitted expansion -> test_result_adjudication
#       ::test_initial_close_call_requires_expansion_with_original_prefix
#   above-FULL failure -> test_result_adjudication
#       ::test_fifth_rank_and_full_sanity_use_actual_nested_outcomes


def _signed(core_bytes):
    import base64

    return encoded(
        dict(
            json.loads(core_bytes),
            signature={
                'algorithm': 'Ed25519',
                'key_id': 'fixture',
                'value_b64': base64.b64encode(bytes(64)).decode('ascii'),
            },
        )
    )


def _receipt(context, checkpoint, work_id, assessment, campaign_state, **extra):
    return encoded(
        dict(
            {
                'schema': 'qualification_campaign_checkpoint_receipt/v1',
                'attempt_id': context.attempt_id,
                'checkpoint': checkpoint,
                'work_id': work_id,
                'campaign_id': 'c1',
                'assessment_sha256': sha256(assessment),
                'cutoff_sha256': '1' * 64,
                'decision': 'CONTINUE',
                'campaign_state': campaign_state,
                'signing_at_utc': '2026-09-22T02:00:00Z',
                'committed_at_utc': '2026-09-22T02:00:01Z',
                'intent_sha256': '2' * 64,
            },
            **extra,
        )
    )


def _family(context, *, checkpoint, work_id, plan_bytes, payload_bytes, campaign_state,
            revision, predecessor=None, predecessor_members=()):
    """The capture family G5 reads for one checkpoint, over real worker bytes."""
    from c1_rail.qualification.journal_snapshot import encode_campaign_checkpoint_snapshot

    release = json.loads(context.installed_release)
    observations = json.loads(payload_bytes)['observations']
    runtime_digest = sha256(encoded(release['runtime_manifests']['worker']))
    times = {
        'authorized_at_utc': '2026-09-22T00:59:59Z',
        'started_utc': '2026-09-22T01:00:00Z',
        'completed_utc': '2026-09-22T01:00:01Z',
    }
    scope = {'campaign_scope_id': 'fpq-c', 'work_scope_id': 'fpq-w', 'payload_slice': 'fpq-p'}
    exit_facts = {'exit_code': 0, 'oom_killed': False}
    result = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_result/v1',
            'attempt_id': context.attempt_id,
            'checkpoint': checkpoint,
            'work_id': work_id,
            'campaign_id': 'c1',
            'plan_sha256': sha256(plan_bytes),
            'plan_byte_length': len(plan_bytes),
            'payload_sha256': sha256(payload_bytes),
            'payload_byte_length': len(payload_bytes),
            'worker_execution_id': work_id,
            'container_id': '9' * 64,
            'worker_image_digest': release['worker_image_digest'],
            'runtime_manifest_sha256': runtime_digest,
            'capture': dict(exit_facts, **times, **scope),
            'limits': {
                'cpu_ns': 120_000_000_000,
                'wall_ns': 300_000_000_000,
                'memory_bytes': 1000000000,
                'orchestration_cpu_ns': 20_000_000_000,
            },
            'observations': dict(exit_facts, **observations),
            'created_utc': '2026-09-22T01:00:02Z',
        }
    )
    attestation = encoded(
        {
            'schema': 'qualification_campaign_checkpoint_attestation/v1',
            'payload': {
                'schema': 'qualification_campaign_checkpoint_attestation_payload/v1',
                'scope': 'ATTEST_CAMPAIGN_CHECKPOINT',
                'attempt_id': context.attempt_id,
                'checkpoint': checkpoint,
                'work_id': work_id,
                'result_sha256': sha256(result),
                'payload_sha256': sha256(payload_bytes),
                'payload_byte_length': len(payload_bytes),
                'plan_sha256': sha256(plan_bytes),
                'execution_release_sha256': sha256(context.installed_release),
                'profile_sha256': release['profile_sha256'],
                'service_id': release['service_id'],
                'worker_image_digest': release['worker_image_digest'],
                'runtime_manifest_sha256': runtime_digest,
                'container_id': '9' * 64,
                'capture': dict(exit_facts, **scope),
                'observations': dict(exit_facts, **observations),
                **times,
                'campaign_revision': revision,
            },
            'signature': {'algorithm': 'Ed25519', 'key_id': 'fixture', 'value_b64': 'AA=='},
        }
    )
    members = [('plan', plan_bytes), ('result', result), ('payload', payload_bytes),
               ('attestation', attestation), ('retained_bundle_index', b'index')]
    members.extend(predecessor_members)
    snapshot = encode_campaign_checkpoint_snapshot(
        attempt_id=context.attempt_id,
        checkpoint=checkpoint,
        contract_sha256=context.contract.contract_sha256,
        trust_domain_sha256=context.contract.trust_domain_sha256,
        policy_sha256=context.policy.sha256,
        validity='VALID',
        campaign_revision=revision,
        authority_head='a' * 64,
        event_head='b' * 64,
        campaign_state=campaign_state,
        works=[
            {'work_id': 'admission', 'phase': 'ADMISSION', 'state': 'COMPLETED', 'settled': True},
            {'work_id': work_id, 'phase': checkpoint, 'state': 'COMPLETED', 'settled': True},
        ],
        capture={
            'work_id': work_id,
            'result_sha256': sha256(result),
            'payload_sha256': sha256(payload_bytes),
            'attestation_sha256': sha256(attestation),
        },
        intent={'work_id': work_id + '-g5', 'candidate_sha256': None},
        members=[
            {'role': name, 'sha256': sha256(raw), 'byte_length': len(raw)} for name, raw in members
        ],
        predecessor=predecessor,
    )
    return {'attestation': attestation, 'snapshot': snapshot}


def _g5_chain(tmp_path, monkeypatch):
    """N1 -> joint N2 -> PART_A on one /v7 bundle; returns the PART_A inputs
    and an ``assess(payload_bytes)`` that reconstructs through G5's builder."""
    from test_contract import NOW
    from test_worker import _stage_bundle, stage_input
    from c1_rail.qualification.checkpoint_plan import derive_checkpoint_plan
    from c1_rail.qualification.evidence import build_checkpoint_evidence, derive_part_a_source_calendar
    from c1_rail.qualification.execution.plan import derive_campaign_plan_from_context
    from c1_rail.qualification.source_admission import admit_source

    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    monkeypatch.setattr(worker, 'utc_now', lambda: NOW)
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)

    def mount(name):
        root = tmp_path / name
        root.mkdir()
        context = stage_input(root, case)
        _stage_bundle(case, root)
        return root, context

    n1, context = mount('n1')
    limit = context.profile.output_byte_limit
    common = dict(contract=context.contract, policy=context.policy,
                  installed_release_bytes=context.installed_release)
    n1_plan = (n1 / 'plan.json').read_bytes()
    n1_payload = decode_frame(worker.run_worker(n1, execution_id='n1work'), limit=limit)
    family = _family(context, checkpoint='N1', work_id='n1work', plan_bytes=n1_plan,
                     payload_bytes=n1_payload, campaign_state='BOUND', revision=3)
    n1_assessment = _signed(build_checkpoint_evidence(
        worker_result_bytes=n1_payload, plan_bytes=n1_plan, checkpoint='N1',
        checkpoint_attestation_bytes=family['attestation'],
        checkpoint_snapshot_bytes=family['snapshot'], **common).envelope_bytes)
    n1_receipt = _receipt(context, 'N1', 'n1g5', n1_assessment, 'N2_READY')
    campaign = derive_campaign_plan_from_context(context)

    n2, _ = mount('n2')
    (n2 / 'predecessor-receipt.json').write_bytes(n1_receipt)
    n2_plan = derive_checkpoint_plan(campaign, 'N2', n1_receipt)
    (n2 / 'plan.json').write_bytes(n2_plan)
    n2_payload = decode_frame(
        worker.run_worker(n2, execution_id='n2work', checkpoint='N2'), limit=limit)
    n1_family = dict(predecessor_receipt_bytes=n1_receipt, predecessor_assessment_bytes=n1_assessment,
                     predecessor_plan_bytes=n1_plan, predecessor_payload_bytes=n1_payload)
    family = _family(
        context, checkpoint='N2', work_id='n2work', plan_bytes=n2_plan, payload_bytes=n2_payload,
        campaign_state='N2_READY', revision=5,
        predecessor={'checkpoint': 'N1', 'assessment_sha256': sha256(n1_assessment),
                     'receipt_sha256': sha256(n1_receipt)},
        predecessor_members=[('predecessor_receipt', n1_receipt), ('predecessor_assessment', n1_assessment),
                             ('predecessor_plan', n1_plan), ('predecessor_payload', n1_payload)])
    n2_core = build_checkpoint_evidence(
        worker_result_bytes=n2_payload, plan_bytes=n2_plan, checkpoint='N2',
        checkpoint_attestation_bytes=family['attestation'],
        checkpoint_snapshot_bytes=family['snapshot'], **common, **n1_family).envelope_bytes
    n2_assessment = _signed(n2_core)
    n2_receipt = _receipt(context, 'N2', 'n2g5', n2_assessment, 'PART_A_READY',
                          predecessor_receipt_sha256=sha256(n1_receipt),
                          stage_decisions=json.loads(n2_core)['stage_decisions'])

    pa, _ = mount('pa')
    for name, raw in (('receipt', n2_receipt), ('assessment', n2_assessment), ('payload', n2_payload)):
        (pa / ('predecessor-' + name + '.json')).write_bytes(raw)
    pa_plan = derive_checkpoint_plan(campaign, 'PART_A', n2_receipt)
    (pa / 'plan.json').write_bytes(pa_plan)
    out = tmp_path / 'out'
    out.mkdir()
    pa_payload = decode_frame(
        worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=out), limit=limit)
    # ``source`` is the loader-built oracle for ``_rederived_sessions``; G5's
    # builder consumes only the loader-free calendar derivation.
    source = admit_source(context.contract, artifact_root=context.bundle_dir, policy=context.policy).source
    calendar = derive_part_a_source_calendar(context.contract, context.retained_bytes)
    n2_family = dict(predecessor_receipt_bytes=n2_receipt, predecessor_assessment_bytes=n2_assessment,
                     predecessor_plan_bytes=n2_plan, predecessor_payload_bytes=n2_payload,
                     n1_plan_bytes=n1_plan, n1_payload_bytes=n1_payload, source=calendar)

    def assess(payload_bytes, builder=None, **overrides):
        family = _family(
            context, checkpoint='PART_A', work_id='pawork', plan_bytes=pa_plan,
            payload_bytes=payload_bytes, campaign_state='PART_A_READY', revision=7,
            predecessor={'checkpoint': 'N2', 'assessment_sha256': sha256(n2_assessment),
                         'receipt_sha256': sha256(n2_receipt)},
            predecessor_members=[('predecessor_receipt', n2_receipt), ('predecessor_assessment', n2_assessment),
                                 ('predecessor_plan', n2_plan), ('predecessor_payload', n2_payload)])
        arguments = dict(worker_result_bytes=payload_bytes, plan_bytes=pa_plan,
                         checkpoint_attestation_bytes=family['attestation'],
                         checkpoint_snapshot_bytes=family['snapshot'], **common, **n2_family)
        arguments.update(overrides)
        if builder is None:
            return build_checkpoint_evidence(checkpoint='PART_A', **arguments)
        accepted = inspect.signature(builder).parameters
        return builder(**{name: value for name, value in arguments.items() if name in accepted})

    return SimpleNamespace(context=context, plan=pa_plan, payload=pa_payload, source=source,
                           assess=assess, n2_payload=n2_payload)


def _remint(document, plan_bytes):
    """Recompute every dependent digest and the inventory after a mutation, so
    that only an independent G5 check can refuse the document."""
    from c1_rail.qualification.execution.evidence import CapturedPartAPanel, part_a_path_inventory
    from c1_rail.qualification.model import PathOutcome

    part = document['part_a']
    panels = [
        CapturedPartAPanel(
            row['index'],
            tuple(row['source_session_ids']),
            tuple(
                PathOutcome(o['status'], o['sessions_to_pass'], o['failure_reason'],
                            tuple(tuple(pair) for pair in o['diagnostics']))
                for o in row['outcomes']
            ),
        )
        for row in part['panels']
    ]
    part['initial_prefix_sha256'] = sha256(compute.part_a_panel_bytes(panels[:part['initial_panels']]))
    part['final_sha256'] = sha256(compute.part_a_panel_bytes(panels))
    document['path_inventory'] = part_a_path_inventory(json.loads(plan_bytes), part['panels'])
    return encoded(document)


def _rederived_sessions(chain, index):
    """The engine's own outer-panel draw for panel ``index`` (the P1 check)."""
    from random import Random

    from c1_rail.qualification.regime import domain_seed, sample_outer_panel

    contract, source = chain.context.contract, chain.source
    seed = domain_seed(root=contract.replay.root_rng_namespace, stage='n2', population='FULL',
                       panel_index=index, path_index=0, purpose='outer',
                       synthetic=contract.trust_domain.permits_synthetic)
    return [s.session_id for s in sample_outer_panel(
        source.sessions, Random(seed), months=contract.replay.outer_months, adjacent=source.adjacent,
        covered_until=source.covered_until, tail_covered=source.tail_covered)]


@pytest.fixture(scope='module')
def g5_chain(tmp_path_factory):
    monkeypatch = pytest.MonkeyPatch()
    try:
        yield _g5_chain(tmp_path_factory.mktemp('g5-part-a'), monkeypatch)
    finally:
        monkeypatch.undo()


def test_g5_part_a_reconstructs_continue_from_a_genuine_chain(g5_chain):
    from c1_rail.qualification.evidence import (
        compare_checkpoint_evidence, parse_checkpoint_assessment)

    evidence = g5_chain.assess(g5_chain.payload)
    core = json.loads(evidence.envelope_bytes)
    assert core['checkpoint'] == 'PART_A' and core['decision'] == 'CONTINUE'
    assert [row['stage'] for row in core['stages']] == ['LEGALITY', 'N1', 'N2', 'PART_B', 'PART_A']
    assert core['predecessor']['checkpoint'] == 'N2' and 'stage_decisions' not in core
    part = core['part_a']
    assert set(part) == {'initial_panels', 'final_panels', 'expansion_required', 'initial_prefix_sha256',
                         'final_sha256', 'tolerance_comparison', 'floor_comparison',
                         'full_sanity_comparison'}
    assert (part['initial_panels'], part['final_panels'], part['expansion_required']) == (2, 2, False)
    assert part['tolerance_comparison']['within'] is False
    assert part['floor_comparison']['at_or_above'] is True
    assert part['full_sanity_comparison']['at_or_below'] is True
    assert Decimal(part['full_sanity_comparison']['full_pass_rate']) == 1
    assert core['cutoff'] == {'checkpoint': 'PART_A', 'stage_thresholds': {}}
    # The worker's captured occurrences are exactly the engine's re-derived draws.
    doc = json.loads(g5_chain.payload)
    for row in doc['part_a']['panels']:
        assert row['source_session_ids'] == _rederived_sessions(g5_chain, row['index'])
    compare_checkpoint_evidence(evidence, expected=evidence)
    parsed = parse_checkpoint_assessment(_signed(evidence.envelope_bytes),
                                         attempt_id=g5_chain.context.attempt_id)
    assert parsed['decision'] == 'CONTINUE'


def test_g5_part_a_genuine_all_failure_is_a_failure_decision(g5_chain):
    """A below-floor run through the builder: every path FAILURE, the reported
    statistics re-derived to the exact zeros, every digest re-minted."""
    doc = json.loads(g5_chain.payload)
    for row in doc['part_a']['panels']:
        for outcome in row['outcomes']:
            outcome.update(status='FAILURE', sessions_to_pass=None, failure_reason='synthetic')
    doc['part_a'].update(initial_p5=0.0, final_p5=0.0)
    core = json.loads(g5_chain.assess(_remint(doc, g5_chain.plan)).envelope_bytes)
    assert core['decision'] == 'FAILURE' and core['stages'][4]['status'] == 'FAIL'
    assert core['part_a']['floor_comparison'] == {'final_p5': '0', 'floor': '0.95', 'at_or_above': False}


def _nonexistent_session(doc, chain):
    doc['part_a']['panels'][0]['source_session_ids'][0] = 'NONEXISTENT-SESSION'


def _real_but_wrong_occurrence(doc, chain):
    ids = doc['part_a']['panels'][0]['source_session_ids']
    other = next(session for session in ids[1:] if session != ids[0])
    ids[0] = other


def _substituted_prefix(doc, chain):
    ids = doc['part_a']['panels'][0]['source_session_ids']
    assert ids != ids[::-1]
    ids.reverse()


def _reordered_prefix(doc, chain):
    rows = doc['part_a']['panels']
    first, second = rows[0], rows[1]
    assert (first['source_session_ids'], first['outcomes']) != (second['source_session_ids'], second['outcomes'])
    rows[0], rows[1] = dict(second, index=0), dict(first, index=1)


def _initial_p5_overstated(doc, chain):
    doc['part_a']['initial_p5'] += 0.25


def _final_p5_understated(doc, chain):
    doc['part_a']['final_p5'] -= 0.25


def _altered_pilot(doc, chain):
    doc['part_a']['pilot']['seed_input_sha256s'][0] = 'e' * 64


def _mismatched_baseline(doc, chain):
    doc['part_a']['n2_full_baseline']['passes'] -= 1


def _unnecessary_expansion(doc, chain):
    """P-5: a forced-expanded result whose appended panels carry the engine's
    own occurrences, so only the expansion decision can refuse it."""
    part = doc['part_a']
    depth = len(part['panels'][0]['outcomes'])
    for index in range(part['initial_panels'], chain.context.contract.replay.part_a.expanded_panels):
        part['panels'].append({'index': index, 'source_session_ids': _rederived_sessions(chain, index),
                               'outcomes': json.loads(json.dumps(part['panels'][0]['outcomes']))[:depth]})
    part.update(final_panels=len(part['panels']), expansion_required=True)


@pytest.mark.parametrize('mutate,message', [
    (_nonexistent_session, 'altered source occurrences'),
    (_real_but_wrong_occurrence, 'altered source occurrences'),
    (_substituted_prefix, 'altered source occurrences'),
    (_reordered_prefix, 'altered source occurrences'),
    (_initial_p5_overstated, 'part a reported statistic differs'),
    (_final_p5_understated, 'part a reported statistic differs'),
    (_altered_pilot, 'missing pilot identity'),
    (_mismatched_baseline, 'mismatched N2 FULL baseline'),
    (_unnecessary_expansion, 'unnecessary expansion'),
])
def test_g5_part_a_refuses_reminted_mutations(g5_chain, mutate, message):
    """Every dependent digest and the inventory are recomputed after the
    mutation (``_remint``); only G5's independent check can refuse it."""
    doc = json.loads(g5_chain.payload)
    mutate(doc, g5_chain)
    with pytest.raises(ValueError, match=message):
        g5_chain.assess(_remint(doc, g5_chain.plan))


def test_g5_part_a_requires_the_retained_source(g5_chain):
    from c1_rail.qualification.evidence import build_part_a_checkpoint_evidence

    with pytest.raises(ValueError, match='retained source required'):
        g5_chain.assess(g5_chain.payload, builder=build_part_a_checkpoint_evidence, source=None)
    # The loader-built source is not the builder's input either: G5's closure
    # never contains the source loader (test_runtime).
    with pytest.raises(ValueError, match='retained source required'):
        g5_chain.assess(g5_chain.payload, builder=build_part_a_checkpoint_evidence,
                        source=g5_chain.source)


def test_g5_loader_free_calendar_matches_the_loader_built_source(g5_chain):
    """P1 parity: the session metadata G5 derives from the frozen FULL
    population and the retained calendar bytes equals what the admitted
    ``ProductionSource`` hands ``sample_outer_panel``, field by field."""
    from c1_rail.qualification.evidence import derive_part_a_source_calendar

    context, source = g5_chain.context, g5_chain.source
    calendar = derive_part_a_source_calendar(context.contract, context.retained_bytes)
    assert [(s.session_id, s.source_session_date) for s in calendar.sessions] == \
        [(s.session_id, s.source_session_date) for s in source.sessions]
    assert calendar.adjacent == source.adjacent
    assert calendar.covered_until == source.covered_until
    assert calendar.tail_covered is source.tail_covered
    assert any(calendar.adjacent) and len(calendar.adjacent) == len(calendar.sessions) - 1


@pytest.mark.parametrize('mutate', [
    lambda retained: {**retained, 'source_calendar': retained['source_calendar'] + b' '},
    lambda retained: {name: raw for name, raw in retained.items() if name != 'source_calendar'},
])
def test_g5_loader_free_calendar_refuses_unbound_calendar_bytes(g5_chain, mutate):
    from c1_rail.qualification.evidence import derive_part_a_source_calendar

    context = g5_chain.context
    with pytest.raises(ValueError, match='contract-bound retained source calendar required'):
        derive_part_a_source_calendar(context.contract, mutate(dict(context.retained_bytes)))



def test_s4_joint_builder_refuses_a_part_a_plan(g5_chain):
    """Fail-on-base: the S4 joint builder never adjudicates PART_A custody --
    it refuses the PART_A worker document at its closed key set (no
    ``populations``), before any schema or plan comparison."""
    from c1_rail.qualification.evidence import build_joint_checkpoint_evidence

    with pytest.raises(ValueError, match='worker result fields differ'):
        g5_chain.assess(g5_chain.payload, builder=build_joint_checkpoint_evidence)


@pytest.mark.parametrize('key', ['measurement_override', 'within_pp'])
@pytest.mark.parametrize('place', ['assessment', 'part_a', 'tolerance_comparison', 'cutoff'])
def test_p4_part_a_assessment_and_cutoff_refuse_seam_keys(g5_chain, key, place):
    from c1_rail.qualification.evidence import parse_checkpoint_assessment, parse_checkpoint_cutoff

    attempt = g5_chain.context.attempt_id
    core = json.loads(g5_chain.assess(g5_chain.payload).envelope_bytes)
    cutoff = {'schema': 'qualification_campaign_cutoff_receipt/v1', 'attempt_id': attempt,
              'checkpoint': 'PART_A', 'assessment_sha256': sha256(encoded(core)), 'decision': 'CONTINUE',
              'stage_thresholds': {}, 'predecessor_receipt_sha256': core['predecessor']['receipt_sha256'],
              'created_utc': '2026-09-22T03:00:00Z'}
    parse_checkpoint_assessment(_signed(encoded(core)), attempt_id=attempt)
    parse_checkpoint_cutoff(encoded(cutoff), attempt_id=attempt)
    if place == 'cutoff':
        cutoff[key] = 1.0
        with pytest.raises(ValueError):
            parse_checkpoint_cutoff(encoded(cutoff), attempt_id=attempt)
        return
    target = core if place == 'assessment' else core['part_a'] if place == 'part_a' else (
        core['part_a']['tolerance_comparison'])
    target[key] = 1.0
    with pytest.raises(ValueError):
        parse_checkpoint_assessment(_signed(encoded(core)), attempt_id=attempt)


# ---- P1(b) / P2 at the worker-result parser -------------------------------------


def test_part_a_worker_result_parser_checks_occurrences_and_statistics(tmp_path, monkeypatch):
    """The parser's own independent checks: a source occurrence outside the
    contract's admitted FULL population, and reported p5 floats that differ
    from the exact re-derived rank -- each with every dependent digest and
    the inventory re-minted so no hash check can catch it first."""
    worker = importlib.import_module('c1_rail.qualification.execution.worker')
    evidence = importlib.import_module('c1_rail.qualification.execution.evidence')
    case = build_bundle(tmp_path / 'bundle', capability='FULL_E1', part_a=True)
    context, pa, out, *_ = part_a_stage_input(tmp_path, case, monkeypatch)
    frame = worker.run_worker(pa, execution_id='pawork', checkpoint='PART_A', output_dir=out)
    doc = json.loads(decode_frame(frame, limit=context.profile.output_byte_limit))
    plan = (pa / 'plan.json').read_bytes()
    assert all(session in set(context.contract.populations['FULL'])
               for row in doc['part_a']['panels'] for session in row['source_session_ids'])
    evidence.parse_worker_result(_remint(json.loads(json.dumps(doc)), plan), context=context,
                                 execution_id='pawork', plan_bytes=plan)

    def nonexistent_session(document):
        document['part_a']['panels'][0]['source_session_ids'][0] = 'NONEXISTENT-SESSION'

    def initial_p5_overstated(document):
        document['part_a']['initial_p5'] = 456.0

    def final_p5_understated(document):
        document['part_a']['final_p5'] = -123.0

    for mutate, message in (
        (nonexistent_session, 'outside the admitted FULL population'),
        (initial_p5_overstated, 'part a reported statistic differs'),
        (final_p5_understated, 'part a reported statistic differs'),
    ):
        mutated = json.loads(json.dumps(doc))
        mutate(mutated)
        with pytest.raises(ValueError, match=message):
            evidence.parse_worker_result(_remint(mutated, plan), context=context,
                                         execution_id='pawork', plan_bytes=plan)
