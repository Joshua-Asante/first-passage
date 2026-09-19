"""Privileged S2 fixture enrollment within the existing disposable host owner."""
import hashlib
import json
from pathlib import Path
import subprocess
from . import host
from .container_ownership import campaign_host_slice as _scope, campaign_scopes



def install(root, manifest, profile_bytes):
    profile=json.loads(profile_bytes)
    memory_bytes=profile['memory_bytes']
    host.administrator(); host.protected(root)
    run_id = manifest['run_id']
    if run_id != root.name:
        raise ValueError('owned host identity differs')
    scope = _scope(run_id)
    prefix = scope[:-6]
    rule = ('polkit.addRule(function(action, subject) {\n'
        ' if (action.id == "org.freedesktop.systemd1.manage-units" && subject.user == "qexec" &&\n'
        '     action.lookup("unit").indexOf("' + prefix + '") == 0) return polkit.Result.YES;\n'
        '});\n').encode()
    path = Path('/etc/polkit-1/rules.d') / ('49-' + prefix + '.rules')
    enrollment = dict(schema='qualification_campaign_host/v1', host_run_id=run_id, scope=scope,
        memory_bytes=memory_bytes, profile_sha256=hashlib.sha256(profile_bytes).hexdigest(), rule_path=str(path), rule_sha256=hashlib.sha256(rule).hexdigest())
    host.save(root / 'campaign-host.json', enrollment, exclusive=True, mode=0o444)
    # Ownership is durable before either privileged side effect.
    with path.open('xb') as stream:
        stream.write(rule)
    path.chmod(0o644)
    host.run(['/usr/bin/busctl', '--system', '--timeout=5s', 'call', 'org.freedesktop.systemd1',
        '/org/freedesktop/systemd1', 'org.freedesktop.systemd1.Manager', 'StartTransientUnit',
        'ssa(sv)a(sa(sv))', scope, 'fail', '5', 'MemoryMax', 't', str(memory_bytes),
        'MemorySwapMax', 't', '0', 'MemoryOOMGroup', 'b', 'true',
        'MemoryAccounting', 'b', 'true', 'CPUAccounting', 'b', 'true', '0'])
    return enrollment


def restart(root, manifest, interpreter, bootstrap):
    enrollment = json.loads(host.protected(root / 'campaign-host.json').read_bytes())
    unit = enrollment['scope'][:-6] + 'supervisor.service'
    subprocess.run(['/usr/bin/systemctl', '--system', '--no-ask-password', 'stop', unit],
                   stdin=subprocess.DEVNULL, capture_output=True, timeout=15, check=False)
    host.run(['/usr/bin/systemd-run', '--system', '--collect', '--unit=' + unit, '--slice=' + enrollment['scope'],
        '--uid=' + str(manifest['roles']['qexec']), '--property=KillMode=control-group',
        '--property=Restart=no', '--property=MemoryAccounting=yes', '--',
        interpreter, '-I', str(bootstrap), 'supervisor'])


def cleanup(root, manifest, *, retire=False):
    """Stop only enrolled S2 scope, verify absence, retain manager observations."""
    path = root / 'campaign-host.json'
    if not path.exists():
        return
    enrollment = json.loads(host.protected(path).read_bytes())
    scope = _scope(manifest['run_id'])
    if enrollment['host_run_id'] != root.name or enrollment['scope'] != scope:
        raise ValueError('S2 host cleanup enrollment differs')
    result = subprocess.run(['/usr/bin/systemctl', '--system', '--no-ask-password', 'stop', scope],
        stdin=subprocess.DEVNULL, capture_output=True, timeout=30, check=False)
    group = Path('/sys/fs/cgroup') / scope
    if group.exists() and 'populated 1' in (group / 'cgroup.events').read_text():
        raise ValueError('S2 owned scope remains populated')
    docker = [manifest['host_config']['docker'], '--host=unix:///var/run/docker.sock']
    containers = host.run([*docker, 'ps', '--all', '--quiet', '--no-trunc',
                           '--filter=label=fp.s2.host=' + root.name]).split()
    observations = []
    if containers:
        import sqlite3
        with sqlite3.connect((root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True) as connection:
            enrollments = [json.loads(bytes(row[0])) for row in connection.execute(
                "SELECT body FROM full_campaign_objects WHERE role LIKE 'supervision_%' AND role NOT LIKE 'supervision_event_%' AND role NOT LIKE 'supervision_control_%'")]
        for item in enrollments:
            if (item['schema']!='qualification_campaign_supervision/v1' or item['host_run_id']!=root.name
                    or item['scopes']!=campaign_scopes(root.name,item['attempt_id'],item['work_id'])):
                raise ValueError('durable S2 scope binding differs')
        expected = {'/fpqs2-' + hashlib.sha256(json.dumps(item,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(): item for item in enrollments}
        image = json.loads((root / 'code/qualification-installation/release.json').read_bytes())['worker_image_digest']
        for row in json.loads(host.run([*docker, 'inspect', '--type=container', *containers])):
            item = expected.get(row['Name'])
            if (item is None or item['host_run_id'] != root.name or row['Image'] != image
                    or row['Config']['Labels'].get('fp.s2.host') != root.name
                    or row['State']['Running'] or row['State']['Pid']):
                raise ValueError('S2 cleanup lacks owned container absence proof')
            observations.append(row)
            host.run([*docker, 'rm', '--', row['Id']])
    host.save(root / 'evidence/campaign-cleanup.json', dict(scope=scope, populated=False,
        stop_exit=result.returncode, containers=observations))
    if retire:
        rule = Path(enrollment['rule_path'])
        expected_path = Path('/etc/polkit-1/rules.d') / ('49-' + scope[:-6] + '.rules')
        if rule != expected_path:
            raise ValueError('owned policy rule path differs')
        if rule.exists():
            if hashlib.sha256(host.protected(rule).read_bytes()).hexdigest() != enrollment['rule_sha256']:
                raise ValueError('owned policy rule changed')
            rule.unlink()
