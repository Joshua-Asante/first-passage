"""Checkpoint replay only. No journal, signing or launch authority is imported here."""
from dataclasses import dataclass, replace

from mc.simulation import EvaluationState

from ..contract import canonical_json_bytes
from ..part_a import _run_part_a
from ..production import _part_a_request
from ..provider import _ReplayProvider
from ..runner import SyntheticStageRequest, _run_stage
from .evidence import outcome_record


def initial_state(contract):
    state = contract.initial_state
    return EvaluationState(float(state.original_basis), float(state.current_equity),
        float(state.historical_eod_peak), state.prior_trade_days, float(state.prior_max_day_profit))


def stage_request(contract, stage, budget_seconds):
    if stage not in ('n1', 'n2'):
        raise ValueError('E1 executor only permits n1/n2; n3 requires its own authorization')
    specs = contract.stage_specs
    full = specs[stage.upper()].exact_depth
    half = full if stage == 'n1' else specs['PART_B'].exact_depth
    return SyntheticStageRequest(stage, (('FULL', full), ('H1', half), ('H2', half)),
        contract.replay.horizon_sessions, contract.replay.root_rng_namespace, budget_seconds)


def _run_checkpoint_compute(stage, contract, source, budget):
    from ..production_source import ProductionSource
    if type(source) is not ProductionSource:
        raise TypeError('factory-built source required')
    source.verify_for(contract)

    def replay(path):
        budget.check_and_measure()
        try:
            return source.replay(path)
        finally:
            budget.check_and_measure()

    try:
        provider = _ReplayProvider(source.sessions, source.adjacent,
            block_sessions=contract.replay.inner_block_sessions,
            path_start_date=source.path_start_date, replay=replay)
        return _run_stage(stage_request(contract, stage, budget.remaining_wall_seconds()), provider,
            initial_state=initial_state(contract), synthetic=contract.trust_domain.permits_synthetic)
    finally:
        budget.check_and_measure()


def run_n1_compute(contract, source, budget):
    """Retain source proofs, original probe, sampling and final aggregation checks."""
    return _run_checkpoint_compute('n1', contract, source, budget)


def run_n2_compute(contract, source, budget):
    """The joint batch beside run_n1_compute: FULL at the frozen N2 depth and
    H1/H2 at the frozen PART_B depth in one stage run -- one probe, one sample."""
    return _run_checkpoint_compute('n2', contract, source, budget)


# ---- S5 Part A adapter (packet S5-D1/S5-D2 and section 1a) -------------------
#
# ``run_part_a_compute`` adapts the engine Part A loop (part_a._run_part_a)
# exactly as the gated route does (production.ProductionExecutor.run_part_a):
# same request mapping, same provider/proof/replay shape, one computation that
# returns the S5-D1 initial-prefix artifact bytes and the final artifact bytes.
# The measurement override is the section 1a TEST_ONLY seam (SR-1/SR-2); the
# route never passes it.


PART_A_MEASUREMENT_LABEL = 'TEST_ONLY_MEASUREMENT_FORCED_EXPANSION'

# The closed PathOutcome status set (model.PathOutcome.__post_init__).
PART_A_OUTCOME_STATUSES = ('PASS', 'FAILURE', 'UNRESOLVED')


@dataclass(frozen=True)
class PartAMeasurementOverride:
    """Section 1a Stage 1c measurement seam; the closed value is 1.0 only."""
    within_pp: float = 1.0

    def __post_init__(self):
        if type(self.within_pp) is not float or self.within_pp != 1.0:
            raise ValueError('PartAMeasurementOverride requires exactly within_pp=1.0')

    @property
    def label(self):
        return PART_A_MEASUREMENT_LABEL


@dataclass(frozen=True)
class PartACompute:
    """One Part A computation with its S5-D1 prefix and final artifact bytes."""
    result: object
    initial_panel_bytes: bytes
    final_panel_bytes: bytes
    initial_panels: int
    final_panels: int
    expansion_required: bool
    full_pass_rate: float
    measurement_forced: bool


def part_a_panel_bytes(panels):
    """S5-D1 artifact encoding: one canonical JSON line per panel, in order."""
    return b''.join(canonical_json_bytes({
        'index': panel.index,
        'source_session_ids': list(panel.source_session_ids),
        'outcomes': [outcome_record(outcome) for outcome in panel.outcomes],
    }) + b'\n' for panel in panels)


def _part_a_full_pass_rate(n2_full_outcomes):
    """S5-D2: derive the FULL baseline from the captured outcome statuses."""
    if type(n2_full_outcomes) is not tuple or not n2_full_outcomes:
        raise ValueError('nonempty tuple of captured N2 FULL outcome statuses required')
    if any(type(status) is not str or status not in PART_A_OUTCOME_STATUSES
           for status in n2_full_outcomes):
        raise ValueError('N2 FULL outcomes must use the closed PathOutcome status set')
    return sum(status == 'PASS' for status in n2_full_outcomes) / len(n2_full_outcomes)


def run_part_a_compute(contract, source, budget, *, n2_full_outcomes,
                       measurement_override=None, on_initial_prefix=None):
    """One engine Part A computation behind the checkpoint compute boundary.

    ``n2_full_outcomes`` is the staged N2 FULL capture (S5-D2) as outcome
    statuses; the pass rate is derived here, never passed as a number. The
    gate (SR-2) runs first: before source verification, before any compute
    and before ``on_initial_prefix`` is called. The prefix handed to
    ``on_initial_prefix`` and the returned ``initial_panel_bytes`` are the
    same bytes object; a raise from the hook propagates (no expansion, no
    result).
    """
    if measurement_override is not None and (type(measurement_override) is not PartAMeasurementOverride
            or contract.trust_domain.authority_class != 'TEST_ONLY'
            or contract.trust_domain.permits_synthetic is not True):
        raise ValueError('TEST_ONLY synthetic contract required for the Part A measurement override')
    full_pass_rate = _part_a_full_pass_rate(n2_full_outcomes)
    from ..production_source import ProductionSource
    if type(source) is not ProductionSource:
        raise TypeError('factory-built source required')
    source.verify_for(contract)

    def proof(panel):
        budget.check_and_measure()
        try:
            return source.proof(panel)
        finally:
            budget.check_and_measure()

    def replay(path):
        budget.check_and_measure()
        try:
            return source.replay(path)
        finally:
            budget.check_and_measure()

    custody = []
    def prefix_to_custody(panels):
        # S5-D1: encode once; custody and the returned prefix are one object.
        raw = part_a_panel_bytes(panels)
        custody.append(raw)
        if on_initial_prefix is not None:
            on_initial_prefix(raw)

    try:
        request = _part_a_request(contract, source.path_start_date, budget.remaining_wall_seconds())
        if measurement_override is not None:
            request = replace(request, within_pp=measurement_override.within_pp)
        result = _run_part_a(request, source.sessions, adjacent=source.adjacent,
            covered_until=source.covered_until, tail_covered=source.tail_covered,
            proof_provider=proof, replay_provider=replay,
            initial_state=initial_state(contract), full_pass_rate=full_pass_rate,
            synthetic=contract.trust_domain.permits_synthetic,
            on_initial_prefix=prefix_to_custody)
    finally:
        budget.check_and_measure()
    if not custody:
        raise ValueError('Part A initial prefix custody never ran')
    return PartACompute(result=result, initial_panel_bytes=custody[0],
        final_panel_bytes=part_a_panel_bytes(result.panels),
        initial_panels=request.initial_panels, final_panels=len(result.panels),
        expansion_required=result.expanded, full_pass_rate=full_pass_rate,
        measurement_forced=measurement_override is not None)
