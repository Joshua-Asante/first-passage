"""Cleanup planning uses exact durable ownership; no Linux acceptance claim."""
import json
import os
import sqlite3
from pathlib import Path
import pytest
from tools.qualification_verification import host

RUN='a'*32
BUILD='b'*32
IMAGE='sha256:'+'c'*64
RELEASE='d'*64
CONTAINER='e'*64


@pytest.fixture
def cleanup_case(tmp_path,monkeypatch):
    root=tmp_path/RUN
    root.mkdir()
    (root/'data').mkdir()
    registry=dict(schema='qualification_boundary_ownership/v1',run_id=RUN,build_id=BUILD,
                  image_id=IMAGE,release_sha256=RELEASE)
    (root/'boundary-resources.json').write_text(json.dumps(registry))
    with sqlite3.connect(root/'data/journal.sqlite') as connection:
        connection.execute('CREATE TABLE executions(execution_id TEXT,container_id TEXT,release_sha256 TEXT)')
        connection.execute('INSERT INTO executions VALUES(?,?,?)',('exec-1',CONTAINER,RELEASE))
    container=dict(Id=CONTAINER,Name='/qexec-exec-1',Image=IMAGE,Config=dict(Image=IMAGE,
        Labels={'fp.qualification.host':RUN,'org.first-passage.qualification.execution':'exec-1'}))
    image=dict(Id=IMAGE,Config=dict(Labels={'fp.qualification.host':RUN,'fp.qualification.build':BUILD}))
    calls=[]
    def run(command):
        calls.append(command)
        arguments=command[3:]
        if arguments[0]=='ps': return CONTAINER
        if arguments[:2]==['image','ls']: return IMAGE
        if arguments[:2]==['inspect','--type=container']: return json.dumps([container])
        if arguments[:2]==['image','inspect']: return json.dumps([image])
        raise AssertionError(command)
    monkeypatch.setattr(host,'run',run)
    monkeypatch.setattr(host,'protected',lambda path:Path(path))
    # Permission policy is tested on Linux; these units use a real readonly SQL query.
    monkeypatch.setattr(host,'owned_journal',lambda path,uid:Path(path),raising=False)
    manifest=dict(roles={'qexec':61001},host_config={'docker':'/usr/bin/docker'})
    return root,manifest,registry,container,image,calls


def test_cleanup_plan_binds_actual_inspection_to_dispatch_and_build(cleanup_case):
    root,manifest,_,_,_,calls=cleanup_case
    assert host.boundary_cleanup_plan(root,manifest)==dict(containers=[CONTAINER],images=[IMAGE])
    assert all('rm' not in call and 'kill' not in call for call in calls)


@pytest.mark.parametrize('change', ['container','image','build','release','dispatch'])
def test_cleanup_refuses_foreign_resources_before_any_mutation(cleanup_case,change):
    root,manifest,registry,container,image,calls=cleanup_case
    if change=='container': container['Name']='/foreign'
    elif change=='image': image['Id']='sha256:'+'f'*64
    elif change=='build': image['Config']['Labels']['fp.qualification.build']='f'*32
    elif change=='release': registry['release_sha256']='f'*64
    else:
        with sqlite3.connect(root/'data/journal.sqlite') as connection: connection.execute('DELETE FROM executions')
    (root/'boundary-resources.json').write_text(json.dumps(registry))
    with pytest.raises(ValueError): host.boundary_cleanup_plan(root,manifest)
    assert all('rm' not in call and 'kill' not in call for call in calls)


def test_interrupted_build_intent_owns_only_its_exact_labeled_image(cleanup_case,monkeypatch):
    root,manifest,registry,_,image,_=cleanup_case
    registry.update(image_id=None,release_sha256=None)
    (root/'boundary-resources.json').write_text(json.dumps(registry))
    def run(command):
        arguments=command[3:]
        if arguments[0]=='ps': return ''
        if arguments[:2]==['image','ls']: return IMAGE
        if arguments[:2]==['image','inspect']: return json.dumps([image])
        raise AssertionError(command)
    monkeypatch.setattr(host,'run',run)
    assert host.boundary_cleanup_plan(root,manifest)==dict(containers=[],images=[IMAGE])


def test_service_child_is_registered_before_asynchronous_launch(tmp_path,monkeypatch):
    group=tmp_path/'cgroup'
    calls=[]
    def create(root):
        calls.append(('registered',root)); return group
    def spawn(command,**kwargs):
        calls.append(('spawn',command,kwargs)); return object()
    monkeypatch.setattr(host,'create_process_group',create)
    monkeypatch.setattr(host.subprocess,'Popen',spawn)
    host.start_owned(tmp_path,['/usr/bin/setpriv','--reuid=61001','/fixed/env/python','-I','/fixed/bootstrap.py','supervisor'],
                     stdout=None,stderr=None,interpreter='/fixed/env/python')
    assert calls[0]==('registered',tmp_path)
    command=calls[1][1]
    assert command[:4]==['/fixed/env/python','-I','-c',host.ENTER_PROCESS_GROUP]
    assert command[4]==str(group/'cgroup.procs')
    assert command[5]=='/usr/bin/setpriv'
