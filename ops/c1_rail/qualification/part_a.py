"""Part A mechanics with separate synthetic and gated production RNG domains.

No frozen contract, source admission, result authority or production seal can be
created by this module. Each callback must create a fresh continuous replay.
"""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from math import ceil, floor, isfinite
from random import Random
from time import perf_counter

from .model import PathOutcome, ReplayResult, positive_int
from .paths import PathAssembler
from .regime import domain_seed, rebuild_inner_blocks, sample_outer_panel
from .runner import NeedsContext, evaluate_replay
from .replay import ReplayDeadlineFailure


@dataclass(frozen=True)
class SyntheticPartARequest:
    stage: str
    outer_months: int
    inner_block_sessions: int
    depth: int
    horizon_sessions: int
    initial_panels: int
    max_panels: int
    percentile: float
    percentile_method: str
    floor: float
    within_pp: float
    root_rng_namespace: str
    budget_seconds: float
    path_start_date: date

    def __post_init__(self):
        if self.stage != 'n2':
            raise ValueError('Part A is n2 only')
        for name in ('outer_months', 'inner_block_sessions', 'depth', 'horizon_sessions', 'initial_panels', 'max_panels'):
            positive_int(getattr(self, name), name)
        if self.max_panels < self.initial_panels or self.horizon_sessions % self.inner_block_sessions:
            raise ValueError('whole inner blocks and nondecreasing panel expansion required')
        if self.percentile_method not in ('linear', 'nearest', 'nearest_rank'):
            raise ValueError('explicit supported percentile method required')
        for name in ('percentile', 'floor', 'within_pp'):
            value = getattr(self, name)
            if isinstance(value, bool) or not isfinite(value) or not 0 <= value <= 1:
                raise ValueError('probability/fraction fields must lie in [0,1]')
        if not self.root_rng_namespace or not isfinite(self.budget_seconds) or self.budget_seconds <= 0:
            raise ValueError('explicit namespace and finite positive budget required')
        PathAssembler(self.path_start_date)


@dataclass(frozen=True)
class SyntheticPanelResult:
    index: int
    source_session_ids: tuple[str, ...]
    outcomes: tuple[PathOutcome, ...]

    @property
    def passes(self):
        return sum(outcome.status == 'PASS' for outcome in self.outcomes)

    @property
    def failures(self):
        return len(self.outcomes) - self.passes

    @property
    def pass_rate(self):
        return self.passes / len(self.outcomes)


@dataclass(frozen=True)
class PartAResult:
    panels: tuple[SyntheticPanelResult, ...]
    initial_p5: float
    final_p5: float
    expanded: bool
    passed: bool
    failure_reason: str | None
    probe_seconds: float
    predicted_seconds: float
    elapsed_seconds: float
    synthetic: bool = True


SyntheticPartAResult = PartAResult


def _percentile(panels, probability, method):
    values = sorted(panel.pass_rate for panel in panels)
    if method == 'nearest_rank':
        # Distinct from NumPy's nearest interpolation: p=.05, N=100
        # selects the fifth sorted observation, not the sixth.
        rank = ceil(Decimal(str(probability)) * len(values))
        return values[max(0, rank - 1)]
    position = (len(values) - 1) * probability
    if method == 'nearest':
        return values[round(position)]
    lower = floor(position)
    upper = min(lower + 1, len(values) - 1)
    return values[lower] + (position-lower) * (values[upper]-values[lower])


def run_synthetic_part_a(request, source_sessions, *, adjacent, covered_until,
                         proof_provider, replay_provider, initial_state,
                         full_pass_rate, tail_covered=False, timer=perf_counter):
    """Run explicit synthetic panel/depth counts and a disjoint budget pilot.

    ``within_pp`` is a probability fraction: .01 means one percentage point.
    ``full_pass_rate`` must come from the same synthetic n2 FULL stage; no extra
    speed or FULL trials are drawn here. ``proof_provider(panel)`` continuously
    replays that exact occurrence order and supplies N+1 ledger edges plus N-1
    adjacency decisions. Proofs from the original panel cannot substitute.
    The prescribed close-call expansion is decided from the initial percentile;
    the FULL sanity check is applied to the final panel inventory before any
    passing result. An initial sanity excess does not override that expansion.
    """
    if type(request) is not SyntheticPartARequest:
        raise TypeError('explicit synthetic Part A request required')
    return _run_part_a(request,source_sessions,adjacent=adjacent,covered_until=covered_until,
        proof_provider=proof_provider,replay_provider=replay_provider,initial_state=initial_state,
        full_pass_rate=full_pass_rate,tail_covered=tail_covered,timer=timer,synthetic=True)


def _run_part_a(request,source_sessions,*,adjacent,covered_until,proof_provider,replay_provider,
                initial_state,full_pass_rate,synthetic,tail_covered=False,timer=perf_counter):
    """Shared mechanics; ProductionExecutor owns all production authority checks."""
    if type(synthetic) is not bool:
        raise TypeError('explicit evidence domain required')
    if type(covered_until) is not date:
        raise ValueError('explicit attested exclusive source coverage end required')
    if isinstance(full_pass_rate, bool) or not isfinite(full_pass_rate) or not 0 <= full_pass_rate <= 1:
        raise ValueError('same-stage FULL pass rate required')
    assembler = PathAssembler(request.path_start_date)
    start = timer()

    def seed(index, path, purpose, pilot=False):
        return domain_seed(root=request.root_rng_namespace, stage='probe' if pilot else 'n2',
                           population='FULL', panel_index=index, path_index=path,
                           purpose='probe' if pilot else purpose, synthetic=synthetic)

    def panel_blocks(index, pilot=False):
        # Pilot outer/inner use different path addresses within the probe domain.
        panel = sample_outer_panel(source_sessions, Random(seed(index, 0, 'outer', pilot)),
                                   months=request.outer_months, adjacent=adjacent,
                                   covered_until=covered_until, tail_covered=tail_covered)
        builder = rebuild_inner_blocks(panel, proof_provider, block_sessions=request.inner_block_sessions)
        candidates = builder.candidates()
        if not candidates:
            raise NeedsContext('no proven whole inner blocks for this alternate panel')
        return panel, candidates

    def path_result(index, path_index, candidates, pilot=False):
        path = assembler.sample(candidates, Random(seed(index, path_index + int(pilot), 'path', pilot)),
                                horizon_sessions=request.horizon_sessions)
        deadline_failure = False
        try:
            replay = replay_provider(path)
        except ReplayDeadlineFailure as exc:
            replay = exc.result
            deadline_failure = True
            if pilot and len(replay.sessions) != request.horizon_sessions:
                raise NeedsContext('partial deadline-failed pilot cannot measure a full-path budget') from exc
        if type(replay) is not ReplayResult or (not deadline_failure and len(replay.sessions) != request.horizon_sessions):
            raise ValueError('provider must return the entire continuous horizon')
        if deadline_failure and (not 0 < len(replay.sessions) <= request.horizon_sessions or
                                 replay.sessions[-1].flat_before_deadline or
                                 any(not row.flat_before_deadline for row in replay.sessions[:-1])):
            raise ValueError('typed deadline failure requires a matching terminal failed session prefix')
        for expected, actual in zip(path, replay.sessions):
            if (actual.occurrence, actual.path_session_date, actual.source_session_id) != (
                    expected.occurrence, expected.path_session_date, expected.source.session_id):
                raise ValueError('replay differs from sampled occurrence path')
        return evaluate_replay(replay, initial_state=initial_state)

    _, pilot_candidates = panel_blocks(0, True)
    rebuilt = timer()
    path_result(0, 0, pilot_candidates, True)
    pilot_end = timer()
    rebuild_seconds, path_seconds = rebuilt-start, pilot_end-rebuilt
    probe_seconds = pilot_end-start
    predicted = probe_seconds + request.max_panels * (rebuild_seconds + request.depth * path_seconds)
    if any(not isfinite(x) or x < 0 for x in (rebuild_seconds, path_seconds, predicted)) or predicted > request.budget_seconds:
        raise NeedsContext('measured synthetic full-path and panel-rebuild budget exceeded')

    def check_budget():
        elapsed = timer()-start
        if not isfinite(elapsed) or elapsed < 0 or elapsed > request.budget_seconds:
            raise NeedsContext('synthetic Part A runtime budget exhausted; no replacement draws')
        return elapsed

    panels = []
    def extend(limit):
        for index in range(len(panels), limit):
            check_budget()
            panel, candidates = panel_blocks(index)
            outcomes = []
            for path_index in range(request.depth):
                check_budget()
                outcomes.append(path_result(index, path_index, candidates))
            check_budget()
            panels.append(SyntheticPanelResult(index, tuple(s.session_id for s in panel), tuple(outcomes)))

    extend(request.initial_panels)
    initial_p5 = _percentile(panels, request.percentile, request.percentile_method)
    close = abs(Decimal(str(initial_p5))-Decimal(str(request.floor))) <= Decimal(str(request.within_pp))
    expanded = close and request.max_panels > request.initial_panels
    if expanded:
        extend(request.max_panels)
    final_p5 = _percentile(panels, request.percentile, request.percentile_method)
    reason = 'p5_above_full' if final_p5 > full_pass_rate else 'below_floor' if final_p5 < request.floor else None
    return PartAResult(tuple(panels), initial_p5, final_p5, expanded, reason is None, reason,
                       probe_seconds, predicted, check_budget(),synthetic=synthetic)
