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
