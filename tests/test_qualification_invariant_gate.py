"""Real pytest subprocesses must not turn reduced critical coverage green."""
import json
import subprocess

import pytest

from scripts import check_qualification_invariants as checker
from scripts.record_verification import RunRecord


NODE = 'tests/test_gate_case.py::test_critical'


def fixture_run(tmp_path, body):
    repo = tmp_path / 'source'
    repo.mkdir()
    (repo / 'tests').mkdir()
    (repo / '.gitignore').write_text('__pycache__/\n.pytest_cache/\n')
    (repo / 'pyproject.toml').write_text('[tool.pytest.ini_options]\n')
    (repo / 'tests/test_gate_case.py').write_text('import pytest\n' + body + '\ndef test_harmless(): pass\n')
    document = [dict(id=identity, requirement='Fixture obligation', owner='test', producer='pytest',
                     consumer='gate', evidence_kind='report fixture', test_nodeids=[NODE])
                for identity in sorted(checker.INVARIANT_IDS)]
    manifest = repo / 'manifest.json'
    manifest.write_text(json.dumps(document))
    subprocess.run(['git', 'init', '-q', str(repo)], check=True)
    subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True)
    subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Test', '-c',
                    'user.email=test@example.invalid', 'commit', '-qm', 'fixture'], check=True)
    execute = getattr(checker, 'execute_manifest', None)
    assert execute is not None, 'canonical manifest must drive the recorded pytest run'
    with RunRecord(repo, tmp_path / 'evidence', ['gate-fixture']) as record:
        record.begin()
        execute(record, manifest)
        record.data['cleanup'] = {'ok': True, 'failures': []}
    return record, manifest


@pytest.mark.parametrize('body,bucket', [
    ('def test_missing(): pass\n', 'missing'),
    ('def test_critical_renamed(): pass\n', 'missing'),
    ('def test_critical(): pytest.skip("critical Linux prerequisite absent")\n', 'skipped'),
    ('def test_critical(): assert False, "behavior broken"\n', 'failed'),
    ('@pytest.fixture\ndef broken(): raise ValueError("setup failed")\ndef test_critical(broken): pass\n', 'failed'),
])
def test_recorded_gate_rejects_missing_renamed_skipped_failed_and_setup_cases(tmp_path, body, bucket):
    record, manifest = fixture_run(tmp_path, body)
    assert record.data['verification_exit_code'] != 0
    result = json.loads((record.output / 'invariants.json').read_bytes())
    assert not result['passed'] and any(NODE in message for message in result[bucket])


def test_passing_execution_is_bound_to_collection_manifest_and_valid_record(tmp_path):
    record, manifest = fixture_run(tmp_path, 'def test_critical(): pass\n')
    assert record.data['verification_exit_code'] == 0
    verify = getattr(checker, 'validate_record', None)
    assert verify is not None, 'completed recorder evidence must be checked'
    assert verify(record.output / 'record.json', manifest.read_bytes())['passed']
    assert NODE in json.loads((record.output / 'collection.json').read_bytes())['nodeids']
    (record.output / 'collection.json').write_text('{"nodeids": []}')
    assert not verify(record.output / 'record.json', manifest.read_bytes())['passed']


@pytest.mark.parametrize('change', ['status', 'source', 'capture', 'cleanup', 'exit', 'manifest', 'dirty', 'revision'])
def test_record_invalidity_cannot_be_overridden_by_passing_testcases(tmp_path, change):
    record, manifest = fixture_run(tmp_path, 'def test_critical(): pass\n')
    path = record.output / 'record.json'
    doc = json.loads(path.read_bytes())
    raw = manifest.read_bytes()
    if change == 'status': doc['status'] = 'interrupted'
    if change == 'source': doc['source_stable'] = False
    if change == 'capture': doc['capture_complete'] = False
    if change == 'cleanup': doc['cleanup']['ok'] = False
    if change == 'exit': doc['exit_code'] = 1
    if change == 'manifest': raw += b' '
    if change == 'dirty':
        doc['before']['status'] = doc['after']['status'] = ' M tests/test_gate_case.py'
    path.write_text(json.dumps(doc))
    expected = 'not-the-candidate' if change == 'revision' else doc['before']['commit']
    assert not checker.validate_record(path, raw, expected_revision=expected)['passed']
