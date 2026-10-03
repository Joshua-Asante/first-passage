"""T00 step-3 run state: the one transition function, the closed stop classes and the
cross-field record check (design 2026-10-02 §4.2-§4.5; build card §3.6, §3.6a, packet P-D).

``advance`` is the only code that changes durable run state; the coordinator appends an event
only after ``advance`` accepts it, so a refused event writes nothing (row S1). ``classify`` is
the closed §4.3 table (row S9). ``check_record`` holds the ledger, journals, manifest and acts
together (rows K6, S10, S13, S14, the S15 gap clause and X3; card F1-F3, F6, F8), and
``cap_finding`` is the one row S10 cap computation that it and the coordinator share (F8).
"""
from __future__ import annotations

import base64
import binascii
from dataclasses import dataclass, field
import hashlib
import re
from types import MappingProxyType
from typing import Mapping, Sequence

from ..contract import ContractValidationError, canonical_json_bytes, parse_canonical_json
from . import journal

ILLEGAL_TRANSITION = 'ILLEGAL_TRANSITION'
UNCLASSIFIED_ERROR = 'UNCLASSIFIED_ERROR'
OPERATOR_TERMINATED = 'OPERATOR_TERMINATED'
STOPPED, HALTED, TERMINAL, COMPLETE = 'STOPPED', 'HALTED', 'TERMINAL', 'COMPLETE'
STATES = ('NONE', 'BOUND', 'PREPARED', 'PROBING', 'IDLE', 'RUNNING', 'HALTED', 'COMPLETE',
          'TERMINAL', 'AGGREGATED', 'REPORTED', 'FINAL')
LOSS_CAP = 3  # row S10: a third loss of one key, or a third consecutive I/O-error segment, HALTs
CORRUPTION = journal.CORRUPTION

# Design §4.3, closed: a cause or code -> (class, code); anything else is HALTED
# UNCLASSIFIED_ERROR.
CAUSES = MappingProxyType({
    **dict.fromkeys(('APPROVAL_LAPSE', 'SOURCE_APPROVAL_EXPIRED', 'SCREEN_APPROVAL_EXPIRED'),
                    (STOPPED, 'APPROVAL_LAPSE')),
    **dict.fromkeys(('SOURCE_KEY_LIFECYCLE', 'SOURCE_KEY_REVOKED', 'SOURCE_KEY_CHANGED',
                     'SOURCE_KEY_REMOVED'), (TERMINAL, 'SOURCE_KEY_LIFECYCLE')),
    **{code: (TERMINAL, code) for code in (
        'CONTEXT_REFUSAL', 'INTRADAY_LOW_MISSING', 'CANDIDATES_UNAVAILABLE', 'PROBE_INCOMPLETE',
        'PROBE_OVER_BUDGET', 'BUDGET_EXHAUSTED', 'NONDETERMINISM', CORRUPTION,
        'CODE_OR_ARTIFACT_DRIFT', OPERATOR_TERMINATED)},
    **dict.fromkeys(('TREE_CHANGED', 'SCREEN_EPOCH_STALE'), (STOPPED, 'TREE_CHANGED')),
    **{code: (STOPPED, code) for code in ('IO_ERROR', 'WORKER_LOST', 'INTERRUPTED')},
    **{code: (HALTED, code) for code in ('IO_EXHAUSTED', 'RESOURCE_EXHAUSTED',
                                         'OVERHEAD_EXHAUSTED', 'PROBE_INTERRUPTED',
                                         UNCLASSIFIED_ERROR)},
})
_CODE = re.compile(r'([A-Z][A-Z0-9_]*)(?::|$)')
_TYPED_CAUSES = ((MemoryError, 'WORKER_LOST'), (KeyboardInterrupt, 'INTERRUPTED'),
                 (OSError, 'IO_ERROR'))
_IO_EVIDENCE = 'IO_ERROR'  # a recorded cap code is never its own evidence (F8)
_CAPS = ('RESOURCE_EXHAUSTED', 'IO_EXHAUSTED')  # row S10, in precedence order
_TIMING = ('wall_s', 'cpu_s')


class IllegalTransition(ValueError):
    """An event not allowed in the current state (row S1)."""
    code = ILLEGAL_TRANSITION

    def __init__(self, detail):
        super().__init__(f'{ILLEGAL_TRANSITION}: {detail}')


@dataclass(frozen=True)
class State:
    """A §4.2 run state (``NONE`` before AUTHORITY_BOUND); ``halted_from`` is the HALT's from
    state."""
    name: str
    halted_from: str | None = None


@dataclass(frozen=True)
class RecordCheck:
    """``code`` is ``None`` or the first failure; see ``check_record``."""
    code: str | None
    completed: frozenset = frozenset()
    losses: Mapping = field(default_factory=lambda: MappingProxyType({}))


def _cause_code(exc):
    named = getattr(exc, 'code', None)
    found = _CODE.match(str(exc))
    for candidate in (named, found.group(1) if found else None):
        if isinstance(candidate, str) and candidate in CAUSES:
            return candidate
    for kind, code in _TYPED_CAUSES:
        if isinstance(exc, kind):
            return code
    from ..replay import ReplayNeedsContext  # pylint: disable=import-outside-toplevel
    return 'CONTEXT_REFUSAL' if isinstance(exc, ReplayNeedsContext) else UNCLASSIFIED_ERROR


def classify(cause: str | BaseException) -> tuple[str, str]:
    """(class, code) per design §4.3; an unlisted cause is (HALTED, UNCLASSIFIED_ERROR) (row S9).

    An exception is classified by its ``code`` attribute, else the leading ``CODE:`` of its
    message, else its type (``MemoryError``, ``KeyboardInterrupt``, ``OSError``,
    ``ReplayNeedsContext``).
    """
    if isinstance(cause, BaseException):
        cause = _cause_code(cause)
    elif not isinstance(cause, str):
        raise TypeError('cause must be a code or an exception')
    return CAUSES.get(cause, (HALTED, UNCLASSIFIED_ERROR))


# Design §4.2 rows whose body carries no class, from state or act.
_SIMPLE = MappingProxyType({
    ('NONE', 'AUTHORITY_BOUND'): 'BOUND', ('BOUND', 'PREPARED'): 'PREPARED',
    ('PREPARED', 'PROBE_START'): 'PROBING', ('PROBING', 'PROBE'): 'IDLE',
    ('IDLE', 'SEGMENT_START'): 'RUNNING', ('IDLE', 'ALL_DONE'): 'COMPLETE',
    ('RUNNING', 'HEARTBEAT'): 'RUNNING',
    ('COMPLETE', 'AGGREGATED'): 'AGGREGATED', ('TERMINAL', 'AGGREGATED'): 'AGGREGATED',
    ('AGGREGATED', 'REPORTED'): 'REPORTED', ('REPORTED', 'FINAL'): 'FINAL',
    ('FINAL', 'VERIFY_START'): 'FINAL', ('FINAL', 'VERIFY'): 'FINAL',
})
_HALTABLE = frozenset({'BOUND', 'PREPARED', 'PROBING', 'IDLE'})
_TERMINABLE_BY_ACT = frozenset({'BOUND', 'PREPARED', 'IDLE', 'HALTED'})
_NOT_TERMINABLE = frozenset({'NONE', 'RUNNING', 'FINAL'})  # the ledger opens with AUTHORITY_BOUND
_SEGMENT_END = MappingProxyType({STOPPED: State('IDLE'), HALTED: State('HALTED', 'IDLE'),
                                 TERMINAL: State('TERMINAL'), COMPLETE: State('COMPLETE')})


def _target(state, kind, body):
    """The §4.2 target of a schema-valid ledger event, or ``None`` when it is not allowed."""
    name = state.name
    if kind == 'TERMINAL':  # F5: only ACT{TERMINATE} carries OPERATOR_TERMINATED
        code = body['code']
        allowed = (name not in _NOT_TERMINABLE and code != OPERATOR_TERMINATED
                   and classify(code) == (TERMINAL, code))
        return State('TERMINAL') if allowed else None
    if kind == 'HALT':
        allowed = (name in _HALTABLE and body['from'] == name
                   and classify(body['code']) == (HALTED, body['code']))
        return State('HALTED', name) if allowed else None
    if kind == 'ACT':
        if body['act'] == 'TERMINATE':
            return State('TERMINAL') if name in _TERMINABLE_BY_ACT else None
        resumed = 'PREPARED' if state.halted_from == 'PROBING' else state.halted_from
        return State(resumed) if name == 'HALTED' else None
    if kind == 'SEGMENT_CRASHED':  # F1: one record; IDLE, or HALTED if a cap is reached
        halted = State('HALTED', 'IDLE') if body['cap'] is not None else State('IDLE')
        return halted if name == 'RUNNING' else None
    if kind == 'SEGMENT_END':
        cls, cause = body['class'], body['cause']
        named = cause == COMPLETE if cls == COMPLETE else classify(cause) == (cls, cause)
        return _SEGMENT_END[cls] if name == 'RUNNING' and named else None
    target = _SIMPLE.get((name, kind))
    return None if target is None else State(target)


def advance(state: State, event: journal.Record) -> State:
    """The state after ``event``; an event not allowed here raises ``IllegalTransition`` (row S1).
    A body outside its schema raises ``journal.JournalCorrupt`` (row B1)."""
    if (not isinstance(state, State) or state.name not in STATES
            or (state.halted_from in _HALTABLE) != (state.name == 'HALTED')):
        raise IllegalTransition(f'not a run state: {state!r}')
    kind = event.get('type') if isinstance(event, Mapping) else None
    if not isinstance(kind, str) or kind not in journal.LEDGER_BODIES:
        raise IllegalTransition(f'{kind!r} is not a ledger event')
    journal.validate_body(kind, event.get('body'), kind='ledger')
    target = _target(state, kind, event['body'])
    if target is None:
        raise IllegalTransition(f'{kind} is not allowed in {state.name}')
    return target


def fold(ledger: Sequence[journal.Record]) -> State:
    """The run state: ``advance`` applied to every ledger record from ``NONE`` (I3)."""
    current = State('NONE')
    for record in ledger:
        current = advance(current, record)
    return current


class _Failed(Exception):
    """A structural failure found mid-check; ``check_record`` returns its code."""

    def __init__(self, code):
        super().__init__(code)
        self.code = code


def _corrupt(condition):
    if condition:
        raise _Failed(CORRUPTION)


def _chain(records, *, kind):
    prev = None
    for record in records:
        _corrupt(not isinstance(record, Mapping) or set(record) != {'body', 'prev_sha256', 'type'}
                 or record['prev_sha256'] != prev)
        try:
            journal.validate_body(record['type'], record['body'], kind=kind)
            prev = journal.record_sha256(record)
        except (ContractValidationError, journal.JournalCorrupt):
            raise _Failed(CORRUPTION) from None


@dataclass
class _Journals:
    """The worker journals, grouped: segment and verify journals by number and worker."""
    segments: dict = field(default_factory=dict)
    verifies: dict = field(default_factory=dict)
    candidates: list = field(default_factory=list)
    closures: set = field(default_factory=set)
    close_failed: bool = False
    paths: list = field(default_factory=list)
    identities: set = field(default_factory=set)

    def add(self, name, records):
        """Group one journal. Its name is strict and its identity (prefix, number, worker)
        unique (F6); WORKER_STOP is last, and a candidate journal holds no key."""
        parsed = journal.journal_name(name)
        _corrupt(parsed is None or parsed in self.identities)
        self.identities.add(parsed)
        _chain(records, kind='journal')
        types = [record['type'] for record in records]
        _corrupt('WORKER_STOP' in types[:-1])  # always the last record (row S2)
        prefix, number, worker = parsed
        if prefix == 'c':
            _corrupt({'KEY_START', 'PATH'} & set(types))
        else:
            group = self.segments if prefix == 's' else self.verifies
            group.setdefault(number, {})[worker] = records
        for record in records:
            body = record['body']
            if record['type'] == 'CANDIDATES':
                self.candidates.append(body['populations'])
            elif record['type'] == 'EPOCH_OPEN':
                self.closures.add(body['closure_sha256'])
            elif record['type'] == 'EPOCH_CLOSE':
                self.close_failed = self.close_failed or not body['closure_match']
            elif record['type'] == 'PATH':
                self.paths.append(body)


def _check_manifest(ledger, manifest, authority, candidates):
    """§3.4 keys, the PREPARED digest of ``canonical_json_bytes(manifest)`` (F5), and every
    CANDIDATES record equal to it (row R2's mismatch)."""
    prepared = [record['body']['manifest_sha256'] for record in ledger
                if record['type'] == 'PREPARED']
    if manifest is None:
        _corrupt(prepared)
        return
    _corrupt(not isinstance(manifest, Mapping) or set(manifest) != {
        'authority_sha256', 'contract_sha256', 'p7_record_sha256', 'code_head', 'populations',
        'plan_sha256'} or manifest['authority_sha256'] != authority)
    try:
        digest = hashlib.sha256(canonical_json_bytes(dict(manifest))).hexdigest()
    except ContractValidationError:
        raise _Failed(CORRUPTION) from None
    _corrupt(any(value != digest for value in prepared)
             or any(populations != manifest['populations'] for populations in candidates))


def _act_document(name, raw):
    """The act in ``acts/<act_sha256>.json`` = canonical ``{act_b64, approval_b64}`` (F5); the
    act bytes hash to the file name."""
    try:
        container = parse_canonical_json(raw, label='act file')
        _corrupt(not isinstance(container, dict) or set(container) != {'act_b64', 'approval_b64'}
                 or not all(isinstance(value, str) for value in container.values()))
        act = base64.b64decode(container['act_b64'], validate=True)
        _corrupt(base64.b64encode(act).decode('ascii') != container['act_b64']
                 or re.fullmatch(r'[0-9a-f]{64}[.]json', name) is None
                 or hashlib.sha256(act).hexdigest() + '.json' != name)
        doc = parse_canonical_json(act, label='act')
    except (ContractValidationError, binascii.Error, TypeError):
        raise _Failed(CORRUPTION) from None
    _corrupt(not isinstance(doc, dict))
    return doc


def _check_acts(ledger, acts, authority):
    """X3: each ACT record names its act file, whose act binds this authority, the same act and
    the ledger head the record follows; so a stale act is never recorded."""
    documents = {name: _act_document(name, raw) for name, raw in acts.items()}
    for record in ledger:
        if record['type'] == 'ACT':
            doc = documents.get(record['body']['act_sha256'] + '.json')
            _corrupt(doc is None or doc.get('authority_sha256') != authority
                     or doc.get('act') != record['body']['act']
                     or doc.get('ledger_head_sha256') != record['prev_sha256'])


def _keys(records):
    return [tuple(record['body']['key']) for record in records
            if record['type'] in ('KEY_START', 'PATH')]


def _segment_keys(workers):
    """(lost, done, stops) over one segment's journals: a KEY_START with neither its PATH nor a
    WORKER_STOP naming it is lost (row S10); a PATH must follow its own KEY_START; ``stops``
    are the WORKER_STOP reasons."""
    lost, done, stops = set(), set(), set()
    for records in workers.values():
        inflight = None
        for record in records:
            kind, body = record['type'], record['body']
            stops.update((body['reason'],) if kind == 'WORKER_STOP' else ())
            if kind == 'KEY_START':
                lost.update(() if inflight is None else (inflight,))
                inflight = tuple(body['key'])
            elif kind == 'PATH':
                _corrupt(tuple(body['key']) != inflight)
                done.add(inflight)
                inflight = None
            elif kind == 'WORKER_STOP' and body['key'] is not None and \
                    tuple(body['key']) == inflight:
                inflight = None
        lost.update(() if inflight is None else (inflight,))
    return lost, done, stops


def _assignment(remaining, w):
    """F3: worker i's keys ``remaining[i::w]``, and the SHA-256 SEGMENT_START records for them."""
    shares = [remaining[i::w] for i in range(w)]
    listed = [[i, [list(key) for key in share]] for i, share in enumerate(shares)]
    return shares, hashlib.sha256(canonical_json_bytes(listed)).hexdigest()


class _Walk:
    """Rows S10, S13 and S14 over the ledger in order: assignments and witnesses, losses, I/O
    runs and the caps at every boundary (card F1-F3, F8)."""

    def __init__(self, plan, segments):
        self.plan, self.segments = plan, segments
        self.completed, self.losses, self.io_run = set(), {}, 0
        self.halt_code, self.complete, self.started, self.current = None, False, 0, None

    def run(self, ledger, cause=None, reasons=()):
        """Walk every ledger record. A trailing segment without SEGMENT_END or SEGMENT_CRASHED
        is closed with ``cause`` and the worker ``reasons``; ``cause=None`` reads as a crash."""
        handlers = {'SEGMENT_START': self._start, 'SEGMENT_END': self._end,
                    'SEGMENT_CRASHED': self._crashed, 'HALT': self._halt, 'ACT': self._act,
                    'ALL_DONE': self._all_done}
        for record in ledger:
            handler = handlers.get(record['type'])
            if handler is not None:
                handler(record['body'])
        if self.current is not None:  # no SEGMENT_END: crashed unless a cause is given (§4.2)
            self._close(cause=cause, reasons=reasons)
        _corrupt(set(self.segments) - set(range(1, self.started + 1)))
        return self

    def reached(self, cap):
        """Row S10: a third loss of one key, or a third I/O segment without a new completed key,
        since the CONTINUE that reset that cap."""
        if cap == 'RESOURCE_EXHAUSTED':
            return any(count >= LOSS_CAP for count in self.losses.values())
        return self.io_run >= LOSS_CAP

    def cap(self):
        """The cap reached and not reset, ``RESOURCE_EXHAUSTED`` first (F8), else ``None``."""
        return next((cap for cap in _CAPS if self.reached(cap)), None)

    def _start(self, body):
        k, w = body['k'], body['w']
        witnesses = [tuple(key) for key in body['witness_keys']]
        _corrupt(k != self.started + 1 or self.cap() is not None  # F8
                 or len(witnesses) != min(w, len(self.completed))  # F2
                 or len(set(witnesses)) != len(witnesses) or not set(witnesses) <= self.completed)
        shares, digest = _assignment(sorted(self.plan - self.completed), w)  # F3
        _corrupt(body['assignment_sha256'] != digest)
        workers = self.segments.get(k, {})
        _corrupt(any(worker >= w for worker in workers))
        for worker, records in workers.items():
            started = [tuple(r['body']['key']) for r in records if r['type'] == 'KEY_START']
            # F2: worker i re-executes witness i first; S14: every other key is its own share's.
            _corrupt(worker < len(witnesses) and started and started[0] != witnesses[worker])
            allowed = set(witnesses) | set(shares[worker])
            _corrupt(any(key not in allowed for key in _keys(records)))
        self.started, self.current = k, k

    def _close(self, crashed=None, cause=None, reasons=()):
        lost, done, stops = _segment_keys(self.segments.get(self.current, {}))
        _corrupt(crashed is not None and sorted(lost) != sorted(tuple(key) for key in crashed))
        if cause != 'INTERRUPTED':
            for key in lost:
                self.losses[key] = self.losses.get(key, 0) + 1
        io_segment = _IO_EVIDENCE in {cause, *reasons, *stops} and not done - self.completed
        self.io_run = self.io_run + 1 if io_segment else 0
        self.completed.update(done)
        self.current = None

    def _end(self, body):
        cls, cause = body['class'], body['cause']
        self._close(cause=cause, reasons=[worker['reason'] for worker in body['workers']])
        cap = self.cap()
        # F8: at a cap a cause below HALTED is replaced by the cap code; a HALTED or TERMINAL
        # cause stands, and the cap stays reached until a HALT on it and its own CONTINUE. A
        # cap code is recorded only when it is the cap reached.
        _corrupt((cap is not None and cls in (STOPPED, COMPLETE))
                 or (cause in _CAPS and cause != cap))
        self.halt_code = cause if cls == HALTED else self.halt_code
        self.complete = self.complete or cls == COMPLETE

    def _crashed(self, body):  # F1: the recorded cap is the one this crash reaches
        _corrupt(body['k'] != self.current)
        self._close(crashed=body['losses'])
        _corrupt(body['cap'] != self.cap())
        self.halt_code = body['cap'] or self.halt_code

    def _halt(self, body):  # F8: a cap code needs its cap reached
        _corrupt(body['code'] in _CAPS and not self.reached(body['code']))
        self.halt_code = body['code']

    def _act(self, body):  # CONTINUE resets only the cap that halted the run (§4.5, F8)
        if body['act'] != 'CONTINUE':
            return
        if self.halt_code == 'RESOURCE_EXHAUSTED':
            self.losses = {key: count for key, count in self.losses.items() if count < LOSS_CAP}
        elif self.halt_code == 'IO_EXHAUSTED':
            self.io_run = 0
        self.halt_code = None

    def _all_done(self, _body):
        _corrupt(self.cap() is not None)  # F8
        self.complete = True


def _check_verifies(ledger, verifies, plan):
    started = {record['body']['n']: {tuple(key) for key in record['body']['keys']}
               for record in ledger if record['type'] == 'VERIFY_START'}
    _corrupt(set(verifies) - set(started) or any(not keys <= plan for keys in started.values()))
    for n, workers in verifies.items():
        _corrupt(any(key not in started[n] for records in workers.values()
                     for key in _keys(records)))


def _divergent(paths):
    seen = {}
    for body in paths:
        row = {name: value for name, value in body.items() if name not in _TIMING}
        if seen.setdefault(tuple(row['key']), row) != row:
            return True
    return False


def _finding(walk, found, plan):
    if walk.complete and walk.completed != plan:  # O-11: after COMPLETE every key occurs
        return CORRUPTION
    if len(found.closures) > 1 or found.close_failed:  # O-8, row K6
        return 'CODE_OR_ARTIFACT_DRIFT'
    if _divergent(found.paths):  # row S13
        return 'NONDETERMINISM'
    return walk.cap()


def _check(ledger, journals, manifest, acts, plan):
    _chain(ledger, kind='ledger')
    try:
        fold(ledger)
    except (IllegalTransition, journal.JournalCorrupt):
        raise _Failed(CORRUPTION) from None
    if not ledger:
        _corrupt(journals or acts or manifest is not None)
        return RecordCheck(None)
    authority = ledger[0]['body']['authority_sha256']
    found = _Journals()
    for name, records in journals.items():
        found.add(name, records)
    _check_manifest(ledger, manifest, authority, found.candidates)
    _check_acts(ledger, acts, authority)
    walk = _Walk(plan, found.segments).run(ledger)
    _check_verifies(ledger, found.verifies, plan)
    return RecordCheck(_finding(walk, found, plan), frozenset(walk.completed),
                       MappingProxyType(dict(walk.losses)))


def _plan(keys):
    plan = frozenset(tuple(key) for key in keys)
    if not all(journal.is_key(list(key)) for key in plan):
        raise ValueError('plan keys must be (root, population, path index)')
    return plan


def cap_finding(ledger: Sequence[journal.Record], journals: Mapping[str, Sequence[journal.Record]],
                *, keys: Sequence[journal.Key], cause: str | None = None,
                reasons: Sequence[str] = ()) -> str | None:
    """The row S10 cap reached and not reset by CONTINUE (card F8): ``RESOURCE_EXHAUSTED`` if a
    key has three losses, else ``IO_EXHAUSTED`` after three I/O-error segments with no new
    completed key, else ``None``.

    A trailing open segment is closed with ``cause`` and the worker ``reasons``; ``cause=None``
    reads as a crash. An in-flight KEY_START is a loss unless a WORKER_STOP names it or the
    cause is ``INTERRUPTED``. I/O evidence is ``IO_ERROR`` as the cause, a worker reason or a
    journal WORKER_STOP reason; a recorded cap code is never its own evidence. ``check_record``
    applies this computation at every SEGMENT_END and SEGMENT_CRASHED; the coordinator calls it
    to fill ``SEGMENT_CRASHED.cap`` and to choose a SEGMENT_END cause. A record that fails
    ``check_record``'s structure raises ``journal.JournalCorrupt``.
    """
    plan = _plan(keys)
    try:
        ledger = tuple(ledger)
        _chain(ledger, kind='ledger')
        found = _Journals()
        for name, records in dict(journals).items():
            found.add(name, records)
        return _Walk(plan, found.segments).run(ledger, cause, tuple(reasons)).cap()
    except _Failed:
        raise journal.JournalCorrupt('the run record fails its structural checks') from None


def check_record(ledger: Sequence[journal.Record], journals: Mapping[str, Sequence[journal.Record]],
                 manifest: Mapping[str, object] | None, acts: Mapping[str, bytes], *,
                 keys: Sequence[journal.Key]) -> RecordCheck:
    """The first failure over a whole run record, or ``None``.

    In order: TERMINAL ``CORRUPTION`` (chains, schemas, strict and unique journal names (F6), a
    key outside the plan or its worker's assignment and not a tagged witness, an assignment
    digest other than ``sorted(K - completed)[i::W]``'s (F3), witnesses other than
    ``min(W, |completed|)`` distinct completed keys each run first by its worker (F2), a
    SEGMENT_CRASHED whose ``cap`` differs from ``cap_finding`` there (F1), a SEGMENT_END whose
    cause is below HALTED when a cap is reached or names a cap other than the one reached, a
    HALT naming a cap not reached, a SEGMENT_START or ALL_DONE while a cap is reached (F8),
    manifest and candidates, act bindings, a gap after COMPLETE), ``CODE_OR_ARTIFACT_DRIFT``
    (epoch closures), ``NONDETERMINISM`` (duplicates and witnesses); then HALTED
    ``RESOURCE_EXHAUSTED`` or ``IO_EXHAUSTED`` (``cap_finding`` at the end of the ledger).
    ``completed`` holds the plan keys with a PATH in a segment
    journal; ``losses`` counts each key's losses since the CONTINUE that reset its cap. A
    trailing segment without SEGMENT_END or SEGMENT_CRASHED reads as crashed (found at resume),
    so a HALTED ``code`` then names the ``cap`` its SEGMENT_CRASHED must carry. A structural
    ``CORRUPTION`` found before the ledger walk ends returns empty ``completed`` and ``losses``.
    """
    plan = _plan(keys)
    try:
        return _check(tuple(ledger), dict(journals), manifest, dict(acts), plan)
    except _Failed as failed:
        return RecordCheck(failed.code)
