"""Explicit offline, atomic legacy conversion. No transport or recovery authority."""
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
from uuid import uuid4

from .book_account_lock import AccountSerializer
from .book_migration_schema import SOURCE_MANIFESTS


@dataclass(frozen=True)
class MigrationResult:
    source_version: int
    target_version: int
    migration_id: str
    disposition: str
    unresolved_ids: tuple[str, ...]


def _dump(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      default=lambda x: {'sqlite_blob_hex': x.hex()} if isinstance(x, bytes) else _unsupported(x))


def _unsupported(value):
    raise TypeError('unsupported retained value: ' + type(value).__name__)


def _digest(value):
    return hashlib.sha256(_dump(value).encode()).hexdigest()


def _require(ok, detail):
    if not ok:
        from .book_account_owner import AccountOwnerError
        raise AccountOwnerError('migration refused: ' + detail)


def validate_layout(db, schema):
    from .book_account_owner import _SETTLEMENT_TABLES
    actual = dict(db.execute("SELECT name,sql FROM sqlite_master WHERE type='table'"))
    _require(set(schema) <= set(actual) <= set(schema) | _SETTLEMENT_TABLES, 'table manifest')
    # Canonical known CREATE statements include every type and constraint.
    norm = lambda s: ''.join(s.lower().split()).replace('"', '').replace('`', '').replace('[', '').replace(']', '')
    for name, columns in schema.items():
        _require(norm(actual[name]) == norm(f'CREATE TABLE {name} ({columns})'), 'schema ' + name)
    _require(db.execute('PRAGMA integrity_check').fetchone() == ('ok',), 'SQLite integrity')


def logical_source(db):
    return {name: dict(sql=sql, columns=[r[1] for r in db.execute(f'PRAGMA table_info({name})')],
                      rows=db.execute(f'SELECT * FROM {name} ORDER BY rowid').fetchall())
            for name, sql in db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name")}


def validate_records(owner, db, version):
    from .book_account_owner import _time
    from .book_policy import leg
    from .book_protection import ActionOccurrence, occurrence_key
    state = owner._state(db)
    capacity = owner._capacity(db)
    sequences = [r[0] for table in ('capacity_events', 'timeline') for r in db.execute(f'SELECT sequence FROM {table}')]
    _require(len(sequences) == len(set(sequences)) and max(sequences, default=0) == state['sequence'], 'account sequence')
    for session, raw, digest in db.execute('SELECT session_id,body,digest FROM runtime_bindings'):
        body = json.loads(raw)
        _require(hashlib.sha256(raw.encode()).hexdigest() == digest and body['session']['session_id'] == session,
                 'runtime binding ' + session)
        for key in ('as_of', 'valid_until'):
            _time(datetime.fromisoformat(body[key]))
    _require(db.execute('SELECT 1 FROM runtime_bindings').fetchone(), 'missing binding')
    operations = {r[0]: r[1:] for r in db.execute('SELECT operation_id,leg_id,kind,quantity,body FROM operations')}
    scoped_occurrences = {}
    legacy_operations = legacy_ids(db, 'operation') if version == 4 else set()
    if version >= 2:
        scoped_occurrences = {key: json.loads(source) for key, source in db.execute('SELECT key,source FROM action_occurrences')}
    for identity, (leg_id, kind, quantity, raw) in operations.items():
        body = json.loads(raw)
        _require(type(quantity) is int and quantity >= 0 and body['leg_id'] == leg_id, 'operation ' + identity)
        _require(kind in ('entry','add','exit','flat','cancel','bracketamend','attach','amend'), 'operation kind ' + identity)
        symbol, generation, at = db.execute('SELECT order_symbol,generation,created_at FROM operations WHERE operation_id=?', (identity,)).fetchone()
        _require(symbol == leg(leg_id).order_symbol and type(generation) is int and generation > 0, 'operation identity ' + identity)
        _time(datetime.fromisoformat(at))
        if kind in ('entry','add','exit','flat'):
            _require(body['order_id'] == identity and body['kind'] == kind, 'operation action ' + identity)
            if version >= 2 and identity not in legacy_operations:
                _require(any(s['type'] == 'OrderIntent' and s['value'] == body for s in scoped_occurrences.values()), 'operation occurrence ' + identity)
    for identity, op, status, raw in db.execute('SELECT attempt_id,operation_id,state,body FROM attempts'):
        command = json.loads(raw)
        _require(op in operations and command['operation_id'] == op and command['attempt_id'] == identity,
                 'attempt ' + identity)
        _require(status in ('ACCEPTED','REJECTED','UNKNOWN'), 'attempt state ' + identity)
        leg_id, kind, quantity, action = operations[op]
        expected_action = json.loads(action)
        if kind in ('entry','add','exit','flat'):
            expected_action['qty'] = quantity
        generation = db.execute('SELECT generation FROM operations WHERE operation_id=?', (op,)).fetchone()[0]
        _require(command['leg_id'] == leg_id and command['kind'] == kind
                 and command['quantity'] == quantity and command['order_symbol'] == leg(leg_id).order_symbol
                 and command['generation'] == generation and command['action'] == expected_action, 'attempt operation ' + identity)
        if version >= 2 and op not in legacy_operations:
            key = occurrence_key(ActionOccurrence(**command['occurrence']))
            _require(key in scoped_occurrences, 'attempt occurrence ' + identity)
    feedback = dict(db.execute('SELECT fact_id,body FROM feedback'))
    for identity, raw, event in db.execute('SELECT fact_id,body,feedback FROM broker_facts'):
        body = json.loads(raw)
        _require(body['fact_id'] == identity and body['operation_id'] in operations, 'broker fact ' + identity)
        _time(datetime.fromisoformat(body['as_of']))
        _require(event is None or feedback.get(identity) == event, 'fact feedback ' + identity)
        if event is not None:
            emitted = json.loads(event)
            _require(emitted['order_id'] == body['operation_id'] and emitted['leg_id'] == operations[body['operation_id']][0]
                     and emitted['bar_time'] == body['as_of'], 'fact event identity ' + identity)
            if body['kind'] == 'fill':
                fill = emitted['fill']
                _require(type(body['quantity']) is int and body['quantity'] > 0
                         and fill['fill_id'] == identity and fill['qty'] == body['quantity']
                         and fill['price'] == body['price'], 'fact event fill ' + identity)
    for identity, raw, delivered, checkpoint, boundary in db.execute('SELECT * FROM feedback'):
        _require(delivered in (0, 1) and isinstance(json.loads(raw), dict), 'feedback ' + identity)
        _time(datetime.fromisoformat(boundary))
        # acknowledge_feedback historically permits a delivered record without adapter state.
        if checkpoint is not None:
            _require(isinstance(json.loads(checkpoint), dict), 'checkpoint ' + identity)
        _require(db.execute("SELECT 1 FROM timeline WHERE kind='feedback' AND ref_id=?", (identity,)).fetchone(),
                 'feedback timeline ' + identity)
    for event in capacity.operations:
        _require(event.request.operation_id in operations, 'capacity operation')
        leg_id, _, quantity, _ = operations[event.request.operation_id]
        _require(event.request.leg_id == leg_id and event.request.order_symbol == leg(leg_id).order_symbol
                 and (event.request.quantity == quantity or event.status == 'refused' and quantity == 0), 'capacity reservation quantity')
    for fill in capacity.fills:
        row = db.execute('SELECT body FROM broker_facts WHERE fact_id=?', (fill.execution_id,)).fetchone()
        _require(row is not None, 'capacity fill')
        body = json.loads(row[0])
        _require(body['kind'] == 'fill' and body['order_kind'] in ('entry','add')
                 and body['operation_id'] == fill.operation_id and body['quantity'] == fill.quantity
                 and type(body['quantity']) is int, 'broker/capacity fill ' + fill.execution_id)
    if version >= 2:
        owner._validate_occurrence_state_db(db)
        owner._validate_protection_state_db(db)
    if version >= 3:
        owner._validate_takeover_state_db(db)
    attachment = owner._settlement_attachment_state(db)
    if attachment != 'NEVER_ATTACHED':
        from .book_settlement import SettlementStore
        settlement = SettlementStore(owner.path, owner.account, state['boot_id'])
        settlement._state(db, check_boot=False)
        settlement._chain(db)
    return capacity


def _resolved_pending(db, old, op):
    """Find the retained qualifying read, even after later evidence updates."""
    from .book_protection import ProtectionSnapshot, ObservedProtection, bracket_from_dict, has_components
    from .book_protection_owner import ProtectionOwnerMixin
    account, epoch = db.execute('SELECT account,account_epoch FROM owner_state').fetchone()
    for fact_id, raw in db.execute("SELECT fact_id,body FROM protection_facts WHERE kind='snapshot'"):
        data = json.loads(raw)
        snapshot = ProtectionSnapshot(**{**data, 'as_of': datetime.fromisoformat(data['as_of']),
            'scope_legs': tuple(data['scope_legs']), 'positions': tuple(map(tuple, data['positions'])),
            'resolved_operations': tuple(map(tuple, data['resolved_operations'])),
            'orders': tuple(ObservedProtection(**{**r, 'broker_order_ids': tuple(r['broker_order_ids']),
                'effective': bracket_from_dict(r['effective'])}) for r in data['orders'])})
        if (not ProtectionOwnerMixin._snapshot_shape(None, snapshot) or snapshot.fact_id != fact_id
                or (snapshot.account, snapshot.account_epoch) != (account, epoch) or not snapshot.complete
                or old['leg_id'] not in snapshot.scope_legs
                or snapshot.as_of <= datetime.fromisoformat(op['prepared_at'])):
            continue
        outcome = dict(snapshot.resolved_operations).get(op['expected_operation_id'])
        row = next((r for r in snapshot.orders if r.owner_id == old['owner_id']), None)
        if row and (row.entry_fill_id, row.leg_id, row.order_symbol) != (old['entry_fill_id'], old['leg_id'], old['order_symbol']):
            continue
        effective = bracket_from_dict(op['effective'])
        if op['status'] == 'applied' and outcome == 'applied':
            if (row is None and not has_components(effective)) or (row is not None
                    and row.operation_id == op['expected_operation_id'] and row.effective == effective
                    and row.quantity == op['quantity'] and row.revision > op['old_revision']):
                return True
        if (op['status'] == 'rejected_intact' and outcome == 'rejected' and row is not None
                and op['primitive'] not in ('attach', 'entry_attach') and op['old'] is not None
                and row.effective == bracket_from_dict(op['old']) and row.revision == op['old_revision']):
            return True
    return False


def migration_record(db):
    rows = db.execute('SELECT migration_id,source_version,source_digest,target_version,body FROM migration_records').fetchall()
    if not rows:
        _require(not db.execute('SELECT 1 FROM legacy_obligations').fetchone(), 'orphan legacy obligation')
        return None
    _require(len(rows) == 1, 'migration cardinality')
    identity, version, digest, target, raw = rows[0]
    body = json.loads(raw)
    _require(version in SOURCE_MANIFESTS and target == 4 and body['record_version'] == 1
             and body['source_revision'] == SOURCE_MANIFESTS[version]['revision']
             and _digest(body['source']) == digest, 'migration provenance')
    original = body['source']['owner_state']['rows'][0]
    _require(original[0] == version and identity == _digest([original[1], original[2], version, digest, 4]), 'migration identity')
    current = db.execute('SELECT account,account_epoch FROM owner_state').fetchone()
    _require(tuple(original[1:3]) == current, 'migration account')
    source = body['source']
    # Conversion is not permission to discard original history. Only columns
    # that ordinary evidence/checkpoint recovery may update can evolve.
    mutable = {
        'operations': {'status'},
        'feedback': {'delivered','checkpoint'}, 'action_occurrences': {'result','state'},
        'close_reservations': {'status'}, 'protection_streams': {'body'}, 'takeover_streams': {'body'},
        'protection_owners': {'body'}, 'protection_operations': {'body'},
    }
    preserved = set(SOURCE_MANIFESTS[version]['schema']) - {'owner_state','settlement_attachment'}
    for table in preserved:
        columns = source[table]['columns']
        key_columns = [r[1] for r in sorted(db.execute(f'PRAGMA table_info({table})'), key=lambda r: r[5]) if r[5]]
        _require(key_columns, 'missing history primary key ' + table)
        key_indices = [columns.index(c) for c in key_columns]
        for original_row in source[table]['rows']:
            row = db.execute(f"SELECT * FROM {table} WHERE " + ' AND '.join(c+'=?' for c in key_columns),
                             tuple(original_row[i] for i in key_indices)).fetchone()
            _require(row is not None, 'missing original ' + table)
            _require(all(row[i] == value for i, value in enumerate(original_row)
                         if columns[i] not in mutable.get(table, set())), 'changed original ' + table)
            if table == 'feedback' and original_row[2]:
                _require(row[2:] == tuple(original_row[2:]), 'lost delivered checkpoint')
            if table in ('protection_owners', 'protection_operations'):
                old, current_body = json.loads(original_row[-1]), json.loads(row[-1])
                keys = ('owner_id','entry_fill_id','leg_id','order_symbol','side','original_qty') if table == 'protection_owners' else tuple(k for k in old if k != 'status')
                _require(all(old[k] == current_body[k] for k in keys), 'changed protection provenance')
                if table == 'protection_owners' and old['consumed']:
                    _require(current_body['consumed'], 'resurrected protection owner')
                    pending = old['pending_operation']
                    # B observations skip consumed owners. An already attempted
                    # amendment therefore remains independently unresolved.
                    if pending and db.execute('SELECT 1 FROM attempts WHERE operation_id=?', (pending,)).fetchone():
                        _require(current_body['pending_operation'] == pending
                                 and current_body['deadline'] == old['deadline'], 'lost consumed pending amendment')
                if table == 'protection_owners' and old['pending_operation']:
                    pending = old['pending_operation']
                    if current_body['pending_operation'] == pending:
                        _require(current_body['deadline'] == old['deadline'], 'changed pending deadline')
                    else:
                        op = json.loads(db.execute('SELECT body FROM protection_operations WHERE operation_id=?', (pending,)).fetchone()[0])
                        unsent_refusal = op['status'] == 'refused' and not db.execute('SELECT 1 FROM attempts WHERE operation_id=?', (pending,)).fetchone()
                        if not unsent_refusal:
                            _require(not old['consumed'] and op['status'] in ('applied', 'rejected_intact')
                                     and _resolved_pending(db, old, op),
                                     'unproven pending resolution')
    required = set()
    if version == 1:
        required.update(('operations', str(row[0]), 'operation') for row in source['operations']['rows'])
        required.update(('broker_facts', json.loads(row[4])['execution_id'], 'fill')
                        for row in source['capacity_events']['rows'] if row[3] == 'fill')
    if version < 3:
        required.update(('operations', str(row[0]), 'takeover') for row in source['operations']['rows']
                        if row[9] == 'takeover_pending')
        required.update(('operations', json.loads(row[4])['operation_id'], 'takeover')
                        for row in source['capacity_events']['rows'] if row[3] == 'takeover')
    actual = set()
    for oid, table, source_id, kind, obligation_raw in db.execute('SELECT * FROM legacy_obligations'):
        obligation = json.loads(obligation_raw)
        _require(obligation['record_version'] == 1 and obligation['migration_id'] == identity
                 and obligation['source_digest'] == digest and obligation['disposition'] == 'unresolved'
                 and oid == _digest([identity, table, source_id, kind]), 'legacy obligation ' + oid)
        _require(table in body['source'] or table == 'post_migration_fill', 'legacy source table')
        if table != 'post_migration_fill':
            _require((table, source_id, kind) in required, 'unsupported legacy exemption')
            actual.add((table, source_id, kind))
            row = next((row for row in source[table]['rows'] if str(row[0]) == source_id), None)
            _require(row is not None and obligation['content'] == row, 'legacy source row')
        else:
            fact = db.execute('SELECT body FROM broker_facts WHERE fact_id=?', (source_id,)).fetchone()
            _require(version == 1 and kind == 'fill' and fact is not None
                     and json.loads(fact[0]) == obligation['content'], 'late legacy fill')
    _require(actual == required, 'missing legacy obligation')
    return rows[0], body


def legacy_ids(db, kind):
    record = migration_record(db)
    if record is None:
        return set()
    version = record[0][1]
    _require(kind != 'fill' or version == 1 or not db.execute("SELECT 1 FROM legacy_obligations WHERE kind='fill'").fetchone(), 'unexpected legacy fill')
    return {row[0] for row in db.execute('SELECT source_id FROM legacy_obligations WHERE kind=?', (kind,))}


def add_obligation(db, migration_id, digest, table, source_id, kind, content):
    identity = _digest([migration_id, table, source_id, kind])
    db.execute('INSERT INTO legacy_obligations VALUES (?, ?, ?, ?, ?)', (identity, table, source_id, kind,
        _dump(dict(record_version=1, migration_id=migration_id, source_digest=digest, disposition='unresolved', content=content))))
    return identity


def quarantine_late_fill(db, fact):
    record = migration_record(db)
    if record is None or record[0][1] != 1:
        return False
    source = record[1]['source']
    if not any(row[0] == fact.operation_id for row in source['operations']['rows']):
        return False
    from dataclasses import asdict
    from .book_account_owner import _body
    add_obligation(db, record[0][0], record[0][2], 'post_migration_fill', fact.fact_id, 'fill', json.loads(_body(asdict(fact))))
    return True


def migrate_book_owner(path: Path, account: str, *, now: datetime, crash_at=None) -> MigrationResult:
    from .book_account_owner import BookAccountOwner, AccountOwnerError, _SCHEMA, _time
    _time(now)
    path = Path(path)
    serializer = AccountSerializer(path.with_suffix(path.suffix + '.lock'))
    owner = object.__new__(BookAccountOwner)
    owner.path, owner.account, owner._actor_boot_id = path, account, None
    try:
        with serializer.acquire(), closing(sqlite3.connect(path.resolve().as_uri() + '?mode=rw', uri=True, isolation_level=None)) as db:
            db.execute('PRAGMA synchronous=FULL')
            db.execute('BEGIN IMMEDIATE')
            version_rows = db.execute('SELECT schema FROM owner_state').fetchall()
            _require(len(version_rows) == 1 and type(version_rows[0][0]) is int, 'version')
            version = version_rows[0][0]
            owner._read_schema_version = version
            if version == 4:
                validate_layout(db, _SCHEMA)
                owner._bootstrap_db(db)
                validate_records(owner, db, 4)
                retained = migration_record(db)
                _require(retained is not None, 'not a converted account')
                row, _ = retained
                result = MigrationResult(row[1], 4, row[0], 'already_converted', tuple(r[0] for r in db.execute('SELECT obligation_id FROM legacy_obligations ORDER BY obligation_id')))
                db.rollback()
                return result
            _require(version in SOURCE_MANIFESTS, 'unsupported version')
            validate_layout(db, SOURCE_MANIFESTS[version]['schema'])
            capacity = validate_records(owner, db, version)
            source = logical_source(db)
            digest = _digest(source)
            state = owner._state(db)
            migration_id = _digest([account, state['account_epoch'], version, digest, 4])
            for name, fields in _SCHEMA.items():
                if name not in SOURCE_MANIFESTS[version]['schema']:
                    db.execute(f'CREATE TABLE {name} ({fields})')
                    if crash_at == 'ddl:' + name:
                        raise AccountOwnerError('simulated migration interruption')
            db.execute('INSERT INTO migration_records VALUES (?, ?, ?, 4, ?)', (migration_id, version, digest,
                _dump(dict(record_version=1, source_revision=SOURCE_MANIFESTS[version]['revision'], source=source, at=now.isoformat()))))
            if version == 1:
                for fill in capacity.fills:
                    row = next(r for r in source['broker_facts']['rows'] if r[0] == fill.execution_id)
                    add_obligation(db, migration_id, digest, 'broker_facts', fill.execution_id, 'fill', row)
                for row in source['operations']['rows']:
                    add_obligation(db, migration_id, digest, 'operations', row[0], 'operation', row)
            if version < 3:
                roots = {o.request.operation_id for o in capacity.operations if o.status == 'takeover'}
                roots.update(c.operation_id for c in capacity.completed_takeovers)
                for identity in roots:
                    row = next(r for r in source['operations']['rows'] if r[0] == identity)
                    add_obligation(db, migration_id, digest, 'operations', identity, 'takeover', row)
            retained_binding = db.execute('SELECT session_id,body,digest FROM runtime_bindings ORDER BY sequence DESC LIMIT 1').fetchone()
            db.execute("UPDATE owner_state SET schema=4, boot_id=?, generation=generation+1, permission='HALTED', authority='INTERVENTION'", (str(uuid4()),))
            owner._read_schema_version = 4
            current = owner._state(db)
            bootstrap = dict(record_version=1, origin='migrated', account=account, account_epoch=current['account_epoch'],
                boot_id=current['boot_id'], generation=current['generation'], session_id=retained_binding[0],
                binding_digest=retained_binding[2], state='ineligible', activation=None, invalidation='migration')
            db.execute('INSERT INTO bootstrap_identity VALUES (1, ?)', (_dump(bootstrap),))
            if crash_at == 'before_validation':
                raise AccountOwnerError('simulated migration interruption')
            validate_layout(db, _SCHEMA)
            owner._bootstrap_db(db)
            validate_records(owner, db, 4)
            migration_record(db)
            result = MigrationResult(version, 4, migration_id, 'converted', tuple(r[0] for r in db.execute('SELECT obligation_id FROM legacy_obligations ORDER BY obligation_id')))
            if crash_at == 'before_commit':
                raise AccountOwnerError('simulated migration interruption')
            db.commit()
            if crash_at == 'after_commit':
                raise AccountOwnerError('simulated migration interruption')
            return result
    except (sqlite3.Error, ValueError, TypeError, KeyError, IndexError, OSError) as exc:
        raise AccountOwnerError('migration source unavailable or invalid') from exc
