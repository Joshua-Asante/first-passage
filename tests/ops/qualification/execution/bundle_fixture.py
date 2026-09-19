"""Signed TEST_ONLY retained bundles for parser/compute tests, never activation."""
from dataclasses import replace
import json
import platform
from pathlib import Path
import sys

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from c1_rail.qualification.contract import TrustedApprovalKey, ObservedBindings, validate_frozen_contract
from c1_rail.qualification.preflight import exact_depth_subject
from c1_rail.qualification.trust_domain import _composition_test_trust_policy, validate_qualification_trust_domain
from composition_fixture import build_artifacts, verified_domain, contract_document, encoded, signed_approval, digest
from test_contract import NOW
from test_profile import document as profile_document
from c1_rail.qualification.policy_sources import build_qualification_policy


def build_bundle(root, *, idle=False, geometry_bytes=None, workload=None,
                 attempt_id=None, root_rng_namespace=None, capability='N1_ONLY', diagnostic=False, funded=False):
    policy_raw = build_qualification_policy()
    fixture = build_artifacts(root, idle=idle).with_runtime_artifacts(root)
    if geometry_bytes is not None:
        row = next(row for row in fixture.ordinary_modules if row.name == 'dd_geometry')
        fixture = replace(fixture,payloads=dict(fixture.payloads,**{row.role:geometry_bytes}),
            ordinary_modules=tuple(replace(item,source_bytes=geometry_bytes) if item.role == row.role else item
                                   for item in fixture.ordinary_modules))
        (root / fixture.paths[row.role]).write_bytes(geometry_bytes)
    old, private, keys = verified_domain(fixture)
    private['test-execution'] = Ed25519PrivateKey.generate()
    keys['test-execution'] = TrustedApprovalKey('test-execution', private['test-execution'].public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw), 'TEST_ONLY')
    profile = profile_document()
    if capability == 'FULL_E1':
        profile.update(schema='qualification_execution_profile/v2', protocol_version=2,
            capability='FULL_E1', supported_checkpoints=[], dispatch_enabled=False)
    if diagnostic or funded:
        from c1_rail.qualification.execution.profile import diagnostic_execution_profile, funded_diagnostic_execution_profile
        if capability != 'FULL_E1':
            raise ValueError('diagnostic requires FULL_E1 fixture')
        profile = (funded_diagnostic_execution_profile if funded else diagnostic_execution_profile)(encoded(profile))
    ordinary = {row.role: dict(module=row.name, path=row.path, sha256=digest(row.source_bytes))
                for row in fixture.ordinary_modules}
    sources = {row['module']: dict(path=row['path'], sha256=row['sha256']) for row in ordinary.values()}
    repo = Path(__file__).resolve().parents[4]
    runtime = dict(python_version=platform.python_version(), platform=sys.platform,
                   dependency_lock_sha256=digest((repo / 'requirements-ops.lock').read_bytes()),
                   signing_configuration_sha256=digest((repo / 'tools/local_verification/requirements-extra.txt').read_bytes()), sources=sources)
    key_roles = dict(freeze=['test-freeze'], result=['test-producer'], seal=['test-seal'], execution=['test-execution'])
    release_doc = dict(schema='qualification_execution_release/v1', release_id='unit-release',
        qualification_policy_sha256=digest(policy_raw),source_owner_sha256=json.loads(policy_raw)['source_owner_sha256'],
        profile=profile, profile_sha256=digest(encoded(profile)), authority_class='TEST_ONLY',
        service_id='test-service', capability='N1_ONLY', production_execution=False,
        worker_image_digest='sha256:' + 'd' * 64,
        # Parser fixtures do not establish per-entrypoint runtime completeness.
        runtime_manifests={role: runtime for role in ('worker', 'supervisor', 'g5')},
        ordinary_code=ordinary,
        worker_entrypoint=['/opt/ops/bin/python', '-I', '/opt/qualification/bootstrap.py', 'worker'],
        port_roles=['aegis_runtime_port', 'orb_runtime_port', 'striker_runtime_port', 'vanguard_runtime_port'],
        key_roles=key_roles, trusted_key_sha256={key: digest(value.public_key) for key, value in keys.items()})
    if capability == 'FULL_E1':
        release_doc.update(schema='qualification_execution_release/v2', capability='FULL_E1',
            dispatch_enabled=False)
    if diagnostic or funded:
        from c1_rail.qualification.execution.profile import diagnostic_budget_profile
        release_doc.update(schema='qualification_execution_release/' + ('v4' if funded else 'v3'),
            campaign_budget_profile=diagnostic_budget_profile(encoded(profile)))
    release = encoded(release_doc)
    fixture = replace(fixture, payloads=dict(fixture.payloads, execution_release=release,qualification_policy=policy_raw),
                      paths=dict(fixture.paths, execution_release='authority/release.json',qualification_policy='authority/policy.json'))
    from c1_rail.qualification.trust_domain import _workload_dict
    workload = old.workload_policy if workload is None else workload
    doc = json.loads(old.canonical_bytes)
    doc['workload_policy'] = _workload_dict(workload)
    doc.update(schema='qualification_trust_domain/v2', execution_key_ids=['test-execution'],
        policy_sha256=digest(policy_raw),
        execution_service_id='test-service', execution_release_sha256=digest(release),
        required_attested_checkpoints=['N1', 'N2', 'PART_A'], required_artifact_roles=sorted(fixture.payloads),
        trusted_key_sha256=release_doc['trusted_key_sha256'])
    policy = _composition_test_trust_policy(accepted_historical_pins=old.accepted_historical_pins,
        required_artifact_roles=tuple(sorted(fixture.payloads)), runtime_code_roles=old.runtime_code_roles,
        port_runtime_pins=old.port_runtime_pins, effective_settings_sha256=old.effective_settings_sha256,
        workload_policy=workload)
    domain_raw = encoded(doc)
    def approve(raw, scope, contract_sha256=None):
        return signed_approval(raw, private['test-freeze'], key_id='test-freeze', scope=scope,
                               contract_sha256=contract_sha256)
    domain_approval = approve(domain_raw, 'BIND_QUALIFICATION_TRUST_DOMAIN')
    domain = validate_qualification_trust_domain(domain_raw, domain_approval, keys, policy=policy, now=NOW)
    contract_doc = contract_document(fixture, domain)
    contract_doc['schema'] = 'frozen_qualification_contract/v2'
    contract_doc['policy_sha256'] = digest(policy_raw)
    contract_doc['result_plan'] = dict(policy_sha256=digest(policy_raw),
        adjudicator_closure_sha256=contract_doc['result_plan']['adjudicator_closure_sha256'])
    # Variants still pass ordinary domain/contract signature validation below.
    replay = contract_doc['replay']
    if root_rng_namespace is not None:
        replay['root_rng_namespace'] = root_rng_namespace
    replay.update(horizon_sessions=workload.horizon_sessions,
                  inner_block_sessions=workload.inner_block_sessions,
                  outer_months=workload.outer_months)
    for stage in replay['stages']:
        counts = workload.stage_population_depths[stage['name']]
        stage['population_counts'] = {pop: list(values) for pop, values in counts.items()}
        stage['exact_depth'] = (1 if stage['name'] == 'LEGALITY' else
            workload.part_a_paths_per_population_per_panel if stage['name'] == 'PART_A'
            else next(iter(counts.values()))[0])
        if stage['name'] == 'N1':
            from decimal import Decimal
            stage['max_failures_per_population'] = int(
                stage['exact_depth'] * Decimal(replay['decision_rules']['failure_ceiling']))
    for name in ('initial_panels', 'expanded_panels', 'paths_per_population_per_panel'):
        replay['part_a'][name] = getattr(workload, 'part_a_' + name)
    counts = workload.stage_population_depths
    replay['budget'].update(
        n1_paths=sum(values[0] for values in counts['N1'].values()),
        n2_paths=sum(values[0] for stage in ('N2', 'PART_B') for values in counts[stage].values()),
        n3_paths=sum(values[0] for values in counts['N3'].values()),
        part_a_initial_paths=workload.part_a_initial_panels * workload.part_a_paths_per_population_per_panel,
        part_a_expanded_paths=workload.part_a_expanded_panels * workload.part_a_paths_per_population_per_panel)
    contract_raw = encoded(contract_doc)
    freeze = approve(contract_raw, 'FREEZE_F1')
    observed = ObservedBindings({fixture.paths[r]: digest(b) for r, b in fixture.payloads.items()},
        {r: digest(b) for r, b in fixture.payloads.items()}, domain.effective_settings_sha256, 1)
    contract = validate_frozen_contract(contract_raw, freeze, keys, observed, now=NOW, trust_domain=domain,
        qualification_policy_bytes=policy_raw)
    attempt_id = attempt_id or ('synthetic-idle' if idle else 'synthetic-trading')
    extra = dict(contract=contract_raw, freeze_approval=freeze, trust_domain=domain_raw,
                 domain_approval=domain_approval, release_approval=approve(release, 'APPROVE_EXECUTION_RELEASE'),
                 exact_depth_approval=approve(exact_depth_subject(contract, attempt_id=attempt_id),
                    'APPROVE_E1_EXACT_DEPTH', contract.contract_sha256))
    payloads = dict(fixture.payloads, **extra)
    paths = dict(fixture.paths, **{role: 'authority/' + role + '.json' for role in extra})
    for role, raw in payloads.items():
        path = root / paths[role]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    index = encoded(dict(schema='qualification_retained_bundle/v1', attempt_id=attempt_id,
        entries=[dict(role=role, path=paths[role], sha256=digest(payloads[role]), byte_length=len(payloads[role]))
                 for role in sorted(payloads)]))
    (root / 'index.json').write_bytes(index)
    return dict(root=root, release=release, keys=keys, private=private, contract=contract,
                attempt_id=attempt_id, index=index, payloads=payloads, paths=paths)
