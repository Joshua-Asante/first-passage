"""Attended settlement owner: signed one-use challenge -> verified package -> exactly one SettledClose.

All account values are synthetic. The calendar is the ratified September file; the consumer is the
real size_book_request. Signing uses the operator-side library; verification is the rail's own.
"""
import json
import sqlite3
import threading
from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from c1_rail.book_policy import candidate_book_protection_policy
from c1_rail.book_session_calendar import load_ratified_calendar
from c1_rail.book_settlement import (
    CHALLENGE_LIFETIME, CONTRACT, PACKAGE_SCHEMA, Receipt, Refusal, SettlementError, SettlementStore,
    canonical_bytes, load_operator_keys, sha256_hex,
)
from c1_rail.book_sizing_context import SettledClose, size_book_request
from c1_signal_daemon.book_protocol import Mode
from test_tradeify_sizing_integration import inputs
from settlement_signing import signing_envelope
from account_close_test_support import b7_cash_history

cryptography = pytest.importorskip("cryptography")
from cryptography.hazmat.primitives import serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ed25519  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
CAL_DIR = REPO / "ops" / "calendars"
CALENDAR = load_ratified_calendar(CAL_DIR / "book_session_calendar_2026-09.json",
                                  overlay_path=CAL_DIR / "book_closure_overlay.json",
                                  ratified_path=CAL_DIR / "RATIFIED.json", repo_root=REPO)
POLICY = candidate_book_protection_policy()
POLICY_DIGEST = "b" * 64
ACCOUNT = "synthetic-account"
B7_SESSION = "tradeify-account-day:2026-09-11"
B7_CLOSE = datetime(2026, 9, 11, 21, tzinfo=timezone.utc)
S14 = "tradeify-account-day:2026-09-14"
S15 = "tradeify-account-day:2026-09-15"
S16 = "tradeify-account-day:2026-09-16"
NOW14 = datetime(2026, 9, 14, 21, 10, tzinfo=timezone.utc)   # ten minutes after the 09-14 close


def utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Operator:
    def __init__(self):
        self.key = ed25519.Ed25519PrivateKey.generate()
        self.key_id = self.key.public_key().public_bytes(serialization.Encoding.Raw,
                                                          serialization.PublicFormat.Raw).hex()

    def sign(self, envelope: dict) -> bytes:
        return self.key.sign(canonical_bytes(envelope))


TOOL_SHA256 = "7" * 64          # the sealer's digest, supplied out of band by the B7 owner
SEAL_CONTRACT = "docs/spec/2026-09-12-tradeify-account-snapshot-seal-contract.md"


def b7_seal(*, balance="100000", peak="100000", valid_until="2026-09-13T18:00:00-04:00", failing=False,
            mutate=None) -> bytes:
    """A document in the exact shape scripts/seal_account_snapshot.py writes."""
    checks = {f"C{i}": "pass" for i in range(1, 11)}
    if failing:
        checks["C8"] = "fail"
    doc = {
        "values": {"balance": balance, "equity": balance, "trailing_threshold": str(Decimal(peak) - 3000),
                   "prior_trade_days": 3, "prior_max_day_profit": "0", "consistency_display_pct": "0",
                   "profit_target_display": "6000", "cash_adjustments_total": "0", "token_trade_fill_dates": [],
                   "positions_export_shows_flat": True, "working_orders_count": 0},
        "derived": {"original_basis": "100000", "historical_eod_peak": peak, "at_high_water_mark": True,
                    "carried_drawdown": "0", "valid_until": valid_until},
        "evidence": {"E1": {"path": "dash.png", "sha256": "1" * 64, "captured_at": "2026-09-12T09:00:00-04:00"},
                     "E2": {"path": "pos.csv", "sha256": "2" * 64, "captured_at": "2026-09-12T09:01:00-04:00"},
                     "E3": {"path": "cash.csv", "sha256": sha256_hex(b7_cash_history(balance)), "captured_at": "2026-09-12T09:02:00-04:00"}},
        "checks": checks, "seal_timestamp": "2026-09-12T10:00:00-04:00", "tool_sha256": TOOL_SHA256,
        "contract": SEAL_CONTRACT,
    }
    if mutate:
        mutate(doc)
    return json.dumps(doc).encode("utf-8")


def seat(store, seal: bytes, *, now=datetime(2026, 9, 12, 14, tzinfo=timezone.utc), tool=TOOL_SHA256,
         session_id=None, close=None, expected=None, retain_history=True):
    kwargs = {}
    if retain_history and session_id is None and close is None:
        kwargs = {"cash_history_bytes": b7_cash_history(json.loads(seal)["values"]["balance"]),
                  "report_timezone": "America/New_York"}
    return store.bootstrap_b7(seal, expected_seal_sha256=expected or sha256_hex(seal), expected_tool_sha256=tool,
                              session_id=session_id or B7_SESSION, effective_close_utc=close or B7_CLOSE,
                              policy=POLICY, now=now, **kwargs)


def boot(tmp_path, operator, now=NOW14, scopes=("submit_account_close", "record_only")):
    return SettlementStore.boot(tmp_path / "settlement.sqlite", ACCOUNT,
                                trusted_keys={operator.key_id: list(scopes)},
                                calendar_digest=CALENDAR.calendar_digest, policy_digest=POLICY_DIGEST, now=now)


def seated(tmp_path, operator, now=NOW14):
    store = boot(tmp_path, operator, now)
    receipt = seat(store, b7_seal())
    assert isinstance(receipt, Receipt) and receipt.origin == "B7"
    return store, receipt


from account_close_test_support import package


def challenge(store, pkg, *, target, now, scope="submit_account_close", permission="RUNNING", generation=1):
    env = store.issue_challenge(scope=scope, target_session_id=target, proposed_session_id=pkg["session_id"],
                                package_sha256=sha256_hex(canonical_bytes(pkg)), halt_generation=generation,
                                permission=permission, calendar=CALENDAR, now=now)
    assert isinstance(env, dict), env
    return signing_envelope(env, signed_at=now)


def submit(store, operator, env, pkg, files, now, generation=1, on_halt=None, key_id=None, signature=None):
    return store.submit(envelope=env, signature=signature if signature is not None else operator.sign(env),
                        key_id=key_id or operator.key_id, package=pkg, sources=files, halt_generation=generation,
                        policy=POLICY, calendar=CALENDAR, now=now, on_halt=on_halt)


def record_revision(store, *, session_id, revised_package, now, on_halt=None):
    """Provide complete synthetic revision evidence to the actual owner API."""
    with sqlite3.connect(store.path) as db:
        digest = db.execute("SELECT package_sha256 FROM chain WHERE session_id=?", (session_id,)).fetchone()[0]
        original = json.loads(db.execute("SELECT package_json FROM packages WHERE package_sha256=?", (digest,)).fetchone()[0])
        files = dict(db.execute("SELECT file, data FROM sources WHERE package_sha256=?", (digest,)))
    if "sources" not in original:  # B7 correction evidence still requires a new seal to resolve.
        files = {"corrected-b7.txt": b"synthetic corrected B7 observation"}
        original = {"account_id": ACCOUNT, "session_id": session_id, "sources": [
            {"file": "corrected-b7.txt", "sha256": sha256_hex(files["corrected-b7.txt"]), "account_id": ACCOUNT}]}
    revised = {**original, **deepcopy(revised_package)}
    row = revised["sources"][0]
    files[row["file"]] += canonical_bytes(revised_package)
    row["sha256"] = sha256_hex(files[row["file"]])
    return store.record_revision(session_id=session_id, revised_package=revised, sources=files, now=now, on_halt=on_halt)


# ---------------------------------------------------------------- happy path and consumer agreement


def test_signed_close_becomes_exactly_one_settled_close_the_consumer_accepts(tmp_path):
    """Challenge -> signed envelope -> verified package -> durable SettledClose -> size_book_request passes."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    assert env["expires_utc"] == utc(NOW14 + CHALLENGE_LIFETIME)
    receipt = submit(store, operator, env, pkg, files, NOW14)
    assert isinstance(receipt, Receipt), receipt
    assert receipt.session_id == S14 and receipt.equity == "100244.46" and receipt.peak == "100244.46"
    assert receipt.mode_next == Mode.NORMAL.value and receipt.grants_activation is False
    close, mode = store.settled_close()
    assert close == SettledClose(S14, CALENDAR.schedule_for(S14).closes_at, 100244.46, 100244.46, receipt.package_sha256)
    assert mode is Mode.NORMAL
    # Consumer: the 09-15 session names 09-14 as its prior; the store's close satisfies it.
    now = datetime(2026, 9, 15, 13, 30, tzinfo=timezone.utc)
    session = CALENDAR.session_for(now, expected_digest=CALENDAR.calendar_digest).session
    request, context, binding = inputs(protected=False)
    binding = replace(binding, session=session, settlement=close, policy_digest=POLICY_DIGEST)
    context = replace(context, session_id=S15, calendar_digest=CALENDAR.calendar_digest, settled=close,
                      mode=mode, policy_digest=POLICY_DIGEST, as_of=now, valid_until=now + timedelta(seconds=30))
    assert not size_book_request(request, context=context, binding=binding, policy=POLICY, now=now).halt
    # Same challenge again: consumed, no second acceptance, no state advance.
    again = submit(store, operator, env, pkg, files, NOW14 + timedelta(seconds=5))
    assert again == Refusal("challenge_consumed")
    assert store.status()["rows"] == 2


def test_protected_mode_derives_from_the_shared_policy_on_the_ratcheted_peak(tmp_path):
    """A close 1% below the EOD peak yields PROTECTED for the next session; peak never falls."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14, gross="-994.46")      # 100000 - 994.46 - 5.54 = 99000
    env = challenge(store, pkg, target=S15, now=NOW14)
    receipt = submit(store, operator, env, pkg, files, NOW14)
    assert receipt.equity == "99000.00" and receipt.peak == "100000" and receipt.mode_next == Mode.PROTECTED.value


def test_second_close_chains_on_the_first_and_history_must_be_retained(tmp_path):
    """Predecessor digest, prior equity and retained transaction identities all bind the next close."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg1, files1 = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg1, target=S15, now=NOW14), pkg1, files1, NOW14)
    now15 = NOW14 + timedelta(days=1)

    pkg2, files2 = package(r1, S15, now15, prior_tx=pkg1["ledger"]["transactions"])
    r2 = submit(store, operator, challenge(store, pkg2, target=S16, now=now15), pkg2, files2, now15)
    assert isinstance(r2, Receipt) and r2.session_id == S15
    assert store.settled_close()[0].session_id == S15
    # A close that drops or alters an earlier retained transaction is refused.
    pkg3, files3 = package(r2, S16, now15 + timedelta(days=1))          # omits prior ids entirely
    refusal = submit(store, operator, challenge(store, pkg3, target="tradeify-account-day:2026-09-17",
                                                now=now15 + timedelta(days=1)), pkg3, files3, now15 + timedelta(days=1))
    assert refusal == Refusal("history_changed", halt_required=True)


# ---------------------------------------------------------------- authentication and challenge


def test_unknown_key_wrong_scope_and_bad_signature_refuse_without_state_change(tmp_path):
    """Only an enrolled key with the envelope's scope, over exactly these bytes, is accepted."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    stranger = Operator()
    assert submit(store, operator, env, pkg, files, NOW14, key_id=stranger.key_id,
                  signature=stranger.sign(env)) == Refusal("unknown_key_or_scope")
    bad = bytearray(operator.sign(env))
    bad[3] ^= 1
    assert submit(store, operator, env, pkg, files, NOW14, signature=bytes(bad)) == Refusal("bad_signature")
    tampered = dict(env, expires_utc=utc(NOW14 + timedelta(hours=5)))
    assert submit(store, operator, tampered, pkg, files, NOW14, signature=operator.sign(tampered)) == \
        Refusal("challenge_mismatch")
    assert store.status()["rows"] == 1
    # record_only-only key cannot submit a current close.
    limited = Operator()
    (tmp_path / "b").mkdir()
    store2 = boot(tmp_path / "b", limited, scopes=("record_only",))
    seat(store2, b7_seal())
    env2 = challenge(store2, pkg, target=S15, now=NOW14)
    assert submit(store2, limited, env2, pkg, files, NOW14) == Refusal("unknown_key_or_scope")


def test_challenge_expiry_boot_generation_and_evidence_binding(tmp_path):
    """300 s or the target cutoff, whichever is earlier; boot, generation and package bytes are bound."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    assert submit(store, operator, env, pkg, files, NOW14 + timedelta(seconds=300)) == Refusal("challenge_expired")
    env = challenge(store, pkg, target=S15, now=NOW14)
    assert submit(store, operator, env, pkg, files, NOW14, generation=2) == Refusal("stale_boot_generation_or_digest")
    changed = deepcopy(pkg)
    changed["ledger"]["gross_trade_pnl"] = "260.00"
    assert submit(store, operator, env, changed, files, NOW14) == Refusal("evidence_changed")
    # Expiry is capped by the target session's risk-add cutoff.
    late = datetime(2026, 9, 15, 19, 43, tzinfo=timezone.utc)      # two minutes before 15:45 ET cutoff
    env_late = store.issue_challenge(scope="submit_account_close", target_session_id=S15, proposed_session_id=S14,
                                     package_sha256=sha256_hex(canonical_bytes(pkg)), halt_generation=1,
                                     permission="RUNNING", calendar=CALENDAR, now=late)
    assert env_late["expires_utc"] == "2026-09-15T19:45:00Z"
    assert store.issue_challenge(scope="submit_account_close", target_session_id=S15, proposed_session_id=S14,
                                 package_sha256=sha256_hex(canonical_bytes(pkg)), halt_generation=1,
                                 permission="RUNNING", calendar=CALENDAR,
                                 now=datetime(2026, 9, 15, 19, 46, tzinfo=timezone.utc)) == Refusal("target_cutoff_passed")
    assert store.issue_challenge(scope="submit_account_close", target_session_id="tradeify-account-day:2026-09-08",
                                 proposed_session_id="tradeify-account-day:2026-09-07",
                                 package_sha256=sha256_hex(canonical_bytes(pkg)), halt_generation=1,
                                 permission="RUNNING", calendar=CALENDAR, now=NOW14) == Refusal("target_session_unavailable")


def test_concurrent_submissions_accept_exactly_once(tmp_path):
    """Two writers racing on one challenge: one receipt, one refusal, one chain row."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    signature = operator.sign(env)
    results = []

    def worker():
        results.append(submit(store, operator, env, pkg, files, NOW14, signature=signature))

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sum(isinstance(r, Receipt) for r in results) == 1
    assert all(r == Refusal("challenge_consumed") for r in results if not isinstance(r, Receipt))
    assert store.status()["rows"] == 2


# ---------------------------------------------------------------- ordering, duplicates, corrections


def test_duplicate_and_out_of_order_closes_refuse_and_demand_a_halt(tmp_path):
    """TB-S1: a duplicate or out-of-order settlement halts; nothing regresses."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    halts = []
    pkg, files = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    dup, dfiles = package(head, S14, NOW14)                   # same session again, fresh challenge
    dup["predecessor_session_id"], dup["predecessor_package_sha256"] = r1.session_id, r1.package_sha256
    env = challenge(store, dup, target=S15, now=NOW14 + timedelta(minutes=1))
    assert submit(store, operator, env, dup, dfiles, NOW14 + timedelta(minutes=1),
                  on_halt=lambda i, r: halts.append((i, r))) == Refusal("duplicate_settlement", halt_required=True)
    skip, sfiles = package(r1, S16, NOW14 + timedelta(days=2))       # skips 09-15
    env = challenge(store, skip, target="tradeify-account-day:2026-09-17", now=NOW14 + timedelta(days=2))
    assert submit(store, operator, env, skip, sfiles, NOW14 + timedelta(days=2),
                  on_halt=lambda i, r: halts.append((i, r))) == Refusal("out_of_order_settlement", halt_required=True)
    assert [r for _, r in halts] == ["protection", "protection"]
    assert store.settled_close()[0].session_id == S14


def test_revision_of_an_accepted_record_invalidates_dependents_and_halts(tmp_path):
    """Both versions are retained; dependent closes and open challenges are voided; no forward acceptance."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg1, files1 = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg1, target=S15, now=NOW14), pkg1, files1, NOW14)
    now15 = NOW14 + timedelta(days=1)
    pkg2, files2 = package(r1, S15, now15, prior_tx=pkg1["ledger"]["transactions"])
    submit(store, operator, challenge(store, pkg2, target=S16, now=now15), pkg2, files2, now15)
    halts = []
    revised = deepcopy(pkg1)
    revised["ledger"]["transactions"][0]["sha256"] = "f" * 64
    assert record_revision(store, session_id=S14, revised_package=revised, now=now15,
                                 on_halt=lambda i, r: halts.append(i)) == Refusal("accepted_record_revised", halt_required=True)
    assert halts == ["settlement:revision:" + S14]
    assert store.settled_close() == Refusal("chain_invalidated")
    assert store.status()["invalidated"] is True and store.status()["rows"] == 3
    pkg3, files3 = package(r1, S16, now15 + timedelta(days=1))
    assert store.issue_challenge(scope="submit_account_close", target_session_id="tradeify-account-day:2026-09-17",
                                 proposed_session_id=S16, package_sha256=sha256_hex(canonical_bytes(pkg3)),
                                 halt_generation=1, permission="RUNNING", calendar=CALENDAR,
                                 now=now15 + timedelta(days=1)) == Refusal("chain_invalidated")
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        kinds = sorted(k for (k,) in db.execute("SELECT kind FROM packages"))
        assert kinds == ["ACCOUNT_CLOSE", "ACCOUNT_CLOSE", "B7_SEAL", "REVISION"]


# ---------------------------------------------------------------- restart, tamper and restore


def test_restart_begins_restore_pending_voids_open_challenges_and_keeps_the_chain(tmp_path):
    """A restored owner accepts nothing until the durable chain is reconciled; a lost receipt is read-only."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    now15 = NOW14 + timedelta(days=1)
    pkg2, files2 = package(r1, S15, now15, prior_tx=pkg["ledger"]["transactions"])
    env_open = challenge(store, pkg2, target=S16, now=now15)
    restored = boot(tmp_path, operator, now=now15 + timedelta(minutes=1))
    assert restored.status()["restore_pending"] is True and restored.status()["rows"] == 2
    assert restored.settled_close() == Refusal("restore_reconciliation_required")
    assert submit(restored, operator, env_open, pkg2, files2, now15 + timedelta(minutes=2)) == \
        Refusal("restore_reconciliation_required")
    assert restored.reconcile_restore(now15 + timedelta(minutes=3)) == {"rows": 2, "invalidated": False}
    assert restored.settled_close()[0].session_id == S14
    # The pre-restart challenge is void: a new boot is a new owner.
    assert submit(restored, operator, env_open, pkg2, files2, now15 + timedelta(minutes=4)) == \
        Refusal("challenge_consumed")
    # The old handle is fenced.
    with pytest.raises(SettlementError):
        store.status()


def test_tampered_chain_row_is_detected_on_boot(tmp_path):
    """Editing an accepted equity in the database breaks the hash chain; the owner refuses to boot."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        db.execute("UPDATE chain SET equity='999999' WHERE seq=2")
    with pytest.raises(SettlementError, match="integrity"):
        boot(tmp_path, operator, now=NOW14 + timedelta(hours=1))


def test_calendar_rotation_across_restart_is_audited_and_binds_later_challenges(tmp_path):
    """The monthly calendar extension changes the digest; the chain survives and new challenges bind it."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    later = NOW14 + timedelta(days=1)
    rotated = SettlementStore.boot(tmp_path / "settlement.sqlite", ACCOUNT,
                                   trusted_keys={operator.key_id: ["submit_account_close", "record_only"]},
                                   calendar_digest="e" * 64, policy_digest=POLICY_DIGEST, now=later)
    assert rotated.reconcile_restore(later)["rows"] == 2
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        detail = json.loads(db.execute("SELECT detail FROM events WHERE kind='digests_rotated'").fetchone()[0])
    assert detail["calendar"] == [CALENDAR.calendar_digest, "e" * 64]
    pkg2, files2 = package(r1, S15, later, prior_tx=pkg["ledger"]["transactions"])
    # A challenge against the still-loaded September calendar object mismatches the rotated digest.
    assert rotated.issue_challenge(scope="submit_account_close", target_session_id=S16, proposed_session_id=S15,
                                   package_sha256=sha256_hex(canonical_bytes(pkg2)), halt_generation=1,
                                   permission="RUNNING", calendar=CALENDAR, now=later) == Refusal("calendar_digest_mismatch")


def test_key_rotation_across_restart_is_audited_and_the_old_key_is_refused(tmp_path):
    """Revoking or replacing an enrolled key keeps the chain; only current keys can sign afterwards."""
    old_operator, new_operator = Operator(), Operator()
    store, head = seated(tmp_path, old_operator)
    pkg, files = package(head, S14, NOW14)
    r1 = submit(store, old_operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    assert isinstance(r1, Receipt)
    later = NOW14 + timedelta(days=1)
    rotated = SettlementStore.boot(tmp_path / "settlement.sqlite", ACCOUNT,
                                   trusted_keys={new_operator.key_id: ["submit_account_close", "record_only"]},
                                   calendar_digest=CALENDAR.calendar_digest, policy_digest=POLICY_DIGEST, now=later)
    assert rotated.reconcile_restore(later)["rows"] == 2
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        detail = json.loads(db.execute("SELECT detail FROM events WHERE kind='trusted_keys_rotated'").fetchone()[0])
    assert detail["removed"] == [old_operator.key_id] and detail["added"] == [new_operator.key_id]
    pkg2, files2 = package(r1, S15, later, prior_tx=pkg["ledger"]["transactions"])
    env = challenge(rotated, pkg2, target=S16, now=later)
    assert submit(rotated, old_operator, env, pkg2, files2, later) == Refusal("unknown_key_or_scope")
    assert isinstance(submit(rotated, new_operator, env, pkg2, files2, later), Receipt)


# ---------------------------------------------------------------- B7 bootstrap and record-only catch-up


def test_b7_bootstrap_is_initial_only_and_checked(tmp_path):
    """The sealed snapshot seats the head once; failed checks, expiry or a seated chain refuse."""
    operator = Operator()
    store = boot(tmp_path, operator)
    at = datetime(2026, 9, 12, 14, tzinfo=timezone.utc)
    assert store.settled_close() == Refusal("chain_not_seated")
    assert seat(store, b7_seal(failing=True), now=at) == Refusal("seal_checks")
    assert seat(store, b7_seal(), now=datetime(2026, 9, 13, 22, 1, tzinfo=timezone.utc)) == Refusal("seal_expired")
    assert seat(store, b7_seal(), close=B7_CLOSE - timedelta(days=3), now=at) == Refusal("effective_close_not_session_close")
    receipt = seat(store, b7_seal(balance="98500", peak="100000"), now=at)
    assert receipt.origin == "B7" and receipt.mode_next == Mode.PROTECTED.value
    close, mode = store.settled_close()
    assert close.session_id == B7_SESSION and close.equity == 98500.0 and mode is Mode.PROTECTED
    assert seat(store, b7_seal(), now=at) == Refusal("chain_already_seated")


def test_b7_session_metadata_must_match_a_weekday_close(tmp_path):
    """The seal seats only with the session id whose 17:00 ET close is the given effective close."""
    operator = Operator()
    store = boot(tmp_path, operator)
    at = datetime(2026, 9, 12, 14, tzinfo=timezone.utc)
    assert seat(store, b7_seal(), now=at, close=B7_CLOSE + timedelta(hours=1)) == Refusal("effective_close_not_session_close")
    assert seat(store, b7_seal(), now=at, session_id="tradeify-account-day:2026-09-10") == Refusal("effective_close_not_session_close")
    assert isinstance(seat(store, b7_seal(), now=at), Receipt)


def _seal_mutation(name):
    def m(doc):
        if name == "wrong_contract":
            doc["contract"] = "docs/spec/other.md"
        elif name == "c3_not_flat":
            doc["values"]["positions_export_shows_flat"] = False
        elif name == "c4_peak_not_threshold_plus_width":
            doc["derived"]["historical_eod_peak"] = "100500"
        elif name == "c8_adjustments":
            doc["values"]["cash_adjustments_total"] = "25"
        elif name == "evidence_not_distinct":
            doc["evidence"]["E2"]["sha256"] = doc["evidence"]["E1"]["sha256"]
        elif name == "checks_reordered":
            doc["checks"] = {k: "pass" for k in ["C2", "C1"] + [f"C{i}" for i in range(3, 11)]}
        elif name == "extra_value":
            doc["values"]["operator_override"] = True
    return m


@pytest.mark.parametrize("mutation,refusal", [
    ("wrong_contract", "seal_contract_or_tool"), ("c3_not_flat", "seal_c3"),
    ("c4_peak_not_threshold_plus_width", "seal_c4"), ("c8_adjustments", "seal_c8"),
    ("evidence_not_distinct", "seal_evidence"), ("checks_reordered", "seal_checks"), ("extra_value", "seal_values"),
])
def test_b7_seal_is_authenticated_and_rederived_before_seating(tmp_path, mutation, refusal):
    """The seal must match its out-of-band digest, the seal contract, the sealer, and re-check C3/C4/C8."""
    operator = Operator()
    store = boot(tmp_path, operator)
    at = datetime(2026, 9, 12, 14, tzinfo=timezone.utc)
    assert seat(store, b7_seal(mutate=_seal_mutation(mutation)), now=at) == Refusal(refusal)
    assert seat(store, b7_seal(), now=at, expected="e" * 64) == Refusal("seal_identity")
    assert seat(store, b7_seal(), now=at, tool="9" * 64) == Refusal("seal_contract_or_tool")
    assert store.status()["rows"] == 0


def test_record_only_catch_up_accepts_missed_sessions_in_order_while_halted(tmp_path):
    """Historical closes use fresh record_only challenges, no target, predecessor order, and grant nothing."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    late = datetime(2026, 9, 16, 12, tzinfo=timezone.utc)
    pkg14, f14 = package(head, S14, late, scope="record_only")
    # Both fresh queries contain the same complete inventory, including trades
    # from the later missed session. Each close uses its own venue equity view.
    preview = replace(head, session_id=S14, equity=pkg14["equity"]["net_equity"],
                      peak=pkg14["equity"]["net_equity"])
    pkg15, f15 = package(preview, S15, late, prior_tx=pkg14["ledger"]["transactions"], scope="record_only")
    close_source = next(src for src in pkg14["sources"] if src["role"] == "close_equity")
    close_bytes = f14[close_source["file"]]
    pkg14["ledger"]["transactions"] = deepcopy(pkg15["ledger"]["transactions"])
    pkg14["ledger"]["coverage"] = deepcopy(pkg15["ledger"]["coverage"])
    pkg14["sources"] = deepcopy(pkg15["sources"])
    pkg14["sources"] = [close_source if src["role"] == "close_equity" else src for src in pkg14["sources"]]
    pkg14["dashboard"] = deepcopy(pkg15["dashboard"])
    f14 = dict(f15)
    f14[close_source["file"]] = close_bytes
    assert store.issue_challenge(scope="record_only", target_session_id=None, proposed_session_id=S14,
                                 package_sha256=sha256_hex(canonical_bytes(pkg14)), halt_generation=3,
                                 permission="RUNNING", calendar=CALENDAR, now=late) == Refusal("record_only_requires_halted")
    env = challenge(store, pkg14, target=None, now=late, scope="record_only", permission="HALTED", generation=3)
    assert env["expires_utc"] == utc(late + CHALLENGE_LIFETIME) and env["target_session_id"] is None
    r14 = submit(store, operator, env, pkg14, f14, late, generation=3)
    assert isinstance(r14, Receipt) and r14.grants_activation is False
    pkg15["predecessor_package_sha256"] = r14.package_sha256
    env = challenge(store, pkg15, target=None, now=late, scope="record_only", permission="HALTED", generation=3)
    r15 = submit(store, operator, env, pkg15, f15, late, generation=3)
    assert isinstance(r15, Receipt)
    status = store.status()
    assert status["head"]["session_id"] == S15 and status["grants_activation"] is False and status["grants_resume"] is False


# ---------------------------------------------------------------- package refusals


def _mutate(pkg, files, mutation, now):
    if mutation == "stale_evidence":
        for src in pkg["sources"]:
            if src["role"] == "dashboard":
                src["captured_utc"] = utc(now - timedelta(minutes=31))
    elif mutation == "future_capture":
        pkg["positions"]["captured_utc"] = utc(now + timedelta(minutes=1))
        for src in pkg["sources"]:
            if src["role"] == "positions":
                src["captured_utc"] = utc(now + timedelta(minutes=1))
    elif mutation == "cash_adjustments_present":
        pkg["ledger"]["adjustments_abs_total"] = "200.00"          # +100 deposit, -100 withdrawal
    elif mutation == "unclassified_ledger_rows":
        pkg["ledger"]["unlinked_fee_rows"] = 1
    elif mutation == "ledger_arithmetic":
        pkg["ledger"]["trading_costs"]["commission"] = "8.00"      # double-counted commission
    elif mutation == "dashboard_disagreement":
        pkg["dashboard"]["trailing_threshold"] = str(Decimal(pkg["dashboard"]["trailing_threshold"]) - 50)
    elif mutation == "source_bytes_mismatch":
        files["cash_history.csv"] = b"different bytes"
    elif mutation == "source_role_missing":
        pkg["sources"] = [s for s in pkg["sources"] if s["role"] != "balance_history"]
    elif mutation == "coverage_gap":
        pkg["ledger"]["coverage"]["windows"][1]["from_utc"] = "2026-09-04T00:00:00Z"
    elif mutation == "coverage_gap_at_inception":
        pkg["ledger"]["coverage"]["windows"][0]["from_utc"] = "2026-08-21T00:00:00Z"
    elif mutation == "coverage_window_span":
        pkg["ledger"]["coverage"]["windows"][0]["to_utc"] = "2026-09-05T13:00:00Z"
    elif mutation == "coverage_window_limit":
        pkg["ledger"]["coverage"]["window_limit_days"] = 365
    elif mutation == "coverage_window_incomplete":
        pkg["ledger"]["coverage"]["windows"][1]["complete"] = False
    elif mutation == "coverage_ends_before_capture":
        pkg["ledger"]["coverage"]["windows"][1]["to_utc"] = utc(now - timedelta(minutes=20))
    elif mutation == "transaction_revision_detected":
        pkg["ledger"]["revisions"] = [{"id": "tx-09-14-0"}]
    elif mutation == "duplicate_transaction_id":
        pkg["ledger"]["transactions"].append(dict(pkg["ledger"]["transactions"][0]))
    elif mutation == "effective_close_not_session_close":
        pkg["effective_close_utc"] = "2026-09-14T20:30:00Z"
    elif mutation == "flatness_uncertain":
        pkg["unresolved_runtime_requests"] = ["op-77"]
    elif mutation == "flatness_uncertain_open_position":
        pkg["positions"]["open_positions"] = 1
    elif mutation == "capture_time_unbound":
        pkg["dashboard"]["captured_utc"] = utc(now - timedelta(minutes=9))
    elif mutation == "capture_time_unbound_positions":
        pkg["positions"]["captured_utc"] = utc(now - timedelta(minutes=9))
    elif mutation == "capture_before_effective_close":
        early = utc(now - timedelta(minutes=20))          # 20:50Z, before the 21:00Z close
        for src in pkg["sources"]:
            if src["role"] == "cash_history":
                src["captured_utc"] = early
    elif mutation == "source_role_missing_orders":
        pkg["sources"] = [s for s in pkg["sources"] if s["role"] != "orders"]
    elif mutation == "transactions_bad_digest":
        pkg["ledger"]["transactions"][0]["sha256"] = "not-hex"
    elif mutation == "transactions_int_id":
        pkg["ledger"]["transactions"][0]["id"] = 12345
    elif mutation == "source_not_distinct":
        for src in pkg["sources"]:
            if src["role"] == "orders":
                src["file"], src["sha256"] = "positions.csv", sha256_hex(files["positions.csv"])
    elif mutation == "source_publication_utc":
        pkg["source_publication_utc"] = utc(now + timedelta(days=400))
    elif mutation == "scope_mismatch":
        pkg["scope"] = "record_only"
    elif mutation == "venue_equity_at_close":
        pkg["equity"]["flatness_basis"] = "VENUE_EQUITY_AT_CLOSE"    # without venue equity/valuation basis
    elif mutation == "attestation_incomplete":
        pkg["attestations"]["no_known_pending_correction"] = False
    elif mutation == "wrong_account":
        pkg["account_id"] = "someone-else"
    elif mutation == "digest_mismatch":
        pkg["policy_digest"] = "c" * 64
    elif mutation == "predecessor_mismatch":
        pkg["predecessor_package_sha256"] = "9" * 64
    elif mutation == "package_keys":
        pkg["note"] = "extra"
    elif mutation == "report_timezone":
        pkg["report_timezone"] = "UTC-4"
    else:
        raise AssertionError(mutation)


@pytest.mark.parametrize("mutation", [
    "stale_evidence", "future_capture", "cash_adjustments_present", "unclassified_ledger_rows",
    "ledger_arithmetic", "dashboard_disagreement", "source_bytes_mismatch", "source_role_missing",
    "coverage_gap", "coverage_gap_at_inception", "coverage_window_span", "coverage_window_limit",
    "coverage_window_incomplete", "coverage_ends_before_capture", "transaction_revision_detected",
    "duplicate_transaction_id", "effective_close_not_session_close", "flatness_uncertain",
    "venue_equity_at_close", "attestation_incomplete", "wrong_account", "digest_mismatch",
    "predecessor_mismatch", "package_keys", "report_timezone", "operator_signed_in_future",
    "flatness_uncertain_open_position", "capture_time_unbound", "capture_time_unbound_positions",
    "capture_before_effective_close", "source_role_missing_orders", "transactions_bad_digest", "transactions_int_id",
    "source_not_distinct", "source_publication_utc", "scope_mismatch",
])
def test_defective_packages_are_refused_by_name_without_state_advance(tmp_path, mutation):
    """Every contract refusal is a named value; the challenge stays issued and the chain unchanged."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    if mutation != "operator_signed_in_future":
        _mutate(pkg, files, mutation, NOW14)
    env = challenge(store, pkg, target=S15, now=NOW14)
    if mutation == "operator_signed_in_future":
        env["operator_signed_utc"] = utc(NOW14 + timedelta(seconds=30))
    result = submit(store, operator, env, pkg, files, NOW14)
    expected = {"flatness_uncertain_open_position": "flatness_uncertain",
                "venue_equity_at_close": "source_role_missing",
                "capture_time_unbound": "chronology:capture_time_unbound",
                "capture_time_unbound_positions": "chronology:capture_time_unbound",
                "source_role_missing_orders": "source_role_missing", "transactions_bad_digest": "transactions",
                "transactions_int_id": "transactions", "stale_evidence": "chronology:stale_evidence",
                "future_capture": "chronology:capture_in_future", "coverage_gap": "chronology:coverage_gap",
                "coverage_gap_at_inception": "chronology:coverage_gap_at_inception",
                "coverage_window_span": "chronology:coverage_window_span",
                "coverage_window_limit": "chronology:coverage_window_limit",
                "coverage_window_incomplete": "chronology:coverage_window_incomplete",
                "coverage_ends_before_capture": "chronology:coverage_end_not_capture",
                "operator_signed_in_future": "chronology:signed_after_receipt",
                "capture_before_effective_close": "chronology:capture_before_effective_close",
                "source_publication_utc": "chronology:publication_after_receipt"}
    assert result == Refusal(expected.get(mutation, mutation), halt_required=mutation == "transaction_revision_detected"), result
    assert store.status()["rows"] == 1
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        assert db.execute("SELECT status FROM challenges WHERE challenge_id=?", (env["challenge_id"],)).fetchone()[0] == ("VOIDED_REVISION" if mutation == "transaction_revision_detected" else "ISSUED")


def test_venue_equity_basis_accepts_carried_boundary_with_valuation(tmp_path):
    """When flatness at the close is not established, venue-backed equity with its basis is required."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14, flatness="VENUE_EQUITY_AT_CLOSE")
    files["close_equity.png"] = b"venue equity view at the 09-14 close"
    pkg["sources"].append({"role": "close_equity", "file": "close_equity.png", "sha256": sha256_hex(files["close_equity.png"]),
                           "captured_utc": utc(NOW14 - timedelta(minutes=5)), "account_id": ACCOUNT})
    pkg["equity"]["at_effective_close"] = "VENUE_EQUITY"
    pkg["equity"]["equity_at_effective_close"] = pkg["equity"]["net_equity"]
    pkg["equity"]["valuation_basis"] = "venue close-equity capture close_equity.png at the 17:00 ET close"
    pkg["unresolved_runtime_requests"] = ["op-late-close"]
    env = challenge(store, pkg, target=S15, now=NOW14)
    assert isinstance(submit(store, operator, env, pkg, files, NOW14), Receipt)


def test_offsetting_adjustments_refuse_despite_zero_net(tmp_path):
    """Sum of absolute adjustments, never the signed net, decides refusal."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    pkg["ledger"]["adjustments_abs_total"] = "2.00"
    env = challenge(store, pkg, target=S15, now=NOW14)
    assert submit(store, operator, env, pkg, files, NOW14) == Refusal("cash_adjustments_present")


# ---------------------------------------------------------------- enrolled operator keys


ENROLLED = "1f75cea0c36941f8964d393490b6886bcbcdb010b4bc67dd45e925d1a04604aa"


def test_tracked_enrollment_record_loads_the_confirmed_operator_key():
    """The operator-confirmed public key is the only active key, scoped to both contract scopes."""
    keys = load_operator_keys(REPO / "ops" / "c1_rail" / "operator_keys.json")
    assert keys == {ENROLLED: ["submit_account_close", "record_only"]}


@pytest.mark.parametrize("mutation", [
    "not_operator", "bad_point", "extra_scope", "revoked_only", "duplicate", "extra_key", "wrong_schema",
])
def test_defective_enrollment_records_are_refused(tmp_path, mutation):
    """A key record that is malformed, non-operator, revoked or not a curve point enrols nothing."""
    raw = json.loads((REPO / "ops" / "c1_rail" / "operator_keys.json").read_bytes())
    row = raw["keys"][0]
    if mutation == "not_operator":
        row["enrolled_by"] = "agent"
    elif mutation == "bad_point":
        row["key_id"] = "f" * 64          # y >= p: undecodable
    elif mutation == "extra_scope":
        row["scopes"].append("resume")
    elif mutation == "revoked_only":
        row["revoked_utc"] = "2026-09-16T00:00:00Z"
    elif mutation == "duplicate":
        raw["keys"].append(dict(row))
    elif mutation == "extra_key":
        row["private_key"] = "never"
    elif mutation == "wrong_schema":
        raw["schema"] = "operator_signing_keys/v0"
    path = tmp_path / "keys.json"
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    with pytest.raises(SettlementError):
        load_operator_keys(path)


def test_late_added_historical_transaction_is_refused(tmp_path):
    """A transaction not retained from the predecessor must belong to the proposed session."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg1, files1 = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg1, target=S15, now=NOW14), pkg1, files1, NOW14)
    now15 = NOW14 + timedelta(days=1)
    pkg2, files2 = package(r1, S15, now15, prior_tx=pkg1["ledger"]["transactions"])
    pkg2["ledger"]["transactions"].append({"id": "tx-late-history", "sha256": "a" * 64, "session_id": S14})
    env = challenge(store, pkg2, target=S16, now=now15)
    assert submit(store, operator, env, pkg2, files2, now15) == Refusal("history_changed", halt_required=True)


def test_modified_or_missing_package_bytes_break_the_chain(tmp_path):
    """The chain binds the retained package bytes; editing or deleting them refuses every read."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        db.execute("UPDATE packages SET package_json=replace(package_json, '250.00', '260.00') WHERE package_sha256=?",
                   (r1.package_sha256,))
    with pytest.raises(SettlementError, match="package integrity"):
        store.status()
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        db.execute("DELETE FROM packages WHERE package_sha256=?", (r1.package_sha256,))
    with pytest.raises(SettlementError, match="package integrity"):
        store.settled_close()


def test_accepted_source_bytes_are_retained_and_integrity_checked(tmp_path):
    """Every accepted package keeps its evidence bytes; altering them refuses reads after restart."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg, target=S15, now=NOW14), pkg, files, NOW14)
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        retained = {f: bytes(d) for f, d in db.execute("SELECT file, data FROM sources WHERE package_sha256=?",
                                                       (r1.package_sha256,))}
    assert retained == files
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        db.execute("UPDATE sources SET data=? WHERE package_sha256=? AND file='cash_history.csv'", (b"tampered", r1.package_sha256))
    with pytest.raises(SettlementError, match="source-bytes integrity"):
        store.status()


def test_record_only_catch_up_tolerates_a_later_current_peak(tmp_path):
    """Historical catch-up: the current dashboard may show a higher peak than the historical close."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    late = datetime(2026, 9, 16, 12, tzinfo=timezone.utc)
    pkg14, f14 = package(head, S14, late, scope="record_only")
    pkg14["dashboard"]["trailing_threshold"] = str(Decimal(pkg14["dashboard"]["trailing_threshold"]) + 500)   # later peak
    env = challenge(store, pkg14, target=None, now=late, scope="record_only", permission="HALTED", generation=3)
    assert isinstance(submit(store, operator, env, pkg14, f14, late, generation=3), Receipt)
    lower = pkg14.copy(); lower["dashboard"] = dict(pkg14["dashboard"], trailing_threshold=str(Decimal(head.peak) - 3000 - 1))
    env = challenge(store, lower, target=None, now=late, scope="record_only", permission="HALTED", generation=3)
    assert submit(store, operator, env, lower, f14, late, generation=3) == Refusal("duplicate_settlement", halt_required=True)


def test_append_only_revocation_removes_a_key_and_a_full_revocation_leaves_none(tmp_path):
    """A later row with revoked_utc removes the key without editing enrolment history."""
    raw = json.loads((REPO / "ops" / "c1_rail" / "operator_keys.json").read_bytes())
    row = raw["keys"][0]
    raw["keys"].append(dict(row, revoked_utc="2026-09-16T00:00:00Z", instruction="revoke"))
    path = tmp_path / "keys.json"
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    with pytest.raises(SettlementError, match="no active operator key"):
        load_operator_keys(path)
    other = Operator()
    raw["keys"].append(dict(row, key_id=other.key_id, revoked_utc=None, instruction="enrol replacement"))
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    assert load_operator_keys(path) == {other.key_id: ["submit_account_close", "record_only"]}


def test_historical_close_needs_the_venue_balance_row_basis(tmp_path):
    """record_only binds the historical requirement to the signed scope, not a caller flag."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    late = datetime(2026, 9, 16, 12, tzinfo=timezone.utc)
    pkg14, f14 = package(head, S14, late, scope="record_only", basis="NO_ACTIVITY_DASHBOARD_CORROBORATED")
    env = challenge(store, pkg14, target=None, now=late, scope="record_only", permission="HALTED", generation=3)
    assert submit(store, operator, env, pkg14, f14, late, generation=3) == Refusal("historical_close_needs_venue_row")


def test_revoked_key_can_never_be_re_enrolled(tmp_path):
    """An enrolment row appended after a revocation of the same key id refuses the whole record."""
    raw = json.loads((REPO / "ops" / "c1_rail" / "operator_keys.json").read_bytes())
    row = raw["keys"][0]
    raw["keys"].append(dict(row, revoked_utc="2026-09-16T00:00:00Z", instruction="revoke"))
    raw["keys"].append(dict(row, revoked_utc=None, instruction="stale re-enrol"))
    path = tmp_path / "keys.json"
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    with pytest.raises(SettlementError, match="re-enrolment of a revoked key"):
        load_operator_keys(path)


def test_key_bound_to_another_account_is_refused(tmp_path):
    """A literal account binding must equal the booting account; BOUND_AT_RUNTIME is portable."""
    raw = json.loads((REPO / "ops" / "c1_rail" / "operator_keys.json").read_bytes())
    raw["keys"][0]["account_binding"] = "TDFYSL999999999999"
    path = tmp_path / "keys.json"
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    with pytest.raises(SettlementError, match="different account"):
        load_operator_keys(path, account_id="synthetic-account")
    assert set(load_operator_keys(path, account_id="TDFYSL999999999999")) == {ENROLLED}
    raw["keys"][0]["account_binding"] = ""
    path.write_bytes(json.dumps(raw).encode("utf-8"))
    with pytest.raises(SettlementError, match="account_binding"):
        load_operator_keys(path)


def test_state_row_tamper_is_detected(tmp_path):
    """The state row carries authority and safety flags; an edit refuses every read (O1)."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        db.execute("UPDATE state SET invalidated='0', restore_pending='0', trusted_keys=?",
                   (json.dumps({Operator().key_id: ["submit_account_close"]}),))
    with pytest.raises(SettlementError, match="state integrity"):
        store.status()


def test_resolve_invalidation_reseats_the_chain_under_a_reviewed_reconciliation(tmp_path):
    """Revision -> INVALIDATED -> reviewed resolution supersedes the revised rows and re-seats the head (O3)."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg1, files1 = package(head, S14, NOW14)
    r1 = submit(store, operator, challenge(store, pkg1, target=S15, now=NOW14), pkg1, files1, NOW14)
    now15 = NOW14 + timedelta(days=1)
    pkg2, files2 = package(r1, S15, now15, prior_tx=pkg1["ledger"]["transactions"])
    submit(store, operator, challenge(store, pkg2, target=S16, now=now15), pkg2, files2, now15)
    revised = deepcopy(pkg2)
    revised["ledger"]["transactions"][-1]["sha256"] = "f" * 64
    record_revision(store, session_id=S15, revised_package=revised, now=now15)
    assert store.status()["phase"] == "INVALIDATED"
    assert store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="", now=now15) == Refusal("review_record_required")
    result = store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="packet0_review", now=now15)
    assert result == {"head": S14, "superseded_from_seq": 3, "restore_pending": True}
    assert store.settled_close() == Refusal("restore_reconciliation_required")
    store.reconcile_restore(now15)
    close, _ = store.settled_close()
    assert close.session_id == S14 and store.status()["phase"] == "ACCEPTING"
    with sqlite3.connect(tmp_path / "settlement.sqlite") as db:
        assert db.execute("SELECT COUNT(*) FROM superseded_chain").fetchone()[0] == 1
        assert db.execute("SELECT COUNT(*) FROM packages WHERE kind='REVISION'").fetchone()[0] == 1
    pkg2b, files2b = package(r1, S15, now15, prior_tx=pkg1["ledger"]["transactions"], scope="record_only")
    env = challenge(store, pkg2b, target=None, now=now15, scope="record_only", permission="HALTED")
    assert isinstance(submit(store, operator, env, pkg2b, files2b, now15), Receipt)
    assert store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="packet0_review", now=now15) == Refusal("chain_not_invalidated")


def test_revising_the_b7_head_needs_a_new_seal(tmp_path):
    """A revision at the seated head cannot be reconciled in place; only a fresh B7 seal re-seats it."""
    operator = Operator()
    store, head = seated(tmp_path, operator)
    record_revision(store, session_id=B7_SESSION, revised_package={"changed": True}, now=NOW14)
    result = store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="packet0_review", now=NOW14)
    assert result == Refusal("b7_head_revised_reseal_required")


def two_closes(tmp_path):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    p14, f14 = package(head, S14, NOW14)
    r14 = submit(store, operator, challenge(store, p14, target=S15, now=NOW14), p14, f14, NOW14)
    now15 = NOW14 + timedelta(days=1)
    p15, f15 = package(r14, S15, now15, prior_tx=p14["ledger"]["transactions"])
    r15 = submit(store, operator, challenge(store, p15, target=S16, now=now15), p15, f15, now15)
    assert isinstance(r15, Receipt)
    return operator, store, head, p14, p15, r14, r15, now15


@pytest.mark.parametrize("sessions", [(S14, S15), (S15, S14), (S14, S14)])
def test_resolution_removes_every_outstanding_revision(tmp_path, sessions):
    operator, store, head, p14, p15, r14, r15, now = two_closes(tmp_path)
    for i, sid in enumerate(sessions):
        record_revision(store, session_id=sid, revised_package={"correction": i}, now=now)
    # A restart must retain the earliest invalidation, independent of event order.
    store = boot(tmp_path, operator, now)
    result = store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=now)
    assert result == {"head": B7_SESSION, "superseded_from_seq": 2, "restore_pending": True}
    assert store.settled_close() == Refusal("restore_reconciliation_required")
    store.reconcile_restore(now)
    assert store.settled_close()[0].session_id == B7_SESSION
    with sqlite3.connect(store.path) as db:
        assert db.execute("SELECT session_id FROM superseded_chain ORDER BY seq").fetchall() == [(S14,), (S15,)]


def test_second_resolution_does_not_reuse_a_resolved_revision(tmp_path):
    operator, store, head, p14, p15, r14, r15, now = two_closes(tmp_path)
    record_revision(store, session_id=S14, revised_package={"correction": 1}, now=now)
    store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=now)
    store.reconcile_restore(now)
    # Re-submit distinct corrected evidence, then revise only the later session.
    p14b, f14b = package(head, S14, now, gross="200", scope="record_only")
    env = challenge(store, p14b, target=None, now=now, scope="record_only", permission="HALTED")
    r14b = submit(store, operator, env, p14b, f14b, now)
    p15b, f15b = package(r14b, S15, now, prior_tx=p14b["ledger"]["transactions"], scope="record_only")
    env = challenge(store, p15b, target=None, now=now, scope="record_only", permission="HALTED")
    assert isinstance(submit(store, operator, env, p15b, f15b, now), Receipt)
    record_revision(store, session_id=S15, revised_package={"correction": 2}, now=now)
    result = store.resolve_invalidation(review_sha256="2" * 64, reviewed_by="reviewer", now=now)
    assert result["head"] == S14 and result["superseded_from_seq"] == 3
    store = boot(tmp_path, operator, now)
    store.reconcile_restore(now)
    assert store.settled_close()[0].equity == 100194.46


@pytest.mark.parametrize("reader", ["status", "settled_close", "boot"])
@pytest.mark.parametrize("mutation", ["row_edit", "row_delete", "all_rows_delete", "package_edit", "package_delete", "source_edit", "source_delete"])
def test_superseded_history_corruption_blocks_consumers(tmp_path, reader, mutation):
    operator, store, head, p14, p15, r14, r15, now = two_closes(tmp_path)
    record_revision(store, session_id=S14, revised_package={"correction": 1}, now=now)
    store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=now)
    store.reconcile_restore(now)
    with sqlite3.connect(store.path) as db:
        if mutation == "row_edit":
            db.execute("UPDATE superseded_chain SET equity='1' WHERE seq=2")
        elif mutation == "row_delete":
            db.execute("DELETE FROM superseded_chain WHERE seq=3")
        elif mutation == "all_rows_delete":
            db.execute("DELETE FROM superseded_chain")
        elif mutation == "package_edit":
            db.execute("UPDATE packages SET package_json='{}' WHERE package_sha256=?", (r14.package_sha256,))
        elif mutation == "package_delete":
            db.execute("DELETE FROM packages WHERE package_sha256=?", (r14.package_sha256,))
        elif mutation == "source_edit":
            db.execute("UPDATE sources SET data=? WHERE package_sha256=?", (b"changed", r14.package_sha256))
        else:
            db.execute("DELETE FROM sources WHERE package_sha256=?", (r14.package_sha256,))
    with pytest.raises(SettlementError, match="integrity"):
        if reader == "boot":
            boot(tmp_path, operator, now)
        else:
            getattr(store, reader)()


@pytest.mark.parametrize("tx_session", [B7_SESSION, S14, S15])
def test_first_current_close_refuses_relabelled_b7_inventory(tmp_path, tx_session):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    pkg["ledger"]["transactions"][0]["session_id"] = tx_session
    env = challenge(store, pkg, target=S15, now=NOW14)
    result = submit(store, operator, env, pkg, files, NOW14)
    assert result == Refusal("history_changed", halt_required=True)
    assert store.status()["rows"] == 1


@pytest.mark.parametrize("role", ["dashboard", "positions", "orders", "balance_history", "cash_history"])
def test_capture_after_challenge_is_refused_even_before_signing(tmp_path, role):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    capture = utc(NOW14 + timedelta(seconds=1))
    next(s for s in pkg["sources"] if s["role"] == role)["captured_utc"] = capture
    if role in ("dashboard", "positions"):
        pkg[role]["captured_utc"] = capture
    if role == "cash_history":
        pkg["ledger"]["coverage"]["windows"][-1]["to_utc"] = capture
    env = challenge(store, pkg, target=S15, now=NOW14)
    assert submit(store, operator, env, pkg, files, NOW14 + timedelta(seconds=3)) == Refusal("chronology:capture_after_challenge")
    assert store.status()["rows"] == 1


@pytest.mark.parametrize("mutation", ["future_close", "future_seal", "future_capture", "capture_after_seal", "seal_before_close", "naive_seal", "malformed_capture"])
def test_b7_chronology_must_end_before_receipt(tmp_path, mutation):
    operator = Operator()
    store = boot(tmp_path, operator)
    now = datetime(2026, 9, 12, 14, tzinfo=timezone.utc)
    def mutate(doc):
        if mutation == "future_seal":
            doc["seal_timestamp"] = "2026-09-12T10:00:01-04:00"
        elif mutation == "future_capture":
            doc["evidence"]["E2"]["captured_at"] = "2026-09-12T10:00:01-04:00"
        elif mutation == "capture_after_seal":
            doc["seal_timestamp"] = "2026-09-12T09:00:00-04:00"
        elif mutation == "seal_before_close":
            doc["seal_timestamp"] = "2026-09-11T16:59:00-04:00"
        elif mutation == "naive_seal":
            doc["seal_timestamp"] = "2026-09-12T10:00:00"
        elif mutation == "malformed_capture":
            doc["evidence"]["E2"]["captured_at"] = "not a time"
    if mutation == "future_close":
        now = B7_CLOSE - timedelta(seconds=1)
    result = seat(store, b7_seal(mutate=mutate), now=now)
    assert isinstance(result, Refusal)
    assert store.status()["rows"] == 0


@pytest.mark.parametrize("reader", ["status", "settled_close", "boot"])
@pytest.mark.parametrize("suffix_only", [True, False])
def test_active_history_deletion_cannot_roll_back_the_consumed_close(tmp_path, reader, suffix_only):
    operator, store, head, p14, p15, r14, r15, now = two_closes(tmp_path)
    with sqlite3.connect(store.path) as db:
        db.execute("DELETE FROM chain WHERE seq=3" if suffix_only else "DELETE FROM chain")
    with pytest.raises(SettlementError, match="integrity"):
        if reader == "boot":
            boot(tmp_path, operator, now)
        else:
            getattr(store, reader)()


def test_record_only_requires_close_equity_even_with_a_current_flat_snapshot(tmp_path):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    now = NOW14 + timedelta(days=2)
    pkg, files = package(head, S14, now, scope="record_only")
    pkg["equity"].update(flatness_basis="DAILY_FLATTEN_CONFIRMED_NO_LATER_FILLS",
                         at_effective_close="FLAT", equity_at_effective_close=None, valuation_basis=None)
    pkg["sources"] = [s for s in pkg["sources"] if s["role"] != "close_equity"]
    pkg["ledger"]["transactions"][0]["session_id"] = S15
    env = challenge(store, pkg, target=None, now=now, scope="record_only", permission="HALTED")
    assert submit(store, operator, env, pkg, files, now) == Refusal("source_role_missing")
    assert store.status()["rows"] == 1


@pytest.mark.parametrize("mutation", ["revision_delete", "revision_edit", "event_delete", "event_edit"])
def test_revision_evidence_and_linkage_remain_verified_after_resolution(tmp_path, mutation):
    operator, store, head, p14, p15, r14, r15, now = two_closes(tmp_path)
    record_revision(store, session_id=S14, revised_package={"correction": 1}, now=now)
    store.resolve_invalidation(review_sha256="1" * 64, reviewed_by="reviewer", now=now)
    store.reconcile_restore(now)
    with sqlite3.connect(store.path) as db:
        if mutation == "revision_delete":
            db.execute("DELETE FROM packages WHERE kind='REVISION'")
        elif mutation == "revision_edit":
            db.execute("UPDATE packages SET package_json='{}' WHERE kind='REVISION'")
        elif mutation == "event_delete":
            db.execute("DELETE FROM events WHERE kind='revision_recorded'")
        else:
            db.execute("UPDATE events SET detail='{}' WHERE kind='invalidation_resolved'")
    with pytest.raises(SettlementError, match="integrity"):
        store.settled_close()
    with pytest.raises(SettlementError, match="integrity"):
        boot(tmp_path, operator, now)


@pytest.mark.parametrize("column", ["issued_utc", "expires_utc"])
def test_challenge_chronology_uses_the_signed_envelope(tmp_path, column):
    operator = Operator()
    store, head = seated(tmp_path, operator)
    pkg, files = package(head, S14, NOW14)
    now = NOW14 + timedelta(seconds=3)
    if column == "issued_utc":
        next(s for s in pkg["sources"] if s["role"] == "orders")["captured_utc"] = utc(NOW14 + timedelta(seconds=1))
    else:
        now = NOW14 + timedelta(minutes=6)
    env = challenge(store, pkg, target=S15, now=NOW14)
    with sqlite3.connect(store.path) as db:
        if column == "issued_utc":
            db.execute("UPDATE challenges SET issued_utc=?", (utc(NOW14 + timedelta(seconds=1)),))
        else:
            db.execute("UPDATE challenges SET expires_utc=?", (utc(NOW14 + timedelta(hours=1)),))
    result = submit(store, operator, env, pkg, files, now)
    assert result == Refusal("chronology:capture_after_challenge" if column == "issued_utc" else "challenge_expired")
    assert store.status()["rows"] == 1


def test_older_store_is_refused_without_rewriting_its_evidence(tmp_path):
    """Unanchored v1 history needs reviewed migration; boot must not silently bless it."""
    path = tmp_path / "settlement.sqlite"
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE state (version TEXT, account TEXT, boot_id TEXT, calendar_digest TEXT, "
                   "policy_digest TEXT, trusted_keys TEXT, restore_pending TEXT, invalidated TEXT, "
                   "phase TEXT, state_hash TEXT)")
        db.execute("INSERT INTO state VALUES ('1', 'synthetic-account', 'old-boot', '', '', '{}', '0', '0', 'SEATED', '')")
        db.execute("CREATE TABLE retained_evidence (data BLOB)")
        db.execute("INSERT INTO retained_evidence VALUES (?)", (b"preserve this older store for review",))
    before = path.read_bytes()
    with pytest.raises(SettlementError, match="reviewed migration required"):
        boot(tmp_path, Operator())
    assert path.read_bytes() == before
