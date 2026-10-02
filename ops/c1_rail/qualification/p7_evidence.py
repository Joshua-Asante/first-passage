"""T00 P7 evidence: pinned bootstrap, loaded-set closure and acceptance by reconstruction.

Design rev 4.2 (docs/superpowers/specs/2026-09-30-t00-source-only-contract-design.md
§2.5a–§2.5b). A P7 run is one isolated child interpreter launched only as
``python -I -S -B -c P7_BOOTSTRAP``. The bootstrap installs an import audit hook
and a recording finder before any first-party import, inserts the locked
site-packages itself (no ``site``, ``.pth`` or customization module runs), then
runs ``p7_driver`` through ``runpy``. A record is accepted only when a fresh
re-execution over the current bytes reproduces it outside the volatile fields.

P7 output is never fed to MC, the screen or any qualification stage (P7-closure
packet §6); that rule is procedural, not claimed to be enforced here.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

RECORD_SCHEMA = 't00-p7-evidence/v1'
EVIDENCE_LABEL = 'P7 producer-faithfulness evidence; not qualification, screen, GO/NO-GO or F1 evidence'
# Exactly the fields that may differ between two runs over identical inputs (§2.5b(2)).
VOLATILE_FIELDS = ('run_started_at', 'run_finished_at', 'host_run_id')
P7_SITE_PACKAGES_RELATIVE = {'nt': 'Lib/site-packages', 'posix': 'lib/python{major}.{minor}/site-packages'}

# Revision 4.3 (a): modules a P7 run never needs, matched by exact name or
# package prefix only. runner and mc.simulation load with stubbed entry points.
P7_FORBIDDEN_MODULES = (
    'c1_rail.qualification.part_a', 'c1_rail.qualification.bracket', 'c1_rail.qualification.benchmark',
    'c1_rail.qualification.benchmark_part_a', 'c1_rail.qualification.production',
    'c1_rail.qualification.orchestration', 'c1_rail.qualification.result_adjudication',
    'c1_rail.qualification.seal', 'c1_rail.qualification.execution',
)


def forbidden_module(name):
    return any(name == module or name.startswith(module + '.') for module in P7_FORBIDDEN_MODULES)


# The inline bootstrap. Everything before ``runpy`` uses only builtins, ``sys``
# and stdlib modules recorded as stdlib; nothing first-party runs unrecorded.
P7_BOOTSTRAP = r'''
import sys


def _p7_bootstrap():
    argv = list(getattr(sys, 'orig_argv', ()))
    if '-c' not in argv or len(sys.argv) < 8:
        raise SystemExit('P7_BOOTSTRAP_MISMATCH: launch only through p7_evidence.run_p7')
    bootstrap_text = argv[argv.index('-c') + 1]
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise SystemExit('P7_BOOTSTRAP_MISMATCH: -I -S -B are required')

    class State:
        pass
    state = State()
    state.refusals = []
    state.audited_imports = []
    state.first_party, state.third_party, state.stdlib, state.ports = {}, {}, set(), {}
    state.loader_codes, state.compiling = set(), set()
    state.code_root = None

    def refuse(code, detail):
        state.refusals.append(code + ': ' + detail)
        return RuntimeError(code + ': ' + detail)

    def resolve(filename):
        # Absolute first-party paths only; relative names are ports or generated code.
        if not isinstance(filename, str) or not _os.path.isabs(filename):
            return None
        root = state.code_root
        real = _os.path.realpath(filename)
        if root and _os.path.isfile(real) and (real + _os.sep).startswith(root + _os.sep):
            return real
        return None

    def own_installed_source(filename, raw):
        # A site-package or stdlib module compiling exactly its own file's bytes.
        # Under the fresh bytecode prefix every source module compiles, and an
        # empty installed __init__.py shares its digest with any empty tracked
        # first-party file; it is not first-party code.
        if not isinstance(filename, str) or not _os.path.isabs(filename):
            return False
        real = _os.path.realpath(filename)
        if not _os.path.isfile(real) or not any(
                (real + _os.sep).startswith(root.rstrip(_os.sep) + _os.sep) for root in state.installed_roots):
            return False
        with open(real, 'rb') as handle:
            return handle.read() == raw

    def audit(event, args):
        if event == 'import':
            state.audited_imports.append(args[0])
        elif event == 'compile':
            source, filename = args[0], args[1]
            if state.code_root is None or (isinstance(filename, str) and filename in state.compiling):
                return
            raw = source.encode('utf-8') if isinstance(source, str) else bytes(source)                 if isinstance(source, (bytes, bytearray)) else None
            if raw is not None and _hashlib.sha256(raw).hexdigest() in state.first_party_hashes \
                    and not own_installed_source(filename, raw):
                raise refuse('P7_UNAUDITED_EXEC', 'compile of first-party file bytes outside the recording loader: '
                             + repr(filename))
            real = resolve(filename)
            if real is not None:
                raise refuse('P7_UNAUDITED_EXEC', 'compile of first-party bytes outside the recording loader: ' + real)
            if real is None and isinstance(source, (bytes, bytearray)) and isinstance(filename, str) \
                    and not _os.path.isabs(filename) and not filename.startswith('<'):
                state.ports[filename.replace('\\', '/')] = _hashlib.sha256(bytes(source)).hexdigest()
        elif event == 'exec':
            code = args[0]
            if state.code_root is None or not hasattr(code, 'co_filename'):
                return
            real = resolve(code.co_filename)
            if real is not None and id(code) not in state.loader_codes:
                raise refuse('P7_UNAUDITED_EXEC', 'exec of first-party code outside the recording loader: ' + real)

    sys.addaudithook(audit)
    import os as _os
    # -B stops cache writes, not cache reads: a timestamp-valid or unchecked
    # __pycache__ .pyc beside a hashed .py would run instead of the hashed bytes.
    # A fresh, never-created prefix makes every source module compile from the
    # source the finder hashes (Codex P1 on #594).
    state.pycache_prefix = _os.path.join(
        _os.environ.get('TEMP') or _os.environ.get('TMPDIR') or '/tmp', 'p7-no-pycache-' + _os.urandom(16).hex())
    if _os.path.exists(state.pycache_prefix):
        raise SystemExit('P7_BOOTSTRAP_MISMATCH: bytecode cache prefix is not fresh')
    sys.pycache_prefix = state.pycache_prefix
    import hashlib as _hashlib
    import subprocess as _subprocess
    import importlib.machinery as _machinery

    state.bootstrap_sha256 = _hashlib.sha256(bootstrap_text.encode('utf-8')).hexdigest()
    code_root = _os.path.realpath(sys.argv[1])
    relative = {'nt': 'Lib/site-packages',
                'posix': 'lib/python{0}.{1}/site-packages'.format(*sys.version_info[:2])}[_os.name]
    # Under -S the venv's pyvenv.cfg is never applied to sys.prefix, so the
    # environment root is derived from the interpreter binding itself.
    venv = _os.path.dirname(_os.path.dirname(_os.path.abspath(sys.executable)))
    prefix = venv if _os.path.isfile(_os.path.join(venv, 'pyvenv.cfg')) else sys.prefix
    site = _os.path.realpath(_os.path.join(prefix, *relative.split('/')))
    base = _os.path.realpath(sys.base_prefix)
    if _os.name == 'nt':
        stdlib_dirs = [_os.path.join(base, 'Lib'), _os.path.join(base, 'DLLs')]
    else:
        version = 'python{0}.{1}'.format(*sys.version_info[:2])
        stdlib_dirs = [_os.path.join(base, 'lib', version), _os.path.join(base, 'lib', version, 'lib-dynload')]
    stdlib_dirs = [_os.path.realpath(d) for d in stdlib_dirs]
    state.site_packages_path = site
    state.installed_roots = [site] + stdlib_dirs
    state.unexecuted_pth = sorted(
        (name, _hashlib.sha256(open(_os.path.join(site, name), 'rb').read()).hexdigest())
        for name in (_os.listdir(site) if _os.path.isdir(site) else ()) if name.endswith('.pth'))

    def git(*args):
        return _subprocess.run(['git', '-C', code_root, *args], capture_output=True, text=True, check=True).stdout
    try:
        state.code_head = git('rev-parse', 'HEAD').strip()
        dirty = git('status', '--porcelain', '--untracked-files=no').strip()
    except Exception as exc:
        raise SystemExit('P7_TREE_DIRTY: code root is not a readable git checkout: ' + repr(exc))
    if dirty:
        raise SystemExit('P7_TREE_DIRTY: tracked changes in the code root at start')
    state.git = git
    state.first_party_hashes = {
        _hashlib.sha256(open(_os.path.join(code_root, rel), 'rb').read()).hexdigest()
        for rel in git('ls-files', '-z', '--', '*.py').split(chr(0)) if rel}

    forbidden = FORBIDDEN_MODULES
    state.code_root = code_root

    def under(path, root):
        return (path + _os.sep).startswith(root.rstrip(_os.sep) + _os.sep)

    class FirstPartyLoader:
        def __init__(self, name, path, package):
            self.name, self.path, self.package = name, path, package

        def create_module(self, spec):
            return None

        def is_package(self, fullname):
            return self.package

        def get_source(self, fullname):
            return open(self.path, 'rb').read().decode('utf-8')

        def get_code(self, fullname):
            raw = open(self.path, 'rb').read()
            digest = _hashlib.sha256(raw).hexdigest()
            rel = _os.path.relpath(self.path, code_root).replace(_os.sep, '/')
            seen = state.first_party.get(self.name)
            if seen is not None and seen['sha256'] != digest:
                raise refuse('P7_SOURCE_CHANGED_DURING_RUN', rel)
            state.first_party[self.name] = {'path': rel, 'sha256': digest}
            state.compiling.add(self.path)
            try:
                code = compile(raw, self.path, 'exec', dont_inherit=True)
            finally:
                state.compiling.discard(self.path)
            state.loader_codes.add(id(code))
            state.keep = getattr(state, 'keep', [])
            state.keep.append(code)
            return code

        def exec_module(self, module):
            exec(self.get_code(module.__name__), module.__dict__)

    class RecordingFinder:
        def find_spec(self, name, path=None, target=None):
            if name in forbidden or any(name.startswith(prefix + '.') for prefix in forbidden):
                raise refuse('P7_FORBIDDEN_IMPORT', name)
            spec, source = None, None
            for finder in sys.meta_path:
                if finder is self or not hasattr(finder, 'find_spec'):
                    continue
                spec = finder.find_spec(name, path, target)
                if spec is not None:
                    source = finder
                    break
            if spec is None:
                return None
            origin = spec.origin
            if origin in ('built-in', 'frozen'):
                state.stdlib.add(name)
                return spec
            if origin is None and not spec.submodule_search_locations:
                # A virtual module served by an installed importer (e.g. six.moves):
                # classified by where that importer's own code lives.
                owner = sys.modules.get(type(source).__module__)
                owner_file = _os.path.realpath(getattr(owner, '__file__', '') or '')
                if owner_file and under(owner_file, site):
                    state.third_party.setdefault(name, {'path': None, 'sha256': None})
                    return spec
                raise refuse('P7_ORIGIN_OUTSIDE_ROOT', name + ' virtual module from an unrecorded importer')
            if origin is None:  # namespace package
                locations = [_os.path.realpath(p) for p in (spec.submodule_search_locations or ())]
                if locations and all(under(p, code_root) for p in locations):
                    state.first_party.setdefault(name, {'path': None, 'sha256': None})
                    return spec
                if locations and all(under(p, site) for p in locations):
                    state.third_party.setdefault(name, {'path': None, 'sha256': None})
                    return spec
                raise refuse('P7_ORIGIN_OUTSIDE_ROOT', name + ' namespace outside allowed roots')
            real = _os.path.realpath(origin)
            if under(real, site):
                # A sourceless .pyc/.pyd origin is hashed as the executed bytes; a
                # source origin must not resolve to a cache outside the fresh prefix.
                cached = getattr(spec, 'cached', None)
                if cached and (sys.pycache_prefix != state.pycache_prefix
                               or not under(_os.path.abspath(cached), state.pycache_prefix)):
                    raise refuse('P7_UNBOUND_BYTECODE', name + ' would load cached bytecode ' + cached)
                state.third_party[name] = {'path': _os.path.relpath(real, site).replace(_os.sep, '/'),
                                           'sha256': _hashlib.sha256(open(real, 'rb').read()).hexdigest()}
                return spec
            if any(under(real, d) for d in stdlib_dirs):
                state.stdlib.add(name)
                return spec
            if under(real, code_root) and real.endswith('.py'):
                package = spec.submodule_search_locations is not None
                loader = FirstPartyLoader(name, real, package)
                new = _machinery.ModuleSpec(name, loader, origin=real, is_package=package)
                if package:
                    new.submodule_search_locations = list(spec.submodule_search_locations)
                new.has_location = True
                return new
            raise refuse('P7_ORIGIN_OUTSIDE_ROOT', name + ' from ' + real)

    for name in list(state.audited_imports):
        module = sys.modules.get(name)
        origin = getattr(getattr(module, '__spec__', None), 'origin', None)
        if origin not in (None, 'built-in', 'frozen') and not any(
                under(_os.path.realpath(origin), d) for d in stdlib_dirs):
            raise SystemExit('P7_ORIGIN_OUTSIDE_ROOT: pre-finder import ' + name)
        state.stdlib.add(name)
    sys.meta_path.insert(0, RecordingFinder())
    sys.dont_write_bytecode = True
    roots = [_os.path.join(code_root, *part.split('/')) for part in ('core', 'lab', 'ops', 'ops/c1_rail', 'ops/c1_signal_daemon')]
    sys.path[:0] = roots + [code_root]
    sys.path.append(site)
    sys.p7_recorder = state
    # Revision 4.3 (b): runner and mc.simulation load for their types; their kernel
    # entry points are stubbed in this process only and checked again at record time.
    import importlib as _importlib
    runner = _importlib.import_module('c1_rail.qualification.runner')
    simulation = _importlib.import_module('mc.simulation')
    state.stubs = []

    def make_stub(label):
        def stub(*args, **kwargs):
            raise refuse('P7_FORBIDDEN_CALL', label)
        return stub
    for module, attr in ((runner, 'evaluate_replay'), (runner, 'run_synthetic_stage'), (runner, '_run_stage'),
                         (runner, 'simulate_path'), (simulation, 'simulate_path')):
        stub = make_stub(module.__name__ + '.' + attr)
        setattr(module, attr, stub)
        state.stubs.append((module, attr, stub))
    import runpy
    runpy.run_module('c1_rail.qualification.p7_driver', run_name='__main__', alter_sys=False)


_p7_bootstrap()
'''.replace('FORBIDDEN_MODULES', repr(P7_FORBIDDEN_MODULES))
P7_BOOTSTRAP_SHA256 = hashlib.sha256(P7_BOOTSTRAP.encode('utf-8')).hexdigest()


class P7Refusal(ValueError):
    """A P7 run or acceptance is refused; the message leads with its code."""


def site_packages_relative():
    return P7_SITE_PACKAGES_RELATIVE[os.name].format(major=sys.version_info[0], minor=sys.version_info[1])


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')


def sha256_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def run_p7(*, code_root, contract_path, approval_path, registry_path, artifact_root, path_spec_path, out_path,
           bootstrap=None, python=None, timeout=1800):
    """The only launcher: ``python -I -S -B -c P7_BOOTSTRAP`` in a fresh process."""
    command = [str(python or sys.executable), '-I', '-S', '-B', '-c', P7_BOOTSTRAP if bootstrap is None else bootstrap,
               str(Path(code_root).resolve()), str(contract_path), str(approval_path), str(registry_path),
               str(Path(artifact_root).resolve()), str(path_spec_path), str(out_path)]
    workdir = Path(out_path).resolve().parent
    return subprocess.run(command, capture_output=True, text=True, cwd=workdir, timeout=timeout)


def comparable(record_bytes):
    doc = json.loads(record_bytes)
    for field in VOLATILE_FIELDS:
        doc.pop(field, None)
    return canonical(doc)


def current_interpreter_binding(code_root):
    """The acceptor's own interpreter binding, derived exactly as the bootstrap derives it."""
    venv = os.path.dirname(os.path.dirname(os.path.abspath(sys.executable)))
    prefix = venv if os.path.isfile(os.path.join(venv, 'pyvenv.cfg')) else sys.prefix
    site = os.path.realpath(os.path.join(prefix, *site_packages_relative().split('/')))
    pth = sorted((name, sha256_bytes(Path(site, name).read_bytes()))
                 for name in (os.listdir(site) if os.path.isdir(site) else ()) if name.endswith('.pth'))
    lock = Path(code_root) / 'requirements-ops.lock'
    return {
        'interpreter_sha256': sha256_bytes(Path(sys.executable).read_bytes()),
        'base_interpreter_sha256': sha256_bytes(Path(getattr(sys, '_base_executable', sys.executable)).read_bytes()),
        'version': sys.version, 'cache_tag': sys.implementation.cache_tag,
        'lock_sha256': sha256_bytes(lock.read_bytes()) if lock.is_file() else None,
        'site_packages_path': site,
        'unexecuted_pth': [{'name': name, 'sha256': digest} for name, digest in pth],
    }


@dataclass(frozen=True)
class AcceptedP7Record:
    code_closure_sha256: str
    contract_sha256: str
    approval_sha256: str
    accepted_at: datetime


def _current_bytes_check(doc, *, code_root, artifact_root):
    """§2.5b(3): re-hash every contract artifact and closure file before any launch."""
    contract = json.loads(base64.b64decode(doc['contract_b64']))
    root = Path(artifact_root).resolve()
    for row in contract['artifacts']:
        path = (root / row['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file() or sha256_bytes(path.read_bytes()) != row['sha256']:
            raise P7Refusal(f"P7_EVIDENCE_STALE: artifact {row['role']} differs from the contract digest")
    current = current_interpreter_binding(code_root)
    recorded = doc['interpreter']
    differing = sorted(key for key in set(current) | set(recorded) if current.get(key) != recorded.get(key))
    if differing:
        raise P7Refusal('P7_INTERPRETER_MISMATCH: recorded interpreter binding differs: ' + ', '.join(differing))
    code = Path(code_root).resolve()
    closure = doc['loaded_closure']
    for name, row in closure['first_party'].items():
        if row['path'] is None:
            continue
        path = code / row['path']
        if not path.is_file() or sha256_bytes(path.read_bytes()) != row['sha256']:
            raise P7Refusal(f'P7_EVIDENCE_STALE: first-party module {name} differs from the recorded closure')
    site = Path(doc['interpreter']['site_packages_path'])
    for name, row in closure['third_party'].items():
        if row['path'] is None:
            continue
        path = site / row['path']
        if not path.is_file() or sha256_bytes(path.read_bytes()) != row['sha256']:
            raise P7Refusal(f'P7_EVIDENCE_STALE: third-party module {name} differs from the recorded closure')
    return contract


def accept_p7_record(record_bytes, *, code_root, artifact_root, now, public_keys, python=None):
    """Standalone acceptance: current bytes, re-validation, re-execution, byte comparison."""
    from .contract import ObservedBindings, validate_source_contract
    doc = json.loads(record_bytes)
    if doc.get('schema') != RECORD_SCHEMA:
        raise P7Refusal('P7_RECORD_NOT_REPRODUCED: unsupported record schema')
    if python is not None and Path(python).resolve() != Path(sys.executable).resolve():
        raise P7Refusal('P7_INTERPRETER_MISMATCH: acceptance runs only under the acceptor interpreter itself')
    contract = _current_bytes_check(doc, code_root=code_root, artifact_root=artifact_root)
    contract_bytes = base64.b64decode(doc['contract_b64'])
    approval_bytes = base64.b64decode(doc['approval_b64'])
    observed = ObservedBindings({row['path']: row['sha256'] for row in contract['artifacts']},
                                {row['role']: row['sha256'] for row in contract['artifacts']},
                                contract['effective_settings']['settings_sha256'],
                                contract['effective_settings']['orb_normal_base'])
    validate_source_contract(contract_bytes, approval_bytes, dict(public_keys), observed, now=now)
    with tempfile.TemporaryDirectory(prefix='p7-accept-') as tmp:
        tmp = Path(tmp)
        (tmp / 'contract.json').write_bytes(contract_bytes)
        (tmp / 'approval.json').write_bytes(approval_bytes)
        (tmp / 'registry.json').write_text(json.dumps(
            {key: base64.b64encode(raw).decode() for key, raw in public_keys.items()}), encoding='utf-8')
        (tmp / 'path.json').write_text(json.dumps({'sessions': doc['path']}), encoding='utf-8')
        out = tmp / 'reconstructed.json'
        done = run_p7(code_root=code_root, contract_path=tmp / 'contract.json', approval_path=tmp / 'approval.json',
                      registry_path=tmp / 'registry.json', artifact_root=artifact_root,
                      path_spec_path=tmp / 'path.json', out_path=out, python=python)
        if not out.exists():
            raise P7Refusal('P7_RECORD_NOT_REPRODUCED: re-execution produced no record: ' + done.stderr[-2000:])
        if comparable(out.read_bytes()) != comparable(record_bytes):
            raise P7Refusal('P7_RECORD_NOT_REPRODUCED: the presented record differs from a real run')
    return AcceptedP7Record(doc['code_closure_sha256'], doc['contract_sha256'], doc['approval_sha256'],
                            now.astimezone(timezone.utc))


def finish_record(state, fields, out_path):
    """Exit checks, then one exclusive write of the canonical record (driver only)."""
    if state.refusals:
        raise P7Refusal(state.refusals[0])
    for module, attr, stub in state.stubs:
        if getattr(module, attr, None) is not stub:
            raise P7Refusal(f'P7_FORBIDDEN_CALL: {module.__name__}.{attr} was rebound after stubbing')
    if sys.pycache_prefix != state.pycache_prefix or os.path.exists(state.pycache_prefix):
        raise P7Refusal('P7_UNBOUND_BYTECODE: the fresh bytecode cache prefix was changed or populated during the run')
    code_root = Path(state.code_root)
    for name, row in sorted(state.first_party.items()):
        if row['path'] is not None and sha256_bytes((code_root / row['path']).read_bytes()) != row['sha256']:
            raise P7Refusal(f"P7_SOURCE_CHANGED_DURING_RUN: {row['path']}")
    paths = sorted(row['path'] for row in state.first_party.values() if row['path'] is not None)
    tracked = set(state.git('ls-files', '--', *paths).split()) if paths else set()
    if (state.git('rev-parse', 'HEAD').strip() != state.code_head
            or state.git('status', '--porcelain', '--untracked-files=all', '--', *paths).strip()
            or set(paths) - tracked):
        raise P7Refusal('P7_TREE_DIRTY: recorded first-party files are not clean and tracked at exit')
    from importlib import metadata
    tops = {name.split('.')[0] for name in state.third_party}
    mapping = metadata.packages_distributions()
    distributions = {}
    for top in sorted(tops):
        for dist in mapping.get(top, ()):
            distributions[dist] = {'version': metadata.version(dist)}
    closure = {
        'first_party': dict(sorted(state.first_party.items())),
        'third_party': dict(sorted(state.third_party.items())),
        'distributions': dict(sorted(distributions.items())),
        'stdlib': sorted(state.stdlib),
        'ports': dict(sorted(state.ports.items())),
    }
    lock = code_root / 'requirements-ops.lock'
    interpreter = {
        'interpreter_sha256': sha256_bytes(Path(sys.executable).read_bytes()),
        'base_interpreter_sha256': sha256_bytes(Path(getattr(sys, '_base_executable', sys.executable)).read_bytes()),
        'version': sys.version, 'cache_tag': sys.implementation.cache_tag,
        'lock_sha256': sha256_bytes(lock.read_bytes()) if lock.is_file() else None,
        'site_packages_path': state.site_packages_path,
        'unexecuted_pth': [{'name': name, 'sha256': digest} for name, digest in state.unexecuted_pth],
    }
    record = dict(fields, schema=RECORD_SCHEMA, label=EVIDENCE_LABEL, bootstrap_sha256=state.bootstrap_sha256,
                  code_head=state.code_head, code_tree_clean=True, loaded_closure=closure,
                  code_closure_sha256=sha256_bytes(canonical(closure)), interpreter=interpreter)
    record['run_finished_at'] = datetime.now(timezone.utc).isoformat()
    with open(out_path, 'xb') as handle:
        handle.write(canonical(record))
