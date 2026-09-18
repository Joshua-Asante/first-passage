"""Real competing SQLite writers, SIGKILL checkpoints and immutable retries."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import subprocess
import time

import pytest


def test_simultaneous_submissions_contend_before_single_reservation(real_boundary):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True)
    directory = boundary.checkpoints(observe=['SUBMIT_N1.locked', 'SUBMIT_ENTERED.2'],
                                     pause=['SUBMIT_N1.locked'])
    try:
        with ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(boundary.submit, bundle)
            held = boundary.checkpoint(directory, 'SUBMIT_N1.locked')
            second = pool.submit(boundary.submit, bundle)
            try:
                competing = boundary.checkpoint(directory, 'SUBMIT_ENTERED.2')
                assert competing['thread'] != held['thread']
                assert competing['monotonic_ns'] > held['monotonic_ns']
            finally:
                boundary.release_checkpoint(directory, 'SUBMIT_N1.locked')
            assert first.result(timeout=60)['execution_id'] == second.result(timeout=60)['execution_id']
        state = boundary.wait(bundle['attempt_id'])
        before = boundary.events(bundle['attempt_id'])
        with pytest.raises(subprocess.CalledProcessError):
            boundary.submit(dict(bundle, bundle_sha256='f' * 64))
        assert boundary.events(bundle['attempt_id']) == before
        assert state['launch_intent_count'] == 1 and state['attestation_count'] == 1
        assert len(boundary.starts(state['container_id'])) == 1
        assert sum(row['kind'] == 'DISPATCHED' for row in before) == 1
    finally:
        boundary.release_checkpoint(directory, 'SUBMIT_N1.locked')
        boundary.restart()


def test_death_after_reservation_before_scheduling_never_launches_on_retry(real_boundary):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True)
    directory = boundary.checkpoints(observe=['SUBMIT_N1.committed'], pause=['SUBMIT_N1.committed'])
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            response = pool.submit(boundary.submit, bundle)
            boundary.checkpoint(directory, 'SUBMIT_N1.committed')
            reserved = boundary.status(bundle['attempt_id'])
            assert reserved['state'] == 'DISPATCHED' and reserved['container_id'] is None
            boundary.service.kill()
            boundary.service.wait(timeout=15)
            with pytest.raises(subprocess.CalledProcessError):
                response.result(timeout=30)
        boundary.restart()
        state = boundary.wait(bundle['attempt_id'], states=('IN_DOUBT',))
        before = boundary.events(bundle['attempt_id'])
        assert state['execution_id'] == reserved['execution_id']
        assert state['launch_intent_count'] == state['attestation_count'] == 0
        assert state['container_id'] is None
        assert boundary.submit(bundle)['execution_id'] == state['execution_id']
        boundary.restart()
        assert boundary.events(bundle['attempt_id']) == before
    finally:
        boundary.release_checkpoint(directory, 'SUBMIT_N1.committed')
        boundary.restart()


def test_death_during_partial_output_cannot_publish_or_redraw(real_boundary):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True, fault='partial_output')
    boundary.submit(bundle)
    running = boundary.wait(bundle['attempt_id'], states=('RUNNING',))
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        try:
            log = boundary.worker_log(running['execution_id'])
        except FileNotFoundError:
            log = b''
        if b'TEST_ONLY partial frame emitted\n' in log:
            break
        time.sleep(.05)
    else:
        pytest.fail('partial-output callback did not execute')
    boundary.service.kill()
    boundary.service.wait(timeout=15)
    boundary.restart()
    state = boundary.wait(bundle['attempt_id'], states=('IN_DOUBT',))
    assert state['execution_id'] == running['execution_id']
    assert state['attestation_count'] == 0 and state['launch_intent_count'] == 1
    assert boundary.inspect(state['container_id'])['State']['Running'] is False
    events = boundary.events(bundle['attempt_id'])
    assert boundary.submit(bundle)['execution_id'] == state['execution_id']
    assert boundary.events(bundle['attempt_id']) == events
    assert len(boundary.starts(state['container_id'])) == 1
    with pytest.raises(subprocess.CalledProcessError):
        boundary.assess(bundle['attempt_id'])


@pytest.mark.parametrize('operation', ['PUBLISH', 'COMMIT'])
@pytest.mark.parametrize('first', ['VOID', 'ACCEPT'])
def test_void_and_acceptance_have_both_real_writer_orders(real_boundary, operation, first):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True)
    attempt = bundle['attempt_id']
    winner = 'VOID' if first == 'VOID' else operation
    observe = [operation + suffix for suffix in ('.before', '.attempt', '.locked', '.committed')]
    observe += ['VOID.locked', 'VOID_STATUS.attempt', 'PUBLISH.finished']
    directory = boundary.checkpoints(observe=observe, pause=[operation + '.before', winner + '.locked'])
    try:
        boundary.submit(bundle)
        with ThreadPoolExecutor(max_workers=2) as pool:
            assessment = None
            if operation == 'COMMIT':
                boundary.wait(attempt)
                assessment = pool.submit(boundary.assess, attempt)
            boundary.checkpoint(directory, operation + '.before')
            if first == 'VOID':
                cancellation = pool.submit(boundary.void, bundle)
                held = boundary.checkpoint(directory, 'VOID.locked')
                boundary.release_checkpoint(directory, operation + '.before')
                waiting = boundary.checkpoint(directory, operation + '.attempt')
                assert not (directory / (operation + '.locked.json')).exists()
            else:
                boundary.release_checkpoint(directory, operation + '.before')
                held = boundary.checkpoint(directory, operation + '.locked')
                cancellation = pool.submit(boundary.void, bundle)
                waiting = boundary.checkpoint(directory, 'VOID_STATUS.attempt')
                assert not (directory / 'VOID.locked.json').exists()
            assert waiting['monotonic_ns'] > held['monotonic_ns']
            assert waiting['thread'] != held['thread']
            boundary.release_checkpoint(directory, winner + '.locked')
            assert cancellation.result(timeout=60)['validity'] == 'VOID'
            if assessment is not None:
                if first == 'VOID':
                    with pytest.raises(subprocess.CalledProcessError):
                        assessment.result(timeout=60)
                else:
                    receipt = assessment.result(timeout=60)['receipt']
            else:
                boundary.checkpoint(directory, 'PUBLISH.finished')
        boundary.restart()
        state = boundary.status(attempt)
        events = boundary.events(attempt)
        assert state['validity'] == 'VOID' and state['launch_intent_count'] == 1
        assert len(boundary.starts(state['container_id'])) == 1
        kinds = [row['kind'] for row in events]
        assert kinds.count('DISPATCHED') == kinds.count('START_INTENT') == kinds.count('CAPTURED') == 1
        if operation == 'PUBLISH':
            assert state['attestation_count'] == int(first == 'ACCEPT')
            assert 'result_sha256' not in state
            if first == 'ACCEPT':
                assert kinds.index('ATTESTED') < kinds.index('VOID')
            with pytest.raises(subprocess.CalledProcessError):
                boundary.assess(attempt)
        else:
            assert ('result_sha256' in state) is (first == 'ACCEPT')
            if first == 'ACCEPT':
                retry = boundary.assess(attempt)
                assert retry['receipt'] == receipt and retry['historical'] is True
                assert retry['validity'] == 'VOID' and retry['current_policy_eligible'] is False
            else:
                with pytest.raises(subprocess.CalledProcessError):
                    boundary.assess(attempt)
        assert boundary.events(attempt) == events
    finally:
        for name in [operation + '.before', winner + '.locked']:
            boundary.release_checkpoint(directory, name)
        boundary.restart()


@pytest.mark.parametrize('checkpoint,expected,intents', [
    ('CONTAINER', 'IN_DOUBT', 0), ('START_INTENT', 'IN_DOUBT', 1), ('CAPTURED', 'ATTESTED', 1),
])
def test_death_at_durable_checkpoint_preserves_one_execution(real_boundary, checkpoint, expected, intents):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True)
    directory = boundary.checkpoints(observe=[checkpoint], pause=[checkpoint])
    try:
        reserved = boundary.submit(bundle)
        boundary.checkpoint(directory, checkpoint)
        before = boundary.status(bundle['attempt_id'])
        history = boundary.events(bundle['attempt_id'])
        boundary.service.kill()
        boundary.service.wait(timeout=15)
        boundary.restart()
        state = boundary.wait(bundle['attempt_id'], states=(expected,))
        assert state['execution_id'] == reserved['execution_id']
        assert state['container_id'] == before['container_id']
        assert state['plan_sha256'] == before['plan_sha256']
        assert state['launch_intent_count'] == intents
        assert len(boundary.starts(state['container_id'])) == int(checkpoint == 'CAPTURED')
        after = boundary.events(bundle['attempt_id'])
        assert after[:len(history)] == history
        assert boundary.submit(bundle)['execution_id'] == state['execution_id']
        boundary.restart()
        assert boundary.events(bundle['attempt_id']) == after
        if expected == 'ATTESTED':
            assert state['attestation_count'] == 1
            boundary.assess(bundle['attempt_id'])
        else:
            assert state['attestation_count'] == 0 and 'result_sha256' not in state
            assert boundary.inspect(state['container_id'])['State']['Running'] is False
            with pytest.raises(subprocess.CalledProcessError):
                boundary.assess(bundle['attempt_id'])
    finally:
        boundary.release_checkpoint(directory, checkpoint)
        boundary.restart()


def test_expiration_between_start_intent_and_actual_start_never_accepts(real_boundary):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True, depth_valid_seconds=30)
    directory = boundary.checkpoints(observe=['START_INTENT'], pause=['START_INTENT'])
    try:
        boundary.submit(bundle)
        boundary.checkpoint(directory, 'START_INTENT')
        expiry = datetime.fromisoformat(bundle['depth_expires_at'].replace('Z', '+00:00'))
        while datetime.now(timezone.utc) <= expiry:
            time.sleep(.1)
        boundary.release_checkpoint(directory, 'START_INTENT')
        state = boundary.wait(bundle['attempt_id'], states=('IN_DOUBT',))
        assert state['launch_intent_count'] == 1 and state['attestation_count'] == 0
        assert 'result_sha256' not in state
        assert len(boundary.starts(state['container_id'])) == 1
        events = boundary.events(bundle['attempt_id'])
        assert any('expired' in row['data'].get('reason', '').lower() for row in events)
        boundary.restart()
        with pytest.raises(subprocess.CalledProcessError):
            boundary.submit(bundle)
        assert boundary.events(bundle['attempt_id']) == events
        assert len(boundary.starts(state['container_id'])) == 1
    finally:
        boundary.release_checkpoint(directory, 'START_INTENT')
        boundary.restart()


def test_lost_commit_acknowledgment_returns_original_receipt_after_death(real_boundary):
    boundary = real_boundary
    bundle = boundary.prepare(idle=True)
    directory = boundary.checkpoints(observe=['COMMIT.committed'], pause=['COMMIT.committed'])
    try:
        boundary.submit(bundle)
        state = boundary.wait(bundle['attempt_id'])
        with ThreadPoolExecutor(max_workers=1) as pool:
            response = pool.submit(boundary.assess, bundle['attempt_id'])
            boundary.checkpoint(directory, 'COMMIT.committed')
            committed = boundary.status(bundle['attempt_id'])
            events = boundary.events(bundle['attempt_id'])
            authentication = boundary.fetch(bundle['attempt_id'], committed['authentication_sha256'])
            original_receipt = json.loads(boundary.fetch(bundle['attempt_id'], committed['receipt_sha256']))
            boundary.service.kill()
            boundary.service.wait(timeout=15)
            with pytest.raises(subprocess.CalledProcessError):
                response.result(timeout=30)
        boundary.restart()
        # Deny a fresh signature: successful retry must use the original bytes.
        credential = boundary.root / 'keys/qg5/credential.json'
        owner = credential.stat()
        import os
        os.chown(credential, 0, 0)
        try:
            retry = boundary.assess(bundle['attempt_id'])
        finally:
            os.chown(credential, owner.st_uid, owner.st_gid)
        assert retry['historical'] is True
        assert retry['receipt'] == original_receipt
        assert retry['receipt']['authentication_sha256'] == committed['authentication_sha256']
        assert retry['receipt']['result_sha256'] == committed['result_sha256']
        assert boundary.fetch(bundle['attempt_id'], committed['authentication_sha256']) == authentication
        assert boundary.events(bundle['attempt_id']) == events
        assert len(boundary.starts(state['container_id'])) == 1
    finally:
        boundary.release_checkpoint(directory, 'COMMIT.committed')
        boundary.restart()
