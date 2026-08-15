"""Tests for ops/c1_rail/c1_sizing_host_reference.py — the Python reference (oracle)
implementation of the frozen NT8 sizing-host spec.

Spec: docs/spec/c1_nt8_sizing_host_impl.md (B2, GO ADR 2026-07-17). The §7 test
plan is transcribed here as the executable suite; the NinjaScript port must
reproduce this module's outputs at the B6 dry-fire gate.

Oracle: lab/analysis/c1/q_rail_1_2026-07/f2_floors.json — the committed F2 floors.
The worked-check tests read that file directly so the suite is pinned to the
committed bytes, not to re-typed numbers.

Fail-safe doctrine under test (spec §5): any unreadable/malformed state input
=> qty_out=0, submit=False, halt=True. Never fail-open to a default multiplier.
"""

import json
import math
from pathlib import Path

import pytest

from c1_sizing_host_reference import (
    LEG_MAP,
    C1SizingHostReference,
    generate_constants,
)
from dd_protection import BASE_RISK, DD_SCALE, DD_TRIGGER, calculate_protection
from firm_rules import FIRM_RULES
from lifecycle import TIER_MULTIPLIER

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
F2_FLOORS = REPO_ROOT / "lab" / "analysis" / "c1" / "q_rail_1_2026-07" / "f2_floors.json"

TIER = "Tradeify_Select_100K"
E_FIRM = 100_000.0


# ── fixtures ─────────────────────────────────────────────────────────────────

def _write_json(path: Path, obj) -> Path:
    path.write_text(json.dumps(obj), encoding="utf-8")
    return path


@pytest.fixture
def state_dir(tmp_path):
    """A valid three-file state directory: WATCH-1 both legs, no DD."""
    _write_json(tmp_path / "lifecycle_state.json",
                {"Striker": "WATCH-1", "Striker NAS100": "WATCH-1"})
    _write_json(tmp_path / "c1_dd_state.json",
                {"account": TIER, "peak_equity": E_FIRM,
                 "last_updated_utc": "2026-07-17T20:00:00Z"})
    _write_json(tmp_path / "c1_sizing_constants.json", generate_constants(TIER))
    return tmp_path


def make_host(state_dir: Path) -> C1SizingHostReference:
    return C1SizingHostReference(
        lifecycle_state_path=state_dir / "lifecycle_state.json",
        dd_state_path=state_dir / "c1_dd_state.json",
        constants_path=state_dir / "c1_sizing_constants.json",
    )


def entry_payload(leg_id: str, stop_dist_pts: float) -> dict:
    return {"leg_id": leg_id, "signal_type": "entry",
            "bar_time": 1752778800000, "close": 44100.0,
            "stop_dist_pts": stop_dist_pts}


def add_payload(leg_id: str, stop_dist_pts: float) -> dict:
    return {"leg_id": leg_id, "signal_type": "add",
            "bar_time": 1752782400000, "close": 44200.0,
            "stop_dist_pts": stop_dist_pts}


# ── §7 Phase 1 — worked-check reproduction against the committed oracle ──────

def _oracle_rows():
    data = json.loads(F2_FLOORS.read_text(encoding="utf-8"))
    leg_ids = {"MYM": "dj30_mym", "MNQ": "nas100_mnq"}
    rows = []
    for leg in data["legs"]:
        for window in ("full_median", "recent_90d"):
            w = leg[window]
            rows.append(pytest.param(
                leg_ids[leg["symbol"]], w["sl_pts"],
                w["base_capped"], w["add_qty"],
                id=f"{leg['symbol']}-{window}",
            ))
    return rows


@pytest.mark.parametrize("leg_id,sl_pts,expected_base,expected_add", _oracle_rows())
def test_worked_check_reproduces_f2_floors(state_dir, leg_id, sl_pts,
                                           expected_base, expected_add):
    """Entry then add at WATCH-1/no-DD must reproduce f2_floors.json exactly."""
    host = make_host(state_dir)

    entry = host.process_signal(entry_payload(leg_id, sl_pts), current_equity=E_FIRM)
    assert not entry.halt, entry.halt_reason
    assert entry.submit
    assert entry.qty_out == expected_base
    host.confirm_executed_base(entry.leg_key, entry.qty_out)

    add = host.process_signal(add_payload(leg_id, sl_pts), current_equity=E_FIRM)
    assert not add.halt, add.halt_reason
    assert add.submit
    assert add.qty_out == expected_add


def test_worked_check_components_mym_recent(state_dir):
    """Spec §7 Phase 1 components, MYM recent-90d: r_eff/raw/reserve pinned."""
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert d.dd_scale == 1.0
    assert d.lifecycle_multiplier == 0.50
    assert d.r_eff == pytest.approx(0.0035)
    assert d.qty_base_raw == 11
    # reserve_cap derives from this leg's ALLOCATED share (69), not the whole
    # account cap (80) — account-aggregate semantics, re-pinned 2026-07-22.
    assert d.reserve_cap == 8
    assert d.qty_out == 8


def test_add_sized_off_executed_base_not_recomputed(state_dir):
    """Add uses the ACTUAL executed base qty even if state changed in between."""
    host = make_host(state_dir)
    entry = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    host.confirm_executed_base(entry.leg_key, entry.qty_out)
    # Lifecycle demotes between entry and add: add must still be 8-based.
    _write_json(state_dir / "lifecycle_state.json",
                {"Striker": "WATCH-2", "Striker NAS100": "WATCH-1"})
    add = host.process_signal(add_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert add.qty_out == 60  # floor(8 * 7.5), not re-derived at WATCH-2


def test_exit_clears_leg_state(state_dir):
    """Exit does not auto-clear confirmed base; operator clears after flat proof."""
    host = make_host(state_dir)
    entry = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    host.confirm_executed_base(entry.leg_key, entry.qty_out)
    ex = host.process_signal(
        {"leg_id": "dj30_mym", "signal_type": "exit", "bar_time": 1,
         "close": 44000.0, "stop_dist_pts": 12.0},
        current_equity=E_FIRM)
    assert not ex.halt
    assert not ex.submit
    assert ex.qty_out == 0
    # Exit alone leaves confirmed base — add still sizes off it until cleared.
    add_before_clear = host.process_signal(
        add_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert not add_before_clear.halt
    assert add_before_clear.qty_out == 60
    host.clear_executed_base(entry.leg_key)
    # After broker-confirmed flat + clear, add has no tracked base -> halt.
    add = host.process_signal(add_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert add.halt
    assert add.qty_out == 0


def test_flat_treated_like_exit(state_dir):
    host = make_host(state_dir)
    entry = host.process_signal(entry_payload("nas100_mnq", 54.6114), current_equity=E_FIRM)
    host.confirm_executed_base(entry.leg_key, entry.qty_out)
    fl = host.process_signal(
        {"leg_id": "nas100_mnq", "signal_type": "flat", "bar_time": 1,
         "close": 18000.0, "stop_dist_pts": 5.0},
        current_equity=E_FIRM)
    assert not fl.halt and not fl.submit and fl.qty_out == 0


def test_add_without_prior_entry_halts(state_dir):
    host = make_host(state_dir)
    add = host.process_signal(add_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert add.halt
    assert add.submit is False
    assert add.qty_out == 0


def test_add_halts_after_entry_until_confirmed_base(state_dir):
    """Entry alone does not seed executed base — add halts until confirm."""
    host = make_host(state_dir)
    entry = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert not entry.halt
    assert entry.qty_out == 8

    add_before = host.process_signal(add_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert add_before.halt
    assert add_before.qty_out == 0

    host.confirm_executed_base(entry.leg_key, entry.qty_out)
    add_after = host.process_signal(add_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert not add_after.halt
    assert add_after.qty_out == 60


# ── §7 Phase 3 — DD trigger (values corrected from the spec's draft numbers) ──

def test_dd_trigger_scales_quantity(state_dir):
    """peak=100000, equity=98500 -> dd exactly 1.5% -> DD_SCALE applies.

    MYM recent-90d at WATCH-1 + DD: r_eff = 0.0070*0.40*0.50 = 0.0014
    -> floor(140 / 30.41005) = 4 (0.40x the raw, NOT half — DD_SCALE is 0.40).
    """
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201),
                            current_equity=98_500.0)
    assert d.dd_scale == DD_SCALE
    assert d.r_eff == pytest.approx(0.0070 * 0.40 * 0.50)
    assert d.qty_out == 4


def test_dd_just_below_trigger_does_not_scale(state_dir):
    """dd 1.4997% rounds below the 1.5% trigger -> full WATCH-1 size."""
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201),
                            current_equity=98_500.31)
    assert d.dd_scale == 1.0
    assert d.qty_out == 8


def test_peak_ratchets_up_from_current_equity(state_dir):
    """Equity above stored peak ratchets the effective peak (no phantom DD)."""
    host = make_host(state_dir)
    # equity 2% above stored peak: dd must be 0, not negative/garbage
    d = host.process_signal(entry_payload("dj30_mym", 60.8201),
                            current_equity=102_000.0)
    assert d.dd_scale == 1.0
    assert d.qty_out == 8


def test_read_dd_scale_matches_calculate_protection(state_dir):
    """C5: rail ULP path is calculate_protection after the peak ratchet."""
    host = make_host(state_dir)
    cases = (
        98_500.0,    # exactly DD_TRIGGER
        98_500.31,   # just below trigger (ULP round)
        102_000.0,   # ratchet: effective_peak = equity
        E_FIRM,      # at peak
    )
    for equity in cases:
        effective_peak = max(E_FIRM, equity)
        expected = calculate_protection(equity, effective_peak)["multiplier"]
        assert host._read_dd_scale(equity) == expected


# ── lifecycle tier ladder behavior ───────────────────────────────────────────

def test_retired_tier_floors_to_zero_without_halt(state_dir):
    """RETIRED (0.0x) is a legitimate computed zero — floored, not a halt."""
    _write_json(state_dir / "lifecycle_state.json",
                {"Striker": "RETIRED", "Striker NAS100": "WATCH-1"})
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert not d.halt
    assert d.submit is False
    assert d.qty_out == 0
    assert d.floored


def test_watch2_composes(state_dir):
    """WATCH-2 (0.25x): floor(100000*0.0070*0.25 / 30.41005) = 5, under reserve."""
    _write_json(state_dir / "lifecycle_state.json",
                {"Striker": "WATCH-2", "Striker NAS100": "WATCH-1"})
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert d.lifecycle_multiplier == 0.25
    assert d.qty_out == 5


# ── §7 Phase 2 — fail-safe battery (spec §5: halt, never fail-open) ──────────

@pytest.mark.parametrize("missing", [
    "lifecycle_state.json", "c1_dd_state.json", "c1_sizing_constants.json",
])
def test_missing_state_file_halts(state_dir, missing):
    (state_dir / missing).unlink()
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert d.halt
    assert d.submit is False
    assert d.qty_out == 0
    assert missing in (d.halt_reason or "")


@pytest.mark.parametrize("corrupt", [
    "lifecycle_state.json", "c1_dd_state.json", "c1_sizing_constants.json",
])
def test_corrupt_state_file_halts(state_dir, corrupt):
    (state_dir / corrupt).write_text("{not json", encoding="utf-8")
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert d.halt
    assert d.qty_out == 0


def test_missing_lifecycle_key_halts_not_defaults(state_dir):
    """Spec §5: NO fall-through to AUTHORIZED for an unlisted leg (diverges
    from core/lifecycle.py's read-only-surface default, by design)."""
    _write_json(state_dir / "lifecycle_state.json", {"Striker NAS100": "WATCH-1"})
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert d.halt
    assert d.qty_out == 0


def test_unknown_tier_string_halts(state_dir):
    _write_json(state_dir / "lifecycle_state.json",
                {"Striker": "PROMOTED-2X", "Striker NAS100": "WATCH-1"})
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 60.8201), current_equity=E_FIRM)
    assert d.halt
    assert d.qty_out == 0


def test_unknown_leg_id_halts(state_dir):
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("guardian_mgc", 10.0), current_equity=E_FIRM)
    assert d.halt
    assert d.qty_out == 0


def test_unknown_signal_type_halts(state_dir):
    host = make_host(state_dir)
    d = host.process_signal(
        {"leg_id": "dj30_mym", "signal_type": "rebalance", "bar_time": 1,
         "close": 44100.0, "stop_dist_pts": 60.0},
        current_equity=E_FIRM)
    assert d.halt
    assert d.qty_out == 0


def test_missing_payload_field_halts(state_dir):
    host = make_host(state_dir)
    d = host.process_signal(
        {"leg_id": "dj30_mym", "signal_type": "entry", "bar_time": 1,
         "close": 44100.0},  # stop_dist_pts absent
        current_equity=E_FIRM)
    assert d.halt
    assert d.qty_out == 0


def test_nonpositive_stop_dist_floors_to_zero(state_dir):
    """per_contract <= 0 -> qty 0 (spec §2.2), no order, no crash."""
    host = make_host(state_dir)
    d = host.process_signal(entry_payload("dj30_mym", 0.0), current_equity=E_FIRM)
    assert not d.halt
    assert d.submit is False
    assert d.qty_out == 0


# ── constants mirror integrity (the M-9-shaped audit, as a test) ─────────────

def test_generated_constants_match_production_sources():
    c = generate_constants(TIER)
    firm = FIRM_RULES[TIER]
    assert c["tier"] == TIER
    assert c["E_firm"] == firm["starting_balance"]
    assert c["cap_firm"] == firm["micro_contract_cap"]
    assert c["cost_per_side_usd"] == firm["cost_per_side_usd"]
    for leg_id, leg in LEG_MAP.items():
        row = c["leg_map"][leg_id]
        assert row["leg_key"] == leg["leg_key"]
        assert row["base_risk"] == BASE_RISK[leg["leg_key"]]
        assert row["pyr_pct"] == leg["pyr_pct"]
        assert row["dollars_per_pt"] == leg["dollars_per_pt"]


def test_leg_map_matches_spec_table():
    """Spec §2.1 pinned verbatim."""
    assert LEG_MAP["dj30_mym"]["leg_key"] == "Striker"
    assert LEG_MAP["dj30_mym"]["pyr_pct"] == 750.0
    assert LEG_MAP["dj30_mym"]["dollars_per_pt"] == 0.50
    assert LEG_MAP["nas100_mnq"]["leg_key"] == "Striker NAS100"
    assert LEG_MAP["nas100_mnq"]["pyr_pct"] == 1000.0
    assert LEG_MAP["nas100_mnq"]["dollars_per_pt"] == 2.00


def test_ladder_and_dd_constants_come_from_production():
    """The reference must consume production constants, not re-type them."""
    assert TIER_MULTIPLIER["WATCH-1"] == 0.50
    assert DD_TRIGGER == 0.015
    assert DD_SCALE == 0.40
    # reserve caps derive from locked pyramid ratios AND the per-leg cap
    # allocation (NOT the whole account cap — see test_combined_position_*)
    assert math.floor(69 / (1 + 750.0 / 100)) == 8
    assert math.floor(11 / (1 + 1000.0 / 100)) == 1


# --- account-aggregate contract cap (2026-07-22) --------------------------
# Tradeify's limit is per ACCOUNT, not per instrument: "Your combined position
# must stay within your account's contract limit, counted at 10 micros = 1 mini"
# (article 10495868). MFFU states the consequence outright — over-cap "can
# result in a BREACH of the trading account" (article 13286542).


def test_cap_alloc_sums_to_account_cap():
    """The split must allocate exactly the account cap — no over/under-commit."""
    firm = FIRM_RULES["Tradeify_Select_100K"]
    assert sum(leg["cap_alloc"] for leg in LEG_MAP.values()) == firm[
        "micro_contract_cap"
    ]


def test_combined_max_position_within_account_cap():
    """THE invariant this split exists to enforce.

    Worst case = every leg simultaneously at its capped base plus a full
    pyramid add. Before the 2026-07-22 split each leg got the full 80, giving
    MYM 76 + MNQ 77 = 153 micros against an 80 limit (1.91x).
    """
    cap_firm = FIRM_RULES["Tradeify_Select_100K"]["micro_contract_cap"]
    combined = 0
    for leg in LEG_MAP.values():
        pyr = leg["pyr_pct"]
        base = math.floor(leg["cap_alloc"] / (1 + pyr / 100))
        combined += base + math.floor(base * pyr / 100)
    assert combined <= cap_firm, (
        f"combined worst-case {combined} micros exceeds account cap {cap_firm}"
    )


def test_no_leg_alone_exceeds_account_cap():
    for leg_id, leg in LEG_MAP.items():
        assert leg["cap_alloc"] <= FIRM_RULES["Tradeify_Select_100K"][
            "micro_contract_cap"
        ], leg_id


def test_missing_cap_alloc_halts_rather_than_defaulting(state_dir):
    """Fail-safe doctrine: a state defect halts; it never falls back to the
    permissive whole-account cap (which would restore the 1.91x breach)."""
    host = make_host(state_dir)
    path = state_dir / "c1_sizing_constants.json"
    constants = json.loads(path.read_text(encoding="utf-8"))
    del constants["leg_map"]["dj30_mym"]["cap_alloc"]
    path.write_text(json.dumps(constants), encoding="utf-8")
    d = host.process_signal(entry_payload("dj30_mym", 60.8201),
                            current_equity=E_FIRM)
    assert d.halt is True
    assert d.qty_out == 0
    assert d.submit is False
    assert "cap_alloc" in (d.halt_reason or "")
