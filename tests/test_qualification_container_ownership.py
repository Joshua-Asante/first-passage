"""Ownership matching only; real Docker retirement is proved on disposable Linux."""
import copy
import importlib
import pytest


RUN='a'*32
IMAGE='sha256:'+'b'*64
RELEASE='c'*64
CONTAINER='d'*64


def case():
    row=dict(Id=CONTAINER,Name='/qexec-exec-1',Image=IMAGE,
        Config=dict(Image=IMAGE,Labels={'fp.qualification.host':RUN,
            'org.first-passage.qualification.execution':'exec-1'}))
    executions=[dict(execution_id='exec-1',container_id=CONTAINER,release_sha256=RELEASE)]
    return [row],executions


def validate(rows,executions):
    module=importlib.import_module('tools.qualification_verification.container_ownership')
    return module.owned_containers(rows,executions,run_id=RUN,image_id=IMAGE,release_sha256=RELEASE)


@pytest.mark.parametrize('recorded', [True,False])
def test_exact_durable_execution_allows_owned_container_cleanup(recorded):
    rows,executions=case()
    if not recorded: executions[0]['container_id']=None
    assert validate(rows,executions)==(CONTAINER,)


@pytest.mark.parametrize('change', ['foreign_id','foreign_name','foreign_image','foreign_image_config',
    'foreign_host','foreign_execution','missing_label','missing_dispatch','foreign_release','duplicate_container','duplicate_execution'])
def test_lookalike_container_cannot_be_retired(change):
    rows,executions=case()
    row=rows[0]
    if change=='foreign_id': row['Id']='e'*64
    elif change=='foreign_name': row['Name']='/someone-elses-container'
    elif change=='foreign_image': row['Image']='sha256:'+'e'*64
    elif change=='foreign_image_config': row['Config']['Image']='mutable:tag'
    elif change=='foreign_host': row['Config']['Labels']['fp.qualification.host']='e'*32
    elif change=='foreign_execution': row['Config']['Labels']['org.first-passage.qualification.execution']='exec-2'
    elif change=='missing_label': row['Config']['Labels']={}
    elif change=='missing_dispatch': executions=[]
    elif change=='foreign_release': executions[0]['release_sha256']='e'*64
    elif change=='duplicate_container': rows.append(copy.deepcopy(row))
    elif change=='duplicate_execution': executions.append(dict(executions[0]))
    with pytest.raises(ValueError,match='owned container'):
        validate(rows,executions)


def test_no_owned_containers_requires_no_deletion():
    assert validate([],[])==()
