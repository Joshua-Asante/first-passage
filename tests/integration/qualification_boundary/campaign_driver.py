"""S8 synthetic campaign driver over the installed full-E1 route (TEST_ONLY).

The driver submits only registered bundle/attempt/request identities through the
authenticated service (qclient SUBMIT_E1/STATUS; the uid-0 operator peer for
VOID, REQUEST_SEAL and INSPECT_SEAL), dispatches fixed roles through the private
route, and reads durable custody read-only for evidence. It never supplies
outcomes, decisions, signatures or receipts: workers, G5 units and qseal
produce them. Route helpers are the accepted S3-S5 Linux helpers, imported
rather than copied.

The pure half (``plan``, ``terminal_state``, ``result_outcome``,
``accepted_prefix``, ``launch_counts``) derives the expected route from a
declared verdict and is portable. ``CampaignDriver`` needs the disposable
Linux host and its ``real_boundary``; its Linux-only imports are deferred.

Result and seal shapes are the frozen T05 ones (claude/t05-result-seal@6cf2732,
ledger "Coordinator checkpoint C-R"): tables ``full_campaign_result_intents`` /
``full_campaign_seal_intents``, receipts ``qualification_campaign_result_receipt/v1``
and ``qualification_campaign_seal_receipt/v1``, and the read-only
``qualification_campaign_seal_inspection/v1``.
"""
# Linux-only route helpers load at call time.
# pylint: disable=import-outside-toplevel
from __future__ import annotations

from dataclasses import dataclass
import json
import time

STAGE_ORDER = ('LEGALITY', 'N1', 'N2', 'PART_B', 'PART_A')
RESULT_RECEIPT_SCHEMA = 'qualification_campaign_result_receipt/v1'
SEAL_RECEIPT_SCHEMA = 'qualification_campaign_seal_receipt/v1'
SEAL_INSPECTION_SCHEMA = 'qualification_campaign_seal_inspection/v1'
RESULT_RECEIPT_FIELDS = frozenset({
    'schema', 'attempt_id', 'work_id', 'campaign_id', 'aggregate_sha256',
    'authentication_sha256', 'outcome', 'campaign_state', 'accepted_prefix',
    'campaign_revision', 'authority_head', 'budget', 'checkpoints', 'signing_at_utc',
    'committed_at_utc', 'intent_sha256'})
SEAL_RECEIPT_FIELDS = frozenset({
    'schema', 'attempt_id', 'work_id', 'campaign_id', 'intent_id', 'seal_sha256',
    'result_sha256', 'result_receipt_sha256', 'campaign_state', 'campaign_revision',
    'authority_head', 'signing_at_utc', 'committed_at_utc', 'intent_sha256'})
RESULT_WORK = ('rwork', 'result_g5')
SEAL_WORK = 'swork'
RESOURCE_TERMINAL = ('IN_DOUBT', 'ABORTED', 'BUDGET_EXHAUSTED', 'BUDGET_UNCERTAIN')
V2 = 'qualification_campaign_request/v2'


@dataclass(frozen=True)
class Step:
    """One checkpoint: its compute work, its committing G5 work, the stages its
    assessment decides, and the progression state each decision produces."""
    checkpoint: str
    compute: tuple[str, str]
    g5: tuple[str, str]
    stages: tuple[str, ...]
    passed: str
    failed: str


STEPS = (
    Step('N1', ('n1work', 'n1_worker'), ('g5work', 'n1_g5'), ('LEGALITY', 'N1'),
         'N2_READY', 'N1_FAILED'),
    Step('N2', ('n2work', 'n2_worker'), ('n2g5', 'n2_g5'), ('N2', 'PART_B'),
         'PART_A_READY', 'N2_FAILED'),
    Step('PART_A', ('pawork', 'part_a_worker'), ('pag5', 'part_a_g5'), ('PART_A',),
         'FULL_PASS_READY', 'PART_A_FAILED'),
)


def plan(stages):
    """The checkpoint steps a declared verdict runs, in order.

    The verdict must be a canonical legal prefix (policy.required_output_roles):
    LEGALITY/N1 failing at N1, LEGALITY..PART_B failing in the joint batch, or
    all five stages. LEGALITY is pass-only, nothing follows a failed checkpoint
    and nothing stops after a passing one.
    """
    if not isinstance(stages, dict) or any(v not in ('PASS', 'FAIL') for v in stages.values()):
        raise ValueError('closed PASS/FAIL stage statuses required')
    names = tuple(stages)
    if (names not in (STAGE_ORDER[:2], STAGE_ORDER[:4], STAGE_ORDER)
            or stages['LEGALITY'] != 'PASS'):
        raise ValueError('declared verdict is not a legal stage prefix')
    steps = tuple(step for step in STEPS if set(step.stages) <= set(names))
    if any('FAIL' in (stages[name] for name in step.stages) for step in steps[:-1]):
        raise ValueError('declared verdict continues after a failed checkpoint')
    if names != STAGE_ORDER and 'FAIL' not in (stages[name] for name in steps[-1].stages):
        raise ValueError('declared verdict stops after a passing checkpoint')
    return steps


def terminal_state(stages):
    """The progression state the route ends in."""
    last = plan(stages)[-1]
    return last.failed if 'FAIL' in (stages[name] for name in last.stages) else last.passed


def result_outcome(stages):
    """The authenticated result outcome the declared verdict commits."""
    plan(stages)
    return 'FAIL' if 'FAIL' in stages.values() else 'PASS'


def accepted_prefix(stages):
    """The result receipt's accepted stage prefix."""
    plan(stages)
    return list(stages)


def launch_counts(state):
    """Compute works per checkpoint phase in the durable ledger -- the launch
    history: a redraw would be a second work of the same phase."""
    counts = {step.checkpoint: 0 for step in STEPS}
    for row in state['works']:
        if row['phase'] in counts:
            counts[row['phase']] += 1
    return counts


def expected_launch_counts(stages):
    """One compute work per checkpoint the verdict runs, none after it stops."""
    ran = {step.checkpoint for step in plan(stages)}
    return {step.checkpoint: int(step.checkpoint in ran) for step in STEPS}


class CampaignDriver:
    """The installed route on one disposable host (``real_boundary``)."""

    def __init__(self, boundary):
        self.boundary = boundary
        self.bundles = {}

    # ---- admission ---------------------------------------------------------

    def prepare(self, name, *, depth_valid_seconds=14400):
        """Stage one signed TEST_ONLY bundle for a declared source scenario."""
        from uuid import uuid4
        import campaign_sources
        from tools.qualification_verification import host
        row = campaign_sources.scenario(name)
        boundary = self.boundary
        script = 'fixture_install_s8.py' if row.producer == 'derived' else 'fixture_install.py'
        command = [boundary.python, '-I',
                   str(boundary.code / 'tests/integration/qualification_boundary' / script),
                   'prepare', '--manifest', str(boundary.path), '--attempt', 'linux-' + uuid4().hex,
                   '--depth-valid-seconds', str(depth_valid_seconds)]
        if row.idle:
            command.append('--idle')
        elif row.idle_dates:
            command += ['--scenario', name]
        raw = host.run_owned(boundary.group, command, interpreter=boundary.python, timeout=180)
        return json.loads(raw)

    def admit(self, name, **kwargs):
        """SUBMIT_E1 through the client role, then the charged admission work."""
        bundle = self.prepare(name, **kwargs)
        attempt = bundle['attempt_id']
        first = json.loads(self.boundary.request('SUBMIT_E1', schema=V2, request_id='dispatch',
                                                 attempt_id=attempt,
                                                 bundle_sha256=bundle['bundle_sha256']))
        assert first['schema'] == 'qualification_campaign_status/v2', first
        state = self.until(attempt, lambda s: self.work(s, 'admission')['state'] == 'COMPLETED')
        assert state['state'] == 'BOUND', state
        self.bundles[attempt] = dict(bundle, scenario=name)
        self.save(attempt, 'bundle', self.bundles[attempt])
        return attempt

    def source_identity(self, attempt):
        """sha256 of the admitted ORB port, from the staged retained index."""
        index = self.boundary.root / 'keys/retained' / attempt / 'index.json'
        entries = json.loads(index.read_bytes())['entries']
        return next(row['sha256'] for row in entries if row['role'] == 'orb_runtime_port')

    # ---- reads -------------------------------------------------------------

    @staticmethod
    def work(state, work_id):
        """One work row of a ledger snapshot."""
        return next(row for row in state['works'] if row['work_id'] == work_id)

    def status(self, attempt, *, role='qclient'):
        """STATUS through the authenticated client."""
        return json.loads(self.boundary.request('STATUS', role=role, schema=V2,
                                                attempt_id=attempt))

    def ledger(self, attempt):
        """The durable budget snapshot (read-only)."""
        from test_campaign_n1_linux import budget
        return budget(self.boundary, attempt)

    def until(self, attempt, predicate, seconds=330):
        """The ledger once ``predicate`` holds or the campaign is resource-terminal."""
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            state = self.ledger(attempt)
            if predicate(state) or state['state'] in RESOURCE_TERMINAL:
                return state
            time.sleep(0.1)
        raise AssertionError('bounded S8 campaign wait expired')

    def settled(self, attempt, seconds=330):
        """The ledger once every work carries its settlement observation."""
        return self.until(attempt, lambda s: all(row['observation_bytes_b64'] is not None
                                                 for row in s['works']), seconds=seconds)

    def _select(self, statement, parameters):
        import sqlite3
        journal = (self.boundary.root / 'data/journal.sqlite').as_uri() + '?mode=ro'
        with sqlite3.connect(journal, uri=True) as connection:
            row = connection.execute(statement, parameters).fetchone()
        return None if row is None else tuple(None if v is None else bytes(v) for v in row)

    def result_row(self, attempt):
        """(intent, candidate, authentication, receipt) bytes of the result family, or None."""
        return self._select('SELECT intent_bytes,candidate_bytes,authentication_bytes,'
                            'receipt_bytes FROM full_campaign_result_intents WHERE attempt_id=?',
                            (attempt,))

    def seal_row(self, attempt):
        """(intent, signature, receipt) bytes of the seal family, or None."""
        return self._select('SELECT intent_bytes,signature_bytes,receipt_bytes '
                            'FROM full_campaign_seal_intents WHERE attempt_id=?', (attempt,))

    def checkpoint_row(self, attempt, checkpoint):
        """(intent, candidate, receipt) bytes of one checkpoint assessment, or None."""
        return self._select('SELECT intent_bytes,candidate_bytes,receipt_bytes '
                            'FROM full_campaign_checkpoint_intents '
                            'WHERE attempt_id=? AND checkpoint=?', (attempt, checkpoint))

    def stage_decisions(self, attempt, checkpoint):
        """The committed checkpoint assessment's stage split (the joint batch carries two)."""
        row = self.checkpoint_row(attempt, checkpoint)
        return None if row is None else json.loads(row[1]).get('stage_decisions')

    def save(self, attempt, name, value):
        """Retain one evidence document beside the boundary's own exports."""
        from tools.qualification_verification import host
        host.save(self.boundary.output / f'{attempt}-s8-{name}.json', value)

    # ---- route -------------------------------------------------------------

    def schedule(self, attempt, work_id, role, *, fault=None, signing_retry_of=None):
        """The raw private-route reply; a refusal is the caller's to interpret."""
        return self.boundary.schedule({
            'schema': 'qualification_campaign_schedule_request/v1', 'attempt_id': attempt,
            'work_id': work_id, 'role': role, 'probe': 'noop',
            'signing_retry_of': signing_retry_of, 'fault': fault})

    def dispatch(self, attempt, work_id, role, *, fault=None, signing_retry_of=None):
        """A scheduled work that must durably exist before anyone waits on it."""
        reply = self.schedule(attempt, work_id, role, fault=fault,
                              signing_retry_of=signing_retry_of)
        assert reply['ok'], reply
        state = self.until(attempt, lambda s: any(row['work_id'] == work_id
                                                  for row in s['works']), seconds=30)
        assert any(row['work_id'] == work_id for row in state['works']), 'refused ' + work_id
        return reply

    def run_step(self, attempt, step, seconds=1080):
        """One checkpoint: the compute work to ATTESTED/COMPLETED, then its G5
        work to the committed progression and the settled committing work."""
        from test_campaign_n1_linux import committing_g5_completed
        work_id, role = step.compute
        self.dispatch(attempt, work_id, role)

        def attested(state):
            family = (state.get('checkpoints') or {}).get(step.checkpoint) or {}
            return family.get('state') == 'ATTESTED' and \
                self.work(state, work_id)['state'] == 'COMPLETED'
        state = self.until(attempt, attested, seconds=seconds)
        assert self.work(state, work_id)['state'] == 'COMPLETED', state
        g5_id, g5_role = step.g5
        self.dispatch(attempt, g5_id, g5_role)
        state = self.until(attempt, lambda s: s['state'] in (step.passed, step.failed),
                           seconds=seconds)
        assert state['state'] in (step.passed, step.failed), state
        return committing_g5_completed(self.boundary, attempt, state['state'], work_id=g5_id)

    def run_to_terminal(self, attempt, stages):
        """Every checkpoint the declared verdict runs, stopping where the route stops."""
        state = None
        for step in plan(stages):
            state = self.run_step(attempt, step)
            if state['state'] == step.failed:
                break
        self.save(attempt, 'terminal-ledger', state)
        return state

    def commit_result(self, attempt, *, fault=None, work_id=RESULT_WORK[0],
                      signing_retry_of=None, seconds=330):
        """One result_g5 unit; the committed receipt, or None if none committed."""
        self.dispatch(attempt, work_id, RESULT_WORK[1], fault=fault,
                      signing_retry_of=signing_retry_of)
        if fault is not None:
            return None

        def finished(state):
            row = self.result_row(attempt)
            return (row is not None and row[3] is not None) or \
                self.work(state, work_id)['state'] in ('COMPLETED', 'IN_DOUBT', 'ABORTED')
        self.until(attempt, finished, seconds=seconds)
        row = self.result_row(attempt)
        receipt = None if row is None or row[3] is None else json.loads(row[3])
        self.save(attempt, 'result-receipt', receipt)
        return receipt

    def operator(self, operation, attempt, **fields):
        """(reply, None) or (None, refusal text) from the uid-0 operator peer."""
        import subprocess
        try:
            return json.loads(self.boundary.request(operation, role='administrator', schema=V2,
                                                    attempt_id=attempt, **fields)), None
        except subprocess.CalledProcessError as exc:
            return None, exc.stderr or ''

    def request_seal(self, attempt, *, label='seal-request'):
        """REQUEST_SEAL as the operator; ``label`` keeps concurrent evidence apart."""
        reply, error = self.operator('REQUEST_SEAL', attempt)
        self.save(attempt, label, {'reply': reply, 'error': error})
        return reply, error

    def inspect_seal(self, attempt):
        """INSPECT_SEAL: the historical receipt plus current validity/eligibility."""
        reply, error = self.operator('INSPECT_SEAL', attempt)
        assert error is None, error
        assert reply['schema'] == SEAL_INSPECTION_SCHEMA, reply
        self.save(attempt, 'seal-inspection', reply)
        return reply

    def void(self, attempt, reason):
        """An operator-approved VOID through the uid-0 peer: (reply, refusal)."""
        approval = self.boundary.admin('void-approval', '--attempt', attempt, '--contract',
                                       self.bundles[attempt]['contract_sha256'],
                                       '--reason', reason)
        return self.operator('VOID', attempt, reason=reason, **approval)
