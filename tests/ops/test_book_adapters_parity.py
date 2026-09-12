"""Parity of the four private fixed-book adapters against their captured TradingView
exports, and their behaviour at the protected sizes / ORB adds-off mode (Track B
TB-A1..A4 acceptance; umbrella wave-2 gate).

Everything here needs private inputs (gitignored ports, the reconstructed
effective-input file, the frozen CME panels, the captured exports); each test
skips with the missing input named when they are absent (public clone, CI, bare
worktree). Tracked assertions are counts and structural facts only.
"""
from __future__ import annotations

import math

import pytest

from book_policy import candidate_book_protection_policy, leg, leg_quantities
from c1_signal_daemon.book_adapters import ADAPTERS, ADAPTER_BY_LEG, load_port, port_available
from c1_signal_daemon.book_parity import (
    bar_data_dir, load_effective_inputs, load_panel, locate_export, parity_for, run_leg,
)
from c1_signal_daemon.book_protocol import Mode

POLICY = candidate_book_protection_policy()
LEGS = [a.leg_id for a in ADAPTERS]
_PANELS: dict[str, list] = {}


def _missing(leg_id: str) -> str | None:
    eff = load_effective_inputs()
    if eff is None or leg_id not in eff:
        return "effective_inputs.json absent from the port root"
    if not port_available(leg_id):
        return f"private port for {leg_id} absent"
    spec = ADAPTER_BY_LEG[leg_id]
    if not (bar_data_dir() / f"{spec.symbol}_M15.csv").is_file():
        return f"{spec.symbol} panel absent"
    try:
        locate_export(leg_id)
    except (FileNotFoundError, ValueError) as exc:
        return f"export unavailable: {exc}"
    return None


def _require(leg_id: str) -> dict:
    reason = _missing(leg_id)
    if reason:
        pytest.skip(reason)
    return load_effective_inputs()[leg_id]


def _bars(leg_id: str):
    sym = ADAPTER_BY_LEG[leg_id].symbol
    if sym not in _PANELS:
        _PANELS[sym] = load_panel(sym)
    return _PANELS[sym]


def _trades(emu):
    return sorted((t.entry.bar_time, t.exit.bar_time, t.entry.price, t.exit.price, t.entry.qty, t.entry.kind)
                  for t in emu.closed_trades)


# ── pins ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("leg_id", LEGS)
def test_port_declares_its_leg_and_pine_pin(leg_id):
    if not port_available(leg_id):
        pytest.skip(f"private port for {leg_id} absent")
    mod = load_port(leg_id)
    assert mod.LEG_ID == leg_id
    assert mod.PINE_SHA256 == ADAPTER_BY_LEG[leg_id].pine_sha256 == leg(leg_id).pine_sha256


# ── parity at the captured settings ───────────────────────────────────────

@pytest.mark.parametrize("leg_id", LEGS)
def test_parity_with_captured_export_is_exact(leg_id):
    eff = load_effective_inputs()
    _require(leg_id)
    rep = parity_for(leg_id, eff)
    assert rep.passed, rep.summary()
    assert rep.matched == rep.export_trades > 0


# ── protected sizes (TB-S1 (C), D-B10) ───────────────────────────────────

def test_aegis_protected_size_three_with_identical_signals_under_the_fixed_law():
    cfg = _require("aegis_6j")
    bars = _bars("aegis_6j")
    common = dict(adapter_overrides=cfg["adapter"], emulator_overrides=cfg["emulator"], bars=bars)
    _, normal, _ = run_leg("aegis_6j", quantity_rule=lambda n: (8, 0), **common)
    _, protected, _ = run_leg("aegis_6j", mode=Mode.PROTECTED,
                              quantity_rule=lambda n: leg_quantities("aegis_6j", 8, mode=Mode.PROTECTED, policy=POLICY),
                              **common)
    n, p = _trades(normal), _trades(protected)
    assert len(n) == len(p) > 0
    assert [t[:4] for t in n] == [t[:4] for t in p]          # same entry/exit bars and prices
    assert {t[4] for t in n} == {8} and {t[4] for t in p} == {3}


def test_striker_protected_sizes_floor_each_tier_from_its_normal_value():
    cfg = _require("dj30_mym_p250")
    bars = _bars("dj30_mym_p250")
    common = dict(adapter_overrides=cfg["adapter"], emulator_overrides=cfg["emulator"], bars=bars)
    _, normal, _ = run_leg("dj30_mym_p250", **common)
    _, protected, _ = run_leg(
        "dj30_mym_p250", mode=Mode.PROTECTED,
        quantity_rule=lambda n: leg_quantities("dj30_mym_p250", n, mode=Mode.PROTECTED, policy=POLICY),
        **common)
    # Every protected fill is checked against the exact floor of the normal tier the adapter
    # sized from — including entries the full-size run never took (the leg's own realised P&L
    # drives its day soft-stop, so a 40 % book can trade where 100 % halted). The adapter
    # records its normal tier (`initial_size`) when it places an order; a THIS_CLOSE order fills
    # on the same bar, so (bar, kind) keys the expectation exactly.
    from c1_signal_daemon.book_protocol import OrderIntent
    expected = {}

    def instrument(adapter):
        orig = adapter.on_bar

        def on_bar(bar):
            actions = orig(bar)
            for a in actions:
                if isinstance(a, OrderIntent) and a.kind in ("entry", "add"):
                    base, add = leg_quantities("dj30_mym_p250", adapter.initial_size,
                                               mode=Mode.PROTECTED, policy=POLICY)
                    expected[(bar.ts, a.kind)] = base if a.kind == "entry" else add
            return actions
        adapter.on_bar = on_bar

    _, protected, _ = run_leg(
        "dj30_mym_p250", mode=Mode.PROTECTED,
        quantity_rule=lambda n: leg_quantities("dj30_mym_p250", n, mode=Mode.PROTECTED, policy=POLICY),
        adapter_hook=instrument, **common)
    seen = set()
    for t in protected.closed_trades:
        if t.entry.fill_id in seen:
            continue                         # a lot closed in parts appears once per part
        seen.add(t.entry.fill_id)
        want = expected[(t.entry.bar_time, t.entry.kind)]
        assert t.entry.qty == want, (t.entry.bar_time, t.entry.kind, t.entry.qty, want)
    assert len(seen) == len(expected) > 0
    assert max(t.entry.qty for t in protected.closed_trades if t.entry.kind == "entry") <= 8


def test_vanguard_protected_places_nothing_and_watch1_places_one():
    cfg = _require("vanguard_mgc")
    bars = _bars("vanguard_mgc")
    common = dict(adapter_overrides=cfg["adapter"], emulator_overrides=cfg["emulator"], bars=bars)
    _, normal, _ = run_leg("vanguard_mgc", **common)
    _, protected, _ = run_leg(
        "vanguard_mgc", mode=Mode.PROTECTED,
        quantity_rule=lambda n: leg_quantities("vanguard_mgc", n, mode=Mode.PROTECTED, policy=POLICY), **common)
    assert len(normal.closed_trades) > 0 and len(protected.closed_trades) == 0
    _, watch1, _ = run_leg(
        "vanguard_mgc",
        quantity_rule=lambda n: leg_quantities("vanguard_mgc", n, mode=Mode.NORMAL, policy=POLICY,
                                               lifecycle_tier="WATCH-1"), **common)
    assert {t.entry.qty for t in watch1.closed_trades} <= {1}
    assert len(watch1.closed_trades) > 0


# ── ORB adds-off (selection note: base one micro, adds disabled) ─────────

def test_orb_adds_off_mode_equals_pine_scale_in_disabled_and_keeps_base_entries():
    cfg = _require("orb_mnq_v7")
    bars = _bars("orb_mnq_v7")
    rail_emu = dict(cfg["emulator"], margin_pct=0.0)     # the live account has no TradingView margin check
    base_adapter = dict(cfg["adapter"], qty=1)
    _, normal, _ = run_leg("orb_mnq_v7", adapter_overrides=base_adapter, emulator_overrides=rail_emu, bars=bars)
    _, protected, _ = run_leg("orb_mnq_v7", mode=Mode.PROTECTED, adapter_overrides=base_adapter,
                              emulator_overrides=rail_emu, bars=bars)
    _, pine_off, _ = run_leg("orb_mnq_v7", adapter_overrides=dict(base_adapter, use_scale_in=False),
                             emulator_overrides=rail_emu, bars=bars)
    assert _trades(protected) == _trades(pine_off)                 # adds-off == Pine useScaleIn=false
    assert all(t.entry.kind == "entry" for t in protected.closed_trades)
    assert not any(t.exit.reason == "Stall exit" for t in protected.closed_trades)
    assert any(t.entry.kind == "add" for t in normal.closed_trades)
    assert any(t.exit.reason == "Stall exit" for t in normal.closed_trades)
    normal_bases = {(t.entry.bar_time, t.entry.price) for t in normal.closed_trades if t.entry.kind == "entry"}
    protected_bases = {(t.entry.bar_time, t.entry.price) for t in protected.closed_trades}
    assert protected_bases == normal_bases                         # base entries unchanged
    assert {t.entry.qty for t in protected.closed_trades} == {1}
    # exits differ once adds are off (average price, trailing, stall) — record, never assume
    normal_exits = {(t.entry.bar_time, t.exit.bar_time) for t in normal.closed_trades if t.entry.kind == "entry"}
    protected_exits = {(t.entry.bar_time, t.exit.bar_time) for t in protected.closed_trades}
    assert len(protected_exits - normal_exits) > 0


def test_orb_rail_size_one_micro_with_one_micro_adds():
    cfg = _require("orb_mnq_v7")
    bars = _bars("orb_mnq_v7")
    _, emu, _ = run_leg("orb_mnq_v7", adapter_overrides=dict(cfg["adapter"], qty=1),
                        emulator_overrides=dict(cfg["emulator"], margin_pct=0.0), bars=bars)
    assert {t.entry.qty for t in emu.closed_trades} == {1}
    assert sum(1 for t in emu.closed_trades if t.entry.kind == "add") > 0
    assert emu.rejected == []
