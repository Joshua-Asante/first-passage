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
            return [json.loads(p.read_text()) for p in workspace.glob('.agent-handoffs/*/record.json')]

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
    evidence = harness.workspace / '.agent-handoffs' / record['request_id']
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
    body = json.loads((harness.workspace / '.agent-handoffs' / record['request_id'] / 'return.json').read_text())
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
    path = harness.workspace / '.agent-handoffs' / record['request_id'] / 'record.json'
    record['child_pid'] = os.getpid()
    path.write_text(json.dumps(record))
    result = harness.action('status', record['request_id'])
    assert result.returncode == 0
    assert json.loads(result.stdout)['child_may_be_alive'] is True


def test_dry_run_and_path_boundaries(harness):
    assert harness.run('ok', '--dry-run').returncode == 0
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
