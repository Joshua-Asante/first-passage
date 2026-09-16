"""Durable synthetic execution crosses the real listener/account-owner boundary."""
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from c1_rail.book_account_owner import (
    AccountOwnerError,
    BookAccountOwner,
    BrokerFact,
    BrokerResult,
    SyntheticBroker,
    SimulatedOwnerCrash,
)
from c1_rail.book_policy import candidate_book_protection_policy
from c1_rail.book_sizing_context import BookSession, SettledClose
from c1_rail.c1_rail_listener import handle_book_action
from c1_signal_daemon.book_protocol import (
    Bracket,
    BracketAmend,
    FillTiming,
    Mode,
    OrderIntent,
    Side,
)


NOW = datetime(2026, 9, 15, 14, tzinfo=timezone.utc)
SESSION = BookSession(
    "tradeify-account-day:2026-09-15",
    "tradeify-account-day:2026-09-14",
    NOW - timedelta(hours=1),
    NOW + timedelta(hours=1),
    NOW + timedelta(hours=2),
    "c" * 64,
    NOW + timedelta(hours=1, minutes=10),
    NOW + timedelta(hours=1, minutes=15),
)
SETTLED = SettledClose(
    SESSION.prior_session_id,
    SESSION.opens_at - timedelta(minutes=1),
    98_500.0,
    100_000.0,
    "e" * 64,
)


def binding():
    return {
        "session": SESSION,
        "settlement": SETTLED,
        "policy": candidate_book_protection_policy(),
        "policy_digest": "d" * 64,
        "snapshot_digest": "a" * 64,
        "as_of": NOW - timedelta(seconds=1),
        "valid_until": NOW + timedelta(minutes=5),
        "max_evidence_age": timedelta(seconds=30),
        "lifecycle_tiers": {
            "aegis_6j": "AUTHORIZED",
            "dj30_mym_p250": "AUTHORIZED",
            "vanguard_mgc": "AUTHORIZED",
            "orb_mnq_v7": "AUTHORIZED",
        },
        "cap_allocations": {
            "aegis_6j": 80,
            "dj30_mym_p250": 80,
            "vanguard_mgc": 80,
            "orb_mnq_v7": 80,
        },
        "risk_dollars": {"dj30_mym_p250": 100},
    }


def intent(order_id="base", *, kind="entry", qty=5):
    return OrderIntent(
        order_id,
        "dj30_mym_p250",
        kind,
        Side.BUY,
        qty,
        timing=FillTiming.THIS_CLOSE,
        stop_dist_pts=24,
        bar_time=NOW,
    )


def owner(tmp_path, results):
    route = SyntheticBroker(results)
    result = BookAccountOwner.boot(
        tmp_path / "owner.sqlite",
        "synthetic-account",
        binding=binding(),
        synthetic_broker=route,
    )
    result.activate_synthetic(now=NOW)
    return result, route


def test_existing_empty_account_database_is_not_reinitialized(tmp_path):
    path = tmp_path / "owner.sqlite"
    path.touch()

    with pytest.raises(AccountOwnerError, match="state unavailable"):
        BookAccountOwner.boot(
            path, "synthetic-account", binding=binding(),
            synthetic_broker=SyntheticBroker([]),
        )

    assert path.read_bytes() == b""


def test_transport_acceptance_never_creates_fill_credit_and_restart_retains_reservation(tmp_path):
    account, route = owner(tmp_path, [BrokerResult("accepted")])
    outcome = handle_book_action(intent(), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:114"), now=NOW)

    assert outcome.transport_state == "accepted"
    assert outcome.confirmed_events == ()
    assert account.exposure("dj30_mym_p250") == (0, 3)
    assert route.commands[0].quantity == 3

    restarted = BookAccountOwner.boot(
        tmp_path / "owner.sqlite",
        "synthetic-account",
        binding=binding(),
        synthetic_broker=SyntheticBroker([]),
    )
    assert restarted.permission == "HALTED"
    assert restarted.exposure("dj30_mym_p250") == (0, 3)
    assert restarted.unresolved_attempts == (outcome.attempt_id,)


def test_partial_fill_and_duplicate_fact_use_confirmed_base_once(tmp_path):
    fill = BrokerFact.fill("execution-1", "base", "dj30_mym_p250", "entry", 1, 100.0, NOW)
    account, _ = owner(tmp_path, [BrokerResult("accepted", (fill, fill))])
    base = handle_book_action(intent(), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:135"), now=NOW)

    assert [event.fill.qty for event in base.confirmed_events] == [1]
    assert account.exposure("dj30_mym_p250") == (1, 2)

    # Terminal evidence releases only the unfilled remainder. The next add is
    # sized from the one confirmed base contract: floor(1 * 250%) == 2.
    account.observe(BrokerFact.terminal("base", "cancelled", 1, NOW), now=NOW)
    account.activate_synthetic(now=NOW + timedelta(seconds=1))
    account.synthetic_broker.queue(BrokerResult("accepted"))
    add = handle_book_action(intent("add-1", kind="add", qty=12), account,
                             occurrence=account.make_occurrence("direct", "test_book_account_owner:145"), now=NOW + timedelta(seconds=1))
    assert add.quantity == 2
    assert account.exposure("dj30_mym_p250") == (1, 2)


def test_zero_sizing_is_an_ordinary_refusal_not_an_incident(tmp_path):
    data = binding()
    data["lifecycle_tiers"] = dict(data["lifecycle_tiers"], vanguard_mgc="RETIRED")
    account = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=data,
        synthetic_broker=SyntheticBroker([]),
    )
    account.activate_synthetic(now=NOW)
    action = OrderIntent("v", "vanguard_mgc", "entry", Side.BUY, 2, bar_time=NOW)
    outcome = handle_book_action(action, account, occurrence=account.make_occurrence("direct", "test_book_account_owner:160"), now=NOW)

    assert outcome.refusal_reason == "zero_size"
    assert account.permission == "RUNNING"
    assert account.incidents == ()
    assert account.synthetic_broker.commands == []


def test_flat_without_confirmed_exposure_is_an_ordinary_no_send(tmp_path):
    account, route = owner(tmp_path, [])
    action = OrderIntent("empty-flat", "dj30_mym_p250", "flat", Side.SELL,
                         None, bar_time=NOW)
    outcome = account.dispatch(action, occurrence=account.make_occurrence("direct", "test_book_account_owner:172"), now=NOW)
    assert outcome.refusal_reason == "zero_exposure"
    assert route.commands == []
    assert account.permission == "RUNNING"


def test_close_reservation_prevents_duplicate_or_excess_reduction(tmp_path):
    filled = BrokerFact.fill("execution-1", "base", "dj30_mym_p250", "entry",
                             2, 100.0, NOW)
    account, route = owner(tmp_path, [
        BrokerResult("accepted", (filled, BrokerFact.terminal("base", "cancelled", 2, NOW))),
        BrokerResult("accepted"),
    ])
    handle_book_action(intent(qty=5), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:185"), now=NOW)
    first = account.dispatch(OrderIntent(
        "exit-1", "dj30_mym_p250", "exit", Side.SELL, 2,
        scope_fill_ids=("execution-1",), bar_time=NOW), occurrence=account.make_occurrence("direct", "test_book_account_owner:186"), now=NOW)
    duplicate = account.dispatch(OrderIntent(
        "exit-2", "dj30_mym_p250", "exit", Side.SELL, None,
        scope_fill_ids=("execution-1",), bar_time=NOW), occurrence=account.make_occurrence("direct", "test_book_account_owner:189"), now=NOW)

    assert first.transport_state == "accepted", first
    assert duplicate.refusal_reason == "zero_exposure"
    assert [command.operation_id for command in route.commands] == ["base", "exit-1"]


def test_unknown_protection_attempt_fences_before_flat_deadline(tmp_path):
    from book_occurrence_fixtures import bare_protection_owner, prepare_protection
    account, route = bare_protection_owner(tmp_path)
    route.queue(BrokerResult("unknown"))
    outcome = prepare_protection(account, route,
        BracketAmend("dj30_mym_p250", Bracket(stop=99.0), ("base-fill",)), "unknown-attachment")
    assert outcome.transport_state == "unknown"
    assert outcome.attempt_id in account.unresolved_attempts
    assert account.authority == "INTERVENTION"
    count = len(route.commands)
    account.advance_schedule(now=SESSION.own_flat_deadline)
    assert account.authority == "INTERVENTION"
    assert account.incidents[-1]["reason"] == "protection"
    assert len(route.commands) == count
    assert account.exposure("dj30_mym_p250") == (3, 0)


def test_incident_fences_every_later_mutation_and_status_reads_are_pure(tmp_path):
    account, route = owner(tmp_path, [BrokerResult("accepted")])
    before = account.status()
    assert account.status() == before

    account.halt("incident-1", "execution", now=NOW)
    refused = handle_book_action(intent("second"), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:217"), now=NOW)

    assert refused.refusal_reason == "intervention_fence"
    assert account.authority == "INTERVENTION"
    assert len(route.commands) == 0
    assert account.status() == account.status()


def test_stale_or_conflicting_broker_fact_retains_reservation_and_halts(tmp_path):
    account, _ = owner(tmp_path, [BrokerResult("accepted")])
    handle_book_action(intent(), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:227"), now=NOW)
    account.observe(
        BrokerFact.fill("execution-1", "base", "dj30_mym_p250", "entry", 1, 100.0,
                        NOW - timedelta(minutes=1)),
        now=NOW,
    )

    assert account.exposure("dj30_mym_p250") == (0, 3)
    assert account.permission == "HALTED"
    assert account.authority == "INTERVENTION"
    assert account.incidents[-1]["reason"] == "execution"


@pytest.mark.parametrize(("leg_id", "order_kind"), [
    ("vanguard_mgc", "entry"),
    ("dj30_mym_p250", "add"),
])
def test_fill_identity_conflict_retains_reservation_without_feedback(
        tmp_path, leg_id, order_kind):
    account, _ = owner(tmp_path, [BrokerResult("accepted")])
    handle_book_action(intent(), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:247"), now=NOW)

    feedback = account.observe(
        BrokerFact.fill("conflicting-fill", "base", leg_id, order_kind,
                        1, 100.0, NOW),
        now=NOW,
    )

    assert feedback == ()
    assert account.exposure("dj30_mym_p250") == (0, 3)
    assert account.pending_feedback == ()
    assert account.authority == "INTERVENTION"


def test_cutoff_keeps_only_scheduled_exit_authority_and_flatten_uses_confirmed_facts(tmp_path):
    fill = BrokerFact.fill("execution-1", "base", "dj30_mym_p250", "entry", 1,
                           100.0, NOW)
    account, route = owner(tmp_path, [
        BrokerResult("accepted", (fill, BrokerFact.terminal("base", "cancelled", 1, NOW))),
    ])
    handle_book_action(intent(), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:267"), now=NOW)

    account.advance_schedule(now=SESSION.risk_add_cutoff)
    assert account.permission == "HALTED"
    assert account.authority == "SCHEDULED_EXIT"
    assert handle_book_action(intent("late"), account,
                              occurrence=account.make_occurrence("direct", "test_book_account_owner:272"), now=SESSION.risk_add_cutoff).refusal_reason == "risk_add_not_authorized"

    flat_id = "scheduled-flat:" + SESSION.session_id + ":dj30_mym_p250"
    route.queue(BrokerResult("accepted", (
        BrokerFact.fill("flat-1", flat_id, "dj30_mym_p250", "flat", 1, 101.0,
                        SESSION.flatten_start, entry_execution_id="execution-1"),
    )))
    result = account.advance_schedule(now=SESSION.flatten_start)
    assert result[0].operation_id == flat_id
    assert account.exposure("dj30_mym_p250") == (0, 0)
    assert account.authority == "SCHEDULED_EXIT"


def test_ambiguous_cutoff_cancel_is_retained_and_deadline_revokes_all_sends(tmp_path):
    account, route = owner(tmp_path, [BrokerResult("accepted"), BrokerResult("unknown")])
    handle_book_action(intent(), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:288"), now=NOW)

    cutoff = account.advance_schedule(now=SESSION.risk_add_cutoff)
    assert len(cutoff) == 1
    assert route.commands[-1].kind == "cancel"
    assert route.commands[-1].target_operation_id == "base"
    assert account.exposure("dj30_mym_p250") == (0, 3)

    before = len(route.commands)
    account.advance_schedule(now=SESSION.own_flat_deadline)
    assert account.authority == "INTERVENTION"
    assert account.incidents[-1]["reason"] == "schedule"
    account.advance_schedule(now=SESSION.own_flat_deadline + timedelta(seconds=1))
    assert len(route.commands) == before


def test_protected_session_cancels_resting_orb_add_without_resizing_carried_fill(tmp_path):
    normal = binding()
    normal["settlement"] = replace(SETTLED, equity=100_000.0)
    route = SyntheticBroker([
        BrokerResult("accepted", (
            BrokerFact.fill("orb-fill", "orb-base", "orb_mnq_v7", "entry", 1,
                            100.0, NOW),
            BrokerFact.terminal("orb-base", "filled", 1, NOW),
        )),
        BrokerResult("accepted"),
    ])
    account = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                    binding=normal, synthetic_broker=route)
    account.activate_synthetic(now=NOW)
    handle_book_action(OrderIntent("orb-base", "orb_mnq_v7", "entry", Side.BUY, 1,
                                   bar_time=NOW), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:318"), now=NOW)
    handle_book_action(OrderIntent("orb-add", "orb_mnq_v7", "add", Side.BUY, 3,
                                   bar_time=NOW), account, occurrence=account.make_occurrence("direct", "test_book_account_owner:320"), now=NOW)
    assert account.exposure("orb_mnq_v7") == (1, 1)

    next_now = NOW + timedelta(days=1)
    protected = binding()
    protected["session"] = replace(
        SESSION, session_id="tradeify-account-day:2026-09-16",
        prior_session_id=SESSION.session_id,
        opens_at=next_now - timedelta(hours=1), risk_add_cutoff=next_now + timedelta(hours=1),
        flatten_start=next_now + timedelta(hours=1, minutes=10),
        own_flat_deadline=next_now + timedelta(hours=1, minutes=15),
        closes_at=next_now + timedelta(hours=2),
    )
    protected["settlement"] = replace(SETTLED, session_id=SESSION.session_id,
                                      as_of=next_now - timedelta(hours=2))
    protected["as_of"] = next_now - timedelta(seconds=1)
    protected["valid_until"] = next_now + timedelta(minutes=5)
    cancel_route = SyntheticBroker([
        BrokerResult("accepted", (BrokerFact.terminal("orb-add", "cancelled", 0,
                                                       next_now),)),
    ])
    restarted = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                      binding=protected, synthetic_broker=cancel_route)
    restarted.activate_synthetic(now=next_now)

    assert cancel_route.commands[0].kind == "cancel"
    assert cancel_route.commands[0].target_operation_id == "orb-add"
    assert restarted.exposure("orb_mnq_v7") == (1, 0)
    assert restarted.permission == "RUNNING"


def test_aegis_takeover_waits_for_displaced_leg_quiescence_before_send(tmp_path):
    normal = binding()
    normal["settlement"] = replace(SETTLED, equity=100_000.0)
    flat_id = "takeover-flat:aegis-entry:orb_mnq_v7"
    route = SyntheticBroker([
        BrokerResult("accepted", (
            BrokerFact.fill("orb-fill", "orb-base", "orb_mnq_v7", "entry", 1,
                            100.0, NOW),
            BrokerFact.terminal("orb-base", "filled", 1, NOW),
        )),
        BrokerResult("accepted", (
            BrokerFact.fill("orb-flat", flat_id, "orb_mnq_v7", "flat", 1,
                            99.0, NOW, entry_execution_id="orb-fill"),
        )),
        BrokerResult("accepted"),
    ])
    account = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
                                    binding=normal, synthetic_broker=route)
    account.activate_synthetic(now=NOW)
    account.dispatch(OrderIntent("orb-base", "orb_mnq_v7", "entry", Side.BUY, 1,
                                 bar_time=NOW), occurrence=account.make_occurrence("direct", "test_book_account_owner:371"), now=NOW)
    aegis = OrderIntent("aegis-entry", "aegis_6j", "entry", Side.SELL, 8,
                        bar_time=NOW)

    pending = account.dispatch(aegis, occurrence=account.make_occurrence("direct", "test_book_account_owner:376"), now=NOW)
    assert pending.refusal_reason == "takeover_pending"
    assert [command.operation_id for command in route.commands] == ["orb-base"]

    controls, completed = account.advance_takeover(now=NOW)
    assert completed is True
    assert controls[0].operation_id == flat_id
    accepted = account.dispatch(aegis, occurrence=account.make_occurrence("direct", "test_book_account_owner:383"), now=NOW)
    assert accepted.transport_state == "accepted"
    assert [command.operation_id for command in route.commands] == [
        "orb-base", flat_id, "aegis-entry"
    ]
    assert account.exposure("orb_mnq_v7") == (0, 0)
    assert account.exposure("aegis_6j") == (0, 8)


@pytest.mark.parametrize("cut,commands,attempts", [
    ("after_reservation", 0, 0),
    ("before_send", 0, 1),
    ("after_send", 1, 1),
])
def test_crash_cuts_retain_obligation_and_never_retry_on_boot(tmp_path, cut, commands, attempts):
    route = SyntheticBroker([BrokerResult("accepted", (
        BrokerFact.fill("remote-fill", "base", "dj30_mym_p250", "entry", 1,
                        100.0, NOW),
    ))])
    account = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=binding(),
        synthetic_broker=route, crash_at=cut)
    account.activate_synthetic(now=NOW)
    with pytest.raises(SimulatedOwnerCrash):
        account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_book_account_owner:407"), now=NOW)
    assert len(route.commands) == commands

    recovery_route = SyntheticBroker([])
    restarted = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=binding(),
        synthetic_broker=recovery_route)
    assert restarted.permission == "HALTED"
    assert restarted.exposure("dj30_mym_p250") == (0, 3)
    assert len(restarted.unresolved_attempts) == attempts
    assert recovery_route.commands == []


def test_fresh_boot_fences_the_previous_owner_actor(tmp_path):
    old, old_route = owner(tmp_path, [])
    fresh = BookAccountOwner.boot(
        tmp_path / "owner.sqlite", "synthetic-account", binding=binding(),
        synthetic_broker=SyntheticBroker([]))
    with pytest.raises(AccountOwnerError, match="stale account owner boot"):
        old.dispatch(intent(), occurrence=old.make_occurrence("direct", "test_book_account_owner:426"), now=NOW)
    with pytest.raises(AccountOwnerError, match="stale account owner boot"):
        old.activate_synthetic(now=NOW)
    assert old_route.commands == []
    assert fresh.permission == "HALTED"


def test_incident_and_scheduled_cutoff_each_rotate_generation(tmp_path):
    account, _ = owner(tmp_path, [])
    before = account.status()["generation"]
    account.halt("generation-incident", "execution", now=NOW)
    assert account.status()["generation"] == before + 1

    scheduled, _ = owner(tmp_path / "scheduled", [])
    scheduled_before = scheduled.status()["generation"]
    scheduled.advance_schedule(now=SESSION.risk_add_cutoff)
    assert scheduled.status()["generation"] == scheduled_before + 1


def test_same_session_runtime_binding_cannot_be_replaced_on_restart(tmp_path):
    account, _ = owner(tmp_path, [])
    retained_digest = account.status()["runtime_binding_digest"]
    changed = binding()
    changed["settlement"] = replace(changed["settlement"], equity=98_400.0)
    with pytest.raises(AccountOwnerError, match="binding changed within session"):
        BookAccountOwner.boot(
            account.path, "synthetic-account", binding=changed,
            synthetic_broker=SyntheticBroker([]))
    assert account.status()["runtime_binding_digest"] == retained_digest
