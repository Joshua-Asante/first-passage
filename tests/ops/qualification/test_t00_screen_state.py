"""T00 screen run state and journal: rows S1, S3, S9, S10, S13, S14, S16 and B1.

Design 2026-10-02 §4 (persistence, the §4.2 transition table, the §4.3 stop classes) and
build card §3.4-§3.6a at 40080aa (packet P-D): the O-6 ACT case table under ``test_S1``, the
O-8 closure, O-11 gap and X3 act clauses of ``check_record``, and the freeze F1-F8. Synthetic
records only: no source, key, probe or Monte Carlo. Each test imports the modules under test
in its own body, so each row fails on its own before they exist (card §2.2, F7).
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import errno
import functools
import hashlib
import importlib
import json
import os
import random
import socket
from types import MappingProxyType

import pytest

from c1_rail.qualification.contract import ContractValidationError
from c1_rail.qualification.contract import canonical_json_bytes as canonical
from c1_rail.qualification.replay import ReplayNeedsContext

ROOTS = ('root-a', 'root-b')
POPULATIONS = ('FULL', 'H1', 'H2')
STATUSES = ('PASS', 'FAILURE', 'UNDETERMINED')
PLAN = tuple(sorted((root, population, index)
                    for root in ROOTS for population in POPULATIONS for index in range(2)))
BINARY = getattr(os, 'O_BINARY', 0)
APPEND = os.O_WRONLY | os.O_APPEND | os.O_CREAT | BINARY
STATES = ('NONE', 'BOUND', 'PREPARED', 'PROBING', 'IDLE', 'RUNNING', 'HALTED', 'COMPLETE',
          'TERMINAL', 'AGGREGATED', 'REPORTED', 'FINAL')
WORKER_LOST = ('STOPPED', 'WORKER_LOST')
IO_ERROR = ('STOPPED', 'IO_ERROR')
OUTSIDE = ('root-z', 'FULL', 0)


def modules():
    """The modules under test, imported late so each row test fails alone (card §2.2)."""
    package = 'c1_rail.qualification.t00_screen.'
    return importlib.import_module(package + 'state'), importlib.import_module(package + 'journal')


def sha(raw):
    """SHA-256 hex of bytes."""
    return hashlib.sha256(raw).hexdigest()


def hexd(label):
    """A stand-in SHA-256 named by a label."""
    return sha(label.encode())


AUTH = hexd('authority')
CLOSURE = hexd('closure')


def cost(cpu=1.0, wall=1.25):
    """A Cost body field."""
    return {'cpu_s': cpu, 'wall_s': wall}


def epoch_open(closure=CLOSURE):
    """An EPOCH_OPEN body."""
    return {'build': cost(170.0, 200.0), 'integrity': cost(71.0, 80.0), 'closure_sha256': closure,
            'guard_sha256': hexd('guard')}


def epoch_close(match=True):
    """An EPOCH_CLOSE body."""
    return {'integrity': cost(71.0, 80.0), 'closure_match': match}


def run_body(tag, status, salt=''):
    """One PATH run as ``model.PathOutcome`` allows it, with P7's projection names."""
    passed = status == 'PASS'
    return {'digest': hexd(tag + salt), 'sessions': 30, 'fills': 4,
            'events_sha256': hexd(tag + 'ev'), 'deadline_failure': False,
            'consumed_intrabar_split_count': 0,
            'consumed_intrabar_splits_sha256': sha(canonical([])), 'status': status,
            'sessions_to_pass': 12 if passed else None,
            'failure_reason': None if passed else 'bust_trailing',
            'kernel_outcome': 'pass' if passed else 'bust_trailing'}


def path_body(key, *, cpu=2.0, wall=3.0, salt='', statuses=None):
    """A PATH body whose outcome is a pure function of the key (and ``salt``)."""
    tag = repr(key)
    status = STATUSES[int(hexd(tag)[:2], 16) % 3]
    if statuses is None:
        statuses = (status, status) if status != 'UNDETERMINED' else ('PASS', 'FAILURE')
    first, second = statuses
    return {'key': list(key), 'seed': int(hexd(tag)[:16], 16), 'path_sha256': hexd(tag + 'path'),
            'bracket_status': first if first == second else 'UNDETERMINED',
            'runs': {'r1': run_body(tag + 'r1', first, salt),
                     'r2': run_body(tag + 'r2', second, salt)},
            'wall_s': wall, 'cpu_s': cpu}


class Chain:
    """Records chained as card §3.4 defines a line (its SHA-256 is that of the line without LF)."""

    def __init__(self, records=()):
        self.records = []
        for record in records:
            self.add(record['type'], record['body'])

    def add(self, type_, body):
        """Append one record chained to the last."""
        prev = sha(canonical(self.records[-1])) if self.records else None
        self.records.append({'body': body, 'prev_sha256': prev, 'type': type_})
        return self


def edit(records, type_, pick=lambda body: True, **fields):
    """The records re-chained, with ``fields`` replaced in each picked body of ``type_``."""
    return Chain([{**r, 'body': {**r['body'], **fields}}
                  if r['type'] == type_ and pick(r['body']) else r for r in records]).records


def manifest():
    """A manifest with the §3.4 keys."""
    populations = {p: {'indices': [0, 2, 5], 'candidates_sha256': hexd('candidates' + p)}
                   for p in POPULATIONS}
    return {'authority_sha256': AUTH, 'contract_sha256': hexd('r3c'),
            'p7_record_sha256': hexd('p7'), 'code_head': 'c' * 40,
            'populations': populations, 'plan_sha256': hexd('plan')}


def bound_body():
    """An AUTHORITY_BOUND body."""
    return {'authority_sha256': AUTH, 'prereg_path': 'docs/briefs/pre-registration/prereg.md',
            'approvals': [hexd('r3c-approval'), hexd('screen-approval')], 'reused_directory': False}


def idle_ledger(m):
    """The ledger up to IDLE: bound, prepared under ``m`` (F5 digest), probed."""
    return (Chain().add('AUTHORITY_BOUND', bound_body())
            .add('PREPARED', {'manifest_sha256': sha(canonical(m)), 'build': cost(),
                              'integrity': cost()})
            .add('PROBE_START', {})
            .add('PROBE', {'path_cpu_s': 136.0, 'path_wall_s': 170.0,
                           'peak_memory_bytes': 600 << 20}))


def candidate_journal(m):
    """The candidate-and-probe worker's journal ``c1-w0``."""
    probe = {'path_cpu_s': 136.0, 'path_wall_s': 170.0, 'peak_memory_bytes': 600 << 20}
    return (Chain().add('EPOCH_OPEN', epoch_open())
            .add('CANDIDATES', {'populations': m['populations']})
            .add('EPOCH_CLOSE', epoch_close()).add('EPOCH_OPEN', epoch_open())
            .add('PROBE_RESULT', probe).add('EPOCH_CLOSE', epoch_close())
            .add('WORKER_STOP', {'reason': 'DONE', 'key': None})).records


def shares_of(remaining, w):
    """F3: worker i receives ``remaining[i::w]``."""
    return [remaining[i::w] for i in range(w)]


def assignment_sha256(shares):
    """F3: SHA-256 of canonical ``[[i, [key, ...]], ...]``."""
    return sha(canonical([[i, [list(key) for key in share]] for i, share in enumerate(shares)]))


def segment_start(k, w, witnesses=(), shares=None):
    """A SEGMENT_START body."""
    return {'k': k, 'w': w, 'assignment_sha256': assignment_sha256(shares or [[]] * w),
            'witness_keys': [list(key) for key in witnesses], 'approvals': [hexd('r3c-approval')]}


def segment_end(k, w, cls, cause, reasons=None):
    """A SEGMENT_END body; ``reasons`` are the workers' (default: the cause for each)."""
    reasons = reasons or (cause,) * w
    return {'class': cls, 'cause': cause,
            'workers': [{'worker': f's{k}-w{i}', 'reason': reason}
                        for i, reason in enumerate(reasons)],
            'wall_s': 10.0, 'job_cpu_s': 40.0, 'path_cpu_s': 30.0, 'overhead_cpu_s': 10.0,
            'peak_memory_bytes': 600 << 20}


def act_file(head, act='CONTINUE', authority=AUTH):
    """(act SHA-256, {file name: canonical {act_b64, approval_b64}}) for a signed act (F5)."""
    raw = canonical({'act': act, 'authority_sha256': authority, 'ledger_head_sha256': head,
                     'readers': [{'exposure': 'not seen', 'name': 'coordinator (3)'}],
                     'schema': 't00_screen_act/v1', 'statement': 'continue'})
    container = canonical({'act_b64': base64.b64encode(raw).decode('ascii'),
                           'approval_b64': base64.b64encode(b'{}').decode('ascii')})
    return sha(raw), {sha(raw) + '.json': container}


@dataclass(frozen=True)
class Seg:
    """One segment of ``simulate``."""
    w: int
    stop: int | None = None         # keys each worker completes before it stops; None: all
    end: object = 'COMPLETE'        # 'COMPLETE', 'CRASHED', 'OPEN' (not resumed) or (class, cause)
    name_inflight: object = None    # WORKER_STOP reason naming the in-flight key (no loss);
                                    # a tuple gives one per worker, None leaving it in flight
    reasons: tuple | None = None    # SEGMENT_END workers[].reason
    witnesses: tuple | None = None  # SEGMENT_START witness_keys override
    rerun: bool = True              # worker i re-executes witness i first (F2)
    cap: str | None = None          # the cap its SEGMENT_CRASHED records (F1)


@dataclass(frozen=True)
class Act:
    """Joshua's signed act, appended at resume and bound to the ledger head (X3)."""
    act: str = 'CONTINUE'


@dataclass(frozen=True)
class Halt:
    """HALT{code, from: IDLE}, appended at resume (F8's second cap)."""
    code: str


def run_segment(k, seg, done, *, keys, outcome, inject, skip):
    """One segment: (SEGMENT_START body, its journals, keys lost in flight)."""
    remaining = [key for key in sorted(keys) if key not in done]
    shares = shares_of(remaining, seg.w)
    tagged = sorted(done)[:min(seg.w, len(done))] if seg.witnesses is None else seg.witnesses
    witnesses = list(tagged)
    journals, lost = {}, []
    for i in range(seg.w):
        name = f's{k}-w{i}.jsonl'
        first = witnesses[i:i + 1] if seg.rerun else []
        todo = [key for key in first + shares[i] + list(inject.get(name, ())) if key not in skip]
        n = len(todo) if seg.stop is None else min(seg.stop, len(todo))
        journal = Chain().add('EPOCH_OPEN', epoch_open())
        for key in todo[:n]:
            journal.add('KEY_START', {'key': list(key)}).add('PATH', outcome(key, k))
            if key not in done:
                done.append(key)
        if n == len(todo):
            journal.add('EPOCH_CLOSE', epoch_close())
            journal.add('WORKER_STOP', {'reason': 'DONE', 'key': None})
        elif named := (seg.name_inflight[i] if isinstance(seg.name_inflight, tuple)
                       else seg.name_inflight):
            journal.add('KEY_START', {'key': list(todo[n])})
            journal.add('WORKER_STOP', {'reason': named, 'key': list(todo[n])})
        else:
            journal.add('KEY_START', {'key': list(todo[n])})
            lost.append(list(todo[n]))
        journals[name] = journal.records
    return segment_start(k, seg.w, witnesses, shares), journals, sorted(lost)


def simulate(steps, *, keys=PLAN, outcome=None, inject=None, skip=(), seed=0):
    """A driver stand-in: (ledger, journals, manifest, acts). Each segment re-partitions
    K - completed round-robin (F3), worker i first re-executes witness i (F2, row S13), and every
    PATH follows its fsync'd KEY_START (row S10). A crashed segment's SEGMENT_CRASHED, with the
    segment's ``cap`` (F1), is written at resume: before the next step, or at the end."""
    rng = random.Random(seed)
    outcome = outcome or (lambda key, k: path_body(key, cpu=rng.uniform(100, 200),
                                                   wall=rng.uniform(100, 300)))
    m = manifest()
    ledger, journals, acts = idle_ledger(m), {'c1-w0.jsonl': candidate_journal(m)}, {}
    done, crashed, k = [], [], 0

    def resume():
        for number, lost, cap in crashed:
            ledger.add('SEGMENT_CRASHED', {'k': number, 'charge': cost(50.0, 60.0),
                                           'losses': lost, 'cap': cap})
        crashed.clear()
    for step in steps:
        resume()
        if isinstance(step, Act):
            act_sha, files = act_file(sha(canonical(ledger.records[-1])), step.act)
            ledger.add('ACT', {'act_sha256': act_sha, 'act': step.act})
            acts.update(files)
            continue
        if isinstance(step, Halt):
            ledger.add('HALT', {'code': step.code, 'from': 'IDLE'})
            continue
        k += 1
        start, segment, lost = run_segment(k, step, done, keys=keys, outcome=outcome,
                                           inject=inject or {}, skip=skip)
        ledger.add('SEGMENT_START', start)
        journals.update(segment)
        if step.end == 'CRASHED':
            crashed.append((k, lost, step.cap))
        elif step.end != 'OPEN':
            cls, cause = ('COMPLETE', 'COMPLETE') if step.end == 'COMPLETE' else step.end
            ledger.add('SEGMENT_END', segment_end(k, step.w, cls, cause, step.reasons))
    resume()
    return ledger.records, journals, m, acts


def verified_run(listed, ran):
    """A finalized W = 2 run with ``verify`` 1 listing ``listed`` and its worker 0 re-running
    ``ran``: (ledger, journals with c1-w0, s1-w0, s1-w1 and v1-w0, manifest, acts)."""
    ledger, journals, m, acts = simulate([Seg(2)])
    final = Chain(ledger)
    for type_ in ('AGGREGATED', 'REPORTED', 'FINAL'):
        final.add(type_, bodies()[type_])
    keys = [list(key) for key in listed]
    final.add('VERIFY_START', {'n': 1, 'keys': keys})
    final.add('VERIFY', {'n': 1, 'keys': keys, 'match': True})
    journal = Chain().add('EPOCH_OPEN', epoch_open())
    for key in ran:
        journal.add('KEY_START', {'key': list(key)}).add('PATH', path_body(key, cpu=9.0))
    journal.add('EPOCH_CLOSE', epoch_close())
    journal.add('WORKER_STOP', {'reason': 'DONE', 'key': None})
    return final.records, {**journals, 'v1-w0.jsonl': journal.records}, m, acts


def check(ledger, journals, m, acts=None, keys=PLAN):
    """``state.check_record`` over a simulated run."""
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
    read_journals = {path.name: journal.read(path, prev_sha256=None)
                     for path in (run_dir / 'journal').iterdir()}
    assert read_ledger == list(ledger)
    assert {k: list(v) for k, v in read_journals.items()} == journals
    return read_ledger, read_journals


def synthetic_verdict(rows):
    """Stand-in for ``verdict.as_json`` (card §3.7 shape); P-C's module is never imported."""
    tallies = {p: {s: 0 for s in STATUSES} for p in POPULATIONS}
    for row in rows:
        tallies[row['key'][1]][row['bracket_status']] += 1
    return {'kind': 'LABELLED', 'label': 'NO-GO-evidence-UNDETERMINED-dependent',
            'tallies': {'pessimistic': tallies, 'optimistic': tallies},
            'descriptive': {p: {'consumed_split_paths': 0,
                                'undetermined_paths': tallies[p]['UNDETERMINED']}
                            for p in POPULATIONS}}


def event(type_, body):
    """An unchained ledger event."""
    return {'body': body, 'prev_sha256': None, 'type': type_}


def bodies():
    """One valid body per ledger event type (card §3.5); HALT and ACT are tabulated apart."""
    return {
        'AUTHORITY_BOUND': bound_body(),
        'PREPARED': {'manifest_sha256': hexd('manifest'), 'build': cost(), 'integrity': cost()},
        'PROBE_START': {}, 'PROBE': {'path_cpu_s': 1.0, 'path_wall_s': 1.0, 'peak_memory_bytes': 1},
        'SEGMENT_START': segment_start(1, 2), 'HEARTBEAT': {'wall_s': 60.0, 'job_cpu_s': 400.0},
        'SEGMENT_END': segment_end(1, 2, 'STOPPED', 'WORKER_LOST'),
        'SEGMENT_CRASHED': {'k': 1, 'charge': cost(), 'losses': [], 'cap': None},
        'ALL_DONE': {},
        'TERMINAL': {'code': 'BUDGET_EXHAUSTED'}, 'AGGREGATED': {'results_sha256': hexd('results')},
        'REPORTED': {'report_sha256': hexd('report')},
        'FINAL': {'attestation_sha256': hexd('attestation')},
        'VERIFY_START': {'n': 1, 'keys': [list(PLAN[0])]},
        'VERIFY': {'n': 1, 'keys': [list(PLAN[0])], 'match': True},
    }


# Design §4.2, (from, event) -> to, for every event except HALT and ACT.
DESIGN_TABLE = {
    ('NONE', 'AUTHORITY_BOUND'): 'BOUND', ('BOUND', 'PREPARED'): 'PREPARED',
    ('PREPARED', 'PROBE_START'): 'PROBING', ('PROBING', 'PROBE'): 'IDLE',
    ('IDLE', 'SEGMENT_START'): 'RUNNING', ('IDLE', 'ALL_DONE'): 'COMPLETE',
    ('RUNNING', 'HEARTBEAT'): 'RUNNING', ('RUNNING', 'SEGMENT_END'): 'IDLE',
    ('RUNNING', 'SEGMENT_CRASHED'): 'IDLE',
    ('COMPLETE', 'AGGREGATED'): 'AGGREGATED', ('TERMINAL', 'AGGREGATED'): 'AGGREGATED',
    ('AGGREGATED', 'REPORTED'): 'REPORTED', ('REPORTED', 'FINAL'): 'FINAL',
    ('FINAL', 'VERIFY_START'): 'FINAL', ('FINAL', 'VERIFY'): 'FINAL',
    **{(name, 'TERMINAL'): 'TERMINAL' for name in STATES
       if name not in ('NONE', 'RUNNING', 'FINAL')},
}
# O-6: ACT transitions (design §4.2 rows ACT{TERMINATE}, ACT{CONTINUE}; §4.5); None is refused.
ACT_CASES = (
    (('BOUND', None), 'TERMINATE', ('TERMINAL', None)),
    (('PREPARED', None), 'TERMINATE', ('TERMINAL', None)),
    (('IDLE', None), 'TERMINATE', ('TERMINAL', None)),
    (('HALTED', 'PROBING'), 'TERMINATE', ('TERMINAL', None)),
    (('HALTED', 'IDLE'), 'CONTINUE', ('IDLE', None)),
    (('HALTED', 'BOUND'), 'CONTINUE', ('BOUND', None)),
    (('HALTED', 'PREPARED'), 'CONTINUE', ('PREPARED', None)),
    (('HALTED', 'PROBING'), 'CONTINUE', ('PREPARED', None)),  # PROBING resumes as PREPARED
    *((((name, None), 'TERMINATE', None) for name in ('NONE', 'PROBING', 'RUNNING', 'COMPLETE',
                                                       'TERMINAL', 'FINAL'))),
    *((((name, None), 'CONTINUE', None) for name in ('BOUND', 'IDLE', 'RUNNING'))),
)


def test_S1(tmp_path):
    """Row S1: SEGMENT_START from HALTED is ILLEGAL_TRANSITION and writes nothing; the whole
    §4.2 table, the O-6 ACT cases and F5's ACT-only OPERATOR_TERMINATED."""
    state, journal = modules()
    path = tmp_path / 'ledger' / '0001.jsonl'
    path.parent.mkdir()
    fd = os.open(path, APPEND, 0o644)
    current, prev = state.fold(()), None

    def commit(type_, body):  # the coordinator's discipline: advance accepts first, then append
        nonlocal current, prev
        accepted = state.advance(current, {'body': body, 'prev_sha256': prev, 'type': type_})
        prev = journal.append(fd, type_, body, prev_sha256=prev)
        current = accepted
    try:
        assert current == state.State('NONE')
        for type_ in ('AUTHORITY_BOUND', 'PREPARED', 'PROBE_START', 'PROBE'):
            commit(type_, bodies()[type_])
        commit('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'IDLE'})
        halted = state.State('HALTED', 'IDLE')
        assert current == halted == state.fold(journal.read(path, prev_sha256=None))
        before = path.read_bytes()
        with pytest.raises(state.IllegalTransition) as caught:
            commit('SEGMENT_START', segment_start(1, 2))
        assert caught.value.code == state.ILLEGAL_TRANSITION == 'ILLEGAL_TRANSITION'
        assert path.read_bytes() == before and current == halted
    finally:
        os.close(fd)
    # Twin: the same event is allowed from IDLE.
    start = event('SEGMENT_START', segment_start(1, 2))
    assert state.advance(state.State('IDLE'), start) == state.State('RUNNING')
    assert_design_table(state, journal)
    for (name, halted_from), act, expected in ACT_CASES:
        record = event('ACT', {'act_sha256': hexd('act'), 'act': act})
        if expected is None:
            with pytest.raises(state.IllegalTransition):
                state.advance(state.State(name, halted_from), record)
        else:
            assert state.advance(state.State(name, halted_from), record) == state.State(*expected)
    # F5: ACT{TERMINATE} alone carries OPERATOR_TERMINATED; no TERMINAL record names it.
    for name in STATES:
        with pytest.raises(state.IllegalTransition):
            state.advance(state.State(name, 'IDLE' if name == 'HALTED' else None),
                          event('TERMINAL', {'code': 'OPERATOR_TERMINATED'}))


def assert_design_table(state, journal):
    """Every state x event of design §4.2 (HALTED here halted from IDLE)."""
    for name in STATES:
        current = state.State(name, 'IDLE' if name == 'HALTED' else None)
        for type_, body in bodies().items():
            expected = DESIGN_TABLE.get((name, type_))
            if expected is None:
                with pytest.raises(state.IllegalTransition):
                    state.advance(current, event(type_, body))
            else:
                assert state.advance(current, event(type_, body)) == state.State(expected)
        halt = event('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': name})
        if name in ('BOUND', 'PREPARED', 'PROBING', 'IDLE'):
            assert state.advance(current, halt) == state.State('HALTED', name)
        else:
            with pytest.raises(state.IllegalTransition):
                state.advance(current, halt)
    running = state.State('RUNNING')
    for cls, cause, expected in (('HALTED', 'RESOURCE_EXHAUSTED', ('HALTED', 'IDLE')),
                                 ('TERMINAL', 'BUDGET_EXHAUSTED', ('TERMINAL', None)),
                                 ('COMPLETE', 'COMPLETE', ('COMPLETE', None)),
                                 ('STOPPED', 'IO_ERROR', ('IDLE', None))):
        end = event('SEGMENT_END', segment_end(1, 1, cls, cause))
        assert state.advance(running, end) == state.State(*expected)
    for cap in ('RESOURCE_EXHAUSTED', 'IO_EXHAUSTED'):  # F1: one record, HALTED from IDLE
        crashed = event('SEGMENT_CRASHED', {'k': 1, 'charge': cost(), 'losses': [], 'cap': cap})
        assert state.advance(running, crashed) == state.State('HALTED', 'IDLE')
        with pytest.raises(state.IllegalTransition):
            state.advance(state.State('IDLE'), crashed)
    with pytest.raises(journal.JournalCorrupt):  # a cap outside row S10's two
        state.advance(running, event('SEGMENT_CRASHED', {'k': 1, 'charge': cost(), 'losses': [],
                                                         'cap': 'OVERHEAD_EXHAUSTED'}))
    refused = ((running, 'SEGMENT_END', segment_end(1, 1, 'STOPPED', 'BUDGET_EXHAUSTED')),  # §4.3
               (state.State('IDLE'), 'HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'BOUND'}),
               (state.State('IDLE'), 'HALT', {'code': 'CORRUPTION', 'from': 'IDLE'}),
               (state.State('IDLE'), 'TERMINAL', {'code': 'WORKER_LOST'}),
               (state.State('IDLE'), 'KEY_START', {'key': list(PLAN[0])}))  # a journal record
    for current, type_, body in refused:
        with pytest.raises(state.IllegalTransition):
            state.advance(current, event(type_, body))


def test_S3(tmp_path):
    """Row S3: a record removed mid-file is CORRUPTION; twin: a torn final line is dropped."""
    _, journal = modules()
    path = tmp_path / 'journal' / 's1-w0.jsonl'
    path.parent.mkdir()
    records = (('EPOCH_OPEN', epoch_open()), ('KEY_START', {'key': list(PLAN[0])}),
               ('PATH', path_body(PLAN[0])), ('KEY_START', {'key': list(PLAN[1])}))
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

    path.write_bytes(b''.join(line + b'\n' for i, line in enumerate(lines) if i != 1))
    with pytest.raises(journal.JournalCorrupt) as caught:
        journal.read(path, prev_sha256=None)
    assert caught.value.code == 'CORRUPTION'
    for broken, first in ((data, hexd('elsewhere')), (b'\n' + data, None)):
        path.write_bytes(broken)  # a wrong first link, and a blank line before it, are breaks
        with pytest.raises(journal.JournalCorrupt):
            journal.read(path, prev_sha256=first)
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
    """Row S9: an unlisted exception is (HALTED, UNCLASSIFIED_ERROR); twins: every §4.3 cause."""
    state, journal = modules()

    def worker(step):  # a fake worker loop: whatever escapes a key is classified
        try:
            step()
        except BaseException as exc:  # pylint: disable=broad-exception-caught
            return state.classify(exc)
        raise AssertionError('step did not fail')

    def raiser(exc):
        def step():
            raise exc
        return step
    assert worker(raiser(ZeroDivisionError('division by zero'))) == ('HALTED', 'UNCLASSIFIED_ERROR')
    assert state.classify(ValueError('SCREEN_SOMETHING_NEW: x')) == ('HALTED', 'UNCLASSIFIED_ERROR')
    assert state.classify('SOMETHING_NEW') == ('HALTED', 'UNCLASSIFIED_ERROR')
    error = ContractValidationError
    listed = [
        (error('SOURCE_APPROVAL_EXPIRED: approval is not valid at this time'),
         ('STOPPED', 'APPROVAL_LAPSE')),
        ('SCREEN_APPROVAL_EXPIRED', ('STOPPED', 'APPROVAL_LAPSE')),
        (error('SOURCE_KEY_REVOKED: signing key is revoked'), ('TERMINAL', 'SOURCE_KEY_LIFECYCLE')),
        ('SOURCE_KEY_CHANGED', ('TERMINAL', 'SOURCE_KEY_LIFECYCLE')),
        ('SOURCE_KEY_REMOVED', ('TERMINAL', 'SOURCE_KEY_LIFECYCLE')),
        (ReplayNeedsContext('no reviewed price'), ('TERMINAL', 'CONTEXT_REFUSAL')),
        (ValueError('CONTEXT_REFUSAL: short run'), ('TERMINAL', 'CONTEXT_REFUSAL')),
        ('INTRADAY_LOW_MISSING', ('TERMINAL', 'INTRADAY_LOW_MISSING')),
        ('CANDIDATES_UNAVAILABLE', ('TERMINAL', 'CANDIDATES_UNAVAILABLE')),
        ('PROBE_INCOMPLETE', ('TERMINAL', 'PROBE_INCOMPLETE')),
        ('PROBE_OVER_BUDGET', ('TERMINAL', 'PROBE_OVER_BUDGET')),
        ('BUDGET_EXHAUSTED', ('TERMINAL', 'BUDGET_EXHAUSTED')),
        ('NONDETERMINISM', ('TERMINAL', 'NONDETERMINISM')),
        (journal.JournalCorrupt('chain break'), ('TERMINAL', 'CORRUPTION')),
        ('CODE_OR_ARTIFACT_DRIFT', ('TERMINAL', 'CODE_OR_ARTIFACT_DRIFT')),
        ('OPERATOR_TERMINATED', ('TERMINAL', 'OPERATOR_TERMINATED')),
        (ValueError('SCREEN_EPOCH_STALE: stat guard changed'), ('STOPPED', 'TREE_CHANGED')),
        (OSError(28, 'No space left on device'), ('STOPPED', 'IO_ERROR')),
        ('IO_EXHAUSTED', ('HALTED', 'IO_EXHAUSTED')),
        (MemoryError(), ('STOPPED', 'WORKER_LOST')),
        ('RESOURCE_EXHAUSTED', ('HALTED', 'RESOURCE_EXHAUSTED')),
        (KeyboardInterrupt(), ('STOPPED', 'INTERRUPTED')),
        ('OVERHEAD_EXHAUSTED', ('HALTED', 'OVERHEAD_EXHAUSTED')),
        ('PROBE_INTERRUPTED', ('HALTED', 'PROBE_INTERRUPTED')),
    ]
    for cause, expected in listed:
        got = state.classify(cause) if isinstance(cause, str) else worker(raiser(cause))
        assert got == expected, cause
    # Non-deterministic causes reach only STOPPED or HALTED.
    for cause in (OSError(5, 'I/O error'), MemoryError(), KeyboardInterrupt(), TimeoutError()):
        assert state.classify(cause)[0] in ('STOPPED', 'HALTED')


def test_S10():
    """Row S10: a third loss of one key is RESOURCE_EXHAUSTED; a third I/O segment without a new
    completed key is IO_EXHAUSTED, counted from the cause or any worker's reason."""
    kill = Seg(1, stop=0, end='CRASHED')
    key = PLAN[0]
    result = check(*simulate([kill, kill, Seg(1, stop=0, end='OPEN')]))
    assert result.code == 'RESOURCE_EXHAUSTED' and dict(result.losses) == {key: 3}
    # Twin: two kills are two losses, below the cap.
    result = check(*simulate([kill, Seg(1, stop=0, end='OPEN')]))
    assert result.code is None and dict(result.losses) == {key: 2}
    # An INTERRUPTED segment's in-flight key is not a loss.
    interrupted = Seg(1, stop=0, end=('STOPPED', 'INTERRUPTED'))
    result = check(*simulate([kill, interrupted, Seg(1, stop=0, end='OPEN')]))
    assert result.code is None and dict(result.losses) == {key: 2}
    # I/O branch: a third consecutive I/O-error segment with no new completed key HALTs.
    io = Seg(1, stop=0, end=IO_ERROR, name_inflight='IO_ERROR')
    io_cap = Seg(1, stop=0, end=('HALTED', 'IO_EXHAUSTED'), name_inflight='IO_ERROR')
    result = check(*simulate([io, io, io_cap]))
    assert result.code == 'IO_EXHAUSTED' and not result.losses
    # Twin: a new completed key resets the run (two I/O segments, progress, one more).
    progress = Seg(1, stop=1, end=IO_ERROR, name_inflight='IO_ERROR')
    result = check(*simulate([io, io, progress, io]))
    assert result.code is None and result.completed == frozenset({key})
    # One worker's IO_ERROR counts when another worker's cause is the one recorded.
    mixed = Seg(2, stop=0, end=WORKER_LOST, name_inflight='WORKER_LOST',
                reasons=('IO_ERROR', 'WORKER_LOST'))
    mixed_cap = Seg(2, stop=0, end=('HALTED', 'IO_EXHAUSTED'), name_inflight='WORKER_LOST',
                    reasons=('IO_ERROR', 'WORKER_LOST'))
    assert check(*simulate([mixed, mixed, mixed_cap])).code == 'IO_EXHAUSTED'
    lost = Seg(2, stop=0, end=WORKER_LOST, name_inflight='WORKER_LOST')
    assert check(*simulate([lost, lost, lost])).code is None


def test_S13():
    """Row S13: a divergent duplicate (a witness re-executed differently, W5) is NONDETERMINISM."""
    first = [Seg(2, stop=1, end=WORKER_LOST), Seg(2)]

    def divergent(key, k):
        return path_body(key, salt='divergent' if k == 2 else '')
    assert check(*simulate(first, outcome=divergent)).code == 'NONDETERMINISM'
    # Twin: the witnesses re-execute identically (timing differs only) and are deduplicated.
    ledger, journals, m, acts = simulate(first)
    result = check(ledger, journals, m, acts)
    assert result.code is None and result.completed == frozenset(PLAN)
    _, journal = modules()
    assert len(journal.outcomes(journals, PLAN)) == len(PLAN)


def test_S14():
    """Row S14: a key outside the plan, or outside its worker's assignment and not a tagged
    witness, is CORRUPTION."""
    assert check(*simulate([Seg(2)], inject={'s1-w0.jsonl': [OUTSIDE]})).code == 'CORRUPTION'
    assert check(*simulate([Seg(2)], inject={'s1-w0.jsonl': [PLAN[1]]})).code == 'CORRUPTION'
    # Twin: plan keys in their own assignment, and tagged witnesses.
    result = check(*simulate([Seg(2, stop=1, end=WORKER_LOST), Seg(2)]))
    assert result.code is None and result.completed == frozenset(PLAN)


def test_S16(tmp_path):
    """Row S16: W = 1, W = 4 and a three-segment run give byte-identical ``results.json``."""
    state, journal = modules()
    runs = {'w1': [Seg(1)], 'w4': [Seg(4)],
            'three_segments': [Seg(2, stop=2, end='CRASHED'), Seg(3, stop=2, end=WORKER_LOST),
                               Seg(1)]}
    produced, rows = {}, {}
    for seed, (label, segments) in enumerate(runs.items()):
        ledger, journals, m, acts = simulate(segments, seed=seed)
        ledger, journals = materialize(tmp_path / label, ledger, journals)
        assert state.fold(ledger) == state.State('COMPLETE')
        result = state.check_record(ledger, journals, m, acts, keys=PLAN)
        assert result.code is None and result.completed == frozenset(PLAN)
        rows[label] = journal.outcomes(journals, PLAN)
        produced[label] = journal.results(
            authority_sha256=AUTH, contract_sha256=m['contract_sha256'],
            p7_record_sha256=m['p7_record_sha256'], plan_sha256=m['plan_sha256'],
            verdict=synthetic_verdict(rows[label]))
    assert len(set(produced.values())) == 1
    assert len({canonical(list(r)) for r in rows.values()}) == 1
    sample = rows['w1']
    assert [tuple(r['key']) for r in sample] == list(PLAN)
    assert not any({'wall_s', 'cpu_s'} & set(r) for r in sample)
    doc = json.loads(produced['w1'])
    assert canonical(doc) == produced['w1'] and doc['verdict'] == synthetic_verdict(sample)
    assert {'authority_sha256', 'contract_sha256', 'p7_record_sha256', 'plan_sha256',
            'verdict'} <= set(doc)
    # Twin: the bytes do follow their inputs.
    other = journal.results(authority_sha256=hexd('other'), contract_sha256=hexd('r3c'),
                            p7_record_sha256=hexd('p7'), plan_sha256=hexd('plan'),
                            verdict=synthetic_verdict(sample))
    assert other != produced['w1']


def test_B1(tmp_path):
    """Row B1: an epoch record without its INTEGRITY time is refused by the schema; every other
    cost field is required too, and a Cost is exactly {cpu_s, wall_s}."""
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
    path.write_bytes(canonical({'body': no_integrity, 'prev_sha256': None,
                                'type': 'EPOCH_OPEN'}) + b'\n')
    with pytest.raises(journal.JournalCorrupt):  # parseable, so not torn: refused on read
        journal.read(path, prev_sha256=None)

    full = {**bodies(), 'EPOCH_OPEN': epoch_open(), 'EPOCH_CLOSE': epoch_close(),
            'PATH': path_body(PLAN[0]),
            'PROBE_RESULT': {'path_cpu_s': 1.0, 'path_wall_s': 1.0, 'peak_memory_bytes': 1}}
    missing = [('PREPARED', 'build'), ('PREPARED', 'integrity'), ('PROBE', 'path_cpu_s'),
               ('PROBE', 'path_wall_s'), ('HEARTBEAT', 'job_cpu_s'), ('HEARTBEAT', 'wall_s'),
               ('SEGMENT_END', 'job_cpu_s'), ('SEGMENT_END', 'path_cpu_s'),
               ('SEGMENT_END', 'overhead_cpu_s'), ('SEGMENT_CRASHED', 'charge'),
               ('EPOCH_OPEN', 'build'), ('EPOCH_CLOSE', 'integrity'), ('PATH', 'cpu_s'),
               ('PATH', 'wall_s'), ('PROBE_RESULT', 'path_cpu_s'), ('PROBE_RESULT', 'path_wall_s')]
    scratch = tmp_path / 'scratch.jsonl'
    fd = os.open(scratch, APPEND, 0o644)
    try:
        for type_, name in missing:
            with pytest.raises(journal.JournalCorrupt):
                body = {k: v for k, v in full[type_].items() if k != name}
                journal.append(fd, type_, body, prev_sha256=None)
        with pytest.raises(journal.JournalCorrupt):
            body = {**epoch_open(), 'integrity': {'cpu_s': 1.0}}
            journal.append(fd, 'EPOCH_OPEN', body, prev_sha256=None)
        assert scratch.read_bytes() == b''
        prev = None
        for type_, _ in missing:  # twins: the full bodies
            prev = journal.append(fd, type_, full[type_], prev_sha256=prev)
    finally:
        os.close(fd)
    assert len(journal.read(scratch, prev_sha256=None)) == len(missing)


def test_check_record_gap_after_complete():
    """O-11: after COMPLETE (a COMPLETE segment end, or ALL_DONE) every plan key occurs."""
    missing = PLAN[3]
    assert check(*simulate([Seg(2)], skip={missing})).code == 'CORRUPTION'
    ledger, journals, m, acts = simulate([Seg(2, end=WORKER_LOST)], skip={missing})
    assert check(Chain(ledger).add('ALL_DONE', {}).records, journals, m, acts).code == 'CORRUPTION'
    # Twin: the same gap before COMPLETE is no failure.
    result = check(ledger, journals, m, acts)
    assert result.code is None and result.completed == frozenset(PLAN) - {missing}


def test_check_record_closure_agreement():
    """O-8 (row K6): epoch closures that differ, or a failed close, are CODE_OR_ARTIFACT_DRIFT."""
    ledger, journals, m, acts = simulate([Seg(2)])
    assert check(ledger, journals, m, acts).code is None
    for index, name, value in ((0, 'closure_sha256', hexd('other closure')),
                               (-2, 'closure_match', False)):
        records = [dict(r) for r in journals['s1-w1.jsonl']]
        records[index] = {**records[index], 'body': {**records[index]['body'], name: value}}
        changed = {**journals, 's1-w1.jsonl': Chain(records).records}
        assert check(ledger, changed, m, acts).code == 'CODE_OR_ARTIFACT_DRIFT'


def test_check_record_act_binding():
    """X3: an act binds the authority, its own act and the ledger head it answers."""
    m = manifest()
    journals = {'c1-w0.jsonl': candidate_journal(m)}
    halted = idle_ledger(m).add('HALT', {'code': 'OVERHEAD_EXHAUSTED', 'from': 'IDLE'})

    def run(head, **kwargs):
        act_sha, acts = act_file(head, **kwargs)
        ledger = Chain(halted.records).add('ACT', {'act_sha256': act_sha, 'act': 'CONTINUE'})
        return check(ledger.records, journals, m, acts)
    head = sha(canonical(halted.records[-1]))
    assert run(head).code is None  # twin
    assert run(sha(canonical(halted.records[-2]))).code == 'CORRUPTION'  # a stale ledger head
    assert run(head, authority=hexd('other')).code == 'CORRUPTION'
    assert run(head, act='TERMINATE').code == 'CORRUPTION'  # the file's act differs
    act_sha, _ = act_file(head)
    ledger = Chain(halted.records).add('ACT', {'act_sha256': act_sha, 'act': 'CONTINUE'}).records
    assert check(ledger, journals, m, {}).code == 'CORRUPTION'  # no act file


def test_check_record_crash_cap():
    """F1: SEGMENT_CRASHED carries the cap its crash reaches, in one record: null goes to IDLE, a
    cap to HALTED from IDLE. check_record recomputes it by row S10; CONTINUE resets it (§4.5)."""
    state, _ = modules()
    kill, opened, key = Seg(1, stop=0, end='CRASHED'), Seg(1, stop=0, end='OPEN'), PLAN[0]
    third = Seg(1, stop=0, end='CRASHED', cap='RESOURCE_EXHAUSTED')
    ledger, journals, m, acts = simulate([kill, kill, third])
    caps = [r['body']['cap'] for r in ledger if r['type'] == 'SEGMENT_CRASHED']
    assert caps == [None, None, 'RESOURCE_EXHAUSTED']
    assert state.fold(ledger) == state.State('HALTED', 'IDLE')
    result = check(ledger, journals, m, acts)
    assert result.code == 'RESOURCE_EXHAUSTED' and dict(result.losses) == {key: 3}
    assert check(*simulate([kill, kill, kill])).code == 'CORRUPTION'  # null at the cap
    assert check(*simulate([kill, third])).code == 'CORRUPTION'  # a cap below it
    ledger, journals, m, acts = simulate([kill, kill, third, Act(), opened])  # recovery
    assert state.fold(ledger) == state.State('RUNNING')
    result = check(ledger, journals, m, acts)
    assert result.code is None and dict(result.losses) == {key: 1}

    # The I/O run: crashed segments whose worker stopped on IO_ERROR without a new key.
    io_kill = Seg(1, stop=0, end='CRASHED', name_inflight='IO_ERROR')
    io_third = Seg(1, stop=0, end='CRASHED', name_inflight='IO_ERROR', cap='IO_EXHAUSTED')
    io_end = Seg(1, stop=0, end=IO_ERROR, name_inflight='IO_ERROR')
    for steps in ([io_kill, io_kill, io_third], [io_end, io_end, io_third]):
        ledger, journals, m, acts = simulate(steps)
        assert state.fold(ledger) == state.State('HALTED', 'IDLE')
        result = check(ledger, journals, m, acts)
        assert result.code == 'IO_EXHAUSTED' and not result.losses
    other = Seg(1, stop=0, end='CRASHED', name_inflight='IO_ERROR', cap='RESOURCE_EXHAUSTED')
    for broken in ([io_kill, io_kill, io_kill],   # null at the cap
                   [io_kill, io_third],           # a cap below it
                   [io_kill, io_kill, other]):    # the other cap
        assert check(*simulate(broken)).code == 'CORRUPTION', broken
    ledger, journals, m, acts = simulate([io_kill, io_kill, io_third, Act(), opened])
    assert check(ledger, journals, m, acts).code is None  # recovery


def started_before(journals, k):
    """The journals a resume at segment ``k`` can see: every segment journal up to ``k``."""
    return {name: records for name, records in journals.items()
            if name[0] != 's' or int(name[1:name.index('-')]) <= k}


def test_cap_finding():
    """F8: ``cap_finding`` is the row S10 cap at a boundary (RESOURCE_EXHAUSTED first); a
    trailing open segment closes with ``cause`` and ``reasons``, ``cause=None`` reading as a
    crash; check_record agrees with it at every SEGMENT_END and SEGMENT_CRASHED."""
    state, _ = modules()
    kill, lost = Seg(1, stop=0, end='CRASHED'), Seg(1, stop=0, end=WORKER_LOST)
    ledger, journals, _, _ = simulate([kill, lost, Seg(1, stop=0, end='OPEN')])
    find = functools.partial(state.cap_finding, ledger, journals, keys=PLAN)
    assert find() == find(cause='WORKER_LOST') == 'RESOURCE_EXHAUSTED'  # a third loss
    assert find(cause='INTERRUPTED') is None
    io = Seg(1, stop=0, end=IO_ERROR, name_inflight='IO_ERROR')
    ledger, journals, _, _ = simulate([io, io, Seg(1, stop=0, end='OPEN',
                                                   name_inflight='WORKER_LOST')])
    find = functools.partial(state.cap_finding, ledger, journals, keys=PLAN)
    assert find() is None and find(cause='WORKER_LOST') is None
    assert find(cause='IO_ERROR') == find(cause='WORKER_LOST', reasons=('IO_ERROR',)) == \
        'IO_EXHAUSTED'
    assert find(cause='IO_EXHAUSTED') is None  # a recorded cap code is not its own evidence
    f4 = Seg(1, stop=0, end=IO_ERROR)  # both caps: the in-flight key is lost, the segment is I/O
    ledger, journals, _, _ = simulate([f4, f4, Seg(1, stop=0, end='OPEN')])
    assert state.cap_finding(ledger, journals, keys=PLAN, cause='IO_ERROR') == 'RESOURCE_EXHAUSTED'
    # check_record's boundaries are cap_finding's.
    io_cap = Seg(1, stop=0, end=('HALTED', 'IO_EXHAUSTED'), name_inflight='IO_ERROR')
    runs = ([kill, kill, Seg(1, stop=0, end='CRASHED', cap='RESOURCE_EXHAUSTED')], [io, io, io_cap],
            [f4, f4, Seg(1, stop=0, end=('HALTED', 'RESOURCE_EXHAUSTED'), reasons=('IO_ERROR',))])
    for steps in runs:
        ledger, journals, m, acts = simulate(steps)
        assert check(ledger, journals, m, acts).code in ('RESOURCE_EXHAUSTED', 'IO_EXHAUSTED')
        k = 0
        for i, record in enumerate(ledger):
            body = record['body']
            k = body['k'] if record['type'] == 'SEGMENT_START' else k
            if record['type'] not in ('SEGMENT_END', 'SEGMENT_CRASHED'):
                continue
            ended = record['type'] == 'SEGMENT_END'
            got = state.cap_finding(ledger[:i], started_before(journals, k), keys=PLAN,
                                    cause=body['cause'] if ended else None,
                                    reasons=[w['reason'] for w in body['workers']] if ended else ())
            recorded = body['cap'] if not ended else (
                body['cause'] if body['class'] == 'HALTED' else None)
            assert got == recorded, (steps, i)


def test_check_record_caps_at_every_boundary():
    """F8: at a cap a SEGMENT_END cause below HALTED must be the cap code (HALTED and TERMINAL
    causes stand); a cap code is recorded only when it is the cap reached, by SEGMENT_END or
    HALT; SEGMENT_START and ALL_DONE wait until every reached cap has its own CONTINUE."""
    state, _ = modules()
    lost = Seg(1, stop=0, end=WORKER_LOST)
    capped = Seg(1, stop=0, end=('HALTED', 'RESOURCE_EXHAUSTED'))
    ledger, journals, m, acts = simulate([lost, lost, capped])
    assert state.fold(ledger) == state.State('HALTED', 'IDLE')
    assert check(ledger, journals, m, acts).code == 'RESOURCE_EXHAUSTED'  # twin
    terminal = Seg(1, stop=0, end=('TERMINAL', 'BUDGET_EXHAUSTED'))
    assert check(*simulate([lost, lost, terminal])).code == 'RESOURCE_EXHAUSTED'  # it stands
    assert check(*simulate([lost, Halt('OVERHEAD_EXHAUSTED')])).code is None  # not a cap code
    io = Seg(1, stop=0, end=IO_ERROR, name_inflight='IO_ERROR')
    unbacked = Seg(1, stop=0, end=('HALTED', 'IO_EXHAUSTED'), name_inflight='WORKER_LOST')
    for broken in ([lost, lost, lost],                                  # STOPPED at the cap
                   [lost, lost, Seg(1, stop=0, end=('HALTED', 'IO_EXHAUSTED'))],  # another cap
                   [capped],                                            # a cap not reached
                   [io, io, unbacked],                                  # no I/O evidence
                   [lost, Halt('RESOURCE_EXHAUSTED')]):                 # a HALT before its cap
        assert check(*simulate(broken)).code == 'CORRUPTION', broken

    # Both caps on one crash: the record carries RESOURCE_EXHAUSTED and its CONTINUE resets only
    # that; HALT{IO_EXHAUSTED} and a second CONTINUE come before any SEGMENT_START.
    both = Seg(2, stop=0, end='CRASHED', name_inflight=('IO_ERROR', None))
    third = Seg(2, stop=0, end='CRASHED', name_inflight=('IO_ERROR', None),
                cap='RESOURCE_EXHAUSTED')
    opened = Seg(2, stop=0, end='OPEN')
    ledger, journals, m, acts = simulate([both, both, third, Act(), Halt('IO_EXHAUSTED'), Act(),
                                          opened])
    assert state.fold(ledger) == state.State('RUNNING')
    assert check(ledger, journals, m, acts).code is None
    assert check(*simulate([both, both, third, Act(), opened])).code == 'CORRUPTION'
    io_third = Seg(2, stop=0, end='CRASHED', name_inflight=('IO_ERROR', None), cap='IO_EXHAUSTED')
    assert check(*simulate([both, both, io_third])).code == 'CORRUPTION'
    # The same at ALL_DONE: every key done, then three witness re-runs lost to worker I/O errors.
    finish, f4 = Seg(1, end=WORKER_LOST), Seg(1, stop=0, end=IO_ERROR)
    f4_cap = Seg(1, stop=0, end=('HALTED', 'RESOURCE_EXHAUSTED'), reasons=('IO_ERROR',))
    ledger, journals, m, acts = simulate([finish, f4, f4, f4_cap, Act()])
    assert check(Chain(ledger).add('ALL_DONE', {}).records, journals, m, acts).code == 'CORRUPTION'
    ledger, journals, m, acts = simulate([finish, f4, f4, f4_cap, Act(), Halt('IO_EXHAUSTED'),
                                          Act()])
    result = check(Chain(ledger).add('ALL_DONE', {}).records, journals, m, acts)
    assert result.code is None and result.completed == frozenset(PLAN)


HALTED_AT_CAP = {  # a HALTED-class cause other than the cap code, at a reached cap (F8)
    'loss': ([Seg(1, stop=0, end=WORKER_LOST)] * 2
             + [Seg(1, stop=0, end=('HALTED', 'UNCLASSIFIED_ERROR'))], 'RESOURCE_EXHAUSTED'),
    'io': ([Seg(1, stop=0, end=IO_ERROR, name_inflight='IO_ERROR')] * 2
           + [Seg(1, stop=0, end=('HALTED', 'UNCLASSIFIED_ERROR'), name_inflight='IO_ERROR')],
           'IO_EXHAUSTED'),
}


@pytest.mark.parametrize('form', sorted(HALTED_AT_CAP))
def test_check_record_halted_cause_at_a_cap(form):
    """F8 (card text): at a reached cap only a cause below HALTED must become the cap code. A
    HALTED cause such as UNCLASSIFIED_ERROR stands; the cap stays reached, the CONTINUE that
    answers it resets nothing, and HALT{cap, from IDLE} with its own CONTINUE precedes any
    SEGMENT_START (violating twin: that HALT omitted)."""
    state, _ = modules()
    steps, cap = HALTED_AT_CAP[form]
    opened = Seg(1, stop=0, end='OPEN')
    ledger, journals, m, acts = simulate(steps)
    assert state.fold(ledger) == state.State('HALTED', 'IDLE')
    assert check(ledger, journals, m, acts).code == cap
    ledger, journals, m, acts = simulate(steps + [Act()])
    assert state.cap_finding(ledger, journals, keys=PLAN) == cap  # the CONTINUE reset nothing
    ledger, journals, m, acts = simulate(steps + [Act(), Halt(cap), Act(), opened])
    assert state.fold(ledger) == state.State('RUNNING')
    assert check(ledger, journals, m, acts).code is None
    assert check(*simulate(steps + [Act(), opened])).code == 'CORRUPTION'


BOTH_CAPS = {  # one record reaches the loss cap and the I/O cap at once (F8)
    'crashed': ([Seg(2, stop=0, end='CRASHED', name_inflight=('IO_ERROR', None))] * 2
                + [Seg(2, stop=0, end='CRASHED', name_inflight=('IO_ERROR', None),
                       cap='RESOURCE_EXHAUSTED')], Seg(2, stop=0, end='OPEN')),
    'ended': ([Seg(1, stop=0, end=IO_ERROR)] * 2
              + [Seg(1, stop=0, end=('HALTED', 'RESOURCE_EXHAUSTED'), reasons=('IO_ERROR',))],
              Seg(1, stop=0, end='OPEN')),
}


@pytest.mark.parametrize('form', sorted(BOTH_CAPS))
def test_check_record_simultaneous_caps(form):
    """Simultaneous caps (F8): one SEGMENT_CRASHED, or one SEGMENT_END, reaches both caps. It
    carries RESOURCE_EXHAUSTED and folds to HALTED(IDLE); CONTINUE resets only the loss cap, so
    cap_finding gives IO_EXHAUSTED; HALT{IO_EXHAUSTED, from IDLE} and a second CONTINUE follow,
    and only then is SEGMENT_START legal."""
    state, _ = modules()
    capped, opened = BOTH_CAPS[form]
    ledger, journals, _, _ = simulate(capped[:2])
    assert state.cap_finding(ledger, journals, keys=PLAN) is None  # neither before the record
    ledger, journals, m, acts = simulate(capped)
    body = ledger[-1]['body']
    assert (body.get('cap') or body.get('cause')) == 'RESOURCE_EXHAUSTED'
    assert state.fold(ledger) == state.State('HALTED', 'IDLE')
    assert check(ledger, journals, m, acts).code == 'RESOURCE_EXHAUSTED'
    ledger, journals, m, acts = simulate(capped + [Act()])
    assert state.fold(ledger) == state.State('IDLE')
    assert state.cap_finding(ledger, journals, keys=PLAN) == 'IO_EXHAUSTED'
    ledger, journals, m, acts = simulate(capped + [Act(), Halt('IO_EXHAUSTED'), Act(), opened])
    assert state.fold(ledger) == state.State('RUNNING')
    assert check(ledger, journals, m, acts).code is None


@pytest.mark.parametrize('form', sorted(BOTH_CAPS))
def test_check_record_interruption_between_continue_acts(form):
    """Interruption between CONTINUE acts (F8). Stopped after the first CONTINUE, the run is
    IDLE with IO_EXHAUSTED found: SEGMENT_START there is CORRUPTION and the HALT is legal.
    Stopped after HALT{IO_EXHAUSTED}, it is HALTED(IDLE): SEGMENT_START is an IllegalTransition,
    and CORRUPTION in check_record."""
    state, _ = modules()
    capped, opened = BOTH_CAPS[form]
    first = capped + [Act()]
    ledger, journals, m, acts = simulate(first)
    assert state.fold(ledger) == state.State('IDLE')
    assert check(ledger, journals, m, acts).code == 'IO_EXHAUSTED'
    assert check(*simulate(first + [opened])).code == 'CORRUPTION'
    ledger, journals, m, acts = simulate(first + [Halt('IO_EXHAUSTED')])  # the HALT is legal
    assert state.fold(ledger) == state.State('HALTED', 'IDLE')
    assert check(ledger, journals, m, acts).code == 'IO_EXHAUSTED'
    k = sum(record['type'] == 'SEGMENT_START' for record in ledger) + 1
    with pytest.raises(state.IllegalTransition):
        state.advance(state.fold(ledger), event('SEGMENT_START', segment_start(k, opened.w)))
    assert check(*simulate(first + [Halt('IO_EXHAUSTED'), opened])).code == 'CORRUPTION'


def test_check_record_worker_append_failure():
    """F4: a worker whose append raised is named IO_ERROR in SEGMENT_END: that is an I/O-error
    segment for row S10, and its in-flight key is one loss."""
    f4 = Seg(1, stop=0, end=IO_ERROR)  # no WORKER_STOP: the key stays in flight
    result = check(*simulate([f4, f4]))
    assert result.code is None and dict(result.losses) == {PLAN[0]: 2}
    named = Seg(1, stop=0, end=('HALTED', 'IO_EXHAUSTED'), name_inflight='WORKER_LOST',
                reasons=('IO_ERROR',))  # the reason alone is the I/O evidence
    result = check(*simulate([f4, f4, named]))
    assert result.code == 'IO_EXHAUSTED' and dict(result.losses) == {PLAN[0]: 2}
    no_reason = Seg(1, stop=0, end=('HALTED', 'IO_EXHAUSTED'), name_inflight='WORKER_LOST',
                    reasons=('WORKER_LOST',))
    assert check(*simulate([f4, f4, no_reason])).code == 'CORRUPTION'
    f4_cap = Seg(1, stop=0, end=('HALTED', 'RESOURCE_EXHAUSTED'), reasons=('IO_ERROR',))
    result = check(*simulate([f4, f4, f4_cap]))  # a third loss with the I/O run: loss cap first
    assert result.code == 'RESOURCE_EXHAUSTED' and dict(result.losses) == {PLAN[0]: 3}
    assert check(*simulate([f4, f4, f4])).code == 'CORRUPTION'


def test_check_record_witnesses():
    """F2: a resume tags exactly min(W, |completed|) distinct completed keys, and worker i runs
    witness i as its first KEY_START."""
    first = Seg(2, stop=1, end=WORKER_LOST)
    ledger, journals, m, acts = simulate([first, Seg(2)])
    assert check(ledger, journals, m, acts).code is None  # twin
    start = [r['body'] for r in ledger if r['type'] == 'SEGMENT_START'][1]
    tagged = tuple(tuple(key) for key in start['witness_keys'])
    assert len(tagged) == 2
    for broken in (Seg(2, witnesses=tagged[:1]),               # too few
                   Seg(2, witnesses=(tagged[0], tagged[0])),   # not distinct
                   Seg(2, witnesses=(tagged[0], PLAN[-1])),    # not completed
                   Seg(2, rerun=False)):                       # declared, not run first
        assert check(*simulate([first, broken])).code == 'CORRUPTION', broken
    swapped = edit(ledger, 'SEGMENT_START', lambda body: body['k'] == 2,
                   witness_keys=[list(key) for key in tagged[::-1]])  # each run by the other
    assert check(swapped, journals, m, acts).code == 'CORRUPTION'
    # The reviewer's probe: a resume after completed keys that tags none.
    assert check(*simulate([first, Seg(2, witnesses=(), rerun=False)])).code == 'CORRUPTION'


def test_check_record_assignment():
    """F3: assignment_sha256 is recomputed from sorted(K - completed)[i::W] and compared."""
    ledger, journals, m, acts = simulate([Seg(2, stop=1, end=WORKER_LOST), Seg(3)])
    assert check(ledger, journals, m, acts).code is None  # twin: W changes at resume
    whole_plan = assignment_sha256(shares_of(list(PLAN), 3))  # ordinal in K, not K - completed
    for k, digest in ((1, hexd('another assignment')), (2, whole_plan)):
        changed = edit(ledger, 'SEGMENT_START', lambda body, k=k: body['k'] == k,
                       assignment_sha256=digest)
        assert check(changed, journals, m, acts).code == 'CORRUPTION'
    # The order is Python sorted() over Key tuples: path index 2 before 10 (not JSON bytes).
    numeric = (('root-a', 'FULL', 10), ('root-a', 'FULL', 2), ('root-a', 'H1', 10),
               ('root-a', 'H1', 2))
    ledger, journals, m, acts = simulate([Seg(2)], keys=numeric)
    first = [tuple(r['body']['key']) for r in journals['s1-w0.jsonl'] if r['type'] == 'KEY_START']
    assert first == [('root-a', 'FULL', 2), ('root-a', 'H1', 2)]
    assert check(ledger, journals, m, acts, keys=numeric).code is None
    by_bytes = sorted(numeric, key=lambda key: canonical(list(key)))
    assert by_bytes[0] == ('root-a', 'FULL', 10)
    changed = edit(ledger, 'SEGMENT_START', assignment_sha256=assignment_sha256(
        shares_of(by_bytes, 2)))
    assert check(changed, journals, m, acts, keys=numeric).code == 'CORRUPTION'


def test_check_record_journal_names():
    """F6: a journal name is exactly f'{prefix}{n}-w{i}.jsonl', unpadded, and its identity is
    (prefix, n, i): c1-w0, s1-w0 and v1-w0 are distinct; a duplicate identity is CORRUPTION."""
    state, journal = modules()
    ledger, journals, m, acts = verified_run([PLAN[0]], [PLAN[0]])
    assert {'c1-w0.jsonl', 's1-w0.jsonl', 'v1-w0.jsonl'} <= set(journals)
    assert check(ledger, journals, m, acts).code is None  # twin: they coexist
    for bad in ('s1-w01.jsonl', 's01-w1.jsonl', 's0-w1.jsonl', 's1-w1.json', 'x1-w1.jsonl'):
        renamed = {**{n: r for n, r in journals.items() if n != 's1-w1.jsonl'},
                   bad: journals['s1-w1.jsonl']}
        assert check(ledger, renamed, m, acts).code == 'CORRUPTION', bad
    duplicate = {**journals, 's1-w01.jsonl': journals['s1-w1.jsonl']}  # (s, 1, 1) twice
    assert state.check_record(ledger, duplicate, m, acts, keys=PLAN).code == 'CORRUPTION'
    assert [journal.journal_name(n) for n in ('c1-w0.jsonl', 's1-w0.jsonl', 'v12-w10.jsonl')] == [
        ('c', 1, 0), ('s', 1, 0), ('v', 12, 10)]
    assert journal.journal_name('s1-w01.jsonl') is None


def test_append_refuses_after_a_raise(tmp_path):
    """F4: after ``append`` raises, the file takes no more records in this process, through any
    fd, so a retry cannot chain from a stale prev: STOPPED IO_ERROR, not TERMINAL CORRUPTION."""
    state, journal = modules()
    # The reviewer's probe: the null device accepts the write and refuses the fsync.
    fd = os.open(os.devnull, os.O_WRONLY | os.O_APPEND | BINARY)
    try:
        with pytest.raises(OSError) as failed:
            journal.append(fd, 'EPOCH_OPEN', epoch_open(), prev_sha256=None)
        assert failed.value.errno != errno.EIO  # the device's own fsync error
        with pytest.raises(OSError) as refused:
            journal.append(fd, 'WORKER_STOP', {'reason': 'IO_ERROR', 'key': None}, prev_sha256=None)
        assert refused.value.errno == errno.EIO and 'no more records' in str(refused.value)
        assert state.classify(refused.value) == ('STOPPED', 'IO_ERROR')
    finally:
        os.close(fd)
    # On a journal file: one fd's failed write refuses the writer's next record, and the file
    # keeps a valid chain.
    path = tmp_path / 'journal' / 's1-w0.jsonl'
    path.parent.mkdir()
    writer, reader = os.open(path, APPEND, 0o644), None
    try:
        head = journal.append(writer, 'EPOCH_OPEN', epoch_open(), prev_sha256=None)
        reader = os.open(path, os.O_RDONLY | BINARY)
        with pytest.raises(OSError):
            journal.append(reader, 'KEY_START', {'key': list(PLAN[0])}, prev_sha256=head)
        with pytest.raises(OSError) as refused:
            journal.append(writer, 'WORKER_STOP', {'reason': 'IO_ERROR', 'key': None},
                           prev_sha256=head)
        assert refused.value.errno == errno.EIO
    finally:
        os.close(writer)
        if reader is not None:
            os.close(reader)
    assert [r['type'] for r in journal.read(path, prev_sha256=None)] == ['EPOCH_OPEN']
    # Twin: another file still takes records.
    other = tmp_path / 'journal' / 's1-w1.jsonl'
    fd = os.open(other, APPEND, 0o644)
    try:
        head = journal.append(fd, 'EPOCH_OPEN', epoch_open(), prev_sha256=None)
        journal.append(fd, 'WORKER_STOP', {'reason': 'DONE', 'key': None}, prev_sha256=head)
    finally:
        os.close(fd)
    assert len(journal.read(other, prev_sha256=None)) == 2


def test_path_cross_fields(tmp_path):
    """PATH fields agree: bracket_status follows the runs (``bracket.BracketVerdict``), and a run
    is PASS exactly when it has sessions_to_pass and no failure_reason (``model.PathOutcome``)."""
    _, journal = modules()
    key = PLAN[0]
    good = [path_body(key, statuses=pair) for pair in (
        ('PASS', 'PASS'), ('FAILURE', 'FAILURE'), ('UNRESOLVED', 'UNRESOLVED'), ('PASS', 'FAILURE'),
        ('FAILURE', 'UNRESOLVED'))]
    passing = path_body(key, statuses=('PASS', 'PASS'))
    failing = path_body(key, statuses=('FAILURE', 'FAILURE'))

    def with_r1(body, **fields):
        return {**body, 'runs': {**body['runs'], 'r1': {**body['runs']['r1'], **fields}}}
    bad = [{**passing, 'bracket_status': 'UNDETERMINED'}, {**passing, 'bracket_status': 'FAILURE'},
           {**path_body(key, statuses=('PASS', 'FAILURE')), 'bracket_status': 'PASS'},
           with_r1(passing, sessions_to_pass=None), with_r1(passing, failure_reason='bust'),
           with_r1(failing, sessions_to_pass=3), with_r1(failing, failure_reason=None),
           with_r1(failing, status='PASS')]
    path = tmp_path / 'journal' / 's1-w0.jsonl'
    path.parent.mkdir()
    fd = os.open(path, APPEND, 0o644)
    try:
        for body in bad:
            with pytest.raises(journal.JournalCorrupt):
                journal.append(fd, 'PATH', body, prev_sha256=None)
        assert path.read_bytes() == b''
        prev = None
        for body in good:  # twins
            prev = journal.append(fd, 'PATH', body, prev_sha256=prev)
    finally:
        os.close(fd)
    assert [r['body']['bracket_status'] for r in journal.read(path, prev_sha256=None)] == [
        'PASS', 'FAILURE', 'UNRESOLVED', 'UNDETERMINED', 'UNDETERMINED']
    path.write_bytes(canonical({'body': bad[0], 'prev_sha256': None, 'type': 'PATH'}) + b'\n')
    with pytest.raises(journal.JournalCorrupt):  # and on read
        journal.read(path, prev_sha256=None)


def broken_runs():
    """(clause, broken run, twin run) for each structural CORRUPTION clause of check_record."""
    m = manifest()
    kill, opened = Seg(1, stop=0, end='CRASHED'), Seg(1, stop=0, end='OPEN')
    crashed = simulate([kill, opened])
    stopped = simulate([Seg(2, end=WORKER_LOST)])
    ledger, journals, _, acts = stopped
    c_journal = journals['c1-w0.jsonl']
    s_journal = journals['s1-w0.jsonl']
    key_start = next(i for i, r in enumerate(s_journal) if r['type'] == 'KEY_START')

    def with_journal(name, records, run=stopped):
        return run[0], {**run[1], name: Chain(records).records}, run[2], run[3]
    return [
        ('crashed-losses-differ', (edit(crashed[0], 'SEGMENT_CRASHED', losses=[]), *crashed[1:]),
         crashed),
        ('crashed-losses-add-a-key', (edit(crashed[0], 'SEGMENT_CRASHED',
                                           losses=[list(PLAN[0]), list(PLAN[1])]), *crashed[1:]),
         crashed),
        ('key-start-in-candidate-journal',
         with_journal('c1-w0.jsonl', c_journal[:-1] + [{'type': 'KEY_START', 'body': {
             'key': list(PLAN[0])}}] + c_journal[-1:]), stopped),
        ('record-after-worker-stop',
         with_journal('c1-w0.jsonl', c_journal + [{'type': 'EPOCH_OPEN', 'body': epoch_open()}]),
         stopped),
        ('manifest-differs-from-prepared', (ledger, journals, {**m, 'code_head': 'd' * 40}, acts),
         stopped),
        ('no-manifest-after-prepared', (ledger, journals, None, acts), stopped),
        ('candidates-differ-from-manifest',
         with_journal('c1-w0.jsonl', edit(c_journal, 'CANDIDATES', populations={
             **m['populations'], 'H1': {'indices': [1], 'candidates_sha256': hexd('x')}})),
         stopped),
        ('journal-of-unstarted-segment',
         with_journal('s2-w0.jsonl', Chain().add('EPOCH_OPEN', epoch_open()).records), stopped),
        ('path-without-key-start',
         with_journal('s1-w0.jsonl', s_journal[:key_start] + s_journal[key_start + 1:]), stopped),
        ('path-after-other-key-start',
         with_journal('s1-w0.jsonl', edit(s_journal, 'KEY_START',
                                          lambda body: body['key'] == list(PLAN[0]),
                                          key=list(PLAN[2]))), stopped),
    ]


BROKEN = broken_runs()


@pytest.mark.parametrize('clause, broken, twin', BROKEN, ids=[clause for clause, _, _ in BROKEN])
def test_check_record_structural_corruption(clause, broken, twin):
    """Each structural clause alone is CORRUPTION; its unbroken twin passes."""
    assert check(*twin).code is None, clause
    assert check(*broken).code == 'CORRUPTION', clause


def test_check_record_verify_journals():
    """``verify`` journals: each needs its VERIFY_START, runs only its listed keys, and lists
    only plan keys."""
    assert check(*verified_run([PLAN[0]], [PLAN[0]])).code is None  # twin
    assert check(*verified_run([PLAN[0]], [PLAN[0], PLAN[1]])).code == 'CORRUPTION'  # not listed
    assert check(*verified_run([PLAN[0], OUTSIDE], [PLAN[0]])).code == 'CORRUPTION'  # off-plan
    ledger, journals, m, acts = verified_run([PLAN[0]], [PLAN[0]])
    unstarted = {**journals, 'v2-w0.jsonl': journals['v1-w0.jsonl']}
    assert check(ledger, unstarted, m, acts).code == 'CORRUPTION'  # no VERIFY_START n=2


@pytest.mark.skipif(os.name != 'nt', reason='msvcrt byte-range lock (design §4.1)')
def test_read_lock_reads_content_under_the_held_byte(tmp_path):
    """The run lock's content is readable while the byte at LOCK_OFFSET is held (card §3.4)."""
    _, journal = modules()
    msvcrt = importlib.import_module('msvcrt')
    path = tmp_path / 'lock'
    fd = os.open(path, os.O_RDWR | os.O_CREAT | BINARY, 0o644)
    try:
        os.lseek(fd, journal.LOCK_OFFSET, os.SEEK_SET)
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        os.lseek(fd, 0, os.SEEK_SET)
        os.write(fd, canonical({'host': socket.gethostname(), 'pid': os.getpid(),
                                'schema': 't00_screen_lock/v1'}))
        assert journal.read_lock(path) == (os.getpid(), socket.gethostname())
        other = os.open(path, os.O_RDWR | BINARY)
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


def test_read_lock_refuses_stale_bytes(tmp_path):
    """F5: a lock rewrite truncates to the content length; stale trailing bytes are refused."""
    _, journal = modules()
    path = tmp_path / 'lock'
    path.write_bytes(canonical({'host': 'h' * 40, 'pid': 123456, 'schema': 't00_screen_lock/v1'}))
    short = canonical({'host': 'h', 'pid': 7, 'schema': 't00_screen_lock/v1'})
    fd = os.open(path, os.O_RDWR | BINARY)
    try:
        os.write(fd, short)  # rewritten at offset 0 without truncation
        with pytest.raises(journal.JournalCorrupt):
            journal.read_lock(path)
        os.ftruncate(fd, len(short))  # twin
    finally:
        os.close(fd)
    assert journal.read_lock(path) == (7, 'h')


def test_module_globals_are_immutable():
    """No t00_screen module keeps a mutable module-level global. Retained-source provenance
    (``result_adjudication._verify_retained_executable_modules``) re-executes each loaded module
    and compares its globals, so a global that a test or a run mutates breaks it. Constants are
    str, int, tuple, frozenset, compiled patterns or MappingProxyType over such values."""
    state, journal = modules()
    package = importlib.import_module('c1_rail.qualification.t00_screen')
    mutable = (dict, list, set, bytearray)
    found = []
    for module in (package, state, journal):
        for name, value in vars(module).items():
            nested = value.values() if isinstance(value, MappingProxyType) else ()
            if not name.startswith('__') and (isinstance(value, mutable)
                                              or any(isinstance(v, mutable) for v in nested)):
                found.append(f'{module.__name__}.{name}')
    assert not found
