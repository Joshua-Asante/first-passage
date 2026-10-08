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
else is a PREREQUISITE stop. Outputs are create-once files under ``--out``, which must lie
outside the code root and the run directory. stdout is one line, ``T00_TIER1 <mode>
<verdict> <code> keys_sha256=<hex>``; it carries no count, rate or timing.

Stop codes:
- PREREQUISITE, DRIVER_DEFECT and REFUSED are raised before a replay starts.
- NON_REPRODUCTION is any identity mismatch, or any exception raised while replaying a
  selected path other than a documented source-gate refusal. Every retained PATH record came
  from a bracket that returned normally.
- BUDGET is the CPU, wall or checkpoint limit.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import time

H = '5d25f9cfc1e8ff00bacda45478322f9858176e8b'
RESULTS_SHA256 = 'a5b985d0abd79177fd910648ffbfaec040f6a4ac04728c8acee1f1e347a742dc'
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
# The source-gate refusals replay_bracket raises before any engine runs (production_source.py
# _verify_integrity and _check_path at H), plus every ContractValidationError (approval lifecycle).
GATE_MESSAGES = frozenset({
    'factory-issued source object required',
    'issued source execution state changed',
    'source factory identity does not bind the exact production G1 contract',
    'path contains a source session outside retained covered panel',
})


class Stop(Exception):
    """A classified stop; ``code`` is one of the module docstring's stop codes."""

    def __init__(self, code, detail=''):
        super().__init__(detail)
        self.code = code


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
    return isinstance(exc, contract_error) or (type(exc) is ValueError and str(exc) in GATE_MESSAGES)


def _write_once(path: Path, data: bytes):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'xb') as handle:
        handle.write(data)


def _git(code_root, *args):
    return subprocess.run(['git', '-C', str(code_root), *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def isolate_bytecode():
    """No .pyc is written, and none written before this run is read (as the P7 bootstrap guards)."""
    sys.dont_write_bytecode = True
    sys.pycache_prefix = tempfile.mkdtemp(prefix='t00-tier1-pycache-')


def foreign_modules(code_root: Path, allowed_roots, modules=None):
    """Loaded modules whose file is outside the code root and every allowed (stdlib, venv) root."""
    roots = [Path(r).resolve() for r in (code_root, *allowed_roots)]
    found = []
    for name, module in list((sys.modules if modules is None else modules).items()):
        origin = getattr(module, '__file__', None)
        if origin and not any(Path(origin).resolve().is_relative_to(root) for root in roots):
            found.append(name)
    return sorted(found)


def _allowed_roots():
    return (sys.base_prefix, sys.prefix, sys.exec_prefix, Path(__file__).resolve().parent)


def _check_origins(code_root):
    found = foreign_modules(code_root, _allowed_roots())
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
    return code_root, run_dir, out


def prepared_manifest_sha256(m, run_dir: Path) -> str:
    """PREPARED's manifest digest from the chain-verified ledger (files chain in number order)."""
    prev, prepared = None, None
    for path in sorted((run_dir / 'ledger').glob('*.jsonl')):
        records = m['journal'].read(path, prev_sha256=prev)
        if records:
            prev = m['journal'].record_sha256(records[-1])
        prepared = next((r['body']['manifest_sha256'] for r in records if r['type'] == 'PREPARED'), prepared)
    if prepared is None:
        raise Stop('PREREQUISITE', 'no PREPARED record in the ledger')
    return prepared


def retained(m, run_dir: Path, params):
    """The record of truth: the chain-verified segment journals, cross-checked against results.json."""
    results = json.loads((run_dir / 'results.json').read_text(encoding='utf-8'))
    journals = {p.name: m['journal'].read(p, prev_sha256=None) for p in sorted((run_dir / 'journal').glob('s*.jsonl'))}
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
        raise Stop('REFUSED', str(exc).split(':', 1)[0]) from None


def assemble(m, source, run_dir: Path, params, by_key, keys):
    """Self-test: every selected path's seed and path_sha256 equal the retained PATH record."""
    raw = (run_dir / 'manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != prepared_manifest_sha256(m, run_dir):
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


def _replay(m, source, path):
    try:
        sealed = source.replay_bracket(path)
    except Exception as exc:  # pylint: disable=broad-exception-caught  # classified below
        if is_gate_refusal(exc, m['ContractValidationError']):
            raise Stop('REFUSED', str(exc).split(':', 1)[0]) from None
        raise Stop('NON_REPRODUCTION', f'replay raised {type(exc).__name__}') from None
    ev = m['p7_evidence']
    return sealed, {name: sealed_identity(run, ev.canonical, ev.sha256_bytes)
                    for name, run in (('r1', sealed.r1), ('r2', sealed.r2))}


def _series(sealed):
    return {name: [[r.source_session_id, r.occurrence, r.pnl, r.intraday_low, r.fills, r.flat_before_deadline,
                    r.start_flat, r.end_flat] for r in run.sessions] for name, run in (('r1', sealed.r1), ('r2', sealed.r2))}


def run_paths(m, source, paths, keys, by_key, out: Path, *, wall_start: float):
    """Card §5 item 4. CPU is the process's own since start; wall is measured from ``wall_start``
    (the top of ``main``). Returns (verdict, code, paths replayed)."""
    last = 0.0
    for ordinal, (key, path) in enumerate(zip(keys, paths), 1):
        if time.process_time() + last > CPU_CEILING_S or time.monotonic() - wall_start + last > WALL_CEILING_S:
            return 'AMBIGUOUS', 'BUDGET', ordinal - 1
        t_cpu, t_wall = time.process_time(), time.monotonic()
        try:
            sealed, replayed = _replay(m, source, path)
        except Stop as stop:
            return ('FALSIFIED' if stop.code == 'NON_REPRODUCTION' else 'AMBIGUOUS'), stop.code, ordinal - 1
        cost = {'cpu_s': time.process_time() - t_cpu, 'wall_s': time.monotonic() - t_wall}
        bad = mismatches(by_key[key]['runs'], replayed)
        _write_once(out / 'run' / f'{ordinal:02d}.json', json.dumps(
            {'key': list(key), 'identities': replayed, 'mismatches': bad, 'cost': cost,
             'series': _series(sealed)}, sort_keys=True).encode())
        if bad:
            return 'FALSIFIED', 'NON_REPRODUCTION', ordinal
        last = cost['cpu_s']
        if ordinal == 1 and last > CHECKPOINT_CPU_S:
            return 'AMBIGUOUS', 'BUDGET', ordinal
    return 'RESOLVED', 'OK', len(keys)


def _parser():
    parser = argparse.ArgumentParser(prog='t00_tier1_diagnostic')
    parser.add_argument('mode', choices=('freeze', 'selftest', 'run'))
    for name in ('--code-root', '--run-dir', '--authority', '--source-contract', '--source-approval',
                 '--registry', '--artifact-root', '--out'):
        parser.add_argument(name, required=True)
    parser.add_argument('--keys-sha256')
    return parser


def main(argv=None) -> int:  # pylint: disable=too-many-locals
    wall_start = time.monotonic()
    args = _parser().parse_args(argv)
    keys_sha256, verdict, code = args.keys_sha256 or '-', '-', 'OK'
    try:
        code_root, run_dir, out = prerequisites(args)
        if args.mode != 'freeze' and not args.keys_sha256:
            raise Stop('PREREQUISITE', '--keys-sha256 is required')
        if args.mode == 'run' and (out / 'run').exists():
            raise Stop('PREREQUISITE', 'a run output already exists; run is once only')
        isolate_bytecode()
        m = _modules(code_root)
        params = json.loads(Path(args.authority).read_text(encoding='utf-8'))['parameters']
        try:
            by_key = retained(m, run_dir, params)
        except ValueError as exc:
            raise Stop('PREREQUISITE', f'retained evidence: {exc}') from None
        if args.mode == 'freeze':
            keys, available = select_keys(by_key.values(), m['canonical'])
            raw = keys_document(keys, available, m['canonical'])
            _write_once(out / 'keys.json', raw)
            keys_sha256, verdict = hashlib.sha256(raw).hexdigest(), 'FROZEN'
        else:
            keys = load_keys(m, out, args.keys_sha256, by_key)
            source = build_source(m, args)
            _check_origins(code_root)
            paths = assemble(m, source, run_dir, params, by_key, keys)
            if args.mode == 'selftest':
                verdict = 'SELFTEST_PASSED'
            else:
                verdict, code, done = run_paths(m, source, paths, keys, by_key, out, wall_start=wall_start)
                _check_origins(code_root)
                _write_once(out / 'run' / 'summary.json', json.dumps(
                    {'verdict': verdict, 'code': code, 'replayed': done, 'keys_sha256': args.keys_sha256},
                    sort_keys=True).encode())
    except Stop as stop:
        verdict, code = ('AMBIGUOUS' if args.mode == 'run' else 'STOPPED'), stop.code
        sys.stderr.write(f'{stop.code}: {stop}\n')
    except Exception as exc:  # pylint: disable=broad-exception-caught  # unclassified = a driver defect
        verdict, code = ('AMBIGUOUS' if args.mode == 'run' else 'STOPPED'), 'DRIVER_DEFECT'
        sys.stderr.write(f'DRIVER_DEFECT: {type(exc).__name__}: {exc}\n')
    print(f'T00_TIER1 {args.mode} {verdict} {code} keys_sha256={keys_sha256}')
    return 0 if code == 'OK' else 3


if __name__ == '__main__':
    raise SystemExit(main())
