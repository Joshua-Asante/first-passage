"""Real SQLite/runtime ingress boundaries reject malformed values before effects."""
from dataclasses import replace
from decimal import Decimal
from fractions import Fraction

import pytest

from c1_rail.book_account_owner import AccountOwnerError
from c1_signal_daemon.book_protocol import Bracket, BracketAmend
from c1_signal_daemon.book_runtime import FourLegRuntime, LEG_ORDER
from test_four_leg_runtime import owner as runtime_owner, inert_adapters, bars, NOW
from test_book_account_owner import owner, intent


@pytest.mark.parametrize("changes", [
    {"high": 90, "low": 110}, {"close": float("nan")},
    {"open": float("inf")}, {"volume": -1}, {"close": True},
    {"ts": "bad"}, {"ts": NOW.replace(tzinfo=None)},
    {"volume": Decimal("10")},
])
def test_bad_bar_halts_before_partial_or_adapter(tmp_path, changes):
    account = runtime_owner(tmp_path, [])
    adapters = inert_adapters()
    runtime = FourLegRuntime(account, adapters)
    with pytest.raises(AccountOwnerError):
        runtime.on_completed_bar("orb_mnq_v7", replace(bars()["orb_mnq_v7"], **changes), now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.retained_partial_bars == ()
    assert adapters["orb_mnq_v7"].bars == []
    assert account.synthetic_broker.commands == []
    assert account.incidents


@pytest.mark.parametrize("price", [-1, 0, float("nan"), float("inf"), True, "100", Fraction(100), Decimal("100")])
def test_bad_trigger_halts_before_reservation(tmp_path, price):
    account, route = owner(tmp_path, [])
    with pytest.raises(AccountOwnerError):
        account.dispatch(replace(intent(), order_type="stop", price=price), occurrence=account.make_occurrence("direct", "test_book_ingress_validation:38"), now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.observable_accounting()["operations"] == ()
    assert account.unresolved_attempts == ()
    assert route.commands == []
    assert account.incidents


@pytest.mark.parametrize("method", ["set_mode", "on_bar"])
@pytest.mark.parametrize("bad", [None, [object()], [replace(intent(), leg_id="unknown")],
    [intent(), BracketAmend("orb_mnq_v7", "bad")],
    [replace(intent(), scope_fill_ids="bad")], [replace(intent(), bar_time="bad")]])
def test_bad_adapter_batch_is_fenced_before_any_dispatch(tmp_path, method, bad):
    account = runtime_owner(tmp_path, [])
    adapters = inert_adapters()
    setattr(adapters[LEG_ORDER[0]], method, lambda value: bad)
    runtime = FourLegRuntime(account, adapters)
    with pytest.raises(AccountOwnerError):
        for leg in LEG_ORDER:
            runtime.on_completed_bar(leg, bars()[leg], now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.observable_accounting()["operations"] == ()
    assert account.unresolved_attempts == ()
    assert account.synthetic_broker.commands == []
    assert account.incidents
    assert len(account.retained_barriers) == 1
    assert not account.retained_barriers[0]["completed"]


def test_diagnostic_redelivery_is_idempotent_and_conflict_remains_fenced(tmp_path):
    from datetime import timedelta
    from c1_signal_daemon.book_validation import InputViolation
    account, route = owner(tmp_path, [])
    before = account.status()["generation"]
    violation = InputViolation("positive_price", "price")
    account.record_input_incident("boundary:1", violation, source="batch", now=NOW)
    account.record_input_incident("boundary:1", violation, source="batch", now=NOW + timedelta(seconds=1))
    assert len(account.incidents) == 1
    assert account.status()["generation"] == before + 1
    with pytest.raises(AccountOwnerError, match="conflicting"):
        account.record_input_incident("boundary:1", InputViolation("scope", "scope_fill_ids"), source="batch", now=NOW)
    assert account.authority == "INTERVENTION"
    assert route.commands == []


def test_failed_incident_commit_latches_suppression_after_storage_recovers(tmp_path):
    import sqlite3
    from c1_rail.book_account_owner import BookAccountOwner, SyntheticBroker
    from test_book_account_owner import binding
    account, route = owner(tmp_path, [])
    # A real SQLite failure occurs after INSERT but before the authority update;
    # neither the incident nor the fence can be claimed durable.
    with sqlite3.connect(account.path) as db:
        db.execute("CREATE TRIGGER fail_fence BEFORE UPDATE ON owner_state BEGIN SELECT RAISE(ABORT, 'storage failure'); END")
    with pytest.raises(AccountOwnerError, match="state unavailable"):
        account.dispatch(replace(intent(), price=float("nan")), occurrence=account.make_occurrence("direct", "test_book_ingress_validation:93"), now=NOW)
    with sqlite3.connect(account.path) as db:
        db.execute("DROP TRIGGER fail_fence")
    assert account.incidents == ()
    assert account.status()["permission"] == "RUNNING"
    with pytest.raises(AccountOwnerError, match="local send suppression"):
        account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_book_ingress_validation:99"), now=NOW)
    assert route.commands == []
    fresh = BookAccountOwner.boot(account.path, "synthetic-account", binding=binding(), synthetic_broker=SyntheticBroker([]))
    assert fresh.permission == "HALTED"


def test_invalid_output_restart_retains_attempt_and_incomplete_boundary(tmp_path):
    from c1_rail.book_account_owner import BookAccountOwner, BrokerResult, SyntheticBroker
    from test_four_leg_runtime import binding
    account = runtime_owner(tmp_path, [BrokerResult("accepted")])
    prior = account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_book_ingress_validation:109"), now=NOW)
    adapters = inert_adapters()
    adapters[LEG_ORDER[0]].actions = [BracketAmend("orb_mnq_v7", "bad")]
    runtime = FourLegRuntime(account, adapters)
    with pytest.raises(AccountOwnerError):
        for leg in LEG_ORDER:
            runtime.on_completed_bar(leg, bars()[leg], now=NOW)
    assert account.retained_barriers[0]["actions"] is None
    route = SyntheticBroker([])
    fresh = BookAccountOwner.boot(account.path, "synthetic-account", binding=binding(), synthetic_broker=route)
    recovered_adapters = inert_adapters()
    with pytest.raises(AccountOwnerError, match="incomplete retained"):
        FourLegRuntime.recover(fresh, recovered_adapters)
    assert fresh.authority == "INTERVENTION"
    assert fresh.unresolved_attempts == (prior.attempt_id,)
    assert all(adapter.bars == [] for adapter in recovered_adapters.values())
    assert route.commands == []
    assert fresh.retained_barriers[0]["actions"] is None


@pytest.mark.parametrize("method", ["set_mode", "on_bar"])
@pytest.mark.parametrize("factory", [lambda: 1, lambda: (x for x in []),
    lambda: [replace(intent(), price=Fraction(100))], lambda: [replace(intent(), price=Decimal("100"))]])
def test_other_malformed_adapter_outputs(tmp_path, method, factory):
    account = runtime_owner(tmp_path, [])
    adapters = inert_adapters()
    setattr(adapters[LEG_ORDER[0]], method, lambda value: factory())
    runtime = FourLegRuntime(account, adapters)
    with pytest.raises(AccountOwnerError):
        for leg in LEG_ORDER:
            runtime.on_completed_bar(leg, bars()[leg], now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.observable_accounting()["operations"] == ()
    assert account.retained_barriers[0]["actions"] is None
    assert account.synthetic_broker.commands == []


def test_empty_amend_scope_is_explicit_no_target(tmp_path):
    account, route = owner(tmp_path, [])
    result = account.dispatch(BracketAmend("dj30_mym_p250", Bracket(stop=99), ()), occurrence=account.make_occurrence("direct", "test_book_ingress_validation:148"), now=NOW)
    assert result.transport_state == "not_attempted"
    assert result.refusal_reason == "empty_scope"
    assert account.observable_accounting()["operations"] == ()
    assert route.commands == []


@pytest.mark.parametrize("side,stop,expected", [("buy", 98.30, 98.0), ("sell", 101.70, 102.0)])
def test_off_tick_bracket_payload_and_directional_emulator_rounding(tmp_path, side, stop, expected):
    from c1_rail.book_account_owner import BrokerResult
    from c1_signal_daemon.book_protocol import Side, FillTiming, OrderIntent
    from test_tv_broker_emulator import emu, bar, fills
    action = OrderIntent("rounding", "orb_mnq_v7", "entry", Side(side), 1,
                         timing=FillTiming.THIS_CLOSE, bracket=Bracket(stop=stop))
    # Owner side authorization follows each leg's direction, so transport vector
    # uses the long leg; emulator independently exercises both rounding directions.
    if side == "buy":
        account = runtime_owner(tmp_path, [BrokerResult("accepted")])
        account.dispatch(action, occurrence=account.make_occurrence("direct", "test_book_ingress_validation:166"), now=NOW)
        assert account.synthetic_broker.commands[0].action.bracket.stop == 98.30
    from c1_signal_daemon.book_validation import validate_action
    assert validate_action(action) is None
    engine = emu()
    engine.submit([action], bar(0, 100, 100, 100, 100))
    outcomes = fills(engine.process_bar(bar(1, 100, 103, 97, 100)))
    assert outcomes[0].price == expected
    assert outcomes[0].qty == 1


def test_off_tick_trigger_is_not_rounded_before_crossing(tmp_path):
    from c1_rail.book_account_owner import BrokerResult
    from test_tv_broker_emulator import emu, bar, fills, entry
    from c1_signal_daemon.book_protocol import FillTiming
    action = entry("off-tick", price=100.1, order_type="stop", timing=FillTiming.THIS_CLOSE)
    account = runtime_owner(tmp_path, [BrokerResult("accepted")])
    account.dispatch(action, occurrence=account.make_occurrence("direct", "test_book_ingress_validation:183"), now=NOW)
    sent = account.synthetic_broker.commands[0].action
    assert sent.price == 100.1
    engine = emu()
    assert fills(engine.submit([sent], bar(0, 100, 100, 100, 100))) == []
    assert engine.pending_order_ids() == ["off-tick"]
    assert fills(engine.process_bar(bar(1, 100, 101, 99, 100)))[0].price == 100.25


def test_zero_trailing_activation_bare_entry_and_partial_quantity(tmp_path):
    from c1_rail.book_account_owner import BrokerFact, BrokerResult
    from c1_signal_daemon.book_protocol import Side, FillTiming
    from test_tv_broker_emulator import emu, bar, fills, entry
    from c1_signal_daemon.book_validation import validate_action
    trailing = entry("trail", timing=FillTiming.THIS_CLOSE,
                     bracket=Bracket(trail_activation_ticks=0, trail_offset_ticks=4))
    assert validate_action(trailing) is None
    engine = emu()
    engine.submit([trailing], bar(0, 100, 100, 100, 100))
    assert fills(engine.process_bar(bar(1, 100, 102, 99, 100)))[0].price == 100.75
    account, route = owner(tmp_path, [BrokerResult("accepted", (
        BrokerFact.fill("partial", "base", "dj30_mym_p250", "entry", 1, 100, NOW),
        BrokerFact.terminal("base", "cancelled", 1, NOW),
    )), BrokerResult("accepted")])
    account.dispatch(intent(), occurrence=account.make_occurrence("direct", "test_book_ingress_validation:206"), now=NOW)
    assert route.commands[0].action.bracket is None
    assert route.commands[0].quantity == 3
    result = account.dispatch(replace(intent("partial-exit", kind="exit", qty=1),
                                      side=Side.SELL, scope_fill_ids=("partial",)), occurrence=account.make_occurrence("direct", "test_book_ingress_validation:209"), now=NOW)
    assert result.quantity == 1
    assert route.commands[1].action.qty == 1
    assert route.commands[1].action.scope_fill_ids == ("partial",)
    assert account.exposure("dj30_mym_p250") == (1, 0)


@pytest.mark.parametrize("changes", [
    {"qty": True}, {"qty": 1.0}, {"qty": -1}, {"qty": None},
    {"side": "buy"}, {"timing": "this_close"}, {"kind": []},
    {"order_type": []}, {"leg_id": []}, {"order_id": ""},
    {"oca_group": 1}, {"reason": None}, {"stop_dist_pts": True},
    {"stop_dist_pts": -1}, {"bar_time": "bad"},
    {"scope_fill_ids": (["bad"],)}, {"scope_fill_ids": ("a", "a")},
    {"bracket": Bracket(stop=True)}, {"bracket": Bracket(limit=Decimal("100"))},
    {"bracket": Bracket(trail_activation_ticks=1)},
    {"bracket": Bracket(trail_activation_ticks=-1, trail_offset_ticks=1)},
    {"bracket": Bracket(trail_activation_ticks=0, trail_offset_ticks=0)},
])
def test_malformed_typed_action_fields_are_fenced(tmp_path, changes):
    action = intent()
    # Simulate an untrusted producer bypassing dataclass constructor checks.
    for field, value in changes.items():
        object.__setattr__(action, field, value)
    account, route = owner(tmp_path, [])
    with pytest.raises(AccountOwnerError):
        account.dispatch(action, occurrence=account.make_occurrence("direct", "test_book_ingress_validation:236"), now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.incidents
    assert account.observable_accounting()["operations"] == ()
    assert route.commands == []


def test_untyped_source_value_fences_loop(tmp_path):
    from c1_signal_daemon.book_evaluate_loop import FourLegEvaluateLoop
    class Source:
        def poll(self):
            return "invalid source payload"
    account = runtime_owner(tmp_path, [])
    adapters = inert_adapters()
    loop = FourLegEvaluateLoop(sources={leg: Source() for leg in LEG_ORDER},
                              runtime=FourLegRuntime(account, adapters))
    with pytest.raises(AccountOwnerError):
        loop.step(now=NOW)
    assert account.authority == "INTERVENTION"
    assert account.retained_partial_bars == ()
    assert account.synthetic_broker.commands == []
    assert all(adapter.bars == [] for adapter in adapters.values())


def test_legacy_invalid_partial_is_fenced_before_recovery_adapters(tmp_path):
    from c1_rail.book_account_owner import BookAccountOwner, SyntheticBroker
    from test_four_leg_runtime import binding
    account = runtime_owner(tmp_path, [])
    # Existing pre-correction databases could retain structurally invalid bars.
    account.record_partial_bar("orb_mnq_v7", NOW,
        {"ts": NOW.isoformat(), "open": 100, "high": 90, "low": 110, "close": 100, "volume": 10}, acquired_at=NOW)
    fresh = BookAccountOwner.boot(account.path, "synthetic-account", binding=binding(), synthetic_broker=SyntheticBroker([]))
    adapters = inert_adapters()
    with pytest.raises(AccountOwnerError, match="invalid retained bar"):
        FourLegRuntime.recover(fresh, adapters)
    assert fresh.authority == "INTERVENTION"
    assert fresh.incidents
    assert fresh.retained_partial_bars
    assert all(adapter.bars == [] for adapter in adapters.values())
    assert fresh.synthetic_broker.commands == []
