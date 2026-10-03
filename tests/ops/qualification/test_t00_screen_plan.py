"""T00 screen plan rows R1-R3 (design 2026-10-02 sections 2.2, 5.2, 5.3, 7; card 2026-10-03 section 2.8).

Synthetic fixtures only; no test reads the real source. The plan module is imported inside each
test body so each row test fails on its own before the module exists.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import date, timedelta
import hashlib
import json
from types import SimpleNamespace

import pytest

from mc.simulation import EvaluationState
from c1_rail.qualification import regime
from c1_rail.qualification.benchmark import synthetic_source
from c1_rail.qualification.model import (BracketReplayResult, EdgeState, LEG_IDS, PathOutcome, ReplayResult,
                                         SessionRecord)
from c1_rail.qualification.paths import PathAssembler
from c1_rail.qualification.runner import evaluate_replay

ROOTS = ('root-a', 'root-b', 'root-c')
DEPTH = {'FULL': 5, 'H1': 3, 'H2': 4}
PURPOSE = 'T00_STEP3_SELECTED_BOOK_SCREEN'


def _edge(flat=True):
    zero = tuple((leg, 0) for leg in LEG_IDS)
    working = tuple((leg, int(not flat and i == 0)) for i, leg in enumerate(LEG_IDS))
    return EdgeState(zero, working, zero)


def _pool(n):
    return tuple(SimpleNamespace(session_id=f'synthetic:{i}') for i in range(n))


def _run(pool, flat_edges):
    """A chronological run over ``pool`` whose edge ``i`` is flat iff ``flat_edges[i]``."""
    edges = tuple(_edge(f) for f in flat_edges)
    rows = tuple(SessionRecord(i, date(2030, 1, 7) + timedelta(days=i), s.session_id, 0.0, 0.0, 0, True,
                               edges[i], edges[i + 1]) for i, s in enumerate(pool))
    return ReplayResult(rows, ())


def _bracket(pool, r1_flat, r2_flat):
    """A fake ScreenBracket (card section 3.1 fields) from the candidate worker."""
    return SimpleNamespace(bracket=BracketReplayResult(_run(pool, r1_flat), _run(pool, r2_flat)),
                           deadline_failure=(False, False), consumed_splits=((), ()))


def _brackets(sessions, r2_flat_for):
    middle = (len(sessions) + 1) // 2
    pools = {'FULL': sessions, 'H1': sessions[:middle], 'H2': sessions[middle:]}
    return {name: _bracket(pool, (True,) * (len(pool) + 1), r2_flat_for(name, len(pool)))
            for name, pool in pools.items()}


def _shard(keys, workers):
    return [keys[i::workers] for i in range(workers)]


def test_R1():
    from c1_rail.qualification.t00_screen import plan
    keys = plan.key_universe(ROOTS, DEPTH)
    assert keys == tuple(sorted(keys)) and len(keys) == 3 * sum(DEPTH.values())
    assert plan.plan_sha256(keys) == hashlib.sha256(
        json.dumps([list(k) for k in keys], separators=(',', ':')).encode()).hexdigest()

    def seeds(workers):
        out = {}
        for shard in _shard(keys, workers):
            for root, population, index in reversed(shard):
                out[(root, population, index)] = plan.seed(purpose=PURPOSE, root=root, population=population,
                                                           path_index=index)
        return out

    w1, w4 = seeds(1), seeds(4)
    assert w1 == w4  # determinism: W and dispatch order never change a seed
    root, population, index = keys[7]
    expected = int.from_bytes(hashlib.sha256(json.dumps(
        ['t00-screen-rng/v1', PURPOSE, root, population, index], separators=(',', ':')).encode()).digest()[:8], 'big')
    assert w1[keys[7]] == expected
    for change in ({'purpose': 'other'}, {'root': 'root-z'}, {'population': 'H1' if population != 'H1' else 'H2'},
                   {'path_index': index + 1}):
        args = dict(purpose=PURPOSE, root=root, population=population, path_index=index) | change
        assert plan.seed(**args) != expected
    # Collision scan against regime.domain_seed for the same indices: none.
    qualification = {
        regime.domain_seed(root=r, stage=stage, population=p, panel_index=None, path_index=i,
                           synthetic=synthetic, purpose=purpose)
        for r, p, i in keys for stage in ('n1', 'n2', 'n3', 'probe') for synthetic in (True, False)
        for purpose in ('path', 'probe')}
    assert not set(w1.values()) & qualification
    assert len(set(w1.values())) == len(keys)


def test_R1_seed_never_calls_domain_seed(monkeypatch):
    from c1_rail.qualification.t00_screen import plan

    def refused(**_):
        raise AssertionError('plan.seed must not use regime.domain_seed')
    monkeypatch.setattr(regime, 'domain_seed', refused)
    assert type(plan.seed(purpose=PURPOSE, root='r', population='FULL', path_index=0)) is int
    for bad in ({'root': ''}, {'population': 'H3'}, {'path_index': -1}, {'path_index': True}, {'purpose': ''}):
        args = dict(purpose=PURPOSE, root='r', population='FULL', path_index=0) | bad
        with pytest.raises(ValueError):
            plan.seed(**args)


def test_R2():
    from c1_rail.qualification.t00_screen import plan
    sessions, adjacent = _pool(9), (True,) * 8

    def r2_flat(name, n):  # FULL: edge 3 open in R2 only, so blocks at 1 and 3 are flat in R1 only
        return tuple(i != 3 for i in range(n + 1)) if name == 'FULL' else (True,) * (n + 1)
    populations = plan.candidates(sessions, adjacent, _brackets(sessions, r2_flat), block_sessions=2)
    assert list(populations) == ['FULL', 'H1', 'H2']
    assert populations['FULL']['indices'] == [0, 2, 4, 5, 6, 7]  # R1 alone gives 0..7
    assert populations['H1']['indices'] == [0, 1, 2, 3]  # twin: flat in both runs is a candidate
    # Digest rebuild matches; a changed index list does not.
    blocks = plan.rebuild_candidates(sessions, populations, block_sessions=2)
    assert blocks['FULL'] == tuple(sessions[i:i + 2] for i in (0, 2, 4, 5, 6, 7))
    tampered = populations | {'FULL': populations['FULL'] | {'indices': [0, 1, 4, 5, 6, 7]}}
    with pytest.raises(plan.PlanRefusal) as exc:
        plan.rebuild_candidates(sessions, tampered, block_sessions=2)
    assert exc.value.code == 'CORRUPTION'

    # A population whose blocks are flat in R1 only has no candidate left.
    def r2_closed(name, n):
        return (False,) * (n + 1) if name == 'H2' else (True,) * (n + 1)
    with pytest.raises(plan.PlanRefusal) as exc:
        plan.candidates(sessions, adjacent, _brackets(sessions, r2_closed), block_sessions=2)
    assert exc.value.code == 'CANDIDATES_UNAVAILABLE'


def test_R2_chronological_failures_are_unavailable():
    from c1_rail.qualification.t00_screen import plan
    sessions, adjacent = _pool(6), (True,) * 5
    flat = _brackets(sessions, lambda name, n: (True,) * (n + 1))
    deadline = flat | {'H1': SimpleNamespace(**vars(flat['H1']) | {'deadline_failure': (False, True)})}
    short = flat | {'H2': SimpleNamespace(**vars(flat['H2']) | {'bracket': BracketReplayResult(
        replace(flat['H2'].bracket.r1, sessions=flat['H2'].bracket.r1.sessions[:-1]), flat['H2'].bracket.r2)})}
    rows = flat['FULL'].bracket.r2.sessions
    broken = flat | {'FULL': SimpleNamespace(**vars(flat['FULL']) | {'bracket': BracketReplayResult(
        flat['FULL'].bracket.r1, replace(flat['FULL'].bracket.r2, sessions=(
            rows[:2] + (replace(rows[2], start_edge=_edge(False)),) + rows[3:])))})}
    for case in (deadline, short, broken):
        with pytest.raises(plan.PlanRefusal) as exc:
            plan.candidates(sessions, adjacent, case, block_sessions=2)
        assert exc.value.code == 'CANDIDATES_UNAVAILABLE'
    with pytest.raises(plan.PlanRefusal) as exc:  # empty H2 population
        plan.candidates(_pool(1), (), _brackets(_pool(1), lambda name, n: (True,) * (n + 1)), block_sessions=1)
    assert exc.value.code == 'CANDIDATES_UNAVAILABLE'
    # A source gap is never a join (as proof's joins and provider spans).
    gap = plan.candidates(sessions, (True, False, True, True, True), flat, block_sessions=2)
    assert gap['FULL']['indices'] == [0, 2, 3, 4] and gap['H1']['indices'] == [0]


def _path(h):
    sources = tuple(synthetic_source(date(2020, 1, 6) + timedelta(days=i)) for i in range(h))
    return PathAssembler(date(2030, 1, 7)).assemble(tuple((s,) for s in sources), horizon_sessions=h)


def _path_run(path, *, flat=True):
    return ReplayResult(tuple(SessionRecord(s.occurrence, s.path_session_date, s.source.session_id, 0.0, -1.0, 0,
                                            flat, _edge(), _edge()) for s in path), ())


def test_R3():
    from c1_rail.qualification.t00_screen import plan
    path = _path(4)
    run = _path_run(path)
    short = replace(run, sessions=run.sessions[:3])
    with pytest.raises(plan.PlanRefusal) as exc:
        plan.shape_check(short, False, path)
    assert exc.value.code == 'CONTEXT_REFUSAL'
    # Twin: the full-length run passes and is scored by the unchanged runner.
    assert plan.shape_check(run, False, path) is None
    outcome = evaluate_replay(run, initial_state=EvaluationState(100000, 100000, 100000, 0, 0))
    assert type(outcome) is PathOutcome


def test_R3_deadline_prefix_lows_and_identity():
    from c1_rail.qualification.t00_screen import plan
    path = _path(4)
    run = _path_run(path)
    rows = run.sessions
    failed_prefix = replace(run, sessions=rows[:2] + (replace(rows[2], flat_before_deadline=False),))
    assert plan.shape_check(failed_prefix, True, path) is None  # terminal failed prefix is scored
    refusals = {
        'flag_on_flat_prefix': (replace(run, sessions=rows[:3]), True),
        'flag_with_earlier_failure': (replace(run, sessions=(replace(rows[0], flat_before_deadline=False),)
                                              + rows[1:2] + (replace(rows[2], flat_before_deadline=False),)), True),
        'flag_on_empty': (replace(run, sessions=()), True),
        'long': (replace(run, sessions=rows + rows[:1]), False),
        'source_id': (replace(run, sessions=rows[:1] + (replace(rows[1], source_session_id='other'),) + rows[2:]), False),
        'occurrence': (replace(run, sessions=rows[:1] + (replace(rows[1], occurrence=5),) + rows[2:]), False),
        'flag_not_bool': (run, 0),
    }
    for name, (case, failed) in refusals.items():
        with pytest.raises(plan.PlanRefusal) as exc:
            plan.shape_check(case, failed, path)
        assert exc.value.code == 'CONTEXT_REFUSAL', name
    for low in (float('nan'), float('inf'), 0.5):
        bad = replace(rows[1])
        object.__setattr__(bad, 'intraday_low', low)
        with pytest.raises(plan.PlanRefusal) as exc:
            plan.shape_check(replace(run, sessions=rows[:1] + (bad,) + rows[2:]), False, path)
        assert exc.value.code == 'INTRADAY_LOW_MISSING'
