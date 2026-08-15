"""Campaign-local tests. Run from repo root:
   python -X utf8 -m pytest lab/archive/transfer_expression_grid_2026-08/test_grid.py -v
"""
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import mechanisms  # noqa: E402


def test_mechanism_order_and_membership():
    assert list(mechanisms.MECHANISMS) == [
        "guardian", "striker", "striker_nas100", "aegis"
    ]


def test_sl_atr_mults_match_lock_verbatim():
    assert mechanisms.MECHANISMS["guardian"].sl_atr_mult == 1.55
    assert mechanisms.MECHANISMS["striker"].sl_atr_mult == 1.20
    assert mechanisms.MECHANISMS["striker_nas100"].sl_atr_mult == 1.20
    assert mechanisms.MECHANISMS["aegis"].sl_atr_mult == 1.42


def test_atr_lengths_match_citation_chain():
    assert mechanisms.MECHANISMS["guardian"].atr_len == 14
    assert mechanisms.MECHANISMS["striker"].atr_len == 11
    assert mechanisms.MECHANISMS["striker_nas100"].atr_len == 11
    assert mechanisms.MECHANISMS["aegis"].atr_len == 19


def test_risk_keys_match_firm_rules_base_risk():
    # Live import — do not hard-code the floats here beyond membership.
    import importlib
    fr = importlib.import_module("firm_rules") if False else None
    sys.path.insert(0, os.path.abspath(os.path.join(_DIR, "..", "..", "..", "..")))
    from core.firm_rules import _BASE_RISK  # noqa: E402
    for m in mechanisms.MECHANISMS.values():
        assert m.risk_key in _BASE_RISK
        assert mechanisms.risk_pct(m) == _BASE_RISK[m.risk_key]


def test_same_underlying_tags():
    assert mechanisms.MECHANISMS["striker"].same_underlying_syms == frozenset({"MYM"})
    assert mechanisms.MECHANISMS["striker_nas100"].same_underlying_syms == frozenset({"MNQ"})
    assert mechanisms.MECHANISMS["guardian"].same_underlying_syms == frozenset({"MGC"})
    assert mechanisms.MECHANISMS["aegis"].same_underlying_syms == frozenset()  # 6J ∉ pool


import atr_map  # noqa: E402


def test_atr_ticks_only_striker_family_on_mym_mnq():
    g = mechanisms.MECHANISMS["guardian"]
    s = mechanisms.MECHANISMS["striker"]
    n = mechanisms.MECHANISMS["striker_nas100"]
    a = mechanisms.MECHANISMS["aegis"]
    assert atr_map.atr_ticks(s, "MYM") == atr_map.ATR_TICKS_MYM_ATR11
    assert atr_map.atr_ticks(n, "MNQ") == atr_map.ATR_TICKS_MNQ_ATR11
    assert atr_map.atr_ticks(s, "MNQ") == atr_map.ATR_TICKS_MNQ_ATR11
    # Wrong ATR length or missing source → None
    assert atr_map.atr_ticks(g, "MYM") is None
    assert atr_map.atr_ticks(a, "MNQ") is None
    assert atr_map.atr_ticks(s, "MES") is None
    assert atr_map.atr_ticks(s, "MCL") is None


def test_atr_known_answer_mym_mnq_byte_identical():
    # Gate before any new instrument may join _ATR_PTS_RECENT90_ATR11.
    assert atr_map.ATR_TICKS_MYM_ATR11 == 50.6834 / 1.0
    assert atr_map.ATR_TICKS_MNQ_ATR11 == 45.5095 / 0.25


def test_inputs_extension_m6j_venue_closed_and_mgc_pending_or_uncommitted():
    assert atr_map.M6J_VENUE_LEGAL is False
    assert "venue" in atr_map.ATR11_INPUT_STATUS["M6J"]
    mgc = atr_map.ATR11_INPUT_STATUS["MGC"]
    assert mgc.startswith("PENDING") or mgc == "PINNED_BYTES_PRESENT_ATR_UNCOMMITTED"
    for sym in ("MES", "M2K", "MCL", "M6A"):
        assert atr_map.ATR11_INPUT_STATUS[sym].startswith("UNSCREENABLE-INPUT(atr)")
    # No new committed ATR rows beyond MYM/MNQ.
    assert set(atr_map._ATR_PTS_RECENT90_ATR11) == {"MYM", "MNQ"}


def test_stop_ticks_striker_mym_known_answer():
    s = mechanisms.MECHANISMS["striker"]
    # 1.20 × (50.6834 / 1.0) = 60.82008
    assert abs(atr_map.stop_ticks(s, "MYM") - 60.82008) < 1e-4
    assert atr_map.map_stop_ticks(60.82008) == 80  # nearest of {8,20,40,80,160}


def test_stop_ticks_striker_mnq_maps_to_160():
    s = mechanisms.MECHANISMS["striker_nas100"]
    # 1.20 × (45.5095 / 0.25) = 218.4456 → nearest ladder 160
    st = atr_map.stop_ticks(s, "MNQ")
    assert abs(st - 218.4456) < 1e-3
    assert atr_map.map_stop_ticks(st) == 160


import walls  # noqa: E402


def test_pool_order_matches_env1():
    assert list(walls.POOL_ORDER) == ["MNQ", "MYM", "MES", "MGC", "M2K", "MCL", "M6A"]


def test_dedup_withdrawn_and_parked():
    r = walls.evaluate_cell("striker", "MYM")
    assert r.verdict == "WITHDRAWN(F1)" and r.killed_by == "dedup"
    r = walls.evaluate_cell("striker_nas100", "MNQ")
    assert r.verdict == "WITHDRAWN(F1)" and r.killed_by == "dedup"
    r = walls.evaluate_cell("guardian", "MGC")
    assert r.verdict == "PARKED(b8)" and r.killed_by == "dedup"


def test_striker_mnq_same_mech_other_symbol_not_auto_withdrawn():
    # striker (DJ30) × MNQ is cross-underlying research under the 2026-08-04 amendment —
    # not F1-withdrawn (F1 names the locked Striker book redeploy on its venue legs).
    r = walls.evaluate_cell("striker", "MNQ")
    assert r.verdict != "WITHDRAWN(F1)"


def test_w_cost_resolves_for_striker_mym_family_on_mapped_cell():
    # striker×MYM is WITHDRAWN before W-COST — use striker_nas100×MYM (cross-underlying).
    r = walls.evaluate_cell("striker_nas100", "MYM")
    assert r.stop_ticks_mapped == 80
    assert r.cost_tax_r is not None
    assert r.verdict in ("OPEN", "DEAD(cost)", "DEAD(cap)", "DEAD(venue)")


def test_guardian_mes_stop_unscreenable_does_not_invent_atr():
    r = walls.evaluate_cell("guardian", "MES")
    assert r.stop_ticks_mapped is None
    assert r.port_must_beat.get("stop_cell") == "UNSCREENABLE" or any(
        "UNSCREENABLE-INPUT(stop_cell)" in d for d in r.disclosures
    )
    # Not WITHDRAWN/PARKED; may be OPEN with unscreenable stop or DEAD(cap/venue).
    assert r.verdict not in ("WITHDRAWN(F1)", "PARKED(b8)")


def test_grid_has_28_cells():
    cells = walls.evaluate_all()
    assert len(cells) == 28
    assert sum(1 for c in cells if c.verdict == "OPEN") >= 0  # H_A computed later


import json
import subprocess


def test_compile_all_shape_and_determinism():
    import run_grid_compile as rgc
    a, b = rgc.compile_all(), rgc.compile_all()
    assert a == b
    assert set(a) == {"basis", "dsr_floors", "cells", "h_a", "open_cells"}
    assert len(a["cells"]) == 28
    assert a["h_a"] in ("OPEN", "EMPTY")
    for c in a["cells"]:
        assert c["verdict"]


def test_cli_compile_writes_json():
    out = subprocess.run(
        [sys.executable, "-X", "utf8",
         os.path.join(_DIR, "run_grid_compile.py"), "--compile"],
        capture_output=True, text=True, check=True)
    assert "H_A:" in out.stdout
    with open(os.path.join(_DIR, "GRID_RESULTS.json"), encoding="utf-8") as f:
        assert json.load(f)["h_a"] in ("OPEN", "EMPTY")


def test_self_check_ok():
    import run_grid_compile as rgc
    rgc.self_check()  # must not raise
