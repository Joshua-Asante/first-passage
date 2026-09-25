"""The S2 artifact reader accepts only full-selection scopes, each bound to its file set."""
import json

import pytest

from scripts import s2_run_evidence as evidence
from scripts.qualification_boundary_verification import S2_CASES, S3_CASES, S4_CASES

# The selection's own tuples: the reader must not own a second copy of them.
SCOPE_FILES = {'S4_JOINT_N2': S4_CASES, 'S3_N1_CAPTURE': S3_CASES,
               'S2_DIAGNOSTIC_SUPERVISION': S2_CASES}


def nodes(files, per_file=5):
    """Required nodeids spread over `files`, every file contributing at least one."""
    return [f'{file}::test_case_{index}' for file in files for index in range(per_file)]


def artifact(tmp_path, scope, required):
    record_dir = tmp_path / 'record0'
    record_dir.mkdir(exist_ok=True)
    metadata = {} if scope is None else {'acceptance_scope': scope}
    (record_dir / 'record.json').write_text(json.dumps({
        'status': 'completed', 'exit_code': 0, 'verification_exit_code': 0,
        'source_stable': True, 'capture_complete': True, 'cleanup': {'ok': True},
        'metadata': metadata,
        # The measured commit (G3): a bare artifact read requires it, unbound to a run.
        'before': {'commit': 'ab' * 20},
    }))
    # Every other fact green, as a forged or hand-edited record would be.
    (record_dir / 'invariants.json').write_text(json.dumps({'passed': True, 'required_nodeids': required}))
    total = len(required) or 1
    (record_dir / 'junit.xml').write_text(
        f'<testsuites><testsuite tests="{total}" failures="0" errors="0" skipped="0"/></testsuites>')
    return tmp_path


def test_the_default_expected_scope_is_the_s4_joint_set():
    # The workflow's default mode is s4, so a plain read asks for S4_JOINT_N2.
    assert evidence.ACCEPTANCE_SCOPES == ('S4_JOINT_N2', 'S3_N1_CAPTURE',
                                          'S2_DIAGNOSTIC_SUPERVISION')
    assert evidence.DEFAULT_SCOPE == 'S4_JOINT_N2'


def test_each_scope_is_bound_to_the_selectors_own_file_set():
    # The reader reads the selector's tuples rather than duplicating them, so
    # the scope a record is read as and the selection it ran cannot drift.
    assert evidence.SCOPE_FILES == SCOPE_FILES
    for files in SCOPE_FILES.values():
        assert files and len(set(files)) == len(files)


@pytest.mark.parametrize('scope', ['S4_JOINT_N2', 'S3_N1_CAPTURE', 'S2_DIAGNOSTIC_SUPERVISION'])
def test_full_selection_scopes_are_evidence(tmp_path, scope):
    # G1: each full-selection scope is evidence only when it is the scope asked
    # for, and only when its required nodes cover exactly that scope's files.
    ok, facts = evidence.evaluate(artifact(tmp_path, scope, nodes(SCOPE_FILES[scope])),
                                  expect_scope=scope)
    assert ok and facts['acceptance_scope'] == scope


def test_an_s4_record_reads_ok_with_the_default_scope(tmp_path):
    # Twenty nodes over the four S4 files, each file contributing at least one.
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S4_JOINT_N2', nodes(S4_CASES)))
    assert ok and facts['required_nodes'] == 4 * 5


@pytest.mark.parametrize('scope', ['S3_N1_CAPTURE', 'S2_DIAGNOSTIC_SUPERVISION'])
def test_a_smaller_selection_is_refused_unless_asked_for_explicitly(tmp_path, scope):
    ok, facts = evidence.evaluate(artifact(tmp_path, scope, nodes(SCOPE_FILES[scope])))
    assert not ok and facts['expected_scope'] == 'S4_JOINT_N2'
    ok, _facts = evidence.evaluate(artifact(tmp_path, scope, nodes(SCOPE_FILES[scope])),
                                   expect_scope=scope)
    assert ok


def test_an_s3_record_is_refused_as_s4_and_reads_ok_as_s3(tmp_path):
    # The S3 shape: three files, nineteen nodes, no N2 file among them.
    required = nodes(S3_CASES)
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S3_N1_CAPTURE', required))
    assert not ok
    assert facts['acceptance_scope'] == 'S3_N1_CAPTURE' and facts['expected_scope'] == 'S4_JOINT_N2'
    assert f"required nodes do not match the S4_JOINT_N2 file set: missing {S4_CASES[2]}" \
        in facts['refusals']
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S3_N1_CAPTURE', required),
                                  expect_scope='S3_N1_CAPTURE')
    assert ok and facts['required_nodes'] == 3 * 5


def test_an_s4_record_is_refused_when_read_as_s3(tmp_path):
    # The mirror image: a twenty-two-node S4 record carries the N2 file, which
    # the S3 selection never runs, so it is foreign to the S3 file set.
    required = nodes(S4_CASES)
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S4_JOINT_N2', required),
                                  expect_scope='S3_N1_CAPTURE')
    assert not ok
    assert f"required nodes do not match the S3_N1_CAPTURE file set: foreign {S4_CASES[2]}" \
        in facts['refusals']


def test_an_s3_labelled_record_with_the_n2_file_is_refused(tmp_path):
    # The pre-C2 defect shape: the label says S3, the nodes say otherwise.
    required = nodes(S3_CASES) + [f'{S4_CASES[2]}::test_joint_compute_ceiling']
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S3_N1_CAPTURE', required),
                                  expect_scope='S3_N1_CAPTURE')
    assert not ok
    assert f"required nodes do not match the S3_N1_CAPTURE file set: foreign {S4_CASES[2]}" \
        in facts['refusals']


def test_an_s4_record_missing_every_node_of_one_file_is_refused(tmp_path):
    # A hand-edited record can claim 22 nodes yet drop a whole file's share.
    n2 = S4_CASES[2]
    required = [node for node in nodes(S4_CASES) if not node.startswith(f'{n2}::')]
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S4_JOINT_N2', required))
    assert not ok
    refusal = f"required nodes do not match the S4_JOINT_N2 file set: missing {n2}"
    assert refusal in facts['refusals']


def test_a_node_from_an_unselected_file_is_foreign(tmp_path):
    required = nodes(S4_CASES, per_file=4) + ['tests/ops/qualification/test_other.py::test_case_0']
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S4_JOINT_N2', required))
    assert not ok
    assert "required nodes do not match the S4_JOINT_N2 file set: foreign " \
        "tests/ops/qualification/test_other.py" in facts['refusals']


@pytest.mark.parametrize('scope', ['DIAGNOSTIC_SUBSET', 'N1_ONLY_TEST_ONLY', None])
def test_other_scopes_are_never_evidence(tmp_path, scope):
    ok, _facts = evidence.evaluate(artifact(tmp_path, scope, nodes(S4_CASES)))
    assert not ok
