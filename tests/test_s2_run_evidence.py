"""The S2 artifact reader accepts only a full-suite record and refuses diagnostic subsets."""
import json

import pytest

from scripts import s2_run_evidence as evidence

JUNIT = '<testsuites><testsuite tests="{tests}" failures="0" errors="0" skipped="0"/></testsuites>'


def artifact(tmp_path, *, metadata, invariants_passed=True, tests=15):
    record_dir = tmp_path / 'record0'
    record_dir.mkdir()
    (record_dir / 'record.json').write_text(json.dumps({
        'status': 'completed', 'exit_code': 0, 'verification_exit_code': 0,
        'source_stable': True, 'capture_complete': True, 'cleanup': {'ok': True},
        'metadata': metadata,
    }))
    (record_dir / 'invariants.json').write_text(json.dumps(
        {'passed': invariants_passed, 'required_nodeids': ['n'] * 15}))
    (record_dir / 'junit.xml').write_text(JUNIT.format(tests=tests))
    return tmp_path


def test_full_suite_record_is_evidence(tmp_path):
    ok, facts = evidence.evaluate(artifact(tmp_path, metadata={'acceptance_scope': evidence.FULL_SCOPE}))
    assert ok and facts['acceptance_scope'] == evidence.FULL_SCOPE and facts['s2_select'] is None


@pytest.mark.parametrize('metadata', [
    # Refused even if every other fact were green (a forged or hand-edited invariants.json).
    {'acceptance_scope': evidence.DIAGNOSTIC_SCOPE, 's2_select': 'deadline'},
    {'acceptance_scope': evidence.FULL_SCOPE, 's2_select': 'deadline'},
    {'acceptance_scope': 'N1_ONLY_TEST_ONLY'},
    {},
])
def test_non_full_scope_is_never_evidence(tmp_path, metadata):
    ok, _facts = evidence.evaluate(artifact(tmp_path, metadata=metadata, tests=1))
    assert not ok


def test_diagnostic_run_exits_three_with_refusal(tmp_path, monkeypatch, capsys):
    dest = artifact(tmp_path, metadata={'acceptance_scope': evidence.DIAGNOSTIC_SCOPE, 's2_select': 'deadline'},
                    invariants_passed=False, tests=1)
    monkeypatch.setattr(evidence, 'run_head', lambda run_id: {'headSha': 'abc123'})
    monkeypatch.setattr(evidence, 'download', lambda run_id, target: None)
    assert evidence.main(['1', '--dest', str(dest)]) == 3
    report = json.loads(capsys.readouterr().out)
    assert not report['ok'] and 'never acceptance evidence' in report['refused']
    assert report['facts']['junit']['tests'] == 1
