"""Image context tests do not establish a built or isolated worker."""
import importlib
import json
from pathlib import Path
import pytest
from c1_rail.qualification.execution.runtime import source_closure

ROOT=Path(__file__).resolve().parents[1]


def test_image_context_is_exact_worker_closure_and_canonical_dependencies(tmp_path):
    image=importlib.import_module('c1_rail.qualification.execution.image')
    result=image.prepare_context(ROOT,tmp_path/'context',base_digest='python@sha256:'+'a'*64)
    closure=source_closure(ROOT,'worker')
    assert set(result['sources'])==set(closure)
    for row in closure.values():
        assert (tmp_path/'context/code'/row['path']).read_bytes()==(ROOT/row['path']).read_bytes()
    actual={p.relative_to(tmp_path/'context').as_posix() for p in (tmp_path/'context').rglob('*') if p.is_file()}
    expected={'code/'+row['path'] for row in closure.values()}
    expected.update({'Dockerfile','signing-requirements.txt','code/requirements-ops.lock',
                     'code/tools/local_verification/requirements-extra.txt'})
    assert actual==expected
    dockerfile=(tmp_path/'context/Dockerfile').read_text()
    assert dockerfile.startswith('FROM python@sha256:'+'a'*64+'\n')
    assert '--require-hashes' in dockerfile and '--only-binary=:all:' in dockerfile
    assert 'COPY .' not in dockerfile and 'COPY code/' not in dockerfile
    assert not any(name.endswith(('.service','.g5','.signing','.credentials')) for name in closure)


@pytest.mark.parametrize('base',['python:latest','python@sha256:bad','python@sha256:'+'a'*64+'\nRUN false'])
def test_image_context_refuses_unpinned_or_injected_base(tmp_path,base):
    image=importlib.import_module('c1_rail.qualification.execution.image')
    with pytest.raises(ValueError): image.prepare_context(ROOT,tmp_path/'context',base_digest=base)
    assert not (tmp_path/'context').exists()


def test_builder_uses_canonical_ready_state_and_registered_children(tmp_path,monkeypatch):
    image=importlib.import_module('c1_rail.qualification.execution.image')
    root=tmp_path/('a'*32); root.mkdir()
    (root/'keys').mkdir(); (root/'evidence').mkdir()
    config=dict(docker='/usr/bin/docker',python='/usr/bin/python3',python_version='3.12.3')
    manifest=dict(run_id=root.name,state='host_ready_boundary_unconfigured',host_config=config)
    calls=[]
    monkeypatch.setattr(image.host,'administrator',lambda:None)
    monkeypatch.setattr(image.host,'protected',lambda path:path)
    def begin(path):
        calls.append('enrolled'); return dict(build_id='b'*32)
    monkeypatch.setattr(image.host,'begin_boundary_build',begin)
    monkeypatch.setattr(image.host,'create_process_group',lambda path:root/'group')
    def execute(group,command,**kwargs):
        assert calls[0]=='enrolled' and group==root/'group'
        assert kwargs['timeout']>=180
        calls.append(command)
        if 'build' in command: Path(command[command.index('--iidfile')+1]).write_text('sha256:'+'c'*64)
    monkeypatch.setattr(image.host,'run_owned',execute)
    def inspect(command):
        if command[-1].startswith('python:'):
            return json.dumps([dict(RepoDigests=['python@sha256:'+'d'*64])])
        return json.dumps([dict(Id='sha256:'+'c'*64,Config=dict(Labels={image.HOST_LABEL:root.name,image.BUILD_LABEL:'b'*32}))])
    monkeypatch.setattr(image.host,'run',inspect)
    def prepare(source,target,**kwargs): target.mkdir(); return kwargs
    monkeypatch.setattr(image,'prepare_context',prepare)
    monkeypatch.setattr(image.host,'save',lambda path,data,**kwargs:path.write_text(json.dumps(data)))
    assert image.build_worker(root,manifest)=='sha256:'+'c'*64
    assert calls[1][3:]==['pull','python:3.12.3-slim-bookworm']
    assert json.loads((root/'evidence/worker-image.json').read_bytes())['base_digest']=='python@sha256:'+'d'*64
