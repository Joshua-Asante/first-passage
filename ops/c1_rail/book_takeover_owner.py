"""Evidence-gated takeover journal owned by the account's existing serializer."""
from dataclasses import asdict, replace
from datetime import datetime, timedelta
import hashlib
import json
from uuid import uuid4

from .book_capacity import CompleteTakeover, Quiescence, exposures, used_micro
from .book_policy import ACCOUNT_MICRO_CAP, BOOK_LEGS, leg
from .book_protection import ActionOccurrence, occurrence_key
from .book_sizing_context import size_book_request
from .book_takeover import AccountInventory, InventoryRead, InventoryPosition, WorkingOrder, RequestOutcome
from c1_signal_daemon.book_protocol import Cancel, OrderIntent
from c1_signal_daemon.book_validation import validate_action, validate_bar


def _dump(value):
    from .book_account_owner import _body
    return _body(value)


def _require(ok, reason):
    if not ok:
        raise ValueError(reason)


class TakeoverOwnerMixin:
    def _takeover_plan_db(self, db, identity):
        row = db.execute('SELECT body FROM takeover_plans WHERE operation_id=?', (identity,)).fetchone()
        return json.loads(row[0]) if row else None

    def _takeover_event_db(self, db, identity, kind, now, **values):
        previous = db.execute('SELECT ordinal,kind FROM takeover_events WHERE operation_id=? ORDER BY ordinal DESC LIMIT 1',
                              (identity,)).fetchone()
        ordinal = previous[0] + 1 if previous else 0
        body = dict(record_version=1, previous=previous[1] if previous else None,
                    at=now.isoformat(), generation=self._state(db)['generation'],
                    capacity_sequence=self._capacity(db).sequence, **values)
        db.execute('INSERT INTO takeover_events VALUES (?, ?, ?, ?, ?)',
                   (identity + ':' + str(ordinal), identity, ordinal, kind, _dump(body)))
        self._takeover_committed_phase = kind

    def _publish_takeover_db(self, db, action, occurrence, quantity, now):
        state, capacity = self._state(db), self._capacity(db)
        displaced = capacity.takeover.displaced
        from .book_account_owner import _binding_record
        request, context, binding = self._context(db, action, now)
        operations = tuple(o.request.operation_id for o in capacity.operations if o.request.leg_id in displaced and o.status == 'active')
        body = dict(record_version=1, **{k: state[k] for k in ('account', 'account_epoch', 'boot_id', 'generation')},
            session_id=occurrence.session_id, action=asdict(action), occurrence=asdict(occurrence),
            quantity=quantity, displaced=displaced, operations=operations,
            scope_operations=tuple(r[0] for r in db.execute('SELECT operation_id,leg_id FROM operations') if r[1] in displaced),
            fills=tuple(f.execution_id for f in capacity.fills if f.operation_id in operations),
            owners=tuple(r[0] for r in db.execute('SELECT owner_id FROM protection_owners')),
            unresolved=tuple(r[1] for r in self._unresolved_attempt_rows(db)),
            request=asdict(request), binding={**asdict(binding), 'max_evidence_age': binding.max_evidence_age.total_seconds()}, created_at=now.isoformat(),
            capacity_sequence=capacity.sequence, admission_binding=_binding_record(self.binding),
            runtime_actor=db.execute('SELECT kind,body FROM runtime_actors WHERE boot_id=?', (state['boot_id'],)).fetchone())
        db.execute('INSERT INTO takeover_plans VALUES (?, ?, ?)', (action.order_id, occurrence_key(occurrence), _dump(body)))
        self._takeover_event_db(db, action.order_id, 'PLAN', now)

    def _takeover_marker_db(self, db):
        # Evidence currency is invalidated by *any* intervening account mutation.
        # A halt changes authority, not broker history: a read already in flight
        # may still update accounting. Send paths separately bind boot/generation.
        value = [self._capacity(db).sequence]
        for table, columns in (('operations', 'operation_id,status'), ('attempts', 'attempt_id,state'),
                               ('protection_owners', 'owner_id,body'), ('protection_operations', 'operation_id,body')):
            value.append(tuple(db.execute(f'SELECT {columns} FROM {table} ORDER BY 1')))
        return hashlib.sha256(_dump(value).encode()).hexdigest()

    def _takeover_phase_db(self, db, identity):
        row = db.execute("SELECT kind FROM takeover_events WHERE operation_id=? AND kind!='HALT' ORDER BY ordinal DESC LIMIT 1", (identity,)).fetchone()
        return row[0] if row else None

    def _validate_takeover_state_db(self, db):
        from .book_account_owner import AccountOwnerError
        try:
            plans = dict(db.execute('SELECT operation_id,body FROM takeover_plans'))
            capacity = self._capacity(db)
            required = {o.request.operation_id for o in capacity.operations if o.status == 'takeover'}
            required.update(c.operation_id for c in capacity.completed_takeovers)
            from .book_migration import legacy_ids
            legacy = legacy_ids(db, 'takeover') if getattr(self, '_read_schema_version', 4) == 4 else set()
            _require(not legacy & plans.keys() and required <= plans.keys() | legacy, 'missing takeover plan')
            for identity, raw in plans.items():
                plan = json.loads(raw)
                fields = {'record_version', 'account', 'account_epoch', 'boot_id', 'generation', 'session_id',
                          'action', 'occurrence', 'quantity', 'displaced', 'operations', 'scope_operations',
                          'fills', 'owners', 'unresolved', 'request', 'binding', 'created_at',
                          'capacity_sequence', 'admission_binding', 'runtime_actor'}
                _require(set(plan) == fields, 'missing or unknown takeover plan field')
                _require(plan['record_version'] == 1 and plan['action']['order_id'] == identity,
                         'invalid takeover plan')
                _require(type(plan['quantity']) is int and plan['quantity'] > 0
                         and type(plan['generation']) is int and plan['generation'] > 0
                         and type(plan['capacity_sequence']) is int and plan['capacity_sequence'] > 0,
                         'invalid takeover quantity or generation')
                _require(datetime.fromisoformat(plan['created_at']).utcoffset() is not None,
                         'invalid plan time')
                _require(type(plan['boot_id']) is str and bool(plan['boot_id']) and type(plan['session_id']) is str,
                         'invalid plan actor')
                op = db.execute('SELECT quantity,generation,session_id,body FROM operations WHERE operation_id=?', (identity,)).fetchone()
                _require(op is not None and op[:3] == (plan['quantity'], plan['generation'], plan['session_id'])
                         and json.loads(op[3]) == plan['action'], 'plan operation mismatch')
                _require(validate_action(self._restore_intent(_dump(plan['action']))) is None, 'invalid retained action')
                _require(plan['request']['operation_id'] == identity and plan['request']['leg_id'] == 'aegis_6j'
                         and plan['binding']['account_id'] == self.account
                         and plan['admission_binding']['session']['session_id'] == plan['session_id'], 'invalid admission witness')
                retained_binding = db.execute('SELECT body FROM runtime_bindings WHERE session_id=?', (plan['session_id'],)).fetchone()
                _require(retained_binding is not None and json.loads(retained_binding[0]) == plan['admission_binding'], 'missing admission binding')
                for name in ('operations', 'scope_operations', 'fills', 'owners', 'unresolved', 'displaced'):
                    _require(type(plan[name]) is list and all(type(x) is str and x for x in plan[name])
                             and len(set(plan[name])) == len(plan[name]), 'invalid plan identity set')
                _require(set(plan['operations']) <= set(plan['scope_operations']), 'incomplete operation scope')
                for op_id in plan['scope_operations']:
                    row = db.execute('SELECT leg_id FROM operations WHERE operation_id=?', (op_id,)).fetchone()
                    _require(row is not None and row[0] in plan['displaced'], 'missing scoped operation')
                _require(plan['account'] == self.account and plan['account_epoch'] == capacity.owner_epoch,
                         'foreign takeover plan')
                _require(tuple(plan['displaced']) == tuple(sorted(set(plan['displaced']), key=lambda x: leg(x).priority, reverse=True)), 'invalid displaced order')
                _require(plan['displaced'] and all(leg(x).priority > 1 for x in plan['displaced']), 'invalid displaced scope')
                occurrence = ActionOccurrence(**plan['occurrence'])
                row = db.execute('SELECT source FROM action_occurrences WHERE key=?', (occurrence_key(occurrence),)).fetchone()
                _require(row is not None and json.loads(row[0])['value'] == plan['action'], 'missing takeover occurrence')
                events = tuple(db.execute('SELECT ordinal,kind,body FROM takeover_events WHERE operation_id=? ORDER BY ordinal', (identity,)))
                _require(events and events[0][1] == 'PLAN', 'missing takeover phase')
                previous = None
                phase = None
                referenced_children = set()
                transitions = {None: ('PLAN',), 'PLAN': ('CANCEL',), 'CANCEL': ('CONFIRM_CANCELLATIONS',),
                    'CONFIRM_CANCELLATIONS': ('CLOSE_DISPLACED',), 'CLOSE_DISPLACED': ('CONFIRM_QUIESCENCE',),
                    'CONFIRM_QUIESCENCE': ('REVALIDATE',), 'REVALIDATE': ('ATTEMPTED',), 'ATTEMPTED': (), 'RETIRED': ()}
                for index, (ordinal, kind, event_raw) in enumerate(events):
                    event = json.loads(event_raw)
                    _require(ordinal == index and event['previous'] == previous and event['record_version'] == 1,
                             'invalid takeover phase chain')
                    _require(datetime.fromisoformat(event['at']).utcoffset() is not None, 'invalid phase time')
                    _require(kind in ('PLAN', 'CANCEL', 'CONFIRM_CANCELLATIONS', 'CLOSE_DISPLACED',
                                      'CONFIRM_QUIESCENCE', 'REVALIDATE', 'ATTEMPTED', 'RETIRED', 'HALT'), 'invalid phase')
                    if kind not in ('HALT', 'RETIRED'):
                        _require(kind in transitions[phase], 'illegal takeover transition')
                        phase = kind
                    elif kind == 'RETIRED':
                        _require(phase not in ('ATTEMPTED', 'RETIRED'), 'invalid retirement')
                        phase = kind
                    for child in event.get('children', ()):
                        _require(db.execute('SELECT 1 FROM takeover_children WHERE operation_id=? AND takeover_id=?',
                                            (child, identity)).fetchone(), 'missing takeover child')
                        referenced_children.add(child)
                    if kind == 'REVALIDATE':
                        evidence = db.execute('SELECT disposition FROM takeover_inventory WHERE fact_id=?', (event['inventory_id'],)).fetchone()
                        _require(evidence == ('qualified',), 'missing takeover proof')
                        _require(event['counts'] == [0, 0, 0, 0] and event['pending'] == []
                                 and type(event['marker']) is str and len(event['marker']) == 64, 'invalid proof counts')
                        _require(db.execute('SELECT 1 FROM takeover_reads WHERE read_id=? AND operation_id=?',
                                            (event['read_id'], identity)).fetchone(), 'missing proof read')
                    previous = kind
                if any(c.operation_id == identity for c in capacity.completed_takeovers):
                    _require(any(k == 'REVALIDATE' for _, k, _ in events), 'missing completion proof')
                _require({r[0] for r in db.execute('SELECT operation_id FROM takeover_children WHERE takeover_id=?', (identity,))}
                         == referenced_children, 'unpublished takeover child')
            for op, root, key, kind, target, raw in db.execute('SELECT * FROM takeover_children'):
                child = json.loads(raw)
                _require(set(child) == {'record_version', 'operation_id', 'occurrence', 'action', 'prepared_at', 'generation'}, 'invalid child fields')
                _require(root in plans and child['record_version'] == 1 and child['operation_id'] == op,
                         'orphan takeover child')
                _require(occurrence_key(ActionOccurrence(**child['occurrence'])) == key and kind in ('cancel', 'flat'), 'invalid child occurrence')
                _require(child['action']['order_id'] == target if kind == 'cancel' else child['action']['leg_id'] == target,
                         'invalid child target')
                _require(datetime.fromisoformat(child['prepared_at']).utcoffset() is not None
                         and type(child['generation']) is int, 'invalid child time')
                action = Cancel(**child['action']) if kind == 'cancel' else self._restore_intent(_dump(child['action']))
                _require(validate_action(action) is None, 'invalid child action')
            for read_id, root, raw in db.execute('SELECT * FROM takeover_reads'):
                read = json.loads(raw)
                _require(set(read) == {'record_version', 'expected_stream', 'prepared_marker', 'read_id', 'occurrence',
                                      'scope_legs', 'prepared_at', 'after_sequence'}, 'invalid read fields')
                _require(root in plans and read['read_id'] == read_id and read['record_version'] == 1, 'invalid takeover read')
                _require(datetime.fromisoformat(read['prepared_at']).utcoffset() is not None
                         and type(read['after_sequence']) is int and read['after_sequence'] >= 0
                         and type(read['expected_stream']) is str and len(read['prepared_marker']) == 64, 'invalid read witness')
            for fact_id, stream, sequence, raw, disposition in db.execute('SELECT * FROM takeover_inventory'):
                retained = json.loads(raw)
                snap = retained['snapshot']
                _require(retained['record_version'] == 1 and retained['root'] in plans
                         and (snap['fact_id'], snap['stream_id'], snap['sequence']) == (fact_id, stream, sequence), 'invalid retained inventory')
                _require(db.execute('SELECT 1 FROM takeover_reads WHERE read_id=? AND operation_id=?',
                                    (snap['read_id'], retained['root'])).fetchone(), 'missing inventory read')
                if disposition == 'qualified':
                    _require(db.execute('SELECT 1 FROM takeover_streams WHERE stream_id=?', (stream,)).fetchone(), 'missing inventory stream')
            for stream, raw in db.execute('SELECT * FROM takeover_streams'):
                cursor = json.loads(raw)
                _require(db.execute('SELECT 1 FROM takeover_inventory WHERE fact_id=? AND stream_id=? AND sequence=? AND disposition=?',
                         (cursor['fact_id'], stream, cursor['sequence'], 'qualified')).fetchone(), 'missing inventory cursor fact')
        except (ValueError, TypeError, KeyError, IndexError, AttributeError) as exc:
            raise AccountOwnerError('invalid takeover journal: ' + str(exc)) from exc

    def prepare_takeover_inventory(self, *, now):
        from .book_account_owner import _time
        _time(now)
        with self.serializer.acquire(), self._transaction() as db:
            self._validate_takeover_state_db(db)
            rows = tuple(db.execute("SELECT operation_id FROM operations WHERE status='takeover_pending'"))
            if not rows:
                return None
            identity = rows[0][0]
            plan = self._takeover_plan_db(db, identity)
            if plan is None:
                # A source-bound legacy obligation is retained, never upgraded
                # into a fabricated C read scope or quiescence proof.
                return None
            cursor = db.execute('SELECT body FROM takeover_streams').fetchone()
            sequence = json.loads(cursor[0])['sequence'] if cursor else 0
            read = InventoryRead(str(uuid4()), ActionOccurrence(**plan['occurrence']), tuple(plan['displaced']), now, sequence)
            stream = getattr(self.synthetic_broker, 'stream_id', None)
            if not stream or not callable(getattr(self.synthetic_broker, 'read_inventory', None)):
                return None
            db.execute('INSERT INTO takeover_reads VALUES (?, ?, ?)',
                       (read.read_id, identity, _dump(dict(record_version=1, expected_stream=stream + ':inventory',
                                                         prepared_marker=self._takeover_marker_db(db), **asdict(read)))))
            return read

    def observe_takeover_inventory(self, snapshot, *, now):
        from .book_account_owner import _time
        _time(now)
        with self.serializer.acquire():
            try:
                self._check_protection_deadlines_locked(now=now)
                return self._observe_takeover_inventory_locked(snapshot, now=now)
            except Exception:
                self._input_send_suppressed = True
                raise

    def _inventory_shape(self, snap):
        from .book_account_owner import BrokerFact
        _require(isinstance(snap, AccountInventory), 'typed inventory required')
        _require(all(type(v) is str and v and v == v.strip() for v in
                     (snap.fact_id, snap.account, snap.account_epoch, snap.stream_id, snap.read_id)), 'invalid inventory identity')
        _require(type(snap.sequence) is int and snap.sequence > 0, 'invalid inventory sequence')
        _require(isinstance(snap.as_of, datetime) and snap.as_of.utcoffset() is not None, 'invalid inventory time')
        _require(type(snap.complete) is bool and type(snap.scope_legs) is tuple
                 and len(set(snap.scope_legs)) == len(snap.scope_legs), 'invalid inventory scope')
        for rows, cls, key in ((snap.positions, InventoryPosition, 'fill_id'),
                               (snap.working_orders, WorkingOrder, 'broker_order_id'),
                               (snap.requests, RequestOutcome, 'operation_id'), (snap.facts, BrokerFact, 'fact_id')):
            _require(type(rows) is tuple and all(isinstance(r, cls) for r in rows), 'invalid inventory rows')
            _require(len({getattr(r, key) for r in rows}) == len(rows), 'duplicate inventory rows')
        _require(self._snapshot_shape(snap.protection), 'invalid protection inventory')

    def _observe_takeover_inventory_locked(self, snap, *, now):
        from .book_account_owner import MAX_FACT_AGE
        with self._transaction() as db:
            self._validate_takeover_state_db(db)
            state = self._state(db)
            raw = root = None
            savepoint = False
            try:
                self._inventory_shape(snap)
                raw = _dump(asdict(snap))
                old = db.execute('SELECT body FROM takeover_inventory WHERE fact_id=? OR (stream_id=? AND sequence=?)',
                                 (snap.fact_id, snap.stream_id, snap.sequence)).fetchone()
                if old:
                    _require(json.loads(old[0])['snapshot'] == json.loads(raw), 'inventory identity conflict')
                    return ()  # no currency renewal, including previously refused evidence
                read_row = db.execute('SELECT operation_id,body FROM takeover_reads WHERE read_id=?', (snap.read_id,)).fetchone()
                _require(read_row is not None, 'unknown inventory read')
                root, read_raw = read_row
                read = json.loads(read_raw)
                _require(snap.stream_id == read['expected_stream'], 'unregistered inventory stream')
                _require(read['prepared_marker'] == self._takeover_marker_db(db), 'inventory read predates account mutation')
                plan = self._takeover_plan_db(db, root)
                _require((snap.account, snap.account_epoch) == (state['account'], state['account_epoch']), 'foreign inventory')
                _require(snap.scope_legs == tuple(plan['displaced']) == tuple(read['scope_legs']), 'incomplete scope')
                _require(snap.complete and snap.protection.complete, 'incomplete inventory')
                _require(datetime.fromisoformat(read['prepared_at']) < snap.as_of <= now
                         and now - snap.as_of <= min(MAX_FACT_AGE, self.binding['max_evidence_age']), 'stale inventory')
                _require(snap.sequence > read['after_sequence'], 'stale stream')
                streams = tuple(db.execute('SELECT stream_id,body FROM takeover_streams'))
                if streams:
                    cursor = json.loads(streams[0][1])
                    _require(streams[0][0] == snap.stream_id and snap.sequence > cursor['sequence']
                             and snap.as_of >= datetime.fromisoformat(cursor['as_of']), 'inventory stream conflict')
                _require((snap.protection.account, snap.protection.account_epoch, snap.protection.scope_legs, snap.protection.as_of)
                         == (snap.account, snap.account_epoch, snap.scope_legs, snap.as_of), 'incoherent protection inventory')
                operations = {r[0]: r[1:] for r in db.execute('SELECT operation_id,leg_id,kind,status,body FROM operations')}
                known = set(plan['scope_operations']) | {r[0] for r in db.execute('SELECT operation_id FROM takeover_children WHERE takeover_id=?', (root,))}
                known.update(r['expected_operation_id'] for r in self._protection_operations(db).values()
                             if self._protection_rows(db)[r['owner_id']]['leg_id'] in snap.scope_legs)
                for op_id, created_at in db.execute('SELECT operation_id,created_at FROM operations'):
                    if op_id in known:
                        _require(datetime.fromisoformat(created_at) <= datetime.fromisoformat(read['prepared_at']),
                                 'inventory read predates scoped request')
                for retained_raw, in db.execute('SELECT body FROM broker_facts'):
                    retained_fact = json.loads(retained_raw)
                    if retained_fact['operation_id'] in known:
                        _require(datetime.fromisoformat(retained_fact['as_of']) <= snap.as_of,
                                 'inventory predates retained causal fact')
                for fact in snap.facts:
                    _require(fact.operation_id in known and fact.operation_id in operations, 'unknown inventory fact')
                    _require(operations[fact.operation_id][0] in snap.scope_legs, 'foreign inventory fact')
                    _require(isinstance(fact.as_of, datetime) and fact.as_of.utcoffset() is not None
                             and fact.as_of <= snap.as_of, 'inventory predates causal fact')
                    retained = db.execute('SELECT body FROM broker_facts WHERE fact_id=?', (fact.fact_id,)).fetchone()
                    _require(retained is None or retained[0] == _dump(asdict(fact)), 'conflicting retained broker fact')
                    _require(fact.kind in ('fill', 'terminal'), 'invalid inventory fact kind')
                    if fact.kind == 'terminal':
                        quantity = db.execute('SELECT quantity FROM operations WHERE operation_id=?', (fact.operation_id,)).fetchone()[0]
                        _require(type(fact.cumulative_filled) is int and 0 <= fact.cumulative_filled <= quantity
                                 and fact.status in ('filled', 'cancelled', 'rejected'), 'invalid terminal cumulative')
                    else:
                        from lib.validation import require_finite_number
                        require_finite_number(fact.price, field='fill price', strictly_positive=True)
                        _require(type(fact.quantity) is int and fact.quantity > 0, 'invalid fill quantity')
                attempts = dict(db.execute('SELECT operation_id,attempt_id FROM attempts'))
                for request in snap.requests:
                    _require(request.operation_id in known and request.operation_id in operations
                             and attempts.get(request.operation_id) == request.attempt_id, 'unknown provider request')
                    _require(request.status in ('pending', 'applied', 'rejected', 'unknown'), 'invalid provider outcome')
                    body = json.loads(operations[request.operation_id][3])
                    target = body['order_id'] if operations[request.operation_id][1] == 'cancel' else None
                    _require(request.target_operation_id == target, 'invalid request target')
                expected_requests = {op for op in known if op in attempts}
                _require({r.operation_id for r in snap.requests} == expected_requests, 'missing provider request')
                for order in snap.working_orders:
                    _require(order.operation_id in known and order.operation_id in operations, 'unknown working order')
                    op = operations[order.operation_id]
                    _require(order.leg_id == op[0] and order.order_symbol == leg(op[0]).order_symbol
                             and order.kind == op[1] and type(order.remaining) is int and order.remaining > 0, 'invalid working order')
                _require(len({r.operation_id for r in snap.working_orders}) == len(snap.working_orders), 'duplicate working operation')
                # An envelope missing causal fills cannot resolve a terminal.
                capacity = self._capacity(db)
                seen = {r[0] for r in db.execute('SELECT fact_id FROM broker_facts')}
                totals = {op: sum(f.quantity for f in capacity.fills if f.operation_id == op) for op in known}
                for fact in snap.facts:
                    if fact.fact_id not in seen and fact.kind == 'fill' and fact.order_kind in ('entry', 'add'):
                        totals[fact.operation_id] += fact.quantity
                for fact in snap.facts:
                    if fact.kind == 'terminal' and operations[fact.operation_id][1] in ('entry', 'add'):
                        _require(fact.cumulative_filled >= totals[fact.operation_id], 'terminal contradicts confirmed fills')
                        if fact.cumulative_filled != totals[fact.operation_id]:
                            db.execute('INSERT INTO takeover_inventory VALUES (?, ?, ?, ?, ?)',
                                (snap.fact_id, snap.stream_id, snap.sequence,
                                 _dump(dict(record_version=1, snapshot=json.loads(raw), root=root,
                                            reason='missing_causal_fills')), 'unqualified'))
                            return ()  # retain original obligations; no invented allocation
                db.execute('SAVEPOINT takeover_inventory_apply')
                savepoint = True
                before_incidents = db.execute('SELECT count(*) FROM incidents').fetchone()[0]
                events = []
                for fact in sorted(snap.facts, key=lambda f: (f.as_of, f.kind == 'terminal')):
                    events.extend(self._observe_locked(fact, now=now, db=db))
                _require(db.execute('SELECT count(*) FROM incidents').fetchone()[0] == before_incidents, 'invalid inventory facts')
                capacity = self._capacity(db)
                fills = {f.execution_id: f for f in capacity.fills}
                actual = {}
                for position in snap.positions:
                    _require(position.fill_id in fills and position.operation_id == fills[position.fill_id].operation_id,
                             'unknown position')
                    op = operations[position.operation_id]
                    _require(position.leg_id == op[0] and position.order_symbol == leg(op[0]).order_symbol
                             and position.side == leg(op[0]).entry_side.value and type(position.remaining) is int
                             and position.remaining > 0, 'invalid position')
                    actual[position.fill_id] = position.remaining
                expected = {fid: qty for leg_id in snap.scope_legs for fid, qty in
                            self._open_fill_quantities(db, leg_id, subtract_reservations=False).items() if qty}
                _require(actual == expected and dict(snap.protection.positions) == actual, 'position inventory mismatch')
                protection_seen = db.execute('SELECT 1 FROM protection_facts WHERE fact_id=?',
                                             (snap.protection.fact_id,)).fetchone()
                _require(self._apply_protection_snapshot_db(db, snap.protection, now=now), 'protection inventory mismatch')
                if not protection_seen:
                    events.extend(self._reconcile_close_protection_db(db, snap.protection, now=now))
                # A complete inventory must include every admitted working remainder unless terminal.
                working = {r.operation_id: r.remaining for r in snap.working_orders}
                for op in capacity.operations:
                    if op.request.operation_id in plan['operations']:
                        remainder = op.request.quantity - sum(f.quantity for f in capacity.fills if f.operation_id == op.request.operation_id)
                        provider = next((r for r in snap.requests if r.operation_id == op.request.operation_id), None)
                        if op.terminal is None and provider and provider.status == 'applied' and remainder:
                            _require(working.get(op.request.operation_id) == remainder, 'missing working remainder')
                        if op.terminal is not None:
                            _require(op.request.operation_id not in working, 'terminal order still working')
                for request in snap.requests:
                    if request.terminal_fact_id is not None:
                        row = db.execute('SELECT body FROM broker_facts WHERE fact_id=?', (request.terminal_fact_id,)).fetchone()
                        _require(row is not None, 'missing terminal linkage')
                        terminal = json.loads(row[0])
                        _require(terminal['kind'] == 'terminal' and terminal['operation_id'] ==
                                 (request.target_operation_id or request.operation_id), 'wrong terminal linkage')
                body = dict(record_version=1, snapshot=json.loads(raw), root=root, marker=self._takeover_marker_db(db))
                db.execute('INSERT INTO takeover_inventory VALUES (?, ?, ?, ?, ?)',
                           (snap.fact_id, snap.stream_id, snap.sequence, _dump(body), 'qualified'))
                db.execute('INSERT OR REPLACE INTO takeover_streams VALUES (?, ?)',
                           (snap.stream_id, _dump(dict(record_version=1, sequence=snap.sequence, fact_id=snap.fact_id, as_of=snap.as_of.isoformat()))))
                db.execute('RELEASE takeover_inventory_apply')
                savepoint = False
                return tuple(events)
            except (ValueError, TypeError, KeyError, AttributeError) as exc:
                if savepoint:
                    db.execute('ROLLBACK TO takeover_inventory_apply')
                    db.execute('RELEASE takeover_inventory_apply')
                if raw is not None and root is not None:
                    db.execute('INSERT OR IGNORE INTO takeover_inventory VALUES (?, ?, ?, ?, ?)',
                        (snap.fact_id, snap.stream_id, snap.sequence,
                         _dump(dict(record_version=1, snapshot=json.loads(raw), root=root, reason=str(exc))), 'rejected'))
                self._halt_db(db, 'takeover-inventory:' + str(getattr(snap, 'fact_id', uuid4())), 'execution:' + str(exc), now)
                return ()

    def _latest_takeover_inventory_db(self, db, identity, now):
        from .book_account_owner import MAX_FACT_AGE
        row = db.execute('SELECT body,disposition FROM takeover_inventory ORDER BY rowid DESC LIMIT 1').fetchone()
        if row is None:
            return None
        if row[1] != 'qualified':
            return None
        value = json.loads(row[0])
        snap = value['snapshot']
        if (value['root'] != identity or value['marker'] != self._takeover_marker_db(db)
                or not timedelta(0) <= now - datetime.fromisoformat(snap['as_of']) <= min(MAX_FACT_AGE, self.binding['max_evidence_age'])):
            return None
        return snap

    def _takeover_child_db(self, db, root, action, now):
        event = root + (':cancel:' + action.order_id if isinstance(action, Cancel) else ':close:' + action.leg_id)
        state = self._state(db)
        occurrence = ActionOccurrence(self.account, state['account_epoch'],
            self.binding['session'].session_id, 'takeover', event, 0)
        op = 'control:' + occurrence_key(occurrence) if isinstance(action, Cancel) else action.order_id
        body = dict(record_version=1, operation_id=op, occurrence=asdict(occurrence), action=asdict(action),
                    prepared_at=now.isoformat(), generation=self._state(db)['generation'])
        old = db.execute('SELECT body FROM takeover_children WHERE operation_id=?', (op,)).fetchone()
        if old is None:
            db.execute('INSERT INTO takeover_children VALUES (?, ?, ?, ?, ?, ?)',
                       (op, root, occurrence_key(occurrence), 'cancel' if isinstance(action, Cancel) else 'flat',
                        action.order_id if isinstance(action, Cancel) else action.leg_id, _dump(body)))
        return op

    def _advance_takeover_locked(self, *, now):
        from .book_account_owner import _time, opposite
        from .book_schedule import classify_schedule, SchedulePhase
        _time(now)
        if getattr(self, '_input_send_suppressed', False):
            return (), False
        self._check_protection_deadlines_locked(now=now)
        if classify_schedule(self.binding['session'], now) is not SchedulePhase.RISK_ADD:
            return self._advance_schedule_locked(now=now), False
        actions = []
        with self._transaction() as db:
            self._validate_takeover_state_db(db)
            state = self._state(db)
            capacity = self._capacity(db)
            if state['authority'] != 'NORMAL' or state['permission'] != 'RUNNING' or capacity.takeover is None:
                return (), False
            root = capacity.takeover.operation_id
            plan = self._takeover_plan_db(db, root)
            if plan['boot_id'] != state['boot_id'] or plan['generation'] != state['generation']:
                return (), False
            action = self._restore_intent(_dump(plan['action']))
            refusal = None
            if not self.binding['as_of'] <= now < self.binding['valid_until']:
                refusal = 'stale_or_future_account_evidence'
            elif now - self.binding['as_of'] > self.binding['max_evidence_age']:
                refusal = 'stale_account_evidence'
            elif action.bar_time is None or not action.bar_time <= now <= action.bar_time + timedelta(minutes=15, seconds=30):
                refusal = 'stale_or_invalid_takeover_source'
            if refusal:
                result = self._retire_takeover_db(db, action, refusal, now)
                if now >= self.binding['valid_until']:
                    self._halt_db(db, 'takeover-authorization-expired:' + root, 'execution', now)
                return (result,), False
            snap = self._latest_takeover_inventory_db(db, root, now)
            if snap is None:
                return (), False
            if any(r['status'] == 'unknown' for r in snap['requests']):
                self._halt_db(db, 'takeover-unknown:' + root, 'execution', now)
                return (), False
            phase = self._takeover_phase_db(db, root)
            if phase == 'PLAN':
                for op in capacity.operations:
                    if op.request.operation_id in plan['operations'] and op.terminal is None:
                        self._takeover_child_db(db, root, Cancel(op.request.leg_id, op.request.operation_id), now)
                children = tuple(r[0] for r in db.execute("SELECT operation_id FROM takeover_children WHERE takeover_id=? AND kind='cancel' ORDER BY rowid", (root,)))
                self._takeover_event_db(db, root, 'CANCEL', now, inventory_id=snap['fact_id'], children=children)
                phase = 'CANCEL'
            if phase in ('CANCEL', 'CONFIRM_CANCELLATIONS'):
                for child_id, raw in db.execute("SELECT operation_id,body FROM takeover_children WHERE takeover_id=? AND kind='cancel' ORDER BY rowid", (root,)):
                    child = json.loads(raw)
                    target = next(o for o in capacity.operations if o.request.operation_id == child['action']['order_id'])
                    if target.terminal is None and not db.execute('SELECT 1 FROM attempts WHERE operation_id=?', (child_id,)).fetchone():
                        actions.append((Cancel(**child['action']), ActionOccurrence(**child['occurrence'])))
                if phase == 'CANCEL':
                    self._takeover_event_db(db, root, 'CONFIRM_CANCELLATIONS', now)
                targets_done = all(o.terminal is not None for o in capacity.operations if o.request.operation_id in plan['operations'])
                requests_done = all(r['status'] in ('applied', 'rejected') and r['terminal_fact_id']
                                    for r in snap['requests'] if r['operation_id'] in plan['operations'] or r['target_operation_id'])
                if not targets_done or not requests_done or actions:
                    pass
                else:
                    for leg_id in plan['displaced']:
                        fills = self._open_fill_quantities(db, leg_id, subtract_reservations=False)
                        if sum(fills.values()):
                            action = OrderIntent('takeover-flat:' + root + ':' + leg_id, leg_id, 'flat',
                                opposite(leg(leg_id).entry_side),
                                sum(fills.values()), scope_fill_ids=tuple(fid for fid, qty in fills.items() if qty), bar_time=now, reason='aegis_takeover')
                            self._takeover_child_db(db, root, action, now)
                    children = tuple(r[0] for r in db.execute("SELECT operation_id FROM takeover_children WHERE takeover_id=? AND kind='flat' ORDER BY rowid", (root,)))
                    self._takeover_event_db(db, root, 'CLOSE_DISPLACED', now, inventory_id=snap['fact_id'], children=children)
                    phase = 'CLOSE_DISPLACED'
            if phase == 'CLOSE_DISPLACED':
                for child_id, raw in db.execute("SELECT operation_id,body FROM takeover_children WHERE takeover_id=? AND kind='flat' ORDER BY rowid", (root,)):
                    child = json.loads(raw)
                    op = db.execute('SELECT status FROM operations WHERE operation_id=?', (child_id,)).fetchone()
                    if op is None:
                        actions.append((self._restore_intent(_dump(child['action'])), ActionOccurrence(**child['occurrence'])))
                        break
                    gross = sum(p['remaining'] for p in snap['positions'] if p['leg_id'] == child['action']['leg_id'])
                    if op[0] == 'terminal' and gross:
                        self._halt_db(db, 'takeover-residual:' + child_id, 'execution', now)
                        return (), False
                    if op[0] != 'terminal' or gross:
                        break
                else:
                    self._takeover_event_db(db, root, 'CONFIRM_QUIESCENCE', now)
                    phase = 'CONFIRM_QUIESCENCE'
            if phase == 'CONFIRM_QUIESCENCE':
                pending = self._takeover_pending_db(db, plan, snap)
                counts = (sum(p['remaining'] for p in snap['positions']), len(snap['working_orders']),
                          len(snap['protection']['orders']), len(pending))
                if not any(counts):
                    proof = Quiescence(capacity.sequence + 1, tuple(plan['displaced']), *counts)
                    self._append_capacity(db, 'takeover', CompleteTakeover(root, proof), now, event_id='takeover-complete:' + root)
                    self._takeover_event_db(db, root, 'REVALIDATE', now, inventory_id=snap['fact_id'], counts=counts,
                                            pending=pending, read_id=snap['read_id'], marker=self._takeover_marker_db(db))
                    return (), True
        results = []
        for action, occurrence in actions:
            result = self._dispatch_locked(action, occurrence=occurrence, now=now)
            results.append(result)
            if result.transport_state in ('unknown', 'rejected'):
                with self._transaction() as db:
                    self._halt_db(db, 'takeover-child:' + result.operation_id, 'execution', now)
                break
        return tuple(results), False

    def _takeover_pending_db(self, db, plan, snap):
        pending = {r['operation_id'] for r in snap['requests'] if r['status'] in ('pending', 'unknown')}
        pending.update(row[1] for row in self._unresolved_attempt_rows(db)
                       if db.execute('SELECT leg_id FROM operations WHERE operation_id=?', (row[1],)).fetchone()[0] in plan['displaced'])
        pending.update(row['pending_operation'] for row in self._protection_rows(db).values()
                       if row['leg_id'] in plan['displaced'] and row['pending_operation'])
        return tuple(sorted(pending))

    def _revalidate_takeover_db(self, db, operation_id, *, now):
        from c1_signal_daemon.book_protocol import BAR_PERIOD, BAR_SLACK
        from .book_account_owner import _binding_record, MAX_FACT_AGE
        state = self._state(db)
        plan = self._takeover_plan_db(db, operation_id)
        if self._ordinary_unknown_orders_db(db, now=now):
            return 'unknown_order'
        if (not plan or self._takeover_phase_db(db, operation_id) != 'REVALIDATE'
                or plan['boot_id'] != state['boot_id'] or plan['generation'] != state['generation']
                or state['authority'] != 'NORMAL' or state['permission'] != 'RUNNING'):
            return 'risk_add_not_authorized'
        proof = json.loads(db.execute("SELECT body FROM takeover_events WHERE operation_id=? AND kind='REVALIDATE' ORDER BY ordinal DESC LIMIT 1", (operation_id,)).fetchone()[0])
        latest = db.execute('SELECT fact_id,disposition FROM takeover_inventory ORDER BY rowid DESC LIMIT 1').fetchone()
        if latest != (proof['inventory_id'], 'qualified'):
            return 'superseded_takeover_proof'
        row = db.execute('SELECT body FROM takeover_inventory WHERE fact_id=? AND disposition=?',
                         (proof['inventory_id'], 'qualified')).fetchone()
        if row is None:
            return 'missing_takeover_proof'
        evidence = json.loads(row[0])['snapshot']
        if (proof['marker'] != self._takeover_marker_db(db)
                or not timedelta(0) <= now - datetime.fromisoformat(evidence['as_of']) <= min(MAX_FACT_AGE, self.binding['max_evidence_age'])):
            return 'stale_takeover_proof'
        if json.loads(_dump(_binding_record(self.binding))) != plan['admission_binding']:
            return 'takeover_binding_changed'
        action = self._restore_intent(_dump(plan['action']))
        if validate_action(action) or action.bar_time is None or not action.bar_time <= now <= action.bar_time + BAR_PERIOD + BAR_SLACK:
            return 'stale_or_invalid_takeover_source'
        occurrence = ActionOccurrence(**plan['occurrence'])
        if occurrence.producer == 'runtime':
            from c1_signal_daemon.feed import Bar
            row = db.execute('SELECT actions,body,session_id,mode FROM barriers WHERE bar_time=?', (action.bar_time.isoformat(),)).fetchone()
            if row is None or row[0] is None or row[2] != occurrence.session_id or occurrence.event_id != action.bar_time.isoformat():
                return 'missing_takeover_source'
            actor = db.execute('SELECT kind,body FROM runtime_actors WHERE boot_id=?', (state['boot_id'],)).fetchone()
            if actor is None or list(actor) != plan['runtime_actor']:
                return 'invalid_takeover_runtime'
            batch, bars = json.loads(row[0]), json.loads(row[1])
            if (occurrence.ordinal >= len(batch) or batch[occurrence.ordinal].get('occurrence') != plan['occurrence']
                    or batch[occurrence.ordinal].get('type') != 'OrderIntent'
                    or batch[occurrence.ordinal].get('value') != plan['action']
                    or set(bars) != {spec.leg_id for spec in BOOK_LEGS}):
                return 'invalid_takeover_source'
            try:
                for value in bars.values():
                    bar = Bar(**{**value, 'ts': datetime.fromisoformat(value['ts'])})
                    if validate_bar(bar) or bar.ts != action.bar_time:
                        return 'invalid_takeover_source'
            except (ValueError, TypeError, KeyError):
                return 'invalid_takeover_source'
            for boundary, in db.execute('SELECT DISTINCT bar_time FROM partial_bars'):
                if now > datetime.fromisoformat(boundary) + BAR_PERIOD + BAR_SLACK:
                    self._halt_db(db, 'takeover-source-barrier:' + boundary, 'barrier', now)
                    return 'expired_source_barrier'
        capacity = self._capacity(db)
        request, context, binding = self._context(db, action, now)
        own = next(o for o in capacity.operations if o.request.operation_id == operation_id)
        if (own.status != 'active' or own.terminal or any(f.operation_id == operation_id for f in capacity.fills)
                or db.execute('SELECT 1 FROM attempts WHERE operation_id=?', (operation_id,)).fetchone()):
            return 'invalid_retained_reservation'
        context = replace(context, exposures=tuple(replace(e, reserved=e.reserved - plan['quantity'])
            if e.leg_id == action.leg_id else e for e in context.exposures),
            pending_operation_ids=tuple(i for i in context.pending_operation_ids if i != operation_id))
        decision = size_book_request(request, context=context, binding=binding, policy=self.binding['policy'], now=now)
        if decision.halt:
            return decision.halt_reason
        if decision.qty_out != plan['quantity'] or decision.qty_out <= 0:
            return 'takeover_quantity_changed'
        if used_micro(capacity) > ACCOUNT_MICRO_CAP or self._unresolved_attempt_rows(db):
            return 'takeover_account_not_quiescent'
        return None
