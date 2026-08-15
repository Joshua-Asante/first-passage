# lab/archive/approach_scoreboard_2026-08/test_inventory_closed.py
"""Campaign-local tests. Run from repo root:
   python -X utf8 -m pytest lab/archive/approach_scoreboard_2026-08/test_inventory_closed.py -v
"""
import os
import sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

import inventory_closed  # noqa: E402


def test_closed_grammar_rejects_explore_record_and_date_aliases():
    assert inventory_closed.has_machine_closed("**Closed:** 2026-08-10\n")
    assert inventory_closed.has_machine_closed("Closed: 2026-08-10\n")
    assert not inventory_closed.has_machine_closed("**Closed (explore record):** 2026-08-10\n")
    assert not inventory_closed.has_machine_closed("**Date:** 2026-08-04 · **Parent:** x\n")
    assert not inventory_closed.has_machine_closed("**Verdict:** `FALSIFIED` · 2026-08-11 · $0\n")


def test_design_time_coverage_floor_at_head():
    # Design §3: 13/50 = 74% at measurement time. HEAD may grow; coverage must stay
    # honest under the frozen grammar (never "fixed" by broadening the regex).
    s = inventory_closed.summarize()
    assert s["n_closures"] >= 50
    assert s["n_without_closed"] >= 13
    assert s["date_coverage"] < 0.80  # H_A date limb still fails unless corpus healed


def test_concentration_rule_labels_recent_spread_when_applicable():
    s = inventory_closed.summarize()
    assert s["grandfather_concentration"] in {
        "grandfathered-majority", "recent-spread", "mixed"
    }
    # At the design-time corpus the undated recent share is 6/13 ≥ 40%.
    if s["n_without_closed"] == 13 and len(s["without_closed_recent"]) == 6:
        assert s["grandfather_concentration"] == "recent-spread"
