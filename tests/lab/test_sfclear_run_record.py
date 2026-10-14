"""Card E chronology/publication acceptance; only disposable repositories."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

SOURCE = Path(__file__).resolve().parents[2] / 'lab/analysis/c1/sfclear_2026-10/run_record.py'


@pytest.fixture
def r():
    assert SOURCE.exists(), 'E chronology implementation absent'
    spec = importlib.util.spec_from_file_location('sfclear_run_record', SOURCE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / 'repo'
    root.mkdir()
    git(root, 'init')
    git(root, 'config', 'user.email', 'synthetic@example.invalid')
    git(root, 'config', 'user.name', 'Synthetic')
    git(root, 'config', 'core.hooksPath', str(tmp_path / 'no-hooks'))
    (root / 'frozen').write_text('frozen\n')
    (root / 'code').write_text('source\n')
    (root / 'evidence').write_text('')
    git(root, 'add', '.')
    git(root, 'commit', '-m', 'synthetic freeze')
    return root, git(root, 'rev-parse', 'HEAD')


def begin(r, repo, tmp_path, **changes):
    root, freeze = repo
    fg = tmp_path / 'fg.json'
    fg.write_text('{"status":"PASS"}')
    args = dict(repo=root, private_root=tmp_path / 'sfclear2-run-20260101T000000Z', freeze=freeze,
                frozen_paths=('frozen',), fg_path=fg, fg_sha256=sha(fg.read_bytes()))
    args.update(changes)
    return r.begin(**args)


def outputs(r, receipt):
    root = receipt.private_root
    (root / 'cells.json').write_text('{"synthetic":true}')
    r.seal_outputs(receipt, ('cells.json',))
    return r.finish(receipt, required=('cells.json',))


def test_e1_dirty_head_refuses(r, repo, tmp_path):
    (repo[0] / 'code').write_text('dirty')
    with pytest.raises(r.Refusal):
        begin(r, repo, tmp_path)
    assert not (tmp_path / 'sfclear2-run-20260101T000000Z').exists()


@pytest.mark.parametrize('committed', [False, True])
def test_e2_source_change_invalidates_completion(r, repo, tmp_path, committed):
    receipt = begin(r, repo, tmp_path)
    (repo[0] / 'code').write_text('changed')
    if committed:
        git(repo[0], 'add', 'code')
        git(repo[0], 'commit', '-m', 'change')
    with pytest.raises(r.Refusal):
        outputs(r, receipt)


def test_e3_frozen_change_refuses(r, repo, tmp_path):
    (repo[0] / 'frozen').write_text('changed')
    git(repo[0], 'add', 'frozen')
    git(repo[0], 'commit', '-m', 'change')
    with pytest.raises(r.Refusal):
        begin(r, repo, tmp_path)


def test_e3_unrelated_freeze_refuses(r, repo, tmp_path):
    git(repo[0], 'checkout', '--orphan', 'unrelated')
    git(repo[0], 'commit', '-m', 'unrelated')
    with pytest.raises(r.Refusal):
        begin(r, repo, tmp_path)


@pytest.mark.parametrize('status', ['FAIL', None])
def test_e4_fg_refuses_before_driver(r, repo, tmp_path, status):
    fg = tmp_path / 'bad-fg'
    fg.write_text(json.dumps({'status': status}))
    with pytest.raises(r.Refusal):
        begin(r, repo, tmp_path, fg_path=fg, fg_sha256=sha(fg.read_bytes()))
    assert not (tmp_path / 'sfclear2-run-20260101T000000Z').exists()


@pytest.mark.parametrize('other', [False, True])
def test_e5_any_git_tree_refuses(r, repo, tmp_path, other):
    root = repo[0]
    if other:
        root = tmp_path / 'other'
        root.mkdir()
        git(root, 'init')
    with pytest.raises(r.Refusal):
        begin(r, repo, tmp_path, private_root=root / 'outputs')


@pytest.mark.parametrize('damage', ['nonce', 'output', 'manifest', 'escape'])
def test_e6_manifest_integrity(r, repo, tmp_path, damage):
    receipt = begin(r, repo, tmp_path)
    outputs(r, receipt)
    root = receipt.private_root
    if damage == 'nonce':
        (root / 'nonce').unlink()
    elif damage == 'output':
        (root / 'cells.json').unlink()
    elif damage == 'manifest':
        (root / 'cells.json').write_text('changed')
    else:
        with (root / 'SHA256SUMS').open('a') as stream:
            stream.write('0' * 64 + '  ../outside\n')
    with pytest.raises(r.Refusal):
        r.finish(receipt, required=('cells.json',))


@pytest.mark.parametrize('field,value', [('extra', 123), ('run_head', 'abc'),
                                          ('started_utc', '2026-10-14T12:00:00')])
def test_e7_closed_public_record(r, repo, tmp_path, field, value):
    candidate = outputs(r, begin(r, repo, tmp_path))
    record = dict(candidate.record, **{field: value})
    with pytest.raises(r.Refusal):
        r.validate_public_record(record)


def test_e8_paired_publication_and_no_overwrite(r, repo, tmp_path):
    candidate = outputs(r, begin(r, repo, tmp_path))
    r.publish(candidate, repo=repo[0], record_path='records/run.json', evidence_path='evidence')
    assert set(git(repo[0], 'diff', '--cached', '--name-only').splitlines()) == {'evidence', 'records/run.json'}
    assert (repo[0] / 'evidence').read_text() == candidate.row + '\n'
    assert set(json.loads((repo[0] / 'records/run.json').read_text())) == {
        'run_head', 'started_utc', 'private_sha256sums_sha256'}
    with pytest.raises(r.Refusal):
        r.publish(candidate, repo=repo[0], record_path='records/run.json', evidence_path='evidence')


@pytest.mark.parametrize('remaining', ['record', 'row'])
def test_e8_half_publication_is_unusable_and_recoverable(r, repo, tmp_path, remaining):
    candidate = outputs(r, begin(r, repo, tmp_path))
    r.publish(candidate, repo=repo[0], record_path='records/run.json', evidence_path='evidence')
    git(repo[0], 'reset', '--mixed', 'HEAD')
    if remaining == 'record':
        (repo[0] / 'evidence').write_text('')
    else:
        (repo[0] / 'records/run.json').unlink()
    assert not r.publication_complete(candidate, repo[0], 'records/run.json', 'evidence')
    r.recover_publication(candidate, repo[0], 'records/run.json', 'evidence')
    assert git(repo[0], 'status', '--porcelain') == ''
    r.publish(candidate, repo=repo[0], record_path='records/run.json', evidence_path='evidence')
    assert r.publication_complete(candidate, repo[0], 'records/run.json', 'evidence')


def test_e15_candidate_is_public_safe(r, repo, tmp_path, capsys):
    candidate = outputs(r, begin(r, repo, tmp_path))
    assert set(candidate.record) == {'run_head', 'started_utc', 'private_sha256sums_sha256'}
    assert candidate.row.endswith('/SHA256SUMS')
    assert str(tmp_path) not in candidate.row
    assert capsys.readouterr() == ('', '')


def test_execute_uses_two_processes_and_seals_required_outputs(r,repo,tmp_path):
    # Exercise the wrapper with explicit child scripts; scoring itself is covered
    # by the separate artifact-to-verdict tests and its real subprocess CLI.
    launcher=repo[0]/'scripts/fp.py'
    launcher.parent.mkdir()
    launcher.write_text('import subprocess,sys\nraise SystemExit(subprocess.call([sys.executable,*sys.argv[2:]]))\n')
    git(repo[0],'add','scripts/fp.py');git(repo[0],'commit','-m','synthetic launcher')
    driver=tmp_path/'driver.py'
    driver.write_text('import pathlib,sys\np=pathlib.Path(sys.argv[1]);(p/"route.json").write_text("{}")\n(p/"port_state.json").write_text("{}")\n')
    scorer=tmp_path/'scorer.py'
    scorer.write_text('import pathlib,sys\np=pathlib.Path(sys.argv[1]);assert (p/"route.json").exists()\n(p/"cells.json").write_text("{}")\n(p/"residuals.json").write_text("{}")\n')
    receipt=begin(r,(repo[0],repo[1]),tmp_path)
    candidate=r.execute_processes(receipt,
        replay_script=driver,replay_sha256=sha(driver.read_bytes()),replay_args=[str(receipt.private_root)],
        scoring_script=scorer,scoring_sha256=sha(scorer.read_bytes()),scoring_args=[str(receipt.private_root)],
        required=('route.json','port_state.json','cells.json','residuals.json'))
    provenance=json.loads((receipt.private_root/'provenance.json').read_bytes())
    assert provenance['driver']['sha256']==sha(driver.read_bytes())
    assert provenance['fg']['sha256']==receipt.fg_sha256
    assert 'provenance.json' in (receipt.private_root/'INPUT_SHA256SUMS').read_text()
    assert candidate.record['run_head']==git(repo[0],'rev-parse','HEAD')
    manifest=(receipt.private_root/'SHA256SUMS').read_text()
    assert all(name in manifest for name in ('nonce','route.json','port_state.json','cells.json','residuals.json'))


def test_e8_collision_row_cannot_be_reused(r,repo,tmp_path):
    candidate=outputs(r,begin(r,repo,tmp_path))
    (repo[0]/'evidence').write_text('f'*64+'  '+candidate.row.split('  ')[1]+'\n')
    git(repo[0],'add','evidence');git(repo[0],'commit','-m','collision')
    with pytest.raises(r.Refusal):
        r.publish(candidate,repo=repo[0],record_path='records/new.json',evidence_path='evidence')
    assert not (repo[0]/'records/new.json').exists()


def test_publication_row_names_actual_private_directory(r,repo,tmp_path):
    receipt=begin(r,repo,tmp_path)
    candidate=outputs(r,receipt)
    assert candidate.row.endswith('/'+receipt.private_root.name+'/SHA256SUMS')


def test_publication_pair_must_be_staged_together(r,repo,tmp_path):
    candidate=outputs(r,begin(r,repo,tmp_path))
    r.publish(candidate,repo=repo[0],record_path='records/run.json',evidence_path='evidence')
    git(repo[0],'reset','HEAD','--','evidence')
    assert not r.publication_complete(candidate,repo[0],'records/run.json','evidence')


def test_freeze_provenance_from_public_git_objects(r):
    # Read public Git blobs only; this does not open the pinned private artifact.
    pins=r.freeze_bindings(SOURCE.parents[4])
    assert pins['freeze']=='91c2754e6373f39ed8ae2f522854fed5333568213157d23d33bb31ad7b1e5425'
    assert pins['calculator']=='2333844dd2a9342239812baa38a119b55f4b8a65841165740a9a39633f2297bf'


def test_job_cannot_record_another_checkout(r,repo,tmp_path):
    job=dict.fromkeys(('repo','private_root','fg','driver','inputs','calculator','panels'))
    job['repo']=str(repo[0])
    with pytest.raises(r.Refusal,match='recorded checkout'):
        r.run_job(job)


RUN_MUTANTS = {
    'M-E1': [('    _clean(repo)\n', '    pass\n')],
    'M-E3': [(" or strict_object(fg_raw).get('status') != 'PASS'", '')],
    'M-E4': [("+ candidate.row.encode() + b'\\n'", "+ b''"),
             ('if not publication_complete(candidate, root, record_path, evidence_path):', 'if False:')],
    'M-E7': [('    return Candidate(record, row, receipt.private_root)',
              "    record['e0']=123\n    return Candidate(record, row, receipt.private_root)")],
}


@pytest.mark.parametrize('name', RUN_MUTANTS)
def test_named_run_mutant_is_killed(name,r,repo,tmp_path):
    import types
    source=SOURCE.read_text()
    for old,new in RUN_MUTANTS[name]:
        assert source.count(old)==1, (name,old)
        source=source.replace(old,new)
    mutant=types.ModuleType('sfclear_run_mutant')
    mutant.__file__=str(SOURCE)
    sys.modules[mutant.__name__]=mutant
    exec(compile(source,str(SOURCE),'exec'),mutant.__dict__)
    # Only an assertion failure (including pytest DID NOT RAISE) kills a mutant.
    # An unrelated runtime exception is a test failure, not a mutation kill.
    with pytest.raises((AssertionError,pytest.fail.Exception)):
        if name=='M-E1':
            test_e1_dirty_head_refuses(mutant,repo,tmp_path)
        elif name=='M-E3':
            test_e4_fg_refuses_before_driver(mutant,repo,tmp_path,'FAIL')
        elif name=='M-E4':
            test_e8_paired_publication_and_no_overwrite(mutant,repo,tmp_path)
        else:
            candidate=outputs(mutant,begin(mutant,repo,tmp_path))
            assert set(candidate.record)=={'run_head','started_utc','private_sha256sums_sha256'}
