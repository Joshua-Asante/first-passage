"""Source-only sources never reach qualification consumers (spec §2.6, A10/A10b)."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from test_source_contract import NOW, build_source_case, refused

OPS = Path(__file__).resolve().parents[3] / 'ops'
# Modules that may hold a source-only source without qualification authorization.
SOURCE_ONLY_ALLOWLIST = {'c1_rail/qualification/production_source.py', 'c1_rail/qualification/p7_driver.py'}
GUARDS = {'verify_for', 'require_validated_frozen_contract'}
CAPABILITIES = {'replay', 'replay_bracket', 'proof'}


def _root_name(node):
    while isinstance(node, ast.Attribute):
        node = node.value
    return node.id if isinstance(node, ast.Name) else ''


def unguarded_consumers(root: Path, allowlist=SOURCE_ONLY_ALLOWLIST):
    """Outermost functions that name ProductionSource, or call a source capability,
    without a verify_for / require_validated_frozen_contract call in the same function."""
    findings = []
    for path in sorted(root.rglob('*.py')):
        relative = path.relative_to(root).as_posix()
        if relative in allowlist:
            continue
        tree = ast.parse(path.read_text(encoding='utf-8'), filename=relative)
        for top in ast.walk(tree):
            if not isinstance(top, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            uses, guarded = False, False
            for node in ast.walk(top):
                if isinstance(node, ast.Name) and node.id == 'ProductionSource':
                    uses = True
                if isinstance(node, ast.alias) and node.name == 'ProductionSource':
                    uses = True
                if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr in CAPABILITIES and 'source' in _root_name(node.func).lower()):
                    uses = True
                if isinstance(node, ast.Call):
                    name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, 'id', '')
                    guarded = guarded or name in GUARDS
            if uses and not guarded:
                findings.append(f'{relative}:{top.lineno}:{top.name}')
    # A nested function inherits its enclosing function's guard.
    nested = set()
    for path in sorted(root.rglob('*.py')):
        relative = path.relative_to(root).as_posix()
        tree = ast.parse(path.read_text(encoding='utf-8'))
        for outer in ast.walk(tree):
            if isinstance(outer, (ast.FunctionDef, ast.AsyncFunctionDef)):
                guarded = any(isinstance(n, ast.Call) and (getattr(n.func, 'attr', None) in GUARDS
                                                          or getattr(n.func, 'id', None) in GUARDS)
                              for n in ast.walk(outer))
                if guarded:
                    for inner in ast.walk(outer):
                        if inner is not outer and isinstance(inner, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            nested.add(f'{relative}:{inner.lineno}:{inner.name}')
    return [finding for finding in findings if finding not in nested]


def test_every_production_source_consumer_is_allowlisted_or_verified(tmp_path):  # A10b
    assert unguarded_consumers(OPS) == []
    planted = tmp_path / 'ops' / 'planted.py'
    planted.parent.mkdir()
    planted.write_text('def leak(source, path):\n    return source.replay_bracket(path)\n', encoding='utf-8')
    guarded = tmp_path / 'ops' / 'guarded.py'
    guarded.write_text('def ok(source, contract, path):\n    source.verify_for(contract)\n'
                       '    return source.replay_bracket(path)\n', encoding='utf-8')
    assert unguarded_consumers(tmp_path / 'ops', allowlist=set()) == ['planted.py:1:leak']


def test_source_only_source_is_refused_by_qualification_consumers(tmp_path, monkeypatch):  # A10
    from composition_fixture import build_verified_composition
    from c1_rail.qualification import production_source
    from c1_rail.qualification.execution import compute, evidence
    composition = build_verified_composition(tmp_path / 'f1')
    composition.source.verify_for(composition.contract)  # twin: the F1 source passes
    monkeypatch.setattr(production_source, '_now', lambda: NOW)
    case = build_source_case(tmp_path / 'source', monkeypatch)
    source = production_source.ProductionSource.build(case.validate(), artifact_root=case.root)
    refused('SOURCE_ONLY_NOT_QUALIFICATION', lambda: source.verify_for(composition.contract))
    refused('SOURCE_ONLY_NOT_QUALIFICATION', lambda: source.verify_for(source.contract))
    refused('SOURCE_ONLY_NOT_QUALIFICATION',
            lambda: compute._run_checkpoint_compute('n1', composition.contract, source, None))
    refused('SOURCE_ONLY_NOT_QUALIFICATION', lambda: evidence.encode_worker_result(
        SimpleNamespace(contract=composition.contract), 'execution', b'{}', None, (),
        admitted=SimpleNamespace(source=source)))
