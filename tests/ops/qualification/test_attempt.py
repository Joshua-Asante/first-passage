from __future__ import annotations

import json
import sqlite3
import hashlib
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from c1_rail.qualification.attempt import (
    AttemptConflict,
    AttemptCorrupt,
    AttemptStore,
    BootFenceError,
    StageClaim,
    TransitionError,
    ValidatedResultClaim,
    _issue_validated_result_claim,
)


NOW = datetime(2026, 9, 15, 14, 0, tzinfo=timezone.utc)
CONTRACT = "a" * 64


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def open_store(tmp_path, *, boot_id="boot-A", campaign="campaign-001", contract=CONTRACT):
    return AttemptStore.open(
        tmp_path / "attempt.sqlite3",
        campaign_id=campaign,
        contract_digest=contract,
        trust_domain_sha256="d" * 64,
        boot_id=boot_id,
        now=NOW,
    )


def reserve_and_start(store, stage="TB_E1", *, binding=None):
    binding = binding or canonical({"contract_digest": CONTRACT, "stage": stage})
    store.reserve(stage, binding, now=NOW)
    claim = store.claimed_reservation(stage)
    dispatch = store.start_once(stage, claim, now=NOW + timedelta(seconds=1))
    return claim, dispatch


def finish_checkpoints(store):
    parent = store.claimed_reservation("TB_E1")
    for index, checkpoint in enumerate(("N1", "CUTOFF", "N2", "PART_A"), 1):
        dispatch = store.start_checkpoint_once(
            checkpoint, parent, canonical({"checkpoint": checkpoint}),
            now=NOW + timedelta(seconds=index * 2),
        )
        store.consume_checkpoint_dispatch(dispatch)
        store.complete_checkpoint(
            checkpoint, dispatch, canonical({"checkpoint": checkpoint, "status": "PASS"}),
            now=NOW + timedelta(seconds=index * 2 + 1),
        )


def validated_commit(store, stage, manifest, *, outcome, now):
    if stage == "TB_E1" and any(
            row["state"] != "COMPLETED" for row in store.checkpoints()):
        finish_checkpoints(store)
    claim = _issue_validated_result_claim(
        campaign_id=store.campaign_id, contract_digest=store.contract_digest,
        stage=stage, manifest_sha256=hashlib.sha256(manifest).hexdigest(),
        outcome=outcome, producer_scope="TEST_ONLY_RESULT_VALIDATOR",
        attestation_digest="c" * 64,
        result_stages=(("LEGALITY", "N1", "N2", "PART_B", "PART_A")
                       if stage == "TB_E1" else ("N3",)),
    )
    return store._commit_validated_result(
        stage, manifest, outcome=outcome, validation_claim=claim,
        now=now,
    )


def test_reserve_start_and_exact_repeats_are_idempotent(tmp_path):
    store = open_store(tmp_path)
    binding = canonical({"contract_digest": CONTRACT, "inputs": ["panel", "clock"]})

    first = store.reserve("TB_E1", binding, now=NOW)
    repeated = store.reserve("TB_E1", binding, now=NOW + timedelta(seconds=5))
    assert first == repeated
    assert first["state"] == "RESERVED"

    claim = store.claimed_reservation("TB_E1")
    started = store.start_once("TB_E1", claim, now=NOW + timedelta(seconds=6))
    with pytest.raises(TransitionError, match="already dispatched"):
        store.start_once("TB_E1", claim, now=NOW + timedelta(seconds=9))
    assert started.stage == "TB_E1"
    assert store.stage("TB_E1")["state"] == "STARTED_IN_DOUBT"
    assert [event["kind"] for event in store.events()] == [
        "CAMPAIGN_CREATED", "BOOT_CLAIMED", "STAGE_RESERVED", "STAGE_DISPATCHED"
    ]


def test_changed_reservation_conflicts_and_completed_stage_cannot_reopen(tmp_path):
    store = open_store(tmp_path)
    reserve_and_start(store)
    with pytest.raises(AttemptConflict, match="binding"):
        store.reserve("TB_E1", canonical({"different": True}), now=NOW)

    manifest = canonical({"outputs": {"paths": "1"}, "status": "PASS"})
    validated_commit(store, "TB_E1", manifest, outcome="PASS", now=NOW + timedelta(minutes=1))
    with pytest.raises(TransitionError, match="already dispatched"):
        store.start_once("TB_E1", store.claimed_reservation("TB_E1"), now=NOW + timedelta(minutes=2))
    assert not hasattr(store, "retry")
    assert not hasattr(store, "reset")
    assert not hasattr(store, "reopen")


def test_e1_must_complete_successfully_before_n3_can_be_reserved(tmp_path):
    store = open_store(tmp_path)
    with pytest.raises(TransitionError, match="TB_E1"):
        store.reserve("TB_E2_N3", canonical({"stage": "TB_E2_N3"}), now=NOW)

    reserve_and_start(store)
    validated_commit(store,
        "TB_E1", canonical({"status": "PASS"}), outcome="PASS",
        now=NOW + timedelta(minutes=1),
    )
    assert store.reserve(
        "TB_E2_N3", canonical({"stage": "TB_E2_N3"}), now=NOW + timedelta(minutes=2)
    )["state"] == "RESERVED"


@pytest.mark.parametrize(
    ("stage", "outcome", "expected"),
    [
        ("TB_E1", "FAILURE", "FALSIFIED"),
        ("TB_E1", "UNRESOLVED", "AMBIGUOUS"),
    ],
)
def test_failure_and_ambiguity_are_terminal(tmp_path, stage, outcome, expected):
    store = open_store(tmp_path)
    reserve_and_start(store, stage)
    validated_commit(store,
        stage, canonical({"status": outcome}), outcome=outcome,
        now=NOW + timedelta(minutes=1),
    )
    assert store.status()["verdict"] == expected
    with pytest.raises(TransitionError, match="terminal"):
        store.reserve("TB_E2_N3", canonical({"stage": "TB_E2_N3"}), now=NOW)


def test_two_successful_stages_resolve_attempt(tmp_path):
    store = open_store(tmp_path)
    reserve_and_start(store)
    validated_commit(store, "TB_E1", canonical({"status": "PASS"}), outcome="PASS", now=NOW)
    reserve_and_start(store, "TB_E2_N3")
    validated_commit(store,
        "TB_E2_N3", canonical({"status": "PASS"}), outcome="PASS", now=NOW
    )
    assert store.status()["verdict"] == "RESOLVED"


def test_void_is_independent_of_failure_verdict_and_is_idempotent(tmp_path):
    store = open_store(tmp_path)
    reserve_and_start(store)
    validated_commit(store,
        "TB_E1", canonical({"status": "FAILURE"}), outcome="FAILURE", now=NOW
    )
    first = store.void("source evidence invalidated", now=NOW + timedelta(minutes=1))
    assert first["verdict"] == "FALSIFIED"
    assert first["validity"] == "VOID"
    assert store.void("source evidence invalidated", now=NOW + timedelta(minutes=2)) == first
    with pytest.raises(AttemptConflict, match="void reason"):
        store.void("a different reason", now=NOW)


def test_restart_rotates_boot_fence_without_redrawing_started_stage(tmp_path):
    old = open_store(tmp_path)
    reserve_and_start(old)
    restored = open_store(tmp_path, boot_id="boot-B")

    assert restored.stage("TB_E1")["state"] == "STARTED_IN_DOUBT"
    assert restored.status()["boot_id"] == "boot-B"
    with pytest.raises(BootFenceError, match="boot"):
        validated_commit(old, "TB_E1", canonical({"status": "PASS"}), outcome="PASS", now=NOW)


def test_campaign_is_singleton_and_identity_is_immutable(tmp_path):
    open_store(tmp_path)
    with pytest.raises(AttemptConflict, match="campaign identity"):
        open_store(tmp_path, campaign="campaign-002")
    with pytest.raises(AttemptConflict, match="campaign identity"):
        open_store(tmp_path, contract="b" * 64)


def test_result_manifest_and_receipt_commit_atomically_and_lost_receipt_recovers(tmp_path):
    store = open_store(tmp_path)
    reserve_and_start(store)
    manifest = canonical({"outputs": {"journal": "f" * 64}, "status": "PASS"})

    receipt = validated_commit(store, "TB_E1", manifest, outcome="PASS", now=NOW)
    recovered = store.result("TB_E1")
    assert recovered["manifest_bytes"] == manifest
    assert recovered["receipt_bytes"] == receipt
    assert validated_commit(store,
        "TB_E1", manifest, outcome="PASS", now=NOW + timedelta(hours=1)
    ) == receipt
    with pytest.raises(AttemptConflict, match="result"):
        validated_commit(store,
            "TB_E1", canonical({"status": "PASS", "drift": True}),
            outcome="PASS", now=NOW,
        )


def test_failed_receipt_insert_rolls_back_manifest_and_stage_transition(tmp_path):
    store = open_store(tmp_path)
    reserve_and_start(store)
    with sqlite3.connect(store.path) as db:
        db.execute(
            "CREATE TRIGGER refuse_receipt BEFORE INSERT ON receipts "
            "BEGIN SELECT RAISE(ABORT, 'simulated receipt loss'); END"
        )

    with pytest.raises(sqlite3.IntegrityError, match="simulated receipt loss"):
        validated_commit(store,
            "TB_E1", canonical({"status": "PASS"}), outcome="PASS", now=NOW
        )
    assert store.stage("TB_E1")["state"] == "STARTED_IN_DOUBT"
    assert store.result("TB_E1") is None


def test_concurrent_reservation_has_one_exact_winner(tmp_path):
    first = open_store(tmp_path, boot_id="shared-boot")
    second = open_store(tmp_path, boot_id="shared-boot")
    binding = canonical({"worker": 1})
    assert first.reserve("TB_E1", binding, now=NOW)["binding_bytes"] == binding
    assert second.reserve("TB_E1", binding, now=NOW) == first.stage("TB_E1")
    with pytest.raises(AttemptConflict, match="binding"):
        second.reserve("TB_E1", canonical({"worker": 2}), now=NOW)


def test_rejects_noncanonical_bytes_unknown_values_and_naive_time(tmp_path):
    store = open_store(tmp_path)
    with pytest.raises(ValueError, match="canonical JSON"):
        store.reserve("TB_E1", b'{"z": 1}', now=NOW)
    with pytest.raises(ValueError, match="stage"):
        store.reserve("E1", canonical({"x": 1}), now=NOW)
    with pytest.raises(ValueError, match="aware"):
        store.reserve("TB_E1", canonical({"x": 1}), now=NOW.replace(tzinfo=None))
    reserve_and_start(store)
    with pytest.raises(ValueError, match="outcome"):
        validated_commit(store, "TB_E1", canonical({"status": "PASS"}), outcome="MAYBE", now=NOW)


def test_strict_schema_and_event_chain_tampering_refuse_reopen(tmp_path):
    store = open_store(tmp_path)
    store.reserve("TB_E1", canonical({"x": 1}), now=NOW)
    with sqlite3.connect(store.path) as db:
        db.execute("UPDATE events SET body=? WHERE seq=3", (canonical({"x": 2}),))
    with pytest.raises(AttemptCorrupt, match="event chain"):
        open_store(tmp_path, boot_id="boot-B")


def test_store_issued_stage_claim_is_required_and_stale_claim_is_refused(tmp_path):
    store = open_store(tmp_path)
    binding = canonical({"contract_digest": CONTRACT, "stage": "TB_E1"})
    store.reserve("TB_E1", binding, now=NOW)
    claim = store.claimed_reservation("TB_E1")

    assert isinstance(claim, StageClaim)
    assert store.verify_claim(claim, require_state="RESERVED") == claim
    assert claim.binding_sha256 == __import__("hashlib").sha256(binding).hexdigest()
    assert claim.reservation_sequence == 3

    forged = replace(claim, reservation_event_digest="f" * 64)
    with pytest.raises(AttemptConflict, match="claim"):
        store.verify_claim(forged, require_state="RESERVED")
    different_binding = replace(claim, binding_sha256="e" * 64)
    with pytest.raises(AttemptConflict, match="claim"):
        store.verify_claim(different_binding, require_state="RESERVED")

    store.start_once("TB_E1", claim, now=NOW + timedelta(seconds=1))
    with pytest.raises(TransitionError, match="state"):
        store.verify_claim(claim, require_state="RESERVED")


def test_pre_stage_ambiguity_is_terminal_and_exactly_idempotent(tmp_path):
    store = open_store(tmp_path)
    evidence = "d" * 64
    first = store.mark_ambiguous(
        "flatten price provenance is absent", evidence, now=NOW
    )
    assert first["verdict"] == "AMBIGUOUS"
    assert first["validity"] == "VALID"
    assert first["ambiguity_evidence_digest"] == evidence
    assert store.mark_ambiguous(
        "flatten price provenance is absent", evidence, now=NOW + timedelta(hours=1)
    ) == first
    with pytest.raises(AttemptConflict, match="ambiguity"):
        store.mark_ambiguous("different", evidence, now=NOW)
    with pytest.raises(TransitionError, match="terminal"):
        store.reserve("TB_E1", canonical({"x": 1}), now=NOW)


def test_pre_stage_ambiguity_refuses_after_stage_reservation(tmp_path):
    store = open_store(tmp_path)
    store.reserve("TB_E1", canonical({"x": 1}), now=NOW)
    with pytest.raises(TransitionError, match="before any stage"):
        store.mark_ambiguous("late ambiguity", "d" * 64, now=NOW)


def test_duplicate_json_keys_are_explicitly_rejected(tmp_path):
    store = open_store(tmp_path)
    with pytest.raises(ValueError, match="duplicate JSON key"):
        store.reserve("TB_E1", b'{"x":1,"x":1}', now=NOW)


def test_e1_checkpoints_are_ordered_once_only_and_bound_to_parent(tmp_path):
    store = open_store(tmp_path)
    parent, _ = reserve_and_start(store)
    with pytest.raises(TransitionError, match="order"):
        store.start_checkpoint_once(
            "N2", parent, canonical({"checkpoint": "N2"}), now=NOW
        )
    dispatch = store.start_checkpoint_once(
        "N1", parent, canonical({"checkpoint": "N1"}), now=NOW
    )
    with pytest.raises(TransitionError, match="cannot rerun"):
        store.start_checkpoint_once(
            "N1", parent, canonical({"checkpoint": "N1"}), now=NOW
        )
    receipt = canonical({"checkpoint": "N1", "status": "PASS"})
    store.consume_checkpoint_dispatch(dispatch)
    assert store.complete_checkpoint("N1", dispatch, receipt, now=NOW) == receipt
    assert store.complete_checkpoint("N1", dispatch, receipt, now=NOW) == receipt
    with pytest.raises(AttemptConflict, match="completion"):
        store.complete_checkpoint(
            "N1", dispatch, canonical({"different": True}), now=NOW
        )


def test_checkpoint_dispatch_capability_is_exact_once_and_not_recreated_on_restart(tmp_path):
    store = open_store(tmp_path)
    parent, _ = reserve_and_start(store)
    dispatch = store.start_checkpoint_once(
        "N1", parent, canonical({"checkpoint": "N1"}), now=NOW)
    forged = replace(dispatch)
    with pytest.raises(AttemptConflict, match="freshly issued"):
        store.consume_checkpoint_dispatch(forged)
    assert store.consume_checkpoint_dispatch(dispatch) is dispatch
    with pytest.raises(AttemptConflict, match="freshly issued"):
        store.consume_checkpoint_dispatch(dispatch)

    restarted = open_store(tmp_path, boot_id="boot-B")
    with pytest.raises(AttemptConflict, match="freshly issued"):
        restarted.consume_checkpoint_dispatch(dispatch)


def test_checkpoint_cannot_complete_without_durable_consumption(tmp_path):
    store = open_store(tmp_path)
    parent, _ = reserve_and_start(store)
    dispatch = store.start_checkpoint_once('N1', parent, canonical({'checkpoint':'N1'}), now=NOW)
    receipt = canonical({'checkpoint':'N1', 'status':'PASS'})
    with pytest.raises(TransitionError, match='consum'):
        store.complete_checkpoint('N1', dispatch, receipt, now=NOW)
    assert store.checkpoints()[0]['state'] == 'STARTED_IN_DOUBT'
    store.consume_checkpoint_dispatch(dispatch)
    assert store.complete_checkpoint('N1', dispatch, receipt, now=NOW) == receipt
    reopened = open_store(tmp_path, boot_id='boot-B')
    assert reopened.complete_checkpoint('N1', dispatch, receipt, now=NOW) == receipt


def test_result_commit_requires_completed_checkpoints_and_authenticated_claim(tmp_path):
    store = open_store(tmp_path)
    reserve_and_start(store)
    manifest = canonical({"status": "PASS"})
    claim = ValidatedResultClaim(
        campaign_id=store.campaign_id, contract_digest=store.contract_digest,
        stage="TB_E1", manifest_sha256=hashlib.sha256(manifest).hexdigest(),
        outcome="PASS", producer_scope="RESULT_AUTHORITY",
        attestation_digest="c" * 64,
        result_stages=("LEGALITY", "N1", "N2", "PART_B", "PART_A"),
    )
    with pytest.raises(AttemptConflict, match="validated result claim"):
        store._commit_validated_result(
            "TB_E1", manifest, outcome="PASS", validation_claim=claim,
            now=NOW,
        )
    finish_checkpoints(store)
    with pytest.raises(AttemptConflict, match="validated result claim"):
        store._commit_validated_result(
            "TB_E1", manifest, outcome="PASS", validation_claim=claim,
            now=NOW,
        )
    valid_claim = _issue_validated_result_claim(
        campaign_id=store.campaign_id, contract_digest=store.contract_digest,
        stage="TB_E1", manifest_sha256=hashlib.sha256(manifest).hexdigest(),
        outcome="PASS", producer_scope="TEST_ONLY_RESULT_VALIDATOR",
        attestation_digest="c" * 64,
        result_stages=("LEGALITY", "N1", "N2", "PART_B", "PART_A"),
    )
    forged = replace(valid_claim, manifest_sha256="f" * 64)
    with pytest.raises(AttemptConflict, match="binding"):
        store._commit_validated_result(
            "TB_E1", manifest, outcome="PASS", validation_claim=forged,
            now=NOW,
        )
    with pytest.raises(TransitionError, match="direct result commit"):
        store.commit_result("TB_E1", manifest, outcome="PASS", now=NOW)
    with pytest.raises(TransitionError, match="controller-private"):
        store.commit_validated_result(
            "TB_E1", manifest, outcome="PASS", validation_claim=valid_claim, now=NOW)


def test_authenticated_terminal_n1_prefix_commits_without_fake_later_checkpoints(tmp_path):
    store = open_store(tmp_path)
    parent, _ = reserve_and_start(store)
    for index, checkpoint in enumerate(("N1", "CUTOFF"), 1):
        dispatch = store.start_checkpoint_once(
            checkpoint, parent, canonical({"checkpoint": checkpoint}),
            now=NOW + timedelta(seconds=index * 2),
        )
        store.consume_checkpoint_dispatch(dispatch)
        store.complete_checkpoint(
            checkpoint, dispatch, canonical({"checkpoint": checkpoint, "status": "FAIL"}),
            now=NOW + timedelta(seconds=index * 2 + 1),
        )
    manifest = canonical({"status": "FAIL", "terminal_stage": "N1"})
    claim = _issue_validated_result_claim(
        campaign_id=store.campaign_id, contract_digest=store.contract_digest,
        stage="TB_E1", manifest_sha256=hashlib.sha256(manifest).hexdigest(),
        outcome="FAILURE", producer_scope="TEST_ONLY_RESULT_VALIDATOR",
        attestation_digest="c" * 64, result_stages=("LEGALITY", "N1"),
    )
    store._commit_validated_result(
        "TB_E1", manifest, outcome="FAILURE", validation_claim=claim,
        now=NOW + timedelta(minutes=1),
    )
    states = {row["checkpoint"]: row["state"] for row in store.checkpoints()}
    assert states == {
        "N1": "COMPLETED", "CUTOFF": "COMPLETED",
        "N2": "PENDING", "PART_A": "PENDING",
    }


def test_read_only_inspect_does_not_rotate_boot_or_append_event(tmp_path):
    store = open_store(tmp_path)
    before = store.status()
    view = AttemptStore.inspect(store.path)
    after = store.status()
    assert view["status"] == before == after
    assert view["stages"][0]["state"] == "UNRESERVED"
    assert before["event_count"] == 2


@pytest.mark.parametrize('tamper', ['erase_consumption', 'old_schema'])
def test_reopen_rejects_missing_consumption_proof(tmp_path, tamper):
    store = open_store(tmp_path)
    reserve_and_start(store)
    finish_checkpoints(store)
    with sqlite3.connect(store.path) as db:
        if tamper == 'erase_consumption':
            db.execute("UPDATE checkpoints SET consumed=0 WHERE checkpoint='N1'")
        else:
            db.execute('ALTER TABLE checkpoints DROP COLUMN consumed')
            db.execute('UPDATE campaign SET schema_version=2')
    with pytest.raises(AttemptCorrupt, match='consumption|schema'):
        open_store(tmp_path, boot_id='boot-B')
