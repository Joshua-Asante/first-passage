"""Read-only joins of reported use, receipt-time provenance and current checks."""
import json
import re

from .model import EvidenceError, replay
from .retrieval import ancestors, assessment_ids


def events_in_order(state):
    """Recover the validated event sequence without rereading the journal."""
    events = [*state['captures'], *state['records'].values(), *state['dependencies'],
              *state['receipts'].values(), *state['uses'].values(), *state['assessments'].values()]
    return sorted(events, key=lambda event: event['seq'])


def provenance(snapshot, historical):
    """Follow receipt-time edges, overriding the root's assessment with its snapshot."""
    current = snapshot['current']
    if current is None:
        return set()
    edges = {identity: {event['data']['source_version']}
             for identity, event in historical['records'].items()}
    for event in historical['dependencies']:
        data = event['data']
        edges[data['consumer']].update((data['dependency'], data['evidence_version']))
    assessments = assessment_ids(historical, snapshot['known_at'])
    if snapshot.get('belief') is not None:
        selected = snapshot['belief']['assessment']
        assessments.pop(current['id'], None)
        if selected:
            assessments[current['id']] = selected['id']
    for target, identity in assessments.items():
        data = historical['assessments'][identity]['data']
        edges[target].add(identity)
        edges[identity] = {data['source_version']} | {item['revision_id'] for item in data['evidence']}
    seen, pending = set(), [current['id']]
    while pending:
        identity = pending.pop()
        if identity not in seen:
            seen.add(identity)
            pending.extend(edges.get(identity, ()))
    return seen


def receipt_rows(state, receipt, events):
    historical = replay(events[:receipt['seq'] - 1])
    return [(row, provenance(row, historical)) for row in receipt['data']['results'] if row['current']]


def node_check(state, identity, source):
    """Describe present bytes/lineage without reinterpreting past judgment."""
    if identity in state['versions']:
        verification = source(identity)
        changed = verification['current'] != 'unchanged' or verification['preserved'] != 'available'
        return dict(id=identity, kind='source_version', status='needs_review' if changed else 'no_flags',
                    verification=verification)
    if identity in state['records']:
        latest = state['latest'][state['records'][identity]['data']['record_id']]
        kind = 'record_revision'
    elif identity in state['assessments']:
        latest = state['latest_assessments'][state['assessments'][identity]['data']['belief_revision']]
        kind = 'assessment'
    else:
        raise EvidenceError('node must be an exact source version, record revision or assessment ID')
    return dict(id=identity, kind=kind, status='needs_review' if latest != identity else 'no_flags',
                replacement=latest if latest != identity else None)


def disposition(use, identity):
    selection = next((item for item in use['data']['selections'] if item['revision_id'] == identity), None)
    return dict(use_id=use['id'], decision_revision=use['data']['decision_revision'],
                disposition=selection['disposition'] if selection else 'unassessed',
                reason=selection['reason'] if selection else None)


def use_impact(state, identity, source):
    """Find selected roots containing the node as observed, even after replacement."""
    check = node_check(state, identity, source)
    events = events_in_order(state)
    matches, applied = [], set()
    for receipt in state['receipts'].values():
        associated = [use for use in state['uses'].values() if use['data']['receipt_id'] == receipt['id']]
        for row, nodes in receipt_rows(state, receipt, events):
            if identity not in nodes:
                continue
            decisions = [disposition(use, row['current']['id']) for use in associated]
            applied.update(item['decision_revision'] for item in decisions if item['disposition'] == 'applied')
            matches.append(dict(receipt_id=receipt['id'], receipt_revision=receipt['data']['revision'],
                                observed_at=receipt['data']['observed_at'], revision_id=row['current']['id'],
                                record_id=row['record_id'], relation='selected' if identity == row['current']['id'] else 'provenance',
                                decisions=decisions, has_recorded_use=bool(associated)))
    return dict(node_id=identity, current_check=check, matches=matches, applied_decisions=sorted(applied),
                coverage='selected receipt results and receipt-time declared provenance; reported use is not causal proof')


def review(state, decision_revision, source):
    """Assemble an exact decision and its use records; preserve receipt observations."""
    decision = state['records'].get(decision_revision)
    if decision is None or decision['data']['kind'] != 'decision':
        raise EvidenceError('review requires an exact decision revision UUID')
    nodes = {decision_revision} | ancestors(state, decision_revision)
    checks = [node_check(state, identity, source) for identity in sorted(nodes)]
    events, uses, cache = events_in_order(state), [], {}
    for use in state['uses'].values():
        if use['data']['decision_revision'] != decision_revision:
            continue
        receipt = state['receipts'][use['data']['receipt_id']]
        if receipt['id'] not in cache:
            cache[receipt['id']] = receipt_rows(state, receipt, events)
        items = []
        for snapshot, nodes in cache[receipt['id']]:
            entry = disposition(use, snapshot['current']['id'])
            entry.update(as_observed=snapshot, provenance_nodes=sorted(nodes),
                         current_checks=[node_check(state, identity, source) for identity in sorted(nodes)])
            items.append(entry)
        uses.append(dict(use=use, receipt=receipt, items=items))
    current_flags = any(check['status'] == 'needs_review' for check in checks) or any(
        check['status'] == 'needs_review' for use in uses for item in use['items']
        if item['disposition'] == 'applied' for check in item['current_checks'])
    return dict(decision_revision=decision_revision, decision=decision, decision_checks=checks, uses=uses,
                review_status='needs_review' if current_flags else 'unassessed' if not uses else 'no_flags',
                warnings=[] if uses else ['no_recorded_use'],
                coverage='recorded use only; receipt observations and current byte/lineage checks are separate')


def markdown(report):
    """Render untrusted source text inside fences, never as active document markup."""
    def block(value):
        body = json.dumps(value, indent=2, ensure_ascii=True)
        length = max((len(run) for run in re.findall(r'`+', body)), default=0)
        fence = '`' * max(3, length + 1)
        return f'{fence}json\n{body}\n{fence}\n'

    parts = ['# Decision review', '',
             f"Review status: {report['review_status']}", '',
             'This report preserves recorded judgment and use. Current checks request review; they do not invalidate a decision.', '',
             '## Recorded decision and current checks', '',
             block({key: value for key, value in report.items() if key != 'uses'})]
    if not report['uses']:
        parts.extend(['## Evidence use', '', 'No recorded use. This is a coverage gap, not evidence that nothing was used.', ''])
    for use in report['uses']:
        parts.extend(['## Receipt and evidence use', '', block(use)])
    return '\n'.join(parts)
