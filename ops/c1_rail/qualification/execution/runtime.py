"""Measure ordinary code from real process entrypoints without importing ports."""
import ast
from importlib.util import resolve_name
from importlib import metadata
import os
from pathlib import Path
import platform
import re
import stat
import sys

from ..contract import canonical_json_bytes as encoded, parse_canonical_json
from .files import read_regular
from .protocol import sha256

ENTRYPOINTS = {'worker': 'c1_rail.qualification.execution.worker',
              'supervisor': 'c1_rail.qualification.execution.service',
              'g5': 'c1_rail.qualification.execution.g5'}
SIGNING_CONFIGURATION = 'tools/local_verification/requirements-extra.txt'


def installed_code_root():
    return Path(__file__).resolve().parents[4]


def source_closure(root, role):
    root = Path(root)
    roots = [root / part for part in ('ops', 'core', 'lab', 'governance', '')]
    def locate(name):
        relative = Path(*name.split('.'))
        found = [path for base in roots for path in (base / relative.with_suffix('.py'), base / relative / '__init__.py') if path.is_file()]
        if len(found) > 1:
            raise ValueError('ambiguous ordinary source origin: ' + name)
        return found[0] if found else None
    pending, sources = [ENTRYPOINTS[role], __name__], {}
    while pending:
        name = pending.pop()
        if name in sources:
            continue
        path = locate(name)
        if path is None:
            raise ValueError('missing ordinary entrypoint: ' + name)
        relative = path.relative_to(root).as_posix()
        raw = read_regular(root, relative, limit=4 * 1024 * 1024)
        sources[name] = dict(path=relative, sha256=sha256(raw))
        package = name if path.name == '__init__.py' else name.rpartition('.')[0]
        dependencies = {'.'.join(name.split('.')[:index]) for index in range(1, len(name.split('.')))}
        for node in ast.walk(ast.parse(raw, filename=relative)):
            if isinstance(node, ast.Import):
                dependencies.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ''
                if node.level:
                    try:
                        base = resolve_name('.' * node.level + base, package)
                    except (ImportError, ValueError):
                        continue
                dependencies.add(base)
                dependencies.update(base + '.' + alias.name for alias in node.names if alias.name != '*')
        pending.extend(dependency for dependency in dependencies if dependency and locate(dependency) is not None)
    bootstrap = 'deploy/qualification/bootstrap.py'
    sources['qualification_bootstrap'] = dict(path=bootstrap,
        sha256=sha256(read_regular(root, bootstrap, limit=65536)))
    return dict(sorted(sources.items()))


def protected_path(path, *, owner=0):
    path = Path(path)
    for candidate in (path, *path.parents):
        info = candidate.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != owner or info.st_mode & 0o022:
            raise ValueError('administrator-owned immutable path required: ' + str(candidate))


def observe_runtime(root, role):
    root = Path(root)
    return dict(python_version=platform.python_version(), platform=sys.platform,
        dependency_lock_sha256=sha256(read_regular(root, 'requirements-ops.lock', limit=1024 * 1024)),
        signing_configuration_sha256=sha256(read_regular(root,SIGNING_CONFIGURATION,limit=1024 * 1024)),
        sources=source_closure(root, role))


def locked_versions(raw):
    versions = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith(('#', '--hash=')):
            continue
        match = re.fullmatch(r'([A-Za-z0-9_.-]+)==([^\s;\\]+)\s*\\?', line)
        if match is None or match[1] in versions:
            raise ValueError('unsupported or duplicate locked dependency')
        versions[match[1]] = match[2]
    if not versions:
        raise ValueError('nonempty locked dependency inventory required')
    return versions


def measure_runtime(root, role, release_bytes):
    if sys.platform != 'linux' or not sys.flags.isolated:
        raise ValueError('isolated Linux interpreter required')
    root = Path(root)
    protected_path(root)
    release = parse_canonical_json(release_bytes, label='installed release')
    observed = observe_runtime(root, role)
    if observed != release['runtime_manifests'][role]:
        raise ValueError('actual process source/runtime manifest differs')
    for item in observed['sources'].values():
        protected_path(root / item['path'])
    bootstrap = Path(sys.modules['__main__'].__file__)
    protected_path(bootstrap)
    if sha256(read_regular(bootstrap.parent, bootstrap.name, limit=65536)) != observed['sources']['qualification_bootstrap']['sha256']:
        raise ValueError('installed bootstrap differs')
    for name, module in tuple(sys.modules.items()):
        if name in observed['sources']:
            if Path(module.__file__).resolve() != (root / observed['sources'][name]['path']).resolve():
                raise ValueError('loaded ordinary module origin differs')
    protected_path(Path(sys.prefix))
    # The locked environment is installed by the administrator. Verify actual
    # versions rather than treating the presence of the lock as an installation.
    for name, version in locked_versions((root / 'requirements-ops.lock').read_text(encoding='utf-8')).items():
        if metadata.version(name) != version:
            raise ValueError('installed dependency version differs: ' + name)
    protected_path(root / SIGNING_CONFIGURATION)
    signing = locked_versions(read_regular(root,SIGNING_CONFIGURATION,limit=1024*1024).decode('utf-8'))
    if 'cryptography' not in signing or metadata.version('cryptography') != signing['cryptography']:
        raise ValueError('installed canonical signing dependency version differs')
    for directory, subdirectories, filenames in os.walk(sys.prefix, followlinks=False):
        for name in (*subdirectories, *filenames):
            candidate = Path(directory) / name
            if candidate.is_symlink():
                protected_path(candidate.resolve(strict=True))
            else:
                info = candidate.lstat()
                if info.st_uid != 0 or info.st_mode & 0o022:
                    raise ValueError('installed environment contains mutable files')
    return sha256(encoded(observed))


def load_instance(path):
    protected_path(path)
    return parse_canonical_json(read_regular(Path(path).parent, Path(path).name, limit=65536), label='protected instance')
