"""S2-G2 OS evidence on the enrolled S2 host: service-side metering.

Funded post-admission cancellation authentication (durably charged, kernel
guarded, one-use), the queued-cancellation barrier on new work, and the safe
exact-retry resume of an admission interrupted by service death. Runs before
test_campaign_supervision_linux.py (whose last case contaminates the common
memory group) and imports that file's helpers. Simulated counters and the
Windows tests are never a substitute for this file.
"""
import base64
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
import time
import pytest
from tools.qualification_verification import host
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_supervisor import work_enrollment, host_slice
from c1_rail.qualification.execution.protocol import sha256
try:
    from test_campaign_supervision_linux import admit, has_work, schedule_document, snapshot, wait, work
except ModuleNotFoundError:  # importlib mode: sibling test modules are not on sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from test_campaign_supervision_linux import admit, has_work, schedule_document, snapshot, wait, work

CHARGE = 2_000_000_000            # control_cpu_seconds + cpu_granularity_seconds
ADMISSION = 20_000_000_000        # installed orchestration bound, payload cpu 0
V2 = 'qualification_campaign_request/v2'


def journal(boundary, query, *parameters):
    with sqlite3.connect((boundary.root/'data/journal.sqlite').as_uri()+'?mode=ro', uri=True) as connection:
        return [tuple(row) for row in connection.execute(query, parameters)]


def funding(boundary, attempt):
    return json.loads(journal(boundary, 'SELECT body FROM full_campaign_funding WHERE attempt_id=?', attempt)[0][0])


def metering(doc):
    """The allowance facts; restart recovery legitimately appends accounting events (clock, revision, heads)."""
    return {k: doc[k] for k in ('settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns', 'validity', 'state')}


def status(boundary, attempt):
    return json.loads(boundary.request('STATUS', schema=V2, attempt_id=attempt))


def objects(boundary, attempt, prefix):
    return [row[0] for row in journal(boundary, 'SELECT role FROM full_campaign_objects WHERE attempt_id=? AND role GLOB ? ORDER BY role',
                                      attempt, prefix+'*')]


def approval_for(boundary, attempt, contract, reason):
    return boundary.admin('void-approval', '--attempt', attempt, '--contract', contract, '--reason', reason)


def forged(approval):
    """Well-formed approval whose signature was never made by the enrolled freeze key."""
    doc = json.loads(base64.b64decode(approval['operator_approval_bytes']))
    doc['signature']['value_b64'] = base64.b64encode(b'x'*64).decode()
    return dict(operator_approval_bytes=base64.b64encode(encoded(doc)).decode())


def void_fields(attempt, reason, approval):
    return dict(schema=V2, attempt_id=attempt, reason=reason, **approval)


def operator_void(boundary, fields):
    """uid 0 is the installed operator peer. Returns (reply, None) or (None, refusal text)."""
    try:
        return json.loads(boundary.request('VOID', role='administrator', **fields)), None
    except subprocess.CalledProcessError as exc:
        return None, exc.stderr or ''


def units(boundary):
    return host.run(['/usr/bin/systemctl', 'list-units', '--all', '--no-legend', '--plain', host_slice(boundary.root.name)[:-6]+'*'])


def unit_facts(unit):
    values = host.run(['/usr/bin/systemctl', 'show', unit, '--property=NRestarts,ActiveState,ExecMainStatus'])
    return dict(line.split('=', 1) for line in values.splitlines() if '=' in line)


def test_s2_post_admission_void_authentication_is_charged_per_attempt_and_never_forged(real_boundary):
    """Every signature check is preceded by one durable 2 s charge under the real guard; forgeries never set VOID."""
    boundary = real_boundary; attempt = admit(boundary)
    contract = status(boundary, attempt)['receipt']['contract_sha256']
    reason = 'TEST_ONLY metered cancellation'
    approval = approval_for(boundary, attempt, contract, reason)
    before = funding(boundary, attempt)
    assert before['settled_cpu_ns'] == ADMISSION and before['validity'] == 'VALID'
    frozen = snapshot(boundary, attempt)
    forged_fields = void_fields(attempt, reason, forged(approval))
    refusals = []
    for n in (1, 2, 3):
        reply, error = operator_void(boundary, forged_fields)
        assert reply is None and error, (reply, error)
        refusals.append(error[-300:])
        doc = funding(boundary, attempt)
        assert doc['settled_cpu_ns'] == before['settled_cpu_ns'] + n*CHARGE, doc
        assert doc['remaining_cpu_ns'] == before['remaining_cpu_ns'] - n*CHARGE
        assert doc['validity'] == 'VALID'
        current = status(boundary, attempt)
        assert current['validity'] == 'VALID' and current['void_pending'] is False
        assert current['void_authentication_attempts'] == n and current['void_refusal']
        assert current['settled_cpu_ns'] == doc['settled_cpu_ns']
    # The snapshot's per-work totals are untouched: the charge lives in the funding projection.
    assert snapshot(boundary, attempt) == frozen
    assert len(objects(boundary, attempt, 'void_authentication_')) == 3
    assert len(objects(boundary, attempt, 'void_refusal_')) == 3
    assert objects(boundary, attempt, 'pending_void') == []
    # A client-role peer is refused before the queue or any charge.
    with pytest.raises(subprocess.CalledProcessError) as peer:
        boundary.request('VOID', **void_fields(attempt, reason, approval))
    assert 'PEER_NOT_AUTHORIZED' in (peer.value.stderr or '')
    assert funding(boundary, attempt)['settled_cpu_ns'] == before['settled_cpu_ns'] + 3*CHARGE
    # The enrolled TEST_ONLY freeze key: one more charge, then VOID; the exact retry is free.
    valid = void_fields(attempt, reason, approval)
    receipt, error = operator_void(boundary, valid)
    assert error is None and receipt['validity'] == 'VOID', error
    doc = funding(boundary, attempt)
    assert doc['settled_cpu_ns'] == before['settled_cpu_ns'] + 4*CHARGE and doc['validity'] == 'VOID'
    again, error = operator_void(boundary, valid)
    assert error is None and again == receipt and funding(boundary, attempt) == doc
    assert len(objects(boundary, attempt, 'void_authentication_')) == 4 and objects(boundary, attempt, 'pending_void') == []
    boundary.restart()
    # Restart recovery of the completed works appends accounting events (run
    # 35471364817: revision 12 -> 15, later last_clock); the allowance is unchanged.
    assert metering(funding(boundary, attempt)) == metering(doc)
    final = status(boundary, attempt)
    assert final['validity'] == 'VOID' and final['void_authentication_attempts'] == 4
    assert final['settled_cpu_ns'] == doc['settled_cpu_ns']
    assert operator_void(boundary, valid)[0] == receipt
    assert metering(funding(boundary, attempt)) == metering(doc)
    host.save(boundary.output/(attempt+'-void-metering.json'), dict(before=before, after=doc, final=final, refusals=refusals,
        charges=objects(boundary, attempt, 'void_authentication_'), retained_refusals=objects(boundary, attempt, 'void_refusal_')))


def queue_during_admission(boundary, fields, void):
    """Submit and queue the operator body as soon as the campaign row exists.

    The transport queue is serialized behind the submit's dispatch lock, so the
    first accepted body lands right after the guardian launch, while the
    admission guardian is still running. The reply records which path took it.
    """
    replies = {}
    def submit():
        replies['submit'] = json.loads(boundary.request('SUBMIT_E1', **fields))
    worker = threading.Thread(target=submit); worker.start()
    deadline = time.monotonic()+90
    queued = None; errors = []
    while queued is None and time.monotonic() < deadline:
        reply, error = operator_void(boundary, void)
        if reply is not None:
            queued = reply
        else:
            errors.append(error[-200:])
            if fields['attempt_id'] not in error and 'metered history' not in error:
                raise AssertionError('unexpected refusal while queueing: '+error[-2000:])
    worker.join(180)
    assert queued is not None and not worker.is_alive(), errors[-3:]
    assert replies['submit']['schema'] == 'qualification_campaign_status/v2', replies
    return queued, replies['submit']


def test_s2_queued_cancellation_bars_new_work_while_admission_still_settles(real_boundary):
    """A queued body grants nothing, refuses the private route, and never blocks the admission's own charged tail."""
    boundary = real_boundary
    assert boundary.diagnostic
    evidence = {}
    # (a) Forged body queued before the receipt. While it is pending the private
    # route is barred outright (before any state check), with no bootstrap row,
    # no work and no unit. The guardian then refuses the body under its own
    # charged admission work: the refusal is retained, the body cleared, and the
    # admission completes normally with a receipt — validity stays VALID and no
    # authentication charge object exists.
    bundle = boundary.prepare(idle=True); attempt = bundle['attempt_id']
    fields = dict(schema=V2, request_id='diagnostic', attempt_id=attempt, bundle_sha256=bundle['bundle_sha256'])
    reason = 'TEST_ONLY queued cancellation'
    approval = approval_for(boundary, attempt, bundle['contract_sha256'], reason)
    queued, submitted = queue_during_admission(boundary, fields, void_fields(attempt, reason, forged(approval)))
    assert queued['schema'] == 'qualification_campaign_status/v2' and queued['void_pending'] is True, queued
    assert queued['void_authentication_attempts'] == 0 and queued['receipt'] is None
    refused = boundary.schedule(schedule_document(attempt, 'barred'))
    if refused['ok'] is False:
        assert 'cancellation pending' in refused['error'], refused
    else:
        # The receipt landed before the route request: the refusal must have
        # cleared the body by then, which the assertions below verify.
        assert json.loads(base64.b64decode(refused['data_b64']))['schema'] == 'qualification_campaign_status/v2', refused
    assert 'barred' not in units(boundary) or refused['ok'] is True
    state = wait(boundary, attempt, lambda s: work(s, 'admission')['state'] == 'COMPLETED' or s['state'].startswith('BUDGET_'))
    assert work(state, 'admission')['state'] == 'COMPLETED' and state['state'] == 'BOUND' and state['validity'] == 'VALID', state
    assert work(state, 'admission')['charge_cpu_ns'] == ADMISSION
    current = status(boundary, attempt)
    assert current['receipt'] is not None and current['void_pending'] is False and current['void_authentication_attempts'] == 0
    assert current['void_refusal'], current
    assert objects(boundary, attempt, 'void_admission_refusal_') == ['void_admission_refusal_000001']
    assert objects(boundary, attempt, 'void_authentication_') == [] and objects(boundary, attempt, 'pending_void') == []
    if refused['ok'] is False:
        assert journal(boundary, 'SELECT work_id FROM full_campaign_bootstraps WHERE attempt_id=?', attempt) == []
        assert not any(w['work_id'] == 'barred' for w in snapshot(boundary, attempt)['works'])
    # The same forged body after the receipt takes the funded path: one 2 s charge, still VALID.
    again, error = operator_void(boundary, void_fields(attempt, reason, forged(approval)))
    assert again is None and error, (again, error)
    after = status(boundary, attempt)
    assert after['validity'] == 'VALID' and after['void_authentication_attempts'] == 1 and after['void_pending'] is False
    assert funding(boundary, attempt)['settled_cpu_ns'] == ADMISSION + CHARGE
    evidence['forged'] = dict(queued=queued, submitted=submitted, refused=refused, receipt_state=state['state'],
                              refusal=current['void_refusal'], post_receipt_attempts=after['void_authentication_attempts'])
    # (b) Valid body queued before the receipt: authenticated by the guardian
    # under its own charged admission work; the admission settles, VOID is
    # recorded without a receipt, and nothing was charged to authentication.
    bundle = boundary.prepare(idle=True); attempt = bundle['attempt_id']
    fields = dict(schema=V2, request_id='diagnostic', attempt_id=attempt, bundle_sha256=bundle['bundle_sha256'])
    approval = approval_for(boundary, attempt, bundle['contract_sha256'], reason)
    queued, submitted = queue_during_admission(boundary, fields, void_fields(attempt, reason, approval))
    state = wait(boundary, attempt, lambda s: s['validity'] == 'VOID' or s['state'].startswith('BUDGET_') or work(s, 'admission')['state'] == 'COMPLETED')
    assert state['validity'] == 'VOID', state
    assert work(state, 'admission')['observation_bytes_b64'] is not None and work(state, 'admission')['charge_cpu_ns'] >= ADMISSION
    current = status(boundary, attempt)
    assert current['validity'] == 'VOID' and current['receipt'] is None and current['void_authentication_attempts'] == 0
    later = boundary.schedule(schedule_document(attempt, 'after'))
    assert later['ok'] is True and json.loads(base64.b64decode(later['data_b64']))['validity'] == 'VOID', later
    assert 'after' not in units(boundary)
    boundary.restart()
    assert status(boundary, attempt)['validity'] == 'VOID' and status(boundary, attempt)['void_authentication_attempts'] == 0
    evidence['valid'] = dict(queued=queued, submitted=submitted, state=state['state'], later=later)
    # (c) S2-G4 A1: a VOID queued after the campaign has terminalised is still
    # recordable. The started wall work is claimed by restart recovery (the
    # operator-ruled R2b shape): IN_DOUBT work, terminal-but-VALID campaign, and
    # the operator's body is then authenticated once UNCHARGED under the real
    # controller guard -- no allowance exists to charge, so no charge object is
    # minted and the allowance is unchanged by the authentication.
    bundle = boundary.prepare(idle=True); attempt = bundle['attempt_id']
    fields = dict(schema=V2, request_id='diagnostic', attempt_id=attempt, bundle_sha256=bundle['bundle_sha256'])
    submitted = json.loads(boundary.request('SUBMIT_E1', **fields))
    assert submitted['schema'] == 'qualification_campaign_status/v2', submitted
    state = wait(boundary, attempt, lambda s: work(s, 'admission')['state'] == 'COMPLETED')
    contract = status(boundary, attempt)['receipt']['contract_sha256']
    terminal_reason = 'TEST_ONLY terminal cancellation'
    scheduled = boundary.schedule(schedule_document(attempt, 'terminal', kind='wall'))
    assert scheduled['ok'], scheduled
    wait(boundary, attempt, lambda s: has_work(s, 'terminal') and work(s, 'terminal')['state'] == 'RUNNING')
    settled_before = funding(boundary, attempt)['settled_cpu_ns']
    boundary.restart()
    state = wait(boundary, attempt, lambda s: s['state'] == 'IN_DOUBT')
    assert state['validity'] == 'VALID' and work(state, 'terminal')['state'] == 'IN_DOUBT', state
    reply, error = operator_void(boundary, void_fields(attempt, terminal_reason,
        approval_for(boundary, attempt, contract, terminal_reason)))
    assert error is None and reply['validity'] == 'VOID', error
    assert objects(boundary, attempt, 'void_authentication_') == []      # uncharged: no charge object
    assert objects(boundary, attempt, 'pending_void') == []
    current = status(boundary, attempt)
    assert current['validity'] == 'VOID' and current['void_authentication_attempts'] == 0
    assert funding(boundary, attempt)['settled_cpu_ns'] == settled_before  # the terminal attempt costs nothing
    evidence['terminal'] = dict(state=state['state'], settled_before=settled_before,
        settled_after=funding(boundary, attempt)['settled_cpu_ns'],
        charges=objects(boundary, attempt, 'void_authentication_'))
    host.save(boundary.output/'s2-queued-cancellation.json', evidence)


def test_s2_admission_retry_after_service_death_never_double_starts(real_boundary):
    """Whatever state a service death leaves, the identical retry converges with at most one guardian start."""
    boundary = real_boundary
    assert boundary.diagnostic
    supervisor_unit = host_slice(boundary.root.name)[:-6]+'supervisor.service'
    samples = []
    for delay in (0.15, 0.4, 0.8):
        bundle = boundary.prepare(idle=True); attempt = bundle['attempt_id']
        fields = dict(schema=V2, request_id='diagnostic', attempt_id=attempt, bundle_sha256=bundle['bundle_sha256'])
        outcome = {}
        def submit():
            try:
                outcome['reply'] = json.loads(boundary.request('SUBMIT_E1', **fields))
            except subprocess.CalledProcessError as exc:
                outcome['error'] = (exc.stderr or '')[-500:]
        worker = threading.Thread(target=submit); worker.start()
        time.sleep(delay)
        # Freeze the supervisor mid-request, then kill it: the request never completes.
        host.run(['/usr/bin/systemctl', 'kill', '--signal=STOP', supervisor_unit])
        host.run(['/usr/bin/systemctl', 'kill', '--signal=KILL', supervisor_unit])
        worker.join(90)
        rows = journal(boundary, 'SELECT snapshot_bytes FROM full_campaign_budgets WHERE attempt_id=?', attempt)
        left = None if not rows else work(json.loads(rows[0][0]), 'admission')['state']
        boundary.restart()
        resent = json.loads(boundary.request('SUBMIT_E1', **fields))
        assert resent['schema'] == 'qualification_campaign_status/v2', resent
        final = wait(boundary, attempt, lambda s: work(s, 'admission')['state'] in ('COMPLETED', 'IN_DOUBT', 'ABORTED')
                     or s['state'] not in ('PROVISIONAL', 'BOUND'))
        assert not (final['state'] == 'PROVISIONAL' and work(final, 'admission')['state'] == 'RESERVED'), final
        dispatches = [r for r in final.get('dispatches', ()) if r['work_id'] == 'admission' and r['role'] == 'guardian']
        assert len(dispatches) <= 1
        owner = 'supervision_control_'+sha256(encoded(['admission', 'START_OWNER']))
        assert len(journal(boundary, 'SELECT 1 FROM full_campaign_objects WHERE attempt_id=? AND role=?', attempt, owner)) <= 1
        scopes = work_enrollment(boundary.root.name, attempt, 'admission')
        facts = unit_facts(scopes['guardian_unit'])
        assert facts.get('NRestarts', '0') == '0', facts
        # An exact retry after convergence is historical: no further start.
        assert json.loads(boundary.request('SUBMIT_E1', **fields))['schema'] == 'qualification_campaign_status/v2'
        assert len([r for r in snapshot(boundary, attempt).get('dispatches', ()) if r['work_id'] == 'admission']) == len(dispatches)
        samples.append(dict(delay=delay, interrupted_left=left, submit=outcome, resent_state=resent['state'],
                            final_state=final['state'], admission=work(final, 'admission')['state'],
                            dispatches=len(dispatches), guardian=facts))
    host.save(boundary.output/'s2-admission-retry-samples.json', samples)
