"""S5 Part A engine-adapter boundary tests (packet S5-D1/S5-D2 and section 1a).

Pure boundary cases run ``part_a._run_part_a`` directly with synthetic
providers and exact outcome vectors; adapter cases run
``compute.run_part_a_compute`` on the real TEST_ONLY composition fixture the
way ``test_compute.py`` builds it. The packet's third required assertion
(``part_a_worker_launch_count == 1``) needs the worker route and lives with
it, not here.
"""
from dataclasses import FrozenInstanceError, replace
from datetime import date
from decimal import Decimal, localcontext
from math import ceil
from types import SimpleNamespace

import pytest

from composition_fixture import build_verified_composition
from test_part_a import EDGE, STATE, request, source
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
