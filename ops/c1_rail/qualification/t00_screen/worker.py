"""T00 step-3 screen worker (design 2026-10-02 §5.1-§5.3; build card §2.9, §3.2, §3.3, P-F note).

Runs only as ``python -I -S -B -c SCREEN_BOOTSTRAP code_root run_dir authority_sha256
journal_name``: the bootstrap installs its audit hook, recording finder and stubs, then runs this
module as ``__main__``. As its first statements, before anything outside the standard library is
imported, the worker installs a second audit hook (card note item 12) that refuses, and records
into ``sys.p7_recorder.refusals``, every rename, link, symlink, path truncate, remove, rmdir,
mkdir and rmtree. Imported under any other name (a test, ``result_adjudication``) it installs
nothing and runs nothing.

The worker binds the run once (row K4), validates r3c and the authority from the bytes the
coordinator sends on stdin, builds its own ``ProductionSource`` and opens its epoch (row K6).
It writes only its own journal (row S2), one record per ``journal.append``; after an append
raises it appends nothing more and reports ``IO_ERROR`` (card F4). ``open_epoch`` and
``bracket`` are the only callers of the screen capability (card §3.2, note item 3). Before each
PATH append and before WORKER_STOP it reads the recorder's refusals: a refusal, even one that
library code swallowed, ends the worker with WORKER_STOP naming that code and ``key: null``,
so the in-flight key stays a loss (note item 11). Coordinator messages are JSON lines on stdin;
replies are ``T00W <json>`` lines on stdout (internal to P-F, card §3.3).
"""
import sys


def _install_write_hook():
    """P-F card note item 12: the write paths the bootstrap's open check does not see."""
    recorder = getattr(sys, 'p7_recorder', None)
    if recorder is None:
        raise SystemExit('SCREEN_BOOTSTRAP_MISMATCH: the worker runs only under the screen bootstrap')
    refusals = recorder.refusals
    events = frozenset({'os.rename', 'os.link', 'os.symlink', 'os.truncate', 'os.remove', 'os.rmdir',
                        'os.mkdir', 'shutil.rmtree'})

    def hook(event, args):
        # os.truncate on a descriptor is covered by that descriptor's own open check.
        if event not in events or (event == 'os.truncate' and isinstance(args[0], int)):
            return
        detail = 'SCREEN_WRITE_REFUSED: ' + event + ' ' + repr(args[0])
        refusals.append(detail)
        raise RuntimeError(detail)
    sys.addaudithook(hook)


if __name__ == '__main__':
    _install_write_hook()

# pylint: disable=wrong-import-position,wrong-import-order
import base64  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
from pathlib import Path  # noqa: E402
import random  # noqa: E402
import re  # noqa: E402
import time  # noqa: E402

from c1_rail.qualification import p7_evidence, screen_authority  # noqa: E402
from c1_rail.qualification.blocks import partition_populations  # noqa: E402
from c1_rail.qualification.contract import (  # noqa: E402
    ObservedBindings, canonical_json_bytes, parse_canonical_json, validate_source_contract)
from c1_rail.qualification.paths import PathAssembler  # noqa: E402
from c1_rail.qualification.production_source import ProductionSource, _now  # noqa: E402
from c1_rail.qualification.runner import evaluate_replay  # noqa: E402
from c1_rail.qualification.t00_screen import journal, plan, state  # noqa: E402
from mc.simulation import EvaluationState  # noqa: E402

PROTOCOL = 'T00W '
DONE = 'DONE'
_CODE = re.compile(r'([A-Z][A-Z0-9_]*):')


class _IOFailed(Exception):
    """A journal append raised (card F4): nothing more is appended to this journal."""


def source_receipt(contract_bytes, approval_bytes, public_keys, artifact_root, now):
    """r3c validated against the bytes on disk, as ``p7_driver._run`` does."""
    doc = parse_canonical_json(contract_bytes, label='source contract')
    root = Path(artifact_root)
    digests = {row['path']: hashlib.sha256((root / row['path']).read_bytes()).hexdigest()
               for row in doc['artifacts']}
    observed = ObservedBindings(digests, {row['role']: digests[row['path']] for row in doc['artifacts']},
                                doc['effective_settings']['settings_sha256'],
                                doc['effective_settings']['orb_normal_base'])
    return validate_source_contract(contract_bytes, approval_bytes, dict(public_keys), observed, now=now)


def decode_inputs(inputs):
    """The launch bytes the coordinator sends (``coordinator.Inputs.message``)."""
    raw = {name: base64.b64decode(inputs[name], validate=True) for name in (
        'authority_b64', 'approval_b64', 'source_contract_b64', 'source_approval_b64', 'p7_record_b64')}
    keys = {key: base64.b64decode(value, validate=True) for key, value in inputs['public_keys'].items()}
    return raw, keys, Path(inputs['artifact_root'])


def open_epoch(source, authority):
    """The only ``screen_epoch`` caller (card §3.2)."""
    return screen_authority.screen_epoch(source, authority=authority)


def bracket(source, path, authority, epoch):
    """The only ``screen_bracket`` caller (card §3.2): the candidate pass, the probe, every path
    key and every ``verify`` re-execution."""
    return screen_authority.screen_bracket(source, path, authority=authority, epoch=epoch)


def reason_code(exc):
    """A worker stop reason: the exception's own code, else its §4.3 class code."""
    named = getattr(exc, 'code', None)
    if isinstance(named, str) and re.fullmatch(r'[A-Z][A-Z0-9_]*', named):
        return named
    found = _CODE.match(str(exc))
    return found.group(1) if found else state.classify(exc)[1]


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _trace(exc):
    """The stop's traceback, on stderr only: the coordinator keeps it under ``errors/`` (row X2)."""
    import traceback  # pylint: disable=import-outside-toplevel
    sys.stderr.write(''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
    sys.stderr.flush()


def _clock():
    return time.process_time(), time.perf_counter()


def _cost(start):
    cpu, wall = _clock()
    return {'cpu_s': max(0.0, cpu - start[0]), 'wall_s': max(0.0, wall - start[1])}


def _add(*costs):
    return {name: sum(cost[name] for cost in costs) for name in ('cpu_s', 'wall_s')}


def _peak_memory():
    """This process's peak working set (Windows) or maximum resident set (POSIX), in bytes."""
    if os.name == 'nt':
        import ctypes  # pylint: disable=import-outside-toplevel
        from ctypes import wintypes  # pylint: disable=import-outside-toplevel

        class Counters(ctypes.Structure):  # PROCESS_MEMORY_COUNTERS
            _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD),
                        ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                        ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t),
                        ('PeakPagefileUsage', ctypes.c_size_t)]
        counters = Counters(cb=ctypes.sizeof(Counters))
        query = ctypes.WinDLL('psapi').GetProcessMemoryInfo
        query.argtypes = (wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD)
        if not query(wintypes.HANDLE(-1), ctypes.byref(counters), counters.cb):  # -1: this process
            return 0
        return int(counters.PeakWorkingSetSize)
    import resource  # pylint: disable=import-outside-toplevel
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024


def path_sha256(path):
    """The path's identity: each occurrence's source session and account date."""
    return _sha(canonical_json_bytes([[s.occurrence, s.source.session_id, s.path_session_date.isoformat()]
                                      for s in path]))


def run_projection(run, failed, splits, outcome):
    """One run of a PATH: P7's projection names (p7_driver.py:55-65) plus the kernel outcome."""
    events = json.dumps([[e.path_time.isoformat(), e.kind, e.leg_id, e.detail] for e in run.events],
                        separators=(',', ':')).encode()
    rows = [[row.source_session_id, row.occurrence, float.hex(row.pnl), float.hex(row.intraday_low), row.fills,
             row.flat_before_deadline, row.start_edge.is_flat, row.end_edge.is_flat] for row in run.sessions]
    events_sha256 = _sha(events)
    return {
        'digest': _sha(p7_evidence.canonical([rows, events_sha256])), 'sessions': len(run.sessions),
        'fills': sum(row.fills for row in run.sessions), 'events_sha256': events_sha256,
        'deadline_failure': failed, 'consumed_intrabar_split_count': len(splits),
        'consumed_intrabar_splits_sha256': _sha(p7_evidence.canonical(sorted(list(item) for item in splits))),
        'status': outcome.status, 'sessions_to_pass': outcome.sessions_to_pass,
        'failure_reason': outcome.failure_reason, 'kernel_outcome': dict(outcome.diagnostics)['kernel_outcome'],
    }


class _Journal:
    """This worker's own journal: created once (O_EXCL), appended by one writer (card F4)."""

    def __init__(self, path):
        flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_EXCL | getattr(os, 'O_BINARY', 0)
        self.fd = os.open(path, flags, 0o644)
        self.prev, self.broken = None, False

    def append(self, kind, body):
        if self.broken:
            raise _IOFailed()
        try:
            self.prev = journal.append(self.fd, kind, body, prev_sha256=self.prev)
        except OSError:
            self.broken = True
            raise _IOFailed() from None


class _Stop(Exception):
    """End the worker with WORKER_STOP{reason, key}."""

    def __init__(self, reason, key=None):
        super().__init__(reason)
        self.reason, self.key = reason, key


class _Worker:  # pylint: disable=too-many-instance-attributes
    """One worker process: its run binding, source, epoch and journal."""

    def __init__(self, run_dir, authority_sha256, own):
        self.recorder = sys.p7_recorder
        self.run_dir, self.authority_sha256, self.journal = run_dir, authority_sha256, own
        self.auth = self.receipt = self.source = self.epoch = self.candidates = None
        self.params = self.initial = None
        self.build = {'cpu_s': 0.0, 'wall_s': 0.0}

    # ---- protocol ---------------------------------------------------------------------------

    @staticmethod
    def say(message):
        sys.stdout.write(PROTOCOL + json.dumps(message, sort_keys=True) + '\n')
        sys.stdout.flush()

    @staticmethod
    def read():
        line = sys.stdin.readline()
        if not line:
            raise _Stop('INTERRUPTED')  # the coordinator is gone
        return json.loads(line)

    def refused(self):
        """The first recorded refusal's code (``p7_evidence`` recorder entries), or None."""
        refusals = self.recorder.refusals
        return refusals[0].split(':', 1)[0] if refusals else None

    # ---- epochs -----------------------------------------------------------------------------

    def open(self, build):
        start = _clock()
        self.epoch = open_epoch(self.source, self.auth)
        integrity = _cost(start)
        self.journal.append('EPOCH_OPEN', {'build': build, 'integrity': integrity,
                                           'closure_sha256': self.epoch.closure_sha256,
                                           'guard_sha256': self.epoch.guard_sha256})
        return integrity

    def close(self):
        """Close the open epoch once; the source stays referenced until then (note item 7)."""
        if self.epoch is None:
            return None
        epoch, self.epoch = self.epoch, None
        start = _clock()
        closed = screen_authority.close_screen_epoch(epoch)
        integrity = _cost(start)
        self.journal.append('EPOCH_CLOSE', {'integrity': integrity, 'closure_match': closed.closure_match,
                                            'closure': json.loads(canonical_json_bytes(dict(closed.closure)))})
        return integrity, closed.closure_match

    # ---- startup ----------------------------------------------------------------------------

    def start(self, message):
        start = _clock()
        screen_authority.bind_screen_run(self.run_dir, self.authority_sha256)
        raw, keys, artifact_root = decode_inputs(message['inputs'])
        self.receipt = source_receipt(raw['source_contract_b64'], raw['source_approval_b64'], keys, artifact_root,
                                      _now())
        self.auth = screen_authority.validate_screen_authority(
            raw['authority_b64'], raw['approval_b64'], keys, source_receipt=self.receipt,
            p7_record_bytes=raw['p7_record_b64'], artifact_root=artifact_root, now=_now())
        if self.auth.authority_sha256 != self.authority_sha256:
            raise _Stop('SCREEN_RUN_UNBOUND')
        self.params = self.auth.parameters
        self.source = ProductionSource.build(self.receipt, artifact_root=artifact_root)
        initial = self.receipt.initial_state
        self.initial = EvaluationState(float(initial.original_basis), float(initial.current_equity),
                                       float(initial.historical_eod_peak), initial.prior_trade_days,
                                       float(initial.prior_max_day_profit))
        self.build = _cost(start)

    def manifest_candidates(self, manifest_sha256):
        """The manifest's candidates, rebuilt and matched (row R2); the bytes must hash to PREPARED's."""
        raw = (self.run_dir / 'manifest.json').read_bytes()
        if _sha(raw) != manifest_sha256:
            raise _Stop(journal.CORRUPTION)
        manifest = parse_canonical_json(raw, label='manifest')
        return plan.rebuild_candidates(self.source.sessions, manifest['populations'],
                                       block_sessions=self.params['block']['length_sessions'])

    # ---- the candidate pass and the probe (design §5.2) -------------------------------------

    def candidate_pass(self):
        start = _clock()
        brackets = {}
        assembler = PathAssembler(self.source.path_start_date)
        for population, pool in partition_populations(self.source.sessions).items():
            path = assembler.assemble(tuple((s,) for s in pool), horizon_sessions=len(pool))
            brackets[population] = bracket(self.source, path, self.auth, self.epoch)
        populations = plan.candidates(self.source.sessions, self.source.adjacent, brackets,
                                      block_sessions=self.params['block']['length_sessions'])
        passed = _cost(start)
        self.journal.append('CANDIDATES', {'populations': populations})
        return populations, passed

    def probe(self, manifest_sha256):
        """One ``probe_root`` path, timed and never scored (rows B2, B3)."""
        build = self.build if self.epoch is None and self.candidates is None else {'cpu_s': 0.0, 'wall_s': 0.0}
        if self.epoch is None:
            self.open(build)
        candidates = self.manifest_candidates(manifest_sha256)
        root = self.params['rng']['probe_root']
        start = _clock()
        complete = True
        try:
            seed = plan.seed(purpose='probe', root=root, population='FULL', path_index=0)
            path = PathAssembler(self.source.path_start_date).sample(
                candidates['FULL'], random.Random(seed), horizon_sessions=self.params['horizon_sessions'])
            screened = bracket(self.source, path, self.auth, self.epoch)
            complete = screened.deadline_failure == (False, False)
            for run, failed in zip((screened.bracket.r1, screened.bracket.r2), screened.deadline_failure):
                plan.shape_check(run, failed, path)
                evaluate_replay(run, initial_state=self.initial)
        except plan.PlanRefusal:
            complete = False
        cost = _cost(start)
        body = {'path_cpu_s': cost['cpu_s'], 'path_wall_s': cost['wall_s'], 'peak_memory_bytes': _peak_memory()}
        self.journal.append('PROBE_RESULT', body)
        _, match = self.close()
        self.say({'type': 'probe', 'complete': complete, 'closure_match': match, **body})

    # ---- path keys (design §5.3) ------------------------------------------------------------

    def path(self, key):
        """Rows K2/K6 checks before KEY_START, then one PATH."""
        screen_authority.require_validated_screen_authority(self.auth, source_contract=self.receipt, now=_now())
        screen_authority.require_open_screen_epoch(self.epoch, source=self.source, authority=self.auth)
        root, population, index = key
        self.journal.append('KEY_START', {'key': list(key)})
        try:
            start = _clock()
            seed = plan.seed(purpose='path', root=root, population=population, path_index=index)
            path = PathAssembler(self.source.path_start_date).sample(
                self.candidates[population], random.Random(seed), horizon_sessions=self.params['horizon_sessions'])
            screened = bracket(self.source, path, self.auth, self.epoch)
            runs = {}
            for name, run, failed, splits in zip(('r1', 'r2'), (screened.bracket.r1, screened.bracket.r2),
                                                 screened.deadline_failure, screened.consumed_splits):
                plan.shape_check(run, failed, path)
                runs[name] = run_projection(run, failed, splits, evaluate_replay(run, initial_state=self.initial))
            first, second = runs['r1']['status'], runs['r2']['status']
            cost = _cost(start)
        except _IOFailed:
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught  # the reason names the key
            _trace(exc)
            raise _Stop(reason_code(exc), key) from None
        if self.refused() is not None:  # note item 11: no PATH after a refusal
            raise _Stop(self.refused())
        self.journal.append('PATH', {
            'key': list(key), 'seed': seed, 'path_sha256': path_sha256(path),
            'bracket_status': first if first == second else 'UNDETERMINED', 'runs': runs,
            'wall_s': cost['wall_s'], 'cpu_s': cost['cpu_s']})
        self.say({'type': 'done', 'key': list(key), 'cpu_s': cost['cpu_s']})

    # ---- roles ------------------------------------------------------------------------------

    @staticmethod
    def guarded(call, *args):
        """Run one step; any exception other than a stop or an append failure stops the worker
        with its reason code (no key: the step ran before any KEY_START or after its PATH)."""
        try:
            return call(*args)
        except (_Stop, _IOFailed):
            raise
        except Exception as exc:  # pylint: disable=broad-exception-caught
            _trace(exc)
            raise _Stop(reason_code(exc)) from None

    def serve(self):
        if self.refused() is not None:
            raise _Stop(self.refused())
        message = self.read()
        self.guarded(self.start, message)
        role = message['role']
        if role == 'candidate':
            self.candidate_role()
        elif role == 'probe':
            self.guarded(self.probe, message['manifest_sha256'])
        else:  # segment and verify workers
            integrity = self.guarded(self.open, self.build)
            self.candidates = self.guarded(self.manifest_candidates, message['manifest_sha256'])
            self.say({'type': 'ready', 'integrity': integrity})
            while True:
                command = self.read()
                if command['cmd'] == 'stop':
                    raise _Stop(command.get('reason') or DONE)
                self.guarded(self.path, tuple(command['key']))

    def candidate_role(self):
        integrity = self.guarded(self.open, self.build)
        populations, passed = self.guarded(self.candidate_pass)
        closed, match = self.guarded(self.close)
        self.candidates = populations
        self.say({'type': 'candidates', 'populations': populations, 'closure_match': match,
                  'build': _add(self.build, passed), 'integrity': _add(integrity, closed)})
        command = self.read()
        if command['cmd'] == 'probe':
            self.guarded(self.probe, command['manifest_sha256'])
        else:
            raise _Stop(command.get('reason') or DONE)

    def stop(self, reason, key):
        """Close any open epoch, then WORKER_STOP as the last record; a refusal overrides the reason."""
        if self.refused() is not None:
            reason, key = self.refused(), None
        try:
            closed = self.close()
        except _IOFailed:
            raise
        except Exception:  # pylint: disable=broad-exception-caught  # a failed close is drift
            closed = None
        if closed is not None and not closed[1] and reason == DONE:
            reason = 'CODE_OR_ARTIFACT_DRIFT'
        if self.refused() is not None:
            reason, key = self.refused(), None
        self.journal.append('WORKER_STOP', {'reason': reason, 'key': None if key is None else list(key)})
        self.say({'type': 'stopped', 'reason': reason})
        return 0 if reason == DONE else 3


def main():
    code_root, run_dir, authority_sha256, journal_name = sys.argv[1:5]  # pylint: disable=unbalanced-tuple-unpacking
    del code_root  # the bootstrap's import root; the run is bound by run_dir and authority_sha256
    run_dir = Path(run_dir)
    worker = _Worker(run_dir, authority_sha256, _Journal(run_dir / 'journal' / journal_name))
    try:
        try:
            worker.serve()
            status = worker.stop(DONE, None)
        except _Stop as stop:
            status = worker.stop(stop.reason, stop.key)
    except _IOFailed:
        _Worker.say({'type': 'io_error'})
        status = 4
    sys.stdout.flush()
    raise SystemExit(status)


if __name__ == '__main__':
    main()
