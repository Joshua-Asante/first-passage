"""S3 genuine N1 capture and committed G5 decision on the canonical host.

Requires FP_QUALIFICATION_S3=1 (the dispatch/v5 installation) on top of the S2
environment. One deterministic synthetic PASS and one FAIL through actual
compute, capture, reconstruction and store; recovery, VOID ordering and payload
identity are asserted from the durable journal.
"""

import base64
import json
import sqlite3
import time

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from tools.qualification_verification import host


def budget(boundary, attempt):
    with sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    ) as connection:
        row = connection.execute(
            'SELECT snapshot_bytes FROM full_campaign_budgets WHERE attempt_id=?', (attempt,)
        ).fetchone()
    return json.loads(bytes(row[0]))


def has_work(state, work_id):
    return any(w['work_id'] == work_id for w in state['works'])


def work(state, work_id):
    return next(w for w in state['works'] if w['work_id'] == work_id)


def wait(boundary, attempt, predicate, seconds=330):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        state = budget(boundary, attempt)
        if predicate(state):
            host.save(boundary.output / (attempt + '-n1-budget.json'), state)
            return state
        if state['state'] in (
            'BUDGET_EXHAUSTED',
            'BUDGET_UNCERTAIN',
            'IN_DOUBT',
            'ABORTED',
            'N1_FAILED',
        ):
            host.save(boundary.output / (attempt + '-n1-budget.json'), state)
            return state
        time.sleep(0.1)
    raise AssertionError('bounded N1 campaign wait expired')


def admit(boundary, *, idle):
    bundle = boundary.prepare(idle=idle)
    fields = {
        'schema': 'qualification_campaign_request/v2',
        'request_id': 'dispatch',
        'attempt_id': bundle['attempt_id'],
        'bundle_sha256': bundle['bundle_sha256'],
    }
    first = json.loads(boundary.request('SUBMIT_E1', **fields))
    assert first['schema'] == 'qualification_campaign_status/v2', first
    state = wait(
        boundary, bundle['attempt_id'], lambda s: work(s, 'admission')['state'] == 'COMPLETED'
    )
    assert state['state'] == 'BOUND', state
    return bundle['attempt_id']


def dispatch(boundary, attempt, work_id, role):
    reply = boundary.schedule(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': attempt,
            'work_id': work_id,
            'role': role,
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': None,
        }
    )
    assert reply['ok'], reply
    # A compact refusal answers ok with status only; the work must durably exist
    # before the caller waits on it.
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if has_work(budget(boundary, attempt), work_id):
            return reply
        time.sleep(0.1)
    raise AssertionError(
        'dispatch refused for ' + work_id + ': ' + json.dumps(reply.get('data_b64', b''))[:400]
    )


def completed_works(state):
    return [w for w in state['works'] if w['state'] == 'COMPLETED']


def payload_identity_events(boundary, attempt, work_id):
    from test_campaign_supervision_linux import payload_process_events

    return payload_process_events(boundary, attempt, work_id)


def committing_g5_completed(boundary, attempt, progression, seconds=120):
    """The G5 work that committed the checkpoint settles after T2 and completes
    in the progression state its commit produced (PR #455 review, Codex P2);
    a resource-terminal state here would mean the settlement ended authority."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        state = budget(boundary, attempt)
        row = work(state, 'g5work')
        if row['state'] == 'COMPLETED':
            assert state['state'] == progression, state
            assert row['observation_bytes_b64'] is not None and row['charge_cpu_ns'] <= row['limits']['cpu_ns'], row
            return state
        assert state['state'] == progression, state
        time.sleep(0.1)
    raise AssertionError('the committing g5 work never completed')


def test_s3_genuine_pass_reaches_n2_ready(real_boundary):
    boundary = real_boundary
    if not boundary.dispatch:
        pytest.skip('FP_QUALIFICATION_S3=1 required; the S2 selection skips the N1 dispatch installation')
    attempt = admit(boundary, idle=False)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: (
            s.get('checkpoints', {}).get('N1', {}).get('state') == 'ATTESTED'
            and work(s, 'n1work')['state'] == 'COMPLETED'
        )
        or s['state'] not in ('BOUND',),
    )
    assert state['state'] == 'BOUND', state
    family = state['checkpoints']['N1']
    assert family['work_id'] == 'n1work' and family['state'] == 'ATTESTED'
    assert work(state, 'n1work')['state'] == 'COMPLETED'
    dispatch(boundary, attempt, 'g5work', 'n1_g5')
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'))
    assert state['state'] == 'N2_READY', state
    # Exactly one N1 compute work; no N2/Part A work exists.
    phases = [w['phase'] for w in state['works']]
    assert phases.count('N1') == 1 and not any(
        p.startswith('N2') or p.startswith('PART_A') for p in phases
    )
    assert state['checkpoints']['N1']['state'] == 'COMMITTED'
    assert state['checkpoints']['N1']['decision'] == 'CONTINUE'
    # The admission work is R1's explicit exemption (its guardian is the
    # supervised process, outside any payload slice); every other completed
    # work carries a retained payload identity.
    state = committing_g5_completed(boundary, attempt, 'N2_READY')
    for row in completed_works(state):
        if row['work_id'] != 'admission':
            assert payload_identity_events(boundary, attempt, row['work_id']), row['work_id']


def test_s3_genuine_fail_is_terminal(real_boundary):
    boundary = real_boundary
    if not boundary.dispatch:
        pytest.skip('FP_QUALIFICATION_S3=1 required; the S2 selection skips the N1 dispatch installation')
    attempt = admit(boundary, idle=True)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: (
            s.get('checkpoints', {}).get('N1', {}).get('state') == 'ATTESTED'
            and work(s, 'n1work')['state'] == 'COMPLETED'
        )
        or s['state'] not in ('BOUND',),
    )
    dispatch(boundary, attempt, 'g5work', 'n1_g5')
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'))
    assert state['state'] == 'N1_FAILED', state
    assert state['checkpoints']['N1']['decision'] == 'FAILURE'
    committing_g5_completed(boundary, attempt, 'N1_FAILED')


def test_s3_guardian_death_mid_n1_is_in_doubt_with_no_capture(real_boundary):
    boundary = real_boundary
    if not boundary.dispatch:
        pytest.skip('FP_QUALIFICATION_S3=1 required; the S2 selection skips the N1 dispatch installation')
    attempt = admit(boundary, idle=False)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    # Kill the guardian mid-RUNNING; under A3 only a service restart recovers
    # the work, so the restart IS the scene's mechanism, not cleanup.
    deadline = time.monotonic() + 30
    killed = False
    while time.monotonic() < deadline:
        state = budget(boundary, attempt)
        if work(state, 'n1work')['state'] == 'RUNNING' and not killed:
            _kill_guardian(boundary, state)
            killed = True
            break
        time.sleep(0.1)
    assert killed, 'guardian never reached RUNNING'
    boundary.restart()
    state = wait(
        boundary,
        attempt,
        lambda s: work(s, 'n1work')['state'] == 'IN_DOUBT' or s['state'] not in ('BOUND',),
        seconds=120,
    )
    assert work(state, 'n1work')['state'] == 'IN_DOUBT', state
    assert 'checkpoints' not in state or 'N1' not in state.get('checkpoints', {}), state
    boundary.restart()
    final = wait(boundary, attempt, lambda s: work(s, 'n1work')['state'] == 'IN_DOUBT', seconds=120)
    assert work(final, 'n1work')['state'] == 'IN_DOUBT', final


def _kill_guardian(boundary, state):
    import subprocess
    from tools.qualification_verification.container_ownership import campaign_scopes

    scopes = campaign_scopes(boundary.manifest['run_id'], state['attempt_id'], 'n1work')
    subprocess.run(
        [
            '/usr/bin/systemctl',
            '--system',
            '--no-ask-password',
            'kill',
            '--signal=KILL',
            scopes['guardian_unit'],
        ],
        capture_output=True,
        check=False,
    )


def test_s3_g5_unit_death_and_exact_receipt_retry(real_boundary):
    """E06/E07: the qg5 unit dies after T1, before T2; a fresh retry unit
    redelivers the exact candidate and the interrupted signing completes with
    the persisted instant -- never a fresh time or signature."""
    boundary = real_boundary
    if not boundary.dispatch:
        pytest.skip('FP_QUALIFICATION_S3=1 required; the S2 selection skips the N1 dispatch installation')
    attempt = admit(boundary, idle=False)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    wait(
        boundary,
        attempt,
        lambda s: (
            s.get('checkpoints', {}).get('N1', {}).get('state') == 'ATTESTED'
            and work(s, 'n1work')['state'] == 'COMPLETED'
        )
        or s['state'] not in ('BOUND',),
    )
    # (1) Hold the commit open between T1 and T2 (the ruled diagnostic fault),
    # wait for the durable intent, then kill the real qg5 unit mid-window.
    dispatch_frozen = boundary.schedule(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': attempt,
            'work_id': 'g5work',
            'role': 'n1_g5',
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': 'hold_after_intent',
        }
    )
    assert dispatch_frozen['ok'], dispatch_frozen
    deadline = time.monotonic() + 120
    unit = None
    while time.monotonic() < deadline:
        with sqlite3.connect(
            (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
        ) as connection:
            row = connection.execute(
                'SELECT candidate_bytes FROM full_campaign_checkpoint_intents '
                'WHERE attempt_id=?',
                (attempt,),
            ).fetchone()
        if row is not None:
            import subprocess
            from tools.qualification_verification.container_ownership import campaign_scopes

            scopes = campaign_scopes(boundary.manifest['run_id'], attempt, 'g5work')
            unit = scopes['payload_slice'][:-6] + '-g5.service'
            subprocess.run(
                [
                    '/usr/bin/systemctl',
                    '--system',
                    '--no-ask-password',
                    'kill',
                    '--signal=KILL',
                    unit,
                ],
                capture_output=True,
                check=False,
            )
            break
        time.sleep(0.1)
    assert unit is not None, 'the held intent never became durable'
    state = wait(
        boundary,
        attempt,
        lambda s: (
            work(s, 'g5work')['state'] == 'SIGNING_INTENT'
            and work(s, 'g5work')['observation_bytes_b64'] is not None
        )
        or s['state'] not in ('BOUND',),
        seconds=120,
    )
    assert state['state'] == 'BOUND', state
    settled = work(state, 'g5work')
    assert (
        settled['state'] == 'SIGNING_INTENT' and settled['observation_bytes_b64'] is not None
    ), state
    with sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    ) as connection:
        intent_row, receipt_row = connection.execute(
            'SELECT intent_bytes,receipt_bytes FROM full_campaign_checkpoint_intents WHERE attempt_id=?',
            (attempt,),
        ).fetchone()
    assert intent_row is not None and receipt_row is None, 'no receipt may exist mid-window'
    persisted_intent = json.loads(bytes(intent_row))
    # (2) A fresh retry unit redelivers the exact candidate; the interrupted
    # signing completes with the persisted instant.
    retry = boundary.schedule(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': attempt,
            'work_id': 'g5retry',
            'role': 'n1_g5',
            'probe': 'noop',
            'signing_retry_of': 'g5work',
            'fault': None,
        }
    )
    assert retry['ok'], retry
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'), seconds=330)
    assert state['state'] == 'N2_READY', state
    with sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    ) as connection:
        receipt_bytes = connection.execute(
            'SELECT receipt_bytes FROM full_campaign_checkpoint_intents WHERE attempt_id=?',
            (attempt,),
        ).fetchone()[0]
    receipt = json.loads(bytes(receipt_bytes))
    assert receipt['signing_at_utc'] == persisted_intent['signing_at_utc'], receipt
    # (3) The exact wire retry as the qg5 peer returns the byte-identical
    # receipt, historical.
    retry_reply = json.loads(
        boundary.request(
            'COMMIT_CHECKPOINT_ASSESSMENT',
            role='qg5',
            schema='qualification_campaign_request/v2',
            attempt_id=attempt,
            checkpoint='N1',
            work_id='g5work',
            candidate_bytes_b64=base64.b64encode(_candidate(boundary, attempt)).decode('ascii'),
            artifacts=[],
        )
    )
    assert retry_reply['receipt'] == receipt and retry_reply['historical'] is True, retry_reply
    # (4) A different candidate under the persisted intent refuses.
    tampered = json.loads(_candidate(boundary, attempt))
    tampered['cutoff']['n1_cutoffs'] = {'FULL': 9, 'H1': 9, 'H2': 9}
    tampered_bytes = json.dumps(tampered, sort_keys=True, separators=(',', ':')).encode()
    try:
        boundary.request(
            'COMMIT_CHECKPOINT_ASSESSMENT',
            role='qg5',
            schema='qualification_campaign_request/v2',
            attempt_id=attempt,
            checkpoint='N1',
            work_id='g5work',
            candidate_bytes_b64=base64.b64encode(tampered_bytes).decode('ascii'),
            artifacts=[],
        )
        raise AssertionError('a different candidate under a persisted intent must refuse')
    except Exception as exc:
        assert 'exact checkpoint candidate retry required' in str(exc), exc


def _candidate(boundary, attempt):
    with sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    ) as connection:
        row = connection.execute(
            'SELECT candidate_bytes FROM full_campaign_checkpoint_intents ' 'WHERE attempt_id=?',
            (attempt,),
        ).fetchone()
    return bytes(row[0])
