"""Schema 3 recovery graph; structural facts do not confer broker authority."""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json

from book_halt import HaltStoreError, _text, validate_schema


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def positive(value, *, zero=False):
    if type(value) is not int or value < (0 if zero else 1):
        raise HaltStoreError('invalid recovery quantity/sequence')


def timestamp(value):
    _text(value)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise HaltStoreError('invalid recovery timestamp') from exc
    if parsed.utcoffset() is None:
        raise HaltStoreError('recovery timestamp must have timezone')
    return parsed


@dataclass(frozen=True)
class RecoveryDemand:
    operation_id: str
    incident_id: str
    kind: str
    symbol: str
    scope_ids: tuple
    order_ids: tuple
    quantity: int | None = None
    transition: str = 'explicit_scope'


@dataclass(frozen=True)
class RecoveryEvidence:
    account: str
    route: str
    version: str
    domain: str
    acquisition_id: str
    timestamp: str
    sequence: int
    orders: tuple
    allocations: tuple
    protection: tuple
    observed_symbols: tuple
    bindings: tuple


def _unique(rows, key):
    identities = [_text(row[key]) for row in rows]
    if len(identities) != len(set(identities)):
        raise HaltStoreError('duplicate recovery identity: ' + key)


def validate_inputs(demand, evidence):
    """Reject malformed structure; never assert E1–E3 completeness or credit."""
    try:
        for key in ('operation_id', 'incident_id', 'symbol'):
            _text(demand[key])
        for key in ('account', 'route', 'version', 'domain', 'acquisition_id'):
            _text(evidence[key])
        timestamp(evidence['timestamp'])
        positive(evidence['sequence'])
        if demand['kind'] not in ('CANCEL', 'CLOSE') or demand['transition'] != 'explicit_scope':
            raise HaltStoreError('unsupported recovery transition')
        if demand['quantity'] is not None:
            positive(demand['quantity'])
        for values in (demand['scope_ids'], demand['order_ids'], evidence['observed_symbols']):
            if not isinstance(values, (tuple, list)) or len(values) != len(set(values)):
                raise HaltStoreError('invalid recovery identity sequence')
            for value in values:
                _text(value)
        if not demand['scope_ids'] or demand['symbol'] not in evidence['observed_symbols']:
            raise HaltStoreError('missing recovery scope/location')
        bound = set()
        for binding in evidence['bindings']:
            _text(binding['product'])
            _text(binding['symbol'])
            hashed = binding['evidence_digest']
            if not isinstance(hashed, str) or len(hashed) != 64 or any(c not in '0123456789abcdef' for c in hashed):
                raise HaltStoreError('missing dated-symbol binding evidence')
            pair = (binding['product'], binding['symbol'])
            if pair in bound:
                raise HaltStoreError('duplicate symbol binding')
            bound.add(pair)
        for scope in demand['scope_ids']:
            if scope.startswith('product:'):
                if (scope[8:], demand['symbol']) not in bound:
                    raise HaltStoreError('product/datestamped symbol binding mismatch')
            elif scope != 'location:' + demand['symbol']:
                raise HaltStoreError('invalid demand scope')
        for key in ('orders', 'allocations', 'protection'):
            if not isinstance(evidence[key], (list, tuple)):
                raise HaltStoreError('invalid evidence collection')
        _unique(evidence['orders'], 'order_id')
        _unique(evidence['allocations'], 'execution_id')
        _unique(evidence['protection'], 'owner_id')
        orders = {r['order_id']: r for r in evidence['orders']}
        for row in orders.values():
            for key in ('order_id', 'request_id', 'symbol'):
                _text(row[key])
            if row['symbol'] not in evidence['observed_symbols']:
                raise HaltStoreError('missing observed order location')
            if row['side'] not in ('buy', 'sell') or row['kind'] not in ('risk_add', 'protection'):
                raise HaltStoreError('invalid original order facts')
            positive(row['quantity'])
            positive(row['remaining'], zero=True)
            if row['remaining'] > row['quantity']:
                raise HaltStoreError('order remainder exceeds original quantity')
            authority = row['authority_digest']
            if authority is not None and (not isinstance(authority, str) or len(authority) != 64
                                          or any(c not in '0123456789abcdef' for c in authority)):
                raise HaltStoreError('invalid original order authority digest')
        allocations = {r['execution_id']: r for r in evidence['allocations']}
        totals = {}
        for row in allocations.values():
            _text(row['lot_id'])
            positive(row['quantity'])
            positive(row['sequence'])
            if row['order_id'] not in orders:
                raise HaltStoreError('allocation without original order')
            totals[row['order_id']] = totals.get(row['order_id'], 0) + row['quantity']
        for order_id, quantity in totals.items():
            if quantity + orders[order_id]['remaining'] > orders[order_id]['quantity']:
                raise HaltStoreError('allocations exceed original order quantity')
        refs = []
        for row in evidence['protection']:
            if row['origin_execution_id'] not in allocations:
                raise HaltStoreError('protection without originating execution')
            positive(row['quantity'])
            if not isinstance(row['components'], (list, tuple)) or not row['components']:
                raise HaltStoreError('invalid protection components')
            origin_side = orders[allocations[row['origin_execution_id']]['order_id']]['side']
            kinds, links = set(), set()
            for component in row['components']:
                refs.append(_text(component['order_ref']))
                _text(component['linkage'])
                positive(component['quantity'])
                if (component['side'] != ('sell' if origin_side == 'buy' else 'buy') or
                        component['kind'] not in ('stop', 'limit', 'trail') or
                        component['quantity'] != row['quantity'] or
                        not isinstance(component['parameters'], dict) or not component['parameters']):
                    raise HaltStoreError('incomplete protection component')
                if component['kind'] in kinds:
                    raise HaltStoreError('duplicate protection kind')
                kinds.add(component['kind'])
                links.add(component['linkage'])
                parameters = component['parameters']
                required = ({'activation_ticks', 'offset_ticks', 'anchor'} if component['kind'] == 'trail'
                            else {'price'})
                if not required <= set(parameters) or not set(parameters) <= required | {'anchor'}:
                    raise HaltStoreError('incomplete protection parameters')
                for value in parameters.values():
                    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
                        raise HaltStoreError('invalid protection parameter')
                    number = Decimal(str(value))
                    if not number.is_finite() or number <= 0:
                        raise HaltStoreError('invalid protection parameter')
            if len(links) != 1:
                raise HaltStoreError('inconsistent bracket linkage')
        if len(refs) != len(set(refs)):
            raise HaltStoreError('duplicate protection component')
        for order_id in demand['order_ids']:
            if order_id not in orders or orders[order_id]['symbol'] != demand['symbol']:
                raise HaltStoreError('demand original order mismatch')
        expected = {r['order_id'] for r in orders.values() if r['symbol'] == demand['symbol']}
        if demand['kind'] == 'CLOSE' and set(demand['order_ids']) != expected:
            raise HaltStoreError('incomplete full-symbol order ownership')
        if demand['kind'] == 'CANCEL' and len(demand['order_ids']) != 1:
            raise HaltStoreError('cancel requires exact original order')
        canonical(evidence)
    except (KeyError, TypeError, ValueError, InvalidOperation) as exc:
        raise HaltStoreError('malformed recovery demand/evidence') from exc


def graph(demand, evidence):
    """Deterministic immutable child graph, checked on each read."""
    orders = [r for r in evidence['orders'] if r['order_id'] in demand['order_ids']]
    allocations = [r for r in evidence['allocations'] if r['order_id'] in demand['order_ids']]
    executions = {r['execution_id'] for r in allocations}
    protection = [r for r in evidence['protection'] if r['origin_execution_id'] in executions]
    return {
        'operation_scopes': [(s, {'scope_id': s}) for s in demand['scope_ids']],
        'operation_orders': [(r['order_id'], r) for r in orders],
        'operation_allocations': [(r['execution_id'], r) for r in allocations],
        'operation_protection': [(r['owner_id'], r) for r in protection],
        'recovery_effects': [('effect:' + demand['operation_id'],
                             {'demand': demand, 'orders': orders, 'allocations': allocations,
                              'protection': protection, 'route': evidence['route'],
                              'version': evidence['version'], 'account': evidence['account']})],
    }


def unknown_owners(evidence):
    """Observed external identities only; not a covering E3 request fence."""
    context = {k: evidence[k] for k in ('account', 'route', 'version', 'domain')}
    for order in evidence['orders']:
        if order['authority_digest'] is not None:
            continue
        identity = {**context, 'order_id': order['order_id']}
        yield ('unknown_order', digest(identity),
               {**context, **{k: order[k] for k in ('order_id', 'request_id', 'symbol', 'side', 'kind', 'quantity')}})
        request = {**context, 'request_id': order['request_id']}
        yield 'unknown_request', digest(request), request


SCHEMA = {
    'recovery_operations': 'operation_id TEXT PRIMARY KEY NOT NULL, body TEXT NOT NULL, digest TEXT NOT NULL, attempt_id TEXT',
    'recovery_obligations': 'reason TEXT NOT NULL, owner TEXT NOT NULL, body TEXT NOT NULL, PRIMARY KEY(reason, owner)',
    'recovery_attempts': 'attempt_id TEXT PRIMARY KEY NOT NULL, operation_id TEXT NOT NULL UNIQUE REFERENCES recovery_operations(operation_id), request_id TEXT NOT NULL UNIQUE, body TEXT NOT NULL, observation TEXT',
    'recovery_events': 'sequence INTEGER PRIMARY KEY, kind TEXT NOT NULL, owner TEXT NOT NULL, digest TEXT NOT NULL',
    'recovery_meta': 'event_count INTEGER NOT NULL CHECK(event_count >= 0)',
}
for _name in ('operation_scopes', 'operation_orders', 'operation_allocations',
              'operation_protection', 'recovery_effects'):
    SCHEMA[_name] = ('operation_id TEXT NOT NULL REFERENCES recovery_operations(operation_id), '
                     'identity TEXT NOT NULL, body TEXT NOT NULL, PRIMARY KEY(operation_id, identity)')


def migrate(db):
    for name, body in SCHEMA.items():
        db.execute(f'CREATE TABLE {name} ({body})')
    db.execute('INSERT INTO recovery_meta VALUES (0)')
    db.execute('UPDATE state SET version=3')


def validate(db):
    validate_schema(db, SCHEMA)
    if db.execute('PRAGMA foreign_key_check').fetchall():
        raise HaltStoreError('broken recovery foreign key')
    meta = db.execute('SELECT event_count FROM recovery_meta').fetchall()
    events = db.execute('SELECT sequence, kind, owner, digest FROM recovery_events ORDER BY sequence').fetchall()
    if len(meta) != 1 or meta[0][0] != len(events) or [e[0] for e in events] != list(range(1, len(events) + 1)):
        raise HaltStoreError('incomplete recovery event journal')
    operations = []
    attempts = []
    account, generation = db.execute('SELECT account, generation FROM state').fetchone()
    incidents = dict(db.execute('SELECT incident_id, generation FROM incidents'))
    scopes = {row[0] for row in db.execute('SELECT scope_id FROM recovery_scopes')}
    for operation_id, raw, hashed, attempt_id in db.execute('SELECT * FROM recovery_operations ORDER BY rowid'):
        body = json.loads(raw)
        demand, evidence = body['demand'], body['evidence']
        validate_inputs(demand, evidence)
        positive(body['generation'])
        positive(body['prepared']['sequence'])
        timestamp(body['prepared']['timestamp'])
        _text(body['prepared']['domain'])
        if (evidence['account'] != account or demand['incident_id'] not in incidents or
                not set(demand['scope_ids']) <= scopes or
                'boot:' + body['boot_id'] not in incidents or
                not incidents['boot:' + body['boot_id']] <= body['generation'] <= generation or
                incidents[demand['incident_id']] > body['generation'] or
                body['provenance'] not in ('SYNTHETIC', 'UNQUALIFIED')):
            raise HaltStoreError('invalid recovery preparation binding')
        if digest(body) != hashed or demand['operation_id'] != operation_id:
            raise HaltStoreError('changed recovery operation')
        if not any(e[1:] == ('prepared', operation_id, hashed) for e in events):
            raise HaltStoreError('missing preparation event')
        children = graph(demand, evidence)
        for table, expected in children.items():
            actual = db.execute(f'SELECT identity, body FROM {table} WHERE operation_id=?', (operation_id,)).fetchall()
            if sorted(actual) != sorted((key, canonical(value)) for key, value in expected):
                raise HaltStoreError('incomplete or changed recovery graph: ' + table)
        rows = db.execute('SELECT attempt_id, request_id, body, observation FROM recovery_attempts WHERE operation_id=?', (operation_id,)).fetchall()
        if (attempt_id is None and rows) or (attempt_id is not None and (len(rows) != 1 or rows[0][0] != attempt_id)):
            raise HaltStoreError('incomplete recovery attempt ownership')
        for identity, request_id, attempt_raw, observation in rows:
            attempt = json.loads(attempt_raw)
            command = {**children['recovery_effects'][0][1], 'request_id': request_id}
            boundary = attempt['boundary']
            positive(boundary['sequence'])
            if (attempt['account'] != account or attempt['route'] != evidence['route'] or
                    attempt['version'] != evidence['version'] or
                    attempt['boot_id'] != body['boot_id'] or attempt['generation'] != body['generation'] or
                    attempt['command_digest'] != digest(command) or
                    boundary['domain'] != evidence['domain'] or
                    boundary['sequence'] <= body['prepared']['sequence'] or
                    timestamp(boundary['timestamp']) <= timestamp(body['prepared']['timestamp'])):
                raise HaltStoreError('invalid recovery attempt binding')
            if (attempt['attempt_id'] != identity or attempt['request_id'] != request_id
                    or attempt['operation_id'] != operation_id or attempt['state'] != 'UNKNOWN'
                    or not any(e[1:] == ('attempt', identity, digest(attempt)) for e in events)):
                raise HaltStoreError('invalid recovery attempt')
            observed = None if observation is None else json.loads(observation)
            if observed is not None and not any(e[1:] == ('observation', identity, digest(observed)) for e in events):
                raise HaltStoreError('changed recovery observation')
            attempts.append({**attempt, 'observation': observed})
        operations.append({**body, 'operation_id': operation_id,
                           'orders': [v for _, v in children['operation_orders']],
                           'allocations': [v for _, v in children['operation_allocations']],
                           'protection': [v for _, v in children['operation_protection']],
                           'status': 'unresolved' if attempt_id else 'prepared'})
    obligations = [dict(reason=r, owner=o, facts=json.loads(b)) for r, o, b in db.execute(
        'SELECT reason, owner, body FROM recovery_obligations ORDER BY reason, owner')]
    by_identity = {(o['reason'], o['owner']): o['facts'] for o in obligations}
    for operation in operations:
        for reason, owner, facts in unknown_owners(operation['evidence']):
            if by_identity.get((reason, owner)) != facts:
                raise HaltStoreError('missing independent unknown order/request owner')
    for obligation in obligations:
        if not any(e[1:] == ('obligation', obligation['reason'] + ':' + obligation['owner'],
                            digest(obligation['facts'])) for e in events):
            raise HaltStoreError('changed recovery obligation')
    # Every retained event still has its owned row; deleting the final child is detected.
    owned = {('prepared', o['operation_id']) for o in operations}
    owned |= {('attempt', a['attempt_id']) for a in attempts}
    owned |= {('observation', a['attempt_id']) for a in attempts if a['observation'] is not None}
    owned |= {('obligation', o['reason'] + ':' + o['owner']) for o in obligations}
    if any((kind, owner) not in owned for _, kind, owner, _ in events):
        raise HaltStoreError('missing recovery event owner')
    for operation in operations:
        if operation['status'] == 'prepared' and (any(o['owner'] == operation['operation_id'] for o in obligations)
                or any(r['authority_digest'] is None for r in operation['orders'])):
            operation['status'] = 'blocked'
    return {'operations': operations, 'attempts': attempts, 'obligations': obligations}
