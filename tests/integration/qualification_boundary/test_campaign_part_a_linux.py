"""S5 genuine Part A campaigns and committed G5 decisions on the canonical host.

Requires FP_QUALIFICATION_S5=1 (the Part A /v7 installation, fixture_install
--part-a) on top of the S4 environment; skips everywhere else, including
--test-only. Every campaign here runs actual synthetic market/session sources
through the committed N1 and joint N2/Part B route to PART_A_READY first, then
one metered part_a_worker and one part_a_g5.

Disclosures (packet section 4, verbatim): "prescribed expansion cannot occur on
the (2, 4, 2) fixture (section 0.1 F1), so the required-expansion case stands on
the arithmetic boundary test, which is not called a full-route witness".

Cases the packet's Linux line names, and how each stands here:

(a) genuine Part A without expansion -> FULL_PASS_READY, after which the SR-8
    export ``evidence/boundary/part_a_observations.json`` is written from the
    settled observation, the work's reservation-to-CAPTURED clocks and the
    captured payload's own ``part_a`` block (the closed key set of
    scripts/s2_run_evidence.py). The payload/guardian CPU split is exported as
    null: the guardian retains no per-side CPU (PAYLOAD_EXIT carries exit
    facts only), so it is "not available" in SR-8's own words.

(b) a genuine below-floor or above-FULL failure -> PART_A_FAILED: NOT
    PRESENT. The fixture supports exactly two synthetic sources, the default
    ORB port (which passes N1, N2/Part B and Part A: the S4 witness plus F1)
    and ``--idle`` (no orders at all, which fails at N1 -> N1_FAILED before any
    PART_A dispatch exists). ``--fault`` variants fault the first replayed bar
    inside the N1 worker, and a ``budget`` override ends in BUDGET_EXHAUSTED,
    never a statistical decision. Section 3 forbids a fabricated FAIL, so the
    Linux line has no genuine PART_A_FAILED witness on this fixture; the
    below-floor and above-FULL decisions stand on the adapter boundary tests
    and the G5 all-failure reconstruction in
    tests/ops/qualification/execution/test_campaign_part_a.py.

(c) crash after the initial-prefix artifact is fsynced and before the final
    artifact -> IN_DOUBT with the initial prefix retained: the NEAREST HONEST
    CASE only. The existing fault mechanism (fixture_install --fault
    stop|exit_zero|cpu|memory|wall) is a signed port hook at the first
    replayed bar: it fires in the N1 worker, so a fault bundle never reaches
    PART_A_READY, and inside a PART_A worker every replay precedes the prefix
    write. No existing mechanism lands between the two S5-D1 writes, and no
    production seam is added. The case here kills the payload slice while the
    PART_A worker is RUNNING: the guardian's abnormal-exit path then archives
    whichever S5-D1 artifact already exists (role part_a_initial_prefix and/or
    part_a_final) for inspection before the IN_DOUBT transition, and the
    campaign never relaunches. Which artifacts exist at the kill is timing
    dependent, so the assertions are conditional: a retained final implies a
    retained initial prefix that it byte-extends, and nothing else is ever
    staged. The retained-prefix-only outcome is therefore witnessed only when
    the kill happens to land in the window; it is never forced.

(d) g5 death + exact retry: the held PART_A intent, the killed part_a_g5
    unit, the SIGNING_INTENT work, and an exact ``signing_retry_of`` that
    commits FULL_PASS_READY with the persisted intent's signing clock.

No case constructs PartAMeasurementOverride (P-3).
"""

import base64
import hashlib
import json
import sqlite3
import subprocess
import time

import pytest

from test_campaign_n1_linux import (
    budget,
    committing_g5_completed,
    completed_works,
    dispatch,
    payload_identity_events,
    wait,
    work,
)
from test_campaign_n2_linux import committed_n1, n2_family
from tools.qualification_verification import host

PART_A_EXPORT_NAME = 'part_a_observations.json'
PART_A_EXPORT_SCHEMA = 'qualification_part_a_observations/v1'
PART_A_STAGED_ROLES = {'part_a_initial_prefix', 'part_a_final'}


def part_a_family(state):
    return (state.get('checkpoints') or {}).get('PART_A')


def _journal(boundary):
    return sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    )


def staged_part_a(boundary, attempt):
    """The archived S5-D1 artifacts, role -> bytes (campaigns.stage_checkpoint_artifact,
    checkpoint PART_A)."""
    connection = _journal(boundary)
    try:
        rows = connection.execute(
            'SELECT role,body FROM full_campaign_checkpoint_staged '
            "WHERE attempt_id=? AND checkpoint='PART_A'",
            (attempt,),
        ).fetchall()
    finally:
        connection.close()
    staged = {}
    for role, body in rows:
        assert role not in staged, 'one archived artifact per PART_A role'
        staged[role] = bytes(body)
    return staged


def captured_part_a_payload(boundary, attempt):
    """The captured PART_A worker document exactly as archived."""
    connection = _journal(boundary)
    try:
        row = connection.execute(
            'SELECT payload_bytes FROM full_campaign_checkpoint_captures '
            "WHERE attempt_id=? AND checkpoint='PART_A'",
            (attempt,),
        ).fetchone()
    finally:
        connection.close()
    assert row is not None, 'captured PART_A payload required'
    return json.loads(bytes(row[0]))


def _decoded(value):
    return json.loads(base64.b64decode(value))


def committed_n2(boundary):
    """Admission through the committed joint N2/Part B receipt (campaign
    PART_A_READY): the S4 genuine joint pass, reused as this file's prelude."""
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
        boundary, attempt, lambda s: s['state'] in ('PART_A_READY', 'N2_FAILED'), seconds=1080
    )
    assert state['state'] == 'PART_A_READY', state
    committing_g5_completed(boundary, attempt, 'PART_A_READY', work_id='n2g5')
    return attempt


def attested_part_a(boundary, attempt):
    """One metered part_a_worker through the route to ATTESTED/COMPLETED."""
    dispatch(boundary, attempt, 'pawork', 'part_a_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: work(s, 'pawork')['state'] != 'START_INTENT',
        seconds=90,
    )
    assert work(state, 'pawork')['state'] == 'RUNNING'
    state = wait(
        boundary,
        attempt,
        lambda s: (part_a_family(s) or {}).get('state') == 'ATTESTED'
        and work(s, 'pawork')['state'] == 'COMPLETED',
        seconds=1080,
    )
    assert work(state, 'pawork')['state'] == 'COMPLETED', state
    return state


def write_part_a_observations(boundary, attempt):
    """SR-8: the PART_A settled observation fields, the reservation-to-CAPTURED
    boottime, the CPU split where available (null here), and the captured
    payload's probe_seconds and predicted_seconds -- exactly the closed key set
    scripts/s2_run_evidence.py reads at evidence/boundary/part_a_observations.json."""
    state = budget(boundary, attempt)
    row = work(state, 'pawork')
    observation = _decoded(row['observation_bytes_b64'])
    reservation = _decoded(row['reservation_bytes_b64'])
    transitions = [_decoded(item) for item in row['transitions']]
    captured = next(t for t in transitions if t['state'] == 'CAPTURED')
    reserved_at = reservation['clock']['boottime_ns']
    captured_at = captured['clock']['boottime_ns']
    assert reserved_at is not None and captured_at is not None, 'boottime clocks required'
    part_a = captured_part_a_payload(boundary, attempt)['part_a']
    doc = {
        'schema': PART_A_EXPORT_SCHEMA,
        'attempt_id': attempt,
        'cpu_ns': observation['cpu_ns'],
        'memory_peak_bytes': observation['memory_peak_bytes'],
        'oom_events': observation['oom_events'],
        'reservation_to_captured_boottime_ns': captured_at - reserved_at,
        # The guardian retains no per-side CPU (PAYLOAD_EXIT carries exit facts
        # only), so the split is not available: null on both sides.
        'payload_cpu_ns': None,
        'guardian_cpu_ns': None,
        'probe_seconds': part_a['probe_seconds'],
        'predicted_seconds': part_a['predicted_seconds'],
    }
    for key in ('cpu_ns', 'memory_peak_bytes', 'oom_events', 'reservation_to_captured_boottime_ns'):
        assert type(doc[key]) is int and doc[key] >= 0, (key, doc[key])
    for key in ('probe_seconds', 'predicted_seconds'):
        assert type(doc[key]) is float and doc[key] >= 0.0, (key, doc[key])
    host.save(boundary.output / PART_A_EXPORT_NAME, doc, exclusive=True)
    return doc


def test_s5_genuine_part_a_without_expansion_reaches_full_pass_ready(real_boundary):
    if not getattr(real_boundary, 'part_a', False):
        pytest.skip('FP_QUALIFICATION_S5=1 required; the Part A /v7 installation')
    boundary = real_boundary
    attempt = committed_n2(boundary)
    attested_part_a(boundary, attempt)
    dispatch(boundary, attempt, 'pag5', 'part_a_g5')
    state = wait(
        boundary,
        attempt,
        lambda s: s['state'] in ('FULL_PASS_READY', 'PART_A_FAILED'),
        seconds=1080,
    )
    assert state['state'] == 'FULL_PASS_READY', state
    family = part_a_family(state)
    assert family['state'] == 'COMMITTED' and family['decision'] == 'CONTINUE'
    committing_g5_completed(boundary, attempt, 'FULL_PASS_READY', work_id='pag5')
    # S5-D1 custody: both artifacts archived, the final a byte-extension of the
    # initial prefix, each bound to the payload's own digests; no expansion (F1).
    payload_part_a = captured_part_a_payload(boundary, attempt)['part_a']
    staged = staged_part_a(boundary, attempt)
    assert set(staged) == PART_A_STAGED_ROLES, sorted(staged)
    initial = staged['part_a_initial_prefix']
    final = staged['part_a_final']
    assert final[: len(initial)] == initial
    assert hashlib.sha256(initial).hexdigest() == payload_part_a['initial_prefix_sha256']
    assert hashlib.sha256(final).hexdigest() == payload_part_a['final_sha256']
    assert payload_part_a['expansion_required'] is False
    assert payload_part_a['final_panels'] == payload_part_a['initial_panels']
    state = budget(boundary, attempt)
    finished = {w['work_id'] for w in completed_works(state)}
    assert finished >= {'admission', 'n1work', 'g5work', 'n2work', 'n2g5', 'pawork'}
    for row in completed_works(state):
        if row['work_id'] != 'admission':
            assert payload_identity_events(boundary, attempt, row['work_id']), row['work_id']
    exported = write_part_a_observations(boundary, attempt)
    assert exported['attempt_id'] == attempt


def _kill_payload_slice(boundary, attempt, work_id):
    from tools.qualification_verification.container_ownership import campaign_scopes

    unit = campaign_scopes(boundary.manifest['run_id'], attempt, work_id)['payload_slice']
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


def test_s5_payload_death_mid_part_a_is_in_doubt_and_archives_only_written_artifacts(
    real_boundary,
):
    """The nearest honest form of the packet's case (c); see the module
    docstring for the gap. The payload dies while the PART_A worker is RUNNING;
    the guardian's abnormal-exit path archives whichever S5-D1 artifact exists,
    the work is IN_DOUBT, no PART_A family exists, N2 stays COMMITTED, and a
    restart relaunches nothing."""
    if not getattr(real_boundary, 'part_a', False):
        pytest.skip('FP_QUALIFICATION_S5=1 required; the Part A /v7 installation')
    boundary = real_boundary
    attempt = committed_n2(boundary)
    dispatch(boundary, attempt, 'pawork', 'part_a_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: work(s, 'pawork')['state'] == 'RUNNING'
        and payload_identity_events(boundary, attempt, 'pawork'),
        seconds=120,
    )
    assert state['state'] == 'PART_A_READY'
    assert work(state, 'pawork')['state'] == 'RUNNING'
    _kill_payload_slice(boundary, attempt, 'pawork')
    state = wait(boundary, attempt, lambda s: work(s, 'pawork')['state'] == 'IN_DOUBT')
    assert work(state, 'pawork')['state'] == 'IN_DOUBT'
    assert state['state'] == 'PART_A_READY'
    assert part_a_family(state) is None
    assert (n2_family(state) or {}).get('state') == 'COMMITTED'
    works_before = sorted(w['work_id'] for w in state['works'])
    staged = staged_part_a(boundary, attempt)
    assert set(staged) <= PART_A_STAGED_ROLES, sorted(staged)
    if 'part_a_final' in staged:
        assert 'part_a_initial_prefix' in staged
        initial = staged['part_a_initial_prefix']
        assert staged['part_a_final'][: len(initial)] == initial
    boundary.restart()
    state = wait(boundary, attempt, lambda s: work(s, 'pawork')['state'] == 'IN_DOUBT')
    assert work(state, 'pawork')['state'] == 'IN_DOUBT'
    assert part_a_family(state) is None
    assert sorted(w['work_id'] for w in state['works']) == works_before
    assert staged_part_a(boundary, attempt) == staged


def test_s5_part_a_g5_unit_death_and_exact_receipt_retry(real_boundary):
    if not getattr(real_boundary, 'part_a', False):
        pytest.skip('FP_QUALIFICATION_S5=1 required; the Part A /v7 installation')
    boundary = real_boundary
    attempt = committed_n2(boundary)
    attested_part_a(boundary, attempt)
    dispatch_frozen = boundary.schedule(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': attempt,
            'work_id': 'pag5',
            'role': 'part_a_g5',
            'probe': 'noop',
            'signing_retry_of': None,
            'fault': 'hold_after_intent',
        }
    )
    assert dispatch_frozen['ok'], dispatch_frozen
    connection = _journal(boundary)
    try:
        row = None
        for _ in range(1200):
            row = connection.execute(
                'SELECT intent_bytes,candidate_bytes FROM full_campaign_checkpoint_intents '
                "WHERE attempt_id=? AND checkpoint='PART_A'",
                (attempt,),
            ).fetchone()
            if row is not None:
                break
            time.sleep(0.25)
    finally:
        connection.close()
    assert row is not None, 'the held PART_A intent never persisted'
    persisted_intent = json.loads(bytes(row[0]))
    from tools.qualification_verification.container_ownership import campaign_scopes

    unit = campaign_scopes(boundary.manifest['run_id'], attempt, 'pag5')['g5_unit']
    subprocess.run(
        ['systemctl', '--system', 'kill', '--signal=KILL', unit],
        check=False,
        capture_output=True,
        timeout=10,
    )
    state = wait(
        boundary, attempt, lambda s: work(s, 'pag5')['observation_bytes_b64'] is not None
    )
    assert work(state, 'pag5')['state'] == 'SIGNING_INTENT'
    retry = boundary.schedule(
        {
            'schema': 'qualification_campaign_schedule_request/v1',
            'attempt_id': attempt,
            'work_id': 'pag5retry',
            'role': 'part_a_g5',
            'probe': 'noop',
            'signing_retry_of': 'pag5',
            'fault': None,
        }
    )
    assert retry['ok'], retry
    state = wait(
        boundary, attempt, lambda s: s['state'] in ('FULL_PASS_READY', 'PART_A_FAILED')
    )
    assert state['state'] == 'FULL_PASS_READY'
    connection = _journal(boundary)
    try:
        receipt = connection.execute(
            'SELECT receipt_bytes FROM full_campaign_checkpoint_intents '
            "WHERE attempt_id=? AND checkpoint='PART_A'",
            (attempt,),
        ).fetchone()
    finally:
        connection.close()
    committed = json.loads(bytes(receipt[0]))
    assert committed['signing_at_utc'] == persisted_intent['signing_at_utc'], committed
    assert committed['campaign_state'] == 'FULL_PASS_READY'
