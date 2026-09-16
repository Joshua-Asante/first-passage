"""Second-review regressions across owner ingress and durable feedback."""
from dataclasses import replace
import sqlite3
from datetime import datetime, timedelta, timezone
from fractions import Fraction

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact, BrokerResult, SyntheticBroker
from c1_signal_daemon.book_protocol import Bracket, BracketAmend, Cancel, Side
from c1_signal_daemon.book_runtime import FourLegRuntime
from test_book_account_owner import NOW, SESSION, binding, intent, owner
from test_four_leg_runtime import LEGS, bars, inert_adapters, binding as runtime_binding, owner as runtime_owner
from test_pr409_owner_lifecycle import filled_owner
from test_book_settlement import (
    CALENDAR, NOW14, Operator, S14, B7_SESSION, B7_CLOSE, b7_seal, package, seat,
    boot as settlement_boot,
)
from c1_rail.book_settlement import Receipt, Refusal, canonical_bytes, sha256_hex
from settlement_signing import signing_envelope
from test_pr395_owner_repairs import boundary_seal
from c1_rail.book_settlement import SettlementStore


@pytest.mark.parametrize("price", [None, "100", -1, 0, True, float("nan"), float("inf"), -float("inf")])
@pytest.mark.parametrize("kind", ["entry", "flat"])
def test_invalid_price_is_fenced_before_capacity_and_feedback(tmp_path, price, kind):
    account, route = filled_owner(tmp_path)
    account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_pr409_review2:29"), now=NOW)
    if kind == "entry":
        account.dispatch(replace(intent("orb"), leg_id="orb_mnq_v7", qty=1), occurrence=account.make_occurrence("direct", "test_pr409_review2:31"), now=NOW)
        fact = BrokerFact.fill("bad", "orb", "orb_mnq_v7", "entry", 1, price, NOW)
    else:
        account.dispatch(replace(intent("flat", kind="flat", qty=1), side=Side.SELL), occurrence=account.make_occurrence("direct", "test_pr409_review2:34"), now=NOW)
        fact = BrokerFact.fill("bad", "flat", "dj30_mym_p250", "flat", 1, price, NOW,
                               entry_execution_id="base-fill")
    before = account.observable_accounting()["exposures"]
    feedback = account.all_feedback
    assert account.observe(fact, now=NOW) == ()
    assert account.authority == "INTERVENTION"
    assert account.observable_accounting()["exposures"] == before
    assert account.all_feedback == feedback
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(),
                                     synthetic_broker=route)
    assert restarted.all_feedback == feedback
    assert restarted.observable_accounting()["exposures"] == before


def test_bracket_refusal_is_durable_and_replays(tmp_path):
    amend = BracketAmend("orb_mnq_v7", Bracket(stop=100))
    def registry():
        values = inert_adapters()
        values["orb_mnq_v7"].actions = [amend]
        return values
    account = runtime_owner(tmp_path, [])
    account.halt("operator", "operator", now=NOW)
    runtime = FourLegRuntime(account, registry())
    for leg_id in LEGS:
        result = runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    assert result[0].refusal_reason == "intervention_fence"
    event = runtime.adapters["orb_mnq_v7"].events[0]
    assert event == ("reject", result[0].operation_id, None)
    later = NOW + timedelta(minutes=15)
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, replace(bars()[leg_id], ts=later), now=later)
    assert account.pending_feedback == ()
    expected_events = list(runtime.adapters["orb_mnq_v7"].events)
    assert len(expected_events) == 2
    assert expected_events[0][1] != expected_events[1][1]
    restarted = BookAccountOwner.boot(account.path, account.account, binding=runtime_binding(),
                                     synthetic_broker=SyntheticBroker([]))
    recovered = FourLegRuntime.recover(restarted, registry())
    assert recovered.adapters["orb_mnq_v7"].events == expected_events


@pytest.mark.parametrize("kind", ["entry", "flat", "cancel", "bracket"])
def test_definitive_rejection_releases_only_its_own_reservation(tmp_path, kind):
    account, route = owner(tmp_path, [])
    if kind == "entry":
        action = intent()
    elif kind == "cancel":
        account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_pr409_review2:79"), now=NOW)
        action = Cancel("dj30_mym_p250", "base")
    elif kind == "bracket":
        from book_occurrence_fixtures import bare_protection_owner, prepare_protection
        # A real first attachment is rejected; entry exposure must stay owned.
        account, route = bare_protection_owner(tmp_path / "protected")
        route.queue(BrokerResult("rejected"))
        action = BracketAmend("dj30_mym_p250", Bracket(stop=99), ("base-fill",))
        result = prepare_protection(account, route, action, "rejected-first-attachment")
        assert result.transport_state == "rejected"
        assert account.exposure("dj30_mym_p250") == (3, 0)
        assert account.authority == "INTERVENTION"
        assert account.protection_owners[0].pending_operation is not None
        restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(), synthetic_broker=route)
        assert restarted.exposure("dj30_mym_p250") == (3, 0)
        assert restarted.protection_owners[0].pending_operation is not None
        return
    else:
        route.queue(BrokerResult("accepted", (
            BrokerFact.fill("base-fill", "base", "dj30_mym_p250", "entry", 3, 100, NOW),
            BrokerFact.terminal("base", "filled", 3, NOW),
        )))
        account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_pr409_review2:88"), now=NOW)
        action = replace(intent("flat", kind="flat", qty=3), side=Side.SELL)
    route.queue(BrokerResult("rejected"))
    result = account.dispatch(action, occurrence=account.make_occurrence("direct", "test_pr409_review2:91"), now=NOW)
    assert len(result.confirmed_events) == 1
    event = result.confirmed_events[0]
    assert event.event == "reject"
    assert result.attempt_id not in account.unresolved_attempts
    expected = {"entry": (0, 0), "flat": (3, 0), "cancel": (0, 3), "bracket": (0, 0)}[kind]
    assert account.exposure("dj30_mym_p250") == expected
    if kind == "flat":
        retry = account.dispatch(replace(action, order_id="retry"), occurrence=account.make_occurrence("direct", "test_pr409_review2:99"), now=NOW)
        assert retry.refusal_reason is None and retry.quantity == 3
    elif kind in ("entry", "bracket"):
        account.advance_schedule(now=SESSION.own_flat_deadline)
        assert account.authority == "SCHEDULED_EXIT"
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(),
                                     synthetic_broker=SyntheticBroker([]))
    assert any(row["body"]["event"] == "reject" for row in restarted.all_feedback)


@pytest.mark.parametrize("activate", [False, True])
def test_record_only_requires_halted_at_submission(tmp_path, activate):
    from c1_rail.book_synthetic_protection import SyntheticProtectionBroker
    operator = Operator()
    bound = binding()
    # An offline owner window containing the submission instant lets this test
    # isolate the permission race through real activation, without state edits.
    bound["session"] = replace(bound["session"], session_id=S14, prior_session_id=B7_SESSION,
        opens_at=NOW14 - timedelta(hours=1), risk_add_cutoff=NOW14 + timedelta(hours=1),
        flatten_start=NOW14 + timedelta(hours=1, minutes=10),
        own_flat_deadline=NOW14 + timedelta(hours=1, minutes=15),
        closes_at=NOW14 + timedelta(hours=2), calendar_digest=CALENDAR.calendar_digest)
    bound["settlement"] = replace(bound["settlement"], session_id=B7_SESSION, as_of=B7_CLOSE,
        equity=100000, peak=100000, seal_digest=sha256_hex(b7_seal()))
    bound["policy_digest"] = "b" * 64
    bound["as_of"], bound["valid_until"] = NOW14 - timedelta(seconds=1), NOW14 + timedelta(minutes=5)
    route = SyntheticProtectionBroker(account='synthetic-account', account_epoch='unbound', at=NOW14)
    account = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account", binding=bound,
                                    synthetic_broker=route)
    route.account_epoch = account.make_occurrence('direct', 'fixture-bind').account_epoch
    store = account.open_settlement(trusted_keys={operator.key_id: ["record_only"]}, now=NOW14)
    head = seat(store, b7_seal())
    proposed, sources = package(head, S14, NOW14, scope="record_only")
    challenge = account.issue_settlement_challenge(scope="record_only", target_session_id=None,
        proposed_session_id=S14, package_sha256=sha256_hex(canonical_bytes(proposed)),
        calendar=CALENDAR, now=NOW14)
    envelope = signing_envelope(challenge, signed_at=NOW14)
    generation = account.status()["generation"]
    if activate:
        account.activate_synthetic(now=NOW14)
        assert account.status()["generation"] == generation
    outcome = account.submit_settlement(envelope=envelope, signature=operator.sign(envelope),
        key_id=operator.key_id, package=proposed, sources=sources, calendar=CALENDAR, now=NOW14)
    if activate:
        assert outcome == Refusal("record_only_requires_halted")
        assert store.status()["head"]["session_id"] == B7_SESSION
        with sqlite3.connect(account.path) as db:
            assert db.execute("SELECT status FROM challenges WHERE challenge_id=?",
                              (challenge["challenge_id"],)).fetchone() == ("ISSUED",)
    else:
        assert isinstance(outcome, Receipt)


def test_b7_cannot_seat_a_head_outside_bound_calendar(tmp_path):
    store = settlement_boot(tmp_path, Operator())
    seal = boundary_seal("2026-10-30T17:10:00-04:00", "2026-10-30T17:15:00-04:00",
                         "2026-11-01T18:00:00-05:00")
    result = seat(store, seal, session_id="tradeify-account-day:2026-10-30",
                  close=datetime(2026, 10, 30, 21, tzinfo=timezone.utc),
                  now=datetime(2026, 10, 30, 21, 16, tzinfo=timezone.utc))
    assert result == Refusal("calendar_session_unavailable")
    assert store.status()["rows"] == 0


def test_b7_must_match_the_store_calendar_digest(tmp_path):
    store = SettlementStore.boot(tmp_path / "settlement.sqlite", "synthetic-account",
        trusted_keys={Operator().key_id: ["record_only"]}, calendar_digest="f" * 64,
        policy_digest="b" * 64, now=NOW14)
    assert seat(store, b7_seal()) == Refusal("calendar_digest_mismatch")
    assert store.status()["rows"] == 0


@pytest.mark.parametrize("defect,reason", [
    ("missing", "calendar_required"),
    ("unratified", "calendar_not_ratified"),
    ("future", "calendar_not_ratified"),
    ("close", "effective_close_not_session_close"),
    ("successor", "calendar_successor_unavailable"),
    ("reopen", "seal_reopen_mismatch"),
])
def test_b7_calendar_refusals_do_not_write_authority(tmp_path, defect, reason):
    store = settlement_boot(tmp_path, Operator())
    calendar = CALENDAR
    if defect == "missing":
        calendar = None
    elif defect == "unratified":
        calendar = replace(calendar, ratified_at=None)
    elif defect == "future":
        calendar = replace(calendar, ratified_at=NOW14)
    elif defect == "close":
        calendar = replace(calendar, rows=tuple(replace(row, closes_at=B7_CLOSE - timedelta(minutes=1))
            if row.session_id == B7_SESSION else row for row in calendar.rows))
    elif defect == "successor":
        calendar = replace(calendar, rows=tuple(row for row in calendar.rows if row.session_id != S14))
    elif defect == "reopen":
        calendar = replace(calendar, rows=tuple(replace(row, opens_at=row.opens_at + timedelta(minutes=1))
            if row.session_id == S14 else row for row in calendar.rows))
    assert seat(store, b7_seal(), calendar=calendar) == Refusal(reason)
    with sqlite3.connect(store.path) as db:
        for table in ("chain", "packages", "receipts", "sources"):
            assert db.execute(f"SELECT COUNT(*) FROM {table}").fetchone() == (0,)


def test_b7_can_record_a_denied_accounting_day(tmp_path):
    session = "tradeify-account-day:2026-09-07"
    assert CALENDAR.schedule_for(session).permission == "DENIED"
    store = settlement_boot(tmp_path, Operator())
    seal = boundary_seal("2026-09-07T17:10:00-04:00", "2026-09-07T17:15:00-04:00",
                         "2026-09-07T18:00:00-04:00")
    result = seat(store, seal, session_id=session,
                  close=datetime(2026, 9, 7, 21, tzinfo=timezone.utc),
                  now=datetime(2026, 9, 7, 21, 16, tzinfo=timezone.utc))
    assert isinstance(result, Receipt)


def test_transport_rejection_reaches_adapter_and_replays_without_resending(tmp_path):
    def registry():
        values = inert_adapters()
        values["orb_mnq_v7"].actions = [replace(intent("orb"), leg_id="orb_mnq_v7", qty=1)]
        return values
    account = runtime_owner(tmp_path, [BrokerResult("rejected")])
    runtime = FourLegRuntime(account, registry())
    for leg_id in LEGS:
        runtime.on_completed_bar(leg_id, bars()[leg_id], now=NOW)
    assert runtime.adapters["orb_mnq_v7"].events == [("reject", "orb", None)]
    assert account.pending_feedback == ()
    assert account.unresolved_attempts == ()
    assert account.exposure("orb_mnq_v7") == (0, 0)
    route = SyntheticBroker([])
    restarted = BookAccountOwner.boot(account.path, account.account, binding=runtime_binding(),
                                     synthetic_broker=route)
    recovered = FourLegRuntime.recover(restarted, registry())
    assert recovered.adapters["orb_mnq_v7"].events == [("reject", "orb", None)]
    assert route.commands == []


def test_control_refusal_deduplicates_retries_within_one_bar(tmp_path):
    account, _route = owner(tmp_path, [])
    amend = BracketAmend("orb_mnq_v7", Bracket(stop=100))
    for seconds in (1, 2):
        events = account.record_local_refusal(amend, "intervention_fence",
            operation_id="control:test", boundary_time=NOW, now=NOW + timedelta(seconds=seconds))
        assert len(events) == 1
    assert len(account.all_feedback) == 1


def test_accepted_real_price_stays_numeric_in_durable_feedback(tmp_path):
    account, _route = owner(tmp_path, [])
    account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_pr409_review2:244"), now=NOW)
    fact = BrokerFact.fill("real-price", "base", "dj30_mym_p250", "entry", 1, Fraction(1, 4), NOW)
    events = account.observe(fact, now=NOW)
    assert events[0].fill.price == 0.25
    assert account.all_feedback[0]["body"]["fill"]["price"] == 0.25
    assert account.observe(fact, now=NOW) == ()
