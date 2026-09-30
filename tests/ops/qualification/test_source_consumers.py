"""Source-only sources never reach qualification consumers (spec §2.6, A10/A10b).

A10b (Codex code review P1): a use counts as guarded only when a verify_for on the same
object precedes it unconditionally in the function's top-level statement sequence.
"""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from test_source_contract import NOW, build_source_case, refused

OPS = Path(__file__).resolve().parents[3] / 'ops'
# Modules that may hold a source-only source without qualification authorization.
SOURCE_ONLY_ALLOWLIST = {'c1_rail/qualification/production_source.py', 'c1_rail/qualification/p7_driver.py'}
# Reviewed exceptions: (module, qualified function) -> reason.
FUNCTION_ALLOWLIST = {
    ('c1_rail/qualification/production.py', 'ProductionExecutor._replay'):
        'reachable only from run_stage/run_part_a after _admit, whose unconditional verify_for binds '
        'self.source to a ValidatedFrozenContract; _initialize also refuses non-synthetic executors',
}
CAPABILITIES = {'replay', 'replay_bracket', 'proof'}


def _last_name(node):
    if isinstance(node, ast.Attribute):
        return node.attr
    return node.id if isinstance(node, ast.Name) else ''


def _source_like(node):
    return 'source' in _last_name(node).lower()


def _uses(statement):
    """(object, line) uses in a statement, excluding nested function bodies."""
    stack = [statement]
    while stack:
        node = stack.pop()
        if node is not statement and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in CAPABILITIES and _source_like(node.func.value)):
            yield ast.unparse(node.func.value), node.lineno
        if (isinstance(node, ast.Attribute) and node.attr == 'contract' and isinstance(node.ctx, ast.Load)
                and _source_like(node.value)):
            yield ast.unparse(node.value), node.lineno
        stack.extend(ast.iter_child_nodes(node))


def _guarded_by(statement, guard_methods):
    """Objects guarded by an unconditional top-level statement."""
    if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
        return set()
    func = statement.value.func
    if isinstance(func, ast.Attribute) and func.attr == 'verify_for':
        return {ast.unparse(func.value)}
    if (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name) and func.value.id == 'self'
            and func.attr in guard_methods):
        return set(guard_methods[func.attr])
    return set()


def _nested_functions(statement):
    stack = list(ast.iter_child_nodes(statement))
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node
            continue
        stack.extend(ast.iter_child_nodes(node))


def _check(function, qualname, inherited, guard_methods, findings, relative):
    guarded = set(inherited)
    for statement in function.body:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            _check(statement, qualname + '.' + statement.name, guarded, guard_methods, findings, relative)
            continue
        for obj, line in _uses(statement):
            if obj not in guarded and (relative, qualname) not in FUNCTION_ALLOWLIST:
                findings.append(f'{relative}:{line}:{qualname}:{obj}')
        guarded |= _guarded_by(statement, guard_methods)
        for nested in _nested_functions(statement):
            _check(nested, qualname + '.' + nested.name, guarded, guard_methods, findings, relative)


def unguarded_consumers(root: Path, allowlist=SOURCE_ONLY_ALLOWLIST):
    """Each source capability call or ``.contract`` read on a source-like object must be
    preceded, unconditionally and at the function's top-level statement sequence, by a
    ``verify_for`` on the same object (or a same-class method that does so)."""
    findings = []
    for path in sorted(root.rglob('*.py')):
        relative = path.relative_to(root).as_posix()
        if relative in allowlist:
            continue
        tree = ast.parse(path.read_text(encoding='utf-8'), filename=relative)
        scopes = [(tree.body, '')]
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                scopes.append((node.body, node.name + '.'))
        for body, prefix in scopes:
            methods = [n for n in body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            guard_methods = {}
            if prefix:
                for method in methods:
                    objects = set()
                    for statement in method.body:
                        objects |= _guarded_by(statement, {})
                    if objects:
                        guard_methods[method.name] = objects
            for function in methods:
                _check(function, prefix + function.name, set(), guard_methods, findings, relative)
    return findings


def test_every_production_source_consumer_is_allowlisted_or_verified():  # A10b
    assert unguarded_consumers(OPS) == []


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


PLANTED = {
    'use_before_guard': 'def f(source, contract, path):\n    x = source.replay_bracket(path)\n'
                        '    source.verify_for(contract)\n    return x\n',
    'guard_under_if': 'def f(source, contract, path, flag):\n    if flag:\n        source.verify_for(contract)\n'
                      '    return source.replay(path)\n',
    'guard_in_dead_code': 'def f(source, contract, path):\n    return source.proof(path)\n'
                          '    source.verify_for(contract)\n',
    'unguarded_contract_read': 'def f(source):\n    return source.contract\n',
    'guard_on_other_object': 'def f(source, other, contract, path):\n    other.verify_for(contract)\n'
                             '    return source.replay(path)\n',
}
GUARDED_TWINS = {
    'use_before_guard': 'def f(source, contract, path):\n    source.verify_for(contract)\n'
                        '    return source.replay_bracket(path)\n',
    'guard_under_if': 'def f(source, contract, path, flag):\n    source.verify_for(contract)\n'
                      '    if flag:\n        return source.replay(path)\n',
    'guard_in_dead_code': 'def f(source, contract, path):\n    source.verify_for(contract)\n'
                          '    return source.proof(path)\n',
    'unguarded_contract_read': 'def f(source, contract):\n    source.verify_for(contract)\n    return source.contract\n',
    'guard_on_other_object': 'def f(source, contract, path):\n    source.verify_for(contract)\n'
                             '    def inner():\n        return source.replay(path)\n    return inner\n',
}


@pytest.mark.parametrize('case', sorted(PLANTED))
def test_a10b_planted_negatives_fail_and_guarded_twins_pass(tmp_path, case):  # A10b (Codex P1)
    bad, good = tmp_path / 'bad', tmp_path / 'good'
    for folder, text in ((bad, PLANTED[case]), (good, GUARDED_TWINS[case])):
        folder.mkdir()
        (folder / 'planted.py').write_text(text, encoding='utf-8')
    assert unguarded_consumers(bad, allowlist=set()), case
    assert unguarded_consumers(good, allowlist=set()) == [], case
