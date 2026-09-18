"""Ordinary source closure for synthetic composition fixtures only.

This helper imports ordinary modules, never invokes a private port loader. It
does not issue authority or replace G1's mandatory runtime role declaration.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import importlib
from importlib.util import resolve_name
from pathlib import Path
import sys
from types import FunctionType, ModuleType


ROOT=Path(__file__).resolve().parents[3]
DEFAULT_SEEDS=tuple('c1_rail.qualification.'+name for name in (
    'production_source','production','orchestration','result_adjudication','runtime_inventory'))


@dataclass(frozen=True)
class OrdinaryModule:
    role: str
    name: str
    path: str
    sha256: str
    source_bytes: bytes
    module: ModuleType
    dependencies: tuple[str,...]


def ordinary_runtime_fixture(*, role_modules, seeds=DEFAULT_SEEDS):
    """Collect actual ordinary modules and exact bytes under canonical names.

    Explicit role assignments must be one-to-one. Additional transitive modules
    receive deterministic ``runtime_dependency__<module>`` fixture roles. AST
    traversal includes local/deferred imports without invoking their call sites.
    """
    if len(set(role_modules.values()))!=len(role_modules):
        raise ValueError('multiple roles cannot designate one ordinary module')
    roots=(ROOT/'ops',ROOT/'core',ROOT/'lab',ROOT/'governance',ROOT)
    def locate(name):
        if name.startswith(('fp_port_','fp_qualification_port_')):
            raise ValueError('private ports are outside the ordinary fixture helper')
        relative=Path(*name.split('.'))
        paths=[]
        for root in roots:
            for candidate in (root/relative.with_suffix('.py'),root/relative/'__init__.py'):
                if candidate.is_file():paths.append(candidate.resolve())
        paths=list(dict.fromkeys(paths))
        if len(paths)>1:raise ValueError(f'conflicting canonical source paths for {name}')
        return paths[0] if paths else None

    paths={};sources={};edges={};pending=list(seeds)+list(role_modules.values())
    while pending:
        name=pending.pop()
        if name in paths:continue
        path=locate(name)
        if path is None:raise ValueError(f'ordinary seed/module has no local source: {name}')
        # Reject the alias forms caught by the production collector.
        relative=path.relative_to(ROOT)
        parts=list(relative.with_suffix('').parts)
        if parts[0] in ('core','ops','lab','governance'):parts.pop(0)
        if parts[-1]=='__init__':parts.pop()
        canonical='.'.join(parts)
        if name!=canonical:raise ValueError(f'noncanonical module name {name}, expected {canonical}')
        paths[name]=path;sources[name]=path.read_bytes();edges[name]=set()
        package=name if path.name=='__init__.py' else name.rpartition('.')[0]
        dependencies=set()
        # Package initialization is executable source too.
        for count in range(1,len(name.split('.'))):
            parent='.'.join(name.split('.')[:count])
            if locate(parent) is not None:dependencies.add(parent)
        for node in ast.walk(ast.parse(sources[name],filename=str(path))):
            if isinstance(node,ast.Import):
                dependencies.update(alias.name for alias in node.names if locate(alias.name) is not None)
            elif isinstance(node,ast.ImportFrom):
                base=node.module or ''
                if node.level:
                    try:base=resolve_name('.'*node.level+base,package)
                    except (ImportError,ValueError):
                        # Flat core imports retain package-relative fallback
                        # branches which cannot execute in this canonical mode.
                        continue
                if base and locate(base) is not None:dependencies.add(base)
                for alias in node.names:
                    candidate=base+'.'+alias.name
                    if alias.name!='*' and locate(candidate) is not None:dependencies.add(candidate)
        dependencies.discard(name)
        edges[name]=dependencies;pending.extend(dependencies-paths.keys())

    modules={name:importlib.import_module(name) for name in sorted(paths)}
    loaded_dependencies=set()
    for name,module in modules.items():
        if type(module) is not ModuleType or Path(module.__file__).resolve()!=paths[name]:
            raise ValueError(f'loaded ordinary origin differs for {name}')
        if paths[name].read_bytes()!=sources[name]:raise ValueError('source changed during fixture capture')
        for value in tuple(vars(module).values()):
            dependency=value.__name__ if type(value) is ModuleType else getattr(value,'__module__',None) if isinstance(value,(FunctionType,type)) else None
            if dependency and dependency!=name and locate(dependency) is not None and dependency not in modules:
                loaded_dependencies.add(dependency)
    if loaded_dependencies:
        # Test collection can already have imported package children. Capture
        # their real closure before signing, rather than pretending the loaded
        # package is identical to a fresh minimal import. Recapture every byte
        # and retain the same canonical-origin and alias checks below.
        return ordinary_runtime_fixture(role_modules=role_modules,
            seeds=tuple(sorted(set(paths)|loaded_dependencies)))
    actual_origins={path:name for name,path in paths.items()}
    for alias,module in tuple(sys.modules.items()):
        raw=getattr(module,'__file__',None) if type(module) is ModuleType else None
        if not raw:continue
        try:path=Path(raw).resolve()
        except (OSError,ValueError):continue
        if path in actual_origins and alias!=actual_origins[path]:
            raise ValueError(f'ordinary loaded source alias: {alias}')
    roles={name:role for role,name in role_modules.items()}
    rows=[];used=set()
    for name in sorted(paths):
        role=roles.get(name,'runtime_dependency__'+name.replace('.','__'))
        if role in used:raise ValueError('explicit and generated dependency roles conflict')
        used.add(role)
        rows.append(OrdinaryModule(role,name,paths[name].relative_to(ROOT).as_posix(),
            hashlib.sha256(sources[name]).hexdigest(),sources[name],modules[name],tuple(sorted(edges[name]))))
    return tuple(rows)


if __name__=='__main__':
    for item in ordinary_runtime_fixture(role_modules={}):
        print(item.name+'\t'+item.path)
