"""PR 365 at bafdd97: restart fences, complete attach intents and trustworthy risk fields."""
from dataclasses import replace

import pytest

from book_protocol import Bracket
from tests.ops.tb_s3_kernel.harness import MIN, Sequence, entry, fill_lot, make_world
from tests.ops.test_tb_s3_kernel_redesign import Crash, crash_once
from tests.ops.test_tb_s3_kernel_review_round4 import CutStore
from tests.ops.tb_s3_kernel.broker import BAR


def test_retained_amendment_cannot_loosen_using_a_pre_restart_read():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    ref = w.broker.lots[lot].protection["stop"]
    crash_once(w.kernel, "modify", "planned")
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=95), w.now)
    w.broker.orders[ref].price = 100
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    assert w.broker.orders[ref].price == 100
    assert not [e for e in w.broker.log if e["event"] == "modify"]
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), order_level=False))
    w.kernel.progress(w.now)
    assert w.broker.orders[ref].price == 100


def test_retained_tightening_resumes_only_after_post_restart_full_evidence():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 2, Bracket(stop=90))
    ref = w.broker.lots[lot].protection["stop"]
    crash_once(w.kernel, "modify", "planned")
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=95), w.now)
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    assert w.broker.orders[ref].price == 90
    w.advance(MIN)
    w.snap("MGC")
    assert w.broker.orders[ref].price == 95


@pytest.mark.parametrize("writes", [1, 2])
def test_first_attach_store_write_retains_its_effect_for_restart(writes):
    w = make_world()
    lot = fill_lot(w, "dj30_mym_p250", 1)
    w.kernel.store = CutStore(w.kernel.store.data, writes)
    with pytest.raises(Crash):
        w.kernel.amend(lot, Bracket(stop=90), w.now)
    Sequence.start(w).restart()
    w.kernel.progress(w.now)
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MYM"] == 1
    ref = w.broker.lots[lot].protection["stop"]
    assert w.broker.orders[ref].price == 90
    assert w.kernel.expected[lot].status == {"stop": "working"}
    assert w.kernel.reconcile_restart(w.now).ok


@pytest.mark.parametrize("bracket", [Bracket(trail_activation_ticks=40),
                                     Bracket(trail_offset_ticks=20),
                                     Bracket(stop=90, trail_activation_ticks=40)])
@pytest.mark.parametrize("route", ["entry", "attach", "amend"])
def test_incomplete_trailing_bracket_is_refused_before_changing_protection(bracket, route):
    w = make_world()
    if route == "entry":
        result = w.kernel.admit_entry(entry("vanguard_mgc", 1, bracket), w.now)
        assert not result.ok
        assert not w.broker.orders
        assert w.kernel.ledger.reserved.get("vanguard_mgc", 0) == 0
    else:
        leg = "dj30_mym_p250" if route == "attach" else "vanguard_mgc"
        lot = fill_lot(w, leg, 1, None if route == "attach" else Bracket(stop=85))
        before = dict(w.kernel.expected[lot].intended)
        result = w.kernel.amend(lot, bracket, w.now)
        assert not result.ok
        assert w.kernel.expected[lot].intended == before
        assert not [e for e in w.broker.log if e["event"] in ("attach", "modify")]
        w.advance(MIN)
        w.snap()
        assert w.kernel.lots[lot].qty == 1
        assert "protection_gap" not in w.kernel.blocks


@pytest.mark.parametrize("field,value", [("qty", 99), ("side", "sell"), ("kind", "flat"),
                                        ("order_type", "limit"), ("price", 111),
                                        ("attached_to", "unowned-lot")])
def test_known_entry_ref_with_changed_risk_fields_blocks_admission(field, value):
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1, order_type="stop", price=110), w.now)
    setattr(w.broker.orders[d.ref], field, value)
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok


@pytest.mark.parametrize("observe_drift", [False, True])
@pytest.mark.parametrize("reboot", [False, True])
def test_known_ref_overfill_is_owned_without_exceeding_its_reservation(observe_drift, reboot):
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].qty = 99
    if observe_drift:
        w.advance(MIN)
        w.snap()
    if reboot:
        Sequence.start(w).restart()
    w.broker.fill(d.ref)
    w.advance(MIN)
    w.snap()  # the evidence handler must not throw on a broker-side overfill
    assert w.kernel.risk_add_blocked
    assert not w.kernel.admit_entry(entry("dj30_mym_p250", 1), w.now).ok
    assert w.kernel.ledger.confirmed.get("vanguard_mgc", 0) <= 1
    assert w.kernel.ledger.reserved.get("vanguard_mgc", 0) >= 0
    assert w.broker.positions["MGC"] == 99


def test_one_order_cannot_spend_its_siblings_reservation():
    w = make_world()
    a = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    b = w.kernel.admit_entry(entry("vanguard_mgc", 2), w.now)
    w.broker.orders[a.ref].qty = 2
    w.broker.fill(a.ref)
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.confirmed.get("vanguard_mgc", 0) == 0
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 2
    assert w.kernel.pending[b.ref].reserved == 2
    w.broker.fill(b.ref)
    w.advance(MIN)
    w.snap()
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 2
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 0
    assert w.kernel.risk_add_blocked


@pytest.mark.parametrize("reboot", [False, True])
def test_terminal_order_cannot_reopen_and_grow_allocation(reboot):
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 1)
    ref = w.kernel.lots[lot].entry_ref
    if reboot:
        Sequence.start(w).restart()
    w.broker.orders[ref].qty = 99
    w.broker.orders[ref].status = "partial"
    w.broker.fill(ref)
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 1
    assert w.kernel.lots[lot].qty == 1
    assert w.broker.positions["MGC"] == 99


@pytest.mark.parametrize("field,value", [("side", "sell"), ("leg_id", "external"),
                                        ("kind", "flat"), ("price", 111)])
def test_change_fill_restore_cannot_fabricate_an_owned_fill(field, value):
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    order = w.broker.orders[d.ref]
    old = getattr(order, field)
    setattr(order, field, value)
    w.broker.fill(d.ref)
    setattr(order, field, old)
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.confirmed.get("vanguard_mgc", 0) == 0
    assert not [e for e in w.kernel.telemetry if e["kind"] == "fill"]


def test_quarantine_survives_restore_and_restart_until_terminal_recovery():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].side = "sell"
    w.advance(MIN)
    w.snap()
    w.broker.orders[d.ref].side = "buy"
    Sequence.start(w).restart()
    w.advance(MIN)
    w.snap()
    w.kernel.reconcile_restart(w.now)
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 1
    assert w.kernel.cancel(d.ref, w.now).ok
    w.advance(MIN)
    w.snap()
    w.kernel.reconcile_restart(w.now)
    assert "unknown_order" not in w.kernel.blocks
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 0


def test_partial_drift_cannot_assign_ambiguous_residual_to_the_verified_lot():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 3), w.now)
    lot = w.broker.fill(d.ref, 1)
    w.advance(MIN)
    w.snap()
    w.broker.orders[d.ref].qty = 99
    w.broker.fill(d.ref)
    w.broker.close(sym="MGC", qty=98)
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 1
    # Matching net quantity does not prove which execution remains.
    w.broker.close(sym="MGC")
    w.advance(MIN)
    w.snap()
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 0
    assert "unknown_order" not in w.kernel.blocks


def test_cancel_quarantined_order_uses_current_kind_and_preserves_open_protection():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 1)
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].kind = "stop"
    w.broker.orders[d.ref].attached_to = lot
    w.advance(MIN)
    w.snap()
    assert not w.kernel.cancel(d.ref, w.now).ok
    assert w.broker.orders[d.ref].status == "working"


def test_unfilled_drift_cancel_can_resolve_beside_an_unrelated_owned_lot():
    w = make_world()
    fill_lot(w, "vanguard_mgc", 1)
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].qty = 99
    w.advance(MIN)
    w.snap()
    assert w.kernel.cancel(d.ref, w.now).ok
    w.advance(MIN)
    w.snap()
    assert not w.kernel.risk_add_blocked
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 1
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 0


def test_missing_execution_history_cannot_clear_quarantine_after_liquidation():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].qty = 99
    w.broker.fill(d.ref)
    w.advance(MIN)
    w.snap()
    w.broker.close(sym="MGC")
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(replace(ev, executions=()))
    assert "unknown_order" in w.kernel.blocks
    w.advance(MIN)
    w.snap()
    assert "unknown_order" not in w.kernel.blocks


def test_same_timestamp_terminal_mismatch_retains_reserve_until_postdating_read():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].qty = 99
    w.broker.fill(d.ref)
    w.snap()
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 1
    w.advance(MIN)
    w.snap()
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 0


def test_dry_run_read_does_not_create_phantom_order_mismatch():
    w = make_world()
    w.kernel.dry_run = True
    assert w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now).ok
    w.advance(MIN)
    w.snap()
    assert "unknown_order" not in w.kernel.blocks


def test_foreign_symbol_order_does_not_resolve_as_an_original_symbol_absence():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].sym = "MNQ"
    w.advance(BAR + MIN)
    w.snap("MGC")  # absence at the original symbol is not absence of this ref
    assert w.kernel.pending[d.ref].reserved == 1
    w.snap("MNQ")
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 1
    assert w.kernel.risk_add_blocked
    assert w.kernel.cancel(d.ref, w.now).ok
    w.advance(MIN)
    w.snap()
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 0
    assert "unknown_order" not in w.kernel.blocks


def test_rewritten_execution_identity_cannot_replace_previously_trusted_history():
    w = make_world()
    fill_lot(w, "vanguard_mgc", 1)
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    bad = tuple(replace(e, side="sell") for e in ev.executions)
    w.kernel.apply_evidence(replace(ev, executions=bad))
    assert w.kernel.risk_add_blocked
    w.broker.close(sym="MGC")
    w.advance(MIN)
    w.kernel.apply_evidence(replace(w.broker.snapshot("MGC"), executions=bad))
    assert "unknown_order" in w.kernel.blocks


def test_cancelled_status_with_working_remainder_does_not_release_quarantined_reserve():
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 1), w.now)
    w.broker.orders[d.ref].qty = 99
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(replace(ev, order_status={d.ref: "cancelled"}))
    assert w.kernel.risk_add_blocked
    assert w.kernel.ledger.reserved["vanguard_mgc"] == 1
    assert w.kernel.pending[d.ref].reserved == 1


@pytest.mark.parametrize("field,value", [("side", "sell"), ("sym", "MNQ")])
def test_native_recovery_consumes_the_actual_executions_after_partial_identity_drift(field, value):
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 3), w.now)
    w.broker.fill(d.ref, 1)
    w.advance(MIN)
    w.snap()
    setattr(w.broker.orders[d.ref], field, value)
    w.broker.fill(d.ref)
    w.advance(MIN)
    w.snap()
    assert w.kernel.risk_add_blocked
    w.kernel.close("sym", "MGC", w.now, "attended_external_recovery")
    if field == "sym":
        assert w.broker.positions["MNQ"] == 2
        w.kernel.close("sym", "MNQ", w.now, "attended_external_recovery")
    w.advance(MIN)
    w.snap()
    assert w.broker.positions["MGC"] == 0
    assert w.broker.positions.get("MNQ", 0) == 0
    assert all(lot.qty == 0 for lot in w.broker.lots.values())
    assert w.kernel.ledger.confirmed["vanguard_mgc"] == 0


@pytest.mark.parametrize("route", ["partial", "bounded", "fill"])
def test_mixed_side_scope_cannot_partly_close_in_a_way_that_increases_net_exposure(route):
    w = make_world()
    d = w.kernel.admit_entry(entry("vanguard_mgc", 3), w.now)
    lot = w.broker.fill(d.ref, 1)
    w.broker.orders[d.ref].side = "sell"
    w.broker.fill(d.ref)
    payload = {"sym": "MGC"}
    if route == "partial":
        w.broker.inject["close"] = ("partial", 1)
    elif route == "bounded":
        payload["qty"] = 1
    else:
        payload["fill_id"] = lot
    result = w.broker.close(**payload)
    assert result.status == "rejected"
    assert w.broker.positions["MGC"] == -1
    assert sum(l.qty for l in w.broker.lots.values()) == 3
    assert w.broker.close(sym="MGC").status == "accepted"
    assert w.broker.positions["MGC"] == 0


def test_later_identity_conflict_survives_an_earlier_quarantine_and_restored_history():
    w = make_world()
    lot = fill_lot(w, "vanguard_mgc", 1)
    ref = w.kernel.lots[lot].entry_ref
    w.broker.orders[ref].qty = 99
    w.advance(MIN)
    w.snap()
    w.advance(MIN)
    ev = w.broker.snapshot("MGC")
    w.kernel.apply_evidence(replace(ev, executions=tuple(replace(e, side="sell")
                                                       for e in ev.executions)))
    Sequence.start(w).restart()
    w.broker.orders[ref].qty = 1
    w.broker.close(sym="MGC")
    w.advance(MIN)
    w.snap()
    assert "unknown_order" in w.kernel.blocks
