"""Installed hooks must validate the checkout environment before consumers run."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from test_fp_launcher import checkout, ops_env  # Reuse offline launcher fixtures.

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ('pre-commit', 'pre-merge-commit', 'pre-push', 'post-merge')
PROBE = '''import json, os, sys
from pathlib import Path
with Path(os.environ['HOOK_TRACE']).open('a') as output:
    output.write(json.dumps(dict(script=Path(__file__).name, prefix=sys.prefix,
                                cwd=str(Path.cwd()), args=sys.argv[1:])) + '\\n')
if '--dry-run' in sys.argv:
    print('changed')
raise SystemExit(int(os.environ.get('HOOK_PROBE_EXIT', '0')))
'''


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.fixture
def hook_checkout(checkout):
    templates = checkout / 'scripts/githooks'
    templates.mkdir()
    # Routing tests start with canonical LF blob contents. The separate fresh
    # autocrlf checkout test below exercises the checkout/installer boundary.
    for name in HOOKS:
        (templates / name).write_text((ROOT / 'scripts/githooks' / name).read_text(),
                                     encoding='utf-8', newline='\n')
    for name in ('install_hooks.sh', 'install_hooks.bat'):
        shutil.copy2(ROOT / 'scripts' / name, checkout / 'scripts' / name)
    shutil.copy2(ROOT / '.gitattributes', checkout / '.gitattributes')
    for name in ('probe.py', 'roll_sessions.py', 'check_push_collision.py', 'check_pine_manifest.py'):
        (checkout / 'scripts' / name).write_text(PROBE, encoding='utf-8')
    (checkout / 'scripts/gates.yml').write_text(
        'version: 1\ngates:\n  - id: probe\n    tier: always\n'
        '    cmd:\n      - python\n      - scripts/probe.py\n', encoding='utf-8')
    docs = checkout / 'docs'
    docs.mkdir()
    (docs / 'SESSIONS.md').write_text('fixture\n')
    git(checkout, 'add', '.')
    git(checkout, '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
        'commit', '-qm', 'hook fixture')
    git(checkout, 'update-ref', 'ORIG_HEAD', 'HEAD~1')
    return checkout


def run_hook(root, shell, hook, env):
    return subprocess.run([shell, str(root / 'scripts/githooks' / hook)], cwd=root / 'docs',
                          env=env, capture_output=True, text=True, encoding='utf-8',
                          errors='replace', check=False, timeout=45)


def environment(root, ops_env):
    return dict(os.environ, FP_OPS_ENV=ops_env, HOOK_TRACE=str(root / '.cache/hook-trace.jsonl'),
                PATH=str(Path(sys.executable).parent) + os.pathsep + os.environ.get('PATH', ''))


@pytest.mark.parametrize('hook', HOOKS)
def test_hooks_select_validated_interpreter_and_checkout(hook_checkout, ops_env, shell, hook):
    root = hook_checkout
    (root / '.cache').mkdir(exist_ok=True)
    result = run_hook(root, shell, hook, environment(root, ops_env))
    assert result.returncode == 0, result.stdout + result.stderr
    events = [json.loads(line) for line in (root / '.cache/hook-trace.jsonl').read_text().splitlines()]
    assert len(events) == {'pre-commit': 1, 'pre-merge-commit': 2, 'pre-push': 1, 'post-merge': 4}[hook]
    assert all(Path(event['prefix']).samefile(ops_env) for event in events)
    assert all(Path(event['cwd']).samefile(root) for event in events)
    if hook == 'pre-merge-commit':
        assert [event['args'][0] for event in events] == ['--check-order', '--check-append-only']
    if hook == 'post-merge':
        assert events[0]['args'] == ['--check-pin-provenance', '--base', 'ORIG_HEAD']
        assert '--dry-run' in events[2]['args'] and '--dry-run' not in events[3]['args']


@pytest.mark.parametrize('hook', HOOKS)
@pytest.mark.parametrize('invalid', ['missing', 'mismatch'])
def test_invalid_environment_never_runs_hook_consumer(hook_checkout, ops_env, shell, hook, invalid):
    root = hook_checkout
    (root / '.cache').mkdir(exist_ok=True)
    env = environment(root, ops_env)
    if invalid == 'missing':
        env['FP_OPS_ENV'] = str(root / 'missing environment')
    else:
        (root / 'requirements-ops.lock').write_text('pytest==0.0.0\n')
    result = run_hook(root, shell, hook, env)
    assert (result.returncode == 0) == (hook == 'post-merge')
    assert not Path(env['HOOK_TRACE']).exists(), result.stdout + result.stderr
    assert 'fp:' in result.stderr
    if hook == 'post-merge':
        assert 'WARNING' in result.stdout + result.stderr


@pytest.mark.parametrize('hook', HOOKS[:3])
def test_blocking_hooks_preserve_consumer_failure(hook_checkout, ops_env, shell, hook):
    root = hook_checkout
    (root / '.cache').mkdir(exist_ok=True)
    env = environment(root, ops_env)
    env['HOOK_PROBE_EXIT'] = '7'
    result = run_hook(root, shell, hook, env)
    assert result.returncode != 0
    events = Path(env['HOOK_TRACE']).read_text().splitlines()
    assert len(events) == 1  # A failed first check must prevent later commands.


@pytest.mark.parametrize('installer', ['sh', 'bat'])
def test_fresh_autocrlf_worktree_installs_runnable_common_hooks(hook_checkout, ops_env, shell, tmp_path, installer):
    if installer == 'bat' and os.name != 'nt':
        pytest.skip('Windows batch installer')
    root = hook_checkout
    git(root, 'config', 'core.autocrlf', 'true')
    linked = tmp_path / 'linked checkout with spaces'
    git(root, 'worktree', 'add', '--detach', str(linked), 'HEAD')
    command = ([shell, str(linked / 'scripts/install_hooks.sh')] if installer == 'sh' else
               ['cmd', '/d', '/c', 'scripts\\install_hooks.bat'])
    installed = subprocess.run(command, cwd=linked, capture_output=True, text=True,
                               encoding='utf-8', errors='replace', check=False)
    assert installed.returncode == 0, installed.stdout + installed.stderr
    (linked / '.cache').mkdir(exist_ok=True)
    env = environment(linked, ops_env)
    # Invoke the installed common hook, not the source template. Its root must
    # come from the linked checkout where Git invoked it.
    hook = Path(git(linked, 'rev-parse', '--git-path', 'hooks/pre-commit'))
    result = subprocess.run([shell, str(hook)], cwd=linked, env=env,
                            capture_output=True, text=True, encoding='utf-8',
                            errors='replace', check=False, timeout=45)
    assert result.returncode == 0, result.stdout + result.stderr
    event, = [json.loads(line) for line in Path(env['HOOK_TRACE']).read_text().splitlines()]
    assert Path(event['prefix']).samefile(ops_env)
    assert Path(event['cwd']).samefile(linked)
