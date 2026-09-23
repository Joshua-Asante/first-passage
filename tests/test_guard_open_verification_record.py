"""The open-record write guard refuses tree writes only while a live record is running."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import guard_open_verification_record as guard  # noqa: E402

NOW = datetime(2026, 9, 20, 18, 0, tzinfo=timezone.utc)


def checkout(tmp_path):
    root = tmp_path / 'repo'
    (root / '.git').mkdir(parents=True)
    (root / 'docs').mkdir()
    return root


def record(root, name, status, started):
    folder = root / guard.RECORDS_DIR / name
    folder.mkdir(parents=True)
    (folder / 'record.json').write_text(json.dumps(dict(status=status, started_at=started.isoformat())), encoding='utf-8')
    return folder


def test_no_records_allows(tmp_path):
    root = checkout(tmp_path)
    assert guard.decide(str(root / 'docs' / 'x.md'), now=NOW)[0] == 'allow'


def test_running_record_denies_writes_into_the_measured_tree(tmp_path):
    root = checkout(tmp_path)
    record(root, '20260920T175741Z-abc', 'running', NOW - timedelta(minutes=10))
    permission, agent, user = guard.decide(str(root / 'docs' / 'x.md'), now=NOW)
    assert permission == 'deny'
    assert '20260920T175741Z-abc' in user and 'scratchpad' in agent


@pytest.mark.parametrize('status', ['completed', 'failed', 'interrupted', 'not_started'])
def test_closed_records_allow(tmp_path, status):
    root = checkout(tmp_path)
    record(root, 'r', status, NOW - timedelta(minutes=10))
    assert guard.decide(str(root / 'docs' / 'x.md'), now=NOW)[0] == 'allow'


def test_abandoned_running_record_does_not_lock_the_tree(tmp_path):
    root = checkout(tmp_path)
    record(root, 'r', 'running', NOW - timedelta(seconds=guard.STALE_AFTER_SECONDS + 1))
    assert guard.decide(str(root / 'docs' / 'x.md'), now=NOW)[0] == 'allow'


def test_writes_under_cache_and_outside_the_checkout_are_exempt(tmp_path):
    root = checkout(tmp_path)
    record(root, 'r', 'running', NOW - timedelta(minutes=1))
    assert guard.decide(str(root / '.cache' / 'notes.md'), now=NOW)[0] == 'allow'
    assert guard.decide(str(tmp_path / 'elsewhere' / 'draft.md'), now=NOW)[0] == 'allow'


def test_relative_and_malformed_targets_fail_open(tmp_path):
    assert guard.decide('docs/x.md', now=NOW)[0] == 'allow'
    assert guard.decide('', now=NOW)[0] == 'allow'
    root = checkout(tmp_path)
    folder = root / guard.RECORDS_DIR / 'bad'
    folder.mkdir(parents=True)
    (folder / 'record.json').write_text('{not json', encoding='utf-8')
    assert guard.decide(str(root / 'docs' / 'x.md'), now=NOW)[0] == 'allow'


def test_main_emits_claude_code_pretooluse_shape(tmp_path, monkeypatch, capsys):
    root = checkout(tmp_path)
    record(root, 'r', 'running', datetime.now(timezone.utc) - timedelta(minutes=1))
    payload = json.dumps(dict(tool_input=dict(file_path=str(root / 'docs' / 'x.md'))))
    monkeypatch.setattr('sys.stdin', __import__('io').StringIO(payload))
    assert guard.main() == 0
    out = json.loads(capsys.readouterr().out)['hookSpecificOutput']
    assert out['hookEventName'] == 'PreToolUse' and out['permissionDecision'] == 'deny'
    assert 'permissionDecisionReason' in out and 'additionalContext' in out


def test_main_emits_nothing_when_it_does_not_deny(tmp_path, monkeypatch, capsys):
    """2026-09-23: an allowed write produces no output, so the hook never
    approves anything on the operator's behalf (D15 of the guard hardening)."""
    root = checkout(tmp_path)
    payload = json.dumps(dict(tool_input=dict(file_path=str(root / 'docs' / 'y.md'))))
    monkeypatch.setattr('sys.stdin', __import__('io').StringIO(payload))
    assert guard.main() == 0
    assert capsys.readouterr().out.strip() == ''
