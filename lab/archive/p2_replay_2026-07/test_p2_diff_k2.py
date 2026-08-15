"""Fixture tests — K2 diff module. One synthetic fixture per divergence class
(ROLL-SEAM / SESSION / BASIS / DATA-GAP), the roll_mask reuse path, the
missing-bar-context hard error, and the pyramid-add pairing case under the
current TV schema. All synthetic — no vendor data.

Scenario (ET, June 2026 — inside the quarterly roll window so the seam case
is exercised through the real roll_mask calendar):

  T1 2026-06-09 10:00  both fire long          -> agree
  T2 2026-06-10 09:30  pep-only; seam @ 09:45  -> ROLL-SEAM (1 bar away)
  T3 2026-06-11 18:15  cme-only; bar cme-only  -> SESSION
  T4 2026-06-12 10:00  pep-only; both bars     -> BASIS
  T5 2026-06-15 11:30  cme-only; bar neither   -> DATA-GAP
  T6 2026-06-16 14:00  both fire long          -> agree
  T7 2026-06-16 15:00  pep long / cme short    -> direction-flip -> BASIS

  union 7, agree 2, divergent 5
  with-roll 5/7 = 71.43% ; ex-roll 4/6 = 66.67%
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from p2_ingest import (  # noqa: E402
    GridAlignmentError,
    NeedsContextError,
    Signal,
    extract_signals,
    load_export,
    to_et_boundary as et,
)
import p2_diff_k2 as diff  # noqa: E402

FIX = _HERE / "fixtures"

T1, T2, T3 = et("2026-06-09 10:00"), et("2026-06-10 09:30"), et("2026-06-11 18:15")
T4, T5 = et("2026-06-12 10:00"), et("2026-06-15 11:30")
T6, T7 = et("2026-06-16 14:00"), et("2026-06-16 15:00")

#: Bar-existence indexes (classification aid): T3 exists on CME only
#: (SESSION), T5 on neither (DATA-GAP), everything else on both.
BARS_PEP = {T1, T2, T4, T6, T7}
BARS_CME = {T1, T2, T3, T4, T6, T7}


def _seam_panel() -> pd.DataFrame:
    """Synthetic CME continuous panel with one roll seam: 0.72% overnight-gap
    bar at 2026-06-10 13:45Z (= 09:45 ET), inside roll_mask's quarterly June
    window."""
    return pd.DataFrame({
        "time": ["2026-06-10T13:15:00Z", "2026-06-10T13:30:00Z",
                 "2026-06-10T13:45:00Z"],
        "open": [40000.0, 40012.0, 40300.0],
        "close": [40010.0, 40010.0, 40310.0],
    })


def _report() -> diff.K2Report:
    sig_pep = extract_signals(load_export(FIX / "pep_diff_new.csv"))
    sig_cme = extract_signals(load_export(FIX / "cme_diff_new.csv"))
    seams = diff.seam_timestamps_from_bars(_seam_panel(), "MYM1!")
    return diff.k2_report("dj30", sig_pep, sig_cme, seams, BARS_PEP, BARS_CME)


# --- roll_mask reuse ---------------------------------------------------------

def test_seam_wrapper_reuses_roll_mask_calendar():
    seams = diff.seam_timestamps_from_bars(_seam_panel(), "MYM1!")
    assert seams == [et("2026-06-10 09:45")]


def test_unknown_symbol_needs_context():
    with pytest.raises(NeedsContextError):
        diff.seam_timestamps_from_bars(_seam_panel(), "ES1!")


# --- the four divergence classes --------------------------------------------

def test_union_agree_divergent_counts():
    r = _report()
    assert r.n_union == 7
    assert r.n_agree == 2
    assert r.n_divergent == 5


def test_taxonomy_one_fixture_per_class_and_sums_to_total():
    r = _report()
    assert r.cause_counts == {"ROLL-SEAM": 1, "SESSION": 1, "BASIS": 2, "DATA-GAP": 1}
    assert sum(r.cause_counts.values()) == r.n_divergent  # §7 quality check


def test_each_divergent_signal_classified_as_designed():
    r = _report()
    by_ts = {d.ts: (d.kind, d.cause) for d in r.divergences}
    assert by_ts[T2] == ("pep-only", "ROLL-SEAM")
    assert by_ts[T3] == ("cme-only", "SESSION")
    assert by_ts[T4] == ("pep-only", "BASIS")
    assert by_ts[T5] == ("cme-only", "DATA-GAP")
    assert by_ts[T7] == ("direction-flip", "BASIS")


def test_both_roll_treatments_emitted():
    r = _report()
    assert r.pct_with_roll == pytest.approx(100 * 5 / 7, abs=1e-6)
    assert r.pct_ex_roll == pytest.approx(100 * 4 / 6, abs=1e-6)
    out = diff.format_report(r)
    assert "with-roll" in out and "ex-roll" in out  # §0.5-c: both, always


# --- hard errors (never guess) ----------------------------------------------

def test_missing_bar_index_needs_context():
    with pytest.raises(NeedsContextError):
        diff.classify_divergence(T4, [], None, BARS_CME)


def test_empty_union_needs_context():
    with pytest.raises(NeedsContextError):
        diff.k2_report("dj30", [], [], [], BARS_PEP, BARS_CME)


def test_off_grid_signal_rejected_before_pairing():
    bad = [Signal(ts=et("2026-06-09 10:07"), direction="long",
                  is_add=False, trade_no=1)]
    with pytest.raises(GridAlignmentError):
        diff.k2_report("dj30", bad, bad, [], BARS_PEP, BARS_CME)


# --- pyramid-add pairing under the current schema ----------------------------

def test_pyramid_add_pairing_current_schema():
    """Pepperstone has base + 'Long Add' leg; CME has base only. The add is a
    signal in its own right: union 2, one divergence at the add timestamp."""
    sig_pep = extract_signals(load_export(FIX / "pep_pyramid_new.csv"))
    sig_cme = extract_signals(load_export(FIX / "cme_pyramid_new.csv"))
    t_base, t_add = et("2026-06-09 10:00"), et("2026-06-09 11:30")
    r = diff.k2_report("nas100", sig_pep, sig_cme, [],
                       {t_base, t_add}, {t_base, t_add})
    assert r.n_union == 2 and r.n_agree == 1 and r.n_divergent == 1
    d = r.divergences[0]
    assert (d.ts, d.kind, d.cause) == (t_add, "pep-only", "BASIS")


# --- scoring requires an explicit (ratified) threshold ------------------------

def test_score_k2_takes_explicit_threshold_only():
    r = _report()
    # synthetic-fixture unit check of the scorer, NOT a Phase-B scoring run
    assert diff.score_k2(r, kill_threshold_pct=10.0, treatment="with-roll") == "KILL"
    assert diff.score_k2(r, kill_threshold_pct=75.0, treatment="with-roll") == "PASS"
    assert diff.score_k2(r, kill_threshold_pct=70.0, treatment="ex-roll") == "PASS"
    with pytest.raises(TypeError):
        diff.score_k2(r)  # no default threshold exists ([RATIFY]-pending)
    with pytest.raises(ValueError):
        diff.score_k2(r, kill_threshold_pct=10.0, treatment="rolls-excluded")
