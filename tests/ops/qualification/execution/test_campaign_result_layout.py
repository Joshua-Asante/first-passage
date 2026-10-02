"""H9 DB custody integration: preserve accepted v9 bytes, refuse false mounts."""
import sqlite3
from types import SimpleNamespace

import pytest
import test_campaign_n1 as n1
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.campaign_result import ResultStore, RESULT_SCHEMA, SEAL_SCHEMA
from c1_rail.qualification.execution.store import ExecutionStore


def accepted_v9(tmp_path, monkeypatch):
    instance, _ = n1.campaign(tmp_path, monkeypatch)
    campaigns = CampaignStore(instance.store)
    with instance.store.transaction() as connection:
        campaigns._ensure_checkpoint_layout(connection)
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 9
    return instance, campaigns


def contents(connection):
    names = [row[0] for row in connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    return {name: sorted([tuple(row) for row in connection.execute('SELECT * FROM ' + name)], key=repr)
            for name in names}


def test_v9_mount_preserves_every_existing_row_and_reopens(tmp_path, monkeypatch):
    instance, campaigns = accepted_v9(tmp_path, monkeypatch)
    with instance.store.transaction() as connection:
        before = contents(connection)
        ResultStore(campaigns)._ensure_result_layout(connection)
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 10
        after = contents(connection)
        assert set(after) - set(before) == {'full_campaign_result_intents', 'full_campaign_seal_intents'}
        assert {name: after[name] for name in before} == before
    reopened = ExecutionStore(instance.store.path)
    context = CampaignStore(reopened).context(instance.attempt, instance.release, instance.keys(), now=n1.NOW)
    assert context.attempt_id == instance.attempt
    with reopened.transaction() as connection:
        statements = []
        connection.set_trace_callback(statements.append)
        changes = connection.total_changes
        ResultStore(CampaignStore(reopened))._ensure_result_layout(connection)
        assert connection.total_changes == changes
        assert not any(sql.lstrip().split()[0].upper() in {'INSERT','UPDATE','DELETE','CREATE','ALTER','DROP'} for sql in statements)
        assert contents(connection) == after


@pytest.mark.parametrize('false_mount', ['result_table', 'malformed_checkpoint', 'missing_seal', 'missing_result'])
def test_false_mount_refuses_without_repairing_or_rewriting(tmp_path, monkeypatch, false_mount):
    instance, campaigns = accepted_v9(tmp_path, monkeypatch)
    with instance.store.transaction() as connection:
        if false_mount == 'result_table':
            connection.execute('CREATE TABLE full_campaign_result_intents (attempt_id TEXT)')
        elif false_mount == 'malformed_checkpoint':
            connection.execute('ALTER TABLE full_campaign_checkpoint_intents ADD COLUMN unexpected TEXT')
        else:
            schema = RESULT_SCHEMA if false_mount == 'missing_seal' else SEAL_SCHEMA
            for statement in schema.split(';'):
                if statement.strip():
                    connection.execute(statement)
            connection.execute('PRAGMA user_version=10')
        before = contents(connection)
        with pytest.raises(ValueError, match='layout'):
            ResultStore(campaigns)._ensure_result_layout(connection)
        assert contents(connection) == before


@pytest.mark.parametrize('version', [0, 7, 8, 11])
def test_result_mount_refuses_unknown_or_non_predecessor_versions(version):
    connection = sqlite3.connect(':memory:')
    connection.execute('PRAGMA user_version=' + str(version))
    campaigns = SimpleNamespace(store=SimpleNamespace(validate_layout=ExecutionStore.validate_layout))
    try:
        with pytest.raises(ValueError, match='database v9 or v10'):
            ResultStore(campaigns)._ensure_result_layout(connection)
        assert not connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    finally:
        connection.close()

def test_retained_s5_journal_migrates_preserving_all_rows_and_reopens(tmp_path):
    """Run36766144433 archive#853; original compressed and decompressed owner pins.

    Optional private input stays outside Git. A selected local run supplies the
    exact retained path explicitly; absence is a disclosed skip elsewhere.
    """
    import gzip
    import hashlib
    import os
    from pathlib import Path
    import shutil
    source_name = os.environ.get('FP_H9_S5_JOURNAL_GZIP')
    if not source_name:
        pytest.skip('retained private S5 journal not supplied')
    source = Path(source_name)
    compressed_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert compressed_digest == '7ace9a9d11fbd0e79bdde119739597b9b0cf9119f269c24cba32ade226c84ef6'
    copy = tmp_path / 'journal.sqlite'
    with gzip.open(source, 'rb') as original, copy.open('xb') as output:
        shutil.copyfileobj(original, output)
    assert hashlib.sha256(copy.read_bytes()).hexdigest() == 'efec03b10f30f74ec8bd29a26792b5864fc99313c69f3b51fda3a305b1f1be86'
    store = ExecutionStore(copy)
    with store.transaction() as connection:
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 9
        before = contents(connection)
        ResultStore(CampaignStore(store))._ensure_result_layout(connection)
        assert connection.execute('PRAGMA user_version').fetchone()[0] == 10
        after = contents(connection)
        assert set(after) - set(before) == {'full_campaign_result_intents','full_campaign_seal_intents'}
        assert {name:after[name] for name in before} == before
    reopened = ExecutionStore(copy)
    with reopened.transaction() as connection:
        assert contents(connection) == after
    assert hashlib.sha256(source.read_bytes()).hexdigest() == compressed_digest
    print('retained S5 journal: original pins verified; all v9 rows preserved; v10 reopened')
