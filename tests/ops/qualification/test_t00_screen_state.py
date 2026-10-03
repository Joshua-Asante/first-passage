"""T00 screen run state and journal: rows S1, S3, S9, S10, S13, S14, S16 and B1.

Design 2026-10-02 §4 (persistence, the §4.2 transition table, the §4.3 stop classes) and
build card §3.4-§3.6 (packet P-D), with the O-6 ACT case table under ``test_S1`` and the
O-8 closure, O-11 gap and X3 act clauses of ``check_record``. Synthetic records only: no
source, key, probe or Monte Carlo. Each test imports the modules under test in its own
body, so each row fails on its own before they exist (card §2.2, red-first).
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
import importlib
import json
import os
import random
import socket

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as canonical

ROOTS = ('root-a', 'root-b')
POPULATIONS = ('FULL', 'H1', 'H2')
STATUSES = ('PASS', 'FAILURE', 'UNDETERMINED')
PLAN = tuple(sorted((root, population, index) for root in ROOTS for population in POPULATIONS for index in range(2)))
APPEND = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, 'O_BINARY', 0)
STATES = ('NONE', 'BOUND', 'PREPARED', 'PROBING', 'IDLE', 'RUNNING', 'HALTED', 'COMPLETE', 'TERMINAL',
          'AGGREGATED', 'REPORTED', 'FINAL')


def modules():
    package = 'c1_rail.qualification.t00_screen.'
    return importlib.import_module(package + 'state'), importlib.import_module(package + 'journal')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def hexd(label):
    return sha(label.encode())


AUTH = hexd('authority')
CLOSURE = hexd('closure')


def cost(cpu=1.0, wall=1.25):
    return {'cpu_s': cpu, 'wall_s': wall}


def epoch_open(closure=CLOSURE):
    return {'build': cost(170.0, 200.0), 'integrity': cost(71.0, 80.0), 'closure_sha256': closure,
            'guard_sha256': hexd('guard')}


def epoch_close(match=True):
    return {'integrity': cost(71.0, 80.0), 'closure_match': match}


def path_body(key, *, cpu=2.0, wall=3.0, salt=''):
    tag = repr(key)
    status = STATUSES[int(hexd(tag)[:2], 16) % 3]

    def run(name, run_status):
        passed = run_status == 'PASS'
        return {'digest': hexd(tag + name + salt), 'sessions': 30, 'fills': 4, 'events_sha256': hexd(tag + name + 'ev'),
                'deadline_failure': False, 'consumed_intrabar_split_count': 0,
                'consumed_intrabar_splits_sha256': sha(canonical([])), 'status': run_status,
                'sessions_to_pass': 12 if passed else None, 'failure_reason': None if passed else 'bust_trailing',
                'kernel_outcome': 'pass' if passed else 'bust_trailing'}
    r1, r2 = (status, status) if status != 'UNDETERMINED' else ('PASS', 'FAILURE')
    return {'key': list(key), 'seed': int(hexd(tag)[:16], 16), 'path_sha256': hexd(tag + 'path'),
            'bracket_status': status, 'runs': {'r1': run('r1', r1), 'r2': run('r2', r2)}, 'wall_s': wall, 'cpu_s': cpu}


class Chain:
    """Records chained exactly as card §3.4 defines a line (its SHA-256 is that of the line without LF)."""

    def __init__(self, records=()):
        self.records = []
        for record in records:
            self.add(record['type'], record['body'])

    def add(self, type_, body):
        prev = sha(canonical(self.records[-1])) if self.records else None
        self.records.append({'body': body, 'prev_sha256': prev, 'type': type_})
        return self


def manifest():
    populations = {p: {'indices': [0, 2, 5], 'candidates_sha256': hexd('candidates' + p)} for p in POPULATIONS}
    return {'authority_sha256': AUTH, 'contract_sha256': hexd('r3c'), 'p7_record_sha256': hexd('p7'),
            'code_head': 'c' * 40, 'populations': populations, 'plan_sha256': hexd('plan')}


def bound_body():
    return {'authority_sha256': AUTH, 'prereg_path': 'docs/briefs/pre-registration/prereg.md',
            'approvals': [hexd('r3c-approval'), hexd('screen-approval')], 'reused_directory': False}


def idle_ledger(m):
    return (Chain().add('AUTHORITY_BOUND', bound_body())
            .add('PREPARED', {'manifest_sha256': sha(canonical(m)), 'build': cost(), 'integrity': cost()})
            .add('PROBE_START', {})
            .add('PROBE', {'path_cpu_s': 136.0, 'path_wall_s': 170.0, 'peak_memory_bytes': 600 << 20}))


def candidate_journal(m):
    return (Chain().add('EPOCH_OPEN', epoch_open()).add('CANDIDATES', {'populations': m['populations']})
            .add('EPOCH_CLOSE', epoch_close()).add('EPOCH_OPEN', epoch_open())
            .add('PROBE_RESULT', {'path_cpu_s': 136.0, 'path_wall_s': 170.0, 'peak_memory_bytes': 600 << 20})
            .add('EPOCH_CLOSE', epoch_close()).add('WORKER_STOP', {'reason': 'DONE', 'key': None})).records


def segment_start(k, w, witnesses=()):
    return {'k': k, 'w': w, 'assignment_sha256': hexd(f'assignment{k}'),
            'witness_keys': [list(key) for key in witnesses], 'approvals': [hexd('r3c-approval')]}


def segment_end(k, w, cls, cause):
    return {'class': cls, 'cause': cause, 'workers': [{'worker': f's{k}-w{i}', 'reason': cause} for i in range(w)],
            'wall_s': 10.0, 'job_cpu_s': 40.0, 'path_cpu_s': 30.0, 'overhead_cpu_s': 10.0,
            'peak_memory_bytes': 600 << 20}


@dataclass(frozen=True)
class Seg:
    w: int
    stop: int | None = None      # keys each worker completes before it stops; None runs its whole list
    end: object = 'COMPLETE'     # 'COMPLETE', 'CRASHED', 'OPEN' (killed, not yet resumed) or (class, cause)
    name_inflight: bool = False  # the worker's WORKER_STOP names its in-flight key (not a loss)


def simulate(segments, *, keys=PLAN, outcome=None, inject=None, skip=(), seed=0):
    """A driver stand-in: each segment re-partitions K - completed round-robin by ordinal mod W
    (design §7), worker i first re-executes tagged witness i (row S13), and every PATH follows
    its fsync'd KEY_START (row S10). A crashed segment's SEGMENT_CRASHED is written at resume."""
    rng = random.Random(seed)
    outcome = outcome or (lambda key, k: path_body(key, cpu=rng.uniform(100, 200), wall=rng.uniform(100, 300)))
    m = manifest()
    ledger, journals, done, crashed = idle_ledger(m), {'c1-w0': candidate_journal(m)}, [], None
    for k, seg in enumerate(segments, 1):
        if crashed is not None:
            ledger.add('SEGMENT_CRASHED', {'k': crashed[0], 'charge': cost(50.0, 60.0), 'losses': crashed[1]})
            crashed = None
        remaining = [key for key in sorted(keys) if key not in done]
        witnesses = sorted(done)[:min(seg.w, len(done))]
        ledger.add('SEGMENT_START', segment_start(k, seg.w, witnesses))
        lost = []
        for i in range(seg.w):
            name = f's{k}-w{i}'
            todo = [key for key in witnesses[i:i + 1] + remaining[i::seg.w] + list((inject or {}).get(name, ()))
                    if key not in skip]
            n = len(todo) if seg.stop is None else min(seg.stop, len(todo))
            journal = Chain().add('EPOCH_OPEN', epoch_open())
            for key in todo[:n]:
                journal.add('KEY_START', {'key': list(key)}).add('PATH', outcome(key, k))
                if key not in done:
                    done.append(key)
            if n < len(todo):
                journal.add('KEY_START', {'key': list(todo[n])})
                if seg.name_inflight:
                    journal.add('WORKER_STOP', {'reason': seg.end[1], 'key': list(todo[n])})
                else:
                    lost.append(list(todo[n]))
            else:
                journal.add('EPOCH_CLOSE', epoch_close()).add('WORKER_STOP', {'reason': 'DONE', 'key': None})
            journals[name] = journal.records
        if seg.end == 'CRASHED':
            crashed = (k, sorted(lost))
        elif seg.end != 'OPEN':
            cls, cause = ('COMPLETE', 'COMPLETE') if seg.end == 'COMPLETE' else seg.end
            ledger.add('SEGMENT_END', segment_end(k, seg.w, cls, cause))
    return ledger.records, journals, m


def check(ledger, journals, m, acts=None, keys=PLAN):
    state, _ = modules()
    return state.check_record(ledger, journals, m, acts or {}, keys=keys)


def materialize(run_dir, ledger, journals):
    """Write every record with ``journal.append`` (one ledger file per coordinator invocation)
    and read the run back with ``journal.read``."""
    _, journal = modules()
    (run_dir / 'ledger').mkdir(parents=True)
    (run_dir / 'journal').mkdir()

    def write(path, records, prev):
        fd = os.open(path, APPEND, 0o644)
        try:
            for record in records:
                assert record['prev_sha256'] == prev
                prev = journal.append(fd, record['type'], record['body'], prev_sha256=prev)
                assert prev == sha(canonical(record))
        finally:
            os.close(fd)
        return prev
    files, prev = [[]], None
    for record in ledger:
        if record['type'] == 'SEGMENT_START':
            files.append([])
        files[-1].append(record)
    for number, records in enumerate(files, 1):
        prev = write(run_dir / 'ledger' / f'{number:04d}.jsonl', records, prev)
    for name, records in journals.items():
        write(run_dir / 'journal' / name, records, None)
    read_ledger, prev = [], None
    for path in sorted((run_dir / 'ledger').iterdir()):
        records = journal.read(path, prev_sha256=prev)
        read_ledger.extend(records)
        prev = sha(canonical(records[-1])) if records else prev
    read_journals = {path.name: journal.read(path, prev_sha256=None) for path in (run_dir / 'journal').iterdir()}
    assert read_ledger == list(ledger) and {k: list(v) for k, v in read_journals.items()} == journals
    return read_ledger, read_journals


def synthetic_verdict(rows):
    """Stand-in for ``verdict.as_json`` (card §3.7 shape); P-C's module is never imported (card §2.7)."""
    tallies = {p: {s: 0 for s in STATUSES} for p in POPULATIONS}
    for row in rows:
        tallies[row['key'][1]][row['bracket_status']] += 1
    return {'kind': 'LABELLED', 'label': 'NO-GO-evidence-UNDETERMINED-dependent',
            'tallies': {'pessimistic': tallies, 'optimistic': tallies},
            'descriptive': {p: {'consumed_split_paths': 0, 'undetermined_paths': tallies[p]['UNDETERMINED']}
                            for p in POPULATIONS}}


def event(type_, body):
    return {'body': body, 'prev_sha256': None, 'type': type_}


def bodies():
    """One valid body per ledger event type (card §3.5); HALT and ACT are tabulated separately."""
    return {
        'AUTHORITY_BOUND': bound_body(),
        'PREPARED': {'manifest_sha256': hexd('manifest'), 'build': cost(), 'integrity': cost()},
        'PROBE_START': {}, 'PROBE': {'path_cpu_s': 1.0, 'path_wall_s': 1.0, 'peak_memory_bytes': 1},
        'SEGMENT_START': segment_start(1, 2), 'HEARTBEAT': {'wall_s': 60.0, 'job_cpu_s': 400.0},
        'SEGMENT_END': segment_end(1, 2, 'STOPPED', 'WORKER_LOST'),
        'SEGMENT_CRASHED': {'k': 1, 'charge': cost(), 'losses': []}, 'ALL_DONE': {},
        'TERMINAL': {'code': 'BUDGET_EXHAUSTED'}, 'AGGREGATED': {'results_sha256': hexd('results')},
        'REPORTED': {'report_sha256': hexd('report')}, 'FINAL': {'attestation_sha256': hexd('attestation')},
        'VERIFY_START': {'n': 1, 'keys': [list(PLAN[0])]}, 'VERIFY': {'n': 1, 'keys': [list(PLAN[0])], 'match': True},
    }


# Design §4.2, (from, event) -> to, for every event except HALT and ACT.
DESIGN_TABLE = {
    ('NONE', 'AUTHORITY_BOUND'): 'BOUND', ('BOUND', 'PREPARED'): 'PREPARED', ('PREPARED', 'PROBE_START'): 'PROBING',
    ('PROBING', 'PROBE'): 'IDLE', ('IDLE', 'SEGMENT_START'): 'RUNNING', ('IDLE', 'ALL_DONE'): 'COMPLETE',
    ('RUNNING', 'HEARTBEAT'): 'RUNNING', ('RUNNING', 'SEGMENT_END'): 'IDLE', ('RUNNING', 'SEGMENT_CRASHED'): 'IDLE',
    ('COMPLETE', 'AGGREGATED'): 'AGGREGATED', ('TERMINAL', 'AGGREGATED'): 'AGGREGATED',
    ('AGGREGATED', 'REPORTED'): 'REPORTED', ('REPORTED', 'FINAL'): 'FINAL',
    ('FINAL', 'VERIFY_START'): 'FINAL', ('FINAL', 'VERIFY'): 'FINAL',
    **{(name, 'TERMINAL'): 'TERMINAL' for name in STATES if name not in ('NONE', 'RUNNING', 'FINAL')},
}


def test_S1(tmp_path):
    state, journal = modules()
    State, advance, fold = state.State, state.advance, state.fold
    path = tmp_path / 'ledger' / '0001.jsonl'
    path.parent.mkdir()
    fd = os.open(path, APPEND, 0o644)
    current, prev = fold(()), None

    def commit(type_, body):  # the coordinator's discipline: advance accepts first, then one append
        nonlocal current, prev
        accepted = advance(current, {'body': body, 'prev_sha256': prev, 'type': type_})
        prev = journal.append(fd, type_, body, prev_sha256=prev)
        current = accepted
    try:
        assert current == State('NONE')
        for type_ in ('AUTHORITY_BOUND', 'PREPARED', 'PROBE_START', 'PROBE'):
            commit(type_, bodies()[type_])
        commit('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'IDLE'})
        assert current == State('HALTED', 'IDLE') == fold(journal.read(path, prev_sha256=None))
        before = path.read_bytes()
        with pytest.raises(state.IllegalTransition) as caught:
            commit('SEGMENT_START', segment_start(1, 2))
        assert caught.value.code == state.ILLEGAL_TRANSITION == 'ILLEGAL_TRANSITION'
        assert path.read_bytes() == before and current == State('HALTED', 'IDLE')
    finally:
        os.close(fd)
    # Twin: the same event is allowed from IDLE.
    assert advance(State('IDLE'), event('SEGMENT_START', segment_start(1, 2))) == State('RUNNING')

    # The whole §4.2 table, state x event (HALTED here halted from IDLE).
    for name in STATES:
        current = State(name, 'IDLE' if name == 'HALTED' else None)
        for type_, body in bodies().items():
            expected = DESIGN_TABLE.get((name, type_))
            if expected is None:
                with pytest.raises(state.IllegalTransition):
                    advance(current, event(type_, body))
            else:
                assert advance(current, event(type_, body)) == State(expected), (name, type_)
        halt = event('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': name})
        if name in ('BOUND', 'PREPARED', 'PROBING', 'IDLE'):
            assert advance(current, halt) == State('HALTED', name)
        else:
            with pytest.raises(state.IllegalTransition):
                advance(current, halt)
    running = State('RUNNING')
    for cls, cause, expected in (('HALTED', 'RESOURCE_EXHAUSTED', State('HALTED', 'IDLE')),
                                 ('TERMINAL', 'BUDGET_EXHAUSTED', State('TERMINAL')),
                                 ('COMPLETE', 'COMPLETE', State('COMPLETE')), ('STOPPED', 'IO_ERROR', State('IDLE'))):
        assert advance(running, event('SEGMENT_END', segment_end(1, 1, cls, cause))) == expected
    for refused in (event('SEGMENT_END', segment_end(1, 1, 'STOPPED', 'BUDGET_EXHAUSTED')),  # class differs from §4.3
                    event('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'BOUND'}),       # from differs from state
                    event('HALT', {'code': 'CORRUPTION', 'from': 'IDLE'}),                # a TERMINAL-class code
                    event('TERMINAL', {'code': 'WORKER_LOST'}),                           # a STOPPED-class code
                    event('KEY_START', {'key': list(PLAN[0])})):                          # a journal record
        with pytest.raises(state.IllegalTransition):
            advance(State('IDLE') if refused['type'] != 'SEGMENT_END' else running, refused)

    # O-6: ACT transitions (design §4.2 rows ACT{TERMINATE}, ACT{CONTINUE}; §4.5).
    act_cases = [
        (State('BOUND'), 'TERMINATE', State('TERMINAL')), (State('PREPARED'), 'TERMINATE', State('TERMINAL')),
        (State('IDLE'), 'TERMINATE', State('TERMINAL')), (State('HALTED', 'PROBING'), 'TERMINATE', State('TERMINAL')),
        (State('HALTED', 'IDLE'), 'CONTINUE', State('IDLE')), (State('HALTED', 'BOUND'), 'CONTINUE', State('BOUND')),
        (State('HALTED', 'PREPARED'), 'CONTINUE', State('PREPARED')),
        (State('HALTED', 'PROBING'), 'CONTINUE', State('PREPARED')),  # PROBING resumes as PREPARED
        (State('NONE'), 'TERMINATE', None), (State('PROBING'), 'TERMINATE', None),
        (State('RUNNING'), 'TERMINATE', None), (State('COMPLETE'), 'TERMINATE', None),
        (State('TERMINAL'), 'TERMINATE', None), (State('FINAL'), 'TERMINATE', None),
        (State('BOUND'), 'CONTINUE', None), (State('IDLE'), 'CONTINUE', None), (State('RUNNING'), 'CONTINUE', None),
    ]
    for current, act, expected in act_cases:
        record = event('ACT', {'act_sha256': hexd('act'), 'act': act})
        if expected is None:
            with pytest.raises(state.IllegalTransition):
                advance(current, record)
        else:
            assert advance(current, record) == expected, (current, act)


def test_S3(tmp_path):
    _, journal = modules()
    path = tmp_path / 'journal' / 's1-w0.jsonl'
    path.parent.mkdir()
    records = (('EPOCH_OPEN', epoch_open()), ('KEY_START', {'key': list(PLAN[0])}), ('PATH', path_body(PLAN[0])),
               ('KEY_START', {'key': list(PLAN[1])}))
    fd = os.open(path, APPEND, 0o644)
    try:
        prev = None
        for type_, body in records:
            prev = journal.append(fd, type_, body, prev_sha256=prev)
    finally:
        os.close(fd)
    data = path.read_bytes()
    lines = data.split(b'\n')[:-1]
    assert len(lines) == 4 and prev == sha(lines[-1])
    assert [r['type'] for r in journal.read(path, prev_sha256=None)] == [t for t, _ in records]

    path.write_bytes(b''.join(line + b'\n' for i, line in enumerate(lines) if i != 1))  # one record removed mid-file
    with pytest.raises(journal.JournalCorrupt) as caught:
        journal.read(path, prev_sha256=None)
    assert caught.value.code == 'CORRUPTION'
    for broken in (data, b'\n' + data):  # a wrong first link, and a blank line before it, are breaks too
        path.write_bytes(broken)
        with pytest.raises(journal.JournalCorrupt):
            journal.read(path, prev_sha256=hexd('elsewhere') if broken == data else None)
    ledger = tmp_path / 'ledger' / '0001.jsonl'  # a journal record in a ledger file is a break
    ledger.parent.mkdir()
    ledger.write_bytes(lines[0] + b'\n')
    with pytest.raises(journal.JournalCorrupt):
        journal.read(ledger, prev_sha256=None)

    # Twin: a torn final line (no LF) is dropped, and only it.
    path.write_bytes(data[:-7])
    assert [r['type'] for r in journal.read(path, prev_sha256=None)] == [t for t, _ in records[:3]]
    path.write_bytes(data + b'{"body":{"key"\n')  # an unparseable last line is torn too
    assert len(journal.read(path, prev_sha256=None)) == 4


def test_S9():
    state, journal = modules()
    from c1_rail.qualification.contract import ContractValidationError
    from c1_rail.qualification.replay import ReplayNeedsContext

    def worker(step):  # a fake worker loop: whatever escapes a key is classified
        try:
            step()
        except BaseException as exc:  # noqa: BLE001 - the classifier sees every escape
            return state.classify(exc)
        raise AssertionError('step did not fail')

    def divide():
        return 1 / 0
    assert worker(divide) == ('HALTED', 'UNCLASSIFIED_ERROR')
    assert state.classify(ValueError('SCREEN_SOMETHING_NEW: unlisted')) == ('HALTED', 'UNCLASSIFIED_ERROR')
    assert state.classify('SOMETHING_NEW') == ('HALTED', 'UNCLASSIFIED_ERROR')

    def raiser(exc):
        def step():
            raise exc
        return step
    listed = [  # twins: every §4.3 cause
        (ContractValidationError('SOURCE_APPROVAL_EXPIRED: approval is not valid at this time'),
         ('STOPPED', 'APPROVAL_LAPSE')),
        ('SCREEN_APPROVAL_EXPIRED', ('STOPPED', 'APPROVAL_LAPSE')),
        (ContractValidationError('SOURCE_KEY_REVOKED: signing key is revoked'), ('TERMINAL', 'SOURCE_KEY_LIFECYCLE')),
        ('SOURCE_KEY_CHANGED', ('TERMINAL', 'SOURCE_KEY_LIFECYCLE')),
        ('SOURCE_KEY_REMOVED', ('TERMINAL', 'SOURCE_KEY_LIFECYCLE')),
        (ReplayNeedsContext('no reviewed price'), ('TERMINAL', 'CONTEXT_REFUSAL')),
        (ValueError('CONTEXT_REFUSAL: short run'), ('TERMINAL', 'CONTEXT_REFUSAL')),
        ('INTRADAY_LOW_MISSING', ('TERMINAL', 'INTRADAY_LOW_MISSING')),
        ('CANDIDATES_UNAVAILABLE', ('TERMINAL', 'CANDIDATES_UNAVAILABLE')),
        ('PROBE_INCOMPLETE', ('TERMINAL', 'PROBE_INCOMPLETE')), ('PROBE_OVER_BUDGET', ('TERMINAL', 'PROBE_OVER_BUDGET')),
        ('BUDGET_EXHAUSTED', ('TERMINAL', 'BUDGET_EXHAUSTED')), ('NONDETERMINISM', ('TERMINAL', 'NONDETERMINISM')),
        (journal.JournalCorrupt('chain break'), ('TERMINAL', 'CORRUPTION')),
        ('CODE_OR_ARTIFACT_DRIFT', ('TERMINAL', 'CODE_OR_ARTIFACT_DRIFT')),
        ('OPERATOR_TERMINATED', ('TERMINAL', 'OPERATOR_TERMINATED')),
        (ValueError('SCREEN_EPOCH_STALE: stat guard changed'), ('STOPPED', 'TREE_CHANGED')),
        (OSError(28, 'No space left on device'), ('STOPPED', 'IO_ERROR')), ('IO_EXHAUSTED', ('HALTED', 'IO_EXHAUSTED')),
        (MemoryError(), ('STOPPED', 'WORKER_LOST')), ('RESOURCE_EXHAUSTED', ('HALTED', 'RESOURCE_EXHAUSTED')),
        (KeyboardInterrupt(), ('STOPPED', 'INTERRUPTED')),
        ('OVERHEAD_EXHAUSTED', ('HALTED', 'OVERHEAD_EXHAUSTED')), ('PROBE_INTERRUPTED', ('HALTED', 'PROBE_INTERRUPTED')),
    ]
    for cause, expected in listed:
        got = state.classify(cause) if isinstance(cause, str) else worker(raiser(cause))
        assert got == expected, cause
    # Non-deterministic causes reach only STOPPED or HALTED.
    for cause in (OSError(5, 'I/O error'), MemoryError(), KeyboardInterrupt(), TimeoutError()):
        assert state.classify(cause)[0] in ('STOPPED', 'HALTED')


def test_S10():
    kill = Seg(1, stop=0, end='CRASHED')
    key = PLAN[0]
    result = check(*simulate([kill, kill, Seg(1, stop=0, end='OPEN')]))
    assert result.code == 'RESOURCE_EXHAUSTED' and dict(result.losses) == {key: 3}
    # Twin: two kills are two losses, below the cap.
    result = check(*simulate([kill, Seg(1, stop=0, end='OPEN')]))
    assert result.code is None and dict(result.losses) == {key: 2}
    # An INTERRUPTED segment's in-flight key is not a loss.
    result = check(*simulate([kill, Seg(1, stop=0, end=('STOPPED', 'INTERRUPTED')), Seg(1, stop=0, end='OPEN')]))
    assert result.code is None and dict(result.losses) == {key: 2}
    # I/O branch: a third consecutive I/O-error segment with no new completed key HALTs.
    io = Seg(1, stop=0, end=('STOPPED', 'IO_ERROR'), name_inflight=True)
    result = check(*simulate([io, io, io]))
    assert result.code == 'IO_EXHAUSTED' and dict(result.losses) == {}
    # Twin: a new completed key in between resets the run of I/O errors.
    progress = Seg(1, stop=1, end=('STOPPED', 'IO_ERROR'), name_inflight=True)
    result = check(*simulate([io, progress, io]))
    assert result.code is None and result.completed == frozenset({key})


def test_S13():
    first = [Seg(2, stop=1, end=('STOPPED', 'WORKER_LOST')), Seg(2)]
    result = check(*simulate(first, outcome=lambda key, k: path_body(key, salt='divergent' if k == 2 else '')))
    assert result.code == 'NONDETERMINISM'
    # Twin: the witnesses re-execute identically (timing differs only) and are deduplicated.
    ledger, journals, m = simulate(first)
    result = check(ledger, journals, m)
    assert result.code is None and result.completed == frozenset(PLAN)
    _, journal = modules()
    assert len(journal.outcomes(journals, PLAN)) == len(PLAN)


def test_S14():
    outside = ('root-z', 'FULL', 0)
    assert check(*simulate([Seg(2)], inject={'s1-w0': [outside]})).code == 'CORRUPTION'
    # A plan key in another worker's assignment, not a tagged witness, is the same.
    assert check(*simulate([Seg(2)], inject={'s1-w0': [PLAN[1]]})).code == 'CORRUPTION'
    # Twin: plan keys in their own assignment, and tagged witnesses.
    result = check(*simulate([Seg(2, stop=1, end=('STOPPED', 'WORKER_LOST')), Seg(2)]))
    assert result.code is None and result.completed == frozenset(PLAN)


def test_S16(tmp_path):
    state, journal = modules()
    runs = {'w1': [Seg(1)], 'w4': [Seg(4)],
            'three_segments': [Seg(2, stop=2, end='CRASHED'), Seg(3, stop=2, end=('STOPPED', 'WORKER_LOST')), Seg(1)]}
    produced, rows = {}, {}
    for seed, (label, segments) in enumerate(runs.items()):
        ledger, journals, m = simulate(segments, seed=seed)
        ledger, journals = materialize(tmp_path / label, ledger, journals)
        assert state.fold(ledger) == state.State('COMPLETE')
        result = state.check_record(ledger, journals, m, {}, keys=PLAN)
        assert result.code is None and result.completed == frozenset(PLAN)
        rows[label] = journal.outcomes(journals, PLAN)
        produced[label] = journal.results(authority_sha256=AUTH, contract_sha256=m['contract_sha256'],
                                          p7_record_sha256=m['p7_record_sha256'], plan_sha256=m['plan_sha256'],
                                          verdict=synthetic_verdict(rows[label]))
    assert len(set(produced.values())) == 1 and len({canonical(list(r)) for r in rows.values()}) == 1
    sample = rows['w1']
    assert [tuple(r['key']) for r in sample] == list(PLAN) and not any({'wall_s', 'cpu_s'} & set(r) for r in sample)
    doc = json.loads(produced['w1'])
    assert canonical(doc) == produced['w1'] and doc['verdict'] == synthetic_verdict(sample)
    assert {'authority_sha256', 'contract_sha256', 'p7_record_sha256', 'plan_sha256', 'verdict'} <= set(doc)
    # Twin: the bytes do follow their inputs.
    other = journal.results(authority_sha256=hexd('other'), contract_sha256=hexd('r3c'), p7_record_sha256=hexd('p7'),
                            plan_sha256=hexd('plan'), verdict=synthetic_verdict(sample))
    assert other != produced['w1']


def test_B1(tmp_path):
    _, journal = modules()
    path = tmp_path / 'journal' / 's1-w0.jsonl'
    path.parent.mkdir()
    no_integrity = {k: v for k, v in epoch_open().items() if k != 'integrity'}
    fd = os.open(path, APPEND, 0o644)
    try:
        with pytest.raises(journal.JournalCorrupt) as caught:
            journal.append(fd, 'EPOCH_OPEN', no_integrity, prev_sha256=None)
        assert caught.value.code == 'CORRUPTION' and path.read_bytes() == b''
        journal.append(fd, 'EPOCH_OPEN', epoch_open(), prev_sha256=None)  # twin
    finally:
        os.close(fd)
    assert journal.read(path, prev_sha256=None)[0]['body'] == epoch_open()
    path.write_bytes(canonical({'body': no_integrity, 'prev_sha256': None, 'type': 'EPOCH_OPEN'}) + b'\n')
    with pytest.raises(journal.JournalCorrupt):  # parseable, so not torn: refused by the schema on read
        journal.read(path, prev_sha256=None)

    # Every other cost field is required too, and a Cost is exactly {cpu_s, wall_s}.
    full = {**bodies(), 'EPOCH_OPEN': epoch_open(), 'EPOCH_CLOSE': epoch_close(), 'PATH': path_body(PLAN[0]),
            'PROBE_RESULT': {'path_cpu_s': 1.0, 'path_wall_s': 1.0, 'peak_memory_bytes': 1}}
    missing = [('PREPARED', 'build'), ('PREPARED', 'integrity'), ('PROBE', 'path_cpu_s'), ('PROBE', 'path_wall_s'),
               ('HEARTBEAT', 'job_cpu_s'), ('HEARTBEAT', 'wall_s'), ('SEGMENT_END', 'job_cpu_s'),
               ('SEGMENT_END', 'path_cpu_s'), ('SEGMENT_END', 'overhead_cpu_s'), ('SEGMENT_CRASHED', 'charge'),
               ('EPOCH_OPEN', 'build'), ('EPOCH_CLOSE', 'integrity'), ('PATH', 'cpu_s'), ('PATH', 'wall_s'),
               ('PROBE_RESULT', 'path_cpu_s'), ('PROBE_RESULT', 'path_wall_s')]
    scratch = tmp_path / 'scratch.jsonl'
    fd = os.open(scratch, APPEND, 0o644)
    try:
        for type_, field in missing:
            with pytest.raises(journal.JournalCorrupt):
                journal.append(fd, type_, {k: v for k, v in full[type_].items() if k != field}, prev_sha256=None)
        with pytest.raises(journal.JournalCorrupt):
            journal.append(fd, 'EPOCH_OPEN', {**epoch_open(), 'integrity': {'cpu_s': 1.0}}, prev_sha256=None)
        assert scratch.read_bytes() == b''
        prev = None
        for type_, _ in missing:  # twins: the full bodies
            prev = journal.append(fd, type_, full[type_], prev_sha256=prev)
    finally:
        os.close(fd)
    assert len(journal.read(scratch, prev_sha256=None)) == len(missing)


def test_check_record_gap_after_complete():
    missing = PLAN[3]
    assert check(*simulate([Seg(2)], skip={missing})).code == 'CORRUPTION'
    ledger, journals, m = simulate([Seg(2, end=('STOPPED', 'WORKER_LOST'))], skip={missing})
    assert check(Chain(ledger).add('ALL_DONE', {}).records, journals, m).code == 'CORRUPTION'
    # Twin: the same gap before COMPLETE is no failure.
    result = check(ledger, journals, m)
    assert result.code is None and result.completed == frozenset(PLAN) - {missing}


def test_check_record_closure_agreement():  # O-8: K6's closure clause
    ledger, journals, m = simulate([Seg(2)])
    assert check(ledger, journals, m).code is None
    for index, field, value in ((0, 'closure_sha256', hexd('other closure')), (-2, 'closure_match', False)):
        records = [dict(r) for r in journals['s1-w1']]
        records[index] = {**records[index], 'body': {**records[index]['body'], field: value}}
        assert check(ledger, {**journals, 's1-w1': Chain(records).records}, m).code == 'CODE_OR_ARTIFACT_DRIFT'


def test_check_record_act_binding():  # X3: an act binds the authority and the ledger head it answers
    m = manifest()
    journals = {'c1-w0': candidate_journal(m)}
    halted = idle_ledger(m).add('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'IDLE'})

    def act_file(head, act='CONTINUE', authority=AUTH):
        raw = canonical({'act': act, 'authority_sha256': authority, 'ledger_head_sha256': head,
                         'readers': [{'exposure': 'not seen', 'name': 'coordinator (3)'}],
                         'schema': 't00_screen_act/v1', 'statement': 'continue'})
        container = canonical({'act_b64': base64.b64encode(raw).decode('ascii'),
                               'approval_b64': base64.b64encode(b'{}').decode('ascii')})
        return sha(raw), {sha(raw) + '.json': container}

    def run(head, **kwargs):
        act_sha, acts = act_file(head, **kwargs)
        ledger = Chain(halted.records).add('ACT', {'act_sha256': act_sha, 'act': 'CONTINUE'}).records
        return check(ledger, journals, m, acts)
    head = sha(canonical(halted.records[-1]))
    assert run(head).code is None  # twin
    assert run(sha(canonical(halted.records[-2]))).code == 'CORRUPTION'  # a stale ledger head
    assert run(head, authority=hexd('other')).code == 'CORRUPTION'
    assert run(head, act='TERMINATE').code == 'CORRUPTION'  # the file's act differs from the record's
    act_sha, _ = act_file(head)
    ledger = Chain(halted.records).add('ACT', {'act_sha256': act_sha, 'act': 'CONTINUE'}).records
    assert check(ledger, journals, m, {}).code == 'CORRUPTION'  # no act file


@pytest.mark.skipif(os.name != 'nt', reason='msvcrt byte-range lock (design §4.1)')
def test_read_lock_reads_content_under_the_held_byte(tmp_path):
    _, journal = modules()
    import msvcrt
    path = tmp_path / 'lock'
    binary = getattr(os, 'O_BINARY', 0)
    fd = os.open(path, os.O_RDWR | os.O_CREAT | binary, 0o644)
    try:
        os.lseek(fd, journal.LOCK_OFFSET, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, canonical({'host': socket.gethostname(), 'pid': os.getpid(), 'schema': 't00_screen_lock/v1'}))
        assert journal.read_lock(path) == (os.getpid(), socket.gethostname())
        other = os.open(path, os.O_RDWR | binary)
        try:
            os.lseek(other, journal.LOCK_OFFSET, os.SEEK_SET)
            with pytest.raises(OSError):
                msvcrt.locking(other, msvcrt.LK_NBLCK, 1)
        finally:
            os.close(other)
        os.lseek(fd, journal.LOCK_OFFSET, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    finally:
        os.close(fd)
    path.write_bytes(canonical({'host': 'h', 'pid': 1, 'schema': 't00_screen_lock/v0'}))
    with pytest.raises(journal.JournalCorrupt):
        journal.read_lock(path)
