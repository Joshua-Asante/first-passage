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

(b) a genuine below-floor failure -> PART_A_FAILED, through the installed
    service path on the ``part_a_below_floor`` source scenario
    (fixture_producer.PART_A_BELOW_FLOOR_IDLE_DATES): the default ORB port
    stays flat on two source session dates that only Part A panel 1, path 0
    contains together, so N1 and the joint N2/Part B batch pass exactly as
    before (every N2 path passes; a path with one idle session still passes,
    on day 5) and the Part A p5 is 0.5 against the 0.95 floor. The decision is the installed
    adjudicator's own, reconstructed by G5 from genuinely computed outcomes.
    The above-FULL failure has no genuine witness on this fixture: at N2 depth
    60 the joint rule tolerates zero failures (max_certifying_busts(60, 0.05,
    0.05) == 0), so any campaign that reaches PART_A_READY carries a FULL
    baseline of exactly 1.0 and ``final_p5 > 1.0`` is unreachable. That
    decision stands on the adapter boundary test
    (tests/ops/qualification/execution/test_campaign_part_a.py).

(c) crash after the initial-prefix artifact is fsynced and before the final
    artifact -> IN_DOUBT with the initial prefix retained. The boundary host
    caps the work's output tmpfs at exactly one free inode (a host-side
    remount of the manager-created mount, applied before artifact creation:
    the test polls for the mount and asserts it is still empty with one free
    inode, so a late cap cannot pass falsely; no production seam; this is not
    evidence of SIGKILL or power-loss behavior). The worker's SR-4 writer then creates, writes,
    fsyncs and chmods the initial-prefix artifact as the last inode, and the
    final artifact's exclusive create is refused by the kernel (ENOSPC): the
    payload dies from that refusal after the prefix fsync and before any final
    artifact exists. This is deterministic synchronization by construction, not
    by timing. A host-side SIGSTOP or cgroup freeze cannot land in that window
    deterministically: on the non-expanding fixture nothing but in-memory work
    (two percentile reads and the result encoding) separates the two writes,
    and a host poller only sees the prefix once it exists.

(d) g5 death + exact retry: the held PART_A intent, the part_a_g5 unit
    asserted not active after T1 (under ``hold_after_intent`` the unit exits on
    its own right after the persisted intent, so a KILL may find nothing to
    kill; the unit's exit is asserted, not a successful kill), the
    SIGNING_INTENT work, an exact
    ``signing_retry_of`` that commits FULL_PASS_READY with the persisted
    intent's signing clock, the receipt bound to the original candidate bytes
    and the persisted intent, and a byte-identical historical receipt on a
    repeated committed retry.

No case constructs PartAMeasurementOverride (P-3).
"""

import base64
import hashlib
import json
import os
import sqlite3
import stat
import subprocess
import time
from decimal import Decimal
from pathlib import Path

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
from test_campaign_n2_linux import committed_n1, n2_family, stage_decisions
from tools.qualification_verification import host

PART_A_EXPORT_NAME = 'part_a_observations.json'
PART_A_EXPORT_SCHEMA = 'qualification_part_a_observations/v1'
# The two S5-D1 artifacts the guardian archives on a normal exit
# (ops/c1_rail/qualification/execution/campaign_supervisor.py:1889-1892
# PART_A_ARTIFACT_ROLES, staged at :1951-1954 under checkpoint PART_A).
PART_A_S5_D1_ROLES = {'part_a_initial_prefix', 'part_a_final'}
# The committing part_a_g5 stages every PART_A assessment output under the same
# checkpoint (ops/c1_rail/qualification/execution/g5.py:748-759 stages each role
# of evidence.output_bytes_by_role). Those roles are the ``outputs`` dict of
# build_part_a_checkpoint_evidence (ops/c1_rail/qualification/evidence.py:2944-2953,
# returned at :3023), checked by validate_output_roles (:2954-2960) against
# policy.required_output_roles (ops/c1_rail/qualification/policy.py:144-154):
# BASE_ARTIFACT_ROLES (:18) plus STAGE_ARTIFACT_ROLES (:16-17) for all five
# stages. For the full stage order the role set is the same for verdict PASS
# and FAIL (policy.py:151,154), so CONTINUE and FAILURE stage one set.
PART_A_G5_OUTPUT_ROLES = {
    'attempt_journal',
    'path_inventory',
    'runtime_load_trace',
    'legality_result',
    'n1_result',
    'n2_result',
    'part_b_result',
    'part_a_result',
}
PART_A_STAGED_ROLES = PART_A_S5_D1_ROLES | PART_A_G5_OUTPUT_ROLES
PART_A_INITIAL_ARTIFACT = 'part-a-initial.jsonl'
PART_A_FINAL_ARTIFACT = 'part-a-final.jsonl'
PART_A_BELOW_FLOOR_SCENARIO = 'part_a_below_floor'


def part_a_family(state):
    return (state.get('checkpoints') or {}).get('PART_A')


def _journal(boundary):
    return sqlite3.connect(
        (boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro', uri=True
    )


def _query(boundary, statement, parameters):
    connection = _journal(boundary)
    try:
        return connection.execute(statement, parameters).fetchall()
    finally:
        connection.close()


def staged_part_a(boundary, attempt):
    """Every artifact archived under checkpoint PART_A, role -> bytes
    (campaigns.stage_checkpoint_artifact): the S5-D1 artifacts and, once a
    part_a_g5 has staged them, its assessment outputs."""
    rows = _query(
        boundary,
        'SELECT role,body FROM full_campaign_checkpoint_staged '
        "WHERE attempt_id=? AND checkpoint='PART_A'",
        (attempt,),
    )
    staged = {}
    for role, body in rows:
        assert role not in staged, 'one archived artifact per PART_A role'
        staged[role] = bytes(body)
    return staged


def captured_part_a_payload(boundary, attempt):
    """The captured PART_A worker document exactly as archived."""
    rows = _query(
        boundary,
        'SELECT payload_bytes FROM full_campaign_checkpoint_captures '
        "WHERE attempt_id=? AND checkpoint='PART_A'",
        (attempt,),
    )
    assert rows, 'captured PART_A payload required'
    return json.loads(bytes(rows[0][0]))


def part_a_intent_row(boundary, attempt):
    """(intent_bytes, candidate_bytes, receipt_bytes) of the PART_A checkpoint, or None."""
    rows = _query(
        boundary,
        'SELECT intent_bytes,candidate_bytes,receipt_bytes FROM full_campaign_checkpoint_intents '
        "WHERE attempt_id=? AND checkpoint='PART_A'",
        (attempt,),
    )
    if not rows:
        return None
    intent, candidate, receipt = rows[0]
    return bytes(intent), bytes(candidate), None if receipt is None else bytes(receipt)


def retained_enrollment(boundary, attempt, work_id):
    """The guardian's retained supervision enrollment (campaigns.retain_supervision,
    role supervision_<work_id>), or None before the work is prepared."""
    rows = _query(
        boundary,
        'SELECT body FROM full_campaign_objects WHERE attempt_id=? AND role=?',
        (attempt, 'supervision_' + work_id),
    )
    return None if not rows else json.loads(bytes(rows[0][0]))


def _decoded(value):
    return json.loads(base64.b64decode(value))


def _transitions(row):
    return [_decoded(item)['state'] for item in row['transitions']]


def _sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def _prefix_panels(raw):
    """The S5-D1 artifact lines (execution/evidence.part_a_panel_bytes)."""
    return [json.loads(line) for line in raw.split(b'\n') if line]


def _admit(boundary, *, scenario):
    """Admission of a source-scenario bundle (test_campaign_n1_linux.admit
    takes the idle variant only); the same request and BOUND wait."""
    bundle = boundary.prepare(idle=False, scenario=scenario)
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


def _commit_n1(boundary, attempt):
    """The committed N1 receipt (campaign N2_READY) for an already admitted
    attempt: test_campaign_n2_linux.committed_n1's route, minus its admission."""
    dispatch(boundary, attempt, 'n1work', 'n1_worker')
    state = wait(
        boundary,
        attempt,
        lambda s: n2_family(s) is None
        and work(s, 'n1work')['state'] == 'COMPLETED'
        and (s.get('checkpoints') or {}).get('N1', {}).get('state') == 'ATTESTED',
    )
    assert work(state, 'n1work')['state'] == 'COMPLETED', state
    dispatch(boundary, attempt, 'g5work', 'n1_g5')
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'))
    assert state['state'] == 'N2_READY', state
    committing_g5_completed(boundary, attempt, 'N2_READY')


def committed_n2(boundary, *, scenario=None):
    """Admission through the committed joint N2/Part B receipt (campaign
    PART_A_READY): the S4 genuine joint pass, reused as this file's prelude.
    A source scenario admits its own bundle and takes the same route."""
    if scenario is None:
        attempt = committed_n1(boundary)
    else:
        attempt = _admit(boundary, scenario=scenario)
        _commit_n1(boundary, attempt)
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


def committed_part_a_decision(boundary, attempt, progression):
    """One part_a_g5 through the route to the named terminal progression; the
    committed family, the settled committing work and the custody assertions
    shared by the CONTINUE and FAILURE witnesses."""
    dispatch(boundary, attempt, 'pag5', 'part_a_g5')
    state = wait(
        boundary,
        attempt,
        lambda s: s['state'] in ('FULL_PASS_READY', 'PART_A_FAILED'),
        seconds=1080,
    )
    assert state['state'] == progression, state
    family = part_a_family(state)
    assert family['state'] == 'COMMITTED'
    assert family['decision'] == ('CONTINUE' if progression == 'FULL_PASS_READY' else 'FAILURE')
    committing_g5_completed(boundary, attempt, progression, work_id='pag5')
    # The archived PART_A set is exactly the S5-D1 artifacts plus the committing
    # g5's assessment outputs (module constants cite the production sources).
    from c1_rail.qualification.execution.campaign_supervisor import PART_A_ARTIFACT_ROLES
    from c1_rail.qualification.policy import BASE_ARTIFACT_ROLES, STAGE_ARTIFACT_ROLES

    assert PART_A_S5_D1_ROLES == set(PART_A_ARTIFACT_ROLES.values())
    assert PART_A_G5_OUTPUT_ROLES == set(BASE_ARTIFACT_ROLES) | set(STAGE_ARTIFACT_ROLES.values())
    payload_part_a = captured_part_a_payload(boundary, attempt)['part_a']
    staged = staged_part_a(boundary, attempt)
    assert set(staged) == PART_A_STAGED_ROLES, sorted(staged)
    # S5-D1 custody: both artifacts archived, the final a byte-extension of the
    # initial prefix, each bound to the payload's own digests; no expansion (F1).
    assert PART_A_S5_D1_ROLES <= set(staged), sorted(staged)
    initial = staged['part_a_initial_prefix']
    final = staged['part_a_final']
    assert final[: len(initial)] == initial
    assert _sha256(initial) == payload_part_a['initial_prefix_sha256']
    assert _sha256(final) == payload_part_a['final_sha256']
    assert payload_part_a['expansion_required'] is False
    assert payload_part_a['final_panels'] == payload_part_a['initial_panels'] == 2
    state = budget(boundary, attempt)
    finished = {w['work_id'] for w in completed_works(state)}
    assert finished >= {'admission', 'n1work', 'g5work', 'n2work', 'n2g5', 'pawork'}
    for row in completed_works(state):
        if row['work_id'] != 'admission':
            assert payload_identity_events(boundary, attempt, row['work_id']), row['work_id']
    return payload_part_a


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
    payload_part_a = committed_part_a_decision(boundary, attempt, 'FULL_PASS_READY')
    assert all(
        outcome['status'] == 'PASS'
        for panel in payload_part_a['panels']
        for outcome in panel['outcomes']
    ), payload_part_a['panels']
    exported = write_part_a_observations(boundary, attempt)
    assert exported['attempt_id'] == attempt


def test_s5_genuine_below_floor_part_a_is_part_a_failed(real_boundary):
    """Case (b): the ``part_a_below_floor`` source scenario through the whole
    installed route. N1 and the joint batch commit CONTINUE on the same
    adjudicators as the pass witness; the Part A decision is the installed
    below-floor FAILURE on genuinely computed outcomes (module docstring)."""
    if not getattr(real_boundary, 'part_a', False):
        pytest.skip('FP_QUALIFICATION_S5=1 required; the Part A /v7 installation')
    boundary = real_boundary
    attempt = committed_n2(boundary, scenario=PART_A_BELOW_FLOOR_SCENARIO)
    assert stage_decisions(boundary, attempt) == {'N2': 'PASS', 'PART_B': 'PASS'}
    attested_part_a(boundary, attempt)
    payload_part_a = committed_part_a_decision(boundary, attempt, 'PART_A_FAILED')
    # The designed outcome vector, computed by the worker and reconstructed by
    # G5: panel 0 passes on both paths, panel 1 fails exactly path 0 (the two
    # idle sessions leave three winning sessions, one short of the pass), so
    # the panel rates are 1.0 and 0.5 and p5 is 0.5.
    statuses = [
        [outcome['status'] for outcome in panel['outcomes']] for panel in payload_part_a['panels']
    ]
    assert statuses == [['PASS', 'PASS'], ['UNRESOLVED', 'PASS']], statuses
    assert payload_part_a['panels'][1]['outcomes'][0]['failure_reason'] == 'horizon_cap'
    # Panel 1, path 1 holds one idle session and passes on day 5; every other
    # passing path passes on day 4 exactly as the unmodified source does.
    days = [
        [outcome['sessions_to_pass'] for outcome in panel['outcomes']]
        for panel in payload_part_a['panels']
    ]
    assert days == [[4, 4], [None, 5]], days
    assert payload_part_a['initial_p5'] == payload_part_a['final_p5'] == 0.5
    assert payload_part_a['n2_full_baseline'] == {'passes': 60, 'paths': 60}
    intent, candidate, receipt = part_a_intent_row(boundary, attempt)
    assessment = json.loads(candidate)['part_a']
    comparison = assessment['floor_comparison']
    assert Decimal(comparison['final_p5']) == Decimal('0.5'), comparison
    assert Decimal(comparison['floor']) == Decimal('0.95'), comparison
    assert comparison['at_or_above'] is False, comparison
    assert assessment['full_sanity_comparison']['at_or_below'] is True, assessment
    assert assessment['tolerance_comparison']['within'] is False, assessment
    assert assessment['expansion_required'] is False
    committed = json.loads(receipt)
    assert committed['decision'] == 'FAILURE' and committed['campaign_state'] == 'PART_A_FAILED'
    assert committed['assessment_sha256'] == _sha256(candidate)
    assert committed['intent_sha256'] == _sha256(intent)
    host.save(
        boundary.output / (attempt + '-part-a-below-floor.json'),
        dict(scenario=PART_A_BELOW_FLOOR_SCENARIO, statuses=statuses, part_a=assessment,
             receipt=committed),
    )


def output_mount(boundary, attempt, work_id, seconds=120):
    """The work's output tmpfs (campaign_supervisor.checkpoint_io_paths of the
    retained enrollment), once the manager has mounted it."""
    from c1_rail.qualification.execution.campaign_supervisor import checkpoint_io_paths

    deadline = time.monotonic() + seconds
    out_path = None
    while time.monotonic() < deadline:
        if out_path is None:
            enrollment = retained_enrollment(boundary, attempt, work_id)
            if enrollment is not None:
                out_path = Path(checkpoint_io_paths(enrollment)['out_path'])
        if out_path is not None and os.path.ismount(out_path):
            return out_path
        time.sleep(0.002)
    raise AssertionError('the PART_A output mount never appeared')


def cap_output_mount_inodes(boundary, attempt, work_id):
    """Case (c)'s host-side condition: the output tmpfs keeps exactly one free
    inode. Applied to the manager-created mount before artifact creation: this
    polls for the mount and does not synchronize with container creation; the
    empty-mount and one-free-inode assertions below make a late cap fail
    rather than pass. The first exclusive create on the mount -- the SR-4 initial-prefix
    write -- succeeds and the second -- the final artifact -- is refused by the
    kernel with ENOSPC. Nothing in production changes."""
    out_path = output_mount(boundary, attempt, work_id)
    before = os.statvfs(out_path)
    assert before.f_files > 0, 'tmpfs inode accounting required'
    used = before.f_files - before.f_ffree
    remount = subprocess.run(
        ['/usr/bin/mount', '-o', 'remount,nr_inodes=%d' % (used + 1), str(out_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert remount.returncode == 0, remount.stderr
    after = os.statvfs(out_path)
    assert after.f_files == used + 1 and after.f_ffree == 1, (before, after)
    # The cap precedes every payload write: the mount is still empty.
    assert list(out_path.iterdir()) == [], list(out_path.iterdir())
    from test_campaign_supervision_linux import supervision_events

    return out_path, dict(
        out_path=str(out_path),
        inodes_before=dict(f_files=before.f_files, f_ffree=before.f_ffree),
        inodes_after=dict(f_files=after.f_files, f_ffree=after.f_ffree),
        container_events_at_cap=len(supervision_events(boundary, attempt, 'CONTAINER', work_id)),
    )


IO_LIVE_STATES = ('active', 'activating', 'deactivating', 'reloading')


def live_io_mounts():
    """Every checkpoint io mount unit the manager holds live, host-wide."""
    rows = subprocess.run(
        ['/usr/bin/systemctl', '--system', '--no-pager', '--no-legend', '--all', '--plain',
         'list-units', 'var-lib-fpq-*.mount'],
        capture_output=True, text=True, check=True, timeout=30,
    ).stdout.splitlines()
    return sorted(
        fields[0] for fields in (row.split() for row in rows)
        if len(fields) >= 3 and fields[2] in IO_LIVE_STATES
    )


def _unit_active_state(unit):
    """The manager's ActiveState; an unknown (collected) unit reads inactive."""
    result = subprocess.run(
        ['/usr/bin/systemctl', '--system', 'show', '--property=ActiveState', '--value', '--', unit],
        capture_output=True, text=True, check=False, timeout=30,
    )
    return result.stdout.strip() or 'absent'


def io_pair_released(boundary, attempt, work_id, seconds=60):
    """Fix card A1: the work's io tmpfs pair is inactive or absent once its
    guardian unit has ended (BindsTo), and neither path is still mounted.
    Bounded: the guardian exits shortly after its last store call."""
    from c1_rail.qualification.execution.campaign_supervisor import checkpoint_io_paths

    enrollment = retained_enrollment(boundary, attempt, work_id)
    assert enrollment is not None, work_id
    io = checkpoint_io_paths(enrollment)
    deadline = time.monotonic() + seconds
    while True:
        states = {unit: _unit_active_state(unit) for unit in (io['in_unit'], io['out_unit'])}
        mounted = [p for p in (io['in_path'], io['out_path']) if os.path.ismount(p)]
        if not mounted and not set(states.values()) & set(IO_LIVE_STATES):
            return dict(work_id=work_id, units=states)
        if time.monotonic() >= deadline:
            raise AssertionError(('io pair still live after the guardian', work_id, states, mounted))
        time.sleep(0.1)


def final_prefix(boundary, attempt, work_id, out_path, seconds=120):
    """Fix card A2: while the work is RUNNING, wait until the initial-prefix
    artifact is final -- mode 0444 (the SR-4 writer chmods only after its
    fsync) and the one-inode cap full -- so the host reads it from the live
    mount before the guardian settles and its pair is released."""
    prefix_path = out_path / PART_A_INITIAL_ARTIFACT
    deadline = time.monotonic() + seconds
    checked = 0.0
    while time.monotonic() < deadline:
        assert os.path.ismount(out_path), 'the output mount was released before the prefix read'
        try:
            final = (
                stat.S_IMODE(prefix_path.stat().st_mode) == 0o444
                and os.statvfs(out_path).f_ffree == 0
            )
        except FileNotFoundError:
            final = False
        if final:
            return prefix_path
        if time.monotonic() - checked >= 0.5:
            checked = time.monotonic()
            assert work(budget(boundary, attempt), work_id)['state'] == 'RUNNING'
        time.sleep(0.002)
    raise AssertionError('the PART_A initial prefix never became final')


def settled_in_doubt(boundary, attempt, work_id, seconds=1080):
    """The work IN_DOUBT with its settlement retained (the guardian's
    abnormal-exit path transitions and settles in two store calls)."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        state = budget(boundary, attempt)
        row = work(state, work_id)
        assert row['state'] != 'COMPLETED', row
        assert not {'CAPTURED', 'SIGNING_INTENT'} & set(_transitions(row)), _transitions(row)
        if row['state'] == 'IN_DOUBT' and row['observation_bytes_b64'] is not None:
            host.save(boundary.output / (attempt + '-part-a-in-doubt.json'), state)
            return state
        time.sleep(0.1)
    raise AssertionError('bounded PART_A settlement wait expired')


def test_s5_payload_death_between_the_part_a_writes_is_in_doubt_with_the_prefix_retained(
    real_boundary,
):
    """Case (c), deterministic by construction (module docstring): the payload
    dies after the initial-prefix artifact is written, fsynced and marked
    read-only, and before any final artifact exists. The guardian's
    abnormal-exit path archives exactly the initial prefix, the work is
    IN_DOUBT, the campaign ends IN_DOUBT from PART_A_READY with no PART_A
    family, N2 stays COMMITTED, nothing relaunches, and a restart preserves
    all of it."""
    if not getattr(real_boundary, 'part_a', False):
        pytest.skip('FP_QUALIFICATION_S5=1 required; the Part A /v7 installation')
    from test_campaign_supervision_linux import payload_exit_retained, supervision_events

    boundary = real_boundary
    attempt = committed_n2(boundary)
    dispatch(boundary, attempt, 'pawork', 'part_a_worker')
    out_path, cap = cap_output_mount_inodes(boundary, attempt, 'pawork')
    state = wait(
        boundary,
        attempt,
        lambda s: work(s, 'pawork')['state'] == 'RUNNING'
        and payload_identity_events(boundary, attempt, 'pawork'),
        seconds=120,
    )
    assert state['state'] == 'PART_A_READY'
    assert work(state, 'pawork')['state'] == 'RUNNING'
    # Fix card A2: the guardian's pair is released when its unit ends (A1), so
    # the host reads the output mount before settlement, once the prefix is
    # final. The mount holds exactly the fsynced prefix: the SR-4 writer chmods
    # 0444 only after its fsync, and the final artifact was never created.
    prefix_path = final_prefix(boundary, attempt, 'pawork', out_path)
    assert sorted(p.name for p in out_path.iterdir()) == [PART_A_INITIAL_ARTIFACT]
    assert stat.S_IMODE(prefix_path.stat().st_mode) == 0o444
    assert os.statvfs(out_path).f_ffree == 0
    host_prefix = prefix_path.read_bytes()
    panels = _prefix_panels(host_prefix)
    assert [panel['index'] for panel in panels] == [0, 1], panels
    assert all(len(panel['outcomes']) == 2 for panel in panels), panels
    assert not (out_path / PART_A_FINAL_ARTIFACT).exists()
    assert not (out_path / 'result.frame').exists()
    state = settled_in_doubt(boundary, attempt, 'pawork')
    row = work(state, 'pawork')
    assert row['state'] == 'IN_DOUBT'
    assert state['state'] == 'IN_DOUBT', state['state']
    assert part_a_family(state) is None
    assert (n2_family(state) or {}).get('state') == 'COMMITTED'
    assert not {'CAPTURED', 'SIGNING_INTENT', 'COMPLETED'} & set(_transitions(row)), _transitions(row)
    # Archived for inspection: the initial prefix only, byte-identical to what
    # the worker wrote; no part_a_final.
    staged = staged_part_a(boundary, attempt)
    assert set(staged) == {'part_a_initial_prefix'}, sorted(staged)
    assert staged['part_a_initial_prefix'] == host_prefix
    assert _sha256(staged['part_a_initial_prefix']) == _sha256(host_prefix)
    # The retained cause is the refused final create, after the prefix fsync.
    failures = [e['data']['reason'] for e in supervision_events(boundary, attempt, 'FAILURE', 'pawork')]
    assert len(failures) == 1, failures
    assert 'No space left on device' in failures[0] and PART_A_FINAL_ARTIFACT in failures[0], failures
    exit_facts = payload_exit_retained(boundary, attempt, 'pawork')
    assert exit_facts['exit_code'] != 0 and not exit_facts['oom_killed'], exit_facts
    # No relaunch: one container, one guardian dispatch, and no other PART_A work.
    assert len(supervision_events(boundary, attempt, 'CONTAINER', 'pawork')) == 1
    guardian_dispatches = [
        r for r in state.get('dispatches', ()) if r['work_id'] == 'pawork' and r['role'] == 'guardian'
    ]
    assert len(guardian_dispatches) == 1, guardian_dispatches
    assert [w['work_id'] for w in state['works'] if w['phase'] == 'PART_A'] == ['pawork']
    works_before = sorted((w['work_id'], w['state']) for w in state['works'])
    # Fix card A2 (added): the inspection copy is archived, so the work's io
    # pair is released with its guardian unit.
    released = io_pair_released(boundary, attempt, 'pawork')
    host.save(
        boundary.output / (attempt + '-part-a-prefix-crash.json'),
        dict(cap=cap, prefix_sha256=_sha256(host_prefix), prefix_panels=len(panels),
             failure=failures[0], payload_exit=exit_facts, campaign_state=state['state'],
             io_release=released),
    )
    boundary.restart()
    state = settled_in_doubt(boundary, attempt, 'pawork', seconds=120)
    assert work(state, 'pawork')['state'] == 'IN_DOUBT'
    assert state['state'] == 'IN_DOUBT'
    assert part_a_family(state) is None
    assert (n2_family(state) or {}).get('state') == 'COMMITTED'
    assert sorted((w['work_id'], w['state']) for w in state['works']) == works_before
    assert len(supervision_events(boundary, attempt, 'CONTAINER', 'pawork')) == 1
    assert staged_part_a(boundary, attempt) == staged
    assert not (out_path / PART_A_FINAL_ARTIFACT).exists()


def test_s5_part_a_g5_unit_death_and_exact_receipt_retry(real_boundary):
    """Case (d): the qg5 unit dies after T1 (the durable PART_A intent and
    candidate), before T2. A fresh retry unit redelivers the exact candidate,
    the commit completes with the persisted instant, the receipt binds the
    original candidate bytes and the persisted intent, and the exact wire retry
    returns the byte-identical historical receipt."""
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
    row = None
    for _ in range(1200):
        row = part_a_intent_row(boundary, attempt)
        if row is not None:
            break
        time.sleep(0.25)
    assert row is not None, 'the held PART_A intent never persisted'
    intent_bytes, original_candidate, receipt_bytes = row
    assert receipt_bytes is None, 'no receipt may exist mid-window'
    persisted_intent = json.loads(intent_bytes)
    assert persisted_intent['checkpoint'] == 'PART_A' and persisted_intent['work_id'] == 'pag5'
    assert persisted_intent['candidate_sha256'] == _sha256(original_candidate)
    from tools.qualification_verification.container_ownership import campaign_scopes

    unit = campaign_scopes(boundary.manifest['run_id'], attempt, 'pag5')['g5_unit']
    # The g5 unit exits on its own right after T1 under 'hold_after_intent'
    # (service.py returns after the persisted intent), so the kill may find no
    # running unit: its exit status is not the fact under test. What is
    # asserted is that the unit is not active afterwards -- exactly inactive,
    # failed, or no longer loaded by systemd.
    # The kill's return code is recorded as a fact (host.save below), not asserted.
    kill = subprocess.run(
        ['/usr/bin/systemctl', '--system', '--no-ask-password', 'kill', '--signal=KILL', unit],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    def unit_property(name):
        shown = subprocess.run(
            ['/usr/bin/systemctl', '--system', 'show', '-p', name, '--value', unit],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return shown.stdout.strip()

    active_state, load_state = unit_property('ActiveState'), unit_property('LoadState')
    assert load_state == 'not-found' or active_state in ('inactive', 'failed'), (
        unit, active_state, load_state,
    )
    state = wait(
        boundary, attempt, lambda s: work(s, 'pag5')['observation_bytes_b64'] is not None
    )
    assert work(state, 'pag5')['state'] == 'SIGNING_INTENT'
    assert state['state'] == 'PART_A_READY', state
    assert part_a_intent_row(boundary, attempt)[:2] == (intent_bytes, original_candidate)
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
    intent_after, candidate_after, receipt_bytes = part_a_intent_row(boundary, attempt)
    assert (intent_after, candidate_after) == (intent_bytes, original_candidate)
    assert receipt_bytes is not None
    committed = json.loads(receipt_bytes)
    assert committed['signing_at_utc'] == persisted_intent['signing_at_utc'], committed
    assert committed['campaign_state'] == 'FULL_PASS_READY' and committed['decision'] == 'CONTINUE'
    assert committed['checkpoint'] == 'PART_A'
    # Bound to the original candidate bytes and the persisted intent.
    assert committed['assessment_sha256'] == _sha256(original_candidate)
    assert committed['intent_sha256'] == _sha256(intent_bytes)
    family = part_a_family(state)
    assert family['state'] == 'COMMITTED' and family['decision'] == 'CONTINUE'
    assert family['assessment_sha256'] == _sha256(original_candidate)
    assert family['receipt_sha256'] == _sha256(receipt_bytes)
    # The exact wire retry as the qg5 peer returns the byte-identical receipt,
    # historical, with nothing re-signed.
    retry_reply = json.loads(
        boundary.request(
            'COMMIT_CHECKPOINT_ASSESSMENT',
            role='qg5',
            schema='qualification_campaign_request/v2',
            attempt_id=attempt,
            checkpoint='PART_A',
            work_id='pag5',
            candidate_bytes_b64=base64.b64encode(original_candidate).decode('ascii'),
            artifacts=[],
        )
    )
    assert retry_reply['receipt'] == committed and retry_reply['historical'] is True, retry_reply
    assert part_a_intent_row(boundary, attempt) == (intent_bytes, original_candidate, receipt_bytes)
    host.save(
        boundary.output / (attempt + '-part-a-g5-retry.json'),
        dict(unit=unit, kill_returncode=kill.returncode, intent=persisted_intent,
             candidate_sha256=_sha256(original_candidate), receipt=committed),
    )


def test_s5_io_mount_pairs_are_released_with_each_work_guardian(real_boundary):
    """Fix card test (4), QEXEC-01: on one attempt's multi-work sequence --
    N1 worker, N1 g5, N2 worker, N2 g5, Part A worker, Part A g5 -- the live
    var-lib-fpq-*.mount count never exceeds 2 x the worker works in flight
    (the sequence runs one worker work at a time and a g5 work creates no
    mount), and after each worker work settles its pair is inactive or
    absent. A background sampler reads the manager's unit table every 50 ms
    for the whole sequence."""
    if not getattr(real_boundary, 'part_a', False):
        pytest.skip('FP_QUALIFICATION_S5=1 required; the Part A /v7 installation')
    import threading

    boundary = real_boundary
    # Units a prior case left live (none expected) are outside this sequence.
    baseline = set(live_io_mounts())
    samples = []
    stop = threading.Event()
    failures = []

    def sample():
        while not stop.is_set():
            try:
                samples.append(len(set(live_io_mounts()) - baseline))
            except (OSError, subprocess.SubprocessError) as exc:  # retained, never swallowed
                failures.append(repr(exc))
            stop.wait(0.05)

    sampler = threading.Thread(target=sample, daemon=True)
    sampler.start()
    try:
        attempt = committed_n2(boundary)
        boundaries = []
        for work_id in ('n1work', 'n2work'):
            boundaries.append(io_pair_released(boundary, attempt, work_id))
        after_prefix = sorted(set(live_io_mounts()) - baseline)
        assert after_prefix == [], after_prefix
        attested_part_a(boundary, attempt)
        boundaries.append(io_pair_released(boundary, attempt, 'pawork'))
        committed_part_a_decision(boundary, attempt, 'FULL_PASS_READY')
        settled = sorted(set(live_io_mounts()) - baseline)
    finally:
        stop.set()
        sampler.join(timeout=30)
    assert not failures, failures
    assert samples, 'the io-mount sampler took no sample'
    # One worker work in flight at a time: at most one pair live.
    assert max(samples) <= 2, max(samples)
    assert settled == [], settled
    host.save(
        boundary.output / (attempt + '-io-release.json'),
        dict(baseline=sorted(baseline), samples=len(samples), max_live_io_mounts=max(samples),
             released=boundaries, settled_live_io_mounts=settled),
    )
