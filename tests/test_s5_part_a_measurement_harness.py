"""Regression tests for the S5 Part A measurement harness (H1 step (b), PR #526).

Allowed by the H1 dispatch record's amendment of 2026-09-27 (r2 §12.9). Synthetic
inputs only: hand-written rows, unit files and bundles, and the workflow's own
step scripts run against stubbed system commands. No engine workload, measurement,
private read, vendor data, network, dispatch or artifact download; nothing is
imported from lab/. The harness is loaded from its .py.txt path; its module level
is standard library only.

S5PA_HARNESS_ROOT (optional) points the suite at another checkout's harness,
README and workflow, which is how the before-state is recorded.
"""
# Pytest idioms: fixtures shadow outer names, tests are named not docstringed, the
# harness's own %-format style is kept, and subprocess return codes are asserted.
# pylint: disable=missing-function-docstring,redefined-outer-name,consider-using-f-string,subprocess-run-check
import copy
import importlib.machinery
import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(os.environ.get('S5PA_HARNESS_ROOT') or Path(__file__).resolve().parents[1]).resolve()
NOTE = ROOT / 'docs/notes/2026-09-27-s5-part-a-measurement'
HARNESS = NOTE / 'measure_part_a_max.py.txt'


@pytest.fixture
def h(monkeypatch):
    loader = importlib.machinery.SourceFileLoader('s5pa_harness_under_test', str(HARNESS))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    # code identity would import ops modules; synthetic tests pin it empty.
    monkeypatch.setattr(module, '_code_identity', lambda: ({'worker_runtime': {'python_version': 'x'}}, set()))
    # git is pinned so records do not depend on this worktree's state.
    monkeypatch.setattr(module, '_git', lambda *args: {'rev-parse': HEAD, 'status': ''}[args[0]])
    return module


HEAD = 'c' * 40
ARM_ORDER = ('forced', 'prescribed')
PANELS = {'forced': (4, True), 'prescribed': (2, False)}
PREFIX = 'p' * 64
FINAL = {'forced': 'f' * 64, 'prescribed': PREFIX}


COUNTS = {'forced': {'replay': 14, 'proof': 5, 'verify_for': 15},
          'prescribed': {'replay': 8, 'proof': 3, 'verify_for': 9}}      # r2 §4
WORKLOAD = {'initial_panels': 2, 'expanded_panels': 4, 'paths_per_panel': 2, 'horizon_sessions': 5,
            'inner_block_sessions': 5, 'outer_months': 6, 'budget_seconds': 3600.0, 'full_pass_rate_input': 1.0,
            'idle': False, 'fixture': 'tests/ops/qualification/composition_fixture.py'}   # r2 §4, §6.3
THREADS = {name: '1' for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                                  'NUMEXPR_NUM_THREADS')}


def _row(arm, repeat, *, stage='1b', dry_run=False, unit=None):
    panels, expanded = PANELS[arm]
    instrumented = repeat == 0 or dry_run
    return {
        'row_schema': 'x', 'stage': stage, 'arm': arm, 'repeat': repeat, 'unit': unit,
        'cold': repeat == 1 and not dry_run, 'instrumented': instrumented, 'dry_run': dry_run,
        'cpu': {'start': 0.5, 'admission': 1.0, 'setup_excluded': 10.0, 'verify': 1.0, 'part_a': 20.0,
                'serialize': 0.1, 'adapter': None, 'workload': 22.6, 'process_total': 33.0},
        'wall': {'outer': None, 'setup_excluded': 11.0, 'workload': None,
                 'boundaries': {'admission': 1.0, 'verify': 1.0, 'part_a': 21.0, 'serialize': 0.1}},
        'panels': panels, 'expanded': expanded, 'probe_seconds': 1.0, 'predicted_seconds': 30.0,
        'elapsed_seconds': 21.0, 'counts': dict(COUNTS[arm]) if instrumented else None,
        'initial_prefix_sha256': PREFIX, 'final_sha256': FINAL[arm], 'fsync_count': None,
        'assertions': {'expected_panels': panels, 'expected_expanded': expanded, 'ok': True},
        # `expected` is what a real row derives from its own request (the real fixture gives the r2
        # literals); the harness records it but judges counts against its fixed table only.
        'workload': {'arm': arm, 'within_pp': 1.0 if arm == 'forced' else 0.01, **WORKLOAD,
                     'expected': {'panels': panels, 'expanded': expanded, 'replays': COUNTS[arm]['replay'],
                                  'proofs': COUNTS[arm]['proof'], 'verify_for': COUNTS[arm]['verify_for']}},
        'memory': {'lower_bound_bytes': 100_000_000, 'lower_bound_method': 'lower_bound_ru_maxrss',
                   'swap_total_kb': 0, 'cgroup_path': '/system.slice/%s.service' % unit,
                   'cgroup_path_matches_unit': True, 'in_unit_peak_bytes': 120_000_000, 'swap_max': '0',
                   'swap_peak_bytes': 0, 'oom_events': 0, 'cgroup_cpu_usage_usec': 1},
        'environment': {'python': '3.11', 'implementation': 'CPython', 'executable': None,
                        'thread_env': dict(THREADS), 'loaded_fixture_files': []},
        'exit_status': 0,
    }


def _unit_text(*, exit_ts=True, cold=False):
    lines = ['CPUUsageNSec=34000000000', 'MemoryPeak=121000000', 'MemorySwapPeak=0', 'ExecMainStatus=0',
             'ControlGroup=/system.slice/x.service', 'ExecMainStartTimestampMonotonic=1000000',
             'Result=success', 'HarnessPollTimeout=no', 'HarnessPollBoundS=1800']
    if cold:
        lines.append('HarnessColdPrep=done')
    lines.append('ExecMainExitTimestampMonotonic=%d' % (35_000_000 if exit_ts else 0))
    return '\n'.join(lines) + '\n'


def _linux_job(directory, *, arm_order=ARM_ORDER, exit_ts=True):
    directory.mkdir(parents=True)
    for arm in arm_order:
        for repeat in (1, 2, 3, 4, 5, 0):
            unit = 'fp-s5pa-1b-%s-%d' % (arm, repeat)
            (directory / ('%s-%d.json' % (arm, repeat))).write_text(json.dumps(_row(arm, repeat, unit=unit)))
            (directory / ('%s-%d.unit' % (arm, repeat))).write_text(_unit_text(exit_ts=exit_ts, cold=repeat == 1))
    (directory / 'probe.json').write_text(json.dumps({'ok': True, 'swap_total_kb': 0, 'reasons': []}))
    (directory / 'git-head.txt').write_text(HEAD + '\n')
    return directory


def _summarize_job(h, directory, *, job='a', run_id='42', arm_order=ARM_ORDER, extra=()):
    argv = ['--summarize', str(directory), '--stage', '1b', '--mode', 'measure', '--job', job,
            '--run-id', run_id, '--run-attempt', '1', '--arm-order', ' '.join(arm_order),
            '--dispatched-head', HEAD, *extra]
    code = h.main(argv)
    return code, json.loads((directory / 'record.json').read_text())


# ---------------------------------------------------------------- baseline

def test_baseline_synthetic_job_is_valid_and_applicable(h, tmp_path):
    code, record = _summarize_job(h, _linux_job(tmp_path / 'a'))
    assert record['verdict']['validity_ok'] is True
    assert record['verdict']['rule_applicable'] is True
    assert code == 0


# ------------------------------------------- finding 1 (4116641275): Ĉ/Ŵ/P̂ required

def test_missing_wall_timestamp_is_not_rule_applicable(h, tmp_path):
    code, record = _summarize_job(h, _linux_job(tmp_path / 'a', exit_ts=False))
    assert record['summary']['estimates']['W_hat_s'] is None
    assert record['verdict']['rule_applicable'] is False
    assert any('ceiling input' in reason for reason in record['verdict']['reasons'])


def test_one_missing_wall_repeat_does_not_yield_a_subset_maximum(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    (directory / 'forced-3.unit').write_text(_unit_text(exit_ts=False))
    code, record = _summarize_job(h, directory)
    assert record['verdict']['rule_applicable'] is False


# ------------------------------------------- finding 5 (4116641299): truncated Linux row

def test_truncated_linux_row_is_retained_as_i6(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    (directory / 'forced-3.json').write_text('{"row_schema": "x", "cpu": {"start"')
    code, record = _summarize_job(h, directory)
    rep = next(r for r in record['repeats'] if r['arm'] == 'forced' and r['repeat'] == 3)
    assert rep['row_present'] is False
    assert 'unreadable row' in rep['error']
    assert any(reason.startswith('I-6: forced-3') and 'unreadable row' in reason
               for reason in record['verdict']['reasons'])
    assert record['verdict']['stop_class'] == 'INVALID_MEASUREMENT'
    assert code == 3


# ------------------------------------------- finding 2 (4116641285): combine inputs

def _receipt(directory, *, job, run_id='42', run_attempt='1', cleanup_exit=0):
    (directory / 'cleanup-receipt.json').write_text(json.dumps({
        'schema': 's5-part-a-max-expansion-measurement/v2#cleanup-receipt', 'cleanup_exit': cleanup_exit,
        'run_id': run_id, 'run_attempt': run_attempt, 'job': job}))


def _two_jobs(h, tmp_path, *, run_b='42'):
    _, _ = _summarize_job(h, _linux_job(tmp_path / 'a'), job='a')
    _, _ = _summarize_job(h, _linux_job(tmp_path / 'b', arm_order=('prescribed', 'forced')), job='b',
                          run_id=run_b, arm_order=('prescribed', 'forced'))
    _receipt(tmp_path / 'a', job='a')
    _receipt(tmp_path / 'b', job='b', run_id=run_b)
    return tmp_path / 'a' / 'record.json', tmp_path / 'b' / 'record.json'


def test_combine_accepts_one_a_and_one_b_of_one_run(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    code = h.main(['--summarize', str(a), str(b), '--record', str(tmp_path / 'combined.json')])
    record = json.loads((tmp_path / 'combined.json').read_text())
    assert record['verdict']['validity_ok'] is True and record['verdict']['rule_applicable'] is True
    assert code == 0


def test_combine_refuses_the_same_job_record_twice(h, tmp_path):
    a, _ = _two_jobs(h, tmp_path)
    with pytest.raises(SystemExit) as refused:
        h.main(['--summarize', str(a), str(a), '--record', str(tmp_path / 'combined.json')])
    assert 'job' in str(refused.value.code)
    assert not (tmp_path / 'combined.json').exists()


def test_combine_refuses_jobs_from_different_runs(h, tmp_path):
    a, b = _two_jobs(h, tmp_path, run_b='43')
    with pytest.raises(SystemExit) as refused:
        h.main(['--summarize', str(a), str(b), '--record', str(tmp_path / 'combined.json')])
    assert 'run' in str(refused.value.code)
    assert not (tmp_path / 'combined.json').exists()


def test_combine_marks_mismatched_code_identity_i7(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    other = json.loads(b.read_text())
    other['harness_sha256'] = '0' * 64
    b.write_text(json.dumps(other))
    code = h.main(['--summarize', str(a), str(b), '--record', str(tmp_path / 'combined.json')])
    record = json.loads((tmp_path / 'combined.json').read_text())
    assert any(reason.startswith('I-7') and 'harness_sha256' in reason for reason in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 4


# ------------------------------------------- finding 3 (4116641294): README launcher form

def test_readme_combine_command_uses_the_operations_launcher():
    text = (NOTE / 'README.md').read_text(encoding='utf-8')
    lines = [line.strip() for line in text.splitlines() if '--record <combined>' in line]
    assert lines, 'README combine command not found'
    for line in lines:
        assert line.startswith(('python -I scripts/fp.py python ', r'.\fp.ps1 python ')), line


# ------------------------------------------- Windows bundles (findings 4 and 6)

def _launcher_unit(repeat):
    return {'pid': 1, 'exit_code': 0, 'timed_out': False, 'outer_wall_s': 35.0, 'job_cpu_s': 34.0,
            'job_processes': 1, 'job_peak_process_commit_bytes': 1, 'job_peak_commit_bytes': 1,
            'pycache_dirs_purged': 3 if repeat == 1 else None, 'purge_failed_dirs': [] if repeat == 1 else None}


def _bundle(h, path, *, arms=ARM_ORDER, repeats=5, identity='current'):
    entries = []
    for arm in arms:
        for repeat in [*range(1, repeats + 1), 0]:
            row = _row(arm, repeat, stage='1a')
            row['memory'] = {'lower_bound_bytes': 100_000_000,
                             'lower_bound_method': 'lower_bound_windows_working_set', 'swap_total_kb': None}
            entries.append({'arm': arm, 'repeat': repeat, 'row': row, 'unit': _launcher_unit(repeat)})
    bundle = {'schema': h.BUNDLE_SCHEMA, 'artifact_class': h.ARTIFACT_CLASS, 'decision_bearing': False,
              'stage': '1a', 'mode': 'measure', 'platform_accounting': 'windows_process_time_job_object',
              'arm_order': list(arms), 'timed_repeats': repeats, 'timeout_s': 1800.0, 'recorded_utc': 'x',
              'harness_sha256': h._sha256_file(h.HARNESS), 'entries': entries}
    if identity == 'current' and hasattr(h, '_executed_identity'):
        bundle['executed_identity'] = h._executed_identity([e['row'] for e in entries])
    elif isinstance(identity, dict):
        bundle['executed_identity'] = identity
    path.write_text(json.dumps(bundle))
    return path


def _summarize_bundle(h, path):
    code = h.main(['--summarize', str(path), '--stage', '1a'])
    return code, json.loads(path.with_suffix('.record.json').read_text())


def test_conforming_bundle_summarizes_valid(h, tmp_path):
    code, record = _summarize_bundle(h, _bundle(h, tmp_path / 'windows.json'))
    assert record['verdict']['validity_ok'] is True, record['verdict']['reasons']
    assert code == 0


# finding 6 (4116641309): fixed Stage 1a shape

@pytest.mark.parametrize('arms, repeats', [(('forced',), 5), (ARM_ORDER, 2), (('prescribed',), 3)])
def test_nonconforming_bundle_shape_is_invalid(h, tmp_path, arms, repeats):
    code, record = _summarize_bundle(h, _bundle(h, tmp_path / 'windows.json', arms=arms, repeats=repeats))
    assert record['verdict']['validity_ok'] is False
    assert any(reason.startswith('H-SHAPE') for reason in record['verdict']['reasons'])
    assert code == 4


def test_linux_record_with_short_repeat_count_is_invalid(h, tmp_path):
    code, record = _summarize_job(h, _linux_job(tmp_path / 'a'), extra=('--repeats', '3'))
    assert record['verdict']['validity_ok'] is False
    assert record['verdict']['rule_applicable'] is False
    assert any(reason.startswith('H-SHAPE') for reason in record['verdict']['reasons'])


# finding 4 (4116641306): bundle bound to the executed code

def test_bundle_with_mismatched_executed_identity_is_rejected(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json', identity=None)
    bundle = json.loads(path.read_text())
    rows = [e['row'] for e in bundle['entries']]
    executed = h._executed_identity(rows) if hasattr(h, '_executed_identity') else {}
    executed = copy.deepcopy(executed)
    executed['harness_sha256'] = '0' * 64
    bundle['executed_identity'] = executed
    bundle['harness_sha256'] = '0' * 64
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(reason.startswith('I-7') and 'harness_sha256' in reason for reason in record['verdict']['reasons'])
    assert record['verdict']['validity_ok'] is False
    assert code == 4


def test_bundle_without_executed_identity_is_rejected(h, tmp_path):
    # r2 §12.9 (2): no executed_identity marks a legacy bundle (was I-7 before the ruling).
    code, record = _summarize_bundle(h, _bundle(h, tmp_path / 'windows.json', identity=None))
    assert record['verdict']['stop_class'] == 'LEGACY_UNACCEPTED'
    assert any(reason.startswith('LEGACY') and 'executed_identity' in reason
               for reason in record['verdict']['reasons'])
    assert code == 4


def test_bundle_with_changed_source_is_rejected(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    if 'executed_identity' not in bundle:
        pytest.fail('launcher bundle carries no executed identity')
    name = next(iter(bundle['executed_identity']['source_sha256']))
    bundle['executed_identity']['source_sha256'][name] = '0' * 64
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(reason.startswith('I-7') and name in reason for reason in record['verdict']['reasons'])
    assert code == 4


# =================================================================== round 2
# Codex re-review of c67166a8: 4116712133, 4116712135, 4116712138, 4116712131.



WORKFLOW = ROOT / '.github/workflows/qualification-s5-part-a-measurement.yml'


def _combine(h, a, b, tmp_path):
    return h.main(['--summarize', str(a), str(b), '--record', str(tmp_path / 'combined.json')])


# ------------------------------------- 4116712135: cleanup receipt required to combine

def test_combine_refuses_a_job_without_a_cleanup_receipt(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    (b.parent / 'cleanup-receipt.json').unlink()
    with pytest.raises(SystemExit) as refused:
        _combine(h, a, b, tmp_path)
    assert 'cleanup receipt' in str(refused.value.code)
    assert not (tmp_path / 'combined.json').exists()


def test_combine_refuses_a_job_whose_cleanup_failed(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    _receipt(a.parent, job='a', cleanup_exit=1)
    with pytest.raises(SystemExit) as refused:
        _combine(h, a, b, tmp_path)
    assert 'cleanup' in str(refused.value.code)
    assert not (tmp_path / 'combined.json').exists()


def test_combine_refuses_a_receipt_from_another_attempt(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    _receipt(b.parent, job='b', run_attempt='2')
    with pytest.raises(SystemExit):
        _combine(h, a, b, tmp_path)
    assert not (tmp_path / 'combined.json').exists()


# ------------------------------------- 4116712138: combine bound to the executing revision

@pytest.mark.parametrize('key', ['harness_sha256', 'measured_commit', 'source'])
def test_combine_refuses_records_from_another_revision(h, tmp_path, key):
    a, b = _two_jobs(h, tmp_path)
    for path in (a, b):
        record = json.loads(path.read_text())
        if key == 'source':
            name = next(iter(record['source_sha256']))
            record['source_sha256'][name] = '0' * 64
        else:
            record[key] = '0' * (64 if key == 'harness_sha256' else 40)
        path.write_text(json.dumps(record))
    with pytest.raises(SystemExit) as refused:
        _combine(h, a, b, tmp_path)
    assert 'recorded revision' in str(refused.value.code)
    assert not (tmp_path / 'combined.json').exists()


# ------------------------------------- 4116712131: dirty Windows execution identity

@pytest.mark.parametrize('value', [False, None, 'missing'])
def test_bundle_with_dirty_or_unknown_execution_tree_is_rejected(h, tmp_path, value):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    if 'executed_identity' not in bundle:
        pytest.fail('launcher bundle carries no executed identity')
    if value == 'missing':
        bundle['executed_identity'].pop('tree_clean_tracked', None)
    else:
        bundle['executed_identity']['tree_clean_tracked'] = value
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(reason.startswith('I-7') and 'tree' in reason for reason in record['verdict']['reasons'])
    assert code == 4


# ------------------------------------- 4116712133: the loop leaves time to summarize

def _workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding='utf-8'))


def _timeout_min(job):
    """Resolve the job timeout from its single source (a one-valued matrix key)."""
    match = re.fullmatch(r'\$\{\{\s*matrix\.(\w+)\s*\}\}', str(job['timeout-minutes']))
    assert match, 'timeout-minutes is not single-sourced: %r' % job['timeout-minutes']
    values = job['strategy']['matrix'][match.group(1)]
    assert isinstance(values, list) and len(values) == 1, values   # one value: no extra job combinations
    return match.group(1), int(values[0])


def test_loop_budget_constant_matches_the_job_timeout():
    job = _workflow()['jobs']['measure']
    key, minutes = _timeout_min(job)
    assert minutes == 120                                               # r2 §12.3
    assert job['env']['JOB_TIMEOUT_MIN'] == '${{ matrix.%s }}' % key    # same source, not a second copy


STUBS = {
    'sudo': 'if [ "$1" = tee ]; then cat > /dev/null; exit 0; fi\nexec "$@"\n',
    'systemd-run': 'echo "$@" >> "$SIM/started.log"\n',
    # every unit hangs: never exited, never failed
    'systemctl': ('case "$1" in show) for a in "$@"; do [ "$a" = --value ] && { echo running; exit 0; }; done\n'
                  '  printf "CPUUsageNSec=1\\nExecMainStatus=\\nResult=success\\n" ;; *) exit 0 ;; esac\n'),
    # fake clock: date reads it; each poll sleep advances it by 60 s
    'date': 'if [ "$1" = +%s ]; then cat "$SIM/clock"; else exec /bin/date "$@"; fi\n',
    'sleep': 'echo $(( $(cat "$SIM/clock") + 60 )) > "$SIM/clock"\n',
}


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_hung_repeats_leave_the_post_loop_reserve(h, tmp_path):
    job = _workflow()['jobs']['measure']
    step = next(s for s in job['steps'] if s.get('name') == 'Measurement loop')
    sim = tmp_path / 'sim'
    (sim / 'bin').mkdir(parents=True)
    for name, body in STUBS.items():
        stub = sim / 'bin' / name
        stub.write_text('#!/bin/bash\n' + body)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    start = 1_000_000
    clock0 = start + 11 * 60      # r2 §12.6: provisioning 8 + checkout/doctor/probe 3 min before the loop
    (sim / 'clock').write_text(str(clock0))
    runner_temp = sim / 'rt'
    out = runner_temp / 's5-part-a-measurement'
    out.mkdir(parents=True)
    (sim / 'host').mkdir()
    (runner_temp / 'qualification-manifest').write_text(str(sim / 'host' / 'manifest'))
    (sim / 'ws').mkdir()
    env = {'PATH': '%s:/usr/bin:/bin' % (sim / 'bin'), 'SIM': str(sim), 'RUNNER_TEMP': str(runner_temp),
           'GITHUB_WORKSPACE': str(sim / 'ws'), 'STAGE': '1b', 'MODE': 'measure', 'NOTE_DIR': 'x',
           'ARM_ORDER': 'forced prescribed', 'JOB_START_EPOCH': str(start)}
    env.update({k: str(v) for k, v in job['env'].items() if '${{' not in str(v)})
    env['JOB_TIMEOUT_MIN'] = str(_timeout_min(job)[1])
    done = subprocess.run(['bash', '-c', step['run']], env=env, capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    elapsed_min = (int((sim / 'clock').read_text()) - start) / 60
    # The loop returns with at least 10 min of the 120 min job left for summarize,
    # cleanup (r2 §12.6 budgets 2 min for cleanup and upload) and upload.
    assert elapsed_min <= _timeout_min(job)[1] - 10, elapsed_min
    units = {p.stem: p.read_text() for p in out.glob('*.unit')}
    assert sorted(units) == sorted('%s-%d' % (a, r) for a in ('forced', 'prescribed') for r in (1, 2, 3, 4, 5, 0))
    assert any('HarnessNotStarted=loop-deadline' in text for text in units.values())
    # Every repeat is then summarized as retained I-6 evidence.
    (out / 'probe.json').write_text(json.dumps({'ok': True, 'swap_total_kb': 0, 'reasons': []}))
    (out / 'git-head.txt').write_text(HEAD + '\n')
    code = h.main(['--summarize', str(out), '--stage', '1b', '--mode', 'measure', '--job', 'a', '--run-id', '42',
                   '--arm-order', 'forced prescribed', '--dispatched-head', HEAD, '--run-attempt', '1'])
    record = json.loads((out / 'record.json').read_text())
    i6 = [reason for reason in record['verdict']['reasons'] if reason.startswith('I-6')]
    assert len(i6) == 12
    assert any('not-started' in reason for reason in i6)
    assert code == 3


# =================================================================== round 3
# Codex re-review of 1d2ab1f3: 4116766993 (start the deadline clock before checkout).

def test_job_clock_starts_in_the_first_step_before_checkout():
    steps = _workflow()['jobs']['measure']['steps']
    setters = [i for i, s in enumerate(steps) if 'JOB_START_EPOCH=' in (s.get('run') or '')]
    checkout = next(i for i, s in enumerate(steps) if str(s.get('uses', '')).startswith('actions/checkout@'))
    assert setters == [0], setters          # exactly one setter, and it is the first step
    assert setters[0] < checkout
    assert '"$GITHUB_ENV"' in steps[0]['run'] and 'date +%s' in steps[0]['run']


# =================================================================== round 4
# Codex re-review of 396eb9f2: 4116790816 (propagate transient-unit cleanup failures).

CLEANUP_STUBS = {
    'sudo': 'exec "$@"\n',
    # SIM_LIST_FAIL=1: the listing fails; SIM_STOP_FAIL=<unit>: stopping that unit fails
    'systemctl': ('case "$1" in\n'
                  '  list-units) [ "${SIM_LIST_FAIL:-0}" = 1 ] && exit 1\n'
                  '    printf "fp-s5pa-1b-forced-1.service loaded active exited x\\n'
                  'fp-s5pa-1b-forced-2.service loaded active exited x\\n" ;;\n'
                  '  stop) [ "$2" = "${SIM_STOP_FAIL:-}" ] && exit 1; echo "$2" >> "$SIM/stopped.log" ;;\n'
                  '  *) exit 0 ;;\nesac\n'),
    'journalctl': 'echo journal\n',
}


def _run_cleanup_step(tmp_path, **sim):
    job = _workflow()['jobs']['measure']
    step = next(s for s in job['steps'] if s.get('name') == 'Owned cleanup and journal export')
    root = tmp_path / 'sim'
    (root / 'bin').mkdir(parents=True)
    for name, body in CLEANUP_STUBS.items():
        stub = root / 'bin' / name
        stub.write_text('#!/bin/bash\n' + body)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    runner_temp = root / 'rt'     # no qualification-manifest: cleanup.py is never invoked
    runner_temp.mkdir()
    env = {'PATH': '%s:/usr/bin:/bin' % (root / 'bin'), 'SIM': str(root), 'RUNNER_TEMP': str(runner_temp),
           'GITHUB_RUN_ID': '42', 'GITHUB_RUN_ATTEMPT': '1', 'JOB': 'a', **sim}
    # GitHub's default bash for `run`: bash --noprofile --norc -eo pipefail {0}
    done = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', step['run']],
                          env=env, capture_output=True, text=True, timeout=60)
    receipt = json.loads((runner_temp / 's5-part-a-measurement' / 'cleanup-receipt.json').read_text())
    stopped = (root / 'stopped.log').read_text().split() if (root / 'stopped.log').exists() else []
    return done.returncode, receipt, stopped


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_owned_cleanup_success_writes_a_zero_receipt(tmp_path):
    code, receipt, stopped = _run_cleanup_step(tmp_path)
    assert (code, receipt['cleanup_exit']) == (0, 0)
    assert len(stopped) == 2


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_failed_unit_stop_makes_the_receipt_and_step_nonzero(tmp_path):
    code, receipt, stopped = _run_cleanup_step(tmp_path, SIM_STOP_FAIL='fp-s5pa-1b-forced-1.service')
    assert receipt['cleanup_exit'] != 0
    assert code != 0
    assert stopped == ['fp-s5pa-1b-forced-2.service']     # the loop still continued past the failure


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_failed_unit_listing_makes_the_receipt_and_step_nonzero(tmp_path):
    code, receipt, _ = _run_cleanup_step(tmp_path, SIM_LIST_FAIL='1')
    assert receipt['cleanup_exit'] != 0
    assert code != 0


# =================================================================== round 5
# Codex review of 51f0f64c: 4116822293 (call-count mismatch must fail),
# 4116822295 (single-source the job timeout).

def _set_counts(directory, arm, repeat, counts):
    path = directory / ('%s-%d.json' % (arm, repeat))
    row = json.loads(path.read_text())
    row['counts'] = counts
    path.write_text(json.dumps(row))


def test_linux_instrumented_call_count_mismatch_is_invalid(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _set_counts(directory, 'forced', 0, {'replay': 13, 'proof': 1, 'verify_for': 1})
    code, record = _summarize_job(h, directory)
    assert any(reason.startswith('H-COUNTS') for reason in record['verdict']['reasons'])
    assert record['verdict']['validity_ok'] is False
    assert record['verdict']['rule_applicable'] is False
    assert record['verdict']['stop_class'] == 'INVALID_MEASUREMENT'
    assert code == 4


def test_linux_instrumented_repeat_without_counts_is_invalid(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _set_counts(directory, 'prescribed', 0, None)
    code, record = _summarize_job(h, directory)
    assert any(reason.startswith('H-COUNTS') for reason in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 4


def test_windows_instrumented_call_count_mismatch_fails_harness_validation(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    entry = next(e for e in bundle['entries'] if e['arm'] == 'prescribed' and e['repeat'] == 0)
    entry['row']['counts'] = {'replay': 1, 'proof': 2, 'verify_for': 1}
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(reason.startswith('H-COUNTS') for reason in record['verdict']['reasons'])
    assert record['verdict']['validity_ok'] is False
    assert code == 4


def test_matching_call_counts_add_no_count_reason(h, tmp_path):
    code, record = _summarize_job(h, _linux_job(tmp_path / 'a'))
    assert not any('call counts' in reason for reason in record['verdict']['reasons'])
    assert code == 0


# =================================================================== round 6
# Codex review of 20a8e682: 4116862954 (unit CPU required), 4116862960 (attempts <= 2),
# plus the fail-closed class sweep.

def _edit_unit(directory, name, drop=(), set_=None):
    path = directory / name
    lines = [line for line in path.read_text().splitlines() if line.split('=', 1)[0] not in drop]
    for key, value in (set_ or {}).items():
        lines = [line for line in lines if not line.startswith(key + '=')] + ['%s=%s' % (key, value)]
    path.write_text('\n'.join(lines) + '\n')


def _edit_row(directory, name, **changes):
    path = directory / name
    row = json.loads(path.read_text())
    row.update(changes)
    path.write_text(json.dumps(row))


# ---- 4116862954: a missing per-repeat unit CPU reading is incomplete, not a fallback

@pytest.mark.parametrize('value', [None, '[not set]', str(2 ** 64 - 1)])
def test_missing_unit_cpu_makes_the_ceiling_incomplete(h, tmp_path, value):
    directory = _linux_job(tmp_path / 'a')
    if value is None:
        _edit_unit(directory, 'forced-2.unit', drop=('CPUUsageNSec',))
    else:
        _edit_unit(directory, 'forced-2.unit', set_={'CPUUsageNSec': value})
    code, record = _summarize_job(h, directory)
    rep = next(r for r in record['repeats'] if r['arm'] == 'forced' and r['repeat'] == 2)
    assert rep['cpu_input_s'] is None
    assert record['verdict']['rule_applicable'] is False
    assert record['verdict']['ceiling_inputs_complete'] is False


# ---- 4116862960: run attempts above 2 are refused; the 1/2 mixture is allowed

def _set_attempt(path, attempt):
    record = json.loads(path.read_text())
    record['runtime']['run_attempt'] = attempt
    path.write_text(json.dumps(record))


@pytest.mark.parametrize('attempt', ['3', '0', None, 'x'])
def test_combine_refuses_run_attempts_outside_one_and_two(h, tmp_path, attempt):
    a, b = _two_jobs(h, tmp_path)
    _set_attempt(b, attempt)
    _receipt(b.parent, job='b', run_attempt=str(attempt))
    with pytest.raises(SystemExit) as refused:
        _combine(h, a, b, tmp_path)
    assert 'attempt' in str(refused.value.code)
    assert not (tmp_path / 'combined.json').exists()


def test_combine_accepts_the_failed_rerun_mixture_of_attempts_one_and_two(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    _set_attempt(b, '2')
    _receipt(b.parent, job='b', run_attempt='2')
    assert _combine(h, a, b, tmp_path) == 0


# ---- sweep: system-manager inputs fail closed

def test_missing_poll_timeout_marker_is_i6(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'forced-2.unit', drop=('HarnessPollTimeout',))
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('I-6: forced-2') for r in record['verdict']['reasons'])
    assert code == 3


@pytest.mark.parametrize('result', ['', 'signal', 'oom-kill'])
def test_unit_result_other_than_success_is_i6(h, tmp_path, result):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'forced-2.unit', set_={'Result': result})
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('I-6: forced-2') for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False


def test_missing_unit_file_is_i6(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    (directory / 'forced-2.unit').unlink()
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('I-6: forced-2') for r in record['verdict']['reasons'])


def test_row_error_exit_with_clean_unit_status_is_i6(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_row(directory, 'forced-2.json', exit_status=1, error='RuntimeError: x')
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('I-6: forced-2') for r in record['verdict']['reasons'])


# ---- sweep: row content fails closed

def test_completed_repeat_without_assertions_or_panels_is_i5(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_row(directory, 'forced-2.json', assertions=None, panels=None)
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('I-5: forced-2') for r in record['verdict']['reasons'])
    assert code == 4


def test_completed_repeat_without_digests_is_i4(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_row(directory, 'prescribed-3.json', final_sha256=None, initial_prefix_sha256=None)
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('I-4: prescribed-3') for r in record['verdict']['reasons'])
    assert code == 4


def test_row_filed_under_the_wrong_repeat_is_h_shape(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_row(directory, 'forced-3.json', instrumented=True)    # a timed row claiming to be instrumented
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('H-SHAPE: forced-3') for r in record['verdict']['reasons'])
    assert code == 4


def test_extra_repeat_outside_the_shape_is_h_shape(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    (directory / 'forced-6.json').write_text((directory / 'forced-5.json').read_text())
    (directory / 'forced-6.unit').write_text((directory / 'forced-5.unit').read_text())
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('H-SHAPE: forced-6') for r in record['verdict']['reasons'])


# ---- sweep: provenance fails closed

@pytest.mark.parametrize('case', ['no-dispatched-head', 'no-start-head', 'start-head-differs'])
def test_stage_1b_head_provenance_is_required(h, tmp_path, case):
    directory = _linux_job(tmp_path / 'a')
    extra = ()
    if case == 'no-start-head':
        (directory / 'git-head.txt').unlink()
    elif case == 'start-head-differs':
        (directory / 'git-head.txt').write_text('d' * 40 + '\n')
    argv = ['--summarize', str(directory), '--stage', '1b', '--mode', 'measure', '--job', 'a', '--run-id', '42',
            '--run-attempt', '1', '--arm-order', 'forced prescribed']
    if case != 'no-dispatched-head':
        argv += ['--dispatched-head', HEAD]
    code = h.main(argv)
    record = json.loads((directory / 'record.json').read_text())
    assert any(r.startswith('I-7') for r in record['verdict']['reasons'])
    assert code == 4


def test_job_arm_order_must_follow_the_alternation(h, tmp_path):
    directory = _linux_job(tmp_path / 'b', arm_order=('forced', 'prescribed'))
    code, record = _summarize_job(h, directory, job='b')
    assert any(r.startswith('H-SHAPE') and 'alternation' in r for r in record['verdict']['reasons'])


def test_combine_refuses_a_job_with_the_wrong_arm_order(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    record = json.loads(b.read_text())
    record['runtime']['arm_order'] = ['forced', 'prescribed']
    b.write_text(json.dumps(record))
    with pytest.raises(SystemExit) as refused:
        _combine(h, a, b, tmp_path)
    assert 'arm order' in str(refused.value.code)


def test_bundle_without_the_fixed_launcher_timeout_is_h_shape(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    bundle['timeout_s'] = 7200.0
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(r.startswith('H-SHAPE') and 'timeout' in r for r in record['verdict']['reasons'])
    assert code == 4


def test_bundle_with_duplicate_entries_is_h_shape(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    bundle['entries'].append(copy.deepcopy(bundle['entries'][0]))
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(r.startswith('H-SHAPE') and 'repeats an' in r for r in record['verdict']['reasons'])


def test_bundle_with_unknown_timeout_flag_is_i6(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    entry = next(e for e in bundle['entries'] if e['arm'] == 'forced' and e['repeat'] == 2)
    del entry['unit']['timed_out']
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(r.startswith('I-6: forced-2') for r in record['verdict']['reasons'])


def test_bundle_without_observe_runtime_identity_is_i7(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    if 'executed_identity' not in bundle:
        pytest.fail('launcher bundle carries no executed identity')
    bundle['executed_identity']['code_identity'] = {'worker_runtime_error': 'ImportError: x'}
    path.write_text(json.dumps(bundle))
    code, record = _summarize_bundle(h, path)
    assert any(r.startswith('I-7') and 'observe_runtime' in r for r in record['verdict']['reasons'])
    assert code == 4


def test_absent_forced_memory_does_not_crash_the_verdict(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    for r in (1, 2, 3, 4, 5):
        _edit_row(directory, 'forced-%d.json' % r, exit_status=1, error='RuntimeError: x')
    code, record = _summarize_job(h, directory)
    assert record['verdict']['memory_feasibility'] == 'UNVERIFIED'
    assert record['verdict']['rule_applicable'] is False


# =================================================================== round 7
# Codex review of a613f47f: 4116900414 (identity failure), 4116900412 (prescribed CPU),
# 4116900418 (cold-inclusive spread), plus the symmetry / ordering / output audit.

# ---- 4116900414: observe_runtime failure is I-7 before the verdict, Linux as on Windows

def test_linux_identity_collection_failure_is_i7_in_the_job_record(h, tmp_path, monkeypatch):
    monkeypatch.setattr(h, '_code_identity', lambda: ({'worker_runtime_error': 'ImportError: x'}, set()))
    code, record = _summarize_job(h, _linux_job(tmp_path / 'a'))
    assert any(r.startswith('I-7') and 'observe_runtime' in r for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert record['code_identity'] == {'worker_runtime_error': 'ImportError: x'}   # attached, not after
    assert code == 4


def test_combine_marks_records_without_runtime_identity_i7(h, tmp_path):
    a, b = _two_jobs(h, tmp_path)
    for path in (a, b):
        record = json.loads(path.read_text())
        record['code_identity'] = {'worker_runtime_error': 'ImportError: x'}
        path.write_text(json.dumps(record))
    code = _combine(h, a, b, tmp_path)
    record = json.loads((tmp_path / 'combined.json').read_text())
    assert any(r.startswith('I-7') and 'observe_runtime' in r for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 4


# ---- 4116900412: a missing prescribed warm CPU input makes the measurement incomplete

def test_missing_prescribed_warm_cpu_input_is_incomplete(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'prescribed-3.unit', drop=('CPUUsageNSec',))
    code, record = _summarize_job(h, directory)
    assert record['summary']['arms']['prescribed']['warm_spread'] is None     # no spread over a subset
    assert record['verdict']['rule_applicable'] is False
    assert any(r.startswith('INCOMPLETE') and 'prescribed' in r for r in record['verdict']['reasons'])


def test_missing_prescribed_cold_cpu_input_is_incomplete(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'prescribed-1.unit', drop=('CPUUsageNSec',))
    code, record = _summarize_job(h, directory)
    assert record['verdict']['rule_applicable'] is False


# ---- 4116900418 / output audit: spreads and distributions with and without the cold repeat

def test_record_carries_cold_inclusive_spread_and_distributions(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'forced-1.unit', set_={'CPUUsageNSec': str(40 * 10 ** 9)})   # a slower cold repeat
    code, record = _summarize_job(h, directory)
    forced = record['summary']['arms']['forced']
    assert forced['spread_all'] is not None and forced['spread_all'] > forced['warm_spread']
    for key in ('cpu_input_s', 'wall_workload_s', 'memory_bytes'):
        for part in ('all', 'warm'):
            stats = forced[key][part]
            assert {'max', 'median', 'min', 'spread', 'n', 'missing'} <= set(stats), (key, part)


# ---- symmetry audit fixes

def test_stage_1b_job_record_rejects_run_attempt_three(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    code = h.main(['--summarize', str(directory), '--stage', '1b', '--mode', 'measure', '--job', 'a',
                   '--run-id', '42', '--run-attempt', '3', '--arm-order', 'forced prescribed',
                   '--dispatched-head', HEAD])
    record = json.loads((directory / 'record.json').read_text())
    assert any(r.startswith('I-7') and 'run attempt' in r for r in record['verdict']['reasons'])
    assert code == 4


def test_stage_1b_required_fields_apply_like_stage_1a(h, tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_row(directory, 'forced-2.json', elapsed_seconds=None)
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('H-FIELDS: forced-2') for r in record['verdict']['reasons'])
    assert code == 4


@pytest.mark.parametrize('bound', [None, '7200'])
def test_linux_unit_without_the_fixed_poll_bound_is_h_shape(h, tmp_path, bound):
    directory = _linux_job(tmp_path / 'a')
    if bound is None:
        _edit_unit(directory, 'forced-2.unit', drop=('HarnessPollBoundS',))
    else:
        _edit_unit(directory, 'forced-2.unit', set_={'HarnessPollBoundS': bound})
    code, record = _summarize_job(h, directory)
    assert any(r.startswith('H-SHAPE: forced-2') and 'poll bound' in r for r in record['verdict']['reasons'])


def test_workflow_units_record_the_poll_bound():
    job = _workflow()['jobs']['measure']
    loop = next(s for s in job['steps'] if s.get('name') == 'Measurement loop')['run']
    assert int(job['env']['REPEAT_POLL_BOUND_S']) == 1800
    assert loop.count('HarnessPollBoundS=') == 3          # the waited, not-started and launch-failed unit files
    assert '+ REPEAT_POLL_BOUND_S' in loop                 # the wait uses the same value


def test_windows_bundle_arm_order_follows_the_stage_1a_command(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json', arms=('prescribed', 'forced'))
    code, record = _summarize_bundle(h, path)
    assert any(r.startswith('H-SHAPE') and 'arm order' in r for r in record['verdict']['reasons'])
    assert code == 4


# =================================================================== r2 §12.9 (operator ruling 2026-09-27)
# Exit semantics through the real --summarize / combine entry points, as a subprocess.
# The subprocess runs the harness's own main(): argument parsing, file reads, the
# verdict, the record write and the process exit code are all real. Only the two
# environment probes are pinned so the records do not depend on this checkout's
# git state or on importing ops/: _git (HEAD, tree status) and _code_identity
# (observe_runtime). The same pins are used by the in-process tests above.


CLI_RUNNER = """
import importlib.machinery, importlib.util, sys
harness, head = sys.argv[1], sys.argv[2]
loader = importlib.machinery.SourceFileLoader('s5pa_harness_cli', harness)
spec = importlib.util.spec_from_loader(loader.name, loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)
module._git = lambda *args: {'rev-parse': head, 'status': ''}[args[0]]
module._code_identity = lambda: ({'worker_runtime': {'python_version': 'x'}}, set())
sys.exit(module.main(sys.argv[3:]))
"""


def _cli(tmp_path, *argv):
    runner = tmp_path / 'cli_runner.py'
    if not runner.exists():
        runner.write_text(CLI_RUNNER)
    done = subprocess.run([sys.executable, '-I', str(runner), str(HARNESS), HEAD, *map(str, argv)],
                          capture_output=True, text=True, timeout=120)
    return done.returncode, done


def _cli_job(tmp_path, directory, *, job='a', attempt='1', arm_order=ARM_ORDER, mode='measure'):
    code, done = _cli(tmp_path, '--summarize', directory, '--stage', '1b', '--mode', mode, '--job', job,
                      '--run-id', '42', '--run-attempt', attempt, '--arm-order', ' '.join(arm_order),
                      '--dispatched-head', HEAD)
    record = json.loads((directory / 'record.json').read_text())
    return code, record, done


def _drop_unit_cpu(directory, arm):
    _edit_unit(directory, '%s-2.unit' % arm, drop=('CPUUsageNSec',))


@pytest.mark.parametrize('arm', ['forced', 'prescribed'])
@pytest.mark.parametrize('attempt, eligible', [('1', True), ('2', False)])
def test_cli_job_missing_ceiling_input_is_incomplete_evidence(tmp_path, arm, attempt, eligible):
    directory = _linux_job(tmp_path / 'a')
    _drop_unit_cpu(directory, arm)
    code, record, done = _cli_job(tmp_path, directory, attempt=attempt)
    verdict = record['verdict']
    assert code == 3, done.stdout + done.stderr
    assert verdict['exit_code'] == 3
    assert verdict['stop_class'] == 'INCOMPLETE_EVIDENCE'
    assert verdict['validity_ok'] is False and verdict['rule_applicable'] is False
    assert verdict['rerun_eligible'] is eligible
    incomplete = [r for r in verdict['reasons'] if r.startswith('INCOMPLETE')]
    assert incomplete and '%s-2' % arm in incomplete[0] or 'arm %s' % arm in incomplete[0]


def _cli_two_jobs(tmp_path, *, incomplete_arm=None, failing_job='b', attempt='1'):
    jobs = {'a': ('forced', 'prescribed'), 'b': ('prescribed', 'forced')}
    paths = {}
    for job, order in jobs.items():
        directory = _linux_job(tmp_path / job, arm_order=order)
        job_attempt = attempt if job == failing_job else '1'
        if incomplete_arm and job == failing_job:
            _drop_unit_cpu(directory, incomplete_arm)
        _cli_job(tmp_path, directory, job=job, attempt=job_attempt, arm_order=order)
        _receipt(directory, job=job, run_attempt=job_attempt)
        paths[job] = directory / 'record.json'
    code, done = _cli(tmp_path, '--summarize', paths['a'], paths['b'], '--record', tmp_path / 'combined.json')
    return code, json.loads((tmp_path / 'combined.json').read_text()), done


@pytest.mark.parametrize('arm', ['forced', 'prescribed'])
@pytest.mark.parametrize('attempt, eligible', [('1', True), ('2', False)])
def test_cli_combined_missing_ceiling_input_is_incomplete_evidence(tmp_path, arm, attempt, eligible):
    code, record, done = _cli_two_jobs(tmp_path, incomplete_arm=arm, attempt=attempt)
    verdict = record['verdict']
    assert code == 3, done.stdout + done.stderr
    assert verdict['stop_class'] == 'INCOMPLETE_EVIDENCE'
    assert verdict['validity_ok'] is False and verdict['rule_applicable'] is False
    assert verdict['rerun_eligible'] is eligible
    assert any(r.startswith('INCOMPLETE') for r in verdict['reasons'])


def test_cli_complete_stage_1b_job_and_combination_are_rule_applicable(tmp_path):
    code, record, done = _cli_job(tmp_path, _linux_job(tmp_path / 'solo'))
    assert code == 0, done.stdout + done.stderr
    assert record['verdict']['rule_applicable'] is True and record['verdict']['stop_class'] == 'none'
    assert record['verdict']['rerun_eligible'] is False
    code, combined, done = _cli_two_jobs(tmp_path / 'pair')
    assert code == 0, done.stdout + done.stderr
    assert combined['verdict']['rule_applicable'] is True and combined['verdict']['validity_ok'] is True


def test_cli_stage_1a_bundle_without_complete_memory_exits_0_never_rule_applicable(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    code, done = _cli(tmp_path, '--summarize', path, '--stage', '1a')
    record = json.loads(path.with_suffix('.record.json').read_text())
    assert code == 0, done.stdout + done.stderr
    assert record['summary']['memory_complete_all_timed_repeats'] is False
    assert record['verdict']['validity_ok'] is True
    assert record['verdict']['rule_applicable'] is False
    assert record['verdict']['rerun_eligible'] is None


def _dry_job(directory):
    directory.mkdir(parents=True)
    for arm in ARM_ORDER:
        unit = 'fp-s5pa-1b-%s-1' % arm
        (directory / ('%s-1.json' % arm)).write_text(json.dumps(_row(arm, 1, dry_run=True, unit=unit)))
        (directory / ('%s-1.unit' % arm)).write_text(_unit_text())
    (directory / 'probe.json').write_text(json.dumps({'ok': True, 'swap_total_kb': 0, 'reasons': []}))
    (directory / 'git-head.txt').write_text(HEAD + '\n')
    return directory


def test_cli_dry_run_meeting_its_requirements_exits_0_never_rule_applicable(tmp_path):
    directory = _dry_job(tmp_path / 'dry')
    code, record, done = _cli_job(tmp_path, directory, mode='dry-run')
    assert code == 0, done.stdout + done.stderr
    assert record['mode'] == 'dry-run'
    assert record['verdict']['validity_ok'] is True
    assert record['verdict']['rule_applicable'] is False
    assert record['verdict']['rerun_eligible'] is None


@pytest.mark.parametrize('missing', ['timeout_s', 'executed_identity'])
def test_cli_legacy_bundle_is_legacy_unaccepted_and_left_unmodified(h, tmp_path, missing):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    bundle.pop(missing)
    path.write_text(json.dumps(bundle))
    before = path.read_bytes()
    code, done = _cli(tmp_path, '--summarize', path, '--stage', '1a')
    record = json.loads(path.with_suffix('.record.json').read_text())
    assert code == 4, done.stdout + done.stderr
    assert record['verdict']['stop_class'] == 'LEGACY_UNACCEPTED'
    assert record['verdict']['validity_ok'] is False and record['verdict']['rule_applicable'] is False
    assert path.read_bytes() == before            # retained unmodified


@pytest.mark.parametrize('drop', ['Result', 'HarnessPollTimeout', 'ExecMainStatus'])
def test_cli_missing_completion_field_is_i6(tmp_path, drop):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'forced-3.unit', drop=(drop,))
    code, record, done = _cli_job(tmp_path, directory)
    assert any(r.startswith('I-6: forced-3') for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 3, done.stdout + done.stderr


def test_cli_missing_windows_timed_out_field_is_i6(h, tmp_path):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    entry = next(e for e in bundle['entries'] if e['arm'] == 'prescribed' and e['repeat'] == 4)
    del entry['unit']['timed_out']
    path.write_text(json.dumps(bundle))
    code, done = _cli(tmp_path, '--summarize', path, '--stage', '1a')
    record = json.loads(path.with_suffix('.record.json').read_text())
    assert any(r.startswith('I-6: prescribed-4') for r in record['verdict']['reasons'])
    assert code == 3, done.stdout + done.stderr


# ---- workflow: record generation, owned cleanup and upload still run after an exit 3

def test_workflow_cleanup_and_upload_run_after_a_summarize_failure():
    steps = _workflow()['jobs']['measure']['steps']
    names = [s.get('name', '') for s in steps]
    summarize = next(i for i, n in enumerate(names) if n.startswith('Summarize'))
    cleanup = names.index('Owned cleanup and journal export')
    upload = names.index("Upload this job's measurement evidence")
    assert summarize < cleanup < upload
    assert '!cancelled()' in steps[summarize]['if']            # runs after a failed loop, too
    assert steps[cleanup]['if'] == 'always()' and steps[upload]['if'] == 'always()'
    assert 'set +e' in steps[summarize]['run']                  # the exit status is captured, not aborted on


SUMMARIZE_STUBS = {
    'sudo': 'exec "$@"\n',
}
FAKE_HARNESS_PYTHON = """#!/bin/bash
out="$RUNNER_TEMP/s5-part-a-measurement"
printf '{"verdict": {"exit_code": 3, "stop_class": "INCOMPLETE_EVIDENCE"}}' > "$out/record.json"
echo 'S5 Part A measurement: stage=1b mode=measure stop_class=INCOMPLETE_EVIDENCE exit=3'
exit 3
"""


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_summarize_step_keeps_the_record_and_step_summary_on_exit_3(tmp_path):
    job = _workflow()['jobs']['measure']
    step = next(s for s in job['steps'] if s.get('name', '').startswith('Summarize'))
    sim = tmp_path / 'sim'
    (sim / 'bin').mkdir(parents=True)
    for name, body in SUMMARIZE_STUBS.items():
        stub = sim / 'bin' / name
        stub.write_text('#!/bin/bash\n' + body)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    host = sim / 'host'
    (host / 'env' / 'bin').mkdir(parents=True)
    python = host / 'env' / 'bin' / 'python'
    python.write_text(FAKE_HARNESS_PYTHON)
    python.chmod(python.stat().st_mode | stat.S_IEXEC)
    runner_temp = sim / 'rt'
    (runner_temp / 's5-part-a-measurement').mkdir(parents=True)
    (runner_temp / 'qualification-manifest').write_text(str(host / 'manifest'))
    summary = sim / 'step-summary.md'
    env = {'PATH': '%s:/usr/bin:/bin' % (sim / 'bin'), 'RUNNER_TEMP': str(runner_temp), 'NOTE_DIR': 'x',
           'STAGE': '1b', 'MODE': 'measure', 'JOB': 'a', 'GITHUB_RUN_ID': '42', 'GITHUB_RUN_ATTEMPT': '1',
           'RUNNER_NAME': 'r', 'GITHUB_SHA': HEAD, 'RUNTIME': 'host_venv', 'ARM_ORDER': 'forced prescribed',
           'GITHUB_STEP_SUMMARY': str(summary)}
    # GitHub's default bash for `run`: bash --noprofile --norc -eo pipefail {0}
    done = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', step['run']],
                          env=env, capture_output=True, text=True, timeout=60, cwd=str(sim))
    assert done.returncode == 3, done.stderr
    assert (runner_temp / 's5-part-a-measurement' / 'record.json').is_file()
    assert 'INCOMPLETE_EVIDENCE' in (runner_temp / 's5-part-a-measurement' / 'summarize.log').read_text()
    assert 'exit=3' in summary.read_text()


# =================================================================== review of 11e15c6b
# 4116981570 (unreadable probe is I-1), 4116981563 (launcher keeps results when a job
# fails to start), 4116981558 (dry-run fields stay gated), and the retained-failure sweep.

def _no_traceback(done):
    assert 'Traceback' not in done.stderr, done.stderr


# ---- 4116981570: an unreadable probe.json is a retained failed probe (I-1, exit 3)

@pytest.mark.parametrize('content', ['{"ok": tr', '[1, 2]', ''])
def test_cli_unreadable_probe_is_i1_and_the_record_is_written(tmp_path, content):
    directory = _linux_job(tmp_path / 'a')
    (directory / 'probe.json').write_text(content)
    code, record, done = _cli_job(tmp_path, directory)
    _no_traceback(done)
    assert any(r.startswith('I-1') and 'probe.json unreadable' in r for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 3


# ---- 4116981563: the Windows launcher retains every repeat and always writes the bundle

def _fake_job(**overrides):
    unit = {'pid': 1, 'exit_code': 0, 'timed_out': False, 'outer_wall_s': 35.0, 'job_cpu_s': 34.0,
            'job_processes': 1, 'job_peak_process_commit_bytes': 1, 'job_peak_commit_bytes': 1}
    unit.update(overrides)
    return unit


def _run_launcher(h, tmp_path, monkeypatch, fail, purge=lambda: (0, [])):
    """launcher() in-process with os.name pinned to 'nt' and the job-object call stubbed:
    `fail(arm, repeat)` returns an exception to raise, or None to succeed."""
    import types

    def run_in_job(command, *, env, timeout_s):
        arm, repeat = command[command.index('--arm') + 1], int(command[command.index('--repeat') + 1])
        exc = fail(arm, repeat)
        if exc is not None:
            raise exc
        out = Path(command[command.index('--out') + 1])
        out.write_text(json.dumps(_row(arm, repeat, stage='1a')))
        return _fake_job()
    monkeypatch.setattr(h, 'os', types.SimpleNamespace(name='nt', environ=dict(os.environ)))
    monkeypatch.setattr(h, '_run_in_job', run_in_job)
    monkeypatch.setattr(h, '_purge_pycache', purge)
    out = tmp_path / 'windows.json'
    code = h.main(['--launcher', '--stage', '1a', '--arms', 'forced,prescribed', '--repeats', '5',
                   '--out', str(out)])
    monkeypatch.setattr(h, 'os', os)   # the summarize that follows runs on the real platform
    return code, out


def test_launcher_retains_a_repeat_whose_job_creation_fails(h, tmp_path, monkeypatch):
    code, out = _run_launcher(h, tmp_path, monkeypatch,
                              lambda arm, r: OSError(5, 'AssignProcessToJobObject failed')
                              if (arm, r) == ('forced', 3) else None)
    assert code == 0 and out.is_file()
    bundle = json.loads(out.read_text())
    assert len(bundle['entries']) == 12
    failed = next(e for e in bundle['entries'] if (e['arm'], e['repeat']) == ('forced', 3))
    assert 'AssignProcessToJobObject' in failed['unit']['launch_error'] and failed['row'] is None
    code, record = _summarize_bundle(h, out)
    assert any(r.startswith('I-6: forced-3') and 'AssignProcessToJobObject' in r
               for r in record['verdict']['reasons'])
    assert code == 3


class _SimulatedInterrupt(BaseException):
    """Stands in for KeyboardInterrupt (the same BaseException path in the launcher)
    without stopping the pytest session if a launcher fails to catch it."""


def test_interrupted_launcher_still_writes_the_bundle(h, tmp_path, monkeypatch):
    code, out = _run_launcher(h, tmp_path, monkeypatch,
                              lambda arm, r: _SimulatedInterrupt() if (arm, r) == ('prescribed', 2) else None)
    assert code == 130 and out.is_file()
    bundle = json.loads(out.read_text())
    assert bundle['interrupted'].startswith('_SimulatedInterrupt')
    code, record = _summarize_bundle(h, out)
    reasons = record['verdict']['reasons']
    assert any('interrupted' in r for r in reasons) and any(r.startswith('I-6: prescribed-2') for r in reasons)
    assert record['verdict']['validity_ok'] is False


# ---- 4116981558: dry-run fields stay gated; runner accounting values are I-1

@pytest.mark.parametrize('drop', ['CPUUsageNSec', 'ExecMainExitTimestampMonotonic'])
def test_cli_dry_run_without_runner_accounting_is_i1(tmp_path, drop):
    directory = _dry_job(tmp_path / 'dry')
    _edit_unit(directory, 'forced-1.unit', drop=(drop,))
    code, record, done = _cli_job(tmp_path, directory, mode='dry-run')
    named = 'CPUUsageNSec' if drop == 'CPUUsageNSec' else 'ExecMainExitTimestampMonotonic'
    assert any(r.startswith('I-1: ') and named in r and 'unset on dry-run repeat forced-1' in r
               for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 3, done.stdout + done.stderr


def test_cli_dry_run_missing_a_harness_field_is_h_fields(tmp_path):
    directory = _dry_job(tmp_path / 'dry')
    _edit_row(directory, 'prescribed-1.json', predicted_seconds=None)
    code, record, done = _cli_job(tmp_path, directory, mode='dry-run')
    assert any(r.startswith('H-FIELDS: prescribed-1') and 'predicted_seconds' in r
               for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 4, done.stdout + done.stderr


def test_cli_stage_1b_measure_ceiling_fields_stay_incomplete_not_i1(tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'forced-2.unit', drop=('CPUUsageNSec',))
    code, record, done = _cli_job(tmp_path, directory)
    assert record['verdict']['stop_class'] == 'INCOMPLETE_EVIDENCE'
    assert not any(r.startswith('I-1') for r in record['verdict']['reasons'])
    assert code == 3


# ---- sweep: every unreadable input ends in a retained record or a clear refusal

@pytest.mark.parametrize('content', ['{"schema": "s5-part', '{"schema": "%s", "entries": 7}'])
def test_cli_unreadable_or_malformed_bundle_is_retained_as_i6(tmp_path, content):
    path = tmp_path / 'windows.json'
    path.write_text(content.replace('%s', 's5-part-a-max-expansion-measurement/v2#windows-launcher-bundle'))
    before = path.read_bytes()
    code, done = _cli(tmp_path, '--summarize', path, '--stage', '1a')
    _no_traceback(done)
    record = json.loads(path.with_suffix('.record.json').read_text())
    assert any(r.startswith('I-6') and 'bundle unreadable or malformed' in r for r in record['verdict']['reasons'])
    assert record['verdict']['validity_ok'] is False and path.read_bytes() == before
    assert code == 3


def test_cli_non_bundle_file_is_refused_without_a_traceback(tmp_path):
    path = tmp_path / 'not-a-bundle.json'
    path.write_text(json.dumps({'schema': 'something-else'}))
    code, done = _cli(tmp_path, '--summarize', path, '--stage', '1a')
    _no_traceback(done)
    assert code != 0 and 'not a launcher bundle' in done.stderr


def test_cli_missing_input_is_refused_without_a_traceback(tmp_path):
    code, done = _cli(tmp_path, '--summarize', tmp_path / 'absent', '--stage', '1b')
    _no_traceback(done)
    assert code != 0 and 'no such input' in done.stderr


@pytest.mark.parametrize('content', ['', '\xff\xfe'])
def test_cli_unreadable_start_head_is_i7(tmp_path, content):
    directory = _linux_job(tmp_path / 'a')
    (directory / 'git-head.txt').write_bytes(content.encode('latin-1'))
    code, record, done = _cli_job(tmp_path, directory)
    _no_traceback(done)
    assert any(r.startswith('I-7') for r in record['verdict']['reasons'])
    assert code == 4


@pytest.mark.parametrize('damage', ['truncated', 'malformed'])
def test_cli_combine_refuses_an_unreadable_job_record_without_a_traceback(tmp_path, damage):
    code, _, _ = _cli_two_jobs(tmp_path)
    assert code == 0
    b = tmp_path / 'b' / 'record.json'
    if damage == 'truncated':
        b.write_text(b.read_text()[:200])
    else:
        record = json.loads(b.read_text())
        del record['verdict']
        b.write_text(json.dumps(record))
    (tmp_path / 'combined.json').unlink()
    code, done = _cli(tmp_path, '--summarize', tmp_path / 'a' / 'record.json', b, '--record',
                      tmp_path / 'combined.json')
    _no_traceback(done)
    assert code != 0 and 'refused' in done.stderr
    assert not (tmp_path / 'combined.json').exists()


def test_cli_probe_verdict_with_malformed_in_unit_output_fails_closed(tmp_path):
    directory = tmp_path / 'probe'
    directory.mkdir()
    (directory / 'probe-in-unit.json').write_text('[1]')
    (directory / 'probe.unit').write_text('CPUUsageNSec=1\n')
    code, done = _cli(tmp_path, '--probe-verdict', directory)
    _no_traceback(done)
    assert code == 3
    assert json.loads((directory / 'probe.json').read_text())['ok'] is False


LOOP_STUBS = {
    'sudo': 'if [ "$1" = tee ]; then cat > /dev/null; exit 0; fi\nexec "$@"\n',
    # systemd-run fails for the unit named in SIM_FAIL_RUN
    'systemd-run': ('for a in "$@"; do case "$a" in --unit=*) u="${a#--unit=}" ;; esac; done\n'
                    '[ "$u" = "${SIM_FAIL_RUN:-}" ] && exit 1\necho "$u" >> "$SIM/started.log"\n'),
    # every started unit has exited; `show` of the unit in SIM_FAIL_SHOW fails
    'systemctl': ('case "$1" in show)\n'
                  '  for a in "$@"; do [ "$a" = --value ] && { echo exited; exit 0; }; done\n'
                  '  for a in "$@"; do u="$a"; done\n'
                  '  [ "$u" = "${SIM_FAIL_SHOW:-}" ] && exit 1\n'
                  '  printf "CPUUsageNSec=1\\nExecMainStatus=0\\nResult=success\\n" ;; *) exit 0 ;; esac\n'),
    'date': 'if [ "$1" = +%s ]; then cat "$SIM/clock"; else exec /bin/date "$@"; fi\n',
    'sleep': 'exit 0\n',
}


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_loop_retains_a_failed_unit_start_and_a_failed_show_and_continues(h, tmp_path):
    job = _workflow()['jobs']['measure']
    step = next(s for s in job['steps'] if s.get('name') == 'Measurement loop')
    sim = tmp_path / 'sim'
    (sim / 'bin').mkdir(parents=True)
    for name, body in LOOP_STUBS.items():
        stub = sim / 'bin' / name
        stub.write_text('#!/bin/bash\n' + body)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    (sim / 'clock').write_text('1000000')
    runner_temp = sim / 'rt'
    out = runner_temp / 's5-part-a-measurement'
    out.mkdir(parents=True)
    (sim / 'host').mkdir()
    (runner_temp / 'qualification-manifest').write_text(str(sim / 'host' / 'manifest'))
    (sim / 'ws').mkdir()
    env = {'PATH': '%s:/usr/bin:/bin' % (sim / 'bin'), 'SIM': str(sim), 'RUNNER_TEMP': str(runner_temp),
           'GITHUB_WORKSPACE': str(sim / 'ws'), 'STAGE': '1b', 'MODE': 'measure', 'NOTE_DIR': 'x',
           'ARM_ORDER': 'forced prescribed', 'JOB_START_EPOCH': '1000000',
           'SIM_FAIL_RUN': 'fp-s5pa-1b-forced-2', 'SIM_FAIL_SHOW': 'fp-s5pa-1b-forced-3'}
    env.update({k: str(v) for k, v in job['env'].items() if '${{' not in str(v)})
    env['JOB_TIMEOUT_MIN'] = str(_timeout_min(job)[1])
    done = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', step['run']],
                          env=env, capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    units = {p.stem: p.read_text() for p in out.glob('*.unit')}
    assert len(units) == 12                                            # the loop went on after both
    assert 'HarnessLaunchFailed=systemd-run' in units['forced-2']
    assert 'HarnessShowFailed=yes' in units['forced-3'] and 'Result=' not in units['forced-3']
    started = (sim / 'started.log').read_text().split()
    assert 'fp-s5pa-1b-forced-4' in started and 'fp-s5pa-1b-prescribed-0' in started
    (out / 'probe.json').write_text(json.dumps({'ok': True, 'swap_total_kb': 0, 'reasons': []}))
    (out / 'git-head.txt').write_text(HEAD + '\n')
    code = h.main(['--summarize', str(out), '--stage', '1b', '--mode', 'measure', '--job', 'a', '--run-id', '42',
                   '--arm-order', 'forced prescribed', '--dispatched-head', HEAD, '--run-attempt', '1'])
    record = json.loads((out / 'record.json').read_text())
    reasons = record['verdict']['reasons']
    assert any(r.startswith('I-6: forced-2') and 'launch-failed' in r for r in reasons)
    assert any(r.startswith('I-6: forced-3') for r in reasons)
    assert code == 3


def test_cli_failed_probe_with_complete_memory_is_never_rule_applicable(tmp_path):
    # r2 §12.7 I-1: memory UNVERIFIED and the rule not applicable, even when every repeat's
    # in-unit memory reading is complete.
    directory = _linux_job(tmp_path / 'a')
    (directory / 'probe.json').write_text(json.dumps({'ok': False, 'reasons': ['SwapTotal is not 0 kB']}))
    code, record, done = _cli_job(tmp_path, directory)
    assert record['summary']['memory_complete_all_timed_repeats'] is True
    assert record['verdict']['memory_feasibility'] == 'UNVERIFIED'
    assert record['verdict']['rule_applicable'] is False
    assert record['verdict']['stop_class'] == 'MEMORY_EVIDENCE_MISSING'
    assert code == 3, done.stdout + done.stderr


# =================================================================== review of 73526d6d
# 4117030870 (cold purge must succeed), 4117030878 (probe unit must complete),
# 4117030873 (fixed workload oracles), and the precondition / oracle sweep.

# ---- 4117030870: a failed cold purge is observable and the cold repeat does not validate

def test_purge_reports_directories_it_could_not_remove(h, tmp_path, monkeypatch):
    for name in ('ops/a/__pycache__', 'core/b/__pycache__', 'tests/c/__pycache__'):
        (tmp_path / name).mkdir(parents=True)
    monkeypatch.setattr(h, 'ROOT', tmp_path)
    real = shutil.rmtree

    def rmtree(path, *args, **kwargs):   # the core/ directory is locked and survives
        if 'core' not in Path(path).parts:
            real(path)
    monkeypatch.setattr(h.shutil, 'rmtree', rmtree)
    removed, failed = h._purge_pycache()
    assert removed == 2 and failed == ['core/b/__pycache__']


def test_launcher_cold_repeat_with_a_failed_purge_is_i6(h, tmp_path, monkeypatch):
    code, out = _run_launcher(h, tmp_path, monkeypatch, lambda arm, r: None,
                              purge=lambda: (2, ['ops/x/__pycache__']))
    bundle = json.loads(out.read_text())
    cold = next(e for e in bundle['entries'] if (e['arm'], e['repeat']) == ('forced', 1))
    assert cold['unit']['purge_failed_dirs'] == ['ops/x/__pycache__']
    code, record = _summarize_bundle(h, out)
    reasons = record['verdict']['reasons']
    assert any(r.startswith('I-6: forced-1') and 'cold precondition' in r for r in reasons)
    assert any(r.startswith('I-6: prescribed-1') and 'cold precondition' in r for r in reasons)
    assert record['verdict']['validity_ok'] is False and code == 3


@pytest.mark.parametrize('unit_change', [{'purge_error': 'PermissionError: x'}, {'purge_failed_dirs': None},
                                         {'pycache_dirs_purged': None}])
def test_cli_bundle_cold_repeat_without_purge_evidence_is_i6(h, tmp_path, unit_change):
    path = _bundle(h, tmp_path / 'windows.json')
    bundle = json.loads(path.read_text())
    entry = next(e for e in bundle['entries'] if (e['arm'], e['repeat']) == ('prescribed', 1))
    entry['unit'].update(unit_change)
    bundle['executed_identity'] = h._executed_identity([e['row'] for e in bundle['entries']])
    path.write_text(json.dumps(bundle))
    code, done = _cli(tmp_path, '--summarize', path, '--stage', '1a')
    record = json.loads(path.with_suffix('.record.json').read_text())
    assert any(r.startswith('I-6: prescribed-1') and 'cold precondition' in r for r in record['verdict']['reasons'])
    assert code == 3, done.stdout + done.stderr


def test_cli_linux_cold_repeat_without_cold_prep_marker_is_i6(tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_unit(directory, 'forced-1.unit', drop=('HarnessColdPrep',))
    code, record, done = _cli_job(tmp_path, directory)
    assert any(r.startswith('I-6: forced-1') and 'cold precondition' in r for r in record['verdict']['reasons'])
    assert record['verdict']['rule_applicable'] is False
    assert code == 3


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_loop_stops_when_the_cold_purge_leaves_bytecode_behind(tmp_path):
    job = _workflow()['jobs']['measure']
    step = next(s for s in job['steps'] if s.get('name') == 'Measurement loop')
    sim = tmp_path / 'sim'
    (sim / 'bin').mkdir(parents=True)
    stubs = dict(LOOP_STUBS)
    stubs['rm'] = 'exit 0\n'          # the purge silently removes nothing
    for name, body in stubs.items():
        stub = sim / 'bin' / name
        stub.write_text('#!/bin/bash\n' + body)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    (sim / 'clock').write_text('1000000')
    runner_temp = sim / 'rt'
    out = runner_temp / 's5-part-a-measurement'
    out.mkdir(parents=True)
    (sim / 'host').mkdir()
    (runner_temp / 'qualification-manifest').write_text(str(sim / 'host' / 'manifest'))
    (sim / 'ws' / 'ops' / '__pycache__').mkdir(parents=True)
    env = {'PATH': '%s:/usr/bin:/bin' % (sim / 'bin'), 'SIM': str(sim), 'RUNNER_TEMP': str(runner_temp),
           'GITHUB_WORKSPACE': str(sim / 'ws'), 'STAGE': '1b', 'MODE': 'measure', 'NOTE_DIR': 'x',
           'ARM_ORDER': 'forced prescribed', 'JOB_START_EPOCH': '1000000'}
    env.update({k: str(v) for k, v in job['env'].items() if '${{' not in str(v)})
    env['JOB_TIMEOUT_MIN'] = str(_timeout_min(job)[1])
    done = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', step['run']],
                          env=env, capture_output=True, text=True, timeout=60)
    assert done.returncode != 0 and 'cold purge left __pycache__ behind' in done.stderr
    assert not (sim / 'started.log').exists()             # no unit ran as a false cold repeat


@pytest.mark.skipif(os.name == 'nt', reason='runs the workflow bash step with POSIX stubs')
def test_loop_records_the_cold_prep_on_repeat_1_only(tmp_path):
    job = _workflow()['jobs']['measure']
    step = next(s for s in job['steps'] if s.get('name') == 'Measurement loop')
    sim = tmp_path / 'sim'
    (sim / 'bin').mkdir(parents=True)
    for name, body in LOOP_STUBS.items():
        stub = sim / 'bin' / name
        stub.write_text('#!/bin/bash\n' + body)
        stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    (sim / 'clock').write_text('1000000')
    runner_temp = sim / 'rt'
    out = runner_temp / 's5-part-a-measurement'
    out.mkdir(parents=True)
    (sim / 'host').mkdir()
    (runner_temp / 'qualification-manifest').write_text(str(sim / 'host' / 'manifest'))
    (sim / 'ws' / 'ops' / '__pycache__').mkdir(parents=True)
    env = {'PATH': '%s:/usr/bin:/bin' % (sim / 'bin'), 'SIM': str(sim), 'RUNNER_TEMP': str(runner_temp),
           'GITHUB_WORKSPACE': str(sim / 'ws'), 'STAGE': '1b', 'MODE': 'measure', 'NOTE_DIR': 'x',
           'ARM_ORDER': 'forced prescribed', 'JOB_START_EPOCH': '1000000'}
    env.update({k: str(v) for k, v in job['env'].items() if '${{' not in str(v)})
    env['JOB_TIMEOUT_MIN'] = str(_timeout_min(job)[1])
    done = subprocess.run(['bash', '--noprofile', '--norc', '-eo', 'pipefail', '-c', step['run']],
                          env=env, capture_output=True, text=True, timeout=60)
    assert done.returncode == 0, done.stderr
    assert not (sim / 'ws' / 'ops' / '__pycache__').exists()
    units = {p.stem: p.read_text() for p in out.glob('*.unit')}
    assert 'HarnessColdPrep=done' in units['forced-1'] and 'HarnessColdPrep=done' in units['prescribed-1']
    assert not any('HarnessColdPrep' in text for name, text in units.items() if not name.endswith('-1'))


# ---- 4117030878: the probe unit must have exited 0 with Result=success

def _probe_dir(tmp_path, unit_text):
    directory = tmp_path / 'probe'
    directory.mkdir()
    (directory / 'probe-in-unit.json').write_text(json.dumps({
        'child_exit': 0, 'child_touched_bytes': 64 << 20, 'cgroup_path': '/system.slice/fp-s5pa-probe.service',
        'memory_peak': str(70_000_000), 'memory_swap_max': '0', 'cpu_stat': 'usage_usec 1', 'swap_total_kb': 0}))
    (directory / 'probe.unit').write_text(unit_text)
    return directory


@pytest.mark.parametrize('unit_text, ok', [
    ('CPUUsageNSec=5\nMemoryPeak=70000000\nExecMainStatus=0\nResult=success\n', True),
    ('CPUUsageNSec=5\nMemoryPeak=70000000\nExecMainStatus=9\nResult=signal\n', False),
    ('CPUUsageNSec=5\nMemoryPeak=70000000\nExecMainStatus=0\nResult=timeout\n', False),
    ('CPUUsageNSec=5\nMemoryPeak=70000000\nResult=success\n', False),
    ('CPUUsageNSec=5\nMemoryPeak=70000000\nExecMainStatus=0\n', False),
])
def test_cli_probe_requires_a_completed_probe_unit(tmp_path, unit_text, ok):
    directory = _probe_dir(tmp_path, unit_text)
    code, done = _cli(tmp_path, '--probe-verdict', directory)
    probe = json.loads((directory / 'probe.json').read_text())
    assert probe['ok'] is ok and code == (0 if ok else 3), done.stdout
    if not ok:
        assert any('probe unit did not complete' in r for r in probe['reasons'])


# ---- 4117030873: counts and workload against the fixed r2 §4 values, never derived

def _drift_to_depth_3(directory, arm, repeats=(1, 2, 3, 4, 5, 0)):
    panels = 4 if arm == 'forced' else 2
    for r in repeats:
        path = directory / ('%s-%d.json' % (arm, r))
        row = json.loads(path.read_text())
        replays = 2 + panels * (1 + 3)
        row['workload'].update(paths_per_panel=3, expected={'panels': panels, 'expanded': arm == 'forced',
                                                             'replays': replays, 'proofs': 1 + panels,
                                                             'verify_for': replays + 1})
        if r == 0:   # counts that agree with the drifted request's own derivation
            row['counts'] = {'replay': replays, 'proof': 1 + panels, 'verify_for': replays + 1}
        path.write_text(json.dumps(row))


def test_cli_drifted_fixture_depth_fails_counts_and_shape(tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _drift_to_depth_3(directory, 'forced')
    code, record, done = _cli_job(tmp_path, directory)
    reasons = record['verdict']['reasons']
    assert any(r.startswith('H-COUNTS: forced-0') for r in reasons)
    assert any(r.startswith('H-SHAPE: forced-2') and 'paths_per_panel=3' in r for r in reasons)
    assert code == 4, done.stdout


@pytest.mark.parametrize('field, value', [('horizon_sessions', 6), ('expanded_panels', 5), ('outer_months', 5),
                                          ('within_pp', 0.02), ('budget_seconds', 60.0)])
def test_cli_workload_off_the_fixed_r2_values_is_h_shape(tmp_path, field, value):
    directory = _linux_job(tmp_path / 'a')
    path = directory / 'prescribed-3.json'
    row = json.loads(path.read_text())
    row['workload'][field] = value
    path.write_text(json.dumps(row))
    code, record, done = _cli_job(tmp_path, directory)
    assert any(r.startswith('H-SHAPE: prescribed-3') and field in r for r in record['verdict']['reasons'])
    assert code == 4


def test_counts_oracle_is_the_r2_literal_table(h):
    assert h.EXPECTED_COUNTS == {'forced': {'replays': 14, 'proofs': 5, 'verify_for': 15},
                                 'prescribed': {'replays': 8, 'proofs': 3, 'verify_for': 9}}


# ---- sweep: other preconditions and oracles

def test_pinned_fixture_hashes_match_this_revision(h):
    for name, pinned in h.PINNED_FIXTURE_SHA256.items():
        assert h._sha256_file(ROOT / name) == pinned, name


def test_changed_fixture_is_h_shape(h, tmp_path, monkeypatch):
    monkeypatch.setitem(h.PINNED_FIXTURE_SHA256, 'tests/ops/qualification/composition_fixture.py', '0' * 64)
    code, record = _summarize_job(h, _linux_job(tmp_path / 'a'))
    assert any(r.startswith('H-SHAPE') and 'composition_fixture.py' in r for r in record['verdict']['reasons'])
    assert code == 4


def test_cli_thread_environment_not_pinned_is_h_shape(tmp_path):
    directory = _linux_job(tmp_path / 'a')
    path = directory / 'forced-4.json'
    row = json.loads(path.read_text())
    row['environment']['thread_env']['OMP_NUM_THREADS'] = None
    path.write_text(json.dumps(row))
    code, record, done = _cli_job(tmp_path, directory)
    assert any(r.startswith('H-SHAPE: forced-4') and 'thread environment' in r for r in record['verdict']['reasons'])
    assert code == 4


def test_cli_repeat_run_in_another_unit_is_h_shape(tmp_path):
    directory = _linux_job(tmp_path / 'a')
    _edit_row(directory, 'forced-4.json', unit='fp-s5pa-1b-forced-3')
    code, record, done = _cli_job(tmp_path, directory)
    assert any(r.startswith('H-SHAPE: forced-4') and 'unit' in r for r in record['verdict']['reasons'])
    assert code == 4
