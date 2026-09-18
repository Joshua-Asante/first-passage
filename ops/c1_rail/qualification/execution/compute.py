"""N1 replay only. No journal, signing or launch authority is imported here."""
from mc.simulation import EvaluationState

from ..provider import _ReplayProvider
from ..runner import SyntheticStageRequest, _run_stage


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


def run_n1_compute(contract, source, budget):
    """Retain source proofs, original probe, sampling and final aggregation checks."""
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
        return _run_stage(stage_request(contract, 'n1', budget.remaining_wall_seconds()), provider,
            initial_state=initial_state(contract), synthetic=contract.trust_domain.permits_synthetic)
    finally:
        budget.check_and_measure()
