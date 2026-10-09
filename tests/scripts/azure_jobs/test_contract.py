import hashlib
import json
from pathlib import Path
import pytest
from scripts.azure_jobs import contract


def valid():
    return dict(job_id='qualification-742', commit='a' * 40, command=['scripts/fp.py', '--workers', '8', 'python', '-m', 'pytest', 'tests/ops/qualification', '-q'], environment='operations', max_wall_seconds=28800, expected_outputs=['.cache/fp-verification'], authority='Joshua 2026-10-09 public qualification acceptance', private_inputs=[], private_ruling=None)


@pytest.mark.parametrize('key,value', [('commit', 'main'), ('commit', 'a'*39), ('environment', 'system'), ('max_wall_seconds', 0), ('max_wall_seconds', True), ('expected_outputs', ['../secret']), ('expected_outputs', ['.env']), ('expected_outputs', ['C:/secret']), ('command', 'echo hello'), ('authority', ''), ('private_inputs', ['port.py']), ('job_id', '../bad')])
def test_bad_spec_rejected(key, value):
    spec = valid(); spec[key] = value
    with pytest.raises(ValueError):
        contract.validate(spec)


def test_private_ruling_does_not_enable_unimplemented_transfer():
    spec = valid(); spec.update(private_inputs=['port.py'], private_ruling='T00 only')
    with pytest.raises(ValueError, match='private'):
        contract.validate(spec)


def test_valid_public_job():
    assert contract.validate(valid())['environment'] == 'operations'


@pytest.mark.parametrize('name', ['.GIT/config', 'out/.gIt/config', '.ENV', 'out/.EnV.local'])
def test_mixed_case_private_components_rejected(name):
    spec = valid(); spec['expected_outputs'] = [name]
    with pytest.raises(ValueError, match='forbidden'):
        contract.validate(spec)


@pytest.mark.parametrize('name', ['.GIT/config', '.gIt/config', '.ENV', '.EnV.local'])
def test_collection_rejects_synthetic_windows_aliases_before_hashing(tmp_path, monkeypatch, name):
    # Synthetic names only. On Windows these spellings alias the excluded names;
    # Linux still exercises the inventory traversal and validation boundary.
    alias = tmp_path / 'out' / name
    alias.parent.mkdir(parents=True)
    alias.write_text('synthetic fixture')
    monkeypatch.setattr(contract, 'sha256', lambda path: pytest.fail('read forbidden artifact'))
    with pytest.raises(ValueError, match='forbidden'):
        contract.inventory(tmp_path, ['out'])


def test_allowed_output_spelling_is_preserved(tmp_path):
    (tmp_path / 'Result.TXT').write_text('synthetic result')
    assert list(contract.inventory(tmp_path, ['Result.TXT'])) == ['Result.TXT']


def test_artifact_inventory_excludes_env_and_refuses_links(tmp_path):
    (tmp_path / 'out').mkdir()
    (tmp_path / 'out/a.txt').write_text('hello')
    (tmp_path / 'out/.env').write_text('secret')
    with pytest.raises(ValueError, match='forbidden'):
        contract.inventory(tmp_path, ['out'])


def test_complete_and_corrupt_results(tmp_path):
    (tmp_path / 'answer').write_bytes(b'42')
    rows = contract.inventory(tmp_path, ['answer'])
    assert rows['answer']['sha256'] == hashlib.sha256(b'42').hexdigest()
    contract.verify_inventory(tmp_path, rows)
    (tmp_path / 'answer').write_bytes(b'43')
    with pytest.raises(ValueError, match='hash'):
        contract.verify_inventory(tmp_path, rows)


@pytest.mark.parametrize('delta', [{'status':'running'}, {'exit_code':1}, {'source_stable':False}, {'capture_complete':False}, {'report_errors':['missing']}, {'verification_exit_code':3}])
def test_launcher_failure_never_verified(delta):
    record = dict(status='completed',exit_code=0,verification_exit_code=0,source_stable=True,capture_complete=True,report_errors=[])
    assert contract.verified(record)
    record.update(delta)
    assert not contract.verified(record)
