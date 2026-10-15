"""Q-SFCLEAR-3 chronology and paired publication; no default private paths.

The coordinator supplies the reviewed private replay driver. This module invokes
it through the checkout launcher in a separate process; it never imports ops.
Publication is a separate coordinator action, not an automatic consequence of a
score. Only a complete pair staged together is a publication candidate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import subprocess
import sys

from discovery.sfgrowth_acceptance import strict_object

FREEZE2 = '83867f0d362931c2a516a62b990bb1c209372527'
FREEZE = '15bea250fc8ee9a57b59735c9e8be685c4ddbf22'
FROZEN_PATHS = ('docs/briefs/pre-registration/Q-SFCLEAR-3-verdict-preregistration.md',
                'docs/briefs/pre-registration/Q-SFCLEAR-2-verdict-preregistration.md',
                'lab/analysis/c1/sfclear_2026-10/schedule',
                'lab/analysis/c1/sfclear_2026-10/build_historical_schedule.py')
PUBLIC_KEYS = {'run_head', 'started_utc', 'private_sha256sums_sha256'}


class Refusal(ValueError):
    """Public-safe failure; never includes captured process output or paths."""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _hex(value, length):
    return type(value) is str and re.fullmatch('[0-9a-f]{%d}' % length, value) is not None


def _json(doc):
    return (json.dumps(doc, sort_keys=True, allow_nan=False) + '\n').encode()


def _git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    if result.returncode:
        raise Refusal('git verification failed')
    return result.stdout.decode('utf-8').strip()


def _clean(repo):
    if _git(repo, 'status', '--porcelain', '--untracked-files=all'):
        raise Refusal('source must be clean')


def outside_git(path):
    path = Path(path).resolve()
    for parent in (path, *path.parents):
        if (parent / '.git').exists():
            raise Refusal('output root must be outside every git work tree')
    return path


def _relative(name):
    if (type(name) is not str or '\\' in name or ':' in name or '\n' in name
            or '\r' in name or not name or name.startswith('/')):
        raise Refusal('invalid relative artifact name')
    parts = name.split('/')
    if any(part in ('', '.', '..') for part in parts):
        raise Refusal('invalid relative artifact name')
    return PurePosixPath(name)


def _within(root, name):
    candidate = root.joinpath(*_relative(name).parts)
    if not candidate.resolve().is_relative_to(root.resolve()) or candidate.is_symlink():
        raise Refusal('artifact escapes root')
    return candidate


def validate_public_record(doc):
    if type(doc) is not dict or set(doc) != PUBLIC_KEYS:
        raise Refusal('public record fields')
    if not _hex(doc['run_head'], 40) or not _hex(doc['private_sha256sums_sha256'], 64):
        raise Refusal('public record identity')
    try:
        stamp = datetime.fromisoformat(doc['started_utc'])
        if stamp.utcoffset() != timedelta(0):
            raise ValueError
    except (ValueError, TypeError):
        raise Refusal('public record UTC timestamp') from None
    return doc


@dataclass(frozen=True, repr=False)
class Receipt:
    repo: Path = field(repr=False)
    private_root: Path = field(repr=False)
    run_head: str
    started_utc: str
    freeze: str
    frozen_paths: tuple
    fg_path: Path = field(repr=False)
    fg_sha256: str


@dataclass(frozen=True, repr=False)
class Candidate:
    record: dict
    row: str
    private_root: Path = field(repr=False)


def begin(*, repo, private_root, fg_path, fg_sha256, freeze=FREEZE, frozen_paths=FROZEN_PATHS):
    repo = Path(repo).resolve()
    root = outside_git(private_root)
    _clean(repo)
    head = _git(repo, 'rev-parse', 'HEAD')
    if not _hex(head, 40) or not _hex(freeze, 40) or not frozen_paths:
        raise Refusal('invalid source identity')
    _git(repo, 'merge-base', '--is-ancestor', freeze, head)
    _git(repo, 'diff', '--quiet', freeze, head, '--', *frozen_paths)
    if freeze == FREEZE:
        _git(repo, 'diff', '--quiet', FREEZE2, head, '--', *FROZEN_PATHS[1:])
    try:
        fg_path = Path(fg_path).resolve()
        fg_raw = fg_path.read_bytes()
        if not _hex(fg_sha256, 64) or digest(fg_raw) != fg_sha256 or strict_object(fg_raw).get('status') != 'PASS':
            raise Refusal('FG PASS reference required')
    except (OSError, ValueError):
        raise Refusal('FG PASS reference required') from None
    started = datetime.now(timezone.utc).isoformat()
    try:
        root.mkdir(parents=True, exist_ok=False)
        (root / 'nonce').write_bytes(secrets.token_bytes(32))
    except OSError:
        raise Refusal('new private root required') from None
    return Receipt(repo, root, head, started, freeze, tuple(frozen_paths), fg_path, fg_sha256)


def unchanged(receipt):
    _clean(receipt.repo)
    if _git(receipt.repo, 'rev-parse', 'HEAD') != receipt.run_head:
        raise Refusal('run revision changed')
    _git(receipt.repo, 'diff', '--quiet', receipt.freeze, 'HEAD', '--', *receipt.frozen_paths)
    try:
        if digest(receipt.fg_path.read_bytes()) != receipt.fg_sha256:
            raise Refusal('FG reference changed')
    except OSError:
        raise Refusal('FG reference unavailable') from None


def run_process(receipt, script, args, *, expected_sha256):
    """Run a hash-bound driver via the launcher, without leaking its output."""
    unchanged(receipt)
    script = Path(script).resolve()
    try:
        if digest(script.read_bytes()) != expected_sha256:
            raise Refusal('driver identity mismatch')
        result = subprocess.run([sys.executable, '-I', str(receipt.repo / 'scripts/fp.py'),
                                 'python', str(script), *map(str, args)],
                                cwd=receipt.repo, capture_output=True)
        if result.returncode:
            raise Refusal('private process failed')
        if digest(script.read_bytes()) != expected_sha256:
            raise Refusal('driver changed')
    except OSError:
        raise Refusal('private process unavailable') from None
    unchanged(receipt)


def read_manifest(root, *, required=(), filename='SHA256SUMS'):
    root = outside_git(root)
    try:
        blob = _within(root, filename).read_bytes()
        rows = {}
        for line in blob.decode('utf-8').splitlines():
            match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
            if match is None:
                raise Refusal('manifest encoding')
            expected, name = match.groups()
            path = _within(root, name)
            if name in rows or name == filename or not path.is_file():
                raise Refusal('manifest inventory')
            if digest(path.read_bytes()) != expected:
                raise Refusal('manifest hash mismatch')
            rows[name] = expected
        if not {'nonce', *required} <= set(rows) or len((root / 'nonce').read_bytes()) < 16:
            raise Refusal('missing nonce or output')
    except (OSError, UnicodeError):
        raise Refusal('manifest unavailable') from None
    return blob, rows


def seal_outputs(receipt, names):
    unchanged(receipt)
    if len(set(names)) != len(names):
        raise Refusal('duplicate output')
    names = sorted({'nonce', *names})
    if 'SHA256SUMS' in names:
        raise Refusal('manifest cannot list itself')
    try:
        rows = [digest(_within(receipt.private_root, name).read_bytes()) + '  ' + name for name in names]
        with (receipt.private_root / 'SHA256SUMS').open('xb') as stream:
            stream.write(('\n'.join(rows) + '\n').encode())
    except OSError:
        raise Refusal('cannot seal outputs') from None


def finish(receipt, *, required):
    unchanged(receipt)
    blob, _ = read_manifest(receipt.private_root, required=required)
    record = validate_public_record(dict(run_head=receipt.run_head, started_utc=receipt.started_utc,
                                        private_sha256sums_sha256=digest(blob)))
    name = receipt.private_root.name
    if not re.fullmatch(r'sfclear2-run-[0-9TZ]+', name):
        raise Refusal('private directory must carry a run identifier')
    row = f'{digest(blob)}  t00-step3-console/{name}/SHA256SUMS'
    return Candidate(record, row, receipt.private_root)


def _publication(candidate, repo, record_path, evidence_path):
    validate_public_record(candidate.record)
    root = Path(repo).resolve()
    record = _within(root, record_path)
    evidence = _within(root, evidence_path)
    if record == evidence:
        raise Refusal('publication paths collide')
    if not re.fullmatch(r'[0-9a-f]{64}  t00-step3-console/sfclear2-run-[0-9TZ]+/SHA256SUMS', candidate.row):
        raise Refusal('publication row form')
    if (not candidate.row.endswith('/'+candidate.private_root.name+'/SHA256SUMS')
            or candidate.row.split('  ')[0] != candidate.record['private_sha256sums_sha256']):
        raise Refusal('publication identity mismatch')
    return root, record, evidence


def publication_complete(candidate, repo, record_path, evidence_path):
    _, record, evidence = _publication(candidate, repo, record_path, evidence_path)
    try:
        return (record.read_bytes() == _json(candidate.record)
                and evidence.read_text(encoding='utf-8').splitlines().count(candidate.row) == 1
                and _git_bytes(repo, 'show', ':'+record_path).replace(b'\r\n',b'\n') == _json(candidate.record)
                and _git_bytes(repo, 'show', ':'+evidence_path).decode().splitlines().count(candidate.row) == 1)
    except (OSError, Refusal):
        return False


def publish(candidate, *, repo, record_path, evidence_path):
    """Stage an exact pair; failures leave an explicitly recoverable pair/half-pair.

    A caller must use publication_complete before advertising a staged result.
    The initial clean-index requirement protects unrelated staged work.
    """
    root, record, evidence = _publication(candidate, repo, record_path, evidence_path)
    _clean(root)
    blob, _ = read_manifest(candidate.private_root)
    if digest(blob) != candidate.record['private_sha256sums_sha256']:
        raise Refusal('private manifest changed')
    if _git(root, 'rev-parse', 'HEAD') != candidate.record['run_head']:
        raise Refusal('publication revision differs')
    original = evidence.read_bytes() if evidence.exists() else b''
    name = candidate.row.split('  ')[1]
    if record.exists() or any(line.endswith('  '+name) for line in original.decode().splitlines()):
        raise Refusal('publication collision')
    record.parent.mkdir(parents=True, exist_ok=True)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    try:
        with record.open('xb') as stream:
            stream.write(_json(candidate.record))
        with evidence.open('wb') as stream:
            stream.write(original + (b'\n' if original and not original.endswith(b'\n') else b'')
                         + candidate.row.encode() + b'\n')
        _git(root, 'add', '--', record_path, evidence_path)
    except OSError:
        raise Refusal('publication interrupted; recover before reuse') from None
    if not publication_complete(candidate, root, record_path, evidence_path):
        raise Refusal('publication incomplete')


def recover_publication(candidate, repo, record_path, evidence_path):
    """Remove only this candidate's exact bytes/row; never overwrite other work."""
    root, record, evidence = _publication(candidate, repo, record_path, evidence_path)
    if record.exists() and record.read_bytes() != _json(candidate.record):
        raise Refusal('record collision during recovery')
    if _git(root, 'rev-parse', 'HEAD') != candidate.record['run_head']:
        raise Refusal('cannot recover after source commit')
    _git(root, 'reset', 'HEAD', '--', record_path, evidence_path)
    if record.exists():
        record.unlink()
    if evidence.exists():
        lines = evidence.read_bytes().splitlines(keepends=True)
        evidence.write_bytes(b''.join(line for line in lines if line.rstrip(b'\r\n') != candidate.row.encode()))


def _git_bytes(repo,*args):
    proc=subprocess.run(['git','-C',str(repo),*args],capture_output=True)
    if proc.returncode:
        raise Refusal('git object unavailable')
    return proc.stdout


def freeze_bindings(repo, freeze=FREEZE):
    """Q-SFCLEAR-3 hook 4 (I1–I5), from committed public objects only."""
    p=FROZEN_PATHS[0]
    study='lab/analysis/c1/sfclear_2026-10'
    evidence='docs/evidence/PRIVATE_EVIDENCE.sha256'
    audited=_git(repo,'rev-parse','HEAD')
    try:
        _git(repo,'merge-base','--is-ancestor',freeze,audited)
        _git(repo,'merge-base','--is-ancestor',FREEZE2,freeze)
        _git(repo,'diff','--quiet',FREEZE2,freeze,'--',*FROZEN_PATHS[1:])
        _git(repo,'diff','--quiet',freeze,audited,'--',*FROZEN_PATHS)
        frozen=_git_bytes(repo,'show',f'{freeze}:{p}')
        parent=_git_bytes(repo,'show',f'{freeze}^:{p}')
        lines=frozen.decode().splitlines()
        statuses=[line for line in lines if line.startswith('**Status:**')]
        if len(statuses)!=1 or not statuses[0].startswith('**Status:** `FROZEN'):
            raise Refusal('freeze status invalid')
        status=statuses[0]
        ratified=re.search(r'ratify Q-SFCLEAR-3 at ([0-9a-f]{40})',status)
        hashes=re.findall(r'\b[0-9a-f]{64}\b',status)
        if (ratified is None or not hashes or 'exposure attestation' not in status.lower()
                or any(marker not in status for marker in ('2026-10-11T23:39:57Z',
                    '(s1)','(s2)','(s3)','G1/G3','2026-10-12 coordinator',
                    '62d7ae196059b7d98fd814c7b07a911558e8e5891dd2a669170393583b6c671f'))):
            raise Refusal('freeze ratification or exposure missing')
        _git(repo,'merge-base','--is-ancestor',ratified[1],freeze+'^')
        if _git_bytes(repo,'show',f'{ratified[1]}:{p}')!=parent:
            raise Refusal('ratified text changed')
        without=lambda blob:[line for line in blob.splitlines() if not line.startswith(b'**Status:**')]
        if without(frozen)!=without(parent) or _git(repo,'diff','--numstat',freeze+'^',freeze,'--',p).split()[:2]!=['1','1']:
            raise Refusal('freeze changed more than status')
        history=_git(repo,'log','--format=%H','-G',r'^\*\*Status:\*\*.*FROZEN',audited,'--',p).splitlines()
        if not history or history[-1]!=freeze:
            raise Refusal('not first freeze')
        if set(_git(repo,'diff','--name-only',freeze+'^',freeze).splitlines())!={p,evidence}:
            raise Refusal('freeze changed unexpected paths')
        delta=_git(repo,'diff','--unified=0',freeze+'^',freeze,'--',evidence).splitlines()
        added=[line[1:] for line in delta if line.startswith('+') and not line.startswith('+++')]
        removed=[line for line in delta if line.startswith('-') and not line.startswith('---')]
        matches=[re.fullmatch(r'([0-9a-f]{64})  (t00-step3-console/sfclear3-freeze-[0-9]{8}T[0-9]{6}Z)/FREEZE_RECORD\.json',line)
                 for line in added]
        matches=[match for match in matches if match]
        if len(matches)!=1 or len(added)!=2 or removed:
            raise Refusal('freeze record not uniquely pinned')
        if not any(re.fullmatch('[0-9a-f]{64}  '+re.escape(matches[0][2])+'/SHA256SUMS',line) for line in added):
            raise Refusal('freeze manifest pair missing')
        inherited=_git_bytes(repo,'show',f'{FREEZE2}:{FROZEN_PATHS[1]}').decode().splitlines()
        def line_hash(prefix):
            found=[line for line in inherited if line.startswith(prefix)]
            if len(found)!=1:
                raise Refusal('missing frozen binding')
            return re.search(r'\b[0-9a-f]{64}\b',found[0])[0]
        calculator=line_hash('**G1/G3 calculator:**')
        roll=line_hash('**G4 roll-date list:**')
        roll_path=study+'/schedule/roll_dates_6J_MGC_2022-09-01_2026-09-02.json'
        schedule_path=study+'/schedule/historical_schedule_2022-09-01_2026-09-02.json'
        if digest(_git_bytes(repo,'show',f'{freeze}:{roll_path}'))!=roll:
            raise Refusal('frozen roll identity differs')
        brief=_git_bytes(repo,'show',f'{audited}:docs/briefs/Q-SFCLEAR-2-personal-clearance-tradeify-book.md').decode()
        recorded=re.findall(r'^Q-SFCLEAR-3 pre-registration commit hash: `([0-9a-f]{40})`',brief,re.M)
        if recorded!=[freeze]:
            raise Refusal('freeze metadata differs')
        lineage=strict_object(_git_bytes(repo,'show',f'{audited}:discovery_manifests/t00_tradeify_book_lineage_2026_10_10.json'))
        trials=[t for t in strict_object(lineage['params'].encode('utf-8'))['further_trial_log'] if t['trial']==10]
        if (len(trials)!=1 or trials[0].get('successor_freeze_commit')!=freeze
                or type(trials[0].get('superseded_before_run_freezes')) is not list
                or FREEZE2 not in trials[0]['superseded_before_run_freezes']):
            raise Refusal('trial lineage differs')
        additions=[]
        for name in _git(repo,'ls-tree','-r','--name-only',audited,'--',study+'/run_records/').splitlines():
            added_at=_git(repo,'log','--diff-filter=A','--format=%H',audited,'--',name).splitlines()[-1]
            original=_git_bytes(repo,'show',f'{added_at}:{name}')
            if original!=_git_bytes(repo,'show',f'{audited}:{name}'):
                raise Refusal('run record changed')
            record=validate_public_record(strict_object(original))
            _git(repo,'merge-base','--is-ancestor',freeze,record['run_head'])
            _git(repo,'merge-base','--is-ancestor',record['run_head'],added_at)
            _git(repo,'diff','--quiet',freeze,record['run_head'],'--',*FROZEN_PATHS)
            changes=_git(repo,'show','--format=','--unified=0',added_at,'--',evidence).splitlines()
            if not any(re.fullmatch(r'\+'+record['private_sha256sums_sha256']+r'  t00-step3-console/[^\s]+/SHA256SUMS',line) for line in changes):
                raise Refusal('run evidence row not added with record')
            additions.append(added_at)
        for commit in _git(repo,'log','--format=%H',audited,'--','docs/briefs/closures/Q-SFCLEAR-3-*').splitlines():
            _git(repo,'merge-base','--is-ancestor',freeze,commit)
            _git(repo,'diff','--quiet',freeze,commit,'--',*FROZEN_PATHS)
            ancestors=set(_git(repo,'rev-list',commit).splitlines())
            if not any(added_at in ancestors for added_at in additions):
                raise Refusal('closure without prior run record')
        return {'freeze':matches[0][1],'calculator':calculator,'tuple':hashes[0],
                'roll_list':roll,'schedule':digest(_git_bytes(repo,'show',f'{freeze}:{schedule_path}'))}
    except (ValueError,AttributeError,IndexError,KeyError,TypeError):
        raise Refusal('freeze provenance malformed') from None


def write_input_manifest(root):
    """Private intermediate inventory; not a publication manifest."""
    root=outside_git(root)
    names=sorted(path.relative_to(root).as_posix() for path in root.rglob('*')
                 if path.is_file() and path.name not in ('INPUT_SHA256SUMS','SHA256SUMS'))
    rows=[digest(_within(root,name).read_bytes())+'  '+name for name in names]
    raw=('\n'.join(rows)+'\n').encode()
    (root/'INPUT_SHA256SUMS').write_bytes(raw)
    return digest(raw)


def execute_processes(receipt, *, replay_script, replay_sha256, replay_args,
                      scoring_script, scoring_sha256, scoring_args, required,
                      preflight_args=None):
    """Run hash-bound replay then scoring, protect inputs, and seal completion."""
    unchanged(receipt)
    provenance={'schema':'sfclear_run_provenance/v1','run_head':receipt.run_head,
        'fg':{'path':str(receipt.fg_path),'sha256':receipt.fg_sha256},
        'driver':{'path':str(Path(replay_script).resolve()),'sha256':replay_sha256,'args':list(replay_args)},
        'scorer':{'path':str(Path(scoring_script).resolve()),'sha256':scoring_sha256,'args':list(scoring_args)}}
    for script,expected in ((replay_script,replay_sha256),(scoring_script,scoring_sha256)):
        if not _hex(expected,64) or digest(Path(script).read_bytes())!=expected:
            raise Refusal('process source identity')
    with (receipt.private_root/'provenance.json').open('xb') as stream:
        stream.write(_json(provenance))
    initial_hash=write_input_manifest(receipt.private_root)
    protected={p:p.read_bytes() for p in receipt.private_root.rglob('*') if p.is_file() and p.name!='INPUT_SHA256SUMS'}
    if preflight_args is not None:
        run_process(receipt,scoring_script,[str(a).replace('{manifest_sha256}',initial_hash) for a in preflight_args],expected_sha256=scoring_sha256)
    run_process(receipt,replay_script,replay_args,expected_sha256=replay_sha256)
    if any(not path.is_file() or path.read_bytes()!=blob for path,blob in protected.items()):
        raise Refusal('replay changed a retained input')
    input_hash=write_input_manifest(receipt.private_root)
    args=[str(arg).replace('{manifest_sha256}',input_hash) for arg in scoring_args]
    run_process(receipt,scoring_script,args,expected_sha256=scoring_sha256)
    if any(not path.is_file() or path.read_bytes()!=blob for path,blob in protected.items()):
        raise Refusal('scoring changed a retained input')
    if digest((receipt.private_root/'INPUT_SHA256SUMS').read_bytes())!=input_hash:
        raise Refusal('scoring changed input manifest')
    names=tuple(path.relative_to(receipt.private_root).as_posix()
                for path in receipt.private_root.rglob('*') if path.is_file())
    if not set(required)<=set(names):
        raise Refusal('required output missing')
    seal_outputs(receipt,names)
    return finish(receipt,required=required)


def run_job(job):
    """Coordinator API. Inputs are explicit path+hash references; no real defaults.

    job keys: repo, private_root, fg {path,sha256}, driver {path,sha256,args},
    inputs {role:{path,sha256}}, calculator {path,inputs}, panels,
    source_build {path,sha256,inputs:{role:{path,sha256}}}. The source-build
    folder stays in place, read-only; the coordinator owns host copy and teardown.
    Driver args may contain {private_root} and {run_head}. It must write route.json
    and port_state.json. Calculator inputs stay in place (never copy ports/Pine).
    Only the public candidate is returned; publication remains a separate action.
    """
    required={'repo','private_root','fg','driver','inputs','calculator','panels','source_build'}
    if type(job) is not dict or set(job)!=required:
        raise Refusal('job fields')
    module_root=Path(job['repo']).resolve()/'lab/analysis/c1/sfclear_2026-10'
    if Path(__file__).resolve()!=module_root/'run_record.py':
        raise Refusal('wrapper must execute from recorded checkout')
    scoring=module_root/'score_r1.py'
    pins=freeze_bindings(job['repo'])
    receipt=begin(repo=job['repo'],private_root=job['private_root'],
                  fg_path=job['fg']['path'],fg_sha256=job['fg']['sha256'])
    roles={'freeze','fees','margin','score_inputs',
           'tuple','size_vector','source_bundle','schedule','roll_list','generator',
           'calendar','reference_friction','e0'}
    if set(job['inputs'])!=roles:
        raise Refusal('input roles')
    local={}
    for role,ref in job['inputs'].items():
        if type(ref) is not dict or set(ref)!= {'path','sha256'}:
            raise Refusal('input reference fields')
        blob=Path(ref['path']).read_bytes()
        if digest(blob)!=ref['sha256'] or not _hex(ref['sha256'],64):
            raise Refusal('input identity mismatch')
        name=f'inputs/{role}.bin'
        target=_within(receipt.private_root,name)
        target.parent.mkdir(exist_ok=True)
        with target.open('xb') as stream:
            stream.write(blob)
        local[role]=name
    request={'schema':'sfclear_score_request/v1','repo':str(receipt.repo),
             'root':str(receipt.private_root),'run_head':receipt.run_head,'pins':pins,
             'inputs':local,'calculator':job['calculator'],'panels':job['panels'],
             'source_build':job['source_build']}
    request_path=receipt.private_root/'request.json'
    request_path.write_bytes(_json(request))
    args=['--request',str(request_path),'--manifest-sha256','{manifest_sha256}']
    driver=job['driver']
    replay_args=[str(arg).replace('{private_root}',str(receipt.private_root)).replace('{run_head}',receipt.run_head)
                 for arg in driver['args']]
    return execute_processes(receipt,replay_script=driver['path'],replay_sha256=driver['sha256'],
        replay_args=replay_args,scoring_script=scoring,scoring_sha256=digest(scoring.read_bytes()),
        scoring_args=args,preflight_args=['--request',str(request_path),'--manifest-sha256','{manifest_sha256}','--preflight'],
        required=('route.json','port_state.json','cells.json','residuals.json','inputs/score_inputs.bin'))


def main(argv=None):
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        candidate=run_job(strict_object(args.job.read_bytes()))
        print(json.dumps({'record':candidate.record,'row':candidate.row},sort_keys=True))
        return 0
    except (OSError,ValueError,KeyError,TypeError):
        print('SFCLEAR run refused; no publication candidate',file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
