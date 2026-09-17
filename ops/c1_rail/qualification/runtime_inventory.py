"""Observe loaded source origins; retain bytes for a separately captured executor.

This receipt is source provenance, not approval or proof that mutable Python
globals execute those bytes. Consumers must capture execution from these bytes
or independently validate their live code objects before claiming that binding.
``dynamic_code_sites`` records recognizable dynamic import/execution calls for
consumer review. It is not an exhaustive analysis of arbitrary Python aliases
or generated code. A reviewed dynamic loader needs its own closed dependency
map and observation of every mandated port; otherwise closure is unresolved.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from importlib.util import resolve_name
from pathlib import Path
import sys
from types import FunctionType, ModuleType

from .contract import ValidatedFrozenContract


REPOSITORY_ROOT=Path(__file__).resolve().parents[3]
_FIRST_PARTY=('c1_rail','c1_signal_daemon','mc','scripts','ops','core')
# Exact names assigned by book_adapters.load_qualification_adapters. These
# roles remain executable source regardless of their retained filename suffix.
_PORT_MODULES={
    'aegis_runtime_port':'fp_qualification_port_aegis_6j',
    'striker_runtime_port':'fp_qualification_port_dj30_mym_p250',
    'vanguard_runtime_port':'fp_qualification_port_vanguard_mgc',
    'orb_runtime_port':'fp_qualification_port_orb_mnq_v7',
}


@dataclass(frozen=True)
class ModuleObservation:
    role: str
    module_name: str
    origin: str
    sha256: str
    source_bytes: bytes
    dependencies: tuple[str,...]
    dynamic_code_sites: tuple[tuple[int,str],...]


@dataclass(frozen=True)
class DataBinding:
    role: str
    artifact_path: str
    sha256: str
    source_bytes: bytes


@dataclass(frozen=True)
class RuntimeInventoryReceipt:
    contract_sha256: str
    modules: tuple[ModuleObservation,...]
    data_bindings: tuple[DataBinding,...]
    runtime_load_sha256: tuple[tuple[str,str],...]


def _module_name(relative):
    parts=list(relative.with_suffix('').parts)
    if parts[0]=='core' or parts[:2] in (['ops','c1_rail'],['ops','c1_signal_daemon']):
        parts.pop(0)
    if parts[-1]=='__init__':parts.pop()
    if not parts or any(not part.isidentifier() for part in parts):
        raise ValueError('canonical Python artifact path required')
    return '.'.join(parts)


def collect_runtime_inventory(contract, *, loaded_modules, retained_source_bytes, artifact_root=None):
    """Read each actual origin once and verify the declared first-party closure.

    ``loaded_modules`` maps frozen code roles to their actual module objects,
    never to caller-supplied hashes. Data roles are retained byte bindings only.
    Deferred first-party imports must already be loaded to establish the full
    execution closure; otherwise collection refuses to claim completeness.
    ``artifact_root`` is the same retained artifact root supplied to production
    source preparation. Relative port-loader origins resolve there; ordinary
    imported code must originate in REPOSITORY_ROOT. Neither origin may escape
    its respective root. The four closed port roles are always code. G1's authoritative
    classification for additional mandatory code roles remains a prerequisite
    to using this source-provenance receipt as complete production inventory.
    """
    if type(contract) is not ValidatedFrozenContract:
        raise TypeError('exact validated frozen contract required')
    artifacts={item.role:item for item in contract.artifacts}
    if len(artifacts)!=len(contract.artifacts) or set(artifacts)!=set(contract.runtime_load_sha256):
        raise ValueError('complete frozen artifact/runtime inventory required')
    if set(retained_source_bytes)!=set(artifacts) or any(type(v) is not bytes for v in retained_source_bytes.values()):
        raise ValueError('complete retained immutable source/data bytes required')
    repository=REPOSITORY_ROOT.resolve(strict=True)
    root=Path(repository if artifact_root is None else artifact_root).resolve(strict=True)
    if not root.is_dir():raise ValueError('retained artifact root must be a directory')
    resolved={}
    def origin(raw):
        if not isinstance(raw,str) or not raw:raise ValueError('actual module origin required')
        if raw not in resolved:
            candidate=Path(raw)
            resolved[raw]=(candidate if candidate.is_absolute() else root/candidate).resolve(strict=True)
        return resolved[raw]
    expected={};data=[]
    for role,item in artifacts.items():
        digest=hashlib.sha256(retained_source_bytes[role]).hexdigest()
        if digest!=item.sha256 or digest!=contract.runtime_load_sha256[role]:
            raise ValueError('retained source/data differs from frozen runtime identity')
        relative=Path(item.path)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('canonical repository-relative artifact path required')
        if relative.suffix=='.py' or role in _PORT_MODULES:
            source_root=root if role in _PORT_MODULES else repository
            path=origin(str(source_root/relative))
            if not path.is_relative_to(source_root):raise ValueError('code origin escapes designated root')
            expected[role]=(_PORT_MODULES[role] if role in _PORT_MODULES else _module_name(relative),path)
        else:
            data.append(DataBinding(role,item.path,digest,retained_source_bytes[role]))
    uses_ports=bool(set(artifacts)&set(_PORT_MODULES)) or any(
        name=='c1_signal_daemon.book_adapters' for name,_ in expected.values())
    if uses_ports and not set(_PORT_MODULES)<=set(expected):
        raise ValueError('reviewed qualification loader requires all four port roles')
    if set(loaded_modules)!=set(expected):raise ValueError('every frozen code role requires an actual loaded module')
    by_name={};by_origin={};sources={}
    for role,(name,path) in expected.items():
        module=loaded_modules[role]
        if type(module) is not ModuleType or module.__name__!=name or sys.modules.get(name) is not module:
            raise ValueError('actual canonical loaded module object required')
        actual=origin(getattr(module,'__file__',None))
        spec=getattr(module,'__spec__',None)
        retained_port=role in _PORT_MODULES
        if (spec is None and not retained_port) or (spec is not None and spec.name!=name):
            raise ValueError('import specification canonical name differs')
        expected_package = name if path.name == '__init__.py' else name.rpartition('.')[0]
        if module.__package__ != expected_package:
            raise ValueError('canonical module package identity differs')
        if actual!=path or (spec is not None and origin(spec.origin)!=actual):
            raise ValueError('actual module origin differs from frozen artifact path')
        if name in by_name or actual in by_origin:raise ValueError('duplicate code role/origin alias')
        by_name[name]=role;by_origin[actual]=name
        if actual not in sources:sources[actual]=actual.read_bytes()
        if sources[actual]!=retained_source_bytes[role]:raise ValueError('actual source bytes differ from retained frozen source')
    # Inspect only aliases of these origins, not unrelated pytest modules.
    for alias,module in tuple(sys.modules.items()):
        raw=getattr(module,'__file__',None) if type(module) is ModuleType else None
        if not raw:continue
        try:path=origin(raw)
        except (OSError,ValueError):continue
        if path in by_origin and (alias!=by_origin[path] or module is not loaded_modules[by_name[by_origin[path]]]):
            raise ValueError('same-origin sys.modules alias is forbidden')

    def first_party(name):
        if name in by_name or name in _PORT_MODULES.values() or name.split('.')[0] in _FIRST_PARTY:return True
        module=sys.modules.get(name)
        if type(module) is not ModuleType or not getattr(module,'__file__',None):return False
        try:
            path=origin(module.__file__)
            return path.is_relative_to(root) or path.is_relative_to(repository)
        except (OSError,ValueError):return False

    observations=[]
    for role,(name,path) in expected.items():
        module=loaded_modules[role];dependencies=set()
        def require(dependency):
            if dependency==name or not first_party(dependency):return
            if dependency not in by_name:
                raise ValueError(f'first-party dependency {dependency} absent from loaded code inventory')
            dependencies.add(dependency)
        for value in tuple(vars(module).values()):
            if type(value) is ModuleType:require(value.__name__)
            elif isinstance(value,(FunctionType,type)):
                owner=getattr(value,'__module__','')
                if owner:require(owner)
                if type(value) is FunctionType and first_party(owner):
                    owner_module=sys.modules.get(owner)
                    # Decorators such as contextlib.contextmanager legitimately
                    # retain wrapper globals while preserving __module__ and
                    # __name__. Bind the imported object to the exact canonical
                    # owner module attribute instead of assuming raw globals.
                    same_module = owner == name and value.__globals__ is vars(module)
                    canonical_object = (owner_module is not None
                                        and getattr(owner_module, value.__name__, None) is value)
                    if not (same_module or canonical_object):
                        raise ValueError(
                            f'imported function {owner}.{value.__qualname__} differs '
                            f'from actual canonical module object while inspecting {name}')
        tree=ast.parse(sources[path],filename=str(path))
        dynamic_sites=[]
        dynamic_names={'__import__','import_module','spec_from_file_location','exec_module','exec','eval','compile'}
        imported_dynamic=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom):
                imported_dynamic.update(alias.asname or alias.name for alias in node.names if alias.name in dynamic_names)
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                for alias in node.names:require(alias.name)
            elif isinstance(node,ast.ImportFrom):
                base=node.module or ''
                if node.level:
                    if not module.__package__:
                        # A flat canonical module cannot execute this package-relative
                        # branch. Its explicit absolute fallback is inspected separately.
                        continue
                    try:
                        base=resolve_name('.'*node.level+base,module.__package__)
                    except ImportError:
                        # The exact loaded package identity was checked above;
                        # a beyond-root relative branch cannot execute in this
                        # canonical import mode. Inspect its explicit fallback.
                        continue
                if base:require(base)
                for alias in node.names:
                    candidate=base+'.'+alias.name
                    if candidate in sys.modules:require(candidate)
            elif isinstance(node,ast.Call):
                call=node.func
                label=call.id if isinstance(call,ast.Name) else call.attr if isinstance(call,ast.Attribute) else ''
                if label in dynamic_names or label in imported_dynamic:
                    dynamic_sites.append((node.lineno,ast.unparse(call)))
        observations.append(ModuleObservation(role,name,str(path),hashlib.sha256(sources[path]).hexdigest(),
                                               sources[path],tuple(sorted(dependencies)),tuple(sorted(dynamic_sites))))
    return RuntimeInventoryReceipt(contract.contract_sha256,tuple(sorted(observations,key=lambda r:r.role)),
        tuple(sorted(data,key=lambda r:r.role)),tuple(sorted(contract.runtime_load_sha256.items())))
