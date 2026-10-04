"""T00 step-3 run-directory records (design 2026-10-02 §4.1; build card §3.4-§3.5, §3.6a).

Every line of ``ledger/*.jsonl`` and ``journal/*.jsonl`` is
``canonical_json_bytes({"body": ..., "prev_sha256": ..., "type": ...}) + LF``. A record's
SHA-256 is that of its line without the LF, and ``prev_sha256`` chains it to the previous
record (row S3). Bodies have closed schemas, cost fields included (row B1), checked before a
write and on every read. ``results`` renders ``results.json`` from digests and the verdict
only: no timestamp, W, approval or timing (row S16).
"""
from __future__ import annotations

import errno
import hashlib
import math
import os
import re
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

try:
    from msvcrt import setmode as _setmode
except ImportError:  # POSIX: no text mode to clear
    _setmode = None

from ..contract import ContractValidationError, canonical_json_bytes, parse_canonical_json

# Exact JSON types are intended: bool is an int subclass, so isinstance() would admit it.
# pylint: disable=unidiomatic-typecheck

CORRUPTION = 'CORRUPTION'
LOCK_OFFSET = 1 << 20
LOCK_SCHEMA = 't00_screen_lock/v1'
RESULTS_SCHEMA = 't00_screen_results/v1'
POPULATIONS = ('FULL', 'H1', 'H2')
JOURNAL_NAME = re.compile(r'([csv])([0-9]+)-w([0-9]+)[.]jsonl')

Record = Mapping[str, object]
Key = tuple[str, str, int]
Outcome = Mapping[str, object]


class JournalCorrupt(ValueError):
    """A record or file breaks its chain or schema; TERMINAL ``CORRUPTION`` (design §4.3)."""
    code = CORRUPTION

    def __init__(self, detail):
        super().__init__(f'{CORRUPTION}: {detail}')


def _hex(value):
    return type(value) is str and re.fullmatch(r'[0-9a-f]{64}', value) is not None


def _num(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def _count(value):
    return type(value) is int and value >= 0


def _positive(value):
    return type(value) is int and value >= 1


def _text(value):
    return type(value) is str and value != ''


def _bool(value):
    return type(value) is bool


def _seed(value):
    return type(value) is int and 0 <= value < 1 << 64


def _cost(value):
    return (type(value) is dict and set(value) == {'cpu_s', 'wall_s'}
            and all(map(_num, value.values())))


def is_key(value):
    """A Key as a JSON list: [root, population, path index] (design §7)."""
    return (type(value) is list and len(value) == 3 and _text(value[0])
            and value[1] in POPULATIONS and _count(value[2]))


def _one_of(*allowed):
    return lambda value: type(value) is str and value in allowed


def _optional(check):
    return lambda value: value is None or check(value)


def _list(check):
    return lambda value: type(value) is list and all(map(check, value))


def _object(fields):
    fields = MappingProxyType(fields)
    return lambda value: (type(value) is dict and set(value) == set(fields)
                          and all(check(value[name]) for name, check in fields.items()))


_RUN_FIELDS = _object({  # P7's projection names (p7_driver.py:55-65) plus the kernel outcome
    'digest': _hex, 'sessions': _count, 'fills': _count, 'events_sha256': _hex,
    'deadline_failure': _bool, 'consumed_intrabar_split_count': _count,
    'consumed_intrabar_splits_sha256': _hex, 'status': _one_of('PASS', 'FAILURE', 'UNRESOLVED'),
    'sessions_to_pass': _optional(_count), 'failure_reason': _optional(_text),
    'kernel_outcome': _text})


def _frozen(table):
    """A record-type table as read-only mappings (no module global is ever mutated)."""
    return MappingProxyType({name: MappingProxyType(fields) for name, fields in table.items()})


_POPULATION = _object({'indices': _list(_count), 'candidates_sha256': _hex})


def _run(value):
    """One run of a PATH (no P&L series); ``model.PathOutcome``'s rule: PASS has a session
    count and no failure reason, FAILURE and UNRESOLVED the reverse."""
    if not _RUN_FIELDS(value):
        return False
    passed = value['status'] == 'PASS'
    return (value['sessions_to_pass'] is not None) == passed == (value['failure_reason'] is None)


def _populations(value):
    return (type(value) is dict and set(value) == set(POPULATIONS)
            and all(map(_POPULATION, value.values())))


def _bracket_agrees(body):
    """``bracket.BracketVerdict``'s rule: the runs' status where both agree, else UNDETERMINED."""
    first, second = body['runs']['r1']['status'], body['runs']['r2']['status']
    return body['bracket_status'] == (first if first == second else 'UNDETERMINED')


LEDGER_BODIES = _frozen({
    'AUTHORITY_BOUND': {'authority_sha256': _hex, 'prereg_path': _text, 'approvals': _list(_hex),
                        'reused_directory': _bool},
    'PREPARED': {'manifest_sha256': _hex, 'build': _cost, 'integrity': _cost},
    'PROBE_START': {}, 'ALL_DONE': {},
    'PROBE': {'path_cpu_s': _num, 'path_wall_s': _num, 'peak_memory_bytes': _count},
    'SEGMENT_START': {'k': _positive, 'w': _positive, 'assignment_sha256': _hex,
                      'witness_keys': _list(is_key), 'approvals': _list(_hex)},
    'HEARTBEAT': {'wall_s': _num, 'job_cpu_s': _num},
    'SEGMENT_END': {'class': _one_of('STOPPED', 'HALTED', 'TERMINAL', 'COMPLETE'),
                    'cause': _text, 'workers': _list(_object({'worker': _text, 'reason': _text})),
                    'wall_s': _num, 'job_cpu_s': _num, 'path_cpu_s': _num,
                    'overhead_cpu_s': _num, 'peak_memory_bytes': _count},
    'SEGMENT_CRASHED': {'k': _positive, 'charge': _cost, 'losses': _list(is_key),
                        'cap': _optional(_one_of('RESOURCE_EXHAUSTED', 'IO_EXHAUSTED'))},
    'HALT': {'code': _text, 'from': _text},
    'TERMINAL': {'code': _text},
    'ACT': {'act_sha256': _hex, 'act': _one_of('TERMINATE', 'CONTINUE')},
    'AGGREGATED': {'results_sha256': _hex}, 'REPORTED': {'report_sha256': _hex},
    'FINAL': {'attestation_sha256': _hex},
    'VERIFY_START': {'n': _positive, 'keys': _list(is_key)},
    'VERIFY': {'n': _positive, 'keys': _list(is_key), 'match': _bool},
})
JOURNAL_BODIES = _frozen({
    'EPOCH_OPEN': {'build': _cost, 'integrity': _cost, 'closure_sha256': _hex,
                   'guard_sha256': _hex},
    'KEY_START': {'key': is_key},
    'PATH': {'key': is_key, 'seed': _seed, 'path_sha256': _hex,
             'bracket_status': _one_of('PASS', 'FAILURE', 'UNRESOLVED', 'UNDETERMINED'),
             'runs': _object({'r1': _run, 'r2': _run}), 'wall_s': _num, 'cpu_s': _num},
    'CANDIDATES': {'populations': _populations},
    'PROBE_RESULT': {'path_cpu_s': _num, 'path_wall_s': _num, 'peak_memory_bytes': _count},
    'EPOCH_CLOSE': {'integrity': _cost, 'closure_match': _bool},
    'WORKER_STOP': {'reason': _text, 'key': _optional(is_key)},
})
_AGREES = MappingProxyType({'PATH': _bracket_agrees})  # cross-field rules, once fields are valid
_TABLES = MappingProxyType({'ledger': (LEDGER_BODIES,), 'journal': (JOURNAL_BODIES,),
                            None: (LEDGER_BODIES, JOURNAL_BODIES)})


def validate_body(record_type, body, *, kind=None):
    """Refuse a body outside its type's closed schema (row B1); ``kind`` limits the types."""
    fields = next((table[record_type] for table in _TABLES[kind] if type(record_type) is str
                   and record_type in table), None)
    if fields is None:
        raise JournalCorrupt(f'{record_type!r} is not a {kind or "run"} record type')
    if type(body) is not dict or set(body) != set(fields):
        raise JournalCorrupt(f'{record_type} body fields differ from its schema')
    bad = sorted(name for name, check in fields.items() if not check(body[name]))
    if bad:
        raise JournalCorrupt(f'{record_type} body field(s) invalid: {", ".join(bad)}')
    if not _AGREES.get(record_type, lambda _: True)(body):
        raise JournalCorrupt(f'{record_type} body fields disagree with each other')


def _kind(path):
    return {'ledger': 'ledger', 'journal': 'journal'}.get(Path(path).parent.name)


def record_sha256(record: Record) -> str:
    """The SHA-256 of a record's line without its LF (card §3.4)."""
    return hashlib.sha256(canonical_json_bytes(dict(record))).hexdigest()


def append(fd: int, type: str, body: Mapping[str, object], *,  # pylint: disable=redefined-builtin
           prev_sha256: str | None) -> str:
    """One ``os.write`` of the record line, then ``os.fsync``; returns the record's SHA-256.

    ``fd`` is opened ``O_WRONLY | O_APPEND | O_BINARY`` by its single writer; on Windows binary
    mode is set again here, so no LF becomes CRLF. A body outside its schema is refused before
    anything is written (row B1).

    After ``append`` raises, the writer appends nothing more to that file (card F4): the line
    may be on disk while the writer holds no SHA-256 for it, so a further record would chain
    from a stale ``prev_sha256`` and read as CORRUPTION. A worker then exits without
    WORKER_STOP and reports IO_ERROR; the coordinator names it ``IO_ERROR`` in SEGMENT_END.
    The rule is the writer's (P-F); this module keeps no state between calls.
    """
    if prev_sha256 is not None and not _hex(prev_sha256):
        raise JournalCorrupt('prev_sha256 must be null or a SHA-256')
    validate_body(type, body)
    try:
        raw = canonical_json_bytes({'body': body, 'prev_sha256': prev_sha256, 'type': type})
    except ContractValidationError as exc:
        raise JournalCorrupt(str(exc)) from None
    line = raw + b'\n'
    if _setmode is not None:
        _setmode(fd, os.O_BINARY)
    written = os.write(fd, line)
    if written != len(line):
        raise OSError(errno.EIO, f'short record write: {written} of {len(line)} bytes')
    os.fsync(fd)
    return hashlib.sha256(raw).hexdigest()


def _parse(raw):
    try:
        return parse_canonical_json(raw, label='record')
    except ContractValidationError:
        return None


def read(path, *, prev_sha256: str | None) -> tuple[Record, ...]:
    """Every record, its chain verified from ``prev_sha256`` (row S3).

    Only a torn final line is dropped: bytes after the last LF, or an unparseable last line.
    Any other break raises ``JournalCorrupt``. A file under ``ledger/`` or ``journal/`` holds
    only that kind's record types.
    """
    kind = _kind(path)
    lines = Path(path).read_bytes().split(b'\n')
    if lines.pop() == b'' and lines and _parse(lines[-1]) is None:
        lines.pop()  # an LF-terminated but unparseable last line is torn as well
    records, prev = [], prev_sha256
    for number, raw in enumerate(lines, 1):
        record = _parse(raw)
        if type(record) is not dict or set(record) != {'body', 'prev_sha256', 'type'}:
            raise JournalCorrupt(f'{Path(path).name}:{number} is not a record line')
        if record['prev_sha256'] != prev:
            raise JournalCorrupt(f'{Path(path).name}:{number} breaks the hash chain')
        validate_body(record['type'], record['body'], kind=kind)
        records.append(record)
        prev = hashlib.sha256(raw).hexdigest()
    return tuple(records)


def read_lock(path) -> tuple[int, str]:
    """(pid, host) of a run or run-root lock; the byte at ``LOCK_OFFSET`` is never read.

    The content is exactly the canonical lock document; a holder's rewrite truncates the file
    to it (card F5), so stale trailing bytes are refused here.
    """
    with open(path, 'rb') as handle:
        raw = handle.read(LOCK_OFFSET)
    doc = _parse(raw)
    if (type(doc) is not dict or set(doc) != {'host', 'pid', 'schema'}
            or doc['schema'] != LOCK_SCHEMA or not _text(doc['host'])
            or not _positive(doc['pid'])):
        raise JournalCorrupt(f'lock content is not {LOCK_SCHEMA}')
    return doc['pid'], doc['host']


def journal_name(name):
    """(kind, number, worker) of a journal file name, or ``None``. The name is exactly
    ``f'{kind}{number}-w{worker}.jsonl'`` with decimal, unpadded numbers and ``number >= 1``
    (card §3.3, F6), so no two names share a (kind, number, worker)."""
    found = JOURNAL_NAME.fullmatch(name) if type(name) is str else None
    if found is None:
        return None
    kind, number, worker = found.group(1), int(found.group(2)), int(found.group(3))
    return (kind, number, worker) if number and name == f'{kind}{number}-w{worker}.jsonl' else None


def outcomes(journals: Mapping[str, Sequence[Record]],
             keys: Sequence[Key]) -> tuple[Outcome, ...]:
    """Per plan key, the first PATH body of the segment journals without ``wall_s`` and
    ``cpu_s``, sorted by key. Duplicates are equal by row S13, so which is first never matters."""
    wanted = {tuple(key) for key in keys}
    order = sorted((parsed[1:], name) for name, parsed in ((n, journal_name(n)) for n in journals)
                   if parsed is not None and parsed[0] == 's')
    first = {}
    for _, name in order:
        for record in journals[name]:
            key = tuple(record['body']['key']) if record['type'] == 'PATH' else None
            if key in wanted and key not in first:
                first[key] = {field: value for field, value in record['body'].items()
                              if field not in ('wall_s', 'cpu_s')}
    return tuple(first[key] for key in sorted(first))


def results(*, authority_sha256: str, contract_sha256: str, p7_record_sha256: str,
            plan_sha256: str, verdict: Mapping[str, object]) -> bytes:
    """The canonical bytes of ``results.json`` (row S16); ``verdict`` is
    ``verdict.as_json(...)``."""
    digests = {'authority_sha256': authority_sha256, 'contract_sha256': contract_sha256,
               'p7_record_sha256': p7_record_sha256, 'plan_sha256': plan_sha256}
    bad = sorted(name for name, value in digests.items() if not _hex(value))
    if bad:
        raise ValueError(f'results digests must be SHA-256 hex: {", ".join(bad)}')
    if not isinstance(verdict, Mapping) or verdict.get('kind') not in ('INSUFFICIENT', 'LABELLED'):
        raise ValueError('results verdict must be verdict.as_json output')
    return canonical_json_bytes({**digests, 'schema': RESULTS_SCHEMA, 'verdict': dict(verdict)})
