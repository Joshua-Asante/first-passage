"""The S2 artifact reader accepts only full-selection scopes, each bound to its file set."""
import json

import pytest

from scripts import s2_run_evidence as evidence
from scripts.qualification_boundary_verification import S2_CASES, S3_CASES, S4_CASES

PART_A_CASE = 'tests/integration/qualification_boundary/test_campaign_part_a_linux.py'
# The S5 selection: S4's set plus the Part A file, inserted before the
# supervision file (S4's placement rule — its OOM case stays last). Derived
# from the selector's own S4 tuple plus the fixed Part A path, exactly as the
# reader derives it, so the pin below is not the reader checking itself.
S5_CASES = (*S4_CASES[:-1], PART_A_CASE, S4_CASES[-1])
# The selection's own tuples: the reader must not own a second copy of them.
SCOPE_FILES = {'S4_JOINT_N2': S4_CASES, 'S3_N1_CAPTURE': S3_CASES,
               'S2_DIAGNOSTIC_SUPERVISION': S2_CASES, 'S5_PART_A': S5_CASES}


def nodes(files, per_file=5):
    """Required nodeids spread over `files`, every file contributing at least one."""
    return [f'{file}::test_case_{index}' for file in files for index in range(per_file)]


def part_a_export(**overrides):
    """One valid SR-8 export document; `overrides` forge single fields."""
    doc = {
        'schema': 'qualification_part_a_observations/v1',
        'attempt_id': 'linux-' + '0f' * 16,
        'cpu_ns': 42_000_000_000,
        'memory_peak_bytes': 252_549_120,
        'oom_events': 0,
        'reservation_to_captured_boottime_ns': 97_000_000_000,
        'payload_cpu_ns': 40_000_000_000,
        'guardian_cpu_ns': 1_900_000_000,
        'probe_seconds': 12.5,
        'predicted_seconds': 33.25,
    }
    doc.update(overrides)
    return doc


# The SR-8 export's own field groups (packet §1a SR-8): the settled counters,
# the payload/guardian CPU split (null where that side's CPU was not logged)
# and the PART_A result's two seconds.
SR8_COUNTERS = ('cpu_ns', 'memory_peak_bytes', 'oom_events',
                'reservation_to_captured_boottime_ns')
SR8_SPLIT = ('payload_cpu_ns', 'guardian_cpu_ns')
SR8_SECONDS = ('probe_seconds', 'predicted_seconds')


def read_s5(tmp_path, part_a):
    """A green S5 record carrying `part_a` as its SR-8 export; (ok, facts)."""
    return evidence.evaluate(
        artifact(tmp_path, 'S5_PART_A', nodes(S5_CASES), part_a=part_a),
        expect_scope='S5_PART_A')


def refused_with(facts, fragment):
    """True when some refusal message carries `fragment`."""
    return any(fragment in message for message in facts['refusals'])


def artifact(tmp_path, scope, required, part_a=None):
    """A green record for `scope`; `part_a` also writes the SR-8 export, either
    as a dict (encoded as JSON) or as raw text (to forge an unparseable one)."""
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
    if part_a is not None:
        export_dir = tmp_path / 'boundary'
        export_dir.mkdir(exist_ok=True)
        (export_dir / 'part_a_observations.json').write_text(
            part_a if isinstance(part_a, str) else json.dumps(part_a))
    return tmp_path


def test_the_default_expected_scope_is_the_s4_joint_set():
    # The workflow's default mode is s4, so a plain read asks for S4_JOINT_N2.
    assert evidence.ACCEPTANCE_SCOPES == ('S4_JOINT_N2', 'S3_N1_CAPTURE',
                                          'S2_DIAGNOSTIC_SUPERVISION', 'S5_PART_A')
    assert evidence.DEFAULT_SCOPE == 'S4_JOINT_N2'


def test_each_scope_is_bound_to_the_selectors_own_file_set():
    # The reader reads the selector's tuples rather than duplicating them, so
    # the scope a record is read as and the selection it ran cannot drift.
    assert evidence.SCOPE_FILES == SCOPE_FILES
    for files in SCOPE_FILES.values():
        assert files and len(set(files)) == len(files)


def test_the_s5_scope_is_the_s4_set_plus_the_part_a_file():
    # S5 is the S4 set plus the Part A file, in S4's own placement rule
    # (packet §2: the Part A Linux file before the S2 OOM case, which stays
    # last), and in the selector's own type: a tuple.
    s5 = SCOPE_FILES['S5_PART_A']
    assert isinstance(s5, tuple)
    assert set(s5) - set(S4_CASES) == {PART_A_CASE}
    assert len(s5) == len(S4_CASES) + 1
    # Dropping the Part A entry leaves S4's tuple in its own order.
    assert tuple(path for path in s5 if path != PART_A_CASE) == S4_CASES
    # The Part A file is inserted immediately before S4's last file.
    assert s5 == (*S4_CASES[:-1], PART_A_CASE, S4_CASES[-1])


@pytest.mark.parametrize('scope', ['S4_JOINT_N2', 'S3_N1_CAPTURE', 'S2_DIAGNOSTIC_SUPERVISION',
                                   'S5_PART_A'])
def test_full_selection_scopes_are_evidence(tmp_path, scope):
    # G1: each full-selection scope is evidence only when it is the scope asked
    # for, and only when its required nodes cover exactly that scope's files.
    ok, facts = evidence.evaluate(artifact(tmp_path, scope, nodes(SCOPE_FILES[scope]),
                                           part_a=part_a_export() if scope == 'S5_PART_A' else None),
                                  expect_scope=scope)
    assert ok and facts['acceptance_scope'] == scope


def test_an_s4_record_reads_ok_with_the_default_scope(tmp_path):
    # Twenty nodes over the four S4 files, each file contributing at least one.
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S4_JOINT_N2', nodes(S4_CASES)))
    assert ok and facts['required_nodes'] == 4 * 5


@pytest.mark.parametrize('scope', ['S3_N1_CAPTURE', 'S2_DIAGNOSTIC_SUPERVISION', 'S5_PART_A'])
def test_a_smaller_selection_is_refused_unless_asked_for_explicitly(tmp_path, scope):
    ok, facts = evidence.evaluate(artifact(tmp_path, scope, nodes(SCOPE_FILES[scope]),
                                           part_a=part_a_export() if scope == 'S5_PART_A' else None))
    assert not ok and facts['expected_scope'] == 'S4_JOINT_N2'
    ok, _facts = evidence.evaluate(artifact(tmp_path, scope, nodes(SCOPE_FILES[scope]),
                                            part_a=part_a_export() if scope == 'S5_PART_A' else None),
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


def test_a_valid_sr8_export_reads_ok(tmp_path):
    # The whole closed document is accepted and retained in `facts` for
    # citation, not skimmed for a subset of its fields.
    ok, facts = read_s5(tmp_path, part_a_export())
    assert ok
    assert facts['part_a_observations'] == part_a_export()


def test_a_missing_sr8_export_is_refused(tmp_path):
    ok, facts = read_s5(tmp_path, None)
    assert not ok and refused_with(facts, f'{evidence.PART_A_EXPORT} is missing')
    assert facts['part_a_observations'] is None


@pytest.mark.parametrize('part_a', ['{not json', '[1, 2, 3]', 'null'])
def test_an_unreadable_sr8_export_is_refused(tmp_path, part_a):
    # Raw text forges every non-document shape: unparseable JSON, a JSON
    # array and a JSON null.
    ok, facts = read_s5(tmp_path, part_a)
    assert not ok and facts['part_a_observations'] is None


def test_a_foreign_sr8_schema_is_refused(tmp_path):
    doc = part_a_export(schema='qualification_part_a_observations/v2')
    ok, facts = read_s5(tmp_path, doc)
    assert not ok and refused_with(facts, 'schema is')
    assert facts['part_a_observations'] == doc


def test_an_empty_sr8_attempt_id_is_refused(tmp_path):
    ok, facts = read_s5(tmp_path, part_a_export(attempt_id=''))
    assert not ok and refused_with(facts, 'attempt_id is not a non-empty string')


def test_an_added_sr8_field_is_refused(tmp_path):
    # The key set is closed: a producer that adds a field is refused, never
    # skimmed for the fields the reader knows.
    doc = part_a_export(wall_ns=12)
    ok, facts = read_s5(tmp_path, doc)
    assert not ok and refused_with(facts, 'fields differ from the closed SR-8 set')
    assert facts['part_a_observations'] is None


@pytest.mark.parametrize('field,value', [
    ('cpu_ns', 41_500_000_000),
    ('memory_peak_bytes', 252_549_120),
    ('oom_events', 1),
    ('reservation_to_captured_boottime_ns', 0),
    ('payload_cpu_ns', 40_000_000_000),
    ('guardian_cpu_ns', None),
    ('probe_seconds', 0.0),
    ('predicted_seconds', 120.0),
])
def test_each_sr8_field_has_an_accepted_value(tmp_path, field, value):
    # Zero and null are accepted where the field's own kind allows them: a
    # counter or a second may be zero, and a split side may not have been
    # logged at all.
    ok, facts = read_s5(tmp_path, part_a_export(**{field: value}))
    assert ok
    assert facts['part_a_observations'][field] == value


@pytest.mark.parametrize('field', SR8_COUNTERS + SR8_SPLIT + SR8_SECONDS)
def test_a_missing_sr8_field_is_refused(tmp_path, field):
    # A missing key breaks the closed set before any value is validated, and
    # the reader retains nothing from a refused document.
    doc = part_a_export()
    del doc[field]
    ok, facts = read_s5(tmp_path, doc)
    assert not ok and refused_with(facts, 'fields differ from the closed SR-8 set')
    assert facts['part_a_observations'] is None


@pytest.mark.parametrize('field,bad', [
    ('cpu_ns', '42000000000'), ('cpu_ns', 42.0), ('cpu_ns', True),
    ('memory_peak_bytes', '252549120'), ('memory_peak_bytes', 252549120.5),
    ('memory_peak_bytes', False),
    ('oom_events', '0'), ('oom_events', 0.0), ('oom_events', True),
    ('reservation_to_captured_boottime_ns', '97000000000'),
    ('reservation_to_captured_boottime_ns', 97.0),
    ('reservation_to_captured_boottime_ns', True),
])
def test_an_sr8_counter_of_the_wrong_type_is_refused(tmp_path, field, bad):
    # Counters are integers: a string, a float and a JSON boolean (which is
    # an int subclass in Python) are all refused.
    ok, facts = read_s5(tmp_path, part_a_export(**{field: bad}))
    assert not ok
    assert refused_with(facts, f'{evidence.PART_A_EXPORT} {field} is not a nonnegative integer')


@pytest.mark.parametrize('field,bad', [
    ('payload_cpu_ns', '40000000000'), ('payload_cpu_ns', 40.5), ('payload_cpu_ns', True),
    ('guardian_cpu_ns', '1900000000'), ('guardian_cpu_ns', 1.9), ('guardian_cpu_ns', False),
])
def test_an_sr8_split_value_of_the_wrong_type_is_refused(tmp_path, field, bad):
    # Only two shapes are allowed: a nonnegative integer, or null for a side
    # whose CPU was not logged.
    ok, facts = read_s5(tmp_path, part_a_export(**{field: bad}))
    assert not ok
    assert refused_with(facts, f'{evidence.PART_A_EXPORT} {field} is neither a nonnegative '
                               'integer nor null')


@pytest.mark.parametrize('field,bad', [
    ('probe_seconds', 12), ('probe_seconds', '12.5'), ('probe_seconds', True),
    ('predicted_seconds', 33), ('predicted_seconds', '33.25'), ('predicted_seconds', False),
])
def test_an_sr8_second_of_the_wrong_type_is_refused(tmp_path, field, bad):
    # The two seconds carry the worker-result document's own type, a float:
    # a JSON integer, a string and a JSON boolean are refused.
    ok, facts = read_s5(tmp_path, part_a_export(**{field: bad}))
    assert not ok
    assert refused_with(facts, f'{evidence.PART_A_EXPORT} {field} is not a finite nonnegative '
                               'float')


@pytest.mark.parametrize('field', SR8_COUNTERS)
def test_a_negative_sr8_counter_is_refused(tmp_path, field):
    ok, facts = read_s5(tmp_path, part_a_export(**{field: -1}))
    assert not ok
    assert refused_with(facts, f'{evidence.PART_A_EXPORT} {field} is not a nonnegative integer')


@pytest.mark.parametrize('field', SR8_SPLIT)
def test_a_negative_sr8_split_value_is_refused(tmp_path, field):
    ok, facts = read_s5(tmp_path, part_a_export(**{field: -1}))
    assert not ok
    assert refused_with(facts, f'{evidence.PART_A_EXPORT} {field} is neither a nonnegative '
                               'integer nor null')


@pytest.mark.parametrize('field', SR8_SECONDS)
def test_a_negative_sr8_second_is_refused(tmp_path, field):
    ok, facts = read_s5(tmp_path, part_a_export(**{field: -0.5}))
    assert not ok
    assert refused_with(facts, f'{evidence.PART_A_EXPORT} {field} is not a finite nonnegative '
                               'float')


@pytest.mark.parametrize('field', SR8_SECONDS)
@pytest.mark.parametrize('bad', [float('nan'), float('inf')])
def test_a_nonfinite_sr8_second_is_refused(tmp_path, field, bad):
    # json.dumps writes NaN/Infinity and json.loads reads them back, so the
    # reader must refuse them on finiteness, not on parsing.
    ok, facts = read_s5(tmp_path, part_a_export(**{field: bad}))
    assert not ok
    assert refused_with(facts, f'{evidence.PART_A_EXPORT} {field} is not a finite nonnegative '
                               'float')


def test_the_sr8_export_is_read_only_under_the_s5_scope(tmp_path):
    # A garbage export beside a green S4 record neither helps nor harms the
    # read: the reader opens the file only under the S5 scope.
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S4_JOINT_N2', nodes(S4_CASES),
                                           part_a='{not json'))
    assert ok and 'part_a_observations' not in facts
