"""The S2 artifact reader accepts only full-selection scopes and refuses diagnostic subsets."""
import json

import pytest

from scripts import s2_run_evidence as evidence

JUNIT = '<testsuites><testsuite tests="15" failures="0" errors="0" skipped="0"/></testsuites>'


def artifact(tmp_path, scope):
    record_dir = tmp_path / 'record0'
    record_dir.mkdir()
    metadata = {} if scope is None else {'acceptance_scope': scope}
    (record_dir / 'record.json').write_text(json.dumps({
        'status': 'completed', 'exit_code': 0, 'verification_exit_code': 0,
        'source_stable': True, 'capture_complete': True, 'cleanup': {'ok': True},
        'metadata': metadata,
        # The measured commit (G3): a bare artifact read requires it, unbound to a run.
        'before': {'commit': 'ab' * 20},
    }))
    # Every other fact green, as a forged or hand-edited record would be.
    (record_dir / 'invariants.json').write_text(json.dumps({'passed': True, 'required_nodeids': ['n'] * 15}))
    (record_dir / 'junit.xml').write_text(JUNIT)
    return tmp_path


@pytest.mark.parametrize('scope', ['S2_DIAGNOSTIC_SUPERVISION', 'S3_N1_CAPTURE'])
def test_full_selection_scopes_are_evidence(tmp_path, scope):
    # G1: each full-selection scope is evidence only when it is the scope asked for.
    ok, facts = evidence.evaluate(artifact(tmp_path, scope), expect_scope=scope)
    assert ok and facts['acceptance_scope'] == scope


@pytest.mark.parametrize('scope', ['DIAGNOSTIC_SUBSET', 'N1_ONLY_TEST_ONLY', None])
def test_other_scopes_are_never_evidence(tmp_path, scope):
    ok, _facts = evidence.evaluate(artifact(tmp_path, scope))
    assert not ok
