"""Direct OS denials from the real client and installed worker identities."""
import errno
import json
import time

import pytest

from tools.qualification_verification import host


PROBE = '''import json,os,socket,sys
results=[]
for label,operation,path in json.loads(sys.argv[1]):
    try:
        if operation=='connect':
            with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as peer:
                peer.settimeout(2); peer.connect(path)
        elif operation=='unlink':
            os.unlink(path)
        else:
            flags=os.O_RDONLY if operation=='read' else os.O_WRONLY
            fd=os.open(path,flags)
            os.close(fd)
        results.append(dict(label=label,operation=operation,allowed=True))
    except OSError as exc:
        results.append(dict(label=label,operation=operation,allowed=False,errno=exc.errno))
print(json.dumps(dict(uid=os.geteuid(),gid=os.getegid(),groups=os.getgroups(),results=results)))
'''


@pytest.mark.parametrize('role', ['qclient', 'worker'])
def test_real_untrusted_identity_cannot_access_authority_or_write_code(real_boundary, role):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True, fault='stop') if role == 'worker' else boundary.prepare(idle=True)
    boundary.submit(bundle)
    state = boundary.wait(bundle['attempt_id'], states=('RUNNING',) if role == 'worker' else ('ATTESTED',))
    config = boundary.config
    private = [('execution_key', config['execution_credential']),
               ('result_key', str(boundary.root / 'keys/qg5/credential.json')),
               ('journal', str(boundary.root / 'data/journal.sqlite'))]
    probes = [(label, mode, path) for label, path in private for mode in ('read', 'write')]
    probes.append(('docker_socket', 'connect', '/var/run/docker.sock'))
    if role == 'worker':
        probes += [('service_socket', 'connect', config['socket_path']),
                   ('code', 'read', '/opt/qualification/bootstrap.py'),
                   ('code', 'write', '/opt/qualification/bootstrap.py'),
                   ('input', 'read', '/input/plan.json'), ('input', 'write', '/input/plan.json')]
        command = [boundary.manifest['host_config']['docker'], '--host=unix:///var/run/docker.sock',
                   'exec', state['container_id'], '/opt/ops/bin/python', '-I', '-c', PROBE, json.dumps(probes)]
    else:
        probes += [('code', 'read', str(boundary.code / 'bootstrap.py')),
                   ('code', 'write', str(boundary.code / 'bootstrap.py')),
                   ('service_socket', 'unlink', config['socket_path'])]
        command = boundary.identity('qclient', [boundary.python, '-I', '-c', PROBE, json.dumps(probes)])
    try:
        report = json.loads(host.run_owned(boundary.group, command, interpreter=boundary.python, timeout=30))
        host.save(boundary.output / (bundle['attempt_id'] + '-permissions.json'), report)
        expected_uid = json.loads((boundary.installation / 'profile.json').read_bytes())['worker_uid'] if role == 'worker' else boundary.roles[role]
        assert report['uid'] == report['gid'] == expected_uid
        if role == 'worker':
            assert set(report['groups']) <= {expected_uid}
        for row in report['results']:
            if row['label'] in ('code', 'input') and row['operation'] == 'read':
                assert row['allowed'] is True
            else:
                assert row['allowed'] is False, row
                allowed_errors = {errno.EACCES, errno.EPERM, errno.EROFS}
                if role == 'worker':
                    allowed_errors.add(errno.ENOENT)  # Host resources are not mounted.
                assert row['errno'] in allowed_errors, row
        assert len(boundary.starts(state['container_id'])) == 1
    finally:
        if role == 'worker':
            boundary.void(bundle)
            # Wait for the real worker termination before a subsequent test.
            deadline = time.monotonic() + 30
            while boundary.inspect(state['container_id'])['State']['Running']:
                assert time.monotonic() < deadline
                time.sleep(.05)
