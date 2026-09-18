"""Unit consistency traces, not OS interruption or execution-attestation proof.

The reference imports no production guards. The adapter applies inputs to the
real store; it never supplies the reference's predicted state to that store.
"""
import base64
import hashlib
import json
import random

import pytest

from lifecycle_model import LifecycleModel
from test_store import NOW, contract_bytes, inputs, store_at
from test_atomic_assessment import assessed_inputs, captured_case
from c1_rail.qualification.execution.files import archive_bytes
from c1_rail.qualification.execution.store import ExecutionStore


def raw(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


class StoreTrace:
    def __init__(self, path):
        self.store = store_at(path)
        self.request, self.plan = inputs()
        self.attempt = 'vector-attempt'
        self.execution_id = None
        self.worker = b'{"unit_capture":true}'
        self.facts = dict(schema='qualification_capture/v1', container_id='c' * 64,
            service_id='test-service', profile_sha256='d' * 64, runtime_manifest_sha256='e' * 64,
            worker_image_digest='sha256:' + 'f' * 64,
            authorized_at_utc='2026-09-17T12:00:00Z', started_utc='2026-09-17T12:00:00Z',
            completed_utc='2026-09-17T12:00:01Z',
            artifacts=[dict(role=role, sha256=digest(value), byte_length=len(value))
                       for role, value in (('plan', self.plan), ('worker_result', self.worker))],
            observations=dict(exit_code=0, oom_killed=False, supervisor_wall_ns=1000000000,
                worker_compute_wall_ns=100000000, worker_cpu_ns=50000000, worker_peak_memory_bytes=10000))
        self.attestation = None
        self.capture_bytes = None
        self.model = LifecycleModel()

    def step(self, action):
        identity = None
        if action == 'submit': identity = (self.request, self.plan)
        if action == 'conflicting_submit': identity = (self.request + b'changed', self.plan)
        if action == 'capture': identity = digest(raw(self.facts))
        if action == 'publish':
            if self.capture_bytes is not None:
                self.attestation = raw(dict(schema='qualification_execution_attestation/v1',
                    payload=json.loads(self.capture_bytes),
                    signature=dict(algorithm='Ed25519', key_id='unit-test-key', value_b64='AA==')))
            identity = digest(self.attestation) if self.attestation else 'unavailable'
        predicted = self.model.apply(action, identity=identity)
        before = self.store.snapshot_for_assessment(self.attempt) if self.execution_id else None
        try:
            response = self._apply(action)
        except ValueError as exc:
            observed = 'CONFLICT' if 'conflict' in str(exc) else 'REJECTED'
            assert predicted == observed, (action, predicted, str(exc))
            assert self.store.snapshot_for_assessment(self.attempt) == before
        else:
            assert predicted in ('ACCEPTED', 'RETRY'), (action, predicted)
            if action in ('submit', 'conflicting_submit'):
                if self.execution_id is None:
                    self.execution_id = response.execution_id
                assert response.execution_id == self.execution_id
                assert response.state == self.model.state
            if predicted == 'RETRY':
                assert self.store.snapshot_for_assessment(self.attempt) == before
        self.assert_state()

    def _apply(self, action):
        if action == 'reopen':
            self.store = store_at(self.store.path)
            return None
        if action in ('submit', 'conflicting_submit'):
            request = json.loads(self.request)
            if action == 'conflicting_submit': request['bundle_sha256'] = 'a' * 64
            result = self.store.reserve(raw(request), self.plan, now=NOW)
            self.store.archive_object(result.execution_id, 'context_contract', contract_bytes())
            return result
        status = json.loads(self.store.status(self.attempt))
        revision = status['revision']
        if action == 'container':
            return self.store.record_container(self.execution_id, 'c' * 64, expected_revision=revision)
        if action == 'intent':
            return self.store.record_start_intent(self.execution_id, expected_revision=revision, now=NOW)
        if action == 'running':
            return self.store.record_running(self.execution_id, expected_revision=revision, now=NOW)
        if action == 'capture':
            archive_bytes(self.store.archive_dir, self.worker)
            response = self.store.record_capture(self.execution_id, raw(self.facts), expected_revision=revision)
            self.capture_bytes = self.store.get_captured_payload(self.execution_id)
            return response
        if action == 'publish':
            envelope = self.attestation or raw(dict(schema='qualification_execution_attestation/v1', payload={}, signature={}))
            return self.store.publish_attestation(self.execution_id, envelope, expected_revision=revision)
        if action == 'void':
            return json.loads(self.store.void(self.attempt, 'unit cancellation', b'{"unit_approval":true}', now=NOW))
        if action in ('uncertain', 'abort'):
            # This is the recovery disposition input, not a simulated OS restart.
            return self.store.record_abort(self.execution_id, 'unit interruption', uncertain=action == 'uncertain')
        raise AssertionError('unknown adapter action ' + action)

    def assert_state(self):
        status = json.loads(self.store.status(self.attempt))
        snapshot = json.loads(self.store.snapshot_for_assessment(self.attempt))
        assert status['state'] == self.model.state
        assert status['validity'] == self.model.validity
        assert status['launch_intent_count'] == self.model.launch_intents
        assert status['attestation_count'] == int(self.model.attestation is not None)
        assert status['attestation_sha256'] == self.model.attestation
        assert status['revision'] == snapshot['campaign_revision'] == self.model.events
        assert ('result_sha256' in status) is (self.model.result_authentication is not None)
        if self.model.captured_identity is not None:
            payload = json.loads(self.store.get_captured_payload(self.execution_id))
            retained = {key: payload[key] for key in self.facts if key not in ('schema', 'container_id')}
            retained.update(schema='qualification_capture/v1', container_id=status['container_id'])
            assert digest(raw(retained)) == self.model.captured_identity
            assert self.store.get_captured_payload(self.execution_id) == self.capture_bytes
        else:
            with pytest.raises(ValueError, match='no durable capture'):
                self.store.get_captured_payload(self.execution_id)
        assert self.store.retry_assessment(self.attempt, '0' * 64, b'no authentication') is None
        # Every observation also exercises persisted integrity on another store instance.
        assert store_at(self.store.path).status(self.attempt) == self.store.status(self.attempt)


@pytest.mark.parametrize('trace', [
    ('submit', 'submit', 'conflicting_submit', 'uncertain', 'reopen', 'submit', 'container', 'intent'),
    ('submit', 'container', 'uncertain', 'reopen', 'submit', 'intent', 'running'),
    ('submit', 'container', 'intent', 'uncertain', 'reopen', 'submit', 'intent', 'running'),
    ('submit', 'container', 'intent', 'running', 'uncertain', 'reopen', 'capture', 'publish'),
    ('submit', 'container', 'intent', 'running', 'capture', 'reopen', 'void', 'publish', 'reopen'),
    ('submit', 'container', 'intent', 'running', 'capture', 'publish', 'void', 'reopen', 'submit', 'publish'),
    ('submit', 'container', 'container', 'intent', 'intent', 'running', 'capture', 'capture', 'publish', 'publish'),
    ('submit', 'void', 'uncertain', 'reopen', 'submit', 'intent', 'void'),
    ('submit', 'container', 'abort', 'reopen', 'submit', 'intent', 'running'),
])
def test_deterministic_store_traces_preserve_independent_lifecycle(trace, tmp_path):
    driver = StoreTrace(tmp_path / 'journal.sqlite')
    for action in trace:
        driver.step(action)


@pytest.mark.parametrize('seed', [2, 7, 19, 37, 61, 101])
def test_seeded_store_sequences_preserve_event_counts_and_no_redraw(seed, tmp_path):
    rng = random.Random(seed)
    driver = StoreTrace(tmp_path / 'journal.sqlite')
    driver.step('submit')
    progression = ['container', 'intent', 'running', 'capture', 'publish']
    for action in progression:
        for _ in range(rng.randrange(1, 4)):
            driver.step(rng.choice(['submit', 'conflicting_submit', 'reopen', 'publish']))
        driver.step(action)
    for _ in range(20):
        driver.step(rng.choice(['submit', 'conflicting_submit', 'reopen', 'void', 'capture', 'publish', 'intent', 'uncertain']))


def attested_model(captured_identity, attestation):
    model = LifecycleModel()
    for action, identity in [('submit', 'original-request'), ('container', None), ('intent', None),
                             ('running', None), ('capture', captured_identity), ('publish', attestation)]:
        assert model.apply(action, identity=identity) == 'ACCEPTED'
    assert model.events == 6  # Hand-counted dispatch/container/intent/run/capture/publication.
    return model


@pytest.mark.parametrize('trace', [
    ('commit', 'reopen', 'commit', 'void', 'commit', 'changed_auth', 'reopen', 'commit'),
    ('void', 'commit', 'reopen', 'commit'),
    ('commit', 'changed_auth', 'void', 'changed_auth', 'commit'),
])
def test_commit_and_void_traces_preserve_original_identity(assessed_inputs, trace):
    store, attempt, evidence, authentication = assessed_inputs
    initial = json.loads(store.status(attempt))
    model = attested_model('fixture-capture', initial['attestation_sha256'])
    first_receipt = None
    for action in trace:
        supplied = authentication
        if action == 'changed_auth':
            document = json.loads(authentication)
            document['signature']['value_b64'] = base64.b64encode(b'x' * 64).decode()
            supplied = raw(document)
        identity = (digest(evidence.result_bytes), digest(supplied))
        expected = model.apply('commit' if action == 'changed_auth' else action, identity=identity)
        before = store.snapshot_for_assessment(attempt)
        try:
            if action == 'reopen': store = ExecutionStore(store.path)
            elif action == 'void': store.void(attempt, 'unit cancellation', b'{"unit_approval":true}', now=NOW)
            else:
                response = json.loads(store.commit_assessment(evidence, supplied, now=NOW))
                assert response['validity'] == model.validity
                assert response['historical'] is (expected == 'RETRY')
                if first_receipt is None: first_receipt = response['receipt']
                assert response['receipt'] == first_receipt
        except ValueError as exc:
            actual = 'CONFLICT' if 'conflict' in str(exc) else 'REJECTED'
            assert expected == actual, (action, expected, str(exc))
        else:
            assert expected in ('ACCEPTED', 'RETRY')
        if expected in ('REJECTED', 'CONFLICT', 'RETRY') or action == 'reopen':
            assert store.snapshot_for_assessment(attempt) == before
        status = json.loads(store.status(attempt))
        assert status['revision'] == model.events
        assert status['validity'] == model.validity
        assert status['state'] == model.state
        assert status['launch_intent_count'] == model.launch_intents == 1
        assert status['attestation_sha256'] == model.attestation
        assert ('result_sha256' in status) is (model.result_authentication is not None)
        if model.result_authentication:
            assert (status['result_sha256'], status['authentication_sha256']) == model.result_authentication
            assert store.fetch(attempt, status['authentication_sha256']) == authentication
        assert ExecutionStore(store.path).status(attempt) == store.status(attempt)
