"""Path-position bracket convention for schedule instants inside an M15 bar.

Ratified 2026-09-23 (revision 2) with build GO 2026-09-24:
docs/briefs/phase3-preparation/2026-09-15/schedule-execution-evidence.md.
The accepted emulator path of a bar is fixed; each run places an intrabar
schedule instant at one vertex of it and supplies that split through the
``schedule_quotes`` seam (the frozen ``ScheduleSplit`` interface), so ``BookReplay._split`` validates it
unchanged. R1 and R2 are complete replays evaluated separately; a path's
outcome is taken only where they agree. The two placements are extreme
vertices, not proven bounds on the true instant.

Engine-layer capability only: no G1 artifact role, production source, stage
runner or adjudication consumes it yet.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from .model import PathOutcome
from .replay import ReplayDeadlineFailure, ReplayNeedsContext, accepted_path
# vertex_split and placement moved verbatim to production_source (T00 step-1b
# Task 2); re-exported here under their public names.
from .production_source import placement, vertex_split  # noqa: F401
from .runner import evaluate_replay

CONVENTION = 'PATH_POSITION_BRACKET/rev2'
RUNS = ('R1', 'R2')
UNDETERMINED = 'UNDETERMINED'


@dataclass(frozen=True)
class Placement:
    occurrence: int
    source_session_date: date
    leg_id: str
    instant: datetime
    run: str
    position: int
    rule: str
    vertex: int
    price: float


class BracketScheduleQuotes:
    """One run's schedule prices for one fresh replay; never reused.

    Ported to the frozen T00 step-1b split interface: the replay passes each
    leg's captured ``ScheduleExposure`` and receives one ``ScheduleSplit``.
    Placement, pricing and the R2 pending-only non-executing prefix are
    delegated to a fresh ``ScheduleExecutionBracket.for_run`` provider over
    empty reviewed evidence; this class adds only the placement record. A
    grid-boundary instant uses the retained source price there: the open of
    the leg's bar starting at the instant, else the close of its bar ending
    there. Anything else fails closed.
    """

    def __init__(self, run):
        from types import MappingProxyType
        from .production_source import ScheduleExecutionBracket, ScheduleExecutionEvidence
        if run not in RUNS:
            raise ValueError('bracket run must be R1 or R2')
        self.run = run
        empty = ScheduleExecutionEvidence(MappingProxyType({}), MappingProxyType({}), ())
        self._provider = ScheduleExecutionBracket(empty).for_run(run)
        self.placements = []

    def split_bar(self, session, pb, instant, leg, *, exposure):
        split = self._provider.split_bar(session, pb, instant, leg, exposure=exposure)
        return self._record(session, dict(pb.bars)[leg], instant, leg, exposure, split)

    def split_interval(self, session, pb, original, instant, leg, *, exposure):
        split = self._provider.split_interval(session, pb, original, instant, leg, exposure=exposure)
        return self._record(session, original, instant, leg, exposure, split)

    def _record(self, session, original, instant, leg, exposure, split):
        rule, vertex = placement(self.run, exposure.position, accepted_path(original))
        if split.prefix.close != accepted_path(original)[vertex] or split.prefix_executes is (rule == 'cancel'):
            raise ReplayNeedsContext('bracket provider placement differs from the ratified table')
        self.placements.append(Placement(session.occurrence, session.source.source_session_date, leg,
                                         instant, self.run, exposure.position, rule, vertex, split.prefix.close))
        return split

    def __call__(self, session, instant, leg):
        return self._provider(session, instant, leg)


@dataclass(frozen=True)
class BracketRun:
    run: str
    outcome: PathOutcome
    placements: tuple[Placement, ...]


@dataclass(frozen=True)
class BracketVerdict:
    """PASS, FAILURE or UNRESOLVED only where both runs agree; else UNDETERMINED.

    Each run keeps its own outcome, including its own sessions_to_pass; no
    combined count or R2-P&L/R1-lows hybrid is formed here.
    """
    status: str
    runs: tuple[BracketRun, BracketRun]
    convention: str = CONVENTION

    def __post_init__(self):
        if tuple(r.run for r in self.runs) != RUNS:
            raise ValueError('verdict requires R1 then R2')
        statuses = {r.outcome.status for r in self.runs}
        expected = statuses.pop() if len(statuses) == 1 else UNDETERMINED
        if self.status != expected:
            raise ValueError('verdict status must follow run agreement')


def run_bracket(build_replay, path, *, initial_state, evaluate=evaluate_replay):
    """Replay ``path`` once per run on a fresh engine and combine the verdicts.

    ``build_replay(quotes)`` must return a new single-use BookReplay whose
    ``schedule_quotes`` is ``quotes``. A confirmed deadline violation is that
    run's result; missing context aborts the path.
    """
    runs = []
    for run in RUNS:
        quotes = BracketScheduleQuotes(run)
        replay = build_replay(quotes)
        if getattr(replay, 'schedule_quotes', None) is not quotes:
            raise ValueError("replay must consume this run's placements")
        try:
            result = replay.run(path)
        except ReplayDeadlineFailure as exc:
            result = exc.result
        runs.append(BracketRun(run, evaluate(result, initial_state=initial_state), tuple(quotes.placements)))
    statuses = {r.outcome.status for r in runs}
    return BracketVerdict(statuses.pop() if len(statuses) == 1 else UNDETERMINED, tuple(runs))
