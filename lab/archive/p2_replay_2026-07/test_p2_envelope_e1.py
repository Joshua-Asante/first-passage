"""Fixture tests — E1 envelope module. Exits-only P&L (Q-A1-c double-count
trap), explicit-window filtering (no hardcoded dates), identical-window
enforcement, ill-conditioned-baseline hard errors, and explicit-floor
scoring. All synthetic — no vendor data.

Full-window fixture arithmetic (pep_diff_new / cme_diff_new):
  pep: wins 100+100+80+40=320, loss -50  -> PF 6.4,     net 270, n 5
  cme: wins 100+25+90+30=245,  loss -60  -> PF 4.08333, net 185, n 5
  pf_ratio  = 4.08333/6.4 = 0.638021
  net_ratio = 185/270     = 0.685185
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from p2_ingest import NeedsContextError, load_export  # noqa: E402
import p2_envelope_e1 as env  # noqa: E402

FIX = _HERE / "fixtures"

WSTART, WEND = "2026-06-01", "2026-07-01"   # explicit test window, ET


def test_pf_net_is_exits_only():
    """Entry rows carry Net PnL 0 here, but the loader must not need that:
    counting exits only is the convention (Q-A1-c). Net 270 / PF 6.4 / n 5."""
    m = env.pf_net(load_export(FIX / "pep_diff_new.csv"))
    assert m.n_trades == 5
    assert m.net == pytest.approx(270.0)
    assert m.pf == pytest.approx(6.4)


def test_pyramid_leg_pnl_counted_once_legacy():
    m = env.pf_net(load_export(FIX / "dj30_pyramid_legacy.csv"))
    assert m.n_trades == 2
    assert m.net == pytest.approx(5000.0)   # 5500 (multi-leg trade 1) - 500
    assert m.pf == pytest.approx(11.0)


def test_window_filter_by_first_entry_keeps_whole_trade():
    df = env.filter_window(load_export(FIX / "pep_diff_new.csv"),
                           "2026-06-10", "2026-06-16")
    m = env.pf_net(df)
    assert m.n_trades == 2          # trades 2 (06-10) and 3 (06-12)
    assert m.net == pytest.approx(50.0)


def test_window_bounds_are_required_and_validated():
    df = load_export(FIX / "pep_diff_new.csv")
    with pytest.raises(TypeError):
        env.filter_window(df)       # no default window exists anywhere
    with pytest.raises(NeedsContextError):
        env.filter_window(df, "2026-06-16", "2026-06-10")


def test_e1_ratios_full_window():
    r = env.e1_ratios("dj30",
                      load_export(FIX / "pep_diff_new.csv"),
                      load_export(FIX / "cme_diff_new.csv"),
                      WSTART, WEND)
    assert r.pep.pf == pytest.approx(6.4)
    assert r.cme.pf == pytest.approx(245 / 60)
    assert r.pf_ratio == pytest.approx((245 / 60) / 6.4, abs=1e-9)
    assert r.net_ratio == pytest.approx(185 / 270, abs=1e-9)


def test_e1_applies_identical_window_to_both_sides():
    """Both frames are filtered inside e1_ratios with the same bounds (§7:
    ratios computed on identical windows)."""
    r = env.e1_ratios("dj30",
                      load_export(FIX / "pep_diff_new.csv"),
                      load_export(FIX / "cme_diff_new.csv"),
                      "2026-06-10", "2026-06-16")
    assert r.pep.net == pytest.approx(50.0)     # pep trades 2,3
    assert r.cme.net == pytest.approx(-35.0)    # cme trades 2,3
    assert r.net_ratio == pytest.approx(-0.7)


def test_nonpositive_baseline_net_needs_context():
    """A non-positive Pepperstone baseline net makes the net ratio
    ill-defined — hard error, not a silent verdict (swap sides so the
    baseline nets -35 on the narrow window)."""
    with pytest.raises(NeedsContextError):
        env.e1_ratios("dj30",
                      load_export(FIX / "cme_diff_new.csv"),
                      load_export(FIX / "pep_diff_new.csv"),
                      "2026-06-10", "2026-06-16")


def test_zero_loss_pf_is_refused(tmp_path):
    """Zero-loss cohort -> PF infinite -> ratio ill-conditioned (PF-spike
    lesson): hard error."""
    header = ("Trade number,Type,Date and time,Signal,Price USD,Size (qty),"
              "Size (value),Net PnL USD,Net PnL %,Favorable excursion USD,"
              "Favorable excursion %,Adverse excursion USD,Adverse excursion %,"
              "Cumulative PnL USD,Cumulative PnL %")
    rows = [
        "1,Entry long,2026-06-09 10:00,Long,100,1,100,0,0,0,0,0,0,0,0",
        "1,Exit long,2026-06-09 11:00,Exit Long,103,1,103,3,1.5,4,2,0,0,3,1.5",
    ]
    p = tmp_path / "all_wins.csv"
    p.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
    with pytest.raises(NeedsContextError):
        env.pf_net(load_export(p))


def test_score_e1_takes_explicit_floors_only():
    r = env.e1_ratios("dj30",
                      load_export(FIX / "pep_diff_new.csv"),
                      load_export(FIX / "cme_diff_new.csv"),
                      WSTART, WEND)
    # synthetic-fixture unit check of the scorer, NOT a Phase-B scoring run
    assert env.score_e1(r, pf_floor=0.8, net_floor=0.7) == "MISS-AMBIGUOUS"
    assert env.score_e1(r, pf_floor=0.5, net_floor=0.5) == "PASS"
    with pytest.raises(TypeError):
        env.score_e1(r)  # no default floors exist ([RATIFY]-pending)
