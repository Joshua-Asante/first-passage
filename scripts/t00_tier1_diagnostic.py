#!/usr/bin/env python3
"""T00 step-12 diagnostic, Tier 1 driver.

Card: docs/briefs/handoffs/2026-10-08-t00-step12-diagnostic-tier1-card.md. Three modes, each
run once and in order:

- ``freeze`` selects the keys from the retained step-12 journals and writes the key list. It
  builds no source and replays nothing.
- ``selftest`` re-derives the selection, builds the source, rebuilds every selected path from
  its key and checks its seed and ``path_sha256`` against the retained PATH record. It replays
  nothing.
- ``run`` repeats the self-test, then replays each path once through the sealed
  ``ProductionSource.replay_bracket`` (the p7_driver pattern) and compares its identities
  with the retained PATH record. The first path is the checkpoint.

Every module except this file is imported from ``--code-root``, the clean detached checkout at
H, with bytecode writes off and a fresh ``sys.pycache_prefix``. A module loaded from anywhere
else is a PREREQUISITE stop. Outputs are create-once, atomically written files under ``--out``,
which must lie outside the code root and the run directory. stdout is one line, ``T00_TIER1
<mode> <verdict> <code> keys_sha256=<hex>``; it carries no count, rate or timing.

Stop codes:
- PREREQUISITE is raised before a replay starts.
- REFUSED is a source refusal: at build, or during a replay when it is a
  ``ContractValidationError`` or is raised inside ``ProductionSource._check_path`` (which runs
  ``_verify_integrity``, ``_resolve_domain`` and ``_qualification_snapshots`` before any engine is
  built). It is classified by where it was raised, not by its message.
- NON_REPRODUCTION is any identity mismatch, or any other exception raised while replaying a
  selected path (host faults such as ``MemoryError`` and ``OSError`` included). Every retained
  PATH record came from a bracket that returned normally.
- DRIVER_DEFECT is a driver fault, before a replay or after one has returned.
- BUDGET is the CPU, wall or checkpoint limit.
- EVIDENCE_WRITE_FAILED: a run that would be RESOLVED could not write ``summary.json``. A run that
  had already stopped keeps its verdict and code; the write failure goes to stderr. Either way the
  exit status is nonzero, and the reservation still blocks a retry.

For a run, every stop's exception type and detail go to ``summary.json`` and to stderr, so a
host fault can be told apart from a real non-reproduction.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import os
import random
import subprocess
import sys
import tempfile
import threading
import time

H = '5d25f9cfc1e8ff00bacda45478322f9858176e8b'
RESULTS_SHA256 = 'a5b985d0abd79177fd910648ffbfaec040f6a4ac04728c8acee1f1e347a742dc'
ATTESTATION_SHA256 = 'f627e805ba3e92ef1bc461804cb8877494d77c9a42d5344626c4795d379d1ed5'
PINS = {  # build card §8 and the step-12 return
    'authority': '241708a197c2ce3964df77674eaa8189f4b1882b29aa650ad280e62692bc91d3',
    'source_contract': 'a526b50fa75e68451bdd2b5b57fa7a04e6ee08e61f96865c915ae8116a848d97',
    'source_approval': '2cc7195efd4f221fcd011d94a9b9692b7254cffa87dd79e0c876b987dd3cb163',
    'registry': '780da6c997a8515d6c1a92f343317e6e7ea3199014028e4e083ab4df39b589e3',
}
POPULATIONS = ('FULL', 'H1', 'H2')
CLASSES = ('FAILURE', 'PASS', 'UNDETERMINED')  # FULL/FAILURE first: the checkpoint stratum
PER_STRATUM = 2
CPU_CEILING_S, WALL_CEILING_S, CHECKPOINT_CPU_S = 7200.0, 10800.0, 225.0
COMPARED = ('digest', 'sessions', 'fills', 'events_sha256', 'deadline_failure',
            'consumed_intrabar_split_count', 'consumed_intrabar_splits_sha256')
KEYS_SCHEMA = 't00_tier1_keys/v1'
# replay_bracket's pre-replay gate (production_source.py at H): _check_path runs _verify_integrity,
# which runs _resolve_domain and _qualification_snapshots, before any engine is built.
GATE_FRAME = ('production_source.py', '_check_path')
PORT_MODULE_PREFIX = 'fp_qualification_port_'  # book_adapters._load_domain_adapters


class Stop(Exception):
    """A classified stop; ``code`` is one of the module docstring's stop codes."""

    def __init__(self, code, detail='', exc_type=None):
        super().__init__(detail)
        self.code, self.exc_type = code, exc_type


def sha256_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def key_hash(key, canonical) -> str:
    return hashlib.sha256(canonical(list(key))).hexdigest()


def select_keys(outcomes, canonical):
    """Card §3: per (population, class), the first PER_STRATUM keys by sha256(canonical(key)).

    A stratum with fewer paths contributes all it has; nothing is substituted from another stratum.
    Returns (keys in checkpoint-first stratum order, available count per stratum)."""
    strata = {(p, c): [] for p in POPULATIONS for c in CLASSES}
    for outcome in outcomes:
        cell = (outcome['key'][1], outcome['bracket_status'])
        if cell in strata:
            strata[cell].append(tuple(outcome['key']))
    keys = []
    for cell in strata:
        keys.extend(sorted(strata[cell], key=lambda k: key_hash(k, canonical))[:PER_STRATUM])
    return keys, {f'{p}|{c}': len(v) for (p, c), v in strata.items()}


def keys_document(keys, available, canonical) -> bytes:
    return canonical({'schema': KEYS_SCHEMA, 'results_sha256': RESULTS_SHA256,
                      'keys': [list(k) for k in keys], 'available': available})


def sealed_identity(run, canonical, sha256_bytes):
    """A sealed run's identities, computed as t00_screen/worker.py:run_projection computes them."""
    rows = [[r.source_session_id, r.occurrence, float.hex(r.pnl), float.hex(r.intraday_low), r.fills,
             r.flat_before_deadline, r.start_flat, r.end_flat] for r in run.sessions]
    return {'digest': sha256_bytes(canonical([rows, run.events_sha256])), 'sessions': len(run.sessions),
            'fills': sum(r.fills for r in run.sessions), 'events_sha256': run.events_sha256,
            'deadline_failure': run.deadline_failure,
            'consumed_intrabar_split_count': len(run.consumed_intrabar_splits),
            'consumed_intrabar_splits_sha256': sha256_bytes(canonical(
                sorted(list(item) for item in run.consumed_intrabar_splits)))}


def mismatches(retained_runs, replayed):
    return [f'{name}.{field}' for name in ('r1', 'r2') for field in COMPARED
            if retained_runs[name][field] != replayed[name][field]]


def is_gate_refusal(exc, contract_error) -> bool:
    """A source refusal, classified by where it was raised, not by its message."""
    if isinstance(exc, contract_error):
        return True
    frame = exc.__traceback__
    while frame is not None:
        code = frame.tb_frame.f_code
        if (Path(code.co_filename).name, code.co_name) == GATE_FRAME:
            return True
        frame = frame.tb_next
    return False


def _write_once(path: Path, data: bytes):
    """Create-once and atomic: a flushed, synced temporary file, then os.replace. An interruption
    leaves no partial target."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(str(path))
    temporary = path.with_name(f'{path.name}.tmp-{os.getpid()}')
    with open(temporary, 'xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _git(code_root, *args):
    return subprocess.run(['git', '-C', str(code_root), *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def isolate_bytecode():
    """No .pyc is written, and none written before this run is read (as the P7 bootstrap guards)."""
    sys.dont_write_bytecode = True
    sys.pycache_prefix = tempfile.mkdtemp(prefix='t00-tier1-pycache-')


def foreign_modules(code_root: Path, allowed_roots, modules=None, *, artifact_paths=frozenset()):
    """Loaded modules whose file is outside the code root and every allowed (stdlib, venv, driver) root.

    The port modules carry ``__file__`` = their contract artifact path, relative to the artifact root
    (book_adapters._load_domain_adapters). They are allowed by that exact path, whose bytes the
    source build digest-checked, so the check does not depend on the working directory."""
    roots = [Path(r).resolve() for r in (code_root, *allowed_roots)]
    found = []
    for name, module in list((sys.modules if modules is None else modules).items()):
        origin = getattr(module, '__file__', None)
        if not origin:
            continue
        if name.startswith(PORT_MODULE_PREFIX) and str(origin).replace('\\', '/') in artifact_paths:
            continue
        if not any(Path(origin).resolve().is_relative_to(root) for root in roots):
            found.append(name)
    return sorted(found)


def _allowed_roots():
    return (sys.base_prefix, sys.prefix, sys.exec_prefix, Path(__file__).resolve())


def artifact_paths(source_contract) -> frozenset:
    doc = json.loads(Path(source_contract).read_bytes())
    return frozenset(row['path'].replace('\\', '/') for row in doc['artifacts'])


def _foreign_after_run(code_root, artifacts=frozenset()):
    return foreign_modules(code_root, _allowed_roots(), artifact_paths=artifacts)


def _check_origins(code_root, artifacts=frozenset()):
    found = foreign_modules(code_root, _allowed_roots(), artifact_paths=artifacts)
    if found:
        raise Stop('PREREQUISITE', 'modules loaded from outside the code root: ' + ', '.join(found[:5]))


def _modules(code_root: Path):
    """Import the H modules from ``code_root`` only."""
    for layer in ('core', 'ops'):
        sys.path.insert(0, str(code_root / layer))
    # pylint: disable=import-outside-toplevel
    from c1_rail.qualification import p7_evidence
    from c1_rail.qualification.contract import (
        ContractValidationError, ObservedBindings, canonical_json_bytes, parse_canonical_json,
        validate_source_contract)
    from c1_rail.qualification.paths import PathAssembler
    from c1_rail.qualification.production_source import ProductionSource, _now
    from c1_rail.qualification.t00_screen import journal, plan, verdict, worker
    _check_origins(code_root)
    return dict(p7_evidence=p7_evidence, ObservedBindings=ObservedBindings, canonical=canonical_json_bytes,
                parse=parse_canonical_json, validate_source_contract=validate_source_contract,
                ContractValidationError=ContractValidationError, PathAssembler=PathAssembler,
                ProductionSource=ProductionSource, now=_now, journal=journal, plan=plan, verdict=verdict,
                worker=worker)


def prerequisites(args):
    code_root, run_dir, out = (Path(p).resolve() for p in (args.code_root, args.run_dir, args.out))
    if _git(code_root, 'rev-parse', 'HEAD') != H or _git(code_root, 'status', '--porcelain', '--untracked-files=all'):
        raise Stop('PREREQUISITE', 'code root is not a clean checkout at H')
    if out.is_relative_to(code_root) or out.is_relative_to(run_dir):
        raise Stop('PREREQUISITE', 'output directory inside the code root or the run directory')
    for name, pin in PINS.items():
        if sha256_file(getattr(args, name)) != pin:
            raise Stop('PREREQUISITE', f'{name} does not match its pin')
    if sha256_file(run_dir / 'results.json') != RESULTS_SHA256:
        raise Stop('PREREQUISITE', 'results.json does not match #724')
    if sha256_file(run_dir / 'attestation.json') != ATTESTATION_SHA256:
        raise Stop('PREREQUISITE', 'attestation.json does not match #724')
    return code_root, run_dir, out


def ledger_binding(m, run_dir: Path):
    """(PREPARED's manifest digest, [(type, record SHA-256, body)]) from the chain-verified ledger;
    its files chain in number order."""
    prev, prepared, chain = None, None, []
    for path in sorted((run_dir / 'ledger').glob('*.jsonl')):
        for record in m['journal'].read(path, prev_sha256=prev):
            prev = m['journal'].record_sha256(record)
            chain.append((record['type'], prev, record['body']))
            if record['type'] == 'PREPARED':
                prepared = record['body']['manifest_sha256']
    if prepared is None:
        raise Stop('PREREQUISITE', 'no PREPARED record in the ledger')
    return prepared, chain


def attested_ledger(chain, attested_head) -> bool:
    """The attestation is written at REPORTED (coordinator.finalize): the attested head must be a
    REPORTED record, the next record the FINAL naming this attestation, then one or more
    VERIFY_START/VERIFY pairs numbered from 1, each VERIFY with its start's ``n`` and ``keys`` and
    ``match: true``."""
    at = [i for i, (_, sha, _) in enumerate(chain) if sha == attested_head]
    if len(at) != 1 or chain[at[0]][0] != 'REPORTED' or at[0] + 1 >= len(chain):
        return False
    kind, _, body = chain[at[0] + 1]
    tail = chain[at[0] + 2:]
    if kind != 'FINAL' or body.get('attestation_sha256') != ATTESTATION_SHA256 or not tail or len(tail) % 2:
        return False
    for n, ((k1, _, start), (k2, _, done)) in enumerate(zip(tail[::2], tail[1::2]), 1):
        if (k1, k2) != ('VERIFY_START', 'VERIFY') or start.get('n') != n or done.get('n') != n:
            return False
        if done.get('keys') != start.get('keys') or done.get('match') is not True:
            return False
    return True


def retained(m, run_dir: Path, params):
    """The record of truth: the chain-verified segment journals, bound to the pinned attestation (each
    segment journal's head and the ledger) and cross-checked against results.json."""
    results = json.loads((run_dir / 'results.json').read_text(encoding='utf-8'))
    attestation = json.loads((run_dir / 'attestation.json').read_text(encoding='utf-8'))
    journals = {p.name: m['journal'].read(p, prev_sha256=None) for p in sorted((run_dir / 'journal').glob('s*.jsonl'))}
    attested = {name: head for name, head in attestation['journal_heads'].items() if name.startswith('s')}
    heads = {name: m['journal'].record_sha256(records[-1]) if records else None for name, records in journals.items()}
    if attestation.get('results_sha256') != RESULTS_SHA256 or not attested or heads != attested:
        raise Stop('PREREQUISITE', 'segment journals do not match the attested heads')
    if not attested_ledger(ledger_binding(m, run_dir)[1], attestation.get('ledger_head_sha256')):
        raise Stop('PREREQUISITE', 'ledger is not the attested ledger plus FINAL and matching verify records')
    keys = m['plan'].key_universe(params['rng']['roots'], params['depth_per_root'])
    if m['plan'].plan_sha256(keys) != results['plan_sha256']:
        raise Stop('PREREQUISITE', 'plan digest differs from results.json')
    outcomes = m['journal'].outcomes(journals, keys)
    if len(outcomes) != len(keys) or m['verdict'].as_json(m['verdict'].evaluate(outcomes, params, ())) != results['verdict']:
        raise Stop('PREREQUISITE', 'journals do not re-derive the finalized verdict')
    return {tuple(o['key']): o for o in outcomes}


def load_keys(m, out: Path, keys_sha256: str, by_key):
    """The frozen key list: its hash, schema and results binding, and the selection re-derived."""
    raw = (out / 'keys.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != keys_sha256:
        raise Stop('PREREQUISITE', 'keys.json does not match the published key-list hash')
    doc = m['parse'](raw, label='keys')
    keys, available = select_keys(by_key.values(), m['canonical'])
    if (doc.get('schema') != KEYS_SCHEMA or doc.get('results_sha256') != RESULTS_SHA256
            or raw != keys_document(keys, available, m['canonical'])):
        raise Stop('PREREQUISITE', 'keys.json is not the selection the retained journals give')
    return keys


def build_source(m, args):
    contract_bytes, approval_bytes = Path(args.source_contract).read_bytes(), Path(args.source_approval).read_bytes()
    registry = {k: base64.b64decode(v) for k, v in json.loads(Path(args.registry).read_text(encoding='utf-8')).items()}
    doc, root = json.loads(contract_bytes), Path(args.artifact_root)
    digests = {row['path']: sha256_file(root / row['path']) for row in doc['artifacts']}
    observed = m['ObservedBindings'](digests, {row['role']: digests[row['path']] for row in doc['artifacts']},
                                     doc['effective_settings']['settings_sha256'],
                                     doc['effective_settings']['orb_normal_base'])
    try:
        receipt = m['validate_source_contract'](contract_bytes, approval_bytes, registry, observed, now=m['now']())
        return m['ProductionSource'].build(receipt, artifact_root=root)
    except ValueError as exc:
        raise Stop('REFUSED', str(exc).split(':', 1)[0], exc_type=type(exc).__name__) from None


def assemble(m, source, run_dir: Path, params, by_key, keys):
    """Self-test: every selected path's seed and path_sha256 equal the retained PATH record."""
    raw = (run_dir / 'manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != ledger_binding(m, run_dir)[0]:
        raise Stop('PREREQUISITE', "manifest.json does not match PREPARED's digest")
    manifest = m['parse'](raw, label='manifest')
    candidates = m['plan'].rebuild_candidates(source.sessions, manifest['populations'],
                                              block_sessions=params['block']['length_sessions'])
    paths = []
    for root, population, index in keys:
        seed = m['plan'].seed(purpose='path', root=root, population=population, path_index=index)
        path = m['PathAssembler'](source.path_start_date).sample(
            candidates[population], random.Random(seed), horizon_sessions=params['horizon_sessions'])
        record = by_key[(root, population, index)]
        if seed != record['seed'] or m['worker'].path_sha256(path) != record['path_sha256']:
            raise Stop('DRIVER_DEFECT', f'path {len(paths) + 1}: seed or path_sha256 differs')
        paths.append(path)
    return paths


class ReplayGuard:
    """Marks the span of ``replay_bracket``: the watchdog may hard-stop only inside it."""

    def __init__(self):
        self.lock, self.active = threading.Lock(), False

    def set(self, active: bool):
        with self.lock:
            self.active = active


def _replay(m, source, path, guard=None):
    if guard is not None:
        guard.set(True)
    try:
        sealed = source.replay_bracket(path)
    except Exception as exc:  # pylint: disable=broad-exception-caught  # classified below
        kind = type(exc).__name__
        if is_gate_refusal(exc, m['ContractValidationError']):
            raise Stop('REFUSED', str(exc).split(':', 1)[0], exc_type=kind) from None
        raise Stop('NON_REPRODUCTION', f'replay raised {kind}: {str(exc)[:300]}', exc_type=kind) from None
    finally:
        if guard is not None:
            guard.set(False)
    ev = m['p7_evidence']
    return sealed, {name: sealed_identity(run, ev.canonical, ev.sha256_bytes)
                    for name, run in (('r1', sealed.r1), ('r2', sealed.r2))}


def _series(sealed):
    return {name: [[r.source_session_id, r.occurrence, r.pnl, r.intraday_low, r.fills, r.flat_before_deadline,
                    r.start_flat, r.end_flat] for r in run.sessions] for name, run in (('r1', sealed.r1), ('r2', sealed.r2))}


def budget_breached(cpu_s, elapsed_s) -> bool:
    return cpu_s > CPU_CEILING_S or elapsed_s > WALL_CEILING_S


def watchdog(wall_start, done, guard, on_breach, *, interval=5.0, clock=time):
    """In-replay enforcement. Polls process CPU and wall time until ``done`` is set. On a breach it
    acts only while ``guard`` marks a replay in progress, holding the guard's lock so the replay
    cannot be marked finished meanwhile; outside a replay the main thread's own checks stop the run."""
    while not done.wait(interval):
        if budget_breached(clock.process_time(), clock.monotonic() - wall_start):
            with guard.lock:
                if guard.active:
                    on_breach()
                    return


def _hard_stop(out: Path, keys_sha256: str, *, exit_fn=os._exit):  # pylint: disable=protected-access
    """A breach during a replay: no path record is in progress, so record the stop atomically, print
    the stop line and end the process at once."""
    try:
        _write_once(out / 'run' / 'summary.json', json.dumps(
            {'verdict': 'AMBIGUOUS', 'code': 'BUDGET', 'replayed': None, 'in_replay': True,
             'keys_sha256': keys_sha256, 'exc_type': None, 'detail': 'budget breached during a replay'},
            sort_keys=True).encode())
    except OSError as exc:
        sys.stderr.write(f'SUMMARY_NOT_WRITTEN: {type(exc).__name__}: {exc}\n')
    sys.stderr.write('BUDGET: -: budget breached during a replay\n')
    sys.stdout.write(f'T00_TIER1 run AMBIGUOUS BUDGET keys_sha256={keys_sha256}\n')
    sys.stdout.flush()
    sys.stderr.flush()
    exit_fn(3)


def reserve(out: Path):
    """Atomically reserve the one run before anything is built or replayed. The reservation is
    never removed: a crash, a refusal or a second invocation finds it and stops."""
    out.mkdir(parents=True, exist_ok=True)
    try:
        (out / 'run').mkdir()
    except FileExistsError:
        raise Stop('PREREQUISITE', 'the run is already reserved; run is once only') from None
    _write_once(out / 'run' / 'RESERVED', json.dumps(
        {'pid': os.getpid(), 'reserved_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}).encode())


def run_paths(m, source, paths, keys, by_key, out: Path, *, wall_start: float, guard=None):
    """Card §5 item 4. CPU is the process's own since start; wall is measured from ``wall_start``
    (the top of ``main``). Before each path the last path's CPU and wall costs predict the next;
    after each path the cumulative limits are checked, so an overrun is never RESOLVED. A detected
    mismatch returns before any budget check, so it is never reported as BUDGET. The watchdog in
    ``main`` enforces the limits during a replay. Returns (verdict, code, paths replayed, detail),
    ``detail`` None or {exc_type, detail}."""
    last_cpu = last_wall = 0.0
    for ordinal, (key, path) in enumerate(zip(keys, paths), 1):
        if budget_breached(time.process_time() + last_cpu, time.monotonic() - wall_start + last_wall):
            return 'AMBIGUOUS', 'BUDGET', ordinal - 1, None
        t_cpu, t_wall = time.process_time(), time.monotonic()
        try:
            sealed, replayed = _replay(m, source, path, guard)
        except Stop as stop:
            return (('FALSIFIED' if stop.code == 'NON_REPRODUCTION' else 'AMBIGUOUS'), stop.code, ordinal - 1,
                    {'exc_type': stop.exc_type, 'detail': str(stop)})
        last_cpu, last_wall = time.process_time() - t_cpu, time.monotonic() - t_wall
        bad = mismatches(by_key[key]['runs'], replayed)
        _write_once(out / 'run' / f'{ordinal:02d}.json', json.dumps(
            {'key': list(key), 'identities': replayed, 'mismatches': bad,
             'cost': {'cpu_s': last_cpu, 'wall_s': last_wall}, 'series': _series(sealed)}, sort_keys=True).encode())
        if bad:
            return ('FALSIFIED', 'NON_REPRODUCTION', ordinal,
                    {'exc_type': None, 'detail': 'identity mismatch: ' + ', '.join(bad)})
        if budget_breached(time.process_time(), time.monotonic() - wall_start):
            return 'AMBIGUOUS', 'BUDGET', ordinal, None
        if ordinal == 1 and last_cpu > CHECKPOINT_CPU_S:
            return 'AMBIGUOUS', 'BUDGET', ordinal, None
    return 'RESOLVED', 'OK', len(keys), None


def _parser():
    parser = argparse.ArgumentParser(prog='t00_tier1_diagnostic')
    parser.add_argument('mode', choices=('freeze', 'selftest', 'run'))
    for name in ('--code-root', '--run-dir', '--authority', '--source-contract', '--source-approval',
                 '--registry', '--artifact-root', '--out'):
        parser.add_argument(name, required=True)
    parser.add_argument('--keys-sha256')
    return parser


def _run_summary(out: Path, keys_sha256, verdict, code, replayed, detail) -> bool:
    """summary.json for a reserved run, with the stop's exception type and detail. Returns whether it
    was written; a failure is reported on stderr and never swallowed silently."""
    detail = detail or {}
    try:
        _write_once(out / 'run' / 'summary.json', json.dumps(
            {'verdict': verdict, 'code': code, 'replayed': replayed, 'keys_sha256': keys_sha256,
             'exc_type': detail.get('exc_type'), 'detail': detail.get('detail'),
             'foreign_modules': detail.get('foreign_modules', [])}, sort_keys=True).encode())
        return True
    except OSError as exc:
        sys.stderr.write(f'EVIDENCE_WRITE_FAILED: {type(exc).__name__}: {exc}\n')
        return False


def _after_run(verdict, code, detail, foreign):
    """The post-run origin check is recorded alongside; it turns only a RESOLVED run into a
    PREREQUISITE stop and never overrides a FALSIFIED or other stop."""
    detail = dict(detail or {})
    if foreign:
        detail['foreign_modules'] = foreign
        if code == 'OK':
            verdict, code = 'AMBIGUOUS', 'PREREQUISITE'
            detail.setdefault('detail', 'modules loaded from outside the code root: ' + ', '.join(foreign[:5]))
    return verdict, code, detail


def main(argv=None) -> int:  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    wall_start = time.monotonic()
    args = _parser().parse_args(argv)
    keys_sha256, verdict, code, reserved, out = args.keys_sha256 or '-', '-', 'OK', False, None
    try:
        code_root, run_dir, out = prerequisites(args)
        if args.mode != 'freeze' and not args.keys_sha256:
            raise Stop('PREREQUISITE', '--keys-sha256 is required')
        if args.mode == 'run':
            reserve(out)
            reserved = True
        isolate_bytecode()
        m = _modules(code_root)
        params = json.loads(Path(args.authority).read_text(encoding='utf-8'))['parameters']
        try:
            by_key = retained(m, run_dir, params)
        except ValueError as exc:
            raise Stop('PREREQUISITE', f'retained evidence: {exc}', exc_type=type(exc).__name__) from None
        if args.mode == 'freeze':
            keys, available = select_keys(by_key.values(), m['canonical'])
            raw = keys_document(keys, available, m['canonical'])
            _write_once(out / 'keys.json', raw)
            keys_sha256, verdict = hashlib.sha256(raw).hexdigest(), 'FROZEN'
        else:
            keys = load_keys(m, out, args.keys_sha256, by_key)
            artifacts = artifact_paths(args.source_contract)
            source = build_source(m, args)
            _check_origins(code_root, artifacts)
            paths = assemble(m, source, run_dir, params, by_key, keys)
            if args.mode == 'selftest':
                verdict = 'SELFTEST_PASSED'
            else:
                done_event, guard = threading.Event(), ReplayGuard()
                threading.Thread(target=watchdog, args=(wall_start, done_event, guard,
                                                        lambda: _hard_stop(out, args.keys_sha256)), daemon=True).start()
                try:
                    verdict, code, done, detail = run_paths(m, source, paths, keys, by_key, out,
                                                            wall_start=wall_start, guard=guard)
                finally:
                    done_event.set()
                verdict, code, detail = _after_run(verdict, code, detail, _foreign_after_run(code_root, artifacts))
                if detail:
                    sys.stderr.write(f"{code}: {detail.get('exc_type') or '-'}: {detail.get('detail')}\n")
                reserved = False  # the summary is attempted once, here
                if not _run_summary(out, args.keys_sha256, verdict, code, done, detail) and code == 'OK':
                    # A host or evidence fault, not a driver bug: an otherwise RESOLVED run is not reported
                    # as RESOLVED without its summary. A stop already recorded keeps its verdict and code.
                    verdict, code = 'AMBIGUOUS', 'EVIDENCE_WRITE_FAILED'
    except Stop as stop:
        verdict, code = ('AMBIGUOUS' if args.mode == 'run' else 'STOPPED'), stop.code
        sys.stderr.write(f'{stop.code}: {stop.exc_type or "-"}: {stop}\n')
        if reserved:
            _run_summary(out, args.keys_sha256, verdict, code, None, {'exc_type': stop.exc_type, 'detail': str(stop)})
    except Exception as exc:  # pylint: disable=broad-exception-caught  # unclassified = a driver defect
        verdict, code = ('AMBIGUOUS' if args.mode == 'run' else 'STOPPED'), 'DRIVER_DEFECT'
        sys.stderr.write(f'DRIVER_DEFECT: {type(exc).__name__}: {exc}\n')
        if reserved:
            _run_summary(out, args.keys_sha256, verdict, code, None,
                         {'exc_type': type(exc).__name__, 'detail': str(exc)[:300]})
    print(f'T00_TIER1 {args.mode} {verdict} {code} keys_sha256={keys_sha256}')
    return 0 if code == 'OK' else 3


if __name__ == '__main__':
    raise SystemExit(main())
