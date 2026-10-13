"""Review regressions use synthetic files and transports; never activate Azure."""
import json
import os
from pathlib import Path
import shutil
import sys
import time
from types import SimpleNamespace
import zipfile

import pytest

from scripts.azure_jobs import contract, guest, runner, watchdog
from scripts.azure_jobs.control import atomic, Ledger, locked


def spec(environment='operations'):
    return dict(job_id='job', commit='a' * 40, command=[
        'scripts/fp.py' if environment == 'operations' else 'entry.py', 'test'],
        environment=environment, max_wall_seconds=60, expected_outputs=['out'],
        authority='synthetic review regression', private_inputs=[])


def completed():
    return dict(status='completed', exit_code=0, verification_exit_code=0,
                source_stable=True, capture_complete=True, report_errors=[],
                cpu_seconds=3600, wall_seconds=1, finished_at=time.time())


def disk_job(tmp_path, *, environment='operations', status='completed'):
    job = tmp_path / 'jobs/job'; repo = tmp_path / 'repos/job'
    job.mkdir(parents=True); repo.mkdir(parents=True)
    (repo / 'out').write_text('synthetic output')
    value = spec(environment)
    entry = repo / value['command'][0]
    entry.parent.mkdir(parents=True, exist_ok=True)
    entry.write_text('pass')
    record = completed()
    record['launcher_records'] = [launcher(repo)]
    record['status'] = status
    if status != 'completed':
        record.update(exit_code=130, verification_exit_code=130)
    atomic(job / 'record.json', record); atomic(job / 'spec.json', value)
    return job, repo, value, record


def launcher(repo):
    directory = repo / '.cache/fp-verification/run'
    directory.mkdir(parents=True, exist_ok=True)
    files = {'stdout.txt': 'captured stdout', 'stderr.txt': '',
             'junit.xml': '<testsuite tests="1" failures="0" errors="0"/>',
             'extra.txt': 'retained extra capture'}
    for name, body in files.items():
        (directory / name).write_text(body)
    record = completed()
    record.update(artifacts={n: contract.sha256(directory / n) for n in files},
                  junit=[{'file': 'junit.xml'}])
    atomic(directory / 'record.json', record)
    return '.cache/fp-verification/run/record.json'


def execution(tmp_path, monkeypatch, *, environment='operations'):
    job, repo, value, _ = disk_job(tmp_path, environment=environment)
    (job / 'record.json').unlink()  # Fresh execution rather than replay protection.
    calls = []
    monkeypatch.setattr(guest, 'checkout', lambda *a: None)
    monkeypatch.setattr(guest, 'environment', lambda *a: (Path(sys.executable), tmp_path / 'env', 'lock'))
    monkeypatch.setattr(guest, 'bounded_snapshot', lambda *a, **k: {'commit': 'a' * 40, 'status': ''})
    def run(*args, **kwargs):
        calls.append(args[0]); return completed()
    monkeypatch.setattr(guest, 'run_tree', run)
    monkeypatch.setattr(guest, 'upload', lambda *a: None)
    for key in ('PATH', 'VIRTUAL_ENV', 'PYTHONPATH', 'PYTHONHOME', 'FP_VERIFICATION_ID'):
        if key in os.environ:
            monkeypatch.setenv(key, os.environ[key])
        else:
            monkeypatch.delenv(key, raising=False)
    config = {'guest_root': str(tmp_path), 'deadline': time.time() + 600, 'git': 'git'}
    return job, repo, value, config, calls


@pytest.mark.parametrize('entry', ['-c', '-m', '-', '--help', './', 'nested/../entry.py'])
def test_operations_entrypoint_rejects_nonlauncher_syntax(entry):
    value = spec(); value['command'] = [entry, 'synthetic argument']
    with pytest.raises(ValueError):
        contract.validate(value)


@pytest.mark.parametrize('kind', ['missing', 'directory', 'symlink'])
def test_execute_refuses_entrypoint_outside_pinned_file_boundary(tmp_path, monkeypatch, kind):
    job, repo, value, config, calls = execution(tmp_path, monkeypatch)
    entry = repo / 'scripts/fp.py'; entry.unlink()
    if kind == 'directory':
        entry.mkdir()
    elif kind == 'symlink':
        outside = tmp_path / 'outside.py'; outside.write_text('pass')
        try:
            entry.symlink_to(outside)
        except OSError:
            pytest.skip('test host cannot create symlinks')
    guest.execute(config, value)
    assert calls == [], 'untrusted entrypoint reached workload launch'
    assert runner.read(job / 'record.json')['status'] == 'failed'


def test_operations_launcher_keeps_arguments(tmp_path, monkeypatch):
    job, repo, value, config, calls = execution(tmp_path, monkeypatch)
    value['command'] += ['-m', 'ordinary-script-argument']
    guest.execute(config, value)
    assert len(calls) == 1
    assert Path(calls[0][2]).resolve() == (repo / 'scripts/fp.py').resolve()
    assert calls[0][-2:] == ['-m', 'ordinary-script-argument']
    assert contract.verified(runner.read(job / 'record.json'))


def test_output_removed_after_inventory_cannot_publish_completed(tmp_path, monkeypatch):
    job, repo, value, config, _ = execution(tmp_path, monkeypatch)
    original = guest.inventory
    checked = []
    def remove_after_check(root, outputs, **kwargs):
        rows = original(root, outputs, **kwargs)
        if not checked:
            checked.append(True); (repo / 'out').unlink()
        return rows
    monkeypatch.setattr(guest, 'inventory', remove_after_check)
    guest.execute(config, value)
    record = runner.read(job / 'record.json')
    assert record['status'] == 'failed'
    assert not contract.verified(record)
    rows = runner.unpack(job / 'results.zip', tmp_path / 'unpacked')
    assert 'runner/record.json' in rows and 'out' not in rows


@pytest.mark.parametrize('publisher', ['bundle', 'recover'])
def test_completed_publishers_require_outputs(tmp_path, monkeypatch, publisher):
    job, repo, value, record = disk_job(tmp_path)
    (repo / 'out').unlink()
    monkeypatch.setattr(guest, 'upload', lambda *a: pytest.fail('published incomplete completion'))
    monkeypatch.setattr(watchdog, 'upload', lambda *a: pytest.fail('published incomplete completion'))
    monkeypatch.setattr(watchdog, 'terminate_tree', lambda *a: True)
    with pytest.raises(ValueError, match='output'):
        if publisher == 'bundle':
            guest.bundle(job, repo, ['out'], partial=True)
        else:
            watchdog.recover({'guest_root': str(tmp_path)}, {'job_id': 'job'}, 'guest supervisor lost')
    assert runner.read(job / 'record.json') == record


@pytest.mark.parametrize('status', ['failed', 'interrupted'])
def test_partial_archive_allows_missing_expected_output(tmp_path, status):
    job, repo, value, record = disk_job(tmp_path, status=status)
    (repo / 'out').unlink()
    guest.bundle(job, repo, ['out'], partial=True)
    rows = runner.unpack(job / 'results.zip', tmp_path / 'unpacked')
    assert 'runner/record.json' in rows and 'out' not in rows


def retrieve(tmp_path, monkeypatch, job):
    cfg = {'state_dir': str(tmp_path / 'host')}
    Ledger(Path(cfg['state_dir']) / 'ledger.json', initial_seconds=0)
    descriptor = {'sha256': contract.sha256(job / 'results.zip'),
                  'bytes': (job / 'results.zip').stat().st_size}
    def download(config, action, name, target):
        if name.endswith('/archive.json'):
            atomic(target, descriptor)
        else:
            shutil.copyfile(job / 'results.zip', target)
    monkeypatch.setattr(runner, 'blob', download)
    return runner.results(cfg, 'job')


def alter_archive(job, *, remove=None, change=None):
    with zipfile.ZipFile(job / 'results.zip') as archive:
        files = {n: archive.read(n) for n in archive.namelist()}
    rows = json.loads(files['manifest.json'])
    if remove:
        files.pop(remove); rows.pop(remove)
    if change:
        import hashlib
        name, body = change
        files[name] = body
        rows[name] = {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
    files['manifest.json'] = json.dumps(rows).encode()
    with zipfile.ZipFile(job / 'results.zip', 'w') as archive:
        for name, body in files.items():
            archive.writestr(name, body)


def test_retrieval_rejects_missing_output_even_with_stale_extracted_copy(tmp_path, monkeypatch):
    job, repo, value, record = disk_job(tmp_path)
    guest.bundle(job, repo, ['out'], partial=True)
    alter_archive(job, remove='out')
    old = tmp_path / 'host/results/job/files/out'
    old.parent.mkdir(parents=True); old.write_text('stale output')
    with pytest.raises(ValueError, match='output'):
        retrieve(tmp_path, monkeypatch, job)


def test_operations_automatically_bundle_launcher_captures_and_verify_retrieval(tmp_path, monkeypatch):
    job, repo, value, config, calls = execution(tmp_path, monkeypatch, environment='operations')
    path = launcher(repo)
    guest.execute(config, value)
    result = retrieve(tmp_path, monkeypatch, job)
    assert result['workload_verified']
    root = Path(result['directory']) / 'files'
    for name in ('record.json', 'stdout.txt', 'stderr.txt', 'junit.xml', 'extra.txt'):
        assert (root / Path(path).parent / name).is_file()


@pytest.mark.parametrize('damage', ['missing_record', 'missing_capture', 'tampered_junit', 'no_record_list'])
def test_retrieval_rejects_incomplete_launcher_proof(tmp_path, monkeypatch, damage):
    job, repo, value, record = disk_job(tmp_path, environment='operations')
    path = launcher(repo); record['launcher_records'] = [path]
    atomic(job / 'record.json', record)
    # Explicitly include cache so pre-fix bundling also makes this fixture.
    guest.bundle(job, repo, ['out', '.cache/fp-verification'], partial=True)
    if damage == 'missing_record':
        alter_archive(job, remove=path)
    elif damage == 'missing_capture':
        alter_archive(job, remove=(Path(path).parent / 'stdout.txt').as_posix())
    elif damage == 'tampered_junit':
        alter_archive(job, change=((Path(path).parent / 'junit.xml').as_posix(), b'not original junit'))
    else:
        record.pop('launcher_records')
        alter_archive(job, change=('runner/record.json', json.dumps(record).encode()))
    with pytest.raises(ValueError, match='launcher'):
        retrieve(tmp_path, monkeypatch, job)


@pytest.mark.parametrize('known', [False, True])
def test_recovery_sessions_report_only_original_missing_cpu(tmp_path, known):
    now = time.time()
    atomic(tmp_path / 'jobs/job/session.json', {'mode': 'execute', 'job_id': 'job'})
    for name in ('recover-one', 'recover-two'):
        atomic(tmp_path / 'jobs' / name / 'session.json',
               {'mode': 'republish', 'source_job_id': 'job', 'job_id': name})
    atomic(tmp_path / 'jobs/recover-real-workload/session.json', {'mode': 'execute'})
    if known:
        atomic(tmp_path / 'results/job/files/runner/record.json', completed())
    result = runner.cpu_report({'state_dir': str(tmp_path)}, now=now)
    assert result['jobs_without_cpu_results'] == (['recover-real-workload'] if known else ['job', 'recover-real-workload'])
    assert result['week_process_cpu_hours'] == (1 if known else 0)


@pytest.mark.parametrize('phase', ['checkout', 'environment'])
def test_preparation_cancel_before_command_never_starts_subprocess(tmp_path, monkeypatch, phase):
    repo = tmp_path / 'repo'; repo.mkdir()
    (repo / 'requirements-ops.lock').write_text('synthetic lock')
    cancel = tmp_path / 'cancel'; cancel.touch()
    calls = []
    def old_run(command, **kwargs):
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout='a' * 40 if 'rev-parse' in command else '', stderr='')
    monkeypatch.setattr(guest.subprocess, 'run', old_run)
    monkeypatch.setattr(guest.WindowsJob, 'create', lambda **k: pytest.fail('created job after cancel'))
    config = dict(guest_root=str(tmp_path), python='python', git='git',
                  preparation_deadline=time.time() + 60,
                  preparation=dict(output=tmp_path / 'preparation', cancel_path=cancel, job_name='job'))
    with pytest.raises(InterruptedError, match='cancel'):
        if phase == 'checkout':
            guest.checkout(config, 'a' * 40, repo)
        else:
            guest.environment(config, spec(), repo)
    assert not calls


def test_preparation_cancel_during_command_owns_tree_and_keeps_capture(tmp_path, monkeypatch):
    repo = tmp_path / 'repo'; repo.mkdir()
    cancel = tmp_path / 'jobs/job/cancel'
    cancel.parent.mkdir(parents=True)
    events = []
    owned = SimpleNamespace(active_processes=lambda: 0, close=lambda: events.append('close'))
    owned.terminate = lambda: events.append('terminate')
    def create(**kwargs):
        assert kwargs['name'] == 'Local\\FP-Offline-job'
        events.append('create'); return owned
    def spawn(command, cwd, stdout, stderr, job):
        assert job is owned
        stdout.write(b'partial preparation'); stdout.flush()
        # The live supervisor owns the lock; the independent watchdog must still
        # stop this preparation Job Object and leave finalization to its owner.
        assert watchdog.recover({'guest_root': str(tmp_path)}, {'job_id': 'job'}, 'cancelled') is False
        return SimpleNamespace(pid=123, poll=lambda: 0 if 'terminate' in events else None,
                               wait=lambda **kwargs: 0)
    monkeypatch.setattr(guest.WindowsJob, 'create', create)
    monkeypatch.setattr(guest, 'spawn_provider', spawn)
    monkeypatch.setattr(guest, 'accounting', lambda job: 0)
    def stop(name):
        assert name == 'job'; owned.terminate(); return True
    monkeypatch.setattr(watchdog, 'terminate_tree', stop)
    monkeypatch.setattr(watchdog, 'upload', lambda *a: pytest.fail('concurrent recovery'))
    monkeypatch.setattr(guest.subprocess, 'run', lambda *a, **k: SimpleNamespace(returncode=0, stdout='a' * 40 if 'rev-parse' in a[0] else '', stderr=''))
    config = dict(git='git', preparation_deadline=time.time() + 60,
                  preparation=dict(output=tmp_path / 'preparation', cancel_path=cancel, job_name='job'))
    with locked(tmp_path / 'guest.lock'):
        with pytest.raises(InterruptedError, match='cancel'):
            guest.checkout(config, 'a' * 40, repo)
    assert events == ['create', 'terminate', 'close']
    assert [p.read_text() for p in (tmp_path / 'preparation').glob('*/stdout.log')] == ['partial preparation']


def test_cancelled_preparation_preserves_interrupted_record_and_logs(tmp_path, monkeypatch):
    job, repo, value, config, calls = execution(tmp_path, monkeypatch)
    def cancel(*args):
        path = job / 'preparation/step/stdout.log'
        path.parent.mkdir(parents=True); path.write_text('partial setup')
        raise InterruptedError('cancelled')
    monkeypatch.setattr(guest, 'checkout', cancel)
    guest.execute(config, value)
    record = runner.read(job / 'record.json')
    assert record['status'] == 'interrupted' and record['exit_code'] == 130
    assert not calls
    rows = runner.unpack(job / 'results.zip', tmp_path / 'unpacked')
    assert 'runner/preparation/step/stdout.log' in rows


def test_empty_expected_directory_cannot_attest_completed_archive(tmp_path):
    job, repo, value, record = disk_job(tmp_path)
    (repo / 'out').unlink(); (repo / 'out').mkdir()
    with pytest.raises(ValueError, match='output'):
        guest.bundle(job, repo, ['out'], partial=True)


@pytest.mark.parametrize('publisher', ['recover'])
def test_recovery_publishers_include_launcher_directory(tmp_path, monkeypatch, publisher):
    job, repo, value, record = disk_job(tmp_path, environment='operations')
    path = launcher(repo); record['launcher_records'] = [path]
    atomic(job / 'record.json', record)
    monkeypatch.setattr(guest, 'upload', lambda *a: None)
    monkeypatch.setattr(watchdog, 'upload', lambda *a: None)
    monkeypatch.setattr(watchdog, 'terminate_tree', lambda *a: True)
    watchdog.recover({'guest_root': str(tmp_path)}, {'job_id': 'job'}, 'guest supervisor lost')
    result = retrieve(tmp_path, monkeypatch, job)
    assert result['workload_verified']
    assert (Path(result['directory']) / 'files' / Path(path).parent / 'stdout.txt').read_text() == 'captured stdout'


@pytest.mark.parametrize('damage', ['no_artifacts', 'missing_stdout', 'bad_digest', 'escaping_artifact', 'escaping_record', 'missing_junit', 'malformed_junit'])
def test_completed_bundle_rejects_malformed_launcher_evidence(tmp_path, damage):
    job, repo, value, record = disk_job(tmp_path, environment='operations')
    path = launcher(repo); record['launcher_records'] = [path]
    original = runner.read(repo / path)
    if damage == 'no_artifacts':
        original.pop('artifacts')
    elif damage == 'missing_stdout':
        (repo / Path(path).parent / 'stdout.txt').unlink()
    elif damage == 'bad_digest':
        original['artifacts']['stdout.txt'] = '0' * 64
    elif damage == 'escaping_artifact':
        original['artifacts']['../outside'] = '0' * 64
    elif damage == 'escaping_record':
        record['launcher_records'] = ['../outside/record.json']
    elif damage == 'malformed_junit':
        original['junit'][0]['file'] = []
    else:
        original['junit'][0]['file'] = 'absent.xml'
    atomic(repo / path, original); atomic(job / 'record.json', record)
    with pytest.raises(ValueError):
        guest.bundle(job, repo, ['out'], partial=True)


def test_retrieval_stale_launcher_capture_does_not_prove_current_archive(tmp_path, monkeypatch):
    job, repo, value, record = disk_job(tmp_path, environment='operations')
    path = launcher(repo); record['launcher_records'] = [path]
    atomic(job / 'record.json', record)
    guest.bundle(job, repo, ['out'], partial=True)
    capture = (Path(path).parent / 'stdout.txt').as_posix()
    alter_archive(job, remove=capture)
    stale = tmp_path / 'host/results/job/files' / capture
    stale.parent.mkdir(parents=True, exist_ok=True); stale.write_text('captured stdout')
    with pytest.raises(ValueError, match='launcher'):
        retrieve(tmp_path, monkeypatch, job)


def test_malformed_recovery_mapping_stays_missing_cpu(tmp_path):
    atomic(tmp_path / 'jobs/recover-broken/session.json', {'mode': 'republish', 'source_job_id': None})
    assert runner.cpu_report({'state_dir': str(tmp_path)})['jobs_without_cpu_results'] == ['recover-broken']


@pytest.mark.skipif(os.name != 'nt', reason='native Windows preparation Job Object')
def test_windows_preparation_cancel_terminates_owned_step_and_retains_capture(tmp_path):
    import threading
    import uuid
    marker = tmp_path / 'cancel'
    entered = tmp_path / 'entered'
    natural_completion = tmp_path / 'natural-completion'
    stopped = threading.Event()
    cancelled_at = []
    def cancel_started_step():
        limit = time.monotonic() + 10
        while not entered.exists() and time.monotonic() < limit:
            if stopped.wait(0.01):
                return
        if entered.exists():
            cancelled_at.append(time.monotonic())
            marker.touch()
    trigger = threading.Thread(target=cancel_started_step)
    trigger.start()
    try:
        with pytest.raises(InterruptedError, match='cancel'):
            guest.checked([sys.executable, '-c',
                           "import time; from pathlib import Path; print('partial setup', flush=True); "
                           f"Path({str(entered)!r}).touch(); time.sleep(60); Path({str(natural_completion)!r}).touch()"],
                          timeout=20, preparation=dict(output=tmp_path / 'steps', cancel_path=marker,
                                                       job_name='prep-' + uuid.uuid4().hex))
    finally:
        stopped.set()
        trigger.join(timeout=2)
    assert cancelled_at and time.monotonic() - cancelled_at[0] < 10
    assert not natural_completion.exists()
    assert [p.read_text().strip() for p in (tmp_path / 'steps').glob('*/stdout.log')] == ['partial setup']
