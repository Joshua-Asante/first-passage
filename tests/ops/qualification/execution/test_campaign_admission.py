"""Dormant admission tests exercise signed bundles, real journal and service."""
import base64
import json
import threading
from dataclasses import replace
from datetime import timedelta
from types import SimpleNamespace

import pytest
from bundle_fixture import build_bundle
from test_contract import NOW
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import service
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.execution.store import ExecutionStore


def message(case, operation='SUBMIT_E1', **values):
    doc = dict(schema='qualification_campaign_request/v1', operation=operation,
               attempt_id=case['attempt_id'])
    if operation == 'SUBMIT_E1':
        doc.update(bundle_sha256=sha256(case['index']), request_id='request-1')
    doc.update(values)
    return encoded(doc)


def running(tmp_path, monkeypatch, **options):
    case = build_bundle(tmp_path / 'staged', capability='FULL_E1', **options)
    root = tmp_path / 'service'
    (root / 'bundles').mkdir(parents=True)
    case['root'].rename(root / 'bundles' / sha256(case['index']))
    instance = object.__new__(service.ExecutionService)
    instance.root = root
    instance.release = case['release']
    instance.authority = 'TEST_ONLY'
    from c1_rail.qualification.execution.profile import parse_profile
    instance.profile = parse_profile(encoded(json.loads(case['release'])['profile']))
    instance.roles = {1001: 'client', 1002: 'g5', 1003: 'operator'}
    instance.dispatch_lock = threading.Lock()
    instance.store = ExecutionStore(root / 'journal.sqlite')
    def forbidden(*args, **kwargs):
        raise AssertionError('admission must never launch work')
    instance.executor = SimpleNamespace(submit=forbidden)
    monkeypatch.setattr(instance, 'keys', lambda: case['keys'])
    monkeypatch.setattr(service, 'now', lambda: NOW)
    return instance, case


def test_durable_admission_retry_restart_and_no_dispatch(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    first = json.loads(instance.handle_request(1001, message(case)))
    assert first['validity'] == 'VALID' and first['current_policy_eligible'] is True
    receipt = first['receipt']
    assert receipt['state'] == 'ADMITTED' and receipt['dispatch_enabled'] is False
    assert receipt['plan_byte_length'] > 0 and len(encoded(first)) < 8192
    instance.store = ExecutionStore(instance.store.path)
    assert json.loads(instance.handle_request(1001, message(case))) == first
    assert json.loads(instance.handle_request(1001, message(case, 'STATUS'))) == first
    assert instance.store.execution_rows() == []
    changed = message(case, request_id='another-request')
    with pytest.raises(ValueError, match='conflict'):
        instance.handle_request(1001, changed)
    monkeypatch.setattr(service, 'now', lambda: NOW + timedelta(days=1000))
    expired = json.loads(instance.handle_request(1001, message(case)))
    assert expired['receipt'] == receipt and expired['current_policy_eligible'] is False


def test_new_admission_expired_rejected_without_state(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    monkeypatch.setattr(service, 'now', lambda: NOW + timedelta(days=1000))
    with pytest.raises(ValueError):
        instance.handle_request(1001, message(case))
    with pytest.raises(KeyError):
        instance.handle_request(1001, message(case, 'STATUS'))


def test_chunk_roundtrip_exact_membership_and_retries(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    receipt = json.loads(instance.handle_request(1001, message(case)))['receipt']
    request = message(case, 'FETCH_PLAN_CHUNK', object_sha256=receipt['plan_sha256'], offset=0, length=1048576)
    raw = instance.handle_request(1001, request)
    assert instance.handle_request(1001, request) == raw
    chunk = json.loads(raw)
    data = base64.b64decode(chunk['bytes_b64'])
    assert chunk['offset'] == 0 and chunk['byte_length'] == len(data)
    assert chunk['total_byte_length'] == receipt['plan_byte_length']
    assert sha256(data) == receipt['plan_sha256']
    for uid in (9999, 1002, 1003):
        with pytest.raises(ValueError, match='AUTHORIZED'):
            instance.handle_request(uid, request)
    with pytest.raises(ValueError, match='membership'):
        instance.handle_request(1001, message(case, 'FETCH_PLAN_CHUNK', object_sha256='f'*64, offset=0, length=1))


@pytest.mark.parametrize('field,value', [('offset', True), ('offset', -1), ('offset', 2**63),
    ('length', True), ('length', 0), ('length', -1), ('length', 1048577), ('length', 0.5)])
def test_chunk_rejects_invalid_ranges(field, value):
    from c1_rail.qualification.execution.campaign_protocol import parse_campaign_request
    params = dict(object_sha256='a'*64, offset=0, length=1)
    params[field] = value
    with pytest.raises(ValueError):
        parse_campaign_request(message({'attempt_id': 'test'}, 'FETCH_PLAN_CHUNK', **params))

@pytest.mark.parametrize('operation', ['START', 'SUBMIT_N1', 'COMMIT_E1_RESULT', 'SIGN', 'STORE_RESULT'])
def test_campaign_protocol_cannot_dispatch_or_publish(operation):
    from c1_rail.qualification.execution.campaign_protocol import parse_campaign_request
    with pytest.raises(ValueError):
        parse_campaign_request(message({'attempt_id': 'test'}, operation))

def test_campaign_unknown_field_rejected(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    with pytest.raises(ValueError):
        instance.handle_request(1001, message(case, seed_inputs=[]))


def test_legacy_submit_rejected_on_full_release(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    with pytest.raises(ValueError):
        instance.handle_request(1001, encoded(dict(operation='SUBMIT_N1', attempt_id=case['attempt_id'], bundle_sha256=sha256(case['index']))))
    assert instance.store.execution_rows() == []


def test_atomic_admission_failure_can_retry(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    from c1_rail.qualification.execution.campaign_store import CampaignStore
    original = CampaignStore.admit
    def interrupted(self, *args, **kwargs):
        original(self, *args, **kwargs)
        raise OSError('injected before outer commit')
    with monkeypatch.context() as patch:
        patch.setattr(CampaignStore, 'admit', interrupted)
        with pytest.raises(OSError): instance.handle_request(1001, message(case))
    instance.store = ExecutionStore(instance.store.path)
    with pytest.raises(KeyError): instance.handle_request(1001, message(case, 'STATUS'))
    assert json.loads(instance.handle_request(1001, message(case)))['validity'] == 'VALID'


def test_void_is_authorized_durable_and_exact_retry(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    first = json.loads(instance.handle_request(1001, message(case)))
    from composition_fixture import signed_approval
    subject = encoded(dict(attempt_id=case['attempt_id'], reason='stop', contract_sha256=case['contract'].contract_sha256))
    approval = signed_approval(subject, case['private']['test-freeze'], key_id='test-freeze', scope='VOID_QUALIFICATION_ATTEMPT', contract_sha256=case['contract'].contract_sha256)
    request = message(case, 'VOID', reason='stop', operator_approval_bytes=base64.b64encode(approval).decode('ascii'))
    with pytest.raises(ValueError, match='AUTHORIZED'): instance.handle_request(1001, request)
    result = instance.handle_request(1003, request)
    instance.store = ExecutionStore(instance.store.path)
    assert instance.handle_request(1003, request) == result
    retry = json.loads(instance.handle_request(1001, message(case)))
    assert retry['receipt'] == first['receipt'] and retry['validity'] == 'VOID'
    assert retry['current_policy_eligible'] is False
    chunk = message(case, 'FETCH_PLAN_CHUNK', object_sha256=first['receipt']['plan_sha256'], offset=0, length=1)
    assert json.loads(instance.handle_request(1001, chunk))['byte_length'] == 1


@pytest.mark.parametrize('value', [[], {}, True, None, 1])
def test_malformed_operation_and_nonobject_release_rejected(value):
    from c1_rail.qualification.execution.campaign_protocol import parse_campaign_request
    from c1_rail.qualification.execution.profile import parse_profile
    from c1_rail.qualification.execution.release_schema import parse_release
    with pytest.raises(ValueError):
        parse_campaign_request(message({'attempt_id': 'test'}, value))
    if type(value) is not dict:
        for parser in (parse_profile, parse_release):
            with pytest.raises(ValueError): parser(encoded(value))


def test_client_reconstructs_only_verified_ordered_chunks(monkeypatch):
    from c1_rail.qualification.execution import client
    body = b'x' * (1048576 + 11)
    receipt = dict(attempt_id='test', plan_sha256=sha256(body), plan_byte_length=len(body), profile_sha256='a'*64)
    monkeypatch.setattr(client, '_configuration', lambda path: ({}, SimpleNamespace(input_byte_limit=67108864, sha256='a'*64)), raising=False)
    def transport(path, operation, fields):
        if operation == 'STATUS': return encoded(dict(receipt=receipt))
        start = fields['offset']; part = body[start:start+fields['length']]
        return encoded(dict(schema='qualification_campaign_plan_chunk/v1', attempt_id='test', object_sha256=sha256(body),
            offset=start, total_byte_length=len(body), byte_length=len(part), bytes_b64=base64.b64encode(part).decode('ascii')))
    monkeypatch.setattr(client, 'request', transport)
    assert client.fetch_campaign_plan('unused', attempt_id='test') == body
    for field, value in [('offset', 1), ('object_sha256', 'f'*64), ('byte_length', 2), ('total_byte_length', 1), ('bytes_b64', 'eA==')]:
        def corrupt(path, operation, fields):
            doc = json.loads(transport(path, operation, fields))
            if operation != 'STATUS': doc[field] = value
            return encoded(doc)
        monkeypatch.setattr(client, 'request', corrupt)
        with pytest.raises(ValueError): client.fetch_campaign_plan('unused', attempt_id='test')
    # Coherent length and chunk metadata do not replace the final digest check.
    def corrupt_digest(path, operation, fields):
        doc = json.loads(transport(path, operation, fields))
        if operation != 'STATUS':
            part = base64.b64decode(doc['bytes_b64'])
            doc['bytes_b64'] = base64.b64encode(b'y' + part[1:]).decode('ascii')
        return encoded(doc)
    monkeypatch.setattr(client, 'request', corrupt_digest)
    with pytest.raises(ValueError): client.fetch_campaign_plan('unused', attempt_id='test')


def test_reference_plan_chunk_transport_and_retained_history(tmp_path, monkeypatch):
    from bundle_fixture import build_bundle
    small = build_bundle(tmp_path/'policy')
    workload = small['contract'].trust_domain.workload_policy
    counts = {stage: dict(pops) for stage, pops in workload.stage_population_depths.items()}
    counts.update(N1={pop: (200,) for pop in ('FULL', 'H1', 'H2')}, N2={'FULL': (970,)},
                  PART_B={pop: (970,) for pop in ('H1', 'H2')}, PART_A={'REGIME': (100, 200)})
    workload = replace(workload, stage_population_depths=counts, part_a_initial_panels=100,
                       part_a_expanded_panels=200, part_a_paths_per_population_per_panel=200)
    instance, case = running(tmp_path/'large', monkeypatch, workload=workload)
    receipt = json.loads(instance.handle_request(1001, message(case)))['receipt']
    assert receipt['plan_byte_length'] > instance.profile.rpc_byte_limit
    assembled = bytearray()
    while len(assembled) < receipt['plan_byte_length']:
        raw = instance.handle_request(1001, message(case, 'FETCH_PLAN_CHUNK',
            object_sha256=receipt['plan_sha256'], offset=len(assembled), length=1048576))
        assert len(encoded(dict(ok=True, data_b64=base64.b64encode(raw).decode('ascii')))) < instance.profile.rpc_byte_limit
        chunk = json.loads(raw)
        assert chunk['offset'] == len(assembled) and chunk['byte_length'] <= 1048576
        assembled.extend(base64.b64decode(chunk['bytes_b64']))
    assert len(assembled) == receipt['plan_byte_length'] and sha256(bytes(assembled)) == receipt['plan_sha256']
    with pytest.raises(ValueError):
        instance.handle_request(1001, message(case, 'FETCH_PLAN_CHUNK', object_sha256=receipt['plan_sha256'], offset=len(assembled), length=1))
    # Custody is durable in the journal, not dependent on staged paths.
    import shutil
    shutil.rmtree(instance.root/'bundles')
    instance.store = ExecutionStore(instance.store.path)
    assert json.loads(instance.handle_request(1001, message(case)))['receipt'] == receipt
    assert json.loads(instance.handle_request(1001, message(case)))['current_policy_eligible'] is True


def test_commit_refresh_rejects_expiry_during_planning(tmp_path, monkeypatch):
    instance, case = running(tmp_path, monkeypatch)
    instants = iter([NOW, NOW + timedelta(days=1000)])
    monkeypatch.setattr(service, 'now', lambda: next(instants))
    with pytest.raises(ValueError): instance.handle_request(1001, message(case))
    with pytest.raises(KeyError): instance.handle_request(1001, message(case, 'STATUS'))


def test_concurrent_duplicate_and_void_do_not_remint(tmp_path, monkeypatch):
    from concurrent.futures import ThreadPoolExecutor
    instance, case = running(tmp_path, monkeypatch)
    with ThreadPoolExecutor(max_workers=2) as pool:
        replies = list(pool.map(lambda _: instance.handle_request(1001, message(case)), range(2)))
    assert replies[0] == replies[1]
    receipt = json.loads(replies[0])['receipt']
    from composition_fixture import signed_approval
    subject = encoded(dict(attempt_id=case['attempt_id'], reason='stop', contract_sha256=case['contract'].contract_sha256))
    approval = signed_approval(subject, case['private']['test-freeze'], key_id='test-freeze', scope='VOID_QUALIFICATION_ATTEMPT', contract_sha256=case['contract'].contract_sha256)
    void = message(case, 'VOID', reason='stop', operator_approval_bytes=base64.b64encode(approval).decode('ascii'))
    with ThreadPoolExecutor(max_workers=2) as pool:
        duplicate = pool.submit(instance.handle_request, 1001, message(case))
        cancel = pool.submit(instance.handle_request, 1003, void)
        assert json.loads(duplicate.result())['receipt'] == receipt
        assert json.loads(cancel.result())['validity'] == 'VOID'
    status = json.loads(instance.handle_request(1001, message(case)))
    assert status['validity'] == 'VOID' and status['receipt'] == receipt


def test_exact_v4_migration_preserves_n1_and_rolls_back_failure(tmp_path, monkeypatch):
    import sqlite3
    from test_store import reserved
    from c1_rail.qualification.execution import store as store_module
    original, record, _ = reserved(tmp_path)
    expected = original.status(record.attempt_id)
    with sqlite3.connect(original.path) as connection:
        connection.execute('DROP TABLE full_campaign_objects')
        connection.execute('DROP TABLE full_campaigns')
        connection.execute('PRAGMA user_version=4')
    with monkeypatch.context() as patch:
        patch.setattr(store_module, 'CAMPAIGN_SCHEMA', store_module.CAMPAIGN_SCHEMA + ' invalid migration;')
        with pytest.raises(sqlite3.OperationalError): ExecutionStore(original.path)
    with sqlite3.connect(original.path) as connection:
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 4
        assert connection.execute("SELECT 1 FROM sqlite_master WHERE name='full_campaigns'").fetchone() is None
    reopened = ExecutionStore(original.path)
    assert reopened.status(record.attempt_id) == expected
    with sqlite3.connect(original.path) as connection:
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 5
    assert ExecutionStore(original.path).status(record.attempt_id) == expected


def test_cross_capability_attempt_collisions_both_directions(tmp_path, monkeypatch):
    from test_store import inputs
    instance, case = running(tmp_path, monkeypatch, attempt_id='vector-attempt')
    request, plan = inputs()
    instance.store.reserve(request, plan, now=NOW)
    with pytest.raises(ValueError, match='promote'):
        instance.handle_request(1001, message(case))
    other, other_case = running(tmp_path/'other', monkeypatch, attempt_id='vector-attempt')
    other.handle_request(1001, message(other_case))
    with pytest.raises(ValueError, match='FULL_E1'):
        other.store.reserve(request, plan, now=NOW)


@pytest.mark.parametrize('damage', ['layout', 'object', 'validity'])
def test_campaign_restart_rejects_corrupted_projection(tmp_path, monkeypatch, damage):
    import sqlite3
    instance, case = running(tmp_path, monkeypatch)
    instance.handle_request(1001, message(case))
    with sqlite3.connect(instance.store.path) as connection:
        if damage == 'layout': connection.execute('ALTER TABLE full_campaigns ADD COLUMN unapproved TEXT')
        elif damage == 'object': connection.execute("UPDATE full_campaign_objects SET body=x'7b7d' WHERE role='plan'")
        else: connection.execute("UPDATE full_campaigns SET validity='VOID'")
    with pytest.raises((ValueError, TypeError, KeyError)):
        ExecutionStore(instance.store.path)


def test_chunk_offset_cannot_overflow_sqlite_one_based_index():
    from c1_rail.qualification.execution.campaign_protocol import parse_campaign_request
    with pytest.raises(ValueError):
        parse_campaign_request(message({'attempt_id': 'test'}, 'FETCH_PLAN_CHUNK',
            object_sha256='a'*64, offset=2**63-1, length=1))
