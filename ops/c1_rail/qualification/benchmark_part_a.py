"""One representative synthetic Part A workload, never a qualification panel batch."""
from __future__ import annotations

import argparse
from calendar import monthrange
from dataclasses import asdict
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import platform
from random import Random
from time import perf_counter

from mc.simulation import EvaluationState
from .benchmark import synthetic_replay, synthetic_source
from .paths import PathAssembler
from .regime import domain_seed, rebuild_inner_blocks, sample_outer_panel
from .runner import evaluate_replay


def benchmark_part_a(*, horizon_sessions, seed, source_start=date(2020, 1, 6), source_months=8):
    if type(horizon_sessions) is not int or horizon_sessions <= 0 or horizon_sessions % 5:
        raise ValueError('whole five-session benchmark horizon required')
    if type(source_months) is not int or source_months < 7:
        raise ValueError('at least seven synthetic source calendar months required')
    if type(seed) is not int or type(source_start) is not date:
        raise ValueError('explicit integer seed and synthetic date required')
    start = perf_counter()
    year, month0 = divmod(source_start.year*12+source_start.month-1+source_months, 12)
    end = date(year, month0+1, min(source_start.day, monthrange(year, month0+1)[1]))
    days = []
    day = source_start
    while day < end:
        if day.weekday() < 5:
            days.append(day)
        day += timedelta(days=1)
    source = tuple(synthetic_source(day) for day in days)
    built = perf_counter()
    root_seed = 'representative-part-a-benchmark:' + str(seed)
    outer_seed = domain_seed(root=root_seed, stage='n2', population='FULL', panel_index=0,
                             path_index=0, purpose='outer', synthetic=True)
    # This generated fixture defines every weekday as covered. It makes no
    # statement about exchange holidays, historical feeds or approved sessions.
    panel = sample_outer_panel(source, Random(outer_seed), months=6,
                               adjacent=(True,)*(len(source)-1), covered_until=end, tail_covered=True)
    selected = perf_counter()
    assembler = PathAssembler(date(2030, 1, 7))
    proof_result = None

    def prove(occurrences):
        nonlocal proof_result
        proof_path = assembler.assemble(tuple((session,) for session in occurrences), horizon_sessions=len(occurrences))
        proof_result = synthetic_replay(proof_path)
        rows = proof_result.sessions
        if len(rows) != len(occurrences):
            raise ValueError('proof replay did not cover entire alternate panel')
        for i, (row, expected) in enumerate(zip(rows, proof_path)):
            if (row.occurrence, row.source_session_id, row.path_session_date) != (
                    expected.occurrence, expected.source.session_id, expected.path_session_date):
                raise ValueError('proof replay occurrence mismatch')
            if i and rows[i-1].end_edge != row.start_edge:
                raise ValueError('proof ledger edge discontinuity')
        edges = (rows[0].start_edge,) + tuple(row.end_edge for row in rows)
        # Every occurrence join is exercised by the continuous synthetic replay.
        # Original source-calendar adjacency is separately checked by outer_ranges.
        return edges, (True,)*(len(occurrences)-1)

    candidates = rebuild_inner_blocks(panel, prove, block_sessions=5).candidates()
    if not candidates:
        raise ValueError('representative fixture has no proven whole inner blocks')
    proved = perf_counter()
    inner_seed = domain_seed(root=root_seed, stage='n2', population='FULL', panel_index=0,
                             path_index=0, purpose='path', synthetic=True)
    path = assembler.sample(candidates, Random(inner_seed), horizon_sessions=horizon_sessions)
    replay = synthetic_replay(path)
    evaluate_replay(replay, initial_state=EvaluationState(100000, 100000, 100000, 0, 0))
    replayed = perf_counter()
    canonical = json.dumps({'proof': asdict(proof_result), 'path': asdict(replay)},
                           default=str, sort_keys=True, separators=(',', ':')).encode()
    serialized = perf_counter()
    repo = Path(__file__).resolve().parents[3]
    modules = sorted((repo/'ops/c1_rail/qualification').glob('*.py'))
    modules.extend(repo/name for name in (
        'ops/c1_rail/book_policy.py', 'ops/c1_signal_daemon/tv_broker_emulator.py',
        'ops/c1_signal_daemon/book_protocol.py', 'ops/c1_signal_daemon/pine_ta.py',
        'ops/c1_signal_daemon/book_adapters.py', 'core/mc/simulation.py', 'core/mc/preflight.py',
        'core/firm_rules.py', 'core/dd_geometry.py', 'core/lifecycle.py', 'requirements-ops.lock'))
    return {
        'schema': 'synthetic-part-a-workload/v1', 'synthetic': True, 'processes': 1, 'seed': seed,
        'source_sessions': len(source), 'source_months': source_months,
        'proof_sessions': len(proof_result.sessions), 'inner_candidates': len(candidates),
        'path_sessions': len(replay.sessions), 'path_bars': sum(len(s.bars) for s in path),
        'proof_bars': sum(len(s.bars) for s in panel),
        'fills': sum(s.fills for s in replay.sessions), 'events': len(replay.events),
        'serialized_bytes': len(canonical), 'equivalence_sha256': hashlib.sha256(canonical).hexdigest(),
        'python': platform.python_version(), 'platform': platform.platform(),
        'source_sha256': {p.relative_to(repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in modules},
        'timings': {'source_build': built-start, 'outer_selection': selected-built,
                    'proof_rebuild': proved-selected, 'path_replay_kernel': replayed-proved,
                    'serialization': serialized-replayed, 'total': serialized-start}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--horizon', type=int, required=True)
    parser.add_argument('--seed', type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(benchmark_part_a(horizon_sessions=args.horizon, seed=args.seed), sort_keys=True))
