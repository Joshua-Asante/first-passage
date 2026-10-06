"""T00 step-3 screen coordinator (design 2026-10-02 §4-§5; build card §2.9, §3.3-§3.6a, P-F note).

The coordinator is the only ledger writer (row S2). It holds ``<run_dir>/lock`` for its whole
invocation and ``<run_root>/lock`` while it creates or binds a run directory (card §3.4), appends
a ledger event only after ``state.advance`` accepts it (row S1), and starts workers suspended
inside a Windows Job Object with ``JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`` (row S12), so they die
with it. Durable state is the fold of the ledger; every decision at ``resume`` is taken from the
ledger and journals on disk.

Budgets are CPU seconds (design §5.4): the dispatch gate books path CPU from the first PATH of
each plan key only (row B4); overhead (the candidate pass, the probe, every segment's job CPU
beyond its booked path CPU and every crash charge) is checked before each segment (row B5).
A crashed segment is charged its last heartbeat plus one interval of wall, and that heartbeat's
job CPU plus one interval x W less the path CPU its PATH records already booked (card §3.5
clarification 2026-10-03). Caps follow card F1/F8 and note item 5; ``check_record`` gets the
pinned ``source:`` keys and the real time (note item 6).

Named encodings chosen here (card K-4 latitude; behaviour of the design unchanged):
- a non-terminal, non-lapse stop in BOUND is recorded as HALT ``UNCLASSIFIED_ERROR`` (the closed
  §4.3 table has no other HALTED code for it); a crash in PREPARED re-times the probe (W1);
- PREPARED's ``build`` is the candidate worker's build plus its candidate pass, its
  ``integrity`` the candidate epoch's opening and closing checks;
- candidate journals are ``c1-w0``, ``c2-w0``, ... with no gap; ``finalize`` refuses CORRUPTION
  for any other file under ``journal/`` (note item 12).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import queue
import re
import socket
import subprocess
import sys
import threading
import time
import traceback
from typing import Mapping

from .. import p7_evidence, screen_authority
from ..contract import (ContractValidationError, TrustedApprovalKey, _check_source_key_lifecycle,
                        _pinned_source_keys, canonical_json_bytes, parse_canonical_json,
                        require_validated_source_contract)
from . import journal, plan, state, verdict
from .worker import PROTOCOL, decode_inputs, source_receipt

HEARTBEAT_S = 60
VERIFY_K = 9
STOPPED, HALTED, TERMINAL, COMPLETE = state.STOPPED, state.HALTED, state.TERMINAL, state.COMPLETE
_PRECEDENCE = {COMPLETE: 0, STOPPED: 1, HALTED: 2, TERMINAL: 3}
_LAPSE = 'APPROVAL_LAPSE'
_CODE = re.compile(r'([A-Z][A-Z0-9_]*):')
_BINARY = getattr(os, 'O_BINARY', 0)
_CREATE_SUSPENDED, _CREATE_NEW_PROCESS_GROUP, _CREATE_NO_WINDOW = 0x4, 0x200, 0x08000000
ATTESTATION_SCHEMA = 't00_screen_attestation/v1'
ACCEPTANCE_SCHEMA = 't00_screen_p7_acceptance/v1'


class ScreenRefusal(Exception):
    """A refusal; the console prints ``code`` alone (row X1)."""

    def __init__(self, code: str, detail: str = ''):
        super().__init__(f'{code}: {detail}' if detail else code)
        self.code = code


def refusal_code(exc: BaseException, default: str) -> str:
    """An exception's own code (attribute or leading ``CODE:``), else ``default``."""
    named = getattr(exc, 'code', None)
    if isinstance(named, str) and re.fullmatch(r'[A-Z][A-Z0-9_]*', named):
        return named
    found = _CODE.match(str(exc))
    return found.group(1) if found else default


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _now(now=None) -> datetime:
    return datetime.now(timezone.utc) if now is None else now


# ---- launch inputs -----------------------------------------------------------------------------

@dataclass(frozen=True)
class Inputs:  # pylint: disable=too-many-instance-attributes
    """The launch bytes: the signed authority and its approval, r3c and its approval, the pinned
    public keys, the accepted P7 record, and the private root (``artifact_root``)."""
    authority: bytes
    approval: bytes
    source_contract: bytes
    source_approval: bytes
    public_keys: Mapping[str, bytes]
    p7_record: bytes
    artifact_root: Path

    @property
    def authority_sha256(self) -> str:
        return _sha(self.authority)

    @property
    def run_dir(self) -> Path:
        return (Path(self.artifact_root) / screen_authority.RUN_ROOT_NAME).resolve() / self.authority_sha256

    def message(self) -> dict:
        """The worker's copy (``worker.decode_inputs``)."""
        def b64(raw):
            return base64.b64encode(raw).decode('ascii')
        return {'authority_b64': b64(self.authority), 'approval_b64': b64(self.approval),
                'source_contract_b64': b64(self.source_contract), 'source_approval_b64': b64(self.source_approval),
                'p7_record_b64': b64(self.p7_record),
                'public_keys': {key: b64(raw) for key, raw in sorted(self.public_keys.items())},
                'artifact_root': str(Path(self.artifact_root).resolve())}


def _window_lapsed(approval_bytes: bytes, now: datetime) -> bool:
    """True when an approval's own signed window does not contain ``now`` (row K2, W8)."""
    try:
        payload = parse_canonical_json(approval_bytes, label='approval')['payload']
        issued = datetime.fromisoformat(payload['issued_at'].replace('Z', '+00:00'))
        expires = datetime.fromisoformat(payload['expires_at'].replace('Z', '+00:00'))
    except (ContractValidationError, KeyError, TypeError, ValueError, AttributeError):
        return False
    return not issued <= now < expires


def lapsed(inputs: Inputs, now: datetime) -> bool:
    return _window_lapsed(inputs.approval, now) or _window_lapsed(inputs.source_approval, now)


def launch_checks(inputs: Inputs, now: datetime):
    """r3c and the authority validated afresh (rows A1-A11): (receipt, authority)."""
    raw, keys, root = decode_inputs(inputs.message())
    receipt = source_receipt(raw['source_contract_b64'], raw['source_approval_b64'], keys, root, now)
    auth = screen_authority.validate_screen_authority(
        inputs.authority, inputs.approval, dict(inputs.public_keys), source_receipt=receipt,
        p7_record_bytes=inputs.p7_record, artifact_root=inputs.artifact_root, now=now)
    return receipt, auth


def _check_lifecycles(receipt, auth, now) -> str | None:
    """Both approval windows and the pin lifecycle (row K2): None, the lapse code, or a
    key-lifecycle code."""
    try:
        require_validated_source_contract(receipt, now=now)
        _check_source_key_lifecycle(auth.approval, now, auth.key_sha256)
    except ContractValidationError as exc:
        return state.classify(refusal_code(exc, state.UNCLASSIFIED_ERROR))[1]
    return None


def trusted_keys(public_keys: Mapping[str, bytes]) -> dict:
    """The pinned, lifecycle-checked ``source:`` keys for ``check_record`` (card note item 6)."""
    pinned = _pinned_source_keys()
    keys = {}
    for key_id, pin in pinned.items():
        raw = public_keys.get(key_id)
        if type(raw) is not bytes or _sha(raw) != pin.sha256:
            raise ScreenRefusal('SCREEN_TRUST_ROOT_MISMATCH', 'supplied public keys differ from the pinned root')
        keys[key_id] = TrustedApprovalKey(key_id, raw, 'OPERATOR', pin.revoked_at)
    return keys


def _document(inputs: Inputs) -> dict:
    return parse_canonical_json(inputs.authority, label='screen authority')


def plan_keys(params) -> tuple:
    return plan.key_universe(params['rng']['roots'], params['depth_per_root'])


# ---- locks (card §3.4) --------------------------------------------------------------------------

class _Lock:
    """A run or run-root lock: ``msvcrt.locking`` on the byte at ``journal.LOCK_OFFSET``."""

    def __init__(self, path: Path):
        try:
            import msvcrt  # pylint: disable=import-outside-toplevel
        except ImportError:
            raise ScreenRefusal('SCREEN_PLATFORM_UNSUPPORTED', 'the run locks are msvcrt byte-range locks') from None
        self.msvcrt, self.path = msvcrt, path
        self.fd = os.open(path, os.O_RDWR | os.O_CREAT | _BINARY, 0o644)
        try:
            os.lseek(self.fd, journal.LOCK_OFFSET, os.SEEK_SET)
            msvcrt.locking(self.fd, msvcrt.LK_NBLCK, 1)
        except OSError:
            os.close(self.fd)
            raise ScreenRefusal('SCREEN_WORKERS_ALIVE', f'{path.name} is held') from None
        content = canonical_json_bytes({'host': socket.gethostname(), 'pid': os.getpid(),
                                        'schema': journal.LOCK_SCHEMA})
        os.lseek(self.fd, 0, os.SEEK_SET)
        os.write(self.fd, content)
        os.ftruncate(self.fd, len(content))  # card F5: a rewrite truncates to the content
        os.fsync(self.fd)

    def release(self):
        if self.fd is None:
            return
        try:
            os.lseek(self.fd, journal.LOCK_OFFSET, os.SEEK_SET)
            self.msvcrt.locking(self.fd, self.msvcrt.LK_UNLCK, 1)
        finally:
            os.close(self.fd)
            self.fd = None


def _probe_lock(path: Path) -> None:
    """Refuse while ``path`` is held by anyone (row S8): take it and release it at once."""
    if path.exists():
        _Lock(path).release()


# ---- the run record ----------------------------------------------------------------------------

def _ledger_files(run_dir: Path):
    folder = run_dir / 'ledger'
    if not folder.is_dir():
        return []
    return sorted((int(path.stem), path) for path in folder.iterdir()
                  if path.suffix == '.jsonl' and re.fullmatch(r'[0-9]{4}', path.stem))


def read_ledger(run_dir: Path) -> tuple:
    """Every ledger record, each file chained to the last valid record of the one before (card §3.4)."""
    records, prev = [], None
    for _, path in _ledger_files(run_dir):
        rows = journal.read(path, prev_sha256=prev)
        records.extend(rows)
        if rows:
            prev = journal.record_sha256(rows[-1])
    return tuple(records)


def read_journals(run_dir: Path) -> dict:
    folder = run_dir / 'journal'
    if not folder.is_dir():
        return {}
    return {path.name: journal.read(path, prev_sha256=None) for path in sorted(folder.iterdir())}


def read_manifest(run_dir: Path):
    path = run_dir / 'manifest.json'
    return parse_canonical_json(path.read_bytes(), label='manifest') if path.is_file() else None


def read_acts(run_dir: Path) -> dict:
    folder = run_dir / 'acts'
    return {path.name: path.read_bytes() for path in sorted(folder.iterdir())} if folder.is_dir() else {}


def _head(records) -> str | None:
    return journal.record_sha256(records[-1]) if records else None


def _fsync_dir(path: Path) -> None:
    if os.name != 'nt':
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def _write_atomic(path: Path, raw: bytes) -> None:
    """Temp file, fsync, ``os.replace`` (design §4.1)."""
    temporary = path.with_name(path.name + '.tmp')
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | _BINARY, 0o644)
    try:
        os.write(fd, raw)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(temporary, path)
    _fsync_dir(path.parent)


def _write_once(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | _BINARY, 0o644)
    try:
        os.write(fd, raw)
        os.fsync(fd)
    finally:
        os.close(fd)


class Ledger:
    """The run's ledger: one new file per invocation, created at its first append (card §3.4)."""

    def __init__(self, run_dir: Path, *, number: int | None = None):
        self.folder = run_dir / 'ledger'
        self.records = list(read_ledger(run_dir))
        self.state = state.fold(self.records)
        files = _ledger_files(run_dir)
        self.number = number if number is not None else (files[-1][0] + 1 if files else 1)
        self.fd = None

    @property
    def head(self) -> str | None:
        return _head(self.records)

    def append(self, kind: str, body: dict) -> str:
        """``advance`` first: a refused event writes nothing (row S1)."""
        event = {'body': body, 'prev_sha256': self.head, 'type': kind}
        after = state.advance(self.state, event)
        if self.fd is None:
            self.folder.mkdir(exist_ok=True)
            self.fd = os.open(self.folder / f'{self.number:04d}.jsonl',
                              os.O_WRONLY | os.O_APPEND | os.O_CREAT | _BINARY, 0o644)
        journal.append(self.fd, kind, body, prev_sha256=self.head)
        self.records.append(event)
        self.state = after
        return journal.record_sha256(event)

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None


def terminal_codes(ledger) -> list:
    """The run's TERMINAL codes, in order: TERMINAL records, TERMINAL segment ends and TERMINATE acts."""
    codes = []
    for record in ledger:
        body = record['body']
        if record['type'] == 'TERMINAL':
            codes.append(body['code'])
        elif record['type'] == 'SEGMENT_END' and body['class'] == TERMINAL:
            codes.append(body['cause'])
        elif record['type'] == 'ACT' and body['act'] == 'TERMINATE':
            codes.append(state.OPERATOR_TERMINATED)
    return codes


def _last_halt(ledger) -> str | None:
    for record in reversed(ledger):
        if record['type'] == 'HALT':
            return record['body']['code']
        if record['type'] == 'SEGMENT_END' and record['body']['class'] == HALTED:
            return record['body']['cause']
        if record['type'] == 'SEGMENT_CRASHED' and record['body']['cap'] is not None:
            return record['body']['cap']
    return None


def _segment_journals(journals, k):
    found = {}
    for name, records in journals.items():
        parsed = journal.journal_name(name)
        if parsed is not None and parsed[0] == 's' and parsed[1] == k:
            found[parsed[2]] = records
    return found


def _ordered(journals, prefix):
    rows = []
    for name, records in journals.items():
        parsed = journal.journal_name(name)
        if parsed is not None and parsed[0] == prefix:
            rows.append((parsed[1], parsed[2], name, records))
    return sorted(rows)


def booked_path_cpu(journals, keys) -> float:
    """Row B4: ``cpu_s`` of the first PATH of each plan key in the segment journals only."""
    wanted, seen, total = {tuple(key) for key in keys}, set(), 0.0
    for _, _, _, records in _ordered(journals, 's'):
        for record in records:
            if record['type'] == 'PATH':
                key = tuple(record['body']['key'])
                if key in wanted and key not in seen:
                    seen.add(key)
                    total += record['body']['cpu_s']
    return total


def _segment_booked(journals, k, booked_before) -> float:
    """The path CPU segment ``k``'s PATH records booked (keys first completed there)."""
    total = 0.0
    seen = set(booked_before)
    for _, records in sorted(_segment_journals(journals, k).items()):
        for record in records:
            if record['type'] == 'PATH':
                key = tuple(record['body']['key'])
                if key not in seen:
                    seen.add(key)
                    total += record['body']['cpu_s']
    return total


def _keys_before(journals, k) -> set:
    done = set()
    for number, _, _, records in _ordered(journals, 's'):
        if number < k:
            done.update(tuple(r['body']['key']) for r in records if r['type'] == 'PATH')
    return done


def crash_charge(ledger, journals, *, k: int, w: int) -> dict:
    """Row S11/B5 and the card §3.5 clarification: the last heartbeat (SEGMENT_START is heartbeat 0)
    plus one interval of wall; that heartbeat's job CPU plus one interval x W, less the path CPU the
    segment's PATH records booked; never negative."""
    wall = cpu = 0.0
    started = False
    for record in ledger:
        if record['type'] == 'SEGMENT_START' and record['body']['k'] == k:
            started, wall, cpu = True, 0.0, 0.0
        elif started and record['type'] == 'HEARTBEAT':
            wall, cpu = record['body']['wall_s'], record['body']['job_cpu_s']
    booked = _segment_booked(journals, k, _keys_before(journals, k))
    return {'cpu_s': max(0.0, cpu + HEARTBEAT_S * w - booked), 'wall_s': wall + HEARTBEAT_S}


def overhead_used(ledger, journals) -> float:
    """Row B5: overhead CPU since the last CONTINUE that answered an OVERHEAD_EXHAUSTED halt. The
    candidate-and-probe journals' share (``candidate_overhead``) is counted at the last PROBE, or at
    the end before any PROBE."""
    total, halted_on = 0.0, None
    probes = [i for i, record in enumerate(ledger) if record['type'] == 'PROBE']
    at = probes[-1] if probes else None
    for index, record in enumerate(ledger):
        kind, body = record['type'], record['body']
        if kind == 'PREPARED':
            total += body['build']['cpu_s'] + body['integrity']['cpu_s']
        elif kind == 'PROBE':
            total += body['path_cpu_s']
        elif kind == 'SEGMENT_END':
            total += body['overhead_cpu_s']
        elif kind == 'SEGMENT_CRASHED':
            total += body['charge']['cpu_s']
        elif kind == 'HALT':
            halted_on = body['code']
        elif kind == 'ACT' and body['act'] == 'CONTINUE':
            if halted_on == 'OVERHEAD_EXHAUSTED':
                total = 0.0
            halted_on = None
        if index == at:
            total += candidate_overhead(ledger, journals)
    return total + (candidate_overhead(ledger, journals) if at is None else 0.0)


def _epochs(records) -> list:
    """(cost CPU, holds CANDIDATES, holds PROBE_RESULT) per epoch of one journal."""
    epochs = []
    for record in records:
        kind, body = record['type'], record['body']
        if kind == 'EPOCH_OPEN':
            epochs.append([body['build']['cpu_s'] + body['integrity']['cpu_s'], False, False])
        elif epochs and kind == 'EPOCH_CLOSE':
            epochs[-1][0] += body['integrity']['cpu_s']
        elif epochs and kind == 'CANDIDATES':
            epochs[-1][1] = True
        elif epochs and kind == 'PROBE_RESULT':
            epochs[-1][2] = True
    return epochs


def candidate_overhead(ledger, journals) -> float:
    """The candidate and probe journals' overhead that PREPARED and PROBE do not carry (design §5.4,
    a crash can only overcharge). The candidate attempt PREPARED records is the highest-numbered
    candidate journal with CANDIDATES; its candidate epoch is PREPARED's. Every other candidate
    attempt never reached PREPARED and is charged as a crash: one heartbeat interval for its one
    worker (heartbeat 0 is its start) plus every epoch cost its journal recorded. A probe epoch is
    charged its recorded costs, plus the interval when it ended without PROBE_RESULT."""
    ordered = _ordered(journals, 'c')
    prepared = any(record['type'] == 'PREPARED' for record in ledger)
    attempts = [number for number, _, _, records in ordered if any(r['type'] == 'CANDIDATES' for r in records)]
    accounted = attempts[-1] if prepared and attempts else None
    total = 0.0
    for number, _, _, records in ordered:
        epochs = _epochs(records)
        if accounted is None or number < accounted or not epochs:
            total += HEARTBEAT_S + sum(cost for cost, _, _ in epochs)
            continue
        for cost, candidates, probed in epochs:
            if candidates and number == accounted:
                continue
            total += cost + (0.0 if probed else HEARTBEAT_S)
    return total


def probe_refusal(path_cpu_s: float, total_paths: int, path_cpu_seconds) -> str | None:
    """Row B3: the in-run probe's projection, refused when it exceeds the path budget."""
    return 'PROBE_OVER_BUDGET' if path_cpu_s * total_paths > path_cpu_seconds else None


def segment_cause(ledger, journals, keys, provisional: str, reasons) -> tuple[str, str]:
    """(class, cause) for SEGMENT_END (card F8, note item 5). A STOPPED (or COMPLETE) provisional
    cause is replaced by the cap ``cap_finding`` reaches, iterated to a fixed point; a HALTED or
    TERMINAL cause is written unchanged."""
    cls = COMPLETE if provisional == COMPLETE else state.classify(provisional)[0]
    if cls not in (STOPPED, COMPLETE):
        return cls, provisional
    cap = state.cap_finding(ledger, journals, keys=keys, cause=provisional, reasons=reasons)
    if cap is None:
        return cls, provisional
    for _ in range(len(state.CAUSES)):
        again = state.cap_finding(ledger, journals, keys=keys, cause=cap, reasons=reasons)
        if again is None or again == cap:
            break
        cap = again
    return HALTED, cap


def provisional_cause(reasons, *, interrupted: bool, refused: bool, complete: bool) -> str:
    """The highest-class stop of a segment (design §4.3 precedence)."""
    best = None
    for reason in reasons:
        if reason == 'DONE':
            continue
        cls, code = state.classify(reason)
        if best is None or _PRECEDENCE[cls] > _PRECEDENCE[best[0]]:
            best = (cls, code)
    for flag, (cls, code) in ((refused, (TERMINAL, 'BUDGET_EXHAUSTED')), (interrupted, (STOPPED, 'INTERRUPTED'))):
        if flag and (best is None or _PRECEDENCE[cls] > _PRECEDENCE[best[0]]):
            best = (cls, code)
    if best is not None:
        return best[1]
    return COMPLETE if complete else 'WORKER_LOST'


class Dispatcher:
    """Row B4's gate over one segment: worker ``i`` runs its witness first (card F2), then its
    share ``sorted(K - completed)[i::W]`` (F3). Path CPU is booked from the first PATH of each
    plan key; no key is dispatched once the booked CPU reaches ``path_cpu_seconds``."""

    def __init__(self, shares, witnesses, *, booked: float, budget, completed):
        self.queues = [([tuple(witnesses[i])] if i < len(witnesses) else []) + [tuple(key) for key in share]
                       for i, share in enumerate(shares)]
        self.booked, self.budget = booked, budget
        self.completed = set(completed)
        self.segment_booked = 0.0
        self.refused = False

    def next(self, worker: int):
        """The worker's next key, or None (no key left, or the gate refused)."""
        if not self.queues[worker]:
            return None
        if self.booked >= self.budget:
            self.refused = True
            return None
        return self.queues[worker].pop(0)

    def report(self, key, cpu_s: float) -> None:
        key = tuple(key)
        if key not in self.completed:
            self.completed.add(key)
            self.booked += cpu_s
            self.segment_booked += cpu_s


def assignment(remaining, w):
    """Card F3: shares and the SHA-256 SEGMENT_START records for them."""
    shares = [remaining[i::w] for i in range(w)]
    listed = [[i, [list(key) for key in share]] for i, share in enumerate(shares)]
    return shares, _sha(canonical_json_bytes(listed))


def witnesses(completed, w, head) -> list:
    """Row S13, card F2: min(W, |completed|) completed keys, ordered by a hash of the ledger head."""
    ranked = sorted(completed, key=lambda key: (_sha(canonical_json_bytes([head, list(key)])), key))
    return ranked[:min(w, len(ranked))]


# ---- the Job Object and worker processes (row S12) ---------------------------------------------

def _win():
    """The kernel32 calls and structures for the Job Object, built per use (no module state)."""
    import ctypes  # pylint: disable=import-outside-toplevel
    from ctypes import wintypes  # pylint: disable=import-outside-toplevel

    class Basic(ctypes.Structure):  # JOBOBJECT_BASIC_LIMIT_INFORMATION
        _fields_ = [('PerProcessUserTimeLimit', ctypes.c_int64), ('PerJobUserTimeLimit', ctypes.c_int64),
                    ('LimitFlags', wintypes.DWORD), ('MinimumWorkingSetSize', ctypes.c_size_t),
                    ('MaximumWorkingSetSize', ctypes.c_size_t), ('ActiveProcessLimit', wintypes.DWORD),
                    ('Affinity', ctypes.c_size_t), ('PriorityClass', wintypes.DWORD),
                    ('SchedulingClass', wintypes.DWORD)]

    class Io(ctypes.Structure):  # IO_COUNTERS
        _fields_ = [(name, ctypes.c_uint64) for name in (
            'ReadOperationCount', 'WriteOperationCount', 'OtherOperationCount', 'ReadTransferCount',
            'WriteTransferCount', 'OtherTransferCount')]

    class Extended(ctypes.Structure):  # JOBOBJECT_EXTENDED_LIMIT_INFORMATION
        _fields_ = [('BasicLimitInformation', Basic), ('IoInfo', Io), ('ProcessMemoryLimit', ctypes.c_size_t),
                    ('JobMemoryLimit', ctypes.c_size_t), ('PeakProcessMemoryUsed', ctypes.c_size_t),
                    ('PeakJobMemoryUsed', ctypes.c_size_t)]

    class Accounting(ctypes.Structure):  # JOBOBJECT_BASIC_ACCOUNTING_INFORMATION
        _fields_ = [('TotalUserTime', ctypes.c_int64), ('TotalKernelTime', ctypes.c_int64),
                    ('ThisPeriodTotalUserTime', ctypes.c_int64), ('ThisPeriodTotalKernelTime', ctypes.c_int64),
                    ('TotalPageFaultCount', wintypes.DWORD), ('TotalProcesses', wintypes.DWORD),
                    ('ActiveProcesses', wintypes.DWORD), ('TotalTerminatedProcesses', wintypes.DWORD)]

    class Thread(ctypes.Structure):  # THREADENTRY32
        _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD), ('th32ThreadID', wintypes.DWORD),
                    ('th32OwnerProcessID', wintypes.DWORD), ('tpBasePri', wintypes.LONG),
                    ('tpDeltaPri', wintypes.LONG), ('dwFlags', wintypes.DWORD)]

    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
    kernel.SetInformationJobObject.argtypes = (wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD)
    kernel.QueryInformationJobObject.argtypes = (wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD,
                                                 ctypes.c_void_p)
    kernel.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.CreateToolhelp32Snapshot.argtypes = (wintypes.DWORD, wintypes.DWORD)
    kernel.Thread32First.argtypes = (wintypes.HANDLE, ctypes.c_void_p)
    kernel.Thread32Next.argtypes = (wintypes.HANDLE, ctypes.c_void_p)
    kernel.OpenThread.restype = wintypes.HANDLE
    kernel.OpenThread.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    kernel.ResumeThread.argtypes = (wintypes.HANDLE,)
    kernel.ResumeThread.restype = wintypes.DWORD
    return ctypes, kernel, Extended, Accounting, Thread


class Job:
    """A Job Object with ``JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`` and a non-inheritable handle; a
    worker is created suspended, assigned, then resumed (row S12)."""

    def __init__(self):
        if os.name != 'nt':
            raise ScreenRefusal('SCREEN_PLATFORM_UNSUPPORTED', 'workers run in a Windows Job Object')
        self.ctypes, self.kernel, self.extended, self.accounting_type, self.thread = _win()
        self.handle = self.kernel.CreateJobObjectW(None, None)  # NULL attributes: not inheritable
        if not self.handle:
            raise OSError(self.ctypes.get_last_error(), 'CreateJobObjectW failed')
        info = self.extended()
        info.BasicLimitInformation.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.kernel.SetInformationJobObject(self.handle, 9, self.ctypes.byref(info),
                                                   self.ctypes.sizeof(info)):
            self.close()
            raise OSError(self.ctypes.get_last_error(), 'SetInformationJobObject failed')

    def spawn(self, command, *, env, cwd):
        process = subprocess.Popen(  # pylint: disable=consider-using-with
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=cwd,
            creationflags=_CREATE_SUSPENDED | _CREATE_NEW_PROCESS_GROUP | _CREATE_NO_WINDOW)
        handle = int(process._handle)  # pylint: disable=protected-access
        if not self.kernel.AssignProcessToJobObject(self.handle, handle):
            process.kill()
            raise OSError(self.ctypes.get_last_error(), 'AssignProcessToJobObject failed')
        self._resume(process.pid)
        return process

    def _resume(self, pid):
        snapshot = self.kernel.CreateToolhelp32Snapshot(0x4, 0)  # TH32CS_SNAPTHREAD
        entry = self.thread()
        entry.dwSize = self.ctypes.sizeof(entry)
        try:
            found = self.kernel.Thread32First(snapshot, self.ctypes.byref(entry))
            while found:
                if entry.th32OwnerProcessID == pid:
                    thread = self.kernel.OpenThread(0x0002, False, entry.th32ThreadID)  # THREAD_SUSPEND_RESUME
                    if thread:
                        self.kernel.ResumeThread(thread)
                        self.kernel.CloseHandle(thread)
                found = self.kernel.Thread32Next(snapshot, self.ctypes.byref(entry))
        finally:
            self.kernel.CloseHandle(snapshot)

    def _query(self, kind, info):
        """One QueryInformationJobObject; a closed job or a FALSE return is unreadable, never a read
        of zero (Codex r4189920851; review 5423080976)."""
        if not self.handle:
            raise OSError('the job is closed; its accounting was read before closing or is charged as a crash')
        if not self.kernel.QueryInformationJobObject(self.handle, kind, self.ctypes.byref(info),
                                                     self.ctypes.sizeof(info), None):
            raise OSError(self.ctypes.get_last_error() if hasattr(self.ctypes, 'get_last_error') else 0,
                          'QueryInformationJobObject failed')
        return info

    def cpu_s(self) -> float:
        """The job's accounted CPU, exited workers included (row B1)."""
        info = self._query(1, self.accounting_type())
        return (info.TotalUserTime + info.TotalKernelTime) / 1e7

    def peak_memory(self) -> int:
        return int(self._query(9, self.extended()).PeakProcessMemoryUsed)

    def close(self):
        if self.handle:
            self.kernel.CloseHandle(self.handle)
            self.handle = None


def worker_environment() -> dict:
    """The pinned worker environment (design §5.1)."""
    keep = ('SYSTEMROOT', 'SystemRoot', 'WINDIR', 'TEMP', 'TMP', 'PATH', 'COMSPEC', 'PATHEXT', 'USERPROFILE',
            'HOME', 'TMPDIR', 'LANG')
    env = {name: os.environ[name] for name in keep if name in os.environ}
    env.update(PYTHONHASHSEED='0', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    return env


def worker_launch() -> tuple[str, dict]:
    """argv[0] and the pinned environment (card §3.3 as amended by PF-1): a Windows venv redirector
    would itself become the worker interpreter's parent, so row K4's ``os.getppid()`` check could
    never name the coordinator; the base interpreter is started instead, with
    ``__PYVENV_LAUNCHER__`` naming the redirector, so the worker's ``sys.executable``, venv and
    interpreter binding are unchanged."""
    env = worker_environment()
    base = getattr(sys, '_base_executable', sys.executable)
    if os.name == 'nt' and os.path.normcase(base) != os.path.normcase(sys.executable):
        env['__PYVENV_LAUNCHER__'] = sys.executable
        return base, env
    return sys.executable, env


class Worker:
    """One worker process and its reader threads; messages arrive on a shared queue."""

    def __init__(self, job: Job, run_dir: Path, authority_sha256: str, name: str, inbox: queue.Queue, index: int):
        self.name, self.index, self.inbox, self.run_dir = name, index, inbox, run_dir
        code_root = Path(screen_authority.REPOSITORY_ROOT).resolve()
        executable, env = worker_launch()
        command = [executable, '-I', '-S', '-B', '-c', p7_evidence.SCREEN_BOOTSTRAP, str(code_root),
                   str(run_dir), authority_sha256, name]
        self.process = job.spawn(command, env=env, cwd=str(run_dir))
        self.stderr = []
        self.io_error, self.exited, self.key = False, False, None
        threading.Thread(target=self._read, daemon=True).start()
        self.drainer = threading.Thread(target=self._drain, daemon=True)
        self.drainer.start()

    def _read(self):
        for raw in self.process.stdout:
            line = raw.decode('utf-8', errors='replace')
            if line.startswith(PROTOCOL):
                try:
                    message = json.loads(line[len(PROTOCOL):])
                except ValueError:
                    continue
                if message.get('type') == 'io_error':
                    self.io_error = True
                self.inbox.put((self.index, message))
        self.process.wait()
        self.inbox.put((self.index, None))

    def _drain(self):
        for raw in self.process.stderr:
            self.stderr.append(raw)
            del self.stderr[:-200]

    def send(self, message: dict) -> None:
        try:
            self.process.stdin.write((json.dumps(message, sort_keys=True) + '\n').encode('utf-8'))
            self.process.stdin.flush()
        except OSError:
            pass  # the worker is gone; its exit arrives on the inbox

    def reason(self) -> str:
        """Its WORKER_STOP reason, else IO_ERROR (card F4), else WORKER_LOST."""
        try:
            records = journal.read(self.run_dir / 'journal' / self.name, prev_sha256=None)
        except (OSError, ValueError):
            records = ()
        if records and records[-1]['type'] == 'WORKER_STOP':
            return records[-1]['body']['reason']
        return 'IO_ERROR' if self.io_error else 'WORKER_LOST'

    def keep_stderr(self) -> None:
        """An abnormal worker's stderr tail goes to ``errors/`` (reading it is exposure, row X2)."""
        self.drainer.join(timeout=10)
        folder = self.run_dir / 'errors'
        folder.mkdir(exist_ok=True)
        (folder / (self.name + '.stderr.txt')).write_bytes(b''.join(self.stderr))


# ---- the run ------------------------------------------------------------------------------------

@dataclass
class Stop:
    """How an invocation ended: STOPPED, HALTED, TERMINAL or COMPLETE, and its code."""
    kind: str
    code: str | None = None


class _Run:  # pylint: disable=too-many-instance-attributes
    """One coordinator invocation over one run directory, holding its run lock."""

    def __init__(self, inputs: Inputs, receipt, auth, ledger: Ledger, lock: _Lock, workers: int | None, now):
        self.inputs, self.receipt, self.auth, self.ledger, self.lock = inputs, receipt, auth, ledger, lock
        self.run_dir = inputs.run_dir
        self.requested_workers = workers
        self.params = json.loads(canonical_json_bytes(screen_authority._thaw(auth.parameters)))  # pylint: disable=protected-access
        self.keys = plan_keys(self.params)
        self.now = now
        self.candidate = None   # the live candidate worker, kept for the probe (design §5.2)
        self.job = None

    @property
    def approvals(self) -> list:
        return [self.receipt.approval.approval_sha256, self.auth.approval.approval_sha256]

    def time(self):
        return _now(self.now)

    def journals(self) -> dict:
        return read_journals(self.run_dir)  # a broken chain raises journal.JournalCorrupt

    def check(self):
        return state.check_record(self.ledger.records, self.journals(), read_manifest(self.run_dir),
                                  read_acts(self.run_dir), keys=self.keys,
                                  trusted_keys=trusted_keys(self.inputs.public_keys), now=self.time())

    def _start(self, name, inbox, index=0):
        self.run_dir.joinpath('journal').mkdir(exist_ok=True)
        if self.job is None:
            self.job = Job()
        return Worker(self.job, self.run_dir, self.auth.authority_sha256, name, inbox, index)

    def _end_job(self):
        if self.job is not None:
            self.job.close()
            self.job = None
        self.candidate = None

    # ---- the drive loop ---------------------------------------------------------------------

    def drive(self) -> Stop:
        try:
            while True:
                name = self.ledger.state.name
                step = {'BOUND': self.bound, 'PREPARED': self.prepared, 'PROBING': self.probing,
                        'IDLE': self.idle, 'RUNNING': self.crashed}.get(name)
                if step is None:
                    return self.final_stop()
                try:
                    stop = step()
                except journal.JournalCorrupt:  # a journal broken mid-file (row S3)
                    if self.ledger.state.name == 'RUNNING':
                        raise
                    stop = self.terminal(journal.CORRUPTION)
                if stop is not None:
                    return stop
        finally:
            self._end_job()

    def final_stop(self) -> Stop:
        current = self.ledger.state
        if current.name == 'HALTED':
            return Stop(HALTED, _last_halt(self.ledger.records))
        codes = terminal_codes(self.ledger.records)
        if codes:
            return Stop(TERMINAL, codes[-1])
        return Stop(COMPLETE)

    def halt(self, code: str) -> Stop:
        self.ledger.append('HALT', {'code': code, 'from': self.ledger.state.name})
        return Stop(HALTED, code)

    def terminal(self, code: str) -> Stop:
        self.ledger.append('TERMINAL', {'code': code})
        return Stop(TERMINAL, code)

    def lifecycle_stop(self) -> Stop | None:
        """Row K2 before PROBE_START or a segment: a lapse writes nothing; a key-lifecycle event is
        TERMINAL."""
        found = _check_lifecycles(self.receipt, self.auth, self.time())
        if found is None:
            return None
        if state.classify(found)[0] == TERMINAL:
            return self.terminal(state.classify(found)[1])
        return Stop(STOPPED, state.classify(found)[1])

    # ---- BOUND: the candidate pass (design §5.2, row R2) ------------------------------------

    def _unanswered_candidate_crash(self) -> bool:
        """A candidate journal that did not end in a lapse and has no HALT from BOUND answering it."""
        attempts = 0
        for _, _, _, records in _ordered(self.journals(), 'c'):
            last = records[-1] if records else None
            lapse = (last is not None and last['type'] == 'WORKER_STOP'
                     and state.classify(last['body']['reason'])[1] == _LAPSE)
            attempts += 0 if lapse else 1
        answered = sum(1 for r in self.ledger.records if r['type'] == 'HALT' and r['body']['from'] == 'BOUND')
        return attempts > answered

    def bound(self) -> Stop | None:
        if self._unanswered_candidate_crash():  # W0: a crash in BOUND HALTs; CONTINUE repeats the pass
            return self.halt(state.UNCLASSIFIED_ERROR)
        found = _check_lifecycles(self.receipt, self.auth, self.time())
        if found is not None:
            return self.terminal(found) if state.classify(found)[0] == TERMINAL else Stop(STOPPED, found)
        inbox = queue.Queue()
        number = len(_ordered(self.journals(), 'c')) + 1
        worker = self._start(f'c{number}-w0.jsonl', inbox)
        worker.send({'type': 'init', 'role': 'candidate', 'inputs': self.inputs.message()})
        reply = self._await(worker, inbox, 'candidates')
        if reply is None:
            return self._candidate_failed(worker)
        if not reply['closure_match']:
            worker.send({'cmd': 'stop', 'reason': 'DONE'})
            return self.terminal('CODE_OR_ARTIFACT_DRIFT')
        manifest = {'authority_sha256': self.auth.authority_sha256,
                    'contract_sha256': self.receipt.contract_sha256,
                    'p7_record_sha256': self.auth.p7['record_sha256'], 'code_head': self.auth.code_head,
                    'populations': reply['populations'], 'plan_sha256': plan.plan_sha256(self.keys)}
        raw = canonical_json_bytes(manifest)
        _write_atomic(self.run_dir / 'manifest.json', raw)
        self.ledger.append('PREPARED', {'manifest_sha256': _sha(raw), 'build': _cost(reply['build']),
                                        'integrity': _cost(reply['integrity'])})
        self.candidate = (worker, inbox)
        return None

    def _candidate_failed(self, worker) -> Stop:
        """A candidate worker that ended without its candidates: TERMINAL, a lapse (nothing
        written) or HALT from BOUND (design §4.2 last paragraph)."""
        worker.process.wait()
        reason = worker.reason()
        if reason not in ('DONE',):
            worker.keep_stderr()
        cls, code = state.classify(reason)
        if cls == TERMINAL:
            return self.terminal(code)
        if code == _LAPSE:
            return Stop(STOPPED, code)
        return self.halt(code if cls == HALTED else state.UNCLASSIFIED_ERROR)

    @staticmethod
    def _await(worker, inbox, kind):
        """The worker's next ``kind`` message, or None once it has exited."""
        while True:
            _, message = inbox.get()
            if message is None:
                worker.exited = True
                return None
            if message.get('type') == kind:
                return message

    # ---- PREPARED and PROBING: the probe (rows B2, B3) --------------------------------------

    def prepared(self) -> Stop | None:
        stop = self.lifecycle_stop()
        if stop is not None:
            if self.candidate is not None:
                self.candidate[0].send({'cmd': 'stop', 'reason': 'DONE'})
            return stop
        manifest_sha256 = next(r['body']['manifest_sha256'] for r in reversed(self.ledger.records)
                               if r['type'] == 'PREPARED')
        self.ledger.append('PROBE_START', {})
        if self.candidate is not None:
            worker, inbox = self.candidate
            worker.send({'cmd': 'probe', 'manifest_sha256': manifest_sha256})
        else:  # W1: resume from PREPARED times the probe in a fresh candidate-numbered worker
            inbox = queue.Queue()
            number = len(_ordered(self.journals(), 'c')) + 1
            worker = self._start(f'c{number}-w0.jsonl', inbox)
            worker.send({'type': 'init', 'role': 'probe', 'inputs': self.inputs.message(),
                         'manifest_sha256': manifest_sha256})
        reply = self._await(worker, inbox, 'probe')
        self.candidate = None
        if reply is None:
            worker.process.wait()
            worker.keep_stderr()
            cls, code = state.classify(worker.reason())
            return self.terminal(code) if cls == TERMINAL else self.halt('PROBE_INTERRUPTED')
        worker.process.wait()
        if not reply['closure_match']:
            return self.terminal('CODE_OR_ARTIFACT_DRIFT')
        if not reply['complete']:
            return self.terminal('PROBE_INCOMPLETE')
        refused = probe_refusal(reply['path_cpu_s'], len(self.keys), self.params['budget']['path_cpu_seconds'])
        if refused is not None:
            return self.terminal(refused)
        self.ledger.append('PROBE', {'path_cpu_s': reply['path_cpu_s'], 'path_wall_s': reply['path_wall_s'],
                                     'peak_memory_bytes': reply['peak_memory_bytes']})
        return None

    def probing(self) -> Stop:
        """W21: PROBE_START without PROBE HALTs; the probe is re-timed only after CONTINUE (row B2)."""
        return self.halt('PROBE_INTERRUPTED')

    # ---- RUNNING found at resume: SEGMENT_CRASHED (W22, card F1) -----------------------------

    def crashed(self) -> None:
        """The losses are ``state``'s in-flight rule (row S10); a structure ``check_record`` would
        refuse is recorded with no losses and no cap and found as CORRUPTION at IDLE."""
        start = next(r['body'] for r in reversed(self.ledger.records) if r['type'] == 'SEGMENT_START')
        try:
            journals = self.journals()
            lost = state._segment_keys(_segment_journals(journals, start['k']))[0]  # pylint: disable=protected-access
            cap = state.cap_finding(self.ledger.records, journals, keys=self.keys, cause=None)
            charge = crash_charge(self.ledger.records, journals, k=start['k'], w=start['w'])
        except Exception:  # pylint: disable=broad-exception-caught  # state._Failed or JournalCorrupt
            lost, cap = (), None
            charge = {'cpu_s': float(HEARTBEAT_S * start['w']), 'wall_s': float(HEARTBEAT_S)}
        self.ledger.append('SEGMENT_CRASHED', {'k': start['k'], 'charge': charge,
                                               'losses': [list(key) for key in sorted(lost)], 'cap': cap})

    # ---- IDLE: checks, then one segment -----------------------------------------------------

    def idle(self) -> Stop | None:
        found = self.check()
        if found.code is not None:
            if state.classify(found.code)[0] == TERMINAL:
                return self.terminal(found.code)
            return self.halt(found.code)  # a reached cap, unwritten (card F8, note item 5)
        remaining = sorted(set(self.keys) - found.completed)
        if not remaining:
            self.ledger.append('ALL_DONE', {})
            return Stop(COMPLETE)
        journals = self.journals()
        if overhead_used(self.ledger.records, journals) >= self.params['budget']['overhead_cpu_seconds']:
            return self.halt('OVERHEAD_EXHAUSTED')
        booked = booked_path_cpu(journals, self.keys)
        if booked >= self.params['budget']['path_cpu_seconds']:
            return self.terminal('BUDGET_EXHAUSTED')
        stop = self.lifecycle_stop()
        if stop is not None:
            return stop
        return self.segment(remaining, found.completed, booked)

    def reexecute(self, n, chosen):
        """One ``verify`` worker re-executes ``chosen`` inside the gate of rows K3-K4; its PATH rows
        must equal the segment journals' first rows byte for byte (row X4). None after a lapse."""
        inbox = queue.Queue()
        manifest_sha256 = next(r['body']['manifest_sha256'] for r in reversed(self.ledger.records)
                               if r['type'] == 'PREPARED')
        try:
            worker = self._start(f'v{n}-w0.jsonl', inbox)
            worker.send({'type': 'init', 'role': 'verify', 'inputs': self.inputs.message(),
                         'manifest_sha256': manifest_sha256})
            pending = list(chosen)
            while True:
                _, message = inbox.get()
                if message is None:
                    break
                if message.get('type') in ('ready', 'done'):
                    worker.send({'cmd': 'key', 'key': list(pending.pop(0))} if pending else
                                {'cmd': 'stop', 'reason': 'DONE'})
            worker.process.wait()
            reason = worker.reason()
        finally:
            self._end_job()
        if state.classify(reason)[1] == _LAPSE:
            return None
        if reason != 'DONE':
            return False
        journals = self.journals()
        original = {tuple(o['key']): canonical_json_bytes(dict(o)) for o in journal.outcomes(journals, chosen)}
        again = {}
        for record in journals.get(f'v{n}-w0.jsonl', ()):
            if record['type'] == 'PATH':
                body = {name: value for name, value in record['body'].items() if name not in ('wall_s', 'cpu_s')}
                again.setdefault(tuple(body['key']), canonical_json_bytes(body))
        return set(again) == {tuple(key) for key in chosen} and all(again[key] == original.get(key) for key in again)

    def worker_count(self, remaining) -> int:
        if self.requested_workers is not None:
            wanted = self.requested_workers
        else:
            peak = next((r['body']['peak_memory_bytes'] for r in reversed(self.ledger.records)
                         if r['type'] == 'PROBE'), 0)
            wanted = min(8, math.floor(0.8 * _ram_bytes() / peak)) if peak else 1
        return max(1, min(wanted, len(remaining)))

    def segment(self, remaining, completed, booked) -> Stop:  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
        """Design §5.3 over one segment: SEGMENT_START (heartbeat 0) is durable before any worker
        starts (row S11); SEGMENT_END by the highest class (§4.3; card F8)."""
        w = self.worker_count(remaining)
        shares, digest = assignment(remaining, w)
        chosen = witnesses(completed, w, self.ledger.head)
        k = 1 + sum(1 for r in self.ledger.records if r['type'] == 'SEGMENT_START')
        manifest_sha256 = next(r['body']['manifest_sha256'] for r in reversed(self.ledger.records)
                               if r['type'] == 'PREPARED')
        self.ledger.append('SEGMENT_START', {'k': k, 'w': w, 'assignment_sha256': digest,
                                             'witness_keys': [list(key) for key in chosen],
                                             'approvals': self.approvals})
        started = time.perf_counter()
        beat = started + HEARTBEAT_S
        dispatcher = Dispatcher(shares, chosen, booked=booked, budget=self.params['budget']['path_cpu_seconds'],
                                completed=completed)
        inbox = queue.Queue()
        workers, alive, stopping, interrupted = [], set(), False, False
        self._end_job()
        self.job = Job()
        try:
            for i in range(w):
                workers.append(self._start(f's{k}-w{i}.jsonl', inbox, i))
                workers[-1].send({'type': 'init', 'role': 'segment', 'inputs': self.inputs.message(),
                                  'manifest_sha256': manifest_sha256})
                alive.add(i)
        except OSError:
            stopping = True

        def dispatch(i):
            key = None if stopping else dispatcher.next(i)
            workers[i].key = key
            workers[i].send({'cmd': 'stop', 'reason': 'INTERRUPTED' if interrupted else 'DONE'} if key is None
                            else {'cmd': 'key', 'key': list(key)})

        last_cpu, closed = 0.0, None  # heartbeat 0 is SEGMENT_START (row S11)

        def heartbeat():
            # Checked on every iteration, whatever the inbox holds (Codex r4189920841).
            nonlocal beat, last_cpu
            now = time.perf_counter()
            if now < beat:
                return
            cpu = _read_job(self.job)[0]
            last_cpu = last_cpu if cpu is None else max(last_cpu, cpu)
            self.ledger.append('HEARTBEAT', {'wall_s': now - started, 'job_cpu_s': last_cpu})
            beat += HEARTBEAT_S
            if beat <= now:  # fell behind: the next one an interval from now
                beat = now + HEARTBEAT_S

        while alive:
            try:
                heartbeat()
                try:
                    i, message = inbox.get(timeout=max(0.01, beat - time.perf_counter()))
                except queue.Empty:
                    continue
                if message is None:
                    alive.discard(i)
                    workers[i].exited = True
                    if workers[i].reason() != 'DONE':
                        workers[i].keep_stderr()
                        if not stopping:
                            stopping = True
                            for j in alive:
                                if workers[j].key is None:
                                    dispatch(j)
                elif message.get('type') == 'ready':
                    dispatch(i)
                elif message.get('type') == 'done':
                    dispatcher.report(message['key'], message['cpu_s'])
                    dispatch(i)
            except KeyboardInterrupt:  # run directly: SEGMENT_END INTERRUPTED (design §4.3 Ctrl-C)
                if interrupted:  # a second Ctrl-C: read the job's CPU, then close it (Codex r4189920851)
                    closed = _read_job(self.job)
                    self.job.close()
                    break
                interrupted = stopping = True
                for j in alive:
                    if workers[j].key is None:
                        dispatch(j)
        for worker in workers:
            worker.process.wait()
        journals = self.journals()
        reasons = [worker.reason() for worker in workers]
        complete = set(self.keys) <= dispatcher.completed | set(completed)
        provisional = provisional_cause(reasons, interrupted=interrupted,
                                        refused=dispatcher.refused and not complete, complete=complete)
        cls, cause = segment_cause(self.ledger.records, journals, self.keys, provisional,
                                   [reason for reason in reasons if reason != 'DONE'])
        job_cpu, peak = closed if closed is not None else _read_job(self.job)
        segment_booked = _segment_booked(journals, k, _keys_before(journals, k))
        if job_cpu is None:  # unreadable: the crash charge, as overhead, never 0 (design §5.4)
            overhead = last_cpu + HEARTBEAT_S * w
            job_cpu = overhead + segment_booked
        else:
            overhead = max(0.0, job_cpu - segment_booked)
        self.ledger.append('SEGMENT_END', {
            'class': cls, 'cause': cause,
            'workers': [{'worker': worker.name, 'reason': reason} for worker, reason in zip(workers, reasons)],
            'wall_s': time.perf_counter() - started, 'job_cpu_s': job_cpu, 'path_cpu_s': segment_booked,
            'overhead_cpu_s': overhead, 'peak_memory_bytes': peak})
        return Stop(cls, None if cls == COMPLETE else cause)


def _read_job(job) -> tuple:
    """(CPU seconds or None when unreadable, peak process memory or 0 when unreadable) of a
    segment's job; each query is read on its own."""
    try:
        cpu = job.cpu_s()
    except OSError:
        cpu = None
    try:
        peak = job.peak_memory()
    except OSError:
        peak = 0
    return cpu, peak


def _cost(value) -> dict:
    return {'cpu_s': float(value['cpu_s']), 'wall_s': float(value['wall_s'])}


def _ram_bytes() -> int:
    if os.name != 'nt':
        return os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    import ctypes  # pylint: disable=import-outside-toplevel

    class Status(ctypes.Structure):  # MEMORYSTATUSEX
        _fields_ = [('dwLength', ctypes.c_uint32), ('dwMemoryLoad', ctypes.c_uint32),
                    ('ullTotalPhys', ctypes.c_uint64), ('ullAvailPhys', ctypes.c_uint64),
                    ('ullTotalPageFile', ctypes.c_uint64), ('ullAvailPageFile', ctypes.c_uint64),
                    ('ullTotalVirtual', ctypes.c_uint64), ('ullAvailVirtual', ctypes.c_uint64),
                    ('ullAvailExtendedVirtual', ctypes.c_uint64)]
    status = Status()
    status.dwLength = ctypes.sizeof(status)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
    return int(status.ullTotalPhys)


# ---- acts (rows X2, X3; design §4.5) ------------------------------------------------------------

def _act_files(run_dir: Path, ledger) -> list:
    """Unrecorded act files: (act_sha256, act document, act bytes, approval bytes)."""
    recorded = {r['body']['act_sha256'] for r in ledger if r['type'] == 'ACT'}
    pending = []
    for name, raw in read_acts(run_dir).items():
        sha = name[:-len('.json')] if name.endswith('.json') else name
        if sha in recorded:
            continue
        try:
            container = parse_canonical_json(raw, label='act file')
            act_bytes = base64.b64decode(container['act_b64'], validate=True)
            approval = base64.b64decode(container['approval_b64'], validate=True)
            doc = parse_canonical_json(act_bytes, label='act')
        except (ContractValidationError, KeyError, TypeError, ValueError) as exc:
            raise ScreenRefusal('SCREEN_ACT_PENDING', f'{name} is unreadable') from exc
        pending.append((sha, doc, act_bytes, approval))
    return pending


def record_pending_acts(ledger: Ledger, inputs: Inputs, now) -> None:
    """``act`` and ``resume`` first append the ACT of any unrecorded act file whose ledger head is
    current; any other unrecorded act file refuses (row S8)."""
    for sha, doc, act_bytes, approval in _act_files(ledger.folder.parent, ledger.records):
        if doc.get('ledger_head_sha256') != ledger.head:
            raise ScreenRefusal('SCREEN_ACT_PENDING', f'act {sha} has no ledger record')
        try:
            valid = screen_authority.validate_screen_act(act_bytes, approval, dict(inputs.public_keys),
                                                         authority=inputs.authority, ledger_head=ledger.head, now=now)
            ledger.append('ACT', {'act_sha256': valid.act_sha256, 'act': valid.act})
        except (ContractValidationError, state.IllegalTransition) as exc:
            raise ScreenRefusal('SCREEN_ACT_PENDING', str(exc)) from exc


def _bound_authority(ledger, inputs: Inputs) -> None:
    if not ledger or ledger[0]['body']['authority_sha256'] != inputs.authority_sha256:
        raise ScreenRefusal('SCREEN_RUN_UNBOUND', 'no AUTHORITY_BOUND for this authority')


# ---- subcommands --------------------------------------------------------------------------------

def preflight(inputs: Inputs, *, now=None) -> str:
    """Launch checks only; no state (design §5.6)."""
    try:
        _, auth = launch_checks(inputs, _now(now))
    except (ContractValidationError, ValueError, OSError) as exc:
        raise ScreenRefusal(refusal_code(exc, 'LAUNCH_CHECK_FAILED'), str(exc)) from exc
    return auth.authority_sha256


def accept_p7(*, p7_record: bytes, artifact_root: Path, public_keys, now=None) -> str:
    """``accept_p7_record`` at the code root, then ``<private root>/p7_acceptance.json`` (design §3.2)."""
    code_root = Path(screen_authority.REPOSITORY_ROOT)
    try:
        p7_evidence.accept_p7_record(p7_record, code_root=code_root, artifact_root=artifact_root,
                                     now=_now(now), public_keys=dict(public_keys))
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        raise ScreenRefusal(refusal_code(exc, 'P7_RECORD_NOT_REPRODUCED'), str(exc)) from exc
    _, head = screen_authority._git('rev-parse', '--verify', 'HEAD^{commit}')  # pylint: disable=protected-access
    raw = canonical_json_bytes({'schema': ACCEPTANCE_SCHEMA, 'record_sha256': _sha(p7_record),
                                'accepted_at': _now(now).isoformat(), 'code_head': head.decode('ascii').strip(),
                                'exit_status': 0})
    try:
        _write_once(Path(artifact_root) / 'p7_acceptance.json', raw)
    except FileExistsError:
        raise ScreenRefusal('P7_ACCEPTANCE_EXISTS', 'p7_acceptance.json is written once') from None
    return _sha(raw)


def _launch_or_refuse(inputs, now, code=None):
    if lapsed(inputs, now):
        raise ScreenRefusal(_LAPSE, 'an approval window does not contain now')
    try:
        return launch_checks(inputs, now)
    except (ContractValidationError, ValueError, OSError) as exc:
        raise ScreenRefusal(code or refusal_code(exc, 'LAUNCH_CHECK_FAILED'), str(exc)) from exc


def _scan_attempts(run_root: Path, auth) -> None:
    """Rows S6, S4, S5 under the run-root lock, in that order."""
    own = run_root / auth.authority_sha256
    for path in sorted(run_root.iterdir()):
        if not path.is_dir() or re.fullmatch(r'[0-9a-f]{64}', path.name) is None:
            continue
        try:
            ledger = read_ledger(path)
            current = state.fold(ledger).name
        except (OSError, ValueError):
            ledger, current = None, None
        bound = bool(ledger) and ledger[0]['type'] == 'AUTHORITY_BOUND'
        if path == own:
            if bound:
                raise ScreenRefusal('SCREEN_ALREADY_RUN', 'this authority already has a run directory')
            continue
        if bound and ledger[0]['body']['prereg_path'] == auth.prereg['path']:
            raise ScreenRefusal('PREREG_CONSUMED', 'an AUTHORITY_BOUND already names this pre-registration')
        if (ledger is None or bound) and current != 'FINAL':
            raise ScreenRefusal('SCREEN_ATTEMPT_OPEN', f'attempt {path.name} is open')


def _bind(inputs: Inputs, auth, receipt) -> tuple[Ledger, _Lock]:
    """Create (O_EXCL) or reuse the run directory under the run-root lock and write AUTHORITY_BOUND."""
    run_root = Path(auth.run_root)
    run_root.mkdir(parents=True, exist_ok=True)
    root_lock = _Lock(run_root / 'lock')
    try:
        _scan_attempts(run_root, auth)
        run_dir = run_root / auth.authority_sha256
        try:
            os.mkdir(run_dir)
            reused = False
        except FileExistsError:
            reused = True
        for sub in ('ledger', 'journal', 'acts', 'errors'):
            (run_dir / sub).mkdir(exist_ok=True)
        lock = _Lock(run_dir / 'lock')
        try:
            first = run_dir / 'ledger' / '0001.jsonl'
            if reused and first.exists():  # no durable record in it (row S6): a torn or empty write
                os.truncate(first, 0)
            ledger = Ledger(run_dir, number=1)
            ledger.append('AUTHORITY_BOUND', {
                'authority_sha256': auth.authority_sha256, 'prereg_path': auth.prereg['path'],
                'approvals': [receipt.approval.approval_sha256, auth.approval.approval_sha256],
                'reused_directory': reused})
        except BaseException:
            lock.release()
            raise
        return ledger, lock
    finally:
        root_lock.release()


def run(inputs: Inputs, *, workers: int | None = None, on_launch=None, now=None) -> Stop:
    """``run``: launch checks, the binding of rows S4-S6, then the drive loop."""
    receipt, auth = _launch_or_refuse(inputs, _now(now))
    ledger, lock = _bind(inputs, auth, receipt)
    try:
        if on_launch is not None:
            on_launch(auth.authority_sha256)
        return _Run(inputs, receipt, auth, ledger, lock, workers, now).drive()
    finally:
        ledger.close()
        lock.release()


def _open_run(inputs: Inputs):
    run_dir = inputs.run_dir
    if not (run_dir / 'ledger').is_dir():
        raise ScreenRefusal('SCREEN_RUN_UNBOUND', 'no run directory for this authority')
    _probe_lock(run_dir.parent / 'lock')
    lock = _Lock(run_dir / 'lock')
    try:
        ledger = Ledger(run_dir)
    except (OSError, ValueError) as exc:
        lock.release()
        raise ScreenRefusal(journal.CORRUPTION, str(exc)) from exc
    return ledger, lock


def resume(inputs: Inputs, *, workers: int | None = None, on_launch=None, now=None) -> Stop:
    """``resume``: locks (row S8), launch checks without state change (row S7), pending acts, then
    the drive loop from the folded state."""
    ledger, lock = _open_run(inputs)
    try:
        _bound_authority(ledger.records, inputs)
        current = _now(now)
        receipt, auth = _launch_or_refuse(inputs, current, 'RESUME_LAUNCH_CHECK')
        record_pending_acts(ledger, inputs, current)
        if ledger.state.name == 'HALTED':
            raise ScreenRefusal('SCREEN_HALTED', 'resume from HALTED needs a CONTINUE act')
        if on_launch is not None:
            on_launch(auth.authority_sha256)
        return _Run(inputs, receipt, auth, ledger, lock, workers, now).drive()
    finally:
        ledger.close()
        lock.release()


def act(inputs: Inputs, act_bytes: bytes, act_approval: bytes, *, now=None) -> tuple[str, str]:
    """``act``: Joshua's signed act, written O_EXCL and fsync'd before its ACT record (row X3)."""
    ledger, lock = _open_run(inputs)
    try:
        _bound_authority(ledger.records, inputs)
        current = _now(now)
        record_pending_acts(ledger, inputs, current)
        try:
            valid = screen_authority.validate_screen_act(act_bytes, act_approval, dict(inputs.public_keys),
                                                         authority=inputs.authority, ledger_head=ledger.head,
                                                         now=current)
        except ContractValidationError as exc:
            raise ScreenRefusal(refusal_code(exc, 'SCREEN_ACT_FIELDS'), str(exc)) from exc
        body = {'act_sha256': valid.act_sha256, 'act': valid.act}
        try:
            state.advance(ledger.state, {'body': body, 'prev_sha256': ledger.head, 'type': 'ACT'})
        except state.IllegalTransition as exc:
            raise ScreenRefusal(state.ILLEGAL_TRANSITION, str(exc)) from exc
        container = canonical_json_bytes({'act_b64': base64.b64encode(act_bytes).decode('ascii'),
                                          'approval_b64': base64.b64encode(act_approval).decode('ascii')})
        (inputs.run_dir / 'acts').mkdir(exist_ok=True)
        _write_once(inputs.run_dir / 'acts' / f'{valid.act_sha256}.json', container)
        ledger.append('ACT', body)
        return valid.act, valid.act_sha256
    finally:
        ledger.close()
        lock.release()


# ---- finalize and verify (rows S15, S16, X4, X5; design §5.5-§5.6) ------------------------------

def _named_journals(ledger, names) -> bool:
    """Card note item 12: every journal file is one the ledger names (segment and verify journals by
    their SEGMENT_START and VERIFY_START, candidate journals c1-w0, c2-w0, ... without a gap)."""
    allowed = set()
    for record in ledger:
        if record['type'] == 'SEGMENT_START':
            allowed.update(f"s{record['body']['k']}-w{i}.jsonl" for i in range(record['body']['w']))
        elif record['type'] == 'VERIFY_START':
            allowed.add(f"v{record['body']['n']}-w0.jsonl")
    candidates = sorted(journal.journal_name(name)[1] for name in names
                        if journal.journal_name(name) is not None and journal.journal_name(name)[0] == 'c')
    allowed.update(f'c{n}-w0.jsonl' for n in range(1, len(candidates) + 1))
    return set(names) <= allowed


def _report(results_raw: bytes) -> bytes:
    """REPORT.md, rendered from ``results.json`` only by a fixed template (design §4.1)."""
    doc = json.loads(results_raw)
    found = doc['verdict']
    label = 'INSUFFICIENT' if found['kind'] == 'INSUFFICIENT' else found['label']
    return ('# T00 step-3 screen report\n\n'
            f'- results.json SHA-256: `{_sha(results_raw)}`\n'
            f'- Verdict: `{label}`\n\n'
            'Rendered from results.json only.\n\n```json\n'
            + json.dumps(doc, sort_keys=True, indent=2) + '\n```\n').encode('utf-8')


def verdict_label(results_raw: bytes) -> str:
    found = json.loads(results_raw)['verdict']
    return 'INSUFFICIENT' if found['kind'] == 'INSUFFICIENT' else found['label']


def _attestation(inputs: Inputs, ledger, journals, results_sha, report_sha, params) -> bytes:  # pylint: disable=too-many-arguments
    """The run's attestation (design §4.1); ``verify`` journals, written after FINAL, are not in it."""
    journals = {name: records for name, records in journals.items() if not name.startswith('v')}
    approvals, acts, segments, closures = set(), [], [], []
    for record in ledger:
        kind, body = record['type'], record['body']
        if kind in ('AUTHORITY_BOUND', 'SEGMENT_START'):
            approvals.update(body['approvals'])
        elif kind == 'ACT':
            acts.append(body['act_sha256'])
        elif kind in ('SEGMENT_END', 'SEGMENT_CRASHED'):
            segments.append({'type': kind, 'k': body.get('k'), 'class': body.get('class'),
                             'cause': body.get('cause'), 'cap': body.get('cap')})
    for name, records in sorted(journals.items()):
        closures.extend({'journal': name, 'closure_sha256': _sha(canonical_json_bytes(r['body']['closure'])),
                         'closure_match': r['body']['closure_match']}
                        for r in records if r['type'] == 'EPOCH_CLOSE')
    acceptance = Path(inputs.artifact_root) / 'p7_acceptance.json'
    keys = plan_keys(params)
    booked = booked_path_cpu(journals, keys)
    return canonical_json_bytes({
        'schema': ATTESTATION_SCHEMA, 'authority_sha256': inputs.authority_sha256,
        'results_sha256': results_sha, 'report_sha256': report_sha, 'ledger_head_sha256': _head(ledger),
        'journal_heads': {name: _head(records) for name, records in sorted(journals.items())},
        'approvals': sorted(approvals), 'acts': acts, 'segments': segments, 'epoch_closures': closures,
        'p7_acceptance_sha256': _sha(acceptance.read_bytes()) if acceptance.is_file() else None,
        'path_budget': {'booked_cpu_s': booked, 'path_cpu_seconds': params['budget']['path_cpu_seconds'],
                        'overrun_cpu_s': max(0.0, booked - params['budget']['path_cpu_seconds'])}})


def _results(inputs: Inputs, doc, ledger, journals, keys) -> bytes:
    params = doc['parameters']
    reasons = sorted(set(terminal_codes(ledger)))
    found = verdict.evaluate(journal.outcomes(journals, keys), params, reasons)
    return journal.results(authority_sha256=inputs.authority_sha256,
                           contract_sha256=doc['source']['contract_sha256'],
                           p7_record_sha256=doc['p7']['record_sha256'], plan_sha256=plan.plan_sha256(keys),
                           verdict=verdict.as_json(found))


def finalize(inputs: Inputs, *, now=None) -> tuple[str, str]:  # pylint: disable=too-many-locals
    """``finalize`` under the run lock, from COMPLETE or TERMINAL only (row S15): ``check_record``,
    a TERMINAL failure appended before AGGREGATED, then results, report and attestation (W6, W7)."""
    ledger, lock = _open_run(inputs)
    try:
        _bound_authority(ledger.records, inputs)
        doc = _document(inputs)
        if ledger.state.name not in ('COMPLETE', 'TERMINAL', 'AGGREGATED', 'REPORTED', 'FINAL'):
            raise ScreenRefusal('FINALIZE_NOT_COMPLETE', f'the run is {ledger.state.name}')
        run_dir, keys = inputs.run_dir, plan_keys(doc['parameters'])
        journals, code = _record_code(inputs, ledger.records, keys, _now(now))
        fresh = ledger.state.name in ('COMPLETE', 'TERMINAL')
        failed = code is not None and state.classify(code)[0] == TERMINAL and code not in terminal_codes(ledger.records)
        if failed and not fresh:  # the record changed after aggregation
            raise ScreenRefusal(code, 'the run record fails check_record after aggregation')
        if failed:  # a HALTED cap code on a TERMINAL run is informational (note item 5)
            ledger.append('TERMINAL', {'code': code})
        results_raw = _results(inputs, doc, ledger.records, journals, keys)
        if fresh:
            _write_atomic(run_dir / 'results.json', results_raw)
            ledger.append('AGGREGATED', {'results_sha256': _sha(results_raw)})
        recorded = next(r['body']['results_sha256'] for r in ledger.records if r['type'] == 'AGGREGATED')
        if _sha(results_raw) != recorded:
            raise ScreenRefusal(journal.CORRUPTION, 'the run record no longer reproduces AGGREGATED')
        _write_atomic(run_dir / 'results.json', results_raw)  # W6: byte-identical rewrite
        report = _report(results_raw)
        _write_atomic(run_dir / 'REPORT.md', report)
        if ledger.state.name == 'AGGREGATED':
            ledger.append('REPORTED', {'report_sha256': _sha(report)})
        upto = ledger.records if ledger.state.name == 'REPORTED' else ledger.records[:_index(ledger.records, 'FINAL')]
        attestation = _attestation(inputs, upto, journals, recorded, _sha(report), doc['parameters'])
        _write_atomic(run_dir / 'attestation.json', attestation)
        if ledger.state.name == 'REPORTED':  # W7: re-verified digests, then FINAL
            ledger.append('FINAL', {'attestation_sha256': _sha(attestation)})
        final = next(r['body']['attestation_sha256'] for r in ledger.records if r['type'] == 'FINAL')
        reported = next(r['body']['report_sha256'] for r in ledger.records if r['type'] == 'REPORTED')
        if (final, reported) != (_sha(attestation), _sha(report)):
            raise ScreenRefusal(journal.CORRUPTION, 'the report or attestation no longer reproduces its digest')
        return verdict_label(results_raw), recorded
    finally:
        ledger.close()
        lock.release()


def _index(records, kind) -> int:
    return next(i for i, record in enumerate(records) if record['type'] == kind)


def _record_code(inputs: Inputs, ledger, keys, now):
    """(journals, the first failure): an unreadable journal or one the ledger does not name is
    CORRUPTION (row S3, note item 12); otherwise ``check_record``'s code."""
    try:
        journals = read_journals(inputs.run_dir)
    except (OSError, ValueError):
        return {}, journal.CORRUPTION
    if not _named_journals(ledger, journals):
        return journals, journal.CORRUPTION
    found = state.check_record(ledger, journals, read_manifest(inputs.run_dir), read_acts(inputs.run_dir), keys=keys,
                               trusted_keys=trusted_keys(inputs.public_keys), now=now)
    return journals, found.code


def label_check(results_doc_outcomes, params, reasons) -> str:
    """Row X5: the label recomputed by ``scripts/t00_screen_label_check.py`` in its own process."""
    script = Path(screen_authority.REPOSITORY_ROOT) / 'scripts' / 't00_screen_label_check.py'
    payload = canonical_json_bytes({'outcomes': list(results_doc_outcomes), 'parameters': params,
                                    'reasons': list(reasons)})
    done = subprocess.run([sys.executable, '-I', '-B', str(script)], input=payload, capture_output=True,
                          check=False, timeout=600)
    return done.stdout.decode('utf-8').strip() if done.returncode == 0 else 'LABEL_CHECK_FAILED'


def verify_keys(results_raw: bytes, keys, completed) -> list:
    """Row X4: k = 9 hash-derived keys, one per root x population, from ``sha256(results.json)``."""
    chosen = []
    by_group = {}
    for key in sorted(completed):
        by_group.setdefault((key[0], key[1]), []).append(key)
    seed = _sha(results_raw)
    for group in sorted({(key[0], key[1]) for key in keys}):
        members = by_group.get(group)
        if members:
            index = int(_sha(canonical_json_bytes([seed, list(group)])), 16) % len(members)
            chosen.append(members[index])
    return chosen[:VERIFY_K]


def verify(inputs: Inputs, *, now=None) -> str:  # pylint: disable=too-many-locals,too-many-return-statements
    """``verify`` (design §5.6): VERIFIED, REFUTED, or VERIFY_BLOCKED_APPROVAL_EXPIRED (row X4)."""
    ledger, lock = _open_run(inputs)
    try:
        _bound_authority(ledger.records, inputs)
        current = _now(now)
        if lapsed(inputs, current):
            return 'VERIFY_BLOCKED_APPROVAL_EXPIRED'
        try:
            receipt, auth = launch_checks(inputs, current)
        except (ContractValidationError, ValueError, OSError):
            return 'REFUTED'
        if ledger.state.name != 'FINAL':
            raise ScreenRefusal('VERIFY_NOT_FINAL', f'the run is {ledger.state.name}')
        run_dir, doc = inputs.run_dir, _document(inputs)
        params, keys = doc['parameters'], plan_keys(doc['parameters'])
        results_raw = (run_dir / 'results.json').read_bytes()
        journals, code = _record_code(inputs, ledger.records, keys, current)
        recorded = next(r['body']['results_sha256'] for r in ledger.records if r['type'] == 'AGGREGATED')
        reasons = sorted(set(terminal_codes(ledger.records)))
        held = (_sha(results_raw) == recorded
                and (code is None or code in reasons or state.classify(code)[0] == HALTED)
                and results_raw == _results(inputs, doc, ledger.records, journals, keys)
                and label_check(journal.outcomes(journals, keys), params, reasons) == verdict_label(results_raw))
        completed = {tuple(o['key']) for o in journal.outcomes(journals, keys)}
        chosen = verify_keys(results_raw, keys, completed)
        if not chosen:
            return 'VERIFIED' if held else 'REFUTED'
        n = 1 + sum(1 for r in ledger.records if r['type'] == 'VERIFY_START')
        ledger.append('VERIFY_START', {'n': n, 'keys': [list(key) for key in chosen]})
        match = _Run(inputs, receipt, auth, ledger, lock, 1, now).reexecute(n, chosen)
        ledger.append('VERIFY', {'n': n, 'keys': [list(key) for key in chosen], 'match': bool(match)})
        if match is None:
            return 'VERIFY_BLOCKED_APPROVAL_EXPIRED'
        return 'VERIFIED' if held and match else 'REFUTED'
    finally:
        ledger.close()
        lock.release()


def write_error(inputs: Inputs | None, exc: BaseException) -> None:
    """An unexpected exception's traceback, to ``errors/`` of the run directory when there is one."""
    if inputs is None:
        return
    try:
        folder = inputs.run_dir / 'errors'
        if not folder.parent.is_dir():
            return
        folder.mkdir(exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        (folder / f'{stamp}-{os.getpid()}.txt').write_text(
            ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)), encoding='utf-8')
    except OSError:
        pass
