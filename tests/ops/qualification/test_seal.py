from __future__ import annotations

import base64
import hashlib
import shutil
import tempfile
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from cryptography.hazmat.primitives import serialization

from c1_rail.qualification.contract import (
    canonical_json_bytes,
)
from c1_rail.qualification.attempt import AttemptStore
from c1_rail.qualification.preflight import (
    exact_depth_subject, preflight_binding_bytes, validate_e1_preflight,
)
from c1_rail.qualification.model import PathOutcome
from c1_rail.qualification.result_adjudication import (
    frozen_adjudicator,
)
from c1_rail.qualification.seal import (
    AuthenticatedResult,
    ResultValidationError,
    TrustedResultKey,
    inspect_result_authentication,
    _reauthenticate,
    _require_attempt_store_binding,
    _verify_external_record,
    authenticate_result,
    authenticated_result_claim,
    commit_authenticated_result,
    e1_seal_payload,
    seal_e1_pass,
    validate_result_envelope,
    verify_authenticated_result_claim,
)


NOW = datetime(2026, 9, 15, 20, tzinfo=timezone.utc)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


_CONTEXTS = {}


def context(contract):
    return _CONTEXTS[contract.contract_sha256]


def contract():
    from signed_g5_fixture import build_signed_g5_fixture
    fixture = build_signed_g5_fixture(Path(tempfile.mkdtemp()))
    _CONTEXTS[fixture.contract.contract_sha256] = fixture
    return fixture.contract

def outcomes(frozen, *, status="PASS"):
    failure = None if status == "PASS" else "synthetic-path"
    rows = {}
    shapes = {
        name: {p: counts[0] * (frozen.replay.part_a.paths_per_population_per_panel
                             if name == 'PART_A' else 1)
               for p, counts in spec.population_counts.items()}
        for name, spec in frozen.stage_specs.items() if spec.included_in_e1_seal
    }
    for name, populations in shapes.items():
        rows[name] = {
            population: tuple(PathOutcome(
                status, 1 if status == "PASS" else None, failure, ())
                for _ in range(count))
            for population, count in populations.items()
        }
    return rows


def outcome_digest(rows) -> str:
    value = {
        population: [{"diagnostics": [list(item) for item in row.diagnostics],
                      "failure_reason": row.failure_reason,
                      "sessions_to_pass": row.sessions_to_pass,
                      "status": row.status} for row in population_rows]
        for population, population_rows in rows.items()
    }
    return sha(canonical_json_bytes(value))


def path_inventory(path_rows, frozen):
    records = []
    seed_ordinal = 1
    for stage, populations in path_rows.items():
        for population, rows in populations.items():
            for flat_index, row in enumerate(rows):
                index = flat_index % frozen.replay.part_a.paths_per_population_per_panel if stage == "PART_A" else flat_index
                outcome_record = {
                    "diagnostics": [list(item) for item in row.diagnostics],
                    "failure_reason": row.failure_reason,
                    "sessions_to_pass": row.sessions_to_pass,
                    "status": row.status,
                }
                records.append({
                    "stage": stage,
                    "population": population,
                    "path_index": index,
                    "panel_id": (panel_record(frozen,flat_index // frozen.replay.part_a.paths_per_population_per_panel)["panel_id"]
                                 if stage == "PART_A" else None),
                    "seed_input_sha256": sha(canonical_json_bytes(
                        checkpoint_seed_input(
                            frozen, stage, population, index,
                            flat_index // frozen.replay.part_a.paths_per_population_per_panel if stage == "PART_A" else None))),
                    "outcome_sha256": sha(canonical_json_bytes(outcome_record)),
                })
                seed_ordinal += 1
    return canonical_json_bytes({
        "schema": "qualification_path_inventory/v1", "records": records,
        "trust_domain_sha256": frozen.trust_domain_sha256,
    })


def checkpoint_seed_input(frozen, stage, population, path_index, panel_index):
    from c1_rail.qualification.orchestration import seed_input
    return __import__('json').loads(seed_input(frozen,
        stage='n1' if stage=='N1' else 'n2',
        population='FULL' if stage=='PART_A' else population,
        panel_index=panel_index,path_index=path_index,synthetic=True).canonical_bytes)


def panel_record(frozen,index):
    from c1_rail.qualification.orchestration import panel_identity
    source=tuple(frozen.populations['FULL'])
    identity=panel_identity(frozen,SimpleNamespace(index=index,source_session_ids=source))
    return dict(panel_index=index,panel_id=identity,source_session_ids=list(source))


def checkpoint_plan(checkpoint, inventory_document, frozen, exact_approval):
    stages = {
        "N1": ("N1",), "CUTOFF": (), "N2": ("N2", "PART_B"),
        "PART_A": ("PART_A",),
    }[checkpoint]
    seed_inputs = [
        checkpoint_seed_input(
            frozen, row["stage"], row["population"], row["path_index"],
            index // frozen.replay.part_a.paths_per_population_per_panel
            if row["panel_id"] is not None else None)
        for index,row in enumerate([r for r in inventory_document["records"] if r["stage"] in stages])
    ]
    if checkpoint=='PART_A':
        from c1_rail.qualification.orchestration import _part_a_seeds
        seed_inputs=[__import__('json').loads(s.canonical_bytes) for s in _part_a_seeds(frozen,True)]
    return {
        "schema": "e1_checkpoint_plan/v1",
        "checkpoint": checkpoint,
        "contract_sha256": frozen.contract_sha256,
        "trust_domain_sha256": frozen.trust_domain_sha256,
        "synthetic": True,
        "exact_depth_approval_sha256": exact_approval,
        "horizon_sessions": frozen.replay.horizon_sessions,
        "seed_inputs": seed_inputs,
        "extra": ({'initial_panels':frozen.replay.part_a.initial_panels,
                   'expanded_panels':frozen.replay.part_a.expanded_panels}
                  if checkpoint=='PART_A' else None),
    }


def stage_input_digests(inventory_bytes, *, contract_sha256="a" * 64,
                        exact_depth_approval_sha256="c" * 64):
    document = __import__("json").loads(inventory_bytes)
    stages = ("LEGALITY", "N1", "N2", "PART_B", "PART_A")
    return {
        stage: sha(canonical_json_bytes(
            {"contract_sha256": contract_sha256,
             "trust_domain_sha256": document["trust_domain_sha256"],
             "exact_depth_approval_sha256": exact_depth_approval_sha256,
             "stage": stage}
            if stage == "LEGALITY" else {
                "stage": stage,
                "paths": [{key: record[key] for key in (
                    "population", "path_index", "panel_id", "seed_input_sha256")}
                          for record in document["records"] if record["stage"] == stage],
            }))
        for stage in stages
    }


def result_case(*, completion="COMPLETE", verdict="PASS", path_status="PASS"):
    frozen = contract()
    path_rows = outcomes(frozen, status=path_status)
    inventory = path_inventory(path_rows, frozen)
    output_bytes = {
        "private-result": b"private synthetic result",
        "public-projection": b"public synthetic projection",
    }
    journal = b"canonical journal export"
    runtime = canonical_json_bytes(dict(frozen.runtime_load_sha256))
    fixture = context(frozen)
    approval_private = fixture.private_keys['test-freeze']
    approval_keys = fixture.trusted_keys
    subject = exact_depth_subject(frozen, attempt_id="attempt-1")
    approval_payload = {
        "schema": "qualification_approval_payload/v1",
        "scope": "APPROVE_E1_EXACT_DEPTH",
        "subject_sha256": sha(subject),
        "contract_sha256": frozen.contract_sha256,
        "issued_at": "2026-09-15T19:00:00Z",
        "expires_at": "2026-09-16T19:00:00Z",
        "authority_class": "TEST_ONLY",
    }
    approval_bytes = canonical_json_bytes({
        "schema": "qualification_approval/v1",
        "payload": approval_payload,
        "signature": {
            "algorithm": "Ed25519", "key_id": "test-freeze",
            "value_b64": base64.b64encode(approval_private.sign(
                canonical_json_bytes(approval_payload))).decode(),
        },
    })
    output_parent = __import__("pathlib").Path(tempfile.mkdtemp())
    preflight = validate_e1_preflight(
        frozen, attempt_id="attempt-1", output_root=output_parent / "outputs",
        exact_depth_approval_bytes=approval_bytes, trusted_keys=approval_keys,
        now=NOW, trust_domain=frozen.trust_domain,
    )
    exact = preflight.exact_depth_approval.approval_sha256
    input_digests = stage_input_digests(
        inventory, contract_sha256=frozen.contract_sha256,
        exact_depth_approval_sha256=exact,
    )
    document = {
        "schema": "qualification_result_envelope/v1",
        "attempt_id": "attempt-1",
        "contract_sha256": frozen.contract_sha256,
        "trust_domain_sha256": frozen.trust_domain_sha256,
        "shared_manifest_sha256": next(a.sha256 for a in frozen.artifacts if a.role == "shared_manifest"),
        "exact_depth_approval_sha256": exact,
        "producer": {"producer_id": "runner", "boot_id": "boot-1",
                     "tool_sha256": frozen.runtime_load_sha256["qualification_runner"],
                     "runtime_sha256": frozen.runtime_load_sha256["runtime_distribution"]},
        "started_utc": "2026-09-15T20:00:00Z",
        "completed_utc": None if completion == "PARTIAL" else "2026-09-15T20:00:00Z",
        "completion": completion,
        "verdict": verdict,
        "terminal_reason": None if verdict in ("PASS", "NONE") else "SYNTHETIC_TERMINAL",
        "stage_results": [
            {"stage": spec.name,
             "status": ("PASS" if not spec.population_counts
                        or path_status == "PASS" else "FAIL"),
             "input_sha256": input_digests[spec.name],
             "output_sha256": outcome_digest(path_rows[spec.name]),
             "population_counts": {
                 name: allowed[0] for name, allowed in spec.population_counts.items()
             }}
            for spec in frozen.stage_specs.values() if spec.included_in_e1_seal
        ],
        "outputs": [
            {"role": role, "path": f"{role}.bin", "sha256": sha(raw), "byte_length": len(raw),
             "privacy": "PRIVATE" if role == "private-result" else "PUBLIC_PROJECTION"}
            for role, raw in output_bytes.items()
        ],
        "path_inventory_sha256": sha(inventory),
        "runtime_load_trace_sha256": sha(runtime),
        "attempt_journal_sha256": sha(journal),
        "previous_result_sha256": None,
    }
    return (frozen, canonical_json_bytes(document), output_bytes, path_rows,
            inventory, journal, runtime, preflight, approval_bytes, approval_keys)


def validate(case, *, mutate_checkpoint_plan=None):
    (frozen, raw, outputs, paths, inventory, journal, runtime, preflight,
     approval_bytes, approval_keys) = case
    output_root = Path(preflight.output_root)
    for role, payload in outputs.items():
        (output_root / f"{role}.bin").write_bytes(payload)
    input_digests = stage_input_digests(
        inventory, contract_sha256=frozen.contract_sha256,
        exact_depth_approval_sha256=(
            preflight.exact_depth_approval.approval_sha256),
    )
    completion = __import__("json").loads(raw)["completion"]
    checkpoint_inputs = {
        "N1": {"N1": input_digests["N1"]} if "N1" in paths else {},
        "CUTOFF": {},
        "N2": ({"N2": input_digests["N2"],
                "PART_B": input_digests["PART_B"]}
               if "N2" in paths and "PART_B" in paths else {}),
        "PART_A": ({"PART_A": input_digests["PART_A"]}
                   if "PART_A" in paths else {}),
    }
    required_checkpoints = ({"N1", "CUTOFF"}
                            | ({"N2"} if "N2" in paths else set())
                            | ({"PART_A"} if "PART_A" in paths else set()))
    inventory_document = __import__("json").loads(inventory)
    normalized = {
        stage: {
            population: [{
                "diagnostics": [list(item) for item in row.diagnostics],
                "failure_reason": row.failure_reason,
                "sessions_to_pass": row.sessions_to_pass,
                "status": row.status,
            } for row in rows]
            for population, rows in populations.items()
        }
        for stage, populations in paths.items()
        if all(isinstance(row, PathOutcome)
               for rows in populations.values() for row in rows)
    }
    try:
        receipt_decisions = frozen_adjudicator(
            frozen, retained_source_bytes=context(frozen).retained_source_bytes,
            runtime_inventory=context(frozen).runtime_inventory)(
                paths, inventory_document)
    except Exception:
        receipt_decisions = {}
    checkpoint_stages = {
        "N1": ("N1",), "CUTOFF": (), "N2": ("N2", "PART_B"),
        "PART_A": ("PART_A",),
    }
    checkpoint_decisions = {
        "N1": (), "CUTOFF": ("N1",), "N2": ("N2", "PART_B"),
        "PART_A": ("PART_A",),
    }
    checkpoint_snapshot = []
    checkpoint_payloads = {}
    for checkpoint in ("N1", "CUTOFF", "N2", "PART_A"):
        state = ("COMPLETED" if completion == "COMPLETE"
                 and checkpoint in required_checkpoints else "PENDING")
        plan = checkpoint_plan(
            checkpoint, inventory_document, frozen,
            preflight.exact_depth_approval.approval_sha256)
        if mutate_checkpoint_plan is not None:
            mutate_checkpoint_plan(checkpoint, plan)
        binding = canonical_json_bytes(plan)
        dispatch_digest = sha(canonical_json_bytes({"dispatch": checkpoint}))
        retained_stages = tuple(
            stage for stage in checkpoint_stages[checkpoint] if stage in paths)
        receipt = (canonical_json_bytes({
            "schema": "e1_checkpoint_receipt/v1",
            "checkpoint": checkpoint,
            "attempt_id": "attempt-1",
            "contract_sha256": frozen.contract_sha256,
            "trust_domain_sha256": frozen.trust_domain_sha256,
            "binding_sha256": sha(binding),
            "dispatch_event_digest": dispatch_digest,
            "synthetic": True,
            "decisions": {
                stage: receipt_decisions[stage]
                for stage in checkpoint_decisions[checkpoint]
                if stage in receipt_decisions
            },
            "stage_input_sha256": checkpoint_inputs[checkpoint],
            "path_inventory": [
                row for row in inventory_document["records"]
                if row["stage"] in retained_stages
            ],
            "outcomes": {stage: normalized.get(stage, {}) for stage in retained_stages},
            "extra": ({'panels':[panel_record(frozen,i) for i in range(
                len(paths['PART_A']['REGIME'])//frozen.replay.part_a.paths_per_population_per_panel)]}
                if checkpoint=='PART_A' else {}),
        }) if state == "COMPLETED" else None)
        checkpoint_snapshot.append({
            "checkpoint": checkpoint, "state": state,
            "binding_bytes": binding if state == "COMPLETED" else None,
            "dispatch_event_digest": dispatch_digest if state == "COMPLETED" else None,
            "receipt_bytes": receipt,
        })
        checkpoint_payloads[checkpoint] = (binding, receipt, state)
    journal_path = Path(tempfile.mkdtemp()) / "attempt.sqlite"
    store = AttemptStore.open(
        journal_path, campaign_id="attempt-1",
        contract_digest=frozen.contract_sha256, trust_domain_sha256=frozen.trust_domain_sha256,
        boot_id="boot-1", now=NOW,
    )
    store.reserve("TB_E1", preflight_binding_bytes(preflight), now=NOW)
    parent = store.claimed_reservation("TB_E1")
    store.start_once("TB_E1", parent, now=NOW)
    parent = store.claimed_reservation("TB_E1")
    for index, checkpoint in enumerate(("N1", "CUTOFF", "N2", "PART_A"), 1):
        binding, receipt, state = checkpoint_payloads[checkpoint]
        if state != "COMPLETED":
            break
        dispatch = store.start_checkpoint_once(
            checkpoint, parent, binding, now=NOW)
        store.consume_checkpoint_dispatch(dispatch)
        receipt_document = __import__("json").loads(receipt)
        receipt_document["dispatch_event_digest"] = dispatch.dispatch_event_digest
        receipt = canonical_json_bytes(receipt_document)
        store.complete_checkpoint(
            checkpoint, dispatch, receipt, now=NOW)
    raw_document = __import__("json").loads(raw)
    raw_document["attempt_journal_sha256"] = sha(journal_path.read_bytes())
    raw = canonical_json_bytes(raw_document)
    return validate_result_envelope(
        frozen, raw, path_outcomes=paths,
        path_inventory_bytes=inventory,
        attempt_store=store, runtime_load_trace_bytes=runtime,
        preflight_receipt=preflight,
        exact_depth_approval_bytes=approval_bytes,
        exact_depth_trusted_keys=approval_keys,
        approval_now=NOW,
        stage_input_sha256={name: input_digests[name] for name in paths},
        adjudicator=frozen_adjudicator(
            frozen, retained_source_bytes=context(frozen).retained_source_bytes,
            runtime_inventory=context(frozen).runtime_inventory),
        trust_domain=frozen.trust_domain,
    )


def signed_record(result, private, *, schema, scope, subject, authority, attempt="attempt-1"):
    payload = {"scope": scope, "subject_sha256": subject,
               "contract_sha256": result.contract_sha256,
               "trust_domain_sha256": result.trust_domain_sha256, "attempt_id": attempt,
               "issued_utc": "2026-09-15T19:00:00Z",
               "expires_utc": "2026-09-16T19:00:00Z"}
    return canonical_json_bytes({
        "schema": schema,
        "payload": payload,
        "signature": {"algorithm": "Ed25519", "key_id": authority,
                      "value_b64": base64.b64encode(
                          private.sign(canonical_json_bytes(payload))).decode()},
    })


def key(private, key_id, authority, scope):
    public = private.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return TrustedResultKey(key_id, public, authority, (scope,))


def _historical_claim(authenticated, *, trusted_keys, now, trust_domain):
    """Fixture-only v3 store input; never a protected execution capability."""
    from c1_rail.qualification.attempt import _issue_validated_result_claim
    verified = _reauthenticate(authenticated, trusted_keys=trusted_keys, now=now,
                              trust_domain=trust_domain)
    result = verified.result
    assert result.completion == 'COMPLETE' and result.verdict == 'PASS'
    return _issue_validated_result_claim(
        campaign_id=result.attempt_id, contract_digest=result.contract_sha256,
        stage='TB_E1', manifest_sha256=result.result_sha256, outcome='PASS',
        producer_scope='ATTEST_E1_RESULT', attestation_digest=verified.authentication_sha256,
        result_stages=tuple(result.stage_output_sha256))


def _historical_commit(store, authenticated, *, trusted_keys, now, trust_domain):
    """Exercise the old private journal mechanics, not the retired G5 route."""
    _require_attempt_store_binding(authenticated.result, store, precommit=True)
    claim = _historical_claim(authenticated, trusted_keys=trusted_keys, now=now,
                            trust_domain=trust_domain)
    return store._commit_validated_result('TB_E1', authenticated.result.canonical_bytes,
                                         outcome='PASS', validation_claim=claim, now=now)


def _inspect_historical_seal(authenticated, record, *, trusted_keys, trust_domain):
    """Read-only signature verification; does not commit or issue a seal."""
    return _verify_external_record(
        record, schema='e1_qualification_seal/v1', scope='SEAL_E1_PASS',
        subject_sha256=sha(e1_seal_payload(authenticated, sealed_utc=NOW)),
        contract_sha256=authenticated.result.contract_sha256,
        attempt_id=authenticated.result.attempt_id, trusted_keys=trusted_keys,
        now=NOW, trust_domain=trust_domain, enrolled_key_ids=trust_domain.seal_key_ids)


def test_historical_complete_pass_signatures_inspect_but_active_authority_is_retired():
    result = validate(result_case())
    producer_private = context(result).private_keys["test-producer"]
    attestation = signed_record(
        result, producer_private, schema="qualification_result_authentication/v1",
        scope="ATTEST_E1_RESULT", subject=result.result_sha256, authority="test-producer")
    producer_keys = {
        "test-producer": key(producer_private, "test-producer", "TEST_ONLY",
                        "ATTEST_E1_RESULT")
    }
    authenticated = inspect_result_authentication(
        result, attestation, trusted_keys=producer_keys, now=NOW, trust_domain=context(result).domain)
    claim = _historical_claim(
        authenticated, trusted_keys=producer_keys, now=NOW, trust_domain=context(result).domain)
    assert claim.outcome == "PASS"
    assert not verify_authenticated_result_claim(
        authenticated, claim, trusted_keys=producer_keys, now=NOW, trust_domain=context(result).domain)
    attempt_store = AttemptStore(
        Path(result.attempt_journal_path), result.attempt_id,
        result.contract_sha256, "boot-1", result.trust_domain_sha256)
    seal_private = context(result).private_keys["test-seal"]
    payload = e1_seal_payload(authenticated, sealed_utc=NOW)
    seal_record = signed_record(
        result, seal_private, schema="e1_qualification_seal/v1", scope="SEAL_E1_PASS",
        subject=sha(payload), authority="test-seal")
    before = attempt_store.events()
    with pytest.raises(ResultValidationError, match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        authenticate_result(result, attestation, trusted_keys=producer_keys, now=NOW,
                            trust_domain=context(result).domain)
    with pytest.raises(ResultValidationError, match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        authenticated_result_claim(authenticated, trusted_keys=producer_keys, now=NOW,
                                   trust_domain=context(result).domain)
    with pytest.raises(ResultValidationError, match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        commit_authenticated_result(attempt_store, authenticated, trusted_keys=producer_keys,
                                    now=NOW, trust_domain=context(result).domain)
    with pytest.raises(ResultValidationError, match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        seal_e1_pass(
            authenticated, seal_record, sealed_utc=NOW,
            trusted_keys={"test-seal": key(seal_private, "test-seal", "TEST_ONLY",
                                      "SEAL_E1_PASS")}, now=NOW,
            result_trusted_keys=producer_keys, attempt_store=attempt_store,
        trust_domain=context(result).domain)
    assert attempt_store.events() == before
    _historical_commit(
        attempt_store, authenticated, trusted_keys=producer_keys, now=NOW, trust_domain=context(result).domain)

    assert _inspect_historical_seal(
        authenticated, seal_record,
        trusted_keys={"test-seal": key(seal_private, "test-seal", "TEST_ONLY",
                                  "SEAL_E1_PASS")},
        trust_domain=context(result).domain) == 'test-seal'
    before = attempt_store.events()
    with pytest.raises(ResultValidationError, match='LEGACY_QUALIFICATION_INSPECTION_ONLY'):
        seal_e1_pass(authenticated, seal_record, sealed_utc=NOW,
            trusted_keys={'test-seal': key(seal_private, 'test-seal', 'TEST_ONLY', 'SEAL_E1_PASS')},
            now=NOW, result_trusted_keys=producer_keys, attempt_store=attempt_store,
            trust_domain=context(result).domain)
    assert attempt_store.events() == before
    sealed = payload
    assert b'"grants_activation":false' in sealed
    assert b'"grants_admission":false' in sealed
    assert b'"grants_deployment":false' in sealed
    assert b'"grants_n3":false' in sealed


def test_historical_authentication_refuses_reconstructed_validated_result():
    result = validate(result_case())
    fixture = context(result)
    private = fixture.private_keys['test-producer']
    attestation = signed_record(result, private, schema='qualification_result_authentication/v1',
        scope='ATTEST_E1_RESULT', subject=result.result_sha256, authority='test-producer')
    keys = {'test-producer': key(private, 'test-producer', 'TEST_ONLY', 'ATTEST_E1_RESULT')}
    with pytest.raises(ResultValidationError, match='validator-issued'):
        inspect_result_authentication(replace(result, verdict='FAIL'), attestation,
            trusted_keys=keys, now=NOW, trust_domain=fixture.domain)


def test_historical_authentication_subclass_cannot_supply_unverified_digest():
    class ForgedAuthentication(AuthenticatedResult):
        def __eq__(self, other):
            return True

        def __ne__(self, other):
            return False

    result = validate(result_case())
    fixture = context(result)
    private = fixture.private_keys['test-producer']
    attestation = signed_record(result, private, schema='qualification_result_authentication/v1',
        scope='ATTEST_E1_RESULT', subject=result.result_sha256, authority='test-producer')
    keys = {'test-producer': key(private, 'test-producer', 'TEST_ONLY', 'ATTEST_E1_RESULT')}
    authenticated = inspect_result_authentication(result, attestation, trusted_keys=keys,
        now=NOW, trust_domain=fixture.domain)
    forged = ForgedAuthentication(result, 'f' * 64, authenticated.key_id,
                                  attestation, fixture.domain.sha256)
    with pytest.raises(ResultValidationError, match='authenticated result'):
        _reauthenticate(forged, trusted_keys=keys, now=NOW, trust_domain=fixture.domain)


def test_historical_reauthentication_consumes_verified_digest_despite_field_equality():
    class EqualDigest(str):
        def __eq__(self, other):
            return True

    result = validate(result_case())
    fixture = context(result)
    private = fixture.private_keys['test-producer']
    attestation = signed_record(result, private, schema='qualification_result_authentication/v1',
        scope='ATTEST_E1_RESULT', subject=result.result_sha256, authority='test-producer')
    keys = {'test-producer': key(private, 'test-producer', 'TEST_ONLY', 'ATTEST_E1_RESULT')}
    supplied = AuthenticatedResult(result, EqualDigest('f' * 64), 'test-producer',
                                   attestation, fixture.domain.sha256)
    claim = _historical_claim(supplied, trusted_keys=keys, now=NOW,
                                       trust_domain=fixture.domain)
    assert type(claim.attestation_digest) is str
    assert claim.attestation_digest == sha(attestation)


@pytest.mark.parametrize('refresh_authentication', [False, True])
def test_historical_v3_private_commit_retry_preserves_exact_authentication_after_restart(refresh_authentication):
    import json
    from c1_rail.qualification.attempt import AttemptConflict

    result = validate(result_case())
    fixture = context(result)
    private = fixture.private_keys['test-producer']
    attestation = signed_record(result, private, schema='qualification_result_authentication/v1',
        scope='ATTEST_E1_RESULT', subject=result.result_sha256, authority='test-producer')
    keys = {'test-producer': key(private, 'test-producer', 'TEST_ONLY', 'ATTEST_E1_RESULT')}
    authenticated = inspect_result_authentication(result, attestation, trusted_keys=keys,
        now=NOW, trust_domain=fixture.domain)
    store = AttemptStore(Path(result.attempt_journal_path), result.attempt_id,
                         result.contract_sha256, 'boot-1', result.trust_domain_sha256)
    receipt = _historical_commit(store, authenticated, trusted_keys=keys,
        now=NOW, trust_domain=fixture.domain)
    reopened = AttemptStore.open(store.path, campaign_id=result.attempt_id,
        contract_digest=result.contract_sha256, trust_domain_sha256=fixture.domain.sha256,
        boot_id='retry-boot', now=NOW)
    before = reopened.events()
    if refresh_authentication:
        document = json.loads(attestation)
        document['payload']['issued_utc'] = '2026-09-15T19:30:00Z'
        document['signature']['value_b64'] = base64.b64encode(
            private.sign(canonical_json_bytes(document['payload']))).decode()
        refreshed = inspect_result_authentication(result, canonical_json_bytes(document),
            trusted_keys=keys, now=NOW, trust_domain=fixture.domain)
        with pytest.raises(AttemptConflict, match='result'):
            _historical_commit(reopened, refreshed, trusted_keys=keys,
                now=NOW, trust_domain=fixture.domain)
    else:
        assert _historical_commit(reopened, authenticated, trusted_keys=keys,
            now=NOW, trust_domain=fixture.domain) == receipt
    assert reopened.events() == before
    assert reopened.result('TB_E1')['receipt_bytes'] == receipt


def test_checkpoint_plan_seed_inputs_must_bind_retained_result_inputs():
    def mutate(checkpoint, plan):
        if checkpoint == "N1":
            plan["seed_inputs"][0]["seed"] += 1

    with pytest.raises(ResultValidationError, match="checkpoint plan.*input"):
        validate(result_case(), mutate_checkpoint_plan=mutate)


def test_authenticated_result_cannot_move_to_a_lookalike_journal(tmp_path):
    result = validate(result_case())
    private = context(result).private_keys["test-producer"]
    attestation = signed_record(
        result, private, schema="qualification_result_authentication/v1",
        scope="ATTEST_E1_RESULT", subject=result.result_sha256,
        authority="test-producer")
    keys = {"test-producer": key(private, "test-producer", "TEST_ONLY",
                            "ATTEST_E1_RESULT")}
    authenticated = inspect_result_authentication(
        result, attestation, trusted_keys=keys, now=NOW, trust_domain=context(result).domain)
    copied_path = tmp_path / "lookalike.sqlite"
    shutil.copyfile(result.attempt_journal_path, copied_path)
    lookalike = AttemptStore(
        copied_path, result.attempt_id, result.contract_sha256, "boot-1", result.trust_domain_sha256)

    with pytest.raises(ResultValidationError, match="journal binding"):
        _historical_commit(
            lookalike, authenticated, trusted_keys=keys, now=NOW, trust_domain=context(result).domain)


def test_partial_and_nonpass_results_never_seal():
    partial_case = list(result_case(completion="PARTIAL", verdict="NONE"))
    document = __import__("json").loads(partial_case[1])
    document["stage_results"] = document["stage_results"][:2]
    document["outputs"] = document["outputs"][:1]
    partial_case[1] = canonical_json_bytes(document)
    partial_case[2] = {"private-result": partial_case[2]["private-result"]}
    partial_case[3] = {name: partial_case[3][name] for name in ("LEGALITY", "N1")}
    partial_case[4] = path_inventory(partial_case[3], partial_case[0])
    document = __import__("json").loads(partial_case[1])
    document["path_inventory_sha256"] = sha(partial_case[4])
    partial_case[1] = canonical_json_bytes(document)
    partial = validate(tuple(partial_case))
    auth = SimpleNamespace(result=partial, authentication_sha256="a" * 64)
    with pytest.raises(ResultValidationError, match="complete PASS"):
        e1_seal_payload(auth, sealed_utc=NOW)

    failed_case = list(result_case(verdict="FAIL", path_status="FAILURE"))
    failed_document = __import__("json").loads(failed_case[1])
    failed_document["stage_results"] = failed_document["stage_results"][:2]
    failed_case[3] = {name: failed_case[3][name] for name in ("LEGALITY", "N1")}
    failed_case[4] = path_inventory(failed_case[3], failed_case[0])
    failed_document["path_inventory_sha256"] = sha(failed_case[4])
    failed_case[1] = canonical_json_bytes(failed_document)
    failed = validate(tuple(failed_case))
    auth = SimpleNamespace(result=failed, authentication_sha256="a" * 64)
    with pytest.raises(ResultValidationError, match="complete PASS"):
        e1_seal_payload(auth, sealed_utc=NOW)


def test_bounded_path_failures_are_decided_by_frozen_adjudicator_not_all_pass_rule():
    case = list(result_case())
    paths = case[3]
    paths["N1"]["FULL"] = (
        PathOutcome("UNRESOLVED", None, "synthetic-timeout", ()),
    ) + paths["N1"]["FULL"][1:]
    document = __import__("json").loads(case[1])
    for row in document["stage_results"]:
        row["output_sha256"] = outcome_digest(paths[row["stage"]])
    case[1] = canonical_json_bytes(document)
    case[4] = path_inventory(paths, case[0])
    document["path_inventory_sha256"] = sha(case[4])
    case[1] = canonical_json_bytes(document)
    result = validate(tuple(case))
    assert result.verdict == "PASS"

    paths["N1"]["H1"] = tuple(
        PathOutcome("UNRESOLVED", None, "synthetic-timeout", ())
        for _ in paths["N1"]["H1"])
    document = __import__("json").loads(case[1])
    for row in document["stage_results"]:
        row["output_sha256"] = outcome_digest(paths[row["stage"]])
    case[4] = path_inventory(paths, case[0])
    document["path_inventory_sha256"] = sha(case[4])
    case[1] = canonical_json_bytes(document)
    with pytest.raises(ResultValidationError, match="adjudication"):
        validate(tuple(case))


def test_output_or_runtime_drift_refuses():

    case = list(result_case())
    case[2] = {**case[2], "extra": b"untracked"}
    with pytest.raises(ResultValidationError, match="extras"):
        validate(tuple(case))

    case = list(result_case())
    case[6] = canonical_json_bytes({"runner": "0" * 64})
    with pytest.raises(ResultValidationError, match="identity|differs"):
        validate(tuple(case))


def test_exact_counts_and_typed_outcomes_are_required():
    case = list(result_case())
    case[3]["N1"]["FULL"] = case[3]["N1"]["FULL"][:1]
    with pytest.raises(ResultValidationError, match="count"):
        validate(tuple(case))


def test_path_inventory_binds_stage_population_index_panel_seed_and_outcome():
    case = list(result_case())
    inventory = __import__("json").loads(case[4])
    inventory["records"][0]["seed_input_sha256"] = "f" * 64
    case[4] = canonical_json_bytes(inventory)
    document = __import__("json").loads(case[1])
    document["path_inventory_sha256"] = sha(case[4])
    case[1] = canonical_json_bytes(document)
    with pytest.raises(ResultValidationError, match="binding"):
        validate(tuple(case))

    case = list(result_case())
    inventory = __import__("json").loads(case[4])
    inventory["records"][1]["seed_input_sha256"] = inventory["records"][0]["seed_input_sha256"]
    case[4] = canonical_json_bytes(inventory)
    document = __import__("json").loads(case[1])
    document["path_inventory_sha256"] = sha(case[4])
    case[1] = canonical_json_bytes(document)
    with pytest.raises(ResultValidationError, match="duplicated"):
        validate(tuple(case))

    case = list(result_case())
    case[3]["N1"]["FULL"] = ({"status": "PASS"},) * case[0].stage_specs["N1"].exact_depth
    with pytest.raises(ResultValidationError, match="typed PathOutcome"):
        validate(tuple(case))


def test_producer_cannot_self_issue_seal_and_test_keys_are_explicit():
    result = validate(result_case())
    domain = context(result).domain
    private = context(result).private_keys['test-producer']
    attestation = signed_record(
        result, private, schema='qualification_result_authentication/v1',
        scope='ATTEST_E1_RESULT', subject=result.result_sha256, authority='test-producer')
    producer_key = key(private, 'test-producer', 'TEST_ONLY', 'ATTEST_E1_RESULT')
    keys = {'test-producer': producer_key}
    authenticated = inspect_result_authentication(result, attestation, trusted_keys=keys,
        now=NOW, trust_domain=domain)
    store = AttemptStore(Path(result.attempt_journal_path), result.attempt_id,
        result.contract_sha256, 'boot-1', domain.sha256)
    _historical_commit(store, authenticated, trusted_keys=keys,
        now=NOW, trust_domain=domain)
    payload = e1_seal_payload(authenticated, sealed_utc=NOW)
    forged_scope = signed_record(result, private, schema='e1_qualification_seal/v1',
        scope='SEAL_E1_PASS', subject=sha(payload), authority='test-producer')
    with pytest.raises(ResultValidationError, match='key/scope|authority'):
        _inspect_historical_seal(authenticated, forged_scope, trusted_keys=keys,
                                 trust_domain=domain)
    with pytest.raises(ResultValidationError, match='authority'):
        inspect_result_authentication(result, attestation, trusted_keys={
            'test-producer': replace(producer_key, authority_class='RESULT_PRODUCER')},
            now=NOW, trust_domain=domain)
    assert inspect_result_authentication(result, attestation, trusted_keys=keys,
        now=NOW, trust_domain=domain).key_id == 'test-producer'
