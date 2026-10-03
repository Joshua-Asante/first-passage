"""T00 screen plan: seeds, key universe, candidates and per-run shape (design 2026-10-02 sections 5.2, 5.3, 7).

Pure functions. Nothing here calls a source capability: ``candidates`` receives the candidate
worker's ``ScreenBracket``s (rows R1-R3).
"""
from __future__ import annotations

import hashlib
from math import isfinite

from ..blocks import JointFlatBlocks, partition_populations
from ..contract import canonical_json_bytes
from ..model import BracketReplayResult, ReplayResult

SEED_TAG = 't00-screen-rng/v1'
CANDIDATES_TAG = 't00-screen-candidates/v1'
POPULATIONS = ('FULL', 'H1', 'H2')


class PlanRefusal(ValueError):
    """A plan or shape refusal; ``code`` is the design section 4.3 code."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _sha256(value) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _text(value, label):
    if type(value) is not str or not value:
        raise ValueError(f'{label} must be nonempty text')


def _index(value, label):
    if type(value) is not int or value < 0:
        raise ValueError(f'{label} must be a nonnegative integer')


def seed(*, purpose: str, root: str, population: str, path_index: int) -> int:
    """First 8 bytes of SHA-256 of canonical [tag, purpose, root, population, path_index] (row R1)."""
    _text(purpose, 'purpose')
    _text(root, 'root')
    if population not in POPULATIONS:
        raise ValueError('population must be FULL, H1 or H2')
    _index(path_index, 'path_index')
    digest = hashlib.sha256(canonical_json_bytes([SEED_TAG, purpose, root, population, path_index])).digest()
    return int.from_bytes(digest[:8], 'big')


def key_universe(roots, depth_per_root) -> tuple[tuple[str, str, int], ...]:
    """K = {(root, population, path_index) : path_index < depth_per_root[population]}, sorted (section 7)."""
    roots = tuple(roots)
    if not roots or len(set(roots)) != len(roots):
        raise ValueError('distinct roots required')
    for root in roots:
        _text(root, 'root')
    if set(depth_per_root) != set(POPULATIONS) or any(
            type(d) is not int or d <= 0 for d in depth_per_root.values()):
        raise ValueError('positive integer depth for FULL, H1 and H2 required')
    return tuple(sorted((root, population, index) for root in roots for population in POPULATIONS
                        for index in range(depth_per_root[population])))


def plan_sha256(keys) -> str:
    """SHA-256 of the canonical sorted key list (section 7)."""
    return _sha256([list(key) for key in keys])


def _candidates_sha256(population, pool, indices, block_sessions):
    return _sha256([CANDIDATES_TAG, population, block_sessions,
                    [[s.session_id for s in pool[i:i + block_sessions]] for i in indices]])


def _flat_starts(pool, run, joins, block_sessions):
    """Block-start indices flat at both edges in one chronological run, as ``proof`` derives edges."""
    rows = run.sessions if type(run) is ReplayResult else None
    if (rows is None or len(rows) != len(pool) or any(not row.flat_before_deadline for row in rows)
            or any((row.occurrence, row.source_session_id) != (i, s.session_id)
                   for i, (row, s) in enumerate(zip(rows, pool)))
            or any(a.end_edge != b.start_edge for a, b in zip(rows, rows[1:]))):
        raise PlanRefusal('CANDIDATES_UNAVAILABLE')
    edges = (rows[0].start_edge,) + tuple(row.end_edge for row in rows)
    blocks = JointFlatBlocks(tuple(range(len(pool))), edges, block_sessions, joins).candidates()
    return {block[0] for block in blocks}


def candidates(sessions, adjacent, brackets, *, block_sessions: int) -> dict[str, dict[str, object]]:
    """Per population, the R1 and R2 joint-flat intersection as block-start indices plus digest (row R2).

    ``sessions``/``adjacent`` are the source's chronological panel and join proofs; ``brackets`` maps
    each population to the candidate worker's ``ScreenBracket`` over that population's chronological
    path. The result is the manifest's ``populations`` value.
    """
    sessions, adjacent = tuple(sessions), tuple(adjacent)
    if len(adjacent) != max(0, len(sessions) - 1):
        raise ValueError('one adjacency proof per source join required')
    index = {s.session_id: i for i, s in enumerate(sessions)}
    result = {}
    for population, pool in partition_populations(sessions).items():
        screen = brackets.get(population)
        if not pool or screen is None or type(screen.bracket) is not BracketReplayResult:
            raise PlanRefusal('CANDIDATES_UNAVAILABLE')
        if tuple(screen.deadline_failure) != (False, False):
            raise PlanRefusal('CANDIDATES_UNAVAILABLE')
        joins = tuple(adjacent[index[a.session_id]] if index[b.session_id] == index[a.session_id] + 1 else True
                      for a, b in zip(pool, pool[1:]))
        starts = (_flat_starts(pool, screen.bracket.r1, joins, block_sessions)
                  & _flat_starts(pool, screen.bracket.r2, joins, block_sessions))
        if not starts:
            raise PlanRefusal('CANDIDATES_UNAVAILABLE')
        indices = sorted(starts)
        result[population] = {'indices': indices,
                              'candidates_sha256': _candidates_sha256(population, pool, indices, block_sessions)}
    return result


def rebuild_candidates(sessions, populations, *, block_sessions: int) -> dict[str, tuple[tuple, ...]]:
    """Rebuild each population's candidate blocks from stored indices; any malformed entry or digest
    mismatch is CORRUPTION (closed stop classes, design section 4.3)."""
    pools = partition_populations(tuple(sessions))
    if type(populations) is not dict or set(populations) != set(POPULATIONS):
        raise PlanRefusal('CORRUPTION')
    result = {}
    for population, pool in pools.items():
        entry = populations[population]
        indices = entry.get('indices') if type(entry) is dict else None
        if (type(indices) is not list or not indices
                or any(type(i) is not int or not 0 <= i <= len(pool) - block_sessions for i in indices)
                or indices != sorted(set(indices))
                or entry.get('candidates_sha256') != _candidates_sha256(population, pool, indices, block_sessions)):
            raise PlanRefusal('CORRUPTION')
        result[population] = tuple(pool[i:i + block_sessions] for i in indices)
    return result


def shape_check(run, failed, path) -> None:
    """A run is scored only with full length and no deadline flag, or the flag on a terminal failed prefix (row R3)."""
    if type(run) is not ReplayResult or type(failed) is not bool:
        raise PlanRefusal('CONTEXT_REFUSAL')
    rows, horizon = run.sessions, len(path)
    if not failed:
        shaped = len(rows) == horizon
    else:
        shaped = (0 < len(rows) <= horizon and not rows[-1].flat_before_deadline
                  and all(row.flat_before_deadline for row in rows[:-1]))
    if not shaped or any((row.occurrence, row.source_session_id) != (s.occurrence, s.source.session_id)
                         for row, s in zip(rows, path)):
        raise PlanRefusal('CONTEXT_REFUSAL')
    for row in rows:
        low = row.intraday_low
        if type(low) not in (float, int) or not isfinite(low) or low > 0:
            raise PlanRefusal('INTRADAY_LOW_MISSING')
