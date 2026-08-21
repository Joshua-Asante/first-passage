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


# Q-SCORE-1 Block 1 undated residue still on disk under the frozen F3 grammar.
# Pin the filenames, not the date_coverage ratio: new *dated* closures raise the
# ratio without healing anyone (68/85 = 0.80 after Q-M1WIRE-1 tripped
# `date_coverage < 0.80` on every later lab/** CI run). This is not an H_A
# recount and does not authorize Block 2.
UNDATED_RESIDUE = frozenset({
    "2026-07-27-hermes-agent-adoption-closure-resolved.md",
    "2026-08-11-guardian-mgc-transfer-cell-dead-nsurv.md",
    "MNQBASE-1-closure-intake-dry.md",
    "Q-6JCOMPOSE-1-closure-void-unexecutable.md",
    "Q-6JCOMPOSE-2-closure-void-c2-red-gate-unreachable.md",
    "Q-ICT-1-closure-moot.md",
    "Q-JOINT-TAIL-WEEKLY-closure-retired.md",
    "Q-KBUDGET-1-axis-reachability-screen.md",
    "Q-KBUDGET-HARVEST-1-bounded-axis-literature-sweep.md",
    "Q-MCLTAS-1-closure-falsified.md",
    "Q-TNEC-CON-3-closure-ambiguous-hold.md",
    "Q-TNEC-CON-4-closure-ambiguous-hold.md",
    "Q-TNEC-CON-5-closure-ambiguous-hold.md",
    "Q-TNEC-ENV-1-closure.md",
    "Q-USOIL-1-closure-subtract.md",
    "Q-XMEM-1-closure-subtract.md",
    "ST-EH-1-closure-operator-stopped.md",
})


def test_design_time_coverage_floor_at_head():
    # Design §3: 13/50 = 74% at measurement time. HEAD may grow; the undated
    # residue must stay honest under the frozen grammar (never "fixed" by
    # broadening the regex). Healing = drop a name from UNDATED_RESIDUE after
    # a new campaign, not a silent Closed: edit or CLOSED_RE broaden.
    s = inventory_closed.summarize()
    assert s["n_closures"] >= 50
    assert s["n_without_closed"] >= 13
    assert UNDATED_RESIDUE <= set(s["without_closed"])


def test_concentration_rule_labels_recent_spread_when_applicable():
    s = inventory_closed.summarize()
    assert s["grandfather_concentration"] in {
        "grandfathered-majority", "recent-spread", "mixed"
    }
    # At the design-time corpus the undated recent share is 6/13 ≥ 40%.
    if s["n_without_closed"] == 13 and len(s["without_closed_recent"]) == 6:
        assert s["grandfather_concentration"] == "recent-spread"
