"""Signed TEST_ONLY G1 and retained runtime for isolated G5 behavior tests."""
from dataclasses import dataclass
import sys

from composition_fixture import (
    PORT_ROLES, build_artifacts, contract_document, digest, encoded,
    signed_approval, verified_domain,
)
from test_contract import NOW


@dataclass(frozen=True)
class SignedG5Fixture:
    contract: object
    domain: object
    private_keys: dict
    trusted_keys: dict
    retained_source_bytes: dict
    runtime_inventory: object


def build_signed_g5_fixture(root):
    from c1_rail.qualification.contract import ObservedBindings, validate_frozen_contract
    from c1_rail.qualification.production_source import ProductionSource
    from c1_rail.qualification.runtime_inventory import collect_runtime_inventory

    fixture = build_artifacts(root).with_runtime_artifacts(root)
    domain, private, keys = verified_domain(fixture)
    document = contract_document(fixture, domain)
    # The relaxed, explicitly signed TEST_ONLY screen preserves the unit test
    # for bounded failures without changing production policy or issued receipts.
    document['replay']['decision_rules']['failure_ceiling'] = '0.5'
    for stage in document['replay']['stages']:
        if stage['name'] == 'N1':
            stage['max_failures_per_population'] = 1
    document['result_plan']['required_output_roles'] = ['private-result', 'public-projection']
    document['result_plan']['permitted_optional_output_roles'] = []
    raw = encoded(document)
    approval = signed_approval(raw, private['test-freeze'], key_id='test-freeze', scope='FREEZE_F1')
    retained = dict(fixture.payloads)
    observed = ObservedBindings(
        artifact_sha256={fixture.paths[r]: digest(b) for r, b in retained.items()},
        runtime_load_sha256={r: digest(b) for r, b in retained.items()},
        effective_settings_sha256=digest(retained['effective_settings_successor']), orb_normal_base=1)
    contract = validate_frozen_contract(raw, approval, keys, observed, now=NOW, trust_domain=domain)
    ProductionSource._build_composition(contract, artifact_root=root)
    modules = {row.role: row.module for row in fixture.ordinary_modules}
    modules.update({role: sys.modules['fp_qualification_port_' + leg] for leg, role in PORT_ROLES.items()})
    inventory = collect_runtime_inventory(contract, loaded_modules=modules,
        retained_source_bytes=retained, artifact_root=root)
    return SignedG5Fixture(contract, domain, private, keys, retained, inventory)
