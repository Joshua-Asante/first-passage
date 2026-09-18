"""Service-internal persistence tests; these confer no execution authority."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import importlib
import json
from pathlib import Path
import sqlite3
from threading import Event

import pytest
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.files import archive_bytes
from c1_rail.qualification.execution.protocol import sha256

NOW = datetime(2026, 9, 17, 12, tzinfo=timezone.utc)


def store_at(path):
    return importlib.import_module('c1_rail.qualification.execution.store').ExecutionStore(path)


def inputs():
    plan = json.loads((Path(__file__).parent / 'fixtures/n1_plan.json').read_bytes())
    plan['budget'].update(maximum_cpu_seconds=60, maximum_memory_bytes=1000000000)
    plan['contract_sha256'] = sha256(contract_bytes())
    plan['policy_sha256'] = '9' * 64
    return encoded({'operation': 'SUBMIT_N1', 'attempt_id': 'vector-attempt', 'bundle_sha256': 'b' * 64}), encoded(plan)


def contract_bytes():
    return encoded(dict(replay=dict(stages=[dict(name='N1', max_failures_per_population=0)])))


def reserved(tmp_path):
    store = store_at(tmp_path / 'journal.sqlite')
    request, plan = inputs()
    record = store.reserve(request, plan, now=NOW)
    store.archive_object(record.execution_id, 'context_contract', contract_bytes())
    return store, record, plan


def captured(tmp_path):
    store, record, plan = reserved(tmp_path)
    record = store.record_container(record.execution_id, 'c' * 64, expected_revision=record.revision)
    record = store.record_start_intent(record.execution_id, expected_revision=record.revision, now=NOW)
    record = store.record_running(record.execution_id, expected_revision=record.revision, now=NOW)
    raw = b'{"unit_capture":true}'
    archive = tmp_path / 'objects'
    for value in (plan, raw):
        archive_bytes(archive, value)
    facts = dict(schema='qualification_capture/v1', container_id='c' * 64,
        service_id='test-service', profile_sha256='d' * 64, runtime_manifest_sha256='e' * 64,
        worker_image_digest='sha256:' + 'f' * 64,
        authorized_at_utc='2026-09-17T12:00:00Z', started_utc='2026-09-17T12:00:00Z',
        completed_utc='2026-09-17T12:00:01Z',
        artifacts=[dict(role=role, sha256=sha256(value), byte_length=len(value))
                   for role, value in (('plan', plan), ('worker_result', raw))],
        observations=dict(exit_code=0, oom_killed=False, supervisor_wall_ns=1000000000,
            worker_compute_wall_ns=100000000, worker_cpu_ns=50000000, worker_peak_memory_bytes=10000))
    record = store.record_capture(record.execution_id, encoded(facts), expected_revision=record.revision)
    payload = store.get_captured_payload(record.execution_id)
    # Publication validates exact stored payload custody. Cryptographic signing
    # and verification are separately exercised at the real service boundary.
    envelope = encoded(dict(schema='qualification_execution_attestation/v1', payload=json.loads(payload),
        signature=dict(algorithm='Ed25519', key_id='unit-test-key', value_b64='AA==')))
    return store, record, envelope


def test_snapshot_and_candidate_storage_leave_campaign_unchanged(tmp_path):
    store,record,attestation = captured(tmp_path)
    record = store.publish_attestation(record.execution_id,attestation,expected_revision=record.revision)
    before = store.snapshot_for_assessment(record.attempt_id)
    snapshot = json.loads(before)
    assert snapshot['policy_sha256'] == '9'*64
    assert snapshot['executions'][0]['attestation_sha256'] == sha256(attestation)
    stored = store.store_proposed_artifact(record.attempt_id,'attempt_journal',before)
    assert stored == sha256(before)
    assert store.snapshot_for_assessment(record.attempt_id) == before
    with pytest.raises(ValueError,match='published member'):
        store.fetch(record.attempt_id,stored)
    assert store.fetch_candidate(record.attempt_id,stored) == before
    reopened = store_at(tmp_path / 'journal.sqlite')
    assert reopened.snapshot_for_assessment(record.attempt_id) == before
    assert reopened.fetch_candidate(record.attempt_id,stored) == before


@pytest.mark.parametrize('role,raw', [('private-result',b'{}'),('attempt_journal',b'{}')])
def test_candidate_storage_rejects_unknown_role_or_unrelated_artifact(tmp_path,role,raw):
    store,record,attestation = captured(tmp_path)
    record = store.publish_attestation(record.execution_id,attestation,expected_revision=record.revision)
    with pytest.raises(ValueError): store.store_proposed_artifact(record.attempt_id,role,raw)


def test_snapshot_after_void_preserves_attestation_but_changes_validity(tmp_path):
    store,record,attestation = captured(tmp_path)
    store.publish_attestation(record.execution_id,attestation,expected_revision=record.revision)
    before = json.loads(store.snapshot_for_assessment(record.attempt_id))
    store.void(record.attempt_id,'cancelled',b'{"test_only_approval":true}',now=NOW)
    after = json.loads(store.snapshot_for_assessment(record.attempt_id))
    assert after['validity'] == 'VOID'
    assert after['campaign_revision'] == before['campaign_revision']+1
    assert after['executions'][0]['attestation_sha256'] == before['executions'][0]['attestation_sha256']


def test_simultaneous_exact_submits_share_one_durable_execution(tmp_path):
    path = tmp_path / 'journal.sqlite'
    store_at(path)
    request, plan = inputs()
    with ThreadPoolExecutor(max_workers=2) as pool:
        records = list(pool.map(lambda _: store_at(path).reserve(request, plan, now=NOW), range(2)))
    assert records[0] == records[1]
    assert json.loads(store_at(path).status('vector-attempt'))['launch_intent_count'] == 0


def test_same_attempt_with_changed_bundle_cannot_redraw(tmp_path):
    store, _, plan = reserved(tmp_path)
    request = json.loads(inputs()[0])
    request['bundle_sha256'] = 'c' * 64
    with pytest.raises(ValueError, match='conflict'):
        store.reserve(encoded(request), plan, now=NOW)


def test_start_intent_is_once_only_across_reopen(tmp_path):
    store, record, _ = reserved(tmp_path)
    record = store.record_container(record.execution_id, 'c' * 64, expected_revision=record.revision)
    record = store.record_start_intent(record.execution_id, expected_revision=record.revision, now=NOW)
    reopened = store_at(tmp_path / 'journal.sqlite')
    with pytest.raises(ValueError, match='transition|revision'):
        reopened.record_start_intent(record.execution_id, expected_revision=record.revision, now=NOW)
    reopened.record_abort(record.execution_id, 'uncertain start', uncertain=True)
    again = reopened.reserve(*inputs(), now=NOW)
    assert again.execution_id == record.execution_id
    assert again.state == 'IN_DOUBT'
    assert json.loads(reopened.status(record.attempt_id))['launch_intent_count'] == 1


def test_capture_event_has_no_attestation_hash_cycle_and_survives_reopen(tmp_path):
    store, record, envelope = captured(tmp_path)
    payload = json.loads(store.get_captured_payload(record.execution_id))
    assert payload['capture_revision'] == record.revision
    reopened = store_at(tmp_path / 'journal.sqlite')
    assert reopened.get_captured_payload(record.execution_id) == store.get_captured_payload(record.execution_id)
    published = reopened.publish_attestation(record.execution_id, envelope, expected_revision=record.revision)
    assert published.state == 'ATTESTED'
    assert store_at(tmp_path / 'journal.sqlite').fetch(record.attempt_id, sha256(envelope)) == envelope


def test_void_after_capture_prevents_publication(tmp_path):
    store, record, envelope = captured(tmp_path)
    store.void(record.attempt_id, 'unit invalidation', b'{"validated_by_service":true}', now=NOW)
    with pytest.raises(ValueError, match='VOID'):
        store.publish_attestation(record.execution_id, envelope, expected_revision=record.revision)
    assert json.loads(store.status(record.attempt_id))['validity'] == 'VOID'


class _ObservedConnection:
    def __init__(self, connection, attempted):
        self._connection = connection
        self._attempted = attempted

    def execute(self, statement, *arguments):
        if statement == 'BEGIN IMMEDIATE':
            self._attempted.set()
        return self._connection.execute(statement, *arguments)

    def __getattr__(self, name):
        return getattr(self._connection, name)


@pytest.mark.parametrize('first', ['void', 'publication'])
def test_void_and_attestation_publication_serialize_in_both_orders(tmp_path, first):
    store, record, envelope = captured(tmp_path)
    second = store_at(tmp_path / 'journal.sqlite')
    attempted = Event()
    original_connect = second._connect
    second._connect = lambda: _ObservedConnection(original_connect(), attempted)

    def publish(target):
        return target.publish_attestation(
            record.execution_id, envelope, expected_revision=record.revision)

    with ThreadPoolExecutor(max_workers=1) as pool:
        with store.transaction():
            if first == 'void':
                store.void(record.attempt_id, 'unit invalidation', b'{"validated":true}', now=NOW)
                operation = lambda: publish(second)
            else:
                publish(store)
                operation = lambda: second.void(
                    record.attempt_id, 'unit invalidation', b'{"validated":true}', now=NOW)
            future = pool.submit(operation)
            assert attempted.wait(2), 'second writer never attempted BEGIN IMMEDIATE'
        if first == 'void':
            with pytest.raises(ValueError, match='VOID'):
                future.result(timeout=2)
        else:
            assert json.loads(future.result(timeout=2))['validity'] == 'VOID'
    status = json.loads(store_at(tmp_path / 'journal.sqlite').status(record.attempt_id))
    assert status['validity'] == 'VOID'
    assert status['attestation_count'] == (first == 'publication')
    assert status['launch_intent_count'] == 1


def test_concurrent_publication_has_only_one_completion_event(tmp_path):
    store, record, envelope = captured(tmp_path)
    def publish(_):
        try:
            return store_at(tmp_path / 'journal.sqlite').publish_attestation(
                record.execution_id, envelope, expected_revision=record.revision).state
        except ValueError:
            return 'CONFLICT'
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(publish, range(2)))
    assert 'ATTESTED' in results
    assert json.loads(store.status(record.attempt_id))['attestation_count'] == 1


def test_caller_cannot_replace_captured_payload_at_publication(tmp_path):
    store, record, envelope = captured(tmp_path)
    changed = json.loads(envelope)
    changed['payload']['plan_sha256'] = 'f' * 64
    with pytest.raises(ValueError, match='payload'):
        store.publish_attestation(record.execution_id, encoded(changed), expected_revision=record.revision)


@pytest.mark.parametrize('sql', [
    "UPDATE executions SET state='ATTESTED'",
    "UPDATE campaigns SET event_head='bad'",
    "DELETE FROM execution_objects WHERE role='worker_result'",
    "UPDATE executions SET captured_payload=CAST(replace(CAST(captured_payload AS TEXT),'COMPLETED','FORGED') AS BLOB)",
    "UPDATE campaigns SET validity='VOID'",
    "UPDATE executions SET container_id='wrong-container'",
])
def test_reopen_detects_corrupted_transition_chain_or_membership(tmp_path, sql):
    captured(tmp_path)
    with sqlite3.connect(tmp_path / 'journal.sqlite') as connection:
        connection.execute(sql)
    with pytest.raises(ValueError, match='integrity'):
        store_at(tmp_path / 'journal.sqlite')


def test_v3_database_is_never_migrated_in_place(tmp_path):
    path = tmp_path / 'legacy.sqlite'
    with sqlite3.connect(path) as connection:
        connection.execute('PRAGMA user_version=3')
    with pytest.raises(ValueError, match='migration|schema'):
        store_at(path)


@pytest.mark.parametrize('damage',["DROP TABLE proposed_artifacts", "ALTER TABLE campaigns DROP COLUMN policy_sha256"])
def test_incomplete_schema_four_is_rejected_even_without_campaigns(tmp_path,damage):
    path = tmp_path/'journal.sqlite'
    store_at(path)
    with sqlite3.connect(path) as connection:
        connection.execute(damage)
    with pytest.raises(ValueError,match='schema'):
        store_at(path)


@pytest.mark.parametrize('outputs',[None,1,{},[None],[{}],[{'role':[]}],[{'role':'n1_result','sha256':False,'byte_length':1,'privacy':'PRIVATE'}]])
def test_malformed_proposal_inventory_is_a_bounded_rejection(tmp_path,outputs):
    store,record,attestation=captured(tmp_path)
    store.publish_attestation(record.execution_id,attestation,expected_revision=record.revision)
    raw=encoded(dict(schema='qualification_result_envelope/v2',attempt_id=record.attempt_id,outputs=outputs))
    with pytest.raises(ValueError): store.store_proposed_result(record.attempt_id,raw)
