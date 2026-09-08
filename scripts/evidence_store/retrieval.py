"""Deterministic applicability and validation of observed retrieval/use events."""
import json

from .model import EvidenceError, canonical, keys, text, timestamp


def request(context, record_ids, known_at, as_of):
    if not isinstance(context, dict):
        raise EvidenceError('context must be a JSON object')
    try:
        if json.loads(canonical(context)) != context:
            raise EvidenceError('context must use JSON types and string object keys')
    except (TypeError, ValueError) as exc:
        raise EvidenceError('context must contain finite JSON data') from exc
    if record_ids is not None:
        if not isinstance(record_ids, list) or not record_ids:
            raise EvidenceError('record_ids must be a nonempty list or null')
        for item in record_ids:
            text(item, 'record_id')
        if len(set(record_ids)) != len(record_ids):
            raise EvidenceError('duplicate record IDs')
        record_ids = sorted(record_ids)
    if not context and record_ids is None:
        raise EvidenceError('supply nonempty context or explicit record IDs')
    return dict(context=context, record_ids=record_ids,
                known_at=timestamp(known_at), as_of=timestamp(as_of))


def applicability(conditions, context):
    matched, conflicting, unknown = [], [], []
    for key, wanted in sorted((conditions or {}).items()):
        actual = context.get(key)
        supported = (str, bool, int, float)
        if type(wanted) not in supported or type(actual) not in supported:
            unknown.append(key)
        elif ((type(wanted) is not type(actual) and
               not (type(wanted) in (int, float) and type(actual) in (int, float))) or wanted != actual):
            conflicting.append(key)
        else:
            matched.append(key)
    status = 'conflicting' if conflicting else 'unknown' if unknown or not conditions else 'matching'
    return dict(status=status, matching=matched, conflicting=conflicting, unknown=unknown)


def temporal(history, effective):
    eligible = [row for row in history if row['effective_at'] is not None and row['effective_at'] <= effective]
    undated = [row for row in history if row['effective_at'] is None]
    current = eligible[-1] if eligible else None
    if undated and (current is None or history.index(undated[-1]) > history.index(current)):
        current = None
    return current, undated


def candidates(state, query, revision):
    identities = query['record_ids']
    if identities is not None and any(item not in state['latest'] for item in identities):
        raise EvidenceError('unknown explicit record ID')
    results = []
    for identity in identities or sorted(state['latest']):
        history = [dict(event['data'], id=event['id'], recorded_at=event['recorded_at'])
                   for event in state['records'].values()
                   if event['data']['record_id'] == identity and event['recorded_at'] <= query['known_at']]
        current, undated = temporal(history, query['as_of'])
        results.append(dict(record_id=identity, known_at=query['known_at'], as_of=query['as_of'],
                            revision=revision, history=history, current=current, undated=undated,
                            applicability=applicability(current['conditions'] if current else None,
                                                        query['context'])))
    order = {'matching': 0, 'unknown': 1, 'conflicting': 2}
    return sorted(results, key=lambda row: (order[row['applicability']['status']], row['record_id']))


def ancestors(state, revision_id):
    edges = {item: {event['data']['source_version']} for item, event in state['records'].items()}
    for event in state['dependencies']:
        data = event['data']
        edges[data['consumer']].update((data['dependency'], data['evidence_version']))
    seen, pending = set(), [revision_id]
    while pending:
        item = pending.pop()
        if item not in seen:
            seen.add(item)
            pending.extend(edges.get(item, ()))
    return seen - {revision_id}


def validate_source(observation, state, version_id):
    version = state['versions'][version_id]
    keys(observation, set(version) | {'preserved', 'current', 'current_path'})
    if any(observation[key] != value for key, value in version.items()):
        raise EvidenceError('receipt source metadata differs from captured version')
    locator = next(event['data']['path'] for event in reversed(state['captures'])
                   if event['data']['source_id'] == version['source_id'])
    if observation['current_path'] != locator:
        raise EvidenceError('receipt source locator differs from observed journal')
    if observation['current'] not in {'unchanged', 'changed', 'missing', 'unavailable'}:
        raise EvidenceError('invalid current source observation')
    if observation['preserved'] not in {'available', 'missing', 'unavailable', 'corrupt'}:
        raise EvidenceError('invalid preserved source observation')


def validate_receipt(event, state):
    data = event['data']
    keys(data, {'request', 'observed_at', 'revision', 'results'})
    keys(data['request'], {'context', 'record_ids', 'known_at', 'as_of'})
    query = request(**data['request'])
    if query != data['request']:
        raise EvidenceError('receipt request must be normalized')
    if timestamp(data['observed_at']) != data['observed_at'] or data['observed_at'] > event['recorded_at']:
        raise EvidenceError('invalid receipt observation time')
    if query['known_at'] > data['observed_at']:
        raise EvidenceError('known_at cannot exceed observation time')
    if not isinstance(data['revision'], str) or len(data['revision']) != 64:
        raise EvidenceError('invalid receipt journal digest')
    expected = candidates(state, query, data['revision'])
    if not isinstance(data['results'], list) or len(data['results']) != len(expected):
        raise EvidenceError('receipt candidate set differs from journal')
    for row, base in zip(data['results'], expected):
        keys(row, set(base) | {'warnings', 'current_source_verification', 'corrections'})
        if any(canonical(row[key]) != canonical(value) for key, value in base.items()):
            raise EvidenceError('receipt record differs from journal')
        warnings = ['unknown_effective_time'] if base['undated'] else []
        current = row['current']
        if current:
            observation = row['current_source_verification']
            validate_source(observation, state, current['source_version'])
            if observation['current'] != 'unchanged':
                warnings.append('source_needs_review')
            if observation['preserved'] != 'available':
                warnings.append('preserved_source_unavailable')
        elif row['current_source_verification'] is not None:
            raise EvidenceError('unselected record cannot claim source verification')
        allowed = ancestors(state, current['id']) if current else set()
        if not isinstance(row['corrections'], list):
            raise EvidenceError('corrections must be a list')
        seen = set()
        for correction in row['corrections']:
            node = correction['id']
            if node not in allowed or node in seen:
                raise EvidenceError('correction must name a unique declared ancestor')
            seen.add(node)
            if node in state['versions']:
                keys(correction, {'id', 'reason', 'source'})
                validate_source(correction['source'], state, node)
                if correction['reason'] != 'source_needs_review' or (
                        correction['source']['current'] == 'unchanged' and
                        correction['source']['preserved'] == 'available'):
                    raise EvidenceError('invalid source correction finding')
            else:
                keys(correction, {'id', 'reason', 'replacement'})
                latest = state['latest'][state['records'][node]['data']['record_id']]
                if correction['reason'] != 'dependency_superseded' or latest == node or correction['replacement'] != latest:
                    raise EvidenceError('invalid superseded dependency finding')
        superseded = {node for node in allowed if node in state['records'] and
                      state['latest'][state['records'][node]['data']['record_id']] != node}
        if not superseded <= seen:
            raise EvidenceError('receipt omits superseded dependencies')
        if row['corrections']:
            warnings.append('dependencies_need_review')
        if warnings != row['warnings']:
            raise EvidenceError('receipt warnings do not match observations')


def selectable(receipt):
    return {row['current']['id'] for row in receipt['data']['results'] if row['current']}


def validate_use(event, state):
    data = event['data']
    keys(data, {'receipt_id', 'decision_revision', 'selections'})
    receipt = state['receipts'].get(text(data['receipt_id'], 'receipt_id'))
    decision = state['records'].get(text(data['decision_revision'], 'decision_revision'))
    if receipt is None or decision is None or decision['data']['kind'] != 'decision':
        raise EvidenceError('use requires an existing receipt and decision revision')
    if any(item['data']['receipt_id'] == data['receipt_id'] and
           item['data']['decision_revision'] == data['decision_revision'] for item in state['uses'].values()):
        raise EvidenceError('receipt already assessed for this decision revision')
    if not isinstance(data['selections'], list):
        raise EvidenceError('selections must be a list')
    allowed, seen = selectable(receipt), set()
    for item in data['selections']:
        keys(item, {'revision_id', 'disposition', 'reason'})
        identity = text(item['revision_id'], 'revision_id')
        if identity not in allowed or identity in seen:
            raise EvidenceError('selection must name a unique retrieved revision')
        seen.add(identity)
        if item['disposition'] not in {'applied', 'not_applied'}:
            raise EvidenceError('use disposition must be applied or not_applied')
        text(item['reason'], 'reason')
