"""Owner boundary regressions; all evidence and keys are synthetic."""
import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from book_settlement import Receipt, Refusal, SettlementError, canonical_bytes, sha256_hex
from test_book_settlement import (
    Operator, boot, seated, seat, b7_seal, package, challenge, submit, utc,
    NOW14, S14, S15, POLICY, CALENDAR,
)


def boundary_seal(captured, sealed, expiry):
    def mutate(doc):
        for row in doc["evidence"].values():
            row["captured_at"] = captured
        doc["seal_timestamp"] = sealed
    return b7_seal(valid_until=expiry, mutate=mutate)


def test_thursday_close_cannot_use_friday_captures(tmp_path):
    store = boot(tmp_path, Operator())
    seal = boundary_seal("2026-09-11T10:00:00-04:00", "2026-09-11T10:05:00-04:00",
                         "2026-09-12T18:00:00-04:00")
    result = seat(store, seal, close=datetime(2026, 9, 10, 21, tzinfo=timezone.utc),
                  session_id="tradeify-account-day:2026-09-10",
                  now=datetime(2026, 9, 11, 14, 6, tzinfo=timezone.utc))
    assert result == Refusal("seal_reopen_mismatch")
    assert store.status()["rows"] == 0


@pytest.mark.parametrize("close,captured,sealed,expiry,received", [
    ("2026-09-10T21:00:00Z", "2026-09-10T17:10:00-04:00", "2026-09-10T17:15:00-04:00",
     "2026-09-10T18:00:00-04:00", "2026-09-10T21:16:00Z"),
    ("2026-10-30T21:00:00Z", "2026-10-30T17:10:00-04:00", "2026-10-30T17:15:00-04:00",
     "2026-11-01T18:00:00-05:00", "2026-10-30T21:16:00Z"),
    ("2026-03-06T22:00:00Z", "2026-03-06T17:10:00-05:00", "2026-03-06T17:15:00-05:00",
     "2026-03-08T18:00:00-04:00", "2026-03-06T22:16:00Z"),
])
def test_b7_boundary_uses_local_reopen_across_dst(tmp_path, close, captured, sealed, expiry, received):
    store = boot(tmp_path, Operator())
    result = seat(store, boundary_seal(captured, sealed, expiry),
                  close=datetime.fromisoformat(close), session_id="tradeify-account-day:" + close[:10],
                  now=datetime.fromisoformat(received))
    assert isinstance(result, Receipt), result


def revised_close(tmp_path):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    assert isinstance(submit(store, operator, challenge(store, pkg, target=S15, now=NOW14),
                             pkg, files, NOW14), Receipt)
    row = next(s for s in pkg["sources"] if s["role"] == "dashboard")
    files[row["file"]] = b"corrected dashboard"
    row["sha256"] = sha256_hex(files[row["file"]])
    return operator, store, pkg, files


def test_revision_retains_all_declared_bytes(tmp_path):
    _, store, pkg, files = revised_close(tmp_path)
    result = store.record_revision(session_id=S14, revised_package=pkg, sources=files, now=NOW14)
    assert result == Refusal("accepted_record_revised", halt_required=True)
    with sqlite3.connect(store.path) as db:
        digest, payload = db.execute("SELECT package_sha256, package_json FROM packages WHERE kind='REVISION'").fetchone()
        assert json.loads(payload)["revised_package"] == pkg
        retained = dict(db.execute("SELECT file, data FROM sources WHERE package_sha256=?", (digest,)))
    assert retained == files


@pytest.mark.parametrize("reader", ["status", "settled_close", "boot"])
@pytest.mark.parametrize("resolved", [False, True])
@pytest.mark.parametrize("mutation", ["edit", "delete"])
def test_revised_source_corruption_blocks_even_after_resolution(tmp_path, reader, resolved, mutation):
    operator, store, pkg, files = revised_close(tmp_path)
    store.record_revision(session_id=S14, revised_package=pkg, sources=files, now=NOW14)
    if resolved:
        store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=NOW14)
        store.reconcile_restore(NOW14)
    with sqlite3.connect(store.path) as db:
        digest = db.execute("SELECT package_sha256 FROM packages WHERE kind='REVISION'").fetchone()[0]
        db.execute("UPDATE sources SET data=x'00' WHERE package_sha256=?" if mutation == "edit"
                   else "DELETE FROM sources WHERE package_sha256=?", (digest,))
    with pytest.raises(SettlementError, match="integrity"):
        boot(tmp_path, operator) if reader == "boot" else getattr(store, reader)()


def test_revision_missing_bytes_refuses_without_advancing_state(tmp_path):
    _, store, pkg, _ = revised_close(tmp_path)
    assert store.record_revision(session_id=S14, revised_package=pkg, sources={}, now=NOW14) == Refusal("revision_source_bytes_mismatch")
    assert store.status()["phase"] == "ACCEPTING"


def test_exact_revised_package_can_be_accepted_after_reconciliation(tmp_path):
    operator, store, pkg, files = revised_close(tmp_path)
    store.record_revision(session_id=S14, revised_package=pkg, sources=files, now=NOW14)
    store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=NOW14)
    store.reconcile_restore(NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    result = submit(store, operator, env, pkg, files, NOW14)
    assert isinstance(result, Receipt), result
    assert store.status()["rows"] == 2


def test_unchanged_superseded_package_can_be_readmitted_with_fresh_signature(tmp_path):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    assert isinstance(submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14), Receipt)
    correction = {**pkg, "observed_problem": "pending report disagreement"}
    store.record_revision(session_id=S14, revised_package=correction, sources=files, now=NOW14)
    store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=NOW14)
    store.reconcile_restore(NOW14)
    result = submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    assert isinstance(result, Receipt), result
    assert store.status()["rows"] == 2


def test_honest_delayed_signing_accepts_without_predicting_timestamp(tmp_path):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    pkg.pop("operator_signed_utc", None)
    issued = NOW14 + timedelta(seconds=10)
    env = challenge(store, pkg, target=S15, now=issued)
    env["operator_signed_utc"] = utc(issued + timedelta(seconds=10))
    signature = operator.sign(env)
    result = store.submit(envelope=env, signature=signature, key_id=operator.key_id,
                          package=pkg, sources=files, halt_generation=1, policy=POLICY,
                          calendar=CALENDAR, now=issued + timedelta(seconds=20))
    assert isinstance(result, Receipt), result


@pytest.mark.parametrize("stamp,reason", [
    ("2026-09-14T21:09:59Z", "chronology:signed_before_challenge"),
    ("2026-09-14T21:10:21Z", "chronology:signed_after_receipt"),
    ("2026-09-14T21:10:10", "chronology:signing_timestamp_shape"),
    (None, "chronology:signing_timestamp_shape"),
])
def test_invalid_signed_timestamp_never_advances_chain(tmp_path, stamp, reason):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    env["operator_signed_utc"] = stamp
    assert submit(store, operator, env, pkg, files, NOW14 + timedelta(seconds=20)) == Refusal(reason)
    assert store.status()["rows"] == 1


def test_signing_time_is_signature_bound(tmp_path):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    signature = operator.sign(env)
    env["operator_signed_utc"] = utc(NOW14 + timedelta(seconds=1))
    assert submit(store, operator, env, pkg, files, NOW14 + timedelta(seconds=2), signature=signature) == Refusal("bad_signature")


@pytest.mark.parametrize("mutation", ["delete", "edit"])
def test_signed_acceptance_evidence_is_integrity_checked_after_restart(tmp_path, mutation):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    signature = operator.sign(env)
    assert isinstance(submit(store, operator, env, pkg, files, NOW14, signature=signature), Receipt)
    with sqlite3.connect(store.path) as db:
        detail = json.loads(db.execute("SELECT detail FROM events WHERE kind='close_accepted'").fetchone()[0])
        assert detail["signed_envelope"] == env and detail["signature"] == signature.hex()
        db.execute("DELETE FROM events WHERE kind='close_accepted'" if mutation == "delete" else
                   "UPDATE events SET detail='{}' WHERE kind='close_accepted'")
    with pytest.raises(SettlementError, match="integrity"):
        boot(tmp_path, operator)


def test_operator_envelope_builder_records_aware_time_without_mutating_challenge(tmp_path):
    from settlement_signing import signing_envelope
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    issued = challenge(store, pkg, target=S15, now=NOW14)
    issued.pop("operator_signed_utc")
    reply = signing_envelope(issued, signed_at=NOW14 + timedelta(seconds=5))
    assert "operator_signed_utc" not in issued
    assert reply["operator_signed_utc"] == "2026-09-14T21:10:05Z"
    assert isinstance(submit(store, operator, reply, pkg, files, NOW14 + timedelta(seconds=6)), Receipt)
    with pytest.raises(ValueError, match="aware"):
        signing_envelope(issued, signed_at=NOW14.replace(tzinfo=None))


@pytest.mark.parametrize("kind", ["trusted_keys_rotated", "digests_rotated", "restore_reconciled"])
@pytest.mark.parametrize("mutation", ["delete", "edit"])
@pytest.mark.parametrize("reader", ["status", "boot"])
def test_authority_audit_corruption_blocks_reads_and_restart(tmp_path, kind, mutation, reader):
    from book_settlement import SettlementStore
    from test_book_settlement import ACCOUNT, POLICY_DIGEST
    operator = Operator()
    store, _ = seated(tmp_path, operator)
    keys = {operator.key_id: ["submit_account_close", "record_only"]}
    if kind == "trusted_keys_rotated":
        keys[operator.key_id] = ["record_only"]
    digest = "a" * 64 if kind == "digests_rotated" else CALENDAR.calendar_digest
    store = SettlementStore.boot(store.path, ACCOUNT, trusted_keys=keys,
                                 calendar_digest=digest, policy_digest=POLICY_DIGEST, now=NOW14)
    store.reconcile_restore(NOW14)
    assert store.status()["rows"] == 1
    with sqlite3.connect(store.path) as db:
        assert db.execute("SELECT count(*) FROM events WHERE kind=?", (kind,)).fetchone()[0] == 1
        db.execute("DELETE FROM events WHERE kind=?" if mutation == "delete" else
                   "UPDATE events SET detail='{}' WHERE kind=?", (kind,))
    with pytest.raises(SettlementError, match="integrity"):
        boot(tmp_path, operator) if reader == "boot" else store.status()


def test_naive_restore_clock_cannot_clear_pending_state(tmp_path):
    operator = Operator()
    seated(tmp_path, operator)
    store = boot(tmp_path, operator)
    before = store.path.read_bytes()
    assert store.reconcile_restore(NOW14.replace(tzinfo=None)) == Refusal("invalid_now")
    assert store.path.read_bytes() == before
    assert store.settled_close() == Refusal("restore_reconciliation_required")
    assert store.reconcile_restore(NOW14) == {"rows": 1, "invalidated": False}


def test_correction_preserves_empty_bytes_accepted_in_original_source(tmp_path):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    row = next(s for s in pkg["sources"] if s["role"] == "positions")
    files[row["file"]] = b""
    row["sha256"] = sha256_hex(b"")
    assert isinstance(submit(store, operator, challenge(store, pkg, target=S15, now=NOW14),
                             pkg, files, NOW14), Receipt)
    pkg["observed_problem"] = "position evidence was empty"
    halts = []
    assert store.record_revision(session_id=S14, revised_package=pkg, sources=files, now=NOW14,
                                 on_halt=lambda reason, _: halts.append(reason)) == Refusal(
                                     "accepted_record_revised", halt_required=True)
    assert halts == ["settlement:revision:" + S14]
    assert store.settled_close() == Refusal("chain_invalidated")
    store = boot(tmp_path, operator)
    store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=NOW14)
    store.reconcile_restore(NOW14)
    with sqlite3.connect(store.path) as db:
        retained = db.execute("SELECT data FROM sources WHERE file=?", (row["file"],)).fetchall()
    assert retained == [(b"",), (b"",)]


@pytest.mark.parametrize("number", ["1e309", "1e999999", "-1"])
def test_b7_unsupported_policy_numbers_refuse_without_seating(tmp_path, number):
    store = boot(tmp_path, Operator())
    seal = b7_seal(balance=number, peak=number if number != "-1" else "100000")
    result = seat(store, seal)
    assert result == Refusal("seal_values")
    assert store.status()["rows"] == 0


@pytest.mark.parametrize("value", [float("nan"), float("inf"), {"not", "json"}])
@pytest.mark.parametrize("target", ["package", "envelope"])
def test_uncanonical_caller_values_are_refusals_not_store_faults(tmp_path, value, target):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    signature = operator.sign(env)
    (pkg if target == "package" else env)["bad_value"] = value
    before = store.path.read_bytes()
    result = submit(store, operator, env, pkg, files, NOW14, signature=signature)
    assert result == Refusal(target + "_serialization")
    assert store.path.read_bytes() == before
    assert store.status()["rows"] == 1


def test_pre_audit_integrity_store_refused_without_rewriting(tmp_path):
    from book_settlement import SettlementStore, _STATE_FIELDS
    operator = Operator()
    store, _ = seated(tmp_path, operator)
    with sqlite3.connect(store.path) as db:
        values = dict(zip(_STATE_FIELDS, db.execute("SELECT " + ",".join(_STATE_FIELDS) + " FROM state").fetchone()))
        values["version"] = "3"
        db.execute("UPDATE state SET version=?, state_hash=?", ("3", SettlementStore._state_hash(values)))
    before = store.path.read_bytes()
    with pytest.raises(SettlementError, match="unsupported settlement store version"):
        boot(tmp_path, operator)
    assert store.path.read_bytes() == before
