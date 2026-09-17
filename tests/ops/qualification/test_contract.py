from __future__ import annotations

import base64
import hashlib
import json
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

cryptography = pytest.importorskip("cryptography")
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from c1_rail.qualification.contract import (
    ACCEPTED_HISTORICAL_PINS,
    ContractValidationError,
    ObservedBindings,
    TrustedApprovalKey,
    canonical_json_bytes,
    require_validated_frozen_contract,
    validate_frozen_contract,
)


UTC = timezone.utc
NOW = datetime(2026, 9, 15, 20, 0, tzinfo=UTC)


def _sha(label: str) -> str:
    return hashlib.sha256(label.encode()).hexdigest()


def _document() -> dict:
    from c1_rail.qualification.trust_domain import PRODUCTION_TRUST_POLICY
    sessions = ["s1", "s2", "s3", "s4", "s5"]
    roles = PRODUCTION_TRUST_POLICY.required_roles
    artifact_sha256 = {role: _sha(role) for role in roles}
    artifact_sha256.update(ACCEPTED_HISTORICAL_PINS)
    artifact_sha256["effective_settings_successor"] = _sha("reviewed-settings-successor")
    runtime = {role: artifact_sha256[role] for role in roles}
    document = {
        "schema": "frozen_qualification_contract/v1",
        "contract_id": "tradeify-f1-2026-09-15",
        "trust_domain_sha256": "d" * 64,
        "artifacts": [
            {
                "role": role,
                "path": f"reviewed/{role}.bin",
                "sha256": artifact_sha256[role],
                "producer": f"owner:{role}",
                "authority_class": "PRODUCTION_REVIEWED",
            }
            for role in roles
        ],
        "dependencies": [
            {"consumer_role": role,
             "requires_roles": ([item for item in roles if item != role]
                                if role == "qualification_runner" else [])}
            for role in roles
        ],
        "runtime_load_trace": [
            {"role": role, "sha256": runtime[role]} for role in roles
        ],
        "role_owners": [
            {"role": role, "owner": f"owner:{role}"} for role in roles
        ],
        "clocks": {
            "source": "immutable_source_metadata",
            "path": "strict_monotonic_unique_path_time",
            "deployment": "ratified_forward_calendar",
        },
        "populations": {
            "FULL": sessions,
            "H1": sessions[:3],
            "H2": sessions[3:],
        },
        "coverage": {
            "legs": ["aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7"],
            "states": ["AUTHORIZED/NORMAL", "AUTHORIZED/PROTECTED", "WATCH-1", "WATCH-2", "RETIRED"],
            "matrix": [
                {"leg": leg, "state": state,
                 "witnesses": ["allocation", "confirmed_base", "refusal", "risk", "schedule", "stop", "zero"]}
                for leg in ["aegis_6j", "dj30_mym_p250", "vanguard_mgc", "orb_mnq_v7"]
                for state in ["AUTHORIZED/NORMAL", "AUTHORIZED/PROTECTED", "WATCH-1", "WATCH-2", "RETIRED"]
            ],
        },
        "historical_pins": dict(ACCEPTED_HISTORICAL_PINS),
        "effective_settings": {
            "settings_sha256": _sha("reviewed-settings-successor"),
            "reviewed": True,
            "orb_normal_base": 1,
        },
        "replay": {
            "horizon_sessions": 500,
            "speed_horizon_sessions": 200,
            "inner_block_sessions": 5,
            "outer_months": 6,
            "root_rng_namespace": "tradeify-f1-reviewed/v1",
            "decision_rules": {
                "failure_ceiling": "0.05",
                "alpha": "0.05",
                "speed_target": "0.5",
                "speed_horizon_sessions": 200,
            },
            "stages": [
                {"name": "LEGALITY", "outcome_bearing": True, "included_in_e1_seal": True,
                 "population_counts": {}, "exact_depth": 1, "max_failures_per_population": None,
                 "rng_namespace": "legality"},
                {"name": "N1", "outcome_bearing": True, "included_in_e1_seal": True,
                 "population_counts": {"FULL": [200], "H1": [200], "H2": [200]},
                 "exact_depth": 200, "max_failures_per_population": 10, "rng_namespace": "n1"},
                {"name": "N2", "outcome_bearing": True, "included_in_e1_seal": True,
                 "population_counts": {"FULL": [970]}, "exact_depth": 970,
                 "max_failures_per_population": None, "rng_namespace": "n2"},
                {"name": "PART_B", "outcome_bearing": True, "included_in_e1_seal": True,
                 "population_counts": {"H1": [970], "H2": [970]}, "exact_depth": 970,
                 "max_failures_per_population": None, "rng_namespace": "n2"},
                {"name": "PART_A", "outcome_bearing": True, "included_in_e1_seal": True,
                 "population_counts": {"REGIME": [100, 200]}, "exact_depth": 200,
                 "max_failures_per_population": None, "rng_namespace": "part_a"},
                {"name": "N3", "outcome_bearing": True, "included_in_e1_seal": False,
                 "population_counts": {"FULL": [970], "H1": [970], "H2": [970]},
                 "exact_depth": 970, "max_failures_per_population": None, "rng_namespace": "n3"},
            ],
            "part_a": {
                "initial_panels": 100,
                "expanded_panels": 200,
                "paths_per_population_per_panel": 200,
                "expansion_center_p5": "0.95",
                "expansion_tolerance": "0.01",
                "expansion_rule": "ABS_P5_MINUS_CENTER_LTE_TOLERANCE",
                "percentile": "0.05",
                "percentile_method": "INVERSE_ECDF_LEFT",
                "sanity_rule": "P5_LTE_N2_FULL_POINT_PASS_RATE",
                "rng_namespace": "part_a",
            },
            "budget": {
                "identity_sha256": _sha("budget"),
                "maximum_cpu_seconds": 86400,
                "maximum_wall_seconds": 43200,
                "maximum_memory_bytes": 17179869184,
                "n1_paths": 600,
                "n2_paths": 2910,
                "part_a_initial_paths": 20000,
                "part_a_expanded_paths": 40000,
                "n3_paths": 2910,
            },
        },
        "initial_state": {
            "class": "PRISTINE",
            "original_basis": "100000",
            "current_equity": "100000",
            "historical_eod_peak": "100000",
            "prior_trade_days": 0,
            "prior_max_day_profit": "0",
        },
        "authority": {
            "evidence_class": "PRODUCTION_REVIEWED",
            "permits_synthetic_authority": False,
        },
        "approval_policy": {
            "freeze_scope": "FREEZE_F1",
            "freeze_authority_class": "OPERATOR",
            "freeze_key_ids": ["operator"],
        },
        "result_plan": {
            "adjudicator_role": "qualification_adjudicator",
            "adjudicator_closure_sha256": hashlib.sha256(canonical_json_bytes({
                "schema": "qualification-adjudicator-closure/v1", "sources": runtime,
            })).hexdigest(),
            "required_output_roles": ["attempt_journal", "legality_result", "n1_result", "n2_result",
                                      "part_a_result", "part_b_result", "runtime_load_trace"],
            "permitted_optional_output_roles": ["diagnostics_private"],
        },
    }
    return document


def _observed(document: dict) -> ObservedBindings:
    return ObservedBindings(
        artifact_sha256={row["path"]: row["sha256"] for row in document["artifacts"]},
        runtime_load_sha256={row["role"]: row["sha256"] for row in document["runtime_load_trace"]},
        effective_settings_sha256=document["effective_settings"]["settings_sha256"],
        orb_normal_base=1,
    )


def _approval(
    contract_bytes: bytes,
    private: Ed25519PrivateKey,
    *,
    key_id="operator",
    scope="FREEZE_F1",
    authority_class="OPERATOR",
) -> bytes:
    digest = hashlib.sha256(contract_bytes).hexdigest()
    payload = {
        "schema": "qualification_approval_payload/v1",
        "scope": scope,
        "subject_sha256": digest,
        "contract_sha256": digest,
        "issued_at": "2026-09-15T19:00:00Z",
        "expires_at": "2026-09-16T19:00:00Z",
        "authority_class": authority_class,
    }
    return canonical_json_bytes({
        "schema": "qualification_approval/v1",
        "payload": payload,
        "signature": {
            "algorithm": "Ed25519",
            "key_id": key_id,
            "value_b64": base64.b64encode(private.sign(canonical_json_bytes(payload))).decode(),
        },
    })


def _operator_domain(document):
    from test_trust_domain import operator_case, signed
    from c1_rail.qualification.trust_domain import production_trust_domain
    domain_doc, _, private, keys = operator_case()
    domain_doc["effective_settings_sha256"] = document["effective_settings"]["settings_sha256"]
    domain_doc["workload_policy"] = {
        "stage_population_depths": {
            row["name"]: row["population_counts"] for row in document["replay"]["stages"]
        },
        "horizon_sessions": document["replay"]["horizon_sessions"],
        "inner_block_sessions": document["replay"]["inner_block_sessions"],
        "outer_months": document["replay"]["outer_months"],
        "part_a_initial_panels": document["replay"]["part_a"]["initial_panels"],
        "part_a_expanded_panels": document["replay"]["part_a"]["expanded_panels"],
        "part_a_paths_per_population_per_panel":
            document["replay"]["part_a"]["paths_per_population_per_panel"],
    }
    domain = production_trust_domain(*signed(domain_doc, private), keys, now=NOW)
    return domain, private, keys


@pytest.fixture
def valid_case():
    document = _document()
    domain, private, keys = _operator_domain(document)
    document["trust_domain_sha256"] = domain.sha256
    document["approval_policy"]["freeze_key_ids"] = ["test"]
    contract_bytes = canonical_json_bytes(document)
    return (document, contract_bytes,
            _approval(contract_bytes, private, key_id="test"), keys, domain, private)


def test_valid_contract_returns_immutable_runner_interfaces(valid_case):
    document, contract_bytes, approval, keys, domain, private = valid_case
    result = validate_frozen_contract(
        contract_bytes, approval, keys, _observed(document), now=NOW, trust_domain=domain
    )

    assert result.contract_sha256 == hashlib.sha256(contract_bytes).hexdigest()
    assert result.initial_state.original_basis == 100000
    assert result.replay.horizon_sessions == 500
    assert result.replay.stages["N2"].population_counts["FULL"] == (970,)
    assert result.replay.part_a.expanded_panels == 200
    assert result.replay.part_a.should_expand(Decimal("0.94"))
    assert result.replay.part_a.should_expand(Decimal("0.96"))
    assert not result.replay.part_a.should_expand(Decimal("0.9399"))
    assert result.replay.part_a.sanity_passes(Decimal("0.94"), Decimal("0.95"))
    assert result.replay.budget.part_a_initial_paths == 20000
    assert result.required_output_roles == tuple(sorted(result.required_output_roles))
    assert result.populations["H1"] == ("s1", "s2", "s3")
    with pytest.raises(TypeError):
        result.populations["H1"] = ()


def test_validated_contract_reconstruction_and_same_object_mutation_lose_authority(valid_case):
    document, contract_bytes, approval, keys, domain, private = valid_case
    result = validate_frozen_contract(
        contract_bytes, approval, keys, _observed(document), now=NOW,
        trust_domain=domain,
    )
    assert require_validated_frozen_contract(result) is result
    with pytest.raises(ContractValidationError, match="validator-issued"):
        require_validated_frozen_contract(replace(result))
    object.__setattr__(result.replay, "horizon_sessions", True)
    with pytest.raises(ContractValidationError, match="fields changed"):
        require_validated_frozen_contract(result)


def test_mutable_contract_or_approval_buffers_cannot_become_g1_authority(valid_case):
    document, contract_bytes, approval, keys, domain, private = valid_case
    with pytest.raises(ContractValidationError, match="immutable bytes"):
        validate_frozen_contract(
            bytearray(contract_bytes), approval, keys, _observed(document), now=NOW,
            trust_domain=domain,
        )
    with pytest.raises(ContractValidationError, match="immutable bytes"):
        validate_frozen_contract(
            contract_bytes, bytearray(approval), keys, _observed(document), now=NOW,
            trust_domain=domain,
        )


@pytest.mark.parametrize(
    "mutate",
    [
        lambda b: b + b"\n",
        lambda b: b"\xef\xbb\xbf" + b,
        lambda b: b.replace(b'"schema":', b'"schema":"duplicate","schema":', 1),
        lambda b: b.replace(b'"horizon_sessions":500', b'"horizon_sessions":NaN'),
    ],
)
def test_contract_bytes_must_be_strict_canonical(valid_case, mutate):
    document, contract_bytes, approval, keys, domain, private = valid_case
    with pytest.raises(ContractValidationError, match="canonical|duplicate|UTF-8|constant"):
        validate_frozen_contract(
            mutate(contract_bytes), approval, keys, _observed(document), now=NOW
        )


def test_closed_schema_rejects_missing_and_extra_fields(valid_case):
    document, _, _, keys, domain, private = valid_case
    for changed in (deepcopy(document), deepcopy(document)):
        if "unexpected" not in changed:
            changed["unexpected"] = True
        contract_bytes = canonical_json_bytes(changed)
        with pytest.raises(ContractValidationError, match="fields"):
            validate_frozen_contract(contract_bytes, b"{}", keys, _observed(document), now=NOW)
        changed.pop("unexpected", None)
        changed.pop("contract_id")
        contract_bytes = canonical_json_bytes(changed)
        with pytest.raises(ContractValidationError, match="fields"):
            validate_frozen_contract(contract_bytes, b"{}", keys, _observed(document), now=NOW)
        break


def test_exact_historical_pins_and_corrected_striker_are_required(valid_case):
    document, _, _, keys, domain, private = valid_case
    document["historical_pins"]["striker_runtime_port"] = "c81aa59c".ljust(64, "0")
    contract_bytes = canonical_json_bytes(document)
    with pytest.raises(ContractValidationError, match="historical pins"):
        validate_frozen_contract(contract_bytes, b"{}", keys, _observed(document), now=NOW)


def test_observed_inventory_and_runtime_trace_are_closed_world(valid_case):
    document, contract_bytes, approval, keys, domain, private = valid_case
    observed = _observed(document)
    observed = ObservedBindings(
        artifact_sha256={**observed.artifact_sha256, "unlisted.bin": _sha("x")},
        runtime_load_sha256=observed.runtime_load_sha256,
        effective_settings_sha256=observed.effective_settings_sha256,
        orb_normal_base=1,
    )
    with pytest.raises(ContractValidationError, match="artifact inventory"):
        validate_frozen_contract(contract_bytes, approval, keys, observed, now=NOW)

    observed = _observed(document)
    observed = ObservedBindings(
        artifact_sha256=observed.artifact_sha256,
        runtime_load_sha256={**observed.runtime_load_sha256, "runner": _sha("drift")},
        effective_settings_sha256=observed.effective_settings_sha256,
        orb_normal_base=1,
    )
    with pytest.raises(ContractValidationError, match="runtime load"):
        validate_frozen_contract(contract_bytes, approval, keys, observed, now=NOW)


def test_role_ownership_dependency_closure_and_synthetic_authority(valid_case):
    document, _, _, keys, domain, private = valid_case
    runner_dependency = next(row for row in document["dependencies"]
                             if row["consumer_role"] == "qualification_runner")
    runner_dependency["requires_roles"].append("missing")
    with pytest.raises(ContractValidationError, match="dependency"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)

    document = _document()
    document["artifacts"][0]["authority_class"] = "TEST_ONLY"
    with pytest.raises(ContractValidationError, match="authority|synthetic|TEST_ONLY"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)


def test_qualification_runner_must_reach_every_frozen_role(valid_case):
    document, _, _, keys, domain, private = valid_case
    runner = next(row for row in document["dependencies"]
                  if row["consumer_role"] == "qualification_runner")
    runner["requires_roles"] = []

    with pytest.raises(ContractValidationError, match="runner.*reach"):
        validate_frozen_contract(
            canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)


def test_population_partition_clock_and_coverage_are_exact(valid_case):
    document, _, _, keys, domain, private = valid_case
    document["populations"]["H2"] = ["s3", "s4", "s5"]
    with pytest.raises(ContractValidationError, match="partition"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)

    document = _document()
    document["clocks"]["path"] = document["clocks"]["source"]
    with pytest.raises(ContractValidationError, match="clock"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)

    document = _document()
    document["coverage"]["legs"].pop()
    with pytest.raises(ContractValidationError, match="coverage"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)

    document = _document()
    document["coverage"]["matrix"][0]["witnesses"].remove("refusal")
    with pytest.raises(ContractValidationError, match="witnesses"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)


def test_stage_depth_part_a_and_numeric_budgets_are_frozen_exactly(valid_case):
    document, _, _, keys, domain, private = valid_case
    document["replay"]["stages"][1]["exact_depth"] = 199
    with pytest.raises(ContractValidationError, match="stage|N1"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)

    document = _document()
    document["replay"]["part_a"]["expansion_tolerance"] = "0.0101"
    with pytest.raises(ContractValidationError, match="Part A"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)

    document = _document()
    document["replay"]["budget"]["part_a_initial_paths"] -= 1
    with pytest.raises(ContractValidationError, match="budget"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)


def test_signed_synthetic_depths_are_derived_not_hardcoded():
    document = _document()
    stages = {row["name"]: row for row in document["replay"]["stages"]}
    for population in ("FULL", "H1", "H2"):
        stages["N1"]["population_counts"][population] = [50]
    stages["N1"]["exact_depth"] = 50
    stages["N1"]["max_failures_per_population"] = 2
    stages["N2"]["exact_depth"] = 60
    stages["N2"]["population_counts"] = {"FULL": [60]}
    stages["PART_B"]["exact_depth"] = 60
    stages["PART_B"]["population_counts"] = {"H1": [60], "H2": [60]}
    stages["PART_A"]["exact_depth"] = 25
    document["replay"]["part_a"]["paths_per_population_per_panel"] = 25
    stages["N3"]["exact_depth"] = 70
    stages["N3"]["population_counts"] = {"FULL": [70], "H1": [70], "H2": [70]}
    budget = document["replay"]["budget"]
    budget.update(n1_paths=150, n2_paths=180, part_a_initial_paths=2500,
                  part_a_expanded_paths=5000, n3_paths=210)
    domain, private, keys = _operator_domain(document)
    document["trust_domain_sha256"] = domain.sha256
    document["approval_policy"]["freeze_key_ids"] = ["test"]
    raw = canonical_json_bytes(document)
    result = validate_frozen_contract(
        raw, _approval(raw, private, key_id="test"), keys,
        _observed(document), now=NOW, trust_domain=domain)
    assert result.replay.stages["N2"].exact_depth == 60
    assert result.replay.budget.part_a_expanded_paths == 5000


def test_pristine_e1_state_and_block_divisibility_are_enforced(valid_case):
    document, _, _, keys, domain, private = valid_case
    document["initial_state"]["current_equity"] = "99999"
    with pytest.raises(ContractValidationError, match="PRISTINE"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)

    document = _document()
    document["replay"]["horizon_sessions"] = 501
    with pytest.raises(ContractValidationError, match="divisible"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)


def test_freeze_signature_key_must_be_enrolled_by_contract(valid_case):
    document, _, _, keys, domain, private = valid_case
    document["approval_policy"]["freeze_key_ids"] = ["different-operator"]
    contract_bytes = canonical_json_bytes(document)
    private = Ed25519PrivateKey.generate()
    public = private.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    with pytest.raises(ContractValidationError, match="enroll"):
        validate_frozen_contract(
            contract_bytes, _approval(contract_bytes, private),
            {"operator": TrustedApprovalKey("operator", public, "OPERATOR")},
            _observed(document), now=NOW, trust_domain=domain,
        )

def test_historical_orb_qty_two_is_refused_not_silently_overridden(valid_case):
    document, contract_bytes, approval, keys, domain, private = valid_case
    observed = _observed(document)
    observed = ObservedBindings(
        artifact_sha256=observed.artifact_sha256,
        runtime_load_sha256=observed.runtime_load_sha256,
        effective_settings_sha256=observed.effective_settings_sha256,
        orb_normal_base=2,
    )
    with pytest.raises(ContractValidationError, match="ORB.*fixed normal base 1"):
        validate_frozen_contract(contract_bytes, approval, keys, observed, now=NOW,
                                 trust_domain=domain)

    document["effective_settings"]["settings_sha256"] = ACCEPTED_HISTORICAL_PINS["historical_effective_inputs"]
    document["effective_settings"]["orb_normal_base"] = 1
    with pytest.raises(ContractValidationError, match="successor|qty=2"):
        validate_frozen_contract(canonical_json_bytes(document), b"{}", keys, _observed(document), now=NOW)


def test_detached_approval_binds_scope_subject_time_revocation_and_authority(valid_case):
    document, contract_bytes, approval, keys, domain, private = valid_case
    validate_frozen_contract(contract_bytes, approval, keys, _observed(document), now=NOW,
                             trust_domain=domain)

    wrong_scope = _approval(contract_bytes, private, key_id="test",
                            scope="APPROVE_E1_EXACT_DEPTH")
    with pytest.raises(ContractValidationError, match="scope"):
        validate_frozen_contract(contract_bytes, wrong_scope, keys, _observed(document), now=NOW,
                                 trust_domain=domain)

    revoked = {"test": TrustedApprovalKey("test", keys["test"].public_key, "OPERATOR",
                                           NOW - timedelta(seconds=1))}
    with pytest.raises(ContractValidationError, match="revoked"):
        validate_frozen_contract(contract_bytes, approval, revoked, _observed(document), now=NOW,
                                 trust_domain=domain)

    test_key = {"test": TrustedApprovalKey("test", keys["test"].public_key, "TEST_ONLY")}
    with pytest.raises(ContractValidationError, match="authority|fingerprint"):
        validate_frozen_contract(contract_bytes, approval, test_key, _observed(document), now=NOW,
                                 trust_domain=domain)

    test_document = _document()
    test_document["approval_policy"]["freeze_authority_class"] = "TEST_ONLY"
    test_contract_bytes = canonical_json_bytes(test_document)
    test_approval = _approval(test_contract_bytes, private, authority_class="TEST_ONLY")
    explicit_test_key = {"operator": TrustedApprovalKey(
        "operator", keys["test"].public_key, "TEST_ONLY")}
    with pytest.raises(TypeError, match="allow_test_authority"):
        validate_frozen_contract(
            test_contract_bytes, test_approval, explicit_test_key, _observed(test_document),
            now=NOW, allow_test_authority=True,
        )
