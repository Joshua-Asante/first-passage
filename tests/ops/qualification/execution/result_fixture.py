"""T05 S6 fixtures: the synthetic committed-checkpoint predecessors and the
F1 service double.

The real S3 scene (test_campaign_n1's helpers, imported -- never edited) runs
a genuine N1 to its committed assessment. On frozen bytes only that N1 custody
exists; the F3 successors (the joint N2 batch, PART_A) are fixture-built rows
labelled ``synthetic_predecessor=True`` in every record, overlaid on the real
custody read by ``OverlayResultStore``. At integration S4/S5's real custody
replaces the overlay (the C-R seam table names this row).

The double supplies the real ``threading.Lock`` (the service instance's own
``dispatch_lock``), the real ``CampaignStore`` and the real ``ResultStore`` on
a journal mounted at the T05 v9 layout, and owns re-validation between T1 and
T2 exactly as ``service._commit_checkpoint`` does for N1.
"""
import base64
import json

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution import campaign_supervisor as supervisor
from c1_rail.qualification.execution import campaign_result
from c1_rail.qualification.execution.campaign_result import ResultStore
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.protocol import sha256

from test_contract import NOW
import test_campaign_n1 as n1

G5_UID = 1002
SYNTHETIC_ASSESSMENT_SCHEMA = 'qualification_synthetic_predecessor_assessment/v1'
SYNTHETIC_RECEIPT_SCHEMA = 'qualification_synthetic_predecessor_receipt/v1'


def result_context(double, attempt_id):
    """The enrollment context, built exactly as CampaignStore.context does
    (verify_retained_bundle + the admission-receipt binding) minus the status
    leg that refuses metered campaigns at this revision (S3 seam finding:
    full_campaigns.receipt_bytes keeps the provisional intent after
    admission, so status() raises; the C-R return lists it)."""
    from c1_rail.qualification.execution.admission import verify_retained_bundle
    campaigns = double.campaigns
    objects = campaigns.objects(attempt_id)
    retained = {role.removeprefix('context_'): raw for role, raw in objects.items()
                if role.startswith('context_')}
    context = verify_retained_bundle(objects['bundle_index'], retained,
                                     double.instance.release, double.keys(), NOW)
    receipt = json.loads(objects['diagnostic_receipt'])
    if context.bundle_sha256 != receipt['bundle_sha256'] or context.attempt_id != attempt_id:
        raise ValueError('retained campaign context differs')
    return context


def committed_n1(tmp_path, monkeypatch, *, decision='CONTINUE'):
    """The real S3 scene to a committed N1 assessment (never edited, only
    driven): genuine capture, attestation, intent and commit, then the
    guardian's settlement tail for the assessing work (still in the
    v8 world, exactly as _run_n1_g5 ends the unit).

    The S3 builders carry placeholder signature values (the C1 disclosure);
    the wrappers below sign the same envelopes with the fixture's enrolled
    keys so the real verifier paths (verify_checkpoint_attestation and
    verify_checkpoint_assessment) run on Windows too."""
    def signed_attestation(original):
        def build(instance, result, payload):
            document = json.loads(original(instance, result, payload))
            signature = instance.case['private']['test-execution'].sign(
                encoded(document['payload']))
            document['signature'] = dict(algorithm='Ed25519', key_id='test-execution',
                value_b64=base64.b64encode(signature).decode('ascii'))
            return encoded(document)
        return build

    def signed_candidate(original):
        def build(instance, decision='CONTINUE', revision=None):
            document = json.loads(original(instance, decision=decision,
                                           revision=revision))
            core = {name: value for name, value in document.items() if name != 'signature'}
            signature = instance.case['private']['test-producer'].sign(encoded(core))
            document['signature'] = dict(algorithm='Ed25519', key_id='test-producer',
                value_b64=base64.b64encode(signature).decode('ascii'))
            return encoded(document)
        return build

    monkeypatch.setattr(n1, 'attestation_document',
                        signed_attestation(n1.attestation_document))
    monkeypatch.setattr(n1, 'candidate_document', signed_candidate(n1.candidate_document))
    instance = n1.g5_claimed(tmp_path, monkeypatch)
    candidate = n1.persisted_intent(
        instance, n1.candidate_document(instance, decision=decision))
    response = json.loads(n1.commit(instance, candidate))
    assert response['receipt'] is not None
    # The guardian's durable tail: settlement works post-terminal; the S3
    # COMPLETED gate refuses terminal campaigns (a C-R finding -- S3's own
    # _run_n1_g5 tail has the same wrinkle on Linux).
    n1.settle(instance, 'g5work')
    return instance, candidate


def synthetic_checkpoint(attempt_id, campaign_id, checkpoint, *, fail=False):
    """One F3 successor custody row with its synthetic documents.

    Every record carries ``synthetic_predecessor=True``. The joint N2 batch's
    stage rows put the batch's single joint decision on its final stage (the
    aggregate prefix represents the batch, the assessment carries the split).
    """
    stages = campaign_result.CHECKPOINT_STAGES[checkpoint]
    status = 'FAIL' if fail else 'PASS'
    stage_rows = [dict(stage=name, status='PASS') for name in stages[:-1]] + [
        dict(stage=stages[-1], status=status)]
    decision = ('FAILURE' if fail else 'CONTINUE') if checkpoint == 'N1' else (
        'FAIL' if fail else 'PASS')
    assessment = encoded(dict(schema=SYNTHETIC_ASSESSMENT_SCHEMA, attempt_id=attempt_id,
        checkpoint=checkpoint, work_id='synthetic-' + checkpoint.lower(),
        decision=decision, stages=stage_rows, synthetic_predecessor=True))
    cutoff = encoded(dict(schema='qualification_campaign_cutoff_receipt/v1',
        attempt_id=attempt_id, checkpoint=checkpoint, assessment_sha256=sha256(assessment),
        decision=decision, synthetic_predecessor=True))
    receipt = encoded(dict(schema=SYNTHETIC_RECEIPT_SCHEMA, attempt_id=attempt_id,
        checkpoint=checkpoint, assessment_sha256=sha256(assessment),
        cutoff_sha256=sha256(cutoff), decision=decision, synthetic_predecessor=True))
    result_bytes = encoded(dict(schema=SYNTHETIC_ASSESSMENT_SCHEMA,
        kind='checkpoint_result', checkpoint=checkpoint, synthetic_predecessor=True))
    payload_bytes = encoded(dict(schema=SYNTHETIC_ASSESSMENT_SCHEMA,
        kind='checkpoint_payload', checkpoint=checkpoint, synthetic_predecessor=True))
    attestation = encoded(dict(schema=SYNTHETIC_ASSESSMENT_SCHEMA,
        kind='checkpoint_attestation', checkpoint=checkpoint, synthetic_predecessor=True))
    row = dict(attempt_id=attempt_id, campaign_id=campaign_id, checkpoint=checkpoint,
        work_id='synthetic-' + checkpoint.lower(), decision=decision, stages=stage_rows,
        result_sha256=sha256(result_bytes), payload_sha256=sha256(payload_bytes),
        attestation_sha256=sha256(attestation), assessment_sha256=sha256(assessment),
        cutoff_sha256=sha256(cutoff), receipt_sha256=sha256(receipt),
        assessment_bytes=assessment, cutoff_bytes=cutoff, receipt_bytes=receipt,
        synthetic_predecessor=True)
    artifacts = dict(result=result_bytes, payload=payload_bytes)
    return row, artifacts, attestation


def synthetic_predecessors(attempt_id, campaign_id, *, through='PART_A', fail_at=None):
    """Ordered synthetic rows after the real N1: through='N2' appends the joint
    batch, through='PART_A' appends both successors; ``fail_at`` names the
    checkpoint whose batch fails."""
    order = campaign_result.CHECKPOINTS[1:]
    limit = order.index(through) + 1 if through in order else 0
    rows, artifacts, attestations = [], {}, {}
    for checkpoint in order[:limit]:
        row, capture, attestation = synthetic_checkpoint(
            attempt_id, campaign_id, checkpoint, fail=(checkpoint == fail_at))
        rows.append(row)
        artifacts[checkpoint] = capture
        attestations[checkpoint] = attestation
    return rows, artifacts, attestations


class OverlayResultStore(ResultStore):
    """The closed accessor with the fixture's synthetic successor rows layered
    after the real N1 custody (ordered; the builder still validates shape)."""

    def __init__(self, campaigns, synthetic_rows=()):
        super().__init__(campaigns)
        self.synthetic_rows = list(synthetic_rows)

    def _checkpoint_receipts(self, connection, attempt_id):
        return super()._checkpoint_receipts(connection, attempt_id) + [
            campaign_result.parse_receipt_row(dict(row)) for row in self.synthetic_rows]


class ResultServiceDouble:
    """The F1 service double: the real lock, store and re-validation between
    T1 and T2; dispatches the two S6 operations (the service seam's stand-in)."""

    def __init__(self, instance, *, synthetic_rows=(), synthetic_artifacts=None,
                 synthetic_attestations=None):
        self.instance = instance
        self.campaigns = CampaignStore(instance.store)
        self.results = OverlayResultStore(self.campaigns, synthetic_rows)
        self.synthetic_artifacts = dict(synthetic_artifacts or {})
        self.synthetic_attestations = dict(synthetic_attestations or {})

    @property
    def dispatch_lock(self):
        return self.instance.dispatch_lock

    def seal_enrollment_context(self, attempt_id):
        """The S7 signing phase's enrollment context (seam #19: S3's
        CampaignStore.context refuses metered campaigns at this revision;
        removed at integration)."""
        return result_context(self, attempt_id)

    def keys(self):
        return self.instance.keys()

    def custody(self, attempt_id):
        """Attestations and capture artifacts for every custody row: the real
        N1 bytes from S3 custody, the synthetic successors from the fixture."""
        rows = self.results.checkpoint_receipts(attempt_id)
        attestations, artifacts = {}, {}
        for row in rows:
            if row['checkpoint'] == 'N1':
                capture = self.campaigns.checkpoint_capture(attempt_id)
                attestations['N1'] = capture['attestation_bytes']
                artifacts['N1'] = dict(result=capture['result_bytes'],
                                       payload=capture['payload_bytes'])
            else:
                attestations[row['checkpoint']] = self.synthetic_attestations[row['checkpoint']]
                artifacts[row['checkpoint']] = self.synthetic_artifacts[row['checkpoint']]
        return rows, attestations, artifacts

    def handle_result_request(self, peer_uid, raw):
        from c1_rail.qualification.execution.protocol import decode_base64
        request = campaign_result.parse_result_operation(raw)
        if peer_uid != G5_UID:
            raise ValueError('PEER_NOT_AUTHORIZED')
        attempt = request['attempt_id']
        if request['operation'] == 'RESULT_SNAPSHOT':
            return self.results.result_snapshot(attempt)
        staged = self.staged_authentication(attempt, request['authentication_sha256'])
        return self._commit_result(attempt, request, staged)

    def staged_authentication(self, attempt_id, authentication_sha256):
        """The privately staged authentication envelope (role
        result_authentication), fetched by digest exactly as the seam will."""
        with self.instance.store.transaction() as connection:
            row = connection.execute(
                "SELECT body FROM full_campaign_checkpoint_staged "
                "WHERE attempt_id=? AND role='result_authentication' AND sha256=?",
                (attempt_id, authentication_sha256)).fetchone()
        if row is None:
            raise ValueError('staged result authentication membership differs')
        return bytes(row[0])

    def _commit_result(self, attempt, request, authentication_bytes):
        from c1_rail.qualification.execution.g5_result import verify_result_authentication
        from c1_rail.qualification.execution.store import instant
        candidate_bytes = n1_store_decode(request['candidate_bytes_b64'])
        with self.dispatch_lock:
            with self.instance.store.transaction() as connection:
                prior = connection.execute(
                    'SELECT candidate_bytes FROM full_campaign_result_intents WHERE attempt_id=?',
                    (attempt,)).fetchone()
            if prior is not None and bytes(prior[0]) != candidate_bytes:
                raise ValueError('exact result candidate retry required')
            if prior is None:
                snapshot_bytes = self.results.result_snapshot(attempt)
                authentication = campaign_result.ResultStore._parse_authentication(
                    authentication_bytes, attempt_id=attempt)
                intent_bytes = encoded(dict(
                    schema=campaign_result.RESULT_INTENT_SCHEMA, attempt_id=attempt,
                    work_id=request['work_id'],
                    key_id=authentication['signature']['key_id'],
                    signing_at_utc=instant(NOW), candidate_sha256=sha256(candidate_bytes),
                    snapshot_sha256=sha256(snapshot_bytes)))
                self.results.persist_result_intent(
                    attempt, request['work_id'], snapshot_bytes, intent_bytes,
                    candidate_bytes, expected_revision=request['expected_revision'])
            # T2's own re-validation window: the service verifies the staged
            # signature and re-validates the candidate against its own context.
            context = result_context(self, attempt)
            keys = self.keys()
            verify_result_authentication(authentication_bytes, context=context,
                                         current_keys=keys)
            rows, attestations, artifacts = self.custody(attempt)
            snapshot_bytes = self.persisted_snapshot(attempt)
            validated = campaign_result.validate_campaign_result(
                context, candidate_bytes, attestations=attestations, artifacts=artifacts,
                assessment_receipts=rows, snapshot_bytes=snapshot_bytes, current_keys=keys)
            return self.results.commit_campaign_result(
                attempt, request['work_id'], validated, authentication_bytes, now=NOW)

    def persisted_snapshot(self, attempt_id):
        with self.instance.store.transaction() as connection:
            row = connection.execute('SELECT snapshot_bytes FROM full_campaign_result_intents '
                                     'WHERE attempt_id=?', (attempt_id,)).fetchone()
        if row is None:
            raise ValueError('persisted result intent absent')
        return bytes(row[0])


def n1_store_decode(value_b64):
    from c1_rail.qualification.execution.protocol import decode_base64
    return decode_base64(value_b64)


def scene(tmp_path, monkeypatch, *, n1_decision='CONTINUE', through=None, fail_at=None,
          work='rwork'):
    """A full S6 scene: the real committed N1, the v9 mount, the synthetic
    successors, the reserved+running+identified RESULT work, and the double.
    ``through``/``fail_at`` shape the aggregate the scene can commit:
    through=None -- only the real N1 (FAIL after LEGALITY/N1);
    through='N2' with fail_at='N2' -- FAIL after the joint batch;
    through='PART_A' with fail_at='PART_A' -- FAIL after all five;
    through='PART_A', fail_at=None -- the all-stage PASS (requires n1 PASS)."""
    instance, candidate = committed_n1(tmp_path, monkeypatch, decision=n1_decision)
    attempt = instance.attempt
    campaign_id = CampaignStore(instance.store).row(attempt)['campaign_id']
    synthetic_rows, artifacts, attestations = ([], {}, {})
    if through is not None:
        synthetic_rows, artifacts, attestations = synthetic_predecessors(
            attempt, campaign_id, through=through, fail_at=fail_at)
    double = ResultServiceDouble(instance, synthetic_rows=synthetic_rows,
                                 synthetic_artifacts=artifacts,
                                 synthetic_attestations=attestations)
    results = double.results
    state = json.loads(results.result_state_bytes(attempt))
    profile = state['profile']
    clock_doc = json.loads(supervisor.observe_campaign_clock())
    reservation = encoded(dict(limits=profile['phases']['RESULT'], clock=clock_doc,
                               input_sha256=sha256(b'result-aggregate-input')))
    scopes = supervisor.work_enrollment('host1', attempt, work)
    start = encoded(dict(schema='qualification_campaign_work_transition/v1',
        attempt_id=attempt, work_id=work, state='START_INTENT', clock=clock_doc,
        data=dict(campaign_scope_id=scopes['campaign_slice'],
                  work_scope_id=scopes['payload_slice'])))
    results.reserve_result_work(attempt, work, reservation,
                                expected_revision=state['authority_revision'],
                                start_transition_bytes=start)
    results.retain_result_enrollment(encoded(dict(
        schema='qualification_campaign_supervision/v1', host_run_id='host1',
        attempt_id=attempt, work_id=work,
        manifest_bytes_b64=base64.b64encode(encoded(dict(
            # The manifest role the installed WORK_ROLES knows at this revision
            # for the RESULT phase; the seam registers 'result_g5' beside it.
            schema='qualification_campaign_work_manifest/v1', attempt_id=attempt,
            work_id=work, role='probe_result', probe='noop'))).decode('ascii'),
        scopes=scopes)))
    state = json.loads(results.result_state_bytes(attempt))
    results.retain_result_supervision_event(encoded(dict(
        schema='qualification_campaign_supervision_event/v2', attempt_id=attempt,
        work_id=work, kind='PROCESS', clock=clock_doc,
        data=dict(pid=4242, start_ticks=99, uid=7,
                  cgroup='/fpq/' + scopes['payload_slice'] + '/payload-scope',
                  comm='fpq-armed', exe=''))))
    running = encoded(dict(schema='qualification_campaign_work_transition/v1',
        attempt_id=attempt, work_id=work, state='RUNNING', clock=clock_doc, data={}))
    results.record_result_transition(attempt, work, running,
                                     expected_revision=state['authority_revision'])
    instance.results = results
    instance.double = double
    return instance, double


def build_candidate(double, snapshot_bytes):
    """The canonical aggregate bound to one result-snapshot view (the driver
    and the double both build it this way)."""
    context = result_context(double, double.instance.attempt)
    rows, _, _ = double.custody(double.instance.attempt)
    return campaign_result.build_campaign_result(
        checkpoint_receipts=rows,
        cutoffs={row['checkpoint']: row['cutoff_bytes'] for row in rows},
        budget_digest=sha256(snapshot_bytes),
        release=double.instance.release, policy=context.policy)


def sign_candidate(double, candidate_bytes, *, revision, snapshot_sha256, key_id='test-producer'):
    """Sign the authentication envelope with the fixture's result key (the
    Linux-only credential loader's stand-in on Windows)."""
    from cryptography.hazmat.primitives import serialization
    from c1_rail.qualification.execution.g5_result import _authentication_core, _sign_authentication
    private = double.instance.case['private'][key_id]
    context = result_context(double, double.instance.attempt)
    core = _authentication_core(attempt_id=context.attempt_id,
                                aggregate_sha256=sha256(candidate_bytes),
                                campaign_revision=revision, snapshot_sha256=snapshot_sha256)
    return _sign_authentication(core, key_id, private)


def commit_request(attempt, work, candidate_bytes, authentication_bytes, *, revision):
    return encoded(dict(schema='qualification_campaign_request/v2',
        operation='COMMIT_E1_RESULT', attempt_id=attempt, work_id=work,
        candidate_bytes_b64=base64.b64encode(candidate_bytes).decode('ascii'),
        authentication_sha256=sha256(authentication_bytes), expected_revision=revision,
        artifacts=[dict(role='result_authentication',
                        sha256=sha256(authentication_bytes))]))


def stage_authentication(double, authentication_bytes):
    """Private staging through the real store path (STAGE_CHECKPOINT_ARTIFACT
    pattern, role result_authentication)."""
    return double.results.stage_result_artifact(
        double.instance.attempt, 'result_authentication', authentication_bytes)
