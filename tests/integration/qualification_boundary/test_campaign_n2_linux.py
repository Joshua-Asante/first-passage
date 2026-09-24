"""S4 genuine joint N2/Part B batch and committed G5 decisions on the canonical
host. Requires FP_QUALIFICATION_S4=1 (the joint dispatch/v6 installation) on top
of the S3 environment; skips everywhere else, including --test-only."""

import json
import sqlite3

import pytest

from test_campaign_n1_linux import (
    admit,
    budget,
    committing_g5_completed,
    completed_works,
    dispatch,
    payload_identity_events,
    wait,
    work,
)


def n2_family(state):
    return (state.get('checkpoints') or {}).get('N2')


def stage_decisions(boundary, attempt):
    """The committed N2 assessment's stage decisions, from the custody row."""
    connection = sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    )
    try:
        row = connection.execute(
            'SELECT candidate_bytes FROM full_campaign_checkpoint_intents '
            "WHERE attempt_id=? AND checkpoint='N2'",
            (attempt,),
        ).fetchone()
    finally:
        connection.close()
    assert row is not None, 'committed N2 assessment required'
    return json.loads(bytes(row[0]))['stage_decisions']


def committed_n1(boundary, *, idle=False):
    """Admission through the committed N1 receipt (campaign N2_READY)."""
    attempt = admit(boundary, idle=idle)
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    wait(
        boundary,
        attempt,
        lambda s: n2_family(s) is None
        and next(w for w in s['works'] if w['work_id'] == 'n1work')['state']
        == 'COMPLETED'
        and (s.get('checkpoints') or {}).get('N1', {}).get('state') == 'ATTESTED',
    )
    dispatch(boundary, attempt, 'g5work', 'n1_g5')
    wait(boundary, attempt, lambda s: s['state'] == 'N2_READY')
    # #461: N2_READY commits while the qg5 unit is still returning; the N1 G5
    # work settles (leaves SIGNED) only once its cgroup empties, and until then
    # the service refuses the next signing work ('signing authority serialized').
    committing_g5_completed(boundary, attempt, 'N2_READY')
    return attempt


def test_s4_genuine_joint_pass_reaches_part_a_ready(real_boundary):
    if not getattr(real_boundary, 'joint', False):
        pytest.skip('FP_QUALIFICATION_S4=1 required; the joint dispatch installation')
    boundary = real_boundary
    attempt = committed_n1(boundary)
    dispatch(boundary, attempt, 'n2work', 'n2_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: work(s, 'n2work')['state'] != 'START_INTENT',
        seconds=90,
    )
    assert work(state, 'n2work')['state'] == 'RUNNING'
    wait(
        boundary,
        attempt,
        lambda s: (n2_family(s) or {}).get('state') == 'ATTESTED'
        and work(s, 'n2work')['state'] == 'COMPLETED',
        seconds=1080,
    )
    dispatch(boundary, attempt, 'n2g5', 'n2_g5')
    state = wait(
        boundary, attempt, lambda s: s['state'] in ('PART_A_READY', 'N2_FAILED'),
        seconds=1080,
    )
    assert state['state'] == 'PART_A_READY'
    family = n2_family(state)
    assert family['state'] == 'COMMITTED' and family['decision'] == 'CONTINUE'
    assert stage_decisions(boundary, attempt) == {'N2': 'PASS', 'PART_B': 'PASS'}
    committing_g5_completed(boundary, attempt, 'PART_A_READY', work_id='n2g5')
    state = budget(boundary, attempt)
    finished = {w['work_id'] for w in completed_works(state)}
    assert finished >= {'admission', 'n1work', 'g5work', 'n2work'}
    for row in completed_works(state):
        if row['work_id'] != 'admission':
            assert payload_identity_events(boundary, attempt, row['work_id'])


def test_s4_guardian_death_mid_n2_is_in_doubt_with_no_capture(real_boundary):
    if not getattr(real_boundary, 'joint', False):
        pytest.skip('FP_QUALIFICATION_S4=1 required; the joint dispatch installation')
    boundary = real_boundary
    attempt = committed_n1(boundary)
    dispatch(boundary, attempt, 'n2work', 'n2_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: work(s, 'n2work')['state'] == 'RUNNING'
        and payload_identity_events(boundary, attempt, 'n2work'),
        seconds=120,
    )
    assert state['state'] == 'N2_READY'
    assert work(state, 'n2work')['state'] == 'RUNNING'
    _kill_work_guardian(boundary, attempt, 'n2work')
    boundary.restart()
    state = wait(boundary, attempt, lambda s: work(s, 'n2work')['state'] == 'IN_DOUBT')
    assert work(state, 'n2work')['state'] == 'IN_DOUBT'
    assert n2_family(state) is None
    assert (state.get('checkpoints') or {}).get('N1', {}).get('state') == 'COMMITTED'
    boundary.restart()
    state = wait(boundary, attempt, lambda s: work(s, 'n2work')['state'] == 'IN_DOUBT')
    assert work(state, 'n2work')['state'] == 'IN_DOUBT'
    assert n2_family(state) is None


def _kill_work_guardian(boundary, attempt, work_id):
    import subprocess
    from tools.qualification_verification.container_ownership import campaign_scopes

    unit = campaign_scopes(boundary.manifest['run_id'], attempt, work_id)['guardian_unit']
    subprocess.run(
        [
            '/usr/bin/systemctl',
            '--system',
            '--no-ask-password',
            'kill',
            '--signal=KILL',
            unit,
        ],
        check=True,
    )


def test_s4_n2_g5_unit_death_and_exact_receipt_retry(real_boundary):
    if not getattr(real_boundary, 'joint', False):
        pytest.skip('FP_QUALIFICATION_S4=1 required; the joint dispatch installation')
    boundary = real_boundary
    attempt = committed_n1(boundary)
    dispatch(boundary, attempt, 'n2work', 'n2_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: work(s, 'n2work')['state'] != 'START_INTENT',
        seconds=90,
    )
    assert work(state, 'n2work')['state'] == 'RUNNING'
    wait(
        boundary,
        attempt,
        lambda s: (n2_family(s) or {}).get('state') == 'ATTESTED'
        and work(s, 'n2work')['state'] == 'COMPLETED',
        seconds=1080,
    )
    dispatch_frozen = boundary.schedule(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': attempt,
            'work_id': 'n2g5',
            'role': 'n2_g5',
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': 'hold_after_intent',
        }
    )
    assert dispatch_frozen['ok'], dispatch_frozen
    connection = sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    )
    try:
        row = None
        for _ in range(1200):
            row = connection.execute(
                'SELECT intent_bytes,candidate_bytes FROM full_campaign_checkpoint_intents '
                "WHERE attempt_id=? AND checkpoint='N2'",
                (attempt,),
            ).fetchone()
            if row is not None:
                break
            import time

            time.sleep(0.25)
    finally:
        connection.close()
    assert row is not None, 'the held N2 intent never persisted'
    persisted_intent = json.loads(bytes(row[0]))
    import subprocess

    from tools.qualification_verification.container_ownership import campaign_scopes

    unit = campaign_scopes(boundary.manifest['run_id'], attempt, 'n2g5')['payload_slice'][
        :-6
    ] + '-g5.service'
    subprocess.run(
        ['systemctl', '--system', 'kill', '--signal=KILL', unit],
        check=False,
        capture_output=True,
        timeout=10,
    )
    state = wait(
        boundary, attempt, lambda s: work(s, 'n2g5')['observation_bytes_b64'] is not None
    )
    assert work(state, 'n2g5')['state'] == 'SIGNING_INTENT'
    retry = boundary.schedule(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': attempt,
            'work_id': 'n2g5retry',
            'role': 'n2_g5',
            'probe': 'noop',
            'signing_retry_of': 'n2g5',
            'fault': None,
        }
    )
    assert retry['ok'], retry
    state = wait(boundary, attempt, lambda s: s['state'] in ('PART_A_READY', 'N2_FAILED'))
    assert state['state'] == 'PART_A_READY'
    connection = sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    )
    try:
        receipt = connection.execute(
            'SELECT receipt_bytes FROM full_campaign_checkpoint_intents '
            "WHERE attempt_id=? AND checkpoint='N2'",
            (attempt,),
        ).fetchone()
    finally:
        connection.close()
    committed = json.loads(bytes(receipt[0]))
    assert committed['signing_at_utc'] == persisted_intent['signing_at_utc'], committed
    assert committed['campaign_state'] == 'PART_A_READY'
    assert committed['stage_decisions'] == {'N2': 'PASS', 'PART_B': 'PASS'}
