"""Protected supervisor: the only active journal and container authority."""
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import os
from pathlib import Path
import socket
import struct
import subprocess
import threading
import time

from ..contract import canonical_json_bytes as encoded, parse_canonical_json, verify_detached_approval
from .admission import verify_bundle
from .archive import archive_capture
from .evidence import parse_worker_result
from .files import fsync_directory, read_regular
from .g5 import validate_result_envelope_v2
from .keys import load_keys
from .launcher import create_worker, find_owned_worker, inspect_worker, start_and_capture, stop_owned_worker
from .plan import derive_n1_plan
from .preflight import build_binding
from .protocol import decode_base64, encode_frame, fields, parse_request, sha256
from .signing import sign_captured
from .store import ExecutionStore
from .transport import receive
from .verification import utc_instant, verify_role_signature

RPC_CONNECTION_LIMIT = 16

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
        self.store = ExecutionStore(self.root / 'journal.sqlite', installation_dir=self.installation)
        self.dispatch_lock = threading.Lock()
        self.recovery_issues = {}
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='qualification-execution')

    def keys(self):
        return load_keys(read_regular(self.installation, 'keys.json', limit=1024 * 1024), authority_class=self.authority)

    def _context(self, bundle_digest, *, at):
        context = verify_bundle(self.root / 'bundles' / bundle_digest, self.release, self.keys(), at)
        if context.bundle_sha256 != bundle_digest or context.domain.authority_class != 'TEST_ONLY':
            raise ValueError('N1_ONLY release forbids production execution or substituted bundle')
        return context

    def handle_request(self, peer_uid, request_bytes):
        request = parse_request(request_bytes)
        operation, attempt = request['operation'], request['attempt_id']
        role = self.roles.get(peer_uid)
        if not permitted(role, operation):
            raise ValueError('PEER_NOT_AUTHORIZED')
        if operation == 'SUBMIT_N1':
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
            response = parse_canonical_json(self.store.commit_assessment(evidence,authentication,now=now()),label='commit receipt')
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
                raw = receive(connection, limit=self.profile.rpc_byte_limit)
                result = self.handle_request(uid, raw)
                response = encoded(dict(ok=True, data_b64=base64.b64encode(result).decode('ascii')))
            except (ValueError, KeyError, OSError, RecursionError) as exc:
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
