"""Protection journal behavior of the account owner, under its serializer.

This mixin owns no independent connection, permission or transport. All mutations
use the account owner's transaction and all commands use its existing route.
"""
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import math
from uuid import uuid4

from c1_signal_daemon.book_adapters import ADAPTER_BY_LEG
from c1_signal_daemon.book_protocol import Bracket, BracketAmend, ExecutionEvent, Fill, Side
from c1_signal_daemon.book_validation import InputViolation, validate_action
from .book_capacity import Reduction
from .book_policy import leg
from .book_protection import (
    ObservedProtection, ProtectionChange, ProtectionExecution, ProtectionRead,
    ProtectionSnapshot, ProtectionTarget, bracket_from_dict, changed_components,
    has_components, is_loosening, normalize_bracket,
)

PROTECTION_PERIOD = timedelta(minutes=15)


def _dump(value):
    def encoded(item):
        if isinstance(item, datetime):
            return item.isoformat()
        if isinstance(item, Enum):
            return item.value
        raise TypeError(type(item).__name__)
    return json.dumps(value, default=encoded, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _aware(value):
    return isinstance(value, datetime) and value.utcoffset() is not None


def _identity(value):
    return type(value) is str and bool(value.strip())


def _number(value):
    return type(value) is int or (type(value) is float and math.isfinite(value))


@dataclass(frozen=True)
class ProtectionOwnerView:
    owner_id: str
    entry_fill_id: str
    leg_id: str
    consumed: bool
    observed: Bracket | None
    quantity: int
    pending_operation: str | None
    trail_active: bool
    trail_anchor: float | None
    deadline: datetime | None


class ProtectionOwnerMixin:
    def _protection_rows(self, db):
        return {row[0]: json.loads(row[1]) for row in db.execute(
            'SELECT owner_id, body FROM protection_owners ORDER BY rowid')}

    def _put_protection(self, db, row):
        db.execute('UPDATE protection_owners SET body=? WHERE owner_id=?',
                   (_dump(row), row['owner_id']))

    def _protection_operations(self, db):
        return {row[0]: json.loads(row[1]) for row in db.execute(
            'SELECT operation_id, body FROM protection_operations ORDER BY rowid')}

    def _put_protection_operation(self, db, row):
        db.execute('UPDATE protection_operations SET body=? WHERE operation_id=?',
                   (_dump(row), row['operation_id']))

    def _validate_protection_state_db(self, db):
        from .book_account_owner import AccountOwnerError
        try:
            owners = self._protection_rows(db)
            operations = self._protection_operations(db)
            fills = {f.execution_id: f for f in self._capacity(db).fills}
            indexed = dict(db.execute('SELECT owner_id,entry_fill_id FROM protection_owners'))
            from .book_migration import legacy_ids
            legacy = legacy_ids(db, 'fill') if getattr(self, '_read_schema_version', 4) == 4 else set()
            if set(indexed.values()) & legacy or set(indexed.values()) | legacy != set(fills):
                raise ValueError('missing original protection owner')
            for identity, row in owners.items():
                if (identity != row['owner_id'] or row['entry_fill_id'] not in fills
                        or identity != 'protection:' + row['entry_fill_id']
                        or indexed[identity] != row['entry_fill_id']
                        or row['leg_id'] not in ADAPTER_BY_LEG
                        or row['order_symbol'] != leg(row['leg_id']).order_symbol
                        or row['side'] != leg(row['leg_id']).entry_side.value
                        or type(row['original_qty']) is not int
                        or row['original_qty'] != fills[row['entry_fill_id']].quantity
                        or type(row['consumed']) is not bool
                        or type(row['ever_protected']) is not bool
                        or type(row['quantity']) is not int or row['quantity'] < 0
                        or type(row['revision']) is not int or row['revision'] < 0
                        or type(row['trail_active']) is not bool
                        or type(row['broker_order_ids']) is not list
                        or any(not _identity(item) for item in row['broker_order_ids'])
                        or row['consumed'] and (row['observed'] is not None or row['quantity'] != 0)
                        or row['pending_operation'] is not None and row['pending_operation'] not in operations):
                    raise ValueError('invalid protection ownership')
                for name in ('deadline', 'evidence_at'):
                    if row[name] is not None and not _aware(datetime.fromisoformat(row[name])):
                        raise ValueError('invalid retained evidence time')
                if row['pending_operation'] is not None and operations[row['pending_operation']]['owner_id'] != identity:
                    raise ValueError('protection obligation owner mismatch')
                if row['observed'] is not None:
                    if validate_action(BracketAmend(row['leg_id'], bracket_from_dict(row['observed']))):
                        raise ValueError('invalid retained protection')
                    if row['quantity'] <= 0 or not row['broker_order_ids']:
                        raise ValueError('invalid retained protection coverage')
            for identity, row in operations.items():
                if (identity != row['operation_id'] or row['owner_id'] not in owners
                        or row['status'] not in ('pending_confirmation', 'awaiting_evidence', 'applied',
                                                 'rejected', 'unknown', 'rejected_intact', 'noop', 'refused')
                        or not _aware(datetime.fromisoformat(row['prepared_at']))
                        or row['deadline'] is not None and not _aware(datetime.fromisoformat(row['deadline']))
                        or type(row['quantity']) is not int or row['quantity'] < 0
                        or type(row['old_revision']) is not int or row['old_revision'] < 0
                        or row['primitive'] not in ('entry_attach', 'attach', 'amend')
                        or not _identity(row['expected_operation_id'])):
                    raise ValueError('orphan protection operation')
                if validate_action(BracketAmend(owners[row['owner_id']]['leg_id'], bracket_from_dict(row['effective']))):
                    raise ValueError('invalid retained requested protection')
        except (KeyError, ValueError, TypeError) as exc:
            raise AccountOwnerError('invalid protection journal') from exc

    @property
    def protection_owners(self):
        with self._transaction() as db:
            self._validate_protection_state_db(db)
            return tuple(ProtectionOwnerView(
                r['owner_id'], r['entry_fill_id'], r['leg_id'], r['consumed'],
                bracket_from_dict(r['observed']), r['quantity'], r['pending_operation'],
                r['trail_active'], r['trail_anchor'],
                datetime.fromisoformat(r['deadline']) if r['deadline'] else None,
            ) for r in self._protection_rows(db).values())

    def _register_protection_fill_db(self, db, fact, operation_body):
        raw = json.loads(operation_body)
        bracket = bracket_from_dict(raw.get('bracket'))
        expected = has_components(bracket)
        identity = 'protection:' + fact.fact_id
        op_id = 'attached:' + fact.fact_id if expected else None
        deadline = (fact.as_of + PROTECTION_PERIOD).isoformat() if expected else None
        row = dict(owner_id=identity, entry_fill_id=fact.fact_id, leg_id=fact.leg_id,
                   order_symbol=leg(fact.leg_id).order_symbol, side=leg(fact.leg_id).entry_side.value,
                   original_qty=fact.quantity, consumed=False, ever_protected=expected,
                   desired=asdict(bracket) if bracket else None, observed=None, quantity=0,
                   broker_order_ids=[], revision=0, trail_active=False, trail_anchor=None,
                   evidence_at=None, evidence_fact=None, pending_operation=op_id, deadline=deadline)
        db.execute('INSERT INTO protection_owners VALUES (?, ?, ?)', (identity, fact.fact_id, _dump(row)))
        if expected:
            effective = normalize_bracket(bracket, leg(fact.leg_id).entry_side,
                                          ADAPTER_BY_LEG[fact.leg_id].mintick)
            op = dict(operation_id=op_id, owner_id=identity, expected_operation_id=fact.operation_id,
                      primitive='entry_attach', status='pending_confirmation', desired=asdict(bracket),
                      effective=asdict(effective), quantity=fact.quantity, old=None, old_revision=0,
                      prepared_at=fact.as_of.isoformat(), deadline=deadline, attempt_id=None)
            db.execute('INSERT INTO protection_operations VALUES (?, ?, ?, ?)',
                       (op_id, 'entry:' + fact.operation_id, identity, _dump(op)))

    def _protection_fault(self, db, identity, now):
        self._halt_db(db, 'protection:' + identity, 'protection', now)

    def _check_protection_deadlines_locked(self, *, now):
        with self._transaction() as db:
            self._check_close_protection_deadlines_db(db, now=now)
            for row in self._protection_rows(db).values():
                if row['deadline'] and now >= datetime.fromisoformat(row['deadline']):
                    self._protection_fault(db, 'deadline:' + row['pending_operation'], now)

    def check_protection_deadlines(self, *, now):
        with self.serializer.acquire():
            try:
                self._check_protection_deadlines_locked(now=now)
            except Exception:
                self._input_send_suppressed = True
                raise

    def _snapshot_shape(self, snapshot):
        if type(snapshot) is not ProtectionSnapshot:
            return False
        if not all(_identity(x) for x in (snapshot.fact_id, snapshot.account, snapshot.account_epoch,
                                          snapshot.stream_id)) or not _aware(snapshot.as_of):
            return False
        if type(snapshot.sequence) is not int or snapshot.sequence < 0 or type(snapshot.complete) is not bool:
            return False
        if (type(snapshot.scope_legs) is not tuple or not snapshot.scope_legs
                or any(type(x) is not str or x not in ADAPTER_BY_LEG for x in snapshot.scope_legs)
                or len(set(snapshot.scope_legs)) != len(snapshot.scope_legs)):
            return False
        if any(type(x) is not tuple for x in (snapshot.orders, snapshot.positions, snapshot.resolved_operations)):
            return False
        ids, broker_ids = set(), set()
        for row in snapshot.orders:
            if type(row) is not ObservedProtection or row.leg_id not in snapshot.scope_legs:
                return False
            if not all(_identity(x) for x in (row.owner_id, row.entry_fill_id, row.order_symbol)):
                return False
            if row.owner_id in ids or type(row.quantity) is not int or row.quantity <= 0:
                return False
            ids.add(row.owner_id)
            if type(row.revision) is not int or row.revision < 1 or type(row.trail_active) is not bool:
                return False
            if row.operation_id is not None and not _identity(row.operation_id):
                return False
            if (type(row.broker_order_ids) is not tuple or not row.broker_order_ids
                    or any(not _identity(x) or x in broker_ids for x in row.broker_order_ids)
                    or len(set(row.broker_order_ids)) != len(row.broker_order_ids)):
                return False
            broker_ids.update(row.broker_order_ids)
            if validate_action(BracketAmend(row.leg_id, row.effective)) or not has_components(row.effective):
                return False
            if row.trail_anchor is not None and (not _number(row.trail_anchor) or row.trail_anchor <= 0):
                return False
            if row.trail_active and (row.trail_anchor is None or row.effective.trail_offset_ticks is None):
                return False
        for pairs, quantity in ((snapshot.positions, True), (snapshot.resolved_operations, False)):
            seen = set()
            for pair in pairs:
                if type(pair) is not tuple or len(pair) != 2 or not _identity(pair[0]) or pair[0] in seen:
                    return False
                seen.add(pair[0])
                if quantity:
                    if type(pair[1]) is not int or pair[1] < 0:
                        return False
                elif pair[1] not in ('applied', 'rejected'):
                    return False
        return True

    def observe_protection(self, snapshot, *, now):
        with self.serializer.acquire():
            try:
                return self._observe_protection_locked(snapshot, now=now)
            except Exception:
                self._input_send_suppressed = True
                raise

    def _observe_protection_locked(self, snapshot, *, now):
        self._check_protection_deadlines_locked(now=now)
        if not self._snapshot_shape(snapshot):
            self._record_input_incident_locked('protection-input:' + str(uuid4()),
                InputViolation('type', 'protection_snapshot'), source='protection', now=now)
            return ()
        with self._transaction() as db:
            previously_seen = db.execute('SELECT 1 FROM protection_facts WHERE fact_id=?',
                                        (snapshot.fact_id,)).fetchone()
            db.execute('SAVEPOINT protection_read')
            if not self._apply_protection_snapshot_db(db, snapshot, now=now):
                db.execute('ROLLBACK TO protection_read')
                db.execute('RELEASE protection_read')
                db.execute('INSERT OR IGNORE INTO protection_facts VALUES (?, ?, ?)',
                           (snapshot.fact_id, _dump(asdict(snapshot)), 'rejected_snapshot'))
                self._protection_fault(db, 'invalid-snapshot:' + snapshot.fact_id, now)
            else:
                db.execute('RELEASE protection_read')
                if not previously_seen:
                    return self._reconcile_close_protection_db(db, snapshot, now=now)
        return ()

    def _apply_protection_snapshot_db(self, db, snapshot, *, now):
        raw = _dump(asdict(snapshot))
        previous = db.execute('SELECT body,kind FROM protection_facts WHERE fact_id=?', (snapshot.fact_id,)).fetchone()
        if previous:
            if previous[0] != raw:
                self._protection_fault(db, 'fact-conflict:' + snapshot.fact_id, now)
                return False
            return previous[1] == 'snapshot'
        state = self._state(db)
        fault = None
        owners = self._protection_rows(db)
        ops = self._protection_operations(db)
        if (snapshot.account != state['account'] or snapshot.account_epoch != state['account_epoch']
                or not timedelta(0) <= now - snapshot.as_of <= PROTECTION_PERIOD):
            fault = 'binding-or-time'
        stream_row = db.execute('SELECT body FROM protection_streams WHERE stream_id=?', (snapshot.stream_id,)).fetchone()
        if stream_row:
            stream = json.loads(stream_row[0])
            if snapshot.sequence <= stream['sequence'] or snapshot.as_of < datetime.fromisoformat(stream['as_of']):
                fault = 'stream-order'
        elif db.execute('SELECT 1 FROM protection_streams').fetchone():
            fault = 'stream-binding'
        positions = dict(snapshot.positions)
        expected = {}
        for leg_id in snapshot.scope_legs:
            expected.update(self._open_fill_quantities(db, leg_id, subtract_reservations=False))
        if any(fid not in expected or qty != expected[fid] for fid, qty in positions.items()):
            fault = 'position-linkage'
        if snapshot.complete and any(positions.get(fid, 0) != qty for fid, qty in expected.items()):
            fault = 'position-completeness'
        observed = {r.owner_id: r for r in snapshot.orders}
        for leg_id in snapshot.scope_legs:
            coverage = sum(q for fid, q in expected.items()
                           if owners.get('protection:' + fid, {}).get('leg_id') == leg_id)
            if sum(row.quantity for row in snapshot.orders if row.leg_id == leg_id) > coverage:
                fault = 'overlapping-protection'
        for identity, row in observed.items():
            old = owners.get(identity)
            if (old is None or old['consumed'] or row.entry_fill_id != old['entry_fill_id']
                    or row.leg_id != old['leg_id'] or row.order_symbol != old['order_symbol']
                    or row.quantity > sum(q for fid, q in expected.items()
                                           if owners.get('protection:' + fid, {}).get('leg_id') == row.leg_id)
                    or row.revision < old['revision']):
                fault = 'owner-linkage'
                break
            pending = ops.get(old['pending_operation'])
            permitted = {pending['expected_operation_id']} if pending else set()
            if old.get('last_operation_id'):
                permitted.add(old['last_operation_id'])
            if row.operation_id not in permitted:
                fault = 'operation-linkage'
        db.execute('INSERT INTO protection_facts VALUES (?, ?, ?)', (snapshot.fact_id, raw, 'snapshot'))
        if fault:
            self._protection_fault(db, fault + ':' + snapshot.fact_id, now)
            return False
        db.execute('INSERT OR REPLACE INTO protection_streams VALUES (?, ?)',
                   (snapshot.stream_id, _dump(dict(sequence=snapshot.sequence, as_of=snapshot.as_of,
                                                   scope=list(snapshot.scope_legs), fact_id=snapshot.fact_id))))
        if not snapshot.complete:
            return True
        resolved = dict(snapshot.resolved_operations)
        valid = True
        for identity, old in owners.items():
            if old['leg_id'] not in snapshot.scope_legs or old['consumed']:
                continue
            row = observed.get(identity)
            pending = ops.get(old['pending_operation'])
            postdates = pending and snapshot.as_of > datetime.fromisoformat(pending['prepared_at'])
            outcome = resolved.get(pending['expected_operation_id']) if pending else None
            if pending and postdates and pending['status'] in ('pending_confirmation', 'rejected', 'unknown'):
                effective = bracket_from_dict(pending['effective'])
                matches = (row is not None and row.operation_id == pending['expected_operation_id']
                           and row.effective == effective and row.quantity == pending['quantity']
                           and row.revision > pending['old_revision'])
                removed = not has_components(effective) and row is None and outcome == 'applied'
                if (matches and outcome == 'applied') or removed:
                    pending['status'] = 'applied'
                    old['pending_operation'] = None
                    old['deadline'] = None
                    old['ever_protected'] = old['ever_protected'] or has_components(effective)
                    old['last_operation_id'] = pending['expected_operation_id']
                    self._put_protection_operation(db, pending)
                    db.execute("UPDATE operations SET status='observed' WHERE operation_id=?", (pending['operation_id'],))
                elif outcome == 'rejected':
                    intact = row is not None and pending['old'] is not None and row.effective == bracket_from_dict(pending['old'])
                    if pending['primitive'] == 'attach' or pending['primitive'] == 'entry_attach':
                        self._protection_fault(db, 'attach-rejected:' + pending['operation_id'], now)
                        # A linked definitive rejection is a coherent negative
                        # outcome. Retain successful siblings from this read.
                        # Unexpected live protection is still invalid below.
                    elif intact and row.revision == pending['old_revision']:
                        pending['status'] = 'rejected_intact'
                        old['pending_operation'] = None
                        old['deadline'] = None
                        self._put_protection_operation(db, pending)
                        db.execute("UPDATE operations SET status='terminal' WHERE operation_id=?", (pending['operation_id'],))
                    else:
                        self._protection_fault(db, 'rejected-unprotected:' + pending['operation_id'], now)
                        valid = False
                elif outcome == 'applied':
                    self._protection_fault(db, 'mismatched:' + pending['operation_id'], now)
                    valid = False
            if row is None:
                coverage = sum(q for fid, q in expected.items()
                               if owners.get('protection:' + fid, {}).get('leg_id') == old['leg_id'])
                closed_original = expected.get(old['entry_fill_id'], 0) == 0 and any(
                    any(fid == old['entry_fill_id'] for fid, _ in reduction.allocations)
                    and db.execute("SELECT 1 FROM operations WHERE operation_id=? AND kind IN ('exit','flat')",
                                   (reduction.close_request_id,)).fetchone()
                    for reduction in self._capacity(db).reductions)
                if (coverage == 0 or closed_original) and old['observed'] is not None and pending is None:
                    old.update(consumed=True, observed=None, quantity=0, broker_order_ids=[])
                elif old['observed'] is not None and not (pending and pending.get('status') == 'applied'
                                                       and not has_components(bracket_from_dict(pending['effective']))):
                    self._protection_fault(db, 'missing:' + identity + ':' + snapshot.fact_id, now)
                    valid = False
                elif pending and pending.get('status') == 'applied':
                    old['observed'], old['quantity'], old['broker_order_ids'] = None, 0, []
            else:
                # Observations while pending may prove old protection, but cannot
                # install desired state without the matching operation outcome.
                if old['observed'] is None and pending is None:
                    self._protection_fault(db, 'unrequested-attachment:' + snapshot.fact_id, now)
                    valid = False
                    continue
                if pending and pending['status'] not in ('applied', 'rejected_intact') and row.revision > pending['old_revision']:
                    if not postdates:
                        continue
                    if pending['status'] != 'applied':
                        self._protection_fault(db, 'unproved-revision:' + snapshot.fact_id, now)
                        valid = False
                        continue
                if not pending or pending['status'] != 'applied':
                    coverage = sum(q for fid, q in expected.items()
                                   if owners.get('protection:' + fid, {}).get('leg_id') == old['leg_id'])
                    if (old['observed'] is not None and (row.effective != bracket_from_dict(old['observed'])
                            or row.revision != old['revision']
                            or row.quantity != min(old['quantity'], coverage)
                            or list(row.broker_order_ids) != old['broker_order_ids'])):
                        self._protection_fault(db, 'unrequested-change:' + snapshot.fact_id, now)
                        valid = False
                        continue
                before = bracket_from_dict(old['observed'])
                if before is not None and 'trail' not in changed_components(before, row.effective) and old['trail_active']:
                    worsened = (row.trail_anchor is None or
                                (row.trail_anchor < old['trail_anchor'] if old['side'] == Side.BUY.value
                                 else row.trail_anchor > old['trail_anchor']))
                    if not row.trail_active or worsened:
                        self._protection_fault(db, 'trail-reset:' + snapshot.fact_id, now)
                        valid = False
                        continue
                old.update(observed=asdict(row.effective), quantity=row.quantity,
                           broker_order_ids=list(row.broker_order_ids), revision=row.revision,
                           trail_active=row.trail_active, trail_anchor=row.trail_anchor,
                           last_operation_id=row.operation_id, ever_protected=True)
            old['evidence_at'], old['evidence_fact'] = snapshot.as_of.isoformat(), snapshot.fact_id
            self._put_protection(db, old)
        return valid

    def _protection_admission(self, db, occurrence, rows, *, now, weakening):
        state = self._state(db)
        if state['authority'] == 'INTERVENTION' or getattr(self, '_input_send_suppressed', False):
            return 'intervention_fence'
        if state['authority'] == 'SCHEDULED_EXIT' and occurrence.producer != 'schedule':
            return 'mutation_not_authorized'
        refusal = self._validate_settlement_binding(db, now)
        if refusal:
            return refusal
        if weakening:
            session = self.binding['session']
            if (state['permission'] != 'RUNNING' or state['authority'] != 'NORMAL'
                    or not session.opens_at <= now < session.risk_add_cutoff
                    or not self.binding['as_of'] <= now < self.binding['valid_until']
                    or now - self.binding['as_of'] > self.binding['max_evidence_age']
                    or any(self.binding['lifecycle_tiers'][row['leg_id']] != 'AUTHORIZED' for row in rows)
                    or self._capacity(db).blocks
                    or self._ordinary_unknown_orders_db(db, now=now)
                    or db.execute("SELECT 1 FROM attempts a JOIN operations o USING(operation_id) "
                                  "WHERE a.state='UNKNOWN' AND o.status NOT IN ('terminal','observed')").fetchone()):
                return 'risk_add_not_authorized'
        return None

    def _dispatch_protection_locked(self, action, occurrence, key, *, now):
        result = self._prepare_dispatch_protection_locked(action, occurrence, key, now=now)
        if result.refusal_reason not in (None, 'awaiting_evidence', 'intervention_fence'):
            # A refused, unsent desire is not an outstanding broker mutation.
            # Attempted children and expired obligations remain retained.
            with self._transaction() as db:
                for op in self._protection_operations(db).values():
                    if (op['operation_id'].startswith('control:' + key + ':')
                            and op['status'] == 'awaiting_evidence'
                            and not db.execute('SELECT 1 FROM attempts WHERE operation_id=?',
                                               (op['operation_id'],)).fetchone()):
                        op['status'] = 'refused'
                        self._put_protection_operation(db, op)
                        row = self._protection_rows(db)[op['owner_id']]
                        if row['pending_operation'] == op['operation_id']:
                            row.update(pending_operation=None, deadline=None)
                            self._put_protection(db, row)
                        db.execute("UPDATE operations SET status='terminal' WHERE operation_id=?",
                                   (op['operation_id'],))
        return result

    def _prepare_dispatch_protection_locked(self, action, occurrence, key, *, now):
        from .book_account_owner import BrokerCommand, BrokerResult, DispatchResult, SimulatedOwnerCrash
        parent = 'control:' + key
        self._check_protection_deadlines_locked(now=now)
        with self._transaction() as db:
            state = self._state(db)
            if state['authority'] == 'INTERVENTION':
                return DispatchResult(parent, 0, refusal_reason='intervention_fence')
            record = db.execute('SELECT scope,prepared_at,generation,boot_id FROM action_occurrences WHERE key=?', (key,)).fetchone()
            if state['generation'] != record[2] or state['boot_id'] != record[3]:
                return DispatchResult(parent, 0, refusal_reason='stale_preparation')
            owners = self._protection_rows(db)
            if record[0] is None:
                if action.scope_fill_ids is None:
                    available = self._open_fill_quantities(db, action.leg_id, subtract_reservations=False)
                    ids = [identity for identity, row in owners.items() if row['leg_id'] == action.leg_id
                           and not row['consumed'] and (row['ever_protected'] or available.get(row['entry_fill_id'], 0) > 0)]
                else:
                    ids = ['protection:' + fid for fid in action.scope_fill_ids]
                if any(i not in owners or owners[i]['leg_id'] != action.leg_id for i in ids):
                    self._protection_fault(db, 'target:' + key, now)
                    return DispatchResult(parent, 0, refusal_reason='invalid_protection_target')
                db.execute('UPDATE action_occurrences SET scope=? WHERE key=?', (_dump(ids), key))
                if not ids:
                    return DispatchResult(parent, 0, refusal_reason='empty_scope')
                if any(owners[i]['consumed'] for i in ids):
                    return DispatchResult(parent, 0, refusal_reason='consumed_protection')
                if any(owners[i]['pending_operation'] for i in ids) or db.execute(
                        "SELECT 1 FROM operations WHERE kind IN ('exit','flat') AND status!='terminal' AND leg_id=?",
                        (action.leg_id,)).fetchone():
                    return DispatchResult(parent, 0, refusal_reason='amend_deferred')
                prepared = datetime.fromisoformat(record[1])
                for index, identity in enumerate(ids):
                    row = owners[identity]
                    child = parent + ':' + str(index)
                    effective = normalize_bracket(action.bracket, Side(row['side']), ADAPTER_BY_LEG[action.leg_id].mintick)
                    op = dict(operation_id=child, owner_id=identity, expected_operation_id=child,
                              primitive='amend' if row['ever_protected'] else 'attach', status='awaiting_evidence',
                              desired=asdict(action.bracket), effective=asdict(effective), quantity=0,
                              old=row['observed'], old_revision=row['revision'], prepared_at=record[1],
                              deadline=(prepared + PROTECTION_PERIOD).isoformat(), attempt_id=None)
                    if not row['ever_protected'] and not has_components(effective):
                        op['deadline'] = None
                    db.execute('INSERT INTO protection_operations VALUES (?, ?, ?, ?)', (child, key, identity, _dump(op)))
                    row.update(pending_operation=child, deadline=op['deadline'], desired=op['desired'])
                    self._put_protection(db, row)
            else:
                ids = json.loads(record[0])
            prepared = datetime.fromisoformat(record[1])
        reader = getattr(self.synthetic_broker, 'read_protection', None)
        if reader:
            snapshot = reader(ProtectionRead(occurrence, (action.leg_id,), prepared))
            if snapshot is not None:
                self._observe_protection_locked(snapshot, now=now)
        changes = []
        weakening = False
        with self._transaction() as db:
            state = self._state(db)
            if state['authority'] == 'INTERVENTION':
                return DispatchResult(parent, 0, refusal_reason='intervention_fence')
            owners, ops = self._protection_rows(db), self._protection_operations(db)
            available = self._open_fill_quantities(db, action.leg_id, subtract_reservations=False)
            for index, identity in enumerate(ids):
                row, op = owners[identity], ops[parent + ':' + str(index)]
                if not row['evidence_at'] or not prepared < datetime.fromisoformat(row['evidence_at']) <= now:
                    return DispatchResult(parent, 0, refusal_reason='awaiting_evidence')
                if now - datetime.fromisoformat(row['evidence_at']) > PROTECTION_PERIOD:
                    return DispatchResult(parent, 0, refusal_reason='awaiting_evidence')
                effective = bracket_from_dict(op['effective'])
                old = bracket_from_dict(row['observed'])
                if row['ever_protected'] and old is None:
                    return DispatchResult(parent, 0, refusal_reason='amend_deferred')
                quantity = row['quantity'] if old is not None else available.get(row['entry_fill_id'], 0)
                if quantity <= 0 or row['consumed']:
                    return DispatchResult(parent, 0, refusal_reason='consumed_protection')
                components = changed_components(old, effective)
                if old is not None and is_loosening(old, effective, Side(row['side'])):
                    weakening = True
                refusal = self._protection_admission(db, occurrence, [owners[i] for i in ids],
                                                     now=now, weakening=weakening)
                if refusal:
                    return DispatchResult(parent, 0, refusal_reason=refusal)
                op.update(quantity=quantity, old=row['observed'], old_revision=row['revision'])
                if not components:
                    op['status'] = 'noop'
                    row.update(pending_operation=None, deadline=None)
                    self._put_protection(db, row)
                else:
                    target = ProtectionTarget(identity, row['entry_fill_id'], action.leg_id,
                        row['order_symbol'], Side(row['side']), quantity, op['primitive'])
                    changes.append((op, ProtectionChange(target, action.bracket, effective, components)))
                self._put_protection_operation(db, op)
            for op, change in changes:
                db.execute('INSERT INTO operations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (op['operation_id'], action.leg_id, leg(action.leg_id).order_symbol, 'bracketamend',
                     None, change.target.quantity, occurrence.session_id, state['generation'], now.isoformat(),
                     'reserved', _dump(asdict(action))))
        if not changes:
            return DispatchResult(parent, 0, refusal_reason='unchanged_protection')
        if self.crash_at == 'after_reservation':
            raise SimulatedOwnerCrash('after protection preparation')
        last_attempt, transports = None, []
        for op, change in changes:
            with self._transaction() as db:
                state = self._state(db)
                current_record = db.execute('SELECT generation,boot_id FROM action_occurrences WHERE key=?', (key,)).fetchone()
                if current_record != (state['generation'], state['boot_id']):
                    return DispatchResult(parent, 0, refusal_reason='stale_preparation')
                current_rows = self._protection_rows(db)
                refusal = self._protection_admission(db, occurrence, [current_rows[i] for i in ids],
                                                     now=now, weakening=weakening)
                if refusal:
                    return DispatchResult(parent, 0, last_attempt, refusal_reason=refusal)
                current = current_rows[change.target.owner_id]
                if (current['consumed'] or current['pending_operation'] != op['operation_id']
                        or not prepared < datetime.fromisoformat(current['evidence_at']) <= now
                        or now - datetime.fromisoformat(current['evidence_at']) > PROTECTION_PERIOD):
                    return DispatchResult(parent, 0, last_attempt, refusal_reason='stale_protection_evidence')
                last_attempt = str(uuid4())
                command = BrokerCommand(last_attempt, op['operation_id'], action.leg_id, 'bracketamend',
                    None, change.target.quantity, change.target.order_symbol, state['authority'], state['generation'],
                    action, occurrence=occurrence, protection_change=change)
                db.execute("INSERT INTO attempts VALUES (?, ?, 'UNKNOWN', ?, ?, NULL)",
                    (last_attempt, op['operation_id'], state['generation'], _dump(asdict(command))))
                db.execute("UPDATE operations SET status='attempted' WHERE operation_id=?", (op['operation_id'],))
                op.update(status='pending_confirmation', attempt_id=last_attempt)
                self._put_protection_operation(db, op)
            if self.crash_at == 'before_send':
                raise SimulatedOwnerCrash('after protection attempt before send')
            try:
                result = self.synthetic_broker.send(command) if self.synthetic_broker else BrokerResult('unknown')
            except Exception:
                result = BrokerResult('unknown')
            if not isinstance(result, BrokerResult) or result.state not in ('accepted', 'rejected', 'unknown'):
                result = BrokerResult('unknown')
            if self.crash_at == 'after_send':
                raise SimulatedOwnerCrash('after protection send before observation')
            transports.append(result.state)
            with self._transaction() as db:
                db.execute('UPDATE attempts SET state=?,observation=? WHERE attempt_id=?',
                           (result.state.upper(), _dump({'state': result.state}), last_attempt))
                if result.state in ('rejected', 'unknown'):
                    op['status'] = result.state
                    self._put_protection_operation(db, op)
                if result.state == 'unknown' or result.state == 'rejected' and op['primitive'] == 'attach':
                    self._protection_fault(db, result.state + ':' + op['operation_id'], now)
                    break
        transport = 'unknown' if 'unknown' in transports else 'rejected' if 'rejected' in transports else 'accepted'
        return DispatchResult(parent, 0, last_attempt, transport)

    def observe_protection_execution(self, event, *, now):
        from .book_account_owner import opposite
        with self.serializer.acquire():
            try:
                self._check_protection_deadlines_locked(now=now)
                if (type(event) is not ProtectionExecution or not self._snapshot_shape(event.snapshot)
                        or not all(_identity(x) for x in (event.fact_id, event.account, event.account_epoch,
                                                         event.owner_id, event.broker_order_id))
                        or not _aware(event.as_of) or type(event.quantity) is not int or event.quantity <= 0
                        or not _number(event.price) or event.price <= 0 or type(event.terminal) is not bool
                        or type(event.allocations) is not tuple
                        or any(type(pair) is not tuple or len(pair) != 2 or not _identity(pair[0])
                               or type(pair[1]) is not int or pair[1] <= 0 for pair in event.allocations)):
                    self._record_input_incident_locked('protection-execution:' + str(uuid4()),
                        InputViolation('type', 'protection_execution'), source='protection', now=now)
                    return ()
                raw = _dump(asdict(event))
                with self._transaction() as db:
                    previous = db.execute('SELECT body FROM protection_facts WHERE fact_id=?', (event.fact_id,)).fetchone()
                    if previous:
                        if previous[0] != raw:
                            self._protection_fault(db, 'execution-conflict:' + event.fact_id, now)
                        return ()
                    state = self._state(db)
                    owners = self._protection_rows(db)
                    from .book_migration import legacy_ids
                    legacy_fills = legacy_ids(db, 'fill')
                    if (event.account == state['account'] and event.account_epoch == state['account_epoch']
                            and any(fid in legacy_fills for fid, _qty in event.allocations)):
                        db.execute('INSERT INTO protection_facts VALUES (?, ?, ?)',
                                   (event.fact_id, raw, 'legacy_unresolved'))
                        return ()
                    row = owners.get(event.owner_id)
                    valid = (row is not None and not row['consumed'] and row['observed'] is not None
                             and event.account == state['account'] and event.account_epoch == state['account_epoch']
                             and event.broker_order_id in row['broker_order_ids'] and event.quantity <= row['quantity']
                             and timedelta(0) <= now - event.as_of <= PROTECTION_PERIOD
                             and row['evidence_at'] is not None
                             and event.as_of >= datetime.fromisoformat(row['evidence_at'])
                             and event.snapshot.as_of >= event.as_of and event.snapshot.complete
                             and row['leg_id'] in event.snapshot.scope_legs
                             and not db.execute('SELECT 1 FROM protection_facts WHERE fact_id=?',
                                                (event.snapshot.fact_id,)).fetchone())
                    expected = []
                    if valid:
                        remaining = event.quantity
                        for fid, qty in self._open_fill_quantities(db, row['leg_id'], subtract_reservations=False).items():
                            take = min(remaining, max(0, qty))
                            if take:
                                expected.append((fid, take))
                                remaining -= take
                        valid = remaining == 0 and tuple(expected) == event.allocations
                    if not valid:
                        self._protection_fault(db, 'invalid-execution:' + event.fact_id, now)
                        return ()
                    after = {o.owner_id: o for o in event.snapshot.orders}
                    trigger = after.get(event.owner_id)
                    if (event.terminal and trigger is not None or not event.terminal and
                            (trigger is None or trigger.quantity != row['quantity'] - event.quantity)):
                        self._protection_fault(db, 'execution-remainder:' + event.fact_id, now)
                        return ()
                    # Savepoint allows a failed residual snapshot to keep only its
                    # diagnostic, never a partially applied execution/feedback.
                    db.execute('SAVEPOINT protection_execution')
                    self._append_capacity(db, 'reduction', Reduction(event.fact_id,
                        'protective:' + event.fact_id, event.allocations), event.as_of,
                        event_id='protection-fill:' + event.fact_id)
                    if event.terminal:
                        # Consumption of the working order is not an outcome
                        # for a separately pending mutation of that order.
                        row.update(consumed=True, observed=None, quantity=0, broker_order_ids=[])
                        self._put_protection(db, row)
                    else:
                        row['quantity'] -= event.quantity
                        self._put_protection(db, row)
                    if not self._apply_protection_snapshot_db(db, event.snapshot, now=now):
                        db.execute('ROLLBACK TO protection_execution')
                        db.execute('RELEASE protection_execution')
                        self._protection_fault(db, 'execution-snapshot:' + event.fact_id, now)
                        return ()
                    db.execute('INSERT INTO protection_facts VALUES (?, ?, ?)', (event.fact_id, raw, 'execution'))
                    events = list(self._reconcile_close_protection_db(db, event.snapshot, now=now))
                    for index, (fid, qty) in enumerate(event.allocations):
                        fact_id = event.fact_id + ':' + str(index)
                        fill = Fill(fact_id, 'protective:' + event.fact_id, row['leg_id'], 'exit',
                                    opposite(Side(row['side'])), qty, event.price, event.as_of,
                                    entry_fill_id=fid, reason='protective_execution')
                        feedback = ExecutionEvent('fill', row['leg_id'], event.as_of,
                                                  fill=fill, order_id=fill.order_id)
                        db.execute('INSERT INTO feedback(fact_id,body,delivered,boundary_time) VALUES (?, ?, 0, ?)',
                                   (fact_id, _dump(asdict(feedback)), event.as_of.isoformat()))
                        self._append_timeline(db, 'feedback', fact_id, now)
                        events.append(feedback)
                    db.execute('RELEASE protection_execution')
                    return tuple(events)
            except Exception:
                self._input_send_suppressed = True
                raise
