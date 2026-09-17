"""Real source admission and retained-byte legality; no execution claim."""
import hashlib
import json

import pytest

from c1_rail.qualification.contract import canonical_json_bytes, ObservedBindings, validate_frozen_contract
from c1_rail.qualification.policy import parse_policy
from c1_rail.qualification.policy_sources import build_qualification_policy
from composition_fixture import build_artifacts, verified_domain, contract_document, signed_approval
from test_contract import NOW


EMPTY = b'POLICY_REGISTRY: dict[str, ProtectionPolicy] = {}\n'
NONEMPTY = EMPTY.replace(b'{}', b'{"tradeify_portfolio@Tradeify_Select_100K": ProtectionPolicy(reference_mode="trailing", trigger=0.01, scale=0.40, provenance="synthetic sealed provenance")}')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check(raw, digest=None):
    from c1_rail.qualification.legality import verify_static_legality
    verify_static_legality(contract_sha256='a'*64, domain_sha256='b'*64,
        policy=parse_policy(build_qualification_policy()), geometry_bytes=raw,
        expected_geometry_sha256=sha(raw) if digest is None else digest)


def test_bound_nonempty_registry_is_not_legality_pass():
    with pytest.raises(ValueError, match='LEGALITY_REGISTRY_NOT_EMPTY'): check(NONEMPTY)


def test_empty_registry_is_static_legal():
    check(EMPTY)


@pytest.mark.parametrize('raw', [b'', b'invalid source(', b'POLICY_REGISTRY = dict()\n', EMPTY + b'POLICY_REGISTRY.update({})\n'])
def test_malformed_registry_is_distinct_from_nonempty(raw):
    with pytest.raises(ValueError, match='LEGALITY_GEOMETRY_MALFORMED'): check(raw)


@pytest.mark.parametrize('digest', ['', 'c'*64])
def test_geometry_requires_exact_retained_digest(digest):
    with pytest.raises(ValueError): check(EMPTY, digest)


def signed_source_case(root, *, change=None):
    fixture = build_artifacts(root).with_runtime_artifacts(root)
    if change == 'nonempty':
        role = next(row.role for row in fixture.ordinary_modules if row.name == 'dd_geometry')
        fixture.payloads[role] = NONEMPTY
        (root / fixture.paths[role]).write_bytes(NONEMPTY)
    elif change == 'bad_cost':
        fixture.payloads['cost_model'] = b'{}'
        (root / fixture.paths['cost_model']).write_bytes(b'{}')
    domain, private, keys = verified_domain(fixture)
    doc = contract_document(fixture, domain)
    raw = canonical_json_bytes(doc)
    approval = signed_approval(raw, private['test-freeze'], key_id='test-freeze', scope='FREEZE_F1')
    hashes = {role: sha(payload) for role, payload in fixture.payloads.items()}
    observed = ObservedBindings(
        artifact_sha256={fixture.paths[role]: digest for role, digest in hashes.items()},
        runtime_load_sha256=hashes, effective_settings_sha256=hashes['effective_settings_successor'], orb_normal_base=1)
    contract = validate_frozen_contract(raw, approval, keys, observed, now=NOW, trust_domain=domain)
    return contract, domain


def test_real_source_produces_bound_records(tmp_path):
    from c1_rail.qualification.source_admission import admit_source
    contract, domain = signed_source_case(tmp_path)
    policy = parse_policy(build_qualification_policy())
    result = admit_source(contract, artifact_root=tmp_path, policy=policy)
    result.source.verify_for(contract)
    admission = json.loads(result.source_admission_bytes)
    legality = json.loads(result.legality_bytes)
    assert admission['contract_sha256'] == contract.contract_sha256
    assert admission['trust_domain_sha256'] == domain.sha256
    assert admission['policy_sha256'] == policy.sha256
    assert admission['population_sha256'] == {pop: sha(canonical_json_bytes(list(contract.populations[pop]))) for pop in ('FULL','H1','H2')}
    assert admission['retained_roles'] == [
        {'role': role, 'sha256': digest} for role, _, digest in sorted(result.source.prepared.load_trace)]
    assert legality['source_admission_sha256'] == sha(result.source_admission_bytes)
    assert legality['check_id'] == 'PRE_ADMISSION_REGISTRY_EMPTY'
    assert legality['status'] == 'PASS'


def test_resigned_nonempty_registry_rejected_before_source_construction(tmp_path):
    from c1_rail.qualification.source_admission import admit_source
    contract, _ = signed_source_case(tmp_path, change='nonempty')
    with pytest.raises(ValueError, match='LEGALITY_REGISTRY_NOT_EMPTY'):
        admit_source(contract, artifact_root=tmp_path, policy=parse_policy(build_qualification_policy()))


def test_source_failure_cannot_produce_legality_pass(tmp_path):
    from c1_rail.qualification.source_admission import admit_source
    contract, _ = signed_source_case(tmp_path, change='bad_cost')
    with pytest.raises(ValueError, match='cost capture'):
        admit_source(contract, artifact_root=tmp_path, policy=parse_policy(build_qualification_policy()))


@pytest.mark.parametrize('mapping', [{}, {'one':'dd_geometry','two':'dd_geometry'}])
def test_geometry_role_resolution_requires_one_match(mapping):
    from c1_rail.qualification.legality import geometry_role
    with pytest.raises(ValueError, match='LEGALITY_GEOMETRY_ROLE'):
        geometry_role(mapping)


def test_legality_record_rejects_unbound_admission():
    from c1_rail.qualification.legality import build_legality_record
    with pytest.raises(ValueError):
        build_legality_record(contract_sha256='a'*64, domain_sha256='b'*64,
            policy=parse_policy(build_qualification_policy()), geometry_bytes=EMPTY,
            expected_geometry_sha256=sha(EMPTY), source_admission_bytes=b'{}')


def test_prepared_replacement_cannot_supply_unretained_bars(tmp_path):
    from dataclasses import replace
    from c1_rail.qualification.production_source import ProductionSource, _prepare_domain_inputs, parse_schedule_execution_evidence
    contract, domain = signed_source_case(tmp_path)
    prepared = _prepare_domain_inputs(contract, artifact_root=tmp_path, domain=domain)
    # Preserve times, retained bytes, hashes and admission; alter only derived volume.
    path = next(path for role, path, _ in prepared.load_trace if role == 'schedule_execution_evidence')
    quotes = parse_schedule_execution_evidence(dict(prepared.retained_bytes)[path])
    claimed = {(leg, instant) for _, leg, instant, _, _ in quotes.source_rows}
    panels = tuple((leg, tuple(replace(bar, volume=bar.volume + 1) if (leg, bar.ts) not in claimed else bar for bar in bars))
                   for leg, bars in prepared.panels)
    assert panels != prepared.panels
    forged = replace(prepared, panels=panels)
    with pytest.raises(ValueError, match='prepared source derived state mismatch'):
        ProductionSource._build_from_prepared(contract, forged, domain=domain)
