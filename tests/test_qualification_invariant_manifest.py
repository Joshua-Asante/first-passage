"""Report fixtures test evidence accounting, never protected execution itself."""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from scripts.check_qualification_invariants import validate_manifest


IDS = ('QPOL-01', 'QLEG-01', 'QART-01', 'QPLAN-01', 'QEXEC-01',
       'QKEY-01', 'QSTATE-01', 'QISOL-01', 'QGATE-01')
NODE = 'tests/ops/qualification/test_boundary.py::test_capture[real-linux]'
CLASS = 'tests.ops.qualification.test_boundary'
NAME = 'test_capture[real-linux]'


def manifest(nodes=(NODE,)):
    return [dict(id=identity, requirement='Explicit behavioral obligation', owner='qualification',
                 producer='real producer', consumer='real consumer', test_nodeids=list(nodes),
                 evidence_kind='report fixture') for identity in IDS]


def case(*, name=NAME, classname=CLASS, outcome=None, properties=None, nodeid=None):
    row = ET.Element('testcase', classname=classname, name=name)
    if nodeid is not None:
        row.set('nodeid', nodeid)
    if outcome:
        ET.SubElement(row, outcome)
    if properties:
        props = ET.SubElement(row, 'properties')
        for key, value in properties:
            ET.SubElement(props, 'property', name=key, value=str(value))
    return row


def report(root, name='junit.xml', cases=None):
    cases = [case()] if cases is None else cases
    suite = ET.Element('testsuite', tests=str(len(cases)),
        failures=str(sum(row.find('failure') is not None for row in cases)),
        errors=str(sum(row.find('error') is not None for row in cases)),
        skipped=str(sum(row.find('skipped') is not None for row in cases)))
    suite.extend(cases)
    outer = ET.Element('testsuites')
    outer.append(suite)
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(ET.tostring(outer))
    return path


def check(root, *, document=None, collected=None, reports=None):
    return validate_manifest(json.dumps(manifest() if document is None else document).encode(),
        collected_nodeids={NODE} if collected is None else collected,
        junit_paths=tuple([report(root)] if reports is None else reports), evidence_root=root)


def test_complete_reports_satisfy_every_explicit_invariant(tmp_path):
    assert check(tmp_path) == dict(passed=True, missing=[], skipped=[], failed=[])


@pytest.mark.parametrize('kind', ['uncollected', 'renamed', 'unexecuted'])
def test_collection_or_promising_names_never_replace_execution(tmp_path, kind):
    collected = set() if kind == 'uncollected' else {NODE}
    cases = [] if kind == 'unexecuted' else [case(name='test_capture_renamed')]
    result = check(tmp_path, collected=collected, reports=[report(tmp_path, cases=cases)])
    assert not result['passed']
    assert any('QEXEC-01' in item and NODE in item for item in result['missing'])


@pytest.mark.parametrize('outcome,bucket', [('skipped', 'skipped'), ('failure', 'failed'), ('error', 'failed')])
def test_critical_skip_failure_or_setup_error_cannot_satisfy_manifest(tmp_path, outcome, bucket):
    result = check(tmp_path, reports=[report(tmp_path, cases=[case(outcome=outcome)])])
    assert not result['passed']
    assert any('QISOL-01' in item and NODE in item for item in result[bucket])


def test_ambiguous_classname_never_selects_one_collected_case(tmp_path):
    nodes = {'tests/a/test_boundary.py::test_capture[real-linux]',
             'tests/b/test_boundary.py::test_capture[real-linux]'}
    result = check(tmp_path, document=manifest(tuple(nodes)), collected=nodes,
        reports=[report(tmp_path, cases=[case(classname='test_boundary')])])
    assert not result['passed'] and any('ambiguous' in item for item in result['failed'])


def test_explicit_recorded_nodeid_disambiguates_matching_names(tmp_path):
    other = 'tests/other/test_boundary.py::' + NAME
    row = case(classname='test_boundary', properties=[('nodeid', NODE)])
    assert check(tmp_path, collected={NODE, other}, reports=[report(tmp_path, cases=[row])])['passed']


def test_recorded_nodeid_cannot_override_contradictory_xml_identity(tmp_path):
    row = case(name='test_something_else', nodeid=NODE)
    result = check(tmp_path, reports=[report(tmp_path, cases=[row])])
    assert not result['passed'] and result['failed']


@pytest.mark.parametrize('bad', ['skip', 'failure', 'error'])
def test_duplicate_pass_report_cannot_hide_a_nonpassing_report(tmp_path, bad):
    passing = report(tmp_path)
    failing = report(tmp_path, 'second.xml', [case(outcome='skipped' if bad == 'skip' else bad)])
    result = check(tmp_path, reports=[passing, passing, failing, passing])
    assert not result['passed']
    bucket = result['skipped'] if bad == 'skip' else result['failed']
    assert len(bucket) == len(IDS)


def test_identical_reports_count_once_without_inventing_missing_case(tmp_path):
    first = report(tmp_path)
    second = report(tmp_path, 'duplicate.xml')
    assert check(tmp_path, reports=[first, first, second])['passed']
    missing = 'tests/ops/qualification/test_boundary.py::test_never_executed'
    result = check(tmp_path, document=manifest((NODE, missing)), collected={NODE, missing},
                   reports=[first, second])
    assert not result['passed'] and all(missing in item for item in result['missing'])


def child_parent(root, *, child_outcome=None, digest=None, target=None):
    child = report(root, 'child/junit.xml', [case(outcome=child_outcome)])
    properties = [('qualification_child_junit', str(child if target is None else target)),
                  ('qualification_child_junit_sha256', digest or hashlib.sha256(child.read_bytes()).hexdigest())]
    parent = report(root, 'parent.xml', [case(name='test_bridge', classname='tests.test_bridge', properties=properties)])
    return parent, child


def test_hash_bound_child_report_supplies_actual_execution(tmp_path):
    parent, child = child_parent(tmp_path)
    assert check(tmp_path, reports=[parent, child])['passed']


@pytest.mark.parametrize('outcome', ['skipped', 'failure', 'error'])
def test_child_nonpassing_outcomes_remain_critical(tmp_path, outcome):
    parent, _ = child_parent(tmp_path, child_outcome=outcome)
    result = check(tmp_path, reports=[parent])
    assert not result['passed'] and (result['failed'] or result['skipped'])


def test_child_digest_is_checked_even_when_child_was_already_processed(tmp_path):
    parent, child = child_parent(tmp_path, digest='0' * 64)
    result = check(tmp_path, reports=[child, parent])
    assert not result['passed'] and any('digest' in item for item in result['failed'])


@pytest.mark.parametrize('escape', ['absolute', 'relative', 'symlink'])
def test_child_must_remain_under_evidence_root(tmp_path, escape):
    root = tmp_path / 'evidence'; root.mkdir()
    outside = report(tmp_path, 'outside.xml')
    if escape == 'symlink':
        link = root / 'linked.xml'
        try:
            link.symlink_to(outside)
        except OSError:
            pytest.skip('host cannot create test symlinks')
        target = link
    else:
        target = outside if escape == 'absolute' else '../outside.xml'
    parent, _ = child_parent(root, target=target, digest=hashlib.sha256(outside.read_bytes()).hexdigest())
    result = check(root, reports=[parent])
    assert not result['passed'] and any('evidence root' in item for item in result['failed'])


@pytest.mark.parametrize('kind', ['wrong_count', 'contradictory', 'malformed', 'missing_hash', 'duplicate_property'])
def test_invalid_reports_fail_closed(tmp_path, kind):
    row = case()
    if kind == 'contradictory':
        ET.SubElement(row, 'failure'); ET.SubElement(row, 'skipped')
    if kind == 'missing_hash':
        row = case(properties=[('qualification_child_junit', 'child.xml')])
    if kind == 'duplicate_property':
        row = case(properties=[('nodeid', NODE), ('nodeid', NODE)])
    path = report(tmp_path, cases=[row])
    if kind == 'wrong_count':
        path.write_bytes(path.read_bytes().replace(b'tests="1"', b'tests="9"'))
    if kind == 'malformed':
        path.write_bytes(b'<testsuite>')
    result = check(tmp_path, reports=[path])
    assert not result['passed'] and result['failed']


@pytest.mark.parametrize('outcome', [None, 'failure', 'error', 'skipped'])
def test_recorder_subtest_outcomes_attach_to_collected_parent(tmp_path, outcome):
    sub = case(classname=CLASS + '.' + NAME, name='subtest-1 [matrix] (value=1)', outcome=outcome)
    result = check(tmp_path, reports=[report(tmp_path, cases=[case(), sub])])
    assert result['passed'] is (outcome is None)
    if outcome:
        assert any(NODE in item for item in result['skipped'] + result['failed'])


def test_subtest_success_cannot_stand_in_for_parent_completion(tmp_path):
    sub = case(classname=CLASS + '.' + NAME, name='subtest-1 [matrix]')
    result = check(tmp_path, reports=[report(tmp_path, cases=[sub])])
    assert not result['passed'] and result['missing']


@pytest.mark.parametrize('outcome', ['failure', 'skipped'])
def test_parameterized_recorder_subtest_cannot_hide_behind_passing_parent(tmp_path, outcome):
    # pytest's address mangler keeps everything after the first '[' in name.
    sub = case(name=NAME + '::subtest-1 [matrix] (value=1)', outcome=outcome)
    result = check(tmp_path, reports=[report(tmp_path, cases=[case(), sub])])
    assert not result['passed']
    assert any(NODE in item for item in result['failed'] + result['skipped'])


def test_report_cannot_satisfy_manifest_with_uncounted_nested_testcase(tmp_path):
    path = report(tmp_path, cases=[])
    xml = ET.fromstring(path.read_bytes())
    hidden = ET.SubElement(xml.find('testsuite'), 'unrecognized')
    hidden.append(case())
    path.write_bytes(ET.tostring(xml))
    result = check(tmp_path, reports=[path])
    assert not result['passed'] and result['failed']


def test_child_counts_must_agree_with_hash_bound_report(tmp_path):
    parent, _ = child_parent(tmp_path)
    xml = ET.fromstring(parent.read_bytes())
    ET.SubElement(xml.find('.//properties'), 'property', name='qualification_child_tests', value='2')
    parent.write_bytes(ET.tostring(xml))
    result = check(tmp_path, reports=[parent])
    assert not result['passed'] and any('count' in item for item in result['failed'])


def test_actual_recorder_parameterized_subtest_report_retains_critical_skip(tmp_path):
    import subprocess
    import sys
    source = tmp_path / 'test_real_report.py'
    source.write_text('import pytest\n'
        '@pytest.mark.parametrize("value", [1], ids=["real-case"])\n'
        'def test_matrix(subtests, value):\n'
        '    with subtests.test(msg="real-subtest", value=value):\n'
        '        pytest.skip("required subtest unavailable")\n')
    repository = Path(__file__).resolve().parents[1]
    driver = ('import sys; sys.path.insert(0, sys.argv[1]); import pytest; '
              'raise SystemExit(pytest.main(sys.argv[2:]))')
    completed = subprocess.run([sys.executable, '-c', driver, str(repository),
        'test_real_report.py', '-q', '-o', 'addopts=', '-p', 'scripts.pytest_junit_subtests',
        '--junitxml=actual.xml'], cwd=tmp_path, capture_output=True, text=True, timeout=60)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    node = 'test_real_report.py::test_matrix[real-case]'
    result = check(tmp_path, document=manifest((node,)), collected={node},
                   reports=[tmp_path / 'actual.xml'])
    assert not result['passed']
    assert any('QISOL-01' in item and node in item for item in result['skipped'])


def test_literal_parameter_characters_are_not_wildcard_selectors(tmp_path):
    node = 'tests/ops/qualification/test_boundary.py::test_capture[*?]'
    assert check(tmp_path, document=manifest((node,)), collected={node},
        reports=[report(tmp_path, cases=[case(name='test_capture[*?]')])])['passed']
    result = check(tmp_path, document=manifest((node,)), collected={NODE})
    assert not result['passed'] and result['missing']


@pytest.mark.parametrize('kind', ['omit_invariant', 'unknown_field', 'empty_owner', 'wildcard', 'duplicate_id', 'duplicate_node'])
def test_manifest_cannot_weaken_explicit_inventory(tmp_path, kind):
    doc = manifest()
    if kind == 'omit_invariant': doc.pop()
    if kind == 'unknown_field': doc[0]['optional'] = True
    if kind == 'empty_owner': doc[0]['owner'] = ''
    if kind == 'wildcard': doc[0]['test_nodeids'] = ['tests/test_*.py::*']
    if kind == 'duplicate_id': doc.append(doc[0])
    if kind == 'duplicate_node': doc[0]['test_nodeids'] *= 2
    result = check(tmp_path, document=doc)
    assert not result['passed'] and result['failed']


def test_canonical_manifest_has_all_owned_families():
    from scripts.check_qualification_invariants import _manifest
    path = Path(__file__).parent / 'ops/qualification/invariant_manifest.json'
    required = _manifest(path.read_bytes())
    assert required
    assert any(node.startswith('tests/integration/qualification_boundary/') for node in required)


def test_actual_collection_plugin_records_selected_nodes(tmp_path):
    import subprocess
    import sys
    root = Path(__file__).resolve().parents[1]
    (tmp_path / 'test_selected.py').write_text('def test_present(): pass\n')
    driver = 'import sys; sys.path.insert(0, sys.argv[1]); import pytest; raise SystemExit(pytest.main(sys.argv[2:]))'
    result = subprocess.run([sys.executable, '-c', driver, str(root),
        'test_selected.py', '-q', '-o', 'addopts=', '-p', 'scripts.pytest_qualification_collection',
        '--qualification-collection=collected.json'], cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads((tmp_path / 'collected.json').read_bytes()) == ['test_selected.py::test_present']

def test_explicit_subset_reports_its_scope_and_never_waives_selected_failures(tmp_path):
    other='tests/ops/qualification/test_boundary.py::test_other'
    raw=json.dumps(manifest(nodes=(NODE,other))).encode()
    result=validate_manifest(raw,collected_nodeids={NODE},junit_paths=(report(tmp_path),),
                             evidence_root=tmp_path,required_nodeids={NODE})
    assert result['passed'] and result['scope']=='selected_nodes'
    assert result['required_nodeids']==[NODE]
    assert not validate_manifest(raw,collected_nodeids={NODE},junit_paths=(report(tmp_path),),
                                 evidence_root=tmp_path)['passed']
    for selected in (set(),{'tests/unknown.py::test_invented'}):
        assert not validate_manifest(raw,collected_nodeids={NODE},junit_paths=(report(tmp_path),),
            evidence_root=tmp_path,required_nodeids=selected)['passed']
    assert not validate_manifest(raw,collected_nodeids={NODE},junit_paths=(report(tmp_path,cases=[case(outcome='skipped')]),),
        evidence_root=tmp_path,required_nodeids={NODE})['passed']
