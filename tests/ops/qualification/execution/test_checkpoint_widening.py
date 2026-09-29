"""C2 repair R2a: the S4-D1 8 -> 9 widening on a real S3 v8 journal.

The previous widening raised sqlite3.OperationalError here."""

import sqlite3

import pytest

from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_funding import SCHEMA as FUNDING_SCHEMA
from c1_rail.qualification.execution.campaign_store import (
    BUDGET_SCHEMA,
    CHECKPOINT_SCHEMA,
    CHECKPOINT_SCHEMA_V8,
    SCHEMA as CAMPAIGN_SCHEMA,
    widen_checkpoint_layout,
)
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.execution.store import _SCHEMA, ExecutionStore

ATTEMPT = 'attempt-widen'
LAYOUT = 'SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name'
CAPTURES = 'full_campaign_checkpoint_captures'
STAGED = 'full_campaign_checkpoint_staged'
INTENTS = 'full_campaign_checkpoint_intents'
CHECKPOINT_TABLES = (CAPTURES, STAGED, INTENTS)
# The staged table's v8 columns; named so the same insert also fits the
# deliberately reordered (inexact) v8 layout of the refusal test.
STAGED_COLUMNS = ' (attempt_id,role,sha256,body)'


def _dormant_campaign():
    """A real dormant (admitted, unfunded) campaign: exactly the parent rows
    CampaignStore.integrity's dormant branch walks, so the eager widening on
    reopen happens in a journal that still reopens clean."""
    plan = encoded(
        {
            'schema': 'qualification_campaign_plan/v1',
            'attempt_id': ATTEMPT,
            'source_bundle_sha256': 'e' * 64,
            'budget': {'maximum_cpu_seconds': 1, 'maximum_wall_seconds': 1},
            'contract_sha256': 'a' * 64,
            'trust_domain_sha256': 'b' * 64,
            'execution_release_sha256': 'c' * 64,
            'policy_sha256': 'd' * 64,
        }
    )
    index = encoded({'schema': 'qualification_bundle_index/v1', 'entries': []})
    request = encoded(
        {
            'schema': 'qualification_campaign_request/v1',
            'operation': 'SUBMIT_E1',
            'attempt_id': ATTEMPT,
            'bundle_sha256': sha256(index),
            'request_id': 'request-1',
        }
    )
    receipt = encoded(
        {
            'schema': 'qualification_campaign_admission_receipt/v1',
            'campaign_id': 'campaign-widen',
            'attempt_id': ATTEMPT,
            'state': 'ADMITTED',
            'authority_class': 'TEST_ONLY',
            'dispatch_enabled': False,
            'request_sha256': sha256(request),
            'bundle_sha256': sha256(index),
            'plan_sha256': sha256(plan),
            'plan_byte_length': len(plan),
            'contract_sha256': 'a' * 64,
            'trust_domain_sha256': 'b' * 64,
            'execution_release_sha256': 'c' * 64,
            'profile_sha256': 'f' * 64,
            'policy_sha256': 'd' * 64,
            'budget_sha256': sha256(
                encoded({'maximum_cpu_seconds': 1, 'maximum_wall_seconds': 1})
            ),
            'admitted_at_utc': '2026-09-22T00:00:00Z',
        }
    )
    return (ATTEMPT, 'campaign-widen', request, receipt, 'VALID', None, None), (
        ('plan', plan),
        ('bundle_index', index),
    )


def _insert_journal_rows(connection):
    """S3's own v8 checkpoint rows, on the parent campaign they reference."""
    campaign, objects = _dormant_campaign()
    connection.execute('INSERT INTO full_campaigns VALUES(?,?,?,?,?,?,?)', campaign)
    for role, raw in objects:
        connection.execute(
            'INSERT INTO full_campaign_objects VALUES(?,?,?,?,?)',
            (ATTEMPT, role, sha256(raw), len(raw), raw),
        )
    connection.execute(
        'INSERT INTO ' + CAPTURES + ' VALUES(?,?,?,?,?,?)',
        (ATTEMPT, 'N1', 'work-1', b'result-bytes', b'payload-bytes', None),
    )
    connection.execute(
        'INSERT INTO ' + STAGED + STAGED_COLUMNS + ' VALUES(?,?,?,?)',
        (ATTEMPT, 'role-1', 'a' * 64, b'staged-bytes'),
    )
    connection.execute(
        'INSERT INTO ' + INTENTS + ' VALUES(?,?,?,?,?,?,?,?)',
        (ATTEMPT, 'N1', 'work-1', b'snapshot', b'intent', b'candidate', None, None),
    )


def _v8_journal(path, *, checkpoint_schema=CHECKPOINT_SCHEMA_V8):
    """S3's journal exactly as a8a983e left it: v8 layout, user_version 8."""
    connection = sqlite3.connect(path, isolation_level=None)
    connection.execute('PRAGMA journal_mode=WAL')
    connection.executescript(
        _SCHEMA
        + CAMPAIGN_SCHEMA
        + BUDGET_SCHEMA
        + FUNDING_SCHEMA
        + checkpoint_schema
        + '\nPRAGMA user_version=8;\n'
    )
    _insert_journal_rows(connection)
    connection.close()
    return path


def _reference_layout(path):
    """A fresh v9 journal from the current schema owner: the exact widened layout."""
    connection = sqlite3.connect(path, isolation_level=None)
    connection.execute('PRAGMA journal_mode=WAL')
    connection.executescript(
        _SCHEMA
        + CAMPAIGN_SCHEMA
        + BUDGET_SCHEMA
        + FUNDING_SCHEMA
        + CHECKPOINT_SCHEMA
        + '\nPRAGMA user_version=9;\n'
    )
    try:
        return [tuple(row) for row in connection.execute(LAYOUT)]
    finally:
        connection.close()


def _journal_state(path):
    """version, the three checkpoint tables' rows, and the whole sqlite_master."""
    connection = sqlite3.connect(path)
    try:
        return (
            connection.execute('PRAGMA user_version').fetchone()[0],
            {table: [tuple(row) for row in connection.execute('SELECT * FROM ' + table)]
             for table in CHECKPOINT_TABLES},
            [tuple(row) for row in connection.execute(LAYOUT)],
        )
    finally:
        connection.close()


def _assert_widened(path, reference):
    """The widened journal: v9, byte-identical rows (staged gains N1), exact layout."""
    version, rows, layout = _journal_state(path)
    assert version == 9
    # Every column of every row is byte-identical; the one change is the staged
    # row, which carried no checkpoint at v8 and gains its N1 custody key.
    assert rows[CAPTURES] == [(ATTEMPT, 'N1', 'work-1', b'result-bytes', b'payload-bytes', None)]
    assert rows[STAGED] == [(ATTEMPT, 'N1', 'role-1', 'a' * 64, b'staged-bytes')]
    assert rows[INTENTS] == [
        (ATTEMPT, 'N1', 'work-1', b'snapshot', b'intent', b'candidate', None, None)
    ]
    assert layout == reference
    assert not [row for row in layout if row[1].endswith('_v8')]


def test_a_real_s3_v8_journal_widens_to_v9_exactly(tmp_path, monkeypatch):
    """Reopen widens eagerly, so the exact-layout walk that follows sees v9 only."""
    from test_campaign_n1 import g5_claimed, persisted_intent, commit, store

    instance = g5_claimed(tmp_path, monkeypatch)
    commit(instance, persisted_intent(instance))
    journal = instance.store.path
    # Build the frozen predecessor layout around actual funded N1 custody.
    # Opaque marker bytes suffice for the low-level copying test below, but
    # cannot establish successful reopen through the restored integrity walk.
    connection = sqlite3.connect(journal)
    original = {table: connection.execute('SELECT * FROM ' + table).fetchall()
                for table in CHECKPOINT_TABLES}
    connection.executescript(''.join('DROP TABLE ' + table + ';' for table in CHECKPOINT_TABLES)
                             + CHECKPOINT_SCHEMA_V8)
    for table, rows in original.items():
        for row in rows:
            values = row[:1] + row[2:] if table == STAGED else row
            connection.execute('INSERT INTO ' + table + ' VALUES('
                               + ','.join('?' for _ in values) + ')', values)
    connection.execute('PRAGMA user_version=8')
    connection.commit()
    connection.close()
    before = store(instance).checkpoint_receipt(instance.attempt, 'N1')
    ExecutionStore(journal)  # the widening lands eagerly on reopen
    version, rows, layout = _journal_state(journal)
    assert version == 9 and rows == original
    assert layout == _reference_layout(tmp_path / 'reference.sqlite')
    assert store(instance).checkpoint_receipt(instance.attempt, 'N1') == before


def test_the_lazy_path_widens_the_same_way(tmp_path):
    """The writer's own lazy call, inside its BEGIN IMMEDIATE, lands identically."""
    journal = _v8_journal(tmp_path / 'journal.sqlite')
    reference = _reference_layout(tmp_path / 'reference.sqlite')

    connection = sqlite3.connect(journal, isolation_level=None)
    connection.execute('BEGIN IMMEDIATE')
    widen_checkpoint_layout(connection)
    connection.execute('COMMIT')
    connection.close()

    _assert_widened(journal, reference)


def test_a_non_exact_v8_journal_is_refused_before_any_rebuild(tmp_path):
    """A v8 journal that is not S3's exact layout is refused before any rename."""
    inexact = CHECKPOINT_SCHEMA_V8.replace(
        ' role TEXT NOT NULL, sha256 TEXT NOT NULL,', ' sha256 TEXT NOT NULL, role TEXT NOT NULL,'
    )
    journal = _v8_journal(tmp_path / 'journal.sqlite', checkpoint_schema=inexact)
    connection = sqlite3.connect(journal, isolation_level=None)
    version, rows, layout = _journal_state(journal)
    assert version == 8

    connection.execute('BEGIN IMMEDIATE')
    with pytest.raises(ValueError, match='unsupported journal schema layout'):
        widen_checkpoint_layout(connection)
    connection.execute('ROLLBACK')
    try:
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 8
        assert _journal_state(journal) == (8, rows, layout)
    finally:
        connection.close()


def test_the_frozen_v8_literal_is_not_the_widened_layout():
    """The frozen predecessor really is the narrower S3 shape, not v9 by another name."""
    assert CHECKPOINT_SCHEMA_V8 != CHECKPOINT_SCHEMA
    assert "CHECK(checkpoint='N1')" in CHECKPOINT_SCHEMA_V8
    assert 'PRIMARY KEY(attempt_id,role,sha256)' in CHECKPOINT_SCHEMA_V8


# ---- S5 R1/R2/R4: the PART_A progression pair and the capture field set -----


def test_part_a_progression_pair_and_phase_sets():
    """R1: the PART_A advance pair exists and both names are progression states
    (the settling G5 work completes in them). R2: PART_A_READY admits exactly
    the PART_A compute/capture/G5 phases; FULL_PASS_READY and PART_A_FAILED
    admit none."""
    from c1_rail.qualification.execution.campaign_store import (
        CHECKPOINT_ADVANCES,
        CHECKPOINT_PROGRESSION_STATES,
        PROGRESSION_PHASES,
    )

    assert CHECKPOINT_ADVANCES['PART_A'] == ('FULL_PASS_READY', 'PART_A_FAILED')
    assert 'FULL_PASS_READY' in CHECKPOINT_PROGRESSION_STATES
    assert 'PART_A_FAILED' in CHECKPOINT_PROGRESSION_STATES
    assert PROGRESSION_PHASES['PART_A_READY'] == ('PART_A', 'PART_A_CAPTURE', 'PART_A_G5')
    assert 'FULL_PASS_READY' not in PROGRESSION_PHASES
    assert 'PART_A_FAILED' not in PROGRESSION_PHASES


def test_part_a_capture_fields_form_a_validated_closed_set():
    """R4: PART_A requires the five S5-D1 fields, N1/N2 refuse any of them, and
    the digests, panel counts and expansion fact are validated. The method is
    a static helper, so it is tested directly."""
    from c1_rail.qualification.execution.campaign_store import (
        PART_A_CAPTURE_FIELDS,
        CampaignStore,
    )

    capture = CampaignStore._part_a_capture
    valid = {
        'initial_prefix_sha256': '1' * 64,
        'final_sha256': '2' * 64,
        'initial_panels': 2,
        'final_panels': 4,
        'expansion_required': True,
    }
    assert capture('PART_A', **valid) == valid
    # The production call shape (retain_checkpoint_capture) always names all
    # five arguments; an unset one arrives as None.
    unset = dict.fromkeys(PART_A_CAPTURE_FIELDS)
    # N1 and N2 take none of the fields; their capture stays the empty set.
    assert capture('N1', **unset) == {}
    assert capture('N2', **unset) == {}
    for checkpoint in ('N1', 'N2'):
        for name in PART_A_CAPTURE_FIELDS:
            with pytest.raises(
                ValueError, match='part a capture fields required only for part a'
            ):
                capture(checkpoint, **dict(unset, **{name: valid[name]}))
    # PART_A without the whole set refuses, whichever field is missing.
    with pytest.raises(ValueError, match='part a capture fields required'):
        capture('PART_A', **unset)
    for name in PART_A_CAPTURE_FIELDS:
        partial = dict(valid, **{name: None})
        with pytest.raises(ValueError, match='part a capture fields required'):
            capture('PART_A', **partial)
    # Both digests must be canonical lowercase SHA-256 hex.
    for name in ('initial_prefix_sha256', 'final_sha256'):
        for bad in ('0' * 63, 'A' * 64, 'prefix', 64):
            with pytest.raises(ValueError, match='canonical SHA256 required'):
                capture('PART_A', **dict(valid, **{name: bad}))
    # Both panel counts must be exact positive integers.
    for name in ('initial_panels', 'final_panels'):
        for bad in (0, -2, True, 2.0, '4'):
            with pytest.raises(ValueError, match='bounded exact integer required'):
                capture('PART_A', **dict(valid, **{name: bad}))
    # final_panels never falls below initial_panels.
    with pytest.raises(ValueError, match='part a panel counts differ'):
        capture(
            'PART_A',
            initial_prefix_sha256=valid['initial_prefix_sha256'],
            final_sha256=valid['final_sha256'],
            initial_panels=4,
            final_panels=2,
            expansion_required=False,
        )
    # The expansion fact must follow the panel counts, both ways.
    for initial, final, fact in ((2, 4, False), (3, 3, True)):
        with pytest.raises(ValueError, match='part a expansion fact differs'):
            capture(
                'PART_A',
                initial_prefix_sha256=valid['initial_prefix_sha256'],
                final_sha256=valid['final_sha256'],
                initial_panels=initial,
                final_panels=final,
                expansion_required=fact,
            )
