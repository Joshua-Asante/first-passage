"""Fixture tests — tolerant-pairing K2 diff module (Q-P2-MEASURE-1).

Scenario (ET, 2026-06-09 — no roll seams in window, isolates pairing logic
from ROLL-SEAM/SESSION classification, which the frozen module already
covers in test_p2_diff_k2.py). Groups are spaced >=75 minutes apart (far
beyond the 30-minute/2-bar tolerance) so no cross-group match is possible —
an earlier draft with 15-minute inter-group gaps produced an unintended
cross-group collapse (B's cme-only signal matched C's pep-only signal,
both "long" and 15 minutes apart), caught by the fixture's own arithmetic
assertions failing. Widened spacing here removes that degree of freedom.

  A: pep long 10:00 / cme long 10:30  — exactly 2 bars (30m) apart, SAME
     direction -> WITHIN tolerance -> COLLAPSES to 1 agree event.
  B: pep long 12:00 / cme long 12:45  — 3 bars (45m) apart, SAME direction
     -> BEYOND tolerance -> stays 2 divergences (pep-only + cme-only).
  C: pep long 14:00 / cme SHORT 14:15 — 1 bar apart but OPPOSITE direction
     -> direction mismatch -> stays 2 divergences (never collapses).
  D: both long 16:00 (exact match)    -> agree (both_ts path, untouched).
  E: pep long / cme short, both 18:00 (exact match) -> direction-flip,
     BASIS -> untouched by tolerance (only unmatched-timestamp pairs are
     eligible for collapse; a same-bar disagreement never launders into
     agreement — brief Sec5 forbidden move).

Hand-computed at tolerance=2 bars (30 min):
  both_ts={16:00,18:00}: 16:00 agree, 18:00 direction-flip (divergent)
  collapse: A matches (10:00,10:30) -> 1 agree event
  no match: B (12:00,12:45 — 45m > 30m), C (14:00 long vs 14:15 short — dir mismatch)
  n_agree = 1(D) + 1(A collapsed) = 2
  n_divergent = 1(E) + 2(B: pep-only 12:00, cme-only 12:45) + 2(C: pep-only 14:00, cme-only 14:15) = 5
  n_union = 2(both_ts) + 1(collapsed) + 2(still pep-only: B,C) + 2(still cme-only: B,C) = 7
  pct_with_roll = 100*5/7 = 71.428571...%

Hand-computed at tolerance=0 (seeded-defect invariant — must equal the
FROZEN p2_diff_k2.k2_report on the identical inputs, since A's 30-minute gap
can never satisfy `abs(delta) <= 0`):
  union = {10:00,10:30,12:00,12:45,14:00,14:15,16:00,18:00} = 8
  agree = 1 (16:00 only) ; divergent = 7 (6 only's + 1 flip)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from p2_ingest import extract_signals, load_export, to_et_boundary as et  # noqa: E402
import p2_diff_k2 as base  # noqa: E402
import p2_diff_k2_tolerant as tol  # noqa: E402

FIX = _HERE / "fixtures"

T_A_PEP, T_A_CME = et("2026-06-09 10:00"), et("2026-06-09 10:30")
T_B_PEP, T_B_CME = et("2026-06-09 12:00"), et("2026-06-09 12:45")
T_C_PEP, T_C_CME = et("2026-06-09 14:00"), et("2026-06-09 14:15")
T_D = et("2026-06-09 16:00")
T_E = et("2026-06-09 18:00")

ALL_TS = {T_A_PEP, T_A_CME, T_B_PEP, T_B_CME, T_C_PEP, T_C_CME, T_D, T_E}


def _signals():
    sig_pep = extract_signals(load_export(FIX / "pep_tolerant.csv"))
    sig_cme = extract_signals(load_export(FIX / "cme_tolerant.csv"))
    return sig_pep, sig_cme


def _tolerant_report(tolerance_bars=2):
    sig_pep, sig_cme = _signals()
    return tol.k2_report_tolerant("dj30", sig_pep, sig_cme, [], ALL_TS, ALL_TS,
                                   tolerance_bars=tolerance_bars)


def _frozen_report():
    sig_pep, sig_cme = _signals()
    return base.k2_report("dj30", sig_pep, sig_cme, [], ALL_TS, ALL_TS)


# --- tolerance=2 (the frozen default, TOLERANT_BAR_WINDOW) -------------------

def test_within_tolerance_same_direction_collapses():
    r = _tolerant_report(tolerance_bars=2)
    by_ts = {d.ts for d in r.divergences}
    assert T_A_PEP not in by_ts and T_A_CME not in by_ts  # collapsed away


def test_beyond_tolerance_stays_divergent():
    r = _tolerant_report(tolerance_bars=2)
    by_ts = {d.ts: d.kind for d in r.divergences}
    assert by_ts[T_B_PEP] == "pep-only"
    assert by_ts[T_B_CME] == "cme-only"


def test_direction_mismatch_never_collapses_even_within_tolerance():
    r = _tolerant_report(tolerance_bars=2)
    by_ts = {d.ts: d.kind for d in r.divergences}
    assert by_ts[T_C_PEP] == "pep-only"
    assert by_ts[T_C_CME] == "cme-only"


def test_exact_match_direction_flip_untouched_by_tolerance():
    r = _tolerant_report(tolerance_bars=2)
    by_ts = {d.ts: d.kind for d in r.divergences}
    assert by_ts[T_E] == "direction-flip"


def test_counts_at_tolerance_2():
    r = _tolerant_report(tolerance_bars=2)
    assert r.n_union == 7
    assert r.n_agree == 2
    assert r.n_divergent == 5
    assert r.pct_with_roll == pytest.approx(100 * 5 / 7, abs=1e-6)


def test_taxonomy_sums_to_total():
    r = _tolerant_report(tolerance_bars=2)
    assert sum(r.cause_counts.values()) == r.n_divergent


# --- seeded-defect invariant: tolerance=0 reduces EXACTLY to the frozen harness --

def test_tolerance_zero_reduces_to_frozen_harness():
    """The module's entire justification rests on this: at tolerance=0 it
    must be indistinguishable from p2_diff_k2.k2_report, because pep_only
    and cme_only are constructed as set differences and can never share an
    element (no delta can satisfy <= a zero window). If this test fails, the
    module is a DIFFERENT instrument, not a generalization, and Q-P2-MEASURE-1
    Sec7's Phase-1 gate is not met."""
    tolerant_zero = _tolerant_report(tolerance_bars=0)
    frozen = _frozen_report()
    assert tolerant_zero.n_union == frozen.n_union == 8
    assert tolerant_zero.n_agree == frozen.n_agree == 1
    assert tolerant_zero.n_divergent == frozen.n_divergent == 7
    assert tolerant_zero.cause_counts == frozen.cause_counts
    assert {d.ts for d in tolerant_zero.divergences} == {d.ts for d in frozen.divergences}


def test_tolerance_zero_matches_published_phase_b_shape():
    """Sanity: at tolerance=0, A no longer collapses (30-min gap > 0), so all
    three pairs (A,B,C) contribute 2 divergent members each, same shape as
    the frozen harness's exact-timestamp counting."""
    r = _tolerant_report(tolerance_bars=0)
    by_ts = {d.ts: d.kind for d in r.divergences}
    assert by_ts[T_A_PEP] == "pep-only" and by_ts[T_A_CME] == "cme-only"


# --- hard errors (never guess) -----------------------------------------------

def test_empty_union_needs_context():
    with pytest.raises(base.NeedsContextError):
        tol.k2_report_tolerant("dj30", [], [], [], ALL_TS, ALL_TS)


# --- frozen module and scoring are genuinely reused, not reimplemented ------

def test_score_k2_reused_unmodified():
    r = _tolerant_report(tolerance_bars=2)
    # 5/7 = 71.43% > 10% -> KILL either way; confirms base.score_k2 is called
    # against the tolerant report's own counts, not a copy-pasted scorer.
    assert base.score_k2(r, kill_threshold_pct=10.0, treatment="with-roll") == "KILL"
    assert base.score_k2(r, kill_threshold_pct=75.0, treatment="with-roll") == "PASS"
