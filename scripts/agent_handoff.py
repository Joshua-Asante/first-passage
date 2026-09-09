"""Durable local CLI handoffs. See agent_handoff.md for protocol and recovery."""
from __future__ import annotations

import argparse
import base64
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import uuid


class HandoffError(RuntimeError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


DIGEST_CHUNK = 1024 * 1024


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open('rb') as handle:
        while True:
            chunk = handle.read(DIGEST_CHUNK)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def privatize(path, directory=False):
    if os.name == 'nt':
        return
    os.chmod(path, 0o700 if directory else 0o600)


def secure_mkdir(path):
    path.mkdir(parents=True, exist_ok=True)
    privatize(path, directory=True)


def ensure_dir(path):
    # Create missing parents for workspace staging without rewriting existing modes.
    path.mkdir(parents=True, exist_ok=True)


def write_json(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
    privatize(temporary)
    os.replace(temporary, path)
    privatize(path)


def cache_home():
    return Path.home() / '.cache' / 'agent-handoffs'


INSTANCE_DIRNAME = '.agent-handoffs'
INSTANCE_FILENAME = 'workspace-instance'


def read_workspace_instance(workspace):
    marker = Path(workspace) / INSTANCE_DIRNAME / INSTANCE_FILENAME
    if not marker.is_file():
        return None
    value = marker.read_text(encoding='utf-8').strip()
    return value or None


def ensure_workspace_instance(workspace):
    existing = read_workspace_instance(workspace)
    if existing:
        return existing
    secure_mkdir(Path(workspace) / INSTANCE_DIRNAME)
    instance = str(uuid.uuid4())
    marker = Path(workspace) / INSTANCE_DIRNAME / INSTANCE_FILENAME
    temporary = marker.with_suffix('.tmp')
    temporary.write_text(instance + '\n', encoding='utf-8')
    privatize(temporary)
    os.replace(temporary, marker)
    privatize(marker)
    return instance


def handoff_root(workspace, instance_id=None):
    # Key by resolved path + durable instance id so a deleted/recreated worktree
    # at the same pathname cannot inherit the prior workspace's receipts.
    workspace = Path(workspace)
    if instance_id is None:
        instance_id = read_workspace_instance(workspace)
        if instance_id is None:
            raise HandoffError('Workspace has no instance identity yet')
    key = hashlib.sha256(f'{workspace.resolve(strict=False)}\n{instance_id}'.encode()).hexdigest()
    return cache_home() / key


def normalize_workspace_path(value):
    return str(Path(value).expanduser().resolve(strict=False))


def locate_receipt(workspace_arg, request_id):
    # Recovery must work after the workspace directory is gone.
    request_id = identifier(request_id)
    workspace_arg = Path(workspace_arg).expanduser()
    if workspace_arg.exists():
        try:
            workspace = workspace_arg.resolve(strict=True)
        except OSError:
            workspace = None
        else:
            instance = read_workspace_instance(workspace)
            if instance:
                path = handoff_root(workspace, instance) / request_id / 'record.json'
                if path.is_file():
                    record = load(path)
                    if record.get('workspace') == str(workspace):
                        return path, record
    target = normalize_workspace_path(workspace_arg)
    matches = []
    if cache_home().is_dir():
        for path in cache_home().glob(f'*/{request_id}/record.json'):
            try:
                record = load(path)
            except (OSError, ValueError):
                continue
            recorded = record.get('workspace')
            if recorded is None:
                continue
            if recorded == target or normalize_workspace_path(recorded) == target:
                matches.append((path, record))
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise HandoffError('Receipt not found')
    raise HandoffError('Ambiguous receipt match for request ID and workspace path')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def identifier(value):
    try:
        return str(uuid.UUID(value))
    except ValueError as exc:
        raise HandoffError('Request ID must be a UUID') from exc


def inside(workspace, value):
    path = (workspace / value).resolve()
    if not path.is_relative_to(workspace):
        raise HandoffError(f'Path leaves workspace: {value}')
    if path.is_relative_to(workspace / '.agent-handoffs'):
        raise HandoffError('Dispatcher evidence cannot be a task input/output')
    return path


@contextmanager
def workspace_lock(root):
    secure_mkdir(root)
    with (root / 'dispatch.lock').open('a+b') as lock:
        lock.seek(0, 2)
        if lock.tell() == 0:
            lock.write(b'0')
            lock.flush()
        lock.seek(0)
        privatize(root / 'dispatch.lock')
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise HandoffError('A dispatcher is active in this workspace; inspect status before retrying') from exc
        try:
            yield
        finally:
            lock.seek(0)
            if os.name == 'nt':
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock, fcntl.LOCK_UN)


def live(pid):
    if not pid:
        return False
    if os.name == 'nt':
        # os.kill(pid, 0) is not a safe liveness probe on Windows.
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        kernel.OpenProcess.restype = wintypes.HANDLE
        kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return ctypes.get_last_error() != 87  # access denied is conservatively alive
        try:
            code = wintypes.DWORD()
            return not kernel.GetExitCodeProcess(handle, ctypes.byref(code)) or code.value == 259
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def executable_command(provider, override):
    if override:
        command = json.loads(override)
        if not isinstance(command, list) or not command or not all(isinstance(x, str) and x for x in command):
            raise HandoffError('--command-json must be a nonempty executable/argument array')
        return command
    candidate = shutil.which('agent' if provider == 'cursor' else 'claude')
    if not candidate and os.name == 'nt':
        candidate = str(Path(os.environ['LOCALAPPDATA']) / 'cursor-agent/agent.ps1') if provider == 'cursor' else str(Path.home() / '.local/bin/claude.exe')
    if not candidate or not Path(candidate).is_file():
        raise HandoffError(f'{provider} executable not found; supply --command-json')
    return [candidate]


def windows_command(command):
    """Keep prompts out of cmd.exe parsing, including its %, &, and quote expansion."""
    if os.name != 'nt' or Path(command[0]).suffix.lower() not in ('.cmd', '.bat', '.ps1'):
        return command
    target = Path(command[0])
    if target.suffix.lower() in ('.cmd', '.bat'):
        target = target.with_suffix('.ps1')
        if not target.is_file():
            raise HandoffError('Batch launcher has no PowerShell sibling; supply a native executable command')
    payload = base64.b64encode(json.dumps([str(target), *command[1:]], ensure_ascii=False).encode()).decode()
    script = ('$a = ConvertFrom-Json ([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("' + payload + '"))); '
              '$exe=$a[0]; $rest=@($a | Select-Object -Skip 1); & $exe @rest; exit $LASTEXITCODE')
    shell = shutil.which('pwsh') or shutil.which('powershell')
    if not shell:
        raise HandoffError('PowerShell is required for this launcher')
    return [shell, '-NoProfile', '-NonInteractive', '-EncodedCommand', base64.b64encode(script.encode('utf-16-le')).decode()]


def cli_args(args, prompt, session, fresh_session):
    result = ['-p', '--output-format', 'stream-json']
    if args.provider == 'cursor':
        result += ['--workspace', str(args.workspace), '--trust']
        if args.mode in ('plan', 'ask'):
            result += ['--mode', args.mode]
        if args.force_commands:
            result += ['--force']
    else:
        result += ['--verbose']
        if args.mode == 'plan':
            result += ['--permission-mode', 'plan']
        elif args.mode == 'ask':
            result += ['--tools', 'Read,Glob,Grep', '--allowedTools', 'Read,Glob,Grep']
        if args.allowed_tools:
            result += ['--allowedTools', args.allowed_tools]
        if fresh_session:
            result += ['--session-id', fresh_session]
    for root in args.add_dir:
        result += ['--add-dir', root]
    if session:
        result += ['--resume', session]
    if args.model:
        result += ['--model', args.model]
    return result + [prompt]


def validate_return(event, record, workspace):
    verify_inputs(record['contract'])
    if event.get('is_error') or event.get('subtype', 'success') != 'success':
        raise HandoffError('Provider returned an error result; see stdout/stderr')
    body = event.get('result')
    if isinstance(body, str):
        body = body.strip()
        if body.startswith('```json\n') and body.endswith('```'):
            body = body[8:-3].strip()
        try:
            body = json.loads(body)
        except (ValueError, TypeError) as exc:
            raise HandoffError('Worker result does not contain the required JSON return') from exc
    if not isinstance(body, dict):
        raise HandoffError('Worker result must be an object')
    if body.get('request_id') != record['request_id']:
        raise HandoffError('Stale or mismatched request ID in return')
    if body.get('packet_sha256') != record['packet_sha256']:
        raise HandoffError('Packet hash mismatch in return')
    status = body.get('status')
    if status not in ('DONE', 'DONE_WITH_CONCERNS', 'NEEDS_CONTEXT', 'BLOCKED'):
        raise HandoffError('Missing/invalid worker status')
    if not isinstance(body.get('summary'), str) or not body['summary'].strip():
        raise HandoffError('Missing return summary')
    if not isinstance(body.get('artifacts'), list) or not isinstance(body.get('checks'), list):
        raise HandoffError('Return must contain artifacts and checks arrays')
    if not all(isinstance(item, dict) for item in body['artifacts'] + body['checks']):
        raise HandoffError('Artifact/check entries must be objects')
    if status in ('DONE', 'DONE_WITH_CONCERNS') and record['mode'] == 'execute':
        reported = {}
        for artifact in body['artifacts']:
            if not isinstance(artifact.get('path'), str):
                raise HandoffError('Artifact path must be a string')
            path = inside(workspace, artifact['path'])
            if not path.is_file() or artifact.get('sha256') != digest(path):
                raise HandoffError(f"Reported artifact hash mismatch: {artifact['path']}")
            reported[path.relative_to(workspace).as_posix()] = artifact['sha256']
        for output in record['contract']['expected_outputs']:
            path = inside(workspace, output)
            if not path.is_file() or reported.get(output) != digest(path):
                raise HandoffError(f'Missing artifact or hash mismatch: {output}')
        checks = {item.get('name'): item for item in body['checks']}
        for name in record['contract']['required_checks']:
            check = checks.get(name, {})
            evidence = check.get('evidence')
            if check.get('status') != 'passed' or not isinstance(evidence, str) or not evidence.strip():
                raise HandoffError(f'Required check not reported passed with evidence: {name}')
    return body


def verify_inputs(contract):
    inputs = {contract['pointer']: contract['pointer_sha256'], **contract['inputs']}
    for path, expected in inputs.items():
        try:
            if digest(path) == expected:
                continue
        except OSError as exc:
            raise HandoffError(f'Immutable input unavailable: {path}: {exc}') from exc
        raise HandoffError(f'Immutable input changed: {path}')


class WindowsJob:
    """Retain a Windows Job Object handle for the owned provider tree."""

    JobObjectBasicAccountingInformation = 1
    JobObjectExtendedLimitInformation = 9
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
    PROCESS_TERMINATE = 0x0001
    PROCESS_SET_QUOTA = 0x0100

    def __init__(self, handle):
        self.handle = handle
        self._kernel = None

    @classmethod
    def _api(cls):
        import ctypes
        from ctypes import wintypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
        kernel.CreateJobObjectW.restype = wintypes.HANDLE
        kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, wintypes.INT, wintypes.LPVOID, wintypes.DWORD]
        kernel.SetInformationJobObject.restype = wintypes.BOOL
        kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        kernel.AssignProcessToJobObject.restype = wintypes.BOOL
        kernel.QueryInformationJobObject.argtypes = [wintypes.HANDLE, wintypes.INT, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD]
        kernel.QueryInformationJobObject.restype = wintypes.BOOL
        kernel.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
        kernel.TerminateJobObject.restype = wintypes.BOOL
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        return ctypes, wintypes, kernel

    @classmethod
    def create(cls):
        ctypes, wintypes, kernel = cls._api()

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [
                ('ReadOperationCount', ctypes.c_ulonglong),
                ('WriteOperationCount', ctypes.c_ulonglong),
                ('OtherOperationCount', ctypes.c_ulonglong),
                ('ReadTransferCount', ctypes.c_ulonglong),
                ('WriteTransferCount', ctypes.c_ulonglong),
                ('OtherTransferCount', ctypes.c_ulonglong),
            ]

        class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ('PerProcessUserTimeLimit', ctypes.c_int64),
                ('PerJobUserTimeLimit', ctypes.c_int64),
                ('LimitFlags', wintypes.DWORD),
                ('MinimumWorkingSetSize', ctypes.c_size_t),
                ('MaximumWorkingSetSize', ctypes.c_size_t),
                ('ActiveProcessLimit', wintypes.DWORD),
                ('Affinity', ctypes.c_size_t),
                ('PriorityClass', wintypes.DWORD),
                ('SchedulingClass', wintypes.DWORD),
            ]

        class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
            _fields_ = [
                ('BasicLimitInformation', JOBOBJECT_BASIC_LIMIT_INFORMATION),
                ('IoInfo', IO_COUNTERS),
                ('ProcessMemoryLimit', ctypes.c_size_t),
                ('JobMemoryLimit', ctypes.c_size_t),
                ('PeakProcessMemoryUsed', ctypes.c_size_t),
                ('PeakJobMemoryUsed', ctypes.c_size_t),
            ]

        handle = kernel.CreateJobObjectW(None, None)
        if not handle:
            raise OSError('CreateJobObject failed')
        info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        info.BasicLimitInformation.LimitFlags = cls.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not kernel.SetInformationJobObject(handle, cls.JobObjectExtendedLimitInformation, ctypes.byref(info), ctypes.sizeof(info)):
            kernel.CloseHandle(handle)
            raise OSError('SetInformationJobObject failed')
        job = cls(handle)
        job._kernel = kernel
        job._ctypes = ctypes
        job._wintypes = wintypes
        job._accounting = type('JOBOBJECT_BASIC_ACCOUNTING_INFORMATION', (ctypes.Structure,), {
            '_fields_': [
                ('TotalUserTime', ctypes.c_int64),
                ('TotalKernelTime', ctypes.c_int64),
                ('ThisPeriodTotalUserTime', ctypes.c_int64),
                ('ThisPeriodTotalKernelTime', ctypes.c_int64),
                ('TotalPageFaultCount', wintypes.DWORD),
                ('TotalProcesses', wintypes.DWORD),
                ('ActiveProcesses', wintypes.DWORD),
                ('TotalTerminatedProcesses', wintypes.DWORD),
            ]
        })
        return job

    def assign(self, process):
        handle = getattr(process, '_handle', None)
        if not handle:
            raise OSError('Windows process handle unavailable for job assignment')
        if not self._kernel.AssignProcessToJobObject(self.handle, int(handle)):
            raise OSError('AssignProcessToJobObject failed')

    def active_processes(self):
        info = self._accounting()
        returned = self._wintypes.DWORD()
        if not self._kernel.QueryInformationJobObject(
            self.handle, self.JobObjectBasicAccountingInformation, self._ctypes.byref(info),
            self._ctypes.sizeof(info), self._ctypes.byref(returned)
        ):
            return 0
        return int(info.ActiveProcesses)

    def terminate(self):
        self._kernel.TerminateJobObject(self.handle, 1)

    def close(self):
        if self.handle:
            self._kernel.CloseHandle(self.handle)
            self.handle = None


def stop_child(process, job=None):
    # Never kill a PID retrieved from a stale receipt. Only this owned process/tree.
    if job is not None:
        try:
            job.terminate()
        except OSError:
            pass
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        return
    if os.name == 'nt':
        if process.poll() is None:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, timeout=15)
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        # The leader can exit while a tool in its group ignores SIGTERM.
        # Give the group a grace period, then stop survivors independently
        # of the leader's return code. Never use a PID from a saved receipt.
        time.sleep(1)
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        if os.name != 'nt':
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.wait(timeout=5)


def owned_group_alive(process, job=None):
    if job is not None:
        try:
            return job.active_processes() > 0
        except OSError:
            return False
    if os.name == 'nt' or process is None or process.pid is None:
        return False
    try:
        os.killpg(process.pid, 0)
        return True
    except ProcessLookupError:
        return False


def run(args):
    workspace = args.workspace.resolve(strict=True)
    args.workspace = workspace
    pointer = Path(args.pointer).resolve(strict=True)
    followup = Path(args.message_file).read_text(encoding='utf-8') if args.message_file else None
    if args.copy and (args.resume_request or args.resume_session):
        raise HandoffError('Do not stage new copies during resume')
    copies = []
    for pair in args.copy:
        source, separator, destination = pair.partition('::')
        if not separator:
            raise HandoffError('Copy entries must be source::relative-destination')
        copies.append((Path(source).resolve(strict=True), inside(workspace, destination)))
    contract = {
        'pointer': str(pointer), 'pointer_sha256': digest(pointer),
        'inputs': {str(Path(p).resolve(strict=True)): digest(Path(p).resolve(strict=True)) for p in args.input},
        'expected_outputs': sorted({inside(workspace, p).relative_to(workspace).as_posix() for p in args.expected_output}),
        'required_checks': sorted(set(args.required_check)),
        'add_dirs': sorted({str(Path(p).resolve(strict=True)) for p in args.add_dir}),
    }
    for source, destination in copies:
        expected = digest(source)
        if str(destination) in contract['inputs'] and contract['inputs'][str(destination)] != expected:
            raise HandoffError('Conflicting staged input')
        contract['inputs'][str(destination)] = expected
    args.add_dir = contract['add_dirs']
    packet_hash = hashlib.sha256(json.dumps(contract, sort_keys=True).encode()).hexdigest()
    command = executable_command(args.provider, args.command_json)
    if args.dry_run:
        return {'state': 'DRY_RUN', 'workspace': str(workspace), 'contract': contract, 'command': command}
    instance_id = ensure_workspace_instance(workspace)
    root = handoff_root(workspace, instance_id)
    with workspace_lock(root):
        records = [load(p) for p in root.glob('*/record.json')]
        parent = None
        if args.resume_request or args.resume_session:
            matches = [r for r in records if (r['request_id'] == args.resume_request if args.resume_request else r.get('session_id') == args.resume_session) and not r.get('resumed_by')]
            if len(matches) != 1:
                raise HandoffError('Resume requires exactly one local, latest request receipt; unrecorded session IDs are refused')
            parent = matches[0]
            if parent['provider'] != args.provider or parent['workspace'] != str(workspace) or parent['packet_sha256'] != packet_hash:
                raise HandoffError('Resume provider/workspace/packet mismatch; reconcile the changed scope first')
            if not parent.get('session_id'):
                raise HandoffError('No provider session ID captured; reconcile before starting a replacement')
            if parent['state'] not in ('RETURNED', 'RECONCILED'):
                raise HandoffError('Uncertain prior request must be reconciled before resuming')
            if parent.get('resolution') == 'closed':
                raise HandoffError('Request was closed; start a replacement rather than resuming it')
        for previous in records:
            if previous['state'] not in ('RETURNED', 'RECONCILED'):
                raise HandoffError(f"Unresolved request {previous['request_id']}: inspect/reconcile before another launch")
            if previous['packet_sha256'] == packet_hash and not parent and not previous.get('resumed_by') and previous.get('resolution') != 'closed':
                raise HandoffError(f"Packet already dispatched: {previous['request_id']}; resume its session or explicitly reconcile/close it")
        artifacts_before = {}
        for relative in contract['expected_outputs']:
            artifact_path = inside(workspace, relative)
            try:
                artifacts_before[relative] = digest(artifact_path) if artifact_path.is_file() else None
            except OSError as exc:
                raise HandoffError(f'Preflight artifact snapshot failed: {relative}: {exc}') from exc
        request_id = identifier(args.request_id) if args.request_id else str(uuid.uuid4())
        directory = root / request_id
        directory.mkdir(mode=0o700)  # Existing IDs are never overwritten.
        privatize(directory, directory=True)
        record_path = directory / 'record.json'
        fresh_session = str(uuid.uuid4()) if args.provider == 'claude' and not parent else None
        record = dict(request_id=request_id, provider=args.provider, workspace=str(workspace),
                      workspace_instance=instance_id,
                      packet_sha256=packet_hash, contract=contract, mode=args.mode,
                      session_id=parent['session_id'] if parent else fresh_session,
                      parent_request=parent['request_id'] if parent else None,
                      state='STARTING', created_at=now(), controller_pid=os.getpid(), child_pid=None,
                      exit_code=None, timeout_seconds=args.timeout_seconds, independently_verified=False)
        record['artifacts_before'] = artifacts_before
        write_json(record_path, record)
        if parent:
            parent['resumed_by'] = request_id
            write_json(root / parent['request_id'] / 'record.json', parent)
        example = dict(request_id=request_id, packet_sha256=packet_hash, status='DONE', summary='What was done',
                       artifacts=[{'path': p, 'sha256': '<actual SHA256>'} for p in contract['expected_outputs']],
                       checks=[{'name': n, 'status': 'passed', 'evidence': '<actual command/result>'} for n in contract['required_checks']])
        prompt = (f'Read the task packet at {pointer}. Follow its authorized scope. Mode: {args.mode}. '
                  'For ask/plan, make no edits. On a resumed session inspect existing work before continuing; do not repeat completed actions. '
                  f'Request ID: {request_id}. Packet SHA256: {packet_hash}. '
                  'Return exactly one JSON object as your final response with this shape: ' + json.dumps(example) +
                  '. Status must be DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT or BLOCKED. '
                  'Report blocked/skipped checks honestly; never manufacture evidence. No separate return file is required.')
        if followup is not None:
            prompt += '\nFollow-up message:\n' + followup
        process = None
        job = None
        terminal = None
        protocol_error = None
        try:
            prompt_path = directory / 'prompt.txt'
            prompt_path.write_text(prompt, encoding='utf-8')
            privatize(prompt_path)
            record['prompt_sha256'] = digest(prompt_path)
            write_json(record_path, record)
            # Admission and the workspace lock precede every staging write.
            for source, destination in copies:
                destination = inside(workspace, destination)
                expected = contract['inputs'][str(destination)]
                if destination.exists():
                    if digest(destination) != expected:
                        raise HandoffError('Refusing to overwrite staged input')
                else:
                    ensure_dir(destination.parent)
                    with source.open('rb') as src, destination.open('xb') as output:
                        shutil.copyfileobj(src, output, length=DIGEST_CHUNK)
            verify_inputs(contract)
            if (directory / 'cancel.request').exists():
                record.update(state='CANCELLED', error='Cancelled before provider launch')
            else:
                actual_command = windows_command(command + cli_args(args, prompt, record['session_id'] if parent else None, fresh_session))
                stdout_path = directory / 'stdout.jsonl'
                stderr_path = directory / 'stderr.txt'
                with stdout_path.open('wb') as stdout, stderr_path.open('wb') as stderr:
                    privatize(stdout_path)
                    privatize(stderr_path)
                    process = subprocess.Popen(actual_command, cwd=workspace, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr,
                                               start_new_session=os.name != 'nt', creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                    if os.name == 'nt':
                        job = WindowsJob.create()
                        job.assign(process)
                    record.update(state='RUNNING', child_pid=process.pid, started_at=now())
                    write_json(record_path, record)
                    print(json.dumps({'request_id': request_id, 'record': str(record_path), 'child_pid': process.pid}), flush=True)
                    deadline = time.monotonic() + args.timeout_seconds
                    with stdout_path.open('rb') as stream:
                        while True:
                            exited = process.poll() is not None
                            while True:
                                if (directory / 'cancel.request').exists() or time.monotonic() >= deadline:
                                    break
                                position = stream.tell()
                                line = stream.readline()
                                if not line:
                                    break
                                if not line.endswith(b'\n') and not exited:
                                    stream.seek(position)
                                    break
                                try:
                                    event = json.loads(line)
                                    if not isinstance(event, dict):
                                        raise ValueError('event is not an object')
                                except (ValueError, UnicodeError):
                                    protocol_error = 'Malformed provider output; inspect stdout.jsonl'
                                    continue
                                session = event.get('session_id')
                                if session:
                                    if not isinstance(session, str) or (record['session_id'] and record['session_id'] != session):
                                        protocol_error = 'Provider session changed unexpectedly'
                                    else:
                                        record['session_id'] = session
                                record['last_event_at'] = now()
                                if event.get('type') == 'result':
                                    if terminal is not None:
                                        protocol_error = 'Multiple terminal results'
                                    terminal = event
                                write_json(record_path, record)
                            if (directory / 'cancel.request').exists() or time.monotonic() >= deadline:
                                record['state'] = 'CANCELLED' if (directory / 'cancel.request').exists() else 'TIMED_OUT'
                                stop_child(process, job)
                                break
                            if exited:
                                break
                            time.sleep(0.1)
                record['exit_code'] = process.returncode
                if record['state'] in ('TIMED_OUT', 'CANCELLED'):
                    record['error'] = 'Local stop attempted; partial effects or remote work may remain. Reconcile before retry.'
                elif process.returncode != 0:
                    if owned_group_alive(process, job):
                        stop_child(process, job)
                    record.update(state='FAILED', error='Provider exited nonzero; inspect stderr.txt')
                elif protocol_error or terminal is None or not record['session_id']:
                    if owned_group_alive(process, job):
                        stop_child(process, job)
                    record.update(state='UNKNOWN', error=protocol_error or 'Missing terminal result or session ID')
                elif owned_group_alive(process, job):
                    stop_child(process, job)
                    record.update(state='UNKNOWN', error='Owned process-group descendants survived provider exit')
                else:
                    try:
                        body = validate_return(terminal, record, workspace)
                        return_path = directory / 'return.json'
                        write_json(return_path, body)
                        record.update(state='RETURNED', worker_status=body['status'])
                    except HandoffError as exc:
                        record.update(state='UNKNOWN', error=str(exc))
        except BaseException as exc:
            if process is not None and process.poll() is None:
                stop_child(process, job)
            record.update(state='CANCELLED' if isinstance(exc, KeyboardInterrupt) else 'FAILED', error=str(exc))
        finally:
            if process is not None:
                record['exit_code'] = process.poll()
            if job is not None:
                try:
                    job.close()
                except OSError:
                    pass
                job = None
            record['finished_at'] = now()
            record['artifacts_after'] = {}
            for p in contract['expected_outputs']:
                try:
                    path = inside(workspace, p)
                    record['artifacts_after'][p] = digest(path) if path.is_file() else None
                except (OSError, HandoffError, MemoryError) as exc:
                    record.setdefault('artifact_snapshot_errors', {})[p] = str(exc)
                    if record['state'] == 'RETURNED':
                        record.update(state='UNKNOWN', error='Artifact snapshot failed')
            write_json(record_path, record)
        return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['run', 'status', 'cancel', 'reconcile'])
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--request-id')
    parser.add_argument('--provider', choices=['cursor', 'claude'], default='cursor')
    parser.add_argument('--pointer')
    parser.add_argument('--input', action='append', default=[])
    parser.add_argument('--copy', action='append', default=[])
    parser.add_argument('--expected-output', action='append', default=[])
    parser.add_argument('--required-check', action='append', default=[])
    parser.add_argument('--add-dir', action='append', default=[])
    parser.add_argument('--mode', choices=['execute', 'plan', 'ask'], default='execute')
    parser.add_argument('--resume-request')
    parser.add_argument('--resume-session')
    parser.add_argument('--message-file')
    parser.add_argument('--timeout-seconds', type=float, default=900)
    parser.add_argument('--force-commands', action='store_true')
    parser.add_argument('--allowed-tools')
    parser.add_argument('--model')
    parser.add_argument('--command-json')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--note')
    parser.add_argument('--resolution', choices=['resume', 'closed'])
    args = parser.parse_args(argv)
    try:
        if args.action == 'run':
            args.workspace = args.workspace.resolve(strict=True)
            if not args.pointer or not 0 < args.timeout_seconds < float('inf'):
                raise HandoffError('A packet path and a finite positive timeout are required')
            if args.force_commands and (args.provider != 'cursor' or args.mode != 'execute'):
                raise HandoffError('--force-commands is only valid for Cursor execution')
            if args.allowed_tools and (args.provider != 'claude' or args.mode != 'execute'):
                raise HandoffError('--allowed-tools is only valid for Claude execution')
            if args.resume_request and args.resume_session:
                raise HandoffError('Select one resume identifier')
            result = run(args)
        else:
            if not args.request_id:
                raise HandoffError('--request-id is required')
            record_path, result = locate_receipt(args.workspace, args.request_id)
            root = record_path.parent.parent
            args.workspace = Path(result['workspace'])
            if args.action == 'cancel':
                pending = result['state'] in ('STARTING', 'RUNNING')
                if pending:
                    (record_path.parent / 'cancel.request').touch()
                result = dict(result, cancellation_requested=pending)
            elif args.action == 'status':
                result = dict(result, controller_may_be_alive=live(result.get('controller_pid')),
                              child_may_be_alive=live(result.get('child_pid')))
            elif args.action == 'reconcile':
                if not args.note or not args.note.strip() or not args.resolution:
                    raise HandoffError('Reconciliation requires --note describing inspected effects/processes and --resolution resume|closed')
                with workspace_lock(root):
                    result = load(record_path)
                    if result.get('exit_code') is None and (live(result.get('child_pid')) or (result['state'] in ('STARTING', 'RUNNING') and live(result.get('controller_pid')))):
                        raise HandoffError('Recorded process may still be alive; reconcile only after inspecting/stopping it')
                    if result.get('resumed_by'):
                        raise HandoffError('Reconcile the latest request in the chain')
                    if result.get('resolution') == 'closed':
                        raise HandoffError('Closed reconciliation is immutable; start a replacement instead of reopening it')
                    result.update(state='RECONCILED', resolution=args.resolution, reconciliation_note=args.note, reconciled_at=now())
                    write_json(record_path, result)
        print(json.dumps(result, indent=2))
        return 0 if result['state'] in ('DRY_RUN', 'RETURNED', 'RECONCILED') or args.action != 'run' else 1
    except (HandoffError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
