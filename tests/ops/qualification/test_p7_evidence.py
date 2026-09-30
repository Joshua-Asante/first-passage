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
    }
    root = env.code_root(variant, edits={'ops/c1_rail/qualification/production_source.py':
                                         lambda text: text + '\n' + snippets[variant]})
    refusal(code, *env.run(root))


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
