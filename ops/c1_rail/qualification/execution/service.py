"""Protected supervisor: the only active journal and container authority."""
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import os
from pathlib import Path
import socket
import struct
import subprocess
import sys
import threading
import time
import traceback

from ..contract import canonical_json_bytes as encoded, parse_canonical_json, verify_detached_approval
from .admission import verify_bundle, verify_retained_bundle
from .archive import archive_capture
from .evidence import parse_worker_result
from .files import fsync_directory, read_regular
from .g5 import validate_result_envelope_v2
from .keys import load_keys
from .launcher import create_worker, find_owned_worker, inspect_worker, start_and_capture, stop_owned_worker
from .plan import derive_n1_plan, derive_campaign_plan_from_context
from .preflight import build_binding
from .protocol import decode_base64, encode_frame, fields, parse_request, sha256
from .signing import sign_captured
from .store import ExecutionStore
from .transport import receive
from .verification import utc_instant, verify_role_signature

RPC_CONNECTION_LIMIT = 16
SCHEDULE_SCHEMA = 'qualification_campaign_schedule_request/v1'
SCHEDULE_BYTE_LIMIT = 1024  # framing bound for the service-peer private route
EXECUTABLE_DIAGNOSTIC_RELEASE = 'qualification_execution_release/v4'

def now():
    return datetime.now(timezone.utc)


class BoundedConnections:
    """Bound both active handlers and pending admission, never an unbounded queue."""
    def __init__(self,handler,*,limit):
        self.handler=handler
        self.slots=threading.BoundedSemaphore(limit)
        self.pool=ThreadPoolExecutor(max_workers=limit,thread_name_prefix='qualification-rpc')

    def submit(self,connection):
        self.slots.acquire()
        try:
            result=self.pool.submit(self.handler,connection)
        except BaseException:
            self.slots.release()
            raise
        result.add_done_callback(lambda _:self.slots.release())
        return result

    def __enter__(self):
        return self

    def __exit__(self,*exc):
        self.pool.shutdown(wait=True)


def permitted(role, operation):
    return operation in {'client': {'SUBMIT_N1', 'STATUS', 'FETCH'},
        'g5': {'STATUS', 'FETCH', 'SNAPSHOT', 'STORE_ARTIFACT', 'STORE_RESULT', 'COMMIT_N1_RESULT'},
        'operator': {'STATUS', 'VOID'}}.get(role, set())


def uid_roles(config):
    values = [config[key] for key in ('client_uid', 'g5_uid', 'operator_uid', 'service_uid')]
    if any(type(value) is not int or value < 0 for value in values) or len(set(values)) != 4:
        raise ValueError('four distinct OS identities required')
    return dict(zip(values, ('client', 'g5', 'operator', 'service')))


def schedule_eligibility(release, profile):
    """Fixed at startup: the execution-capable diagnostic revisions open the
    funded route for harmless probe work. The /v5 dispatch revision is a
    superset of /v4: it keeps every v4 restriction for probes and additionally
    admits the two dispatch roles through its own gate."""
    pairs = ((EXECUTABLE_DIAGNOSTIC_RELEASE, 'qualification_execution_profile/v4'),
             (release_schema.DISPATCH_DIAGNOSTIC_RELEASE, 'qualification_execution_profile/v5'))
    return (type(release) is dict and release.get('capability') == 'FULL_E1'
            and (release.get('schema'), profile.values['schema']) in pairs)


def dispatch_eligibility(release, profile):
    """Fixed at startup: only the S3 dispatch revision (D4) admits N1 dispatch roles."""
    return (type(release) is dict and release.get('schema') == release_schema.DISPATCH_DIAGNOSTIC_RELEASE
            and release.get('capability') == 'FULL_E1' and release.get('dispatch_enabled') is True
            and release.get('dispatch_checkpoints') == ['N1']
            and profile.values['schema'] == 'qualification_execution_profile/v5')


def _write(root, relative, raw):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    with path.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    path.chmod(0o444)


class ExecutionService:
    def __init__(self, config):
        from .runtime import protected_path
        import stat
        self.config = config
        self.roles = uid_roles(config)
        self.root = Path(config['data_root'])
        self.installation = Path(config['installation_root'])
        for name in ('release.json', 'keys.json', 'release-approval.json'):
            protected_path(self.installation / name)
        info = self.root.lstat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != config['service_uid']
                or stat.S_IMODE(info.st_mode) != 0o700):
            raise ValueError('service-owned private data root required')
        for parent in self.root.parents:
            protected_path(parent)
        socket_parent = Path(config['socket_path']).parent
        info = socket_parent.lstat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != config['service_uid']
                or info.st_gid != config['socket_gid'] or info.st_mode & 0o027
                or not info.st_mode & stat.S_ISGID):
            raise ValueError('protected service socket directory required')
        self.release = read_regular(self.installation, 'release.json', limit=16 * 1024 * 1024)
        from .profile import parse_profile
        release = parse_canonical_json(self.release, label='installed release')
        self.profile = parse_profile(encoded(release['profile']))
        self.authority = release['authority_class']
        # Private scheduler eligibility is fixed at startup from the installed
        # release; no request re-reads or re-parses the release to decide it.
        self.schedule_eligible = schedule_eligibility(release, self.profile)
        self.dispatch_eligible = dispatch_eligibility(release, self.profile)
        self.store = ExecutionStore(self.root / 'journal.sqlite', installation_dir=self.installation)
        self.dispatch_lock = threading.Lock()
        self.recovery_issues = {}
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='qualification-execution')

    def keys(self):
        return load_keys(read_regular(self.installation, 'keys.json', limit=1024 * 1024), authority_class=self.authority)

    def _context(self, bundle_digest, *, at):
        context = verify_bundle(self.root / 'bundles' / bundle_digest, self.release, self.keys(), at)
        if context.bundle_sha256 != bundle_digest or context.domain.authority_class != 'TEST_ONLY':
            raise ValueError('protected release forbids production execution or substituted bundle')
        return context

    def handle_request(self, peer_uid, request_bytes):
        wire = parse_canonical_json(request_bytes, label='request')
        if type(wire) is dict and wire.get('schema') == SCHEDULE_SCHEMA:
            return self._schedule_request(peer_uid, request_bytes)
        if type(wire) is dict and 'schema' in wire:
            return self._campaign_request(peer_uid, request_bytes)
        request = parse_request(request_bytes)
        operation, attempt = request['operation'], request['attempt_id']
        role = self.roles.get(peer_uid)
        if not permitted(role, operation):
            raise ValueError('PEER_NOT_AUTHORIZED')
        if operation == 'SUBMIT_N1':
            if parse_canonical_json(self.release, label='release')['capability'] != 'N1_ONLY':
                raise ValueError('N1 submit requires N1_ONLY release')
            with self.dispatch_lock:
                with self.store.transaction():
                    admitted_at = now()
                    context = self._context(request['bundle_sha256'],at=admitted_at)
                    if context.attempt_id != attempt:
                        raise ValueError('approved attempt identity differs')
                    plan = derive_n1_plan(context.contract, attempt_id=attempt,
                        exact_depth_approval_sha256=context.exact_depth_approval.approval_sha256)
                    try:
                        self.store.status(attempt)
                        existed = True
                    except KeyError:
                        existed = False
                    record = self.store.reserve(request_bytes, plan, now=admitted_at)
                    self.store.archive_object(record.execution_id,'preflight',build_binding(context,record,plan))
                    self.store.archive_object(record.execution_id, 'bundle_index', context.retained_bundle_index)
                    for name, raw in context.retained_bytes.items():
                        self.store.archive_object(record.execution_id, 'context_' + name, raw)
                if not existed:
                    self.executor.submit(self._execute, record.execution_id)
                return self.store.status(attempt)
        status = parse_canonical_json(self.store.status(attempt), label='status')
        execution_id = status['execution_id']
        if operation == 'STATUS':
            issue = getattr(self,'recovery_issues',{}).get(execution_id)
            if issue is not None:
                status['recovery_issue'] = issue
            if status.get('result_sha256'):
                status['current_policy_eligible'] = self._eligible(execution_id)
            return encoded(status)
        if operation == 'SNAPSHOT':
            return self.store.snapshot_for_assessment(attempt)
        if operation == 'STORE_ARTIFACT':
            raw = decode_base64(request['bytes_b64'])
            if len(raw) > self.profile.output_byte_limit:
                raise ValueError('artifact exceeds profile limit')
            return encoded(dict(artifact_sha256=self.store.store_proposed_artifact(attempt,request['role'],raw)))
        if operation == 'FETCH':
            if role == 'client':
                with self.store.transaction() as connection:
                    roles = {row[0] for row in connection.execute('SELECT role FROM execution_objects WHERE execution_id=? AND sha256=?',
                        (execution_id, request['object_sha256']))}
                if not roles.intersection({'attestation','preflight'}):
                    raise ValueError('ARTIFACT_PRIVATE')
            try:
                return self.store.fetch(attempt, request['object_sha256'])
            except ValueError:
                if role != 'g5': raise
                return self.store.fetch_candidate(attempt,request['object_sha256'])
        if operation == 'STORE_RESULT':
            raw = decode_base64(request['envelope_bytes_b64'])
            if len(raw) > self.profile.output_byte_limit:
                raise ValueError('result exceeds profile limit')
            result_digest = self.store.store_proposed_result(attempt,raw)
            return encoded(dict(envelope_sha256=result_digest))
        if operation == 'COMMIT_N1_RESULT':
            return self._commit(attempt, execution_id, request)
        if operation == 'VOID':
            with self.store.transaction():
                enrollment, keys = self.store.cancellation_enrollment(execution_id)
                current = now()
                approval_raw = decode_base64(request['operator_approval_bytes'])
                subject = sha256(encoded(dict(attempt_id=attempt, reason=request['reason'], contract_sha256=enrollment['contract_sha256'])))
                approval = verify_detached_approval(approval_raw, trusted_keys=keys,
                    expected_scope='VOID_QUALIFICATION_ATTEMPT', expected_subject_sha256=subject,
                    expected_contract_sha256=enrollment['contract_sha256'], now=current,
                    allow_test_authority=enrollment['authority_class'] == 'TEST_ONLY')
                if (approval.key_id not in enrollment['freeze_key_ids']
                        or approval.authority_class != enrollment['authority_class']
                        or sha256(keys[approval.key_id].public_key) != enrollment['trusted_key_sha256'][approval.key_id]):
                    raise ValueError('VOID authority is not enrolled')
                receipt = self.store.void(attempt, request['reason'], approval_raw, now=current)
            if status['container_id']:
                self._stop_recovering(status['container_id'],execution_id)
            return receipt
        raise ValueError('UNKNOWN_OPERATION')

    def _campaign_request(self, peer_uid, raw):
        request = campaign_protocol.parse_campaign_request(raw)
        operation, attempt = request['operation'], request['attempt_id']
        if not campaign_protocol.permitted(self.roles.get(peer_uid), operation):
            raise ValueError('PEER_NOT_AUTHORIZED')
        release = release_schema.parse_release(self.release)
        if release['capability'] != 'FULL_E1':
            raise ValueError('FULL_E1 installed release required')
        campaigns = campaign_store.CampaignStore(self.store)
        if release['schema'] in ('qualification_execution_release/v3', EXECUTABLE_DIAGNOSTIC_RELEASE,
                                 release_schema.DISPATCH_DIAGNOSTIC_RELEASE):
            if operation == 'SUBMIT_E1' and request['schema'] != 'qualification_campaign_request/v2':
                raise ValueError('fresh versioned diagnostic admission required')
            if request['schema'] != 'qualification_campaign_request/v2':
                raise ValueError('diagnostic installation requires versioned historical requests')
            if request['schema'] == 'qualification_campaign_request/v2':
                return self._diagnostic_campaign_request(campaigns, request, raw, release)
        elif request['schema'] == 'qualification_campaign_request/v2':
            raise ValueError('installed diagnostic release required')
        with self.store.transaction():
            if operation == 'SUBMIT_E1':
                status = campaigns.retry(raw)
                if status is None:
                    context = self._context(request['bundle_sha256'], at=now())
                    if context.attempt_id != attempt:
                        raise ValueError('approved campaign attempt differs')
                    plan = derive_campaign_plan_from_context(context)
                    # Plan materialization takes time. Revalidate the retained exact
                    # inputs at commit time; a fresh staging read cannot replace them.
                    admitted_at = now()
                    context = verify_retained_bundle(context.retained_bundle_index,
                        context.retained_bytes, self.release, self.keys(), admitted_at)
                    status = campaigns.admit(raw, context, plan, now=admitted_at)
            elif operation == 'STATUS':
                status = campaigns.status(attempt)
            elif operation == 'FETCH_PLAN_CHUNK':
                return campaigns.chunk(request)
            elif operation == 'VOID':
                retry = campaigns.void_retry(raw)
                if retry is not None:
                    return retry
                objects = campaigns.objects(attempt)
                domain = parse_canonical_json(objects['context_trust_domain'], label='original enrollment')
                contract_sha = campaigns.status(attempt)['receipt']['contract_sha256']
                keys = self.keys()
                approval = verify_detached_approval(decode_base64(request['operator_approval_bytes']),
                    trusted_keys=keys, expected_scope='VOID_QUALIFICATION_ATTEMPT',
                    expected_subject_sha256=sha256(encoded(dict(attempt_id=attempt,
                        reason=request['reason'], contract_sha256=contract_sha))),
                    expected_contract_sha256=contract_sha, now=now(), allow_test_authority=True)
                if (approval.authority_class != 'TEST_ONLY' or approval.key_id not in domain['freeze_key_ids']
                        or sha256(keys[approval.key_id].public_key) != domain['trusted_key_sha256'][approval.key_id]):
                    raise ValueError('VOID authority is not enrolled')
                return campaigns.void(raw, now=now())
            eligible = False
            if status['validity'] == 'VALID':
                try:
                    campaigns.context(attempt, self.release, self.keys(), now=now())
                    eligible = True
                except (ValueError, KeyError, OSError):
                    pass
            status['current_policy_eligible'] = eligible
            return encoded(status)

    def _diagnostic_campaign_request(self, campaigns, request, raw, release):
        operation, attempt = request['operation'], request['attempt_id']
        if operation == 'SUBMIT_E1':
            with self.dispatch_lock, campaign_supervisor.controller_cpu_guard():
                try:
                    existing = campaigns.row(attempt)
                except KeyError:
                    existing = None
                manifest = encoded(dict(schema='qualification_campaign_work_manifest/v1', attempt_id=attempt,
                    work_id='admission', role='admission', probe='noop'))
                # Attempts whose first launch this process has already delegated to
                # completion: an exact retry after that never resamples the clock
                # or re-enters the launcher (the work is no longer RESERVED). The
                # set is process-local, so a restart keeps the resume path below.
                delegated = self.__dict__.setdefault('delegated_admissions', set())
                if existing is not None:
                    if bytes(existing['request_bytes']) != raw:
                        raise ValueError('immutable diagnostic admission request differs')
                    if attempt in delegated:
                        return encoded(campaigns.diagnostic_status(attempt))
                    # An exact retry resumes a structurally absent RESERVED admission
                    # (service died after begin_admission, before the start intent):
                    # nothing was started, so the first launch is still safe and
                    # happens at most once (prepare_campaign_work retains START_INTENT
                    # before any OS effect; run_campaign_work returns status for any
                    # other work state). Every other existing state is status only.
                    unstarted = campaigns.inspect_unstarted_admission(attempt, campaign_supervisor.observe_campaign_clock)
                    if unstarted is None or not unstarted['resumable']:
                        return encoded(campaigns.diagnostic_status(attempt))
                    reservation = unstarted['reservation_bytes']
                else:
                    state = parse_canonical_json(campaigns.begin_admission(raw,
                        encoded(release['campaign_budget_profile']), campaign_supervisor.observe_campaign_clock()), label='provisional budget')
                    reservation = decode_base64(state['works'][0]['reservation_bytes_b64'])
                result = campaign_supervisor.run_campaign_work(self, reservation, manifest)
                delegated.add(attempt)
                return result
        if operation == 'STATUS':
            return encoded(campaigns.diagnostic_status(attempt))
        if operation == 'FETCH_PLAN_CHUNK':
            if campaigns.diagnostic_status(attempt)['receipt'] is None:
                raise ValueError('diagnostic admission has no retained plan')
            return campaigns.chunk(request)
        if operation in campaign_protocol.CHECKPOINT_OPERATIONS:
            if not self.dispatch_eligible:
                raise ValueError('installed N1 dispatch release required')
            if operation == 'CHECKPOINT_SNAPSHOT':
                return campaigns.checkpoint_snapshot(attempt)
            if operation == 'FETCH_CHECKPOINT_MEMBER':
                return campaigns.fetch_checkpoint_member(attempt, request['object_sha256'],
                                                         request['offset'], request['length'])
            if operation == 'STAGE_CHECKPOINT_ARTIFACT':
                raw = decode_base64(request['bytes_b64'])
                if len(raw) > self.profile.output_byte_limit:
                    raise ValueError('artifact exceeds profile limit')
                return encoded(dict(artifact_sha256=campaigns.stage_checkpoint_artifact(
                    attempt, request['role'], raw)))
            return self._commit_checkpoint(campaigns, attempt, request)
        if operation == 'VOID':
            # (i) Cheap bounded transport, unmetered: the exact historical retry,
            # single-body byte-bounded queueing and compact status. Serialized
            # with the funded producers so a queued body never races a claim
            # already in flight; a pre-admission body waits for the admission
            # guardian, which authenticates it under its own charged work.
            with self.dispatch_lock:
                with self.store.transaction():
                    retry = campaigns.void_retry(raw)
                    if retry is not None:
                        return retry
                    status = campaigns.queue_diagnostic_void(raw)
                    if parse_canonical_json(status, label='status')['receipt'] is None:
                        return status
                # (ii) Signature verification runs only inside a durably funded,
                # guarded, one-use controller operation charged to the original
                # allowance. A refused claim returns status with the body still
                # queued; a failed verification retains its refusal, clears the
                # body and is never refunded.
                with campaign_supervisor.controller_cpu_guard():
                    sequence, status = campaigns.claim_void_authentication(raw, campaign_supervisor.observe_campaign_clock())
                    if sequence is None:
                        return status
                    try:
                        domain = parse_canonical_json(campaigns.retained_object(attempt, 'context_trust_domain'), label='original enrollment')
                        contract_sha = campaigns.diagnostic_status(attempt)['receipt']['contract_sha256']
                        keys = self.keys()
                        approval = verify_detached_approval(decode_base64(request['operator_approval_bytes']),
                            trusted_keys=keys, expected_scope='VOID_QUALIFICATION_ATTEMPT',
                            expected_subject_sha256=sha256(encoded(dict(attempt_id=attempt,
                                reason=request['reason'], contract_sha256=contract_sha))),
                            expected_contract_sha256=contract_sha, now=now(), allow_test_authority=True)
                        if (approval.authority_class != 'TEST_ONLY' or approval.key_id not in domain['freeze_key_ids']
                                or sha256(keys[approval.key_id].public_key) != domain['trusted_key_sha256'][approval.key_id]):
                            raise ValueError('VOID authority is not enrolled')
                    except (ValueError, KeyError) as refusal:
                        campaigns.refuse_void_authentication(raw, sequence, str(refusal)[:1024],
                                                             campaign_supervisor.observe_campaign_clock())
                        raise
                    return campaigns.complete_void_authentication(raw, sequence, now=now())
        raise ValueError('UNKNOWN_OPERATION')

    def _commit_checkpoint(self, campaigns, attempt, request):
        """COMMIT_CHECKPOINT_ASSESSMENT under the service lock.

        T1 persists the g5 work's CAPTURED + SIGNING_INTENT and the durable
        candidate; T2 independently re-validates the candidate against the
        service's own retained context and reconstruction, then commits. An
        exact retry returns the identical receipt with no fresh time/signature.
        """
        import base64
        from ..checkpoint_plan import derive_checkpoint_plan
        from .campaign_store import (parse_checkpoint_assessment, parse_checkpoint_cutoff,
            CHECKPOINT_INTENT_SCHEMA)
        from .g5 import validate_campaign_checkpoint, verify_checkpoint_assessment
        from .store import instant
        work_id = request['work_id']
        candidate_bytes = decode_base64(request['candidate_bytes_b64'])
        candidate = parse_checkpoint_assessment(candidate_bytes, attempt_id=attempt)
        with self.dispatch_lock:
            with self.store.transaction() as connection:
                row = connection.execute('SELECT snapshot_bytes,intent_bytes,candidate_bytes,receipt_bytes '
                    'FROM full_campaign_checkpoint_intents WHERE attempt_id=?', (attempt,)).fetchone()
            if row is None:
                snapshot_bytes = campaigns.checkpoint_snapshot(attempt)
                signing_at = instant(now())
                intent_bytes = encoded(dict(schema=CHECKPOINT_INTENT_SCHEMA, attempt_id=attempt,
                    checkpoint='N1', work_id=work_id, key_id=candidate['signature']['key_id'],
                    signing_at_utc=signing_at, candidate_sha256=sha256(candidate_bytes),
                    snapshot_sha256=sha256(snapshot_bytes)))
                capture = encoded(dict(schema='qualification_campaign_g5_capture/v1', attempt_id=attempt,
                    checkpoint='N1', work_id=work_id, candidate_sha256=sha256(candidate_bytes),
                    staged=[dict(role=row2['role'], sha256=row2['sha256']) for row2 in request['artifacts']]))
                capture_transition = encoded(dict(
                    schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id=work_id,
                    state='CAPTURED', clock=parse_canonical_json(campaign_supervisor.observe_campaign_clock(), label='clock'),
                    data=dict(capture_bytes_b64=base64.b64encode(capture).decode('ascii'))))
                signing_transition = encoded(dict(
                    schema='qualification_campaign_work_transition/v1', attempt_id=attempt, work_id=work_id,
                    state='SIGNING_INTENT', clock=parse_canonical_json(campaign_supervisor.observe_campaign_clock(), label='clock'),
                    data=dict(intent_id=work_id + '-intent', payload_bytes_b64=base64.b64encode(candidate_bytes).decode('ascii'),
                              key_id=candidate['signature']['key_id'], signing_at_utc=signing_at)))
                campaigns.persist_checkpoint_intent(attempt, work_id, snapshot_bytes, intent_bytes,
                    candidate_bytes, capture_transition, signing_transition)
            elif bytes(row[2]) != candidate_bytes:
                raise ValueError('exact checkpoint candidate retry required')
            # T2: the service re-validates against its own retained context.
            context = campaigns.context(attempt, self.release, self.keys(), now=now())
            keys = self.keys()
            verify_checkpoint_assessment(candidate_bytes, context=context, current_keys=keys)
            family = campaigns.checkpoint_capture(attempt)
            # The candidate was bound at T1 to that moment's snapshot; T2 re-validates
            # against exactly those persisted bytes, and the store checks freshness
            # (current revision/head) inside the commit transaction. The row is
            # (snapshot_bytes, intent_bytes, candidate_bytes, cutoff, receipt).
            snapshot_bytes = bytes(row[0]) if row is not None else snapshot_bytes
            plan_bytes = derive_checkpoint_plan(campaigns.retained_object(attempt, 'plan'), 'N1', None)
            evidence = validate_campaign_checkpoint(context, checkpoint='N1', plan_bytes=plan_bytes,
                attestation_bytes=family['attestation_bytes'],
                artifacts={'result': family['result_bytes'], 'worker_result': family['payload_bytes']},
                snapshot_bytes=snapshot_bytes, current_keys=keys)
            core = parse_canonical_json(candidate_bytes, label='candidate')
            unsigned = {name: value for name, value in core.items() if name != 'signature'}
            if encoded(unsigned) != evidence.assessment_bytes:
                raise ValueError('checkpoint candidate differs from canonical reconstruction')
            from ..evidence import compare_checkpoint_evidence, InspectedEvidence
            compare_checkpoint_evidence(InspectedEvidence(evidence.assessment_bytes, evidence.output_bytes_by_role),
                expected=InspectedEvidence(evidence.assessment_bytes, evidence.output_bytes_by_role))
            staged = {row2['role']: row2['sha256'] for row2 in request['artifacts']}
            if staged != {role: sha256(raw) for role, raw in evidence.output_bytes_by_role.items()}:
                raise ValueError('staged checkpoint artifact inventory differs')
            with self.store.transaction() as connection:
                for role, digest_value in staged.items():
                    if connection.execute('SELECT 1 FROM full_campaign_checkpoint_staged '
                            'WHERE attempt_id=? AND role=? AND sha256=?', (attempt, role, digest_value)).fetchone() is None:
                        raise ValueError('staged checkpoint artifact membership differs')
            cutoff_bytes = encoded(dict(schema='qualification_campaign_cutoff_receipt/v1',
                attempt_id=attempt, checkpoint='N1', assessment_sha256=sha256(candidate_bytes),
                decision=core['decision'], n1_cutoffs=core['cutoff']['n1_cutoffs'],
                n2_thresholds=core['n2_thresholds']['stages'],
                n2_bound_to=sha256(candidate_bytes), created_utc=instant(now())))
            parse_checkpoint_cutoff(cutoff_bytes, attempt_id=attempt)
            return campaigns.commit_checkpoint_assessment(attempt, work_id, candidate_bytes,
                cutoff_bytes, now=now(), clock_bytes=campaign_supervisor.observe_campaign_clock())

    def _schedule_request(self, peer_uid, raw):
        """Closed private route: the warm service is the only campaign intent producer.

        Nothing campaign-specific is imported, constructed or launched until
        claim_scheduler_bootstrap has durably funded this one-use operation from
        the original allowance. A refused or duplicate claim returns compact
        historical status and has no effect; only the returned token proceeds to
        materialization and then to the prepared-launch tail. The 1 s / 10 s
        controller guard consumes START_OWNER's existing allowance.
        """
        if peer_uid != self.config['service_uid']:
            raise ValueError('PEER_NOT_AUTHORIZED')
        request = campaign_funding.parse_request(raw)
        if request['role'] in campaign_funding.DISPATCH_ROLES:
            # D4: genuine dispatch needs the installed /v5 release; the harmless
            # probe dispatch keeps the unchanged v4 gate.
            if not self.dispatch_eligible:
                raise ValueError('installed N1 dispatch release required')
        elif not self.schedule_eligible:
            raise ValueError('installed execution-capable diagnostic release required')
        campaigns = campaign_store.CampaignStore(self.store)
        with self.dispatch_lock, campaign_supervisor.controller_cpu_guard():
            token, status = campaigns.claim_scheduler_bootstrap(raw, campaign_supervisor.observe_campaign_clock())
            if token is None:
                return status
            reservation, enrollment = campaigns.materialize_scheduler_bootstrap(
                request['attempt_id'], request['work_id'], token, self.config['host_run_id'])
            return campaign_supervisor.launch_prepared_campaign_work(self, reservation, enrollment)

    def _eligible(self, execution_id):
        try:
            context, _ = self.store.context(execution_id, now=now())
            status = parse_canonical_json(self.store.status(context.attempt_id),label='status')
            return status['validity'] == 'VALID' and context.domain.authority_class == 'TEST_ONLY'
        except (ValueError,KeyError,OSError):
            return False

    def _commit(self, attempt, execution_id, request):
        authentication = decode_base64(request['authentication_bytes'])
        with self.store.transaction():
            retry = self.store.retry_assessment(attempt,request['envelope_sha256'],authentication)
            if retry is not None:
                response = parse_canonical_json(retry,label='historical receipt')
                response['current_policy_eligible'] = self._eligible(execution_id)
                return encoded(response)
            status = parse_canonical_json(self.store.status(attempt),label='status')
            context, keys = self.store.context(execution_id,now=now())
            result = self.store.fetch_candidate(attempt,request['envelope_sha256'])
            auth = fields(parse_canonical_json(authentication,label='authentication'),{'schema','payload','signature'})
            doc = parse_canonical_json(result,label='result')
            expected = dict(schema='qualification_result_authentication_payload/v2',scope='ATTEST_E1_RESULT',
                authority_class=context.domain.authority_class,attempt_id=attempt,
                contract_sha256=context.contract.contract_sha256,trust_domain_sha256=context.domain.sha256,
                journal_revision=doc['journal_revision'],result_sha256=sha256(result))
            if auth['schema'] != 'qualification_result_authentication/v2' or encoded(auth['payload']) != encoded(expected):
                raise ValueError('result authentication scope differs')
            verify_role_signature(auth,context=context,current_keys=keys,role='result')
            attestation = self.store.fetch(attempt,status['attestation_sha256'])
            payload = parse_canonical_json(attestation,label='attestation')['payload']
            artifacts = {item['sha256']:self.store.fetch(attempt,item['sha256']) for item in payload['artifacts']}
            outputs = {item['role']:self.store.fetch_candidate(attempt,item['sha256']) for item in doc['outputs']}
            snapshot = self.store.snapshot_for_assessment(attempt)
            evidence = validate_result_envelope_v2(context,result,attestations={'N1':attestation},artifacts=artifacts,
                output_bytes_by_role=outputs,expected_attempt_id=attempt,current_keys=keys,
                expected_revision=status['revision'],journal_snapshot_bytes=snapshot)
            # Reconstruction can outlive approval or key authority. Validate the
            # exact instant retained in the first commit, using freshly loaded keys.
            committed_at = now()
            context, keys = self.store.context(execution_id,now=committed_at)
            verify_role_signature(auth,context=context,current_keys=keys,role='result')
            response = parse_canonical_json(self.store.commit_assessment(evidence,authentication,now=committed_at),label='commit receipt')
            response['current_policy_eligible'] = True
            return encoded(response)
    def _execute(self, execution_id):
        container = None
        try:
            context, _ = self.store.context(execution_id, now=now())
            status = parse_canonical_json(self.store.status(context.attempt_id), label='status')
            plan = self.store.fetch(context.attempt_id, status['plan_sha256'])
            input_root = self.root / 'inputs' / execution_id
            input_root.mkdir(parents=True, mode=0o755, exist_ok=False)
            _write(input_root, 'plan.json', plan)
            _write(input_root, 'installation/release.json', self.release)
            _write(input_root, 'installation/keys.json', read_regular(self.installation, 'keys.json', limit=1024 * 1024))
            _write(input_root, 'bundle/index.json', context.retained_bundle_index)
            index = parse_canonical_json(context.retained_bundle_index, label='index')
            for item in index['entries']:
                _write(input_root, 'bundle/' + item['path'], context.retained_bytes[item['role']])
            fsync_directory(input_root)
            daemon_input = Path(self.config['daemon_data_root']) / 'inputs' / execution_id
            container = create_worker(context, execution_id=execution_id, input_dir=daemon_input, profile=self.profile,
                                      host_run_id=self.config['host_run_id'])
            inspected = parse_canonical_json(inspect_worker(container, context=context, profile=self.profile,
                host_run_id=self.config['host_run_id']), label='inspection')
            if inspected['execution_id'] != execution_id or inspected['input_source'] != str(daemon_input):
                raise ValueError('created container binding differs')
            record = self.store.record_container(execution_id, container, expected_revision=status['revision'])
            authorized = now()
            with self.store.transaction():
                context, _ = self.store.context(execution_id, now=authorized)
                record = self.store.record_start_intent(execution_id, expected_revision=record.revision, now=authorized)
            with ThreadPoolExecutor(max_workers=1) as capture_executor:
                capture_future = capture_executor.submit(start_and_capture, container, spool_dir=self.root / 'spool' / execution_id,
                    profile=self.profile, maximum_wall_seconds=context.contract.replay.budget.maximum_wall_seconds)
                while True:
                    inspected = parse_canonical_json(inspect_worker(container, context=context, profile=self.profile,
                        host_run_id=self.config['host_run_id']), label='inspection')
                    state = inspected['state']
                    if state['StartedAt'] and not state['StartedAt'].startswith('0001-'):
                        break
                    if capture_future.done():
                        capture_future.result()
                        raise ValueError('daemon start instant absent')
                    time.sleep(0.1)
                # Actual start must independently satisfy the approval interval.
                self.store.context(execution_id, now=utc_instant(state['StartedAt']))
                record = self.store.record_running(execution_id, expected_revision=record.revision, now=now())
                capture = capture_future.result()
            artifacts = archive_capture(capture, archive_dir=self.store.archive_dir)
            output = next(iter(artifacts.values()))
            parsed = parse_worker_result(output, context=context, execution_id=execution_id, plan_bytes=plan)
            self.store.archive_object(execution_id, 'worker_result', output)
            inspected = parse_canonical_json(inspect_worker(container, context=context, profile=self.profile,
                host_run_id=self.config['host_run_id']), label='inspection')
            state = inspected['state']
            facts = encoded(dict(schema='qualification_capture/v1', container_id=container,
                service_id=context.domain.execution_service_id, profile_sha256=self.profile.sha256,
                runtime_manifest_sha256=context.release.runtime_sha256('worker'),
                worker_image_digest=inspected['image'], authorized_at_utc=authorized.isoformat().replace('+00:00', 'Z'),
                started_utc=state['StartedAt'], completed_utc=state['FinishedAt'],
                artifacts=[dict(role=role, sha256=sha256(raw), byte_length=len(raw)) for role, raw in [('plan', plan), ('worker_result', output)]],
                observations=dict(exit_code=capture.exit_code, oom_killed=capture.oom_killed,
                    supervisor_wall_ns=capture.supervisor_wall_ns, **parsed.document['observations'])))
            self.store.record_capture(execution_id, facts, expected_revision=record.revision)
            sign_captured(execution_id, store=self.store, credential_reference=self.config['execution_credential'])
        except Exception as exc:
            row = next(row for row in self.store.execution_rows() if row['execution_id'] == execution_id)
            if row['state'] in ('DISPATCHED', 'START_INTENT', 'RUNNING'):
                self.store.record_abort(execution_id, type(exc).__name__ + ': ' + str(exc)[:500], uncertain=True)
            if container:
                self._stop_recovering(container,execution_id)
            # CAPTURED failures remain durable and cannot cause a redraw.

    def _stop_recovering(self,container,execution_id):
        try:
            stop_owned_worker(container,execution_id=execution_id)
        except (ValueError,OSError,subprocess.SubprocessError):
            self.recovery_issues[execution_id] = 'CLEANUP_PENDING'

    def recover_service(self):
        self.recovery_issues = {}
        if self.profile.values['schema'] in ('qualification_execution_profile/v3', 'qualification_execution_profile/v4', 'qualification_execution_profile/v5'):
            campaigns = campaign_store.CampaignStore(self.store)
            with self.store.transaction() as connection:
                exists = connection.execute("SELECT 1 FROM sqlite_master WHERE name='full_campaign_budgets'").fetchone()
                attempts = [] if exists is None else [row[0] for row in connection.execute('SELECT attempt_id FROM full_campaign_budgets')]
            for attempt in attempts:
                with self.store.transaction() as connection:
                    funding = campaigns._funding(connection, attempt)
                if funding is not None:
                    # A pending one-use intent is reported and never materialized;
                    # its work is not yet in the snapshot, so the loop below cannot
                    # touch it. A terminal overlay is likewise reported only.
                    pending = funding['bootstrap_pending_work_id'] is not None or funding['terminal_overlay'] is not None
                    if pending:
                        self.recovery_issues[attempt + ':funding'] = 'FUNDING_PENDING'
                    if self.profile.values['schema'] == 'qualification_execution_profile/v3':
                        if not pending:
                            self.recovery_issues[attempt + ':funding'] = 'FUNDING_RUNTIME_NOT_ENABLED'
                        continue  # R2a persistence alone cannot resume a controller.
                    # Execution-capable installation: materialized funded work gets
                    # the same bounded per-work restart recovery as v2 attempts
                    # (operator ruling 2026-09-19). The funded adapter reads history
                    # directly; the public snapshot stays refused while pending.
                    with self.store.transaction() as connection:
                        state = campaigns._budget(connection, attempt)
                else:
                    state = parse_canonical_json(campaigns.budget_snapshot(attempt), label='recovery budget')
                    if state['profile']['schema'] != 'qualification_campaign_budget_profile/v2':
                        continue  # Historical S1/dormant records gain no runtime ownership.
                for work in state['works']:
                    if work['work_id'] == 'admission' and work['state'] == 'RESERVED' and not work['transitions']:
                        # START_INTENT precedes every OS effect (R1): a never-prepared
                        # admission has nothing to recover, and spending the one-use
                        # RECOVERY_OWNER slot on it would leave a permanent barrier and
                        # bar the exact SUBMIT_E1 retry that may still perform the
                        # first launch. Reported only; this grants nothing.
                        unstarted = campaigns.inspect_unstarted_admission(attempt, campaign_supervisor.observe_campaign_clock)
                        if unstarted is not None:
                            if unstarted['expired']:
                                # Past the admission deadline or on another boot nothing can
                                # ever launch it and no guardian will ever authenticate a
                                # queued body: the same clock observation ends the budget
                                # honestly (BUDGET_EXHAUSTED / BUDGET_UNCERTAIN) through the
                                # ownerless RESERVED recovery path — no slot, no OS effect.
                                campaigns.recover_work(attempt, 'admission', unstarted['clock_bytes'])
                            self.recovery_issues[attempt + ':admission'] = (
                                'ADMISSION_RESUMABLE' if unstarted['resumable'] else 'ADMISSION_UNSTARTED')
                            continue
                    try:
                        campaign_supervisor.recover_campaign_work(self, decode_base64(work['reservation_bytes_b64']),
                                              attempt_id=attempt, work_id=work['work_id'])
                    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
                        self.recovery_issues[attempt + ':' + work['work_id']] = 'RECOVERY_PENDING'
        for row in self.store.execution_rows():
            if row['state'] in ('DISPATCHED', 'START_INTENT', 'RUNNING'):
                self.store.record_abort(row['execution_id'], 'uncertain execution after service restart', uncertain=True)
            if row['validity'] == 'VOID' or row['state'] in ('DISPATCHED','START_INTENT','RUNNING','IN_DOUBT','ABORTED'):
                try:
                    container = row['container_id']
                    if container is None:
                        release = parse_canonical_json(self.release,label='installed release')
                        container = find_owned_worker(row['execution_id'],host_run_id=self.config['host_run_id'],
                            image_id=release['worker_image_digest'],release_sha256=row['release_sha256'])
                    if container is not None:
                        self._stop_recovering(container,row['execution_id'])
                except (ValueError,OSError,subprocess.SubprocessError):
                    self.recovery_issues[row['execution_id']] = 'CLEANUP_PENDING'
            elif row['state'] == 'CAPTURED' and row['validity'] == 'VALID':
                try:
                    sign_captured(row['execution_id'], store=self.store, credential_reference=self.config['execution_credential'])
                except (ValueError,OSError):
                    self.recovery_issues[row['execution_id']] = 'ATTESTATION_PENDING'

    def serve(self):
        if os.geteuid() != self.config['service_uid']:
            raise ValueError('supervisor OS identity differs')
        import fcntl
        lock = (self.root / 'service.lock').open('a+b')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.recover_service()
        path = Path(self.config['socket_path'])
        if path.exists():
            path.unlink()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
            server.bind(str(path))
            path.chmod(0o660)
            info=path.lstat()
            if info.st_uid!=self.config['service_uid'] or info.st_gid!=self.config['socket_gid']:
                raise ValueError('bound socket did not inherit protected identity')
            server.listen(RPC_CONNECTION_LIMIT)
            with BoundedConnections(self._serve_connection, limit=RPC_CONNECTION_LIMIT) as handlers:
                while True:
                    connection, _ = server.accept()
                    try:
                        handlers.submit(connection)
                    except BaseException:
                        connection.close()
                        raise

    def _serve_connection(self, connection):
        with connection:
            connection.settimeout(self.profile.capture_seconds)
            try:
                _, uid, _ = struct.unpack('3i', connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i')))
                # The service identity has no public operation; its only request
                # is the bounded private schedule frame, rejected in framing.
                limit = SCHEDULE_BYTE_LIMIT if uid == self.config['service_uid'] else self.profile.rpc_byte_limit
                raw = receive(connection, limit=limit)
                result = self.handle_request(uid, raw)
                response = encoded(dict(ok=True, data_b64=base64.b64encode(result).decode('ascii')))
            except (ValueError, KeyError, OSError, RecursionError) as exc:
                if not isinstance(exc, ValueError):
                    # A refusal is a ValueError; anything else is a defect whose
                    # only record is this process's stderr (the journal).
                    traceback.print_exc(file=sys.stderr)
                response = encoded(dict(ok=False, error=str(exc)[:1024]))
            if len(response) > self.profile.rpc_byte_limit:
                response = encoded(dict(ok=False, error='RESPONSE_EXCEEDS_PROFILE_LIMIT'))
            try:
                connection.sendall(encode_frame(response, limit=self.profile.rpc_byte_limit))
            except OSError:
                # Peer disconnect cannot cancel an already-reserved execution.
                pass


def main():
    from .runtime import load_instance, measure_runtime, installed_code_root
    from .release import parse_instance
    config = parse_instance(encoded(load_instance(installed_code_root() / 'qualification-installation/supervisor.json')))
    release = read_regular(Path(config['installation_root']), 'release.json', limit=16 * 1024 * 1024)
    measure_runtime(installed_code_root(), 'supervisor', release)
    ExecutionService(config).serve()


# Campaign-specific modules are loaded once at service startup, never lazily
# on a first private request (R2 contract bullet 8). Referenced by module so
# tests may substitute adapters at call time. Placed after the class to keep
# the existing guardian -> service import direction.
import ctypes  # noqa: E402,F401  (kernel timer ABI used by every guarded request)
from . import campaign_budget, campaign_funding, campaign_protocol, campaign_store, campaign_supervisor, release_schema  # noqa: E402,F401
from .. import journal_snapshot, source_admission  # noqa: E402,F401
from tools.qualification_verification import container_ownership  # noqa: E402,F401
from .campaign_supervisor import guardian_main as campaign_guardian_main  # noqa: E402
