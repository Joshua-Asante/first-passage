"""Linux supervisor-only Docker adapter with a fixed local endpoint.

The OS must reserve the daemon socket for the supervisor. No client-selected
environment, executable, daemon endpoint, image or command reaches this adapter.
"""
import json
import os
from pathlib import Path
import selectors
import subprocess
import sys
import time

from ..contract import canonical_json_bytes as encoded
from .admission import WORKER_ENTRYPOINT
from .protocol import CapturedOutput, digest, identity

DOCKER = '/usr/bin/docker'
ENDPOINT = 'unix:///var/run/docker.sock'
LABEL = 'org.first-passage.qualification.execution'


def docker_environment():
    return {'PATH': '/usr/bin:/bin', 'HOME': '/nonexistent', 'LANG': 'C.UTF-8'}


def _command(*args):
    if sys.platform != 'linux':
        raise RuntimeError('execution supervisor requires Linux isolation')
    return [DOCKER, '--host=' + ENDPOINT, *args]


def _run(*args):
    result = subprocess.run(_command(*args), env=docker_environment(), stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False)
    if result.returncode != 0 or len(result.stdout) > 4 * 1024 * 1024:
        raise ValueError('Docker control operation failed')
    return result.stdout


def create_arguments(context, *, execution_id, input_dir, profile):
    identity(execution_id)
    source = str(Path(input_dir).absolute())
    if ',' in source or '\n' in source:
        raise ValueError('unsafe input mount')
    return ['create', '--name=qexec-' + execution_id, '--label=' + LABEL + '=' + execution_id,
        '--network=' + profile.network, '--read-only', '--cap-drop=ALL',
        '--security-opt=no-new-privileges:true', '--ipc=' + profile.ipc_mode,
        '--restart=' + profile.restart, '--user=' + str(profile.worker_uid) + ':' + str(profile.worker_uid),
        '--memory=' + str(profile.memory_bytes), '--memory-swap=' + str(profile.memory_bytes),
        '--pids-limit=' + str(profile.pids_limit), '--log-driver=none',
        '--tmpfs=/tmp:rw,noexec,nosuid,nodev,size=' + str(profile.scratch_bytes),
        '--mount=type=bind,source=' + source + ',destination=/input,readonly,bind-propagation=rprivate',
        '--workdir=/tmp', '--entrypoint=' + WORKER_ENTRYPOINT[0],
        context.release.document['worker_image_digest'], *WORKER_ENTRYPOINT[1:],
        '--execution-id', execution_id, '--input=/input']


def create_worker(context, *, execution_id, input_dir, profile):
    container = _run(*create_arguments(context, execution_id=execution_id, input_dir=input_dir, profile=profile)).decode('ascii').strip()
    return digest(container)


def _inspect(container_id):
    digest(container_id)
    rows = json.loads(_run('inspect', '--type=container', container_id))
    if type(rows) is not list or len(rows) != 1 or rows[0]['Id'] != container_id:
        raise ValueError('daemon container identity differs')
    return rows[0]


def inspect_worker(container_id, *, context, profile):
    row = _inspect(container_id)
    host, config = row['HostConfig'], row['Config']
    execution_id = config.get('Labels', {}).get(LABEL)
    identity(execution_id)
    expected_host = dict(NetworkMode='none', ReadonlyRootfs=True, CapDrop=['ALL'], CapAdd=None,
        Privileged=False, PidMode='', IpcMode='private', Memory=profile.memory_bytes,
        MemorySwap=profile.memory_bytes, PidsLimit=profile.pids_limit,
        RestartPolicy={'Name': 'no', 'MaximumRetryCount': 0})
    if any(host.get(key) != value for key, value in expected_host.items()):
        raise ValueError('effective Docker isolation differs')
    if host.get('SecurityOpt') != ['no-new-privileges:true'] or host.get('Devices') or host.get('DeviceRequests'):
        raise ValueError('effective Docker privileges differ')
    if (row['Image'] != context.release.document['worker_image_digest']
            or config['Image'] != row['Image'] or config['User'] != f'{profile.worker_uid}:{profile.worker_uid}'
            or config['Entrypoint'] != [WORKER_ENTRYPOINT[0]]
            or config['Cmd'] != [*WORKER_ENTRYPOINT[1:], '--execution-id', execution_id, '--input=/input']
            or config['Tty'] or config['OpenStdin']):
        raise ValueError('effective worker identity or command differs')
    mounts = row['Mounts']
    if (len(mounts) != 1 or mounts[0]['Type'] != 'bind' or mounts[0]['Destination'] != '/input'
            or mounts[0]['RW'] or mounts[0]['Propagation'] != 'rprivate'):
        raise ValueError('effective worker mounts differ')
    if host.get('Tmpfs') != {'/tmp': f'rw,noexec,nosuid,nodev,size={profile.scratch_bytes}'}:
        raise ValueError('effective worker scratch differs')
    return encoded(dict(container_id=container_id, execution_id=execution_id, image=row['Image'],
        input_source=mounts[0]['Source'], state=row['State']))


def start_and_capture(container_id, *, spool_dir, profile, maximum_wall_seconds):
    digest(container_id)
    root = Path(spool_dir)
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    deadline_seconds = profile.admission_seconds + maximum_wall_seconds + profile.capture_seconds
    started = time.monotonic_ns()
    process = subprocess.Popen(_command('start', '--attach', container_id), stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=docker_environment())
    output, logged = bytearray(), 0
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, 'stdout')
    selector.register(process.stderr, selectors.EVENT_READ, 'stderr')
    try:
        with (root / 'stderr.log').open('xb') as log:
            while selector.get_map():
                if time.monotonic_ns() - started >= deadline_seconds * 1000000000:
                    raise ValueError('worker supervisor wall timeout or missing EOF')
                for key, _ in selector.select(timeout=0.1):
                    chunk = os.read(key.fileobj.fileno(), 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                    elif key.data == 'stdout':
                        output.extend(chunk)
                        if len(output) > profile.output_byte_limit + 4:
                            raise ValueError('worker output frame exceeds limit')
                    else:
                        logged += len(chunk)
                        if logged > profile.log_byte_limit:
                            raise ValueError('worker stderr exceeds limit')
                        log.write(chunk)
            log.flush()
            os.fsync(log.fileno())
        process.wait(timeout=profile.capture_seconds)
        state = _inspect(container_id)['State']
        if process.returncode != 0 or state['Running'] or state['Status'] != 'exited' or state.get('Restarting'):
            raise ValueError('worker did not stop normally')
        return CapturedOutput(container_id, bytes(output), state['ExitCode'], state['OOMKilled'], time.monotonic_ns() - started)
    except BaseException:
        process.kill()
        process.wait(timeout=10)
        _run('kill', container_id) if _inspect(container_id)['State']['Running'] else None
        raise
    finally:
        selector.close()
        process.stdout.close()
        process.stderr.close()


def stop_owned_worker(container_id, *, execution_id):
    row = _inspect(container_id)
    if row['Config'].get('Labels', {}).get(LABEL) != identity(execution_id):
        raise ValueError('owned container identity differs')
    if row['State']['Running']:
        _run('kill', container_id)
