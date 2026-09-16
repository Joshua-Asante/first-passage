"""One-use offline bootstrap. Observation never restores authority."""
from dataclasses import asdict
from datetime import datetime
import hashlib
import json
from uuid import uuid4

from .book_policy import ACCOUNT_MICRO_CAP, BOOK_LEGS, is_protected, lifecycle_multiplier
from .book_protection import ActionOccurrence, ProtectionSnapshot, validate_occurrence
from .book_takeover import InventoryRead, AccountInventory
from c1_signal_daemon.book_protocol import Mode


class BootstrapOwnerMixin:
    def _decode_bootstrap_evidence(self, evidence, identity, at):
        from .book_account_owner import MAX_FACT_AGE
        if set(evidence) != {'record_version','request','snapshot','expected_stream'} or evidence['record_version'] != 1:
            raise ValueError('invalid bootstrap evidence codec')
        r, s = evidence['request'], evidence['snapshot']
        request = InventoryRead(**{**r, 'occurrence': ActionOccurrence(**r['occurrence']),
            'scope_legs': tuple(r['scope_legs']), 'prepared_at': datetime.fromisoformat(r['prepared_at'])})
        p = s['protection']
        if any(s[k] != [] for k in ('positions','working_orders','requests','facts')) or any(
                p[k] != [] for k in ('orders','positions','resolved_operations')):
            raise ValueError('bootstrap evidence is not empty')
        protection = ProtectionSnapshot(**{**p, 'as_of': datetime.fromisoformat(p['as_of']),
            'scope_legs': tuple(p['scope_legs']), 'orders': (), 'positions': (), 'resolved_operations': ()})
        snapshot = AccountInventory(**{**s, 'as_of': datetime.fromisoformat(s['as_of']),
            'scope_legs': tuple(s['scope_legs']), 'positions': (), 'working_orders': (),
            'requests': (), 'facts': (), 'protection': protection})
        self._inventory_shape(snapshot)
        scope = tuple(spec.leg_id for spec in BOOK_LEGS)
        if (not validate_occurrence(request.occurrence) or request.occurrence != ActionOccurrence(
                self.account, identity['account_epoch'], identity['session_id'], 'direct', 'bootstrap:creation', 0)
                or request.after_sequence != 0 or type(request.after_sequence) is not int
                or snapshot.read_id != request.read_id or snapshot.scope_legs != scope or request.scope_legs != scope
                or snapshot.account != self.account or snapshot.account_epoch != identity['account_epoch']
                or snapshot.stream_id != evidence['expected_stream'] or not snapshot.complete or not protection.complete
                or (protection.account, protection.account_epoch, protection.scope_legs, protection.as_of)
                   != (snapshot.account, snapshot.account_epoch, snapshot.scope_legs, snapshot.as_of)
                or not request.prepared_at <= snapshot.as_of <= at
                or at - snapshot.as_of > MAX_FACT_AGE):
            raise ValueError('invalid bootstrap evidence binding')
        return request, snapshot

    def _new_bootstrap_db(self, db, *, origin='fresh', now=None):
        from .book_account_owner import _body, _binding_record
        state = self._state(db)
        raw = _body(_binding_record(self.binding))
        body = dict(record_version=1, origin=origin, account=self.account,
            account_epoch=state['account_epoch'], boot_id=state['boot_id'], generation=state['generation'],
            session_id=self.binding['session'].session_id, binding_digest=hashlib.sha256(raw.encode()).hexdigest(),
            state='eligible' if origin == 'fresh' else 'ineligible', activation=None,
            invalidation=None if origin == 'fresh' else 'migration')
        db.execute('INSERT INTO bootstrap_identity VALUES (1, ?)', (_body(body),))

    def _bootstrap_db(self, db):
        from .book_account_owner import AccountOwnerError
        try:
            rows = db.execute('SELECT singleton,body FROM bootstrap_identity').fetchall()
            if len(rows) != 1 or rows[0][0] != 1:
                raise ValueError('missing bootstrap identity')
            body = json.loads(rows[0][1])
            required = {'record_version','origin','account','account_epoch','boot_id','generation',
                        'session_id','binding_digest','state','activation','invalidation'}
            state = self._state(db)
            if (set(body) != required or body['record_version'] != 1
                    or body['origin'] not in ('fresh','migrated')
                    or body['account'] != self.account or body['account_epoch'] != state['account_epoch']
                    or type(body['generation']) is not int or body['generation'] < 1
                    or any(type(body[k]) is not str or not body[k] for k in ('boot_id','session_id','binding_digest'))
                    or len(body['binding_digest']) != 64 or body['state'] not in ('eligible','consumed','ineligible')
                    or body['origin'] == 'migrated' and body['state'] != 'ineligible'):
                raise ValueError('invalid bootstrap identity')
            if body['activation'] is not None:
                activation = body['activation']
                if set(activation) != {'at','read_id'} or datetime.fromisoformat(activation['at']).utcoffset() is None:
                    raise ValueError('invalid activation')
                retained = db.execute('SELECT body FROM bootstrap_reads WHERE read_id=?', (activation['read_id'],)).fetchone()
                if retained is None:
                    raise ValueError('missing bootstrap evidence')
                request, _snapshot = self._decode_bootstrap_evidence(json.loads(retained[0]), body,
                    datetime.fromisoformat(activation['at']))
                if request.read_id != activation['read_id']:
                    raise ValueError('bootstrap activation read mismatch')
            if body['state'] == 'consumed' and body['activation'] is None:
                raise ValueError('missing activation')
            if body['state'] == 'eligible' and (body['activation'] is not None or body['invalidation'] is not None):
                raise ValueError('invalid eligible identity')
            from .book_migration import migration_record
            record = migration_record(db)
            if (record is not None) != (body['origin'] == 'migrated'):
                raise ValueError('bootstrap migration provenance mismatch')
            return body
        except (ValueError, TypeError, KeyError) as exc:
            raise AccountOwnerError('invalid bootstrap journal') from exc

    def _invalidate_bootstrap_db(self, db, reason):
        from .book_account_owner import _body
        body = self._bootstrap_db(db)
        body['state'] = 'ineligible'
        if body['invalidation'] is None:
            body['invalidation'] = reason
        db.execute('UPDATE bootstrap_identity SET body=? WHERE singleton=1', (_body(body),))

    def _activate_bootstrap(self, *, now):
        from .book_account_owner import AccountOwnerError, _body, _binding_record, _time
        _time(now, 'activation time')
        with self.serializer.acquire(), self._transaction() as db:
            state = self._state(db)
            body = self._bootstrap_db(db)
            self._validate_schema(db)
            self._validate_protection_state_db(db)
            self._validate_takeover_state_db(db)
            if getattr(self, '_input_send_suppressed', False):
                raise AccountOwnerError('bootstrap suppressed after storage failure')
            refusal = self._validate_settlement_binding(db, now)
            if refusal:
                raise AccountOwnerError(refusal)
            session = self.binding['session']
            if not session.opens_at <= now < session.risk_add_cutoff:
                raise AccountOwnerError('outside synthetic risk-add window')
            if (not self.binding['as_of'] <= now < self.binding['valid_until']
                    or now - self.binding['as_of'] > self.binding['max_evidence_age']):
                raise AccountOwnerError('stale bootstrap binding')
            binding_digest = hashlib.sha256(_body(_binding_record(self.binding)).encode()).hexdigest()
            matches = (body['origin'] == 'fresh' and body['boot_id'] == state['boot_id']
                and body['generation'] == state['generation'] and body['session_id'] == session.session_id
                and body['binding_digest'] == binding_digest)
            if not matches or body['state'] == 'ineligible':
                raise AccountOwnerError('fresh bootstrap entitlement required')
            if state['permission'] == 'RUNNING' and state['authority'] == 'NORMAL' and body['state'] == 'consumed':
                return state
            if body['state'] != 'eligible':
                raise AccountOwnerError('bootstrap already consumed')
            # Input registration alone is inert. Any execution/preparation/history is not fresh.
            for table in ('incidents','operations','attempts','capacity_events','close_reservations',
                          'protection_owners','protection_operations','protection_facts','protection_state',
                          'takeover_plans','feedback','broker_facts','action_occurrences','legacy_obligations'):
                if db.execute(f'SELECT 1 FROM {table} LIMIT 1').fetchone():
                    raise AccountOwnerError('bootstrap history is not empty: ' + table)
            if db.execute('SELECT 1 FROM barriers WHERE actions IS NOT NULL LIMIT 1').fetchone():
                raise AccountOwnerError('bootstrap prepared actions exist')
            if self._capacity(db).blocks:
                raise AccountOwnerError('capacity state blocked')
            desired = Mode.PROTECTED if is_protected(self.binding['settlement'].equity,
                self.binding['settlement'].peak, self.binding['policy']) else Mode.NORMAL
            for spec in BOOK_LEGS:
                lifecycle_multiplier(self.binding['lifecycle_tiers'][spec.leg_id])
                allocation = self.binding['cap_allocations'][spec.leg_id]
                if type(allocation) is not int or not 0 <= allocation <= ACCOUNT_MICRO_CAP:
                    raise AccountOwnerError('invalid bootstrap allocation')
            reader = getattr(self.synthetic_broker, 'read_bootstrap_inventory', None)
            if not callable(reader):
                raise AccountOwnerError('independent bootstrap inventory required')
            read = InventoryRead(str(uuid4()), ActionOccurrence(self.account, state['account_epoch'],
                session.session_id, 'direct', 'bootstrap:creation', 0),
                tuple(spec.leg_id for spec in BOOK_LEGS), now, 0)
            snapshot = reader(read)
            try:
                evidence = json.loads(_body(dict(record_version=1, request=asdict(read), snapshot=asdict(snapshot),
                    expected_stream=self.synthetic_broker.stream_id + ':inventory')))
                self._decode_bootstrap_evidence(evidence, body, now)
                if now - snapshot.as_of > self.binding['max_evidence_age']:
                    raise ValueError('stale bootstrap inventory')
            except (ValueError, TypeError, AttributeError, KeyError) as exc:
                raise AccountOwnerError('bootstrap inventory refused') from exc
            db.execute('INSERT INTO bootstrap_reads VALUES (?, ?)', (read.read_id, _body(evidence)))
            body['state'] = 'consumed'
            body['activation'] = dict(at=now.isoformat(), read_id=read.read_id)
            db.execute('UPDATE bootstrap_identity SET body=? WHERE singleton=1', (_body(body),))
            db.execute("INSERT INTO protection_state VALUES (?, ?, '[]', ?)",
                       (session.session_id, desired.value, state['generation']))
            db.execute("UPDATE owner_state SET permission='RUNNING', authority='NORMAL'")
            return self._state(db)
