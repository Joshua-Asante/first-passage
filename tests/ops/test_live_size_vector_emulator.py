"""P-L3: the offline bundle emulator sizes with the per-leg LegSize (card §4 LE1-LE7).

Synthetic sizes only; no screened vector value appears here.
"""
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from fractions import Fraction

import pytest

from c1_rail.book_policy import (
    BOOK_LEGS, TIER_MULTIPLIER, AddsRule, LegSize, _identity_ladder, add_quantity,
    candidate_book_protection_policy, entry_quantities, leg, validate_size_vector,
)
from c1_rail.book_sizing_context import (
    BookAccountContext, BookExposure, BookSession, BookSizingBinding,
    BookSizingRequest, SettledClose, size_book_request,
)
from c1_signal_daemon.book_bundle_execution import BundleExecution, SizingInputs
from c1_signal_daemon.book_bundle_intake import validate
from c1_signal_daemon.book_protocol import ExecutionEvent, Fill, FillTiming, Mode, OrderIntent
from c1_signal_daemon.feed import Bar

NOW = datetime(2026, 9, 14, 15, tzinfo=timezone.utc)
BAR = Bar(NOW, 100, 101, 99, 100)
POLICY = candidate_book_protection_policy()
LEGS = [spec.leg_id for spec in BOOK_LEGS]
MODES = (Mode.NORMAL, Mode.PROTECTED)
SYNTHETIC = validate_size_vector({
    "aegis_6j": {"base": 3, "adds": "UNCHANGED"},
    "dj30_mym_p250": {"risk_multiplier": "1/3", "cap_reserve_multiplier": "1/1", "adds": "UNCHANGED"},
    "vanguard_mgc": {"base_by_port": {"1": 1, "2": 0}, "adds": "UNCHANGED"},
    "orb_mnq_v7": {"base": 0, "adds": "UNCHANGED"},
})


class Source:
    def __init__(self, leg_id):
        self.leg_id = leg_id
        self.events = []

    def on_execution(self, event):
        self.events.append(event)

    def checkpoint(self):
        return {}


def emulator(leg_id, size, *, mode=Mode.NORMAL, tier="AUTHORIZED", inputs=None, cap_alloc=80):
    inputs = inputs or {}
    source = Source(leg_id)
    sizing = SizingInputs(leg_id, mode, tier, inputs.get("cap_alloc", cap_alloc),
                          Fraction(inputs.get("risk_dollars", 700)), 1, size=size)
    return BundleExecution(source, sizing, policy=POLICY), source


def order(leg_id, kind, inputs=None, oid=None):
    inputs = inputs or {}
    return OrderIntent(oid or kind, leg_id, kind, leg(leg_id).entry_side,
                       inputs.get("normal_base", leg(leg_id).normal_base_values[0]),
                       timing=FillTiming.THIS_CLOSE, stop_dist_pts=inputs.get("per_contract_risk", 10),
                       bar_time=NOW)


def admitted(execution, source, action):
    out = execution.admit([action], BAR)
    if not out:
        assert source.events[-1].detail == "shared_sizing_zero"
        assert execution.checkpoint()["pending"] == {}
        return 0
    return out[0].qty


def confirm(execution, leg_id, qty):
    fill = Fill("f-base", "entry", leg_id, "entry", leg(leg_id).entry_side, qty, 100, NOW, commission=0)
    execution.on_execution(ExecutionEvent("fill", leg_id, NOW, fill=fill, order_id="entry"))


def entry_law(leg_id, mode, tier, inputs, size):
    return entry_quantities(leg_id, mode=mode, policy=POLICY, lifecycle_tier=tier,
                            normal_base=inputs.get("normal_base"),
                            risk_dollars=Fraction(inputs.get("risk_dollars", 700)),
                            per_contract_risk=Fraction(inputs.get("per_contract_risk", 10)),
                            cap_alloc=inputs.get("cap_alloc", 80), size=size)[0]


def live(leg_id, mode, tier, inputs, size):
    """P-L1's size_book_request for the same inputs (its own LS harness shape)."""
    spec = leg(leg_id)
    session = BookSession("session-2", "session-1", NOW - timedelta(hours=1),
                          NOW + timedelta(hours=1), NOW + timedelta(hours=2), "a" * 64)
    settled = SettledClose("session-1", NOW - timedelta(days=1),
                           99000 if mode is Mode.PROTECTED else 100000, 100000, "d" * 64)
    binding = BookSizingBinding("synthetic-account", "boot-2", "b" * 64, "c" * 64, settled,
                                session, timedelta(seconds=30), leg_id, "SYNTHETIC-" + spec.symbol,
                                inputs.get("cap_alloc", 80),
                                Fraction(inputs.get("risk_dollars", 700)), size=size)
    context = BookAccountContext(
        "synthetic-account", "boot-2", "op-2", leg_id, binding.order_symbol, "session-2", mode,
        "b" * 64, "c" * 64, "a" * 64, settled, spec.lifecycle_key, tier, NOW,
        NOW + timedelta(seconds=30), 0, 0, None,
        tuple(BookExposure(item.leg_id, 0, 0) for item in BOOK_LEGS), (), ())
    request = BookSizingRequest("op-2", leg_id, binding.order_symbol, "entry",
                                inputs.get("normal_base"),
                                Fraction(inputs.get("per_contract_risk", 10)))
    decision = size_book_request(request, context=context, binding=binding, policy=POLICY, now=NOW)
    assert not decision.halt, decision.halt_reason
    return decision.qty_out


def cases(leg_id):
    # The emulator refuses a zero allocation at construction, so the ladder's a=0 row is excluded.
    for tier in TIER_MULTIPLIER:
        for mode in MODES:
            for inputs in _identity_ladder(leg_id):
                if inputs.get("cap_alloc", 80) > 0:
                    yield mode, tier, inputs


@pytest.mark.parametrize("leg_id", LEGS)
def test_le1_none_is_todays_entry_and_add(leg_id):
    for mode, tier, inputs in cases(leg_id):
        execution, source = emulator(leg_id, None, mode=mode, tier=tier, inputs=inputs)
        qty = admitted(execution, source, order(leg_id, "entry", inputs))
        assert qty == entry_law(leg_id, mode, tier, inputs, None)
        if qty:
            confirm(execution, leg_id, qty)
            assert admitted(execution, source, order(leg_id, "add", inputs)) == add_quantity(
                leg_id, qty, mode=mode, policy=POLICY, lifecycle_tier=tier)


@pytest.mark.parametrize("leg_id", LEGS)
def test_le2_three_way_parity_with_live_context_and_replay_law(leg_id):
    size = SYNTHETIC.leg(leg_id)
    differs = False
    for mode, tier, inputs in cases(leg_id):
        execution, source = emulator(leg_id, size, mode=mode, tier=tier, inputs=inputs)
        emulated = admitted(execution, source, order(leg_id, "entry", inputs))
        assert emulated == live(leg_id, mode, tier, inputs, size) == entry_law(
            leg_id, mode, tier, inputs, size)
        differs |= emulated != entry_law(leg_id, mode, tier, inputs, None)
    assert differs, f"{leg_id}: synthetic size never changes an emulated entry"


@pytest.mark.parametrize("mode", MODES)
def test_le3_size_reaches_add_law(mode):
    unchanged = SYNTHETIC.leg("dj30_mym_p250")
    inputs = dict(risk_dollars=100, per_contract_risk=10, cap_alloc=80)
    for size in (replace(unchanged, adds=AddsRule.OFF), unchanged):
        execution, source = emulator("dj30_mym_p250", size, mode=mode, inputs=inputs)
        base = admitted(execution, source, order("dj30_mym_p250", "entry", inputs))
        assert base > 0
        confirm(execution, "dj30_mym_p250", base)
        add = execution.admit([order("dj30_mym_p250", "add", inputs)], BAR)
        if size.adds is AddsRule.OFF:
            assert add == [] and source.events[-1].detail == "shared_sizing_zero"
        else:
            assert add[0].qty == add_quantity("dj30_mym_p250", base, mode=mode, policy=POLICY,
                                              lifecycle_tier="AUTHORIZED", size=size) > 0


@pytest.mark.parametrize("mode", MODES)
def test_le4_leg_at_zero_emits_no_order(mode):
    execution, source = emulator("aegis_6j", LegSize("aegis_6j", base=0), mode=mode)
    assert execution.admit([order("aegis_6j", "entry")], BAR) == []
    assert source.events[-1].detail == "shared_sizing_zero"
    assert execution.checkpoint()["pending"] == {}


@pytest.mark.parametrize("size", [SYNTHETIC.leg("aegis_6j"), {"base": 3, "adds": "UNCHANGED"}])
def test_le5_mismatched_or_untyped_size_refused(size):
    with pytest.raises(ValueError, match="size_identity_mismatch"):
        emulator("dj30_mym_p250", size)


def test_le6_allocation_checks_the_sized_quantity():
    cap = 3 * leg("aegis_6j").micro_equiv
    execution, source = emulator("aegis_6j", None, cap_alloc=cap)
    with pytest.raises(ValueError, match="allocation_refusal"):
        execution.admit([order("aegis_6j", "entry")], BAR)
    execution, source = emulator("aegis_6j", SYNTHETIC.leg("aegis_6j"), cap_alloc=cap)
    assert admitted(execution, source, order("aegis_6j", "entry")) == 3


def test_le7_bundle_admission_refuses_a_size_key(tmp_path):
    manifest = {
        "schema": "book-bundle-v1", "bundle_id": "O-N", "leg_id": "orb_mnq_v7", "artifacts": {},
        "adapter_overrides": {"qty": 1}, "approved_deviations": [],
        "emulator_overrides": {"initial_capital": 100000, "margin_pct": .1,
                               "commission_per_side": .91, "slippage_ticks": 1,
                               "orders_on_close": True},
        "sizing": {"mode": "normal", "lifecycle_tier": "AUTHORIZED", "cap_alloc": 3,
                   "risk_dollars": 0, "pointvalue": 2},
        "chart_timezone": "America/New_York", "normalization_version": "tv_trade_ledger-v1",
        "window": {"start": "2022-09-01T00:00:00+00:00", "end": "2026-09-03T00:00:00+00:00"},
        "startup": {"kind": "cold_at_panel_origin", "first_bar": "2022-09-01T00:00:00+00:00",
                    "coverage_verdict": "PASS"},
        "verdicts": dict.fromkeys(("source_state", "normalization", "reconciliation",
                                   "coverage", "margin"), "PASS"),
    }
    # Control: without the key, validation passes the sizing checks and stops later.
    with pytest.raises(ValueError, match="missing_artifacts"):
        validate(manifest, tmp_path)
    manifest["sizing"]["size"] = {"base": 0, "adds": "UNCHANGED"}
    with pytest.raises(ValueError, match="incomplete_sizing_inputs"):
        validate(manifest, tmp_path)
