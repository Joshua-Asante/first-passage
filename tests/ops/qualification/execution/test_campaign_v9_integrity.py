"""C2 repair R2b: S4 moves checkpointed journals to v9, so every v8 integrity
walk and the VOID budget event must also run at v9."""

import json
import sqlite3

import pytest
from test_campaign_n1 import NOW, snap, store
from test_campaign_n2 import committed_n1
from c1_rail.qualification.contract import canonical_json_bytes as encoded
from c1_rail.qualification.execution.campaign_store import CampaignStore
from c1_rail.qualification.execution.store import ExecutionStore

STAGED = 'full_campaign_checkpoint_staged'
EVENTS = 'full_campaign_budget_events'


def committed_v9(tmp_path, monkeypatch):
    """A genuine checkpointed S4 journal with N1 custody: the real committed N1
    prefix (reconstruction, signatures, committed receipt, N2_READY) plus one
    staged custody artifact row under (attempt, checkpoint)."""
    instance = committed_n1(tmp_path, monkeypatch)
    store(instance).stage_checkpoint_artifact(
        instance.attempt, 'attempt_journal', b'staged-bytes'
    )
    with instance.store.transaction() as connection:
        version = connection.execute('PRAGMA user_version').fetchone()[0]
        staged = connection.execute(
            'SELECT checkpoint,role,body FROM ' + STAGED + ' WHERE attempt_id=?',
            (instance.attempt,),
        ).fetchall()
    assert version == 9, 'a checkpointed S4 journal must sit at user_version 9'
    assert staged and bytes(staged[0][2]) == b'staged-bytes'
    return instance


def event_kinds(instance):
    with instance.store.transaction() as connection:
        rows = connection.execute(
            'SELECT body FROM ' + EVENTS + ' WHERE attempt_id=? ORDER BY sequence',
            (instance.attempt,),
        ).fetchall()
    return [json.loads(bytes(row[0])) for row in rows]


def test_reopening_a_v9_journal_detects_corrupted_checkpoint_custody(tmp_path, monkeypatch):
    # Pre-change: no integrity walk ran at v9, so this corrupted staged custody
    # row reopened without any complaint.
    instance = committed_v9(tmp_path, monkeypatch)
    corrupt = sqlite3.connect(instance.store.path)
    try:
        corrupt.execute(
            'UPDATE ' + STAGED + ' SET body=? WHERE attempt_id=?', (b'\x00', instance.attempt)
        )
        corrupt.commit()
    finally:
        corrupt.close()
    with pytest.raises(ValueError, match='checkpoint staged artifact integrity differs'):
        ExecutionStore(instance.store.path)


def test_reopening_a_funded_v9_journal_is_clean(tmp_path, monkeypatch):
    # Pre-change (with only the v9 walk gate repaired) _budget_integrity raised
    # 'funding profile requires database v7' here, so no funded v9 journal reopened.
    instance = committed_v9(tmp_path, monkeypatch)
    reopened = CampaignStore(ExecutionStore(instance.store.path))
    assert json.loads(reopened.budget_snapshot(instance.attempt))['state'] == 'N2_READY'


def test_void_at_v9_records_the_budget_void_event(tmp_path, monkeypatch):
    # Pre-change: at v9 the validity flipped to VOID but the authority-bearing
    # budget 'VOID' event was never appended to the chain.
    instance = committed_v9(tmp_path, monkeypatch)
    campaigns = store(instance)
    before = snap(instance)
    assert before['validity'] == 'VALID'
    before_events = event_kinds(instance)
    cancel = encoded(
        {
            'schema': 'qualification_campaign_request/v2',
            'operation': 'VOID',
            'attempt_id': instance.attempt,
            'reason': 'stop',
            'operator_approval_bytes': 'eA==',
        }
    )
    campaigns.void(cancel, now=NOW)
    after = snap(instance)
    assert after['validity'] == 'VOID'
    with instance.store.transaction() as connection:
        row = connection.execute(
            'SELECT validity FROM full_campaigns WHERE attempt_id=?', (instance.attempt,)
        ).fetchone()
    assert row[0] == 'VOID'
    after_events = event_kinds(instance)
    assert [event['kind'] for event in after_events[:-1]] == [
        event['kind'] for event in before_events
    ]
    final = after_events[-1]
    assert final['kind'] == 'VOID' and final['authority'] is True
    assert after['authority_revision'] > before['authority_revision']
