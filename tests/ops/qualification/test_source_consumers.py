"""No code path in ``ops/`` uses a ProductionSource capability without explicit review (spec §2.6, A10/A10b).

A10b is a deny-by-default lexical scan. ``ast.walk`` visits every node of every ``*.py``
module under ``ops/`` except ``c1_rail/qualification/production_source.py`` (the
capability's owner). It flags every call ``<any>.replay(...)``, ``<any>.replay_bracket(...)``
and ``<any>.proof(...)``, and every load of ``<any>.contract``, on any receiver: no
receiver-name heuristics and no guard-dominance reasoning. A preceding ``verify_for`` does
not clear a finding. Lambdas, comprehensions, nested defs and class bodies are covered by
construction.

Each finding resolves to ``<module path relative to ops/>:<owner>``, where ``<owner>`` is
the dotted chain of enclosing ``class``/``def`` names (``Cls.method``, ``outer.inner``).
Lambdas and comprehensions add no name, so they resolve to the nearest enclosing def or
class. Class-body code outside any def resolves to ``<module>:Cls``; module-level code
resolves to ``<module>:<module>``. A finding passes only when that qualified name is a key
of ``ALLOWLIST``, whose value states what actually protects the site (or why the receiver
is not a ProductionSource at all).

Named residual: dynamic access (``getattr``, ``operator.attrgetter``, string-built names)
is outside a lexical scan. The runtime ``ProductionSource.verify_for`` refusal
(SOURCE_ONLY_NOT_QUALIFICATION) and A10, which tests each qualification consumer directly,
remain the enforcing guard.
"""
from __future__ import annotations

import ast
import shutil
from pathlib import Path
from types import SimpleNamespace

import pytest

from test_source_contract import NOW, build_source_case, refused

OPS = Path(__file__).resolve().parents[3] / 'ops'

CAPABILITY_OWNER = 'c1_rail/qualification/production_source.py'
CAPABILITY_CALLS = frozenset({'replay', 'replay_bracket', 'proof'})
CAPABILITY_ATTRIBUTE = 'contract'
MODULE_OWNER = '<module>'

_EXECUTION_CONTEXT = ('`context` is an admission.ExecutionContext built by verify_bundle/verify_retained_bundle '
                      '(admission.py:101-215); `.contract` is its validated frozen contract record, read for '
                      'digests/fields only. Where the function does not type-check `context`, this holds by its current '
                      'callers only. No ProductionSource is the receiver and no replay/proof is called here.')
_PARSE_HELPER = (' Private helper reached only from parse_worker_result (directly, or through '
                 '_parse_part_a_worker_result, whose only caller is parse_worker_result), so `context` is that '
                 'function\'s ExecutionContext.')

ALLOWLIST = {
    # --- ProductionSource capability uses ---
    'c1_rail/qualification/p7_driver.py:_run':
        'Legitimate source-only consumer by design: builds a ProductionSource from a receipt of '
        'validate_source_contract and calls replay_bracket on it; source-only results are sealed and '
        'the source is refused by verify_for (SOURCE_ONLY_NOT_QUALIFICATION) at every qualification consumer.',
    'c1_rail/qualification/execution/compute.py:_run_checkpoint_compute.replay':
        'Nested closure over `source`; the enclosing function requires type(source) is ProductionSource and '
        'calls source.verify_for(contract) before the closure is defined, so a source-only source raises first.',
    'c1_rail/qualification/execution/compute.py:run_part_a_compute.proof':
        'Nested closure over `source`; run_part_a_compute requires type(source) is ProductionSource and calls '
        'source.verify_for(contract) before the closure is defined, so a source-only source raises first.',
    'c1_rail/qualification/execution/compute.py:run_part_a_compute.replay':
        'Nested closure over `source`; run_part_a_compute requires type(source) is ProductionSource and calls '
        'source.verify_for(contract) before the closure is defined, so a source-only source raises first.',
    'c1_rail/qualification/production.py:ProductionExecutor._replay':
        'Directly callable without _admit (no checkpoint-dispatch check). Protected only by the issued executor: '
        '_initialize required a validated frozen contract, a permits_synthetic domain, type ProductionSource and '
        'source.verify_for(contract); each call runs _budget -> _checked_domain, which re-checks registry identity '
        'of contract/source/store/domain and revalidates the contract.',
    'c1_rail/qualification/production.py:ProductionExecutor.run_part_a.proof':
        'Nested closure defined inside run_part_a after self._admit(dispatch, "PART_A") (source.verify_for plus '
        'durable dispatch consumption); each call runs _budget -> _checked_domain identity checks.',
    'c1_rail/qualification/provider.py:_ReplayProvider.__call__':
        'Receiver is the provider\'s own `replay` attribute, a callable injected at construction, not a '
        'ProductionSource. The provider admits nothing itself and does not check what it is given; its current '
        'construction sites in ops/ (an observation, not enforced) are compute._run_checkpoint_compute (after '
        'verify_for) and ProductionExecutor.run_stage (after _admit).',
    # --- `.contract` reads on ProductionExecutor (self.contract is the executor's validated contract slot) ---
    'c1_rail/qualification/production.py:ProductionExecutor.initial_state':
        'Reads the executor\'s own contract slot after self._checked_domain(); not a ProductionSource receiver.',
    'c1_rail/qualification/production.py:ProductionExecutor._checked_domain':
        'This is the identity check: compares self.contract to the issued registry binding.contract and '
        'revalidates it with require_validated_frozen_contract; receivers are the executor and its binding.',
    'c1_rail/qualification/production.py:ProductionExecutor._budget':
        'Reads the executor\'s contract replay budget after self._checked_domain(); not a ProductionSource receiver.',
    'c1_rail/qualification/production.py:ProductionExecutor._admit':
        'Reads the executor\'s contract for the dispatch digest comparison and passes it to '
        'self.source.verify_for after _checked_domain(); receiver is the executor.',
    'c1_rail/qualification/production.py:ProductionExecutor.run_stage':
        'Reads the executor\'s contract after self._admit(dispatch, stage); receiver is the executor.',
    'c1_rail/qualification/production.py:ProductionExecutor.run_part_a':
        'Reads the executor\'s contract after self._admit(dispatch, "PART_A"); receiver is the executor.',
    # --- `.contract` reads on non-ProductionSource receivers ---
    'c1_rail/qualification/result_adjudication.py:FrozenAdjudicator.verify_for':
        'Receiver is the FrozenAdjudicator dataclass; this method is its own identity check of '
        'self.contract against the G1 contract. Not a ProductionSource.',
    'c1_rail/qualification/result_adjudication.py:FrozenAdjudicator.__call__':
        'Receiver is the FrozenAdjudicator; __call__ runs self.verify_for(self.contract) before passing the '
        'contract to its entrypoint. Not a ProductionSource.',
    'c1_rail/account_close_ledger.py:reconcile':
        'Receiver is an account_close_evidence.CashRow whose `contract` field is an instrument-contract string; '
        'unrelated to ProductionSource.',
    'c1_signal_daemon/m1_stage1_control.py:main':
        'Receiver is the argparse Namespace; `args.contract` is the --contract CLI string. Unrelated to ProductionSource.',
    'c1_rail/qualification/execution/campaign_store.py:CampaignStore.admit': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/campaign_store.py:CampaignStore.finish_diagnostic_admission': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/campaign_supervisor.py:guardian_main':
        '`verified` is the ExecutionContext from ExecutionService._context (verify_bundle); `.contract` is read '
        'for its canonical bytes and passed to source_admission.admit_source, which builds the ProductionSource '
        'and calls source.verify_for(contract) itself. No replay/proof here.',
    'c1_rail/qualification/execution/evidence.py:encode_worker_result':
        _EXECUTION_CONTEXT + ' The function calls admitted.source.verify_for(context.contract) first.',
    'c1_rail/qualification/execution/evidence.py:_captured_outcome': _EXECUTION_CONTEXT + _PARSE_HELPER,
    'c1_rail/qualification/execution/evidence.py:_verify_worker_bindings': _EXECUTION_CONTEXT + _PARSE_HELPER,
    'c1_rail/qualification/execution/evidence.py:_verify_worker_observations': _EXECUTION_CONTEXT + _PARSE_HELPER,
    'c1_rail/qualification/execution/evidence.py:_parse_part_a_worker_result': _EXECUTION_CONTEXT + _PARSE_HELPER,
    'c1_rail/qualification/execution/g5.py:_inspect_capture':
        '`current` is an ExecutionContext (verify_bundle at both callers); `.contract` is passed to evidence '
        'builders as a record. No ProductionSource receiver.',
    'c1_rail/qualification/execution/g5.py:inspect_historical_n1': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/g5.py:authenticate_n1_evidence': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/g5.py:validate_campaign_checkpoint': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/plan.py:derive_campaign_plan_from_context':
        'Requires type(context) is ExecutionContext and runs require_validated_frozen_contract(context.contract). '
        'No ProductionSource receiver.',
    'c1_rail/qualification/execution/preflight.py:build_binding':
        'Requires type(context) is ExecutionContext; `.contract` feeds plan/digest derivation only. '
        'No ProductionSource receiver.',
    'c1_rail/qualification/execution/service.py:ExecutionService.handle_request': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/service.py:ExecutionService._commit': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/service.py:ExecutionService._execute': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/store.py:ExecutionStore.cancellation_enrollment': _EXECUTION_CONTEXT,
    'c1_rail/qualification/execution/verification.py:verify_execution':
        _EXECUTION_CONTEXT + ' `original` is a second verify_bundle ExecutionContext.',
    'c1_rail/qualification/execution/worker.py:run_worker':
        _EXECUTION_CONTEXT + ' The ProductionSource is obtained via admit_source (verify_for inside) and '
        'replayed only through compute.run_n1/n2_compute.',
    'c1_rail/qualification/execution/worker.py:run_part_a_body':
        _EXECUTION_CONTEXT + ' Its only caller in ops/ is run_worker, whose `context` is verify_bundle\'s; the '
        'ProductionSource is admitted.source (admit_source, verify_for inside) and is replayed only through '
        'compute.run_part_a_compute.',
}


def _owner(node, parents):
    names = []
    current = parents.get(node)
    while current is not None:
        if isinstance(current, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(current.name)
        current = parents.get(current)
    return '.'.join(reversed(names)) or MODULE_OWNER


def _is_capability_use(node):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        return node.func.attr in CAPABILITY_CALLS
    return (isinstance(node, ast.Attribute) and node.attr == CAPABILITY_ATTRIBUTE
            and isinstance(node.ctx, ast.Load))


def capability_uses(root: Path):
    """Every flagged node under ``root``, as sorted ``(qualified owner, line)`` pairs."""
    found = []
    for path in sorted(Path(root).rglob('*.py')):
        relative = path.relative_to(root).as_posix()
        if relative == CAPABILITY_OWNER:
            continue
        tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        found.extend((f'{relative}:{_owner(node, parents)}', node.lineno)
                     for node in ast.walk(tree) if _is_capability_use(node))
    return sorted(found)


def unreviewed_uses(root: Path, allowlist):
    return [(name, line) for name, line in capability_uses(root) if name not in allowlist]


def test_every_production_source_consumer_is_allowlisted():  # A10b
    assert unreviewed_uses(OPS, ALLOWLIST) == []


def _defined_owners(path: Path):
    tree = ast.parse(path.read_text(encoding='utf-8'))
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    owners = {MODULE_OWNER}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            outer = _owner(node, parents)
            owners.add(node.name if outer == MODULE_OWNER else f'{outer}.{node.name}')
    return owners


def test_allowlist_has_no_stale_entries():  # A10b meta
    flagged = {name for name, _ in capability_uses(OPS)}
    for name, reason in ALLOWLIST.items():
        relative, owner = name.split(':', 1)
        assert (OPS / relative).is_file(), f'allowlisted module is gone: {name}'
        assert owner in _defined_owners(OPS / relative), f'allowlisted owner is gone: {name}'
        assert name in flagged, f'allowlisted owner no longer uses a capability: {name}'
        assert reason.strip(), f'allowlist entry needs a reason: {name}'


PLANTED = {
    'lambda': ('def f(source, path):\n    g = lambda: source.replay(path)\n    return g\n', 'f'),
    'nested_def': ('def f(source):\n    def inner(path):\n        return source.replay_bracket(path)\n'
                   '    return inner\n', 'f.inner'),
    'comprehension': ('def f(xs, p):\n    return [s.replay(p) for s in xs]\n', 'f'),
    'contract_any_receiver': ('def f(thing):\n    return thing.contract\n', 'f'),
    'after_verify_for': ('def f(source, contract, path):\n    source.verify_for(contract)\n'
                         '    return source.replay(path)\n', 'f'),
    'method_proof': ('class C:\n    def m(self, panel):\n        return self.source.proof(panel)\n', 'C.m'),
    'class_body': ('class C:\n    value = registry.contract\n', 'C'),
    'module_level': ('result = source.replay(path)\n', MODULE_OWNER),
}


@pytest.mark.parametrize('case', sorted(PLANTED))
def test_planted_use_fails_closed_and_review_clears_exactly_it(tmp_path, case):  # A10b
    source, owner = PLANTED[case]
    (tmp_path / 'planted.py').write_text(source, encoding='utf-8')
    qualified = f'planted.py:{owner}'
    findings = unreviewed_uses(tmp_path, {})
    assert findings and {name for name, _ in findings} == {qualified}
    assert unreviewed_uses(tmp_path, {qualified: 'reviewed'}) == []


def test_new_function_in_reviewed_module_is_flagged(tmp_path):  # A10b
    relative = 'c1_rail/qualification/production.py'
    planted = tmp_path / relative
    planted.parent.mkdir(parents=True)
    shutil.copyfile(OPS / relative, planted)
    with planted.open('a', encoding='utf-8') as handle:
        handle.write('\n\ndef leak(executor, path):\n    return executor.source.replay(path)\n')
    findings = unreviewed_uses(tmp_path, ALLOWLIST)
    assert [name for name, _ in findings] == [f'{relative}:leak']


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


K9_PLANTED = ('def f(source, path, authority, epoch):\n'
              '    source.replay_bracket(path)\n'
              '    return source.{name}\n')


@pytest.mark.parametrize('name', ('_engine', '_replay_raw', 'screen_bracket', 'screen_epoch'))
def test_K9(tmp_path, name):
    """A planted screen capability use in scripts/, under an owner allowlisted only for
    replay_bracket, is a finding keyed by (owner, capability); its own entry clears it."""
    (tmp_path / 'scripts').mkdir()
    (tmp_path / 'scripts' / 'planted.py').write_text(K9_PLANTED.format(name=name), encoding='utf-8')
    owner = 'scripts/planted.py:f'
    reviewed = {(owner, 'replay_bracket'): 'reviewed'}
    assert unreviewed_uses(tmp_path, reviewed) == [(owner, name, 3)]
    assert unreviewed_uses(tmp_path, {**reviewed, (owner, name): 'reviewed'}) == []
