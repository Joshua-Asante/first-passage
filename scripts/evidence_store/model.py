"""Strict, deterministic validation of the durable evidence journal."""
from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import PurePosixPath, PureWindowsPath


class EvidenceError(ValueError):
    """Invalid input or an integrity failure; never silently repaired."""


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise EvidenceError(f'{name} must be a non-empty string')
    return value


def timestamp(value):
    text(value, 'timestamp')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError('timezone required')
        return parsed.astimezone(timezone.utc).isoformat(timespec='microseconds').replace('+00:00', 'Z')
    except ValueError as exc:
        raise EvidenceError(f'invalid timezone-aware timestamp: {value}') from exc


def relative_path(value):
    text(value, 'path')
    path = PurePosixPath(value.replace('\\', '/'))
    if (path.is_absolute() or PureWindowsPath(value).drive or '..' in path.parts
            or any(part.rstrip(' .').casefold() == '.git' or ':' in part for part in path.parts)
            or not path.parts):
        raise EvidenceError('source path must be repository-relative, outside Git internals')
    return path.as_posix()


def verify_excerpt(data, content):
    """Require the quote within one unambiguous Markdown ATX section, outside fences."""
    try:
        lines = content.decode('utf-8').splitlines()
    except UnicodeError as exc:
        raise EvidenceError('record excerpts require a UTF-8 source') from exc
    section = data['section']
    if not re.fullmatch(r'#{1,6} .+', section):
        raise EvidenceError('section must be an exact Markdown ATX heading')
    headings = []
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence) and not line.strip()[len(token):].strip():
                fence = None
            continue
        if fence is None:
            heading = re.match(r'^(#{1,6}) ', line)
            if heading:
                headings.append((index, len(heading.group(1)), line))
    matches = [item for item in headings if item[2] == section]
    if len(matches) != 1:
        raise EvidenceError('section must identify exactly one heading in the preserved source')
    start, level, _ = matches[0]
    end = next((index for index, depth, _ in headings if index > start and depth <= level), len(lines))
    if data['statement'] not in '\n'.join(lines[start:end]):
        raise EvidenceError('statement must occur verbatim inside the cited section')


def keys(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise EvidenceError(f'expected fields: {", ".join(sorted(expected))}')


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)


def source_version(data):
    # Available bytes keep identity across relocations; absent bytes have only a locator identity.
    identity = [data['source_id'], data['sha256']] if data['sha256'] else [
        data['source_id'], data['path'], data['commit'], data['availability']]
    return 'version:' + hashlib.sha256(canonical(identity).encode()).hexdigest()


def replay(events):
    """Validate before any projection is changed; return normalized relational inputs."""
    state = {'versions': {}, 'captures': [], 'records': {}, 'latest': {}, 'dependencies': [],
             'receipts': {}, 'uses': {}, 'assessments': {}, 'latest_assessments': {}}
    ids = set()
    last_time = ''
    for seq, event in enumerate(events, 1):
        keys(event, {'schema', 'seq', 'id', 'recorded_at', 'type', 'data'})
        if not isinstance(event['data'], dict):
            raise EvidenceError('event data must be a JSON object')
        expected_schema = 2 if event['type'] in {'retrieval', 'use'} else 1
        if event['type'] == 'assessment' or (event['type'] == 'record' and event['data'].get('kind') == 'belief'):
            expected_schema = 3
        allowed = {2, 3, 4} if event['type'] == 'retrieval' else {expected_schema}
        if type(event['schema']) is not int or event['schema'] not in allowed:
            raise EvidenceError('unsupported event schema')
        if type(event['seq']) is not int or event['seq'] != seq:
            raise EvidenceError('journal sequence must be contiguous')
        try:
            uuid.UUID(event['id'])
        except (ValueError, TypeError, AttributeError) as exc:
            raise EvidenceError('event id must be a UUID') from exc
        if event['id'] in ids:
            raise EvidenceError('duplicate event id')
        ids.add(event['id'])
        when = timestamp(event['recorded_at'])
        if when != event['recorded_at'] or when < last_time:
            raise EvidenceError('recorded times must be canonical UTC and nondecreasing')
        last_time = when
        data = event['data']
        if event['type'] == 'capture':
            keys(data, {'source_id', 'kind', 'path', 'commit', 'sha256', 'availability', 'version_id'})
            text(data['source_id'], 'source_id')
            text(data['kind'], 'kind')
            if relative_path(data['path']) != data['path']:
                raise EvidenceError('path must use canonical forward slashes')
            if data['commit'] is not None and not re.fullmatch(r'[0-9a-f]{40}', data['commit']):
                raise EvidenceError('commit must be a full lowercase Git SHA-1')
            if data['availability'] not in {'available', 'missing', 'unavailable'}:
                raise EvidenceError('invalid source availability')
            if data['availability'] == 'available':
                if not isinstance(data['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', data['sha256']):
                    raise EvidenceError('available sources require a SHA-256')
            elif data['sha256'] is not None:
                raise EvidenceError('unavailable observations cannot claim captured bytes')
            if data['version_id'] != source_version(data):
                raise EvidenceError('source version identity mismatch')
            existing = state['versions'].get(data['version_id'])
            if existing is not None and existing['kind'] != data['kind']:
                raise EvidenceError('captured source version already exists with a different kind')
            state['versions'].setdefault(data['version_id'], data)
            state['captures'].append(event)
        elif event['type'] == 'record':
            keys(data, {'record_id', 'kind', 'source_version', 'section', 'statement',
                        'status', 'conditions', 'effective_at', 'supersedes'})
            for name in ('record_id', 'source_version', 'section', 'statement', 'status'):
                text(data[name], name)
            if data['kind'] not in {'decision', 'finding', 'analysis', 'belief'}:
                raise EvidenceError('record kind must be decision, finding, analysis or belief')
            version = state['versions'].get(data['source_version'])
            if version is None or version['availability'] != 'available':
                raise EvidenceError('record must cite a captured source version')
            if not isinstance(data['conditions'], dict):
                raise EvidenceError('conditions must be a JSON object')
            try:
                if json.loads(canonical(data['conditions'])) != data['conditions']:
                    raise EvidenceError('conditions must use JSON types and string object keys')
            except (TypeError, ValueError) as exc:
                raise EvidenceError('conditions must contain finite JSON data') from exc
            if data['effective_at'] is not None and timestamp(data['effective_at']) != data['effective_at']:
                raise EvidenceError('effective time must be canonical UTC or null')
            previous = state['latest'].get(data['record_id'])
            if data['supersedes'] != previous:
                raise EvidenceError('replacement must explicitly supersede the latest revision of this record')
            if previous and state['records'][previous]['data']['kind'] != data['kind']:
                raise EvidenceError('a record cannot change kind')
            state['records'][event['id']] = event
            state['latest'][data['record_id']] = event['id']
        elif event['type'] == 'dependency':
            keys(data, {'consumer', 'dependency', 'evidence_version', 'note'})
            for name in data:
                text(data[name], name)
            if data['consumer'] not in state['records']:
                raise EvidenceError('consumer must name an existing record revision')
            if data['dependency'] not in state['records'] and data['dependency'] not in state['versions']:
                raise EvidenceError('dependency must name an existing version or record revision')
            if data['consumer'] == data['dependency']:
                raise EvidenceError('self-dependency is not meaningful')
            version = state['versions'].get(data['evidence_version'])
            if version is None or version['availability'] != 'available':
                raise EvidenceError('dependency declaration must cite captured evidence')
            state['dependencies'].append(event)
        elif event['type'] == 'retrieval':
            from .retrieval import validate_receipt
            validate_receipt(event, state)
            state['receipts'][event['id']] = event
        elif event['type'] == 'use':
            from .retrieval import validate_use
            validate_use(event, state)
            state['uses'][event['id']] = event
        elif event['type'] == 'assessment':
            from .beliefs import validate_assessment
            validate_assessment(event, state)
            state['assessments'][event['id']] = event
            state['latest_assessments'][data['belief_revision']] = event['id']
        else:
            raise EvidenceError(f'unsupported event type: {event["type"]}')
    return state
