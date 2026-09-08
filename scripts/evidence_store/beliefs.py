"""Reviewed assessments and transparent, non-numeric belief readouts."""
from .model import EvidenceError, canonical, keys, text
from .retrieval import ancestors, applicability, validate_source


def validate_assessment(event, state):
    """Validate references and structure; semantic judgment remains with reviewer."""
    data = event['data']
    keys(data, {'belief_revision', 'judgment', 'reviewer', 'source_version', 'section',
                'statement', 'evidence', 'supersedes'})
    for field in ('belief_revision', 'reviewer', 'source_version', 'section', 'statement'):
        text(data[field], field)
    target = state['records'].get(data['belief_revision'])
    if target is None or target['data']['kind'] != 'belief':
        raise EvidenceError('assessment must target an existing belief revision')
    if data['judgment'] not in {'supported', 'contested', 'insufficient'}:
        raise EvidenceError('judgment must be supported, contested or insufficient')
    version = state['versions'].get(data['source_version'])
    if version is None or version['availability'] != 'available':
        raise EvidenceError('assessment must cite a captured review source')
    previous = state['latest_assessments'].get(data['belief_revision'])
    if data['supersedes'] != previous:
        raise EvidenceError('replacement must supersede the latest assessment for this belief revision')
    if not isinstance(data['evidence'], list):
        raise EvidenceError('assessment evidence must be a list')
    seen, relationships = set(), set()
    for item in data['evidence']:
        keys(item, {'revision_id', 'relationship', 'rationale', 'resolution'})
        identity = text(item['revision_id'], 'revision_id')
        if identity not in state['records'] or identity == data['belief_revision'] or identity in seen:
            raise EvidenceError('evidence must name unique existing revisions other than the assessed belief')
        seen.add(identity)
        relationship = item['relationship']
        if relationship not in {'supporting', 'challenging', 'scope_limiting'}:
            raise EvidenceError('invalid belief evidence relationship')
        relationships.add(relationship)
        text(item['rationale'], 'rationale')
        if item['resolution'] is not None:
            text(item['resolution'], 'resolution')
            if relationship != 'challenging':
                raise EvidenceError('only challenging evidence can have a resolution')
    if data['judgment'] == 'supported' and 'supporting' not in relationships:
        raise EvidenceError('supported requires supporting evidence')
    if data['judgment'] == 'contested' and 'challenging' not in relationships:
        raise EvidenceError('contested requires challenging evidence')


def view(state, current, known_at, context, source, legacy=False):
    """Current observations annotate the preserved assessment; they never rewrite it."""
    if current is None or current['kind'] != 'belief':
        return None
    history = [event for event in state['assessments'].values()
               if event['data']['belief_revision'] == current['id'] and event['recorded_at'] <= known_at]
    selected = history[-1] if history else None
    evidence, unresolved, groups = [], [], {}
    cutoff = None if legacy else known_at
    nodes = {current['id'], current['source_version']} | ancestors(
        state, current['id'], skip_assessment=current['id'], known_at=cutoff)
    warnings = []
    if applicability(current['conditions'], context)['status'] != 'matching':
        warnings.append('belief_scope_unresolved')
    if selected:
        nodes.add(selected['data']['source_version'])
        for item in selected['data']['evidence']:
            event = state['records'][item['revision_id']]
            record = dict(event['data'], id=event['id'], recorded_at=event['recorded_at'])
            scope = applicability(record['conditions'], context)
            evidence.append(dict(item, record=record, applicability=scope))
            nodes.update({record['id'], record['source_version']} |
                         ancestors(state, record['id'], skip_assessment=current['id'], known_at=cutoff))
            digest = state['versions'][record['source_version']]['sha256']
            groups.setdefault(digest, []).append(record['id'])
            if item['relationship'] == 'challenging' and item['resolution'] is None:
                unresolved.append(record['id'])
        if any(row['applicability']['status'] != 'matching' for row in evidence):
            warnings.append('evidence_scope_unresolved')
    else:
        warnings.append('unassessed')
    sources, superseded = [], []
    for identity in sorted(nodes):
        if identity in state['versions']:
            sources.append(dict(id=identity, verification=source(identity)))
        else:
            latest = state['latest'][state['records'][identity]['data']['record_id']]
            if latest != identity:
                superseded.append(dict(id=identity, replacement=latest))
    if any(item['verification']['current'] != 'unchanged' or
           item['verification']['preserved'] != 'available' for item in sources):
        warnings.append('sources_need_review')
    if superseded:
        warnings.append('revisions_superseded')
    if unresolved:
        warnings.append('unresolved_challenges')
    return dict(belief_revision=current['id'], assessment=selected, history=history,
                judgment=selected['data']['judgment'] if selected else None,
                review_status='unassessed' if not selected else 'needs_review' if warnings else 'no_flags',
                evidence=evidence, sources=sources, superseded=superseded,
                unresolved_challenges=unresolved, warnings=warnings,
                shared_source_groups=[dict(sha256=digest, revision_ids=sorted(identities))
                                      for digest, identities in sorted(groups.items()) if len(identities) > 1])


def validate_view(value, state, current, query, legacy=False):
    """Reconstruct journal-derived fields using the receipt's historical observations."""
    if current is None or current['kind'] != 'belief':
        if value is not None:
            raise EvidenceError('only a selected belief can carry an assessment view')
        return
    if not isinstance(value, dict) or not isinstance(value.get('sources'), list):
        raise EvidenceError('belief view must include source observations')
    observations = {}
    for item in value['sources']:
        keys(item, {'id', 'verification'})
        identity = text(item['id'], 'source observation ID')
        if identity not in state['versions'] or identity in observations:
            raise EvidenceError('invalid belief source observation')
        validate_source(item['verification'], state, identity)
        observations[identity] = item['verification']

    def source(identity):
        if identity not in observations:
            raise EvidenceError('belief view omits required source observation')
        return observations[identity]

    expected = view(state, current, query['known_at'], query['context'], source, legacy=legacy)
    if canonical(expected) != canonical(value):
        raise EvidenceError('belief snapshot differs from reviewed assessment or observations')
