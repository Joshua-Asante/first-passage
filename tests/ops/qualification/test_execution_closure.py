"""Closure omissions and cached callables cannot change admitted execution."""
from dataclasses import replace
import pytest

from test_trust_domain import operator_case, signed, NOW
from c1_rail.qualification.trust_domain import production_trust_domain


@pytest.mark.parametrize('module', [
    'c1_rail.qualification.production', 'c1_rail.qualification.production_source',
    'c1_rail.qualification.runner', 'c1_rail.qualification.provider',
    'c1_rail.qualification.attempt', 'c1_rail.qualification.runtime_inventory',
    'c1_rail.qualification.blocks', 'c1_rail.qualification.panel',
    'mc.simulation', 'c1_rail.book_policy', 'c1_signal_daemon.tv_broker_emulator',
])
def test_operator_domain_cannot_omit_outcome_producer(module):
    doc, _, private, keys = operator_case()
    roles = [role for role, name in doc['runtime_code_roles'].items() if name == module]
    for role in roles:
        del doc['runtime_code_roles'][role]
        doc['required_artifact_roles'].remove(role)
    with pytest.raises(ValueError, match='role'):
        production_trust_domain(*signed(doc, private), keys, now=NOW)


def test_production_policy_covers_real_transitive_execution_imports():
    from runtime_fixture import ordinary_runtime_fixture
    from c1_rail.qualification.trust_domain import PRODUCTION_TRUST_POLICY
    roles = dict(PRODUCTION_TRUST_POLICY.required_code_roles)
    modules = ordinary_runtime_fixture(role_modules={r: n for r, n in roles.items()
                                                     if not n.startswith('fp_qualification_port_')})
    by_name = {row.name: row for row in modules}
    reachable = set()
    pending = list(roles.values()) + ['c1_rail.qualification.production',
                                     'c1_rail.qualification.production_source']
    while pending:
        name = pending.pop()
        if name in reachable or name.startswith('fp_qualification_port_'):
            continue
        reachable.add(name)
        pending.extend(by_name[name].dependencies)
    assert reachable <= set(roles.values())


@pytest.fixture(scope='module')
def closure_setup(tmp_path_factory):
    from composition_fixture import build_verified_composition
    return build_verified_composition(tmp_path_factory.mktemp('closure-inputs'))


@pytest.mark.parametrize('missing', ['c1_rail.qualification.provider', 'mc.simulation',
                                     'c1_rail.qualification'])
def test_adjudicator_rederives_import_closure_instead_of_trusting_receipt_edges(closure_setup, missing):
    from c1_rail.qualification.result_adjudication import _verify_runtime_inventory, _runtime_dependencies
    setup = closure_setup
    rows = tuple(replace(row, dependencies=()) for row in setup.runtime_inventory.modules
                 if row.module_name != missing)
    roles = {row.role: row.module_name for row in rows}
    hashes = tuple((role, digest) for role, digest in setup.runtime_inventory.runtime_load_sha256
                   if role not in {r.role for r in setup.runtime_inventory.modules if r.module_name == missing})
    receipt = replace(setup.runtime_inventory, modules=rows, runtime_load_sha256=hashes)
    # Isolate the inventory boundary; this synthetic view claims no G1 authority.
    contract = replace(setup.contract, runtime_load_sha256=dict(hashes),
        artifacts=tuple(item for item in setup.contract.artifacts if item.role in dict(hashes)),
        trust_domain=replace(setup.domain, runtime_code_roles=roles))
    with pytest.raises(ValueError, match='dependency|closure'):
        _verify_runtime_inventory(contract, receipt, _runtime_dependencies())


def test_executor_does_not_accept_a_prepopulated_replay_callable(closure_setup, tmp_path, monkeypatch):
    from c1_rail.qualification import production
    from c1_rail.qualification.attempt import AttemptStore
    from test_runner import result
    setup = closure_setup
    store = AttemptStore.open(tmp_path/'attempt.sqlite', campaign_id='provider-substitution',
        contract_digest=setup.contract.contract_sha256, trust_domain_sha256=setup.domain.sha256,
        boot_id='first', now=NOW)
    driver = production._composition_executor(setup.contract, setup.source, store)
    store.reserve('TB_E1', b'{}', now=NOW)
    claim = store.claimed_reservation('TB_E1')
    store.start_once('TB_E1', claim, now=NOW)
    dispatch = store.start_checkpoint_once('N1', store.claimed_reservation('TB_E1'), b'{}', now=NOW)
    fabricated = result([-2000] * setup.contract.replay.horizon_sessions)
    monkeypatch.setattr(production, '_EXECUTOR_PROVIDERS',
                        {id(driver): lambda **kwargs: fabricated}, raising=False)
    observed = driver.run_stage('n1', dispatch)
    # Admitted fixture replays pass; substituted evidence makes every path fail.
    assert all(outcome.status == 'PASS' for _, rows in observed.populations for outcome in rows)
