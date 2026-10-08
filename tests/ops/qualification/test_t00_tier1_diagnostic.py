"""scripts/t00_tier1_diagnostic.py (T00 step-12 diagnostic, Tier 1 card §0.5, §3, §5, §6).

Synthetic fixtures only; no real source is read. The load-bearing claims:
- identities computed from a sealed ``replay_bracket`` run equal the ones the screen worker
  wrote from the raw run, so a replay mismatch is a non-reproduction, not a driver defect;
- every stop path (budget, checkpoint, mismatch, replay exception, refusal, driver defect,
  prerequisites) maps to the card's code, and ``selftest`` never replays.
"""
from __future__ import annotations

import ast
from datetime import date, datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from c1_rail.qualification import p7_evidence
from c1_rail.qualification.contract import ContractValidationError, canonical_json_bytes as canonical
from c1_rail.qualification.model import LEG_IDS, EdgeState, PathOutcome, ReplayEvent, ReplayResult, SessionRecord
from c1_rail.qualification.production_source import SourceOnlyBracket, _consumed_splits, _seal
from c1_rail.qualification.t00_screen import worker

SCRIPT = Path(__file__).resolve().parents[3] / 'scripts' / 't00_tier1_diagnostic.py'
CONTRACT = SimpleNamespace(evidence_class='T00_STEP3_SCREEN', contract_sha256='0' * 64,
                           approval=SimpleNamespace(approval_sha256='1' * 64))


@pytest.fixture(name='driver')
def _driver():
    spec = importlib.util.spec_from_file_location('t00_tier1_diagnostic', SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _edge(held=0):
    positions = tuple((leg, held if i == 0 else 0) for i, leg in enumerate(LEG_IDS))
    zeros = tuple((leg, 0) for leg in LEG_IDS)
    return EdgeState(positions, zeros, zeros)


def _result(pnl=125.5):
    sessions = (
        SessionRecord(0, date(2022, 9, 1), 's-a', pnl, -40.25, 3, True, _edge(), _edge(1)),
        SessionRecord(1, date(2022, 9, 2), 's-b', -0.1, -310.0, 0, False, _edge(1), _edge()),
    )
    events = (ReplayEvent(datetime(2022, 9, 1, 10, 7), 'fill', LEG_IDS[0], '{"qty":1}'),
              ReplayEvent(datetime(2022, 9, 2, 15, 0), 'session_mode', '', 'normal'))
    return ReplayResult(sessions, events)


PROVIDER = SimpleNamespace(_placed=[(1, LEG_IDS[1], datetime(2022, 9, 2, 10, 7, 30)),
                                    (0, LEG_IDS[0], datetime(2022, 9, 1, 9, 45)),  # grid instant: not a split
                                    (0, LEG_IDS[2], datetime(2022, 9, 1, 11, 3))])


def _sealed(pnl=125.5, failed=False):
    run = _seal(CONTRACT, _result(pnl), provider=PROVIDER, deadline_failure=failed)
    return SourceOnlyBracket(run, run)


# ---- fidelity --------------------------------------------------------------------------------

@pytest.mark.parametrize('failed', [False, True])
def test_sealed_identity_equals_worker_projection(driver, failed):
    result = _result()
    sealed = _seal(CONTRACT, result, provider=PROVIDER, deadline_failure=failed)
    outcome = PathOutcome('PASS', 1, None, (('kernel_outcome', 'pass'),))
    expected = worker.run_projection(result, failed, _consumed_splits(PROVIDER), outcome)
    got = driver.sealed_identity(sealed, p7_evidence.canonical, p7_evidence.sha256_bytes)
    assert {field: expected[field] for field in got} == got
    assert set(got) == set(driver.COMPARED)


def test_sealed_identity_detects_a_planted_divergence(driver):
    outcome = PathOutcome('PASS', 1, None, (('kernel_outcome', 'pass'),))
    expected = worker.run_projection(_result(), False, _consumed_splits(PROVIDER), outcome)
    planted = _seal(CONTRACT, _result(pnl=125.5000001), provider=PROVIDER, deadline_failure=False)
    got = driver.sealed_identity(planted, p7_evidence.canonical, p7_evidence.sha256_bytes)
    assert got['digest'] != expected['digest'] and got['events_sha256'] == expected['events_sha256']


def test_mismatches_names_each_differing_field(driver):
    runs = {name: {field: 0 for field in driver.COMPARED} for name in ('r1', 'r2')}
    replayed = {name: dict(fields) for name, fields in runs.items()}
    assert driver.mismatches(runs, replayed) == []
    replayed['r2']['events_sha256'] = 1
    assert driver.mismatches(runs, replayed) == ['r2.events_sha256']


# ---- selection and the frozen key list -------------------------------------------------------

def _outcome(root, population, index, status):
    return {'key': [root, population, index], 'bracket_status': status}


def _outcomes(driver):
    rows = [_outcome(r, p, i, 'PASS') for r in ('a', 'b') for p in ('FULL', 'H1') for i in range(3)]
    rows += [_outcome('a', 'FULL', 10 + i, 'FAILURE') for i in range(5)]
    rows += [_outcome('a', 'H1', 20, 'UNDETERMINED'), _outcome('a', 'FULL', 30, 'UNRESOLVED')]
    return rows


def test_select_keys_rule(driver):
    keys, available = driver.select_keys(_outcomes(driver), canonical)
    by_hash = sorted([('a', 'FULL', 10 + i) for i in range(5)],
                     key=lambda k: hashlib.sha256(canonical(list(k))).hexdigest())
    assert keys[:2] == by_hash[:2]                                # checkpoint stratum first, hash order
    assert ('a', 'H1', 20) in keys                                # shortfall: all it has, no substitution
    assert all(k[1] != 'H2' for k in keys) and ('a', 'FULL', 30) not in keys
    assert available['H2|PASS'] == 0 and available['H1|UNDETERMINED'] == 1
    assert len(keys) == 7


def _m(driver):
    return {'canonical': canonical, 'parse': lambda raw, label: json.loads(raw),
            'p7_evidence': p7_evidence, 'ContractValidationError': ContractValidationError}


def test_load_keys_rederives_the_selection(driver, tmp_path):
    rows = _outcomes(driver)
    by_key = {tuple(r['key']): r for r in rows}
    keys, available = driver.select_keys(rows, canonical)
    good = driver.keys_document(keys, available, canonical)
    (tmp_path / 'keys.json').write_bytes(good)
    assert driver.load_keys(_m(driver), tmp_path, hashlib.sha256(good).hexdigest(), by_key) == keys
    with pytest.raises(driver.Stop) as wrong_hash:
        driver.load_keys(_m(driver), tmp_path, '0' * 64, by_key)
    tampered = driver.keys_document([keys[1], keys[0], *keys[2:]], available, canonical)
    (tmp_path / 'keys.json').write_bytes(tampered)
    with pytest.raises(driver.Stop) as reordered:
        driver.load_keys(_m(driver), tmp_path, hashlib.sha256(tampered).hexdigest(), by_key)
    assert wrong_hash.value.code == reordered.value.code == 'PREREQUISITE'


def test_outputs_are_create_once(driver, tmp_path):
    driver._write_once(tmp_path / 'k' / 'keys.json', b'x')
    with pytest.raises(FileExistsError):
        driver._write_once(tmp_path / 'k' / 'keys.json', b'y')


# ---- run_paths: budget, checkpoint, mismatch, exceptions --------------------------------------

class _Source:
    def __init__(self, results):
        self.results, self.calls = list(results), 0

    def replay_bracket(self, path):
        self.calls += 1
        outcome = self.results.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


class _Clock:
    """Each replay advances CPU and wall by the next step (cpu, wall); a number means both."""

    def __init__(self, start=0.0, steps=(10.0,)):
        self.cpu = self.wall = start
        self.steps = [s if isinstance(s, tuple) else (s, s) for s in steps]

    def process_time(self):
        return self.cpu

    def monotonic(self):
        return self.wall

    def tick(self, source):
        original = source.replay_bracket

        def replay(path):
            cpu, wall = self.steps.pop(0) if len(self.steps) > 1 else self.steps[0]
            self.cpu, self.wall = self.cpu + cpu, self.wall + wall
            return original(path)
        source.replay_bracket = replay
        return source

def _retained(driver, n):
    runs = {name: driver.sealed_identity(getattr(_sealed(), name), p7_evidence.canonical, p7_evidence.sha256_bytes)
            for name in ('r1', 'r2')}
    keys = [('a', 'FULL', i) for i in range(n)]
    return keys, {k: {'runs': runs} for k in keys}


def _run(driver, monkeypatch, tmp_path, results, *, start=0.0, step=10.0, wall_start=0.0, steps=None):
    clock = _Clock(start, steps or (step,))
    monkeypatch.setattr(driver, 'time', clock)
    source = _Source(results)
    clock.tick(source)
    keys, by_key = _retained(driver, len(results))
    out = driver.run_paths(_m(driver), source, ['p'] * len(keys), keys, by_key, tmp_path, wall_start=wall_start)
    return out, source


def test_all_match_is_resolved(driver, monkeypatch, tmp_path):
    (verdict, code, done), source = _run(driver, monkeypatch, tmp_path, [_sealed(), _sealed(), _sealed()])
    assert (verdict, code, done, source.calls) == ('RESOLVED', 'OK', 3, 3)


def test_stops_at_the_first_mismatch(driver, monkeypatch, tmp_path):
    (verdict, code, done), source = _run(driver, monkeypatch, tmp_path, [_sealed(), _sealed(pnl=1.0), _sealed()])
    assert (verdict, code, done, source.calls) == ('FALSIFIED', 'NON_REPRODUCTION', 2, 2)


def test_a_replay_exception_is_non_reproduction(driver, monkeypatch, tmp_path):
    (verdict, code, done), _ = _run(driver, monkeypatch, tmp_path, [_sealed(), ValueError('engine legality')])
    assert (verdict, code, done) == ('FALSIFIED', 'NON_REPRODUCTION', 1)


@pytest.mark.parametrize('refusal', [ContractValidationError('SOURCE_APPROVAL_EXPIRED: lapsed'),
                                     ValueError('path contains a source session outside retained covered panel')])
def test_a_source_gate_refusal_is_refused(driver, monkeypatch, tmp_path, refusal):
    (verdict, code, done), _ = _run(driver, monkeypatch, tmp_path, [refusal])
    assert (verdict, code, done) == ('AMBIGUOUS', 'REFUSED', 0)


def test_budget_is_checked_before_each_path_from_driver_start(driver, monkeypatch, tmp_path):
    """CPU already spent before run_paths (build, self-test) counts: no path may start past the ceiling."""
    (verdict, code, done), source = _run(driver, monkeypatch, tmp_path, [_sealed(), _sealed()],
                                         start=driver.CPU_CEILING_S - 15.0, step=10.0)
    assert (verdict, code, done, source.calls) == ('AMBIGUOUS', 'BUDGET', 1, 1)


def test_wall_budget_counts_from_main(driver, monkeypatch, tmp_path):
    (verdict, code, done), source = _run(driver, monkeypatch, tmp_path, [_sealed()], start=100.0,
                                         wall_start=100.0 - driver.WALL_CEILING_S - 1.0)
    assert (verdict, code, done, source.calls) == ('AMBIGUOUS', 'BUDGET', 0, 0)


def test_an_overrun_on_the_last_path_is_not_resolved(driver, monkeypatch, tmp_path):
    (verdict, code, done), source = _run(driver, monkeypatch, tmp_path, [_sealed(), _sealed()], steps=(200.0, 7201.0))
    assert (verdict, code, done, source.calls) == ('AMBIGUOUS', 'BUDGET', 2, 2)


def test_the_wall_prediction_uses_wall_cost(driver, monkeypatch, tmp_path):
    wall = driver.WALL_CEILING_S / 2 + 1.0
    (verdict, code, done), source = _run(driver, monkeypatch, tmp_path, [_sealed(), _sealed()], steps=((1.0, wall),))
    assert (verdict, code, done, source.calls) == ('AMBIGUOUS', 'BUDGET', 1, 1)


def test_checkpoint_stop_after_an_expensive_first_path(driver, monkeypatch, tmp_path):
    (verdict, code, done), source = _run(driver, monkeypatch, tmp_path, [_sealed(), _sealed()],
                                         step=driver.CHECKPOINT_CPU_S + 1.0)
    assert (verdict, code, done, source.calls) == ('AMBIGUOUS', 'BUDGET', 1, 1)


# ---- assemble: the no-replay self-test --------------------------------------------------------

def _assemble_m(driver, run_dir, prepared):
    m = _m(driver)
    m['journal'] = SimpleNamespace(read=lambda path, prev_sha256: (
        {'type': 'PREPARED', 'body': {'manifest_sha256': prepared}},), record_sha256=lambda record: 'r')
    m['plan'] = SimpleNamespace(rebuild_candidates=lambda *a, **k: {'FULL': 'cands'},
                                seed=lambda **k: 7)
    m['PathAssembler'] = lambda start: SimpleNamespace(sample=lambda *a, **k: 'path')
    m['worker'] = SimpleNamespace(path_sha256=lambda path: 'h')
    return m


@pytest.fixture(name='run_dir')
def _run_dir(tmp_path):
    (tmp_path / 'ledger').mkdir()
    (tmp_path / 'ledger' / '0001.jsonl').write_bytes(b'')
    (tmp_path / 'manifest.json').write_bytes(b'{"populations": {}}')
    return tmp_path


def _assemble(driver, run_dir, record, prepared=None):
    prepared = prepared or hashlib.sha256((run_dir / 'manifest.json').read_bytes()).hexdigest()
    source = SimpleNamespace(sessions=(), path_start_date=date(2022, 9, 1))
    params = {'block': {'length_sessions': 5}, 'horizon_sessions': 1500}
    return driver.assemble(_assemble_m(driver, run_dir, prepared), source, run_dir, params,
                           {('a', 'FULL', 0): record}, [('a', 'FULL', 0)])


def test_assemble_matches_the_retained_record(driver, run_dir):
    assert _assemble(driver, run_dir, {'seed': 7, 'path_sha256': 'h'}) == ['path']


@pytest.mark.parametrize('record', [{'seed': 8, 'path_sha256': 'h'}, {'seed': 7, 'path_sha256': 'x'}])
def test_assemble_mismatch_is_a_driver_defect(driver, run_dir, record):
    with pytest.raises(driver.Stop) as stop:
        _assemble(driver, run_dir, record)
    assert stop.value.code == 'DRIVER_DEFECT'


def test_manifest_is_hash_checked_against_prepared(driver, run_dir):
    with pytest.raises(driver.Stop) as stop:
        _assemble(driver, run_dir, {'seed': 7, 'path_sha256': 'h'}, prepared='0' * 64)
    assert stop.value.code == 'PREREQUISITE'


# ---- main: code mapping, selftest never replays, once-only run --------------------------------

ARGS = ['--code-root', 'c', '--run-dir', 'r', '--authority', 'a', '--source-contract', 's',
        '--source-approval', 'p', '--registry', 'g', '--artifact-root', 't', '--out', 'o']


@pytest.fixture(name='staged')
def _staged(driver, monkeypatch, tmp_path):
    out = tmp_path / 'out'
    out.mkdir()
    authority = tmp_path / 'authority.json'
    authority.write_text(json.dumps({'parameters': {}}), encoding='utf-8')
    source, calls = _Source([_sealed()]), []
    monkeypatch.setattr(driver, 'prerequisites', lambda args: (tmp_path, tmp_path, out))
    monkeypatch.setattr(driver, 'isolate_bytecode', lambda: None)
    monkeypatch.setattr(driver, '_modules', lambda code_root: _m(driver))
    monkeypatch.setattr(driver, '_check_origins', lambda code_root: None)
    monkeypatch.setattr(driver, 'retained', lambda m, run_dir, params: {})
    monkeypatch.setattr(driver, 'load_keys', lambda m, out, sha, by_key: [('a', 'FULL', 0)])
    monkeypatch.setattr(driver, 'build_source', lambda m, args: calls.append('build') or source)
    monkeypatch.setattr(driver, 'assemble', lambda *a: ['path'])
    args = [a if a != 'a' else str(authority) for a in ARGS]
    return SimpleNamespace(out=out, source=source, calls=calls, args=args)


def test_selftest_never_replays(driver, staged, capsys):
    assert driver.main(['selftest', *staged.args, '--keys-sha256', 'k']) == 0
    assert staged.source.calls == 0 and staged.calls == ['build']
    assert capsys.readouterr().out.strip() == 'T00_TIER1 selftest SELFTEST_PASSED OK keys_sha256=k'


def test_run_refuses_an_existing_run_output_before_building(driver, staged, capsys):
    (staged.out / 'run').mkdir()
    assert driver.main(['run', *staged.args, '--keys-sha256', 'k']) == 3
    assert staged.calls == [] and staged.source.calls == 0
    assert capsys.readouterr().out.strip() == 'T00_TIER1 run AMBIGUOUS PREREQUISITE keys_sha256=k'


def test_the_reservation_survives_a_failure_and_blocks_a_second_run(driver, staged, monkeypatch, capsys):
    def refuse(m, args):
        staged.calls.append('build')
        raise driver.Stop('REFUSED', 'SOURCE_APPROVAL_EXPIRED')
    monkeypatch.setattr(driver, 'build_source', refuse)
    assert driver.main(['run', *staged.args, '--keys-sha256', 'k']) == 3
    assert (staged.out / 'run' / 'RESERVED').is_file()
    assert driver.main(['run', *staged.args, '--keys-sha256', 'k']) == 3
    assert staged.calls == ['build'] and staged.source.calls == 0
    assert capsys.readouterr().out.strip().splitlines()[-1] == 'T00_TIER1 run AMBIGUOUS PREREQUISITE keys_sha256=k'


def test_main_maps_stops_and_defects(driver, staged, monkeypatch, capsys):
    assert driver.main(['selftest', *staged.args]) == 3                       # no --keys-sha256
    assert capsys.readouterr().out.strip().endswith('STOPPED PREREQUISITE keys_sha256=-')
    monkeypatch.setattr(driver, 'assemble', lambda *a: (_ for _ in ()).throw(KeyError('bug')))
    assert driver.main(['run', *staged.args, '--keys-sha256', 'k']) == 3
    assert capsys.readouterr().out.strip() == 'T00_TIER1 run AMBIGUOUS DRIVER_DEFECT keys_sha256=k'


# ---- prerequisites, bytecode, module origin ---------------------------------------------------

def test_prerequisites(driver, monkeypatch, tmp_path):
    files = {}
    for name in driver.PINS:
        files[name] = tmp_path / f'{name}.bin'
        files[name].write_bytes(name.encode())
    run_dir, out = tmp_path / 'run', tmp_path / 'out'
    run_dir.mkdir()
    (run_dir / 'results.json').write_bytes(b'r')
    (run_dir / 'attestation.json').write_bytes(b'a')
    monkeypatch.setattr(driver, 'PINS', {n: hashlib.sha256(n.encode()).hexdigest() for n in driver.PINS})
    monkeypatch.setattr(driver, 'RESULTS_SHA256', hashlib.sha256(b'r').hexdigest())
    monkeypatch.setattr(driver, 'ATTESTATION_SHA256', hashlib.sha256(b'a').hexdigest())
    state = {'HEAD': driver.H, 'dirty': ''}
    monkeypatch.setattr(driver, '_git', lambda root, *a: state['HEAD'] if a[0] == 'rev-parse' else state['dirty'])
    args = SimpleNamespace(code_root=tmp_path / 'code', run_dir=run_dir, out=out,
                           **{name: path for name, path in files.items()})
    assert driver.prerequisites(args)[2] == out.resolve()
    for change in ({'HEAD': '0' * 40}, {'dirty': '?? x'}):
        monkeypatch.setitem(state, *next(iter(change.items())))
        with pytest.raises(driver.Stop):
            driver.prerequisites(args)
        state.update({'HEAD': driver.H, 'dirty': ''})
    with pytest.raises(driver.Stop):
        driver.prerequisites(SimpleNamespace(**{**vars(args), 'out': run_dir / 'inside'}))
    files['registry'].write_bytes(b'changed')
    with pytest.raises(driver.Stop):
        driver.prerequisites(args)
    files['registry'].write_bytes(b'registry')
    (run_dir / 'attestation.json').write_bytes(b'tampered')
    with pytest.raises(driver.Stop):
        driver.prerequisites(args)


def test_isolate_bytecode(driver, monkeypatch):
    monkeypatch.setattr(sys, 'dont_write_bytecode', False)
    monkeypatch.setattr(sys, 'pycache_prefix', None)
    driver.isolate_bytecode()
    assert sys.dont_write_bytecode is True
    assert Path(sys.pycache_prefix).is_dir() and not any(Path(sys.pycache_prefix).iterdir())


def test_watchdog_stops_on_a_breach_during_replay(driver):
    import threading
    breaches, done = [], threading.Event()
    clock = SimpleNamespace(process_time=lambda: driver.CPU_CEILING_S + 1.0, monotonic=lambda: 0.0)
    driver.watchdog(0.0, done, lambda: breaches.append(1), interval=0, clock=clock)
    assert breaches == [1]
    calls = []
    quiet = SimpleNamespace(process_time=lambda: calls.append(1) or (done.set() if len(calls) > 2 else None) or 0.0,
                            monotonic=lambda: 0.0)
    done.clear()
    driver.watchdog(0.0, done, lambda: breaches.append(2), interval=0, clock=quiet)
    assert breaches == [1]


def _retained_m(driver, heads, ledger):
    def read(path, prev_sha256):
        name = Path(path).name
        return tuple(ledger) if name == '0001.jsonl' else ({'type': 'PATH', 'body': {}, 'file': name},)
    return {'journal': SimpleNamespace(read=read, record_sha256=lambda r: heads.get(r.get('file')) or r['sha'],
                                       outcomes=lambda journals, keys: [{'key': list(k)} for k in keys]),
            'plan': SimpleNamespace(key_universe=lambda roots, depth: [('a', 'FULL', 0)], plan_sha256=lambda keys: 'p'),
            'verdict': SimpleNamespace(evaluate=lambda *a: None, as_json=lambda v: {})}


def _ledger(driver):
    return [{'type': 'PREPARED', 'sha': 'P', 'body': {'manifest_sha256': 'm'}},
            {'type': 'REPORTED', 'sha': 'L', 'body': {}},
            {'type': 'FINAL', 'sha': 'F', 'body': {'attestation_sha256': driver.ATTESTATION_SHA256}},
            {'type': 'VERIFY_START', 'sha': 'V0', 'body': {}}, {'type': 'VERIFY', 'sha': 'V1', 'body': {}}]


@pytest.mark.parametrize('tamper', [None, 'journal_head', 'ledger_head', 'final', 'trailing', 'results'])
def test_retained_is_bound_to_the_attestation(driver, tmp_path, tamper):
    for sub in ('journal', 'ledger'):
        (tmp_path / sub).mkdir()
    (tmp_path / 'journal' / 's1-w0.jsonl').write_bytes(b'')
    (tmp_path / 'ledger' / '0001.jsonl').write_bytes(b'')
    (tmp_path / 'results.json').write_text(json.dumps({'plan_sha256': 'p', 'verdict': {}}), encoding='utf-8')
    attestation = {'results_sha256': driver.RESULTS_SHA256, 'ledger_head_sha256': 'L',
                   'journal_heads': {'c1-w0.jsonl': 'c', 's1-w0.jsonl': 'J', 'v1-w0.jsonl': 'v'}}
    heads, ledger = {'s1-w0.jsonl': 'J'}, _ledger(driver)
    if tamper == 'journal_head':
        heads['s1-w0.jsonl'] = 'rechained'
    elif tamper == 'ledger_head':
        attestation['ledger_head_sha256'] = 'P'                  # a real record, but not REPORTED
    elif tamper == 'final':
        ledger[2]['body']['attestation_sha256'] = '0' * 64
    elif tamper == 'trailing':
        ledger.append({'type': 'SEGMENT_START', 'sha': 'X', 'body': {}})
    elif tamper == 'results':
        attestation['results_sha256'] = '0' * 64
    (tmp_path / 'attestation.json').write_text(json.dumps(attestation), encoding='utf-8')
    params = {'rng': {'roots': ['a']}, 'depth_per_root': {}}
    m = _retained_m(driver, heads, ledger)
    if tamper is None:
        assert list(driver.retained(m, tmp_path, params)) == [('a', 'FULL', 0)]
    else:
        with pytest.raises(driver.Stop) as stop:
            driver.retained(m, tmp_path, params)
        assert stop.value.code == 'PREREQUISITE'

def test_foreign_modules(driver, tmp_path):
    code, lib, other = tmp_path / 'code', tmp_path / 'lib', tmp_path / 'other'
    modules = {'ok': SimpleNamespace(__file__=str(code / 'ops' / 'm.py')),
               'std': SimpleNamespace(__file__=str(lib / 'json.py')),
               'builtin': SimpleNamespace(),
               'stray': SimpleNamespace(__file__=str(other / 'ops' / 'm.py'))}
    assert driver.foreign_modules(code, (lib,), modules) == ['stray']


def test_imports_nothing_outside_the_standard_library_at_module_level():
    """The H modules are imported only by _modules(code_root), after the code root is on sys.path."""
    tree = ast.parse(SCRIPT.read_text(encoding='utf-8'))
    top = [node for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
    names = {alias.name.split('.')[0] for node in top for alias in node.names} | {
        (node.module or '').split('.')[0] for node in top if isinstance(node, ast.ImportFrom)}
    assert not names & {'c1_rail', 'mc', 'core', 'ops'}
