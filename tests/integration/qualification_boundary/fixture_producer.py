"""Administrator-only TEST_ONLY producers for actual Linux execution tests.

Nothing here supplies PathOutcome, StageRun, adjudication or a completion receipt.
It retains the existing synthetic source producers and signs their exact bytes.
"""
import base64
from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from types import SimpleNamespace

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from c1_rail.qualification.contract import TrustedApprovalKey, ObservedBindings, validate_frozen_contract
from c1_rail.qualification.preflight import exact_depth_subject
from c1_rail.qualification.trust_domain import _composition_test_trust_policy, validate_qualification_trust_domain
from c1_rail.qualification.execution.runtime import observe_runtime
from c1_rail.qualification.execution.protocol import sha256
from c1_rail.qualification.execution.admission import verify_bundle
from c1_rail.qualification.source_admission import admit_source
from c1_rail.qualification.policy_sources import build_qualification_policy
from composition_fixture import build_artifacts, verified_domain, contract_document, encoded


def fresh_keys(*, execution_seed=None, result_seed=None):
    private = {key: Ed25519PrivateKey.generate() for key in ('test-freeze', 'test-producer', 'test-seal', 'test-execution')}
    for name,seed in (('test-execution',execution_seed),('test-producer',result_seed)):
        if seed is not None:
            private[name]=Ed25519PrivateKey.from_private_bytes(seed)
    public = {key: TrustedApprovalKey(key, value.public_key().public_bytes_raw(), 'TEST_ONLY') for key, value in private.items()}
    registry = encoded(dict(schema='qualification_trusted_keys/v1', keys=[dict(key_id=key,
        public_key_b64=base64.b64encode(value.public_key).decode(), authority_class='TEST_ONLY', revoked_at=None)
        for key, value in sorted(public.items())]))
    return private, public, registry


def approve(raw, private, scope, *, contract_sha256=None, current=None,valid_seconds=14400):
    current = current or datetime.now(timezone.utc)
    payload = dict(schema='qualification_approval_payload/v1', scope=scope, subject_sha256=sha256(raw),
        contract_sha256=contract_sha256 or sha256(raw), authority_class='TEST_ONLY',
        issued_at=(current - timedelta(minutes=5)).isoformat().replace('+00:00', 'Z'),
        expires_at=(current + timedelta(seconds=valid_seconds)).isoformat().replace('+00:00', 'Z'))
    return encoded(dict(schema='qualification_approval/v1', payload=payload, signature=dict(
        algorithm='Ed25519', key_id='test-freeze', value_b64=base64.b64encode(private['test-freeze'].sign(encoded(payload))).decode())))


def release_document(repo, profile, image, keys):
    policy=build_qualification_policy()
    runtimes = {role: observe_runtime(repo, role) for role in ('worker', 'supervisor', 'g5')}
    sources = {name: row for runtime in runtimes.values() for name, row in runtime['sources'].items()}
    assignments = {'c1_rail.qualification.execution.worker': 'qualification_runner',
                   'c1_rail.qualification.execution.g5': 'qualification_adjudicator',
                   'c1_rail.qualification.execution.verification': 'qualification_sealer',
                   'c1_rail.qualification.replay': 'replay_kernel',
                   'c1_rail.qualification.paths': 'path_sampler',
                   'c1_rail.qualification.regime': 'rng_allocation'}
    ordinary = {assignments.get(name, 'runtime_dependency__' + name.replace('.', '__')):
        dict(module=name, **row) for name, row in sorted(sources.items())}
    return dict(schema='qualification_execution_release/v1', release_id='linux-test-n1',
        qualification_policy_sha256=sha256(policy),source_owner_sha256=json.loads(policy)['source_owner_sha256'],
        profile=profile, profile_sha256=sha256(encoded(profile)), authority_class='TEST_ONLY',
        service_id='linux-test-service', capability='N1_ONLY', production_execution=False,
        worker_image_digest=image, runtime_manifests=runtimes, ordinary_code=ordinary,
        worker_entrypoint=['/opt/ops/bin/python', '-I', '/opt/qualification/bootstrap.py', 'worker'],
        port_roles=['aegis_runtime_port', 'orb_runtime_port', 'striker_runtime_port', 'vanguard_runtime_port'],
        key_roles=dict(freeze=['test-freeze'], result=['test-producer'], seal=['test-seal'], execution=['test-execution']),
        trusted_key_sha256={key: sha256(value.public_key) for key, value in keys.items()})


def build_real_bundle(root, *, repo, release, private, keys, attempt_id, idle=False, budget=None,
                      fault=None,depth_valid_seconds=14400):
    current = datetime.now(timezone.utc)
    policy_raw=build_qualification_policy()
    port_transform = None
    if fault is not None:
        # These signed synthetic strategy programs cause actual worker faults.
        # They never manufacture PathOutcome, capture or qualification evidence.
        effects={
            'stop':'os.kill(os.getpid(), signal.SIGSTOP)',
            'exit_zero':'os._exit(0)',
            'cpu':'end=time.process_time()+2\n    while time.process_time()<end: pass',
            'wall':'time.sleep(2)',
            'memory':'bytearray(1500000000)',
        }
        if fault not in effects: raise ValueError('unknown TEST_ONLY worker fault')
        def port_transform(leg,raw):
            if leg!='orb_mnq_v7': return raw
            marker=b'    def on_bar(self, bar):\n'
            if raw.count(marker)!=1: raise ValueError('synthetic port hook differs')
            raw=raw.replace(marker,marker+b'        _boundary_fault()\n')
            return raw+('''\n_boundary_fault_seen=False
def _boundary_fault():
    global _boundary_fault_seen
    if _boundary_fault_seen: return
    _boundary_fault_seen=True
    import os, signal, time
    '''+f'os.write(2, {("TEST_ONLY worker fault: "+fault+chr(10)).encode()!r})\n    '+effects[fault]+'\n').encode()
    fixture = build_artifacts(root, idle=idle, port_transform=port_transform)
    release_doc = json.loads(release)
    modules = tuple(SimpleNamespace(role=role, name=row['module'], path=row['path'],
        source_bytes=(repo / row['path']).read_bytes()) for role, row in release_doc['ordinary_code'].items())
    fixture = replace(fixture, ordinary_modules=modules,
        payloads=dict(fixture.payloads, **{row.role: row.source_bytes for row in modules}, execution_release=release,qualification_policy=policy_raw),
        paths=dict(fixture.paths, **{row.role: row.path for row in modules}, execution_release='authority/release.json',qualification_policy='authority/policy.json'))
    old, _, _ = verified_domain(fixture)
    doc = json.loads(old.canonical_bytes)
    doc.update(schema='qualification_trust_domain/v2', execution_key_ids=['test-execution'],
        policy_sha256=sha256(policy_raw),
        execution_service_id=release_doc['service_id'], execution_release_sha256=sha256(release),
        required_attested_checkpoints=['N1', 'N2', 'PART_A'], required_artifact_roles=sorted(fixture.payloads),
        trusted_key_sha256=release_doc['trusted_key_sha256'])
    policy = _composition_test_trust_policy(accepted_historical_pins=old.accepted_historical_pins,
        required_artifact_roles=tuple(sorted(fixture.payloads)), runtime_code_roles=old.runtime_code_roles,
        port_runtime_pins=old.port_runtime_pins, effective_settings_sha256=old.effective_settings_sha256,
        workload_policy=old.workload_policy)
    domain_raw = encoded(doc)
    domain_approval = approve(domain_raw, private, 'BIND_QUALIFICATION_TRUST_DOMAIN', current=current)
    domain = validate_qualification_trust_domain(domain_raw, domain_approval, keys, policy=policy, now=current)
    contract_doc = contract_document(fixture, domain)
    contract_doc['schema'] = 'frozen_qualification_contract/v2'
    contract_doc['policy_sha256']=sha256(policy_raw)
    contract_doc['result_plan']=dict(policy_sha256=sha256(policy_raw),
        adjudicator_closure_sha256=contract_doc['result_plan']['adjudicator_closure_sha256'])
    contract_doc['replay']['budget'].update(maximum_wall_seconds=180, maximum_cpu_seconds=120,
                                           maximum_memory_bytes=900000000)
    if budget:
        contract_doc['replay']['budget'].update(budget)
    if fault in ('cpu','wall'):
        contract_doc['replay']['budget']['maximum_'+fault+'_seconds']=1
    contract_raw = encoded(contract_doc)
    freeze = approve(contract_raw, private, 'FREEZE_F1', current=current)
    observed = ObservedBindings({fixture.paths[role]: sha256(raw) for role, raw in fixture.payloads.items()},
        {role: sha256(raw) for role, raw in fixture.payloads.items()}, domain.effective_settings_sha256, 1)
    contract = validate_frozen_contract(contract_raw, freeze, keys, observed, now=current, trust_domain=domain,
        qualification_policy_bytes=policy_raw)
    extra = dict(contract=contract_raw, freeze_approval=freeze, trust_domain=domain_raw,
        domain_approval=domain_approval, release_approval=approve(release, private, 'APPROVE_EXECUTION_RELEASE', current=current),
        exact_depth_approval=approve(exact_depth_subject(contract, attempt_id=attempt_id), private,
            'APPROVE_E1_EXACT_DEPTH', contract_sha256=contract.contract_sha256, current=current,
            valid_seconds=depth_valid_seconds))
    payloads = dict(fixture.payloads, **extra)
    paths = dict(fixture.paths, **{role: 'authority/' + role + '.json' for role in extra})
    for role, raw in payloads.items():
        path = root / paths[role]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    index = encoded(dict(schema='qualification_retained_bundle/v1', attempt_id=attempt_id,
        entries=[dict(role=role, path=paths[role], sha256=sha256(payloads[role]), byte_length=len(payloads[role]))
                 for role in sorted(payloads)]))
    (root / 'index.json').write_bytes(index)
    # Exercise the worker's real admission path before the administrator stages
    # anything for dispatch. This constructs sources without replaying on_bar.
    context=verify_bundle(root,release,keys,datetime.now(timezone.utc))
    admitted=admit_source(context.contract,artifact_root=root,policy=context.policy)
    return dict(root=root, index=index, contract=contract, domain=domain, payloads=payloads, paths=paths,
        source_admission=admitted.source_admission_bytes,legality=admitted.legality_bytes)
