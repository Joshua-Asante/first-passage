"""The S2 artifact reader accepts only full-selection scopes, each bound to its file set."""
import hashlib
import json
from pathlib import Path

import pytest

from scripts import s2_run_evidence as evidence
# R1_CASES is imported inside the one test that pins it, so the R2 falsifier
# (`--expect-scope T05_R1_COMBINED` is not yet a choice) can even run against
# a base selector that has no R1_CASES to import.
from scripts.qualification_boundary_verification import S2_CASES, S3_CASES, S4_CASES

PART_A_CASE = 'tests/integration/qualification_boundary/test_campaign_part_a_linux.py'
RESULT_SEAL_CASE = 'tests/integration/qualification_boundary/test_campaign_result_seal_linux.py'
CPRIME_CASE = 'tests/integration/qualification_boundary/test_runtime_identity_linux.py'
# The S5 selection: S4's set plus the Part A file, inserted before the
# supervision file (S4's placement rule — its OOM case stays last). Derived
# from the selector's own S4 tuple plus the fixed Part A path, exactly as the
# reader derives it, so the pin below is not the reader checking itself.
S5_CASES = (*S4_CASES[:-1], PART_A_CASE, S4_CASES[-1])
# The R1 selection: the selector's own tuple, spelled out here from the same
# seven fixed paths so the pin below is not the reader checking itself.
R1_SPELLING = (S2_CASES[0], 'tests/integration/qualification_boundary/test_campaign_n1_linux.py',
               'tests/integration/qualification_boundary/test_campaign_n2_linux.py',
               PART_A_CASE, RESULT_SEAL_CASE, CPRIME_CASE, S2_CASES[-1])
# The selection's own tuples: the reader must not own a second copy of them.
SCOPE_FILES = {'S4_JOINT_N2': S4_CASES, 'S3_N1_CAPTURE': S3_CASES,
               'S2_DIAGNOSTIC_SUPERVISION': S2_CASES, 'S5_PART_A': S5_CASES,
               'T05_R1_COMBINED': R1_SPELLING}


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


def artifact(tmp_path, scope, required, part_a=None, collected=None, junit=None):
    """A green record for `scope`; `part_a` also writes the SR-8 export, either
    as a dict (encoded as JSON) or as raw text (to forge an unparseable one);
    `collected` also writes the record's collected.json (or raw text); `junit`
    overrides the JUnit totals."""
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
    tests, failures, errors, skipped = (junit if junit is not None
                                        else (total, 0, 0, 0))
    (record_dir / 'junit.xml').write_text(
        f'<testsuites><testsuite tests="{tests}" failures="{failures}" '
        f'errors="{errors}" skipped="{skipped}"/></testsuites>')
    if collected is not None:
        (record_dir / 'collected.json').write_text(
            collected if isinstance(collected, str) else json.dumps(collected))
    else:
        # A reused tmp_path must not inherit an earlier call's collection.
        (record_dir / 'collected.json').unlink(missing_ok=True)
    if part_a is not None:
        export_dir = tmp_path / 'boundary'
        export_dir.mkdir(exist_ok=True)
        (export_dir / 'part_a_observations.json').write_text(
            part_a if isinstance(part_a, str) else json.dumps(part_a))
    return tmp_path


# A sentinel, because `None` is itself one of the forged node_ids values.
_DEFAULT_NODE_IDS = object()


def selection(node_ids=_DEFAULT_NODE_IDS, **overrides):
    """One frozen r1-dispatch-selection/1 document; `overrides` forge fields."""
    default = nodes(R1_SPELLING)
    ids = default if node_ids is _DEFAULT_NODE_IDS else node_ids
    count = len(ids) if isinstance(ids, list) else len(default)
    doc = {'schema': 'r1-dispatch-selection/1', 'acceptance_scope': 'T05_R1_COMBINED',
           'node_count': count, 'node_ids': ids}
    doc.update(overrides)
    return doc


def write_selection(tmp_path, doc, name='frozen-selection.json'):
    """Write a selection document into a test temp directory; raw text forges one."""
    path = tmp_path / name
    path.write_text(doc if isinstance(doc, str) else json.dumps(doc), encoding='utf-8')
    return path


def read_r1(tmp_path, doc=None, *, required=None, collected='default', part_a='default'):
    """An R1 read of a complete record plus `doc` as the frozen selection."""
    required = nodes(R1_SPELLING) if required is None else required
    if collected == 'default':
        collected = list(required)
    if part_a == 'default':
        part_a = part_a_export()
    path = None if doc is None else (doc if isinstance(doc, Path) else write_selection(tmp_path, doc))
    return evidence.evaluate(
        artifact(tmp_path, 'T05_R1_COMBINED', required, part_a=part_a, collected=collected),
        expect_scope='T05_R1_COMBINED', expect_selection=path)


def test_the_default_expected_scope_is_the_s4_joint_set():
    # The workflow's default mode is s4, so a plain read asks for S4_JOINT_N2;
    # T05_R1_COMBINED is appended, never first (D2 keeps the default unchanged).
    assert evidence.ACCEPTANCE_SCOPES == ('S4_JOINT_N2', 'S3_N1_CAPTURE',
                                          'S2_DIAGNOSTIC_SUPERVISION', 'S5_PART_A',
                                          'T05_R1_COMBINED')
    assert evidence.ACCEPTANCE_SCOPES[-1] == 'T05_R1_COMBINED'
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


# --- T05_R1_COMBINED: the H9 checkpoint R1 combined read -----------------------

def test_the_r1_scope_is_bound_to_the_selectors_own_r1_tuple():
    """G6: the reader imports R1_CASES from the selector rather than duplicating
    it, so the scope a record is read as and the selection it ran cannot drift."""
    from scripts.qualification_boundary_verification import R1_CASES
    assert evidence.SCOPE_FILES['T05_R1_COMBINED'] is R1_CASES
    assert isinstance(R1_CASES, tuple) and len(R1_CASES) == 7
    assert R1_CASES == R1_SPELLING
    assert set(R1_CASES) - set(S5_CASES) == {RESULT_SEAL_CASE, CPRIME_CASE}
    assert R1_CASES[-1] == S5_CASES[-1]


def test_the_r1_scope_is_a_named_choice_of_the_command_line(monkeypatch, tmp_path, capsys):
    """R2 (falsifier-first) and G6: `--expect-scope T05_R1_COMBINED` parses, and
    with it `--expect-selection` is required (argparse/usage error, exit 2)."""
    monkeypatch.setattr(evidence, 'run_head', lambda run_id: {'headSha': 'ab' * 20})
    monkeypatch.setattr(evidence, 'download', lambda run_id, dest: None)
    for argv in (['1', '--dest', str(tmp_path), '--expect-scope', 'T05_R1_COMBINED'],):
        with pytest.raises(SystemExit) as exc:
            evidence.main(argv)
        assert exc.value.code == 2
    out = capsys.readouterr()
    assert '--expect-selection' in (out.err + out.out)
    assert 'unrecognized' not in out.err and 'invalid choice' not in out.err


@pytest.mark.parametrize('scope', ['S4_JOINT_N2', 'S3_N1_CAPTURE',
                                   'S2_DIAGNOSTIC_SUPERVISION', 'S5_PART_A'])
def test_expect_selection_is_refused_with_any_other_scope(monkeypatch, tmp_path, scope):
    """G6: `--expect-selection` applies to T05_R1_COMBINED only."""
    monkeypatch.setattr(evidence, 'run_head', lambda run_id: {'headSha': 'ab' * 20})
    monkeypatch.setattr(evidence, 'download', lambda run_id, dest: None)
    with pytest.raises(SystemExit) as exc:
        evidence.main(['1', '--dest', str(tmp_path), '--expect-scope', scope,
                       '--expect-selection', str(write_selection(tmp_path, selection()))])
    assert exc.value.code == 2


def test_the_r1_scope_never_reads_ok_without_a_selection(tmp_path):
    """G6: `--expect-selection` is required for the R1 scope, refused by name."""
    required = nodes(R1_SPELLING)
    ok, facts = evidence.evaluate(artifact(tmp_path, 'T05_R1_COMBINED', required,
                                           part_a=part_a_export(),
                                           collected=list(required)),
                                  expect_scope='T05_R1_COMBINED')
    assert not ok and refused_with(facts, '--expect-selection is required')
    assert facts['expected_selection_sha256'] is None


def test_a_complete_r1_record_is_refused_only_for_the_owed_cprime_check(tmp_path):
    """G6: every other check green, the record still cannot read ok — the C'
    coverage-export schema is owed by the C' build, so the scope is fail-closed
    (card §3 D6) and names exactly that one reason."""
    ok, facts = read_r1(tmp_path, selection())
    assert not ok
    assert facts['refusals'] == ['cprime_coverage_export_check_owed']
    assert evidence.CPRIME_COVERAGE_OWED == 'cprime_coverage_export_check_owed'
    assert facts['expected_selection_count'] == 7 * 5
    assert facts['expected_selection_sha256'] == hashlib.sha256(
        write_selection(tmp_path, selection()).read_bytes()).hexdigest()


def test_an_r1_record_still_requires_the_sr8_export(tmp_path):
    """G6: R1 runs the S5 selection too, so its file set carries the Part A case
    and the record must export the SR-8 observation."""
    required = nodes(R1_SPELLING)
    path = write_selection(tmp_path, selection())
    ok, facts = evidence.evaluate(artifact(tmp_path, 'T05_R1_COMBINED', required,
                                           part_a=None, collected=list(required)),
                                  expect_scope='T05_R1_COMBINED', expect_selection=path)
    assert not ok and refused_with(facts, f'{evidence.PART_A_EXPORT} is missing')


def test_an_r1_record_is_refused_when_a_skip_a_missing_file_or_a_foreign_node(
        tmp_path):
    """G6: the ordinary record facts bind R1 as they bind S4/S5."""
    required = nodes(R1_SPELLING)
    path = write_selection(tmp_path, selection())
    # A skipped junit case.
    ok, facts = evidence.evaluate(artifact(tmp_path, 'T05_R1_COMBINED', required,
                                           part_a=part_a_export(), collected=list(required),
                                           junit=(len(required), 0, 0, 1)),
                                  expect_scope='T05_R1_COMBINED', expect_selection=path)
    assert not ok and refused_with(facts, 'junit skipped=')
    # A whole file's share of required nodes dropped.
    ok, facts = evidence.evaluate(artifact(tmp_path, 'T05_R1_COMBINED',
                                           [node for node in required
                                            if not node.startswith(CPRIME_CASE + '::')],
                                           part_a=part_a_export(),
                                           collected=[node for node in required
                                                      if not node.startswith(CPRIME_CASE + '::')]),
                                  expect_scope='T05_R1_COMBINED', expect_selection=path)
    assert not ok
    assert f'required nodes do not match the T05_R1_COMBINED file set: missing {CPRIME_CASE}' \
        in facts['refusals']
    # A node from a file R1 never runs.
    ok, facts = evidence.evaluate(artifact(tmp_path, 'T05_R1_COMBINED',
                                           required + ['tests/ops/qualification/test_other.py::test_x'],
                                           part_a=part_a_export(),
                                           collected=required + ['tests/ops/qualification/test_other.py::test_x']),
                                  expect_scope='T05_R1_COMBINED', expect_selection=path)
    assert not ok
    assert 'required nodes do not match the T05_R1_COMBINED file set: foreign ' \
        'tests/ops/qualification/test_other.py' in facts['refusals']


def test_cross_scope_reads_are_refused_both_ways(tmp_path):
    """G6: an S5 record never reads as R1 and an R1 record never reads as S5."""
    required = nodes(R1_SPELLING)
    path = write_selection(tmp_path, selection())
    ok, facts = evidence.evaluate(artifact(tmp_path, 'S5_PART_A', nodes(S5_CASES),
                                           part_a=part_a_export()),
                                  expect_scope='T05_R1_COMBINED', expect_selection=path)
    assert not ok and facts['acceptance_scope'] == 'S5_PART_A'
    assert f'required nodes do not match the T05_R1_COMBINED file set: missing {RESULT_SEAL_CASE}' \
        in facts['refusals']
    ok, facts = evidence.evaluate(artifact(tmp_path, 'T05_R1_COMBINED', required,
                                           part_a=part_a_export(), collected=list(required)),
                                  expect_scope='S5_PART_A')
    assert not ok and facts['acceptance_scope'] == 'T05_R1_COMBINED'
    assert f'required nodes do not match the S5_PART_A file set: foreign {RESULT_SEAL_CASE}' \
        in facts['refusals']


@pytest.mark.parametrize('doc,fragment', [
    ('{not json', 'cannot be read as JSON'),
    ('[1, 2, 3]', 'fields differ from the closed set'),
    (selection(schema='r1-dispatch-selection/2'), 'schema is'),
    (selection(acceptance_scope='S5_PART_A'), 'acceptance_scope is'),
    (selection(node_count=0), 'node_count is not a positive integer'),
    (selection(node_count=True), 'node_count is not a positive integer'),
    (selection(node_count='7'), 'node_count is not a positive integer'),
    (selection(node_ids=None), 'node_ids is not a list of strings'),
    (selection(node_count=2), 'but it lists'),
    (selection(extra=1), 'fields differ from the closed set'),
])
def test_each_selection_defect_is_refused_by_name(tmp_path, doc, fragment):
    """G6: every malformed frozen selection is refused, never skimmed."""
    ok, facts = read_r1(tmp_path, doc)
    assert not ok and refused_with(facts, fragment), fragment


def test_a_selection_with_a_missing_file_or_a_duplicate_node_is_refused(tmp_path):
    required = nodes(R1_SPELLING)
    duplicated = list(required) + [required[0]]
    ok, facts = read_r1(tmp_path, selection(duplicated))
    assert not ok and refused_with(facts, 'repeats node IDs')
    ok, facts = read_r1(tmp_path, Path(tmp_path / 'absent-selection.json'))
    assert not ok and refused_with(facts, 'cannot be read')


def test_a_selection_that_disagrees_with_the_records_collection_is_refused(tmp_path):
    """G6: the frozen selection must equal the record's own collected.json, as a
    set and as a count."""
    required = nodes(R1_SPELLING)
    ok, facts = read_r1(tmp_path, selection(), collected=required[:-1])
    assert not ok
    assert refused_with(facts, 'the frozen selection differs from collected.json')
    assert refused_with(facts, 'collected.json lists 34 nodes, the frozen selection declares 35')
    ok, facts = read_r1(tmp_path, selection(), collected='{not json')
    assert not ok and refused_with(facts, 'collected.json cannot be read as JSON')
    ok, facts = read_r1(tmp_path, selection(), collected=None)
    assert not ok and refused_with(facts, 'collected.json is missing from the record')
