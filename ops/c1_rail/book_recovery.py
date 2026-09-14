"""Listener-owned durable recovery. Production transport is deliberately absent.

SyntheticRoute injection is an explicit Python test seam, never an HTTP/config
option. Observations never confer execution credit, completion or retry authority.
"""
from dataclasses import asdict
from datetime import datetime, timezone
import json
from uuid import uuid4

from book_halt import BookHaltStore, HaltStoreError, _text
from book_recovery_schema import (RecoveryDemand, RecoveryEvidence, canonical,
                                  digest, graph, positive, timestamp, validate_inputs)
from book_recovery_schema import unknown_owners


class RecoveryOwner:
    """Account-scoped journal owner with no production sender or resume API."""

    def __init__(self, store):
        self.store = store
        self.path = store.path
        self._route = None

    @classmethod
    def boot(cls, path, account, *, controlled_products=()):
        return cls(BookHaltStore.boot(path, account, controlled_symbols=controlled_products))

    @classmethod
    def synthetic(cls, owner, route):
        """SYNTHETIC fixture only. Not selectable by production handler/config."""
        result = cls(owner.store)
        result._route = route
        return result

    def snapshot(self):
        return self.store.snapshot()

    def rejection_reason(self):
        return self.store.rejection_reason()

    def report_fault(self, incident_id, reason, *, observed_symbols=()):
        # BookHaltStore publishes report, scopes and recovery obligations atomically.
        return self.store.halt(incident_id, reason, observed_symbols=observed_symbols)

    @staticmethod
    def _event(db, kind, owner, body):
        sequence = db.execute('SELECT event_count FROM recovery_meta').fetchone()[0] + 1
        db.execute('INSERT INTO recovery_events VALUES (?, ?, ?, ?)',
                   (sequence, kind, owner, digest(body)))
        db.execute('UPDATE recovery_meta SET event_count=?', (sequence,))

    @classmethod
    def _obligation(cls, db, reason, owner, body):
        existing = db.execute('SELECT body FROM recovery_obligations WHERE reason=? AND owner=?',
                              (reason, owner)).fetchone()
        if existing:
            if existing[0] != canonical(body):
                raise HaltStoreError('conflicting recovery obligation')
            return
        db.execute('INSERT INTO recovery_obligations VALUES (?, ?, ?)',
                   (reason, owner, canonical(body)))
        cls._event(db, 'obligation', reason + ':' + owner, body)

    def _boundary(self, db, evidence, *, after=None):
        if self._route is None:
            # Unqualified local journal ordering is explicitly not an E1 domain.
            return {'domain': 'unqualified-local:' + self.store.boot_id,
                    'sequence': db.execute('SELECT event_count FROM recovery_meta').fetchone()[0] + 1,
                    'timestamp': datetime.now(timezone.utc).isoformat()}
        boundary = dict(self._route.boundary())
        try:
            positive(boundary['sequence'])
            current_time = timestamp(boundary['timestamp'])
            previous = after or evidence
            if (boundary['domain'] != evidence['domain'] or
                    boundary['sequence'] <= previous['sequence'] or
                    current_time <= timestamp(previous['timestamp'])):
                raise HaltStoreError('invalid synthetic causal boundary')
            prior = [json.loads(row[0])['prepared'] for row in db.execute('SELECT body FROM recovery_operations')]
            prior += [json.loads(row[0])['boundary'] for row in db.execute('SELECT body FROM recovery_attempts')]
            for saved in prior:
                if saved['domain'] == boundary['domain'] and (
                        saved['sequence'] >= boundary['sequence'] or
                        timestamp(saved['timestamp']) >= current_time):
                    raise HaltStoreError('regressed account causal boundary')
        except (KeyError, TypeError, ValueError) as exc:
            raise HaltStoreError('invalid synthetic causal boundary') from exc
        return boundary

    def prepare(self, demand: RecoveryDemand, *, evidence: RecoveryEvidence):
        state = self._prepare((demand,), evidence, whole_account=False)
        return next(o for o in state['operations'] if o['operation_id'] == demand.operation_id)

    def prepare_recovery(self, demands: tuple[RecoveryDemand, ...], *, evidence: RecoveryEvidence):
        return self._prepare(demands, evidence, whole_account=True)

    def _prepare(self, demands, evidence, *, whole_account):
        if not isinstance(evidence, RecoveryEvidence) or not isinstance(demands, tuple) or not demands:
            raise HaltStoreError('explicit typed recovery batch required')
        if not all(isinstance(d, RecoveryDemand) for d in demands):
            raise HaltStoreError('explicit typed recovery demand required')
        # Detach caller-owned nested structures before validation/persistence.
        try:
            encoded_evidence = json.loads(canonical(asdict(evidence)))
            encoded_demands = [json.loads(canonical(asdict(d))) for d in demands]
        except (ValueError, TypeError) as exc:
            raise HaltStoreError('malformed recovery record') from exc
        if len({d['operation_id'] for d in encoded_demands}) != len(demands):
            raise HaltStoreError('duplicate operation in recovery batch')
        for demand in encoded_demands:
            validate_inputs(demand, encoded_evidence)
        with self.store._transaction() as db:
            state = self.store._state(db)
            if encoded_evidence['account'] != state['account']:
                raise HaltStoreError('recovery account mismatch')
            scopes = {s['scope_id'] for s in state['recovery_scopes']}
            incidents = {i['incident_id'] for i in state['incidents']}
            requested_scopes = {s for d in encoded_demands for s in d['scope_ids']}
            if not requested_scopes <= scopes:
                raise HaltStoreError('unpublished recovery scope')
            if whole_account and not scopes <= requested_scopes | {
                    'location:' + d['symbol'] for d in encoded_demands}:
                raise HaltStoreError('incomplete account recovery batch')
            if whole_account and not set(encoded_evidence['observed_symbols']) <= {
                    d['symbol'] for d in encoded_demands}:
                raise HaltStoreError('uncovered observed account location')
            for demand in encoded_demands:
                if demand['incident_id'] not in incidents:
                    raise HaltStoreError('unpublished recovery incident')
                existing = next((o for o in state['operations'] if o['operation_id'] == demand['operation_id']), None)
                if existing:
                    if existing['demand'] != demand or existing['evidence'] != encoded_evidence:
                        raise HaltStoreError('conflicting recovery operation identity')
                    continue
                body = {'demand': demand, 'evidence': encoded_evidence,
                        'prepared': self._boundary(db, encoded_evidence),
                        'boot_id': self.store.boot_id, 'generation': state['generation'],
                        'provenance': 'SYNTHETIC' if self._route else 'UNQUALIFIED'}
                operation_id = demand['operation_id']
                db.execute('INSERT INTO recovery_operations VALUES (?, ?, ?, NULL)',
                           (operation_id, canonical(body), digest(body)))
                for table, rows in graph(demand, encoded_evidence).items():
                    db.executemany(f'INSERT INTO {table} VALUES (?, ?, ?)',
                                   [(operation_id, key, canonical(value)) for key, value in rows])
                self._event(db, 'prepared', operation_id, body)
                selected = [r for r in encoded_evidence['orders'] if r['order_id'] in demand['order_ids']]
                unsupported = (demand['quantity'] is not None or
                               (demand['kind'] == 'CANCEL' and any(r['kind'] != 'risk_add' for r in selected)))
                if unsupported:
                    self._obligation(db, 'capability', operation_id, {'detail': 'unsupported bounded/protection cancel'})
                if self._route is None and not unsupported:
                    self._obligation(db, 'capability', operation_id,
                                     {'detail': 'production E1-E3, adapter and authority unavailable'})
            # Locations absent from selected demands remain independent reconciliation work.
            for symbol in encoded_evidence['observed_symbols']:
                self._obligation(db, 'reconciliation', 'location:' + symbol, {'symbol': symbol})
            for reason, owner, facts in unknown_owners(encoded_evidence):
                self._obligation(db, reason, owner, facts)
            return self.store._state(db)

    def dispatch(self, operation_id):
        """Commit UNKNOWN before SYNTHETIC send; all attempts remain unretryable."""
        _text(operation_id)
        with self.store.serializer.acquire():
            with self.store._transaction(locked=True) as db:
                state = self.store._state(db)
                operation = next((o for o in state['operations'] if o['operation_id'] == operation_id), None)
                if operation is None:
                    raise HaltStoreError('unknown recovery operation')
                if operation['status'] != 'prepared':
                    return operation
                if self._route is None or operation['provenance'] != 'SYNTHETIC':
                    self._obligation(db, 'capability', operation_id,
                                     {'detail': 'production E1-E3, adapter and authority unavailable'})
                    return {**operation, 'status': 'blocked'}
                if operation['boot_id'] != self.store.boot_id or operation['generation'] != state['generation']:
                    self._obligation(db, 'restart_or_halt', operation_id, {'detail': 'fresh preparation required'})
                    return {**operation, 'status': 'blocked'}
                same_symbol = [o for o in state['operations'] if o['demand']['symbol'] == operation['demand']['symbol']]
                if same_symbol[0]['operation_id'] != operation_id:
                    return {**operation, 'status': 'queued'}
                boundary = self._boundary(db, operation['evidence'], after=operation['prepared'])
                attempt_id, request_id = str(uuid4()), str(uuid4())
                command = graph(operation['demand'], operation['evidence'])['recovery_effects'][0][1]
                command = {**command, 'request_id': request_id}
                attempt = {'attempt_id': attempt_id, 'operation_id': operation_id,
                           'request_id': request_id, 'state': 'UNKNOWN', 'boundary': boundary,
                           'boot_id': self.store.boot_id, 'generation': state['generation'],
                           'account': state['account'], 'route': operation['evidence']['route'],
                           'version': operation['evidence']['version'], 'command_digest': digest(command)}
                db.execute('INSERT INTO recovery_attempts VALUES (?, ?, ?, ?, NULL)',
                           (attempt_id, operation_id, request_id, canonical(attempt)))
                db.execute('UPDATE recovery_operations SET attempt_id=? WHERE operation_id=?',
                           (attempt_id, operation_id))
                self._event(db, 'attempt', attempt_id, attempt)
            # Lock still held after durable commit. Boot cannot cross this boundary.
            try:
                observation = self._route.send(command)
                if (not isinstance(observation, dict) or observation.get('state') not in
                        ('accepted', 'partial', 'rejected', 'unknown')):
                    observation = {'state': 'unknown', 'detail': 'malformed synthetic response'}
                observation = json.loads(canonical(observation))
            except Exception:  # noqa: BLE001 - bytes may have left; retain UNKNOWN
                observation = {'state': 'unknown', 'detail': 'synthetic transport exception'}
            with self.store._transaction(locked=True) as db:
                self.store._state(db)
                db.execute('UPDATE recovery_attempts SET observation=? WHERE attempt_id=?',
                           (canonical(observation), attempt_id))
                self._event(db, 'observation', attempt_id, observation)
                state = self.store._state(db)
                return next(o for o in state['operations'] if o['operation_id'] == operation_id)
