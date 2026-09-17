"""Single-process replay/kernel runner. Synthetic results cannot become seals."""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from time import perf_counter

from mc.preflight import firm_kwargs
from mc.simulation import EvaluationState, simulate_path
from c1_rail.book_policy import candidate_book_protection_policy
from .model import PathOutcome, ReplayResult, positive_int
from .regime import domain_seed
from .sessions import WeekClock, session_arrays


class NeedsContext(RuntimeError):
    """A prerequisite/budget is absent; never an extra sample or approximation."""


def evaluate_replay(result: ReplayResult, *, initial_state: EvaluationState, kernel=simulate_path):
    if type(initial_state) is not EvaluationState:
        raise TypeError('explicit EvaluationState required')
    if not isinstance(result, ReplayResult):
        raise TypeError('replay result required')
    pnl, low = session_arrays(result.sessions)
    horizon = len(result.sessions)
    rules = firm_kwargs('Tradeify_Select_100K', inactivity_off=True, consistency=.40, account=initial_state.original_basis)
    # The core inactivity-OFF sentinel is bounded by its default horizon. Keep
    # this barrier off even for an explicitly configured longer path.
    rules['inactivity_limit'] = max(rules['inactivity_limit'], horizon + 1)
    status, day, max_dd, _ = kernel(pnl, candidate_book_protection_policy().trigger, 1.0, horizon,
                                  intraday_low=low, initial_state=initial_state, **rules)
    deadline = next((i+1 for i, row in enumerate(result.sessions) if not row.flat_before_deadline), None)
    diagnostic = (('kernel_outcome', status), ('max_drawdown', repr(max_dd)),
                  ('idle_weeks', str(WeekClock().count_idle(result.sessions))))
    if deadline is not None and not (status == 'pass' and day < deadline):
        return PathOutcome('FAILURE', None, 'own_flat_deadline', diagnostic)
    if status == 'pass':
        return PathOutcome('PASS', int(day), None, diagnostic)
    if status == 'horizon_cap':
        return PathOutcome('UNRESOLVED', None, status, diagnostic)
    if status not in ('bust_daily', 'bust_static', 'bust_trailing', 'bust_inactivity'):
        raise ValueError('unknown kernel result')
    return PathOutcome('FAILURE', None, status, diagnostic)


@dataclass(frozen=True)
class SyntheticStageRequest:
    stage: str
    depths: tuple[tuple[str, int], ...]
    horizon_sessions: int
    root_rng_namespace: str
    budget_seconds: float

    def __post_init__(self):
        if self.stage not in ('n1','n2','n3'):
            raise ValueError('explicit stage required')
        if type(self.depths) is not tuple or len(self.depths)!=3 or {k for k,_ in self.depths}!={'FULL','H1','H2'}:
            raise ValueError('independent FULL/H1/H2 depths required')
        for _, depth in self.depths:
            positive_int(depth,'population depth')
        positive_int(self.horizon_sessions,'horizon_sessions')
        if not self.root_rng_namespace or not isfinite(self.budget_seconds) or self.budget_seconds<=0:
            raise ValueError('explicit RNG domain and positive finite budget required')


@dataclass(frozen=True)
class StageRun:
    stage: str
    populations: tuple[tuple[str, tuple[PathOutcome, ...]], ...]
    probe_seconds: float
    elapsed_seconds: float
    synthetic: bool = True


def run_synthetic_stage(request, replay_provider, *, initial_state, timer=perf_counter):
    """Explicit test-only surface. Provider constructs a fresh continuous replay.

    The probe has its own RNG domain and is not a designated qualification
    trial. No actual source authority can be inferred from this function or its
    output. Production execution is separately gated by the attempt controller.
    """
    if type(request) is not SyntheticStageRequest:
        raise TypeError('explicit synthetic request required')
    return _run_stage(request,replay_provider,initial_state=initial_state,timer=timer,synthetic=True)


def _run_stage(request, replay_provider, *, initial_state, synthetic, timer=perf_counter):
    """Shared mechanics; production authority is checked by ProductionExecutor."""
    if type(synthetic) is not bool:
        raise TypeError('explicit evidence domain required')
    start = timer()
    def run(stage,population,index):
        from .replay import ReplayDeadlineFailure
        seed=domain_seed(root=request.root_rng_namespace,stage=stage,population=population,
                         panel_index=None,path_index=index,synthetic=synthetic)
        try:
            replay=replay_provider(stage=stage,population=population,path_index=index,seed=seed,
                                   horizon_sessions=request.horizon_sessions)
        except ReplayDeadlineFailure as exc:
            if stage == 'probe':
                raise NeedsContext('budget probe must complete a full path') from exc
            return evaluate_replay(exc.result, initial_state=initial_state)
        if len(replay.sessions)!=request.horizon_sessions:
            raise ValueError('provider did not return complete horizon')
        return evaluate_replay(replay,initial_state=initial_state)
    run('probe','FULL',0)
    probe=timer()-start
    total=sum(depth for _,depth in request.depths)
    if probe<0 or not isfinite(probe) or total*probe>request.budget_seconds:
        raise NeedsContext('measured full-path runtime exceeds frozen budget')
    populations=[]
    for population,depth in request.depths:
        outcomes=[]
        for index in range(depth):
            if timer()-start>request.budget_seconds:
                raise NeedsContext('runtime budget exhausted; no continuation draws authorized')
            outcomes.append(run(request.stage,population,index))
        populations.append((population,tuple(outcomes)))
    elapsed=timer()-start
    if elapsed>request.budget_seconds:
        raise NeedsContext('completed batch exceeded runtime budget')
    return StageRun(request.stage,tuple(populations),probe,elapsed,synthetic=synthetic)
