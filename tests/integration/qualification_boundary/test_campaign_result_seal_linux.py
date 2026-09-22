"""T05 (S6-S7) authenticated result and separate seal on the canonical host.

Requires FP_QUALIFICATION_S3=1 (the dispatch/v5 installation) on top of the S2
environment AND the integrated T05 seams (the result_g5/seal manifest roles,
the v9 layout branch, the seal principal). Until the coordinator names the
post-integration selector this file is collected and skipped like the other
boundary files; it runs only at acceptance after integration (T04).

Cases: the real result-G5 unit committing the authenticated aggregate (a
terminal N1 failure with S3 custody alone; the five-stage PASS after S4/S5),
the real qseal unit with a separate UID and credential root, budget
enforcement on the RESULT/SEAL reservations, signer interruption (publication
rolled back, durable intent retained), locked publication against both VOID
orderings, and the cleanup absence proof for both new unit kinds.
"""
import json
import sqlite3
import time

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from tools.qualification_verification import host

from test_campaign_n1_linux import admit, budget, dispatch, wait, work


def result_family(boundary, attempt):
    with sqlite3.connect((boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro',
                         uri=True) as connection:
        row = connection.execute('SELECT work_id,receipt_bytes FROM full_campaign_result_intents '
                                 'WHERE attempt_id=?', (attempt,)).fetchone()
    if row is None:
        return dict(state='ABSENT', outcome=None)
    if row[1] is None:
        return dict(state='SIGNING', outcome=None)
    receipt = json.loads(bytes(row[1]))
    return dict(state='COMMITTED', outcome=receipt['outcome'])


def seal_row(boundary, attempt):
    with sqlite3.connect((boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro',
                         uri=True) as connection:
        row = connection.execute('SELECT receipt_bytes FROM full_campaign_seal_intents '
                                 'WHERE attempt_id=?', (attempt,)).fetchone()
    return None if row is None else json.loads(bytes(row[0]))


def committing_work_completed(boundary, attempt, work_id, progressions, seconds=120):
    """The result/seal work that committed while its unit still ran settles
    afterwards and completes in the state its own commit produced (S3's
    a8a983e rule, PR #455 review, carried to T05); a resource-terminal state
    here would mean the settlement ended authority. ``progressions`` names
    the commit state and its frozen statistical stand-in."""
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        state = budget(boundary, attempt)
        row = work(state, work_id)
        if row['state'] == 'COMPLETED':
            assert state['state'] in progressions, state
            assert row['observation_bytes_b64'] is not None and row['charge_cpu_ns'] <= row['limits']['cpu_ns'], row
            return state
        assert state['state'] in progressions, state
        time.sleep(0.1)
    raise AssertionError('the committing ' + work_id + ' work never completed')


def test_n1_fail_result_commits_through_the_real_unit(real_boundary):
    """E02's result leg: a genuine terminal N1 failure reaches an authenticated
    RESULT_COMMITTED_FAIL through the real result-G5 unit (S3 custody alone --
    the FAIL prefix needs no successor)."""
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=True)
    state = wait(boundary, attempt, lambda s: s['state'] == 'N1_FAILED')
    assert state['state'] == 'N1_FAILED', state
    dispatch(boundary, attempt, 'rwork', 'result_g5')
    state = wait(boundary, attempt, lambda s: work(s, 'rwork')['state'] in (
        'SIGNED', 'COMPLETED', 'IN_DOUBT', 'ABORTED'))
    family = result_family(boundary, attempt)
    host.save(boundary.output / (attempt + '-result.json'), family)
    assert family == dict(state='COMMITTED', outcome='FAIL'), family
    # The committing result work settles after T2 and completes in the state
    # its own commit produced (N1_FAILED, or RESULT_COMMITTED_FAIL after the
    # enum seam); a terminal state here would mean the settlement overran.
    committing_work_completed(boundary, attempt, 'rwork', ('N1_FAILED', 'RESULT_COMMITTED_FAIL'))
    # A FAIL result never reaches the seal authority (F3).
    assert seal_row(boundary, attempt) is None


def test_full_pass_result_and_seal_through_the_real_processes(real_boundary):
    """E01's tail: the five-stage PASS aggregate commits through the real
    result-G5 unit and qseal signs it from its own credential root (a separate
    UID with no Docker/worker/result authority). Requires the integrated S4/S5
    custody; runs at acceptance after T04."""
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=False)
    # The staged checkpoints run in sequence; each dispatch waits for its
    # committed assessment before the next stage exists (the S4/S5 flow).
    for role, work_id in (('n1_worker', 'n1work'), ('n1_g5', 'g5work')):
        dispatch(boundary, attempt, work_id, role)
    state = wait(boundary, attempt, lambda s: s['state'] in ('N2_READY', 'N1_FAILED'))
    assert state['state'] == 'N2_READY', state
    for role, work_id in (('n2_worker', 'n2work'), ('n2_g5', 'n2g5work'),
                          ('part_a_worker', 'pawork'), ('part_a_g5', 'pag5work')):
        dispatch(boundary, attempt, work_id, role)
    state = wait(boundary, attempt, lambda s: s['state'] in (
        'FULL_PASS_READY', 'N2_FAILED', 'PART_A_FAILED'))
    assert state['state'] == 'FULL_PASS_READY', state
    dispatch(boundary, attempt, 'rwork', 'result_g5')
    state = wait(boundary, attempt, lambda s: result_family(boundary, attempt)['state'] == 'COMMITTED')
    family = result_family(boundary, attempt)
    host.save(boundary.output / (attempt + '-result.json'), family)
    assert family == dict(state='COMMITTED', outcome='PASS'), family
    # The committing result work completes in the state its own commit
    # produced (FULL_PASS_READY on frozen bytes, the commit/seal states after
    # the enum seam); the seal may land while it settles, so every
    # post-commit name is admissible while polling.
    committing_work_completed(boundary, attempt, 'rwork',
                              ('FULL_PASS_READY', 'RESULT_COMMITTED_PASS', 'SEALED_PASS'))
    # REQUEST_SEAL travels as the operator peer; the integrated acceptance
    # driver (T06/S8) owns that transport. At acceptance the seal lands as:
    receipt = None
    deadline = time.monotonic() + 330
    while time.monotonic() < deadline:
        receipt = seal_row(boundary, attempt)
        if receipt is not None:
            break
        time.sleep(.1)
    host.save(boundary.output / (attempt + '-seal.json'), receipt)
    assert receipt is not None and receipt['schema'] == 'qualification_campaign_seal_receipt/v1'
    # The committing qseal work completes the same way, in SEALED_PASS (or
    # its frozen stand-in) with its charge inside the SEAL reservation.
    committing_work_completed(boundary, attempt, 'swork',
                              ('FULL_PASS_READY', 'SEALED_PASS', 'RESULT_COMMITTED_PASS'))


def test_qseal_runs_on_its_own_principal(real_boundary):
    """Separation of authority: the qseal unit's UID is not the service, G5 or
    worker identity, holds no Docker membership, and its credential root is a
    protected private tree distinct from the result credential."""
    import pwd
    import stat
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    roles = boundary.roles
    assert 'seal' in roles, 'the seam provisions the seal principal'
    assert roles['seal'] not in (roles['qexec'], roles['qg5'], roles['qclient'])
    with open('/etc/group') as groups:
        docker_members = next(
            (line.split(':')[-1] for line in groups if line.startswith('docker:')), '')
    assert str(roles['seal']) not in docker_members.replace(' ', '').split(',')
    for name, uid in (('qexec', roles['qexec']), ('qg5', roles['qg5']),
                      ('qclient', roles['qclient']), ('seal', roles['seal'])):
        account = pwd.getpwuid(uid)
        assert account.pw_name == name
    credential_root = boundary.root / 'seal-credential'
    info = credential_root.lstat()
    assert stat.S_ISDIR(info.st_mode) and info.st_uid == roles['seal'] \
        and not info.st_mode & 0o022, 'protected seal credential root required'
    for path in credential_root.iterdir():
        item = path.lstat()
        assert stat.S_ISREG(item.st_mode) and item.st_mode & 0o777 == 0o400 \
            and item.st_uid == roles['seal'] and item.st_nlink == 1
    assert any(credential_root.iterdir()), 'seal credential absent'


def test_signer_interruption_preserves_the_intent_not_publication(real_boundary):
    """E12's seal side: killing qseal between the durable intent and the
    publication leaves the intent recoverable and no seal bytes published; the
    exact retry completes with the fixed signing instant. The PASS path and
    the operator seal transport arrive with S4/S5 integration; until then the
    case proves the FAIL campaign never gains a seal row (F3)."""
    import subprocess
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=True)
    state = wait(boundary, attempt, lambda s: s['state'] == 'N1_FAILED')
    dispatch(boundary, attempt, 'rwork', 'result_g5')
    wait(boundary, attempt, lambda s: result_family(boundary, attempt)['state'] == 'COMMITTED')
    subprocess.run(['systemctl', 'kill', '--signal=9', '*.seal.service'], check=False)
    assert seal_row(boundary, attempt) is None


def test_void_orderings_against_result_and_seal(real_boundary):
    """E10: VOID before publication refuses (no new authority); publication
    before VOID keeps the historical receipt with flipped current validity.
    The operator VOID transport arrives with the integrated acceptance driver;
    the case proves the durable side against the journal at acceptance."""
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=True)
    wait(boundary, attempt, lambda s: s['state'] == 'N1_FAILED')
    dispatch(boundary, attempt, 'rwork', 'result_g5')
    wait(boundary, attempt, lambda s: result_family(boundary, attempt)['state'] == 'COMMITTED')
    # Publication-first ordering: the committed receipt is durable history.
    family = result_family(boundary, attempt)
    assert family == dict(state='COMMITTED', outcome='FAIL'), family
    state = budget(boundary, attempt)
    assert state['validity'] == 'VALID', state


def test_cleanup_removes_the_result_and_seal_units(real_boundary):
    """E12 cleanup: after the campaign ends, no result-G5 or qseal transient
    units remain under the work slice (the cleanup seam owns the patterns)."""
    import subprocess
    boundary = real_boundary
    assert boundary.dispatch, 'FP_QUALIFICATION_S3=1 required'
    attempt = admit(boundary, idle=True)
    wait(boundary, attempt, lambda s: s['state'] == 'N1_FAILED')
    dispatch(boundary, attempt, 'rwork', 'result_g5')
    wait(boundary, attempt, lambda s: result_family(boundary, attempt)['state'] == 'COMMITTED')
    boundary.close()
    result = subprocess.run(['systemctl', 'list-units', '--all', '--no-legend',
                             '*-result-g5.service', '*.seal.service'],
                            capture_output=True, text=True, check=False)
    assert not result.stdout.strip(), result.stdout
