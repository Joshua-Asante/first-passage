"""Third-review execution regressions; runtime cases need no signing dependency."""
from dataclasses import asdict, replace
from datetime import timedelta
import json
import sqlite3

import pytest

from c1_rail.book_account_owner import BookAccountOwner, BrokerFact, BrokerResult, SyntheticBroker
from c1_signal_daemon.book_protocol import Bracket, BracketAmend, Mode, Side
from c1_signal_daemon.book_runtime import FourLegRuntime
from test_four_leg_runtime import NOW, binding, entry, inert_adapters
from test_pr409_owner_lifecycle import filled_owner
from test_book_account_owner import intent
from book_bootstrap_fixtures import BootstrapBroker, activate_fresh


class EmptySource:
    def poll(self):
        return None


@pytest.mark.parametrize("completed", [False, True])
@pytest.mark.parametrize("rebuild", [False, True])

def test_total_source_silence_expires_without_a_partial_barrier(tmp_path, completed, rebuild):
    from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
    from test_four_leg_runtime import owner, bars, LEGS
    account = owner(tmp_path, [])
    runtime = FourLegRuntime(account, inert_adapters())
    if completed:
        for leg_id, bar in bars().items():
            runtime.on_completed_bar(leg_id, bar, now=NOW)
    sources = {leg_id: EmptySource() for leg_id in LEGS}
    loop = FourLegEvaluateLoop(sources=sources, runtime=runtime)
    loop.step(now=NOW)
    assert runtime.pending_bar_times == ()
    if rebuild:
        runtime = FourLegRuntime.recover(account, inert_adapters())
        loop = FourLegEvaluateLoop(sources=sources, runtime=runtime)
    deadline = NOW + timedelta(minutes=30, seconds=30)
    loop.step(now=deadline)
    assert account.authority == "NORMAL"
    loop.step(now=deadline + timedelta(seconds=1))
    assert account.authority == "INTERVENTION"
    assert account.permission == "HALTED"
    assert account.synthetic_broker.commands == []
    restarted = BookAccountOwner.boot(account.path, account.account, binding=binding(),
                                     synthetic_broker=BootstrapBroker([]))
    assert restarted.authority == "INTERVENTION"
    with sqlite3.connect(account.path) as db:
        assert db.execute("SELECT reason FROM incidents WHERE reason='feed'").fetchall() == [("feed",)]


@pytest.mark.parametrize("expired", ["age", "valid_until", "cutoff"])
def test_expired_takeover_releases_capacity_and_delivers_rejection(tmp_path, expired):
    bound = binding()
    if expired != "age":
        bound["max_evidence_age"] = timedelta(hours=3)
    if expired == "cutoff":
        bound["valid_until"] = NOW + timedelta(hours=2)
    account = BookAccountOwner.boot(tmp_path / "owner.sqlite", "synthetic-account",
        binding=bound, synthetic_broker=BootstrapBroker([BrokerResult('accepted')]))
    activate_fresh(account, now=NOW)
    runtime = FourLegRuntime(account, inert_adapters())
    runtime._mode_actions(Mode.NORMAL)
    account.dispatch(entry("orb_mnq_v7", 1), occurrence=account.make_occurrence("direct", "test_pr409_review3:65"), now=NOW)
    action = entry("aegis_6j", 8)
    assert account.dispatch(action, occurrence=account.make_occurrence("direct", "test_pr409_review3:67"), now=NOW).refusal_reason == "takeover_pending"
    late = {"age": NOW + timedelta(seconds=31), "valid_until": bound["valid_until"],
            "cutoff": bound["session"].risk_add_cutoff}[expired]
    runtime.observe_fact(BrokerFact.terminal("entry:orb_mnq_v7", "cancelled", 0, late), now=late)
    assert account.exposure("aegis_6j") == (0, 0)
    assert any(row["body"]["event"] == "reject" and row["body"]["order_id"] == action.order_id
               for row in account.all_feedback)
    assert account.pending_feedback == ()
    assert not any(c.operation_id == action.order_id for c in account.synthetic_broker.commands)
    account.resume_takeover(now=late)
    account.advance_schedule(now=bound["session"].own_flat_deadline)
    # Rev9: authorization expiry before cutoff revokes scheduled authority too.
    assert account.authority == ("INTERVENTION" if expired == "valid_until" else "SCHEDULED_EXIT")
    operations = account.observable_accounting()["operations"]
    restarted = BookAccountOwner.boot(account.path, account.account, binding=bound,
                                     synthetic_broker=BootstrapBroker([]))
    assert restarted.exposure("aegis_6j") == (0, 0)
    assert restarted.observable_accounting()["operations"] == operations


def test_source_silence_revokes_scheduled_exit_authority(tmp_path):
    from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
    from test_four_leg_runtime import owner, LEGS
    account = owner(tmp_path, [])
    loop = FourLegEvaluateLoop(sources={leg: EmptySource() for leg in LEGS},
                               runtime=FourLegRuntime(account, inert_adapters()))
    from test_four_leg_runtime import bars
    for minutes in (0, 15, 30):
        at = NOW + timedelta(minutes=minutes)
        for leg_id, bar in bars().items():
            loop.runtime.on_completed_bar(leg_id, replace(bar, ts=at), now=at)
    cutoff = account.binding["session"].risk_add_cutoff
    loop.step(now=cutoff - timedelta(minutes=25))
    loop.step(now=cutoff)
    assert account.authority == "SCHEDULED_EXIT"
    loop.step(now=cutoff + timedelta(minutes=5, seconds=31))
    assert account.authority == "INTERVENTION"


def test_outside_session_poll_does_not_start_or_expire_feed_clock(tmp_path):
    from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
    from test_four_leg_runtime import owner, LEGS
    account = owner(tmp_path, [])
    loop = FourLegEvaluateLoop(sources={leg: EmptySource() for leg in LEGS},
                               runtime=FourLegRuntime(account, inert_adapters()))
    session = account.binding["session"]
    loop.step(now=session.opens_at - timedelta(seconds=1))
    with sqlite3.connect(account.path) as db:
        assert db.execute("SELECT * FROM feed_watch").fetchall() == []
    loop.step(now=session.opens_at)
    assert account.authority == "NORMAL"
    loop.step(now=session.closes_at)
    assert account.authority == "SCHEDULED_EXIT"


def test_schema_two_missing_source_watch_is_corruption(tmp_path):
    from test_four_leg_runtime import owner
    from c1_rail.book_account_owner import AccountOwnerError
    import pytest
    account = owner(tmp_path, [])
    with sqlite3.connect(account.path) as db:
        db.execute("DROP TABLE feed_watch")
    before = account.path.read_bytes()
    with pytest.raises(AccountOwnerError, match="schema"):
        BookAccountOwner.boot(account.path, account.account, binding=binding(),
                              synthetic_broker=BootstrapBroker([]))
    assert account.path.read_bytes() == before


def test_cutoff_retires_takeover_before_displaced_terminal(tmp_path):
    from test_four_leg_runtime import owner
    account = owner(tmp_path, [BrokerResult('accepted')])
    runtime = FourLegRuntime(account, inert_adapters())
    runtime._mode_actions(Mode.NORMAL)
    account.dispatch(entry("orb_mnq_v7", 1), occurrence=account.make_occurrence("direct", "test_pr409_review3:134"), now=NOW)
    action = entry("aegis_6j", 8)
    assert account.dispatch(action, occurrence=account.make_occurrence("direct", "test_pr409_review3:136"), now=NOW).refusal_reason == "takeover_pending"
    cutoff = account.binding["session"].risk_add_cutoff
    runtime.advance_schedule(now=cutoff)
    assert any(row["body"]["order_id"] == action.order_id for row in account.all_feedback)
    assert account.exposure("orb_mnq_v7") == (0, 1)
    runtime.observe_fact(BrokerFact.terminal("entry:orb_mnq_v7", "cancelled", 0, cutoff), now=cutoff)
    assert account.exposure("aegis_6j") == (0, 0)
    with account._transaction() as db:
        assert account._capacity(db).takeover is None
        assert account._capacity(db).blocks == ()
    runtime.advance_schedule(now=account.binding["session"].own_flat_deadline)
    assert account.authority == "SCHEDULED_EXIT"


@pytest.mark.parametrize("kind", ["stop", "bracket", "exit"])
def test_broker_command_and_journal_preserve_normalized_action(tmp_path, kind):
    account, route = filled_owner(tmp_path)
    levels = Bracket(stop=90, limit=120, trail_activation_ticks=4, trail_offset_ticks=2)
    if kind == "stop":
        action = replace(intent(), order_type="stop", price=101, bracket=levels,
                         oca_group="breakout", reason="synthetic stop")
    elif kind == "bracket":
        from book_occurrence_fixtures import bare_protection_owner, prepare_protection
        from c1_rail.book_account_owner import BrokerResult
        account, route = bare_protection_owner(tmp_path / "protection")
        route.queue(BrokerResult("accepted"))
        action = BracketAmend("dj30_mym_p250", levels, ("base-fill",))
    else:
        account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_pr409_review3:158"), now=NOW)
        action = (BracketAmend("dj30_mym_p250", levels, ("base-fill",)) if kind == "bracket"
                  else replace(intent("close", kind="exit", qty=None), side=Side.SELL,
                               scope_fill_ids=("base-fill",), reason="scoped close"))
    result = (prepare_protection(account, route, action, "roundtrip-bracket") if kind == "bracket" else
              account.dispatch(action, occurrence=account.make_occurrence("direct", "test_pr409_review3:162"), now=NOW))
    assert result.refusal_reason is None
    command = route.commands[-1]
    expected = action if kind == "bracket" else replace(action, qty=result.quantity)
    assert command.action == expected
    with sqlite3.connect(account.path) as db:
        raw = json.loads(db.execute("SELECT body FROM attempts WHERE attempt_id=?",
                                   (command.attempt_id,)).fetchone()[0])
    # Round-trip precisely what the receiver sees, including nested bracket/scope.
    from c1_rail.book_account_owner import _body
    assert raw["action"] == json.loads(_body(asdict(expected)))


@pytest.mark.parametrize("basis", [[], {}, ["VENUE_ROW"], {"basis": "VENUE_ROW"}, None, 7, True])
def test_signed_nonscalar_settlement_basis_is_a_refusal(tmp_path, basis):
    from test_book_settlement import Operator, seated, package, S14, NOW14, challenge, submit
    from c1_rail.book_settlement import Refusal
    operator = Operator()
    store, head = seated(tmp_path, operator)
    proposed, sources = package(head, S14, NOW14, scope="record_only")
    proposed["settlement_basis"] = basis
    envelope = challenge(store, proposed, target=None, now=NOW14,
                         scope="record_only", permission="HALTED")
    assert submit(store, operator, envelope, proposed, sources, NOW14) == Refusal("settlement_basis")
    assert store.status()["head"]["session_id"] == head.session_id
