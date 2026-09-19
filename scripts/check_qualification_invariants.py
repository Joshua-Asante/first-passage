"""Account for explicit qualification invariants using actual retained JUnit.

This checks coverage and report integrity, not behavioral adequacy or recorder
validity. The coordinator must separately require a completed, source-stable run,
complete capture, successful cleanup and the appropriate real Linux evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from scripts.record_verification import junit_summary


INVARIANT_IDS = frozenset(f'{family}-01' for family in
    ('QPOL', 'QLEG', 'QART', 'QPLAN', 'QEXEC', 'QKEY', 'QSTATE', 'QISOL', 'QGATE'))
MANIFEST_FIELDS = frozenset({'id', 'requirement', 'owner', 'producer', 'consumer',
                             'test_nodeids', 'evidence_kind'})
NODE_PROPERTIES = frozenset({'nodeid', 'pytest_nodeid', 'qualification_nodeid'})
CHILD_PATH = 'qualification_child_junit'
CHILD_HASH = 'qualification_child_junit_sha256'


def _closed_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON field {key}')
        result[key] = value
    return result


def _nodeid(value):
    if (type(value) is not str or not value or value != value.strip()
            or any(char in value for char in ('\n', '\r', '\0'))):
        raise ValueError('exact test node ID required; wildcard selectors forbidden')
    # Parameters can contain literal glob characters. They are matched exactly,
    # never expanded, just like every other collected node ID.
    address = value.partition('[')[0]
    if any(char in address for char in ('*', '?', '\\')):
        raise ValueError('exact test node ID required; wildcard selectors forbidden')
    path, separator, test = value.partition('::')
    if (not separator or not test or not path.endswith('.py') or path.startswith('/')
            or ':' in path or any(part in ('', '.', '..') for part in path.split('/'))):
        raise ValueError(f'invalid exact test node ID: {value}')
    return value


def _manifest(raw):
    if type(raw) is not bytes:
        raise ValueError('manifest must be immutable UTF-8 bytes')
    document = json.loads(raw.decode('utf-8'), object_pairs_hook=_closed_pairs)
    if type(document) is not list or not document:
        raise ValueError('manifest must be a nonempty closed array')
    identifiers = set()
    required = {}
    for row in document:
        if type(row) is not dict or set(row) != MANIFEST_FIELDS:
            raise ValueError('manifest fields differ from the closed schema')
        for field in MANIFEST_FIELDS - {'test_nodeids'}:
            if type(row[field]) is not str or not row[field].strip():
                raise ValueError(f'manifest {field} must be a nonempty string')
        identity = row['id']
        if identity not in INVARIANT_IDS or identity in identifiers:
            raise ValueError(f'unknown or duplicate invariant ID: {identity}')
        identifiers.add(identity)
        nodes = row['test_nodeids']
        if type(nodes) is not list or not nodes:
            raise ValueError(f'{identity}: nonempty exact test_nodeids required')
        normalized = [_nodeid(node) for node in nodes]
        if len(set(normalized)) != len(normalized):
            raise ValueError(f'{identity}: duplicate test node ID')
        for node in normalized:
            required.setdefault(node, set()).add(identity)
    if identifiers != INVARIANT_IDS:
        raise ValueError('missing invariant IDs: ' + ', '.join(sorted(INVARIANT_IDS - identifiers)))
    return required


def _properties(element):
    properties = {}
    for group in element.findall('properties'):
        for row in group:
            if row.tag != 'property' or not row.get('name') or row.get('value') is None:
                raise ValueError('malformed JUnit property')
            name = row.get('name')
            if name in properties:
                raise ValueError(f'duplicate JUnit property: {name}')
            properties[name] = row.get('value')
    return properties


def _xml_identity(node):
    address, bracket, parameters = node.partition('[')
    path, *names = address.split('::')
    names[-1] += bracket + parameters
    return '.'.join((path[:-3].replace('/', '.'), *names[:-1])), names[-1]


def _matches(classname, expected):
    return classname == expected or bool(classname and expected.endswith('.' + classname))


def _resolve_case(case, collected):
    name, classname = case.get('name'), case.get('classname', '')
    if not name:
        raise ValueError('JUnit testcase lacks a name')
    properties = _properties(case)
    recorded = [properties[key] for key in NODE_PROPERTIES if key in properties]
    if 'nodeid' in case.attrib:
        recorded.append(case.attrib['nodeid'])
    if len(set(recorded)) > 1:
        raise ValueError('contradictory recorded test node IDs')
    parameter_subtest = re.search(r'::subtest-\d+(?:\s|$)', name)
    subtest = parameter_subtest is not None or re.match(r'^subtest-\d+(?:\s|$)', name) is not None
    candidates = []
    for node in collected:
        expected_class, expected_name = _xml_identity(node)
        if parameter_subtest is not None:
            name_matches = name[:parameter_subtest.start()] == expected_name
        elif subtest:
            expected_class += '.' + expected_name
            name_matches = True
        else:
            name_matches = name == expected_name
        if name_matches and _matches(classname, expected_class):
            candidates.append(node)
    if recorded:
        declared = recorded[0]
        # The recorder creates runtime subtest IDs; they are not collected cases.
        if subtest:
            declared = declared.split('::subtest-', 1)[0]
        if declared not in collected:
            raise ValueError(f'recorded test node ID was not collected: {declared}')
        if declared not in candidates:
            # A recorded ID may replace an omitted classname, never contradict one.
            if classname or (not subtest and name != _xml_identity(declared)[1]):
                raise ValueError(f'contradictory JUnit identity for {declared}')
        return declared, subtest
    if len(candidates) > 1:
        raise ValueError(f'ambiguous JUnit identity: {classname}::{name}')
    return (candidates[0] if candidates else None), subtest


def _report_bytes(path, root):
    resolved = path.resolve(strict=True)
    if not resolved.is_relative_to(root):
        raise ValueError(f'report escapes evidence root: {path}')
    if not resolved.is_file():
        raise ValueError(f'report is not a regular file: {path}')
    raw = resolved.read_bytes()
    if b'<!DOCTYPE' in raw.upper() or b'<!ENTITY' in raw.upper():
        raise ValueError('JUnit document declarations are forbidden')
    return resolved, raw


def validate_manifest(manifest_bytes: bytes, *, collected_nodeids: set[str],
                      junit_paths: tuple[Path, ...], evidence_root: Path,
                      required_nodeids: set[str] | None = None) -> dict:
    """Return fail-closed, deduplicated invariant/node diagnostics.

    A passing subtest is never a substitute for its parent's completion. Failed,
    errored or skipped subtests taint the parent. Duplicate reports union adverse
    outcomes; a later pass cannot erase them. Child report pointers are resolved
    relative to their parent report, always checked against their recorded hash,
    and must remain within evidence_root after resolving filesystem links.
    """
    missing, skipped, failed = set(), set(), set()
    try:
        required = _manifest(manifest_bytes)
        if required_nodeids is not None:
            if type(required_nodeids) is not set or not required_nodeids or not required_nodeids <= required.keys():
                raise ValueError('nonempty explicit subset of canonical nodes required')
            required = {node: required[node] for node in required_nodeids}
        if type(collected_nodeids) is not set:
            raise ValueError('collected_nodeids must be an explicit set')
        collected = {_nodeid(node) for node in collected_nodeids}
        root = Path(evidence_root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError('evidence root must be a directory')
    except (ValueError, OSError, UnicodeError, RecursionError) as exc:
        return dict(passed=False, missing=[], skipped=[], failed=[f'manifest: {exc}'])

    def diagnostic(node, bucket, detail):
        for identity in required.get(node, ()):
            bucket.add(f'{identity}: {node}: {detail}')

    observed, outcomes = set(), {}
    visited, active = {}, set()

    def visit(path, expected_hash=None):
        resolved, raw = _report_bytes(path, root)
        actual_hash = hashlib.sha256(raw).hexdigest()
        if expected_hash is not None and actual_hash != expected_hash:
            raise ValueError(f'child report digest differs: {path}')
        if resolved in active:
            raise ValueError(f'cyclic child report reference: {path}')
        if resolved in visited:
            return visited[resolved]
        active.add(resolved)
        xml = ET.fromstring(raw)
        counts = junit_summary(xml)  # Canonical recorder owns xunit count/outcome semantics.
        if len(list(xml.iter('testcase'))) != counts['collected']:
            raise ValueError('JUnit contains an uncounted nested testcase')
        for element in xml.iter():
            if element.tag not in ('testsuites', 'testsuite', 'testcase'):
                continue
            properties = _properties(element)
            links = {CHILD_PATH, CHILD_HASH}.intersection(properties)
            if links:
                if len(links) != 2 or re.fullmatch('[0-9a-f]{64}', properties[CHILD_HASH]) is None:
                    raise ValueError('child report requires path and canonical sha256')
                child = Path(properties[CHILD_PATH])
                if not child.is_absolute():
                    child = resolved.parent / child
                child_counts = visit(child, properties[CHILD_HASH])
                for suffix, count_key in (('tests', 'collected'), ('failure', 'failed'),
                                          ('error', 'errors'), ('skipped', 'skipped')):
                    count = properties.get('qualification_child_' + suffix)
                    if count is not None and (re.fullmatch(r'\d+', count) is None
                                              or int(count) != child_counts[count_key]):
                        raise ValueError(f'child report {suffix} count differs: {child}')
        for case in xml.iter('testcase'):
            node, subtest = _resolve_case(case, collected)
            tags = {tag for tag in ('failure', 'error', 'skipped') if case.find(tag) is not None}
            if node is None:
                if tags.intersection({'failure', 'error'}):
                    failed.add(f'report: unmapped failing case {case.get("classname", "")}::{case.get("name")}')
                continue
            if not subtest:
                observed.add(node)
            outcomes.setdefault(node, set()).update(tags)
        active.remove(resolved)
        visited[resolved] = counts
        return counts

    for path in junit_paths:
        try:
            visit(Path(path))
        except (ValueError, OSError, ET.ParseError, RecursionError) as exc:
            failed.add(f'report: {path}: {exc}')
    for node in required:
        if node not in collected:
            diagnostic(node, missing, 'not collected')
        elif node not in observed:
            diagnostic(node, missing, 'no completed testcase in reports')
        tags = outcomes.get(node, set())
        if 'skipped' in tags:
            diagnostic(node, skipped, 'critical testcase or subtest skipped')
        if tags.intersection({'failure', 'error'}):
            diagnostic(node, failed, 'testcase or subtest failed/errored')
    return dict(passed=not (missing or skipped or failed), missing=sorted(missing),
                skipped=sorted(skipped), failed=sorted(failed),
                **({} if required_nodeids is None else dict(scope='selected_nodes', required_nodeids=sorted(required_nodeids))))
