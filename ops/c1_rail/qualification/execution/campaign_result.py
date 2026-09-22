"""S6: authenticated FULL_E1 campaign result -- aggregate, validation, custody.

The result family (F2): ``qualification_campaign_result/v1`` (the canonical
aggregate), ``..._result_authentication/v1`` (the G5 result-key signature over
the aggregate digest, expected revision and snapshot identity),
``..._result_snapshot/v1`` (the precommit view, excluding its own future
receipt), ``..._result_intent/v1`` (T1) and ``..._result_receipt/v1`` (the one
immutable receipt). The seal family's tables are mounted in the same v9 layout;
their consumers are S7 (``campaign_seal.py`` / ``seal_service.py``).

Frozen-bytes constraints this module is shaped by (C-R findings): the canonical
budget-snapshot parser and the funding projection admit only the S3 state set,
so the RESULT progression is carried by this family's own projection, snapshot
and receipt while the budget snapshot keeps its canonical predecessor state and
fresh works/accounting; the RESULT-phase work is reserved through this module
(S3's reservation paths require a BOUND campaign). Both are integration seams,
listed in the C-R seam table.
"""
from dataclasses import dataclass
from types import MappingProxyType

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .campaign_budget import (WORK_PREDECESSORS, integer,
                              limits as parse_limits, transition as parse_transition,
                              validate_work_id)
from .protocol import decode_base64, digest, fields, identity, sha256

RESULT_SCHEMA_LITERAL = 'qualification_campaign_result/v1'
RESULT_AUTHENTICATION_SCHEMA = 'qualification_campaign_result_authentication/v1'
RESULT_SNAPSHOT_SCHEMA = 'qualification_campaign_result_snapshot/v1'
RESULT_INTENT_SCHEMA = 'qualification_campaign_result_intent/v1'
RESULT_RECEIPT_SCHEMA = 'qualification_campaign_result_receipt/v1'

# The v9 mount (F2): the S3 v8 layout plus the result and seal families. The
# seal tables are created here because user_version 9 is one migration; their
# consumers arrive with S7.
RESULT_SCHEMA = '''
CREATE TABLE IF NOT EXISTS full_campaign_result_intents (
 attempt_id TEXT PRIMARY KEY REFERENCES full_campaigns(attempt_id),
 work_id TEXT NOT NULL,
 snapshot_bytes BLOB NOT NULL CHECK(length(snapshot_bytes)<=262144),
 intent_bytes BLOB NOT NULL CHECK(length(intent_bytes)<=262144),
 candidate_bytes BLOB NOT NULL CHECK(length(candidate_bytes)<=262144),
 authentication_bytes BLOB CHECK(length(authentication_bytes)<=65536),
 receipt_bytes BLOB);
'''
SEAL_SCHEMA = '''
CREATE TABLE IF NOT EXISTS full_campaign_seal_intents (
 attempt_id TEXT PRIMARY KEY REFERENCES full_campaigns(attempt_id),
 intent_bytes BLOB NOT NULL CHECK(length(intent_bytes)<=262144),
 signature_bytes BLOB CHECK(length(signature_bytes)<=65536),
 receipt_bytes BLOB);
'''

STAGE_ORDER = ('LEGALITY', 'N1', 'N2', 'PART_B', 'PART_A')
# policy.CHECKPOINT_GROUPS: N1 assesses LEGALITY+N1, the joint N2 batch assesses
# N2+PART_B with one joint decision, and PART_A is its own checkpoint.
CHECKPOINTS = ('N1', 'N2', 'PART_A')
CHECKPOINT_STAGES = MappingProxyType({'N1': ('LEGALITY', 'N1'), 'N2': ('N2', 'PART_B'),
                                      'PART_A': ('PART_A',)})
# F3 names, frozen for S4/S5 too. On frozen bytes the budget snapshot cannot
# carry them (journal_snapshot.CAMPAIGN_BUDGET_STATES is the S3 set); they map
# to custody shapes here and name the observed states after the enum seam.
F3_PREDECESSOR_STATES = ('N1_FAILED', 'N2_FAILED', 'PART_A_FAILED', 'FULL_PASS_READY')
RESULT_OUTCOME_STATES = ('RESULT_COMMITTED_PASS', 'RESULT_COMMITTED_FAIL')
REFUSED_BUDGET_STATES = ('IN_DOUBT', 'ABORTED', 'BUDGET_EXHAUSTED', 'BUDGET_UNCERTAIN')
ROW_DECISIONS = ('CONTINUE', 'FAILURE', 'PASS', 'FAIL')
RESULT_PHASE = 'RESULT'
# The SEAL phase's names live beside the RESULT ones because ResultStore's
# work state machine below is shared by both T05 phases -- the committing
# qseal work transitions, settles and completes through it exactly as the
# result work does; campaign_seal imports them.
SEAL_PHASE = 'SEAL'
SEALED_PASS = 'SEALED_PASS'
# S3's a8a983e settlement rule (PR #455 review, Codex P1/P2) carried to the
# T05 commits: the result/seal commit lands while its unit still runs and the
# committing work settles afterwards, so a settlement overrun must end
# authority from the state the commit produced -- RESULT_COMMITTED_{PASS,FAIL}
# / SEALED_PASS -- and that work must complete there. On frozen bytes the
# budget snapshot cannot carry those names (the _advance encode fallback), so
# the statistical predecessor the commit rode is the commit state's frozen
# stand-in: S3's N2_READY/N1_FAILED today, the F3 terminal names once S4/S5
# land, the commit states themselves after the enum seam.
COMMIT_PREDECESSOR_STATES = F3_PREDECESSOR_STATES + ('N2_READY',)
SEAL_COMMIT_STATES = (SEALED_PASS,)
# The S7 eligibility this family exposes: only a committed PASS outcome.
SEAL_ELIGIBLE_STATE = 'RESULT_COMMITTED_PASS'

RESULT_OPERATIONS = ('RESULT_SNAPSHOT', 'COMMIT_E1_RESULT')
_RESULT_OPERATION_FIELDS = {
    'RESULT_SNAPSHOT': set(),
    'COMMIT_E1_RESULT': {'work_id', 'candidate_bytes_b64', 'authentication_sha256',
                         'expected_revision', 'artifacts'},
}


def parse_result_operation(raw):
    """The closed shape of the two S6 operations (registered by the seam)."""
    wire = parse_canonical_json(raw, label='campaign request')
    operation = wire.get('operation') if type(wire) is dict else None
    if operation not in _RESULT_OPERATION_FIELDS:
        raise ValueError('UNKNOWN_OPERATION')
    doc = fields(wire, {'schema', 'operation', 'attempt_id'} | _RESULT_OPERATION_FIELDS[operation])
    if doc['schema'] not in ('qualification_campaign_request/v1', 'qualification_campaign_request/v2'):
        raise ValueError('unsupported campaign request schema')
    identity(doc['attempt_id'])
    if operation == 'COMMIT_E1_RESULT':
        identity(doc['work_id'])
        candidate = decode_base64(doc['candidate_bytes_b64'])
        if not candidate or len(candidate) > 262144:
            raise ValueError('bounded result candidate required')
        digest(doc['authentication_sha256'])
        integer(doc['expected_revision'])
        if (type(doc['artifacts']) is not list
                or any(type(row) is not dict or set(row) != {'role', 'sha256'} for row in doc['artifacts'])):
            raise ValueError('closed staged artifact inventory required')
        for row in doc['artifacts']:
            identity(row['role'])
            digest(row['sha256'])
    return doc


# ---------------------------------------------------------------------------
# The closed receipt-row view -- the only read of checkpoint custody (F1).


def _stage_status(decision):
    return 'FAIL' if decision in ('FAILURE', 'FAIL') else 'PASS'


def parse_receipt_row(row):
    """One ordered checkpoint-custody row as the aggregate consumes it.

    ``stages`` are the checkpoint's own assessment stage rows (the joint N2
    batch carries N2 and PART_B); a row's decision is its final stage's
    status. ``synthetic_predecessor`` marks the S4/S5 predecessors a fixture
    supplies until their canonical custody exists; the validator refuses any
    row claiming real later-checkpoint custody at this revision.
    """
    doc = fields(row, {'attempt_id', 'campaign_id', 'checkpoint', 'work_id', 'decision',
                       'stages', 'result_sha256', 'payload_sha256', 'attestation_sha256',
                       'assessment_sha256', 'cutoff_sha256', 'receipt_sha256',
                       'assessment_bytes', 'cutoff_bytes', 'receipt_bytes',
                       'synthetic_predecessor'})
    if doc['checkpoint'] not in CHECKPOINTS or doc['decision'] not in ROW_DECISIONS:
        raise ValueError('checkpoint receipt row differs')
    identity(doc['attempt_id'])
    identity(doc['campaign_id'])
    identity(doc['work_id'])
    if type(doc['stages']) is not list or [item['stage'] for item in doc['stages']] != \
            list(CHECKPOINT_STAGES[doc['checkpoint']]):
        raise ValueError('checkpoint receipt row stages differ')
    for item in doc['stages']:
        fields(item, {'stage', 'status'})
        if item['status'] not in ('PASS', 'FAIL'):
            raise ValueError('receipt row stage status differs')
    statuses = [item['status'] for item in doc['stages']]
    if statuses[-1] != _stage_status(doc['decision']) or any(
            status != 'PASS' for status in statuses[:-1]):
        raise ValueError('checkpoint decision differs from its stage rows')
    if doc['stages'][0]['stage'] == 'LEGALITY' and statuses[0] != 'PASS':
        raise ValueError('legality stage is pass-only')
    for name in ('result_sha256', 'payload_sha256', 'attestation_sha256', 'assessment_sha256',
                 'cutoff_sha256', 'receipt_sha256'):
        digest(doc[name])
    for name in ('assessment_bytes', 'cutoff_bytes', 'receipt_bytes'):
        if type(doc[name]) is not bytes:
            raise ValueError('checkpoint custody bytes required')
    if type(doc['synthetic_predecessor']) is not bool:
        raise ValueError('synthetic predecessor label required')
    return doc


def _row_outcome(rows):
    """The legal outcome of the ordered custody rows, or the refusal reason.

    The present stages must be a complete prefix of STAGE_ORDER; either every
    stage passes (outcome PASS, all checkpoints required), or exactly the last
    present stage fails (outcome FAIL) -- policy.required_output_roles's three
    shapes.
    """
    if [row['checkpoint'] for row in rows] != list(CHECKPOINTS[:len(rows)]):
        return None, 'checkpoint custody order differs'
    stage_rows = []
    for row in rows:
        stage_rows.extend(row['stages'])
    names = [item['stage'] for item in stage_rows]
    if names != list(STAGE_ORDER[:len(names)]):
        return None, 'stage order differs'
    statuses = [item['status'] for item in stage_rows]
    failed = [index for index, status in enumerate(statuses) if status == 'FAIL']
    if not failed:
        if len(names) != len(STAGE_ORDER):
            return None, 'incomplete passing prefix refuses a result'
        return 'PASS', names
    if failed != [len(statuses) - 1]:
        return None, 'only the last stage of a complete prefix may fail'
    return 'FAIL', names


# ---------------------------------------------------------------------------
# The canonical aggregate.


def build_campaign_result(*, checkpoint_receipts, cutoffs, budget_digest, release, policy) -> bytes:
    """The canonical ``qualification_campaign_result/v1`` aggregate.

    Reconstructs the ordered stage decisions and every checkpoint's digest
    chain from the custody rows -- never a "latest verdict". Legal shapes only:
    FAIL after LEGALITY/N1; FAIL after LEGALITY/N1/N2/PART_B; FAIL or PASS
    after all five stages (policy.required_output_roles's three shapes).
    """
    from .release_schema import parse_release
    from ..policy import required_output_roles
    if not isinstance(cutoffs, dict):
        raise ValueError('cutoff custody per checkpoint required')
    rows = [parse_receipt_row(row) for row in checkpoint_receipts]
    if not rows:
        raise ValueError('checkpoint custody required')
    if len({row['attempt_id'] for row in rows}) != 1 or len({row['campaign_id'] for row in rows}) != 1:
        raise ValueError('result identity differs across custody')
    outcome, stages = _row_outcome(rows)
    if outcome is None:
        raise ValueError(stages)
    required_output_roles(policy, stages=tuple(stages), completion='COMPLETE',
                          verdict='FAIL' if outcome == 'FAIL' else 'PASS')
    document = parse_release(release)
    if document.get('qualification_policy_sha256') != policy.sha256:
        raise ValueError('result policy binding differs')
    for row in rows:
        cutoff = cutoffs.get(row['checkpoint'])
        if type(cutoff) is not bytes:
            raise ValueError('cutoff custody absent for ' + row['checkpoint'])
        cutoff_doc = parse_canonical_json(cutoff, label='checkpoint cutoff')
        # Presence checks, not an exact field set: the canonical N1 cutoff
        # carries the cutoff/threshold tail; S4/S5's successors extend it.
        if not {'schema', 'attempt_id', 'checkpoint', 'assessment_sha256',
                'decision'} <= set(cutoff_doc):
            raise ValueError('cutoff binding differs for ' + row['checkpoint'])
        if (cutoff_doc['schema'] != 'qualification_campaign_cutoff_receipt/v1'
                or cutoff_doc['attempt_id'] != row['attempt_id']
                or cutoff_doc['checkpoint'] != row['checkpoint']
                or cutoff_doc['assessment_sha256'] != row['assessment_sha256']
                or _stage_status(cutoff_doc['decision']) != _stage_status(row['decision'])
                or row['cutoff_bytes'] != cutoff):
            raise ValueError('cutoff binding differs for ' + row['checkpoint'])
    aggregate = dict(
        schema=RESULT_SCHEMA_LITERAL, attempt_id=rows[0]['attempt_id'],
        campaign_id=rows[0]['campaign_id'],
        binding=dict(policy_sha256=policy.sha256, execution_release_sha256=sha256(release),
                     budget_digest=budget_digest),
        stages=[dict(stage=item['stage'], status=item['status'])
                for row in rows for item in row['stages']],
        checkpoints=[dict(checkpoint=row['checkpoint'], work_id=row['work_id'],
                          decision=row['decision'], result_sha256=row['result_sha256'],
                          payload_sha256=row['payload_sha256'],
                          attestation_sha256=row['attestation_sha256'],
                          assessment_sha256=row['assessment_sha256'],
                          cutoff_sha256=row['cutoff_sha256'],
                          receipt_sha256=row['receipt_sha256'])
                     for row in rows],
        accepted_prefix=stages, outcome=outcome)
    raw = encoded(aggregate)
    parse_campaign_result(raw, attempt_id=rows[0]['attempt_id'])
    return raw


def parse_campaign_result(raw, *, attempt_id):
    doc = fields(parse_canonical_json(raw, label='campaign result'), {
        'schema', 'attempt_id', 'campaign_id', 'binding', 'stages', 'checkpoints',
        'accepted_prefix', 'outcome'})
    if doc['schema'] != RESULT_SCHEMA_LITERAL or doc['attempt_id'] != attempt_id:
        raise ValueError('campaign result binding differs')
    identity(doc['campaign_id'])
    binding = fields(doc['binding'], {'policy_sha256', 'execution_release_sha256', 'budget_digest'})
    for name in ('policy_sha256', 'execution_release_sha256', 'budget_digest'):
        digest(binding[name])
    if (type(doc['stages']) is not list or not doc['stages']
            or [row['stage'] for row in doc['stages']] != doc['accepted_prefix']
            or doc['accepted_prefix'] != list(STAGE_ORDER[:len(doc['accepted_prefix'])])):
        raise ValueError('campaign result stage order differs')
    for row in doc['stages']:
        fields(row, {'stage', 'status'})
        if row['stage'] not in STAGE_ORDER or row['status'] not in ('PASS', 'FAIL'):
            raise ValueError('campaign result stage differs')
    if doc['stages'][0]['status'] != 'PASS':
        raise ValueError('campaign result legality stage differs')
    if (type(doc['checkpoints']) is not list
            or [row['checkpoint'] for row in doc['checkpoints']] !=
            list(CHECKPOINTS[:len(doc['checkpoints'])])):
        raise ValueError('campaign result checkpoint order differs')
    for row in doc['checkpoints']:
        fields(row, {'checkpoint', 'work_id', 'decision', 'result_sha256', 'payload_sha256',
                     'attestation_sha256', 'assessment_sha256', 'cutoff_sha256', 'receipt_sha256'})
        if row['checkpoint'] not in CHECKPOINTS or row['decision'] not in ROW_DECISIONS:
            raise ValueError('campaign result checkpoint differs')
        identity(row['work_id'])
        for name in ('result_sha256', 'payload_sha256', 'attestation_sha256', 'assessment_sha256',
                     'cutoff_sha256', 'receipt_sha256'):
            digest(row[name])
    statuses = [row['status'] for row in doc['stages']]
    failed = [index for index, status in enumerate(statuses) if status == 'FAIL']
    if doc['outcome'] not in ('PASS', 'FAIL'):
        raise ValueError('campaign result outcome differs')
    if not failed:
        if doc['outcome'] != 'PASS' or len(doc['stages']) != len(STAGE_ORDER):
            raise ValueError('campaign result incomplete pass differs')
    elif failed != [len(statuses) - 1] or doc['outcome'] != 'FAIL':
        raise ValueError('campaign result failure prefix differs')
    for checkpoint_row in doc['checkpoints']:
        row_stages = CHECKPOINT_STAGES[checkpoint_row['checkpoint']]
        present = [row for row in doc['stages'] if row['stage'] in row_stages]
        if [row['stage'] for row in present] != list(row_stages):
            raise ValueError('campaign result stage membership differs')
        if any(row['status'] != 'PASS' for row in present[:-1]) or (
                present[-1]['status'] != _stage_status(checkpoint_row['decision'])):
            raise ValueError('campaign result stage decision differs')
    return doc


def parse_result_snapshot(raw, *, attempt_id):
    doc = fields(parse_canonical_json(raw, label='result snapshot'), {
        'schema', 'attempt_id', 'campaign_id', 'validity', 'campaign_state',
        'campaign_revision', 'authority_head', 'event_head', 'budget_sha256',
        'budget', 'works', 'checkpoints', 'result'})
    if doc['schema'] != RESULT_SNAPSHOT_SCHEMA or doc['attempt_id'] != attempt_id:
        raise ValueError('result snapshot binding differs')
    identity(doc['campaign_id'])
    if doc['validity'] not in ('VALID', 'VOID'):
        raise ValueError('result snapshot validity differs')
    from ..journal_snapshot import CAMPAIGN_BUDGET_STATES
    if doc['campaign_state'] not in CAMPAIGN_BUDGET_STATES + F3_PREDECESSOR_STATES + RESULT_OUTCOME_STATES:
        raise ValueError('result snapshot state differs')
    integer(doc['campaign_revision'])
    for name in ('authority_head', 'event_head', 'budget_sha256'):
        digest(doc[name])
    budget = fields(doc['budget'], {'settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns'})
    for name in ('settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns'):
        integer(budget[name])
    if type(doc['works']) is not list:
        raise ValueError('result snapshot works required')
    seen = set()
    for work in doc['works']:
        fields(work, {'work_id', 'phase', 'state', 'settled'})
        identity(work['work_id'])
        if work['work_id'] in seen or type(work['settled']) is not bool:
            raise ValueError('result snapshot work identity differs')
        seen.add(work['work_id'])
    if type(doc['checkpoints']) is not list:
        raise ValueError('result snapshot custody required')
    for row in doc['checkpoints']:
        fields(row, {'checkpoint', 'work_id', 'decision', 'stages', 'result_sha256',
                     'payload_sha256', 'attestation_sha256', 'assessment_sha256',
                     'cutoff_sha256', 'receipt_sha256', 'synthetic_predecessor'})
        if row['checkpoint'] not in CHECKPOINTS or row['decision'] not in ROW_DECISIONS:
            raise ValueError('result snapshot custody differs')
        identity(row['work_id'])
        if type(row['stages']) is not list or [item['stage'] for item in row['stages']] != \
                list(CHECKPOINT_STAGES[row['checkpoint']]):
            raise ValueError('result snapshot custody stages differ')
        for item in row['stages']:
            fields(item, {'stage', 'status'})
            if item['status'] not in ('PASS', 'FAIL'):
                raise ValueError('snapshot custody stage status differs')
        for name in ('result_sha256', 'payload_sha256', 'attestation_sha256', 'assessment_sha256',
                     'cutoff_sha256', 'receipt_sha256'):
            digest(row[name])
        if type(row['synthetic_predecessor']) is not bool:
            raise ValueError('synthetic predecessor label required')
    result = fields(doc['result'], {'state', 'outcome'})
    if result['state'] not in ('ABSENT', 'SIGNING', 'COMMITTED'):
        raise ValueError('result family projection differs')
    if result['state'] in ('ABSENT', 'SIGNING') and result['outcome'] is not None:
        raise ValueError('result family projection differs')
    if result['state'] == 'COMMITTED' and result['outcome'] not in ('PASS', 'FAIL'):
        raise ValueError('result family projection differs')
    # The precommit view never contains its own future receipt (S6).
    return doc


def encode_result_snapshot(**values) -> bytes:
    raw = encoded(dict(schema=RESULT_SNAPSHOT_SCHEMA, **values))
    parse_result_snapshot(raw, attempt_id=values['attempt_id'])
    return raw


def parse_result_intent(raw, *, attempt_id):
    doc = fields(parse_canonical_json(raw, label='result intent'), {
        'schema', 'attempt_id', 'work_id', 'key_id', 'signing_at_utc',
        'candidate_sha256', 'snapshot_sha256'})
    from .campaign_budget import utc
    if doc['schema'] != RESULT_INTENT_SCHEMA or doc['attempt_id'] != attempt_id:
        raise ValueError('result intent binding differs')
    identity(doc['work_id'])
    identity(doc['key_id'])
    utc(doc['signing_at_utc'])
    digest(doc['candidate_sha256'])
    digest(doc['snapshot_sha256'])
    return doc


def parse_result_receipt(raw, *, attempt_id):
    doc = fields(parse_canonical_json(raw, label='result receipt'), {
        'schema', 'attempt_id', 'work_id', 'campaign_id', 'aggregate_sha256',
        'authentication_sha256', 'outcome', 'campaign_state', 'accepted_prefix',
        'campaign_revision', 'authority_head', 'budget', 'checkpoints',
        'signing_at_utc', 'committed_at_utc', 'intent_sha256'})
    from .campaign_budget import utc
    if (doc['schema'] != RESULT_RECEIPT_SCHEMA or doc['attempt_id'] != attempt_id
            or doc['outcome'] not in ('PASS', 'FAIL')
            or doc['campaign_state'] not in RESULT_OUTCOME_STATES
            or doc['campaign_state'] != 'RESULT_COMMITTED_' + doc['outcome']):
        raise ValueError('result receipt binding differs')
    identity(doc['work_id'])
    identity(doc['campaign_id'])
    for name in ('aggregate_sha256', 'authentication_sha256', 'authority_head', 'intent_sha256'):
        digest(doc[name])
    if doc['accepted_prefix'] != list(STAGE_ORDER[:len(doc['accepted_prefix'])]):
        raise ValueError('result receipt prefix differs')
    integer(doc['campaign_revision'])
    utc(doc['signing_at_utc'])
    utc(doc['committed_at_utc'])
    budget = fields(doc['budget'], {'settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns'})
    for name in ('settled_cpu_ns', 'reserved_cpu_ns', 'remaining_cpu_ns'):
        integer(budget[name])
    if (type(doc['checkpoints']) is not list
            or [row['checkpoint'] for row in doc['checkpoints']] !=
            list(CHECKPOINTS[:len(doc['checkpoints'])])):
        raise ValueError('result receipt custody differs')
    for row in doc['checkpoints']:
        fields(row, {'checkpoint', 'receipt_sha256'})
        if row['checkpoint'] not in CHECKPOINTS:
            raise ValueError('result receipt custody differs')
        digest(row['receipt_sha256'])
    return doc


# ---------------------------------------------------------------------------
# Validator-issued evidence. VerifiedResult is verified evidence, never a
# caller-issued capability: the commit re-derives every field from the
# persisted candidate bytes inside its own transaction, so a forged object
# cannot carry a lying outcome, prefix or digest chain through T2.


@dataclass(frozen=True)
class VerifiedResult:
    attempt_id: str
    result_bytes: bytes
    aggregate_sha256: str
    outcome: str
    accepted_prefix: tuple
    checkpoints: tuple
    expected_revision: int
    snapshot_sha256: str
    receipt_digests: tuple


def require_verified_result(value):
    """Exact-type gate (the deep binding checks live in T2's re-derivation)."""
    if type(value) is not VerifiedResult:
        raise ValueError('validator-issued result provenance is required')


def _require_live_key(current_keys, key_id, *, role):
    key = current_keys.get(key_id)
    if key is None:
        raise ValueError(role + ' key is not currently enrolled')
    if key.revoked_at is not None:
        raise ValueError(role + ' key is revoked')


def validate_campaign_result(context, result_bytes, *, attestations, artifacts,
                             assessment_receipts, snapshot_bytes, current_keys) -> VerifiedResult:
    """The service-side pure validator (S6 §1).

    Verifies every checkpoint's attestation/assessment through the S3
    verifiers where S3 defines them (N1), refuses any row claiming real
    custody S3 never wrote, rebuilds the canonical aggregate from the custody
    rows and requires byte equality, and checks the snapshot binding. Returns
    verified evidence, never a capability object.
    """
    from .g5 import verify_checkpoint_assessment, verify_checkpoint_attestation
    rows = [parse_receipt_row(row) for row in assessment_receipts]
    outcome, stages = _row_outcome(rows)
    if outcome is None:
        raise ValueError(stages)
    snapshot = parse_result_snapshot(snapshot_bytes, attempt_id=context.attempt_id)
    if snapshot['validity'] != 'VALID':
        raise ValueError('VOID campaign')
    aggregate = parse_campaign_result(result_bytes, attempt_id=context.attempt_id)
    rebuilt = build_campaign_result(
        checkpoint_receipts=rows,
        cutoffs={row['checkpoint']: row['cutoff_bytes'] for row in rows},
        budget_digest=sha256(snapshot_bytes),
        release=context.installed_release, policy=context.policy)
    if rebuilt != result_bytes:
        raise ValueError('campaign result differs from canonical reconstruction')
    if (aggregate['binding']['policy_sha256'] != context.policy.sha256
            or aggregate['binding']['execution_release_sha256'] != sha256(context.installed_release)
            or aggregate['binding']['budget_digest'] != sha256(snapshot_bytes)):
        raise ValueError('campaign result binding differs from enrollment')
    if [row['checkpoint'] for row in aggregate['checkpoints']] != [row['checkpoint'] for row in rows]:
        raise ValueError('campaign result custody membership differs')
    for row, aggregate_row in zip(rows, aggregate['checkpoints']):
        if any(aggregate_row[name] != row[name] for name in (
                'work_id', 'decision', 'result_sha256', 'payload_sha256', 'attestation_sha256',
                'assessment_sha256', 'cutoff_sha256', 'receipt_sha256')):
            raise ValueError('campaign result custody digest differs')
    for row in rows:
        attestation_bytes = attestations[row['checkpoint']]
        capture = artifacts[row['checkpoint']]
        if (sha256(attestation_bytes) != row['attestation_sha256']
                or sha256(capture['result']) != row['result_sha256']
                or sha256(capture['payload']) != row['payload_sha256']):
            raise ValueError('checkpoint custody membership differs for ' + row['checkpoint'])
        if row['checkpoint'] == 'N1':
            try:
                verified = verify_checkpoint_attestation(attestation_bytes, context=context,
                                                         current_keys=current_keys)
            except KeyError as exc:
                raise ValueError('execution key is not currently enrolled') from exc
            _require_live_key(current_keys, verified['signature']['key_id'], role='execution')
            if sha256(row['assessment_bytes']) != row['assessment_sha256']:
                raise ValueError('N1 assessment custody differs')
            try:
                assessment = verify_checkpoint_assessment(row['assessment_bytes'],
                                                          context=context, current_keys=current_keys)
            except KeyError as exc:
                raise ValueError('result key is not currently enrolled') from exc
            _require_live_key(current_keys, assessment['signature']['key_id'], role='result')
        elif not row['synthetic_predecessor']:
            # Real later-checkpoint custody cannot exist before S4/S5; a row
            # claiming it is a fabrication.
            raise ValueError('later checkpoint custody requires its canonical verifier')
    return VerifiedResult(
        attempt_id=context.attempt_id, result_bytes=result_bytes,
        aggregate_sha256=sha256(result_bytes), outcome=outcome,
        accepted_prefix=tuple(stages), checkpoints=tuple(row['checkpoint'] for row in rows),
        expected_revision=snapshot['campaign_revision'], snapshot_sha256=sha256(snapshot_bytes),
        receipt_digests=tuple(row['receipt_sha256'] for row in rows))


# ---------------------------------------------------------------------------
# The store companion (F2): same DB, own tables, v9 custody.


class ResultStore:
    """S6 custody: the v9 layout, the RESULT-phase work, T1 and T2.

    Composition over the real ``CampaignStore`` (frozen-bytes constraint: S3's
    ``_budget`` refuses user_version 9, so this class reads the canonical
    budget snapshot itself and appends events with the same chain discipline).
    """

    def __init__(self, campaigns):
        self.campaigns = campaigns
        self.store = campaigns.store

    # -- layout ------------------------------------------------------------
    def _ensure_result_layout(self, connection):
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        if version == 9:
            return
        if version != 8:
            raise ValueError('result custody requires database v8')
        self.store.validate_layout(connection, 8)
        for statement in RESULT_SCHEMA.split(';'):
            if statement.strip():
                connection.execute(statement)
        for statement in SEAL_SCHEMA.split(';'):
            if statement.strip():
                connection.execute(statement)
        connection.execute('PRAGMA user_version=9')

    def _state(self, connection, attempt_id):
        identity(attempt_id)
        if connection.execute('PRAGMA user_version').fetchone()[0] not in (8, 9):
            raise ValueError('no metered campaign')
        row = connection.execute('SELECT snapshot_bytes FROM full_campaign_budgets '
                                 'WHERE attempt_id=?', (attempt_id,)).fetchone()
        if row is None:
            raise ValueError('dormant campaign has no metered history')
        from ..journal_snapshot import parse_campaign_budget_snapshot
        return parse_campaign_budget_snapshot(bytes(row[0]))

    def _advance(self, connection, state, kind, *, authority=True, state_name=None):
        """The _save_budget chain discipline without the v7/v8 funding
        projection (C-R finding: the projection's state enum and version gate
        are integration seams; the projection stays at its last v8 image).

        ``state_name`` is the coordinator-ruled post-seam behavior: once the
        canonical state enum admits RESULT_COMMITTED_*/SEALED_PASS, the advance
        writes the name into the budget snapshot and the family projection is
        a mirror; on frozen bytes the parser still refuses those names, so the
        canonical predecessor state is kept (encode falls back)."""
        from ..journal_snapshot import encode_campaign_budget_snapshot
        self.campaigns._totals(state)
        state['validity'] = self.campaigns.row(state['attempt_id'])['validity']
        previous = state['event_head']
        state['accounting_revision'] += 1
        if authority:
            state['authority_revision'] += 1
        predecessor = state['state']
        if state_name is not None:
            state['state'] = state_name
        body = encoded(dict(kind=kind, authority=authority, snapshot=state))
        head = sha256(previous.encode('ascii') + body)
        try:
            raw = encode_campaign_budget_snapshot(state)
        except ValueError:
            if state_name is None:
                raise
            state['state'] = predecessor
            body = encoded(dict(kind=kind, authority=authority, snapshot=state))
            head = sha256(previous.encode('ascii') + body)
            raw = encode_campaign_budget_snapshot(state)
        state['event_head'] = head
        if authority:
            state['authority_head'] = head
        connection.execute('INSERT INTO full_campaign_budgets VALUES(?,?) '
                           'ON CONFLICT(attempt_id) DO UPDATE SET snapshot_bytes=excluded.snapshot_bytes',
                           (state['attempt_id'], raw))
        connection.execute('INSERT INTO full_campaign_budget_events VALUES(?,?,?,?,?)',
                           (state['attempt_id'], state['accounting_revision'], body, previous, head))
        return state

    # -- eligibility ---------------------------------------------------------
    def result_state_bytes(self, attempt_id):
        """The campaign's budget snapshot bytes (the guardian loop's authority
        view; no funding gate -- S3's budget_snapshot is v7/v8-gated)."""
        with self.store.transaction() as connection:
            return encoded(self._state(connection, attempt_id))

    def stage_result_artifact(self, attempt_id, role, raw):
        """Private bounded staging (the STAGE_CHECKPOINT_ARTIFACT pattern) for
        the result family's roles; S3's staging path is v7/v8-gated at this
        revision (C-R seam finding)."""
        from .protocol import identity
        identity(role)
        if len(raw) > 268435456:
            raise ValueError('staged result artifact exceeds bound')
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            self._state(connection, attempt_id)
            digest_value = sha256(raw)
            connection.execute('INSERT OR IGNORE INTO full_campaign_checkpoint_staged VALUES(?,?,?,?)',
                               (attempt_id, role, digest_value, raw))
            return digest_value

    def retain_result_enrollment(self, raw):
        """The RESULT work's supervision enrollment (the S3 retention path is
        v7/v8-gated; identical shape and bounds here)."""
        from .campaign_supervisor import parse_enrollment
        enrollment = parse_enrollment(raw)
        attempt, work_id = enrollment['attempt_id'], enrollment['work_id']
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            state = self._state(connection, attempt)
            self.campaigns._work(state, work_id)
            if len(raw) > state['profile']['record_byte_limit']:
                raise ValueError('supervision enrollment exceeds storage bound')
            role = 'supervision_' + work_id
            prior = connection.execute('SELECT body FROM full_campaign_objects '
                                       'WHERE attempt_id=? AND role=?', (attempt, role)).fetchone()
            if prior is not None and bytes(prior[0]) != raw:
                raise ValueError('immutable supervision enrollment differs')
            connection.execute('INSERT OR IGNORE INTO full_campaign_objects VALUES(?,?,?,?,?)',
                               (attempt, role, sha256(raw), len(raw), raw))

    def retain_result_supervision_event(self, raw):
        """One supervision event for the RESULT work (S3 shape, v9-safe)."""
        from .campaign_supervisor import parse_supervision_event
        event = parse_supervision_event(raw)
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            state = self._state(connection, event['attempt_id'])
            self.campaigns._work(state, event['work_id'])
            if len(raw) > state['profile']['record_byte_limit']:
                raise ValueError('supervision event exceeds storage bound')
            role = 'supervision_event_' + sha256(raw)
            connection.execute('INSERT OR IGNORE INTO full_campaign_objects VALUES(?,?,?,?,?)',
                               (event['attempt_id'], role, sha256(raw), len(raw), raw))

    def _result_eligibility(self, connection, state, attempt_id):
        """The F3 predecessor test on frozen bytes: custody-derived, with the
        canonical budget states that always refuse."""
        if state['state'] in REFUSED_BUDGET_STATES:
            return None, state['state']
        if self.campaigns.row(attempt_id)['validity'] != 'VALID':
            return None, 'VOID campaign'
        if self.campaigns._cancellation_pending(connection, attempt_id):
            return None, 'campaign cancellation pending'
        rows = self._checkpoint_receipts(connection, attempt_id)
        outcome, stages = _row_outcome(rows)
        if outcome is None:
            return None, stages
        return outcome, stages

    # -- the closed accessor -------------------------------------------------
    def checkpoint_receipts(self, attempt_id):
        """Ordered custody rows -- the only read of checkpoint custody (F1).

        At this revision S3's custody holds the committed N1 family; S4/S5
        widen it. The row carries the assessment/cutoff/receipt bytes so the
        validator verifies signatures without a second read path.
        """
        with self.store.transaction() as connection:
            return self._checkpoint_receipts(connection, attempt_id)

    def _checkpoint_receipts(self, connection, attempt_id):
        if connection.execute('PRAGMA user_version').fetchone()[0] < 8:
            raise ValueError('no checkpoint family retained')
        row = connection.execute('SELECT candidate_bytes,cutoff_bytes,receipt_bytes '
                                 'FROM full_campaign_checkpoint_intents WHERE attempt_id=?',
                                 (attempt_id,)).fetchone()
        if row is None or row[2] is None:
            raise ValueError('no committed checkpoint custody')
        capture = connection.execute('SELECT result_bytes,payload_bytes,attestation_bytes '
                                     'FROM full_campaign_checkpoint_captures WHERE attempt_id=?',
                                     (attempt_id,)).fetchone()
        if capture is None or capture[2] is None:
            raise ValueError('no committed checkpoint custody')
        from ..evidence import parse_checkpoint_assessment as parse_n1_assessment
        candidate = parse_n1_assessment(bytes(row[0]), attempt_id=attempt_id)
        campaign = self.campaigns.row(attempt_id)
        n1_status = 'FAIL' if candidate['n1_decision'] == 'FAIL' else 'PASS'
        return [dict(attempt_id=attempt_id, campaign_id=campaign['campaign_id'], checkpoint='N1',
                     work_id=candidate['work_id'], decision=candidate['decision'],
                     stages=[dict(stage='LEGALITY', status='PASS'), dict(stage='N1', status=n1_status)],
                     result_sha256=sha256(bytes(capture[0])), payload_sha256=sha256(bytes(capture[1])),
                     attestation_sha256=sha256(bytes(capture[2])),
                     assessment_sha256=sha256(bytes(row[0])), cutoff_sha256=sha256(bytes(row[1])),
                     receipt_sha256=sha256(bytes(row[2])), assessment_bytes=bytes(row[0]),
                     cutoff_bytes=bytes(row[1]), receipt_bytes=bytes(row[2]),
                     synthetic_predecessor=False)]

    # -- the RESULT-phase work ------------------------------------------------
    def reserve_result_work(self, attempt_id, work_id, limits_bytes, *, expected_revision,
                            start_transition_bytes=None):
        """Reserve the RESULT phase from a terminal statistical predecessor.

        S3's reservation paths require a BOUND campaign (C-R finding); this
        method keeps their remaining gates: installed phase configuration, one
        RESULT work, cancellation barrier, remaining-after-charges, and
        serialization during signing. ``start_transition_bytes`` is the
        guardian's real enrollment transition (work_enrollment scopes); no
        scope is ever fabricated here.
        """
        from .campaign_budget import clock, limits
        integer(expected_revision)
        validate_work_id(work_id)
        specification = parse_canonical_json(limits_bytes, label='work reservation')
        fields(specification, {'limits', 'clock', 'input_sha256'})
        limits(specification['limits'])
        clock(encoded(specification['clock']))
        digest(specification['input_sha256'])
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            state = self._state(connection, attempt_id)
            existing = next((w for w in state['works'] if w['work_id'] == work_id), None)
            if existing is not None:
                if (existing['phase'] != RESULT_PHASE
                        or decode_base64(existing['reservation_bytes_b64']) != limits_bytes):
                    raise ValueError('work reservation identity conflict')
                return encoded(state)
            self.campaigns._cancellation_barrier(connection, attempt_id, admitted_only=False)
            if expected_revision != state['authority_revision']:
                raise ValueError('campaign authority revision conflict')
            outcome, reason = self._result_eligibility(connection, state, attempt_id)
            if outcome is None:
                raise ValueError('result predecessor refuses: ' + reason)
            if RESULT_PHASE not in state['profile']['phases']:
                raise ValueError('installed RESULT phase required')
            if specification['limits'] != state['profile']['phases'][RESULT_PHASE]:
                raise ValueError('reservation must use installed phase configuration')
            if any(w['phase'] == RESULT_PHASE for w in state['works']):
                raise ValueError('result phase already reserved')
            # An open signing window serializes; committed (SIGNED) checkpoint
            # predecessors are settled facts of the terminal prefix, not
            # in-flight authority (the C-R freeze table records this delta).
            if any(w['state'] == 'SIGNING_INTENT' for w in state['works']):
                raise ValueError('authority-changing work is serialized during signing')
            self.campaigns._observe_clock(state, specification['clock'])
            # _terminal is a no-op on the already-terminal predecessor state,
            # so the deadline is enforced explicitly for the RESULT phase.
            boottime = specification['clock']['boottime_ns']
            if (boottime is None or boottime >= state['deadline_boottime_ns']
                    or state['state'] in REFUSED_BUDGET_STATES):
                self._advance(connection, state, 'RESERVE_RESULT_WORK', authority=True)
                raise ValueError('result reservation refused by campaign budget: BUDGET_EXHAUSTED')
            if specification['limits']['cpu_ns'] > self.campaigns._remaining_after_charges(
                    connection, state):
                self._advance(connection, state, 'RESERVE_RESULT_WORK', authority=True)
                raise ValueError('result reservation exceeds the remaining allowance')
            transitions = []
            state_after_start = 'RESERVED'
            if start_transition_bytes is not None:
                start = parse_transition(start_transition_bytes, attempt_id, work_id)
                if start['state'] != 'START_INTENT' or state['campaign_scope_id'] not in (
                        None, start['data']['campaign_scope_id']):
                    raise ValueError('common campaign memory scope required')
                state['campaign_scope_id'] = start['data']['campaign_scope_id']
                transitions.append(self.campaigns._b64(start_transition_bytes))
                state_after_start = 'START_INTENT'
            state['works'].append(dict(work_id=work_id, phase=RESULT_PHASE,
                limits=specification['limits'], input_sha256=specification['input_sha256'],
                reservation_bytes_b64=self.campaigns._b64(limits_bytes),
                state=state_after_start, transitions=transitions,
                observation_bytes_b64=None, charge_cpu_ns=0))
            state['works'].sort(key=lambda w: w['work_id'])
            return encoded(self._advance(connection, state, 'RESERVE_RESULT_WORK', authority=True))

    def record_result_transition(self, attempt_id, work_id, transition_bytes, *, expected_revision):
        """The RESULT/SEAL works' transitions with S3's gates (idempotency,
        work state machine, clock observation, identity-gated credit) plus
        the a8a983e completion rule: the committing work completes in the
        state its own commit produced; a settlement that ended authority
        (overrun or uncertainty) refuses the completion."""
        integer(expected_revision)
        doc = parse_transition(transition_bytes, attempt_id, work_id)
        target = doc['state']
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            state = self._state(connection, attempt_id)
            work = self.campaigns._work(state, work_id)
            if work['phase'] not in (RESULT_PHASE, SEAL_PHASE):
                raise ValueError('result or seal work required')
            for saved in work['transitions']:
                previous = parse_canonical_json(decode_base64(saved), label='saved transition')
                if previous['state'] == target:
                    if decode_base64(saved) != transition_bytes:
                        raise ValueError('immutable work transition conflict')
                    return encoded(state)
            if self.campaigns.row(attempt_id)['validity'] != 'VALID':
                raise ValueError('VOID campaign')
            if self.campaigns._cancellation_pending(connection, attempt_id):
                raise ValueError('campaign cancellation pending')
            if expected_revision != state['authority_revision']:
                raise ValueError('campaign authority revision conflict')
            if work['state'] not in WORK_PREDECESSORS[target]:
                raise ValueError('illegal work transition; no reexecution')
            if any(w['work_id'] != work_id and w['state'] == 'SIGNING_INTENT'
                   for w in state['works']):
                raise ValueError('authority-changing work is serialized during signing')
            self.campaigns._observe_clock(state, doc['clock'])
            if (target in ('CAPTURED', 'SIGNING_INTENT', 'SIGNED')
                    and len(transition_bytes) > state['profile']['record_byte_limit']):
                raise ValueError('work metadata exceeds bounded storage')
            if target in ('CAPTURED', 'SIGNING_INTENT', 'COMPLETED'):
                self.campaigns._require_payload_identity(connection, state, work)
            if target in ('START_INTENT', 'RUNNING') and work['observation_bytes_b64'] is not None:
                raise ValueError('settled work cannot resume')
            # S2-G4 A2/A5: settlement closes the credit window and requires it
            # before finalization.
            if target in ('CAPTURED', 'SIGNING_INTENT') and work['observation_bytes_b64'] is not None:
                raise ValueError('settled work cannot acquire credit')
            if target == 'COMPLETED' and work['observation_bytes_b64'] is None:
                raise ValueError('settlement required before finalization')
            # The a8a983e completion rule (S3's P2): the committing work
            # completes in the state its own commit produced -- the seal
            # commit's SEALED_PASS, the result commit's RESULT_COMMITTED_*,
            # or that state's frozen statistical stand-in. A settlement that
            # ended authority refuses: the committed receipt is already
            # history (S3's _check_budget shape).
            if target == 'COMPLETED' and state['state'] not in self._completion_states(work):
                raise ValueError('terminal campaign budget')
            work['state'] = target
            work['transitions'].append(self.campaigns._b64(transition_bytes))
            return encoded(self._advance(connection, state, target,
                                         authority=target not in ('IN_DOUBT', 'ABORTED')))

    @staticmethod
    def _commit_progressions(work):
        """The campaign states ``work``'s own commit produces: the seal
        commit's SEALED_PASS or the result commit's RESULT_COMMITTED_{PASS,
        FAIL}, with the statistical predecessors that stand in for them on
        frozen bytes (the _advance encode fallback)."""
        if work['phase'] == SEAL_PHASE:
            return SEAL_COMMIT_STATES + COMMIT_PREDECESSOR_STATES
        return RESULT_OUTCOME_STATES + COMMIT_PREDECESSOR_STATES

    @classmethod
    def _completion_states(cls, work):
        """The live campaign states in which the committing work may complete:
        the state its own commit produced (or its frozen stand-in) plus the
        ordinary live states. An authority-ended state (BUDGET_EXHAUSTED,
        BUDGET_UNCERTAIN, IN_DOUBT, ABORTED) is not among them."""
        return ('PROVISIONAL', 'BOUND') + cls._commit_progressions(work)

    @staticmethod
    def _settlement_terminal(state, reason):
        """S3's a8a983e _settlement_terminal for the result/seal commits: a
        work that committed while it ran settles afterwards, and an overrun or
        uncertain settlement ends authority from the state its own commit
        produced -- and from that state's frozen statistical stand-in -- not
        just from PROVISIONAL/BOUND (campaigns._terminal's no-op would leave
        the successful progression standing). The committed receipt survives
        as history only."""
        live = (('PROVISIONAL', 'BOUND') + COMMIT_PREDECESSOR_STATES
                + RESULT_OUTCOME_STATES + SEAL_COMMIT_STATES)
        if state['state'] in live:
            state['state'] = reason

    def settle_result_work(self, attempt_id, work_id, observations_bytes):
        """The guardian's settlement of the result/seal work (S3 settle_work
        gates, scoped to the T05 phases; the committing work settles after
        its own T2, so its overrun ends authority per _settlement_terminal)."""
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            state = self._state(connection, attempt_id)
            work = self.campaigns._work(state, work_id)
            if work['phase'] not in (RESULT_PHASE, SEAL_PHASE):
                raise ValueError('result or seal work required')
            doc = self.campaigns._observation(state, work, observations_bytes)
            if work['observation_bytes_b64'] is not None:
                if decode_base64(work['observation_bytes_b64']) != observations_bytes:
                    raise ValueError('settlement observation conflict')
                return encoded(state)
            previous_state = state['state']
            self.campaigns._observe_clock(state, doc['clock'])
            work['observation_bytes_b64'] = self.campaigns._b64(observations_bytes)
            from .campaign_budget import observation_charge
            work['charge_cpu_ns'] = observation_charge(doc, work['limits'])
            self.campaigns._observe_resources(state, doc)
            if work['charge_cpu_ns'] > work['limits']['cpu_ns']:
                self._settlement_terminal(state, 'BUDGET_EXHAUSTED')
            return encoded(self._advance(connection, state, 'SETTLE_WORK',
                                         authority=state['state'] != previous_state))

    # -- the precommit snapshot ------------------------------------------------
    def result_snapshot(self, attempt_id):
        """``qualification_campaign_result_snapshot/v1`` -- authority revision
        and head, campaign state, the checkpoint receipt digests, budget state;
        excludes its own future receipt."""
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            return self._result_snapshot(connection, attempt_id)

    def _result_snapshot(self, connection, attempt_id):
        state = self._state(connection, attempt_id)
        rows = self._checkpoint_receipts(connection, attempt_id)
        campaign = self.campaigns.row(attempt_id)
        family = self._result_family(connection, attempt_id)
        outcome, stages = _row_outcome(rows)
        if outcome is None:
            raise ValueError(stages)
        return encode_result_snapshot(
            attempt_id=attempt_id, campaign_id=campaign['campaign_id'],
            validity=campaign['validity'], campaign_state=state['state'],
            campaign_revision=state['authority_revision'], authority_head=state['authority_head'],
            event_head=state['event_head'], budget_sha256=sha256(encoded(state)),
            budget=dict(settled_cpu_ns=state['settled_cpu_ns'],
                        reserved_cpu_ns=state['reserved_cpu_ns'],
                        remaining_cpu_ns=state['remaining_cpu_ns']),
            works=[dict(work_id=work['work_id'], phase=work['phase'], state=work['state'],
                        settled=work['observation_bytes_b64'] is not None)
                   for work in state['works']],
            checkpoints=[{name: row[name] for name in (
                'checkpoint', 'work_id', 'decision', 'stages', 'result_sha256', 'payload_sha256',
                'attestation_sha256', 'assessment_sha256', 'cutoff_sha256', 'receipt_sha256',
                'synthetic_predecessor')} for row in rows],
            result=dict(state=family['state'], outcome=family['outcome']))

    def _result_family(self, connection, attempt_id):
        row = connection.execute('SELECT work_id,receipt_bytes FROM full_campaign_result_intents '
                                 'WHERE attempt_id=?', (attempt_id,)).fetchone()
        if row is None:
            return dict(state='ABSENT', outcome=None, work_id=None)
        if row[1] is None:
            return dict(state='SIGNING', outcome=None, work_id=row[0])
        receipt = parse_result_receipt(bytes(row[1]), attempt_id=attempt_id)
        return dict(state='COMMITTED', outcome=receipt['outcome'], work_id=row[0])

    # -- T1 -------------------------------------------------------------------
    def persist_result_intent(self, attempt_id, work_id, snapshot_bytes, intent_bytes,
                              candidate_bytes, *, expected_revision):
        """T1 (F5): the fixed intent and candidate durably persisted before
        any signature. An exact retry is idempotent; a different candidate
        under a persisted intent always refuses. No fresh time or key."""
        integer(expected_revision)
        parse_campaign_result(candidate_bytes, attempt_id=attempt_id)
        snapshot = parse_result_snapshot(snapshot_bytes, attempt_id=attempt_id)
        intent = parse_result_intent(intent_bytes, attempt_id=attempt_id)
        if (intent['work_id'] != work_id
                or intent['candidate_sha256'] != sha256(candidate_bytes)
                or intent['snapshot_sha256'] != sha256(snapshot_bytes)):
            raise ValueError('result signing intent identity differs')
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            prior = connection.execute('SELECT intent_bytes,candidate_bytes '
                                       'FROM full_campaign_result_intents WHERE attempt_id=?',
                                       (attempt_id,)).fetchone()
            if prior is not None:
                if (bytes(prior[0]), bytes(prior[1])) != (intent_bytes, candidate_bytes):
                    raise ValueError('immutable result signing candidate differs')
                return encoded(self._state(connection, attempt_id))
            state = self._state(connection, attempt_id)
            work = self.campaigns._work(state, work_id)
            if work['phase'] != RESULT_PHASE:
                raise ValueError('result work required')
            if work['state'] not in ('RUNNING', 'CAPTURED'):
                raise ValueError('running result work required')
            outcome, reason = self._result_eligibility(connection, state, attempt_id)
            if outcome is None:
                raise ValueError('result predecessor refuses: ' + reason)
            if expected_revision != state['authority_revision']:
                raise ValueError('campaign authority revision conflict')
            if (snapshot['campaign_revision'] != state['authority_revision']
                    or snapshot['event_head'] != state['event_head']):
                raise ValueError('result snapshot freshness differs')
            # No fresh clock at T1: the signing window rides the persisted
            # last observation (the frozen signature carries no clock source).
            # The CAPTURED -> SIGNING_INTENT pair is the S3 T1 shape: the
            # aggregate's retention is the work's capture fact.
            capture = encoded(dict(schema='qualification_campaign_result_capture/v1',
                attempt_id=attempt_id, work_id=work_id,
                candidate_sha256=sha256(candidate_bytes)))
            captured = encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt_id, work_id=work_id, state='CAPTURED',
                clock=state['last_clock'], data=dict(
                    capture_bytes_b64=self.campaigns._b64(capture))))
            state = parse_canonical_json(self.record_result_transition(
                attempt_id, work_id, captured, expected_revision=state['authority_revision']),
                label='result captured state')
            signing = encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt_id, work_id=work_id, state='SIGNING_INTENT',
                clock=state['last_clock'], data=dict(intent_id=work_id + '-intent',
                    payload_bytes_b64=self.campaigns._b64(candidate_bytes),
                    key_id=intent['key_id'], signing_at_utc=intent['signing_at_utc'])))
            state = parse_canonical_json(self.record_result_transition(
                attempt_id, work_id, signing, expected_revision=state['authority_revision']),
                label='result state')
            connection.execute('INSERT INTO full_campaign_result_intents VALUES(?,?,?,?,?,?,NULL)',
                               (attempt_id, work_id, snapshot_bytes, intent_bytes, candidate_bytes,
                                None))
            return encoded(state)

    # -- T2 -------------------------------------------------------------------
    def commit_campaign_result(self, attempt_id, work_id, validated, authentication_bytes,
                               *, now):
        """T2 (F5/F3): one transaction publishing result, authentication and
        one immutable receipt, advancing to RESULT_COMMITTED_{PASS,FAIL}. An
        exact retry returns the byte-identical receipt with the current
        validity; a VOID before the commit refuses; a VOID after flips the
        wrapper's validity only. The receipt binds the journal head reached
        before its own publication event and the pre-charge budget totals --
        no digest contains itself."""
        from .store import instant
        require_verified_result(validated)
        with self.store.transaction() as connection:
            self._ensure_result_layout(connection)
            row = connection.execute('SELECT snapshot_bytes,intent_bytes,candidate_bytes,'
                                     'receipt_bytes FROM full_campaign_result_intents '
                                     'WHERE attempt_id=?', (attempt_id,)).fetchone()
            if row is None or bytes(row[2]) != validated.result_bytes:
                raise ValueError('exact result candidate retry required')
            if row[3] is not None:
                return encoded(dict(
                    receipt=parse_result_receipt(bytes(row[3]), attempt_id=attempt_id),
                    validity=self.campaigns.row(attempt_id)['validity'], historical=True))
            state = self._state(connection, attempt_id)
            if self.campaigns.row(attempt_id)['validity'] != 'VALID' or state['validity'] != 'VALID':
                raise ValueError('VOID campaign')
            if self.campaigns._cancellation_pending(connection, attempt_id):
                raise ValueError('campaign cancellation pending')
            work = self.campaigns._work(state, work_id)
            if work['phase'] != RESULT_PHASE or work['state'] != 'SIGNING_INTENT':
                raise ValueError('signing intent window required')
            intent = parse_result_intent(bytes(row[1]), attempt_id=attempt_id)
            snapshot = parse_result_snapshot(bytes(row[0]), attempt_id=attempt_id)
            # T2 re-derives every validated field from the persisted candidate
            # bytes: a forged VerifiedResult cannot lie through this commit.
            persisted = parse_campaign_result(bytes(row[2]), attempt_id=attempt_id)
            derived_digests = tuple(item['receipt_sha256'] for item in persisted['checkpoints'])
            derived_checkpoints = tuple(item['checkpoint'] for item in persisted['checkpoints'])
            if (validated.aggregate_sha256 != sha256(bytes(row[2]))
                    or validated.result_bytes != bytes(row[2])
                    or validated.attempt_id != attempt_id
                    or validated.outcome != persisted['outcome']
                    or validated.accepted_prefix != tuple(persisted['accepted_prefix'])
                    or validated.checkpoints != derived_checkpoints
                    or validated.receipt_digests != derived_digests
                    or validated.snapshot_sha256 != sha256(bytes(row[0]))
                    or validated.expected_revision != snapshot['campaign_revision']):
                raise ValueError('validated result differs from the persisted candidate')
            authentication = self._parse_authentication(authentication_bytes, attempt_id=attempt_id)
            if (authentication['aggregate_sha256'] != validated.aggregate_sha256
                    or authentication['campaign_revision'] != validated.expected_revision
                    or authentication['snapshot_sha256'] != validated.snapshot_sha256):
                raise ValueError('result authentication binding differs')
            # The deadline re-check inside T2 (the budget clock's last
            # observation is authoritative on frozen bytes).
            if (state['last_clock']['boottime_ns'] is None
                    or state['last_clock']['boottime_ns'] >= state['deadline_boottime_ns']):
                raise ValueError('result commit refused by campaign budget: BUDGET_EXHAUSTED')
            # Freshness: only this intent's own events since the T1 snapshot head.
            head = state['event_head']
            guard = 0
            while head != snapshot['event_head']:
                event = connection.execute(
                    'SELECT body,previous_sha256 FROM full_campaign_budget_events '
                    'WHERE attempt_id=? AND sha256=?', (attempt_id, head)).fetchone()
                if event is None or (guard := guard + 1) > 64:
                    raise ValueError('result snapshot identity differs')
                if parse_canonical_json(bytes(event[0]), label='interim event')['kind'] not in (
                        'CAPTURED', 'SIGNING_INTENT', 'SETTLE_WORK'):
                    raise ValueError('result snapshot identity differs')
                head = event[1]
            outcome = validated.outcome
            receipt = encoded(dict(
                schema=RESULT_RECEIPT_SCHEMA, attempt_id=attempt_id, work_id=work_id,
                campaign_id=self.campaigns.row(attempt_id)['campaign_id'],
                aggregate_sha256=validated.aggregate_sha256,
                authentication_sha256=sha256(authentication_bytes), outcome=outcome,
                campaign_state='RESULT_COMMITTED_' + outcome,
                accepted_prefix=list(validated.accepted_prefix),
                campaign_revision=state['authority_revision'],
                authority_head=state['event_head'],
                budget=dict(settled_cpu_ns=state['settled_cpu_ns'],
                            reserved_cpu_ns=state['reserved_cpu_ns'],
                            remaining_cpu_ns=state['remaining_cpu_ns']),
                checkpoints=[dict(checkpoint=name, receipt_sha256=digest_value) for name, digest_value
                             in zip(validated.checkpoints, validated.receipt_digests)],
                signing_at_utc=intent['signing_at_utc'], committed_at_utc=instant(now),
                intent_sha256=sha256(bytes(row[1]))))
            parse_result_receipt(receipt, attempt_id=attempt_id)
            signed = encoded(dict(schema='qualification_campaign_work_transition/v1',
                attempt_id=attempt_id, work_id=work_id, state='SIGNED',
                clock=state['last_clock'], data=dict(
                    candidate_bytes_b64=self.campaigns._b64(receipt))))
            self.record_result_transition(attempt_id, work_id, signed,
                                          expected_revision=state['authority_revision'])
            connection.execute('UPDATE full_campaign_result_intents SET authentication_bytes=?,'
                               'receipt_bytes=? WHERE attempt_id=?',
                               (authentication_bytes, receipt, attempt_id))
            state = self._state(connection, attempt_id)
            self._advance(connection, state, 'RESULT_COMMITTED', authority=True,
                          state_name='RESULT_COMMITTED_' + outcome)
            return encoded(dict(receipt=parse_canonical_json(receipt, label='receipt'),
                                validity=self.campaigns.row(attempt_id)['validity'],
                                historical=False))

    @staticmethod
    def _parse_authentication(raw, *, attempt_id):
        doc = fields(parse_canonical_json(raw, label='result authentication'), {
            'schema', 'attempt_id', 'aggregate_sha256', 'campaign_revision',
            'snapshot_sha256', 'signature'})
        if doc['schema'] != RESULT_AUTHENTICATION_SCHEMA or doc['attempt_id'] != attempt_id:
            raise ValueError('result authentication binding differs')
        digest(doc['aggregate_sha256'])
        digest(doc['snapshot_sha256'])
        integer(doc['campaign_revision'])
        signature = fields(doc['signature'], {'algorithm', 'key_id', 'value_b64'})
        if signature['algorithm'] != 'Ed25519':
            raise ValueError('canonical signing algorithm required')
        return doc

    # -- receipts ---------------------------------------------------------------
    def result_receipt(self, attempt_id):
        """(receipt_bytes, historical, current_validity) -- truthful wrappers.

        A read of a persisted receipt is a historical read: it grants no fresh
        authority, and the current validity is reported as it stands (a later
        VOID flips it; history is preserved)."""
        with self.store.transaction() as connection:
            row = connection.execute('SELECT receipt_bytes FROM full_campaign_result_intents '
                                     'WHERE attempt_id=?', (attempt_id,)).fetchone()
            if row is None or row[0] is None:
                raise ValueError('no committed campaign result')
            receipt_bytes = bytes(row[0])
            parse_result_receipt(receipt_bytes, attempt_id=attempt_id)
            return receipt_bytes, True, self.campaigns.row(attempt_id)['validity']

    def committed_result(self, attempt_id):
        """(result_bytes, authentication_bytes, receipt_bytes) of the committed
        campaign result -- the S7 signing phase's exact input."""
        with self.store.transaction() as connection:
            if connection.execute('PRAGMA user_version').fetchone()[0] < 9:
                raise ValueError('no committed campaign result')
            row = connection.execute('SELECT candidate_bytes,authentication_bytes,receipt_bytes '
                                     'FROM full_campaign_result_intents WHERE attempt_id=?',
                                     (attempt_id,)).fetchone()
            if row is None or row[1] is None or row[2] is None:
                raise ValueError('no committed campaign result')
            return bytes(row[0]), bytes(row[1]), bytes(row[2])

    def seal_eligibility(self, attempt_id):
        """The S7-facing eligibility fact (F3): only a currently-valid
        committed PASS outcome is seal-eligible; a FAIL, an uncommitted result
        or a VOID campaign never is."""
        with self.store.transaction() as connection:
            if connection.execute('PRAGMA user_version').fetchone()[0] < 9:
                return dict(eligible=False, reason='result custody absent', state=None)
            family = self._result_family(connection, attempt_id)
            if family['state'] != 'COMMITTED':
                return dict(eligible=False, reason='no committed campaign result',
                            state=family['state'])
            if family['outcome'] != 'PASS':
                return dict(eligible=False, reason='committed FAIL outcome is never sealed',
                            state='RESULT_COMMITTED_FAIL')
            if self.campaigns.row(attempt_id)['validity'] != 'VALID':
                return dict(eligible=False, reason='VOID campaign', state='RESULT_COMMITTED_PASS')
            # A settlement that ended authority from RESULT_COMMITTED_PASS
            # (the a8a983e rule) leaves the committed receipt historical
            # only; the budget state names the refusal, as the eligibility
            # reader of the predecessor test does.
            state = self._state(connection, attempt_id)
            if state['state'] in REFUSED_BUDGET_STATES:
                return dict(eligible=False, reason=state['state'], state=state['state'])
            return dict(eligible=True, reason=None, state=SEAL_ELIGIBLE_STATE)

    def result_integrity(self, connection):
        """The v9 family walk (offline integrity for the result tables)."""
        for row in connection.execute(
                'SELECT attempt_id,work_id,snapshot_bytes,intent_bytes,candidate_bytes,'
                'authentication_bytes,receipt_bytes FROM full_campaign_result_intents'):
            attempt = row[0]
            intent = parse_result_intent(bytes(row[3]), attempt_id=attempt)
            if intent['work_id'] != row[1] or intent['candidate_sha256'] != sha256(bytes(row[4])):
                raise ValueError('result intent integrity differs')
            parse_result_snapshot(bytes(row[2]), attempt_id=attempt)
            parse_campaign_result(bytes(row[4]), attempt_id=attempt)
            if row[6] is not None:
                if row[5] is None:
                    raise ValueError('committed result authentication absent')
                authentication = self._parse_authentication(bytes(row[5]), attempt_id=attempt)
                receipt = parse_result_receipt(bytes(row[6]), attempt_id=attempt)
                if (receipt['aggregate_sha256'] != sha256(bytes(row[4]))
                        or receipt['authentication_sha256'] != sha256(bytes(row[5]))
                        or authentication['aggregate_sha256'] != sha256(bytes(row[4]))
                        or receipt['intent_sha256'] != sha256(bytes(row[3]))):
                    raise ValueError('result receipt integrity differs')
            elif row[5] is not None:
                raise ValueError('result authentication without a receipt')


# ---------------------------------------------------------------------------
# The guardian body (F4): the metered result unit, launched exactly as the
# N1 G5 unit is (the seam maps manifest role 'result_g5' to this function).


def run_result_g5(context, campaigns, runtime, state, work, enrollment, manifest):
    """Supervise the metered result unit under the work's payload slice.

    Same signature and shape as ``campaign_supervisor._run_n1_g5``: derive the
    unit's bounds from the RESULT phase, launch under the work slice, retain
    the unit's PROCESS identities, settle on exit. The aggregate itself is the
    unit's own work over the service socket; credit follows the persisted
    candidate, never the unit's exit status alone.
    """
    from . import campaign_supervisor as supervisor
    from .runtime import installed_code_root
    import sys
    import time
    results = ResultStore(campaigns)
    deadline = min(state['deadline_boottime_ns'],
                   parse_canonical_json(decode_base64(work['reservation_bytes_b64']),
                                        label='reservation')['clock']['boottime_ns']
                   + work['limits']['wall_ns'])
    now_clock = supervisor.clock(supervisor.observe_campaign_clock())
    remaining_wall_ns = deadline - now_clock['boottime_ns']
    spec = supervisor.g5_unit_spec(enrollment['scopes'], attempt_id=state['attempt_id'],
        work_id=work['work_id'], code_root=str(installed_code_root()),
        interpreter=sys.executable, g5_uid=context.config['g5_uid'],
        orchestration_cpu_ns=state['profile']['orchestration_cpu_ns'][work['phase']],
        remaining_wall_ns=remaining_wall_ns, cpu_ns=work['limits']['cpu_ns'])
    unit = enrollment['scopes']['payload_slice'][:-6] + '-result-g5.service'
    with campaigns.launch_gate(state['attempt_id'], work['work_id'],
                               supervisor.observe_campaign_clock, role='payload') as permit:
        supervisor._guardian_bus_call(campaigns, unit, spec['g5'])
    campaigns.acknowledge_dispatch(state['attempt_id'], work['work_id'], 'payload',
                                   permit['token'], supervisor.observe_campaign_clock)
    group = supervisor._scope_path(runtime.parent, enrollment['scopes']['payload_slice']) / unit
    seen = set()
    while True:
        current = parse_canonical_json(results.result_state_bytes(state['attempt_id']),
                                       label='current result authority')
        supervisor._assert_authority(current)
        if not group.exists() or supervisor._kernel_pairs(
                supervisor._read_counter(group / 'cgroup.events')).get('populated') == 0:
            break
        for pid_text in supervisor._payload_processes(group):
            if pid_text in seen:
                continue
            observed_identity = supervisor._process_identity(pid_text)
            if observed_identity is None:
                continue
            birth, uid, cgroup, comm, exe = observed_identity
            if uid != context.config['g5_uid']:
                raise ValueError('result unit role UID differs')
            results.retain_result_supervision_event(encoded(dict(
                schema='qualification_campaign_supervision_event/v2',
                attempt_id=state['attempt_id'], work_id=work['work_id'], kind='PROCESS',
                clock=supervisor.clock(supervisor.observe_campaign_clock()),
                data=dict(pid=int(pid_text), start_ticks=birth, uid=uid, cgroup=cgroup,
                          comm=comm, exe=exe))))
            seen.add(pid_text)
        time.sleep(.2)
    state = parse_canonical_json(results.result_state_bytes(state['attempt_id']),
                                 label='result final state')
    work = campaigns._work(state, work['work_id'])
    if work['state'] == 'RUNNING':
        # The unit ended without a persisted candidate: durable uncertainty.
        running = encoded(dict(schema='qualification_campaign_work_transition/v1',
            attempt_id=state['attempt_id'], work_id=work['work_id'], state='IN_DOUBT',
            clock=state['last_clock'], data={}))
        results.record_result_transition(state['attempt_id'], work['work_id'], running,
                                         expected_revision=state['authority_revision'])
        state = parse_canonical_json(results.result_state_bytes(state['attempt_id']),
                                     label='result in-doubt')
        work = campaigns._work(state, work['work_id'])
    observed = runtime.observation(state, work, enrollment)
    state = parse_canonical_json(results.settle_result_work(
        state['attempt_id'], work['work_id'], observed), label='result settlement')
    work = campaigns._work(state, work['work_id'])
    with campaigns.store.transaction() as connection:
        family = results._result_family(connection, state['attempt_id'])
    # The committing work completes in the state its own commit produced; a
    # settlement that ended authority (overrun/uncertain) skips the
    # completion -- the receipt is history and the store would refuse it
    # (S3's _run_n1_g5 tail guard, a8a983e shape).
    if (work['state'] == 'SIGNED' and state['validity'] == 'VALID'
            and family['state'] == 'COMMITTED'
            and state['state'] in results._completion_states(work)):
        completed = encoded(dict(schema='qualification_campaign_work_transition/v1',
            attempt_id=state['attempt_id'], work_id=work['work_id'], state='COMPLETED',
            clock=state['last_clock'], data={}))
        results.record_result_transition(state['attempt_id'], work['work_id'], completed,
                                         expected_revision=state['authority_revision'])
