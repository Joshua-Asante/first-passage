"""Path-position bracket convention for schedule instants inside an M15 bar.

Ratified 2026-09-23 (revision 2) with build GO 2026-09-24:
docs/briefs/phase3-preparation/2026-09-15/schedule-execution-evidence.md.
The accepted emulator path of a bar is fixed; each run places an intrabar
schedule instant at one vertex of it and supplies that split through the
existing ``schedule_quotes`` seam, so ``BookReplay._split`` validates it
unchanged. R1 and R2 are complete replays evaluated separately; a path's
outcome is taken only where they agree. The two placements are extreme
vertices, not proven bounds on the true instant.

Engine-layer capability only: no G1 artifact role, production source, stage
runner or adjudication consumes it yet.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from c1_signal_daemon.feed import Bar
from .model import PathOutcome
from .replay import ReplayDeadlineFailure, ReplayNeedsContext, accepted_path
from .runner import evaluate_replay

CONVENTION = 'PATH_POSITION_BRACKET/rev2'
RUNS = ('R1', 'R2')
UNDETERMINED = 'UNDETERMINED'


def vertex_split(original, index, instant):
    """Prefix is the accepted path up to vertex ``index``; suffix is the rest.

    Volume carries no price and is kept whole on the prefix so the split
    aggregates to the source bar.
    """
    path = accepted_path(original)
    if type(index) is not int or not 0 <= index < len(path):
        raise ValueError('vertex index outside the accepted path')
    head, tail = path[:index+1], path[index:]
    return (Bar(original.ts, path[0], max(head), min(head), path[index], original.volume),
            Bar(instant, path[index], max(tail), min(tail), path[-1], 0.0))


def placement(run, position, path):
    """(rule, vertex index) for one leg: the addendum's two-run table.

    A signed position places the instant at its adverse (R1) or favourable
    (R2) extreme, first reached along the path. Without a position the
    endpoints are used: close (R1, fill) and open (R2, cancel).
    """
    if run not in RUNS:
        raise ValueError('bracket run must be R1 or R2')
    if type(position) is not int:
        raise ValueError('signed integer position required')
    if position == 0:
        return ('fill', len(path)-1) if run == 'R1' else ('cancel', 0)
    low, high = path.index(min(path)), path.index(max(path))
    adverse, favourable = (low, high) if position > 0 else (high, low)
    return ('adverse', adverse) if run == 'R1' else ('favourable', favourable)


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

    Intrabar prices exist only as placements made from the replay's observed
    exposure. A grid-boundary instant uses the retained source price there:
    the open of the leg's bar starting at the instant, else the close of its
    bar ending there. Anything else fails closed.
    """

    def __init__(self, run):
        if run not in RUNS:
            raise ValueError('bracket run must be R1 or R2')
        self.run = run
        self._exposure = None
        self._prices = {}
        self.placements = []

    def observe_exposure(self, session, instant, positions):
        self._exposure = (session.occurrence, instant, dict(positions))

    def split_bar(self, session, pb, instant, leg):
        return self._place(session, dict(pb.bars)[leg], instant, leg)

    def split_interval(self, session, pb, original, instant, leg):
        return self._place(session, original, instant, leg)

    def _place(self, session, original, instant, leg):
        exposure = self._exposure
        if exposure is None or exposure[:2] != (session.occurrence, instant) or leg not in exposure[2]:
            raise ReplayNeedsContext('bracket placement requires the leg exposure at the instant')
        key = (session.occurrence, leg, instant)
        if key in self._prices:
            raise ReplayNeedsContext('bracket instant already placed for this leg')
        position = exposure[2][leg]
        rule, vertex = placement(self.run, position, accepted_path(original))
        prefix, suffix = vertex_split(original, vertex, instant)
        self._prices[key] = prefix.close
        self.placements.append(Placement(session.occurrence, session.source.source_session_date, leg,
                                         instant, self.run, position, rule, vertex, prefix.close))
        return prefix, suffix

    def __call__(self, session, instant, leg):
        placed = self._prices.get((session.occurrence, leg, instant))
        if placed is not None:
            return placed
        bars = [(pb.source_bar_time, dict(pb.bars).get(leg)) for pb in session.bars]
        for start, bar in bars:
            if bar is not None and start == instant:
                return bar.open
        for start, bar in bars:
            if bar is not None and start + timedelta(minutes=15) == instant:
                return bar.close
        raise ReplayNeedsContext('no placement or retained source price at the schedule instant')


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
