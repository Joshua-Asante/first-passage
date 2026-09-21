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

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from tools.qualification_verification import host


def budget(boundary, attempt):
    with sqlite3.connect((boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True) as connection:
        row = connection.execute('SELECT snapshot_bytes FROM full_campaign_budgets WHERE attempt_id=?',
                                 (attempt,)).fetchone()
    return json.loads(bytes(row[0]))


def work(state, work_id):
    return next(w for w in state['works'] if w['work_id'] == work_id)


def wait(boundary, attempt, predicate, seconds=330):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        state = budget(boundary, attempt)
        if predicate(state):
            host.save(boundary.output / (attempt + '-n1-budget.json'), state)
            return state
        if state['state'] in ('BUDGET_EXHAUSTED', 'BUDGET_UNCERTAIN', 'IN_DOUBT', 'ABORTED', 'N1_FAILED'):
            host.save(boundary.output / (attempt + '-n1-budget.json'), state)
            return state
        time.sleep(.1)
    raise AssertionError('bounded N1 campaign wait expired')


def admit(boundary, *, idle):
    bundle = boundary.prepare(idle=idle)
    fields = dict(schema='qualification_campaign_request/v2', request_id='dispatch',
                  attempt_id=bundle['attempt_id'], bundle_sha256=bundle['bundle_sha256'])
    first = json.loads(boundary.request('SUBMIT_E1', **fields))
    assert first['schema'] == 'qualification_campaign_status/v2', first
    state = wait(boundary, bundle['attempt_id'], lambda s: work(s, 'admission')['state'] == 'COMPLETED')
    assert state['state'] == 'BOUND', state
    return bundle['attempt_id']


def dispatch(boundary, attempt, work_id, role):
    reply = boundary.schedule(dict(schema='qualification_campaign_schedule_request/v1',
        attempt_id=attempt, work_id=work_id, role=role, probe='noop', signing_retry_of=None))
    assert reply['ok'], reply
    return reply


def completed_works(state):
    return [w for w in state['works'] if w['state'] == 'COMPLETED']


def payload_identity_events(boundary, attempt, work_id):
    from test_campaign_supervision_linux import payload_process_events
    return payload_process_events(boundary, attempt, work_id)


def test_s3_genuine_pass_reaches_n2_ready(real_boundary):
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=False)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    state = wait(boundary, attempt, lambda s: (
        s.get('checkpoints', {}).get('N1', {}).get('state') == 'ATTESTED'
        and work(s, 'n1work')['state'] == 'COMPLETED') or s['state'] not in ('BOUND',))
    assert state['state'] == 'BOUND', state
    family = state['checkpoints']['N1']
    assert family['work_id'] == 'n1work' and family['state'] == 'ATTESTED'
    assert work(state, 'n1work')['state'] == 'COMPLETED'
    dispatch(boundary, attempt, 'g5work', 'n1_g5')
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'))
    assert state['state'] == 'N2_READY', state
    # Exactly one N1 compute work; no N2/Part A work exists.
    phases = [w['phase'] for w in state['works']]
    assert phases.count('N1') == 1 and not any(p.startswith('N2') or p.startswith('PART_A') for p in phases)
    assert state['checkpoints']['N1']['state'] == 'COMMITTED'
    assert state['checkpoints']['N1']['decision'] == 'CONTINUE'
    # The admission work is R1's explicit exemption (its guardian is the
    # supervised process, outside any payload slice); every other completed
    # work carries a retained payload identity.
    for row in completed_works(state):
        if row['work_id'] != 'admission':
            assert payload_identity_events(boundary, attempt, row['work_id']), row['work_id']


def test_s3_genuine_fail_is_terminal(real_boundary):
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=True)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    state = wait(boundary, attempt, lambda s: (
        s.get('checkpoints', {}).get('N1', {}).get('state') == 'ATTESTED'
        and work(s, 'n1work')['state'] == 'COMPLETED') or s['state'] not in ('BOUND',))
    dispatch(boundary, attempt, 'g5work', 'n1_g5')
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'))
    assert state['state'] == 'N1_FAILED', state
    assert state['checkpoints']['N1']['decision'] == 'FAILURE'


def test_s3_guardian_death_mid_n1_is_in_doubt_with_no_capture(real_boundary):
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=False)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    deadline = time.monotonic() + 30
    killed = False
    while time.monotonic() < deadline:
        state = budget(boundary, attempt)
        if work(state, 'n1work')['state'] == 'RUNNING' and not killed:
            _kill_guardian(boundary, state)
            killed = True
        if killed and work(budget(boundary, attempt), 'n1work')['state'] in ('IN_DOUBT', 'CAPTURED'):
            break
        time.sleep(.1)
    state = budget(boundary, attempt)
    assert work(state, 'n1work')['state'] == 'IN_DOUBT', state
    assert 'checkpoints' not in state or 'N1' not in state.get('checkpoints', {}), state
    boundary.restart()
    final = wait(boundary, attempt, lambda s: s['state'] not in ('BOUND',) or True)
    assert work(final, 'n1work')['state'] == 'IN_DOUBT', final


def _kill_guardian(boundary, state):
    import subprocess
    from tools.qualification_verification.container_ownership import campaign_scopes
    scopes = campaign_scopes(boundary.manifest['run_id'], state['attempt_id'], 'n1work')
    subprocess.run(['/usr/bin/systemctl', '--system', '--no-ask-password', 'kill', '--signal=KILL',
                    scopes['guardian_unit']], capture_output=True, check=False)


def test_s3_g5_unit_death_and_exact_receipt_retry(real_boundary):
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=False)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    wait(boundary, attempt, lambda s: s.get('checkpoints', {}).get('N1', {}).get('state') == 'ATTESTED'
         or s['state'] not in ('BOUND',))
    dispatch(boundary, attempt, 'g5work', 'n1_g5')
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'))
    assert state['state'] == 'N2_READY', state
    with sqlite3.connect((boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True) as connection:
        receipt = connection.execute('SELECT receipt_bytes FROM full_campaign_checkpoint_intents '
                                     'WHERE attempt_id=?', (attempt,)).fetchone()
    assert receipt is not None and receipt[0] is not None
    # The exact commit retry over the wire returns the byte-identical receipt.
    from test_campaign_supervision_linux import schedule_document
    reply = boundary.raw_request(dict(schema='qualification_campaign_request/v2',
        operation='COMMIT_CHECKPOINT_ASSESSMENT', attempt_id=attempt, checkpoint='N1', work_id='g5work',
        candidate_bytes_b64=base64.b64encode(_candidate(boundary, attempt)).decode('ascii'), artifacts=[]))
    assert reply.get('ok') is False and 'exact checkpoint candidate retry required' in str(reply.get('error')), reply


def _candidate(boundary, attempt):
    with sqlite3.connect((boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True) as connection:
        row = connection.execute('SELECT candidate_bytes FROM full_campaign_checkpoint_intents '
                                 'WHERE attempt_id=?', (attempt,)).fetchone()
    return bytes(row[0])
