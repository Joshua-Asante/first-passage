"""Real processes and containers on the canonical disposable host only."""
import base64
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from uuid import uuid4
import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from scripts.qualification_boundary_environment import inspect_environment,require_environment
from tools.qualification_verification import host
from c1_rail.qualification.execution.image import build_worker
from tools.qualification_verification.role_policy import ROLE_GROUPS
# Generic socket/framing modules are loaded here, before any fork.
import private_route


CLIENT_DRIVER='''import json,sys
from pathlib import Path
root=Path(sys.argv[1])
sys.dont_write_bytecode=True
sys.path[:0]=[str(root/p) for p in ('ops','core','lab','governance','')]
from c1_rail.qualification.execution.client import request
doc=json.loads(sys.argv[3]); operation=doc.pop('operation')
sys.stdout.buffer.write(request(Path(sys.argv[2]),operation,doc))
'''

RAW_DRIVER='''import json,socket,sys
from pathlib import Path
root=Path(sys.argv[1]); sys.dont_write_bytecode=True
sys.path[:0]=[str(root/p) for p in ('ops','core','lab','governance','')]
from c1_rail.qualification.execution.protocol import encode_frame
from c1_rail.qualification.execution.transport import receive
with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as peer:
    peer.settimeout(30); peer.connect(sys.argv[2])
    peer.sendall(encode_frame(sys.argv[3].encode(),limit=1048576))
    peer.shutdown(socket.SHUT_WR)
    sys.stdout.buffer.write(receive(peer,limit=1048576))
'''


class Boundary:
    def __init__(self,path):
        self.path=path; self.root=path.parent
        self.manifest=json.loads(path.read_bytes()); self.roles=self.manifest['roles']
        self.code=self.root/'code'; self.python=str(self.root/'env/bin/python')
        self.output=self.root/'evidence/boundary'; self.output.mkdir(mode=0o700)
        self.group=host.create_process_group(self.root)
        self.image=build_worker(self.root,self.manifest)
        self.diagnostic = os.environ.get('FP_QUALIFICATION_S2') == '1'
        self.admin('install','--image',self.image,*(['--diagnostic'] if self.diagnostic else []))
        self.installation=self.code/'qualification-installation'
        self.config=json.loads((self.installation/'supervisor.json').read_bytes())
        report=inspect_environment(self.installation/'test-instance.json',(self.installation/'profile.json').read_bytes())
        host.save(self.output/'environment.json',report,exclusive=True)
        require_environment(report)
        self.service=None; self.streams=[]; self.restart()

    def admin(self,operation,*arguments):
        try:
            result=host.run_owned(self.group,[self.python,'-I',str(self.code/'tests/integration/qualification_boundary/fixture_install.py'),
                operation,'--manifest',str(self.path),*arguments],interpreter=self.python,timeout=180)
        except subprocess.CalledProcessError as exc:
            # The installer's own diagnostics are the only record of a refusal;
            # run_owned captures them, so surface the tail in the test report.
            raise AssertionError('fixture_install '+operation+' '+' '.join(arguments)+' exited '+str(exc.returncode)
                +'\n--- installer stderr (tail) ---\n'+(exc.stderr or '')[-6000:]) from exc
        return json.loads(result)

    def identity(self,role,command):
        import grp
        uid=self.roles[role]
        groups=[str(grp.getgrnam(name).gr_gid) for name in ROLE_GROUPS[role]]
        return ['/usr/bin/setpriv','--reuid='+str(uid),'--regid='+str(uid),
            '--groups='+','.join(groups) if groups else '--clear-groups',*command]

    def request(self,operation,*,role='qclient',**fields):
        command=[self.python,'-I','-c',CLIENT_DRIVER,str(self.code),self.config['socket_path'],
                 encoded(dict(operation=operation,**fields)).decode()]
        if role!='administrator': command=self.identity(role,command)
        raw=host.run_owned(self.group,command,interpreter=self.python,timeout=60)
        return raw.encode()

    def status(self,attempt):
        return json.loads(self.request('STATUS',attempt_id=attempt))

    def raw_request(self,document,*,role='qclient'):
        """Public historical retries only; the schedule schema never rides this exec."""
        if type(document) is dict and document.get('schema')==private_route.SCHEDULE_SCHEMA:
            raise ValueError('private route requires the bounded transport child')
        command=self.identity(role,[self.python,'-I','-c',RAW_DRIVER,str(self.code),
            self.config['socket_path'],encoded(document).decode()])
        return json.loads(host.run_owned(self.group,command,interpreter=self.python,timeout=60))

    def schedule(self,document,*,role='qexec'):
        """Private route: one pre-encoded frame through a forked transport child.

        The child adopts the role identity before connecting and moves bytes
        only; the warm service funds, materializes and launches. A non-service
        role is used solely to prove the route refuses it.
        """
        import grp
        frame=private_route.schedule_frame(document)
        uid=self.roles[role]
        groups=[grp.getgrnam(name).gr_gid for name in ROLE_GROUPS[role]]
        reply=private_route.forked_exchange(frame,socket_path=self.config['socket_path'],
            uid=uid,gid=uid,groups=groups,timeout=60)
        return json.loads(reply)

    def prepare(self,*,idle,fault=None,depth_valid_seconds=14400):
        attempt='linux-'+uuid4().hex
        return self.admin('prepare','--attempt',attempt,*(['--idle'] if idle else []),
            *(['--fault',fault] if fault else []),'--depth-valid-seconds',str(depth_valid_seconds))

    def submit(self,bundle):
        return json.loads(self.request('SUBMIT_N1',attempt_id=bundle['attempt_id'],bundle_sha256=bundle['bundle_sha256']))

    def wait(self,attempt,states=('ATTESTED',)):
        deadline=time.monotonic()+300
        while time.monotonic()<deadline:
            row=self.status(attempt)
            if row['state'] in states:
                host.save(self.output/(attempt+'-status.json'),row)
                return row
            if row['state'] in ('ABORTED','IN_DOUBT'):
                raise AssertionError('unexpected terminal execution: '+str(row))
            time.sleep(.05)
        raise AssertionError('bounded execution wait expired')

    def assess(self,attempt):
        raw=host.run_owned(self.group,self.identity('qg5',[self.python,'-I',str(self.code/'bootstrap.py'),
            'g5','--attempt-id',attempt]),interpreter=self.python,timeout=180)
        result=json.loads(raw)
        host.save(self.output/(attempt+'-receipt.json'),result)
        return result

    def fetch(self,attempt,digest):
        return self.request('FETCH',role='qg5',attempt_id=attempt,object_sha256=digest)

    def events(self,attempt):
        import sqlite3
        journal=self.root/'data/journal.sqlite'
        with sqlite3.connect(journal.as_uri()+'?mode=ro',uri=True) as connection:
            rows=[json.loads(row[0]) for row in connection.execute(
                'SELECT body FROM events WHERE attempt_id=? ORDER BY sequence',(attempt,))]
        host.save(self.output/(attempt+'-events.json'),rows)
        return rows

    def worker_log(self,execution_id):
        raw=(self.root/'data/spool'/execution_id/'stderr.log').read_bytes()
        (self.output/(execution_id+'-worker.stderr')).write_bytes(raw)
        return raw

    def inspect(self,container):
        row=json.loads(host.run([self.manifest['host_config']['docker'],'--host','unix:///var/run/docker.sock',
            'inspect','--type=container',container]))[0]
        host.save(self.output/(container+'-inspection.json'),row)
        return row

    def starts(self,container):
        return self.docker_events(container, 'start')

    def docker_events(self,container,event):
        raw=host.run_owned(self.group,[self.manifest['host_config']['docker'],'--host','unix:///var/run/docker.sock',
            'events','--since=0','--until='+str(time.time()),'--filter=type=container',
            '--filter=container='+container,'--filter=event='+event,'--format={{json .}}'],interpreter=self.python)
        rows=[json.loads(line) for line in raw.splitlines()]
        assert all(row['Actor']['ID']==container and row['Action']==event for row in rows)
        host.save(self.output/(container+'-'+event+'-events.json'),rows)
        return rows

    def restart(self, *, checkpoint=None):
        if self.diagnostic:
            from tools.qualification_verification import campaign_host
            campaign_host.restart(self.root,self.manifest,self.python,self.code/'bootstrap.py')
            deadline=time.monotonic()+60
            while time.monotonic()<deadline:
                try:
                    response=self.raw_request(dict(schema='qualification_campaign_request/v2', operation='STATUS',
                        attempt_id='readiness-probe'))
                    if response.get('ok') is False and response.get('error') == repr('readiness-probe'): return
                except (OSError,subprocess.SubprocessError): pass
                time.sleep(.1)
            raise AssertionError('diagnostic supervisor startup expired')
        if self.service is not None and self.service.poll() is None:
            self.service.kill(); self.service.wait(timeout=15)
        stdout=(self.output/('supervisor-'+uuid4().hex+'.stdout')).open('wb')
        stderr=(self.output/('supervisor-'+uuid4().hex+'.stderr')).open('wb')
        self.streams.extend([stdout,stderr])
        command=[self.python,'-I',str(self.code/'bootstrap.py'),'supervisor']
        if checkpoint is not None:
            self.checkpoint_receipt=self.root/'data'/('checkpoint-'+uuid4().hex+'.json')
            command=[self.python,'-I',str(self.code/'tests/integration/qualification_boundary/supervisor_checkpoint.py'),
                     str(self.code),checkpoint,str(self.checkpoint_receipt)]
        self.service=host.start_owned(self.root,self.identity('qexec',command),
            stdout=stdout,stderr=stderr,interpreter=self.python)
        deadline=time.monotonic()+60
        while time.monotonic()<deadline:
            if self.service.poll() is not None: raise AssertionError('supervisor exited; inspect retained stderr')
            socket=Path(self.config['socket_path'])
            if socket.exists():
                # A stale socket can survive SIGKILL; require an authenticated reply.
                try: self.status('readiness-probe')
                except subprocess.CalledProcessError as exc:
                    if 'unknown attempt' in (exc.stderr or ''): return
                time.sleep(.1)
            else: time.sleep(.1)
        raise AssertionError('protected supervisor startup expired')

    def close(self):
        if self.diagnostic:
            from tools.qualification_verification import campaign_host
            campaign_host.cleanup(self.root,self.manifest)
        if self.service is not None and self.service.poll() is None:
            self.service.kill(); self.service.wait(timeout=15)
        for stream in self.streams: stream.close()
        # This TEST_ONLY archive contains public keys, approvals and synthetic
        # retained inputs, never private credentials or the ownership manifest.
        import hashlib
        import sqlite3
        from c1_rail.qualification.execution.files import read_regular
        source=self.root/'data/objects'
        target=self.output/'objects'; target.mkdir(exist_ok=True)
        for path in source.iterdir() if source.exists() else ():
            raw=read_regular(source,path.name,limit=100000000)
            if hashlib.sha256(raw).hexdigest()!=path.name: raise ValueError('exported object identity differs')
            (target/path.name).write_bytes(raw)
        journal=self.root/'data/journal.sqlite'
        if journal.exists():
            with sqlite3.connect(journal.as_uri()+'?mode=ro',uri=True) as connection:
                with sqlite3.connect(self.output/'journal.sqlite') as destination: connection.backup(destination)
        (self.output/'public-keys.json').write_bytes((self.installation/'keys.json').read_bytes())
        host.save(self.output/'export-scope.json',dict(authority_class='TEST_ONLY',inputs='synthetic',private_credentials=False))


@pytest.fixture(scope='session')
def real_boundary():
    configured=os.environ.get('FP_QUALIFICATION_HOST_MANIFEST')
    if not configured: pytest.skip('explicit disposable Linux acceptance run required')
    if sys.platform!='linux' or os.geteuid()!=0: pytest.fail('Linux administrator required')
    boundary=Boundary(host.protected(Path(configured)))
    try: yield boundary
    finally: boundary.close()
