"""R-REC packet: recorder re-digest refusal, installed-source execution and the install-tree digest.

Build card 2026-10-03 §8, "R-REC packet: scope, footprint and required attack classes", with the
card-owner rulings of 2026-10-04 (digest set, budget, ``__pycache__``, tests). Class (1): an A→B→A
re-digest of a recorded third-party module or port is refused. Class (2)+(4): one tree digest in
the P7 ``interpreter`` binding; the epoch-close side is in ``test_screen_authority.py``. Class (5):
``runpy.run_path`` or ``exec(compile(...))`` of installed source is refused by the audit hook.
Class (3) is the accepted residual (no test). Each red has a passing twin. The recorder cases run
the real SCREEN_BOOTSTRAP (one recorder implementation, design C8) over a TEST_ONLY copy of
ops/core; nothing here reads a private input or writes the shared environment.
"""
from __future__ import annotations

# pytest fixtures: pylint: disable=redefined-outer-name

import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

import pytest

from test_p7_evidence import P7Env, _copied_venv, _screen_tree, make_code_root

pytestmark = pytest.mark.skipif(shutil.which('git') is None, reason='git required for code-root binding')
REPO = Path(__file__).resolve().parents[3]

# A TEST_ONLY stand-in for t00_screen.worker; the case is read from <run_dir>/case. The screen
# bootstrap refuses write-opens outside the journal, so a site file is replaced by renaming a file
# the test staged in <run_dir>/stage.
RREC_WORKER = """import importlib
import importlib.util
import os
import runpy
import sys

run_dir = sys.argv[2]
with open(os.path.join(run_dir, 'case'), encoding='utf-8') as handle:
    kind = handle.read()
stage = os.path.join(run_dir, 'stage')
if kind == 'reload_same':
    import six
    importlib.reload(six)
    importlib.reload(six)
elif kind == 'reload_aba':
    import six
    os.replace(os.path.join(stage, 'B.py'), six.__file__)
    importlib.reload(six)
    os.replace(os.path.join(stage, 'A.py'), six.__file__)
    importlib.reload(six)
elif kind == 'port_same':
    compile(b'PORT = 1\\n', 'ports/t00_rrec_port.py', 'exec')
    compile(b'PORT = 1\\n', 'ports/t00_rrec_port.py', 'exec')
elif kind == 'port_aba':
    compile(b'PORT = 1\\n', 'ports/t00_rrec_port.py', 'exec')
    compile(b'PORT = 2\\n', 'ports/t00_rrec_port.py', 'exec')
    compile(b'PORT = 1\\n', 'ports/t00_rrec_port.py', 'exec')
elif kind == 'imports':
    import colorsys
    import six
    importlib.reload(colorsys)
    importlib.reload(six)
elif kind == 'run_path_site':
    import six
    runpy.run_path(six.__file__)
elif kind == 'run_path_stdlib':
    import colorsys
    runpy.run_path(colorsys.__file__)
elif kind == 'exec_compile_site':
    import six
    exec(compile(open(six.__file__, 'rb').read(), six.__file__, 'exec'), {'__name__': 'rrec'})
elif kind == 'exec_compile_stdlib':
    import colorsys
    exec(compile(open(colorsys.__file__, 'rb').read(), colorsys.__file__, 'exec'), {'__name__': 'rrec'})
elif kind in ('loader_recorded_site', 'loader_unrecorded_site'):
    import six
    path = os.path.join(os.path.dirname(six.__file__), 't00_rrec_unrecorded.py')
    os.replace(os.path.join(stage, 't00_rrec_unrecorded.py'), path)
    if kind == 'loader_recorded_site':  # twin: the recording finder hashes it first
        importlib.invalidate_caches()
        import t00_rrec_unrecorded
    else:  # a site-packages file loaded by path, around the recording finder
        spec = importlib.util.spec_from_file_location('t00_rrec_unrecorded', path)
        spec.loader.exec_module(importlib.util.module_from_spec(spec))
else:
    raise SystemExit('unknown case ' + kind)
print('WORKER_DONE ' + kind)
"""


@pytest.fixture
def env(tmp_path, monkeypatch):
    return P7Env(tmp_path, monkeypatch)


def run_worker(env, root, case, *, python=None, stage=None):
    from c1_rail.qualification import p7_evidence
    env.runs += 1
    run_dir = env.tmp / f'rrec-run-{env.runs}'
    for sub in ('journal', 'ledger', 'stage'):
        (run_dir / sub).mkdir(parents=True)
    for name, raw in (stage or {}).items():
        (run_dir / 'stage' / name).write_bytes(raw)
    (run_dir / 'case').write_bytes(case.encode('utf-8'))
    command = [str(python or sys.executable), '-I', '-S', '-B', '-c', p7_evidence.SCREEN_BOOTSTRAP,
               str(Path(root).resolve()), str(run_dir.resolve()), 'a' * 64, 's1-w0.jsonl']
    return subprocess.run(command, capture_output=True, text=True, cwd=env.tmp, timeout=600, check=False)


def passed(done, case):
    assert done.returncode == 0 and f'WORKER_DONE {case}' in done.stdout, done.stderr[-3000:]


def refused(done, code, case):
    assert done.returncode != 0 and 'WORKER_DONE' not in done.stdout, f'{case} ran: ' + done.stdout[-2000:]
    assert code in done.stderr, done.stderr[-3000:]


def worker_root(env):
    return make_code_root(env.tmp / 'code', env.case,
                          extra=_screen_tree({'ops/c1_rail/qualification/t00_screen/worker.py': RREC_WORKER}))


# ---- class (1): R-REC-1, no re-digest of a recorded third-party module or port ------------------

def test_class1_third_party_reload_a_b_a_is_refused(env):
    python, site = _copied_venv(env)
    root = worker_root(env)
    original = (site / 'six.py').read_bytes()
    passed(run_worker(env, root, 'reload_same', python=python), 'reload_same')
    done = run_worker(env, root, 'reload_aba', python=python,
                      stage={'A.py': original, 'B.py': original + b'\nT00_RREC_B = 1\n'})
    refused(done, 'SCREEN_SOURCE_CHANGED_DURING_RUN: third-party six', 'reload_aba')


def test_class1_port_recompiled_a_b_a_is_refused(env):
    root = worker_root(env)
    passed(run_worker(env, root, 'port_same'), 'port_same')
    refused(run_worker(env, root, 'port_aba'), 'SCREEN_SOURCE_CHANGED_DURING_RUN: port ports/t00_rrec_port.py',
            'port_aba')


# ---- class (5): R-REC-3, installed source executes only through importlib's loader -------------

@pytest.mark.parametrize('case', ['run_path_site', 'run_path_stdlib', 'exec_compile_site', 'exec_compile_stdlib'])
def test_class5_directly_executed_installed_source_is_refused(env, case):
    root = worker_root(env)
    passed(run_worker(env, root, 'imports'), 'imports')
    refused(run_worker(env, root, case), 'SCREEN_UNAUDITED_EXEC', case)


def test_class5_a_site_file_loaded_by_path_around_the_finder_is_refused(env):
    """importlib's own loader, but no recorded row for the file: refused; imported through the
    recording finder (twin), it is recorded and runs."""
    python, site = _copied_venv(env)
    root = worker_root(env)
    stage ={'t00_rrec_unrecorded.py': b'UNRECORDED = 1\n'}
    passed(run_worker(env, root, 'loader_recorded_site', python=python, stage=stage), 'loader_recorded_site')
    (site / 't00_rrec_unrecorded.py').unlink()
    refused(run_worker(env, root, 'loader_unrecorded_site', python=python, stage=stage),
            'SCREEN_UNAUDITED_EXEC: compile of site-packages bytes that are not a recorded module',
            'loader_unrecorded_site')


# ---- class (2): the install-tree digest (card-owner ruling 2026-10-04 (1)) ---------------------

def fake_install(root: Path):
    """A synthetic base install and venv site-packages in the ruled (Windows) layout."""
    xy = '{0}{1}'.format(*sys.version_info[:2])
    base, site = root / 'base', root / 'venv' / 'Lib' / 'site-packages'
    files = {base / f'python{xy}.dll': b'dll', base / 'vcruntime140.dll': b'rt', base / f'python{xy}.zip': b'zip',
             base / 'LICENSE.txt': b'not bound', base / 'DLLs' / '_ext.pyd': b'pyd',
             base / 'Lib' / 'colorsys.py': b'STDLIB = 1\n',
             base / 'Lib' / '__pycache__' / 'colorsys.cpython.pyc': b'pyc',
             base / 'Lib' / 'site-packages' / 'unreachable.py': b'BASE_SITE = 1\n',
             site / 'dep.py': b'DEP = 1\n', site / '__pycache__' / 'dep.cpython.pyc': b'pyc'}
    for path, raw in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    return base, site, files


class _OsAs:  # pylint: disable=too-few-public-methods
    """p7_evidence's ``os`` with only ``name`` replaced, so either install layout is digested on any host."""

    def __init__(self, name):
        self.name = name

    def __getattr__(self, attr):
        return getattr(os, attr)


def tree_digest(layout, site, base, fn=None):
    """``install_tree_sha256(site, base=base)`` (or ``fn``) with p7_evidence seeing ``os.name == layout``."""
    from c1_rail.qualification import p7_evidence  # pylint: disable=import-outside-toplevel
    saved, p7_evidence.os = p7_evidence.os, _OsAs(layout)
    try:
        return (fn or p7_evidence.install_tree_sha256)(site, base=base)
    finally:
        p7_evidence.os = saved


@pytest.mark.parametrize('layout', ['nt', 'posix'])
def test_class2_install_tree_digest_covers_the_ruled_set_and_nothing_else(tmp_path, layout):
    from c1_rail.qualification import p7_evidence
    base, site, files = fake_install(tmp_path)
    digest = tree_digest(layout, site, base)
    assert digest == p7_evidence.install_tree_sha256(site, base=base)
    xy = '{0}{1}'.format(*sys.version_info[:2])
    bound = (base / f'python{xy}.dll', base / 'vcruntime140.dll', base / f'python{xy}.zip', base / 'DLLs' / '_ext.pyd',
             base / 'Lib' / 'colorsys.py', base / 'Lib' / '__pycache__' / 'colorsys.cpython.pyc', site / 'dep.py',
             site / '__pycache__' / 'dep.cpython.pyc')
    for path in bound:  # red: each ruled file's bytes move the digest
        raw = path.read_bytes()
        path.write_bytes(raw + b'#')
        assert p7_evidence.install_tree_sha256(site, base=base) != digest, path
        path.write_bytes(raw)
    added = base / 'Lib' / '__pycache__' / 'new.cpython.pyc'
    added.write_bytes(b'new')
    assert p7_evidence.install_tree_sha256(site, base=base) != digest, 'a new file is bound'
    added.unlink()
    for path in (base / 'LICENSE.txt', base / 'Lib' / 'site-packages' / 'unreachable.py'):  # twins: unbound
        path.write_bytes(path.read_bytes() + b'#')
    assert p7_evidence.install_tree_sha256(site, base=base) == digest
    assert set(files) - set(bound) == {base / 'LICENSE.txt', base / 'Lib' / 'site-packages' / 'unreachable.py'}


def test_class2_install_tree_digest_is_sorted_relative_paths_plus_bytes(tmp_path):
    """Deterministic: the same tree at another location, written in another order, has the same
    digest; a rename that keeps the bytes changes it."""
    from c1_rail.qualification import p7_evidence
    trees = []
    for name, order in (('one', 1), ('two', -1)):
        base, site = tmp_path / name / 'base', tmp_path / name / 'site'
        rows = [(base / 'DLLs' / 'a.pyd', b'a'), (base / 'Lib' / 'b.py', b'b'), (base / 'Lib' / 'c' / 'd.py', b'd'),
                (site / 'e.py', b'e')]
        for path, raw in rows[::order]:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        trees.append((site, base))
    first = p7_evidence.install_tree_sha256(trees[0][0], base=trees[0][1])
    assert first == p7_evidence.install_tree_sha256(trees[1][0], base=trees[1][1])
    os.replace(trees[1][1] / 'Lib' / 'b.py', trees[1][1] / 'Lib' / 'b2.py')
    assert first != p7_evidence.install_tree_sha256(trees[1][0], base=trees[1][1])


def test_class2_an_unreadable_install_tree_fails_closed(tmp_path):
    from c1_rail.qualification import p7_evidence
    base, site, _ = fake_install(tmp_path)
    with pytest.raises(OSError):
        p7_evidence.install_tree_sha256(site.parent / 'missing', base=base)


def test_class2_base_site_packages_on_sys_path_is_refused(monkeypatch):
    """Card-owner ruling (1): the base Lib/site-packages is outside the digest only while it is
    unreachable; on sys.path, the interpreter binding is refused (twin: the running interpreter)."""
    from c1_rail.qualification import p7_evidence
    monkeypatch.setattr(p7_evidence, 'install_tree_sha256', lambda site, base=None: 'e' * 64, raising=False)
    binding = p7_evidence.current_interpreter_binding(REPO)
    assert binding['install_tree_sha256'] == 'e' * 64
    base_site = os.path.join(sys.base_prefix, *p7_evidence.site_packages_relative().split('/'))
    if os.path.normcase(os.path.realpath(base_site)) == os.path.normcase(binding['site_packages_path']):
        pytest.skip('no venv: the base site-packages is the bound, digested site')
    monkeypatch.setattr(sys, 'path', [*sys.path, base_site])
    with pytest.raises(p7_evidence.P7Refusal, match='P7_INTERPRETER_MISMATCH: the base install site-packages'):
        p7_evidence.current_interpreter_binding(REPO)


def test_class2_a_venv_including_system_site_packages_is_refused(tmp_path):
    """Card-owner ruling (1): pyvenv.cfg include-system-site-packages must be false."""
    venv = tmp_path / 'venv'
    base = getattr(sys, '_base_executable', sys.executable)
    subprocess.run([base, '-m', 'venv', '--without-pip', '--system-site-packages', str(venv)], check=True,
                   capture_output=True)
    python = venv / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    probe = ('import sys; sys.path.insert(0, sys.argv[1]); from c1_rail.qualification import p7_evidence\n'
             'p7_evidence.install_tree_sha256 = lambda site, base=None: "e" * 64\n'
             'p7_evidence.current_interpreter_binding(sys.argv[2]); print("BOUND")')
    done = subprocess.run([str(python), '-I', '-c', probe, str(REPO / 'ops'), str(REPO)], capture_output=True,
                          text=True, check=False, timeout=300)
    assert done.returncode != 0 and 'BOUND' not in done.stdout, done.stdout
    assert 'P7_INTERPRETER_MISMATCH: pyvenv.cfg includes the system site-packages' in done.stderr, done.stderr[-2000:]


def test_class2_the_real_install_tree_digest_once():
    """Card-owner ruling (4): the one test over the real interpreter's install tree. Ruling (2)'s
    per-close cost (the whole interpreter binding, about 15 s at most) is measured alone, outside
    a parallel test run, and reported with the packet; under xdist load this timing is not that
    measurement, so it is printed, not asserted."""
    from c1_rail.qualification import p7_evidence
    started = time.perf_counter()
    binding = p7_evidence.current_interpreter_binding(REPO)
    elapsed = time.perf_counter() - started
    print(f'REAL_INTERPRETER_BINDING_SECONDS {elapsed:.2f}')
    digest = binding['install_tree_sha256']
    assert type(digest) is str and len(digest) == 64 and int(digest, 16) >= 0
