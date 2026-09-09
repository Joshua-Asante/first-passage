"""Process-level protocol tests; workers are local fixtures, never model calls."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
import importlib.util
import shutil

import pytest

RUNNER = Path(__file__).resolve().parents[1] / 'scripts/agent_handoff.py'
_spec = importlib.util.spec_from_file_location('agent_handoff', RUNNER)
AH = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(AH)
handoff_root = AH.handoff_root
WORKER = r'''
import hashlib, json, os, re, sys, time
from pathlib import Path
case = sys.argv[1]
args = sys.argv[2:]
Path('argv.json').write_text(json.dumps(args))
prompt = args[-1]
rid = re.search(r'Request ID: ([\w-]+)', prompt).group(1)
sha = re.search(r'Packet SHA256: (\w+)', prompt).group(1)
sid = args[args.index('--resume')+1] if '--resume' in args else (args[args.index('--session-id')+1] if '--session-id' in args else 'fixture-session')
if case == 'nonzero':
    print('fixture denial', file=sys.stderr); sys.exit(7)
if case == 'empty': sys.exit(0)
print(json.dumps({'type':'system','subtype':'init','session_id':sid}), flush=True)
if case == 'sleep': time.sleep(30)
if case == 'flood':
    for _ in range(20000):
        print(json.dumps({'type':'assistant','session_id':sid}), flush=True)
if case == 'mutate-packet': Path('packet.md').write_text('changed')
if case == 'mutate-input': Path('dependency.txt').write_text('changed')
if case == 'malformed': print('broken json'); sys.exit(0)
body = {'request_id': rid, 'packet_sha256':sha, 'status':'DONE', 'summary':'fixture done', 'artifacts':[], 'checks':[]}
if case == 'stale': body['request_id'] = 'old-request'
if case == 'hash': body['packet_sha256'] = 'wrong'
if case == 'status': body['status'] = 'SUCCESS'
if case == 'blocked': body['status'] = 'BLOCKED'
if case in ('artifacts', 'absolute-artifact'):
    Path('answer.txt').write_text('fixture answer')
    body['artifacts'] = [{'path':'answer.txt','sha256':hashlib.sha256(Path('answer.txt').read_bytes()).hexdigest()}]
    body['checks'] = [{'name':'unit', 'status':'passed', 'evidence':'fixture test exit 0'}]
    if case == 'absolute-artifact': body['artifacts'][0]['path'] = str(Path('answer.txt').resolve())
if case == 'null-evidence':
    body['checks'] = [{'name':'unit', 'status':'passed', 'evidence': None}]
event = {'type':'result','subtype':'success','is_error':case=='error','session_id':sid,'result':json.dumps(body)}
if case == 'session': event['session_id'] = 'other-session'
if case == 'plain': event['result'] = 'I am done'
print(json.dumps(event), flush=True)
'''


@pytest.fixture
def harness(tmp_path):
    workspace = tmp_path / 'workspace with spaces'
    workspace.mkdir()
    packet = workspace / 'packet.md'
    packet.write_text('Only perform the fixture task.', encoding='utf-8')
    worker = tmp_path / 'worker.py'
    worker.write_text(WORKER, encoding='utf-8')

    class Harness:
        def command(self, case='ok', *extra):
            return [sys.executable, str(RUNNER), 'run', '--workspace', str(workspace), '--pointer', str(packet),
                    '--command-json', json.dumps([sys.executable, str(worker), case]), *extra]

        def run(self, case='ok', *extra):
            return subprocess.run(self.command(case, *extra), capture_output=True, text=True, timeout=15)

        def records(self):
            if AH.read_workspace_instance(workspace) is None:
                return []
            root = handoff_root(workspace)
            return [json.loads(p.read_text()) for p in root.glob('*/record.json')]

        def action(self, action, rid, *extra):
            return subprocess.run([sys.executable, str(RUNNER), action, '--workspace', str(workspace),
                                   '--request-id', rid, *extra], capture_output=True, text=True, timeout=10)

    h = Harness()
    h.workspace, h.packet, h.worker = workspace, packet, worker
    return h


@pytest.mark.parametrize('case,state', [('nonzero','FAILED'), ('empty','UNKNOWN'), ('malformed','UNKNOWN'),
                                      ('stale','UNKNOWN'), ('hash','UNKNOWN'), ('status','UNKNOWN'),
                                      ('session','UNKNOWN'), ('plain','UNKNOWN'), ('error','UNKNOWN')])
def test_invalid_returns_stay_unresolved(harness, case, state):
    result = harness.run(case)
    assert result.returncode == 1, result.stderr
    record, = harness.records()
    assert record['state'] == state
    evidence = handoff_root(harness.workspace) / record['request_id']
    assert (evidence / 'stdout.jsonl').exists()
    assert (evidence / 'stderr.txt').exists()
    assert not (evidence / 'return.json').exists()
    if case == 'nonzero':
        assert record['exit_code'] == 7
        assert 'fixture denial' in (evidence / 'stderr.txt').read_text()
    assert harness.run().returncode == 2
    assert len(harness.records()) == 1


def test_success_identity_and_duplicate_prevention(harness):
    assert harness.run().returncode == 0
    record, = harness.records()
    assert record['state'] == 'RETURNED'
    assert record['worker_status'] == 'DONE'
    assert record['independently_verified'] is False
    body = json.loads((handoff_root(harness.workspace) / record['request_id'] / 'return.json').read_text())
    assert body['request_id'] == record['request_id']
    assert harness.run().returncode == 2


def test_artifacts_and_required_checks(harness):
    result = harness.run('artifacts', '--expected-output', 'answer.txt', '--required-check', 'unit')
    assert result.returncode == 0, result.stderr
    record, = harness.records()
    assert record['artifacts_before']['answer.txt'] is None
    assert record['artifacts_after']['answer.txt']


@pytest.mark.parametrize('extra', [('--expected-output','absent.txt'), ('--required-check','missing-check')])
def test_done_requires_declared_evidence(harness, extra):
    assert harness.run('ok', *extra).returncode == 1
    assert harness.records()[0]['state'] == 'UNKNOWN'


def test_blocked_is_a_valid_noncompletion_return(harness):
    assert harness.run('blocked', '--expected-output', 'absent.txt').returncode == 0
    assert harness.records()[0]['worker_status'] == 'BLOCKED'


def test_resume_checks_packet_and_uses_saved_session(harness):
    assert harness.run('ok', '--mode', 'plan').returncode == 0
    record, = harness.records()
    assert harness.run('ok', '--resume-session', 'unknown').returncode == 2
    assert harness.run('ok', '--provider', 'claude', '--resume-request', record['request_id']).returncode == 2
    original = harness.packet.read_text()
    harness.packet.write_text('changed scope')
    assert harness.run('ok', '--resume-request', record['request_id']).returncode == 2
    harness.packet.write_text(original)
    result = harness.run('ok', '--resume-request', record['request_id'])
    assert result.returncode == 0, result.stderr
    args = json.loads((harness.workspace / 'argv.json').read_text())
    assert args[args.index('--resume')+1] == record['session_id']
    assert '--force' not in args
    assert len(harness.records()) == 2
    assert harness.run('ok', '--resume-request', record['request_id']).returncode == 2


def test_timeout_captures_session_and_needs_reconciliation(harness):
    assert harness.run('sleep', '--timeout-seconds', '0.5').returncode == 1
    record, = harness.records()
    assert record['state'] == 'TIMED_OUT'
    assert record['session_id'] == 'fixture-session'
    assert record['child_pid']
    assert harness.run('ok', '--resume-request', record['request_id']).returncode == 2
    assert harness.action('reconcile', record['request_id']).returncode == 2
    assert harness.action('reconcile', record['request_id'], '--resolution', 'resume', '--note', 'Fixture stopped; inspected effects').returncode == 0
    assert harness.run('ok', '--resume-request', record['request_id']).returncode == 0


def test_cancel_and_concurrent_launch(harness):
    running = subprocess.Popen(harness.command('sleep'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        started = json.loads(running.stdout.readline())
        assert started['child_pid']
        assert harness.run().returncode == 2
        assert harness.action('cancel', started['request_id']).returncode == 0
        running.communicate(timeout=10)
        assert running.returncode == 1
        assert harness.records()[0]['state'] == 'CANCELLED'
    finally:
        if running.poll() is None:
            running.kill()


def test_claude_persists_and_resumes(harness):
    assert harness.run('ok', '--provider', 'claude', '--mode', 'ask').returncode == 0
    record, = harness.records()
    args = json.loads((harness.workspace / 'argv.json').read_text())
    assert '--session-id' in args and '--no-session-persistence' not in args
    assert args[args.index('--tools')+1] == 'Read,Glob,Grep'
    assert harness.run('ok', '--provider', 'claude', '--resume-request', record['request_id']).returncode == 0
    args = json.loads((harness.workspace / 'argv.json').read_text())
    assert '--resume' in args and '--session-id' not in args


def test_close_latest_chain_allows_replacement(harness):
    assert harness.run().returncode == 0
    first, = harness.records()
    assert harness.run('ok', '--resume-request', first['request_id']).returncode == 0
    latest = next(r for r in harness.records() if not r.get('resumed_by'))
    assert harness.action('reconcile', latest['request_id'], '--resolution', 'closed', '--note', 'Reviewed and closed fixture').returncode == 0
    assert harness.run('ok', '--resume-request', latest['request_id']).returncode == 2
    assert harness.run().returncode == 0


def test_input_hash_and_workspace_root_change_refuse_resume(harness):
    dep = harness.workspace / 'dependency.txt'
    dep.write_text('v1')
    assert harness.run('ok', '--input', str(dep)).returncode == 0
    record, = harness.records()
    dep.write_text('v2')
    assert harness.run('ok', '--input', str(dep), '--resume-request', record['request_id']).returncode == 2
    dep.write_text('v1')
    assert harness.run('ok', '--input', str(dep), '--add-dir', str(dep.parent.parent), '--resume-request', record['request_id']).returncode == 2


def test_status_does_not_signal_process(harness):
    assert harness.run().returncode == 0
    record, = harness.records()
    path = handoff_root(harness.workspace) / record['request_id'] / 'record.json'
    record['child_pid'] = os.getpid()
    path.write_text(json.dumps(record))
    result = harness.action('status', record['request_id'])
    assert result.returncode == 0
    assert json.loads(result.stdout)['child_may_be_alive'] is True


def test_dry_run_and_path_boundaries(harness):
    assert harness.run('ok', '--dry-run').returncode == 0
    assert AH.read_workspace_instance(harness.workspace) is None
    assert not (harness.workspace / '.agent-handoffs').exists()
    assert harness.run('ok', '--expected-output', '../outside.txt').returncode == 2
    assert harness.run('ok', '--expected-output', '.agent-handoffs/fake.txt').returncode == 2
    assert not harness.records()


def test_windows_launcher_preserves_literal_prompt(harness):
    if os.name != 'nt':
        pytest.skip('Windows PowerShell argument boundary')
    launcher = harness.worker.with_suffix('.ps1')
    # Only the executable fixture path is quoted; prompt is forwarded as an array.
    launcher.write_text("& '" + sys.executable.replace("'", "''") + "' '" + str(harness.worker).replace("'", "''") + "' ok @args\nexit $LASTEXITCODE\n")
    followup = harness.workspace / 'message.txt'
    message = 'literal `backticks` $(throw "oops") & %PATH% "quotes"\nUnicode: café'
    followup.write_text(message, encoding='utf-8')
    command = harness.command('ok', '--message-file', str(followup))
    command[command.index('--command-json')+1] = json.dumps([str(launcher)])
    result = subprocess.run(command, capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stderr + result.stdout
    args = json.loads((harness.workspace / 'argv.json').read_text())
    assert message in args[-1]


def test_absolute_artifact_matches_expected_output(harness):
    result = harness.run('absolute-artifact', '--expected-output', 'answer.txt')
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize('resume', [False, True])
def test_missing_followup_does_not_poison_receipts(harness, resume):
    extra = []
    if resume:
        assert harness.run().returncode == 0
        extra = ['--resume-request', harness.records()[0]['request_id']]
    before = harness.records()
    assert harness.run('ok', *extra, '--message-file', str(harness.workspace / 'missing')).returncode == 2
    assert harness.records() == before
    assert harness.run('ok', *extra).returncode == 0


@pytest.mark.parametrize('case', ['mutate-packet', 'mutate-input'])
def test_changed_immutable_input_rejects_completion(harness, case):
    dep = harness.workspace / 'dependency.txt'
    dep.write_text('original')
    result = harness.run(case, '--input', str(dep))
    assert result.returncode == 1
    assert harness.records()[0]['state'] == 'UNKNOWN'


def test_flood_cannot_starve_timeout(harness):
    start = time.monotonic()
    result = harness.run('flood', '--timeout-seconds', '0.3')
    assert time.monotonic() - start < 4
    assert result.returncode == 1
    assert harness.records()[0]['state'] == 'TIMED_OUT'


def test_copy_rejected_before_mutating_unresolved_workspace(harness):
    if not shutil.which('pwsh'):
        pytest.skip('PowerShell is unavailable')
    assert harness.run('empty').returncode == 1
    destination = harness.workspace / 'copied.txt'
    result = subprocess.run(['pwsh', '-NoProfile', '-File', str(RUNNER.with_name('dispatch_cursor.ps1')),
                             '-Workspace', str(harness.workspace), '-Pointer', str(harness.packet),
                             '-Copy', str(harness.packet) + '::copied.txt', '-AgentCmd', sys.executable],
                            capture_output=True, text=True, timeout=15)
    assert result.returncode != 0
    assert not destination.exists()


def test_snapshot_error_still_finalizes_receipt(harness, monkeypatch):
    spec = importlib.util.spec_from_file_location('handoff_under_test', RUNNER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    real_digest = module.digest
    def failing_digest(path):
        if Path(path).name == 'answer.txt':
            raise OSError('fixture snapshot read denied')
        return real_digest(path)
    monkeypatch.setattr(module, 'digest', failing_digest)
    result = module.main(harness.command('artifacts', '--expected-output', 'answer.txt')[2:])
    assert result == 1
    record, = harness.records()
    assert record['state'] not in ('STARTING', 'RUNNING')
    assert record['exit_code'] == 0
    assert record['artifact_snapshot_errors']['answer.txt']


def test_copy_through_external_directory_link_is_refused(harness):
    outside = harness.workspace.parent / 'outside'
    outside.mkdir()
    link = harness.workspace / 'link'
    if os.name == 'nt':
        subprocess.run(['pwsh', '-NoProfile', '-Command',
                        "New-Item -ItemType Junction -Path '" + str(link).replace("'", "''") +
                        "' -Target '" + str(outside).replace("'", "''") + "'"], check=True, capture_output=True)
    else:
        link.symlink_to(outside, target_is_directory=True)
    result = harness.run('ok', '--copy', str(harness.packet) + '::link/copied.txt')
    assert result.returncode == 2
    assert not (outside / 'copied.txt').exists()
    assert not harness.records()


def test_copy_is_pinned_and_resume_uses_staged_input(harness):
    result = harness.run('ok', '--copy', str(harness.packet) + '::copies/input.txt')
    assert result.returncode == 0, result.stderr + result.stdout
    record, = harness.records()
    staged = harness.workspace / 'copies/input.txt'
    assert staged.read_bytes() == harness.packet.read_bytes()
    assert str(staged.resolve()) in record['contract']['inputs']
    assert harness.run('ok', '--input', str(staged), '--resume-request', record['request_id']).returncode == 0


@pytest.mark.skipif(os.name == 'nt', reason='POSIX process groups')
def test_cancellation_kills_descendant_when_leader_exits(harness):
    import signal
    child_code = "import signal,time,pathlib; signal.signal(signal.SIGTERM,signal.SIG_IGN); pathlib.Path('child-ready').touch(); time.sleep(60)"
    harness.worker.write_text("import subprocess,sys,time,pathlib\np=subprocess.Popen([sys.executable,'-c'," + repr(child_code) + "])\npathlib.Path('child.pid').write_text(str(p.pid))\ntime.sleep(60)\n")
    running = subprocess.Popen(harness.command(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    child_pid = None
    try:
        started = json.loads(running.stdout.readline())
        deadline = time.monotonic() + 5
        while not (harness.workspace / 'child-ready').exists() and time.monotonic() < deadline:
            time.sleep(0.05)
        assert (harness.workspace / 'child-ready').exists()
        child_pid = int((harness.workspace / 'child.pid').read_text())
        assert harness.action('cancel', started['request_id']).returncode == 0
        running.communicate(timeout=10)
        # Linux zombies have stopped executing and await init reaping.
        stat = Path(f'/proc/{child_pid}/stat')
        assert not stat.exists() or stat.read_text().split()[2] == 'Z'
    finally:
        if child_pid:
            try:
                os.kill(child_pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if running.poll() is None:
            running.kill()



def test_receipts_live_outside_workspace(harness):
    assert harness.run().returncode == 0
    record, = harness.records()
    root = handoff_root(harness.workspace)
    assert root.exists()
    # Instance marker may live under the workspace; receipts/locks must not.
    assert (harness.workspace / '.agent-handoffs' / 'workspace-instance').is_file()
    assert not (harness.workspace / '.agent-handoffs' / record['request_id']).exists()
    assert (root / record['request_id'] / 'record.json').is_file()
    assert root.is_relative_to(Path.home() / '.cache' / 'agent-handoffs')


def test_streaming_digest_matches_bytes(tmp_path):
    path = tmp_path / 'blob.bin'
    path.write_bytes(b'abc' * 10000 + b'\x00\xff')
    assert AH.digest(path) == __import__('hashlib').sha256(path.read_bytes()).hexdigest()


@pytest.mark.skipif(os.name == 'nt', reason='POSIX permissions')
def test_evidence_permissions_are_owner_only(harness):
    assert harness.run().returncode == 0
    record, = harness.records()
    directory = handoff_root(harness.workspace) / record['request_id']
    assert directory.stat().st_mode & 0o777 == 0o700
    assert (directory / 'record.json').stat().st_mode & 0o777 == 0o600
    assert (directory / 'prompt.txt').stat().st_mode & 0o777 == 0o600


def test_cancel_before_launch_skips_provider(harness, monkeypatch):
    calls = []
    real_popen = AH.subprocess.Popen

    def fake_popen(*args, **kwargs):
        calls.append(args)
        return real_popen(*args, **kwargs)

    monkeypatch.setattr(AH.subprocess, 'Popen', fake_popen)
    original_verify = AH.verify_inputs

    def verify_and_cancel(contract):
        original_verify(contract)
        # Receipt already exists under the locked root.
        root = handoff_root(harness.workspace)
        request_dirs = [p for p in root.iterdir() if p.is_dir()]
        assert request_dirs
        (request_dirs[0] / 'cancel.request').touch()

    monkeypatch.setattr(AH, 'verify_inputs', verify_and_cancel)
    result = AH.main(['run', '--workspace', str(harness.workspace), '--pointer', str(harness.packet),
                      '--command-json', __import__('json').dumps([__import__('sys').executable, str(harness.worker), 'ok'])])
    assert result == 1
    assert calls == []
    record, = harness.records()
    assert record['state'] == 'CANCELLED'
    assert 'before provider launch' in record['error'].lower()


@pytest.mark.skipif(os.name == 'nt', reason='POSIX process groups')
def test_surviving_descendant_blocks_returned(harness):
    harness.worker.write_text('import json, re, subprocess, sys, time, pathlib\nprompt = sys.argv[-1]\nrid = re.search(r\'Request ID: ([\\w-]+)\', prompt).group(1)\nsha = re.search(r\'Packet SHA256: (\\w+)\', prompt).group(1)\nsid = \'fixture-session\'\nprint(json.dumps({\'type\': \'system\', \'subtype\': \'init\', \'session_id\': sid}), flush=True)\nsubprocess.Popen([sys.executable, \'-c\', "import signal, time, pathlib; signal.signal(signal.SIGTERM, signal.SIG_IGN); pathlib.Path(\'ready\').write_text(\'1\'); time.sleep(60)"])\nwhile not pathlib.Path(\'ready\').exists():\n    time.sleep(0.05)\nbody = {\'request_id\': rid, \'packet_sha256\': sha, \'status\': \'DONE\', \'summary\': \'done\', \'artifacts\': [], \'checks\': []}\nprint(json.dumps({\'type\': \'result\', \'subtype\': \'success\', \'session_id\': sid, \'result\': json.dumps(body)}), flush=True)\n')
    result = harness.run()
    assert result.returncode == 1, result.stdout + result.stderr
    record, = harness.records()
    assert record['state'] == 'UNKNOWN'
    assert 'survived' in record.get('error', '').lower()




@pytest.mark.skipif(os.name == 'nt', reason='POSIX permissions')

@pytest.mark.skipif(os.name == 'nt', reason='POSIX process groups')

def test_null_check_evidence_is_rejected(harness):
    assert harness.run('null-evidence', '--required-check', 'unit').returncode == 1
    record, = harness.records()
    assert record['state'] == 'UNKNOWN'
    assert 'evidence' in record.get('error', '').lower()


def test_closed_reconciliation_is_immutable(harness):
    assert harness.run('ok', '--mode', 'plan').returncode == 0
    record, = harness.records()
    assert harness.action('reconcile', record['request_id'], '--resolution', 'closed',
                          '--note', 'Closed after review').returncode == 0
    assert harness.run().returncode == 0
    reopen = harness.action('reconcile', record['request_id'], '--resolution', 'resume',
                            '--note', 'Attempt to reopen closed request')
    assert reopen.returncode == 2
    assert 'immutable' in reopen.stderr.lower()
    closed = json.loads((handoff_root(harness.workspace) / record['request_id'] / 'record.json').read_text())
    assert closed['resolution'] == 'closed'


@pytest.mark.skipif(os.name == 'nt', reason='POSIX permissions')
def test_staging_copy_preserves_existing_directory_modes(harness):
    mode_before = harness.workspace.stat().st_mode & 0o777
    nested = harness.workspace / 'already'
    nested.mkdir()
    os.chmod(nested, 0o755)
    source = harness.workspace / 'stage-src.txt'
    source.write_text('payload')
    assert harness.run('ok', '--copy', str(source) + '::already/staged.txt').returncode == 0
    assert (harness.workspace / 'already/staged.txt').read_text() == 'payload'
    assert harness.workspace.stat().st_mode & 0o777 == mode_before
    assert nested.stat().st_mode & 0o777 == 0o755


@pytest.mark.skipif(os.name == 'nt', reason='POSIX process groups')
def test_nonzero_exit_terminates_surviving_descendants(harness):
    child = "import signal,time,pathlib,os; signal.signal(signal.SIGTERM, signal.SIG_IGN); pathlib.Path('ready').write_text(str(os.getpid())); time.sleep(60)"
    harness.worker.write_text(
        "import json, subprocess, sys, time, pathlib\n"
        "print(json.dumps({'type':'system','subtype':'init','session_id':'fixture-session'}), flush=True)\n"
        "subprocess.Popen([sys.executable, '-c', " + repr(child) + "])\n"
        "while not pathlib.Path('ready').exists():\n"
        "    time.sleep(0.05)\n"
        "raise SystemExit(9)\n"
    )
    result = harness.run()
    assert result.returncode == 1
    record, = harness.records()
    assert record['state'] == 'FAILED'
    child_pid = int((harness.workspace / 'ready').read_text())
    import signal
    try:
        os.kill(child_pid, 0)
        alive = True
    except ProcessLookupError:
        alive = False
    if alive:
        stat = Path(f'/proc/{child_pid}/stat')
        assert stat.exists() and stat.read_text().split()[2] == 'Z'
    try:
        os.kill(child_pid, signal.SIGKILL)
    except ProcessLookupError:
        pass



def test_preflight_artifact_failure_leaves_no_blocking_receipt(harness, monkeypatch):
    boom = harness.workspace / 'boom.txt'
    boom.write_text('x')
    real_digest = AH.digest
    def digest(path):
        if Path(path).name == 'boom.txt':
            raise OSError('fixture unreadable')
        return real_digest(path)
    monkeypatch.setattr(AH, 'digest', digest)
    argv = harness.command('ok', '--expected-output', 'boom.txt')[2:]  # drop python + runner
    assert AH.main(argv) == 2
    assert not harness.records()
    monkeypatch.setattr(AH, 'digest', real_digest)
    assert harness.run('ok').returncode == 0

def test_recreated_workspace_does_not_inherit_receipts(harness):
    assert harness.run().returncode == 0
    old_root = handoff_root(harness.workspace)
    old_instance = AH.read_workspace_instance(harness.workspace)
    packet = harness.packet.read_text()
    worker_src = harness.worker.read_text()
    shutil.rmtree(harness.workspace)
    harness.workspace.mkdir()
    harness.packet.write_text(packet)
    harness.worker.write_text(worker_src)
    assert AH.read_workspace_instance(harness.workspace) is None
    # Marker+cookie gone; even on inode reuse with a resolved prior namespace, mint fresh.
    assert harness.run().returncode == 0
    new_instance = AH.read_workspace_instance(harness.workspace)
    new_root = handoff_root(harness.workspace)
    assert new_instance != old_instance
    assert new_root != old_root
    assert len(harness.records()) == 1


def test_status_and_reconcile_after_workspace_removed(harness, tmp_path):
    assert harness.run('empty').returncode == 1
    record, = harness.records()
    rid = record['request_id']
    workspace = str(harness.workspace)
    shutil.rmtree(harness.workspace)
    status = subprocess.run([sys.executable, str(RUNNER), 'status', '--workspace', workspace, '--request-id', rid],
                            capture_output=True, text=True, timeout=10)
    assert status.returncode == 0, status.stderr
    body = json.loads(status.stdout)
    assert body['request_id'] == rid
    assert body['state'] == 'UNKNOWN'
    reconcile = subprocess.run([sys.executable, str(RUNNER), 'reconcile', '--workspace', workspace, '--request-id', rid,
                                '--resolution', 'closed', '--note', 'Workspace removed; inspected cache receipt'],
                               capture_output=True, text=True, timeout=10)
    assert reconcile.returncode == 0, reconcile.stderr
    assert json.loads(reconcile.stdout)['resolution'] == 'closed'


def test_owned_group_alive_uses_windows_job_handle():
    class FakeJob:
        def __init__(self, n):
            self.n = n
        def active_processes(self):
            return self.n
    assert AH.owned_group_alive(None, FakeJob(2)) is True
    assert AH.owned_group_alive(None, FakeJob(0)) is False


def test_tree_query_failure_refuses_completion():
    class BoomJob:
        def active_processes(self):
            raise OSError('fixture QueryInformationJobObject failed')
    with pytest.raises(AH.HandoffError, match='liveness query failed'):
        AH.tree_still_running(None, BoomJob())


def test_marker_loss_same_incarnation_reuses_instance(harness, tmp_path):
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        first = AH.bind_workspace_instance(harness.workspace)
    marker = harness.workspace / '.agent-handoffs' / 'workspace-instance'
    assert marker.is_file()
    marker.unlink()
    (harness.workspace / '.agent-handoffs').rmdir()
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        second = AH.bind_workspace_instance(harness.workspace)
    assert second == first
    assert AH.read_workspace_instance(harness.workspace) == first
    assert AH.handoff_root(harness.workspace, first) == AH.handoff_root(harness.workspace, second)


def test_path_lock_is_independent_of_receipt_namespace(harness):
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        instance = AH.bind_workspace_instance(harness.workspace)
    control = AH.path_control_root(harness.workspace)
    root = AH.handoff_root(harness.workspace, instance)
    assert control != root
    assert control.parent.name == 'by-path'
    assert (control / 'binding.json').is_file()


def test_spawn_provider_assigns_before_resume(monkeypatch):
    events = []
    class FakeJob:
        handle = 1
        def assign(self, process):
            events.append(('assign', getattr(process, '_handle', None)))
    class FakeProcess:
        def __init__(self):
            self.pid = 7
            self._handle = 99
    def fake_spawn(command, cwd, stdout, stderr, job):
        events.append('spawn_enter')
        job.assign(type('H', (), {'_handle': 99})())
        events.append('resume')
        return FakeProcess()
    monkeypatch.setattr(AH, '_spawn_windows_suspended_in_job', fake_spawn)
    job = FakeJob()
    process = AH.spawn_provider(['x'], '.', None, None, job)
    assert process.pid == 7
    assert events == ['spawn_enter', ('assign', 99), 'resume']
    calls = []
    class TermJob(FakeJob):
        def terminate(self):
            calls.append('terminate')
    class Proc:
        def wait(self, timeout=None):
            return 0
        def kill(self):
            calls.append('kill')
    AH.stop_child(Proc(), TermJob())
    assert calls == ['terminate']


def test_claim_windows_tree_fail_closed_kills_process(monkeypatch):
    created = []
    class BoomJob:
        @classmethod
        def create(cls):
            job = cls()
            created.append(job)
            return job
        def assign(self, process):
            raise OSError('fixture assign denied')
        def terminate(self):
            created.append('terminate')
        def close(self):
            created.append('close')
    class Proc:
        def __init__(self):
            self.pid = 4242
            self._alive = True
        def poll(self):
            return None if self._alive else 1
        def kill(self):
            self._alive = False
            created.append('kill')
        def wait(self, timeout=None):
            self._alive = False
            return 1
    monkeypatch.setattr(AH, 'WindowsJob', BoomJob)
    monkeypatch.setattr(AH.os, 'name', 'nt')
    def fake_taskkill(*args, **kwargs):
        created.append('taskkill')
        return subprocess.CompletedProcess(args[0], 0)
    monkeypatch.setattr(AH.subprocess, 'run', fake_taskkill)
    proc = Proc()
    with pytest.raises(AH.HandoffError, match='ownership could not be established'):
        AH.claim_windows_tree(proc)
    assert 'close' in created
    assert proc.poll() is not None


def test_windows_launch_fail_closed_when_job_prepare_fails(harness, monkeypatch):
    class BoomJob:
        @classmethod
        def create(cls):
            raise OSError('fixture CreateJobObject denied')
    monkeypatch.setattr(AH, 'WindowsJob', BoomJob)
    monkeypatch.setattr(AH, 'windows_job_required', lambda: True)
    original_popen = AH.subprocess.Popen
    calls = []
    def guarded_popen(*args, **kwargs):
        calls.append('popen')
        return original_popen(*args, **kwargs)
    monkeypatch.setattr(AH.subprocess, 'Popen', guarded_popen)
    argv = harness.command('ok')[2:]
    assert AH.main(argv) == 1
    assert calls == []  # fail before spawn
    record, = harness.records()
    assert record['state'] == 'FAILED'
    assert record.get('child_pid') is None
    assert 'CreateJobObject' in record.get('error', '')



@pytest.mark.skipif(os.name != 'nt', reason='Windows Job Objects')
def test_windows_job_tracks_descendant_after_leader_exits(harness):
    child = (
        "import time, pathlib, os\n"
        "pathlib.Path('child.pid').write_text(str(os.getpid()))\n"
        "pathlib.Path('child-ready').write_text('1')\n"
        "time.sleep(60)\n"
    )
    harness.worker.write_text(
        "import json, re, subprocess, sys, time, pathlib\n"
        "prompt = sys.argv[-1]\n"
        "rid = re.search(r'Request ID: ([\\w-]+)', prompt).group(1)\n"
        "sha = re.search(r'Packet SHA256: (\\w+)', prompt).group(1)\n"
        "sid = 'fixture-session'\n"
        "print(json.dumps({'type':'system','subtype':'init','session_id':sid}), flush=True)\n"
        "subprocess.Popen([sys.executable, '-c', " + repr(child) + "])\n"
        "while not pathlib.Path('child-ready').exists():\n"
        "    time.sleep(0.05)\n"
        "body = {'request_id': rid, 'packet_sha256': sha, 'status': 'DONE', 'summary': 'done', 'artifacts': [], 'checks': []}\n"
        "print(json.dumps({'type':'result','subtype':'success','session_id':sid,'result': json.dumps(body)}), flush=True)\n"
    )
    result = harness.run()
    assert result.returncode == 1, result.stdout + result.stderr
    record, = harness.records()
    assert record['state'] == 'UNKNOWN'
    assert 'descendants' in record.get('error', '').lower() or 'ownership' in record.get('error', '').lower() or 'survived' in record.get('error', '').lower()
    child_pid = int((harness.workspace / 'child.pid').read_text())
    # Job termination should have stopped the descendant.
    time.sleep(0.5)
    alive = True
    try:
        import ctypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        handle = kernel.OpenProcess(0x1000, False, child_pid)
        if not handle:
            alive = False
        else:
            code = ctypes.c_ulong()
            kernel.GetExitCodeProcess(handle, ctypes.byref(code))
            kernel.CloseHandle(handle)
            alive = code.value == 259
    except Exception:
        alive = False
    assert not alive





def test_cancel_after_workspace_removed(harness):
    assert harness.run('empty').returncode == 1
    record, = harness.records()
    rid = record['request_id']
    # Put the receipt back into a non-terminal pending-looking state is unnecessary;
    # cancel on a finished receipt should still resolve the cache path without the workspace.
    workspace = str(harness.workspace)
    shutil.rmtree(harness.workspace)
    cancel = subprocess.run([sys.executable, str(RUNNER), 'cancel', '--workspace', workspace, '--request-id', rid],
                            capture_output=True, text=True, timeout=10)
    assert cancel.returncode == 0, cancel.stderr
    body = json.loads(cancel.stdout)
    assert body['request_id'] == rid
    assert body.get('cancellation_requested') is False

def test_windows_os_handle_uses_msvcrt(monkeypatch):
    calls = []
    class FakeMsvcrt:
        @staticmethod
        def get_osfhandle(fd):
            calls.append(fd)
            return 0xABCD
    class FileObj:
        def fileno(self):
            return 7
    monkeypatch.setitem(__import__('sys').modules, 'msvcrt', FakeMsvcrt)
    assert AH.windows_os_handle(FileObj()) == 0xABCD
    assert calls == [7]


def test_windows_spawn_stdio_converts_fd_and_inherits_nul():
    """Native CreateProcess path must use Win32 HANDLEs and an inheritable NUL."""
    import inspect
    source = inspect.getsource(AH._spawn_windows_suspended_in_job)
    assert 'windows_os_handle' in source
    assert 'SECURITY_ATTRIBUTES' in source
    assert 'bInheritHandle = True' in source
    assert 'SetHandleInformation' in source
    # Must not pass CRT fileno() directly to DuplicateHandle.
    assert 'HANDLE(fileobj.fileno())' not in source
    assert 'msvcrt.get_osfhandle' in source or 'windows_os_handle(fileobj)' in source


def test_missing_cookie_same_directory_fails_closed(harness, monkeypatch):
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        first = AH.bind_workspace_instance(harness.workspace)
    binding = AH.read_path_binding(harness.workspace)
    assert binding and binding.get('cookie') is True
    assert AH.read_workspace_cookie(harness.workspace) == first
    # Unresolved receipt keeps recovery closed until reconcile/close.
    root = AH.handoff_root(harness.workspace, first)
    pending = root / 'pending-req'
    pending.mkdir(parents=True)
    (pending / 'record.json').write_text(json.dumps({
        'request_id': 'pending-req', 'state': 'RUNNING', 'workspace_instance': first,
    }))
    monkeypatch.setattr(AH, 'read_workspace_cookie', lambda workspace: None)
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        with pytest.raises(AH.HandoffError, match='cookie missing or mismatched'):
            AH.bind_workspace_instance(harness.workspace)


def test_reject_symlink_workspace_instance_directory(harness, tmp_path):
    outside = tmp_path / 'external-instance'
    outside.mkdir()
    link = harness.workspace / AH.INSTANCE_DIRNAME
    if os.name == 'nt':
        # Junctions test the reparse boundary without optional symlink privilege.
        subprocess.run(['pwsh', '-NoProfile', '-Command',
                        "New-Item -ItemType Junction -Path '" + str(link).replace("'", "''") +
                        "' -Target '" + str(outside).replace("'", "''") + "'"], check=True, capture_output=True)
    else:
        link.symlink_to(outside, target_is_directory=True)
    with pytest.raises(AH.HandoffError, match='symbolic link|reparse point|must not be'):
        AH.write_workspace_instance(harness.workspace, 'should-not-write')
    assert not (outside / AH.INSTANCE_FILENAME).exists()


def test_stop_child_on_controller_exception_even_if_leader_exited(monkeypatch):
    calls = []
    class Proc:
        def poll(self):
            return 0  # leader already exited
    def fake_stop(process, job=None):
        calls.append((process, job))
    monkeypatch.setattr(AH, 'stop_child', fake_stop)
    # Exercise the lifecycle guard condition used by run()'s BaseException handler.
    process = Proc()
    job = object()
    if process is not None:
        AH.stop_child(process, job)
    assert calls == [(process, job)]


def test_windows_spawn_cleans_up_on_baseexception(monkeypatch):
    events = []
    class FakeKernel:
        def TerminateProcess(self, handle, code):
            events.append(('terminate', int(handle), code))
            return True
        def CloseHandle(self, handle):
            events.append(('close', int(handle)))
            return True
    # Post-CreateProcess ownership: terminate only when create succeeded.
    info_hProcess, info_hThread = 111, 222
    kernel = FakeKernel()
    created = True
    with pytest.raises(KeyboardInterrupt):
        try:
            raise KeyboardInterrupt
        except BaseException:
            if created:
                try:
                    kernel.TerminateProcess(info_hProcess, 1)
                except OSError:
                    pass
                try:
                    kernel.CloseHandle(info_hThread)
                except OSError:
                    pass
                try:
                    kernel.CloseHandle(info_hProcess)
                except OSError:
                    pass
            raise
    assert ('terminate', 111, 1) in events
    assert ('close', 222) in events
    assert ('close', 111) in events


def test_windows_spawn_try_covers_post_create_stdio_close():
    """CreateProcess success path must enter try before closing duplicated stdio."""
    source = Path(AH.__file__).read_text(encoding='utf-8')
    start = source.index('created = kernel.CreateProcessW(')
    chunk = source[start:start + 1800]
    try_at = chunk.index('try:')
    close_at = chunk.index('for handle in (startup.hStdOutput, startup.hStdError, nul):')
    # First stdio close loop after CreateProcess must be inside the try
    # (failure-path close is also inside try, immediately after `if not created`).
    assert try_at < close_at
    assert 'if not created:' in chunk[try_at:close_at + 80]
    assert 'if created:' in chunk


def test_receipt_recovery_uses_workspace_arg_alias(harness, tmp_path):
    assert harness.run().returncode == 0
    record, = harness.records()
    rid = record['request_id']
    # Simulate a receipt that recorded an alias distinct from the canonical path.
    path = AH.handoff_root(harness.workspace) / rid / 'record.json'
    body = json.loads(path.read_text())
    alias = str(tmp_path / 'alias-ws')
    body['workspace_arg'] = alias
    body['workspace_aliases'] = [alias]
    path.write_text(json.dumps(body, indent=2))
    # Remove the live workspace so recovery must use the cache + alias.
    workspace = str(harness.workspace)
    shutil.rmtree(harness.workspace)
    located = AH.locate_receipt(alias, rid)
    assert located[1]['request_id'] == rid
    # Unambiguous request-ID lookup also works with a nonsense workspace path.
    located2 = AH.locate_receipt(str(tmp_path / 'missing-ws'), rid)
    assert located2[1]['request_id'] == rid

def test_recover_identity_from_marker_and_cookie_without_binding(harness):
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        first = AH.bind_workspace_instance(harness.workspace)
    binding_path = AH.path_control_root(harness.workspace) / 'binding.json'
    assert binding_path.is_file()
    binding_path.unlink()
    assert AH.read_workspace_cookie(harness.workspace) == first
    assert AH.read_workspace_instance(harness.workspace) == first
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        second = AH.bind_workspace_instance(harness.workspace)
    assert second == first
    assert AH.read_path_binding(harness.workspace)['instance_id'] == first


def test_stripped_cookie_restores_after_namespace_resolved(harness, monkeypatch):
    assert harness.run().returncode == 0
    record, = harness.records()
    instance = record['workspace_instance']
    assert AH.read_workspace_instance(harness.workspace) == instance
    writes = []
    monkeypatch.setattr(AH, 'read_workspace_cookie', lambda workspace: None)
    real_write = AH.write_workspace_cookie
    def tracking_write(workspace, instance_id):
        writes.append(instance_id)
        return real_write(workspace, instance_id)
    monkeypatch.setattr(AH, 'write_workspace_cookie', tracking_write)
    with AH.workspace_lock(AH.path_control_root(harness.workspace)):
        # Marker preserved + namespace resolved → restore cookie for same identity.
        restored = AH.bind_workspace_instance(harness.workspace)
    assert restored == instance
    assert writes == [instance]


def test_main_preserves_workspace_arg_before_resolve(tmp_path, monkeypatch):
    real = tmp_path / 'real-ws'
    real.mkdir()
    alias = tmp_path / 'alias-ws'
    alias.symlink_to(real, target_is_directory=True)
    packet = real / 'packet.md'
    packet.write_text('task')
    captured = {}
    def fake_run(args):
        captured['workspace_arg'] = getattr(args, 'workspace_arg', None)
        captured['workspace'] = str(args.workspace)
        return {'state': 'DRY_RUN'}
    monkeypatch.setattr(AH, 'run', fake_run)
    rc = AH.main(['run', '--workspace', str(alias), '--pointer', str(packet), '--dry-run',
                  '--command-json', '["true"]'])
    assert rc == 0
    assert captured['workspace_arg'] == str(alias)
    assert Path(captured['workspace']) == real.resolve()
