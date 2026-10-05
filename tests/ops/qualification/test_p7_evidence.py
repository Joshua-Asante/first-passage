"""P7 evidence: pinned bootstrap, loaded-set closure, acceptance by reconstruction.

Spec rev 4.2 §2.5a–§2.5b, §5 A16–A17 and A19–A23. Each test runs the real
bootstrap in a child interpreter against a TEST_ONLY copy of ``ops``/``core``
committed to a throwaway git repository. The copy carries test key and pin
overrides appended as ordinary module text, modelling an operator enrollment
PR. Nothing here touches the shared ops environment or any private input.
"""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from test_source_contract import KEY_ID, PORT_ROLES, build_source_case, sha

REPO = Path(__file__).resolve().parents[3]
LEG_IDS = ('aegis_6j', 'dj30_mym_p250', 'vanguard_mgc', 'orb_mnq_v7')
pytestmark = pytest.mark.skipif(shutil.which('git') is None, reason='git required for code-root binding')


def _git(root, *args):
    return subprocess.run(['git', '-C', str(root), '-c', 'user.email=p7@test', '-c', 'user.name=p7-test',
                           '-c', 'core.autocrlf=false', *args], check=True, capture_output=True, text=True).stdout


def make_code_root(dst: Path, case, *, edits=None, extra=None, commit=True):
    """Copy ops/core, append TEST_ONLY pin overrides, and commit."""
    ignore = shutil.ignore_patterns('__pycache__', '*.pyc', '.pytest_cache')
    for part in ('ops', 'core'):
        shutil.copytree(REPO / part, dst / part, ignore=ignore)
    shutil.copy2(REPO / 'requirements-ops.lock', dst / 'requirements-ops.lock')
    public = case.public_keys[KEY_ID]
    contract = dst / 'ops/c1_rail/qualification/contract.py'
    contract.write_text(contract.read_text(encoding='utf-8') +
                        f'\n# TEST_ONLY code root override\nSOURCE_SIGNING_KEYS = MappingProxyType('
                        f'{{{KEY_ID!r}: SourceKeyPin({sha(public)!r}, None)}})\n', encoding='utf-8', newline='\n')
    historical = {role: sha(case.payloads[role]) for role in case.document['historical_pins']}
    pins = {leg: (sha(case.payloads[PORT_ROLES[leg]]), case.fixture.pine_sha256[leg]) for leg in LEG_IDS}
    trust = dst / 'ops/c1_rail/qualification/trust_domain.py'
    trust.write_text(trust.read_text(encoding='utf-8') +
                     '\n# TEST_ONLY code root override\nSOURCE_TRUST_CONSTANTS = SourceTrustConstants('
                     f'accepted_historical_pins=MappingProxyType({historical!r}), '
                     'port_runtime_pins=MappingProxyType({leg: PortRuntimePin(leg, rt, pine) for leg, (rt, pine) in '
                     f'{pins!r}.items()}}), '
                     f'effective_settings_sha256={sha(case.payloads["effective_settings_successor"])!r})\n',
                     encoding='utf-8', newline='\n')
    for relative, change in (edits or {}).items():
        path = dst / relative
        path.write_text(change(path.read_text(encoding='utf-8')), encoding='utf-8', newline='\n')
    for relative, text in (extra or {}).items():
        path = dst / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
    if commit:
        _git(dst, 'init', '-q')
        _git(dst, 'add', '-A')
        _git(dst, 'commit', '-q', '-m', 'TEST_ONLY P7 code root')
    return dst


class P7Env:
    """One synthetic source-only case plus its signed inputs on disk."""

    def __init__(self, tmp_path, monkeypatch):
        from composition_fixture import build_artifacts
        import composition_fixture
        original = composition_fixture.build_artifacts

        def holding(root, *, idle=False, port_transform=None):
            def hold(leg, raw):
                if leg != 'orb_mnq_v7':
                    return raw
                return raw.replace(b'local.minute == 15 and self.position', b'local.minute == 59 and self.position')
            return original(root, idle=idle, port_transform=hold)
        monkeypatch.setattr(composition_fixture, 'build_artifacts', holding)
        self.tmp = tmp_path
        self.case = build_source_case(tmp_path / 'artifacts', monkeypatch)
        now = datetime.now(timezone.utc).replace(microsecond=0)
        self.issued = (now - timedelta(hours=1)).isoformat().replace('+00:00', 'Z')
        self.expires = (now + timedelta(days=1)).isoformat().replace('+00:00', 'Z')
        inputs = tmp_path / 'inputs'
        inputs.mkdir()
        self.contract_path = inputs / 'contract.json'
        self.approval_path = inputs / 'approval.json'
        self.registry_path = inputs / 'registry.json'
        self.path_spec = inputs / 'path.json'
        self.contract_path.write_bytes(self.case.contract_bytes())
        self.approval_path.write_bytes(self.case.approval(issued_at=self.issued, expires_at=self.expires))
        self.registry_path.write_text(json.dumps({KEY_ID: base64.b64encode(self.case.public_keys[KEY_ID]).decode()}))
        sessions = json.loads(self.case.payloads['population_index'])['populations']['FULL'][:3]
        self.path_spec.write_text(json.dumps({'sessions': sessions}))
        self.runs = 0

    def code_root(self, name='code', **kwargs):
        return make_code_root(self.tmp / name, self.case, **kwargs)

    def run(self, code_root, *, bootstrap=None, python=None):
        from c1_rail.qualification import p7_evidence
        self.runs += 1
        out = self.tmp / f'record-{self.runs}.json'
        done = p7_evidence.run_p7(code_root=code_root, contract_path=self.contract_path,
                                  approval_path=self.approval_path, registry_path=self.registry_path,
                                  artifact_root=self.case.root, path_spec_path=self.path_spec, out_path=out,
                                  bootstrap=bootstrap, python=python)
        return done, (out.read_bytes() if out.exists() else None)

    def accept(self, record, code_root, *, now=None):
        from c1_rail.qualification import p7_evidence
        return p7_evidence.accept_p7_record(record, code_root=code_root, artifact_root=self.case.root,
                                            now=now or datetime.now(timezone.utc),
                                            public_keys=dict(self.case.public_keys))


@pytest.fixture
def env(tmp_path, monkeypatch):
    return P7Env(tmp_path, monkeypatch)


def refusal(code, done, record):
    assert record is None, 'a refused run must leave no record'
    assert done.returncode != 0 and code in (done.stderr + done.stdout), done.stderr[-2000:]


# ---- bootstrap constant --------------------------------------------------------

def test_bootstrap_constant_matches_pinned_hash():
    from c1_rail.qualification import p7_evidence
    assert sha(p7_evidence.P7_BOOTSTRAP.encode('utf-8')) == p7_evidence.P7_BOOTSTRAP_SHA256


# ---- A16 / A16b / A16c -------------------------------------------------------

def test_p7_loaded_set_is_the_closure(env):  # A16
    probe = ('import importlib, sys\n'
             "importlib.import_module('c1_rail.qualification._p7_dynamic_probe')\n"
             "import c1_rail.qualification._p7_deleted_probe\n"
             "del sys.modules['c1_rail.qualification._p7_deleted_probe']\n")
    root = env.code_root(edits={'ops/c1_rail/qualification/production_source.py': lambda text: text + '\n' + probe},
                         extra={'ops/c1_rail/qualification/_p7_dynamic_probe.py': 'VALUE = 1\n',
                                'ops/c1_rail/qualification/_p7_deleted_probe.py': 'VALUE = 2\n'})
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    doc = json.loads(record)
    first = doc['loaded_closure']['first_party']
    for name in ('c1_rail.qualification._p7_dynamic_probe', 'c1_rail.qualification._p7_deleted_probe',
                 'c1_rail.qualification.p7_driver', 'c1_rail.qualification.p7_evidence',
                 'c1_rail.qualification.production_source'):
        assert name in first, name
        assert first[name]['sha256'] == sha((root / first[name]['path']).read_bytes())
    assert doc['loaded_closure']['distributions'], 'third-party distributions are recorded'
    assert all(row['version'] for row in doc['loaded_closure']['distributions'].values())
    from c1_rail.qualification.contract import canonical_json_bytes
    assert doc['code_closure_sha256'] == sha(canonical_json_bytes(doc['loaded_closure']))
    assert doc['code_tree_clean'] is True and doc['code_head'] == _git(root, 'rev-parse', 'HEAD').strip()


def test_dirty_tree_writes_no_p7_record(env):  # A16b
    root = env.code_root()
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    path = root / 'ops/c1_rail/qualification/model.py'
    path.write_text(path.read_text(encoding='utf-8') + '\n# dirty\n', encoding='utf-8', newline='\n')
    refusal('P7_TREE_DIRTY', *env.run(root))


OUTSIDE = 'evil_outside_module'


@pytest.mark.parametrize('variant,code', [
    ('outside_root', 'P7_ORIGIN_OUTSIDE_ROOT'),
    ('forbidden_import', 'P7_FORBIDDEN_IMPORT'),
    ('edited_mid_run', 'P7_SOURCE_CHANGED_DURING_RUN'),
    ('unaudited_exec', 'P7_UNAUDITED_EXEC'),
    ('disguised_exec', 'P7_UNAUDITED_EXEC'),
    ('forbidden_call_evaluate', 'P7_FORBIDDEN_CALL'),
    ('forbidden_call_simulate', 'P7_FORBIDDEN_CALL'),
    ('restored_original', 'P7_FORBIDDEN_CALL'),
    # Codex P1 on #594: aliases of forbidden modules and of the stubbed runner.
    ('alias_forbidden_by_path', 'P7_FORBIDDEN_IMPORT'),
    ('alias_forbidden_package', 'P7_MODULE_ALIAS'),
    ('alias_forbidden_root', 'P7_MODULE_ALIAS'),
    ('alias_runner', 'P7_MODULE_ALIAS'),
])
def test_p7_loaded_set_negatives(env, variant, code):  # A16c
    twin = env.code_root('twin')
    assert env.run(twin)[1] is not None
    outside = env.tmp / 'outside'
    outside.mkdir()
    (outside / (OUTSIDE + '.py')).write_text('VALUE = 1\n', encoding='utf-8')
    snippets = {
        'outside_root': f'import sys\nsys.path.insert(0, {str(outside)!r})\nimport {OUTSIDE}\n',
        'forbidden_import': 'import c1_rail.qualification.part_a\n',
        'edited_mid_run': ('from pathlib import Path as _P\n_f = _P(__file__).with_name("clock.py")\n'
                           '_f.write_bytes(_f.read_bytes() + b"\\n# edited mid-run\\n")\n'),
        'unaudited_exec': ('from pathlib import Path as _P\n_f = _P(__file__).with_name("clock.py").resolve()\n'
                           'exec(compile(_f.read_bytes(), str(_f), "exec"), {})\n'),
        # First-party bytes under a non-path name: only the content digest can see them.
        'disguised_exec': ('from pathlib import Path as _P\n_f = _P(__file__).with_name("clock.py").resolve()\n'
                           'exec(compile(_f.read_bytes(), "<disguised>", "exec"), {})\n'),
        # Revision 4.3: a caught stub call still leaves no record.
        'forbidden_call_evaluate': ('from c1_rail.qualification import runner as _r\n'
                                    'try:\n    _r.evaluate_replay(None, initial_state=None)\nexcept Exception:\n    pass\n'),
        'forbidden_call_simulate': ('import mc.simulation as _s\n'
                                    'try:\n    _s.simulate_path()\nexcept Exception:\n    pass\n'),
        'restored_original': ('from c1_rail.qualification import runner as _r\n'
                              '_r.evaluate_replay = (lambda *a, **k: None)\n'),
        # A top-level name for the forbidden file itself: only the path check sees it.
        'alias_forbidden_by_path': ('import os as _o, sys as _s\n_s.path.insert(0, _o.path.dirname(__file__))\n' 'import part_a\n'),
        'alias_forbidden_package': 'import qualification.part_a\n',
        'alias_forbidden_root': 'import ops.c1_rail.qualification.part_a\n',
        'alias_runner': ('import os as _o, sys as _s\n_s.path.insert(0, _o.path.dirname(__file__))\n' 'import runner as _r\n_r.evaluate_replay(None, initial_state=None)\n'),
    }
    root = env.code_root(variant, edits={'ops/c1_rail/qualification/production_source.py':
                                         lambda text: text + '\n' + snippets[variant]})
    refusal(code, *env.run(root))


def test_empty_tracked_file_does_not_refuse_empty_third_party_modules(env):  # #594 fold follow-up
    """Third-party sources compile from source under the fresh prefix; an empty site-package
    __init__.py shares its digest with any empty tracked first-party file and is not first-party."""
    root = env.code_root(extra={'ops/p7_empty_tracked_marker.py': ''})
    assert 'ops/p7_empty_tracked_marker.py' in _git(root, 'ls-files')
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    third = json.loads(record)['loaded_closure']['third_party']
    assert any(row['sha256'] == sha(b'') for row in third.values() if row['sha256']), 'an empty module was loaded'


def test_accept_requires_the_presented_bytes_to_be_canonical(env):  # Codex P1 on #594
    from c1_rail.qualification import p7_evidence
    root = env.code_root()
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    assert p7_evidence.parse_record(record) == json.loads(record)
    doc = json.loads(record)
    reordered = json.dumps(dict(reversed(list(doc.items()))), separators=(',', ':'), ensure_ascii=False).encode()
    spaced = json.dumps(doc, sort_keys=True, indent=1, ensure_ascii=False).encode()
    duplicate = record[:-1] + b',"schema":' + json.dumps(doc['schema']).encode() + b'}'
    loose = dict(doc, contract_b64=doc['contract_b64'][:8] + '\n' + doc['contract_b64'][8:])
    for presented in (reordered, spaced, duplicate):
        assert presented != record and json.loads(presented)['schema'] == doc['schema']
        with pytest.raises(p7_evidence.P7Refusal, match='P7_RECORD_NOT_CANONICAL'):
            env.accept(presented, root)
    with pytest.raises(p7_evidence.P7Refusal, match='P7_RECORD_NOT_CANONICAL: contract_b64'):
        env.accept(p7_evidence.canonical(loose), root)


def test_accept_refuses_a_failed_reconstruction_child_even_with_matching_output(env, monkeypatch):  # Codex P2 #594
    import subprocess as _subprocess
    from c1_rail.qualification import p7_evidence
    root = env.code_root()
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    real = p7_evidence.run_p7

    def failing_after_write(**kwargs):
        completed = real(**kwargs)
        assert completed.returncode == 0 and Path(kwargs['out_path']).exists()
        return _subprocess.CompletedProcess(completed.args, 1, completed.stdout, completed.stderr)
    monkeypatch.setattr(p7_evidence, 'run_p7', failing_after_write)
    with pytest.raises(p7_evidence.P7Refusal, match='re-execution exited 1'):
        env.accept(record, root)


def test_run_p7_resolves_relative_paths_before_changing_cwd(env, monkeypatch):  # Codex P2 on #594
    from c1_rail.qualification import p7_evidence
    root = env.code_root()
    (env.tmp / 'records').mkdir()
    monkeypatch.chdir(env.tmp)
    relative = lambda path: os.path.relpath(path, env.tmp)
    done = p7_evidence.run_p7(code_root=relative(root), contract_path=relative(env.contract_path),
                              approval_path=relative(env.approval_path), registry_path=relative(env.registry_path),
                              artifact_root=relative(env.case.root), path_spec_path=relative(env.path_spec),
                              out_path=os.path.join('records', 'p7.json'))
    assert done.returncode == 0, done.stderr[-3000:]
    assert (env.tmp / 'records' / 'p7.json').is_file()


def test_forbidden_matching_is_exact_or_package_prefix(env):  # rev 4.3 (a)
    from c1_rail.qualification import p7_evidence
    forbidden = p7_evidence.forbidden_module
    assert forbidden('c1_rail.qualification.production')
    assert not forbidden('c1_rail.qualification.production_source')
    assert forbidden('c1_rail.qualification.execution.worker') and forbidden('c1_rail.qualification.part_a')
    assert not forbidden('c1_rail.qualification.runner') and not forbidden('mc.simulation')
    assert repr(p7_evidence.P7_FORBIDDEN_MODULES) in p7_evidence.P7_BOOTSTRAP
    done, record = env.run(env.code_root())
    assert record is not None, done.stderr[-3000:]
    loaded = json.loads(record)['loaded_closure']['first_party']
    assert 'c1_rail.qualification.production_source' in loaded
    assert 'c1_rail.qualification.runner' in loaded and 'mc.simulation' in loaded
    assert 'c1_rail.qualification.production' not in loaded


# ---- A17, A19–A22 ------------------------------------------------------------

def test_accept_p7_record_from_bytes(env):  # A17
    root = env.code_root('A')
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    accepted = env.accept(record, root)
    assert accepted.code_closure_sha256 == json.loads(record)['code_closure_sha256']
    from c1_rail.qualification.contract import ContractValidationError
    with pytest.raises((ContractValidationError, ValueError), match='not valid at verification time|EXPIRED'):
        env.accept(record, root, now=datetime.now(timezone.utc) + timedelta(days=3))
    path = root / 'ops/c1_rail/qualification/model.py'
    path.write_text(path.read_text(encoding='utf-8') + '\n# closure B\n', encoding='utf-8', newline='\n')
    _git(root, 'commit', '-q', '-am', 'closure B')
    with pytest.raises(ValueError, match='P7_EVIDENCE_STALE'):
        env.accept(record, root)
    done_b, record_b = env.run(root)
    assert record_b is not None, done_b.stderr[-3000:]
    env.accept(record_b, root)


def _without_volatile(record):
    from c1_rail.qualification import p7_evidence
    doc = json.loads(record)
    for field in p7_evidence.VOLATILE_FIELDS:
        doc.pop(field)
    return doc


def test_two_independent_p7_runs_produce_identical_records(env):  # A19
    from c1_rail.qualification import p7_evidence
    assert set(p7_evidence.VOLATILE_FIELDS) == {'run_started_at', 'run_finished_at', 'host_run_id'}
    root = env.code_root()
    first, second = env.run(root), env.run(root)
    assert first[1] is not None and second[1] is not None, first[0].stderr[-3000:]
    assert first[1] != second[1], 'volatile fields vary'
    assert _without_volatile(first[1]) == _without_volatile(second[1])


def test_driver_edit_is_reflected_or_refused(env):  # A20
    from c1_rail.qualification import p7_evidence
    root = env.code_root()
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    driver = root / 'ops/c1_rail/qualification/p7_driver.py'
    before = json.loads(record)['loaded_closure']['first_party']['c1_rail.qualification.p7_driver']['sha256']
    driver.write_text(driver.read_text(encoding='utf-8') + '\n# driver edit\n', encoding='utf-8', newline='\n')
    _git(root, 'commit', '-q', '-am', 'driver edit')
    with pytest.raises(ValueError, match='P7_EVIDENCE_STALE'):
        env.accept(record, root)
    done_b, record_b = env.run(root)
    after = json.loads(record_b)['loaded_closure']['first_party']['c1_rail.qualification.p7_driver']['sha256']
    assert after != before and after == sha(driver.read_bytes())
    direct = subprocess.run([sys.executable, '-I', '-S', '-B', str(driver), str(root)],
                            capture_output=True, text=True, cwd=env.tmp)
    assert direct.returncode != 0 and 'P7_BOOTSTRAP_MISMATCH' in direct.stderr + direct.stdout
    refusal('P7_BOOTSTRAP_MISMATCH', *env.run(root, bootstrap=p7_evidence.P7_BOOTSTRAP + '\n# altered\n'))


@pytest.mark.parametrize('forgery', ['label', 'bootstrap', 'constructed'])
def test_hand_constructed_record_over_valid_contract_is_not_reproduced(env, forgery):  # A21
    root = env.code_root()
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    env.accept(record, root)
    doc = json.loads(record)
    if forgery == 'label':
        doc['result']['labels'] = sorted(set(doc['result']['labels']) | {'FORGED_LABEL'})
    elif forgery == 'bootstrap':
        doc['bootstrap_sha256'] = '0' * 64
    else:
        doc['result'] = {'labels': ['P7_MET'], 'r1': {'digest': '1' * 64, 'sessions': 3},
                         'r2': {'digest': '2' * 64, 'sessions': 3}}
    from c1_rail.qualification.contract import canonical_json_bytes
    with pytest.raises(ValueError, match='P7_RECORD_NOT_REPRODUCED'):
        env.accept(canonical_json_bytes(doc), root)


@pytest.mark.parametrize('role', ['source_calendar', 'panel_orb_mnq_v7', 'orb_runtime_port'])
def test_artifact_changed_after_run_is_stale(env, monkeypatch, role):  # A22
    from c1_rail.qualification import p7_evidence
    root = env.code_root()
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    launches = []
    monkeypatch.setattr(p7_evidence, 'run_p7', lambda **kwargs: launches.append(kwargs))
    path = env.case.root / env.case.paths[role]
    path.write_bytes(path.read_bytes() + b'\n')
    with pytest.raises(ValueError, match='P7_EVIDENCE_STALE'):
        env.accept(record, root)
    assert launches == []


# ---- A23 -----------------------------------------------------------------------

P7_THIRD_PARTY = ('numpy', 'pandas', 'dateutil', 'python_dateutil', 'pytz', 'six', 'tzdata')


def _copy_site_packages(real: Path, target: Path):
    """Copy (never link, never write into ``real``) the packages a P7 child loads.

    Links would resolve back into the shared environment, which the bootstrap
    correctly refuses as an origin outside the bound site-packages.
    """
    target.mkdir(parents=True, exist_ok=True)
    ignore = shutil.ignore_patterns('tests', '__pycache__', '*.pyc')
    for entry in real.iterdir():
        if not entry.name.startswith(P7_THIRD_PARTY):
            continue
        if entry.is_dir():
            shutil.copytree(entry, target / entry.name, ignore=ignore)
        else:
            shutil.copy2(entry, target / entry.name)


def test_bootstrap_runs_no_site_pth_or_sitecustomize(env):  # A23
    import sysconfig
    from c1_rail.qualification import p7_evidence
    venv = env.tmp / 'venv'
    base = getattr(sys, '_base_executable', sys.executable)
    subprocess.run([base, '-m', 'venv', '--without-pip', str(venv)], check=True, capture_output=True)
    python = venv / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    site = Path(sysconfig.get_paths()['purelib'])
    relative = p7_evidence.site_packages_relative()
    target = venv / relative
    shutil.rmtree(target, ignore_errors=True)
    _copy_site_packages(site, target)
    root = env.code_root()
    twin_done, twin = env.run(root, python=python)
    assert twin is not None, twin_done.stderr[-3000:]
    markers = env.tmp / 'markers'
    markers.mkdir()
    (target / 'sitecustomize.py').write_text(
        f'open({str(markers / "sitecustomize")!r}, "w").close()\n', encoding='utf-8')
    (target / 'zz_planted.pth').write_text(
        f'import os; open({str(markers / "pth")!r}, "w").close()\n', encoding='utf-8')
    control = subprocess.run([str(python), '-I', '-B', '-c', 'import numpy'], capture_output=True, text=True,
                             cwd=env.tmp)
    assert control.returncode == 0, control.stderr
    assert sorted(p.name for p in markers.iterdir()) == ['pth', 'sitecustomize'], 'the planted files are live'
    for marker in markers.iterdir():
        marker.unlink()
    done, record = env.run(root, python=python)
    assert record is not None, done.stderr[-3000:]
    assert list(markers.iterdir()) == []
    doc = json.loads(record)
    listed = {row['name']: row['sha256'] for row in doc['interpreter']['unexecuted_pth']}
    assert listed.get('zz_planted.pth') == sha((target / 'zz_planted.pth').read_bytes())
    assert 'numpy' in doc['loaded_closure']['distributions'] or any(
        name.startswith('numpy') for name in doc['loaded_closure']['third_party'])


def _copied_venv(env):
    """A venv whose bound site-packages is a private copy the test may plant into."""
    import sysconfig
    from c1_rail.qualification import p7_evidence
    venv = env.tmp / 'venv'
    base = getattr(sys, '_base_executable', sys.executable)
    subprocess.run([base, '-m', 'venv', '--without-pip', str(venv)], check=True, capture_output=True)
    python = venv / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    target = venv / p7_evidence.site_packages_relative()
    shutil.rmtree(target, ignore_errors=True)
    _copy_site_packages(Path(sysconfig.get_paths()['purelib']), target)
    return python, target


def test_timestamp_valid_planted_pyc_never_runs_in_place_of_hashed_source(env):  # Codex P1 on #594
    import importlib._bootstrap_external as external
    python, target = _copied_venv(env)
    source = target / 'six.py'
    marker = env.tmp / 'planted-bytecode-ran'
    planted = source.read_text(encoding='utf-8') + f'\nopen({str(marker)!r}, "w").close()\n'
    stat = source.stat()
    cache = target / '__pycache__' / f'six.{sys.implementation.cache_tag}.pyc'
    cache.parent.mkdir(exist_ok=True)
    cache.write_bytes(external._code_to_timestamp_pyc(
        compile(planted, str(source), 'exec'), int(stat.st_mtime), stat.st_size))
    control = subprocess.run([str(python), '-I', '-B', '-c', 'import six'], capture_output=True, text=True,
                             cwd=env.tmp)
    assert control.returncode == 0, control.stderr
    assert marker.exists(), 'the planted bytecode is timestamp-valid and live outside P7'
    marker.unlink()
    done, record = env.run(env.code_root(), python=python)
    assert record is not None, done.stderr[-3000:]
    assert not marker.exists(), 'P7 executed cached bytecode instead of the hashed source'
    six = json.loads(record)['loaded_closure']['third_party']['six']
    assert six == {'path': 'six.py', 'sha256': sha(source.read_bytes())}


def test_third_party_reset_of_the_bytecode_prefix_is_refused(env):  # Codex P1 on #594
    python, target = _copied_venv(env)
    source = target / 'six.py'
    source.write_text(source.read_text(encoding='utf-8') + '\nimport sys as _sys\n_sys.pycache_prefix = None\n',
                      encoding='utf-8')
    refusal('P7_UNBOUND_BYTECODE', *env.run(env.code_root(), python=python))


# ---- Codex code review P2s --------------------------------------------------------

LEG_ID_TEXT = LEG_IDS
TIMESTAMP = r'\d{4}-\d\d-\d\dT\d\d:\d\d'


def test_public_record_has_no_event_level_values(env):  # Codex P2: hashes, counts, labels only
    import re
    done, record = env.run(env.code_root())
    assert record is not None, done.stderr[-3000:]
    doc = json.loads(record)
    for run in ('r1', 'r2'):
        result = doc['result'][run]
        assert 'consumed_intrabar_splits' not in result
        assert result['consumed_intrabar_split_count'] > 0
        assert len(result['consumed_intrabar_splits_sha256']) == 64
    assert 'CONSUMED_INTRABAR_SPLIT' in doc['result']['labels']
    public = {key: value for key, value in doc.items() if key not in (
        'contract_b64', 'approval_b64', 'loaded_closure', 'artifact_inventory', 'interpreter',
        'run_started_at', 'run_finished_at')}
    text = json.dumps(public)
    assert not re.search(TIMESTAMP, text), 'no timestamps in the public record'
    assert not any(leg in text for leg in LEG_ID_TEXT), 'no leg identifiers in the public record'
    assert 'occurrence' not in text


@pytest.mark.parametrize('field', ['interpreter_sha256', 'base_interpreter_sha256', 'version', 'cache_tag',
                                   'lock_sha256', 'site_packages_path', 'unexecuted_pth', 'lock_file',
                                   'install_tree_sha256'])
def test_accept_prechecks_interpreter_binding_before_launch(env, monkeypatch, field):  # Codex P2
    from c1_rail.qualification import p7_evidence
    from c1_rail.qualification.contract import canonical_json_bytes
    root = env.code_root()
    done, record = env.run(root)
    assert record is not None, done.stderr[-3000:]
    doc = json.loads(record)
    if field == 'lock_file':
        lock = root / 'requirements-ops.lock'
        lock.write_text(lock.read_text(encoding='utf-8') + '\n# changed\n', encoding='utf-8', newline='\n')
        _git(root, 'commit', '-q', '-am', 'lock change')
    elif field == 'unexecuted_pth':
        doc['interpreter'][field] = doc['interpreter'][field] + [{'name': 'x.pth', 'sha256': '0' * 64}]
    else:
        doc['interpreter'][field] = 'changed'
    launches = []
    monkeypatch.setattr(p7_evidence, 'run_p7', lambda **kwargs: launches.append(kwargs))
    with pytest.raises(ValueError, match='P7_INTERPRETER_MISMATCH'):
        env.accept(canonical_json_bytes(doc), root)
    assert launches == []


# ---- T00 screen rows K10 and S2 (design 2026-10-02 §2.2, §5.1; build card 2026-10-03 §2.4, §3.3) ----

SCREEN_PACKAGE = 'ops/c1_rail/qualification/t00_screen/'
PRODUCTION_SOURCE = 'ops/c1_rail/qualification/production_source.py'
JOURNAL_NAME = 's1-w0.jsonl'
LEDGER_BYTES = b'{"body":{},"prev_sha256":null,"type":"AUTHORITY_BOUND"}\n'
# A TEST_ONLY stand-in for t00_screen.worker; the case ("<kind> [<arg>]") is read from <run_dir>/case.
SCREEN_WORKER = """import os
import sys

run_dir, journal_name = sys.argv[2], sys.argv[4]
with open(os.path.join(run_dir, 'case'), encoding='utf-8') as handle:
    kind, _, arg = handle.read().partition(' ')
journal = os.path.join(run_dir, 'journal', journal_name)
ledger = os.path.join(run_dir, 'ledger', '0001.jsonl')
if kind == 'forbidden_import':
    import c1_rail.qualification.p7_driver
elif kind == 'allowed_import':
    import importlib
    import c1_rail.qualification.bracket
    from c1_rail.qualification import runner
    simulation = importlib.import_module('mc.simulation')
    expected = [('c1_rail.qualification.runner', '_run_stage'), ('c1_rail.qualification.runner', 'run_synthetic_stage')]
    recorded = sorted((module.__name__, attr) for module, attr, _ in sys.p7_recorder.stubs)
    assert recorded == expected, recorded
    # Independently of the recorder: bootstrap-compiled ('<string>') callables bound in runner and mc.simulation.
    planted = sorted((module.__name__, attr) for module in (runner, simulation) for attr, value in vars(module).items()
                     if getattr(getattr(value, '__code__', None), 'co_filename', None) == '<string>')
    assert planted == expected, planted
    for name in ('_run_stage', 'run_synthetic_stage'):
        try:
            getattr(runner, name)()
        except RuntimeError as exc:
            assert str(exc).startswith('SCREEN_FORBIDDEN_CALL'), exc
        else:
            raise AssertionError(name + ' is not stubbed')
    assert runner.evaluate_replay.__module__ == 'c1_rail.qualification.runner', 'evaluate_replay loads live'
    assert runner.simulate_path is simulation.simulate_path, 'runner.simulate_path loads live'
    assert simulation.simulate_path.__module__ == 'mc.simulation', 'simulate_path loads live'
elif kind == 'open':
    with open(ledger if arg != 'xb' else os.path.join(run_dir, 'ledger', '0002.jsonl'), arg) as handle:
        if arg == 'rb':
            assert handle.read() == LEDGER_BYTES
        else:
            handle.write(b'forged\\n')
elif kind == 'os_open':
    fd = os.open(ledger, int(arg))
    if int(arg) & (os.O_WRONLY | os.O_RDWR):
        os.write(fd, b'forged\\n')
    os.close(fd)
elif kind == 'journal_open':
    with open(journal, 'ab') as handle:
        handle.write(b'record\\n')
elif kind == 'journal_os_open':
    fd = os.open(journal, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, 'O_BINARY', 0))
    os.write(fd, b'record\\n')
    os.close(fd)
elif kind == 'devnull':  # card 3.3 note 2026-10-03: the null device holds no data
    import platform
    fd = os.open(os.devnull, os.O_RDWR)
    os.close(fd)
    open(os.devnull, 'wb').close()
    platform._syscmd_ver()  # subprocess.DEVNULL's os.open(os.devnull, os.O_RDWR), without depending on WMI
else:
    raise SystemExit('unknown case ' + kind)
print('WORKER_DONE ' + kind)
""".replace('LEDGER_BYTES', repr(LEDGER_BYTES))
_BINARY = getattr(os, 'O_BINARY', 0)
# Card §3.3: every write-open mode and os.open write, append or create flag is refused outside the journal.
LEDGER_WRITE_OPENS = ('open wb', 'open xb', 'open r+b', 'open ab',
                      *(f'os_open {flags | _BINARY}' for flags in (
                          os.O_WRONLY | os.O_TRUNC, os.O_RDWR, os.O_WRONLY | os.O_CREAT, os.O_APPEND)))
LEDGER_READ_OPENS = ('open rb', f'os_open {os.O_RDONLY | _BINARY}')
BAD_JOURNAL_NAMES = ('../ledger/0001.jsonl', 's0-w0.jsonl', 's1-w0.jsonl\n', 'S1-w0.jsonl')


def _screen_tree(extra=None):
    """TEST_ONLY stubs for the t00_screen package, which does not exist on main yet."""
    files = {SCREEN_PACKAGE + '__init__.py': '"""TEST_ONLY t00_screen stub."""\n',
             SCREEN_PACKAGE + 'plan.py': 'VALUE = 1\n',
             SCREEN_PACKAGE + 'worker.py': SCREEN_WORKER}
    files.update(extra or {})
    return files


def run_screen(env, code_root, case, *, journal_name=JOURNAL_NAME):
    """The card §3.3 worker command, run directly (the coordinator and Job Object are P-F's)."""
    from c1_rail.qualification import p7_evidence
    env.runs += 1
    run_dir = env.tmp / f'screen-run-{env.runs}'
    for sub in ('journal', 'ledger'):
        (run_dir / sub).mkdir(parents=True)
    (run_dir / 'ledger' / '0001.jsonl').write_bytes(LEDGER_BYTES)
    (run_dir / 'case').write_bytes(case.encode('utf-8'))
    command = [sys.executable, '-I', '-S', '-B', '-c', p7_evidence.SCREEN_BOOTSTRAP, str(Path(code_root).resolve()),
               str(run_dir.resolve()), 'a' * 64, journal_name]
    return subprocess.run(command, capture_output=True, text=True, cwd=env.tmp, timeout=600), run_dir


def test_K10(env):
    """P7 never imports the screen, and the screen never imports execution (P7_/SCREEN_FORBIDDEN_IMPORT)."""
    allowed = 'c1_rail.qualification._k10_allowed_probe'
    twin = env.code_root('k10-twin', edits={PRODUCTION_SOURCE: lambda text: text + f'\nimport {allowed}\n'},
                         extra=_screen_tree({'ops/c1_rail/qualification/_k10_allowed_probe.py': 'VALUE = 1\n'}))
    done, record = env.run(twin)
    assert record is not None, done.stderr[-3000:]
    assert allowed in json.loads(record)['loaded_closure']['first_party']
    root = env.code_root('k10', edits={PRODUCTION_SOURCE: lambda text: text +
                                       '\nimport c1_rail.qualification.t00_screen.plan\n'}, extra=_screen_tree())
    refusal('P7_FORBIDDEN_IMPORT', *env.run(root))
    # The screen side: an execution-list import (design §5.1) is refused; bracket and the live kernel load, and
    # the stub set is exactly runner._run_stage and runner.run_synthetic_stage (card §2.4).
    done, _ = run_screen(env, twin, 'allowed_import')
    assert done.returncode == 0 and 'WORKER_DONE allowed_import' in done.stdout, done.stderr[-3000:]
    done, _ = run_screen(env, twin, 'forbidden_import')
    assert done.returncode != 0 and 'WORKER_DONE' not in done.stdout, done.stdout[-3000:]
    assert 'SCREEN_FORBIDDEN_IMPORT: c1_rail.qualification.p7_driver' in done.stderr, done.stderr[-3000:]


def test_S2(env):
    """A screen worker write-opens only realpath(join(run_dir, 'journal', journal_name)) or the null device
    (SCREEN_WRITE_REFUSED)."""
    root = env.code_root('s2', extra=_screen_tree())
    failures = []

    def check(label, ok, detail):
        if not ok:
            failures.append(f'{label}: {detail[-1500:]}')
    for case in ('journal_open', 'journal_os_open', 'devnull', *LEDGER_READ_OPENS):  # twins
        done, run_dir = run_screen(env, root, case)
        check(case, done.returncode == 0 and 'WORKER_DONE' in done.stdout, done.stderr)
        if case.startswith('journal'):
            check(case, (run_dir / 'journal' / JOURNAL_NAME).read_bytes() == b'record\n', 'journal bytes')
        check(case, (run_dir / 'ledger' / '0001.jsonl').read_bytes() == LEDGER_BYTES, 'ledger bytes changed')
        check(case, not (run_dir / 'ledger' / '0002.jsonl').exists(), 'a new non-journal file was created')
    for case in LEDGER_WRITE_OPENS:
        done, run_dir = run_screen(env, root, case)
        check(case, done.returncode != 0 and 'WORKER_DONE' not in done.stdout, done.stdout)
        check(case, 'SCREEN_WRITE_REFUSED' in done.stderr, done.stderr)
        check(case, (run_dir / 'ledger' / '0001.jsonl').read_bytes() == LEDGER_BYTES, 'ledger bytes changed')
        check(case, not (run_dir / 'ledger' / '0002.jsonl').exists(), 'a new non-journal file was created')
    # A journal name outside ^[csv][1-9][0-9]*-w[0-9]+[.]jsonl$ is refused by the bootstrap itself.
    for name in BAD_JOURNAL_NAMES:
        done, run_dir = run_screen(env, root, 'journal_open', journal_name=name)
        check(repr(name), done.returncode != 0 and 'WORKER_DONE' not in done.stdout, done.stdout)
        check(repr(name), 'SCREEN_WRITE_REFUSED' in done.stderr, done.stderr)
        check(repr(name), (run_dir / 'ledger' / '0001.jsonl').read_bytes() == LEDGER_BYTES, 'ledger bytes changed')
        check(repr(name), list((run_dir / 'journal').iterdir()) == [], 'journal written')
    assert not failures, '\n'.join(failures)


def test_render_bootstrap_generates_both_bootstraps():  # design C8; card §3.1 (non-row)
    from c1_rail.qualification import p7_evidence
    q = 'c1_rail.qualification.'
    assert p7_evidence.P7_BOOTSTRAP == p7_evidence.render_bootstrap(p7_evidence._P7_BOOTSTRAP_PARAMS)
    assert p7_evidence.SCREEN_BOOTSTRAP == p7_evidence.render_bootstrap(p7_evidence._SCREEN_BOOTSTRAP_PARAMS)
    assert sha(p7_evidence.SCREEN_BOOTSTRAP.encode('utf-8')) == p7_evidence.SCREEN_BOOTSTRAP_SHA256
    assert p7_evidence.SCREEN_BOOTSTRAP_SHA256 != p7_evidence.P7_BOOTSTRAP_SHA256
    assert set(p7_evidence.P7_FORBIDDEN_MODULES) == {q + name for name in (
        'part_a', 'bracket', 'benchmark', 'benchmark_part_a', 'production', 'orchestration', 'result_adjudication',
        'seal', 'execution', 'screen_authority', 't00_screen')}
    assert set(p7_evidence.SCREEN_FORBIDDEN_MODULES) == {q + name for name in (
        'production', 'orchestration', 'result_adjudication', 'seal', 'execution', 'part_a', 'benchmark',
        'benchmark_part_a', 'p7_driver')}
    assert repr(p7_evidence.SCREEN_FORBIDDEN_MODULES) in p7_evidence.SCREEN_BOOTSTRAP
    with pytest.raises(ValueError):
        p7_evidence.render_bootstrap(dict(p7_evidence._P7_BOOTSTRAP_PARAMS, unknown=1))
