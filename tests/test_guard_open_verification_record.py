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


def docker_record(root, name, **fields):
    """Write a Docker verification record (`.cache/fp-docker-verification/<name>`)."""
    folder = root / guard.DOCKER_RECORDS_DIR / name
    folder.mkdir(parents=True)
    (folder / 'record.json').write_text(json.dumps(fields), encoding='utf-8')
    return folder


def test_running_docker_record_denies_and_names_the_record(tmp_path):
    """2026-09-23 card 2 (B1): Docker verification records lock the tree too."""
    root = checkout(tmp_path)
    docker_record(root, '20260920T175741Z-dkr', status='running',
                  started_at=(NOW - timedelta(minutes=5)).isoformat())
    permission, _, user = guard.decide(str(root / 'docs' / 'x.md'), now=NOW)
    assert permission == 'deny' and '20260920T175741Z-dkr' in user


@pytest.mark.parametrize('fields,locked', [
    (dict(status='not_started', before={'fingerprint': 'f'}, finished_at=None), True),
    (dict(status='not_started', before=None, finished_at=None), False),
    (dict(status='not_started', before={'fingerprint': 'f'},
          finished_at='2026-09-20T17:59:00+00:00'), False),
    (dict(status='failed', before={'fingerprint': 'f'}, finished_at=None), False),
])
def test_measured_window_opens_at_begin(tmp_path, fields, locked):
    """2026-09-23 card 2 (B2): `begin()` measured the tree, `execute()` has not run yet."""
    root = checkout(tmp_path)
    folder = root / guard.RECORDS_DIR / 'r'
    folder.mkdir(parents=True)
    data = dict(fields, started_at=(NOW - timedelta(minutes=1)).isoformat())
    (folder / 'record.json').write_text(json.dumps(data), encoding='utf-8')
    assert (guard.decide(str(root / 'docs' / 'x.md'), now=NOW)[0] == 'deny') is locked


def test_non_object_record_json_fails_open(tmp_path):
    """A record.json that parses but is not an object is skipped, never a crash."""
    root = checkout(tmp_path)
    folder = root / guard.RECORDS_DIR / 'list'
    folder.mkdir(parents=True)
    (folder / 'record.json').write_text('["running"]', encoding='utf-8')
    assert guard.decide(str(root / 'docs' / 'x.md'), now=NOW)[0] == 'allow'


def target_payload(field, doc, other):
    """The `tool_input` a Write/Edit, MultiEdit or NotebookEdit call carries for `doc`."""
    return {
        'file_path': {'file_path': doc},
        'notebook_path': {'notebook_path': doc},
        'edits': {'edits': [{'old_string': 'x'}, {'file_path': doc}]},
        'notebook_path_beside_file_path': {'file_path': other, 'notebook_path': doc},
        'no_target': {},
        'edit_without_target': {'edits': [{'old_string': 'x'}]},
    }[field]


@pytest.mark.parametrize('field,denied', [
    ('file_path', True), ('notebook_path', True), ('edits', True),
    ('notebook_path_beside_file_path', True), ('no_target', False), ('edit_without_target', False),
])
def test_main_reads_every_target_field(tmp_path, monkeypatch, capsys, field, denied):
    """2026-09-23 card 2 (B3): `main()` checks Write/Edit `file_path`, MultiEdit
    `edits[].file_path` and NotebookEdit `notebook_path`; a payload without a
    target emits nothing."""
    root = checkout(tmp_path)
    record(root, 'r', 'running', datetime.now(timezone.utc) - timedelta(minutes=1))
    tool_input = target_payload(field, str(root / 'docs' / 'n.ipynb'), str(tmp_path / 'draft.md'))
    payload = json.dumps({'tool_input': tool_input})
    monkeypatch.setattr('sys.stdin', __import__('io').StringIO(payload))
    assert guard.main() == 0
    out = capsys.readouterr().out
    if denied:
        assert json.loads(out)['hookSpecificOutput']['permissionDecision'] == 'deny'
    else:
        assert out.strip() == ''


@pytest.mark.parametrize('shape,denied', [
    ('edits_not_objects', True), ('edits_not_a_list', True), ('tool_input_a_list', False),
    ('payload_a_list', False),
])
def test_main_tolerates_malformed_payloads(tmp_path, monkeypatch, capsys, shape, denied):
    """Round 3 P3: malformed parts are skipped, not fatal; a valid file_path is still judged."""
    root = checkout(tmp_path)
    record(root, 'r', 'running', datetime.now(timezone.utc) - timedelta(minutes=1))
    target = str(root / 'src' / 'x.py')
    payload = {
        'edits_not_objects': {'tool_input': {'file_path': target, 'edits': ['x', 3]}},
        'edits_not_a_list': {'tool_input': {'file_path': target, 'edits': 'x'}},
        'tool_input_a_list': {'tool_input': [target]},
        'payload_a_list': [{'tool_input': {'file_path': target}}],
    }[shape]
    monkeypatch.setattr('sys.stdin', __import__('io').StringIO(json.dumps(payload)))
    assert guard.main() == 0
    out = capsys.readouterr().out
    if denied:
        assert json.loads(out)['hookSpecificOutput']['permissionDecision'] == 'deny'
    else:
        assert out.strip() == ''


def test_main_emits_nothing_when_it_does_not_deny(tmp_path, monkeypatch, capsys):
    """2026-09-23: an allowed write produces no output, so the hook never
    approves anything on the operator's behalf (D15 of the guard hardening)."""
    root = checkout(tmp_path)
    payload = json.dumps(dict(tool_input=dict(file_path=str(root / 'docs' / 'y.md'))))
    monkeypatch.setattr('sys.stdin', __import__('io').StringIO(payload))
    assert guard.main() == 0
    assert capsys.readouterr().out.strip() == ''
