"""Closed service dispatch tests; OS peer authentication is tested on Linux."""
import importlib

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded


@pytest.mark.parametrize('operation', ['COMPLETE_CHECKPOINT', 'SIGN', 'CONSUME', 'SET_VERDICT'])
def test_unrecognized_authority_operation_is_rejected_before_dispatch(operation):
    service = importlib.import_module('c1_rail.qualification.execution.service')
    instance = object.__new__(service.ExecutionService)
    with pytest.raises(ValueError, match='UNKNOWN_OPERATION'):
        instance.handle_request(2001, encoded(dict(operation=operation, attempt_id='fixture')))


@pytest.mark.parametrize('operation', ['SNAPSHOT', 'STORE_ARTIFACT', 'STORE_RESULT', 'COMMIT_N1_RESULT', 'VOID'])
def test_client_identity_cannot_invoke_protected_operations(operation):
    service = importlib.import_module('c1_rail.qualification.execution.service')
    assert not service.permitted('client', operation)


def test_uid_roles_must_be_distinct():
    service = importlib.import_module('c1_rail.qualification.execution.service')
    with pytest.raises(ValueError, match='distinct'):
        service.uid_roles(dict(client_uid=1001, g5_uid=1001, operator_uid=0, service_uid=1002))


def test_capture_recovery_signing_failure_leaves_history_available(tmp_path,monkeypatch):
    from test_store import captured
    service=importlib.import_module('c1_rail.qualification.execution.service')
    store,record,_=captured(tmp_path)
    instance=object.__new__(service.ExecutionService)
    instance.store=store
    instance.config={'execution_credential':'/protected/key'}
    def failed_sign(*args,**kwargs): raise ValueError('expired fixture approval')
    monkeypatch.setattr(service,'sign_captured',failed_sign)
    instance.recover_service()
    assert store.execution_rows()[0]['state']=='CAPTURED'
    assert instance.recovery_issues[record.execution_id]=='ATTESTATION_PENDING'
    instance.roles={1001:'g5'}
    assert instance.handle_request(1001,encoded(dict(operation='STATUS',attempt_id=record.attempt_id)))


def test_recovery_persists_uncertainty_before_failed_container_cleanup(tmp_path,monkeypatch):
    from test_store import reserved,NOW
    service=importlib.import_module('c1_rail.qualification.execution.service')
    store,record,_=reserved(tmp_path)
    record=store.record_container(record.execution_id,'c'*64,expected_revision=record.revision)
    record=store.record_start_intent(record.execution_id,expected_revision=record.revision,now=NOW)
    instance=object.__new__(service.ExecutionService)
    instance.store=store
    def failed_stop(*args,**kwargs): raise ValueError('daemon unavailable')
    monkeypatch.setattr(service,'stop_owned_worker',failed_stop)
    instance.recover_service()
    assert store.execution_rows()[0]['state']=='IN_DOUBT'
    assert instance.recovery_issues[record.execution_id]=='CLEANUP_PENDING'
    before=store.status(record.attempt_id)
    instance.recover_service()
    assert store.status(record.attempt_id)==before


def test_recovery_discovers_unrecorded_owned_container_without_redraw(tmp_path,monkeypatch):
    from test_store import reserved
    service=importlib.import_module('c1_rail.qualification.execution.service')
    store,record,_=reserved(tmp_path)
    instance=object.__new__(service.ExecutionService)
    instance.store=store
    instance.config={'host_run_id':'a'*32}
    instance.release=encoded({'worker_image_digest':'sha256:'+'b'*64})
    found=[]
    def find(execution_id,**kwargs):
        assert store.execution_rows()[0]['state']=='IN_DOUBT'
        assert kwargs['host_run_id']=='a'*32 and kwargs['image_id']=='sha256:'+'b'*64
        found.append(execution_id)
        return 'c'*64
    stopped=[]
    monkeypatch.setattr(service,'find_owned_worker',find,raising=False)
    monkeypatch.setattr(service,'stop_owned_worker',lambda container,**kwargs:stopped.append(container))
    instance.recover_service()
    assert found==[record.execution_id] and stopped==['c'*64]
    assert b'"launch_intent_count":0' in store.status(record.attempt_id)
    before=store.status(record.attempt_id)
    instance.recover_service()
    assert found==[record.execution_id]*2 and store.status(record.attempt_id)==before


def test_signed_nonempty_registry_never_reserves_or_schedules_worker(tmp_path,monkeypatch):
    import threading
    from types import SimpleNamespace
    from bundle_fixture import build_bundle
    from test_legality_evidence import NONEMPTY
    from test_contract import NOW
    from c1_rail.qualification.execution.store import ExecutionStore
    from c1_rail.qualification.execution.protocol import sha256
    service=importlib.import_module('c1_rail.qualification.execution.service')
    case=build_bundle(tmp_path/'staging',idle=True,geometry_bytes=NONEMPTY)
    root=tmp_path/'service'; (root/'bundles').mkdir(parents=True)
    bundle_sha=sha256(case['index'])
    case['root'].rename(root/'bundles'/bundle_sha)
    instance=object.__new__(service.ExecutionService)
    instance.root=root; instance.release=case['release']; instance.authority='TEST_ONLY'
    instance.roles={1001:'client'}; instance.dispatch_lock=threading.Lock()
    instance.store=ExecutionStore(root/'journal.sqlite')
    scheduled=[]
    instance.executor=SimpleNamespace(submit=lambda *args:scheduled.append(args))
    monkeypatch.setattr(instance,'keys',lambda:case['keys'])
    monkeypatch.setattr(service,'now',lambda:NOW)
    with pytest.raises(ValueError,match='LEGALITY_REGISTRY_NOT_EMPTY'):
        instance.handle_request(1001,encoded(dict(operation='SUBMIT_N1',attempt_id=case['attempt_id'],bundle_sha256=bundle_sha)))
    assert scheduled==[] and instance.store.execution_rows()==[]
