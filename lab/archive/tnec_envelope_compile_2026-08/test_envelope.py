"""Campaign-local tests. Run from repo root:
   python -X utf8 -m pytest lab/archive/tnec_envelope_compile_2026-08/test_envelope.py -v
"""
import json
import os
import subprocess
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import instruments  # noqa: E402


def test_pool_membership_and_order():
    assert list(instruments.POOL) == ["MNQ", "MYM", "MES", "MGC", "M2K", "MCL", "M6A"]


def test_specs_import_live_not_transcribed():
    # The five cost_model-covered symbols must carry the LIVE point/tick values.
    assert instruments.POOL["MNQ"].point_value == 2.0 and instruments.POOL["MNQ"].tick_value == 0.50
    assert instruments.POOL["MYM"].point_value == 0.50 and instruments.POOL["MYM"].tick_value == 0.50
    assert instruments.POOL["MES"].point_value == 5.0 and instruments.POOL["MES"].tick_value == 1.25
    assert instruments.POOL["MGC"].point_value == 10.0 and instruments.POOL["MGC"].tick_value == 1.00
    assert instruments.POOL["M2K"].point_value == 5.0 and instruments.POOL["M2K"].tick_value == 0.50


def test_mcl_m6a_tick_value_connecting_arithmetic():
    # Stage-1 map: RT 1t = 2 x $0.91 + tick_value  =>  $2.82 - $1.82 = $1.00 for MCL and M6A.
    assert instruments.POOL["MCL"].tick_value == 1.00
    assert instruments.POOL["M6A"].tick_value == 1.00
    # No committed point_value for these two -> None (pts column is UNSCREENABLE, cosmetic only).
    assert instruments.POOL["MCL"].point_value is None
    assert instruments.POOL["M6A"].point_value is None


def test_panel_ns_match_stage1_and_stage2():
    assert (instruments.POOL["MYM"].panel_n, instruments.POOL["MYM"].slot_n) == (484, 450)
    assert (instruments.POOL["M2K"].panel_n, instruments.POOL["M2K"].slot_n) == (484, 450)
    assert (instruments.POOL["MCL"].panel_n, instruments.POOL["MCL"].slot_n) == (251, 233)
    assert (instruments.POOL["M6A"].panel_n, instruments.POOL["M6A"].slot_n) == (484, 450)
    for sym in ("MNQ", "MES", "MGC"):
        assert instruments.POOL[sym].panel_n is None and instruments.POOL[sym].slot_n is None


def test_equity_index_rows_flagged_long_only():
    for sym in ("MNQ", "MYM", "MES", "M2K"):
        assert instruments.POOL[sym].long_only
    for sym in ("MGC", "MCL", "M6A"):
        assert not instruments.POOL[sym].long_only


import envelope  # noqa: E402
from envelope import LADDER_TICKS, FRONTIER_RISKS_USD  # noqa: E402


def test_ladder_reproduces_kwall_mnq_rows_at_bare_commission():
    # K-wall section 3 basis: commissions only ($0.95/side => $1.90 RT = 0.95 MNQ pts), slip=0.
    mnq = instruments.POOL["MNQ"]
    c5 = envelope.cell(mnq, stop_ticks=20, slip_ticks=0)   # 5 pt
    assert c5.stop_pts == 5.0 and c5.r_usd == 10.0
    assert round(c5.rt_usd, 2) == 1.90
    assert round(c5.cost_tax_r, 3) == 0.190                 # K-wall: 0.190R at 5 pt
    c2 = envelope.cell(mnq, stop_ticks=8, slip_ticks=0)     # 2 pt
    assert round(c2.cost_tax_r, 3) == 0.475                 # K-wall: 0.475R at 2 pt
    # Req-5 hurdle in pts: 4 x 0.95 pt = 3.80 pt, stop-independent.
    assert round(c5.req_delta_ticks * mnq.tick_value / mnq.point_value, 2) == 3.80
    assert c2.req_delta_ticks == c5.req_delta_ticks


def test_qty_matches_kwall_at_325_and_respects_cap():
    mnq = instruments.POOL["MNQ"]
    c5 = envelope.cell(mnq, stop_ticks=20, slip_ticks=0)
    assert c5.qty["0.85R(hyp)"] == 32                       # K-wall: 32.5 -> floor 32
    c2 = envelope.cell(mnq, stop_ticks=8, slip_ticks=0)
    assert c2.qty["0.85R(hyp)"] == 80                       # 81.25 capped at the 80-micro cap


def test_kill_predicates_fire_correctly():
    mnq = instruments.POOL["MNQ"]
    # K-COST: 2 pt cell at slip=0 needs 4x1.90/4.00 = 1.90R > 0.85R reference -> DEAD(cost).
    c2 = envelope.cell(mnq, stop_ticks=8, slip_ticks=0)
    assert c2.verdict == "DEAD" and c2.killed_by == "cost"
    # 20 pt cell: 4x1.90/40.00 = 0.19R <= 0.85R and qty >= 1 -> no kill.
    c20 = envelope.cell(mnq, stop_ticks=80, slip_ticks=0)
    assert c20.verdict in ("OPEN", "OPEN-CONDITIONAL(power)")


def test_negative_control_absurd_tick_value_is_all_dead():
    from instruments import Inst
    absurd = Inst("XXX", tick_value=500.0, point_value=None, group="Test",
                  long_only=False, panel_n=100, slot_n=None, source="synthetic")
    cells = [envelope.cell(absurd, t) for t in LADDER_TICKS]
    # risk $325 cannot buy 1 contract at any ladder stop (8 x $500 = $4,000 > $325) -> DEAD(qty).
    assert all(c.verdict == "DEAD" and c.killed_by == "qty" for c in cells)
    assert envelope.instrument_verdict(cells) == "EMPTY"


def test_power_floor_known_answers_and_unscreenable():
    mym = instruments.POOL["MYM"]
    assert round(envelope.cell(mym, 20).power_floor, 4) == 0.0891    # 1.96/sqrt(484)
    mnq = instruments.POOL["MNQ"]
    c = envelope.cell(mnq, 80)
    assert c.power_floor is None                                     # UNSCREENABLE-INPUT(panel_N)
    if c.verdict.startswith("OPEN"):
        assert c.verdict == "OPEN-CONDITIONAL(power)"


def test_dsr_floors_match_ratified_harness():
    floors = envelope.dsr_floors()
    assert [round(floors[k], 3) for k in (1, 2, 3)] == [0.650, 0.850, 0.980]


def test_self_check_asserts_kwall_boundary():
    envelope.self_check()  # must not raise: floor_at_k(3) <= CAP < floor_at_k(4)


def test_compile_all_shape_and_determinism():
    import run_envelope_compile as rec
    a, b = rec.compile_all(), rec.compile_all()
    assert a == b                                    # deterministic, no clocks/randomness
    assert set(a) == {"basis", "dsr_floors", "instruments", "h_a"}
    assert list(a["instruments"]) == list(instruments.POOL)
    assert a["h_a"] in ("NON-EMPTY", "EMPTY")
    for sym, block in a["instruments"].items():
        assert len(block["cells"]) == len(LADDER_TICKS)
        assert block["verdict"] in ("NON-EMPTY", "NON-EMPTY-CONDITIONAL(power)", "EMPTY")
        if block["verdict"].startswith("NON-EMPTY"):
            assert block["g0_numbers"]["req_delta_ticks"] > 0


def test_cli_compile_writes_results_json():
    out = subprocess.run(
        [sys.executable, "-X", "utf8",
         os.path.join(_DIR, "run_envelope_compile.py"), "--compile"],
        capture_output=True, text=True, check=True)
    assert "H_A:" in out.stdout
    with open(os.path.join(_DIR, "RESULTS.json"), encoding="utf-8") as f:
        assert json.load(f)["h_a"] in ("NON-EMPTY", "EMPTY")


def _entry(**kw):
    base = dict(name="t", instrument="MYM", stop_ticks=80, delta_ticks_per_event=40.0,
                delta_source="synthetic-fixture", events_per_year=250.0,
                horizon_seconds=3600.0, taxonomy_class="daily auction/settlement windows")
    base.update(kw)
    return base


def test_entry_seed_grade_when_all_walls_clear():
    import run_envelope_compile as rec
    v = rec.score_entry(_entry())     # MYM RT(1t,0.95)=$2.40 -> req delta 4x2.40/0.50 = 19.2 ticks; 40 clears
    assert v["verdict"] == "SEED-GRADE" and v["wall"] is None


def test_entry_fails_cost_wall():
    import run_envelope_compile as rec
    v = rec.score_entry(_entry(delta_ticks_per_event=5.0))       # below the 19.2-tick 4x hurdle
    assert (v["verdict"], v["wall"]) == ("FAIL", "cost")


def test_entry_fails_horizon_and_dead_cell():
    import run_envelope_compile as rec
    assert rec.score_entry(_entry(horizon_seconds=1.0))["wall"] == "horizon"      # < 5 s floor
    assert rec.score_entry(_entry(stop_ticks=8))["wall"] in ("cell", "cost")      # DEAD cell at 8 ticks


def test_entry_unscreenable_delta_routes_not_fails():
    import run_envelope_compile as rec
    v = rec.score_entry(_entry(delta_ticks_per_event=None))
    assert v["verdict"] == "UNSCREENABLE"
    assert "probe" in v["wall"]


def test_entry_unknown_instrument_is_unscreenable():
    import run_envelope_compile as rec
    v = rec.score_entry(_entry(instrument="ZZZ"))
    assert v["verdict"] == "UNSCREENABLE" and "unknown instrument" in v["wall"]


def test_entry_malformed_stop_ticks_is_unscreenable():
    import run_envelope_compile as rec
    v = rec.score_entry(_entry(stop_ticks=None))
    assert v["verdict"] == "UNSCREENABLE" and "stop_ticks" in v["wall"]
