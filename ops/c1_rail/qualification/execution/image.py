"""Administrator-only disposable worker builder; no qualification authority."""
import hashlib
import json
from pathlib import Path
import re

from c1_rail.qualification.execution.files import read_regular
from c1_rail.qualification.execution.runtime import source_closure, SIGNING_CONFIGURATION
from tools.qualification_verification import host
from tools.qualification_verification.container_ownership import HOST_LABEL, BUILD_LABEL


def prepare_context(source, destination, *, base_digest):
    if type(base_digest) is not str or re.fullmatch(r'python@sha256:[0-9a-f]{64}',base_digest) is None:
        raise ValueError('pinned approved Python base digest required')
    source,destination=Path(source),Path(destination)
    closure=source_closure(source,'worker')
    payloads={row['path']:read_regular(source,row['path'],limit=4*1024*1024) for row in closure.values()}
    for row in closure.values():
        if hashlib.sha256(payloads[row['path']]).hexdigest()!=row['sha256']:
            raise ValueError('worker source changed during context construction')
    for relative in ('requirements-ops.lock',SIGNING_CONFIGURATION):
        payloads[relative]=read_regular(source,relative,limit=1024*1024)
    signing=host.signing_requirements(payloads[SIGNING_CONFIGURATION],
        read_regular(source,'tools/qualification_verification/signing-wheel.json',limit=65536))
    destination.mkdir(mode=0o700,parents=True,exist_ok=False)
    lines=['FROM '+base_digest,'ENV PYTHONDONTWRITEBYTECODE=1 PIP_DISABLE_PIP_VERSION_CHECK=1']
    for relative,raw in sorted(payloads.items()):
        target=destination/'code'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(raw)
        lines.append('COPY '+json.dumps(['code/'+relative,'/opt/qualification/code/'+relative]))
    (destination/'signing-requirements.txt').write_bytes(signing)
    lines.extend(['COPY ["signing-requirements.txt", "/opt/signing-requirements.txt"]',
        'RUN python -I -m venv --copies /opt/ops && /opt/ops/bin/python -I -m pip install --require-hashes --only-binary=:all: -r /opt/qualification/code/requirements-ops.lock -r /opt/signing-requirements.txt',
        'RUN cp /opt/qualification/code/deploy/qualification/bootstrap.py /opt/qualification/bootstrap.py && chmod -R go-w /opt/qualification /opt/ops',
        'ENTRYPOINT ["/opt/ops/bin/python", "-I", "/opt/qualification/bootstrap.py", "worker"]'])
    (destination/'Dockerfile').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    return dict(base_digest=base_digest,sources=closure,
        signing_requirements_sha256=hashlib.sha256(signing).hexdigest())


def build_worker(root, manifest):
    """Caller holds host ownership lock; registry survives an interrupted build."""
    root=Path(root)
    host.administrator(); host.protected(root)
    config=manifest['host_config']
    if manifest['run_id']!=root.name or manifest['state']!='host_ready_boundary_unconfigured':
        raise ValueError('ready canonical host ownership required')
    registry=host.begin_boundary_build(root)
    group=host.create_process_group(root)
    docker=[config['docker'],'--host','unix:///var/run/docker.sock']
    version=config['python_version']
    if re.fullmatch(r'\d+\.\d+\.\d+',version) is None:
        raise ValueError('canonical Python patch required')
    reference='python:'+version+'-slim-bookworm'
    host.run_owned(group,[*docker,'pull',reference],interpreter=config['python'],timeout=180)
    inspected=json.loads(host.run([*docker,'image','inspect',reference]))
    digests=inspected[0]['RepoDigests'] if type(inspected) is list and len(inspected)==1 else []
    approved=[value for value in digests if re.fullmatch(r'python@sha256:[0-9a-f]{64}',value)]
    if len(approved)!=1:
        raise ValueError('resolved Python base image identity differs')
    context=root/'keys/worker-build'
    evidence=prepare_context(root/'code',context,base_digest=approved[0])
    image_file=context/'image-id'
    host.run_owned(group,[*docker,'build','--pull=false','--network=default','--iidfile',str(image_file),
        '--label',HOST_LABEL+'='+root.name,'--label',BUILD_LABEL+'='+registry['build_id'],str(context)],
        interpreter=config['python'],timeout=900)
    image_id=image_file.read_text().strip()
    if re.fullmatch(r'sha256:[0-9a-f]{64}',image_id) is None:
        raise ValueError('built worker content identity missing')
    inspected=json.loads(host.run([*docker,'image','inspect',image_id]))
    if (len(inspected)!=1 or inspected[0]['Id']!=image_id
            or inspected[0]['Config']['Labels'].get(HOST_LABEL)!=root.name
            or inspected[0]['Config']['Labels'].get(BUILD_LABEL)!=registry['build_id']):
        raise ValueError('built worker ownership differs')
    evidence.update(image_id=image_id,base_reference=reference,build_id=registry['build_id'])
    host.save(root/'evidence/worker-image.json',evidence,exclusive=True,mode=0o444)
    return image_id
